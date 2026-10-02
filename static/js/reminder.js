/* =====================================================================
   Kotoba — daily reminder settings
   ---------------------------------------------------------------------
   This file only owns the UI in the settings panel (the switch, the
   time picker, remembering the choice). The actual "notify me at 19:00
   every day" scheduling is native Android work - a WebView page has no
   way to wake the phone up on its own - so every real state change is
   handed to window.KotobaNative, a JavascriptInterface bridge that
   MainActivity.kt installs (see scheduleReminder/cancelReminder there).

   In a plain desktop/mobile browser (e.g. while developing on
   127.0.0.1) that bridge doesn't exist, so the switch still remembers
   your choice but a hint explains why nothing will actually fire.
   ================================================================== */

(function () {
  'use strict';

  var KEY = 'kotoba:reminder';
  var DEFAULT_TIME = '19:00';

  function read() {
    try {
      var raw = localStorage.getItem(KEY);
      if (!raw) return { enabled: false, time: DEFAULT_TIME };
      var parsed = JSON.parse(raw);
      return {
        enabled: !!parsed.enabled,
        time: /^\d{2}:\d{2}$/.test(parsed.time) ? parsed.time : DEFAULT_TIME,
      };
    } catch (e) {
      return { enabled: false, time: DEFAULT_TIME };
    }
  }

  function save(state) {
    try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) { /* private mode */ }
  }

  function hasNativeBridge() {
    return !!(window.KotobaNative && typeof window.KotobaNative.scheduleReminder === 'function');
  }

  function applyToNative(state) {
    if (!hasNativeBridge()) return;
    if (state.enabled) {
      var parts = state.time.split(':');
      window.KotobaNative.scheduleReminder(parseInt(parts[0], 10), parseInt(parts[1], 10));
    } else {
      window.KotobaNative.cancelReminder();
    }
  }

  document.addEventListener('DOMContentLoaded', function () {
    var toggle = document.getElementById('reminder-switch');
    var timeRow = document.getElementById('reminder-time-row');
    var timeInput = document.getElementById('reminder-time');
    var hint = document.getElementById('reminder-hint');
    if (!toggle || !timeRow || !timeInput || !hint) return;

    var state = read();

    function render() {
      toggle.setAttribute('aria-checked', String(state.enabled));
      timeRow.hidden = !state.enabled;
      timeInput.value = state.time;
      // Explain the no-op rather than let it look broken, but only once
      // it'd actually matter (the switch is on and there's nothing to
      // back it) - not on every visit.
      hint.hidden = !(state.enabled && !hasNativeBridge());
    }
    render();

    toggle.addEventListener('click', function () {
      state.enabled = toggle.getAttribute('aria-checked') !== 'true';
      save(state);
      render();
      applyToNative(state);
      if (window.Sfx) Sfx.tap();
    });

    timeInput.addEventListener('change', function () {
      if (!/^\d{2}:\d{2}$/.test(timeInput.value)) return; // mid-edit / cleared
      state.time = timeInput.value;
      save(state);
      applyToNative(state);
    });

    // The bridge only exists inside the installed app, and by the time
    // this script runs it's always already there if it's going to be -
    // but re-sync once in case the switch was left on from a previous
    // browser-only visit and the app can now actually honor it.
    applyToNative(state);
  });
})();
