"""
Japanese Learning App
======================
A Flask web app for learning Japanese vocabulary (hiragana, katakana,
kanji) built from a curated dataset extracted from a beginner kanji
textbook, plus a hand-curated set of everyday phrases. Features:

- Search (type in English OR Japanese - kanji, kana, or romaji)
- Hiragana / Katakana charts for learning & memorizing
- Kanji lessons with on-yomi / kun-yomi, stroke count, vocabulary
- Everyday Life word list (3,700+ unique words/phrases, categorized, with
  kanji + hiragana + English shown together)
- Practice mode with Easy / Medium / Hard / Mixed difficulty and a
  choice of round length. Learn N words, then get quizzed with a
  real example sentence (6 options). Right OR wrong, you get the
  full explanation: on-yomi, kun-yomi, sentence in kanji/hiragana/
  romaji, meaning, and where the word is commonly used.

Run with:  python app.py
Then open http://127.0.0.1:5000 in your browser.
"""
import json
import os
import random
import re
import secrets
import unicodedata
from datetime import date, datetime, timedelta
from pathlib import Path

from flask import (
    Flask, render_template, request, jsonify, session, send_from_directory,
    Response, redirect, url_for,
)
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
DATA_DIR = Path(__file__).parent / "data"


def _load_or_create_secret_key():
    """A random key, generated once and reused across restarts (so
    existing login sessions survive a restart) instead of a value baked
    into the source - which anyone reading the app's code could use to
    forge a session cookie."""
    key_file = DATA_DIR / "secret_key.txt"
    if key_file.exists():
        existing = key_file.read_text(encoding="utf-8").strip()
        if existing:
            return existing
    new_key = secrets.token_hex(32)
    try:
        key_file.write_text(new_key, encoding="utf-8")
    except OSError:
        pass  # data dir not writable - key just won't persist across restarts
    return new_key


app.secret_key = _load_or_create_secret_key()
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=180)

# App version, shown in the footer. Bump this when shipping a meaningful
# set of changes so a person (or a bug report) can say which build they're
# on. History:
#   1.0.0 - original app: kana, kanji, verbs, everyday, stories,
#           conversations, flashcards, writing practice, practice rounds
#   1.1.0 - accounts (signup/login), streak tied to accounts, Dashboard
#           progress meters, Kanji Practice (4-option quiz)
#   1.2.0 - JLPT N5-N1 section: level browsing + per-level practice quiz,
#           JLPT badges cross-tagged onto the main Kanji section
#   1.3.0 - full review pass: Kanji/JLPT Practice now count toward the
#           Dashboard, JLPT kanji are searchable, About page and homepage
#           reflect the current feature set, CSRF protection on auth
#           forms, per-install random secret key, debug mode off by
#           default, service worker precache list refreshed
#   1.4.0 - JLPT dataset expanded to 1,000 kanji: N5 (103) and N4 (174)
#           complete, N3 (366) essentially complete, N2 (204) and N1 (153)
#           substantially larger; main Kanji section's JLPT badges
#           re-tagged against the bigger set (276 of 408 now matched)
#   1.5.0 - N5, N4 and N3 all complete (103 / 174 / 393 kanji - N3 now
#           past the standard ~370 count). N2 (204) and N1 (153) unchanged
#           this round. 1,027 JLPT kanji total, 278 of 408 in the main
#           Kanji section now carry a JLPT badge
#   1.6.0 - JLPT kanji cards and hiragana/katakana tiles are now clickable,
#           opening an enlarged detail view (character, readings, meaning,
#           level/difficulty) instead of the small grid text
#           (1.7.0's animation/touch/background-pattern pass was reverted
#           at the user's request - it introduced regressions)
#   1.8.0 - Flashcards page rebuilt with two modes: "Select answer" (new
#           default - 4 options per card, feedback shown immediately,
#           built for learning rather than testing) and "Flip cards"
#           (the original front/back review). The deck picker now covers
#           every JLPT level (N5-N1) alongside the original five decks
#           (Kanji/Vocabulary/Verbs/Hiragana/Katakana), each with its own
#           all/easy/medium/hard difficulty where the data supports it.
#           One new endpoint, /api/flashcards_mcq, powers both modes for
#           all ten decks. JLPT section itself is unchanged.
#   1.9.0 - JLPT dataset expanded further: N2 245 (from 204), N1 207
#           (from 153). N5/N4/N3 unchanged this round (already complete).
#           1,122 JLPT kanji total; 292 of 408 in the main Kanji section
#           now carry a JLPT badge (up from 278)
#   2.0.0 - N2 pushed to 339 (from 204, standard full ~415) and N1 to 236
#           (from 153, standard full ~1,100+) across this and the prior
#           round; N5/N4/N3 remain complete/near-complete. 1,245 JLPT
#           kanji total; 320 of 408 in the main Kanji section now carry a
#           JLPT badge (up from 292)
#   2.1.0 - N2 pushed to 410 (from 339, essentially complete against the
#           standard ~415 count). N1 pushed to 259 (from 236). Writing
#           Practice's kanji tracer now draws from all 1,339 JLPT kanji
#           via /api/kanji_pool, not just the original 408 (JLPT-only
#           entries have no stroke-count data, which the UI now handles
#           gracefully). Main Kanji section: 337 of 408 now carry a
#           badge. Added a contained tap/ripple touch effect (lives
#           inside the tapped element, not a page overlay) across
#           buttons, cards, and tiles site-wide.
# 2.6.0 - N1 kanji expanded from 259 to 855 (+596), filling the gap against
#           the standard public N1 kanji list. 1,991 JLPT kanji total.
#           New entries carry on/kun readings and a short meaning; like
#           other JLPT-only entries they have no stroke-count data.
# 2.9.0 - Radicals: /radicals (57 core radical forms + extras, how each is
#           formed, where it sits, which kanji use it), a radical panel on
#           every kanji page and in the kanji flashcards, a Radicals section
#           in the Roadmap, all chapters unlocked, larger chapter word lists
#           with full-length quizzes, a 40-question Grand Review, and
#           natural-sounding Everyday sentences/conversations.
# 3.1.0 - JLPT Exam Q&A: added EPUB-backed N5-N2 exam practice with instant
#           answer feedback, category/length selection, and offline Android/PWA assets.
#           Existing kanji practice is unchanged; N1 is not populated without a source EPUB.
# 3.2.0 - Added EPUB-backed N1 exam practice and answer explanations with
#           furigana/ruby feedback across JLPT N5-N1.
# 3.3.0 - Imported the supplied frequency-ranked Japanese vocabulary PDF as
#           a canonical app-wide vocabulary source. Added level-aware tiers,
#           duplicate merging, Everyday difficulty filters, and unseen-first
#           vocabulary flashcard selection so mastered words do not crowd out
#           new material until the selected pool has been worked through.
# 4.0.0 - Learner Engine: spaced repetition/Daily Review, Mistake Notebook, favorites/lists,
#           placement test, grammar browser, N3-N1 roadmap expansion, source-backed JLPT mock mode,
#           Japanese TTS/shadowing, speaking practice with recognition/recording fallback, XP/missions/
#           achievements, learning games, portable backup/restore, and Android microphone support.
# 4.1.1 - Fix roadmap quiz rotation for grammar chapters with fewer than 3 prompt types.
# 4.1.0 - Japan Explorer: animated 47-prefecture map using prefectural-capital pins,
#           level-aware local/travel vocabulary, illustrated offline postcards, audio, mini quizzes,
#           passport stamps/XP, search and region filters, favorites, SRS and Mistake Notebook integration.
# 2.8.0 - Roadmap complete: all 42 chapters are playable. Sections 5 (Food &
#           Drink), 6 (Modern Life) and 8 (Toward Fluency) filled in; Section 7
#           is now real grammar (particles, adjectives, counters, sentence
#           patterns) with a "Guidebook" explanation panel, plus two new
#           chapters: the te-form and saying "can do".
# 2.7.3 - Roadmap Sections 3 (Out and About) and 4 (People & Culture) filled
#           in: 10 more lessons. 19 of 40 chapters are now playable.
# 2.7.1 - Roadmap Section 2 (Everyday Life) filled in: My Family, My House,
#           The Human Body, Daily Routines, Telling Time, Days & Dates.
# 2.7.0 - Roadmap: a Duolingo-style learning path (/roadmap) of 40 chapters
#           across 8 sections. Section 1 is fully playable (Hiragana and
#           Katakana link to the existing charts; Greetings, Numbers and
#           Colors are new lessons with meaning/reading/fill-in-the-blank
#           quizzes). Sections 2-8 show as locked "coming soon" nodes.


def _sibling(name):
    """Import a module that lives next to this file.

    `python app.py` puts this folder on sys.path, so a plain
    `import everyday_nl` works there. The Android build instead imports this
    file as `kotoba_app.app` (Chaquopy), where the folder is NOT on sys.path
    and a plain import raises ModuleNotFoundError - which crashed the app on
    launch. Going through the package when there is one works in both cases.
    Any new helper module must also be listed in MODULES in sync_android.py.
    """
    import importlib
    if __package__:
        return importlib.import_module("." + name, __package__)
    return importlib.import_module(name)


_nl = _sibling("everyday_nl")
_learner = _sibling("learner_engine")

APP_VERSION = "4.1.1"


def load_json(name):
    with open(DATA_DIR / name, encoding="utf-8") as f:
        return json.load(f)


KANJI_DATA = load_json("kanji_data.json")                  # 408 kanji entries with vocab
HIRAGANA_DATA = load_json("hiragana.json")                  # hiragana chart
KATAKANA_DATA = load_json("katakana.json")                  # katakana chart
PRACTICE_SENTENCES = load_json("practice_sentences.json")   # curated sentences
EVERYDAY_EXTRA = load_json("everyday_extra.json")           # curated greetings/phrases
COMMON_WORDS = load_json("common_words.json")               # fruits/animals/food not in the kanji book
FREQUENCY_WORDS = load_json("frequency_words.json")           # supplied frequency-ranked 2000-word PDF
GRAMMAR_DATA = load_json("grammar.json")                         # grammar browser + advanced roadmap source
PICTURE_DICT_WORDS = load_json("picture_dict.json")          # from the Japanese Picture Dictionary (Stout)
VERBS_DATA = load_json("verbs.json")                        # verbs + rule-generated conjugations
STORIES_DATA = load_json("stories.json")                    # original graded short stories
CONVERSATIONS_DATA = load_json("conversations.json")        # original multi-turn dialogues
JLPT_KANJI = load_json("jlpt_kanji.json")                    # N5-N1 kanji, cross-referenced
JLPT_EXAM_QUESTIONS = load_json("jlpt_exam_questions.json")      # EPUB-backed N5-N1 exam practice
                                                              # against a Kanji Dictionary for
                                                              # Foreigners-style entry format
ROADMAP = load_json("roadmap.json")                          # Duolingo-style learning path
RADICALS_DATA = load_json("radicals.json")                   # radicals, forms, kanji->radical map
JAPAN_EXPLORER_DATA = load_json("japan_explorer.json")         # 47-prefecture geography + language explorer
JAPAN_PLACES = JAPAN_EXPLORER_DATA.get("places", [])
JAPAN_PLACE_BY_ID = {p["id"]: p for p in JAPAN_PLACES}

for _i, _v in enumerate(VERBS_DATA):
    _v["idx"] = _i

# Build lookup: kanji_id -> sentence entry
SENTENCE_BY_KANJI_ID = {}
for s in PRACTICE_SENTENCES:
    SENTENCE_BY_KANJI_ID.setdefault(s["kanji_id"], s)

# -------------------------------------------------------------- JLPT N5-N1 --

JLPT_LEVELS = ["N5", "N4", "N3", "N2", "N1"]
JLPT_LEVEL_LABELS = {
    "N5": "N5 — Beginner",
    "N4": "N4 — Elementary",
    "N3": "N3 — Intermediate",
    "N2": "N2 — Upper intermediate",
    "N1": "N1 — Advanced",
}
JLPT_LEVEL_DESCRIPTIONS = {k: v.split("—")[1].strip() for k, v in JLPT_LEVEL_LABELS.items()}
JLPT_BY_LEVEL = {lvl: [e for e in JLPT_KANJI if e["level"] == lvl] for lvl in JLPT_LEVELS}
JLPT_BY_CHAR = {e["kanji"]: e for e in JLPT_KANJI}
JLPT_EXAM_CATEGORIES = {
    lvl: sorted({q.get("category", "Practice") for q in JLPT_EXAM_QUESTIONS.get(lvl, [])})
    for lvl in JLPT_LEVELS
}

# --------------------------------------------------------------- radicals --
RADICALS = RADICALS_DATA["radicals"]
RADICAL_BY_ID = {r["id"]: r for r in RADICALS}
RADICAL_BY_GLYPH = {r["glyph"]: r for r in RADICALS}
KANJI_TO_RADICAL = RADICALS_DATA["kanji_to_radical"]
KANJI_BY_CHAR = {e["kanji"]: e for e in KANJI_DATA}
KANJI_STORIES = RADICALS_DATA["stories"]
RADICAL_POSITIONS = RADICALS_DATA["positions"]


def radical_info(char):
    """Radical panel data for one kanji, or None if we have no mapping."""
    g = KANJI_TO_RADICAL.get(char)
    r = RADICAL_BY_GLYPH.get(g) if g else None
    if not r:
        return None
    st = KANJI_STORIES.get(char) or {}
    return {
        "id": r["id"], "glyph": r["glyph"], "name": r["name"], "romaji": r["romaji"],
        "meaning": r["meaning"], "position": r["position_label"],
        "position_note": r["position_note"], "strokes": r["strokes"],
        "origin": r["origin"], "forms": r["forms"], "core": r["core"],
        "parts": st.get("parts", ""), "story": st.get("story", ""),
    }


def radical_hint(char):
    """Breakdown data for flashcards: radical, how the kanji is built,
    meaning and readings. Works for the app's own kanji and for every JLPT
    kanji (radical parts/story exist only for the app's own set)."""
    e = KANJI_BY_CHAR.get(char) or JLPT_BY_CHAR.get(char) or {}
    i = radical_info(char)
    base = {"meaning_full": e.get("meaning", ""), "on": e.get("on_yomi", ""), "kun": e.get("kun_yomi", "")}
    if not i:
        return base if (base["on"] or base["kun"]) else None
    base.update({"glyph": i["glyph"], "name": i["name"], "meaning": i["meaning"],
                 "parts": i["parts"], "story": i["story"], "position_note": i["position_note"]})
    return base


def reading_guide(entry):
    """Plain-language 'how to read this kanji' notes, built from the
    entry's own on/kun readings and vocabulary."""
    def has_kanji(t):
        return any("\u4e00" <= c <= "\u9fff" for c in t)
    kanji = entry["kanji"]
    compounds = [v for v in entry.get("vocab", []) if len(v["word"]) > 1 and v["word"] != kanji
                 and sum(1 for c in v["word"] if "\u4e00" <= c <= "\u9fff") >= 2]
    alone = [v for v in entry.get("vocab", []) if v["word"] == kanji or
             (v["word"].startswith(kanji) and not has_kanji(v["word"][1:]))]
    return {"on": entry.get("on_yomi", ""), "kun": entry.get("kun_yomi", ""),
            "compound": compounds[:3], "alone": alone[:3]}


# ---------------------------------------------------------------- roadmap --
ROADMAP_CHAPTERS = {c["id"]: c for sec in ROADMAP for c in sec["chapters"]}
ROADMAP_CHAPTER_ORDER = [c["id"] for sec in ROADMAP for c in sec["chapters"]]

# Tag the main Kanji-section entries with their JLPT level wherever one of
# our 408 kanji also appears in the JLPT N5-N1 set, so the existing Kanji
# pages can show it without an extra lookup.
for _entry in KANJI_DATA:
    _match = JLPT_BY_CHAR.get(_entry["kanji"])
    _entry["jlpt_level"] = _match["level"] if _match else None


# ------------------------------------------------------ categorization --

CATEGORY_KEYWORDS = [
    ("Numbers & Counting", ["one", "two", "three", "four", "five", "six", "seven",
                             "eight", "nine", "ten", "hundred", "thousand", "counter",
                             "number", "half"]),
    ("Time & Calendar", ["time", "hour", "minute", "month", "week", "year", "today",
                          "tomorrow", "yesterday", "morning", "evening", "night", "day",
                          "now", "sunday", "monday", "tuesday", "wednesday", "thursday",
                          "friday", "saturday", "every", "soon", "interval", "early"]),
    ("Family & People", ["father", "mother", "child", "brother", "sister", "family",
                          "son", "daughter", "parent", "person", "man", "male", "woman",
                          "female", "friend", "teacher", "student", "king", "myself"]),
    ("Nature & Weather", ["mountain", "river", "tree", "wood", "water", "fire", "earth",
                           "ground", "rain", "snow", "sky", "sun", "moon", "star", "wind",
                           "sea", "ocean", "flower", "stone", "field", "grass", "forest",
                           "grove", "heavens", "weather"]),
    ("Body & Health", ["eye", "ear", "mouth", "hand", "foot", "leg", "head", "face",
                        "hair", "heart", "body", "neck"]),
    ("Places & Buildings", ["school", "house", "home", "gate", "temple", "shop", "store",
                             "station", "city", "town", "country", "room", "market",
                             "capital", "library"]),
    ("Food & Drink", ["rice", "food", "tea", "fish", "meat", "vegetable", "fruit", "eat",
                       "drink", "meal"]),
    ("Directions & Position", ["left", "right", "up", "down", "inside", "outside", "near",
                                "far", "north", "south", "east", "west", "front", "back",
                                "middle", "path", "road"]),
    ("Colors", ["white", "black", "red", "blue", "green", "yellow"]),
    ("Animals", ["dog", "cow", "cattle", "bird", "horse", "sheep", "fish", "bug", "cat"]),
    ("Actions & Verbs", ["to "]),  # meanings like "To eat", "To see" start this way
    ("Size & Quantity", ["big", "small", "many", "few", "long", "short", "high", "low"]),
]


def categorize(meaning):
    m = meaning.lower()
    for label, keywords in CATEGORY_KEYWORDS:
        for kw in keywords:
            if kw in m:
                return label
    return "Everyday Objects & Ideas"


def difficulty_for(strokes, word_len):
    """Heuristic difficulty from the parent kanji's stroke count and the
    word's character length (more strokes / longer compounds = harder)."""
    if strokes <= 5 and word_len <= 2:
        return "easy"
    if strokes <= 10 and word_len <= 3:
        return "medium"
    return "hard"


def canonical_word_key(word):
    """Normalize a written word so overlapping sources do not create
    duplicate learning cards or rows."""
    text = unicodedata.normalize("NFKC", str(word or "")).strip()
    return re.sub(r"[\s・]+", "", text)


