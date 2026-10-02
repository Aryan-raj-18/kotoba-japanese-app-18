/* Kotoba v3 lesson reaction.
   Uses one original CSS-drawn companion (Koto) everywhere instead of
   unrelated reaction images/GIFs, keeping feedback visually consistent. */
(function () {
  'use strict';

  var AUTO_DISMISS_MS = 3000;
  var dismissTimer = null;

  function dismiss(overlay) {
    if (!overlay || !overlay.isConnected) return;
    if (dismissTimer) { clearTimeout(dismissTimer); dismissTimer = null; }
    overlay.classList.add('reaction-leaving');
    setTimeout(function () { overlay.remove(); }, 200);
  }

  function mascot(kind) {
    var m = document.createElement('div');
    m.className = 'koto-mascot reaction-koto ' + (kind === 'celebrate' ? 'koto-celebrate' : 'koto-encourage');
    m.setAttribute('aria-hidden', 'true');
    m.innerHTML = '<span class="koto-ear koto-ear-left"></span>' +
      '<span class="koto-ear koto-ear-right"></span>' +
      '<span class="koto-eye koto-eye-left"></span>' +
      '<span class="koto-eye koto-eye-right"></span>' +
      '<span class="koto-mouth"></span>' +
      '<span class="koto-mark">言</span>' +
      '<span class="koto-arm koto-arm-left"></span>' +
      '<span class="koto-arm koto-arm-right"></span>';
    return m;
  }

  window.showLessonReaction = function (percentage) {
    var celebrate = percentage >= 60;
    var existing = document.querySelector('.reaction-overlay');
    if (existing) dismiss(existing);

    var overlay = document.createElement('div');
    overlay.className = 'reaction-overlay';
    overlay.setAttribute('role', 'status');

    var card = document.createElement('div');
    card.className = 'reaction-card';
    card.appendChild(mascot(celebrate ? 'celebrate' : 'encourage'));

    if (celebrate) {
      var confetti = document.createElement('div');
      confetti.className = 'koto-confetti';
      confetti.setAttribute('aria-hidden', 'true');
      confetti.innerHTML = '<i>✦</i><i>●</i><i>✿</i><i>✦</i><i>●</i>';
      card.appendChild(confetti);
    }

    var title = document.createElement('p');
    title.className = 'reaction-title';
    title.textContent = celebrate ? 'やったね！' : 'もう一回！';

    var sub = document.createElement('p');
    sub.className = 'reaction-sub';
    sub.textContent = celebrate
      ? (percentage >= 90 ? 'Excellent work — that was strong!' : 'Nice work. Keep the momentum going!')
      : 'Review the explanation and try again — you are learning.';

    card.appendChild(title);
    card.appendChild(sub);
    overlay.appendChild(card);

    overlay.addEventListener('click', function () { dismiss(overlay); });
    card.addEventListener('click', function (e) { e.stopPropagation(); });
    document.body.appendChild(overlay);
    dismissTimer = setTimeout(function () { dismiss(overlay); }, AUTO_DISMISS_MS);
  };
})();
