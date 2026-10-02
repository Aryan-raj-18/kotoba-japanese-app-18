// Opens a bigger, clearer view of a kanji when its card is tapped - the
// grid tiles are small, so this is where the actual reading happens.
document.addEventListener('DOMContentLoaded', () => {
  const modal = document.getElementById('kanji-modal');
  const cards = document.querySelectorAll('.jlpt-entry-card');
  if (!modal || !cards.length) return;

  const charEl = document.getElementById('modal-kanji-char');
  const onEl = document.getElementById('modal-kanji-on');
  const kunEl = document.getElementById('modal-kanji-kun');
  const meaningEl = document.getElementById('modal-kanji-meaning');
  const levelBadge = document.getElementById('modal-kanji-level-badge');
  const diffBadge = document.getElementById('modal-kanji-diff-badge');

  function openModal(card) {
    charEl.textContent = card.dataset.kanji;
    onEl.textContent = `音 (on) ${card.dataset.on}`;
    kunEl.textContent = `訓 (kun) ${card.dataset.kun}`;
    meaningEl.textContent = card.dataset.meaning;
    levelBadge.textContent = `JLPT ${card.dataset.level}`;
    levelBadge.className = 'jlpt-badge jlpt-badge-' + card.dataset.level;
    diffBadge.textContent = card.dataset.difficulty;
    diffBadge.className = 'jlpt-badge jlpt-badge-' + card.dataset.difficulty;
    const speak = document.getElementById('jlpt-kanji-speak'); if (speak) speak.onclick=()=>window.KotobaSpeech&&KotobaSpeech.speak(card.dataset.kanji);
    const fav = document.getElementById('jlpt-kanji-favorite'); if (fav) fav.onclick=async()=>{if(!window.KotobaLearn)return;const r=await KotobaLearn.favorite({kind:'jlpt-kanji',id:card.dataset.kanji,front:card.dataset.kanji,reading:card.dataset.kun||card.dataset.on||'',meaning:card.dataset.meaning,url:location.pathname});if(r){fav.textContent=r.added?'★ Saved':'☆ Save';KotobaLearn.toast(r.added?'Saved to Favorites':'Removed from Favorites');}};
    modal.hidden = false;
    document.body.style.overflow = 'hidden';
    if (window.Sfx) Sfx.tap();
  }

  function closeModal() {
    modal.hidden = true;
    document.body.style.overflow = '';
  }

  cards.forEach((card) => {
    card.addEventListener('click', () => openModal(card));
  });

  document.getElementById('kanji-modal-close').addEventListener('click', closeModal);
  modal.addEventListener('click', (e) => { if (e.target === modal) closeModal(); });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && !modal.hidden) closeModal();
  });
});
