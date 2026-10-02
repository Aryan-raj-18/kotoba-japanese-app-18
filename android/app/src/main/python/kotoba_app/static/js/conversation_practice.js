document.addEventListener('DOMContentLoaded',()=>{
 const convo=document.querySelector('.convo-standalone');if(!convo)return;const lines=[...convo.querySelectorAll('.convo-line')];
 document.getElementById('convo-play-all')?.addEventListener('click',()=>{const text=lines.map(l=>l.querySelector('.convo-kanji')?.textContent||'').join(' ');KotobaSpeech&&KotobaSpeech.speak(text,.88);});
 document.getElementById('convo-play-slow')?.addEventListener('click',()=>{const text=lines.map(l=>l.querySelector('.convo-kanji')?.textContent||'').join(' ');KotobaSpeech&&KotobaSpeech.speak(text,.7);});
 document.querySelectorAll('[data-shadow]').forEach(b=>b.addEventListener('click',()=>{const role=b.dataset.shadow;document.querySelectorAll('[data-shadow]').forEach(x=>x.classList.toggle('active',x===b));convo.classList.remove('shadow-a','shadow-b');if(role!=='off')convo.classList.add(`shadow-${role.toLowerCase()}`);}));
});