def dedupe_vocab(records):
    """Keep one record per written word, preserving the richer first source.

    If a later frequency-list record overlaps an existing app word, retain
    the existing record but attach its frequency rank / missing reading so
    the app gains metadata without showing the same word twice.
    """
    out, by_key = [], {}
    for raw in records:
        item = dict(raw)
        key = canonical_word_key(item.get("word"))
        if not key:
            continue
        if key not in by_key:
            by_key[key] = item
            out.append(item)
            continue
        keep = by_key[key]
        rank = item.get("frequency_rank")
        if rank and (not keep.get("frequency_rank") or rank < keep.get("frequency_rank")):
            keep["frequency_rank"] = rank
        if not keep.get("reading") and item.get("reading"):
            keep["reading"] = item["reading"]
        if not keep.get("romaji") and item.get("romaji"):
            keep["romaji"] = item["romaji"]
    return out


# ---------------------------------------------------------- emoji/images --
# No bundled photos (this is an offline app) — big emoji stand in as a
# lightweight "picture" for each word. Specific words match first; if
# nothing matches, we fall back to one emoji per category.

EMOJI_KEYWORDS = [
    ("dog", "🐶"), ("cow", "🐄"), ("cattle", "🐄"), ("beef", "🥩"), ("horse", "🐴"),
    ("bird", "🐦"), ("fish", "🐟"), ("insect", "🐛"), ("bug", "🐛"), ("cat", "🐱"),
    ("sheep", "🐑"),
    ("mountain", "⛰️"), ("river", "🏞️"), ("tree", "🌳"), ("wood", "🪵"),
    ("water", "💧"), ("fire", "🔥"), ("earth", "🌍"), ("ground", "🌍"),
    ("rain", "🌧️"), ("snow", "❄️"), ("sky", "🌤️"), ("heaven", "🌤️"),
    ("sun", "☀️"), ("moon", "🌙"), ("star", "⭐"), ("wind", "🌬️"),
    ("sea", "🌊"), ("ocean", "🌊"), ("flower", "🌸"), ("stone", "🪨"),
    ("field", "🌾"), ("grass", "🌱"), ("forest", "🌲"), ("grove", "🌲"),
    ("eye", "👁️"), ("ear", "👂"), ("mouth", "👄"), ("hand", "✋"),
    ("foot", "🦶"), ("leg", "🦵"), ("head", "🧠"), ("face", "😊"),
    ("hair", "💇"), ("heart", "❤️"), ("body", "🧍"),
    ("father", "👨"), ("mother", "👩"), ("child", "🧒"), ("brother", "👦"),
    ("sister", "👧"), ("family", "👪"), ("son", "👦"), ("daughter", "👧"),
    ("king", "👑"), ("teacher", "🧑‍🏫"), ("student", "🎓"), ("friend", "🤝"),
    ("woman", "👩"), ("man", "🧑"), ("person", "🧑"),
    ("school", "🏫"), ("house", "🏠"), ("home", "🏠"), ("gate", "🚪"),
    ("temple", "⛩️"), ("shop", "🏪"), ("store", "🏪"), ("station", "🚉"),
    ("city", "🏙️"), ("town", "🏙️"), ("country", "🌏"), ("room", "🛋️"),
    ("library", "📚"), ("market", "🏪"), ("capital", "🏛️"),
    ("rice", "🍚"), ("tea", "🍵"), ("meat", "🥩"), ("vegetable", "🥦"),
    ("fruit", "🍎"), ("meal", "🍱"), ("food", "🍽️"),
    ("white", "⚪"), ("black", "⚫"), ("red", "🔴"), ("blue", "🔵"),
    ("green", "🟢"), ("yellow", "🟡"),
    ("one", "1️⃣"), ("two", "2️⃣"), ("three", "3️⃣"), ("four", "4️⃣"),
    ("five", "5️⃣"), ("six", "6️⃣"), ("seven", "7️⃣"), ("eight", "8️⃣"),
    ("nine", "9️⃣"), ("ten", "🔟"), ("hundred", "💯"), ("thousand", "🔢"),
    ("left", "⬅️"), ("right", "➡️"), ("up", "⬆️"), ("down", "⬇️"),
    ("north", "⬆️"), ("south", "⬇️"), ("east", "➡️"), ("west", "⬅️"),
    ("big", "🔵"), ("small", "🔹"), ("book", "📖"), ("letter", "✉️"),
    ("sword", "⚔️"), ("gold", "🪙"), ("money", "💰"), ("time", "⏰"),
    ("month", "🗓️"), ("year", "📅"), ("day", "🗓️"), ("morning", "🌅"),
    ("night", "🌃"), ("today", "📆"),
]

CATEGORY_EMOJI = {
    "Numbers & Counting": "🔢",
    "Time & Calendar": "🗓️",
    "Family & People": "👪",
    "Nature & Weather": "🌿",
    "Body & Health": "🩺",
    "Places & Buildings": "🏯",
    "Food & Drink": "🍱",
    "Directions & Position": "🧭",
    "Colors": "🎨",
    "Animals": "🐾",
    "Actions & Verbs": "🎬",
    "Size & Quantity": "📏",
    "Greetings & Phrases": "💬",
    "Shopping & Money": "🛍️",
    "Out & About": "🚶",
    "Everyday Objects & Ideas": "📦",
    "Shapes & Sizes": "🔷",
    "Opposites": "↔️",
    "Money & Shopping": "💴",
    "Seasons & Holidays": "🎏",
    "School & Learning": "🏫",
    "Counters": "🔢",
    "Work & Jobs": "💼",
    "Health & Body": "🩺",
    "Environment & Nature": "🌎",
    "Sports & Fitness": "⚽",
    "Travel": "🧳",
    "Countries": "🌐",
    "Languages": "💬",
    "Music": "🎸",
    "Transportation": "🚗",
    "House & Furniture": "🛋️",
}


def get_emoji(meaning, category):
    m = meaning.lower()
    for kw, emo in EMOJI_KEYWORDS:
        if kw in m:
            return emo
    return CATEGORY_EMOJI.get(category, "📖")


# ---------------------------------------------------- sentence templates --
# For everyday words that don't have a hand-curated practice sentence,
# build a natural-ish example sentence from a per-category template so
# clicking any word in the Everyday Life list shows it in context.

def cap(s):
    return s[:1].upper() + s[1:] if s else s


SENTENCE_TEMPLATES = {
    "Animals": (
        "田中さんの{w}です。", "たなかさんの{r}です。",
        "Tanaka-san no {rm} desu.", "This is Mr. Tanaka's {en}.",
        "Used when pointing out or introducing someone's pet or animal."),
    "Family & People": (
        "これは私の{w}です。", "これはわたしの{r}です。",
        "Kore wa watashi no {rm} desu.", "This is my {en}.",
        "Used when introducing a family member or person to someone."),
    "Nature & Weather": (
        "{w}がとてもきれいです。", "{r}がとてもきれいです。",
        "{rm} ga totemo kirei desu.", "The {en} is very beautiful.",
        "Used when commenting on scenery or the weather."),
    "Body & Health": (
        "{w}が痛いです。", "{r}がいたいです。",
        "{rm} ga itai desu.", "My {en} hurts.",
        "A common phrase for describing minor aches, e.g. at a doctor's visit."),
    "Places & Buildings": (
        "明日、{w}に行きます。", "あした、{r}にいきます。",
        "Ashita, {rm} ni ikimasu.", "Tomorrow, I'm going to the {en}.",
        "Used when talking about daily plans and destinations."),
    "Food & Drink": (
        "晩ご飯に{w}を食べました。", "ばんごはんに{r}をたべました。",
        "Bangohan ni {rm} o tabemashita.", "I ate {en} for dinner.",
        "Used at the table or when talking about meals."),
    "Directions & Position": (
        "駅は{w}の方です。", "えきは{r}のほうです。",
        "Eki wa {rm} no hō desu.", "The station is that way, to the {en}.",
        "Used constantly when giving or asking for directions."),
    "Colors": (
        "私は{w}が好きです。", "わたしは{r}がすきです。",
        "Watashi wa {rm} ga suki desu.", "I like {en}.",
        "Used when talking about preferences or describing objects."),
    "Numbers & Counting": (
        "テーブルの上に{w}あります。", "テーブルのうえに{r}あります。",
        "Tēburu no ue ni {rm} arimasu.", "There is/are {en} on the table.",
        "Used for counting objects in everyday situations."),
    "Time & Calendar": (
        "{w}に会いましょう。", "{r}にあいましょう。",
        "{rm} ni aimashou.", "Let's meet {en}.",
        "Used when making plans or arranging to meet someone."),
    "Size & Quantity": (
        "この家は{w}です。", "このいえは{r}です。",
        "Kono ie wa {rm} desu.", "This house is {en}.",
        "Used when describing the size or amount of something."),
    "Shapes & Sizes": (
        "この箱は{w}です。", "このはこは{r}です。",
        "Kono hako wa {rm} desu.", "This box is a {en}.",
        "Used when describing the shape or size of an object."),
    "Opposites": (
        "この二つは{w}です。", "このふたつは{r}です。",
        "Kono futatsu wa {rm} desu.", "These two are {en}.",
        "A key adjective pair to memorize together with its opposite."),
    "Money & Shopping": (
        "これは{w}ですか。", "これは{r}ですか。",
        "Kore wa {rm} desu ka.", "Is this {en}?",
        "Common vocabulary for shopping, prices, and paying."),
    "Seasons & Holidays": (
        "{w}が近づいています。", "{r}がちかづいています。",
        "{rm} ga chikazuite imasu.", "{en} is coming up.",
        "Used when talking about the seasons, festivals, and annual holidays."),
    "School & Learning": (
        "学校で{w}を使います。", "がっこうで{r}をつかいます。",
        "Gakkō de {rm} o tsukaimasu.", "We use {en} at school.",
        "Common vocabulary for the classroom and studying."),
    "Work & Jobs": (
        "彼は{w}です。", "かれは{r}です。",
        "Kare wa {rm} desu.", "He is a {en}.",
        "Common vocabulary for talking about jobs and the workplace."),
    "Health & Body": (
        "{w}が痛いです。", "{r}がいたいです。",
        "{rm} ga itai desu.", "My {en} hurts.",
        "Common vocabulary at a doctor's visit or when describing how you feel."),
    "Environment & Nature": (
        "{w}を守りましょう。", "{r}をまもりましょう。",
        "{rm} o mamorimashō.", "Let's protect the {en}.",
        "Common vocabulary for nature, weather, and environmental topics."),
    "Sports & Fitness": (
        "私は{w}が好きです。", "わたしは{r}がすきです。",
        "Watashi wa {rm} ga suki desu.", "I like {en}.",
        "Common vocabulary for sports and staying active."),
    "Travel": (
        "旅行に{w}を持って行きます。", "りょこうに{r}をもっていきます。",
        "Ryokō ni {rm} o motte ikimasu.", "I'll bring {en} on the trip.",
        "Common vocabulary for traveling and sightseeing."),
    "Countries": (
        "私は{w}に行きたいです。", "わたしは{r}にいきたいです。",
        "Watashi wa {rm} ni ikitai desu.", "I want to go to {en}.",
        "A place name used when talking about countries and travel."),
    "Languages": (
        "私は{w}を勉強しています。", "わたしは{r}をべんきょうしています。",
        "Watashi wa {rm} o benkyō shite imasu.", "I'm studying {en}.",
        "Used when talking about which languages you speak or are learning."),
    "Music": (
        "私は{w}が好きです。", "わたしは{r}がすきです。",
        "Watashi wa {rm} ga suki desu.", "I like {en}.",
        "Common vocabulary for music, instruments, and dance."),
    "Transportation": (
        "{w}で行きます。", "{r}でいきます。",
        "{rm} de ikimasu.", "I'll go by {en}.",
        "Common vocabulary for getting around town."),
    "House & Furniture": (
        "これは私の{w}です。", "これはわたしの{r}です。",
        "Kore wa watashi no {rm} desu.", "This is my {en}.",
        "Common vocabulary for rooms and things around the house."),
}

VERB_TEMPLATE = (
    "「{w}」は「{en}」という意味の動詞です。", "「{r}」は「{en}」という意味の動詞です。",
    "\"{rm}\" means \"{en}.\"", "\"{w}\" is a verb meaning \"{en}.\"",
    "A common everyday verb — try it with a subject and an object, e.g. 何を{w}か.")

GENERIC_TEMPLATE = (
    "「{w}」は「{en}」という意味です。", "「{r}」は「{en}」という意味です。",
    "\"{rm}\" means \"{en}.\"", "\"{w}\" means \"{en}.\"",
    "A general-purpose word — look at the vocabulary list on its kanji page for more context.")


MASS_NOUNS = {"bread", "rice", "cheese", "milk", "coffee", "juice", "tea", "meat",
              "water", "sugar", "salt", "butter", "beef", "ice cream", "curry"}


def with_article(word):
    """Add a/an for the food templates so 'I ate apple' reads naturally.
    Skips plural-looking and mass-noun meanings."""
    w = word.strip()
    low = w.lower()
    if low in MASS_NOUNS or low.endswith("s") or "," in w:
        return w
    return ("an " if low[:1] in "aeiou" else "a ") + w


def build_everyday_sentence(word, reading, romaji, meaning, category):
    # v2.9: classify-then-template builder (see everyday_nl.py); the old
    # per-category templates below are kept only as a reference.
    return _nl.build_sentence(word, reading, romaji, meaning, category)


def _legacy_build_everyday_sentence(word, reading, romaji, meaning, category):
    reading = reading or word
    romaji = romaji or reading
    meaning_clean = re.sub(r'^to\s+', '', meaning, flags=re.I).strip()

    # Any word whose English gloss reads as a verb ("to eat", "to begin"...)
    # gets the verb template regardless of category - a lot of Opposites,
    # Work, House, and Health entries are verbs, not just Actions & Verbs.
    if category == "Actions & Verbs" or re.match(r'^to\s+\w', meaning.strip(), re.I):
        tmpl = VERB_TEMPLATE
    else:
        tmpl = SENTENCE_TEMPLATES.get(category, GENERIC_TEMPLATE)

    kanji_t, hira_t, romaji_t, en_t, usage_t = tmpl
    en_arg = with_article(meaning_clean) if category == "Food & Drink" else meaning_clean
    return {
        "sentence_kanji": kanji_t.format(w=word, en=meaning_clean),
        "sentence_hiragana": hira_t.format(r=reading, en=meaning_clean),
        "sentence_romaji": cap(romaji_t.format(rm=romaji, en=meaning_clean, w=word)),
        "sentence_en": cap(en_t.format(en=en_arg, w=word)),
        "usage_note": usage_t.format(w=word, r=reading, rm=romaji, en=meaning_clean),
    }


# -------------------------------------------------- conversation builder --
# Each everyday word also gets a short two-person exchange so you can see
# the word used the way it would actually come up in conversation.
# Each line is (speaker, kanji, hiragana, romaji, english).

