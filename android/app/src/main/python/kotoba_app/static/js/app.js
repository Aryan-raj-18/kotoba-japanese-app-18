// Shared behavior across pages. Individual pages load their own scripts
// (kana.js, kanji_list.js, practice.js) for page-specific logic.
document.addEventListener('DOMContentLoaded', () => {

  // ------------------------------------------------------ streak badge --
  const countEl = document.getElementById('streak-count');
  const badgeEl = document.getElementById('streak-badge');
  if (countEl) {
    fetch('/api/streak')
      .then(r => r.json())
      .then(data => {
        countEl.textContent = data.current;
        badgeEl.classList.toggle('streak-cold', data.current === 0);
      })
      .catch(() => { countEl.textContent = '–'; });
  }

  // --------------------------------------------------------- nav strip --
  // The nav scrolls sideways on its own now, so the section you're
  // actually on can start off-screen. Bring it into view on load.
  const nav = document.getElementById('site-nav');
  if (nav) {
    const active = nav.querySelector('a.active');
    if (active && active.scrollIntoView) {
      active.scrollIntoView({ block: 'nearest', inline: 'center' });
    }
  }
});

/**
 * Call this from any page to mark today as an active practice day and
 * refresh the header badge. Returns the streak info so a page can also
 * show its own "streak +1" moment if it wants to.
 */
async function markStreakActive() {
  try {
    const res = await fetch('/api/streak/mark', { method: 'POST' });
    const data = await res.json();
    const countEl = document.getElementById('streak-count');
    const badgeEl = document.getElementById('streak-badge');
    if (countEl) countEl.textContent = data.current;
    if (badgeEl) badgeEl.classList.remove('streak-cold');
    return data;
  } catch (e) {
    return null;
  }
}
