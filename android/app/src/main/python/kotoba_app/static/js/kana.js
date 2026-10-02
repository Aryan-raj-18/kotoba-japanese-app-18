document.addEventListener('DOMContentLoaded', () => {
  const chartEl = document.getElementById('kana-chart');
  const flashEl = document.getElementById('flash-mode');
  const modeBtns = document.querySelectorAll('.mode-btn');

  modeBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      modeBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      if (btn.dataset.mode === 'chart') {
        chartEl.hidden = false;
        flashEl.hidden = true;
      } else {
        chartEl.hidden = true;
        flashEl.hidden = false;
      }
    });
  });

  // tap a tile to see it big, with its romaji reading
  const kanaModal = document.getElementById('kana-modal');
  const kanaModalChar = document.getElementById('modal-kana-char');
  const kanaModalRomaji = document.getElementById('modal-kana-romaji');

  function openKanaModal(tile) {
    kanaModalChar.textContent = tile.dataset.char;
    kanaModalRomaji.textContent = tile.dataset.romaji;
    kanaModal.hidden = false;
    document.body.style.overflow = 'hidden';
    if (window.Sfx) Sfx.tap();
    if (window.KotobaSpeech) KotobaSpeech.speak(tile.dataset.char, .82);
  }
  function closeKanaModal() {
    kanaModal.hidden = true;
    document.body.style.overflow = '';
  }

  document.querySelectorAll('.kana-tile').forEach(tile => {
    tile.addEventListener('click', () => openKanaModal(tile));
  });
  document.getElementById('kana-modal-close').addEventListener('click', closeKanaModal);
  document.getElementById('kana-listen').addEventListener('click', () => { if (window.KotobaSpeech) KotobaSpeech.speak(kanaModalChar.textContent, .78); });
  kanaModal.addEventListener('click', (e) => { if (e.target === kanaModal) closeKanaModal(); });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && !kanaModal.hidden) closeKanaModal();
  });

  // Flashcards
  const basicKana = (window.KANA_DATA || []).filter(k => k.type === 'basic');
  let idx = 0;
  let showingRomaji = false;
  const front = document.getElementById('flash-front');
  const progress = document.getElementById('flash-progress');
  const card = document.getElementById('flashcard');

  function render() {
    if (!basicKana.length) return;
    const item = basicKana[idx];
    front.textContent = showingRomaji ? item.romaji : item.char;
    front.classList.toggle('showing-romaji', showingRomaji);
    progress.textContent = `${idx + 1} / ${basicKana.length}`;
  }

  if (card) {
    card.addEventListener('click', () => {
      showingRomaji = !showingRomaji;
      if (window.Sfx) Sfx.flip();
      render();
    });
    document.getElementById('flash-next').addEventListener('click', () => {
      idx = (idx + 1) % basicKana.length;
      showingRomaji = false;
      render();
    });
    document.getElementById('flash-prev').addEventListener('click', () => {
      idx = (idx - 1 + basicKana.length) % basicKana.length;
      showingRomaji = false;
      render();
    });
    render();
  }
});
