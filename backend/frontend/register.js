"use strict";
const BASE = window.location.port==="5000" ? "" : "http://127.0.0.1:5000";

document.addEventListener("DOMContentLoaded", ()=>{
  const form=document.getElementById("registerForm");
  const nameEl=document.getElementById("name");
  const emailEl=document.getElementById("email");
  const passEl=document.getElementById("password");
  const cpassEl=document.getElementById("confirmPassword");
  const termsEl=document.getElementById("terms");
  const msg=document.getElementById("registerMessage");
  const btn=document.getElementById("registerButton");
  const strengthBars=document.querySelector(".bars");
  const strengthText=document.getElementById("strengthText");
  const matchEl=document.getElementById("passwordMatch");

  document.querySelectorAll(".toggle").forEach(t=>{
    t.addEventListener("click", ()=>{
      const id=t.dataset.target;
      const inp=document.getElementById(id);
      const icon=t.querySelector("i");
      if(inp.type==="password"){ inp.type="text"; icon.classList.replace("fa-eye","fa-eye-slash"); }
      else{ inp.type="password"; icon.classList.replace("fa-eye-slash","fa-eye"); }
    });
  });

  passEl.addEventListener("input", ()=>{
    const v=passEl.value;
    let score=0;
    if(v.length>=6) score++; if(/[A-Z]/.test(v)) score++; if(/[0-9]/.test(v)) score++; if(/[^A-Za-z0-9]/.test(v)) score++;
    strengthBars.className="bars";
    if(v.length===0){ strengthText.textContent="Use at least 6 characters"; }
    else if(score<=1){ strengthBars.classList.add("weak"); strengthText.textContent="Weak"; }
    else if(score===2){ strengthBars.classList.add("medium"); strengthText.textContent="Medium"; }
    else if(score===3){ strengthBars.classList.add("good"); strengthText.textContent="Good"; }
    else{ strengthBars.classList.add("strong"); strengthText.textContent="Strong"; }
    checkMatch();
  });

  cpassEl.addEventListener("input", checkMatch);
  function checkMatch(){
    if(!cpassEl.value){ matchEl.textContent=""; matchEl.className="match"; return; }
    if(cpassEl.value===passEl.value){ matchEl.textContent="✓ Passwords match"; matchEl.className="match ok"; }
    else{ matchEl.textContent="✗ Passwords do not match"; matchEl.className="match bad"; }
  }

  // modal
  const modal=document.getElementById("termsModal");
  document.getElementById("termsLink").addEventListener("click", e=>{ e.preventDefault(); modal.classList.add("active"); });
  document.getElementById("closeTerms").addEventListener("click", ()=>modal.classList.remove("active"));
  document.getElementById("acceptTerms").addEventListener("click", ()=>{ modal.classList.remove("active"); termsEl.checked=true; });

  form.addEventListener("submit", async e=>{
    e.preventDefault();
    const name=nameEl.value.trim();
    const email=emailEl.value.trim().toLowerCase();
    const pass=passEl.value;
    const cpass=cpassEl.value;

    if(name.length<3){ show("Enter full name (min 3 chars)", "error"); return; }
    if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)){ show("Enter valid email", "error"); return; }
    if(pass.length<6){ show("Password min 6 chars", "error"); return; }
    if(pass!==cpass){ show("Passwords do not match", "error"); return; }
    if(!termsEl.checked){ show("Agree to Terms & Privacy", "error"); return; }

    btn.disabled=true; const old=btn.innerHTML; btn.innerHTML=`<i class="fa-solid fa-spinner fa-spin"></i> Creating...`;
    try{
      const res=await fetch(`${BASE}/patient/register`,{
        method:"POST", headers:{"Content-Type":"application/json"},
        body:JSON.stringify({name,email,password:pass})
      });
      const data=await res.json();
      if(!res.ok || !data.success) throw new Error(data.message||"Registration failed");
      show("Registration successful! Redirecting to login...", "success");
      setTimeout(()=>{ window.location.href="/patient/login"; },1000);
    }catch(err){
      show(err.message.includes("Failed to fetch")?"Flask not running":err.message, "error");
    }finally{
      btn.disabled=false; btn.innerHTML=old;
    }
  });

  function show(text,type){
    msg.textContent=text; msg.className=type; msg.style.display="block";
    msg.classList.add(type); // for css
    setTimeout(()=>{ if(msg.textContent===text) msg.style.display="none"; },4000);
  }
});