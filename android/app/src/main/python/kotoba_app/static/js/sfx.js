/* =====================================================================
   Kotoba — sound effects & haptics
   ---------------------------------------------------------------------
   Every sound is synthesised with the Web Audio API rather than loaded
   from a file. That matters here: the app ships inside an APK with no
   network access, so there are no audio assets to miss, nothing to
   precache, and no added download weight.

   Tones are picked from the yo scale (よな抜き音階) — the pentatonic
   scale used in a lot of Japanese folk music — so the feedback chimes
   sit inside the app's overall character instead of sounding generic.

   Preferences live in localStorage and are shared with theme.js:
     kotoba:sound     "on" | "off"
     kotoba:haptics   "on" | "off"
   ================================================================== */

window.Sfx = (function () {
  'use strict';

  var SOUND_KEY = 'kotoba:sound';
  var HAPTIC_KEY = 'kotoba:haptics';

  var ctx = null;
  var master = null;

  function read(key) {
    try { return localStorage.getItem(key); } catch (e) { return null; }
  }
  function write(key, value) {
    try { localStorage.setItem(key, value); } catch (e) { /* private mode */ }
  }

  var soundOn = read(SOUND_KEY) !== 'off';      // default on
  var hapticsOn = read(HAPTIC_KEY) !== 'off';   // default on

  function ensureCtx() {
    if (!soundOn) return null;
    var AC = window.AudioContext || window.webkitAudioContext;
    if (!AC) return null;
    if (!ctx) {
      try {
        ctx = new AC();
        master = ctx.createGain();
        master.gain.value = 0.5;
        master.connect(ctx.destination);
      } catch (e) {
        ctx = null;
        return null;
      }
    }
    // Browsers (and Android WebView) start the context suspended until
    // the page has had a real user gesture.
    if (ctx.state === 'suspended') { ctx.resume().catch(function () {}); }
    return ctx;
  }

  /**
   * One shaped tone. `type` is an oscillator type; `at` is an offset in
   * seconds from now, so a sequence can be scheduled in one go.
   */
  function tone(freq, at, dur, gain, type, glideTo) {
    var c = ensureCtx();
    if (!c) return;
    var t0 = c.currentTime + at;
    var osc = c.createOscillator();
    var env = c.createGain();

    osc.type = type || 'sine';
    osc.frequency.setValueAtTime(freq, t0);
    if (glideTo) osc.frequency.exponentialRampToValueAtTime(glideTo, t0 + dur);

    // quick attack, exponential tail — reads as a struck/plucked sound
    env.gain.setValueAtTime(0.0001, t0);
    env.gain.exponentialRampToValueAtTime(gain, t0 + 0.012);
    env.gain.exponentialRampToValueAtTime(0.0001, t0 + dur);

    osc.connect(env);
    env.connect(master);
    osc.start(t0);
    osc.stop(t0 + dur + 0.02);
  }

  /** Short filtered noise burst — used for the "wrong" thud. */
  function thud(at, dur, gain) {
    var c = ensureCtx();
    if (!c) return;
    var t0 = c.currentTime + at;
    var frames = Math.floor(c.sampleRate * dur);
    var buf = c.createBuffer(1, frames, c.sampleRate);
    var data = buf.getChannelData(0);
    for (var i = 0; i < frames; i++) {
      data[i] = (Math.random() * 2 - 1) * (1 - i / frames);
    }
    var src = c.createBufferSource();
    src.buffer = buf;
    var filter = c.createBiquadFilter();
    filter.type = 'lowpass';
    filter.frequency.value = 420;
    var env = c.createGain();
    env.gain.setValueAtTime(gain, t0);
    env.gain.exponentialRampToValueAtTime(0.0001, t0 + dur);
    src.connect(filter); filter.connect(env); env.connect(master);
    src.start(t0);
    src.stop(t0 + dur);
  }

  function vibrate(pattern) {
    if (!hapticsOn) return;
    if (!navigator.vibrate) return;
    try { navigator.vibrate(pattern); } catch (e) { /* unsupported */ }
  }

  var api = {
    // ---- preference plumbing (the settings menu drives these) ----
    isSoundOn: function () { return soundOn; },
    isHapticsOn: function () { return hapticsOn; },
    setSound: function (on) {
      soundOn = !!on;
      write(SOUND_KEY, soundOn ? 'on' : 'off');
      if (soundOn) { ensureCtx(); api.tap(); }
    },
    setHaptics: function (on) {
      hapticsOn = !!on;
      write(HAPTIC_KEY, hapticsOn ? 'on' : 'off');
      if (hapticsOn) vibrate(18);
    },
    unlock: ensureCtx,
    vibrate: vibrate,

    // ---- the sounds ----

    /** Any minor press: keyboard keys, chips, tabs. */
    tap: function () { tone(880, 0, 0.05, 0.10, 'triangle'); },

    /** Flashcard turning over — a soft two-step whisk. */
    flip: function () {
      tone(520, 0, 0.07, 0.10, 'triangle', 780);
      tone(1040, 0.05, 0.08, 0.05, 'sine');
    },

    /** Right answer — rising yo-scale figure (D–F–A). */
    correct: function () {
      tone(587.33, 0, 0.16, 0.16, 'sine');
      tone(698.46, 0.09, 0.18, 0.15, 'sine');
      tone(880.00, 0.18, 0.34, 0.15, 'sine');
      vibrate(22);
    },

    /** Wrong answer — a short, low, deliberately un-harsh drop. */
    incorrect: function () {
      tone(233.08, 0, 0.16, 0.16, 'triangle');
      tone(174.61, 0.11, 0.30, 0.14, 'triangle');
      thud(0, 0.16, 0.10);
      vibrate([26, 60, 26]);
    },

    /** A traced character was accepted. */
    pass: function () {
      tone(783.99, 0, 0.14, 0.14, 'sine');
      tone(1174.66, 0.08, 0.30, 0.11, 'sine');
      vibrate(24);
    },

    /** A traced character missed — softer than a wrong quiz answer,
        because tracing is meant to be retried. */
    fail: function () {
      tone(311.13, 0, 0.13, 0.13, 'triangle');
      tone(261.63, 0.09, 0.22, 0.11, 'triangle');
    },

    /** Third failed attempt on the same character — paired with the
        shake, so it needs to be felt as well as heard. */
    struggle: function () {
      tone(293.66, 0, 0.12, 0.14, 'square');
      tone(246.94, 0.10, 0.12, 0.13, 'square');
      tone(196.00, 0.20, 0.26, 0.12, 'square');
      vibrate([0, 70, 70, 70, 70, 140]);
    },

    /** End of a round / deck. */
    complete: function () {
      [587.33, 698.46, 880.0, 1174.66].forEach(function (f, i) {
        tone(f, i * 0.1, 0.42, 0.13, 'sine');
      });
      vibrate([0, 30, 40, 30]);
    },
  };

  // The very first gesture on a page unlocks audio for everything after
  // it, so the first chime isn't silently swallowed.
  ['pointerdown', 'touchstart', 'keydown'].forEach(function (evt) {
    window.addEventListener(evt, function once() {
      ensureCtx();
      ['pointerdown', 'touchstart', 'keydown'].forEach(function (e2) {
        window.removeEventListener(e2, once);
      });
    }, { once: false, passive: true });
  });

  return api;
})();
