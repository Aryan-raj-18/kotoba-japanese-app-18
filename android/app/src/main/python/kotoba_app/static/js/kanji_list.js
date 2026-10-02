document.addEventListener('DOMContentLoaded', () => {
  const input = document.getElementById('kanji-filter');
  const cards = document.querySelectorAll('.kanji-card');
  if (!input) return;
  input.addEventListener('input', () => {
    const q = input.value.trim().toLowerCase();
    cards.forEach(card => {
      const hay = card.dataset.search || '';
      card.style.display = (!q || hay.includes(q)) ? '' : 'none';
    });
  });
});
