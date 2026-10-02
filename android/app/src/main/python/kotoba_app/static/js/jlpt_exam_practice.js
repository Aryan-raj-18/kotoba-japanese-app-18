document.addEventListener('DOMContentLoaded', () => {
  const stage = document.getElementById('exam-stage');
  if (!stage) return;

  const level = stage.dataset.level;
  const intro = document.getElementById('exam-panel-intro');
  const quiz = document.getElementById('exam-panel-quiz');
  const results = document.getElementById('exam-panel-results');
  const categoryOptions = document.getElementById('exam-category-options');
  const countOptions = document.getElementById('exam-count-options');
  const startBtn = document.getElementById('exam-start-btn');
  const restartBtn = document.getElementById('exam-restart-btn');
  const nextBtn = document.getElementById('exam-next-btn');
  const introStatus = document.getElementById('exam-intro-status');

  const progressEl = document.getElementById('exam-progress');
  const categoryChip = document.getElementById('exam-category-chip');
  const passageEl = document.getElementById('exam-passage');
  const questionEl = document.getElementById('exam-question');
  const optionsEl = document.getElementById('exam-options');
  const feedbackEl = document.getElementById('exam-feedback');
  const feedbackTitle = document.getElementById('exam-feedback-title');
  const feedbackAnswer = document.getElementById('exam-feedback-answer');
  const feedbackNote = document.getElementById('exam-feedback-note');
  const feedbackExplanation = document.getElementById('exam-feedback-explanation');
  const scoreEl = document.getElementById('exam-score');
  const scoreNote = document.getElementById('exam-score-note');
  const reviewEl = document.getElementById('exam-review');

  let category = 'all';
  let count = 10;
  let questions = [];
  let answers = [];
  let index = 0;
  let locked = false;

  function choose(group, attr, callback) {
    group.querySelectorAll('button').forEach((btn) => {
      btn.addEventListener('click', () => {
        group.querySelectorAll('button').forEach((b) => b.classList.remove('active'));
        btn.classList.add('active');
        callback(btn.dataset[attr]);
      });
    });
  }

  choose(categoryOptions, 'category', (value) => { category = value; });
  choose(countOptions, 'count', (value) => { count = parseInt(value, 10); });

  function show(panel) {
    [intro, quiz, results].forEach((item) => { item.hidden = item !== panel; });
  }

  function appendFuriganaSegments(parent, segments) {
    (segments || []).forEach((segment) => {
      if (typeof segment === 'string') {
        parent.appendChild(document.createTextNode(segment));
        return;
      }
      if (!segment || typeof segment !== 'object' || !segment.text) return;
      if (!segment.reading) {
        parent.appendChild(document.createTextNode(segment.text));
        return;
      }
      const ruby = document.createElement('ruby');
      ruby.appendChild(document.createTextNode(segment.text));
      const rt = document.createElement('rt');
      rt.textContent = segment.reading;
      ruby.appendChild(rt);
      parent.appendChild(ruby);
    });
  }

  function renderExplanation(parent, blocks, fallbackText) {
    parent.innerHTML = '';
    const usableBlocks = Array.isArray(blocks) ? blocks.filter((b) => Array.isArray(b) && b.length) : [];
    if (usableBlocks.length) {
      usableBlocks.forEach((block) => {
        const p = document.createElement('p');
        p.className = 'exam-explanation-line';
        appendFuriganaSegments(p, block);
        parent.appendChild(p);
      });
      return true;
    }
    if (fallbackText) {
      const p = document.createElement('p');
      p.className = 'exam-explanation-line';
      p.textContent = fallbackText;
      parent.appendChild(p);
      return true;
    }
    return false;
  }

  async function startPractice() {
    startBtn.disabled = true;
    startBtn.textContent = 'Loading…';
    introStatus.textContent = 'Loading questions…';
    try {
      const params = new URLSearchParams({ level, category, count: String(count) });
      const response = await fetch(`/api/jlpt_exam_quiz?${params.toString()}`);
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || 'Could not load questions');
      questions = data.questions || [];
    } catch (err) {
      questions = [];
      introStatus.textContent = 'Could not load this practice set. Please try another category.';
    }
    startBtn.disabled = false;
    startBtn.textContent = 'Start practice';
    if (!questions.length) return;

    index = 0;
    answers = [];
    show(quiz);
    renderQuestion();
  }

  function renderQuestion() {
    locked = false;
    feedbackEl.hidden = true;
    nextBtn.textContent = index === questions.length - 1 ? 'See results' : 'Next question';

    const q = questions[index];
    progressEl.textContent = `${index + 1} / ${questions.length}`;
    categoryChip.textContent = q.category || 'Practice';
    questionEl.textContent = q.prompt;
    const listen = document.getElementById('exam-listen'); if (listen) listen.onclick=()=>window.KotobaSpeech&&KotobaSpeech.speak((q.passage ? q.passage + ' ' : '') + q.prompt);

    if (q.passage) {
      passageEl.textContent = q.passage;
      passageEl.hidden = false;
    } else {
      passageEl.textContent = '';
      passageEl.hidden = true;
    }

    optionsEl.innerHTML = '';
    q.options.forEach((option, optionIndex) => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'quiz-option exam-option';
      btn.dataset.index = String(optionIndex);
      btn.textContent = `${optionIndex + 1}. ${option}`;
      btn.addEventListener('click', () => pickAnswer(optionIndex));
      optionsEl.appendChild(btn);
    });
  }

  function pickAnswer(chosenIndex) {
    if (locked) return;
    locked = true;
    const q = questions[index];
    const right = chosenIndex === q.answer_index;

    optionsEl.querySelectorAll('.exam-option').forEach((btn) => {
      const optionIndex = parseInt(btn.dataset.index, 10);
      btn.disabled = true;
      if (optionIndex === q.answer_index) btn.classList.add('correct');
      if (optionIndex === chosenIndex && !right) btn.classList.add('incorrect');
    });

    if (window.KotobaLearn) KotobaLearn.record({
      kind: 'jlpt-exam', id: q.id || `${level}-${index}`, level, front: q.prompt, prompt: q.prompt,
      answer: q.options[q.answer_index], correct_answer: q.options[q.answer_index], chosen: q.options[chosenIndex],
      correct: right, quality: right ? 4 : 1, explanation: q.explanation || ''
    });

    answers.push({
      id: q.id,
      category: q.category,
      prompt: q.prompt,
      chosenIndex,
      chosen: q.options[chosenIndex],
      correctIndex: q.answer_index,
      correct: q.options[q.answer_index],
      explanation: q.explanation || '',
      explanationBlocks: q.explanation_blocks || [],
      right,
    });

    feedbackTitle.textContent = right ? '✓ Correct' : '✗ Not quite';
    feedbackTitle.className = `exam-feedback-title ${right ? 'correct' : 'incorrect'}`;
    feedbackAnswer.textContent = `Correct answer: ${q.answer_index + 1}. ${q.options[q.answer_index]}`;
    feedbackNote.hidden = !renderExplanation(feedbackExplanation, q.explanation_blocks, q.explanation);
    const fListen = document.getElementById('exam-feedback-listen'); if (fListen) fListen.onclick=()=>window.KotobaSpeech&&KotobaSpeech.speak(q.explanation || q.options[q.answer_index]);
    feedbackEl.hidden = false;
  }

  function nextQuestion() {
    if (!locked) return;
    if (index < questions.length - 1) {
      index += 1;
      renderQuestion();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } else {
      finish();
    }
  }

  function finish() {
    const correctCount = answers.filter((answer) => answer.right).length;
    const percent = answers.length ? Math.round((correctCount / answers.length) * 100) : 0;
    scoreEl.textContent = `${correctCount} / ${answers.length} correct (${percent}%)`;
    scoreNote.textContent = 'Review the missed questions below, including the correct sentence and reading.';
    reviewEl.innerHTML = '';

    const missed = answers.filter((answer) => !answer.right);
    if (!missed.length) {
      const perfect = document.createElement('p');
      perfect.className = 'exam-perfect';
      perfect.textContent = 'Perfect round — no missed questions to review.';
      reviewEl.appendChild(perfect);
    } else {
      missed.forEach((answer) => {
        const card = document.createElement('div');
        card.className = 'exam-review-card';

        const cat = document.createElement('span');
        cat.className = 'exam-category-chip';
        cat.textContent = answer.category || 'Practice';

        const prompt = document.createElement('p');
        prompt.className = 'exam-review-question';
        prompt.textContent = answer.prompt;

        const yours = document.createElement('p');
        yours.className = 'exam-review-wrong';
        yours.textContent = `Your answer: ${answer.chosenIndex + 1}. ${answer.chosen}`;

        const correct = document.createElement('p');
        correct.className = 'exam-review-correct';
        correct.textContent = `Correct: ${answer.correctIndex + 1}. ${answer.correct}`;

        card.appendChild(cat);
        card.appendChild(prompt);
        card.appendChild(yours);
        card.appendChild(correct);

        const explanation = document.createElement('div');
        explanation.className = 'exam-review-explanation exam-furigana';
        if (renderExplanation(explanation, answer.explanationBlocks, answer.explanation)) {
          const label = document.createElement('p');
          label.className = 'exam-feedback-label';
          label.textContent = 'Sentence & reading';
          card.appendChild(label);
          card.appendChild(explanation);
        }
        reviewEl.appendChild(card);
      });
    }

    show(results);
    if (window.showLessonReaction) window.showLessonReaction(percent);
    if (window.markStreakActive) window.markStreakActive();
  }

  startBtn.addEventListener('click', startPractice);
  nextBtn.addEventListener('click', nextQuestion);
  restartBtn.addEventListener('click', () => {
    introStatus.textContent = 'Answers are shown after each question, with sentence reading support.';
    show(intro);
  });
});