CONVERSATION_TEMPLATES = {
    "Animals": [
        ("A", "かわいい{w}ですね。", "かわいい{r}ですね。", "Kawaii {rm} desu ne.", "What a cute {en}!"),
        ("B", "ありがとうございます。田中さんの{w}です。", "ありがとうございます。たなかさんの{r}です。",
         "Arigatō gozaimasu. Tanaka-san no {rm} desu.", "Thank you. It's Mr. Tanaka's {en}."),
    ],
    "Family & People": [
        ("A", "この人はどなたですか。", "このひとはどなたですか。", "Kono hito wa donata desu ka.", "Who is this person?"),
        ("B", "私の{w}です。", "わたしの{r}です。", "Watashi no {rm} desu.", "That's my {en}."),
    ],
    "Nature & Weather": [
        ("A", "わあ、{w}がきれいですね。", "わあ、{r}がきれいですね。", "Wā, {rm} ga kirei desu ne.", "Wow, the {en} is beautiful!"),
        ("B", "そうですね。写真を撮りましょう。", "そうですね。しゃしんをとりましょう。",
         "Sō desu ne. Shashin o torimashō.", "It really is. Let's take a photo."),
    ],
    "Body & Health": [
        ("A", "どうしましたか。", "どうしましたか。", "Dō shimashita ka.", "What's wrong?"),
        ("B", "{w}が痛いです。", "{r}がいたいです。", "{rm} ga itai desu.", "My {en} hurts."),
    ],
    "Places & Buildings": [
        ("A", "明日どこへ行きますか。", "あしたどこへいきますか。", "Ashita doko e ikimasu ka.", "Where are you going tomorrow?"),
        ("B", "{w}へ行きます。", "{r}へいきます。", "{rm} e ikimasu.", "I'm going to the {en}."),
    ],
    "Food & Drink": [
        ("A", "晩ご飯は何でしたか。", "ばんごはんはなんでしたか。", "Bangohan wa nan deshita ka.", "What did you have for dinner?"),
        ("B", "{w}を食べました。おいしかったです。", "{r}をたべました。おいしかったです。",
         "{rm} o tabemashita. Oishikatta desu.", "I had {en}. It was delicious."),
    ],
    "Directions & Position": [
        ("A", "すみません、駅はどこですか。", "すみません、えきはどこですか。", "Sumimasen, eki wa doko desu ka.", "Excuse me, where is the station?"),
        ("B", "{w}の方です。", "{r}のほうです。", "{rm} no hō desu.", "It's to the {en}."),
    ],
    "Colors": [
        ("A", "何色が好きですか。", "なにいろがすきですか。", "Nani iro ga suki desu ka.", "What color do you like?"),
        ("B", "{w}が好きです。", "{r}がすきです。", "{rm} ga suki desu.", "I like {en}."),
    ],
    "Numbers & Counting": [
        ("A", "いくつありますか。", "いくつありますか。", "Ikutsu arimasu ka.", "How many are there?"),
        ("B", "{w}あります。", "{r}あります。", "{rm} arimasu.", "There are {en}."),
    ],
    "Time & Calendar": [
        ("A", "いつ会いましょうか。", "いつあいましょうか。", "Itsu aimashō ka.", "When shall we meet?"),
        ("B", "{w}はどうですか。", "{r}はどうですか。", "{rm} wa dō desu ka.", "How about {en}?"),
    ],
    "Size & Quantity": [
        ("A", "この家はどうですか。", "このいえはどうですか。", "Kono ie wa dō desu ka.", "What do you think of this house?"),
        ("B", "とても{w}ですね。", "とても{r}ですね。", "Totemo {rm} desu ne.", "It's very {en}."),
    ],
    "Actions & Verbs": [
        ("A", "今何をしていますか。", "いまなにをしていますか。", "Ima nani o shite imasu ka.", "What are you doing now?"),
        ("B", "「{w}」の練習をしています。", "「{r}」のれんしゅうをしています。",
         "\"{rm}\" no renshū o shite imasu.", "I'm practicing the verb \"{en}\"."),
    ],
    "Greetings & Phrases": [
        ("A", "{w}", "{r}", "{rm}", "{en}"),
        ("B", "はい、こちらこそ。", "はい、こちらこそ。", "Hai, kochira koso.", "Yes, likewise."),
    ],
    "Shopping & Money": [
        ("A", "{w}", "{r}", "{rm}", "{en}"),
        ("B", "はい、少々お待ちください。", "はい、しょうしょうおまちください。",
         "Hai, shōshō omachi kudasai.", "Certainly, one moment please."),
    ],
    "Out & About": [
        ("A", "{w}", "{r}", "{rm}", "{en}"),
        ("B", "はい、大丈夫ですよ。", "はい、だいじょうぶですよ。", "Hai, daijōbu desu yo.", "Yes, of course."),
    ],
    "Shapes & Sizes": [
        ("A", "この箱の形は何ですか。", "このはこのかたちはなんですか。", "Kono hako no katachi wa nan desu ka.", "What shape is this box?"),
        ("B", "{w}です。", "{r}です。", "{rm} desu.", "It's a {en}."),
    ],
    "Opposites": [
        ("A", "これは{w}ですか。", "これは{r}ですか。", "Kore wa {rm} desu ka.", "Is this {en}?"),
        ("B", "いいえ、逆です。", "いいえ、ぎゃくです。", "Iie, gyaku desu.", "No, it's the opposite."),
    ],
    "Money & Shopping": [
        ("A", "これはいくらですか。", "これはいくらですか。", "Kore wa ikura desu ka.", "How much is this?"),
        ("B", "{w}です。", "{r}です。", "{rm} desu.", "It's {en}."),
    ],
    "Seasons & Holidays": [
        ("A", "{w}はいつですか。", "{r}はいつですか。", "{rm} wa itsu desu ka.", "When is {en}?"),
        ("B", "もうすぐですよ。", "もうすぐですよ。", "Mō sugu desu yo.", "It's coming up soon."),
    ],
    "School & Learning": [
        ("A", "これは何ですか。", "これはなんですか。", "Kore wa nan desu ka.", "What is this?"),
        ("B", "{w}です。学校で使います。", "{r}です。がっこうでつかいます。", "{rm} desu. Gakkō de tsukaimasu.", "It's a {en}. We use it at school."),
    ],
    "Counters": [
        ("A", "いくつありますか。", "いくつありますか。", "Ikutsu arimasu ka.", "How many are there?"),
        ("B", "{w}あります。", "{r}あります。", "{rm} arimasu.", "There is/are {en}."),
    ],
    "Work & Jobs": [
        ("A", "お仕事は何ですか。", "おしごとはなんですか。", "Oshigoto wa nan desu ka.", "What's your job?"),
        ("B", "{w}です。", "{r}です。", "{rm} desu.", "I'm a {en}."),
    ],
    "Health & Body": [
        ("A", "どうしましたか。", "どうしましたか。", "Dō shimashita ka.", "What's wrong?"),
        ("B", "{w}が痛いです。", "{r}がいたいです。", "{rm} ga itai desu.", "My {en} hurts."),
    ],
    "Environment & Nature": [
        ("A", "{w}を見てください。", "{r}をみてください。", "{rm} o mite kudasai.", "Please look at the {en}."),
        ("B", "きれいですね。", "きれいですね。", "Kirei desu ne.", "It's beautiful, isn't it."),
    ],
    "Sports & Fitness": [
        ("A", "どんなスポーツをしますか。", "どんなすぽーつをしますか。", "Donna supōtsu o shimasu ka.", "What sports do you play?"),
        ("B", "{w}をします。", "{r}をします。", "{rm} o shimasu.", "I play/do {en}."),
    ],
    "Travel": [
        ("A", "旅行の準備はできましたか。", "りょこうのじゅんびはできましたか。", "Ryokō no junbi wa dekimashita ka.", "Are you ready for the trip?"),
        ("B", "はい、{w}を持ちました。", "はい、{r}をもちました。", "Hai, {rm} o mochimashita.", "Yes, I've got my {en}."),
    ],
    "Countries": [
        ("A", "どこの国から来ましたか。", "どこのくにからきましたか。", "Doko no kuni kara kimashita ka.", "What country are you from?"),
        ("B", "{w}から来ました。", "{r}からきました。", "{rm} kara kimashita.", "I'm from {en}."),
    ],
    "Languages": [
        ("A", "何語を話しますか。", "なにごをはなしますか。", "Nanigo o hanashimasu ka.", "What language do you speak?"),
        ("B", "{w}を話します。", "{r}をはなします。", "{rm} o hanashimasu.", "I speak {en}."),
    ],
    "Music": [
        ("A", "何か楽器をしますか。", "なにかがっきをしますか。", "Nanika gakki o shimasu ka.", "Do you play an instrument?"),
        ("B", "{w}をします。", "{r}をします。", "{rm} o shimasu.", "I play {en}."),
    ],
    "Transportation": [
        ("A", "どうやって行きますか。", "どうやっていきますか。", "Dōyatte ikimasu ka.", "How are you getting there?"),
        ("B", "{w}で行きます。", "{r}でいきます。", "{rm} de ikimasu.", "I'm going by {en}."),
    ],
    "House & Furniture": [
        ("A", "これは何ですか。", "これはなんですか。", "Kore wa nan desu ka.", "What is this?"),
        ("B", "{w}です。", "{r}です。", "{rm} desu.", "It's a {en}."),
    ],
}

GENERIC_CONVERSATION = [
    ("A", "「{w}」はどういう意味ですか。", "「{r}」はどういういみですか。",
     "\"{rm}\" wa dō iu imi desu ka.", "What does \"{w}\" mean?"),
    ("B", "「{en}」という意味です。", "「{en}」といういみです。",
     "\"{en}\" to iu imi desu.", "It means \"{en}\"."),
]


def build_conversation(word, reading, romaji, meaning, category):
    return _nl.build_conv(word, reading, romaji, meaning, category)


def _legacy_build_conversation(word, reading, romaji, meaning, category):
    reading = reading or word
    romaji = romaji or reading
    meaning_clean = re.sub(r'^to\s+', '', meaning, flags=re.I).strip()
    tmpl = CONVERSATION_TEMPLATES.get(category, GENERIC_CONVERSATION)
    lines = []
    for speaker, k, h, rm, en in tmpl:
        lines.append({
            "speaker": speaker,
            "kanji": k.format(w=word, r=reading, rm=romaji, en=meaning_clean),
            "hiragana": h.format(w=word, r=reading, rm=romaji, en=meaning_clean),
            "romaji": cap(rm.format(w=word, r=reading, rm=romaji, en=meaning_clean)),
            "english": cap(en.format(w=word, r=reading, rm=romaji, en=meaning_clean)),
        })
    return lines


# --------------------------------------------------------------- words --

# Flatten every vocabulary word (across all kanji entries) into one big
# searchable list, each tagged with its parent kanji's on/kun-yomi info,
# a category, and a difficulty tier.
ALL_WORDS = []
for entry in KANJI_DATA:
    for v in entry["vocab"]:
        ALL_WORDS.append({
            "word": v["word"],
            "reading": v["reading"],
            "romaji": v["romaji"],
            "meaning": v["meaning"],
            "kanji": entry["kanji"],
            "kanji_id": entry["id"],
            "kanji_meaning": entry["meaning"],
            "on_yomi": entry["on_yomi"],
            "kun_yomi": entry["kun_yomi"],
            "strokes": entry["strokes"],
            "category": categorize(v["meaning"]),
            "difficulty": difficulty_for(entry["strokes"], len(v["word"])),
        })
# also add the bare kanji character itself as a searchable "word" for
# any kanji whose vocab list didn't already include the solo character
seen_words = {w["word"] for w in ALL_WORDS}
for entry in KANJI_DATA:
    if entry["kanji"] not in seen_words:
        ALL_WORDS.append({
            "word": entry["kanji"],
            "reading": "",
            "romaji": "",
            "meaning": entry["meaning"],
            "kanji": entry["kanji"],
            "kanji_id": entry["id"],
            "kanji_meaning": entry["meaning"],
            "on_yomi": entry["on_yomi"],
            "kun_yomi": entry["kun_yomi"],
            "strokes": entry["strokes"],
            "category": categorize(entry["meaning"]),
            "difficulty": difficulty_for(entry["strokes"], len(entry["kanji"])),
        })

# Vocabulary transcribed from the Japanese Picture Dictionary (Stout) -
# shapes, opposites, money, seasons/holidays, counters, jobs, health,
# house/furniture, extended family/animals/numbers, sports, travel,
# countries, languages, music, transportation, directions, and more
# food/drink. See gen_picture_dict.py for how each entry was sourced.
for pw in PICTURE_DICT_WORDS:
    ALL_WORDS.append({
        "word": pw["word"],
        "reading": pw["reading"],
        "romaji": pw["romaji"],
        "meaning": pw["meaning"],
        "kanji": "",
        "kanji_id": None,
        "kanji_meaning": "",
        "on_yomi": "",
        "kun_yomi": "",
        "strokes": 0,
        "category": pw["category"],
        "difficulty": "easy",
    })

# Common everyday words (fruits, animals, food, electronics...) that the
# kanji textbook doesn't cover because they aren't built around a lesson
# kanji. These make English-meaning search work for things like "apple".
for cw in COMMON_WORDS:
    ALL_WORDS.append({
        "word": cw["word"],
        "reading": cw["reading"],
        "romaji": cw["romaji"],
        "meaning": cw["meaning"],
        "kanji": "",
        "kanji_id": None,
        "kanji_meaning": "",
        "on_yomi": "",
        "kun_yomi": "",
        "strokes": 0,
        "category": cw["category"],
        "difficulty": "easy",
    })

# The pool of words usable in Practice mode: exactly one entry per kanji
# (its base character), since that's what has on/kun-yomi + a curated or
# generated sentence tied to it.
PRACTICE_POOL = [w for w in ALL_WORDS if w["word"] == w["kanji"]]
PRACTICE_BY_ID = {w["kanji_id"]: w for w in PRACTICE_POOL}

# Everyday-life word list = every kanji-vocab word (already has kanji +
# hiragana + English) plus the hand-curated greetings/phrases. This is
# well over 250 entries (1,300+ from the book alone). Each entry gets an
# example sentence (curated where we have one, template-generated
# otherwise) and an emoji "image" for a bit of visual flavor.
EVERYDAY_WORDS = []
for w in ALL_WORDS:
    curated = SENTENCE_BY_KANJI_ID.get(w["kanji_id"]) if w["word"] == w["kanji"] else None
    if curated and curated["word"] == w["word"]:
        sentence = {
            "sentence_kanji": curated["sentence_kanji"],
            "sentence_hiragana": curated["sentence_hiragana"],
            "sentence_romaji": curated["sentence_romaji"],
            "sentence_en": curated["sentence_en"],
            "usage_note": curated["usage_note"],
        }
    else:
        sentence = build_everyday_sentence(w["word"], w["reading"], w["romaji"], w["meaning"], w["category"])
    EVERYDAY_WORDS.append({
        "word": w["word"],
        "reading": w["reading"] or w["word"],
        "romaji": w["romaji"],
        "meaning": w["meaning"],
        "category": w["category"],
        "difficulty": w.get("difficulty", "easy"),
        "frequency_rank": w.get("frequency_rank"),
        "emoji": get_emoji(w["meaning"], w["category"]),
        "conversation": build_conversation(w["word"], w["reading"], w["romaji"], w["meaning"], w["category"]),
        **sentence,
    })
# ------------------------------------------------- roadmap words -> app --
# Every word the Roadmap teaches must also exist in the rest of the app
# (Everyday list, search, Vocabulary flashcards, Verbs). Words that are
# already in the main vocabulary or the Verbs page are skipped; the rest
# become ROADMAP_WORDS and are added below. Built from ROADMAP itself so
# the two never drift apart.
_RM_CATEGORY = {
    "greetings-intro": "Greetings & Phrases", "numbers-1-100": "Numbers & Counting",
    "my-family": "Family & People", "my-house": "House & Furniture", "human-body": "Body & Health",
    "daily-routines": "Daily Routines", "telling-time": "Time & Calendar", "days-dates": "Time & Calendar",
    "around-town": "Places & Buildings", "asking-directions-rm": "Directions & Position",
    "transportation": "Transportation", "going-shopping-rm": "Money & Shopping",
    "talking-about-money-rm": "Money & Shopping", "seasons-weather": "Nature & Weather",
    "holidays-festivals": "Seasons & Holidays", "hobbies-music": "Hobbies & Music",
    "at-work-rm": "Work & Jobs", "at-school-rm": "School & Learning", "japanese-food": "Food & Drink",
    "fruits-veg-drinks": "Food & Drink", "at-the-market-rm": "Food & Drink",
    "computers-internet": "Technology", "smartphones-apps": "Technology", "health-doctor": "Body & Health",
    "the-environment": "Environment & Nature", "adjectives-opposites-rm": "Opposites",
    "counters-rm": "Counters", "countries-nationalities": "Countries", "foreign-languages-travel": "Languages",
    "kanji-basics": "Kanji & Writing", "radicals-intro": "Kanji & Writing", "radicals-reading": "Kanji & Writing",
}
_RM_GRAMMAR = {"particles-wa-ga-o", "particles-ni-de-e", "sentence-patterns", "noun-modification",
               "nagara", "giving-reasons", "plans-intentions", "te-extras"}
_RM_SKIP = {"te-form-basics", "potential-form"}      # conjugated forms: covered on the Verbs page
_RM_HARD = {"modern-life", "grammar-foundations", "toward-fluency"}
_RM_MEDIUM = {"people-culture", "food-drink"}
_SHAPE_HINT = ("形", "球", "体", "線", "点", "星", "ハート")


def _build_roadmap_words(existing_words):
    out, seen = [], set(existing_words)
    for sec in ROADMAP:
        diff = "hard" if sec["id"] in _RM_HARD else "medium" if sec["id"] in _RM_MEDIUM else "easy"
        for ch in sec["chapters"]:
            if ch.get("kind") != "lesson" or ch.get("kana") or ch.get("radicals") or ch["id"] in _RM_SKIP:
                continue
            if ch["id"] in _RM_GRAMMAR:
                cat = "Grammar Patterns"
            elif ch["id"] == "colors-shapes":
                cat = None
            else:
                cat = _RM_CATEGORY.get(ch["id"])
            if ch["id"] not in _RM_GRAMMAR and not cat and ch["id"] != "colors-shapes":
                continue
            filled = {}
            for st in ch.get("sentences", []):
                filled.setdefault(st["blank"], st)
            for w in ch.get("vocab", []):
                if w["jp"] in seen:
                    continue
                seen.add(w["jp"])
                c = cat or ("Shapes & Sizes" if w["jp"].endswith(_SHAPE_HINT) or w["jp"] in ("ひし形", "楕円") else "Colors")
                item = {"word": w["jp"], "reading": w["reading"] or w["jp"], "romaji": w["romaji"],
                        "meaning": w["meaning"], "kanji": "", "kanji_id": None, "kanji_meaning": "",
                        "on_yomi": "", "kun_yomi": "", "strokes": 0, "category": c, "difficulty": diff,
                        "roadmap_chapter": ch["id"]}
                st = filled.get(w["jp"])
                if st:   # a real roadmap example sentence, blank filled in
                    item["sentence"] = {
                        "sentence_kanji": st["jp"].replace("___", w["jp"]),
                        "sentence_hiragana": st["reading"].replace("___", w["reading"] or w["jp"]),
                        "sentence_romaji": cap(st["romaji"].replace("___", w["romaji"])),
                        "sentence_en": st["english"],
                        "usage_note": f"From the Roadmap chapter \u201c{ch['title']}\u201d.",
                    }
                out.append(item)
    return out


ROADMAP_WORDS = _build_roadmap_words({w["word"] for w in ALL_WORDS} | {w["word"] for w in VERBS_DATA}
                                     | {e["word"] for e in EVERYDAY_EXTRA})

# Frequency-ranked words imported from the supplied PDF.  Keep these
# separate from ALL_WORDS so they never suppress richer Roadmap records.
FREQUENCY_APP_WORDS = [{
    "word": w["word"],
    "reading": w.get("reading", ""),
    "romaji": w.get("romaji", ""),
    "meaning": w.get("meaning", ""),
    "kanji": "",
    "kanji_id": None,
    "kanji_meaning": "",
    "on_yomi": "",
    "kun_yomi": "",
    "strokes": 0,
    "category": w.get("category", "Everyday Objects & Ideas"),
    "difficulty": w.get("difficulty", "medium"),
    "frequency_rank": w.get("rank"),
    "part_of_speech": w.get("part_of_speech", ""),
    "source_example_ja": w.get("example_ja", ""),
    "source_example_en": w.get("example_en", ""),
} for w in FREQUENCY_WORDS]

# Vocabulary flashcards/search/progress all use the same canonical pool.
# Existing Kotoba records win when sources overlap; new PDF words fill gaps.
VOCAB_POOL = dedupe_vocab(ALL_WORDS + ROADMAP_WORDS + FREQUENCY_APP_WORDS)

for rw in ROADMAP_WORDS:
    sent = rw.get("sentence") or build_everyday_sentence(rw["word"], rw["reading"], rw["romaji"], rw["meaning"], rw["category"])
    EVERYDAY_WORDS.append({
        "word": rw["word"], "reading": rw["reading"], "romaji": rw["romaji"], "meaning": rw["meaning"],
        "category": rw["category"], "difficulty": rw.get("difficulty", "easy"),
        "emoji": get_emoji(rw["meaning"], rw["category"]),
        "conversation": build_conversation(rw["word"], rw["reading"], rw["romaji"], rw["meaning"], rw["category"]),
        **sent,
    })
for extra in EVERYDAY_EXTRA:
    EVERYDAY_WORDS.append({
        "word": extra["word"],
        "reading": extra["reading"],
        "romaji": extra["romaji"],
        "meaning": extra["meaning"],
        "category": extra["category"],
        "difficulty": "easy",
        "emoji": get_emoji(extra["meaning"], extra["category"]),
        "sentence_kanji": extra["word"],
        "sentence_hiragana": extra["reading"],
        "sentence_romaji": cap(extra["romaji"]),
        "sentence_en": cap(extra["meaning"]),
        "usage_note": f"A common everyday phrase, filed under \u201c{extra['category']}\u201d.",
        "conversation": build_conversation(extra["word"], extra["reading"], extra["romaji"], extra["meaning"], extra["category"]),
    })
