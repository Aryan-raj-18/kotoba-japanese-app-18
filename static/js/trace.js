/* =====================================================================
   Kotoba — character tracing pad
   ---------------------------------------------------------------------
   One reusable component, mounted three times (hiragana, katakana,
   kanji) on the Writing Practice page.

   HOW THE MISTAKE DETECTION WORKS
   The guide character and the scoring mask are drawn by the *same* code
   into two stacked canvases of identical size:

       guide canvas  — the faded character you trace over
       ink canvas    — your strokes

   Because both come from one drawText call, they line up exactly, which
   also means the app doesn't care which font actually resolved (the
   bundled web font may not load inside the APK, and that's fine).

   Checking an attempt downsamples both canvases to a 64x64 grid and
   compares them two ways:

       coverage — how much of the character you actually drew over
       spill    — how much of your ink landed outside the character

   A pass needs decent coverage AND low spill, so neither scribbling
   over everything nor drawing one confident stroke gets a pass.
   ================================================================== */

(function () {
  'use strict';

  var GRID = 64;              // scoring resolution
  var GLYPH_FILL = 0.80;      // fraction of the box the character occupies
  var PASS_COVERAGE = 0.62;   // must have traced at least this much of it
  var PASS_SPILL = 0.35;      // ...without this much ink landing outside
  var MIN_INK = 0.15;         // below this there's nothing worth scoring
  var SHAKE_AFTER = 3;        // failed attempts on one character before the shake

  // ---------------------------------------------------------------- utils

  function jpFont() {
    var v = getComputedStyle(document.documentElement).getPropertyValue('--serif-jp');
    return (v && v.trim()) || 'serif';
  }

  /**
   * Draw `ch` centred on its own ink box and scaled to fill the square.
   * Returns false if nothing measurable was drawn.
   */
  function drawGlyph(ctx, ch, box, color) {
    var family = jpFont();
    ctx.save();
    ctx.clearRect(0, 0, box, box);
    ctx.fillStyle = color;

    var probe = box;
    ctx.font = probe + 'px ' + family;
    var m = ctx.measureText(ch);

    var hasBox = typeof m.actualBoundingBoxAscent === 'number' &&
                 typeof m.actualBoundingBoxLeft === 'number';

    if (!hasBox) {
      // Old WebViews without TextMetrics bounding boxes: approximate.
      ctx.font = Math.round(box * 0.78) + 'px ' + family;
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(ch, box / 2, box / 2);
      ctx.restore();
      return true;
    }

    var w = m.actualBoundingBoxLeft + m.actualBoundingBoxRight;
    var h = m.actualBoundingBoxAscent + m.actualBoundingBoxDescent;
    if (!(w > 0) || !(h > 0)) { ctx.restore(); return false; }

    var size = probe * Math.min((box * GLYPH_FILL) / w, (box * GLYPH_FILL) / h);
    ctx.font = size + 'px ' + family;
    m = ctx.measureText(ch);
    w = m.actualBoundingBoxLeft + m.actualBoundingBoxRight;
    h = m.actualBoundingBoxAscent + m.actualBoundingBoxDescent;

    ctx.textAlign = 'left';
    ctx.textBaseline = 'alphabetic';
    ctx.fillText(ch, box / 2 + m.actualBoundingBoxLeft - w / 2,
                     box / 2 + m.actualBoundingBoxAscent - h / 2);
    ctx.restore();
    return true;
  }

  /** Downsample a canvas's alpha channel to a GRIDxGRID occupancy mask. */
  function maskOf(canvas, box) {
    var data;
    try {
      data = canvas.getContext('2d').getImageData(0, 0, box, box).data;
    } catch (e) {
      return null;
    }
    var mask = new Uint8Array(GRID * GRID);
    var step = box / GRID;
    for (var y = 0; y < box; y++) {
      var gy = (y / step) | 0;
      if (gy >= GRID) gy = GRID - 1;
      var rowBase = gy * GRID;
      var pixBase = y * box * 4;
      for (var x = 0; x < box; x++) {
        if (data[pixBase + x * 4 + 3] > 40) {
          var gx = (x / step) | 0;
          if (gx >= GRID) gx = GRID - 1;
          mask[rowBase + gx] = 1;
        }
      }
    }
    return mask;
  }

  /** Grow a mask by `r` cells (separable box dilation). */
  function dilate(mask, r) {
    if (r <= 0) return mask;
    var tmp = new Uint8Array(GRID * GRID);
    var out = new Uint8Array(GRID * GRID);
    var x, y, k;
    for (y = 0; y < GRID; y++) {
      for (x = 0; x < GRID; x++) {
        if (!mask[y * GRID + x]) continue;
        for (k = -r; k <= r; k++) {
          var nx = x + k;
          if (nx >= 0 && nx < GRID) tmp[y * GRID + nx] = 1;
        }
      }
    }
    for (y = 0; y < GRID; y++) {
      for (x = 0; x < GRID; x++) {
        if (!tmp[y * GRID + x]) continue;
        for (k = -r; k <= r; k++) {
          var ny = y + k;
          if (ny >= 0 && ny < GRID) out[ny * GRID + x] = 1;
        }
      }
    }
    return out;
  }

  function count(mask) {
    var n = 0;
    for (var i = 0; i < mask.length; i++) n += mask[i];
    return n;
  }

  function overlap(a, b) {
    var n = 0;
    for (var i = 0; i < a.length; i++) if (a[i] && b[i]) n++;
    return n;
  }

  // ------------------------------------------------------------ component

  /**
   * @param {HTMLElement} root  element carrying the .trace-block markup
   * @param {Object} opts
   *   opts.items     [{ char, label }]
   *   opts.pickerCap how many characters to put in the quick-pick strip
   */
  function Tracer(root, opts) {
    this.root = root;
    this.opts = opts || {};
    this.items = [];
    this.index = 0;
    this.fails = 0;
    this.strokes = 0;
    this.dirty = false;
    this.guideHidden = false;

    this.stage = root.querySelector('.trace-stage');
    this.guideCanvas = root.querySelector('.trace-guide-canvas');
    this.inkCanvas = root.querySelector('.trace-canvas');
    this.verdictEl = root.querySelector('.trace-verdict');
    this.charEl = root.querySelector('.trace-target-char');
    this.labelEl = root.querySelector('.trace-target-meaning');
    this.progressEl = root.querySelector('.trace-progress');
    this.pickerEl = root.querySelector('.trace-picker');

    this.gctx = this.guideCanvas.getContext('2d');
    this.ictx = this.inkCanvas.getContext('2d', { willReadFrequently: true });
    this.box = 0;

    this._bindPointer();
    this._bindButtons();
    this._bindResize();
  }

  Tracer.prototype.setItems = function (items) {
    this.items = items || [];
    this._buildPicker();
    this.show(0);
  };

  Tracer.prototype.current = function () { return this.items[this.index]; };

  // ---- sizing -----------------------------------------------------------

  Tracer.prototype._bindResize = function () {
    var self = this;
    var resize = function () { self.resize(); };
    window.addEventListener('resize', resize);
    window.addEventListener('orientationchange', resize);
    if (window.ResizeObserver) {
      this._ro = new ResizeObserver(resize);
      this._ro.observe(this.stage);
    }
  };

  Tracer.prototype.resize = function () {
    var rect = this.stage.getBoundingClientRect();
    // The stage is a CSS square, but don't *rely* on aspect-ratio having
    // resolved - an older WebView that ignores it would report a height
    // of 0 and leave the pad permanently unsized.
    var css = Math.round(rect.width || rect.height);
    if (rect.height) css = Math.round(Math.min(css, rect.height));
    if (!css) return;                     // panel is hidden right now
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var box = Math.round(css * dpr);
    if (box === this.box) return;

    this.box = box;
    [this.guideCanvas, this.inkCanvas].forEach(function (c) {
      c.width = box;
      c.height = box;
    });
    this._paintGuide();
    this.clearInk();
  };

  // ---- rendering --------------------------------------------------------

  Tracer.prototype._guideColor = function () {
    var v = getComputedStyle(document.documentElement)
      .getPropertyValue('--trace-guide-ink');
    return (v && v.trim()) || 'rgba(43,69,112,0.16)';
  };

  Tracer.prototype._inkColor = function () {
    var v = getComputedStyle(document.documentElement)
      .getPropertyValue('--trace-ink');
    return (v && v.trim()) || '#2B4570';
  };

  Tracer.prototype._paintGuide = function () {
    var item = this.current();
    if (!item || !this.box) return;
    if (this.guideHidden) {
      this.gctx.clearRect(0, 0, this.box, this.box);
      return;
    }
    drawGlyph(this.gctx, item.char, this.box, this._guideColor());
  };

  Tracer.prototype.clearInk = function () {
    if (!this.box) return;
    this.ictx.clearRect(0, 0, this.box, this.box);
    this.ictx.lineWidth = Math.max(4, this.box * 0.055);
    this.ictx.lineCap = 'round';
    this.ictx.lineJoin = 'round';
    this.ictx.strokeStyle = this._inkColor();
    this.dirty = false;
    this.strokes = 0;
  };

  Tracer.prototype.show = function (i) {
    if (!this.items.length) return;
    this.index = ((i % this.items.length) + this.items.length) % this.items.length;
    var item = this.current();
    this.fails = 0;

    if (this.charEl) this.charEl.textContent = item.char;
    if (this.labelEl) this.labelEl.textContent = item.label || '';
    if (this.progressEl) {
      this.progressEl.textContent = (this.index + 1) + ' / ' + this.items.length;
    }
    if (this.pickerEl) {
      var chips = this.pickerEl.querySelectorAll('.trace-chip');
      for (var c = 0; c < chips.length; c++) {
        var on = Number(chips[c].dataset.index) === this.index;
        chips[c].setAttribute('aria-pressed', String(on));
        if (on && chips[c].scrollIntoView) {
          chips[c].scrollIntoView({ block: 'nearest', inline: 'nearest' });
        }
      }
    }

    this.stage.classList.remove('is-pass', 'is-fail');
    this._hideVerdict();
    this.resize();
    this._paintGuide();
    this.clearInk();
  };

  // ---- drawing ----------------------------------------------------------

  Tracer.prototype._pos = function (e) {
    var rect = this.inkCanvas.getBoundingClientRect();
    var t = (e.touches && e.touches[0]) || e;
    var sx = this.box / rect.width;
    var sy = this.box / rect.height;
    return { x: (t.clientX - rect.left) * sx, y: (t.clientY - rect.top) * sy };
  };

  Tracer.prototype._bindPointer = function () {
    var self = this;
    var drawing = false, lx = 0, ly = 0;

    function start(e) {
      if (!self.box) self.resize();
      drawing = true;
      self.strokes++;
      var p = self._pos(e);
      lx = p.x; ly = p.y;
      // a dot, so a tap registers as a mark (small kana strokes are short)
      self.ictx.beginPath();
      self.ictx.moveTo(lx, ly);
      self.ictx.lineTo(lx + 0.01, ly + 0.01);
      self.ictx.stroke();
      self.dirty = true;
      self.stage.classList.remove('is-pass', 'is-fail');
      e.preventDefault();
    }
    function move(e) {
      if (!drawing) return;
      var p = self._pos(e);
      self.ictx.beginPath();
      self.ictx.moveTo(lx, ly);
      self.ictx.lineTo(p.x, p.y);
      self.ictx.stroke();
      lx = p.x; ly = p.y;
      e.preventDefault();
    }
    function end() { drawing = false; }

    var cv = this.inkCanvas;
    cv.addEventListener('mousedown', start);
    cv.addEventListener('mousemove', move);
    window.addEventListener('mouseup', end);
    cv.addEventListener('touchstart', start, { passive: false });
    cv.addEventListener('touchmove', move, { passive: false });
    cv.addEventListener('touchend', end);
    cv.addEventListener('touchcancel', end);
  };

  // ---- buttons ----------------------------------------------------------

  Tracer.prototype._bindButtons = function () {
    var self = this;
    function on(sel, fn) {
      var el = self.root.querySelector(sel);
      if (el) el.addEventListener('click', fn);
    }
    on('.trace-clear', function () {
      self.clearInk();
      self.stage.classList.remove('is-pass', 'is-fail');
      self._hideVerdict();
      if (window.Sfx) Sfx.tap();
    });
    on('.trace-prev', function () { self.show(self.index - 1); if (window.Sfx) Sfx.tap(); });
    on('.trace-next', function () { self.show(self.index + 1); if (window.Sfx) Sfx.tap(); });
    on('.trace-check', function () { self.check(); });
    on('.trace-guide-toggle', function (e) {
      self.guideHidden = !self.guideHidden;
      e.currentTarget.textContent = self.guideHidden ? 'Show guide' : 'Hide guide';
      e.currentTarget.setAttribute('aria-pressed', String(self.guideHidden));
      self._paintGuide();
      if (window.Sfx) Sfx.tap();
    });
  };

  Tracer.prototype._buildPicker = function () {
    if (!this.pickerEl) return;
    var self = this;
    this.pickerEl.innerHTML = '';
    this.items.forEach(function (item, i) {
      var chip = document.createElement('button');
      chip.type = 'button';
      chip.className = 'trace-chip';
      chip.dataset.index = String(i);
      chip.textContent = item.char;
      chip.title = item.label || item.char;
      chip.setAttribute('aria-pressed', 'false');
      chip.addEventListener('click', function () { self.show(i); if (window.Sfx) Sfx.tap(); });
      self.pickerEl.appendChild(chip);
    });
  };

  // ---- verdicts ---------------------------------------------------------

  Tracer.prototype._hideVerdict = function () {
    if (this.verdictEl) this.verdictEl.hidden = true;
  };

  Tracer.prototype._verdict = function (kind, message, detail) {
    if (!this.verdictEl) return;
    this.verdictEl.className = 'trace-verdict ' + kind;
    this.verdictEl.innerHTML = '';
    this.verdictEl.appendChild(document.createTextNode(message));
    if (detail) {
      var small = document.createElement('small');
      small.textContent = detail;
      this.verdictEl.appendChild(small);
    }
    this.verdictEl.hidden = false;
  };

  // ---- scoring ----------------------------------------------------------

  Tracer.prototype.score = function () {
    var box = this.box;
    if (!box) return null;

    // The guide canvas may be blanked ("Hide guide"), so score against a
    // freshly rendered copy of the target rather than what's on screen.
    var target = document.createElement('canvas');
    target.width = box; target.height = box;
    if (!drawGlyph(target.getContext('2d'), this.current().char, box, '#000')) return null;

    var glyph = maskOf(target, box);
    var ink = maskOf(this.inkCanvas, box);
    if (!glyph || !ink) return null;

    var glyphN = count(glyph);
    var inkN = count(ink);
    if (!glyphN) return null;

    var tolerance = 2;                       // ~10px of slack at 320px
    var allowed = dilate(glyph, tolerance);
    var covered = dilate(ink, tolerance);

    return {
      coverage: overlap(glyph, covered) / glyphN,
      spill: inkN ? (inkN - overlap(ink, allowed)) / inkN : 0,
      inkRatio: inkN / glyphN,
      strokes: this.strokes,
    };
  };

  Tracer.prototype.check = function () {
    if (!this.items.length) return;
    if (!this.dirty) {
      this._verdict('nudge', 'Nothing drawn yet.', 'Trace over the faded character with your finger or mouse.');
      return;
    }

    var s = this.score();
    if (!s) {
      this._verdict('nudge', "Couldn't read that attempt.", 'Try clearing and drawing again.');
      return;
    }

    var pct = Math.round(s.coverage * 100);
    var passed = s.coverage >= PASS_COVERAGE && s.spill <= PASS_SPILL && s.inkRatio > MIN_INK;

    this.stage.classList.remove('is-pass', 'is-fail', 'is-shaking');

    if (passed) {
      this.fails = 0;
      this.stage.classList.add('is-pass');
      this._verdict('pass', '正解 — that\'s a good match.',
        pct + '% of the character covered in ' + s.strokes +
        ' stroke' + (s.strokes === 1 ? '' : 's') + '.');
      if (window.Sfx) Sfx.pass();
      if (this.opts.onPass) this.opts.onPass(this.current(), s);
      return;
    }

    this.fails++;
    this.stage.classList.add('is-fail');

    var msg, detail;
    if (s.inkRatio <= MIN_INK) {
      msg = 'Not quite — there\'s hardly any ink on the page.';
      detail = 'Trace the whole character, not just part of a stroke.';
    } else if (s.spill > PASS_SPILL) {
      msg = 'Not quite — your strokes are drifting outside the guide.';
      detail = Math.round(s.spill * 100) + '% of your ink landed off the character.';
    } else {
      msg = 'Not quite — some of the character is still untraced.';
      detail = 'You covered ' + pct + '%; aim for ' + Math.round(PASS_COVERAGE * 100) + '% or more.';
    }

    // More than two misses on the same character: shake the box and buzz
    // the phone, so the feedback is physical and not just another line
    // of text to read past.
    if (this.fails >= SHAKE_AFTER) {
      var stage = this.stage;
      stage.classList.add('is-shaking');
      setTimeout(function () { stage.classList.remove('is-shaking'); }, 520);
      if (window.Sfx) Sfx.struggle();
      else if (navigator.vibrate) { try { navigator.vibrate([0, 70, 70, 70, 70, 140]); } catch (e) {} }

      // Give the guide back if they'd hidden it — they need it now.
      if (this.guideHidden) {
        this.guideHidden = false;
        var toggle = this.root.querySelector('.trace-guide-toggle');
        if (toggle) {
          toggle.textContent = 'Hide guide';
          toggle.setAttribute('aria-pressed', 'false');
        }
        this._paintGuide();
      }
      detail = (detail || '') + ' That\'s ' + this.fails +
               ' misses on this one — clear it and take the strokes slowly.';
    } else if (window.Sfx) {
      Sfx.fail();
    }

    this._verdict('fail', msg, detail);
    if (this.opts.onFail) this.opts.onFail(this.current(), s, this.fails);
  };

  window.KotobaTracer = Tracer;
})();
