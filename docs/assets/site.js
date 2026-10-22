
document.addEventListener('DOMContentLoaded',function(){
  var b=document.querySelector('.burger'),d=document.querySelector('.drawer');
  if(b&&d){b.addEventListener('click',function(){var o=d.classList.toggle('open');b.setAttribute('aria-expanded',o?'true':'false');});}
  var h=document.getElementById('hero-addr');
  if(h){h.addEventListener('submit',function(e){e.preventDefault();var a=encodeURIComponent(h.querySelector('input').value||'');location.href=h.getAttribute('data-to')+(a?'?address='+a:'');});}
  var f=document.getElementById('addr-field');
  if(f){var q=new URLSearchParams(location.search).get('address');if(q)f.value=q;}
});
