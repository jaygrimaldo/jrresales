
document.addEventListener('DOMContentLoaded',function(){
  var b=document.querySelector('.burger'),d=document.querySelector('.drawer');
  if(b&&d){b.addEventListener('click',function(){var o=d.classList.toggle('open');b.setAttribute('aria-expanded',o?'true':'false');});}
  var h=document.getElementById('hero-addr');
  if(h){h.addEventListener('submit',function(e){e.preventDefault();var v=(h.querySelector('input').value||'').trim(),ok=false;
    // The address goes to the next page through this visit's storage, not the page address (kept out of the Meta Pixel).
    try{sessionStorage.setItem('jr_addr',v);ok=true;}catch(err){}
    location.href=h.getAttribute('data-to')+(!ok&&v?'?address='+encodeURIComponent(v):'');});}
  var f=document.getElementById('addr-field');
  if(f){var q=new URLSearchParams(location.search).get('address');if(!q){try{q=sessionStorage.getItem('jr_addr');sessionStorage.removeItem('jr_addr');}catch(err){}}if(q)f.value=q;}
  // Source tag (J.R., 11/10/2026): a link like ?src=fbad marks where the visitor came from.
  // The tag is kept for the visit (sessionStorage), so it survives clicks to other pages,
  // and is written into each form's "source" field when it sends. No tag: the page's own source.
  var tag='';
  try{
    var qs=new URLSearchParams(location.search).get('src');
    if(qs!==null){qs=qs.trim().slice(0,60);if(qs){try{sessionStorage.setItem('jr_src',qs);}catch(e){}tag=qs;}}
    if(!tag){try{tag=sessionStorage.getItem('jr_src')||'';}catch(e){}}
  }catch(e){}
  document.querySelectorAll('form.js-fs').forEach(function(form){
    var sf=form.querySelector('input[name=source]');
    if(!sf){sf=document.createElement('input');sf.type='hidden';sf.name='source';sf.value='website';form.appendChild(sf);}
    sf.dataset.base=sf.value;
    if(tag)sf.value=tag;
    form.addEventListener('submit',function(e){
      e.preventDefault();
      var btn=form.querySelector('button[type=submit]'),msg=form.querySelector('.form-msg'),label=btn.textContent;
      if(form.dataset.need&&!form.querySelector('input[name=books]:checked')){
        msg.className='form-msg bad';msg.textContent=form.dataset.need;msg.hidden=false;
        form.querySelector('.books').scrollIntoView({block:'center'});return;
      }
      if(btn.disabled)return;
      btn.disabled=true;btn.textContent=form.dataset.sending;msg.hidden=true;
      var old=form.querySelector('.form-err');if(old)old.remove();
      // One ID per request, kept across retries and taps, so any repeat is easy to spot (J.R., 11/5/2026).
      if(!form.dataset.rid)form.dataset.rid=Date.now().toString(36)+Math.random().toString(36).slice(2,8);
      var src=new FormData(form),base=[],errs=[];
      try{
        var g=function(k){return (src.get(k)||'').toString().trim();};
        var r={t:form.id==='hv-form'?'v':(form.id==='bk-form'?'b':(form.id.indexOf('nl-')===0?'n':(form.id==='sg-form'?'g':(form.id==='fg-form'?'f':(form.id==='sl-form'?'s':(form.id==='bg-form'?'y':'c')))))),l:document.documentElement.lang==='es'?'es':'en',
               n:g('name'),p:g('phone'),e:g('email'),a:[g('address')||g('street'),g('city')].filter(Boolean).join(', ')};
        base.push(['tap_to_reply',location.origin+'/reply.html#'+new URLSearchParams(r).toString()]);
      }catch(err){}
      src.forEach(function(v,k){base.push([k,v]);});
      if(tag&&sf.dataset.base!==tag)base.push(['source_without_tag',sf.dataset.base]);
      base.push(['request_id',form.dataset.rid]);
      function done(){
        // Meta Pixel 'Lead' for sign-up forms (not the contact form). Only the form's name goes to Facebook.
        try{
          if(window.fbq&&form.id!=='ct-form'){
            var pg=(location.pathname.split('/').pop()||'index.html').replace(/\.html$/,'');
            var nm=form.id==='nl-foot'?'footer':(pg==='index'?'home':pg);
            if(document.documentElement.lang==='es')nm+='-es';
            fbq('track','Lead',{content_name:nm});
          }
        }catch(err){}
        form.querySelectorAll('label,.two,.three,.pair,.fine,button').forEach(function(el){el.hidden=true;});
        msg.className='form-msg ok';msg.textContent=form.dataset.ok;msg.hidden=false;
        msg.scrollIntoView({block:'center'});
      }
      function fail(code){
        btn.disabled=false;btn.textContent=label;
        msg.className='form-msg bad';msg.textContent=form.dataset.bad;msg.hidden=false;
        var sm=document.createElement('p');sm.className='form-err';sm.textContent='Error code: '+code;msg.insertAdjacentElement('afterend',sm);
      }
      function send(n){
        var fd=new FormData();base.forEach(function(kv){fd.append(kv[0],kv[1]);});
        fd.append('attempt',String(n));
        if(errs.length)fd.append('earlier_try_error',errs.join(' | '));
        var ctl=('AbortController' in window)?new AbortController():null,tm=ctl?setTimeout(function(){ctl.abort();},15000):null;
        fetch(form.action,{method:'POST',body:fd,headers:{'Accept':'application/json'},signal:ctl?ctl.signal:undefined})
          .then(function(res){
            if(tm)clearTimeout(tm);
            if(res.ok){done();return;}
            return res.text().then(function(t){
              var code='HTTP '+res.status+(t?' '+t.slice(0,120):'');
              // Retry only when the problem may be passing; a 4xx answer means Formspree refused this request.
              if(res.status>=500||res.status===429)retry(n,code);else fail(code);
            });
          })
          .catch(function(err){
            if(tm)clearTimeout(tm);
            retry(n,(err&&err.name==='AbortError')?'timeout after 15 seconds':'network: '+((err&&err.message)||err));
          });
      }
      function retry(n,code){
        errs.push('try '+n+': '+code);
        if(n<3)setTimeout(function(){send(n+1);},1000*n);else fail(code);
      }
      send(1);
    });
  });
});
