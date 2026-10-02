# v4.1.1 — Android build fix

- Fixed `_build_roadmap_quiz()` so advanced N3/N2/N1 grammar chapters rotate over the actual available question types instead of assuming exactly three.
- Prevents the `IndexError: list index out of range` seen in GitHub Actions Android smoke tests.
- Bumped Android package to **4.1.1 / versionCode 6**.

# v4.1.0 — Japan Explorer

- Added **Japan Explorer**, an animated learning map with all 47 prefectures represented by their prefectural-capital locations. The map is a purpose-built, stylized SVG rather than a copy of the supplied watermarked reference map.
- Added searchable **region and location exploration** with All / Hokkaido / Tohoku / Kanto / Chubu / Kansai / Chugoku / Shikoku / Kyushu / Okinawa filters, unvisited-only mode, major-city labels and a Surprise Me action that prefers unexplored stops.
- Added a responsive location drawer for every stop with Japanese/English names, reading, a concise area description, notable highlights, local tastes, and three original offline illustration postcards. There are **141 bundled SVG postcards** in total.
- Added **Beginner / Intermediate / Advanced map lessons**. Each stop contributes a local term and phrase, then mixes in fresh travel/culture vocabulary while avoiding immediate generic-word repeats within the current session.
- Added Japanese **TTS playback** for place names, map vocabulary and local phrases using the existing speech engine / Android native TTS path.
- Added a **three-question mini quiz** per stop. Correct/incorrect answers feed the unified learner engine, so missed map vocabulary can enter the Mistake Notebook and Smart Review rather than becoming isolated map trivia.
- Added a **Japan Passport** progression layer. The first visit to a unique location awards 12 XP and records a passport stamp; revisits do not farm XP. New achievements unlock at 5, 20 and all 47 explored locations.
- Added **Favorites/My Lists integration** for map places and words, plus global Search support for city, prefecture, Japanese names/readings, region, specialties and local foods. Search results deep-link back to the relevant map stop.
- Added Japan Explorer to Home, Explore, Progress and About surfaces, synchronized it into the Android package, bumped Android to **4.1.0 / versionCode 5**, and updated the offline shell cache.
- Extended Android smoke-test coverage to validate all 47 places and the map visit API. The map remains offline-first and does not depend on a live maps provider.

# v4.0.0 — Adaptive learner engine, listening/speaking, grammar, mocks & games

- Added an offline **Smart Daily Review** scheduler with New / Learning / Weak / Familiar / Mastered stages, due dates, mistake recovery and unseen-item fill.
- Added a **Mistake Notebook**, **Favorites / My Lists**, XP, daily missions, achievements and the existing Koto companion reactions across new learning flows.
- Added a balanced **placement diagnostic** spanning kana and N5–N1 vocabulary, kanji and grammar; it recommends a roadmap start without locking content.
- Added a searchable **Grammar Dictionary** with 229 patterns/expressions plus new N3, N2 and source-backed N1 roadmap chapters. General frequency-derived level tags are explicitly presented as study guidance, not official classifications.
- Added Japanese **text-to-speech** controls across core study surfaces, dialogue/story playback, slow shadowing and Android native Japanese TTS for offline APK playback.
- Added **Speaking Practice** using Japanese speech recognition where supported, with microphone recording + self-check fallback when recognition is unavailable.
- Added source-backed **timed JLPT mock sessions** for N5–N1. Results include category breakdowns and furigana explanations for both correct and incorrect answers.
- Added five adaptive games: Match, Audio Choice, Kana Rush, Verb Challenge and Sentence Hunt.
- Added **portable Backup & Restore** for learner state, SRS, streak, roadmap progress, favorites and browser settings. Profiles remain local/offline; this is not cloud sync.
- Android: added RECORD_AUDIO runtime handling, WebView microphone permission gating, native TTS bridge, version 4.0.0 packaging, and learner runtime files to the sync exclusions.
- Expanded Android smoke-test coverage for grammar pages, mocks, games, learner state, favorites, placement and backup restore.

