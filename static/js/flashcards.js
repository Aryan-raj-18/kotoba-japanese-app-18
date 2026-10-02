document.addEventListener('DOMContentLoaded', () => {
  const panels = {
    intro: document.getElementById('fc-intro'),
    select: document.getElementById('fc-select-run'),
    run: document.getElementById('fc-run'),
    done: document.getElementById('fc-done'),
  };
  function show(name) {
    Object.entries(panels).forEach(([k, el]) => { el.hidden = k !== name; });
  }

  let mode = 'select', deck = 'kanji', level = 'all', count = 20;
  let cards = [], idx = 0, knew = 0, flipped = false, locked = false;

  const NO_DIFFICULTY_DECKS = new Set(['hiragana', 'katakana']);
  const difficultyHeading = document.getElementById('fc-difficulty-heading');
  const difficultyOptionsEl = document.getElementById('fc-level-options');
  function updateDifficultyVisibility() {
    const hide = NO_DIFFICULTY_DECKS.has(deck.toLowerCase());
    difficultyHeading.hidden = hide;
    difficultyOptionsEl.hidden = hide;
  }

  function wire(selector, attr, setter) {
    document.querySelectorAll(selector).forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll(selector).forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        setter(btn.dataset[attr]);
      });
    });
  }
  wire('#fc-mode-options .mode-sel', 'mode', v => mode = v);
  wire('#deck-options .mode-sel', 'deck', v => { deck = v; updateDifficultyVisibility(); });
  wire('#fc-level-options .level-btn', 'level', v => level = v);
  wire('#fc-count-options .count-btn', 'count', v => count = parseInt(v, 10));
  updateDifficultyVisibility();

  // A deck this size can hold anything from a single kanji to a long
  // compound word or an English phrase ("credit card", "to be interested
  // in", …). A fixed font-size overflows the card for the longer ones, so
  // we shrink the font to fit based on the longest line of the text.
  function fitFont(el, cardEl, text, varName, fallback) {
    const raw = getComputedStyle(cardEl).getPropertyValue(varName);
    const maxSize = Number.isFinite(parseFloat(raw)) ? parseFloat(raw) : fallback;
    const longest = String(text).split('\n').reduce((m, l) => Math.max(m, l.length), 1);
    let factor = 1;
    if (longest > 2) factor = 0.78;
    if (longest > 4) factor = 0.6;
    if (longest > 6) factor = 0.46;
    if (longest > 9) factor = 0.34;
    if (longest > 13) factor = 0.26;
    if (longest > 20) factor = 0.2;
    el.style.fontSize = Math.max(12, Math.round(maxSize * factor)) + 'px';
  }

  // Radical / breakdown panel under kanji cards. `detailed` (after the card
  // is answered or flipped) adds how the kanji is built and its readings.
  function showRadical(el, rad, detailed) {
    if (!el) return;
    el.textContent = '';
    if (!rad) { el.hidden = true; return; }
    const head = document.createElement('div');
    if (rad.glyph) {
      const g = document.createElement('span');
      g.className = 'fc-rad-glyph';
      g.textContent = rad.glyph;
      head.appendChild(g);
      const t = document.createElement('span');
      t.textContent = `Radical: ${rad.meaning} (${rad.name})`;
      head.appendChild(t);
    } else {
      head.textContent = 'Kanji breakdown';
    }
    el.appendChild(head);
    if (detailed) {
      const add = (label, text) => {
        if (!text) return;
        const d = document.createElement('div');
        d.className = 'fc-rad-line';
        const b = document.createElement('strong');
        b.textContent = label + ' ';
        d.appendChild(b);
        d.appendChild(document.createTextNode(text));
        el.appendChild(d);
      };
      if (rad.meaning_full) add('Meaning:', rad.meaning_full);
      if (rad.parts) add('Built from:', `${rad.parts} \u2014 ${rad.story}`);
      else if (rad.glyph) add('Built from:', `the ${rad.meaning} radical ${rad.glyph} + another part. The radical gives the topic; the other part often hints at the sound.`);
      if (rad.position_note) add('Where the radical sits:', `it ${rad.position_note}.`);
      if (rad.on) add('On-yomi (Chinese reading):', rad.on);
      if (rad.kun) add('Kun-yomi (Japanese reading):', rad.kun);
    }
    el.hidden = false;
  }

  function markProgress(deckName, front) {
    // Fire-and-forget: a failed save here shouldn't interrupt the deck.
    // JLPT decks (N5-N1) all share one "jlpt" progress bucket on the
    // Dashboard, same as /jlpt practice does.
    const progressDeck = /^N[1-5]$/i.test(deckName) ? 'jlpt' : deckName;
    fetch('/api/progress/mark', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ deck: progressDeck, front }),
    }).catch(() => {});
  }

  // -------------------------------------------------------- flip mode --
  const face = document.getElementById('fc-face');
  const cardEl = document.getElementById('fc-card');

  function renderFlip() {
    const c = cards[idx];
    flipped = false;
    face.classList.remove('showing-romaji');
    face.textContent = c.front;
    fitFont(face, cardEl, c.front, '--fc-front-max', 76);
    showRadical(document.getElementById('fc-radical'), c.radical, false);
    document.getElementById('fc-progress').textContent = `${idx + 1} / ${cards.length}`;
    const sp = document.getElementById('fc-speak'); if (sp) sp.onclick=()=>window.KotobaSpeech&&KotobaSpeech.speak(c.front);
  }

  cardEl.addEventListener('click', () => {
    const c = cards[idx];
    flipped = !flipped;
    if (window.Sfx) Sfx.flip();
    if (flipped) {
      const backText = c.sub ? `${c.back}\n${c.sub}` : c.back;
      face.textContent = backText;
      face.classList.add('showing-romaji');
      fitFont(face, cardEl, backText, '--fc-back-max', 36);
      showRadical(document.getElementById('fc-radical'), c.radical, true);
    } else {
      face.textContent = c.front;
      face.classList.remove('showing-romaji');
      fitFont(face, cardEl, c.front, '--fc-front-max', 76);
      showRadical(document.getElementById('fc-radical'), c.radical, false);
    }
  });

  function advanceFlip(gotIt) {
    const current = cards[idx];
    if (gotIt) {
      knew++;
      markProgress(deck, current.front);
    }
    if (window.KotobaLearn) KotobaLearn.record({
      kind: /^N[1-5]$/i.test(deck) ? 'jlpt-kanji' : (deck === 'vocab' ? 'vocab' : 'flashcard:' + deck),
      id: current.front, front: current.front, answer: current.back, sub: current.sub || '',
      reading: current.sub || '', meaning: current.back, chosen: gotIt ? current.back : 'Did not know',
      correct: !!gotIt, quality: gotIt ? 4 : 1
    });
    if (window.Sfx) { gotIt ? Sfx.correct() : Sfx.fail(); }
    if (idx < cards.length - 1) { idx++; renderFlip(); }
    else finishRound(knew);
  }
  document.getElementById('fc-knew').addEventListener('click', () => advanceFlip(true));
  document.getElementById('fc-again').addEventListener('click', () => advanceFlip(false));

  // ------------------------------------------------------ select mode --
  const selectFace = document.getElementById('fc-select-face');
  const selectCardEl = document.getElementById('fc-select-card');
  const selectSub = document.getElementById('fc-select-sub');
  const selectOptions = document.getElementById('fc-select-options');
  const selectProgress = document.getElementById('fc-select-progress');

  function renderSelect() {
    locked = false;
    const c = cards[idx];
    selectProgress.textContent = `${idx + 1} / ${cards.length}`;
    selectFace.classList.remove('showing-romaji');
    selectFace.textContent = c.front;
    fitFont(selectFace, selectCardEl, c.front, '--fc-front-max', 76);
    selectSub.textContent = c.sub || '';
    showRadical(document.getElementById('fc-select-radical'), c.radical, false);
    const sp = document.getElementById('fc-select-speak'); if (sp) sp.onclick=()=>window.KotobaSpeech&&KotobaSpeech.speak(c.front);
    ['fc-select-feedback', 'fc-select-next'].forEach(id => { const n = document.getElementById(id); if (n) n.hidden = true; });
    selectOptions.innerHTML = '';
    c.options.forEach(opt => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'quiz-option';
      btn.textContent = opt;
      btn.addEventListener('click', () => pickSelect(btn, opt));
      selectOptions.appendChild(btn);
    });
  }

  function pickSelect(btn, chosen) {
    if (locked) return;
    locked = true;
    const c = cards[idx];
    const right = chosen === c.correct;
    // feedback right away - this mode is for learning, not testing
    selectOptions.querySelectorAll('.quiz-option').forEach(b => {
      b.disabled = true;
      if (b.textContent === c.correct) b.classList.add('correct');
      else if (b === btn) b.classList.add('incorrect');
    });
    if (right) {
      knew++;
      markProgress(deck, c.front);
    }
    if (window.KotobaLearn) KotobaLearn.record({
      kind: /^N[1-5]$/i.test(deck) ? 'jlpt-kanji' : (deck === 'vocab' ? 'vocab' : 'flashcard:' + deck),
      id: c.front, front: c.front, answer: c.correct, sub: c.sub || '', reading: c.sub || '',
      meaning: c.correct, chosen, correct: right, quality: right ? 4 : 1
    });
    if (window.Sfx) { right ? Sfx.correct() : Sfx.fail(); }
    // reveal how the kanji is built
    showRadical(document.getElementById('fc-select-radical'), c.radical, true);
    if (c.radical) {
      // kanji cards: stop and let the learner read the breakdown, then tap Next
      let fb = document.getElementById('fc-select-feedback');
      if (!fb) {
        fb = document.createElement('p');
        fb.id = 'fc-select-feedback';
        fb.className = 'fc-select-feedback';
        selectOptions.insertAdjacentElement('afterend', fb);
      }
      fb.textContent = right ? 'Correct!' : `Not quite \u2014 the answer is \u201c${c.correct}\u201d.`;
      fb.className = 'fc-select-feedback ' + (right ? 'fb-ok' : 'fb-bad');
      fb.hidden = false;
      let nx = document.getElementById('fc-select-next');
      if (!nx) {
        nx = document.createElement('button');
        nx.type = 'button';
        nx.id = 'fc-select-next';
        nx.className = 'btn-primary';
        fb.insertAdjacentElement('afterend', nx);
      }
      nx.hidden = false;
      nx.textContent = idx < cards.length - 1 ? 'Next' : 'Finish';
      nx.onclick = () => {
        nx.hidden = true; fb.hidden = true;
        if (idx < cards.length - 1) { idx++; renderSelect(); }
        else finishRound(knew);
      };
      return;
    }
    setTimeout(() => {
      if (idx < cards.length - 1) { idx++; renderSelect(); }
      else finishRound(knew);
    }, right ? 700 : 1100);
  }

  // ------------------------------------------------------------- done --
  function finishRound(rightCount) {
    document.getElementById('fc-score').textContent =
      `You knew ${rightCount} of ${cards.length}.`;
    show('done');
    if (window.Sfx) Sfx.complete();
    if (window.showLessonReaction) showLessonReaction((rightCount / cards.length) * 100);
    markStreakActive();
  }
  document.getElementById('fc-restart').addEventListener('click', () => show('intro'));

  document.getElementById('fc-start').addEventListener('click', async () => {
    const res = await fetch(`/api/flashcards_mcq?deck=${encodeURIComponent(deck)}&difficulty=${encodeURIComponent(level)}&count=${count}`);
    const data = await res.json();
    cards = (data.questions || []).map(q => ({ front: q.front, sub: q.sub, back: q.correct, options: q.options, correct: q.correct, radical: q.radical || null }));
    if (!cards.length) return;
    idx = 0; knew = 0;
    if (mode === 'flip') {
      show('run');
      renderFlip();
    } else {
      show('select');
      renderSelect();
    }
  });
});
