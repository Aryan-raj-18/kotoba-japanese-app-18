#!/usr/bin/env python3
"""Build data/frequency_words.json from the supplied Lingo Mastery PDF.

The PDF presents its vocabulary as a frequency-ranked list.  This importer
keeps only compact learning metadata needed by Kotoba (rank, written form,
reading, romanization, part of speech, meaning, source example) and assigns
an app difficulty/category.  App-side merging then removes surface-form
repetitions against Kotoba's existing vocabulary.

Usage:
    python build_frequency_words.py /path/to/2000-most-common-japanese.pdf
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "data" / "frequency_words.json"
JLPT = ROOT / "data" / "jlpt_kanji.json"

ROMA_MAP = {
    "kya":"きゃ","kyu":"きゅ","kyo":"きょ","gya":"ぎゃ","gyu":"ぎゅ","gyo":"ぎょ",
    "sha":"しゃ","shu":"しゅ","sho":"しょ","sya":"しゃ","syu":"しゅ","syo":"しょ",
    "jya":"じゃ","jyu":"じゅ","jyo":"じょ","cha":"ちゃ","chu":"ちゅ","cho":"ちょ",
    "cya":"ちゃ","cyu":"ちゅ","cyo":"ちょ","nya":"にゃ","nyu":"にゅ","nyo":"にょ",
    "hya":"ひゃ","hyu":"ひゅ","hyo":"ひょ","bya":"びゃ","byu":"びゅ","byo":"びょ",
    "pya":"ぴゃ","pyu":"ぴゅ","pyo":"ぴょ","mya":"みゃ","myu":"みゅ","myo":"みょ",
    "rya":"りゃ","ryu":"りゅ","ryo":"りょ",
    "fa":"ふぁ","fi":"ふぃ","fe":"ふぇ","fo":"ふぉ","she":"しぇ","je":"じぇ","che":"ちぇ",
    "ti":"てぃ","tu":"とぅ","di":"でぃ","du":"どぅ","wi":"うぃ","we":"うぇ","wo":"を",
    "va":"ゔぁ","vi":"ゔぃ","vu":"ゔ","ve":"ゔぇ","vo":"ゔぉ",
    "shi":"し","chi":"ち","tsu":"つ","fu":"ふ","ji":"じ","dji":"ぢ","dzu":"づ",
    "ka":"か","ki":"き","ku":"く","ke":"け","ko":"こ","ga":"が","gi":"ぎ","gu":"ぐ","ge":"げ","go":"ご",
    "sa":"さ","si":"し","su":"す","se":"せ","so":"そ","za":"ざ","zi":"じ","zu":"ず","ze":"ぜ","zo":"ぞ",
    "ta":"た","te":"て","to":"と","da":"だ","de":"で","do":"ど",
    "na":"な","ni":"に","nu":"ぬ","ne":"ね","no":"の",
    "ha":"は","hi":"ひ","he":"へ","ho":"ほ","ba":"ば","bi":"び","bu":"ぶ","be":"べ","bo":"ぼ",
    "pa":"ぱ","pi":"ぴ","pu":"ぷ","pe":"ぺ","po":"ぽ",
    "ma":"ま","mi":"み","mu":"む","me":"め","mo":"も","ya":"や","yu":"ゆ","yo":"よ",
    "ra":"ら","ri":"り","ru":"る","re":"れ","ro":"ろ","wa":"わ",
    "a":"あ","i":"い","u":"う","e":"え","o":"お",
}
ROMA_KEYS = sorted(ROMA_MAP, key=len, reverse=True)


def _hira(c: str) -> str:
    o = ord(c)
    return chr(o - 0x60) if 0x30A1 <= o <= 0x30F6 else c


def kana_to_hira(s: str) -> str:
    return "".join(_hira(c) for c in s)


def clean_romaji(s: str) -> str:
    s = s.strip().lower().replace("’", "'")
    s = re.split(r"[,;/]", s)[0].strip()
    s = re.sub(r"\([^)]*\)", "", s).strip()
    s = s.translate(str.maketrans({"ō":"oo","ū":"uu","ā":"aa","ē":"ee","ī":"ii"}))
    return re.sub(r"[^a-z'\- ]+", "", s).strip()


def translit_core(s: str) -> str:
    s = s.lower().replace("-", "").replace(" ", "")
    out, i = [], 0
    while i < len(s):
        if s[i] == "'":
            i += 1; continue
        if i + 1 < len(s) and s[i] == s[i + 1] and s[i] not in "aeioun":
            out.append("っ"); i += 1; continue
        if s[i] == "n":
            if i + 1 == len(s): out.append("ん"); i += 1; continue
            if s[i + 1] == "'": out.append("ん"); i += 2; continue
            if s[i + 1] not in "aeiouy": out.append("ん"); i += 1; continue
            if s[i + 1] == "n": out.append("ん"); i += 1; continue
        matched = False
        for k in ROMA_KEYS:
            if s.startswith(k, i):
                out.append(ROMA_MAP[k]); i += len(k); matched = True; break
        if not matched:
            out.append(s[i]); i += 1
    return "".join(out)


def romaji_candidates(romaji: str):
    s = clean_romaji(romaji)
    if not s: return []
    variants = []
    # The book writes long /o:/ and /e:/ as oo / ee. In kana these are
    # often おう / えい, but native words can use おお / ええ. Keep both
    # and use the source furigana line to choose whenever possible.
    for v in (s.replace("oo", "ou").replace("ee", "ei"),
              s.replace("oo", "ou"), s.replace("ee", "ei"), s):
        h = translit_core(v)
        if h and h not in variants:
            variants.append(h)
        # Hepburn writes both ず/づ as zu and じ/ぢ as ji; source furigana
        # disambiguates these, so offer the alternates as candidates.
        for a in (h.replace("ず", "づ"), h.replace("じ", "ぢ"), h.replace("ず", "づ").replace("じ", "ぢ")):
            if a and a not in variants:
                variants.append(a)
    return variants


def parse_heading(line: str):
    m = re.match(r"^\s*(\d{1,4})\s*-\s*(.+?)\s*$", line)
    if not m or "[" not in m.group(2):
        return None
    rank, rest = int(m.group(1)), m.group(2)
    pre, after = rest.split("[", 1)
    if "]" in after:
        pos, meaning = after.split("]", 1)
    else:  # one source line is missing its closing bracket
        parts = after.strip().split(None, 1)
        pos, meaning = (parts + [""])[:2]
    pre, pos, meaning = pre.strip(), pos.strip(), meaning.strip()
    if "/" in pre:
        word, romaji = pre.split("/", 1)
    else:  # two source lines omit the slash between Japanese and romaji
        sm = re.match(r"^(.*?)([A-Za-z].*)$", pre)
        if not sm: return None
        word, romaji = sm.group(1), sm.group(2)
    return rank, word.strip(), romaji.strip(), pos, meaning


def trailing_kana(word: str) -> str:
    m = re.search(r"([\u3040-\u30ffー]+)$", word)
    return kana_to_hira(m.group(1)) if m else ""


def choose_reading(word: str, romaji: str, body_lines) -> str:
    # Pure kana words already carry their own reading.
    if word and all(("\u3040" <= c <= "\u30ff") or c in "ー・" for c in word):
        return kana_to_hira(word)
    body = "".join(re.sub(r"\s+", "", x) for x in body_lines)
    suffix = trailing_kana(word)
    cands = romaji_candidates(romaji)
    # Particles are pronounced differently in romanization but written は/へ/を.
    if suffix in {"は", "へ", "を"}:
        particle_map = {"は":"わ", "へ":"え", "を":"お"}
        for c in list(cands):
            if c.endswith(particle_map[suffix]):
                cands.insert(0, c[:-1] + suffix)
    for c in cands:
        if c in body:
            return c
        # Okurigana is printed in the sentence, not repeated in the furigana
        # line above it (e.g. 多い -> furigana only おお). Match the stem too.
        if suffix and c.endswith(suffix) and c[:-len(suffix)] in body:
            return c
    return cands[0] if cands else ""


def category_for(pos: str, meaning: str) -> str:
    m = meaning.lower()
    ws = set(re.findall(r"[a-z]+", m))
    if pos in {"p", "p. case", "p. conj", "p. dic", "aux", "conj", "cp"}:
        return "Grammar & Connectors"
    if pos == "interj": return "Greetings & Phrases"
    if pos == "v": return "Actions & Verbs"
    if pos in {"i-adj", "na-adj", "adn"}: return "Descriptions & Qualities"
    if pos == "num": return "Numbers & Counting"
    rules = [
        ("Time & Calendar", {"time","day","week","month","year","morning","afternoon","evening","night","today","tomorrow","yesterday","hour","minute","season"}),
        ("Family & People", {"mother","father","parent","brother","sister","son","daughter","husband","wife","child","children","friend","person","people","man","woman","boy","girl","baby","family"}),
        ("Body & Health", {"body","head","face","eye","ear","mouth","hand","foot","leg","heart","health","hospital","doctor","illness","disease","pain","medicine"}),
        ("Food & Drink", {"food","rice","meal","breakfast","lunch","dinner","tea","coffee","water","drink","meat","fish","vegetable","fruit","restaurant","cooking","cuisine"}),
        ("Transportation", {"train","bus","taxi","car","bicycle","station","subway","airplane","plane","ship","transportation"}),
        ("Travel", {"travel","trip","hotel","passport","tour","airport","luggage","ticket","sightseeing"}),
        ("Money & Shopping", {"money","price","cost","shop","store","shopping","buy","sell","customer","yen","payment"}),
        ("School & Learning", {"school","teacher","student","study","class","lesson","university","college","education","exam","test","question","answer"}),
        ("Work & Jobs", {"work","job","company","office","business","employee","staff","manager","career","salary"}),
        ("Technology", {"computer","internet","email","software","image","phone","telephone","data","system","file","network","screen"}),
        ("Nature & Weather", {"mountain","river","sea","ocean","tree","flower","rain","snow","wind","sky","sun","moon","weather","island","lake","nature"}),
        ("Animals", {"animal","dog","cat","bird","fish","horse","cow","insect"}),
        ("Directions & Position", {"left","right","north","south","east","west","inside","outside","front","back","direction","place","location"}),
        ("Sports & Fitness", {"sport","soccer","baseball","tennis","exercise","game","match","team"}),
        ("Hobbies & Music", {"music","song","movie","film","book","reading","piano","guitar","hobby","art"}),
        ("Emotions & Feelings", {"feeling","happy","sad","worry","anxiety","love","fear","angry","surprise","hope"}),
        ("Society & Ideas", {"society","history","culture","law","government","world","country","information","opinion","idea","reason","result","problem","fact","truth"}),
    ]
    for cat, kws in rules:
        if ws & kws:
            return cat
    if pos == "adv": return "Grammar & Connectors"
    if pos == "pron": return "Grammar & Connectors"
    return "Everyday Objects & Ideas"


def difficulty_for(rank: int, word: str, pos: str, jlpt_map) -> str:
    rank_score = (rank - 1) / 1999.0
    ks = [jlpt_map.get(ch, 0.65) for ch in word if "\u4e00" <= ch <= "\u9fff"]
    kanji_score = max(ks) if ks else 0.15
    n = len(re.sub(r"[\s・()（）]", "", word))
    length_score = min(1.0, max(0.0, (n - 2) / 5.0))
    grammar_bonus = -0.10 if pos in {"p","p. case","p. conj","p. dic","aux","conj","pron","interj"} and rank < 600 else 0.0
    score = 0.55 * rank_score + 0.35 * kanji_score + 0.10 * length_score + grammar_bonus
    if score < 0.33: return "easy"
    if score < 0.58: return "medium"
    return "hard"


def source_example(body):
    ja_candidates = []
    for i, line in enumerate(body):
        s = line.strip()
        if re.search(r"[\u3040-\u30ff\u4e00-\u9fff]", s) and re.search(r"[。！？!?]$", s):
            ja_candidates.append((i, s))
    if not ja_candidates:
        return "", ""
    i, ja = max(ja_candidates, key=lambda x: len(x[1]))
    acc = []
    for line in body[i + 1:]:
        s = line.strip()
        if not s:
            if acc: break
            continue
        if s.startswith("*"): break
        if re.search(r"[\u3040-\u30ff\u4e00-\u9fff]", s):
            if acc: break
            continue
        if re.search(r"[A-Za-z]", s):
            acc.append(s)
            if re.search(r"[.!?][\"”']?$", s): break
    return ja, " ".join(acc)


def main(pdf: Path) -> int:
    if not pdf.exists():
        print(f"PDF not found: {pdf}", file=sys.stderr); return 2
    with tempfile.TemporaryDirectory() as td:
        txt = Path(td) / "source.txt"
        subprocess.run(["pdftotext", "-layout", str(pdf), str(txt)], check=True)
        lines = txt.read_text(encoding="utf-8", errors="replace").replace("\x0c", "\n").splitlines()
    start = next(i for i, line in enumerate(lines) if "THE 2000 MOST COMMON WORDS IN" in line)
    heads = []
    for i, line in enumerate(lines[start:], start=start):
        h = parse_heading(line)
        if h and 1 <= h[0] <= 2000:
            heads.append((i, *h))
    if len(heads) != 1999:
        raise RuntimeError(f"Expected 1999 extractable numbered entries from this source, got {len(heads)}")

    level_values = {"N5":0.10,"N4":0.25,"N3":0.50,"N2":0.75,"N1":0.95}
    jlpt_map = {}
    for e in json.loads(JLPT.read_text(encoding="utf-8")):
        jlpt_map[e["kanji"]] = max(jlpt_map.get(e["kanji"], 0), level_values.get(e["level"], 0.65))

    entries = []
    for idx, head in enumerate(heads):
        line_i, rank, word, romaji, pos, meaning = head
        end = heads[idx + 1][0] if idx + 1 < len(heads) else len(lines)
        body = lines[line_i + 1:end]
        reading = choose_reading(word, romaji, body)
        ex_ja, ex_en = source_example(body)
        entries.append({
            "rank": rank,
            "word": unicodedata.normalize("NFKC", word),
            "reading": reading,
            "romaji": clean_romaji(romaji),
            "part_of_speech": pos,
            "meaning": meaning,
            "category": category_for(pos, meaning),
            "difficulty": difficulty_for(rank, word, pos, jlpt_map),
            "example_ja": ex_ja,
            "example_en": ex_en,
        })

    # The printed source has no numbered 1772 entry and repeats the exact
    # written form いい at two ranks. We keep source numbering intact here;
    # app-side canonical merging prevents duplicate cards/rows.
    OUT.write_text(json.dumps(entries, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    c = Counter(e["difficulty"] for e in entries)
    print(f"wrote {len(entries)} entries -> {OUT}")
    print("difficulty:", dict(c))
    print("missing ranks:", [n for n in range(1, 2001) if n not in {e['rank'] for e in entries}])
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: build_frequency_words.py /path/to/source.pdf", file=sys.stderr)
        raise SystemExit(2)
    raise SystemExit(main(Path(sys.argv[1])))
