# Kotoba — Japanese Learning App

A Flask web app for learning Japanese: hiragana, katakana, and kanji,
built from a curated dataset of 408 kanji (with on-yomi, kun-yomi,
stroke counts, and ~1,300 vocabulary words) extracted from a beginner
kanji textbook.

## Features

### v4.1 Japan Explorer + adaptive learning

- **Japan Explorer** — an animated, searchable map covering all **47 prefectures through their prefectural-capital pins**. Open a location to see a concise learning profile, what the area is known for, local food/culture cues, three original offline illustration postcards, difficulty-aware vocabulary, a useful Japanese phrase, pronunciation controls and a three-question mini quiz.
- **Map-based progression** — visited locations become passport stamps, first visits award XP, and Japan Starter / Regional Explorer / Japan Passport achievements reward 5 / 20 / 47 locations. Search results can jump directly to a place, and the map supports region filters, unvisited-only study and a Surprise Me mode.
- **Level-aware map lessons without needless repetition** — Beginner / Intermediate / Advanced changes the local term and phrase. Each stop combines its location-specific word with fresh travel/culture vocabulary, avoiding immediate generic-word repeats during the session while keeping missed quiz words eligible for Smart Review.
- **Offline-first map visuals** — the in-app coastline and all 141 location postcards are original, lightweight SVG artwork bundled with the project. The supplied watermarked reference map is not redistributed; the map is deliberately stylized for study rather than navigation.

- **Smart Daily Review (SRS)** — schedules weak items sooner, tracks mastery from New → Mastered, fills spare review slots with unseen level-appropriate vocabulary, and keeps mistakes until they are recovered.
- **Mistake Notebook + Favorites / My Lists** — every scored learning surface can feed one learner history; save vocabulary, kanji and grammar for later.
- **Placement test** — a 25-question diagnostic covering kana plus N5–N1 vocabulary, kanji and grammar recommends where to enter the roadmap. It is study placement, not an official JLPT score prediction.
- **Listening & shadowing** — Japanese playback and slow playback on core vocabulary/kanji/grammar/story/conversation surfaces. Android uses native Japanese TTS for an offline playback path.
- **Speaking practice** — Japanese speech recognition when the browser/device exposes it, with recording/self-comparison fallback otherwise.
- **Grammar Dictionary + advanced roadmap** — 229 searchable patterns/expressions and new upper-intermediate, N2 and source-backed N1 learning chapters. General-frequency level tags are approximate study guidance.
- **Timed JLPT practice mocks** — source-backed N5–N1 timed sessions with navigation, flags, category summaries and furigana explanations after submission. The available uploaded books have uneven section coverage, so these do not claim official JLPT section balance.
- **Learning games** — Match, Audio Choice, Kana Rush, Verb Challenge and Sentence Hunt, tied into learner history where answers are scored.
- **XP, daily missions, achievements and Koto reactions** — lightweight motivation without locking study content.
- **Portable backup** — export/restore local learner state, SRS, progress, favorites and preferences. User profiles are local to the installation; no cloud backend is required.

- **Search** — type in English *or* Japanese (kanji, kana, or romaji)
  in the same search box.
- **Hiragana / Katakana** — full charts (basic, dakuten/handakuten,
  combination sounds) plus a flashcard mode.
- **Kanji** — browse all 408 characters, each with on-yomi, kun-yomi,
  stroke count, and its vocabulary words.
- **Everyday Life words** — 3,700+ unique words and phrases (well beyond the
  requested 250), shown in kanji, hiragana, and English together,
  browsable by category (greetings, numbers, family, food,
  directions, time, and more) with its own filter box. **Click any
  word** to see it used in a real example sentence (kanji/hiragana/
  romaji/English) with a matching emoji and a smooth pop-in modal.
  The supplied 2,000-word frequency list is merged into the app rather than appended blindly: duplicate written forms collapse to one record, while new words are assigned Easy / Medium / Hard using frequency, kanji/JLPT complexity, word length, and part of speech.

