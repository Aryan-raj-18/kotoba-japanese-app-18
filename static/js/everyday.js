document.addEventListener('DOMContentLoaded', () => {
  const filterInput = document.getElementById('everyday-filter');
  const tabs = document.querySelectorAll('.cat-tab');
  const rows = document.querySelectorAll('.everyday-row');
  const blocks = document.querySelectorAll('.category-block');
  const levelButtons = document.querySelectorAll('.everyday-level-btn');
  let activeCat = 'all';
  let activeDifficulty = 'all';

  // ---------------- filtering ----------------
  function applyFilters() {
    const q = (filterInput.value || '').trim().toLowerCase();
    blocks.forEach(block => {
      const catMatches = activeCat === 'all' || block.dataset.cat === activeCat;
      let visibleInBlock = 0;
      block.querySelectorAll('.everyday-row').forEach(row => {
        const textMatches = !q || (row.dataset.search || '').includes(q);
        const levelMatches = activeDifficulty === 'all' || row.dataset.difficulty === activeDifficulty;
        const show = catMatches && textMatches && levelMatches;
        row.style.display = show ? '' : 'none';
        if (show) visibleInBlock++;
      });
      block.style.display = visibleInBlock > 0 ? '' : 'none';
    });
  }

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      activeCat = tab.dataset.cat;
      applyFilters();
    });
  });

  filterInput.addEventListener('input', applyFilters);

  levelButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      levelButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      activeDifficulty = btn.dataset.difficulty || 'all';
      applyFilters();
    });
  });

  // ---------------- word detail modal ----------------
  const modal = document.getElementById('word-modal');
  const convoEl = document.getElementById('modal-convo');

  function setText(id, value) {
    document.getElementById(id).textContent = value || '';
  }

  function renderModal(entry) {
    setText('modal-emoji', entry.emoji);
    setText('modal-word', entry.word);
    setText('modal-reading', `${entry.reading}  ·  ${entry.romaji}`);
    setText('modal-meaning', entry.meaning);
    const rank = entry.frequency_rank ? ` · Common #${entry.frequency_rank}` : '';
    const diff = entry.difficulty ? ` · ${entry.difficulty[0].toUpperCase() + entry.difficulty.slice(1)}` : '';
    setText('modal-category', `${entry.category}${diff}${rank}`);
    setText('modal-usage', entry.usage_note);
    const speakBtn = document.getElementById('modal-speak');
    if (speakBtn) speakBtn.onclick = () => window.KotobaSpeech && KotobaSpeech.speak(entry.word);
    const favBtn = document.getElementById('modal-favorite');
    if (favBtn) {
      favBtn.onclick = async () => {
        if (!window.KotobaLearn) return;
        const r = await KotobaLearn.favorite({kind:'vocab', id:entry.word, front:entry.word, reading:entry.reading || entry.romaji || '', meaning:entry.meaning, url:'/everyday'});
        if (r) { favBtn.textContent = r.added ? '★ Saved' : '☆ Save'; KotobaLearn.toast(r.added ? 'Saved to Favorites' : 'Removed from Favorites'); }
      };
    }

    convoEl.innerHTML = '';
    (entry.conversation || []).forEach(line => {
      const wrap = document.createElement('div');
      wrap.className = 'convo-line convo-' + line.speaker.toLowerCase();

      const who = document.createElement('span');
      who.className = 'convo-speaker';
      who.textContent = line.speaker;
      wrap.appendChild(who);

      const body = document.createElement('div');
      body.className = 'convo-body';
      [
        ['convo-kanji', line.kanji],
        ['convo-hiragana', line.hiragana],
        ['convo-romaji', line.romaji],
        ['convo-english', line.english],
      ].forEach(([cls, text]) => {
        const p = document.createElement('p');
        p.className = cls;
        p.textContent = text;
        body.appendChild(p);
      });
      const listen = document.createElement('button'); listen.type='button'; listen.className='line-speak'; listen.textContent='🔊'; listen.setAttribute('aria-label','Listen'); listen.onclick=()=>window.KotobaSpeech&&KotobaSpeech.speak(line.kanji); body.appendChild(listen);
      wrap.appendChild(body);
      convoEl.appendChild(wrap);
    });
  }

  function closeModal() {
    modal.hidden = true;
    document.body.style.overflow = '';
  }

  rows.forEach(row => {
    row.addEventListener('click', async () => {
      const idx = row.dataset.idx;
      modal.hidden = false;
      document.body.style.overflow = 'hidden';
      convoEl.innerHTML = '<p class="convo-loading">Loading...</p>';
      try {
        const res = await fetch(`/api/everyday/${idx}`);
        if (!res.ok) throw new Error('bad status ' + res.status);
        renderModal(await res.json());
      } catch (err) {
        convoEl.innerHTML = '<p class="convo-loading">Could not load this word.</p>';
      }
    });
  });

  document.getElementById('modal-close').addEventListener('click', closeModal);
  modal.addEventListener('click', (e) => { if (e.target === modal) closeModal(); });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && !modal.hidden) closeModal();
  });
});
