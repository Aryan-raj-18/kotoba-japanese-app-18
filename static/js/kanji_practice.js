// Kanji Practice — a 4-option multiple-choice quiz over every kanji in the
// deck, with All/Easy/Medium/Hard categories and up to a 40-kanji round.
// No answer is marked right or wrong while the test is running; every
// attempt is collected and the full breakdown only appears once the
// round is finished.
document.addEventListener('DOMContentLoaded', () => {
  const stage = document.getElementById('mcq-stage');
  if (!stage) return;

  const panelIntro = document.getElementById('mcq-panel-intro');
  const panelQuiz = document.getElementById('mcq-panel-quiz');
  const panelResults = document.getElementById('mcq-panel-results');

  const levelOptions = document.getElementById('mcq-level-options');
  const countOptions = document.getElementById('mcq-count-options');
  const startBtn = document.getElementById('mcq-start-btn');
  const restartBtn = document.getElementById('mcq-restart-btn');

  const kanjiEl = document.getElementById('mcq-kanji');
  const optionsEl = document.getElementById('mcq-options');
  const progressEl = document.getElementById('mcq-progress');

  const scoreEl = document.getElementById('mcq-score');
  const reviewEl = document.getElementById('mcq-review');

  let level = 'all';
  let count = 20;
  let questions = [];
  let idx = 0;
  let answers = []; // { kanji, correct, chosen, right }
  let locked = false; // guards against double-clicks between questions

  function selectButtons(group, dataAttr, onPick) {
    group.querySelectorAll('button').forEach((btn) => {
      btn.addEventListener('click', () => {
        group.querySelectorAll('button').forEach((b) => b.classList.remove('active'));
        btn.classList.add('active');
        onPick(btn.dataset[dataAttr]);
      });
    });
  }
  selectButtons(levelOptions, 'level', (v) => { level = v; });
  selectButtons(countOptions, 'count', (v) => { count = parseInt(v, 10); });

  function show(panel) {
    [panelIntro, panelQuiz, panelResults].forEach((p) => { p.hidden = (p !== panel); });
  }

  async function startTest() {
    startBtn.disabled = true;
    startBtn.textContent = 'Loading…';
    try {
      const res = await fetch(`/api/kanji_quiz?level=${encodeURIComponent(level)}&count=${count}`);
      const data = await res.json();
      questions = data.questions || [];
    } catch (e) {
      questions = [];
    }
    startBtn.disabled = false;
    startBtn.textContent = 'Start test';
    if (!questions.length) return;

    idx = 0;
    answers = [];
    show(panelQuiz);
    renderQuestion();
  }

  function renderQuestion() {
    locked = false;
    const q = questions[idx];
    progressEl.textContent = `${idx + 1} / ${questions.length}`;
    kanjiEl.textContent = q.kanji;
    optionsEl.innerHTML = '';
    q.options.forEach((opt) => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'quiz-option';
      btn.textContent = opt;
      btn.addEventListener('click', () => pick(opt));
      optionsEl.appendChild(btn);
    });
  }

  function pick(chosen) {
    if (locked) return;
    locked = true;
    const q = questions[idx];
    const right = chosen === q.correct;
    answers.push({
      kanji: q.kanji,
      correct: q.correct,
      chosen,
      right,
    });
    if (window.KotobaLearn) KotobaLearn.record({kind:'kanji', id:q.kanji, front:q.kanji, answer:q.correct, meaning:q.correct, chosen, correct:right, quality:right?4:1});
    if (right) markProgress(q.kanji);
    if (idx < questions.length - 1) {
      idx++;
      renderQuestion();
    } else {
      finish();
    }
  }

  function markProgress(kanji) {
    // Fire-and-forget, same as flashcards: a failed save here shouldn't
    // interrupt the quiz. Correct answers here count toward the same
    // "kanji" deck flashcards use, since both draw from the same pool.
    fetch('/api/progress/mark', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ deck: 'kanji', front: kanji }),
    }).catch(() => {});
  }

  function finish() {
    const right = answers.filter((a) => a.right).length;
    scoreEl.textContent = `You got ${right} of ${answers.length} right.`;
    reviewEl.innerHTML = '';
    answers.forEach((a) => {
      const row = document.createElement('div');
      row.className = 'mcq-review-row ' + (a.right ? 'right' : 'wrong');

      const kEl = document.createElement('span');
      kEl.className = 'mcq-review-kanji';
      kEl.textContent = a.kanji;

      const body = document.createElement('div');
      body.className = 'mcq-review-body';
      const yourAnswer = document.createElement('div');
      yourAnswer.className = 'mcq-review-answer';
      yourAnswer.textContent = `Your answer: ${a.chosen}`;
      body.appendChild(yourAnswer);
      if (!a.right) {
        const correctAnswer = document.createElement('div');
        correctAnswer.className = 'mcq-review-correct';
        correctAnswer.textContent = `Correct: ${a.correct}`;
        body.appendChild(correctAnswer);
      }

      const mark = document.createElement('span');
      mark.className = 'mcq-review-mark';
      mark.textContent = a.right ? '✓' : '✗';

      row.appendChild(kEl);
      row.appendChild(body);
      row.appendChild(mark);
      reviewEl.appendChild(row);
    });
    show(panelResults);
    if (window.showLessonReaction) showLessonReaction((right / answers.length) * 100);
    if (window.markStreakActive) markStreakActive();
  }

  startBtn.addEventListener('click', startTest);
  restartBtn.addEventListener('click', () => show(panelIntro));
});
