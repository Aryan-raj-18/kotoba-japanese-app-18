/* =====================================================================
   Kotoba — touch/tap feedback
   ---------------------------------------------------------------------
   A quick press-scale plus a small ripple that lives INSIDE whatever
   was tapped (not a fixed overlay on the page), so it can't interfere
   with scrolling, z-index, or Android WebView rendering. One delegated
   listener; nothing to wire up per-page or per-template.
   ================================================================== */
(function () {
  'use strict';

  var TARGETS = [
    'button', 'a.path-card', 'a.jlpt-level-card', '.kanji-card',
    '.quiz-option', '.level-btn', '.count-btn', '.mode-btn', '.mode-sel',
    '.theme-opt', '.kana-tile', '.streak-badge', '.jlpt-tab', '.btn-primary',
    '.btn-ghost', '.auth-link', 'a.result-row', '.flashcard', '.sub-btn'
  ].join(', ');

  var reduceMotion = window.matchMedia &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function ripple(target, x, y) {
    target.classList.add('tap-effect');
    var rect = target.getBoundingClientRect();
    var size = Math.max(rect.width, rect.height) * 1.6;
    var span = document.createElement('span');
    span.className = 'tap-effect-ripple';
    span.style.width = size + 'px';
    span.style.height = size + 'px';
    span.style.left = (x - rect.left - size / 2) + 'px';
    span.style.top = (y - rect.top - size / 2) + 'px';
    target.appendChild(span);
    var done = function () { if (span.parentNode) span.parentNode.removeChild(span); };
    span.addEventListener('animationend', done);
    setTimeout(done, 700); // safety net if animationend never fires
  }

  document.addEventListener('pointerdown', function (e) {
    if (e.pointerType === 'mouse' && e.button !== 0) return;
    var target = e.target.closest && e.target.closest(TARGETS);
    if (!target || target.disabled) return;
    target.classList.add('tap-effect'); // press-scale works even with reduced motion off for ripple
    if (reduceMotion) return;
    ripple(target, e.clientX, e.clientY);
  }, { passive: true });
})();
