(function () {
  let current = null;
  function clean(text) { return String(text || '').replace(/\s+/g,' ').trim(); }
  function speak(text, rate) {
    text=clean(text); if (!text) return;
    if (window.KotobaLearn) KotobaLearn.action('audio');
    try {
      if (window.KotobaSpeechNative && typeof window.KotobaSpeechNative.speak === 'function') {
        window.KotobaSpeechNative.speak(text, Number(rate || 0.92));
        return;
      }
    } catch (_) {}
    if (!('speechSynthesis' in window)) return;
    speechSynthesis.cancel();
    const u=new SpeechSynthesisUtterance(text); u.lang='ja-JP'; u.rate=Number(rate || 0.92); u.pitch=1;
    const voices=speechSynthesis.getVoices();
    const ja=voices.find(v=>/^ja(-|_)/i.test(v.lang || ''));
    if (ja) u.voice=ja;
    current=u; speechSynthesis.speak(u);
  }
  function stop() {
    try { if (window.KotobaSpeechNative) window.KotobaSpeechNative.stop(); } catch (_) {}
    if ('speechSynthesis' in window) speechSynthesis.cancel(); current=null;
  }
  function wire(root) {
    (root || document).querySelectorAll('[data-speak]:not([data-speak-wired])').forEach(btn=>{
      btn.dataset.speakWired='1';
      btn.addEventListener('click',(ev)=>{ev.preventDefault();ev.stopPropagation();speak(btn.dataset.speak, btn.dataset.rate);});
    });
  }
  window.KotobaSpeech={speak,stop,wire};
  document.addEventListener('DOMContentLoaded',()=>wire(document));
  const mo=new MutationObserver(m=>{for(const x of m){for(const n of x.addedNodes){if(n.nodeType===1)wire(n);}}});
  document.addEventListener('DOMContentLoaded',()=>{if(document.body)mo.observe(document.body,{childList:true,subtree:true});});
})();