# Fill genuine vocabulary gaps with the frequency-ranked PDF words.
for fw in FREQUENCY_APP_WORDS:
    sent = build_everyday_sentence(fw["word"], fw["reading"], fw["romaji"], fw["meaning"], fw["category"])
    EVERYDAY_WORDS.append({
        "word": fw["word"],
        "reading": fw["reading"] or fw["word"],
        "romaji": fw["romaji"],
        "meaning": fw["meaning"],
        "category": fw["category"],
        "difficulty": fw["difficulty"],
        "frequency_rank": fw.get("frequency_rank"),
        "emoji": get_emoji(fw["meaning"], fw["category"]),
        "conversation": build_conversation(fw["word"], fw["reading"], fw["romaji"], fw["meaning"], fw["category"]),
        **sent,
    })

# The same word can occur in the kanji data, picture dictionary, roadmap,
# common list and frequency PDF.  Show it once, using the richer first
# record, instead of making the learner meet duplicate rows/cards.
EVERYDAY_WORDS = dedupe_vocab(EVERYDAY_WORDS)
for w in EVERYDAY_WORDS:
    w.setdefault("difficulty", "easy")
EVERYDAY_CATEGORIES = sorted(set(w["category"] for w in EVERYDAY_WORDS))

# Keep the original index alongside each word, then group by category so
# the page can render one clearly-labelled block per category.
for i, w in enumerate(EVERYDAY_WORDS):
    w["idx"] = i
EVERYDAY_BY_CATEGORY = [
    (cat, [w for w in EVERYDAY_WORDS if w["category"] == cat])
    for cat in EVERYDAY_CATEGORIES
]


def normalize(text):
    """Lowercase + strip diacritics/macrons for loose matching (e.g. 'kyo' matches 'kyō')."""
    text = text.strip().lower()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    return text


def contains_japanese(text):
    return bool(re.search(r'[\u3040-\u30FF\u4E00-\u9FFF]', text))


def search_words(query, limit=60):
    """Search across word/reading/romaji/meaning, works for English or Japanese input.
    Covers the canonical vocabulary pool (including the supplied frequency
    list) plus the separate JLPT N5-N1 kanji set, so a JLPT-only kanji is
    still findable from the search bar."""
    q = query.strip()
    if not q:
        return []
    q_norm = normalize(q)
    q_raw = q  # keep raw for direct Japanese char matching

    results = []
    seen_words = set()
    for w in VOCAB_POOL:
        score = 0
        if contains_japanese(q_raw):
            if q_raw in w["word"] or q_raw in w["reading"] or q_raw in w["kanji"]:
                score = 3 if (w["word"] == q_raw or w["kanji"] == q_raw) else 2
        else:
            if q_norm and (q_norm in normalize(w["romaji"]) or q_norm in normalize(w["meaning"])):
                score = 3 if normalize(w["romaji"]) == q_norm else 1
        if score:
            results.append((score, w))
            seen_words.add(w["word"])

    for e in JLPT_KANJI:
        if e["kanji"] in seen_words:
            continue  # already covered by a richer ALL_WORDS/kanji_detail result
        score = 0
        if contains_japanese(q_raw):
            if q_raw == e["kanji"] or q_raw in e["on_yomi"] or q_raw in e["kun_yomi"]:
                score = 3 if q_raw == e["kanji"] else 2
        else:
            if q_norm and q_norm in normalize(e["meaning"]):
                score = 1
        if score:
            results.append((score, {
                "word": e["kanji"], "kanji": e["kanji"], "reading": e["on_yomi"],
                "romaji": "", "meaning": f"{e['meaning']} (JLPT {e['level']})",
                "jlpt_level": e["level"],
            }))
            seen_words.add(e["kanji"])

    for r in RADICALS:
        score = 0
        if contains_japanese(q_raw):
            if q_raw == r["glyph"] or q_raw in r["name"]:
                score = 3 if q_raw == r["glyph"] else 2
        elif q_norm and (q_norm in normalize(r["romaji"]) or q_norm == normalize(r["meaning"])
                         or (len(q_norm) > 2 and q_norm in normalize(r["meaning"]))):
            score = 1
        if score:
            results.append((score, {"word": r["glyph"], "reading": r["name"], "romaji": r["romaji"],
                                    "meaning": f"radical: {r['meaning']}", "radical_id": r["id"]}))

    # Places are searchable too, so the global dictionary can act as an
    # entry point into Japan Explorer (Tokyo, 京都, Sapporo, local foods, etc.).
    for place in JAPAN_PLACES:
        fields = [place.get("city_en",""), place.get("city_jp",""), place.get("reading",""),
                  place.get("prefecture_en",""), place.get("prefecture_jp",""), place.get("region","")]
        fields.extend(place.get("famous", [])); fields.extend(place.get("foods", []))
        score = 0
        if contains_japanese(q_raw):
            if any(q_raw in str(v) for v in fields):
                score = 3 if q_raw in {place.get("city_jp"), place.get("prefecture_jp")} else 1
        elif q_norm and any(q_norm in normalize(v) for v in fields):
            score = 3 if q_norm in {normalize(place.get("city_en")), normalize(place.get("prefecture_en"))} else 1
        if score:
            results.append((score, {
                "word": place.get("city_jp"), "reading": place.get("reading"), "romaji": place.get("city_en"),
                "meaning": f"Japan Explorer · {place.get('prefecture_en')} · {place.get('tagline')}",
                "japan_place": place.get("id"),
            }))

    results.sort(key=lambda x: -x[0])
    return [w for _, w in results[:limit]]


def build_explanation(word_entry):
    """Given a flattened word dict, build the rich explanation payload
    shown after a practice answer (right or wrong), or on a word detail view."""
    kanji_id = word_entry["kanji_id"]
    sentence = SENTENCE_BY_KANJI_ID.get(kanji_id)
    if not sentence:
        # fallback: auto-build a simple sentence when we have no curated one
        sentence = {
            "word": word_entry["word"],
            "sentence_kanji": f"これは「{word_entry['word']}」です。",
            "sentence_hiragana": f"これは「{word_entry['reading'] or word_entry['word']}」です。",
            "sentence_romaji": f"Kore wa \"{word_entry['romaji'] or word_entry['reading']}\" desu.",
            "sentence_en": f"This is \"{word_entry['meaning']}\".",
            "usage_note": "A generated practice sentence (no curated example available for this word yet).",
        }
    return {
        "word": word_entry["word"],
        "reading": word_entry["reading"],
        "romaji": word_entry["romaji"],
        "meaning": word_entry["meaning"],
        "kanji": word_entry["kanji"],
        "kanji_meaning": word_entry["kanji_meaning"],
        "on_yomi": word_entry["on_yomi"] or "—",
        "kun_yomi": word_entry["kun_yomi"] or "—",
        "strokes": word_entry["strokes"],
        "sentence_kanji": sentence["sentence_kanji"],
        "sentence_hiragana": sentence["sentence_hiragana"],
        "sentence_romaji": sentence["sentence_romaji"],
        "sentence_en": sentence["sentence_en"],
        "usage_note": sentence["usage_note"],
    }



def first_reading(entry):
    """Pull the first kana reading out of an on-yomi/kun-yomi string like
    'ロク ROKU' or 'む mu, むつ mutsu' -> 'ロク' / 'む'."""
    for field in ("kun_yomi", "on_yomi"):
        raw = entry.get(field) or ""
        for part in raw.split(","):
            m = re.match(r'\s*([\u3040-\u30FF]+)', part)
            if m:
                return m.group(1)
    return ""


def unique_take(candidates, correct, n):
    """Take n distinct candidates, skipping blanks and the correct answer."""
    out = []
    for c in candidates:
        if c and c != correct and c not in out:
            out.append(c)
        if len(out) == n:
            break
    return out



# -------------------------------------------------------------- accounts --
# Optional local accounts, so progress (right now: the streak) can belong
# to a person rather than to the device. Kept as flat JSON files, same as
# everything else in this app - no external database, nothing leaves the
# device/server this is running on. Signing in is entirely optional: a
# visitor who never signs up keeps working exactly like before, with the
# device-wide streak.json file.

USERS_FILE = DATA_DIR / "users.json"
USERNAME_RE = re.compile(r"^[A-Za-z0-9_]{3,20}$")