# v3.3.0 — Frequency-ranked vocabulary expansion + level-aware dedup

- Imported the supplied **2000 Most Common Japanese Words in Context** PDF into `data/frequency_words.json` (1,999 extractable numbered source entries; the source numbering itself skips 1772 and repeats the written form `いい`).
- Added a reproducible importer, `build_frequency_words.py`, which preserves rank, written form, reading/romaji, part of speech, meaning, category, source example, and assigns an app difficulty tier.
- Difficulty is not rank-only: it combines source frequency, JLPT/kanji complexity, written-word length, and grammatical role so beginner selections do not receive arbitrary rare/complex vocabulary.
- Created one canonical `VOCAB_POOL` used by Vocabulary flashcards, progress, and search. Existing richer Kotoba records win on overlap; PDF records fill genuine gaps and contribute frequency metadata.
- Deduplicated the Everyday list and added **All / Easy / Medium / Hard** filters. Frequency rank is shown in the word detail badge when available.
- Vocabulary flashcard rounds now prioritize **unseen** words at the selected difficulty. Words already marked known are held back until the unseen pool is too small; missed words remain eligible for later review.
- Kept JLPT exam questions, curated Roadmap lessons, stories, and fixed conversations intact instead of randomly replacing their pedagogical wording.
- Updated offline service-worker cache to v10 and synchronized the expanded dataset into the Android package.

## v3.2.0 — JLPT N1 + Furigana Answer Feedback

- Added 38 EPUB-backed N1 exam-practice questions: 19 grammar-form choice and 19 sentence-building questions.
- JLPT Exam Q&A now supports N5, N4, N3, N2 and N1 (372 questions total).
- After every answer, whether correct or incorrect, the app now shows the completed/source answer sentence with ruby furigana on kanji where needed.
- N1 source-provided correct-choice rationale is included where available.
- Missed-question review also shows the sentence + furigana feedback.
- Updated offline service-worker cache and synchronized all changes into the Android package.

# v3.1.0 — JLPT exam Q&A practice from uploaded EPUBs

- Added a separate **Exam Q&A** practice mode inside JLPT while keeping the existing kanji practice unchanged.
- Imported source-backed practice for **N5, N4, N3 and N2** from the supplied exam-prep EPUBs: 180 N5, 60 N4, 36 N3 and 58 N2 questions.
- Added category and practice-length selection, immediate correct-answer feedback, final scores and missed-question review.
- N3 includes reading passages with their comprehension questions; N5/N4/N2 include the structured vocabulary/grammar/expression material supported by their source books.
- N1 deliberately has no Exam Q&A dataset because no N1 EPUB source was supplied.
- Synced the new template, JavaScript and question dataset into the Android package and bumped the offline service-worker shell to v8.

# v3.0.2 — Android crash fix (three crashes)

All three were Android-only: the web app and every desktop test were fine, so none were visible until a phone ran the APK.

