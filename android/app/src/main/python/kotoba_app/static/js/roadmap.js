/* Roadmap path page: locked / coming-soon nodes can't be opened, so give
   a short message instead of a dead tap. */
(function () {
  'use strict';
  var toast = document.getElementById('rm-toast');
  var timer = null;

  function say(msg) {
    if (!toast) return;
    toast.textContent = msg;
    toast.hidden = false;
    clearTimeout(timer);
    timer = setTimeout(function () { toast.hidden = true; }, 2200);
  }

  document.querySelectorAll('.rm-node.rm-locked').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var title = btn.getAttribute('data-title');
      if (btn.getAttribute('data-soon') === 'yes') {
        say(title + ' is coming soon.');
      } else {
        say('Finish the chapter before this one to unlock ' + title + '.');
      }
      btn.classList.remove('rm-shake');
      void btn.offsetWidth;
      btn.classList.add('rm-shake');
    });
  });

  // Bring the next chapter to do into view.
  var current = document.querySelector('.rm-current .rm-node') || document.querySelector('.rm-node.rm-unlocked');
  if (current && current.scrollIntoView) {
    current.scrollIntoView({ block: 'center' });
  }

  // If the learner just completed a chapter and returned to the path,
  // celebrate the newly checked node once without blocking navigation.
  try {
    var justDone = sessionStorage.getItem('kotoba:roadmap-just-completed');
    if (justDone) {
      sessionStorage.removeItem('kotoba:roadmap-just-completed');
      say('Chapter complete — your path moved forward!');
    }
  } catch (e) {}

})();
