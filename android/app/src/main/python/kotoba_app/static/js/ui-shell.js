/*
 * Kotoba Immersive UI Shell
 * -------------------------
 * Presentation-only layer. It never replaces page links, form actions,
 * learning data, APIs, or page-specific JavaScript.
 *
 * Wallpaper support is also presentation-only: the selected image/GIF is
 * stored as a Blob in IndexedDB on this device and is never uploaded.
 */
(function () {
  'use strict';

  // data-ui-shell="immersive" is set directly in base.html's <html> tag
  // now, not here — setting it this late (this script loads at the end
  // of <body>) meant every navigation rendered in the plain theme for a
  // moment and then visibly snapped into the glass look afterward.

  var DB_NAME = 'kotoba-ui-shell';
  var DB_VERSION = 1;
  var STORE = 'preferences';
  var WALLPAPER_KEY = 'wallpaper';
  var DIM_KEY = 'kotoba:wallpaper:dim';
  var DEFAULT_DIM = 60;
  var MAX_WALLPAPER_BYTES = 60 * 1024 * 1024; // 60MB — generous for a big GIF, guards against a mistaken pick
  var currentObjectUrl = null;

  function readDim() {
    try {
      var v = localStorage.getItem(DIM_KEY);
      return v !== null ? Number(v) : DEFAULT_DIM;
    } catch (e) { return DEFAULT_DIM; }
  }
  function applyDim(pct) {
    document.documentElement.style.setProperty('--wallpaper-scrim', pct / 100);
  }
  function saveDim(pct) {
    try { localStorage.setItem(DIM_KEY, String(pct)); } catch (e) { /* ignore */ }
  }

  // Applied immediately (not gated on DOMContentLoaded) so the scrim
  // strength is correct from the first frame this script runs, same
  // reasoning as the theme snippet in base.html's <head>.
  applyDim(readDim());

  function iconFor(label) {
    var map = {
      Home: '⌂', Learn: '学', Review: '↻', Explore: '探', Progress: '◔'
    };
    return map[label] || '•';
  }

  function makeBottomNav() {
    if (document.querySelector('.kotoba-bottom-nav')) return;

    var nav = document.createElement('nav');
    nav.className = 'kotoba-bottom-nav';
    nav.setAttribute('aria-label', 'Quick navigation');

    var current = window.location.pathname.replace(/\/$/, '') || '/';
    var items = [
      { label: 'Home', href: '/', match: ['/'] },
      { label: 'Learn', href: '/roadmap', match: ['/roadmap'] },
      { label: 'Review', href: '/flashcards', match: ['/flashcards','/practice','/kanji/practice'] },
      { label: 'Explore', href: '/explore', match: ['/explore','/hiragana','/katakana','/kanji','/jlpt','/verbs','/everyday','/stories','/conversations','/write','/writing-practice'] },
      { label: 'Progress', href: '/dashboard', match: ['/dashboard','/streak'] }
    ];

    items.forEach(function (item) {
      var a = document.createElement('a');
      a.href = item.href;
      a.innerHTML = '<span class="nav-icon" aria-hidden="true">' + iconFor(item.label) + '</span>' +
                    '<span>' + item.label + '</span>';
      var active = item.match.some(function (path) {
        if (path === '/') return current === '/';
        return current === path || current.indexOf(path + '/') === 0;
      });
      if (active) a.classList.add('active');
      nav.appendChild(a);
    });

    document.body.appendChild(nav);
  }

  function openDb() {
    return new Promise(function (resolve, reject) {
      if (!window.indexedDB) {
        reject(new Error('IndexedDB is unavailable'));
        return;
      }
      var request = indexedDB.open(DB_NAME, DB_VERSION);
      request.onupgradeneeded = function () {
        var db = request.result;
        if (!db.objectStoreNames.contains(STORE)) db.createObjectStore(STORE);
      };
      request.onsuccess = function () { resolve(request.result); };
      request.onerror = function () { reject(request.error || new Error('Database error')); };
    });
  }

  function dbGet(key) {
    return openDb().then(function (db) {
      return new Promise(function (resolve, reject) {
        var tx = db.transaction(STORE, 'readonly');
        var req = tx.objectStore(STORE).get(key);
        req.onsuccess = function () { resolve(req.result || null); };
        req.onerror = function () { reject(req.error || new Error('Read error')); };
        tx.oncomplete = function () { db.close(); };
      });
    });
  }

  function dbPut(key, value) {
    return openDb().then(function (db) {
      return new Promise(function (resolve, reject) {
        var tx = db.transaction(STORE, 'readwrite');
        tx.objectStore(STORE).put(value, key);
        tx.oncomplete = function () { db.close(); resolve(); };
        tx.onerror = function () { reject(tx.error || new Error('Write error')); };
      });
    });
  }

  function dbDelete(key) {
    return openDb().then(function (db) {
      return new Promise(function (resolve, reject) {
        var tx = db.transaction(STORE, 'readwrite');
        tx.objectStore(STORE).delete(key);
        tx.oncomplete = function () { db.close(); resolve(); };
        tx.onerror = function () { reject(tx.error || new Error('Delete error')); };
      });
    });
  }

  function setWallpaper(blob) {
    if (currentObjectUrl) URL.revokeObjectURL(currentObjectUrl);
    currentObjectUrl = URL.createObjectURL(blob);

    var wallpaper = document.querySelector('.kotoba-wallpaper');
    if (!wallpaper) {
      wallpaper = document.createElement('div');
      wallpaper.className = 'kotoba-wallpaper';
      wallpaper.setAttribute('aria-hidden', 'true');
      document.body.prepend(wallpaper);
    }
    wallpaper.style.backgroundImage = 'url("' + currentObjectUrl.replace(/"/g, '%22') + '")';
    document.body.classList.add('has-kotoba-wallpaper');

    var clear = document.getElementById('wallpaper-clear');
    if (clear) clear.hidden = false;
    var dimRow = document.getElementById('wallpaper-dim-row');
    if (dimRow) dimRow.hidden = false;
  }

  function clearWallpaper() {
    if (currentObjectUrl) {
      URL.revokeObjectURL(currentObjectUrl);
      currentObjectUrl = null;
    }
    var wallpaper = document.querySelector('.kotoba-wallpaper');
    if (wallpaper) wallpaper.remove();
    document.body.classList.remove('has-kotoba-wallpaper');
    dbDelete(WALLPAPER_KEY).catch(function () {});
    var clear = document.getElementById('wallpaper-clear');
    if (clear) clear.hidden = true;
    var dimRow = document.getElementById('wallpaper-dim-row');
    if (dimRow) dimRow.hidden = true;
  }

  function loadWallpaper() {
    dbGet(WALLPAPER_KEY).then(function (blob) {
      if (blob instanceof Blob && blob.size > 0) setWallpaper(blob);
    }).catch(function () {});
  }

  function buildWallpaperControls(panel) {
    if (!panel || panel.querySelector('.wallpaper-settings')) return;

    var section = document.createElement('div');
    section.className = 'wallpaper-settings';
    section.innerHTML =
      '<h4>背景 · Wallpaper</h4>' +
      '<div class="wallpaper-actions">' +
        '<button type="button" class="wallpaper-upload-btn" id="wallpaper-upload">Upload image / GIF</button>' +
        '<button type="button" class="wallpaper-clear-btn" id="wallpaper-clear" hidden>Reset</button>' +
      '</div>' +
      '<input type="file" id="wallpaper-file" accept="image/*,.gif" hidden>' +
      '<p class="wallpaper-progress" id="wallpaper-progress" hidden></p>' +
      '<div class="wallpaper-dim-row" id="wallpaper-dim-row" hidden>' +
        '<label for="wallpaper-dim">Dim</label>' +
        '<input type="range" id="wallpaper-dim" min="15" max="90" value="' + DEFAULT_DIM + '">' +
      '</div>' +
      '<p class="wallpaper-hint">Set your own photo or GIF as the background. Stored only on this device — never uploaded. The theme picker and the Dim slider both control how strongly it shows through, so words stay readable.</p>';

    panel.appendChild(section);

    var upload = section.querySelector('#wallpaper-upload');
    var input = section.querySelector('#wallpaper-file');
    var clear = section.querySelector('#wallpaper-clear');
    var progress = section.querySelector('#wallpaper-progress');
    var dimSlider = section.querySelector('#wallpaper-dim');

    dimSlider.value = readDim();

    upload.addEventListener('click', function () { input.click(); });
    input.addEventListener('change', function () {
      var file = input.files && input.files[0];
      input.value = ''; // allow re-picking the same file later
      if (!file) return;
      if (!file.type || file.type.indexOf('image/') !== 0) {
        progress.hidden = false;
        progress.textContent = 'That file doesn\u2019t look like an image or GIF.';
        return;
      }
      if (file.size > MAX_WALLPAPER_BYTES) {
        progress.hidden = false;
        progress.textContent = 'That file is larger than 60MB — try a smaller image or GIF.';
        return;
      }
      progress.hidden = true;
      dbPut(WALLPAPER_KEY, file).then(function () {
        setWallpaper(file);
        if (window.Sfx) Sfx.tap();
      }).catch(function () {
        // Keep the existing app functional even if local storage is unavailable.
        setWallpaper(file);
      });
    });
    clear.addEventListener('click', function () {
      clearWallpaper();
      progress.hidden = true;
      if (window.Sfx) Sfx.tap();
    });
    dimSlider.addEventListener('input', function () {
      var pct = Number(dimSlider.value);
      applyDim(pct);
      saveDim(pct);
    });
  }

  function init() {
    makeBottomNav();
    document.body.classList.add('kotoba-shell-ready');

    var panel = document.getElementById('settings-panel');
    buildWallpaperControls(panel);
    loadWallpaper();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true });
  } else {
    init();
  }
})();
