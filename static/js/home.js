(function () {
  'use strict';
  var KEY = 'kotoba:onboarding:v3';
  var GOAL_KEY = 'kotoba:daily-goal-minutes';
  var goal = 10;

  try { goal = Number(localStorage.getItem(GOAL_KEY)) || 10; } catch (e) {}
  var goalPill = document.getElementById('home-goal-pill');
  if (goalPill) goalPill.textContent = 'Daily goal · ' + goal + ' min';

  var overlay = document.getElementById('onboarding-overlay');
  if (!overlay) return;
  try {
    if (localStorage.getItem(KEY)) return;
  } catch (e) {}

  var chips = document.querySelectorAll('#goal-chips [data-goal]');
  chips.forEach(function (chip) {
    var n = Number(chip.getAttribute('data-goal')) || 10;
    chip.classList.toggle('active', n === goal);
    chip.addEventListener('click', function () {
      chips.forEach(function (x) { x.classList.remove('active'); });
      chip.classList.add('active');
      goal = n;
    });
  });

  function saveSetup() {
    try {
      localStorage.setItem(KEY, '1');
      localStorage.setItem(GOAL_KEY, String(goal));
    } catch (e) {}
  }

  document.querySelectorAll('.onboarding-levels [data-start]').forEach(function (button) {
    button.addEventListener('click', function () {
      saveSetup();
      var href = button.getAttribute('data-start');
      var match = /^\/roadmap\/([^/?#]+)/.exec(href || '');
      var roadmapStart = button.getAttribute('data-roadmap-start') || (match ? decodeURIComponent(match[1]) : '');
      if (!roadmapStart) {
        window.location.href = href;
        return;
      }
      fetch('/api/roadmap/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ chapter_id: roadmapStart })
      }).catch(function () {}).finally(function () {
        window.location.href = href;
      });
    });
  });

  var skip = document.getElementById('onboarding-skip');
  if (skip) skip.addEventListener('click', function () {
    saveSetup();
    overlay.hidden = true;
  });

  overlay.addEventListener('click', function (event) {
    if (event.target === overlay) {
      saveSetup();
      overlay.hidden = true;
    }
  });

  setTimeout(function () { overlay.hidden = false; }, 250);
})();