- **Search now covers everyday English words** — "apple", "coffee",
  "umbrella" and 100+ other fruits/animals/food/electronics/clothing
  words now resolve to their Japanese word, even though the kanji
  textbook never covers them (they don't build off a lesson kanji).
  See `data/common_words.json` / `gen_common_words.py`.
- **Writing Practice** — every script has two modes. *Tracing*: draw
  a character inside its practice square over a faded guide, then tap
  **Check my writing** and the app scores the attempt (see
  "How stroke checking works" below). Available for hiragana, katakana
  *and* all 408 kanji. *Keyboard*: an on-screen kana keyboard that
  converts romaji to kana as you type (own conversion engine in
  `static/js/romaji.js`, unit-tested against 17 known-correct
  conversions), plus click-to-type kana keys.
- **Themes** — five palettes drawn from Japanese materials, plus
  "Match system": **Washi** 和紙 (rice paper + indigo ink, the
  default), **Sakura** 桜, **Matcha** 抹茶, **Sumi** 墨 (dark), and
  **Yozakura** 夜桜 (dark). Pick one from the 色 button in the header.
  The choice is remembered and applied before the first paint, so
  navigating between pages never flashes the light palette.
- **Sound & vibration** — answer chimes, flashcard flips and
  writing-check feedback, all synthesised at runtime with the Web
  Audio API (no audio files to bundle or download). Both can be turned
  off from the same header menu.
- **About & Feedback** — an About page, and a Feedback page where
  notes are saved on the device, with a one-tap option to mail them to
  the developer instead.
- **Verbs** — 148 common verbs grouped as godan / ichidan / irregular.
  Click one to see all eight forms (polite, polite negative, polite past,
  te-form, plain past, plain negative, potential, volitional) in both
  kanji and kana.
- **Streak** — a 🔥 badge in the header (visible on every page) tracks
  consecutive days of practice, Duolingo-style. Finishing a Practice
  round or a Flashcards deck marks today as active. Click the badge
  for a full page with your current streak, longest streak ever,
  total active days, and a 30-day calendar. Miss a day and the streak
  resets — the day just gone still has a same-day grace window (it
  only resets once *today* passes with nothing logged). Stored in
  `data/streak.json`; see `_compute_streak()` in `app.py`.
- **Installable as a mobile app (PWA)** — the app has a manifest,
  generated icons, and a service worker, so on a phone you can open
  it in the browser and "Add to Home Screen" (Android: browser menu →
  Install app / Add to Home screen; iOS Safari: Share → Add to Home
  Screen). It then opens full-screen with its own icon, no browser
  chrome, and keeps working (from cache) with no connection.
- **Conversations** — 50 full dialogues for everyday
  situations: ordering at a café/restaurant, asking directions, a
  work meeting, calling in sick, a job interview, hotel check-in,
  apartment hunting, small talk about weather/family/hobbies, and
  more. Each line shows kanji/hiragana/romaji/English (each
  toggleable), plus a vocab list and useful-phrases callout per
  conversation. See `data/conversations.json` /
  `gen_conversations.py`.
- **Short Stories** — 19 graded stories you read line by line, with
  hiragana / romaji / English each toggleable on or off. Each ends with
  multiple-choice comprehension questions (answer + explanation shown on
  click) and a full breakdown: what happens, the grammar points used,
  and cultural background.
- **Flashcards** — flip-card decks for kanji, vocabulary, verbs,
  hiragana and katakana, with difficulty and deck-size options and a
  knew/didn't-know score.
- **Practice** — pick Easy / Medium / Hard / Mixed difficulty and a
  round length (10, 20, or 30 words). Learn the words, then complete
  real example sentences with them, choosing from 6 options. **Right
  or wrong, you always get the full breakdown**: on-yomi, kun-yomi,
  the sentence in kanji / hiragana / romaji, and a note on where the
  word is commonly used.

### Japan Explorer data

`data/japan_explorer.json` contains the 47 learning locations and level-specific map lessons. `static/js/japan_explorer.js` renders the interactive map and learning drawer, while `static/images/japan_explorer/` contains three bundled SVG postcards per prefecture. Coordinates identify prefectural capitals and the coastline is intentionally simplified; this feature is for language/culture exploration, not turn-by-turn or geographic navigation.

## Setup

Requires Python 3.9+.

```bash
cd kotoba-japanese-app
python -m venv venv
source venv/bin/activate      # on Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Then open **http://127.0.0.1:5000** in your browser.

### Trying it on your phone

By default Flask only listens on your own computer. To open it from
your phone on the same Wi-Fi network, edit the last line of `app.py`
from `app.run(debug=True)` to `app.run(debug=True, host="0.0.0.0")`,
restart it, then visit `http://<your-computer's-local-ip>:5000` from
your phone's browser (find the IP with `ipconfig` on Windows or
`ifconfig`/`ip a` on Mac/Linux). From there, use your phone browser's
"Add to Home Screen" option to install it as an app icon.

