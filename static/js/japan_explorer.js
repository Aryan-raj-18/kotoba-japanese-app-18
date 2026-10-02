(() => {
  const payload = window.JAPAN_EXPLORER_DATA || {};
  const places = Array.isArray(payload.places) ? payload.places : [];
  if (!places.length) return;

  const NS = 'http://www.w3.org/2000/svg';
  const map = document.getElementById('japan-map');
  const islands = document.getElementById('japan-islands');
  const pinLayer = document.getElementById('japan-pin-layer');
  const labelLayer = document.getElementById('japan-label-layer');
  const plane = document.getElementById('japan-plane');
  const list = document.getElementById('japan-place-list');
  const countEl = document.getElementById('japan-result-count');
  const titleEl = document.getElementById('japan-list-title');
  const search = document.getElementById('japan-search');
  const regionChips = document.getElementById('japan-region-chips');
  const levelSwitch = document.getElementById('japan-level-switch');
  const drawer = document.getElementById('japan-drawer');
  const drawerContent = document.getElementById('japan-drawer-content');
  const backdrop = document.getElementById('japan-drawer-backdrop');
  const closeBtn = document.getElementById('japan-drawer-close');
  const stampPop = document.getElementById('passport-stamp-pop');
  const stampName = document.getElementById('passport-stamp-name');
  const visitedCount = document.getElementById('japan-visited-count');
  const passportProgress = document.getElementById('japan-passport-progress');
  const surpriseBtn = document.getElementById('japan-surprise');
  const unvisitedBtn = document.getElementById('japan-show-unvisited');

  const visited = new Set(window.JAPAN_VISITED || []);
  let activeRegion = 'All';
  let level = localStorage.getItem('kotoba-japan-level') || window.JAPAN_DEFAULT_LEVEL || 'beginner';
  if (!['beginner','intermediate','advanced'].includes(level)) level='beginner';
  let unvisitedOnly = false;
  let selected = null;
  let lastPoint = null;
  let currentWords = [];
  let quizState = null;

  const pinEls = new Map();
  const labelEls = new Map();
  const seenWords = new Set(JSON.parse(sessionStorage.getItem('kotoba-japan-seen-words') || '[]'));

  const minLon=127.0, maxLon=145.9, minLat=25.5, maxLat=45.8;
  const project=(lon,lat)=>({x:48 + ((lon-minLon)/(maxLon-minLon))*664, y:56 + ((maxLat-lat)/(maxLat-minLat))*806});

  const islandShapes = [
    // Hokkaido
    [[139.55,41.35],[140.12,42.10],[140.55,42.55],[140.65,43.15],[141.35,43.85],[142.25,44.35],[143.20,44.10],[144.15,44.05],[145.25,43.35],[145.55,42.75],[144.90,42.15],[143.70,42.02],[142.85,41.55],[141.70,41.45],[140.70,41.55]],
    // Honshu
    [[140.80,41.45],[140.18,40.65],[139.95,39.95],[139.70,39.25],[139.45,38.70],[138.90,38.05],[138.45,37.55],[137.65,37.02],[137.10,36.55],[136.25,36.15],[135.40,35.85],[134.50,35.60],[133.50,35.50],[132.55,35.05],[131.65,34.55],[131.25,34.20],[132.05,33.95],[133.00,34.20],[133.85,34.35],[134.70,34.42],[135.45,34.18],[136.05,34.25],[136.75,34.48],[137.55,34.58],[138.30,34.58],[139.10,34.82],[139.82,35.20],[140.35,35.70],[140.50,36.30],[140.75,37.05],[141.20,38.10],[141.58,39.15],[141.55,40.10],[141.20,40.90]],
    // Shikoku
    [[132.15,33.95],[132.65,34.30],[133.45,34.35],[134.15,34.25],[134.80,33.92],[134.35,33.45],[133.60,33.30],[132.80,33.35],[132.20,33.55]],
    // Kyushu
    [[129.35,33.75],[130.10,33.85],[130.75,33.55],[131.25,33.10],[131.55,32.55],[131.30,31.75],[130.75,31.10],[130.05,31.05],[129.65,31.55],[129.55,32.20],[129.10,32.65]],
  ];

  function svg(tag, attrs={}) { const el=document.createElementNS(NS,tag); Object.entries(attrs).forEach(([k,v])=>el.setAttribute(k,v)); return el; }
  function polygon(points, cls='jp-island') {
    const p=points.map(([lon,lat])=>{const q=project(lon,lat);return `${q.x.toFixed(1)},${q.y.toFixed(1)}`}).join(' ');
    const el=svg('polygon',{points:p,class:cls}); islands.appendChild(el); return el;
  }

  islandShapes.forEach(p=>polygon(p));
  // Okinawa/Ryukyu chain and a few small island dots, deliberately simplified.
  [[127.68,26.21,10],[128.0,27.0,4],[129.2,28.3,4],[130.0,29.6,3],[130.4,30.4,4],[129.3,30.8,3]].forEach(([lon,lat,r])=>{
    const q=project(lon,lat), c=svg('circle',{cx:q.x,cy:q.y,r, class:'jp-island-dot'}); islands.appendChild(c);
  });
  // Decorative mountains so the map feels geographic without reproducing the reference artwork.
  [[138.73,35.36],[137.2,36.2],[140.0,39.0],[130.8,32.7]].forEach(([lon,lat])=>{
    const q=project(lon,lat); const g=svg('g',{class:'jp-mountain'}); g.appendChild(svg('path',{d:`M ${q.x-13} ${q.y+8} L ${q.x} ${q.y-15} L ${q.x+13} ${q.y+8} Z`})); islands.appendChild(g);
  });

  const major = new Set(['hokkaido','miyagi','tokyo','kanagawa','aichi','kyoto','osaka','hyogo','hiroshima','fukuoka','nagasaki','okinawa']);

  places.forEach(place=>{
    const q=project(place.lon,place.lat);
    const g=svg('g',{class:`jp-map-pin ${visited.has(place.id)?'visited':''}`, tabindex:'0', role:'button', 'aria-label':`${place.city_en}, ${place.prefecture_en}`});
    g.style.transformOrigin=`${q.x}px ${q.y}px`;
    const pulse=svg('circle',{cx:q.x,cy:q.y,r:13,class:'jp-pin-pulse'});
    const dot=svg('circle',{cx:q.x,cy:q.y,r:6.8,class:'jp-pin-dot'});
    const hit=svg('circle',{cx:q.x,cy:q.y,r:18,class:'jp-pin-hit'});
    const title=svg('title'); title.textContent=`${place.city_en} · ${place.prefecture_en}`;
    g.append(pulse,dot,hit,title); pinLayer.appendChild(g); pinEls.set(place.id,g);
    g.addEventListener('click',()=>selectPlace(place));
    g.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();selectPlace(place)}});

    if(major.has(place.id)){
      const t=svg('text',{x:q.x+10,y:q.y-10,class:'jp-major-label'}); t.textContent=place.city_en; labelLayer.appendChild(t); labelEls.set(place.id,t);
    }
  });

  function esc(v){ return String(v??'').replace(/[&<>'"]/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[m])); }
  function normalize(v){ return String(v||'').toLowerCase().normalize('NFKC'); }
  function shuffle(a){ const b=[...a]; for(let i=b.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[b[i],b[j]]=[b[j],b[i]];} return b; }

  function setLevel(next){
    level=next; localStorage.setItem('kotoba-japan-level',level);
    levelSwitch.querySelectorAll('button').forEach(b=>b.classList.toggle('active',b.dataset.level===level));
    if(selected) renderDrawer(selected,false);
  }
  levelSwitch.querySelectorAll('button').forEach(b=>b.addEventListener('click',()=>setLevel(b.dataset.level)));
  setLevel(level);

  (payload.regions||[]).forEach(region=>{
    const b=document.createElement('button'); b.type='button'; b.dataset.region=region; b.textContent=region; regionChips.appendChild(b);
  });
  regionChips.addEventListener('click',e=>{
    const b=e.target.closest('[data-region]'); if(!b)return;
    activeRegion=b.dataset.region; regionChips.querySelectorAll('button').forEach(x=>x.classList.toggle('active',x===b));
    applyFilters();
  });
  search.addEventListener('input',applyFilters);

  function matches(place){
    if(activeRegion!=='All' && place.region!==activeRegion) return false;
    if(unvisitedOnly && visited.has(place.id)) return false;
    const q=normalize(search.value).trim(); if(!q)return true;
    const hay=normalize([place.prefecture_en,place.prefecture_jp,place.city_en,place.city_jp,place.reading,place.region,...place.famous,...place.foods].join(' '));
    return hay.includes(q);
  }

  function applyFilters(){
    const filtered=places.filter(matches);
    renderList(filtered);
    countEl.textContent=filtered.length;
    titleEl.textContent=activeRegion==='All'?(unvisitedOnly?'Unvisited places':'All 47'):`${activeRegion}${unvisitedOnly?' · unvisited':''}`;
    places.forEach(p=>{
      const show=filtered.some(x=>x.id===p.id); const pin=pinEls.get(p.id), label=labelEls.get(p.id);
      if(pin){pin.classList.toggle('filtered-out',!show); pin.setAttribute('aria-hidden',show?'false':'true');}
      if(label) label.classList.toggle('filtered-out',!show);
    });
  }

  function renderList(rows){
    list.innerHTML='';
    rows.forEach((p,i)=>{
      const card=document.createElement('button'); card.type='button'; card.className=`japan-place-card ${visited.has(p.id)?'visited':''}`; card.style.setProperty('--delay',`${Math.min(i,18)*18}ms`);
      card.innerHTML=`<span class="japan-place-code">${String(p.code).padStart(2,'0')}</span><span class="japan-place-copy"><strong>${esc(p.city_en)}</strong><small>${esc(p.city_jp)} · ${esc(p.prefecture_en)}</small><em>${esc(p.tagline)}</em></span><span class="japan-place-status">${visited.has(p.id)?'✓':'›'}</span>`;
      card.addEventListener('click',()=>selectPlace(p)); list.appendChild(card);
    });
    if(!rows.length) list.innerHTML='<div class="japan-empty"><strong>No matching place</strong><span>Try another city, prefecture, or region.</span></div>';
  }

  function pickWords(place){
    const specific=(place.level_words && place.level_words[level])||[];
    const pool=(payload.common_words && payload.common_words[level])||[];
    const words=[];
    specific.forEach(w=>{ if(!words.some(x=>x.jp===w.jp)) words.push({...w,local:true}); });
    let candidates=shuffle(pool.filter(w=>!seenWords.has(`${level}:${w.jp}`)));
    if(candidates.length<4) candidates=shuffle(pool);
    for(const w of candidates){ if(words.length>=5)break; if(!words.some(x=>x.jp===w.jp))words.push({...w,local:false}); }
    currentWords=words.slice(0,5);
    currentWords.forEach(w=>seenWords.add(`${level}:${w.jp}`));
    sessionStorage.setItem('kotoba-japan-seen-words',JSON.stringify([...seenWords].slice(-100)));
    return currentWords;
  }

  function levelLabel(){ return level[0].toUpperCase()+level.slice(1); }
  function placeImage(place,idx){ return `/static/images/japan_explorer/${place.id}-${idx}.svg`; }

  function renderDrawer(place,markVisit=true){
    currentWords=pickWords(place);
    const phrase=(place.phrases||{})[level]||{};
    const words=currentWords.map((w,i)=>`<article class="japan-word-card ${w.local?'local-word':''}">
      <div><span class="word-number">${i+1}</span>${w.local?'<span class="local-word-badge">LOCAL</span>':''}</div>
      <ruby class="japan-word-ruby">${esc(w.jp)}<rt>${esc(w.reading)}</rt></ruby><span>${esc(w.en)}</span>
      <div class="japan-word-actions"><button class="line-speak" type="button" data-speak="${esc(w.jp)}">🔊</button><button class="favorite-btn" type="button" data-favorite-kind="japan-word" data-favorite-id="${esc(place.id+':'+w.jp)}" data-favorite-front="${esc(w.jp)}" data-favorite-reading="${esc(w.reading)}" data-favorite-meaning="${esc(w.en)}" data-favorite-list="Japan Explorer">☆ Save</button></div>
    </article>`).join('');
    const gallery=(place.visuals||[]).map((v,i)=>`<figure class="japan-gallery-card"><img src="${placeImage(place,i+1)}" alt="Illustrated ${esc(place.prefecture_en)} learning postcard: ${esc(v.title)}"><figcaption><strong>${esc(v.title)}</strong><span>${esc(v.caption)}</span></figcaption></figure>`).join('');
    const famous=(place.famous||[]).map(x=>`<li>${esc(x)}</li>`).join('');
    const foods=(place.foods||[]).map(x=>`<span>${esc(x)}</span>`).join('');
    drawerContent.innerHTML=`
      <div class="japan-detail-hero">
        <img src="${placeImage(place,1)}" alt="Illustrated postcard for ${esc(place.prefecture_en)}">
        <div class="japan-detail-overlay"><span class="japan-region-pill">${esc(place.region)}</span><span class="japan-visited-pill ${visited.has(place.id)?'shown':''}">✓ Passport stamp</span></div>
      </div>
      <div class="japan-detail-body">
        <div class="japan-detail-title-row"><div><p class="hero-eyebrow">${esc(place.prefecture_jp)} · ${esc(place.prefecture_en)}</p><h2>${esc(place.city_en)} <small>${esc(place.city_jp)}</small></h2><p class="japan-reading">${esc(place.reading)}</p></div><button class="speak-btn" type="button" data-speak="${esc(place.city_jp)}">🔊 Hear it</button></div>
        <p class="japan-tagline">${esc(place.tagline)}</p><p class="japan-description">${esc(place.description)}</p>
        <div class="japan-fact-grid"><div><span>Famous for</span><ul>${famous}</ul></div><div><span>Local tastes</span><div class="japan-food-tags">${foods}</div></div></div>

        <section class="japan-gallery-section"><div class="japan-section-title"><div><p class="hero-eyebrow">見る — remember visually</p><h3>Location postcards</h3></div><small>Offline illustrations</small></div><div class="japan-gallery">${gallery}</div></section>

        <section class="japan-lesson-section">
          <div class="japan-section-title"><div><p class="hero-eyebrow">ことば — words</p><h3>Your ${levelLabel()} five</h3></div><span class="japan-level-badge">${levelLabel()}</span></div>
          <p class="japan-lesson-note">One local term + fresh travel Japanese. Kotoba avoids repeating generic map words during this session until the pool needs to recycle.</p>
          <div class="japan-word-grid">${words}</div>
          <article class="japan-phrase-card"><span>Phrase for this stop</span><ruby class="japan-phrase-ruby">${esc(phrase.jp||'')}<rt>${esc(phrase.reading||'')}</rt></ruby><p>${esc(phrase.en||'')}</p><button class="speak-btn" type="button" data-speak="${esc(phrase.jp||'')}">🔊 Listen</button></article>
          <div class="japan-lesson-actions"><button class="btn-primary" id="japan-start-quiz" type="button">Mini quiz · 3 questions</button><button class="favorite-btn" type="button" data-favorite-kind="japan-place" data-favorite-id="${esc(place.id)}" data-favorite-front="${esc(place.city_en)}" data-favorite-reading="${esc(place.city_jp+' · '+place.reading)}" data-favorite-meaning="${esc(place.tagline)}" data-favorite-list="Japan Explorer">☆ Save place</button></div>
          <div id="japan-mini-quiz" class="japan-mini-quiz" hidden></div>
        </section>
      </div>`;
    drawer.classList.add('open'); drawer.setAttribute('aria-hidden','false'); backdrop.hidden=false; requestAnimationFrame(()=>backdrop.classList.add('show'));
    document.body.classList.add('japan-drawer-open');
    if(window.KotobaSpeech) KotobaSpeech.wire(drawerContent);
    if(window.KotobaLearn) KotobaLearn.wireFavorites(drawerContent);
    const qbtn=document.getElementById('japan-start-quiz'); if(qbtn)qbtn.addEventListener('click',startMiniQuiz);
    if(markVisit) markVisited(place);
  }

  function movePlane(place){
    const q=project(place.lon,place.lat);
    if(!lastPoint){ plane.style.transition='none'; plane.style.transform=`translate(${q.x}px,${q.y}px)`; requestAnimationFrame(()=>plane.style.transition='transform .85s cubic-bezier(.2,.75,.25,1)'); lastPoint=q; return; }
    const ang=Math.atan2(q.y-lastPoint.y,q.x-lastPoint.x)*180/Math.PI;
    plane.style.setProperty('--plane-angle',`${ang}deg`); plane.classList.add('flying');
    plane.style.transform=`translate(${q.x}px,${q.y}px) rotate(${ang}deg)`;
    clearTimeout(plane._t); plane._t=setTimeout(()=>plane.classList.remove('flying'),900); lastPoint=q;
  }

  function selectPlace(place){
    selected=place; movePlane(place);
    pinEls.forEach((g,id)=>g.classList.toggle('selected',id===place.id));
    renderDrawer(place,true);
    const card=[...list.querySelectorAll('.japan-place-card')].find(c=>c.querySelector('strong')?.textContent===place.city_en); if(card) card.scrollIntoView({block:'nearest',behavior:'smooth'});
  }

  function closeDrawer(){ drawer.classList.remove('open'); drawer.setAttribute('aria-hidden','true'); backdrop.classList.remove('show'); document.body.classList.remove('japan-drawer-open'); setTimeout(()=>backdrop.hidden=true,220); }
  closeBtn.addEventListener('click',closeDrawer); backdrop.addEventListener('click',closeDrawer); document.addEventListener('keydown',e=>{if(e.key==='Escape'&&drawer.classList.contains('open'))closeDrawer()});

  async function markVisited(place){
    try{
      const r=await fetch('/api/japan/visit',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:place.id})});
      if(!r.ok)return; const d=await r.json();
      if(d.visited_ids) { visited.clear(); d.visited_ids.forEach(x=>visited.add(x)); }
      const pin=pinEls.get(place.id); if(pin)pin.classList.add('visited');
      visitedCount.textContent=d.visited_count ?? visited.size; passportProgress.style.width=`${Math.round(100*(d.visited_count??visited.size)/47)}%`;
      applyFilters();
      const vp=drawerContent.querySelector('.japan-visited-pill'); if(vp)vp.classList.add('shown');
      if(d.first_time){ showStamp(place); if(window.KotobaLearn)KotobaLearn.toast(`Passport stamp: ${place.prefecture_en} · +${d.xp_awarded||12} XP`); }
    }catch(_){ }
  }

  function showStamp(place){
    stampName.textContent=`${place.prefecture_en} explored!`; stampPop.hidden=false; stampPop.classList.remove('play'); void stampPop.offsetWidth; stampPop.classList.add('play');
    clearTimeout(stampPop._t); stampPop._t=setTimeout(()=>{stampPop.classList.remove('play');stampPop.hidden=true;},1800);
  }

  function startMiniQuiz(){
    const targetWords=shuffle(currentWords).slice(0,3);
    quizState={idx:0,score:0,words:targetWords}; renderQuizQuestion();
    const box=document.getElementById('japan-mini-quiz'); box.hidden=false; box.scrollIntoView({behavior:'smooth',block:'nearest'});
  }

  function renderQuizQuestion(){
    const box=document.getElementById('japan-mini-quiz'); if(!box||!quizState)return;
    if(quizState.idx>=quizState.words.length){
      box.innerHTML=`<div class="japan-quiz-finish"><span>旅</span><h4>${quizState.score} / ${quizState.words.length}</h4><p>${quizState.score===quizState.words.length?'Perfect stop! These words are now in your learning history.':'Good practice. Any miss is now available in your Mistake Notebook and Smart Review.'}</p><button type="button" class="btn-ghost" id="japan-quiz-again">Quiz again</button></div>`;
      document.getElementById('japan-quiz-again').onclick=startMiniQuiz; return;
    }
    const word=quizState.words[quizState.idx];
    const all=[...currentWords,...((payload.common_words||{})[level]||[])];
    const distract=shuffle(all.filter(w=>w.en!==word.en && w.jp!==word.jp)).slice(0,3).map(w=>w.en);
    const options=shuffle([word.en,...distract]);
    box.innerHTML=`<div class="japan-quiz-head"><span>${quizState.idx+1} / ${quizState.words.length}</span><strong>What does this mean?</strong></div><div class="japan-quiz-prompt">${esc(word.jp)}<small>${esc(word.reading)}</small></div><div class="japan-quiz-options">${options.map(o=>`<button type="button" data-answer="${esc(o)}">${esc(o)}</button>`).join('')}</div><div class="japan-quiz-feedback" id="japan-quiz-feedback"></div>`;
    box.querySelectorAll('[data-answer]').forEach(btn=>btn.addEventListener('click',()=>answerQuiz(btn,word)));
  }

  async function answerQuiz(btn,word){
    const box=document.getElementById('japan-mini-quiz'); if(!box||box.dataset.locked==='1')return; box.dataset.locked='1';
    const correct=btn.dataset.answer===word.en; if(correct)quizState.score++;
    box.querySelectorAll('[data-answer]').forEach(b=>{b.disabled=true;if(b.dataset.answer===word.en)b.classList.add('correct');else if(b===btn)b.classList.add('wrong')});
    const feedback=document.getElementById('japan-quiz-feedback'); feedback.innerHTML=`<strong>${correct?'✓ Correct':'Not quite'}</strong><span>${esc(word.jp)}（${esc(word.reading)}）— ${esc(word.en)}</span>`;
    if(window.KotobaLearn){
      await KotobaLearn.record({kind:'japan-word',id:`${selected.id}:${word.jp}`,front:word.jp,reading:word.reading,meaning:word.en,answer:word.en,correct,chosen:btn.dataset.answer,level:levelLabel(),sub:`Japan Explorer · ${selected.prefecture_en}`,explanation:`${word.jp}（${word.reading}） means “${word.en}”. You met it while exploring ${selected.prefecture_en}.`});
    }
    setTimeout(()=>{quizState.idx++; box.dataset.locked='0'; renderQuizQuestion();},900);
  }

  surpriseBtn.addEventListener('click',()=>{
    let pool=places.filter(p=>!visited.has(p.id)); if(!pool.length)pool=places; selectPlace(pool[Math.floor(Math.random()*pool.length)]);
  });
  unvisitedBtn.addEventListener('click',()=>{unvisitedOnly=!unvisitedOnly;unvisitedBtn.classList.toggle('active',unvisitedOnly);unvisitedBtn.textContent=unvisitedOnly?'Showing unvisited · clear':'Show unvisited';applyFilters()});

  renderList(places); applyFilters();
  const hashId=decodeURIComponent((location.hash||'').replace(/^#/,''));
  if(hashId){ const fromHash=places.find(p=>p.id===hashId); if(fromHash) setTimeout(()=>selectPlace(fromHash),120); }
})();
