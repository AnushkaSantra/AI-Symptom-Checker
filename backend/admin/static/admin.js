"use strict";
document.addEventListener("DOMContentLoaded", function(){
  const form=document.getElementById("loginForm");
  const user=document.getElementById("username");
  const pass=document.getElementById("password");
  const msg=document.getElementById("loginMessage");
  const toggle=document.getElementById("togglePass");
  
  if(toggle && pass){
    toggle.addEventListener("click", ()=>{
      const icon=toggle.querySelector("i");
      if(pass.type==="password"){ pass.type="text"; icon.classList.replace("fa-eye","fa-eye-slash"); }
      else{ pass.type="password"; icon.classList.replace("fa-eye-slash","fa-eye"); }
    });
  }

  function show(t,m){
    msg.textContent=m; msg.className="msg "+t; msg.style.display="block";
    setTimeout(()=>{ msg.style.display="none"; },4000);
  }

  if(form){
    form.addEventListener("submit", function(e){
      // let Flask handle if fields filled - only validate empty
      if(!user.value.trim() || !pass.value.trim()){
        e.preventDefault();
        show("error","Please enter username and password.");
        return;
      }
      // show loading
      const btn=form.querySelector(".login-btn");
      btn.disabled=true;
      btn.innerHTML=`<i class="fa-solid fa-spinner fa-spin"></i> Signing in...`;
    });
  }
});