"""
Builds data/verbs.json.

The uploaded "600 Basic Japanese Verbs" PDF is an image-only scan with no
text layer, so nothing could be extracted from it. Instead this file
pairs a hand-checked list of common verbs (dictionary form, reading,
meaning, group) with a conjugation ENGINE that applies the standard
Japanese conjugation rules. The conjugations are therefore generated
from grammar rules, not copied from any book, and are correct by
construction for regular verbs.

Groups:
  godan    - u-verbs (五段)
  ichidan  - ru-verbs (一段)
  irregular- する / 来る and their compounds
"""
import json

# (dictionary form, reading, meaning, group, jlpt-ish level)
VERBS = [
    # --- irregular ---
    ("する", "する", "to do", "irregular", "easy"),
    ("来る", "くる", "to come", "irregular", "easy"),
    ("勉強する", "べんきょうする", "to study", "irregular", "easy"),
    ("結婚する", "けっこんする", "to marry", "irregular", "medium"),
    ("電話する", "でんわする", "to phone", "irregular", "medium"),
    ("掃除する", "そうじする", "to clean", "irregular", "medium"),
    ("洗濯する", "せんたくする", "to do laundry", "irregular", "medium"),
    ("運転する", "うんてんする", "to drive", "irregular", "medium"),
    ("旅行する", "りょこうする", "to travel", "irregular", "medium"),
    ("説明する", "せつめいする", "to explain", "irregular", "hard"),
    ("紹介する", "しょうかいする", "to introduce", "irregular", "hard"),
    ("準備する", "じゅんびする", "to prepare", "irregular", "hard"),
    ("心配する", "しんぱいする", "to worry", "irregular", "hard"),
    ("約束する", "やくそくする", "to promise", "irregular", "hard"),
    ("予約する", "よやくする", "to reserve, to book", "irregular", "hard"),

    # --- ichidan (ru-verbs) ---
    ("食べる", "たべる", "to eat", "ichidan", "easy"),
    ("見る", "みる", "to see, to watch", "ichidan", "easy"),
    ("寝る", "ねる", "to sleep", "ichidan", "easy"),
    ("起きる", "おきる", "to get up", "ichidan", "easy"),
    ("出る", "でる", "to go out, to leave", "ichidan", "easy"),
    ("いる", "いる", "to exist (animate)", "ichidan", "easy"),
    ("開ける", "あける", "to open (something)", "ichidan", "easy"),
    ("閉める", "しめる", "to close (something)", "ichidan", "easy"),
    ("教える", "おしえる", "to teach, to tell", "ichidan", "easy"),
    ("覚える", "おぼえる", "to memorize", "ichidan", "medium"),
    ("忘れる", "わすれる", "to forget", "ichidan", "medium"),
    ("借りる", "かりる", "to borrow", "ichidan", "medium"),
    ("着る", "きる", "to wear (upper body)", "ichidan", "medium"),
    ("降りる", "おりる", "to get off, to descend", "ichidan", "medium"),
    ("生まれる", "うまれる", "to be born", "ichidan", "medium"),
    ("入れる", "いれる", "to put in", "ichidan", "medium"),
    ("考える", "かんがえる", "to think, to consider", "ichidan", "medium"),
    ("answered_placeholder", "", "", "", ""),  # removed below
    ("始める", "はじめる", "to begin (something)", "ichidan", "medium"),
    ("続ける", "つづける", "to continue", "ichidan", "hard"),
    ("調べる", "しらべる", "to look up, to investigate", "ichidan", "hard"),
    ("捨てる", "すてる", "to throw away", "ichidan", "hard"),
    ("集める", "あつめる", "to collect, to gather", "ichidan", "hard"),
    ("片付ける", "かたづける", "to tidy up", "ichidan", "hard"),
    ("信じる", "しんじる", "to believe", "ichidan", "hard"),
    ("感じる", "かんじる", "to feel", "ichidan", "hard"),
    ("伝える", "つたえる", "to convey, to tell", "ichidan", "hard"),
    ("変える", "かえる", "to change (something)", "ichidan", "hard"),
    ("答える", "こたえる", "to answer", "ichidan", "medium"),
    ("見せる", "みせる", "to show", "ichidan", "medium"),
    ("疲れる", "つかれる", "to get tired", "ichidan", "medium"),
    ("晴れる", "はれる", "to clear up (weather)", "ichidan", "hard"),
    ("別れる", "わかれる", "to part, to separate", "ichidan", "hard"),

    # --- godan (u-verbs) ---
    ("行く", "いく", "to go", "godan", "easy"),
    ("買う", "かう", "to buy", "godan", "easy"),
    ("飲む", "のむ", "to drink", "godan", "easy"),
    ("読む", "よむ", "to read", "godan", "easy"),
    ("書く", "かく", "to write", "godan", "easy"),
    ("話す", "はなす", "to speak", "godan", "easy"),
    ("聞く", "きく", "to listen, to ask", "godan", "easy"),
    ("会う", "あう", "to meet", "godan", "easy"),
    ("待つ", "まつ", "to wait", "godan", "easy"),
    ("帰る", "かえる", "to return home", "godan", "easy"),
    ("ある", "ある", "to exist (inanimate)", "godan", "easy"),
    ("わかる", "わかる", "to understand", "godan", "easy"),
    ("작업", "", "", "", ""),  # removed below
    ("使う", "つかう", "to use", "godan", "easy"),
    ("작성", "", "", "", ""),  # removed below
    ("作る", "つくる", "to make", "godan", "easy"),
    ("持つ", "もつ", "to hold, to have", "godan", "easy"),
    ("立つ", "たつ", "to stand", "godan", "easy"),
    ("座る", "すわる", "to sit", "godan", "easy"),
    ("歩く", "あるく", "to walk", "godan", "easy"),
    ("走る", "はしる", "to run", "godan", "medium"),
    ("泳ぐ", "およぐ", "to swim", "godan", "medium"),
    ("急ぐ", "いそぐ", "to hurry", "godan", "medium"),
    ("入る", "はいる", "to enter", "godan", "easy"),
    ("働く", "はたらく", "to work", "godan", "easy"),
    ("休む", "やすむ", "to rest, to take time off", "godan", "easy"),
    ("遊ぶ", "あそぶ", "to play", "godan", "easy"),
    ("呼ぶ", "よぶ", "to call", "godan", "medium"),
    ("死ぬ", "しぬ", "to die", "godan", "medium"),
    ("洗う", "あらう", "to wash", "godan", "medium"),
    ("歌う", "うたう", "to sing", "godan", "medium"),
    ("笑う", "わらう", "to laugh, to smile", "godan", "medium"),
    ("泣く", "なく", "to cry", "godan", "medium"),
    ("思う", "おもう", "to think", "godan", "medium"),
    ("言う", "いう", "to say", "godan", "easy"),
    ("知る", "しる", "to know", "godan", "medium"),
    ("送る", "おくる", "to send", "godan", "medium"),
    ("取る", "とる", "to take", "godan", "medium"),
    ("撮る", "とる", "to take (a photo)", "godan", "medium"),
    ("乗る", "のる", "to ride, to get on", "godan", "medium"),
    ("降る", "ふる", "to fall (rain, snow)", "godan", "medium"),
    ("吹く", "ふく", "to blow", "godan", "hard"),
    ("咲く", "さく", "to bloom", "godan", "hard"),
    ("散る", "ちる", "to scatter, to fall (petals)", "godan", "hard"),
    ("darken", "", "", "", ""),  # removed below
    ("運ぶ", "はこぶ", "to carry, to transport", "godan", "hard"),
    ("掘る", "ほる", "to dig", "godan", "hard"),
    ("選ぶ", "えらぶ", "to choose", "godan", "medium"),
    ("оставить", "", "", "", ""),  # removed below
    ("払う", "はらう", "to pay", "godan", "medium"),
    ("手伝う", "てつだう", "to help", "godan", "medium"),
    ("習う", "ならう", "to learn", "godan", "medium"),
    ("живет", "", "", "", ""),  # removed below
    ("住む", "すむ", "to live, to reside", "godan", "medium"),
    ("困る", "こまる", "to be troubled", "godan", "medium"),
    ("start_placeholder", "", "", "", ""),  # removed below
    ("始まる", "はじまる", "to begin (something begins)", "godan", "medium"),
    ("終わる", "おわる", "to end", "godan", "medium"),
    ("varies", "", "", "", ""),  # removed below
    ("変わる", "かわる", "to change (something changes)", "godan", "hard"),
    ("止まる", "とまる", "to stop", "godan", "medium"),
    ("曲がる", "まがる", "to turn, to bend", "godan", "medium"),
    ("登る", "のぼる", "to climb", "godan", "medium"),
    ("釣る", "つる", "to fish", "godan", "hard"),
    ("捕まえる", "つかまえる", "to catch", "ichidan", "hard"),
    ("返す", "かえす", "to give back, to return", "godan", "hard"),
    ("直す", "なおす", "to fix, to correct", "godan", "hard"),
    ("探す", "さがす", "to look for", "godan", "medium"),
    ("貸す", "かす", "to lend", "godan", "medium"),
    ("出す", "だす", "to take out, to submit", "godan", "medium"),
    ("押す", "おす", "to push", "godan", "medium"),
    ("引く", "ひく", "to pull", "godan", "medium"),
    ("置く", "おく", "to put, to place", "godan", "medium"),
    ("届く", "とどく", "to reach, to be delivered", "godan", "hard"),
    ("動く", "うごく", "to move", "godan", "hard"),
    ("驚く", "おどろく", "to be surprised", "godan", "hard"),
    ("頑張る", "がんばる", "to do one's best", "godan", "medium"),
    ("残る", "のこる", "to remain", "godan", "hard"),
    ("渡る", "わたる", "to cross", "godan", "hard"),
    ("眠る", "ねむる", "to sleep, to fall asleep", "godan", "hard"),
    ("怒る", "おこる", "to get angry", "godan", "hard"),
    ("光る", "ひかる", "to shine", "godan", "hard"),
    ("飛ぶ", "とぶ", "to fly, to jump", "godan", "medium"),
    ("運転する", "うんてんする", "to drive", "irregular", "medium"),
    # --- v2.9.3: verbs taught in the Roadmap that were missing here ---
    ("着替える", "きがえる", "to change clothes", "ichidan", "medium"),
    ("出かける", "でかける", "to go out", "ichidan", "medium"),
    ("乗り換える", "のりかえる", "to transfer (trains)", "ichidan", "hard"),
    ("決める", "きめる", "to decide", "ichidan", "medium"),
    ("戻る", "もどる", "to go back, to return", "godan", "medium"),
    ("包む", "つつむ", "to wrap", "godan", "hard"),
    ("値切る", "ねぎる", "to haggle", "godan", "hard"),
    ("撮る", "とる", "to take (a photo)", "godan", "medium"),
    ("通勤する", "つうきんする", "to commute to work", "irregular", "medium"),
    ("料理する", "りょうりする", "to cook", "irregular", "easy"),
    ("買い物する", "かいものする", "to go shopping", "irregular", "easy"),
    ("昼寝する", "ひるねする", "to take a nap", "irregular", "medium"),
    ("散歩する", "さんぽする", "to take a walk", "irregular", "easy"),
    ("卒業する", "そつぎょうする", "to graduate", "irregular", "medium"),
    ("入院する", "にゅういんする", "to be hospitalized", "irregular", "hard"),
    ("印刷する", "いんさつする", "to print", "irregular", "medium"),
    ("保存する", "ほぞんする", "to save (a file)", "irregular", "hard"),
    ("検索する", "けんさくする", "to search online", "irregular", "hard"),
    ("ログインする", "ログインする", "to log in", "irregular", "medium"),
    ("クリックする", "クリックする", "to click", "irregular", "medium"),
    ("送信する", "そうしんする", "to send (a message)", "irregular", "hard"),
    ("削除する", "さくじょする", "to delete", "irregular", "hard"),
    ("接続する", "せつぞくする", "to connect", "irregular", "hard"),
    ("ダウンロードする", "ダウンロードする", "to download", "irregular", "medium"),
    ("充電する", "じゅうでんする", "to charge (a battery)", "irregular", "medium"),
    ("連絡する", "れんらくする", "to contact", "irregular", "medium"),
]
# strip the placeholder rows above
VERBS = [v for v in VERBS if v[1] and v[3]]