Two things worth knowing about the PWA setup:
- Service workers require either `https://` or `localhost`/`127.0.0.1`.
  Accessing the app over plain `http://` at a LAN IP (like
  `192.168.1.23:5000`) is fine for using the app, but the browser will
  refuse to register the service worker there, so offline caching
  won't kick in on your phone unless you put it behind HTTPS (a tool
  like `ngrok` or deploying it somewhere with a real certificate both
  work for testing this).
- Guest progress is device-local. Optional Kotoba profiles separate streaks,
  SRS history, favorites and progress by username on the same installation.
  Profiles are not cloud accounts; use **Backup & Restore** to move learning
  state between installations.

## Project structure

```
app.py                        Flask routes + search/practice/categorization logic
data/
  kanji_data.json             408 kanji entries with vocab
  hiragana.json               hiragana chart
  katakana.json               katakana chart
  practice_sentences.json     curated example sentences for practice mode (50 words)
  everyday_extra.json         curated greetings/phrases not in the kanji book
templates/                    Jinja2 HTML templates
static/css/style.css          styling + all five theme palettes
static/fonts/                 optional bundled webfonts (see its README)
static/js/
  theme.js                    theme switching + the header settings menu
  sfx.js                      Web Audio sound effects and haptics
  trace.js                    the tracing pad + stroke checking
  write.js                    Writing Practice page (mounts three tracers)
  feedback.js                 Feedback form
  kana.js, kanji_list.js, everyday.js, practice.js, flashcards.js, ...
sync_android.py               regenerates the APK's copy of the web app
```

## Notes on the data

- The kanji, readings, and vocabulary were extracted and parsed from
  a beginner Japanese textbook's text layer, then cleaned up
  programmatically. A small number of entries may have minor
  formatting quirks — if you spot one, it's easy to fix directly in
  `data/kanji_data.json` (plain JSON).
- **Difficulty tiers** (Easy/Medium/Hard) are assigned automatically
  from each kanji's stroke count and the vocabulary word's length —
  see `difficulty_for()` in `app.py`. It's a heuristic, not a
  perfect JLPT-style rating, but it splits the pool into three
  sensible bands (99 easy / 192 medium / 117 hard words).
- **Categories** on the Everyday Life page are also assigned
  automatically from each word's English meaning via keyword
  matching — see `CATEGORY_KEYWORDS` in `app.py`. Adjust the keyword
  lists there if you want words re-sorted differently.
- **Example sentences on the Everyday Life page**: words that also
  have a hand-curated practice sentence use that; every other word
  gets a sentence built from a per-category template (see
  `SENTENCE_TEMPLATES` and `build_everyday_sentence()` in `app.py`)
  — e.g. animals slot into "Tanaka-san's ___", places slot into "I'm
  going to the ___", etc. It's a light heuristic, not hand-checked
  grammar for all 1,600+ words, so an occasional sentence will read
  a bit stiffly — easiest fix is adding that word to
  `gen_sentences.py` as a fully curated one.
- **Emoji "images"**: since this is an offline app with no bundled
  photos, each word gets a large emoji as a lightweight visual
  instead — matched by keyword first (`EMOJI_KEYWORDS` in `app.py`),
  falling back to one emoji per category. If you'd rather show real
  photos, the natural place to add that is inside
  `everyday_detail()`/`build_everyday_sentence()` — call an image API
  (e.g. Pexels or Unsplash, both have free API keys) keyed off the
  English `meaning` field and return an image URL alongside the
  sentence data for the modal to display.