- **Crash on launch: Python 3.8 syntax error.** `app.py` had a backslash inside an f-string expression (the radical label in the roadmap quiz). Python 3.12 allows it; the phone's Python 3.8 (Chaquopy 16's default) does not, so the module could not even be parsed. Fixed.
- **Crash on launch: sibling modules not importable.** `app.py` did a plain `import everyday_nl`. That works with `python app.py`, but in the APK the file is imported as `kotoba_app.app` and its folder is not on `sys.path`, so Python raised `ModuleNotFoundError` on a background thread and Android killed the app. The 3.0.1 note about packaging `roadmap_extra.py` was right that it must ship, but the lazy `import roadmap_extra` in the kana roadmap quiz had the same bare-import problem, so Hiragana/Katakana chapters would still have failed. Both now load through `_sibling()`, which goes through the package when there is one.
- **Crash when reopening the app or tapping the reminder notification.** Android recreates `MainActivity` while the process (and the Flask server thread) stays alive; each `onCreate()` started a second server on port 5000, Werkzeug exited with "Address already in use", and the uncaught exception on the bare thread killed the process. Fixed on three levels: `startFlaskServer()` starts one server per process and catches/logs failures; `run_server()` is idempotent and returns quietly if the port is already bound; the activity is `singleTask` and handles more config changes (font size, locale, density, fold/unfold) without being recreated.
- Onboarding overlay: added plain `top/right/bottom/left` and `vh` fallbacks for WebViews without `inset` / `dvh`.
- New `smoke_test_android.py`, run in CI **on Python 3.8** before the APK build: imports the packaged app under phone-like conditions, requests every page and API with every real ID, exercises the POST endpoints, and checks repeat `run_server()` calls. The workflow now also triggers on `everyday_nl.py` / `roadmap_extra.py` edits.

# v3.0.1 — Android crash fix

- Fixed Android roadmap lesson crash by packaging `roadmap_extra.py`, which is imported when kana roadmap quizzes are built.
- Android sync now excludes roadmap progress/placement files so development progress is not baked into fresh APKs.
- Pinned Android Flask dependency to 3.0.3 to match `requirements.txt` for reproducible builds.

# Changelog

### v3.0.0 — guided home, onboarding, Explore, Koto companion, lesson motion
- Rebuilt the home screen around one clear **Continue Learning** action with roadmap progress, streak, mastery stats, Daily Review, Practice, and Writing shortcuts.
- Added first-run **starting level + daily goal** setup so complete beginners, kana learners, basic learners, and JLPT learners can jump to an appropriate starting point.
- Added a dedicated **Explore** page and simplified top/mobile navigation into Learn, Review, Explore, Progress, and Practice.
- Roadmap now highlights only the single recommended next chapter instead of pulsing every unfinished node, while keeping every chapter open for free navigation.
- Added stage labels across the roadmap (Foundation → Beginner → Lower Intermediate → Intermediate → Mastery Check).
- Redesigned roadmap lessons with phase progress, answer motion, combo feedback, success particles, and a clearer completion screen.
- Replaced mixed reaction JPG/GIF artwork with **Koto**, one original CSS-drawn companion used consistently for encouragement and celebration.
- Corrected dynamic home/explore counts for verbs, conversations, stories, kanji, and JLPT content.
- Service-worker shell bumped to v7 and now precaches the new v3 scripts.

# What changed

### v2.9.3 — everything the Roadmap teaches now exists across the whole app

I audited every Roadmap word against the Everyday list, search, Vocabulary flashcards and the Verbs page: 431 words were Roadmap-only. Now:
- **Everyday / Vocabulary / Search:** 384 Roadmap words (computers, phones, months, shapes, grammar patterns, kanji terms, food, health...) are added with categories (new: Technology, Grammar Patterns, Daily Routines, Hobbies & Music, Kanji & Writing). Words that appear in a Roadmap sentence use that real sentence as their example. They also appear in Vocabulary flashcards (flip + select) and in search, where each result opens its Roadmap chapter.
- **Verbs page:** 25 verbs the Roadmap uses (着替える, 乗り換える, 戻る, 買い物する, ログインする, ダウンロードする...) added with full conjugations (148 verbs total).
- **Radicals:** new **Radicals** flashcard deck (flip + select, with meaning, position and origin), radicals appear in search (type 氵 or "water"), and the dashboard tracks radical progress.
- Conjugated-form chapters (て-form, potential) are not duplicated as words; their verbs live on the Verbs page.
- Fixes: ダウンロードする reading, awkward "next to" direction sentence. Service-worker cache v6.

### v2.9.2 — Hiragana & Katakana practice in the Roadmap

