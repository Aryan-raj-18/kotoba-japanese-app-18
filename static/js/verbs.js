document.addEventListener('DOMContentLoaded', () => {
  const filterInput = document.getElementById('verb-filter');
  const blocks = document.querySelectorAll('.category-block');
  const modal = document.getElementById('verb-modal');
  const table = document.getElementById('verb-forms');

  filterInput.addEventListener('input', () => {
    const q = filterInput.value.trim().toLowerCase();
    blocks.forEach(block => {
      let visible = 0;
      block.querySelectorAll('.verb-row').forEach(row => {
        const show = !q || (row.dataset.search || '').includes(q);
        row.style.display = show ? '' : 'none';
        if (show) visible++;
      });
      block.style.display = visible ? '' : 'none';
    });
  });

  document.querySelectorAll('.verb-row').forEach(row => {
    row.addEventListener('click', async () => {
      modal.hidden = false;
      document.body.style.overflow = 'hidden';
      table.innerHTML = '<tr><td>Loading...</td></tr>';
      try {
        const res = await fetch(`/api/verb/${row.dataset.idx}`);
        if (!res.ok) throw new Error(res.status);
        const v = await res.json();
        document.getElementById('verb-word').textContent = v.word;
        document.getElementById('verb-reading').textContent = v.reading;
        document.getElementById('verb-meaning').textContent = v.meaning;
        document.getElementById('verb-group').textContent = v.group_label;
        const speak = document.getElementById('verb-speak'); if (speak) speak.onclick=()=>window.KotobaSpeech&&KotobaSpeech.speak(v.word);
        const fav = document.getElementById('verb-favorite'); if (fav) fav.onclick=async()=>{if(!window.KotobaLearn)return;const out=await KotobaLearn.favorite({kind:'verb',id:v.word,front:v.word,reading:v.reading,meaning:v.meaning,url:'/verbs'});if(out){fav.textContent=out.added?'★ Saved':'☆ Save';KotobaLearn.toast(out.added?'Saved to Favorites':'Removed from Favorites');}};
        table.innerHTML = '';
        v.form_labels.forEach(([key, label]) => {
          const tr = document.createElement('tr');
          const f = v.forms[key];
          tr.innerHTML = `<th>${label}</th><td class="conj-kanji">${f.kanji}</td><td class="conj-kana">${f.kana}</td>`;
          table.appendChild(tr);
        });
      } catch (e) {
        table.innerHTML = '<tr><td>Could not load this verb.</td></tr>';
      }
    });
  });

  function close() { modal.hidden = true; document.body.style.overflow = ''; }
  document.getElementById('verb-modal-close').addEventListener('click', close);
  modal.addEventListener('click', e => { if (e.target === modal) close(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && !modal.hidden) close(); });
});