def _load_users():
    if not USERS_FILE.exists():
        return []
    try:
        with open(USERS_FILE, encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def _save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


def _find_user_by_name(username):
    needle = username.strip().lower()
    for u in _load_users():
        if u["username"].lower() == needle:
            return u
    return None


def _find_user_by_id(user_id):
    for u in _load_users():
        if u["id"] == user_id:
            return u
    return None


def current_user():
    uid = session.get("user_id")
    if uid is None:
        return None
    return _find_user_by_id(uid)


@app.context_processor
def inject_current_user():
    # Makes `current_user` available in every template (the header uses it
    # to show either "Log in / Sign up" or the signed-in username).
    return {"current_user": current_user()}


def csrf_token():
    """A per-session token for the auth forms (login/signup/logout), so a
    third-party page can't submit those forms on a visitor's behalf.
    Generated once per session and reused - not rotated per-request,
    since these are simple state-changing forms, not a banking app."""
    token = session.get("csrf_token")
    if not token:
        token = secrets.token_hex(16)
        session["csrf_token"] = token
    return token


def check_csrf():
    submitted = request.form.get("csrf_token", "")
    return submitted and submitted == session.get("csrf_token", "__none__")


@app.context_processor
def inject_csrf_token():
    return {"csrf_token": csrf_token}


@app.context_processor
def inject_app_version():
    return {"app_version": APP_VERSION}


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user():
        return redirect(url_for("index"))
    error = None
    username = ""
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""
        confirm = request.form.get("confirm") or ""
        if not check_csrf():
            error = "Your session expired - please try again."
        elif not USERNAME_RE.match(username):
            error = "Username must be 3-20 characters: letters, numbers, underscore only."
        elif len(password) < 6:
            error = "Password must be at least 6 characters."
        elif password != confirm:
            error = "Those passwords don't match."
        elif _find_user_by_name(username):
            error = "That username is already taken."
        else:
            users = _load_users()
            new_id = max((u["id"] for u in users), default=0) + 1
            users.append({
                "id": new_id,
                "username": username,
                "password_hash": generate_password_hash(password),
                "created_at": datetime.utcnow().isoformat(),
            })
            _save_users(users)
            session.clear()
            session["user_id"] = new_id
            session.permanent = True
            return redirect(url_for("index"))
    return render_template("signup.html", error=error, username=username)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user():
        return redirect(url_for("index"))
    error = None
    username = ""
    next_url = request.values.get("next") or url_for("index")
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""
        user = _find_user_by_name(username)
        if not check_csrf():
            error = "Your session expired - please try again."
        elif not user or not check_password_hash(user["password_hash"], password):
            error = "Incorrect username or password."
        else:
            session.clear()
            session["user_id"] = user["id"]
            session.permanent = True
            return redirect(next_url)
    return render_template("login.html", error=error, username=username, next=next_url)


@app.route("/logout", methods=["POST"])
def logout():
    if check_csrf():
        session.clear()
    return redirect(request.referrer or url_for("index"))


# --------------------------------------------------------------- streak --
# A simple persistent streak tracker, stored as a flat JSON file so it
# survives app restarts (unlike Flask's cookie-based session). Signed-in
# users get their own entry in user_streaks.json, keyed by user id;
# anyone not signed in keeps the original device-wide streak.json file,
# so nothing changes for people who don't create an account.

STREAK_FILE = DATA_DIR / "streak.json"
USER_STREAK_FILE = DATA_DIR / "user_streaks.json"


def _load_all_user_streaks():
    if not USER_STREAK_FILE.exists():
        return {}
    try:
        with open(USER_STREAK_FILE, encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def _load_streak_dates(user=None):
    if user is None:
        if not STREAK_FILE.exists():
            return set()
        try:
            with open(STREAK_FILE, encoding="utf-8") as f:
                data = json.load(f)
            return set(data.get("active_dates", []))
        except (json.JSONDecodeError, OSError):
            return set()
    return set(_load_all_user_streaks().get(str(user["id"]), []))


def _save_streak_dates(dates, user=None):
    if user is None:
        with open(STREAK_FILE, "w", encoding="utf-8") as f:
            json.dump({"active_dates": sorted(dates)}, f)
        return
    all_streaks = _load_all_user_streaks()
    all_streaks[str(user["id"])] = sorted(dates)
    with open(USER_STREAK_FILE, "w", encoding="utf-8") as f:
        json.dump(all_streaks, f, ensure_ascii=False, indent=2)


def _compute_streak(dates):
    """current streak (consecutive days ending today or yesterday),
    longest streak ever, and total active days."""
    if not dates:
        return {"current": 0, "longest": 0, "total_days": 0}

    day_set = {datetime.strptime(d, "%Y-%m-%d").date() for d in dates}
    today = date.today()

    # current streak: walk backward from today (or yesterday, so a
    # missed "today" doesn't zero out a streak that's still alive until
    # midnight) while consecutive days are present
    current = 0
    cursor = today if today in day_set else today - timedelta(days=1)
    while cursor in day_set:
        current += 1
        cursor -= timedelta(days=1)

    # longest streak ever, scanning the sorted run of days
    longest = 0
    run = 0
    prev = None
    for d in sorted(day_set):
        if prev is not None and (d - prev).days == 1:
            run += 1
        else:
            run = 1
        longest = max(longest, run)
        prev = d

    return {"current": current, "longest": longest, "total_days": len(day_set)}


@app.route("/api/streak")
def api_streak_get():
    user = current_user()
    dates = _load_streak_dates(user)
    info = _compute_streak(dates)
    info["active_dates"] = sorted(dates)
    info["logged_in"] = user is not None
    return jsonify(info)


@app.route("/api/streak/mark", methods=["POST"])
def api_streak_mark():
    """Call this whenever the person completes something that should
    count toward today's streak (a practice round, a flashcard deck)."""
    user = current_user()
    dates = _load_streak_dates(user)
    today_str = date.today().isoformat()
    is_new_day = today_str not in dates
    dates.add(today_str)
    _save_streak_dates(dates, user)
    info = _compute_streak(dates)
    info["active_dates"] = sorted(dates)
    info["is_new_day"] = is_new_day
    info["logged_in"] = user is not None
    return jsonify(info)


# ---------------------------------------------------------------- routes --

@app.route("/")
def index():
    user = current_user()
    state = _home_learning_state(user)
    return render_template(
        "index.html",
        kanji_count=len(KANJI_DATA),
        everyday_count=len(EVERYDAY_WORDS),
        jlpt_count=len(JLPT_KANJI),
        verbs_count=len(VERBS_DATA),
        conversation_count=len(CONVERSATIONS_DATA),
        story_count=len(STORIES_DATA),
        roadmap=state["roadmap"],
        next_lesson=state["next_lesson"],
        streak=state["streak"],
        progress=state["progress"],
        learner=state["learner"],
        show_onboarding=(state["roadmap"]["done"] == 0),
    )


@app.route("/explore")
def explore_page():
    return render_template(
        "explore.html",
        kanji_count=len(KANJI_DATA),
        everyday_count=len(EVERYDAY_WORDS),
        jlpt_count=len(JLPT_KANJI),
        verbs_count=len(VERBS_DATA),
        conversation_count=len(CONVERSATIONS_DATA),
        story_count=len(STORIES_DATA),
        grammar_count=len(GRAMMAR_DATA),
    )


@app.route("/japan")
def japan_explorer_page():
    user = current_user()
    state = _learner.load_state(DATA_DIR, user)
    visited_ids = sorted(state.get("japan_visited", {}).keys())
    placement = state.get("placement") if isinstance(state.get("placement"), dict) else {}
    approx = str(placement.get("approx_level") or "N5").upper()
    default_level = "advanced" if approx in {"N1", "N2"} else ("intermediate" if approx == "N3" else "beginner")
    return render_template(
        "japan_explorer.html", japan_data=JAPAN_EXPLORER_DATA,
        visited_ids=visited_ids, visited_count=len(visited_ids), default_level=default_level,
    )


@app.route("/api/japan/visit", methods=["POST"])
def api_japan_visit():
    payload = request.get_json(silent=True) or {}
    place_id = str(payload.get("id") or "").strip()
    place = JAPAN_PLACE_BY_ID.get(place_id)
    if not place:
        return jsonify({"error": "unknown Japan Explorer place"}), 404
    result = _learner.record_japan_visit(
        DATA_DIR, current_user(), place_id, f"{place.get('city_en')} · {place.get('prefecture_en')}"
    )
    if result.get("first_time"):
        dates = _load_streak_dates(current_user())
        dates.add(date.today().isoformat())
        try:
            _save_streak_dates(dates, current_user())
        except OSError:
            pass
    return jsonify(result)


@app.route("/hiragana")
def hiragana():
    return render_template("kana.html", kana_type="Hiragana", data=HIRAGANA_DATA)


@app.route("/katakana")
def katakana():
    return render_template("kana.html", kana_type="Katakana", data=KATAKANA_DATA)


@app.route("/kanji")
def kanji_list():
    return render_template("kanji_list.html", entries=KANJI_DATA)


@app.route("/kanji/practice")
def kanji_practice():
    return render_template("kanji_practice.html")


@app.route("/kanji/<int:kanji_id>")
def kanji_detail(kanji_id):
    entry = next((e for e in KANJI_DATA if e["id"] == kanji_id), None)
    if not entry:
        return "Kanji not found", 404
    word_entry = PRACTICE_BY_ID.get(kanji_id)
    explanation = build_explanation(word_entry) if word_entry else None
    return render_template("kanji_detail.html", entry=entry, explanation=explanation,
                           radical=radical_info(entry["kanji"]), guide=reading_guide(entry))


# ---------------------------------------------------------------- radicals --

@app.route("/radicals")
def radicals_page():
    core = [r for r in RADICALS if r["core"]]
    extra = [r for r in RADICALS if not r["core"]]
    return render_template("radicals.html", core=core, extra=extra, positions=RADICAL_POSITIONS,
                           kanji_by_char={e["kanji"]: e for e in KANJI_DATA})


@app.route("/radicals/<rid>")
def radical_detail(rid):
    r = RADICAL_BY_ID.get(rid)
    if not r:
        return redirect(url_for("radicals_page"))
    by_char = {e["kanji"]: e for e in KANJI_DATA}
    examples = []
    for ch in r["kanji"]:
        e = by_char.get(ch) or JLPT_BY_CHAR.get(ch)
        if not e:
            continue
        st = KANJI_STORIES.get(ch) or {}
        examples.append({"kanji": ch, "meaning": e.get("meaning", ""), "on": e.get("on_yomi", ""),
                         "kun": e.get("kun_yomi", ""), "id": by_char[ch]["id"] if ch in by_char else None,
                         "parts": st.get("parts", ""), "story": st.get("story", "")})
    forms = [RADICAL_BY_GLYPH[f] for f in r["forms"].split() if f in RADICAL_BY_GLYPH]
    return render_template("radical_detail.html", r=r, examples=examples, forms=forms)


KANJI_QUIZ_LEVELS = {"all", "easy", "medium", "hard"}


@app.route("/api/kanji_quiz")
def api_kanji_quiz():
    """Multiple-choice kanji-meaning quiz. ?level=all|easy|medium|hard,
    ?count=up to 40. No correctness is revealed here - the client collects
    every answer and only shows the full breakdown once the round ends."""
    level = (request.args.get("level") or "all").lower()
    if level not in KANJI_QUIZ_LEVELS:
        level = "all"
    try:
        count = int(request.args.get("count", 20))
    except (TypeError, ValueError):
        count = 20
    count = max(4, min(count, 40))

    pool = PRACTICE_POOL if level == "all" else [e for e in PRACTICE_POOL if e["difficulty"] == level]
    if len(pool) < 4:
        pool = PRACTICE_POOL  # too small a pool to build 4 distinct options from

    chosen = random.sample(pool, min(count, len(pool)))

    questions = []
    for entry in chosen:
        correct = entry["kanji_meaning"]
        candidates = [e["kanji_meaning"] for e in pool
                      if e["kanji"] != entry["kanji"] and e["kanji_meaning"] != correct]
        random.shuffle(candidates)
        wrong, seen = [], set()
        for m in candidates:
            if m in seen:
                continue
            seen.add(m)
            wrong.append(m)
            if len(wrong) == 3:
                break
        options = wrong + [correct]
        random.shuffle(options)
        questions.append({
            "kanji": entry["kanji"],
            "on_yomi": entry.get("on_yomi", ""),
            "kun_yomi": entry.get("kun_yomi", ""),
            "correct": correct,
            "options": options,
            "difficulty": entry["difficulty"],
        })
    return jsonify({"level": level, "questions": questions})


# ------------------------------------------------------------- JLPT N5-N1 --
# A separate section from the main Kanji list: every kanji here is tagged
# with its JLPT level (N5 easiest -> N1 hardest), cross-referenced against
# a Kanji-Dictionary-for-Foreigners-style entry (radical-free summary:
# on-yomi, kun-yomi, meaning, plus an easy/medium/hard tier within each
# level for the practice quiz below).

@app.route("/jlpt")
def jlpt_index():
    levels = [{
        "level": lvl,
        "label": JLPT_LEVEL_LABELS[lvl],
        "description": JLPT_LEVEL_DESCRIPTIONS[lvl],
        "count": len(JLPT_BY_LEVEL[lvl]),
        "exam_count": len(JLPT_EXAM_QUESTIONS.get(lvl, [])),
    } for lvl in JLPT_LEVELS]
    return render_template("jlpt_index.html", levels=levels)


@app.route("/jlpt/<level>")
def jlpt_level(level):
    level = level.upper()
    if level not in JLPT_LEVELS:
        return "Level not found", 404
    return render_template(
        "jlpt_level.html",
        level=level,
        label=JLPT_LEVEL_LABELS[level],
        entries=JLPT_BY_LEVEL[level],
        levels=JLPT_LEVELS,
        exam_count=len(JLPT_EXAM_QUESTIONS.get(level, [])),
        exam_categories=JLPT_EXAM_CATEGORIES.get(level, []),
    )


@app.route("/jlpt/<level>/practice")
def jlpt_practice(level):
    level = level.upper()
    if level not in JLPT_LEVELS:
        return "Level not found", 404
    return render_template("jlpt_practice.html", level=level, label=JLPT_LEVEL_LABELS[level])




@app.route("/jlpt/<level>/exam-practice")
def jlpt_exam_practice(level):
    level = level.upper()
    if level not in JLPT_LEVELS:
        return "Level not found", 404
    questions = JLPT_EXAM_QUESTIONS.get(level, [])
    if not questions:
        return "Exam practice is not available for this level yet", 404
    return render_template(
        "jlpt_exam_practice.html",
        level=level,
        label=JLPT_LEVEL_LABELS[level],
        question_count=len(questions),
        categories=JLPT_EXAM_CATEGORIES.get(level, []),
    )


@app.route("/api/jlpt_exam_quiz")
def api_jlpt_exam_quiz():
    """EPUB-backed JLPT exam practice for N5-N1.

    Query params: ?level=N5..N1, ?category=all|<category>, ?count=5..30.
    Question order is randomized while each source question keeps its
    original answer-option order.
    """
    level = (request.args.get("level") or "").upper()
    pool = JLPT_EXAM_QUESTIONS.get(level, [])
    if level not in JLPT_LEVELS or not pool:
        return jsonify({"error": "exam practice unavailable for this level"}), 400

    category = (request.args.get("category") or "all").strip()
    categories = JLPT_EXAM_CATEGORIES.get(level, [])
    if category != "all":
        if category not in categories:
            return jsonify({"error": "invalid category"}), 400
        pool = [q for q in pool if q.get("category") == category]

    try:
        count = int(request.args.get("count", 10))
    except (TypeError, ValueError):
        count = 10
    count = max(5, min(count, 30))
    chosen = random.sample(pool, min(count, len(pool)))

    questions = []
    for q in chosen:
        questions.append({
            "id": q.get("id", ""),
            "category": q.get("category", "Practice"),
            "passage": q.get("passage", ""),
            "prompt": q.get("prompt", ""),
            "options": q.get("options", []),
            "answer_index": q.get("answer_index", 0),
            "answer": q.get("answer", ""),
            "explanation": q.get("explanation", ""),
            "explanation_blocks": q.get("explanation_blocks", []),
        })
    return jsonify({
        "level": level,
        "category": category,
        "available": len(pool),
        "questions": questions,
    })


@app.route("/api/jlpt_quiz")
def api_jlpt_quiz():
    """Same 4-option, no-feedback-until-the-end quiz as /api/kanji_quiz,
    but scoped to one JLPT level. ?level=N5..N1 (required),
    ?difficulty=all|easy|medium|hard, ?count= up to 40."""
    level = (request.args.get("level") or "").upper()
    if level not in JLPT_LEVELS:
        return jsonify({"error": "invalid level"}), 400
    difficulty = (request.args.get("difficulty") or "all").lower()
    if difficulty not in {"all", "easy", "medium", "hard"}:
        difficulty = "all"
    try:
        count = int(request.args.get("count", 20))
    except (TypeError, ValueError):
        count = 20
    count = max(4, min(count, 40))

    level_pool = JLPT_BY_LEVEL[level]
    pool = level_pool if difficulty == "all" else [e for e in level_pool if e["difficulty"] == difficulty]
    if len(pool) < 4:
        pool = level_pool  # this level/difficulty combo is too small on its own

    # Distractors are drawn from the whole level (not just the difficulty
    # slice), so a small "hard" tier doesn't run out of distinct options.
    distractor_pool = level_pool if len(level_pool) >= 4 else JLPT_KANJI

    chosen = random.sample(pool, min(count, len(pool)))
    questions = []
    for entry in chosen:
        correct = entry["meaning"]
        candidates = [e["meaning"] for e in distractor_pool
                      if e["kanji"] != entry["kanji"] and e["meaning"] != correct]
        random.shuffle(candidates)
        wrong, seen = [], set()
        for m in candidates:
            if m in seen:
                continue
            seen.add(m)
            wrong.append(m)
            if len(wrong) == 3:
                break
        options = wrong + [correct]
        random.shuffle(options)
        questions.append({
            "kanji": entry["kanji"],
            "on_yomi": entry.get("on_yomi", ""),
            "kun_yomi": entry.get("kun_yomi", ""),
            "correct": correct,
            "options": options,
            "difficulty": entry["difficulty"],
        })
    return jsonify({"level": level, "difficulty": difficulty, "questions": questions})


@app.route("/everyday")
def everyday_words():
    return render_template(
        "everyday.html",
        grouped=EVERYDAY_BY_CATEGORY,
        categories=EVERYDAY_CATEGORIES,
        total=len(EVERYDAY_WORDS),
    )


@app.route("/api/everyday/<int:idx>")
def everyday_detail(idx):
    if idx < 0 or idx >= len(EVERYDAY_WORDS):
        return jsonify({"error": "not found"}), 404
    return jsonify(EVERYDAY_WORDS[idx])


@app.route("/search")
def search_page():
    query = request.args.get("q", "")
    results = search_words(query) if query else []
    return render_template("search.html", query=query, results=results)


@app.route("/api/search")
def api_search():
    query = request.args.get("q", "")
    results = search_words(query)
    return jsonify(results)


# ------------------------------------------------------------ stories --

# ------------------------------------------------------- conversations --

@app.route("/conversations")
def conversations_list():
    return render_template("conversations.html", conversations=CONVERSATIONS_DATA)


@app.route("/conversations/<conv_id>")
def conversation_detail(conv_id):
    conv = next((c for c in CONVERSATIONS_DATA if c["id"] == conv_id), None)
    if not conv:
        return "Conversation not found", 404
    return render_template("conversation_detail.html", conv=conv)


@app.route("/stories")
def stories_list():
    return render_template("stories.html", stories=STORIES_DATA)


@app.route("/stories/<story_id>")
def story_detail(story_id):
    story = next((st for st in STORIES_DATA if st["id"] == story_id), None)
    if not story:
        return "Story not found", 404
    return render_template("story_detail.html", story=story)


# -------------------------------------------------------------- verbs --

VERB_GROUPS = ["godan", "ichidan", "irregular"]
FORM_LABELS = [
    ("masu", "ます形 (polite)"),
    ("masu_neg", "ません (polite negative)"),
    ("past_polite", "ました (polite past)"),
    ("te", "て形 (te-form)"),
    ("past", "た形 (plain past)"),
    ("nai", "ない形 (plain negative)"),
    ("potential", "可能形 (potential)"),
    ("volitional", "意向形 (volitional)"),
]


@app.route("/verbs")
def verbs_list():
    grouped = [(g, [v for v in VERBS_DATA if v["group"] == g]) for g in VERB_GROUPS]
    return render_template("verbs.html", grouped=grouped, total=len(VERBS_DATA),
                           form_labels=FORM_LABELS)


@app.route("/api/verb/<int:idx>")
def verb_detail(idx):
    if idx < 0 or idx >= len(VERBS_DATA):
        return jsonify({"error": "not found"}), 404
    v = dict(VERBS_DATA[idx])
    v["form_labels"] = FORM_LABELS
    return jsonify(v)


# --------------------------------------------------------- flashcards --

def _sample_vocab_round(pool, count):
    """Choose vocabulary without needlessly recycling mastered words.

    Difficulty is applied before this helper is called. Words the learner has
    already marked as known are held back until there are not enough unseen
    words left for the requested round. Incorrect/unknown words remain eligible
    so useful review is preserved instead of treating every repetition as bad.
    """
    count = min(max(0, int(count)), len(pool))
    if not count:
        return []
    known = _load_progress(current_user()).get("vocab", set())
    unseen = [w for w in pool if w.get("word") not in known]
    review = [w for w in pool if w.get("word") in known]
    random.shuffle(unseen)
    random.shuffle(review)
    return (unseen + review)[:count]


@app.route("/flashcards")
def flashcards():
    return render_template("flashcards.html")


@app.route("/api/flashcards")
def api_flashcards():
    """Build a flashcard deck. deck = hiragana | katakana | kanji | vocab | verbs"""
    deck = (request.args.get("deck") or "kanji").lower()
    level = (request.args.get("difficulty") or "mixed").lower()
    if level in ("mixed", "all"):
        level = "mixed"  # "all" is the label shown in the UI; "mixed" is the internal sentinel
    try:
        count = int(request.args.get("count", 20))
    except ValueError:
        count = 20
    count = max(5, min(count, 100))

    cards = []
    if deck == "hiragana":
        cards = [{"front": k["char"], "back": k["romaji"], "sub": k["type"]}
                 for k in HIRAGANA_DATA]
    elif deck == "katakana":
        cards = [{"front": k["char"], "back": k["romaji"], "sub": k["type"]}
                 for k in KATAKANA_DATA]
    elif deck == "vocab":
        pool = VOCAB_POOL if level == "mixed" else [w for w in VOCAB_POOL if w["difficulty"] == level]
        pool = _sample_vocab_round(pool, count)
        cards = [{"front": w["word"], "back": w["meaning"],
                  "sub": ((w["reading"] or w["romaji"]) +
                          (f" · Common #{w['frequency_rank']}" if w.get("frequency_rank") else ""))} for w in pool]
    elif deck == "verbs":
        pool = VERBS_DATA if level == "mixed" else [v for v in VERBS_DATA if v["difficulty"] == level]
        cards = [{"front": v["word"], "back": v["meaning"],
                  "sub": v["reading"] + " · " + v["forms"]["masu"]["kanji"]} for v in pool]
    elif deck == "radicals":
        cards = [{"front": r["glyph"], "back": r["meaning"],
                  "sub": f"{r['name']} \u00b7 {r['position_label']}",
                  "radical": {"glyph": r["glyph"], "name": r["name"], "meaning": r["meaning"], "parts": "",
                              "story": r["origin"], "position_note": r["position_note"],
                              "meaning_full": r["origin"], "on": "", "kun": ""}}
                 for r in (RADICALS if level == "mixed" else [x for x in RADICALS if x["core"]])]
    else:  # kanji
        pool = PRACTICE_POOL if level == "mixed" else [w for w in PRACTICE_POOL if w["difficulty"] == level]
        cards = [{"front": w["kanji"], "back": w["meaning"],
                  "sub": (w["kun_yomi"] or w["on_yomi"] or "")[:40],
                  "radical": radical_hint(w["kanji"])} for w in pool]

    random.shuffle(cards)
    return jsonify({"deck": deck, "cards": cards[:count]})


@app.route("/api/flashcards_mcq")
def api_flashcards_mcq():
    """4-option flashcards for the Flashcards page's "Select answer" mode.
    Unlike /api/kanji_quiz and /api/jlpt_quiz, this is meant to give
    feedback immediately per card (handled client-side) rather than only
    at the end of a round - it's for learning, not testing.

    ?deck= kanji | vocab | verbs | hiragana | katakana | N5 | N4 | N3 | N2 | N1
    ?difficulty= all | easy | medium | hard (ignored for hiragana/katakana,
        which have no difficulty tiers of their own)
    ?count= up to 40
    """
    deck_raw = (request.args.get("deck") or "kanji").strip()
    deck = deck_raw.lower()
    difficulty = (request.args.get("difficulty") or "all").lower()
    if difficulty not in {"all", "easy", "medium", "hard"}:
        difficulty = "all"
    try:
        count = int(request.args.get("count", 20))
    except (TypeError, ValueError):
        count = 20
    count = max(4, min(count, 40))

    if deck_raw.upper() in JLPT_LEVELS:
        level = deck_raw.upper()
        full_pool = JLPT_BY_LEVEL[level]
        front_key, answer_key, id_key, has_diff = "kanji", "meaning", "kanji", True

        def sub_of(e):
            return e.get("kun_yomi") or e.get("on_yomi") or ""
    elif deck == "kanji":
        full_pool, front_key, answer_key, id_key, has_diff = PRACTICE_POOL, "kanji", "meaning", "kanji", True

        def sub_of(e):
            return (e.get("kun_yomi") or e.get("on_yomi") or "")[:40]
    elif deck == "vocab":
        full_pool, front_key, answer_key, id_key, has_diff = VOCAB_POOL, "word", "meaning", "word", True

        def sub_of(e):
            reading = e.get("reading") or e.get("romaji") or ""
            rank = e.get("frequency_rank")
            return reading + (f" · Common #{rank}" if rank else "")
    elif deck == "verbs":
        full_pool, front_key, answer_key, id_key, has_diff = VERBS_DATA, "word", "meaning", "word", True

        def sub_of(e):
            return e.get("reading") or ""
    elif deck == "radicals":
        full_pool, front_key, answer_key, id_key, has_diff = RADICALS, "glyph", "meaning", "glyph", False

        def sub_of(e):
            return f"{e['name']} \u00b7 {e['position_label']}"
    elif deck == "hiragana":
        full_pool, front_key, answer_key, id_key, has_diff = HIRAGANA_DATA, "char", "romaji", "char", False

        def sub_of(e):
            return ""
    elif deck == "katakana":
        full_pool, front_key, answer_key, id_key, has_diff = KATAKANA_DATA, "char", "romaji", "char", False

        def sub_of(e):
            return ""
    else:
        return jsonify({"error": "invalid deck"}), 400

    pool = full_pool if (difficulty == "all" or not has_diff) else \
        [e for e in full_pool if e.get("difficulty") == difficulty]
    if len(pool) < 4:
        pool = full_pool  # this deck/difficulty combo is too small on its own

    if deck == "vocab":
        chosen = _sample_vocab_round(pool, min(count, len(pool)))
    else:
        chosen = random.sample(pool, min(count, len(pool)))
    questions = []
    for entry in chosen:
        correct = entry[answer_key]
        candidates = [e[answer_key] for e in full_pool
                      if e[id_key] != entry[id_key] and e[answer_key] != correct]
        random.shuffle(candidates)
        wrong, seen = [], set()
        for m in candidates:
            if m in seen:
                continue
            seen.add(m)
            wrong.append(m)
            if len(wrong) == 3:
                break
        options = wrong + [correct]
        random.shuffle(options)
        questions.append({
            "front": entry[front_key],
            "sub": sub_of(entry),
            "correct": correct,
            "options": options,
            "radical": (radical_hint(entry[front_key]) if front_key == "kanji" else
                        {"glyph": entry["glyph"], "name": entry["name"], "meaning": entry["meaning"], "parts": "",
                         "story": entry["origin"], "position_note": entry["position_note"],
                         "meaning_full": "", "on": "", "kun": ""} if front_key == "glyph" else None),
        })
    return jsonify({"deck": deck_raw, "difficulty": difficulty, "questions": questions})


# ----------------------------------------------------------------- progress --
# Tracks which flashcards a person has marked "Knew it" for, per deck, so
# the dashboard can show a real completion meter instead of just the
# streak. Same guest-file / per-user-file split as the streak: a signed-in
# person's progress is saved to their account, a guest's is saved to this
# device only.

PROGRESS_DECKS = {
    "kanji": ("Kanji", lambda: len(PRACTICE_POOL)),
    "vocab": ("Vocabulary", lambda: len(VOCAB_POOL)),
    "verbs": ("Verbs", lambda: len(VERBS_DATA)),
    "radicals": ("Radicals", lambda: len(RADICALS)),
    "hiragana": ("Hiragana", lambda: len(HIRAGANA_DATA)),
    "katakana": ("Katakana", lambda: len(KATAKANA_DATA)),
    "jlpt": ("JLPT (N5–N1)", lambda: len(JLPT_KANJI)),
}

PROGRESS_FILE = DATA_DIR / "progress.json"
USER_PROGRESS_FILE = DATA_DIR / "user_progress.json"


def _load_all_user_progress():
    if not USER_PROGRESS_FILE.exists():
        return {}
    try:
        with open(USER_PROGRESS_FILE, encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def _load_progress(user=None):
    """Returns {deck: set(known fronts)}."""
    if user is None:
        if not PROGRESS_FILE.exists():
            return {}
        try:
            with open(PROGRESS_FILE, encoding="utf-8") as f:
                raw = json.load(f)
        except (json.JSONDecodeError, OSError):
            return {}
    else:
        raw = _load_all_user_progress().get(str(user["id"]), {})
    return {deck: set(items) for deck, items in raw.items() if deck in PROGRESS_DECKS}


def _save_progress(progress, user=None):
    serialisable = {deck: sorted(items) for deck, items in progress.items()}
    if user is None:
        with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
            json.dump(serialisable, f, ensure_ascii=False, indent=2)
        return
    all_progress = _load_all_user_progress()
    all_progress[str(user["id"])] = serialisable
    with open(USER_PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(all_progress, f, ensure_ascii=False, indent=2)


def _progress_summary(user=None):
    progress = _load_progress(user)
    decks = []
    total_known = total_all = 0
    for key, (label, count_fn) in PROGRESS_DECKS.items():
        known = len(progress.get(key, set()))
        total = count_fn()
        known = min(known, total)
        pct = round(100 * known / total) if total else 0
        decks.append({"deck": key, "label": label, "known": known, "total": total, "pct": pct})
        total_known += known
        total_all += total
    overall_pct = round(100 * total_known / total_all) if total_all else 0
    return {
        "decks": decks,
        "known": total_known,
        "total": total_all,
        "pct": overall_pct,
        "logged_in": user is not None,
    }


@app.route("/api/progress")
def api_progress_get():
    return jsonify(_progress_summary(current_user()))


@app.route("/api/progress/mark", methods=["POST"])
def api_progress_mark():
    payload = request.get_json(silent=True) or {}
    deck = (payload.get("deck") or "").lower()
    front = payload.get("front")
    if deck not in PROGRESS_DECKS or not front:
        return jsonify({"error": "invalid deck or front"}), 400
    user = current_user()
    progress = _load_progress(user)
    progress.setdefault(deck, set()).add(str(front))
    _save_progress(progress, user)
    return jsonify(_progress_summary(user))


# --------------------------------------------------------------- roadmap --
# The Duolingo-style learning path: a straight, single-file sequence of
# chapters (ROADMAP_CHAPTER_ORDER) spanning every section. A chapter
# unlocks once the one immediately before it is completed - simpler than
# per-section gating, and it means "the next thing to do" is always
# unambiguous. Same guest-file / per-user-file split as the streak and
# flashcard progress above.

ROADMAP_FILE = DATA_DIR / "roadmap_progress.json"
USER_ROADMAP_FILE = DATA_DIR / "user_roadmap_progress.json"
ROADMAP_START_FILE = DATA_DIR / "roadmap_start.json"
USER_ROADMAP_START_FILE = DATA_DIR / "user_roadmap_start.json"


def _load_all_user_roadmap():
    if not USER_ROADMAP_FILE.exists():
        return {}
    try:
        with open(USER_ROADMAP_FILE, encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def _load_roadmap_progress(user=None):
    """Returns a set of completed chapter ids."""
    if user is None:
        if not ROADMAP_FILE.exists():
            return set()
        try:
            with open(ROADMAP_FILE, encoding="utf-8") as f:
                return set(json.load(f))
        except (json.JSONDecodeError, OSError):
            return set()
    return set(_load_all_user_roadmap().get(str(user["id"]), []))


def _save_roadmap_progress(completed, user=None):
    serialisable = sorted(completed)
    if user is None:
        with open(ROADMAP_FILE, "w", encoding="utf-8") as f:
            json.dump(serialisable, f, ensure_ascii=False, indent=2)
        return
    all_progress = _load_all_user_roadmap()
    all_progress[str(user["id"])] = serialisable
    with open(USER_ROADMAP_FILE, "w", encoding="utf-8") as f:
        json.dump(all_progress, f, ensure_ascii=False, indent=2)


def _load_roadmap_start(user=None):
    """Optional placement preference chosen during v3 onboarding.

    This does not mark earlier chapters complete; it only changes which
    unfinished chapter Kotoba recommends next. Learners can still open any
    earlier chapter from the roadmap.
    """
    path = ROADMAP_START_FILE if user is None else USER_ROADMAP_START_FILE
    if not path.exists():
        return None
    try:
        with open(path, encoding="utf-8") as f:
            raw = json.load(f)
    except (json.JSONDecodeError, OSError):
        return None
    if user is None:
        chapter_id = raw.get("chapter_id") if isinstance(raw, dict) else None
    else:
        chapter_id = raw.get(str(user["id"])) if isinstance(raw, dict) else None
    return chapter_id if chapter_id in ROADMAP_CHAPTERS else None


def _save_roadmap_start(chapter_id, user=None):
    if user is None:
        with open(ROADMAP_START_FILE, "w", encoding="utf-8") as f:
            json.dump({"chapter_id": chapter_id}, f, ensure_ascii=False, indent=2)
        return
    raw = {}
    if USER_ROADMAP_START_FILE.exists():
        try:
            with open(USER_ROADMAP_START_FILE, encoding="utf-8") as f:
                raw = json.load(f)
        except (json.JSONDecodeError, OSError):
            raw = {}
    if not isinstance(raw, dict):
        raw = {}
    raw[str(user["id"])] = chapter_id
    with open(USER_ROADMAP_START_FILE, "w", encoding="utf-8") as f:
        json.dump(raw, f, ensure_ascii=False, indent=2)


def _roadmap_chapter_status(chapter_id, completed):
    """"completed" | "unlocked". Since v2.9 every chapter is open from the
    start - learners can jump to any topic (or the Grand Review) at any
    time; completing a chapter just ticks it off the path."""
    return "completed" if chapter_id in completed else "unlocked"


ROADMAP_STAGE_INFO = {
    "first-steps": ("Foundation", "Start here"),
    "radicals": ("Foundation", "Build kanji sense"),
    "everyday-life": ("Beginner", "Everyday Japanese"),
    "out-and-about": ("Beginner", "Use Japanese outside"),
    "people-culture": ("Beginner", "People and culture"),
    "food-drink": ("Beginner", "Food and ordering"),
    "modern-life": ("Beginner+", "Modern vocabulary"),
    "grammar-foundations": ("Lower intermediate", "Connect your Japanese"),
    "toward-fluency": ("Intermediate", "Read and converse more naturally"),
    "upper-intermediate": ("Upper intermediate", "N3-style grammar and nuance"),
    "advanced-grammar": ("Advanced", "N2-style formal and nuanced grammar"),
    "n1-mastery": ("Advanced+", "N1 source-backed grammar mastery"),
    "grand-review": ("Mastery check", "Mixed review"),
}


def _next_roadmap_id(completed, user=None):
    start_id = _load_roadmap_start(user)
    start_index = ROADMAP_CHAPTER_ORDER.index(start_id) if start_id in ROADMAP_CHAPTER_ORDER else 0
    for chapter_id in ROADMAP_CHAPTER_ORDER[start_index:]:
        if chapter_id not in completed:
            return chapter_id
    return None


def _roadmap_view_data(user):
    completed = _load_roadmap_progress(user)
    next_id = _next_roadmap_id(completed, user)
    sections = []
    for sec in ROADMAP:
        stage, stage_note = ROADMAP_STAGE_INFO.get(sec["id"], ("Course", "Keep learning"))
        chapters = [{**c,
                     "status": _roadmap_chapter_status(c["id"], completed),
                     "is_next": c["id"] == next_id}
                    for c in sec["chapters"]]
        sections.append({**sec, "chapters": chapters, "stage": stage, "stage_note": stage_note})
    done, total = len(completed), len(ROADMAP_CHAPTER_ORDER)
    return {"sections": sections, "done": done, "total": total,
            "next_id": next_id,
            "pct": round(100 * done / total) if total else 0}


def _home_learning_state(user):
    """Compact state for the new learner-first home screen.

    The existing roadmap remains fully open, but home always points to the
    first unfinished chapter so a beginner never has to decide what to do
    next. Nothing is auto-completed or hidden.
    """
    roadmap = _roadmap_view_data(user)
    completed = _load_roadmap_progress(user)
    next_id = roadmap.get("next_id")
    next_lesson = None
    if next_id:
        chapter = ROADMAP_CHAPTERS[next_id]
        section = next((sec for sec in ROADMAP if any(c["id"] == next_id for c in sec["chapters"])), None)
        vocab_count = len(chapter.get("vocab", []))
        if chapter.get("kind") == "review":
            minutes = 10
        elif chapter.get("kind") == "link":
            minutes = 5
        else:
            minutes = max(4, min(12, 3 + round(vocab_count / 7)))
        stage = ROADMAP_STAGE_INFO.get(section["id"] if section else "", ("Course", ""))[0]
        idx = ROADMAP_CHAPTER_ORDER.index(next_id)
        next_lesson = {
            "id": next_id,
            "title": chapter["title"],
            "icon": chapter.get("icon", "学"),
            "section": section["title"] if section else "Roadmap",
            "stage": stage,
            "minutes": minutes,
            "position": idx + 1,
            "total": len(ROADMAP_CHAPTER_ORDER),
            "url": url_for("roadmap_chapter", chapter_id=next_id),
        }
    else:
        next_lesson = {
            "id": "grand-review",
            "title": "Grand Review — 50 Questions",
            "icon": "🏆",
            "section": "Course complete",
            "stage": "Mastery check",
            "minutes": 10,
            "position": len(ROADMAP_CHAPTER_ORDER),
            "total": len(ROADMAP_CHAPTER_ORDER),
            "url": url_for("roadmap_chapter", chapter_id="grand-review"),
        }
    streak = _compute_streak(_load_streak_dates(user))
    learner_state = _learner.load_state(DATA_DIR, user)
    learner = _learner.summary(learner_state, streak_current=streak.get("current", 0))
    return {
        "roadmap": roadmap,
        "next_lesson": next_lesson,
        "streak": streak,
        "progress": _progress_summary(user),
        "learner": learner,
    }


def _roadmap_link_url(chapter):
    try:
        return url_for(chapter["link_endpoint"])
    except Exception:
        return url_for("index")


def _rm_distractors(pool, exclude_value, key, n=3):
    candidates = [item[key] for item in pool if item[key] != exclude_value]
    random.shuffle(candidates)
    out, seen = [], set()
    for val in candidates:
        if val in seen:
            continue
        seen.add(val)
        out.append(val)
        if len(out) == n:
            break
    return out


def _rm_choice(correct, wrong):
    options = wrong + [correct]
    random.shuffle(options)
    return options


def _kana_candidates(chapter):
    """Hiragana / Katakana practice: every character is asked both ways
    ("which sound?" and "which kana?") with an explanation."""
    X = _sibling("roadmap_extra")
    script = chapter["kana"]
    data = load_json(f"{script}.json")
    by_char = {e["char"]: e for e in data}
    vocab = chapter["vocab"]
    out = {"meaning": [], "reading": [], "reverse": [], "fillblank": [], "radical": []}
    for item in vocab:
        ch, rm = item["jp"], item["romaji"]
        ex = X.kana_explain(script, by_char[ch], data)
        wrong = _rm_distractors(vocab, rm, "romaji")
        if len(wrong) == 3:
            out["meaning"].append({"type": "meaning", "label": "Which sound does this kana make?",
                                   "prompt": ch, "correct": rm, "options": _rm_choice(rm, wrong), "explain": ex})
        same_sound = {v["jp"] for v in vocab if v["romaji"] == rm}
        pool = [v for v in vocab if v["jp"] not in same_sound]
        random.shuffle(pool)
        if len(pool) >= 3:
            out["reverse"].append({"type": "reverse", "label": "Which kana makes this sound?",
                                   "prompt": rm, "correct": ch,
                                   "options": _rm_choice(ch, [v["jp"] for v in pool[:3]]), "explain": ex})
    return out


def _rm_candidates(chapter):
    """Every question this chapter can produce, grouped by type:
    meaning / reading / reverse / fillblank / radical. Each question carries
    an `explain` text that the quiz shows right after the learner answers."""
    vocab = chapter.get("vocab", [])
    sentences = chapter.get("sentences", [])
    by_jp = {w["jp"]: w for w in vocab}
    out = {"meaning": [], "reading": [], "reverse": [], "fillblank": [], "radical": []}
    if chapter.get("kana"):
        return _kana_candidates(chapter)
    for item in vocab:
        jp, rd, rm, mn = item["jp"], item["reading"], item["romaji"], item["meaning"]
        wrong = _rm_distractors(vocab, mn, "meaning")
        if len(wrong) == 3:
            out["meaning"].append({
                "type": "meaning", "prompt": jp, "reading": rd, "correct": mn,
                "options": _rm_choice(mn, wrong),
                "explain": f"{jp} is read \u201c{rd}\u201d ({rm}) and means \u201c{mn}\u201d."})
        wrong = _rm_distractors(vocab, rm, "romaji")
        if len(wrong) == 3:
            out["reading"].append({
                "type": "reading", "prompt": jp, "correct": rm,
                "options": _rm_choice(rm, wrong),
                "explain": f"{jp} is written {rd} and pronounced \u201c{rm}\u201d. It means \u201c{mn}\u201d."})
        wrong = _rm_distractors(vocab, jp, "jp")
        if len(wrong) == 3:
            out["reverse"].append({
                "type": "reverse", "prompt": mn, "correct": jp,
                "options": _rm_choice(jp, wrong),
                "explain": f"\u201c{mn}\u201d in Japanese is {jp} ({rd} / {rm})."})
    for sent in sentences:
        wrong = _rm_distractors(vocab, sent["blank"], "jp")
        if len(wrong) == 3:
            w = by_jp.get(sent["blank"], {})
            out["fillblank"].append({
                "type": "fillblank", "prompt": sent["jp"], "reading": sent["reading"],
                "english": sent["english"], "correct": sent["blank"],
                "options": _rm_choice(sent["blank"], wrong),
                "explain": f"The sentence means \u201c{sent['english']}\u201d, so the missing word is {sent['blank']}"
                           + (f" ({w.get('reading', '')}: {w.get('meaning', '')})." if w else ".")})
    rids = chapter.get("radicals") or []
    if rids:
        kmeaning = {e["kanji"]: e["meaning"] for e in KANJI_DATA}

        def label(r):
            short_name = r['name'].split('\u30fb')[0]  # kept out of the f-string: a backslash there is a SyntaxError before Python 3.12
            return f"{r['glyph']}  ({short_name})"
        pool = [RADICAL_BY_ID[i] for i in rids if i in RADICAL_BY_ID]
        for r in pool:
            examples = [k for k in r["kanji"] if k in kmeaning]
            if not examples:
                continue
            ch = random.choice(examples)
            wrong = [label(o) for o in pool if o["glyph"] != r["glyph"]]
            random.shuffle(wrong)
            wrong = wrong[:3]
            if len(wrong) < 3:
                continue
            st = KANJI_STORIES.get(ch) or {}
            why = (f" {ch} = {st['parts']}: {st['story']}" if st.get("parts") else "")
            out["radical"].append({
                "type": "radical", "prompt": ch, "english": kmeaning[ch],
                "correct": label(r), "options": _rm_choice(label(r), wrong),
                "explain": f"{ch} means \u201c{kmeaning[ch]}\u201d and contains the {r['meaning']} radical {r['glyph']} "
                           f"({r['name']}). It {r['position_note']}.{why}"})
    return out


def _build_roadmap_quiz(chapter, count=None):
    """Full-coverage chapter quiz: every word is asked once (rotating between
    meaning / reading / English-to-Japanese), every example sentence becomes a
    fill-in-the-blank, and radical chapters add 'which radical is inside this
    kanji?' cards. Capped at 50 to keep a chapter quick."""
    cand = _rm_candidates(chapter)
    vocab = chapter.get("vocab", [])
    if chapter.get("kana"):
        both = cand["meaning"] + cand["reverse"]
        random.shuffle(both)
        return both[:count or 30]
    picked = list(cand["fillblank"]) + list(cand["radical"])
    by_prompt = {t: {q["prompt"] if t != "reverse" else q["correct"]: q for q in cand[t]}
                 for t in ("meaning", "reading", "reverse")}
    # Grammar-pattern roadmap chapters focus on function and recognition.
    # Many advanced source forms are kana-only or do not have a useful
    # standalone romaji reading, so a reading quiz would test duplicated
    # surface text rather than grammar knowledge.
    order = ["meaning", "reverse"] if "-grammar-" in chapter.get("id", "") else ["meaning", "reading", "reverse"]
    # Only rotate through question types that actually have candidates. Grammar
    # chapters intentionally use two types, and some chapters can have fewer
    # after distractor filtering. Using a fixed modulo of 3 caused IndexError
    # on N3/N2/N1 roadmap grammar routes during the Android smoke test.
    order = [t for t in order if by_prompt.get(t)]
    random.shuffle(order)
    if order:
        n_types = len(order)
        for i, item in enumerate(vocab):
            for k in range(n_types):
                q = by_prompt[order[(i + k) % n_types]].get(item["jp"])
                if q:
                    picked.append(q)
                    break
    random.shuffle(picked)
    return picked[:count or 50]


_QUOTA = {"meaning": 0.26, "reading": 0.16, "reverse": 0.26, "fillblank": 0.20, "radical": 0.12}


def _pooled_quiz(chapters, count):
    """Balanced mixed quiz drawn from several chapters. Words that mean
    different things in different chapters are skipped so every question has
    exactly one right answer."""
    seen, dupes = {}, set()
    for ch in chapters:
        for w in ch.get("vocab", []):
            if seen.setdefault(w["jp"], w["meaning"]) != w["meaning"]:
                dupes.add(w["jp"])
    pools = {t: [] for t in _QUOTA}
    used = set()
    for ch in chapters:
        if ch.get("kind") != "lesson":
            continue
        for t, qs in _rm_candidates(ch).items():
            for q in qs:
                key = (t, q["prompt"], q["correct"])
                word = q["correct"] if t in ("reverse", "fillblank") else q["prompt"]
                if key in used or (t != "radical" and word in dupes):
                    continue
                used.add(key)
                pools[t].append(q)
    for g in pools.values():
        random.shuffle(g)
    picked = []
    for t, frac in _QUOTA.items():
        picked.extend(pools[t][:round(count * frac)])
    left = [q for t, g in pools.items() for q in g[round(count * _QUOTA[t]):]]
    random.shuffle(left)
    picked.extend(left[:max(0, count - len(picked))])
    random.shuffle(picked)
    return picked[:count]


def _build_mixed_quiz(count=50):
    """Grand Review: `count` questions drawn from every lesson chapter."""
    return _pooled_quiz([ch for sec in ROADMAP for ch in sec["chapters"]], count)


def _build_section_quiz(section_id, count=50):
    """Section Review: `count` questions from every chapter in the section."""
    sec = next((x for x in ROADMAP if x["id"] == section_id), None)
    return _pooled_quiz(sec["chapters"] if sec else [], count)


def _roadmap_summary(user, scope="all"):
    """Recap panel shown before a review. scope="all" = one row per section
    (Grand Review); otherwise one row per chapter of that section."""
    completed = _load_roadmap_progress(user)
    rows, words = [], 0
    if scope == "all":
        for sec in ROADMAP:
            if sec["id"] == "grand-review":
                continue
            chs = sec["chapters"]
            n_words = sum(len(c.get("vocab", [])) for c in chs)
            words += n_words
            rows.append({"title": sec["title"], "right": f"{sum(1 for c in chs if c['id'] in completed)} / {len(chs)} chapters \u00b7 {n_words} items"})
        return {"kind": "all", "title": "Your journey so far", "rows": rows, "words": words}
    sec = next((x for x in ROADMAP if x["id"] == scope), None) or {"title": "", "chapters": []}
    for c in sec["chapters"]:
        if c.get("kind") == "lesson":
            n = len(c.get("vocab", []))
            words += n
            rows.append({"title": c["title"], "right": f"{n} items \u00b7 " + ("done" if c["id"] in completed else "not finished yet")})
    return {"kind": "section", "title": f"What you learned in {sec['title']}", "rows": rows, "words": words}


@app.route("/roadmap")
def roadmap_page():
    return render_template("roadmap.html", roadmap=_roadmap_view_data(current_user()))


@app.route("/roadmap/<chapter_id>")
def roadmap_chapter(chapter_id):
    chapter = ROADMAP_CHAPTERS.get(chapter_id)
    if chapter is None:
        return redirect(url_for("roadmap_page"))

    user = current_user()
    completed = _load_roadmap_progress(user)
    status = _roadmap_chapter_status(chapter_id, completed)
    if status == "locked":
        return redirect(url_for("roadmap_page"))

    if chapter["kind"] == "link":
        # The lesson for this chapter already exists elsewhere in the app
        # (Hiragana, Verbs, Conversations, ...) - visiting it here is the
        # whole point, so mark it done and send the person straight there.
        if status != "completed":
            completed.add(chapter_id)
            _save_roadmap_progress(completed, user)
        return redirect(_roadmap_link_url(chapter))

    if chapter["kind"] == "review":
        scope = chapter.get("scope", "all")
        n = chapter.get("count", 50)
        quiz = _build_mixed_quiz(n) if scope == "all" else _build_section_quiz(scope, n)
        return render_template(
            "roadmap_chapter.html",
            chapter={**chapter, "vocab": []},
            quiz_json=json.dumps(quiz, ensure_ascii=False),
            already_completed=(status == "completed"),
            summary=_roadmap_summary(user, scope),
            quiz_count=len(quiz),
        )

    if chapter["kind"] != "lesson":
        return redirect(url_for("roadmap_page"))  # placeholder - nothing built yet

    quiz = _build_roadmap_quiz(chapter)
    return render_template(
        "roadmap_chapter.html",
        chapter=chapter,
        quiz_json=json.dumps(quiz, ensure_ascii=False),
        already_completed=(status == "completed"),
        summary=None,
    )


@app.route("/api/roadmap/start", methods=["POST"])
def api_roadmap_start():
    payload = request.get_json(silent=True) or {}
    chapter_id = payload.get("chapter_id")
    if chapter_id not in ROADMAP_CHAPTERS:
        return jsonify({"error": "unknown chapter"}), 400
    _save_roadmap_start(chapter_id, current_user())
    return jsonify({"ok": True, "chapter_id": chapter_id})


@app.route("/api/roadmap/complete", methods=["POST"])
def api_roadmap_complete():
    payload = request.get_json(silent=True) or {}
    chapter_id = payload.get("chapter_id")
    chapter = ROADMAP_CHAPTERS.get(chapter_id)
    if chapter is None:
        return jsonify({"error": "unknown chapter"}), 400

    user = current_user()
    completed = _load_roadmap_progress(user)
    if _roadmap_chapter_status(chapter_id, completed) == "locked":
        return jsonify({"error": "chapter is locked"}), 400

    completed.add(chapter_id)
    _save_roadmap_progress(completed, user)
    idx = ROADMAP_CHAPTER_ORDER.index(chapter_id)
    next_id = ROADMAP_CHAPTER_ORDER[idx + 1] if idx + 1 < len(ROADMAP_CHAPTER_ORDER) else None
    return jsonify({"ok": True, "next_chapter_id": next_id})


# -------------------------------------------------- writing practice --

@app.route("/write")
@app.route("/writing-practice")
def write_page():
    """The section is called "Writing Practice" in the UI. /write stays
    registered so older bookmarks and any cached service-worker entry
    from a previous version still resolve."""
    return render_template(
        "write.html",
        hiragana=HIRAGANA_DATA,
        katakana=KATAKANA_DATA,
    )


# ------------------------------------------------- about & feedback --

DEVELOPER = {
    "name": "Aryan Raj",
    "role": "Software Engineer",
    "email": "Aryanrajr868@gmail.com",
}

FEEDBACK_FILE = DATA_DIR / "feedback.json"
MAX_FEEDBACK_ENTRIES = 200
MAX_FEEDBACK_CHARS = 4000


@app.route("/about")
def about_page():
    return render_template("about.html", developer=DEVELOPER,
                            jlpt_total=len(JLPT_KANJI), verb_total=len(VERBS_DATA))


@app.route("/feedback")
def feedback_page():
    return render_template("feedback.html", feedback_email=DEVELOPER["email"])


def _load_feedback():
    if not FEEDBACK_FILE.exists():
        return []
    try:
        with open(FEEDBACK_FILE, encoding="utf-8") as f:
            data = json.load(f)
        entries = data.get("entries", [])
        return entries if isinstance(entries, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def _save_feedback(entries):
    with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
        json.dump({"entries": entries}, f, ensure_ascii=False, indent=1)


@app.route("/api/feedback", methods=["GET", "POST", "DELETE"])
def api_feedback():
    """Feedback notes, stored in a flat JSON file beside the app's data.

    This is deliberately local-only: the packaged app has no server to
    talk to, so a note is kept on the device and the person decides
    whether to mail it on from the Feedback page.
    """
    if request.method == "GET":
        return jsonify({"entries": _load_feedback()})

    if request.method == "DELETE":
        try:
            _save_feedback([])
        except OSError:
            return jsonify({"ok": False, "error": "could not write feedback file"}), 500
        return jsonify({"ok": True, "entries": []})

    payload = request.get_json(silent=True) or {}
    message = str(payload.get("message", "")).strip()
    if not message:
        return jsonify({"ok": False, "error": "message is required"}), 400

    try:
        rating = int(payload.get("rating") or 0)
    except (TypeError, ValueError):
        rating = 0

    entry = {
        "topic": str(payload.get("topic", "Other"))[:60],
        "rating": rating if 1 <= rating <= 5 else 0,
        "message": message[:MAX_FEEDBACK_CHARS],
        "name": str(payload.get("name", "")).strip()[:120],
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    entries = _load_feedback()
    entries.append(entry)
    # keep the file bounded - this is a scratchpad, not an archive
    entries = entries[-MAX_FEEDBACK_ENTRIES:]

    try:
        _save_feedback(entries)
    except OSError:
        return jsonify({"ok": False, "error": "could not write feedback file"}), 500

    return jsonify({"ok": True, "entries": entries})


# ---------------------------------------------------------- learner engine --

def _learner_summary(user=None):
    if user is None:
        user = current_user()
    streak = _compute_streak(_load_streak_dates(user))
    state = _learner.load_state(DATA_DIR, user)
    return _learner.summary(state, streak_current=streak.get("current", 0))


@app.route("/api/learner/summary")
def api_learner_summary():
    return jsonify(_learner_summary(current_user()))


@app.route("/api/learner/record", methods=["POST"])
def api_learner_record():
    payload = request.get_json(silent=True) or {}
    if not (payload.get("id") or payload.get("front") or payload.get("prompt")):
        return jsonify({"error": "missing learning item"}), 400
    result = _learner.record_answer(DATA_DIR, current_user(), payload)
    # Count any scored interaction as activity for the existing streak too.
    dates = _load_streak_dates(current_user())
    dates.add(date.today().isoformat())
    try:
        _save_streak_dates(dates, current_user())
    except OSError:
        pass
    return jsonify(result)


@app.route("/api/learner/action", methods=["POST"])
def api_learner_action():
    payload = request.get_json(silent=True) or {}
    action = (payload.get("action") or "").lower()
    if action not in {"audio", "speaking", "lessons", "mock"}:
        return jsonify({"error": "invalid action"}), 400
    return jsonify(_learner.record_action(DATA_DIR, current_user(), action, payload.get("amount", 1)))


@app.route("/review")
def smart_review_page():
    return render_template("smart_review.html", learner=_learner_summary(current_user()))


@app.route("/api/review/due")
def api_review_due():
    try:
        limit = max(5, min(int(request.args.get("limit", 20)), 60))
    except (TypeError, ValueError):
        limit = 20
    user = current_user()
    state = _learner.load_state(DATA_DIR, user)
    list_name=(request.args.get("list") or "").strip()
    if list_name and list_name in state.get("lists",{}):
        saved=state["lists"].get(list_name,[])
        rows=[]
        for fav in saved:
            key=fav.get("key") or _learner.item_key(fav.get("kind"),fav.get("id"))
            existing=state.get("srs",{}).get(key)
            if existing:
                rows.append({"key":key,**existing})
            else:
                rows.append({"key":key,"kind":fav.get("kind","item"),"id":fav.get("id") or fav.get("front"),
                             "front":fav.get("front") or fav.get("id"),"answer":fav.get("meaning","") or fav.get("reading",""),
                             "reading":fav.get("reading", ""),"meaning":fav.get("meaning", ""),"sub":f"Saved in {list_name}",
                             "mastery":"New","reviews":0,"interval":0})
        rank={"Weak":0,"Learning":1,"New":2,"Familiar":3,"Mastered":4}
        rows.sort(key=lambda x:(rank.get(x.get("mastery","New"),9),x.get("next_review","")))
        return jsonify({"items":rows[:limit],"summary":_learner.summary(state),"list":list_name})
    rows = _learner.due_items(state, limit)
    # A Daily Review should never be an empty dead end. Fill remaining slots
    # with unseen vocabulary at the learner's current placement/difficulty.
    seen_keys = set(state.get("srs", {}).keys())
    remaining = limit - len(rows)
    if remaining > 0:
        placement = state.get("placement") or {}
        approx = placement.get("approx_level", "N5")
        difficulty = "easy" if approx in {"N5", "N4"} else ("medium" if approx == "N3" else "hard")
        pool = [w for w in VOCAB_POOL if w.get("difficulty") == difficulty]
        pool += [w for w in VOCAB_POOL if w.get("difficulty") != difficulty]
        random.shuffle(pool)
        for w in pool:
            key = _learner.item_key("vocab", w.get("word"))
            if key in seen_keys:
                continue
            rows.append({
                "key": key, "kind": "vocab", "id": w.get("word"), "front": w.get("word"),
                "answer": w.get("meaning"), "reading": w.get("reading") or w.get("romaji") or "",
                "sub": (f"Common #{w['frequency_rank']}" if w.get("frequency_rank") else "New word"),
                "mastery": "New", "reviews": 0, "interval": 0,
            })
            seen_keys.add(key)
            if len(rows) >= limit:
                break
    return jsonify({"items": rows, "summary": _learner.summary(state)})


@app.route("/mistakes")
def mistakes_page():
    state = _learner.load_state(DATA_DIR, current_user())
    mistakes = list(state.get("mistakes", {}).values())
    mistakes.sort(key=lambda m: (bool(m.get("mastered")), m.get("last_missed", "")), reverse=False)
    return render_template("mistakes.html", mistakes=mistakes, learner=_learner_summary(current_user()))


@app.route("/favorites")
def favorites_page():
    state = _learner.load_state(DATA_DIR, current_user())
    return render_template("favorites.html", lists=state.get("lists", {}))


@app.route("/api/favorites/toggle", methods=["POST"])
def api_favorites_toggle():
    payload = request.get_json(silent=True) or {}
    item = payload.get("item") or {}
    if not (item.get("id") or item.get("front") or item.get("word")):
        return jsonify({"error": "missing item"}), 400
    return jsonify(_learner.toggle_favorite(DATA_DIR, current_user(), item, payload.get("list")))


@app.route("/api/favorites/list", methods=["POST"])
def api_favorites_list():
    payload = request.get_json(silent=True) or {}
    ok = _learner.add_list(DATA_DIR, current_user(), payload.get("name"))
    return jsonify({"ok": ok}), (200 if ok else 400)


@app.route("/api/favorites/copy", methods=["POST"])
def api_favorites_copy():
    payload=request.get_json(silent=True) or {}
    result=_learner.copy_favorite(DATA_DIR,current_user(),payload.get("source"),payload.get("target"),str(payload.get("key") or ""))
    return jsonify(result),(200 if result.get("ok") else 400)


@app.route("/api/favorites/remove", methods=["POST"])
def api_favorites_remove():
    payload=request.get_json(silent=True) or {}
    ok=_learner.remove_favorite(DATA_DIR,current_user(),payload.get("list"),str(payload.get("key") or ""))
    return jsonify({"ok":ok}),(200 if ok else 404)


@app.route("/backup")
def backup_page():
    return render_template("backup.html")


def _backup_payload(user):
    state = _learner.load_state(DATA_DIR, user)
    progress = {k: sorted(v) for k, v in _load_progress(user).items()}
    return {
        "format": "kotoba-backup-v1",
        "created": datetime.now().replace(microsecond=0).isoformat(),
        "app_version": APP_VERSION,
        "learner": state,
        "progress": progress,
        "roadmap_completed": sorted(_load_roadmap_progress(user)),
        "roadmap_start": _load_roadmap_start(user),
        "streak_dates": sorted(_load_streak_dates(user)),
    }


@app.route("/api/backup/data", methods=["GET", "POST"])
def api_backup_data():
    user = current_user()
    if request.method == "GET":
        return jsonify(_backup_payload(user))
    payload = request.get_json(silent=True) or {}
    if payload.get("format") != "kotoba-backup-v1":
        return jsonify({"error": "not a Kotoba backup"}), 400
    try:
        if isinstance(payload.get("learner"), dict):
            _learner.save_state(DATA_DIR, payload["learner"], user)
        if isinstance(payload.get("progress"), dict):
            progress = {k: set(v) for k, v in payload["progress"].items() if k in PROGRESS_DECKS and isinstance(v, list)}
            _save_progress(progress, user)
        if isinstance(payload.get("roadmap_completed"), list):
            _save_roadmap_progress(set(payload["roadmap_completed"]), user)
        if payload.get("roadmap_start") in ROADMAP_CHAPTERS:
            _save_roadmap_start(payload["roadmap_start"], user)
        if isinstance(payload.get("streak_dates"), list):
            _save_streak_dates(set(payload["streak_dates"]), user)
    except OSError:
        return jsonify({"error": "could not write backup data"}), 500
    return jsonify({"ok": True, "summary": _learner_summary(user)})


# ------------------------------------------------------------ placement --

def _choice_question(qid, qtype, prompt, correct, distractors, sub="", band="N5"):
    wrong = []
    seen = {correct}
    for d in distractors:
        if d and d not in seen:
            wrong.append(d); seen.add(d)
        if len(wrong) == 3:
            break
    options = wrong + [correct]
    random.shuffle(options)
    return {"id": qid, "type": qtype, "prompt": prompt, "sub": sub,
            "options": options, "answer_index": options.index(correct), "band": band}


def _placement_questions():
    """Balanced 25-question diagnostic spanning kana and N5→N1 skills.

    It is a study-placement diagnostic, not an official JLPT score estimate.
    Each higher band gets at least one vocabulary, kanji and/or grammar item
    so a strong learner isn't placed solely from beginner material.
    """
    out = []
    kana_pool = random.sample(HIRAGANA_DATA[:46], min(3, len(HIRAGANA_DATA[:46])))
    for i, e in enumerate(kana_pool):
        distract = [x["romaji"] for x in HIRAGANA_DATA[:46] if x["char"] != e["char"]]
        random.shuffle(distract)
        out.append(_choice_question(f"kana-{i}", "Kana", e["char"], e["romaji"], distract, "Choose the sound.", "N5"))

    rank_bands = [(1,300,"N5"),(301,700,"N4"),(701,1200,"N3"),(1201,1600,"N2"),(1601,1999,"N1")]
    for i,(lo,hi,band) in enumerate(rank_bands):
        pool=[w for w in FREQUENCY_WORDS if lo <= int(w.get("rank",9999)) <= hi and w.get("meaning")]
        if not pool: continue
        e=random.choice(pool); distract=[x["meaning"] for x in pool if x["word"] != e["word"]]; random.shuffle(distract)
        out.append(_choice_question(f"vocab-{i}","Vocabulary",e["word"],e["meaning"],distract,e.get("reading") or e.get("romaji") or "",band))

    for i,band in enumerate(JLPT_LEVELS):
        pool=JLPT_BY_LEVEL.get(band,[])
        if not pool: continue
        e=random.choice(pool); distract=[x["meaning"] for x in pool if x["kanji"] != e["kanji"]]; random.shuffle(distract)
        out.append(_choice_question(f"kanji-{i}","Kanji",e["kanji"],e["meaning"],distract,e.get("kun_yomi") or e.get("on_yomi") or "",band))

    # 12 grammar questions: source-backed where those uploaded books contain
    # grammar exercises; N3 uses the app's grammar dictionary because its
    # uploaded N3 book is reading-focused.
    takes={"N5":2,"N4":2,"N3":2,"N2":3,"N1":3}
    gi=0
    for band,take in takes.items():
        if band == "N3":
            pool=[g for g in GRAMMAR_DATA if g.get("level")=="N3" and g.get("meaning")]
            for g in random.sample(pool,min(take,len(pool))):
                distract=[x["meaning"] for x in pool if x["id"]!=g["id"] and x.get("meaning")!=g.get("meaning")]
                random.shuffle(distract)
                out.append(_choice_question(f"grammar-{gi}","Grammar",g["pattern"],g["meaning"],distract,g.get("example_ja", ""),band));gi+=1
            continue
        pool=[q for q in JLPT_EXAM_QUESTIONS.get(band,[]) if "Grammar" in q.get("category","")]
        for q in random.sample(pool,min(take,len(pool))):
            out.append({"id":f"grammar-{gi}","type":"Grammar","prompt":q.get("prompt",""),"sub":"",
                        "options":q.get("options",[]),"answer_index":q.get("answer_index",0),"band":band});gi+=1
    random.shuffle(out)
    return out


@app.route("/placement")
def placement_page():
    return render_template("placement.html")


@app.route("/api/placement_test")
def api_placement_test():
    return jsonify({"questions": _placement_questions()})


def _placement_recommend(score, breakdown=None):
    breakdown = breakdown if isinstance(breakdown, dict) else {}
    pct={}
    for lvl in JLPT_LEVELS:
        row=breakdown.get(lvl) if isinstance(breakdown.get(lvl),dict) else {}
        try:
            total=max(0,int(row.get("total",0))); right=max(0,int(row.get("right",0)))
        except (TypeError,ValueError): total=right=0
        pct[lvl]=(100*right/total) if total else None

    # Sequential band checks prevent one lucky advanced answer from skipping
    # weak fundamentals, while a strong learner can still jump ahead.
    if score < 25 or (pct["N5"] is not None and pct["N5"] < 45): return "hiragana-1", "Foundation", "N5"
    if score < 45 or (pct["N5"] is not None and pct["N5"] < 70): return "greetings-intro", "Beginner", "N5"
    if score < 60 or (pct["N4"] is not None and pct["N4"] < 55): return "particles-wa-ga-o", "Grammar foundations", "N4"
    if score < 72 or (pct["N3"] is not None and pct["N3"] < 55): return "n5-kanji-checkpoint", "Intermediate bridge", "N3"
    if score < 84 or (pct["N2"] is not None and pct["N2"] < 55):
        return ("n3-grammar-01", "Upper intermediate", "N3") if "n3-grammar-01" in ROADMAP_CHAPTERS else ("grand-review","Intermediate","N3")
    if score < 94 or (pct["N1"] is not None and pct["N1"] < 50):
        return ("n2-grammar-01", "Advanced", "N2") if "n2-grammar-01" in ROADMAP_CHAPTERS else ("grand-review","Advanced","N2")
    if "n1-grammar-01" in ROADMAP_CHAPTERS: return "n1-grammar-01", "N1 mastery", "N1"
    return "grand-review", "Advanced", "N1"


@app.route("/api/placement/save", methods=["POST"])
def api_placement_save():
    payload = request.get_json(silent=True) or {}
    try: score = max(0, min(100, int(payload.get("score",0))))
    except (TypeError, ValueError): score = 0
    breakdown = payload.get("breakdown") if isinstance(payload.get("breakdown"), dict) else {}
    chapter_id, label, approx = _placement_recommend(score, breakdown)
    _save_roadmap_start(chapter_id, current_user())
    result = {"score":score,"breakdown":breakdown,"chapter_id":chapter_id,"recommendation":label,"approx_level":approx,
              "chapter_title":ROADMAP_CHAPTERS.get(chapter_id,{}).get("title",label)}
    _learner.save_placement(DATA_DIR, current_user(), result)
    return jsonify({"ok":True, **result, "url":url_for("roadmap_chapter", chapter_id=chapter_id)})


# --------------------------------------------------------------- grammar --

@app.route("/grammar")
def grammar_page():
    counts = {lvl: sum(1 for g in GRAMMAR_DATA if g.get("level") == lvl) for lvl in JLPT_LEVELS}
    return render_template("grammar.html", grammar=GRAMMAR_DATA, levels=JLPT_LEVELS, counts=counts)


@app.route("/grammar/<grammar_id>")
def grammar_detail(grammar_id):
    entry = next((g for g in GRAMMAR_DATA if g.get("id") == grammar_id), None)
    if not entry: return "Grammar pattern not found", 404
    return render_template("grammar_detail.html", entry=entry)


@app.route("/api/grammar_quiz")
def api_grammar_quiz():
    level = (request.args.get("level") or "all").upper()
    pool = GRAMMAR_DATA if level == "ALL" else [g for g in GRAMMAR_DATA if g.get("level") == level]
    if len(pool) < 4: pool = GRAMMAR_DATA
    try: count = max(5, min(int(request.args.get("count",10)), 30))
    except (TypeError, ValueError): count = 10
    chosen = random.sample(pool, min(count, len(pool)))
    qs=[]
    for g in chosen:
        distract=[x["meaning"] for x in pool if x["id"] != g["id"] and x.get("meaning") != g.get("meaning")]
        random.shuffle(distract)
        q=_choice_question(g["id"],"Grammar",g["pattern"],g["meaning"],distract,g.get("example_ja",""),g.get("level",""))
        qs.append(q)
    return jsonify({"questions":qs})


# ------------------------------------------------------------- speaking --

def _speaking_items(level="all"):
    rows=[]
    for conv in CONVERSATIONS_DATA:
        if level != "all" and conv.get("level") != level: continue
        for i,line in enumerate(conv.get("lines",[])):
            text=line.get("kanji") or line.get("hiragana")
            if text:
                rows.append({"id":f"conv-{conv['id']}-{i}","level":conv.get("level","easy"),"jp":text,
                             "reading":line.get("hiragana",""),"romaji":line.get("romaji",""),
                             "english":line.get("english",""),"source":conv.get("title_en","Conversation")})
    for story in STORIES_DATA:
        if level != "all" and story.get("level") != level: continue
        for i,line in enumerate(story.get("sentences",[])[:4]):
            text=line.get("kanji") or line.get("hiragana")
            if text:
                rows.append({"id":f"story-{story['id']}-{i}","level":story.get("level","easy"),"jp":text,
                             "reading":line.get("hiragana",""),"romaji":line.get("romaji",""),
                             "english":line.get("english",""),"source":story.get("title_en","Story")})
    return rows


@app.route("/speaking")
def speaking_page():
    return render_template("speaking.html")


@app.route("/api/speaking_items")
def api_speaking_items():
    level=(request.args.get("level") or "all").lower()
    if level not in {"all","easy","medium","hard"}: level="all"
    pool=_speaking_items(level)
    random.shuffle(pool)
    try: count=max(5,min(int(request.args.get("count",15)),40))
    except (TypeError,ValueError): count=15
    return jsonify({"items":pool[:count]})


# ----------------------------------------------------------- JLPT mocks --

def _mock_questions(level, limit=50):
    pool=list(JLPT_EXAM_QUESTIONS.get(level,[]))
    bycat={}
    for q in pool: bycat.setdefault(q.get("category","Practice"),[]).append(q)
    for qs in bycat.values(): random.shuffle(qs)
    chosen=[]
    cats=list(bycat)
    while cats and len(chosen)<limit:
        next_cats=[]
        for c in cats:
            if bycat[c] and len(chosen)<limit:
                chosen.append(bycat[c].pop())
            if bycat[c]: next_cats.append(c)
        cats=next_cats
    random.shuffle(chosen)
    return chosen


@app.route("/jlpt/<level>/mock")
def jlpt_mock(level):
    level=level.upper()
    if level not in JLPT_LEVELS or not JLPT_EXAM_QUESTIONS.get(level): return "Mock unavailable",404
    count=min(50,len(JLPT_EXAM_QUESTIONS[level]))
    return render_template("jlpt_mock.html",level=level,count=count,minutes=max(20,round(count*1.25)))


@app.route("/api/jlpt_mock")
def api_jlpt_mock():
    level=(request.args.get("level") or "").upper()
    if level not in JLPT_LEVELS or not JLPT_EXAM_QUESTIONS.get(level): return jsonify({"error":"mock unavailable"}),400
    chosen=_mock_questions(level,min(50,len(JLPT_EXAM_QUESTIONS[level])))
    return jsonify({"level":level,"questions":[{
        "id":q.get("id",""),"category":q.get("category","Practice"),"passage":q.get("passage",""),
        "prompt":q.get("prompt",""),"options":q.get("options",[]),"answer_index":q.get("answer_index",0),
        "explanation":q.get("explanation",""),"explanation_blocks":q.get("explanation_blocks",[]),
    } for q in chosen]})


@app.route("/api/jlpt_mock/save", methods=["POST"])
def api_jlpt_mock_save():
    payload=request.get_json(silent=True) or {}
    level=(payload.get("level") or "").upper()
    try:
        score=int(payload.get("score",0)); total=max(1,int(payload.get("total",1)))
    except (TypeError,ValueError): return jsonify({"error":"invalid score"}),400
    result={"level":level,"score":score,"total":total,"percent":round(100*score/total),
            "categories":payload.get("categories",{})}
    _learner.save_mock(DATA_DIR,current_user(),result)
    return jsonify({"ok":True,"summary":_learner_summary(current_user())})


# --------------------------------------------------------------- games --

@app.route("/games")
def games_page():
    return render_template("games.html")


@app.route("/api/games/deck")
def api_games_deck():
    game=(request.args.get("game") or "match").lower()
    difficulty=(request.args.get("difficulty") or "easy").lower()
    if difficulty not in {"easy","medium","hard"}: difficulty="easy"
    vocab=[w for w in VOCAB_POOL if w.get("difficulty")==difficulty and w.get("word") and w.get("meaning")]
    if len(vocab)<12: vocab=VOCAB_POOL
    random.shuffle(vocab)
    if game=="match":
        return jsonify({"game":game,"items":[{"id":i,"jp":w["word"],"en":w["meaning"],"reading":w.get("reading","")} for i,w in enumerate(vocab[:8])]})
    if game=="audio":
        items=[]
        for i,w in enumerate(vocab[:10]):
            wrong=[x["meaning"] for x in vocab[10:] if x["meaning"]!=w["meaning"]][:3]
            opts=wrong+[w["meaning"]]; random.shuffle(opts)
            items.append({"id":i,"jp":w["word"],"reading":w.get("reading","") or w.get("romaji",""),"correct":w["meaning"],"options":opts})
        return jsonify({"game":game,"items":items})
    if game=="kana":
        base=HIRAGANA_DATA[:46]+KATAKANA_DATA[:46]; random.shuffle(base)
        items=[]
        for i,e in enumerate(base[:20]):
            wrong=[x["romaji"] for x in base if x["char"]!=e["char"] and x["romaji"]!=e["romaji"]][:3]
            opts=wrong+[e["romaji"]]; random.shuffle(opts)
            items.append({"id":i,"jp":e["char"],"correct":e["romaji"],"options":opts})
        return jsonify({"game":game,"items":items})
    if game=="verbs":
        pool=[v for v in VERBS_DATA if v.get("difficulty")==difficulty] or VERBS_DATA
        random.shuffle(pool); items=[]
        forms=[("masu","polite present"),("te","て-form"),("past","past"),("nai","negative")]
        for i,v in enumerate(pool[:12]):
            fk,label=random.choice(forms); correct=(v.get("forms",{}).get(fk) or {}).get("kanji")
            if not correct: continue
            wrong=[]
            for x in pool[12:]:
                val=(x.get("forms",{}).get(fk) or {}).get("kanji")
                if val and val!=correct and val not in wrong: wrong.append(val)
                if len(wrong)==3: break
            opts=wrong+[correct]; random.shuffle(opts)
            items.append({"id":i,"jp":v["word"],"prompt":f"Choose the {label} form", "correct":correct,"options":opts})
        return jsonify({"game":game,"items":items})
    if game=="sentence":
        sents=[s for s in PRACTICE_SENTENCES if s.get("word") and s.get("sentence_kanji")]
        random.shuffle(sents); items=[]
        words=[s["word"] for s in sents]
        for i,s in enumerate(sents[:12]):
            prompt=s["sentence_kanji"].replace(s["word"],"＿＿＿",1)
            wrong=[w for w in words if w!=s["word"]][:3]; opts=wrong+[s["word"]]; random.shuffle(opts)
            items.append({"id":i,"jp":prompt,"sub":s.get("sentence_en",""),"correct":s["word"],"options":opts})
        return jsonify({"game":game,"items":items})
    return jsonify({"error":"invalid game"}),400



@app.route("/sw.js")
def service_worker():
    # Served from the root (not /static/sw.js) so its default scope is
    # "/" and it can control every page, not just /static/.
    resp = send_from_directory(app.static_folder, "sw.js")
    resp.headers["Content-Type"] = "application/javascript"
    resp.headers["Service-Worker-Allowed"] = "/"
    return resp


@app.route("/streak")
@app.route("/dashboard")
def streak_page():
    user = current_user()
    return render_template("streak.html", progress=_progress_summary(user), learner=_learner_summary(user))


@app.route("/api/kanji_pool")
def api_kanji_pool():
    """Lightweight list for the kanji-tracing picker. Starts with the
    main Kanji section's 408 (which have a real stroke count), then adds
    every JLPT-only kanji that isn't already among them, so Writing
    Practice can trace any of the 1,000+ JLPT kanji too."""
    seen_chars = {e["kanji"] for e in KANJI_DATA}
    pool = [
        {"id": e["id"], "kanji": e["kanji"], "meaning": e["meaning"], "strokes": e["strokes"]}
        for e in KANJI_DATA
    ]
    for i, e in enumerate(JLPT_KANJI):
        if e["kanji"] in seen_chars:
            continue
        seen_chars.add(e["kanji"])
        pool.append({
            "id": 100000 + i,
            "kanji": e["kanji"],
            "meaning": f"{e['meaning']} (JLPT {e['level']})",
            "strokes": None,
        })
    return jsonify(pool)


@app.route("/practice")
def practice_start():
    return render_template("practice.html")


def pool_for_difficulty(level):
    if level == "mixed" or not level:
        return list(PRACTICE_POOL)
    return [w for w in PRACTICE_POOL if w["difficulty"] == level]


@app.route("/api/practice/new_session", methods=["POST"])
def new_practice_session():
    """Pick N words for a new practice round, filtered by difficulty.
    Prefer words that have a curated sentence so quizzes are richest,
    then fill with other words from the same difficulty pool."""
    payload = request.get_json(silent=True) or {}
    level = payload.get("difficulty", "mixed")
    count = int(payload.get("count", 10))
    count = max(5, min(count, 40))

    base_pool = pool_for_difficulty(level)
    if not base_pool:
        base_pool = list(PRACTICE_POOL)

    curated_ids = set(SENTENCE_BY_KANJI_ID.keys())
    curated_words = [w for w in base_pool if w["kanji_id"] in curated_ids]
    random.shuffle(curated_words)
    pool = curated_words[:count]

    if len(pool) < count:
        remaining = [w for w in base_pool if w not in pool]
        random.shuffle(remaining)
        pool += remaining[: count - len(pool)]

    session["practice_words"] = [w["kanji_id"] for w in pool]
    session["practice_score"] = 0
    session["practice_difficulty"] = level

    return jsonify({
        "words": pool,
        "total": len(pool),
        "difficulty": level,
    })


@app.route("/api/practice/quiz/<int:kanji_id>")
def practice_quiz(kanji_id):
    """Return one clearly-worded multiple-choice question about this kanji.

    Every question type is built straight from the dataset, so the
    question and its answer are always consistent:
      - meaning:  What does X mean?
      - kanji:    Which kanji means "Y"?
      - reading:  How is X read?
      - sentence: fill the blank (only for words with a curated
                  sentence, so the sentence always reads naturally)
    """
    word_entry = PRACTICE_BY_ID.get(kanji_id)
    if not word_entry:
        return jsonify({"error": "not found"}), 404

    requested = (request.args.get("mode") or "mixed").lower()
    sentence = SENTENCE_BY_KANJI_ID.get(kanji_id)

    if requested == "kanji":
        qtype = random.choice(["meaning", "kanji", "reading"])
    elif requested == "sentence" and sentence:
        qtype = "sentence"
    else:
        choices = ["meaning", "kanji", "reading"]
        if sentence:
            choices.append("sentence")
        qtype = random.choice(choices)

    # reading questions need a kana reading to test
    if qtype == "reading" and not first_reading(word_entry):
        qtype = "meaning"

    pool = [w for w in PRACTICE_POOL if w["kanji_id"] != kanji_id]
    same_tier = [w for w in pool if w["difficulty"] == word_entry["difficulty"]]
    random.shuffle(same_tier)
    random.shuffle(pool)
    ordered = same_tier + [w for w in pool if w not in same_tier]

    if qtype == "meaning":
        question = f"What does {word_entry['kanji']} mean?"
        hint = "Pick the English meaning."
        correct = word_entry["meaning"]
        distractors = unique_take([w["meaning"] for w in ordered], correct, 5)
        prompt_big = word_entry["kanji"]

    elif qtype == "kanji":
        question = f"Which kanji means \u201c{word_entry['meaning']}\u201d?"
        hint = "Pick the matching character."
        correct = word_entry["kanji"]
        distractors = unique_take([w["kanji"] for w in ordered], correct, 5)
        prompt_big = ""

    elif qtype == "reading":
        question = f"How is {word_entry['kanji']} read?"
        hint = "Pick the correct kana reading."
        correct = first_reading(word_entry)
        cands = [first_reading(w) for w in ordered]
        distractors = unique_take([c for c in cands if c], correct, 5)
        prompt_big = word_entry["kanji"]

    else:  # sentence
        target = sentence["word"]
        question = "Which word completes this sentence?"
        hint = sentence["sentence_en"]
        correct = target
        distractors = unique_take([w["word"] for w in ordered], correct, 5)
        prompt_big = sentence["sentence_kanji"].replace(target, "＿＿＿", 1)

    options = distractors + [correct]
    random.shuffle(options)

    return jsonify({
        "kanji_id": kanji_id,
        "type": qtype,
        "question": question,
        "hint": hint,
        "prompt_big": prompt_big,
        "options": options,
        "correct_word": correct,
        "difficulty": word_entry["difficulty"],
    })


@app.route("/api/practice/check", methods=["POST"])
def practice_check():
    """Check the answer and ALWAYS return the full explanation for the
    correct word — whether the person got it right or made a mistake."""
    payload = request.get_json(force=True)
    kanji_id = payload.get("kanji_id")
    answer = payload.get("answer", "")
    correct_word = payload.get("correct_word", "")

    is_correct = answer.strip() == correct_word.strip()
    result = {"correct": is_correct, "your_answer": answer}

    word_entry = PRACTICE_BY_ID.get(kanji_id)
    if word_entry:
        result["explanation"] = build_explanation(word_entry)

    if is_correct:
        session["practice_score"] = session.get("practice_score", 0) + 1

    return jsonify(result)


@app.route("/api/practice/score")
def practice_score():
    return jsonify({
        "score": session.get("practice_score", 0),
        "total": len(session.get("practice_words", [])),
    })


if __name__ == "__main__":
    # Debug mode enables Werkzeug's interactive debugger, which can run
    # arbitrary code from an error page - fine for local development,
    # not something to ship on by default now that real accounts exist.
    # Opt in explicitly with: FLASK_DEBUG=1 python app.py
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
