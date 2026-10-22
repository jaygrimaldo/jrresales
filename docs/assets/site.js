
document.addEventListener('DOMContentLoaded',function(){
  var b=document.querySelector('.burger'),d=document.querySelector('.drawer');
  if(b&&d){b.addEventListener('click',function(){var o=d.classList.toggle('open');b.setAttribute('aria-expanded',o?'true':'false');});}
  var h=document.getElementById('hero-addr');
  if(h){h.addEventListener('submit',function(e){e.preventDefault();var a=encodeURIComponent(h.querySelector('input').value||'');location.href=h.getAttribute('data-to')+(a?'?address='+a:'');});}
  var f=document.getElementById('addr-field');
  if(f){var q=new URLSearchParams(location.search).get('address');if(q)f.value=q;}
  document.querySelectorAll('form.js-fs').forEach(function(form){
    form.addEventListener('submit',function(e){
      e.preventDefault();
      var btn=form.querySelector('button[type=submit]'),msg=form.querySelector('.form-msg'),label=btn.textContent;
      btn.disabled=true;btn.textContent=form.dataset.sending;
      fetch(form.action,{method:'POST',body:new FormData(form),headers:{'Accept':'application/json'}})
        .then(function(r){
          if(!r.ok)throw new Error('send failed');
          form.querySelectorAll('label,.two,.three,.fine,button').forEach(function(el){el.hidden=true;});
          msg.className='form-msg ok';msg.textContent=form.dataset.ok;msg.hidden=false;
          msg.scrollIntoView({block:'center'});
        })
        .catch(function(){
          btn.disabled=false;btn.textContent=label;
          msg.className='form-msg bad';msg.textContent=form.dataset.bad;msg.hidden=false;
        });
    });
  });
});
