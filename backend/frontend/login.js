"use strict";
const FLASK_BASE_URL = "";

document.addEventListener("DOMContentLoaded", function(){
  const form=document.getElementById("loginForm");
  const email=document.getElementById("email");
  const pwd=document.getElementById("password");
  const toggle=document.querySelector(".toggle-password");
  if(toggle && pwd){
    toggle.addEventListener("click", ()=>{
      const icon=toggle.querySelector("i");
      if(pwd.type==="password"){ pwd.type="text"; icon.classList.replace("fa-eye","fa-eye-slash"); }
      else{ pwd.type="password"; icon.classList.replace("fa-eye-slash","fa-eye"); }
    });
  }
  if(form) form.addEventListener("submit", handleLogin);
  const g=document.querySelector(".google-btn");
  if(g) g.addEventListener("click", e=>{ e.preventDefault(); showMsg("info","Google Sign-In coming soon"); });
});

async function handleLogin(e){
  e.preventDefault();
  const emailEl=document.getElementById("email");
  const pwdEl=document.getElementById("password");
  const btn=document.querySelector(".login-btn");
  const email=emailEl.value.trim();
  const pwd=pwdEl.value;
  if(!email){ showErr(emailEl,"Enter email"); return; }
  if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)){ showErr(emailEl,"Invalid email"); return; }
  if(!pwd){ showErr(pwdEl,"Enter password"); return; }
  if(pwd.length<6){ showErr(pwdEl,"Min 6 chars"); return; }

  btn.disabled=true; const old=btn.innerHTML; btn.innerHTML=`<i class="fa-solid fa-spinner fa-spin"></i> Signing...`;
  try{
    const r=await fetch(`${FLASK_BASE_URL}/patient/login`,{
      method:"POST", headers:{"Content-Type":"application/json"},
      body:JSON.stringify({email,password:pwd})
    });
    const j=await r.json();
    if(!r.ok || !j.success) throw new Error(j.message||"Login failed");
    localStorage.setItem("patientLoggedIn","true");
    localStorage.setItem("patient", JSON.stringify(j.patient||{email,name:j.name}));
    showMsg("success","Login success! Redirecting...");
    setTimeout(()=>{ window.location.href="/"; },800);
  }catch(err){
    showMsg("error", err.message.includes("Failed to fetch")?"Flask not running. Run python app.py":err.message);
  }finally{
    btn.disabled=false; btn.innerHTML=old;
  }
}
function showErr(input,msg){
  input.classList.add("input-error");
  let next=input.closest(".input-group").nextElementSibling;
  if(next && next.classList.contains("login-input-error")) next.remove();
  const d=document.createElement("div"); d.className="login-input-error"; d.textContent=msg;
  input.closest(".input-group").insertAdjacentElement("afterend",d);
  setTimeout(()=>{ input.classList.remove("input-error"); if(d.parentNode) d.remove(); },3000);
}
function showMsg(type,msg){
  const box=document.getElementById("loginMessage");
  box.className=""; box.id="loginMessage"; box.classList.add(type);
  box.textContent=msg; box.style.display="block";
}