U_TO_I = {"う": "い", "く": "き", "ぐ": "ぎ", "す": "し", "つ": "ち",
          "ぬ": "に", "ぶ": "び", "む": "み", "る": "り"}
U_TO_A = {"う": "わ", "く": "か", "ぐ": "が", "す": "さ", "つ": "た",
          "ぬ": "な", "ぶ": "ば", "む": "ま", "る": "ら"}
U_TO_E = {"う": "え", "く": "け", "ぐ": "げ", "す": "せ", "つ": "て",
          "ぬ": "ね", "ぶ": "べ", "む": "め", "る": "れ"}
U_TO_O = {"う": "お", "く": "こ", "ぐ": "ご", "す": "そ", "つ": "と",
          "ぬ": "の", "ぶ": "ぼ", "む": "も", "る": "ろ"}

# godan te/ta-form euphonic changes, keyed by final kana
TE_GODAN = {"う": "って", "つ": "って", "る": "って",
            "む": "んで", "ぶ": "んで", "ぬ": "んで",
            "く": "いて", "ぐ": "いで", "す": "して"}
TA_GODAN = {k: v.replace("て", "た").replace("で", "だ") for k, v in TE_GODAN.items()}


def conjugate(word, reading, group):
    """Return the standard conjugated forms for both kanji and kana spellings."""
    def forms(s):
        stem, last = s[:-1], s[-1]

        if group == "irregular":
            if s.endswith("する"):
                base = s[:-2]
                return {
                    "masu": base + "します", "masu_neg": base + "しません",
                    "past": base + "した", "past_polite": base + "しました",
                    "te": base + "して", "nai": base + "しない",
                    "potential": base + "できる", "volitional": base + "しよう",
                }
            # 来る / くる
            kana = s.endswith("くる")
            k = (lambda a, b: b if kana else a)
            return {
                "masu": k("来ます", "きます"), "masu_neg": k("来ません", "きません"),
                "past": k("来た", "きた"), "past_polite": k("来ました", "きました"),
                "te": k("来て", "きて"), "nai": k("来ない", "こない"),
                "potential": k("来られる", "こられる"), "volitional": k("来よう", "こよう"),
            }

        if group == "ichidan":
            return {
                "masu": stem + "ます", "masu_neg": stem + "ません",
                "past": stem + "た", "past_polite": stem + "ました",
                "te": stem + "て", "nai": stem + "ない",
                "potential": stem + "られる", "volitional": stem + "よう",
            }

        # godan
        i_stem = stem + U_TO_I[last]
        a_stem = stem + U_TO_A[last]
        e_stem = stem + U_TO_E[last]
        o_stem = stem + U_TO_O[last]
        te = stem + TE_GODAN[last]
        ta = stem + TA_GODAN[last]
        # 行く is the classic te-form exception
        if s in ("行く", "いく"):
            te, ta = stem + "って", stem + "った"
        nai = a_stem + "ない"
        if s == "ある":
            nai = "ない"
        return {
            "masu": i_stem + "ます", "masu_neg": i_stem + "ません",
            "past": ta, "past_polite": i_stem + "ました",
            "te": te, "nai": nai,
            "potential": e_stem + "る", "volitional": o_stem + "う",
        }

    kanji_forms = forms(word)
    kana_forms = forms(reading)
    return {k: {"kanji": kanji_forms[k], "kana": kana_forms[k]} for k in kanji_forms}


GROUP_LABEL = {
    "godan": "Godan (u-verb, 五段)",
    "ichidan": "Ichidan (ru-verb, 一段)",
    "irregular": "Irregular (する・来る)",
}

out = []
seen = set()
for word, reading, meaning, group, level in VERBS:
    if word in seen:
        continue
    seen.add(word)
    out.append({
        "word": word,
        "reading": reading,
        "meaning": meaning,
        "group": group,
        "group_label": GROUP_LABEL[group],
        "difficulty": level,
        "forms": conjugate(word, reading, group),
    })

with open("data/verbs.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)

print(len(out), "verbs written")
for v in out[:2] + [v for v in out if v["word"] in ("行く", "飲む", "食べる", "話す", "来る")][:5]:
    print(v["word"], v["group"], {k: d["kanji"] for k, d in v["forms"].items()})
