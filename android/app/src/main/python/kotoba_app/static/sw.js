// Minimal service worker: precache the app shell (CSS/JS/icons) so the
// app still opens (styled, with cached pages) when there's no network,
// and use a network-first strategy everywhere else so content stays
// fresh whenever a connection is available.

const CACHE_NAME = "kotoba-shell-v12";
const SHELL_ASSETS = [
  "/static/css/style.css",
  "/static/css/ui-shell.css",
  "/static/js/app.js",
  "/static/js/learner.js",
  "/static/js/speech.js",
  "/static/js/smart_review.js",
  "/static/js/favorites.js",
  "/static/js/backup.js",
  "/static/js/placement.js",
  "/static/js/grammar.js",
  "/static/js/speaking.js",
  "/static/js/jlpt_mock.js",
  "/static/js/games.js",
  "/static/js/japan_explorer.js",
  "/static/js/conversation_practice.js",
  "/static/js/story_audio.js",
  "/static/js/sfx.js",
  "/static/js/theme.js",
  "/static/js/ui-shell.js",
  "/static/js/home.js",
  "/static/js/reaction.js",
  "/static/js/roadmap.js",
  "/static/js/roadmap_chapter.js",
  "/static/js/trace.js",
  "/static/js/feedback.js",
  "/static/js/kana.js",
  "/static/js/kanji_list.js",
  "/static/js/everyday.js",
  "/static/js/practice.js",
  "/static/js/flashcards.js",
  "/static/js/story.js",
  "/static/js/verbs.js",
  "/static/js/romaji.js",
  "/static/js/write.js",
  "/static/js/streak.js",
  "/static/js/jp-clock.js",
  "/static/js/kanji_practice.js",
  "/static/js/jlpt_practice.js",
  "/static/js/jlpt_exam_practice.js",
  "/static/manifest.json",
  "/static/icons/icon-192.png",
  "/static/icons/icon-512.png",
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(SHELL_ASSETS)).catch(() => {})
  );
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET") return;

  event.respondWith(
    fetch(req)
      .then((res) => {
        // keep a copy of successful shell/page responses for offline use
        if (res && res.status === 200) {
          const copy = res.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(req, copy)).catch(() => {});
        }
        return res;
      })
      .catch(() => caches.match(req))
  );
});