- The practice mode's example sentences are hand-written for a
  curated set of 50 words spanning all three difficulty tiers, so
  those quizzes stay natural and accurate. Every other word in the
  pool still works in practice — you'll get an auto-generated
  (simpler) sentence instead of a hand-crafted one. To add more
  curated sentences, edit `gen_sentences.py` (or add directly to
  `data/practice_sentences.json`) with this shape:

  ```json
  {
    "kanji_id": 21,
    "word": "山",
    "sentence_kanji": "毎週末、山に登ります。",
    "sentence_hiragana": "まいしゅうまつ、やまにのぼります。",
    "sentence_romaji": "Maishūmatsu, yama ni noborimasu.",
    "sentence_en": "I climb a mountain every weekend.",
    "usage_note": "Also seen in place names like 富士山 (Mt. Fuji)."
  }
  ```

  Then re-run `python gen_sentences.py` to regenerate the JSON (or
  just hand-edit the JSON file directly).

## About the Japanese Picture Dictionary (4th source book)

A fourth book, the *Japanese Picture Dictionary* (Timothy G. Stout,
Tuttle), added **582 words across 16 new or expanded categories**:
Shapes & Sizes, Opposites, Money & Shopping, Seasons & Holidays,
School & Learning, Counters, Work & Jobs, Health & Body, Environment
& Nature, Sports & Fitness, Travel, Countries, Languages, Music,
Transportation, and House & Furniture — plus extra entries folded
into Family & People, Animals, Colors, Directions & Position, and
Food & Drink.

This PDF's Japanese text uses a non-standard CID font encoding that
even installing poppler's Adobe-Japan1 CMap resource couldn't
decode, so bulk text extraction wasn't possible. Every entry in
`data/picture_dict.json` (built by `gen_picture_dict.py`) was instead
transcribed by rasterizing each page to an image and reading it
directly — 30+ chapter spreads' worth. If you want to add more from
the same book, the unread chapters (Life in the City, Years & Dates,
Learning Japanese, Computers & the Internet, My Smartphone) follow
the same layout, so the same page-image approach will work.

## About the three source books

- The **kanji textbook** (first upload) is where the 408 kanji, their
  readings and the 1,300+ vocabulary words come from — extracted from
  its text layer and cleaned up programmatically.
- The **600 Basic Japanese Verbs** PDF is an image-only scan with **no
  text layer at all** (zero extractable characters), so nothing could be
  pulled from it. The Verbs section is instead built from a hand-checked
  list of 148 common verbs plus a conjugation *engine* in
  `gen_verbs.py` that applies the standard godan / ichidan / irregular
  rules — including the 行く→行って exception and する→できる. The forms
  are generated from grammar rules, so they are correct by construction.
  To add verbs, append to the `VERBS` list in `gen_verbs.py` and re-run
  it; conjugations are produced automatically.
- The **Kanji Dictionary (2500, N5–N1)** PDF also has no usable text
  layer — what little it has is mojibake (garbled encoding), not
  Japanese. Running it through the parser would have filled the kanji
  section with corrupted entries, so the kanji section is unchanged.
  Getting the 2,500 kanji out would need OCR with a Japanese model
  (e.g. `tesseract -l jpn`), which is slow and would still need manual
  checking — worth doing as a separate pass if you want it.
- The **short story collection** is copyrighted (2023, all rights
  reserved), so its text is not redistributed in this app. The four
  stories in the Stories section are **original**, written for this app
  in the same Level-1 graded-reader style. Add your own in
  `gen_stories.py` — the format is plain JSON and documented at the top
  of that file.

## Notes on the Writing Practice keyboard's romaji converter

It's a straightforward phonetic converter (greedy longest-match table +
small-tsu and ん handling), not a full Japanese IME — it has no
dictionary and can't do kanji conversion or context-aware spelling.
Two known limitations worth knowing about:
- こんにちは (konnichiwa) comes out こんにちわ — phonetically "wa" is わ;
  the actual word is a fixed spelling exception no phonetic engine
  can know without a dictionary.
- Long vowels in katakana convert phonetically (e.g. "uu" → ウウ)
  rather than using the chōonpu mark ー that real katakana favors
  (e.g. コンピューター). The keyboard grid below the input always gives
  you the exact key if you want to swap it in by hand.

## How stroke checking works

Writing Practice needs to tell a good trace from a bad one without any
stroke-order data, so it compares shapes instead.

