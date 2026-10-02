/* =====================================================================
   Kotoba — Writing Practice page
   ---------------------------------------------------------------------
   Three scripts, each with two ways to practise:

     Tracing  — draw the character over a faded guide and have the app
                check it (see trace.js for how the checking works)
     Keyboard — tap kana, or type romaji and watch it convert

   Kanji is tracing only.
   ================================================================== */

document.addEventListener('DOMContentLoaded', () => {

  const tracers = {};

  // --------------------------------------------------- panel switching --
  // Canvases can't size themselves while their panel is display:none, so
  // whichever tracer just became visible is re-laid-out on every switch.
  function refreshVisibleTracers() {
    Object.values(tracers).forEach(t => {
      if (t.root.offsetParent !== null) t.show(t.index);
    });
  }

  const panelBtns = document.querySelectorAll('.mode-toggle .mode-btn');
  panelBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      panelBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      document.querySelectorAll('.write-panel').forEach(p => { p.hidden = true; });
      document.getElementById(btn.dataset.panel).hidden = false;
      if (window.Sfx) Sfx.tap();
      refreshVisibleTracers();
    });
  });

  // Tracing / Keyboard sub-tabs within a script's panel
  document.querySelectorAll('.sub-toggle').forEach(group => {
    const btns = group.querySelectorAll('.sub-btn');
    btns.forEach(btn => {
      btn.addEventListener('click', () => {
        btns.forEach(b => {
          b.classList.toggle('active', b === btn);
          const panel = document.getElementById(b.dataset.sub);
          if (panel) panel.hidden = b !== btn;
        });
        if (window.Sfx) Sfx.tap();
        refreshVisibleTracers();
      });
    });
  });

  // --------------------------------------------------- kana keyboards --
  function buildKeyboard(containerId, data) {
    const container = document.getElementById(containerId);
    if (!container) return;
    const basic = data.filter(k => k.type === 'basic');
    const dakuten = data.filter(k => k.type === 'dakuten');
    const yoon = data.filter(k => k.type === 'yoon');

    function row(list, label) {
      const wrap = document.createElement('div');
      wrap.className = 'kb-row-group';
      const h = document.createElement('h4');
      h.textContent = label;
      wrap.appendChild(h);
      const grid = document.createElement('div');
      grid.className = 'kb-row';
      list.forEach(k => {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'kb-key';
        btn.textContent = k.char;
        btn.title = k.romaji;
        btn.addEventListener('click', () => {
          appendToOutput(containerId, k.char);
          if (window.Sfx) Sfx.tap();
        });
        grid.appendChild(btn);
      });
      wrap.appendChild(grid);
      return wrap;
    }
    container.appendChild(row(basic, 'Basic'));
    container.appendChild(row(dakuten, 'Dakuten / Handakuten'));
    container.appendChild(row(yoon, 'Combination (yōon)'));

    // backspace / space keys
    const controls = document.createElement('div');
    controls.className = 'kb-row-group';
    const grid = document.createElement('div');
    grid.className = 'kb-row';
    const back = document.createElement('button');
    back.type = 'button'; back.className = 'kb-key kb-wide'; back.textContent = '⌫ back';
    back.addEventListener('click', () => {
      backspaceOutput(containerId);
      if (window.Sfx) Sfx.tap();
    });
    const space = document.createElement('button');
    space.type = 'button'; space.className = 'kb-key kb-wide'; space.textContent = 'space';
    space.addEventListener('click', () => {
      appendToOutput(containerId, '　');
      if (window.Sfx) Sfx.tap();
    });
    grid.appendChild(back); grid.appendChild(space);
    controls.appendChild(grid);
    container.appendChild(controls);
  }

  function outputElFor(keyboardId) {
    return keyboardId === 'hira-keyboard'
      ? document.getElementById('hira-output')
      : document.getElementById('kata-output');
  }
  function appendToOutput(keyboardId, ch) {
    outputElFor(keyboardId).textContent += ch;
  }
  function backspaceOutput(keyboardId) {
    const el = outputElFor(keyboardId);
    el.textContent = el.textContent.slice(0, -1);
  }

  buildKeyboard('hira-keyboard', window.HIRAGANA_DATA || []);
  buildKeyboard('kata-keyboard', window.KATAKANA_DATA || []);

  // ------------------------------------------------- romaji live input --
  function wireRomaji(inputId, outputId, clearId, convert) {
    const input = document.getElementById(inputId);
    const output = document.getElementById(outputId);
    if (!input || !output) return;
    input.addEventListener('input', () => { output.textContent = convert(input.value); });
    const clear = document.getElementById(clearId);
    if (clear) {
      clear.addEventListener('click', () => {
        input.value = '';
        output.textContent = '';
        if (window.Sfx) Sfx.tap();
      });
    }
  }
  wireRomaji('hira-romaji', 'hira-output', 'hira-clear', romajiToHiragana);
  wireRomaji('kata-romaji', 'kata-output', 'kata-clear', romajiToKatakana);

  // ------------------------------------------------------ tracing pads --
  function mount(id, items) {
    const root = document.getElementById(id);
    if (!root || !items.length) return null;
    const tracer = new KotobaTracer(root, {});
    tracer.setItems(items);
    tracers[id] = tracer;
    return tracer;
  }

  // Kana worth practising by hand: the base syllabary plus the voiced
  // forms. Combination (yōon) pairs are two characters, so they don't
  // belong on a single-character tracing square.
  function kanaItems(data) {
    return (data || [])
      .filter(k => k.type === 'basic' || k.type === 'dakuten')
      .map(k => ({ char: k.char, label: k.romaji }));
  }

  mount('hira-tracer', kanaItems(window.HIRAGANA_DATA));
  mount('kata-tracer', kanaItems(window.KATAKANA_DATA));

  // Kanji come from the API so the tracer shares the app's kanji set.
  fetch('/api/kanji_pool')
    .then(r => r.json())
    .then(pool => {
      const items = pool.map(k => ({
        char: k.kanji,
        label: k.strokes ? `${k.meaning} · ${k.strokes} strokes` : k.meaning,
        meaning: k.meaning,
        strokes: k.strokes,
      }));
      const tracer = mount('kanji-tracer', items);
      if (!tracer) return;

      const filter = document.getElementById('kanji-pick-filter');
      if (filter) {
        filter.addEventListener('input', () => {
          const q = filter.value.trim().toLowerCase();
          if (!q) return;
          const match = items.findIndex(
            k => k.meaning.toLowerCase().includes(q) || k.char === q
          );
          if (match >= 0) tracer.show(match);
        });
      }
    })
    .catch(() => {
      const note = document.querySelector('#kanji-tracer .trace-verdict');
      if (note) {
        note.className = 'trace-verdict nudge';
        note.textContent = 'Could not load the kanji list.';
        note.hidden = false;
      }
    });

  // The first visible panel's canvas needs a size once fonts have settled.
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(refreshVisibleTracers).catch(() => {});
  }
  window.addEventListener('load', refreshVisibleTracers);
});
