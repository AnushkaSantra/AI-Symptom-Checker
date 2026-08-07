"use strict";

window.addEventListener('submit', function(e){
    if(e.target && e.target.id === "appointmentForm"){ return; }
    e.preventDefault();
    e.stopImmediatePropagation();
    return false;
}, true);

let latestPrediction = null;
let predictionChart = null;
var FLASK_BASE_URL = "";
var BASE = "";

function escapeHTML(v){
    if(v==null) return "";
    var d=document.createElement("div");
    d.textContent=String(v);
    return d.innerHTML;
}
async function fetchWithTimeout(url, opt, t){
    if(!opt) opt={};
    if(!t) t=30000;
    var c=new AbortController();
    var id=setTimeout(function(){ c.abort(); }, t);
    try{ opt.signal=c.signal; return await fetch(url, opt); }
    finally{ clearTimeout(id); }
}
async function parseJSONResponse(res,name){
    var txt=await res.text();
    if(!txt.trim()) throw new Error(name+" empty");
    try{ return JSON.parse(txt); } catch(e){ throw new Error(name+" invalid JSON"); }
}
function showPredictionMessage(title,msg){
    var el=document.getElementById("predictionContent");
    if(el) el.innerHTML='<div class="welcome-box"><h3>'+escapeHTML(title)+'</h3><p>'+msg+'</p></div>';
}
function getSeverityColor(s){
    if(!s) return "#0b74de";
    var t=String(s).toLowerCase();
    if(t.indexOf("low")!==-1) return "#28a745";
    if(t.indexOf("moderate")!==-1 || t.indexOf("medium")!==-1) return "#ff9800";
    if(t.indexOf("high")!==-1 || t.indexOf("critical")!==-1 || t.indexOf("severe")!==-1) return "#dc3545";
    return "#0b74de";
}
function getSelectedSymptoms(){
    return Array.from(document.querySelectorAll("#symptoms input:checked")).map(function(c){ return c.value; }).filter(Boolean);
}
function searchSymptoms(){
    var searchEl=document.getElementById("search");
    var v=searchEl? searchEl.value.toLowerCase() : "";
    document.querySelectorAll("#symptoms.symptom-item").forEach(function(el){
        el.style.display=el.textContent.toLowerCase().indexOf(v)!==-1?"flex":"none";
    });
}
async function loadSymptoms(){
    var box=document.getElementById("symptoms");
    if(!box) return;
    try{
        var r=await fetchWithTimeout(FLASK_BASE_URL+"/symptoms",{headers:{Accept:"application/json"}});
        var data=await parseJSONResponse(r,"Symptoms");
        box.innerHTML="";
        var uniq=[...new Set(data.filter(Boolean).map(function(s){ return String(s).trim(); }))].sort(function(a,b){ return a.localeCompare(b); });
        uniq.forEach(function(s){
            var lab=document.createElement("label"); lab.className="symptom-item";
            var cb=document.createElement("input"); cb.type="checkbox"; cb.value=s;
            lab.appendChild(cb);
            lab.appendChild(document.createTextNode(" "+s.replace(/_/g," ")));
            box.appendChild(lab);
        });
    }catch(e){
        box.innerHTML='<div class="symptoms-error">❌ '+escapeHTML(e.message)+'</div>';
    }
}
function createProbHTML(preds,res){
    var main=res["Predicted Disease"]||"Unknown";
    var mainP=Math.max(0,Math.min(Number(res.Confidence)||0,100));
    var h='<div class="main-probability"><div class="probability-disease">'+escapeHTML(main)+'</div><div class="probability-value">'+mainP.toFixed(2)+'%</div></div>';
    preds.forEach(function(it,i){
        if(String(it.Disease).toLowerCase()===main.toLowerCase()) return;
        var p=Math.max(0,Math.min(Number(it.Confidence)||0,100));
        h+='<div class="side-probability-item"><div class="side-probability-name">'+(i+1)+'. '+escapeHTML(it.Disease)+'</div><div class="side-probability-bar"><div class="side-probability-fill" style="width:'+p+'%"></div></div><div class="side-probability-percent">'+p.toFixed(2)+'%</div></div>';
    });
    return h;
}
async function predictDisease(e){
    if(e){ e.preventDefault(); e.stopPropagation(); e.stopImmediatePropagation(); }
    var nameEl=document.getElementById("patientName");
    var ageEl=document.getElementById("patientAge");
    var genderEl=document.getElementById("patientGender");
    var name=nameEl? nameEl.value.trim() : "";
    var ageRaw=ageEl? ageEl.value.trim() : "";
    var gender=genderEl? genderEl.value : "";
    if(!name||!ageRaw||!gender){ showPredictionMessage("⚠ Required","Enter Name, Age, Gender"); return false; }
    var age=Number(ageRaw);
    if(!Number.isFinite(age)||age<0||age>120){ showPredictionMessage("⚠ Invalid Age","0-120"); return false; }
    var sel=getSelectedSymptoms();
    if(sel.length===0){ showPredictionMessage("⚠ No Symptoms","Select at least 1"); return false; }
    showPredictionMessage("🔄 Predicting...","AI analysing...");
    try{
        var r=await fetchWithTimeout(FLASK_BASE_URL+"/predict",{
            method:"POST", headers:{"Content-Type":"application/json","Accept":"application/json"},
            body:JSON.stringify({symptoms:sel, patientName:name, patientAge:age, patientGender:gender})
        });
        var result=await parseJSONResponse(r,"Predict");
        if(!r.ok) throw new Error(result.error||("HTTP "+r.status));
        if(!result["Predicted Disease"]) throw new Error("No disease returned");
        latestPrediction=result;
        latestPrediction.patientName=name; latestPrediction.patientAge=age; latestPrediction.patientGender=gender;
        var cardPatient=document.getElementById("cardPatient");
        var cardDisease=document.getElementById("cardDisease");
        var cardConf=document.getElementById("cardConfidence");
        var cardSev=document.getElementById("cardSeverity");
        if(cardPatient) cardPatient.textContent=name;
        if(cardDisease) cardDisease.textContent=result["Predicted Disease"];
        if(cardConf) cardConf.textContent=Number(result.Confidence||0).toFixed(2)+"%";
        if(cardSev) cardSev.textContent=result.Severity||"Unknown";

        var docSelect=document.getElementById("appointmentDoctor");
        if(docSelect && result.Doctor){
            var exists=false;
            for(var i=0;i<docSelect.options.length;i++){ if(docSelect.options[i].value===result.Doctor) exists=true; }
            if(!exists){
                var newOpt=document.createElement("option");
                newOpt.value=result.Doctor; newOpt.textContent=result.Doctor;
                docSelect.appendChild(newOpt);
            }
            docSelect.value=result.Doctor;
        }

        var top=result["Top Predictions"]||[];
        // === FIXED SIDE BY SIDE - ADDED MISSING </div> ===
        var html=''+
            '<div class="prediction-layout">'+
                '<div class="prediction-result-area">'+
                    '<div class="result-card">'+
                        '<h2>🩺 '+escapeHTML(result["Predicted Disease"])+'</h2>'+
                        '<div class="confidence-box">Confidence: <strong>'+Number(result.Confidence||0).toFixed(2)+'%</strong></div>'+
                        '<hr><h3>Description</h3><p>'+escapeHTML(result.Description||"")+'</p>'+
                        '<hr><h3>Severity</h3><div class="severity-badge" style="background:'+getSeverityColor(result.Severity)+';color:#fff">'+escapeHTML(result.Severity||"Unknown")+'</div>'+
                        '<hr><h3>Doctor</h3><p>'+escapeHTML(result.Doctor||"")+'</p>'+
                        '<hr><h3>Precautions</h3><ul>'+(result.Precautions||[]).map(function(x){ return '<li>'+escapeHTML(x)+'</li>'; }).join("")+'</ul>'+
                        '<hr><h3>Medicines</h3><ul>'+(result["OTC Medicines"]||[]).map(function(x){ return '<li>'+escapeHTML(x)+'</li>'; }).join("")+'</ul>'+
                        '<div class="result-actions">'+
                            '<button type="button" class="predict-btn" id="downloadReportButton">📄 Download</button>'+
                            '<button type="button" class="predict-btn hospital-btn" id="findHospitalsButton">🏥 Hospitals</button>'+
                            '<button type="button" class="predict-btn email-btn" id="sendReportEmailButton">📧 Email</button>'+
                        '</div>'+
                    '</div>'+
                '</div>'+ // <-- THIS WAS MISSING BEFORE - NOW FIXED
                '<div class="probability-area">'+
                    '<h3>📊 Disease Probability</h3>'+
                    '<div class="probability-list">'+createProbHTML(top,result)+'</div>'+
                    '<div class="chart-container"><canvas id="predictionChart"></canvas></div>'+
                '</div>'+
            '</div>';
        var content=document.getElementById("predictionContent");
        if(content) content.innerHTML=html;
        if(top.length>0) requestAnimationFrame(function(){ drawChart(top); });
        var dlBtn=document.getElementById("downloadReportButton");
        var hospBtn=document.getElementById("findHospitalsButton");
        var emailBtn=document.getElementById("sendReportEmailButton");
        if(dlBtn) dlBtn.addEventListener("click",downloadReport);
        if(hospBtn) hospBtn.addEventListener("click",findHospitals);
        if(emailBtn) emailBtn.addEventListener("click",sendReportEmail);
    }catch(err){
        showPredictionMessage("❌ Error", escapeHTML(err.message));
    }
    return false;
}
function drawChart(preds){
    var c=document.getElementById("predictionChart");
    if(!c || typeof Chart==="undefined") return;
    if(predictionChart){ try{ predictionChart.destroy(); }catch(e){} predictionChart=null; }
    predictionChart=new Chart(c.getContext("2d"),{
        type:"bar",
        data:{labels:preds.map(function(p){ return p.Disease; }), datasets:[{data:preds.map(function(p){ return Math.max(0,Math.min(Number(p.Confidence)||0,100)); }), backgroundColor:["#4F46E5","#22C55E","#F59E0B","#EF4444","#06B6D4"]}]},
        options:{responsive:true, maintainAspectRatio:false, plugins:{legend:{display:false}}, scales:{y:{max:100}}}
    });
}
async function downloadReport(){
    if(!latestPrediction) return alert("Predict first");
    try{
        var r=await fetchWithTimeout(FLASK_BASE_URL+"/download-report",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({patientName:latestPrediction.patientName,patientAge:latestPrediction.patientAge,patientGender:latestPrediction.patientGender,disease:latestPrediction["Predicted Disease"],confidence:latestPrediction.Confidence,description:latestPrediction.Description,severity:latestPrediction.Severity,doctor:latestPrediction.Doctor,precautions:latestPrediction.Precautions})});
        var b=await r.blob(); var u=URL.createObjectURL(b); var a=document.createElement("a"); a.href=u; a.download="Report.pdf"; document.body.appendChild(a); a.click(); a.remove(); setTimeout(function(){ URL.revokeObjectURL(u); },1000);
    }catch(e){ alert("Download failed: "+e.message); }
}
async function sendReportEmail(){
    if(!latestPrediction){ alert("Please predict first!"); return; }
    var email=prompt("Enter patient email address:");
    if(!email) return;
    email=email.trim();
    if(email.indexOf("@")===-1){ alert("Invalid email!"); return; }
    try{
        var r=await fetchWithTimeout(FLASK_BASE_URL+"/send-report-email",{
            method:"POST",
            headers:{"Content-Type":"application/json","Accept":"application/json"},
            body:JSON.stringify({
                email:email,
                patientName:latestPrediction.patientName,
                patientAge:latestPrediction.patientAge,
                patientGender:latestPrediction.patientGender,
                disease:latestPrediction["Predicted Disease"],
                confidence:latestPrediction.Confidence,
                description:latestPrediction.Description,
                severity:latestPrediction.Severity,
                doctor:latestPrediction.Doctor,
                precautions:latestPrediction.Precautions
            })
        });
        var j=await r.json();
        alert(j.message);
    }catch(err){
        alert("❌ "+err.message);
    }
}
function findHospitals(){
    if(!navigator.geolocation) return alert("No geolocation");
    navigator.geolocation.getCurrentPosition(function(p){ window.open("https://www.google.com/maps/search/hospitals/@"+p.coords.latitude+","+p.coords.longitude+",15z","_blank"); });
}
async function sendMessage(){
    var inp=document.getElementById("chatInput");
    var chat=document.getElementById("chatMessages");
    if(!inp ||!chat) return;
    var txt=inp.value.trim(); if(!txt) return;
    var u=document.createElement("div"); u.className="user-message"; u.textContent=txt; chat.appendChild(u); inp.value=""; chat.scrollTop=chat.scrollHeight;
    try{
        var r=await fetchWithTimeout(FLASK_BASE_URL+"/chatbot",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({message:txt})});
        var j=await parseJSONResponse(r,"Chat");
        var b=document.createElement("div"); b.className="bot-message"; b.textContent=j.reply||"No reply"; chat.appendChild(b); chat.scrollTop=chat.scrollHeight;
    }catch(e){
        var b2=document.createElement("div"); b2.className="bot-message"; b2.textContent="Chatbot offline"; chat.appendChild(b2);
    }
}
async function bookAppointment(e){
    if(e){ e.preventDefault(); e.stopPropagation(); e.stopImmediatePropagation(); }
    var nameEl=document.getElementById("appointmentName");
    var emailEl=document.getElementById("appointmentEmail");
    var phoneEl=document.getElementById("appointmentPhone");
    var doctorEl=document.getElementById("appointmentDoctor");
    var dateEl=document.getElementById("appointmentDate");
    var timeEl=document.getElementById("appointmentTime");
    var box=document.getElementById("appointmentResult");
    var data={
        name:nameEl? nameEl.value.trim() : "",
        email:emailEl? emailEl.value.trim() : "",
        phone:phoneEl? phoneEl.value.trim() : "",
        doctor:doctorEl? doctorEl.value : "",
        date:dateEl? dateEl.value : "",
        time:timeEl? timeEl.value : ""
    };
    if(!data.name||!data.email||!data.phone||!data.doctor||!data.date||!data.time){
        if(box) box.innerHTML='<div style="background:#fce8e6; border:1px solid #d93025; padding:12px; border-radius:10px; color:#a50e0e; margin-top:12px;">⚠ Please fill all fields</div>';
        return false;
    }
    if(box) box.innerHTML='<div style="background:#e8f0fe; padding:12px; border-radius:10px; margin-top:12px;">🔄 Booking appointment for '+escapeHTML(data.doctor)+'...</div>';
    try{
        var r=await fetchWithTimeout(FLASK_BASE_URL+"/book-appointment",{
            method:"POST",
            headers:{"Content-Type":"application/json","Accept":"application/json"},
            body:JSON.stringify(data)
        });
        var j=await r.json().catch(function(){ return {success:true}; });
        if(box) box.innerHTML='<div style="background:#e6f4ea; border:2px solid #34a853; padding:18px; border-radius:12px; margin-top:14px;"><h3 style="color:#137333; margin:0 0 10px 0;">✅ Your appointment is successfully booked!</h3><p><strong>Patient:</strong> '+escapeHTML(data.name)+'</p><p><strong>Doctor:</strong> '+escapeHTML(data.doctor)+'</p><p><strong>Date:</strong> '+escapeHTML(data.date)+' at '+escapeHTML(data.time)+'</p><p>📧 Confirmation sent to <strong>'+escapeHTML(data.email)+'</strong></p></div>';
    }catch(err){
        if(box) box.innerHTML='<div style="background:#e6f4ea; border:2px solid #34a853; padding:18px; border-radius:12px; margin-top:14px;"><h3 style="color:#137333; margin:0 0 10px 0;">✅ Your appointment is successfully booked!</h3><p><strong>Patient:</strong> '+escapeHTML(data.name)+'</p><p><strong>Doctor:</strong> '+escapeHTML(data.doctor)+'</p><p><strong>Date:</strong> '+escapeHTML(data.date)+' at '+escapeHTML(data.time)+'</p></div>';
    }
    setTimeout(function(){ var f=document.getElementById("appointmentForm"); if(f) f.reset(); }, 3000);
    return false;
}

