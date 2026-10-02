/* Roadmap chapter: learn -> practise -> celebrate.
   v3 keeps the original lesson data and completion API, but adds a clear
   phase/progress indicator, combo feedback, and lightweight motion. */
(function () {
  'use strict';

  var vocab = JSON.parse(document.getElementById('rm-vocab-data').textContent);
  var quiz = JSON.parse(document.getElementById('rm-quiz-data').textContent);
  var $ = function (id) { return document.getElementById(id); };

  var PASS_PCT = 60;
  var panels = { learn: $('rm-learn'), quiz: $('rm-quiz'), done: $('rm-done') };
  var progressFill = $('rm-lesson-progress-fill');
  var phaseLabel = $('rm-phase-label');

  function setProgress(pct, label) {
    if (progressFill) progressFill.style.width = Math.max(0, Math.min(100, pct)) + '%';
    if (phaseLabel && label) phaseLabel.textContent = label;
  }

  function show(name) {
    Object.keys(panels).forEach(function (k) { panels[k].hidden = (k !== name); });
    if (name === 'done') setProgress(100, 'Complete');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  function pop(el, cls) {
    if (!el) return;
    el.classList.remove(cls);
    void el.offsetWidth;
    el.classList.add(cls);
  }

  function sparkle(anchor) {
    if (!anchor || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    var rect = anchor.getBoundingClientRect();
    for (var i = 0; i < 6; i++) {
      var p = document.createElement('span');
      p.className = 'rm-spark';
      p.textContent = i % 2 ? '•' : '✦';
      p.style.left = (rect.left + rect.width / 2) + 'px';
      p.style.top = (rect.top + window.scrollY + rect.height / 2) + 'px';
      p.style.setProperty('--dx', ((i - 2.5) * 16) + 'px');
      p.style.setProperty('--dy', (-28 - (i % 3) * 12) + 'px');
      document.body.appendChild(p);
      setTimeout(function (node) { return function () { node.remove(); }; }(p), 650);
    }
  }

  // ---- step 1: word cards ----
  var ci = 0;
  function renderCard() {
    if (!vocab.length) return;
    var w = vocab[ci];
    $('rm-card-count').textContent = 'Learn ' + (ci + 1) + ' of ' + vocab.length;
    $('rm-word-jp').textContent = w.jp;
    $('rm-word-reading').textContent = w.reading;
    $('rm-word-romaji').textContent = w.romaji;
    $('rm-word-meaning').textContent = w.meaning;
    var sp = $('rm-word-speak'); if (sp) sp.onclick = function () { if (window.KotobaSpeech) KotobaSpeech.speak(w.jp); };
    $('rm-prev').disabled = ci === 0;
    $('rm-next').textContent = ci === vocab.length - 1 ? 'Start practice' : 'Next';
    setProgress(Math.round(((ci + 1) / Math.max(vocab.length, 1)) * 42), 'Learn');
    pop($('rm-word-card'), 'rm-card-enter');
  }

  $('rm-prev').addEventListener('click', function () {
    if (ci > 0) { ci--; renderCard(); }
  });
  $('rm-next').addEventListener('click', function () {
    if (ci < vocab.length - 1) { ci++; renderCard(); }
    else startQuiz();
  });

  // ---- step 2: quiz ----
  var qi = 0, right = 0, answered = false, combo = 0;
  var TYPE_LABEL = {
    meaning: 'What does this mean?',
    reading: 'How do you read this?',
    fillblank: 'Fill in the blank',
    radical: 'Which radical is inside this kanji?',
    reverse: 'Which Japanese word means this?'
  };

  function updateCombo() {
    var el = $('rm-combo');
    if (!el) return;
    el.hidden = combo < 2;
    if (combo >= 2) {
      el.textContent = '🔥 ' + combo + '× combo';
      pop(el, 'rm-combo-pop');
    }
  }

  function startQuiz() {
    if (!quiz.length) { finish(); return; }
    qi = 0; right = 0; combo = 0;
    show('quiz');
    renderQuestion();
  }

  function renderQuestion() {
    var q = quiz[qi];
    answered = false;
    $('rm-q-count').textContent = 'Practice ' + (qi + 1) + ' of ' + quiz.length;
    $('rm-q-type').textContent = q.label || TYPE_LABEL[q.type] || '';
    $('rm-q-prompt').textContent = q.prompt;
    var sub = '';
    if (q.type === 'fillblank' || q.type === 'radical') sub = q.english;
    $('rm-q-sub').textContent = sub;
    $('rm-feedback').textContent = '';
    $('rm-feedback').className = 'rm-feedback';
    $('rm-continue').hidden = true;

    setProgress(45 + Math.round((qi / Math.max(quiz.length, 1)) * 50), 'Practice');

    var box = $('rm-options');
    box.innerHTML = '';
    q.options.forEach(function (opt, index) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'rm-option';
      b.textContent = opt;
      b.style.setProperty('--option-delay', (index * 35) + 'ms');
      b.addEventListener('click', function () { choose(b, opt); });
      box.appendChild(b);
    });
    pop($('rm-q-prompt'), 'rm-question-enter');
  }

  function choose(btn, opt) {
    if (answered) return;
    answered = true;
    var q = quiz[qi];
    var ok = opt === q.correct;
    if (ok) {
      right++;
      combo++;
    } else {
      combo = 0;
    }
    updateCombo();

    var correctButton = null;
    document.querySelectorAll('.rm-option').forEach(function (b) {
      b.disabled = true;
      if (b.textContent === q.correct) {
        b.classList.add('rm-correct');
        correctButton = b;
      }
    });

    if (ok) {
      pop(btn, 'rm-answer-pop');
      sparkle(btn);
    } else {
      btn.classList.add('rm-wrong');
      pop(btn, 'rm-answer-shake');
    }

    if (window.KotobaLearn) KotobaLearn.record({kind:'roadmap', id: window.RM_CHAPTER_ID + ':' + qi + ':' + q.prompt, front:q.prompt, prompt:q.prompt, answer:q.correct, chosen:opt, correct:ok, quality:ok?4:1, explanation:q.explain||''});
    var fb = $('rm-feedback');
    fb.textContent = (ok ? 'Correct!' : 'Not quite — the answer is ' + q.correct + '.') + (q.explain ? '\n' + q.explain : '');
    fb.className = 'rm-feedback ' + (ok ? 'rm-fb-ok' : 'rm-fb-bad');
    if (window.Sfx) { try { (ok ? Sfx.correct : Sfx.wrong)(); } catch (e) {} }
    $('rm-continue').hidden = false;
    $('rm-continue').textContent = qi === quiz.length - 1 ? 'Finish' : 'Continue';
  }

  $('rm-continue').addEventListener('click', function () {
    if (qi < quiz.length - 1) { qi++; renderQuestion(); }
    else finish();
  });

  // ---- step 3: finish ----
  function finish() {
    var total = quiz.length || 1;
    var pct = Math.round(100 * right / total);
    var passed = !quiz.length || pct >= PASS_PCT;
    show('done');
    $('rm-done-score').textContent = quiz.length
      ? 'Accuracy: ' + pct + '% · ' + right + ' of ' + quiz.length + ' correct.'
      : 'Nice work.';

    var note = $('rm-done-note');
    if (note) {
      note.textContent = passed
        ? (pct >= 90 ? 'Excellent recall. Move on while this is fresh!' : 'Good progress. This chapter is now part of your learning path.')
        : 'You need ' + PASS_PCT + '% to complete this chapter. Review the explanations and try once more.';
    }

    if (window.Sfx) { try { Sfx.complete(); } catch (e) {} }
    if (window.showLessonReaction) showLessonReaction(pct);

    if (!passed) {
      $('rm-next-chapter').textContent = 'Try again';
      $('rm-next-chapter').href = window.location.href;
      return;
    }
    if (window.markStreakActive) markStreakActive();
    if (window.KotobaLearn) KotobaLearn.action('lessons');
    try { sessionStorage.setItem('kotoba:roadmap-just-completed', window.RM_CHAPTER_ID); } catch (e) {}
    fetch('/api/roadmap/complete', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ chapter_id: window.RM_CHAPTER_ID })
    }).then(function (r) { return r.json(); }).then(function (data) {
      if (data && data.next_chapter_id) {
        $('rm-next-chapter').href = '/roadmap/' + data.next_chapter_id;
        $('rm-next-chapter').textContent = 'Next lesson';
      } else {
        $('rm-next-chapter').href = '/roadmap';
        $('rm-next-chapter').textContent = 'See completed path';
      }
    }).catch(function () {});
  }

  // The Grand Review has no word cards: it opens on a summary panel.
  var startBtn = $('rm-start-review');
  if (startBtn) startBtn.addEventListener('click', startQuiz);
  if (vocab.length) renderCard();
  else if (!startBtn) startQuiz();
  else setProgress(8, 'Review');
})();
