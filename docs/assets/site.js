
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
      if(form.dataset.need&&!form.querySelector('input[name=books]:checked')){
        msg.className='form-msg bad';msg.textContent=form.dataset.need;msg.hidden=false;
        form.querySelector('.books').scrollIntoView({block:'center'});return;
      }
      btn.disabled=true;btn.textContent=form.dataset.sending;
      var src=new FormData(form),fd=new FormData();
      try{
        var g=function(k){return (src.get(k)||'').toString().trim();};
        var r={t:form.id==='hv-form'?'v':(form.id==='bk-form'?'b':'c'),l:document.documentElement.lang==='es'?'es':'en',
               n:g('name'),p:g('phone'),e:g('email'),a:[g('address')||g('street'),g('city')].filter(Boolean).join(', ')};
        fd.append('tap_to_reply',location.origin+'/reply.html#'+new URLSearchParams(r).toString());
      }catch(err){}
      src.forEach(function(v,k){fd.append(k,v);});
      fetch(form.action,{method:'POST',body:fd,headers:{'Accept':'application/json'}})
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
