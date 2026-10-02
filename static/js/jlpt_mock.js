document.addEventListener('DOMContentLoaded',()=>{
 const stage=document.getElementById('mock-stage');if(!stage)return;const level=stage.dataset.level,minutes=+stage.dataset.minutes||30;
 const intro=document.getElementById('mock-intro'),run=document.getElementById('mock-run'),results=document.getElementById('mock-results');let qs=[],answers=[],flags=new Set(),idx=0,endAt=0,timer=null;
 const show=x=>[intro,run,results].forEach(p=>p.hidden=p!==x);
 async function start(){const r=await fetch(`/api/jlpt_mock?level=${level}`),d=await r.json();qs=d.questions||[];answers=Array(qs.length).fill(null);idx=0;flags.clear();endAt=Date.now()+minutes*60000;show(run);render();tick();timer=setInterval(tick,1000);}
 function tick(){const left=Math.max(0,endAt-Date.now()),m=Math.floor(left/60000),s=Math.floor((left%60000)/1000);document.getElementById('mock-timer').textContent=`${m}:${String(s).padStart(2,'0')}`;if(left<=0){clearInterval(timer);finish(true);}}
 function render(){const q=qs[idx];document.getElementById('mock-progress').textContent=`Question ${idx+1} / ${qs.length} · ${q.category||''}`;const p=document.getElementById('mock-passage');p.hidden=!q.passage;p.textContent=q.passage||'';document.getElementById('mock-question').textContent=q.prompt;const o=document.getElementById('mock-options');o.innerHTML='';q.options.forEach((v,i)=>{const b=document.createElement('button');b.className='quiz-option'+(answers[idx]===i?' selected':'');b.textContent=`${i+1}. ${v}`;b.onclick=()=>{answers[idx]=i;render();};o.appendChild(b);});document.getElementById('mock-flag').classList.toggle('active',flags.has(idx));document.getElementById('mock-prev').disabled=idx===0;document.getElementById('mock-next').disabled=idx===qs.length-1;renderPalette();}
 function renderPalette(){const p=document.getElementById('mock-palette');p.innerHTML='';qs.forEach((_,i)=>{const b=document.createElement('button');b.type='button';b.textContent=i+1;b.className='mock-dot'+(answers[i]!=null?' answered':'')+(flags.has(i)?' flagged':'')+(i===idx?' current':'');b.onclick=()=>{idx=i;render();};p.appendChild(b);});}
 document.getElementById('mock-prev').onclick=()=>{if(idx>0){idx--;render();}};document.getElementById('mock-next').onclick=()=>{if(idx<qs.length-1){idx++;render();}};document.getElementById('mock-flag').onclick=()=>{flags.has(idx)?flags.delete(idx):flags.add(idx);render();};document.getElementById('mock-submit').onclick=()=>finish(false);
 function furigana(parent,blocks,text){parent.innerHTML='';if(Array.isArray(blocks)&&blocks.length){blocks.forEach(bl=>{const p=document.createElement('p');(bl||[]).forEach(seg=>{if(typeof seg==='string')p.append(document.createTextNode(seg));else if(seg&&seg.text){if(seg.reading){const ruby=document.createElement('ruby');ruby.append(document.createTextNode(seg.text));const rt=document.createElement('rt');rt.textContent=seg.reading;ruby.append(rt);p.append(ruby);}else p.append(document.createTextNode(seg.text));}});parent.append(p);});}else parent.textContent=text||'';}
 async function finish(timeout){
  if(timer)clearInterval(timer);
  let right=0,cats={};
  qs.forEach((q,i)=>{const ok=answers[i]===q.answer_index;if(ok)right++;const c=q.category||'Practice';cats[c]=cats[c]||{right:0,total:0};cats[c].total++;if(ok)cats[c].right++;});
  await fetch('/api/jlpt_mock/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({level,score:right,total:qs.length,categories:cats})});
  show(results);
  const pct=Math.round(100*right/Math.max(1,qs.length));
  document.getElementById('mock-score').textContent=`${right} / ${qs.length} · ${pct}%${timeout?' · time ended':''}`;
  const bd=document.getElementById('mock-breakdown');bd.innerHTML='';
  Object.entries(cats).forEach(([k,v])=>{const d=document.createElement('div');d.className='learner-stat';const label=document.createElement('span');label.textContent=k;const strong=document.createElement('strong');strong.textContent=`${v.right}/${v.total}`;d.append(label,strong);bd.append(d);});
  const rev=document.getElementById('mock-review');rev.innerHTML='';
  const writes=[];
  qs.forEach((q,i)=>{
    const ok=answers[i]===q.answer_index;
    const card=document.createElement('article');card.className='exam-review-card '+(ok?'correct-review':'missed-review');
    const chip=document.createElement('span');chip.className='exam-category-chip';chip.textContent=`${ok?'✓ Correct':'✕ Review'} · ${q.category||'Practice'}`;
    const question=document.createElement('p');question.className='exam-review-question';question.textContent=q.prompt;
    const chosen=document.createElement('p');chosen.className=ok?'exam-review-correct':'exam-review-wrong';chosen.textContent=`Your answer: ${answers[i]==null?'Unanswered':q.options[answers[i]]}`;
    const correct=document.createElement('p');correct.className='exam-review-correct';correct.textContent=`Correct: ${q.options[q.answer_index]}`;
    const listen=document.createElement('button');listen.type='button';listen.className='btn-ghost speak-btn';listen.textContent='🔊 Hear sentence';listen.onclick=()=>KotobaSpeech&&KotobaSpeech.speak(q.explanation||q.prompt,.82);
    const ex=document.createElement('div');ex.className='exam-review-explanation exam-furigana';furigana(ex,q.explanation_blocks,q.explanation);
    card.append(chip,question,chosen,correct,listen,ex);rev.append(card);
    if(window.KotobaLearn) writes.push(KotobaLearn.record({kind:'jlpt-mock',id:q.id,level,front:q.prompt,prompt:q.prompt,answer:q.options[q.answer_index],correct_answer:q.options[q.answer_index],chosen:answers[i]==null?'Unanswered':q.options[answers[i]],correct:ok,quality:ok?4:1,explanation:q.explanation||''}));
  });
  if(writes.length) await Promise.all(writes);
  if(window.showLessonReaction)showLessonReaction(pct);
 }
 document.getElementById('mock-start').onclick=start;
});
