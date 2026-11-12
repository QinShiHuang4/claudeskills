/* Sends a form to Formspree; falls back to a pre-filled email when no Formspree ID is set. */
function bundleForm(form,subject){
  const st=form.querySelector('.status'),btn=form.querySelector('button[type=submit]');
  form.addEventListener('submit',async e=>{
    e.preventDefault();st.className='status';st.textContent='';
    if(!form.checkValidity()){form.reportValidity();return}
    const data=new FormData(form);data.append('_subject',subject);
    const id=(window.BUNDLE||{}).formspreeId;
    if(!id){
      const body=[...data.entries()].filter(([k])=>!k.startsWith('_')).map(([k,v])=>k+': '+v).join('\n');
      location.href='mailto:'+BUNDLE.supportEmail+'?subject='+encodeURIComponent(subject)+'&body='+encodeURIComponent(body);
      st.className='status ok';st.textContent='Your email app should open with the request filled in. If it doesn’t, email '+BUNDLE.supportEmail+'.';return;
    }
    btn.disabled=true;btn.classList.add('loading');
    try{
      const r=await fetch('https://formspree.io/f/'+id,{method:'POST',body:data,headers:{Accept:'application/json'}});
      if(!r.ok)throw new Error();
      form.reset();st.className='status ok';st.textContent=form.dataset.ok;
    }catch(_){st.className='status err';st.textContent='We couldn’t send that. Check your connection and try again, or email '+BUNDLE.supportEmail+'.'}
    finally{btn.disabled=false;btn.classList.remove('loading')}
  });
}