- First Steps had only two link nodes (Hiragana, Katakana) that opened the chart pages - no quiz. Each script now has four practice chapters: (1) vowels + K S T N, (2) H M Y R W + ん, (3) voiced sounds (゛ ゜), (4) combination sounds (きゃ etc.).
- Each chapter: a guidebook of its rows, flip-through cards, then a 30-question multiple-choice quiz asking both "which sound does this kana make?" and "which kana makes this sound?". You get right/wrong immediately plus an explanation (e.g. ぐ = く + two small marks, so k becomes g).
- The Hiragana/Katakana chart links stay at the top for writing practice. Kana questions also feed the First Steps Section Review and the Grand Review.

### v2.9.1 — JLPT kanji breakdown, kanji/reading intros, 50-question section reviews

- **Flashcards (Select answer, every deck incl. JLPT N5-N1):** after you tap an answer you see right/wrong immediately plus a full kanji breakdown — meaning, radical (and where it sits), how the kanji is built (for the app's own kanji), on-yomi and kun-yomi — then tap **Next**. Radical data now covers 1,990 of the 1,991 JLPT kanji (`radical_map_extra.py`, 54 more radicals).
- **Roadmap introductions:** *What Is Kanji?* (three scripts, meaning vs reading, okurigana, stroke order, how many kanji), *What Are Radicals?*, and *How to Read Kanji* (on/kun rules, sound-hint families like 青→静 晴 清 精).
- **Section Review:** every roadmap section now ends with a 50-question review (meaning, reading, English→Japanese, fill-in-the-blank, radical questions), opened by a recap of what the section covered. Every question shows the right answer **and an explanation** right after you answer. Chapter quizzes and the Grand Review (now 50 questions) show explanations too.

### v2.9.0 — radicals, unlocked roadmap, fuller chapters, Grand Review, natural Everyday sentences

**Radicals (部首)**
- New `/radicals` page: 57 core radical forms + extras, each with its Japanese name, meaning, position (hen / tsukuri / kanmuri / ashi / tare / nyō / kamae), how it formed, related shapes (人→亻, 水→氵…) and every kanji in the app that uses it (`data/radicals.json`, built by `gen_radicals.py`).
- Every kanji page now shows a **Radical & how this kanji is built** panel (e.g. 休 = 亻 + 木) and a **How to read** box separating kun-yomi and on-yomi with example words.
- Kanji flashcards (flip and multiple-choice modes) show the radical under the card; after you answer, the build story appears.
- Roadmap: new **Radicals** section after First Steps — "What Are Radicals?", seven radical-group chapters (their quizzes also ask "which radical is inside this kanji?"), and an explorer link.

**Roadmap**
- All chapters are unlocked from the start.
- Chapter word lists are much larger (all colours and shapes, all 12 months, family, body, house, time, food, travel…). The old 12-question cap is gone: each quiz asks every word plus every example sentence (max 50).
- Five new grammar chapters (describing nouns, 〜ながら, から/ので, つもり/ことにする, てみる/ておく/てしまう).
- New final section **Grand Review**: a summary of your progress and one mixed 40-question practice across every chapter.

**Everyday**
- Example sentences and mini-conversations are rebuilt (`everyday_nl.py`). Each word is classified first (drink, body part, animal, verb, adjective, opposite pair…) and only gets a pattern that fits it, so there are no more lines like 「田中さんのくじらです」. Words that fit nothing specific use neutral, always-correct patterns.

Also: service-worker cache bumped to v5.

### v2.1.1 — immersive shell fixes: opacity, theme picker, wallpaper legibility

`static/css/ui-shell.css`, `static/js/ui-shell.js`, `templates/base.html`,
`static/sw.js`, `app.py`

The immersive glass shell (`IMMERSIVE_UI_SHELL.md`) had three problems,
all from the same root cause: it defined its own fixed dark color
palette under `[data-ui-shell="immersive"]`, at the same CSS specificity
as the theme picker's `[data-theme="…"]` rules and loaded *after* them —
so it always won, silently.

- **Theme picker did nothing.** Switching Washi/Sakura/Matcha/Sumi/
  Yozakura changed `data-theme`, but every color the glass shell painted
  with was hardcoded, not derived from that attribute. Fixed by deleting
  the shell's own palette entirely — every glass surface now reads
  `var(--card-bg)`, `var(--paper)`, `var(--ink)`, etc. (the same tokens
  `style.css` already defines per theme) and only adds translucency with
  `color-mix()` on top. Pick a theme and the whole shell — header, hero,
  cards, bottom nav, wallpaper scrim — recolors with it.
- **"Too transparent."** Cards, the header and inputs were `rgba(255,
  255,255,.16–.20)` — mostly see-through. Raised to 90–96% opacity
  (`--shell-surface`, `--shell-surface-strong`, `--shell-header-bg`,
  `--shell-input-bg`), each declared with a plain opaque fallback before
  the `color-mix()` version for browsers that lack it.
- **Wallpaper made text unreadable / didn't adapt.** The photo's overlay
  was a fixed dark gradient regardless of theme or content. It's now a
  `var(--paper)` scrim (so it darkens for dark themes, stays light for
  light ones) at an adjustable strength — a new **Dim** slider in the
  背景 · Wallpaper panel (15–90%, default 60%, saved to `localStorage`
  and applied pre-paint so it doesn't flash). Practice/writing surfaces
  (kana tiles, kanji cards, the tracing stage) were never touched by the
  shell to begin with, so kana/kanji you write on stay fully opaque and
  legible no matter what wallpaper is behind them.
- Also fixed: `data-ui-shell="immersive"` was being set by JavaScript at
  the very end of `<body>`, so every navigation rendered the plain theme
  first and then visibly snapped into the glass look a moment later.
  It's now a static attribute on `<html>` in `base.html`, so there's no
  flash. A file-size guard (60MB) was added to the wallpaper picker, and
  `static/sw.js`'s precache list/cache name were updated so the fixed
  assets actually reach the offline APK build.

---

Your nine items, plus the themes, mapped to the files that implement
them. Everything was smoke-tested against a local `python app.py` run
(all routes 200, feedback API verified end to end, all JS syntax-checked).

---

### 1 & 2 — page pans sideways / nav should scroll on its own

`static/css/style.css`

Your diagnosis was right, and the specific cause is a flexbox default:
flex items get `min-width: auto`, so `.site-nav` refused to shrink below
the combined width of its ten links and pushed the whole document wider
than the screen. The hero text and the flashcard's "Didn't know" button
were casualties of the same thing.

- `.site-nav` now has `min-width: 0` (lets it shrink) plus
  `overflow-x: auto` (turns the overflow into its own scroll strip),
  `flex-wrap: nowrap`, and `white-space: nowrap` on the links.
- `overscroll-behavior-x: contain` stops a swipe on the nav from
  chaining out to the page.
- `html, body` get `overflow-x: hidden` and `max-width: 100%` as a
  backstop, so no future element can reintroduce the problem.
- Below 880px the nav drops to its own full-width row.
- `static/js/app.js` scrolls the active nav item into view on load,
  since the section you're on can now start off-screen.

### 3 — tighter tracing area + mistake detection

`static/js/trace.js` (new), `static/css/style.css`

- The stage **is** the character box now: a square whose guide glyph is
  measured with `TextMetrics` and scaled to fill 80% of it, so there's
  no dead margin to draw in. It carries a 田-style centring guide like a
  genkō-yōshi practice square.
- Checking compares your ink against the target on a 64×64 grid, scoring
  **coverage** (how much of the character you traced) and **spill** (how
  much ink landed outside it). Both must pass — see "How stroke checking
  works" in the README for the thresholds and how to tune them.
- Three misses on the same character → the square shakes and the phone
  vibrates. Needed `VIBRATE` in `android/app/src/main/AndroidManifest.xml`.

### 4 — same tracing for hiragana and katakana

`templates/write.html`, `static/js/write.js`

One reusable component mounted three times. Hiragana and Katakana panels
now have **Tracing / Keyboard** sub-tabs (tracing first), each with a
scrollable character picker. Kanji keeps its search box.

### 5 — "Write" → "Writing Practice"

`templates/base.html` (nav), `templates/index.html` (homepage card),
`templates/write.html` (page title and `<title>`), `app.py`.

`/writing-practice` added as a route; `/write` kept registered so old
bookmarks and any cached service-worker entry still resolve.

### 6 — sound effects

`static/js/sfx.js` (new)

Synthesised at runtime with the Web Audio API rather than loaded from
files — worth it here because the APK has no network, so there's nothing
to miss and nothing added to the download. Tones come from the yo scale
(よな抜き音階). Wired into: practice quiz answers, story quiz answers,
flashcard flip, kana chart flip, writing-check pass/fail, round complete,
and key taps. Mute toggle in the header menu.

### 7 — verb and everyday popups misfit on mobile

`static/css/style.css`

Below 560px both modals become bottom sheets: full width, anchored to the
bottom edge, with a grab handle. Height is based on `100dvh` (the
*visible* viewport) so a collapsing address bar can't push the card
off-screen — that's what `86vh` was getting wrong. Safe-area padding for
notched phones, and the conjugation table is `table-layout: fixed` so it
stops forcing the card wider than the screen.

### 8 — About Us

`templates/about.html` (new), `/about` in `app.py`

Aryan Raj · Software Engineer · Aryanrajr868@gmail.com. Linked from the
footer, the header settings menu, and a homepage card.

### 9 — Feedback

`templates/feedback.html`, `static/js/feedback.js` (new),
`/feedback` + `/api/feedback` in `app.py`

Topic, 1–5 rating, message, optional name. Saved to
`data/feedback.json` on the device; there's no server to send to, so
"Send by email instead" hands the note to the phone's mail app — the
only path off-device, and the person's choice.

### Themes + dark mode

`static/css/style.css`, `static/js/theme.js` (new), `templates/base.html`

Five palettes plus Match System: **Washi** 和紙 (default), **Sakura** 桜,
**Matcha** 抹茶, **Sumi** 墨 (dark), **Yozakura** 夜桜 (dark). Every
hardcoded colour in the stylesheet became a token, so a theme is just a
different `data-theme` value on `<html>`. An inline script in `<head>`
applies the saved theme before the first paint, so navigation never
flashes the light palette. `values-night/themes.xml` added on the Android
side for the same reason at launch.

---

## Things I fixed along the way

- **`templates/base.html`** had `class="{{ 'active' if ... }}nav-cta"`,
  which concatenates to `activenav-cta` — so the Practice button lost its
  pill styling on its own page. Now `class="nav-cta {{ 'active' if ... }}"`.
- **The APK could silently miss your edits.** It ships its own copy of
  `app.py`/`templates/`/`static/`/`data/` under
  `android/app/src/main/python/kotoba_app/`, and the build workflow only
  triggered on `android/**`. Added `sync_android.py`, wired it into CI as
  a build step, and widened the trigger paths.
- **Webfonts blocked first paint in the APK.** `base.html` loads three
  Google Fonts. With no network, that request stalls rendering until it
  times out. It's now loaded non-blockingly
  (`media="print" onload="this.media='all'"`). See
  `static/fonts/README.md` for making the app fully self-contained.
- **`mailto:` in a WebView** just shows an error page, so
  `MainActivity.kt` now overrides URL loading to hand non-local schemes
  to the system. Also added the Android 11+ `<queries>` entry so the mail
  app is resolvable, and `mediaPlaybackRequiresUserGesture = false` so
  the first sound of a session isn't swallowed.

