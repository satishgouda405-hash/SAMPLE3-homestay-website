/* Lightweight site JS: no dependencies, deferred. */
(function(){
  var d=document,w=window;
  var CFG=w.SITE||{};
  function $(s,c){return (c||d).querySelector(s)}
  function $$(s,c){return Array.prototype.slice.call((c||d).querySelectorAll(s))}

  /* ---- analytics helper (GA4 + dataLayer; safe if absent) ---- */
  function track(name,params){
    params=params||{};
    try{ w.dataLayer=w.dataLayer||[]; w.dataLayer.push(Object.assign({event:name},params)); }catch(e){}
    try{ if(typeof w.gtag==='function') w.gtag('event',name,params); }catch(e){}
  }
  w.track=track;

  /* ---- header ---- */
  var hdr=$('.hdr');
  function onScroll(){ if(hdr) hdr.classList.toggle('solid',w.scrollY>50); }
  onScroll(); w.addEventListener('scroll',onScroll,{passive:true});
  var burger=$('.burger');
  if(burger) burger.addEventListener('click',function(){
    var o=d.body.classList.toggle('menu-open'); burger.setAttribute('aria-expanded',o);
  });
  $$('.nav a').forEach(function(a){a.addEventListener('click',function(){d.body.classList.remove('menu-open')})});

  /* ---- reveal on scroll ---- */
  var rv=$$('.rv');
  if('IntersectionObserver' in w){
    var io=new IntersectionObserver(function(es){
      es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target);} });
    },{threshold:.12,rootMargin:'0px 0px -40px 0px'});
    rv.forEach(function(el){io.observe(el)});
  } else rv.forEach(function(el){el.classList.add('in')});

  /* ---- count-up numbers ---- */
  $$('[data-count]').forEach(function(el){
    var end=parseFloat(el.dataset.count),suf=el.dataset.suffix||'',dec=(el.dataset.count.split('.')[1]||'').length;
    if(!('IntersectionObserver' in w)){el.textContent=end+suf;return}
    var o=new IntersectionObserver(function(es){
      if(!es[0].isIntersecting) return; o.disconnect();
      var t0=performance.now();
      (function step(t){
        var p=Math.min((t-t0)/1400,1),e=1-Math.pow(1-p,3);
        el.textContent=(end*e).toFixed(dec)+suf;
        if(p<1) requestAnimationFrame(step);
      })(t0);
    },{threshold:.6});
    o.observe(el);
  });

  /* ---- WhatsApp helpers ---- */
  function waURL(msg){ return 'https://wa.me/'+CFG.wa+'?text='+encodeURIComponent(msg); }
  var fab=$('.wa-float'),menu=$('.wa-menu');
  if(fab&&menu){
    fab.addEventListener('click',function(e){
      e.preventDefault(); menu.classList.toggle('open');
      track('whatsapp_menu_open',{page:location.pathname});
    });
    d.addEventListener('click',function(e){ if(!menu.contains(e.target)&&!fab.contains(e.target)) menu.classList.remove('open'); });
  }

  /* ---- conversion tracking by delegation ---- */
  d.addEventListener('click',function(e){
    var a=e.target.closest('a,button'); if(!a) return;
    var href=a.getAttribute('href')||'';
    if(href.indexOf('wa.me')>-1) track('whatsapp_click',{page:location.pathname,label:a.dataset.track||'whatsapp'});
    else if(href.indexOf('tel:')===0) track('phone_click',{page:location.pathname});
    else if(href.indexOf('mailto:')===0) track('email_click',{page:location.pathname});
    else if(a.dataset.track) track('cta_click',{page:location.pathname,label:a.dataset.track});
  });

  /* ---- enquiry forms (quick bar + contact form) -> WhatsApp prefilled ---- */
  function handleForm(f,label){
    f.addEventListener('submit',function(e){
      e.preventDefault();
      var g=function(n){var el=f.elements[n];return el&&el.value?el.value.trim():''};
      var lines=['Hello '+CFG.name+'! I would like to enquire.'];
      if(g('name')) lines.push('Name: '+g('name'));
      if(g('phone')) lines.push('Phone: '+g('phone'));
      if(g('checkin')) lines.push('Check-in: '+g('checkin'));
      if(g('checkout')) lines.push('Check-out: '+g('checkout'));
      if(g('guests')) lines.push('Guests: '+g('guests'));
      if(g('room')) lines.push('Room: '+g('room'));
      if(g('message')) lines.push('Message: '+g('message'));
      track('enquiry_submit',{form:label,page:location.pathname});
      w.open(waURL(lines.join('\n')),'_blank','noopener');
    });
  }
  $$('form[data-enquiry]').forEach(function(f){handleForm(f,f.dataset.enquiry)});

  /* ---- date inputs: min today, checkout after checkin ---- */
  var today=new Date().toISOString().slice(0,10);
  $$('input[type=date]').forEach(function(i){i.min=today});
  $$('form').forEach(function(f){
    var ci=f.elements.checkin,co=f.elements.checkout;
    if(ci&&co) ci.addEventListener('change',function(){co.min=ci.value||today; if(co.value&&co.value<ci.value) co.value=''});
  });

  /* ---- gallery filter + lightbox ---- */
  var figs=$$('.masonry figure');
  $$('.fbtn').forEach(function(b){
    b.addEventListener('click',function(){
      $$('.fbtn').forEach(function(x){x.classList.remove('on')}); b.classList.add('on');
      var c=b.dataset.cat;
      figs.forEach(function(f){f.classList.toggle('hide',c!=='all'&&f.dataset.cat!==c)});
    });
  });
  var lb=$('dialog.lb');
  if(lb&&figs.length){
    var img=$('img',lb),cap=$('p',lb),idx=0,vis=[];
    function show(i){
      vis=figs.filter(function(f){return !f.classList.contains('hide')});
      idx=(i+vis.length)%vis.length;
      var s=$('img',vis[idx]); img.src=s.src; img.alt=s.alt; cap.textContent=s.alt;
    }
    figs.forEach(function(f){ f.addEventListener('click',function(){
      vis=figs.filter(function(x){return !x.classList.contains('hide')});
      lb.showModal(); show(vis.indexOf(f)); track('gallery_open',{page:location.pathname});
    })});
    $('.x',lb).addEventListener('click',function(){lb.close()});
    $('.pv',lb).addEventListener('click',function(){show(idx-1)});
    $('.nx',lb).addEventListener('click',function(){show(idx+1)});
    lb.addEventListener('click',function(e){ if(e.target===lb) lb.close(); });
    d.addEventListener('keydown',function(e){
      if(!lb.open) return;
      if(e.key==='ArrowLeft') show(idx-1); if(e.key==='ArrowRight') show(idx+1);
    });
  }

  /* ---- room gallery thumbs ---- */
  var main=$('.rg-main img');
  $$('.rg-th button').forEach(function(b){
    b.addEventListener('click',function(){
      $$('.rg-th button').forEach(function(x){x.classList.remove('on')}); b.classList.add('on');
      var i=$('img',b); main.src=i.src; main.alt=i.alt;
    });
  });

  var yr=$('#yr'); if(yr) yr.textContent=new Date().getFullYear();
})();