The guide character and the scoring mask are produced by the *same*
code (`drawGlyph` in `static/js/trace.js`) into two stacked canvases of
identical size — a guide layer and an ink layer. Because both come from
one `fillText` call, they line up exactly, and the app doesn't care
which font actually resolved. That matters inside the APK, where the
Google-hosted fonts never load.

Checking an attempt downsamples both canvases to a 64x64 grid and
measures two things:

- **coverage** — how much of the character you actually drew over
- **spill** — how much of your ink landed outside the character

A pass needs coverage of 62% or more *and* spill of 35% or less, so
neither scribbling over the whole square nor drawing one confident
stroke gets through. Both masks are dilated by two cells first, which
is roughly 10px of slack at the default size — enough that a fingertip
isn't punished for being imprecise. Tune the three constants at the top
of `trace.js` if it feels too strict or too soft.

Miss the same character more than twice and the square shakes and the
phone vibrates (`navigator.vibrate`, which is why the Android manifest
now requests the `VIBRATE` permission).

## Android app (built via GitHub Actions)

The `android/` folder is a full Android Studio project that wraps this
same Flask app into a real installable APK:

- **How it works**: the APK bundles a real Python interpreter via
  [Chaquopy](https://chaquo.com/chaquopy/) (Python-for-Android). When
  the app launches, `MainActivity.kt` starts `app.py`'s `run_server()`
  on a background thread — the exact same Flask app as the desktop
  version, just running locally on the phone instead of on your
  computer — then loads `http://127.0.0.1:5000/` into a full-screen
  WebView. Nothing leaves the device; the "server" is just Python
  code this same app started, talking to itself over loopback.
- **One source of truth.** The APK needs its own copy of `app.py`,
  `templates/`, `static/` and `data/` inside
  `android/app/src/main/python/kotoba_app/`, because that directory is
  what gets packaged. `sync_android.py` regenerates that copy from the
  top-level app (appending the `run_server` entry point), and CI runs
  it before every build — so an edit to a template can't silently miss
  the APK. Run it yourself after editing anything under `templates/`
  or `static/`:

  ```bash
  python sync_android.py
  ```
- **`.github/workflows/build-apk.yml`** builds a debug APK on every
  push that touches the app or `android/`, and on demand from the Actions tab
  (*Actions → Build Android APK → Run workflow*). It installs JDK 17,
  a pinned Gradle version, and the Android SDK, then runs
  `gradle :app:assembleDebug`.
- **Getting the APK**: after a workflow run finishes, open it from the
  *Actions* tab and download the `kotoba-debug-apk` artifact — a zip
  containing `app-debug.apk`. Transfer that to an Android phone and
  open it (you'll need to allow "install unknown apps" for whichever
  app you download it through, since this isn't distributed via the
  Play Store).
- **No `gradlew` is committed.** Rather than ship Gradle wrapper
  binaries I couldn't actually test in this environment, the workflow
  installs a pinned Gradle version directly
  (`gradle/actions/setup-gradle@v4`) and calls `gradle` straight —
  same result, one less generated binary to get wrong.

### A limitation worth knowing about

I built this Android project without being able to compile it myself:
this environment can't reach Google's Maven repository or Chaquopy's
Maven repository (both needed for an Android build), and there's no
Android SDK or emulator here either. Everything in `android/` is
correct as far as I could verify without actually running Gradle —
valid XML, balanced Groovy braces, a Python module that imports and
compiles cleanly, a workflow file that parses correctly — but the
*first* real build-and-run test will be whenever GitHub Actions
executes it. Android + Chaquopy projects fairly often need one or two
small adjustments the first time (an SDK version mismatch, a
dependency resolution hiccup) even when hand-built by someone with a
real dev environment. If the workflow fails, paste me the error from
the Actions log and I'll fix it from there.

## Extending it

- Swap the Flask dev server for `gunicorn`/`waitress` if you want to
  deploy this somewhere.
- The vocabulary/kanji data is plain JSON, so it's easy to add more
  entries by hand or write a script against another source book.
- Want a 4th difficulty or a totally different split? Edit
  `difficulty_for()` in `app.py` — it only looks at stroke count and
  word length, so it's easy to swap in your own rule.
