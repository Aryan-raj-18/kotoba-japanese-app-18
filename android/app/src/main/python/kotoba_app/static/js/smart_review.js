document.addEventListener('DOMContentLoaded',()=>{
  const intro=document.getElementById('review-intro'), run=document.getElementById('review-run'), done=document.getElementById('review-done');
  if(!intro)return;
  let count=20,items=[],idx=0,remembered=0,revealed=false;
  document.querySelectorAll('#review-count-options .count-btn').forEach(b=>b.addEventListener('click',()=>{document.querySelectorAll('#review-count-options .count-btn').forEach(x=>x.classList.remove('active'));b.classList.add('active');count=+b.dataset.count;}));
  const show=x=>{[intro,run,done].forEach(p=>p.hidden=p!==x);};
  async function start(){
    const list=new URLSearchParams(location.search).get('list');const url=`/api/review/due?limit=${count}${list?`&list=${encodeURIComponent(list)}`:''}`;const r=await fetch(url),d=await r.json();items=d.items||[];idx=0;remembered=0;
    if(!items.length){KotobaLearn&&KotobaLearn.toast('Nothing to review yet');return;} show(run);render();
  }
  function render(){
    const x=items[idx];revealed=false;
    document.getElementById('review-progress').textContent=`${idx+1} / ${items.length}`;
    const chip=document.getElementById('review-mastery');chip.textContent=x.mastery||'Learning';chip.className='mastery-chip mastery-'+String(x.mastery||'learning').toLowerCase();
    document.getElementById('review-front').textContent=x.front||x.id;
    document.getElementById('review-reading').textContent=x.reading||x.sub||'';
    const ans=document.getElementById('review-answer');ans.hidden=true;ans.innerHTML='';
    const h=document.createElement('h3');h.textContent=x.answer||x.meaning||'Review this item';ans.appendChild(h);
    if(x.meaning && x.meaning!==x.answer){const p=document.createElement('p');p.textContent=x.meaning;ans.appendChild(p);}
    if(x.explanation){const p=document.createElement('p');p.className='practice-note';p.textContent=typeof x.explanation==='string'?x.explanation:JSON.stringify(x.explanation);ans.appendChild(p);}
    document.getElementById('review-reveal').hidden=false;document.getElementById('review-rating').hidden=true;
    document.getElementById('review-speak').onclick=()=>KotobaSpeech&&KotobaSpeech.speak(x.front);
  }
  document.getElementById('review-reveal').addEventListener('click',()=>{revealed=true;document.getElementById('review-answer').hidden=false;document.getElementById('review-reveal').hidden=true;document.getElementById('review-rating').hidden=false;});
  document.querySelectorAll('.review-rate').forEach(b=>b.addEventListener('click',async()=>{
    if(!revealed)return;const q=+b.dataset.quality,x=items[idx],ok=q>=3;if(ok)remembered++;
    await KotobaLearn.record({kind:x.kind||'review',id:x.id||x.key,front:x.front,answer:x.answer||x.meaning,reading:x.reading,meaning:x.meaning,sub:x.sub,correct:ok,quality:q,chosen:q===1?'Again':q===3?'Hard':q===4?'Good':'Easy',explanation:x.explanation||''});
    idx++; if(idx<items.length)render(); else finish();
  }));
  function finish(){show(done);const pct=Math.round(100*remembered/items.length);document.getElementById('review-score').textContent=`Remembered ${remembered} of ${items.length} · ${pct}%`;document.getElementById('review-next-note').textContent='Items you found difficult will return sooner; easy items wait longer.';if(window.Sfx)Sfx.complete();if(window.showLessonReaction)showLessonReaction(pct);}
  document.getElementById('review-start').addEventListener('click',start);document.getElementById('review-again').addEventListener('click',()=>show(intro));
});
