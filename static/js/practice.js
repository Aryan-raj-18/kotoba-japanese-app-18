document.addEventListener('DOMContentLoaded', () => {
  const panels = {
    intro: document.getElementById('panel-intro'),
    learn: document.getElementById('panel-learn'),
    quiz: document.getElementById('panel-quiz'),
    explain: document.getElementById('panel-explain'),
    done: document.getElementById('panel-done'),
  };

  function showPanel(name) {
    Object.entries(panels).forEach(([key, el]) => { el.hidden = key !== name; });
  }

  let words = [];        // the words for this round
  let learnIdx = 0;
  let quizIdx = 0;
  let correctCount = 0;
  let selectedLevel = 'mixed';
  let selectedCount = 10;
  let selectedMode = 'kanji';

  // ---------------- level / count pickers ----------------
  document.querySelectorAll('.level-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.level-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      selectedLevel = btn.dataset.level;
    });
  });
  document.querySelectorAll('.mode-sel').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.mode-sel').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      selectedMode = btn.dataset.mode;
    });
  });
  document.querySelectorAll('.count-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.count-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      selectedCount = parseInt(btn.dataset.count, 10);
    });
  });

  // ---------------- start ----------------
  document.getElementById('start-btn').addEventListener('click', startRound);
  document.getElementById('restart-btn').addEventListener('click', () => {
    showPanel('intro');
  });

  async function startRound() {
    const res = await fetch('/api/practice/new_session', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ difficulty: selectedLevel, count: selectedCount, mode: selectedMode }),
    });
    const data = await res.json();
    words = data.words;
    learnIdx = 0;
    quizIdx = 0;
    correctCount = 0;
    showPanel('learn');
    renderLearnCard();
  }

  // ---------------- learn phase ----------------
  function renderLearnCard() {
    const w = words[learnIdx];
    document.getElementById('learn-kanji').textContent = w.kanji;
    document.getElementById('learn-reading').textContent = w.reading || w.romaji || '';
    document.getElementById('learn-meaning').textContent = w.meaning;
    document.getElementById('learn-on').textContent = w.on_yomi || '—';
    document.getElementById('learn-kun').textContent = w.kun_yomi || '—';
    document.getElementById('learn-progress').textContent = `${learnIdx + 1} / ${words.length}`;
    document.getElementById('learn-prev').disabled = learnIdx === 0;
    document.getElementById('learn-next').textContent = (learnIdx === words.length - 1) ? 'Start quiz →' : 'Next →';
  }

  document.getElementById('learn-prev').addEventListener('click', () => {
    if (learnIdx > 0) { learnIdx--; renderLearnCard(); }
  });
  document.getElementById('learn-next').addEventListener('click', () => {
    if (learnIdx < words.length - 1) {
      learnIdx++;
      renderLearnCard();
    } else {
      quizIdx = 0;
      showPanel('quiz');
      renderQuiz();
    }
  });

  // ---------------- quiz phase ----------------
  async function renderQuiz() {
    const w = words[quizIdx];
    document.getElementById('quiz-progress').textContent = `${quizIdx + 1} / ${words.length}`;
    document.getElementById('quiz-feedback').hidden = true;

    const res = await fetch(`/api/practice/quiz/${w.kanji_id}?mode=${selectedMode}`);
    const q = await res.json();

    document.getElementById('quiz-question').textContent = q.question;
    const big = document.getElementById('quiz-sentence');
    big.textContent = q.prompt_big || '';
    big.hidden = !q.prompt_big;
    document.getElementById('quiz-translation').textContent = q.hint || '';

    const optionsEl = document.getElementById('quiz-options');
    optionsEl.innerHTML = '';
    q.options.forEach(opt => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'quiz-option';
      btn.textContent = opt;
      btn.addEventListener('click', () => handleAnswer(w, opt, q.correct_word, btn, optionsEl));
      optionsEl.appendChild(btn);
    });
  }

  async function handleAnswer(word, answer, correctWord, btn, optionsEl) {
    // lock further clicks
    optionsEl.querySelectorAll('.quiz-option').forEach(b => b.disabled = true);

    const res = await fetch('/api/practice/check', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ kanji_id: word.kanji_id, answer, correct_word: correctWord }),
    });
    const result = await res.json();
    if (window.KotobaLearn) KotobaLearn.record({
      kind:'mixed-practice', id:String(word.kanji_id), front:word.word || word.kanji || String(word.kanji_id),
      prompt:document.getElementById('quiz-question') ? document.getElementById('quiz-question').textContent : '',
      answer:correctWord, chosen:answer, correct:!!result.correct, quality:result.correct?4:1,
      meaning:word.meaning || '', explanation: result.explanation ? (typeof result.explanation === 'string' ? result.explanation : JSON.stringify(result.explanation)) : ''
    });

    if (result.correct) {
      btn.classList.add('correct');
      correctCount++;
      if (window.Sfx) Sfx.correct();
    } else {
      btn.classList.add('incorrect');
      optionsEl.querySelectorAll('.quiz-option').forEach(b => {
        if (b.textContent === correctWord) b.classList.add('correct');
      });
      if (window.Sfx) Sfx.incorrect();
    }

    // Right or wrong, show the full explanation after a brief pause so
    // the person sees which option was correct first.
    setTimeout(() => showExplanation(result), 650);
  }

  function showExplanation(result) {
    const exp = result.explanation;
    const banner = document.getElementById('result-banner');
    if (result.correct) {
      banner.textContent = '✓ Correct!';
      banner.className = 'result-banner correct';
    } else {
      banner.textContent = `✗ Not quite — you answered "${result.your_answer}"`;
      banner.className = 'result-banner incorrect';
    }

    document.getElementById('explain-kanji').textContent = exp.kanji;
    document.getElementById('explain-word').textContent = `${exp.word}  (${exp.reading || exp.romaji})`;
    document.getElementById('explain-meaning').textContent = `${exp.meaning} — from kanji meaning "${exp.kanji_meaning}"`;
    document.getElementById('explain-on').textContent = exp.on_yomi;
    document.getElementById('explain-kun').textContent = exp.kun_yomi;
    document.getElementById('explain-strokes').textContent = exp.strokes;
    document.getElementById('explain-sentence-kanji').textContent = exp.sentence_kanji;
    document.getElementById('explain-sentence-hiragana').textContent = exp.sentence_hiragana;
    document.getElementById('explain-sentence-romaji').textContent = exp.sentence_romaji;
    document.getElementById('explain-sentence-en').textContent = exp.sentence_en;
    document.getElementById('explain-usage').textContent = exp.usage_note;
    showPanel('explain');
  }

  document.getElementById('continue-btn').addEventListener('click', () => {
    advanceQuiz();
  });

  function advanceQuiz() {
    if (quizIdx < words.length - 1) {
      quizIdx++;
      showPanel('quiz');
      renderQuiz();
    } else {
      document.getElementById('done-score').textContent = `You got ${correctCount} out of ${words.length} correct.`;
      showPanel('done');
      if (window.Sfx) Sfx.complete();
      if (window.showLessonReaction) showLessonReaction((correctCount / words.length) * 100);
      markStreakActive();
    }
  }
});