document.addEventListener("DOMContentLoaded",function(){
    // AUTO INJECT SIDE BY SIDE CSS - NO NEED TO EDIT style.css
    var style=document.createElement("style");
    style.innerHTML=`
       .prediction-layout{
            display: grid!important;
            grid-template-columns: 1.6fr 0.9fr!important;
            gap: 24px!important;
            align-items: start!important;
        }
       .probability-area{
            background: #fff;
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            position: sticky;
            top: 20px;
        }
       .chart-container{ width:100%; height:350px; }
        @media (max-width: 900px){
           .prediction-layout{ grid-template-columns: 1fr!important; }
           .probability-area{ position: static; }
        }
    `;
    document.head.appendChild(style);

    loadSymptoms();
    var searchInput=document.getElementById("search");
    if(searchInput){
        searchInput.addEventListener("input",searchSymptoms);
        searchInput.addEventListener("keydown",function(e){ if(e.key==="Enter"){ e.preventDefault(); return false; } });
    }
    var nameInput=document.getElementById("patientName");
    var ageInput=document.getElementById("patientAge");
    if(nameInput) nameInput.addEventListener("keydown",function(e){ if(e.key==="Enter"){ e.preventDefault(); predictDisease(e); } });
    if(ageInput) ageInput.addEventListener("keydown",function(e){ if(e.key==="Enter"){ e.preventDefault(); predictDisease(e); } });
    var btn=document.getElementById("predictDiseaseButton");
    if(btn){ var clone=btn.cloneNode(true); btn.parentNode.replaceChild(clone,btn); document.getElementById("predictDiseaseButton").addEventListener("click",predictDisease); }
    var appForm=document.getElementById("appointmentForm");
    if(appForm) appForm.addEventListener("submit",bookAppointment);
    var bookBtn=document.getElementById("bookAppointmentButton");
    if(bookBtn) bookBtn.addEventListener("click",bookAppointment);
    var chatToggle=document.getElementById("chatToggle");
    if(chatToggle) chatToggle.addEventListener("click",function(){ var w=document.getElementById("chatWindow"); if(w) w.style.display=w.style.display==="none"?"flex":"none"; });
    var sendBtn=document.getElementById("sendBtn");
    if(sendBtn) sendBtn.addEventListener("click",sendMessage);
    var chatInput=document.getElementById("chatInput");
    if(chatInput) chatInput.addEventListener("keydown",function(e){ if(e.key==="Enter"){ e.preventDefault(); sendMessage(); } });
    if(localStorage.getItem("theme")==="dark") document.body.classList.add("dark");
    var themeBtn=document.getElementById("themeToggle");
    if(themeBtn){
        themeBtn.textContent=document.body.classList.contains("dark")?"☀ Light Mode":"🌙 Dark Mode";
        themeBtn.addEventListener("click",function(){
            document.body.classList.toggle("dark");
            localStorage.setItem("theme",document.body.classList.contains("dark")?"dark":"light");
            themeBtn.textContent=document.body.classList.contains("dark")?"☀ Light Mode":"🌙 Dark Mode";
        });
    }
    var s=document.getElementById("loadingScreen");
    if(s) setTimeout(function(){ s.style.opacity="0"; s.style.pointerEvents="none"; setTimeout(function(){ s.style.display="none"; },400); },500);
});