# -*- coding: utf-8 -*-
"""
Generates data/roadmap.json - the Duolingo-style learning path.

Every chapter is one of two kinds:
  - "link"   points at an existing section of the app (Hiragana, Katakana,
             Verbs, Kanji, Conversations, Stories, ...). No new content to
             write; visiting it and coming back marks it complete.
  - "lesson" a new, original mini-lesson: a vocab set plus a handful of
             example sentences. Quiz questions (meaning-matching,
             reading-matching, fill-in-the-blank) are generated from this
             at request time in app.py, the same way kanji_practice and
             jlpt_practice already build their quizzes from a word pool
             instead of a hand-written question list.

Only Section 1 has real "lesson" content for now; Sections 2-8 are
placeholders (title + chapter titles only) so the path UI has its full
shape end to end, ready to fill in chapter by chapter.

All wording here is original, written for this app - inspired by the
*topics* a beginner picture-dictionary/course typically covers (family,
numbers, colors, shopping, time...), which is a standard, non-original
way to organize beginner content, not text or examples taken from any
particular book.
"""

import json


def v(jp, reading, romaji, meaning):
    return {"jp": jp, "reading": reading, "romaji": romaji, "meaning": meaning}


def s(jp, reading, romaji, english, blank):
    """One fill-in-the-blank example sentence. `blank` must exactly match
    the `jp` field of one vocab item in the same chapter - that's the
    word blanked out of `jp`/`reading` (as "___") and the correct answer."""
    return {"jp": jp, "reading": reading, "romaji": romaji, "english": english, "blank": blank}


SECTIONS = [
    {
        "id": "first-steps",
        "title": "First Steps",
        "blurb": "Absolute basics - read kana and introduce yourself.",
        "chapters": [
            {
                "id": "hiragana",
                "title": "Hiragana",
                "icon": "あ",
                "kind": "link",
                "link_endpoint": "hiragana",
            },
            {
                "id": "katakana",
                "title": "Katakana",
                "icon": "ア",
                "kind": "link",
                "link_endpoint": "katakana",
            },
            {
                "id": "greetings-intro",
                "title": "Greetings & Introductions",
                "icon": "👋",
                "kind": "lesson",
                "vocab": [
                    v("こんにちは", "こんにちは", "konnichiwa", "hello"),
                    v("おはようございます", "おはようございます", "ohayō gozaimasu", "good morning"),
                    v("こんばんは", "こんばんは", "konbanwa", "good evening"),
                    v("さようなら", "さようなら", "sayōnara", "goodbye"),
                    v("ありがとうございます", "ありがとうございます", "arigatō gozaimasu", "thank you"),
                    v("すみません", "すみません", "sumimasen", "excuse me, sorry"),
                    v("はじめまして", "はじめまして", "hajimemashite", "nice to meet you"),
                    v("お名前は何ですか", "おなまえはなんですか", "onamae wa nan desu ka", "what is your name?"),
                    v("よろしくお願いします", "よろしくおねがいします", "yoroshiku onegaishimasu", "pleased to meet you"),
                    v("お元気ですか", "おげんきですか", "ogenki desu ka", "how are you?"),
                    v("元気です", "げんきです", "genki desu", "I'm fine"),
                ],
                "sentences": [
                    s("___。私はゆきです。", "___。わたしはゆきです。",
                      "___. Watashi wa Yuki desu.", "Nice to meet you. I'm Yuki.", "はじめまして"),
                    s("田中さん、___。", "たなかさん、おげんきですか。",
                      "Tanaka-san, ___.", "Tanaka, how are you?", "お元気ですか"),
                    s("手伝ってくれて、___。", "てつだってくれて、ありがとうございます。",
                      "Tetsudatte kurete, ___.", "Thank you for helping me.", "ありがとうございます"),
                    s("道を聞きたいので、___。", "みちをききたいので、すみません。",
                      "Michi o kikitai node, ___.", "Excuse me, I want to ask for directions.", "すみません"),
                    s("これから一年間、___。", "これからいちねんかん、よろしくおねがいします。",
                      "Kore kara ichinenkan, ___.", "I look forward to working with you this year.", "よろしくお願いします"),
                    s("朝、友達に会って「___」と言いました。", "あさ、ともだちにあって「おはようございます」といいました。",
                      "Asa, tomodachi ni atte '___' to iimashita.", "In the morning, I met my friend and said good morning.", "おはようございます"),
                ],
            },
            {
                "id": "numbers-1-100",
                "title": "Numbers 1-100",
                "icon": "🔢",
                "kind": "lesson",
                "vocab": [
                    v("一", "いち", "ichi", "one"),
                    v("二", "に", "ni", "two"),
                    v("三", "さん", "san", "three"),
                    v("四", "よん", "yon", "four"),
                    v("五", "ご", "go", "five"),
                    v("六", "ろく", "roku", "six"),
                    v("七", "なな", "nana", "seven"),
                    v("八", "はち", "hachi", "eight"),
                    v("九", "きゅう", "kyū", "nine"),
                    v("十", "じゅう", "jū", "ten"),
                    v("二十", "にじゅう", "nijū", "twenty"),
                    v("百", "ひゃく", "hyaku", "one hundred"),
                ],
                "sentences": [
                    s("りんごの数は___です。", "りんごのかずはさんです。",
                      "Ringo no kazu wa ___ desu.", "The number of apples is three.", "三"),
                    s("私の答えは___です。", "わたしのこたえははちです。",
                      "Watashi no kotae wa ___ desu.", "My answer is eight.", "八"),
                    s("部屋の番号は___です。", "へやのばんごうはじゅうです。",
                      "Heya no bangō wa ___ desu.", "The room number is ten.", "十"),
                    s("今の点数は___です。", "いまのてんすうはひゃくです。",
                      "Ima no tensū wa ___ desu.", "The current score is 100.", "百"),
                    s("一足す一は___です。", "いちたすいちはにです。",
                      "Ichi tasu ichi wa ___ desu.", "One plus one is two.", "二"),
                    s("五足す二は___です。", "ごたすにはななです。",
                      "Go tasu ni wa ___ desu.", "Five plus two is seven.", "七"),
                ],
            },
            {
                "id": "colors-shapes",
                "title": "Colors & Shapes",
                "icon": "🎨",
                "kind": "lesson",
                "vocab": [
                    v("赤", "あか", "aka", "red"),
                    v("青", "あお", "ao", "blue"),
                    v("黄色", "きいろ", "kiiro", "yellow"),
                    v("緑", "みどり", "midori", "green"),
                    v("白", "しろ", "shiro", "white"),
                    v("黒", "くろ", "kuro", "black"),
                    v("茶色", "ちゃいろ", "chairo", "brown"),
                    v("丸", "まる", "maru", "circle"),
                    v("四角", "しかく", "shikaku", "square"),
                    v("三角", "さんかく", "sankaku", "triangle"),
                ],
                "sentences": [
                    s("空は___です。", "そらはあおです。",
                      "Sora wa ___ desu.", "The sky is blue.", "青"),
                    s("りんごは___です。", "りんごはあかです。",
                      "Ringo wa ___ desu.", "The apple is red.", "赤"),
                    s("バナナは___です。", "ばななはきいろです。",
                      "Banana wa ___ desu.", "The banana is yellow.", "黄色"),
                    s("葉っぱは___です。", "はっぱはみどりです。",
                      "Happa wa ___ desu.", "The leaf is green.", "緑"),
                    s("このボールは___です。", "このぼーるはまるです。",
                      "Kono bōru wa ___ desu.", "This ball is a circle.", "丸"),
                    s("この箱は___です。", "このはこはしかくです。",
                      "Kono hako wa ___ desu.", "This box is a square.", "四角"),
                ],
            },
        ],
    },
    {
        "id": "everyday-life",
        "title": "Everyday Life",
        "blurb": "The vocabulary of a normal day.",
        "chapters": [
            {"id": "my-family", "title": "My Family", "icon": "👪", "kind": "placeholder"},
            {"id": "my-house", "title": "My House", "icon": "🏠", "kind": "placeholder"},
            {"id": "human-body", "title": "The Human Body", "icon": "🧍", "kind": "placeholder"},
            {"id": "daily-routines", "title": "Daily Routines", "icon": "🌅", "kind": "placeholder"},
            {"id": "telling-time", "title": "Telling Time", "icon": "🕐", "kind": "placeholder"},
            {"id": "days-dates", "title": "Days, Weeks & Dates", "icon": "📅", "kind": "placeholder"},
        ],
    },
    {
        "id": "out-and-about",
        "title": "Out and About",
        "blurb": "Navigating the world outside the house.",
        "chapters": [
            {"id": "around-town", "title": "Around Town", "icon": "🏙", "kind": "placeholder"},
            {"id": "asking-directions-rm", "title": "Asking Directions", "icon": "🧭", "kind": "placeholder"},
            {"id": "transportation", "title": "Transportation", "icon": "🚃", "kind": "placeholder"},
            {"id": "going-shopping-rm", "title": "Going Shopping", "icon": "🛍", "kind": "placeholder"},
            {"id": "talking-about-money-rm", "title": "Talking about Money", "icon": "💴", "kind": "placeholder"},
        ],
    },
    {
        "id": "people-culture",
        "title": "People & Culture",
        "blurb": "Social and seasonal topics.",
        "chapters": [
            {"id": "seasons-weather", "title": "Four Seasons & Weather", "icon": "🌦", "kind": "placeholder"},
            {"id": "holidays-festivals", "title": "Holidays & Festivals", "icon": "🎎", "kind": "placeholder"},
            {"id": "hobbies-music", "title": "Music, Sports & Hobbies", "icon": "🎵", "kind": "placeholder"},
            {"id": "at-work-rm", "title": "At Work", "icon": "💼", "kind": "placeholder"},
            {"id": "at-school-rm", "title": "At School", "icon": "🏫", "kind": "placeholder"},
        ],
    },
    {
        "id": "food-drink",
        "title": "Food & Drink",
        "blurb": "Restaurant- and kitchen-ready vocabulary.",
        "chapters": [
            {"id": "japanese-food", "title": "Japanese Food", "icon": "🍣", "kind": "placeholder"},
            {"id": "fruits-veg-drinks", "title": "Fruits, Vegetables & Drinks", "icon": "🍎", "kind": "placeholder"},
            {"id": "at-the-market-rm", "title": "At the Market", "icon": "🛒", "kind": "placeholder"},
            {
                "id": "at-a-restaurant-rm",
                "title": "At a Restaurant",
                "icon": "🍽",
                "kind": "link",
                "link_endpoint": "conversations_list",
            },
        ],
    },
    {
        "id": "modern-life",
        "title": "Modern Life",
        "blurb": "Vocabulary the book-era word lists usually skip.",
        "chapters": [
            {"id": "computers-internet", "title": "Computers & the Internet", "icon": "💻", "kind": "placeholder"},
            {"id": "smartphones-apps", "title": "Smartphones & Apps", "icon": "📱", "kind": "placeholder"},
            {"id": "health-doctor", "title": "Health & the Doctor", "icon": "🩺", "kind": "placeholder"},
            {"id": "the-environment", "title": "The Environment", "icon": "🌱", "kind": "placeholder"},
        ],
    },
    {
        "id": "grammar-foundations",
        "title": "Grammar Foundations",
        "blurb": "Where vocabulary turns into real sentences.",
        "chapters": [
            {"id": "particles-wa-ga-o", "title": "Particles は・が・を", "icon": "🔤", "kind": "placeholder"},
            {"id": "particles-ni-de-e", "title": "Particles に・で・へ", "icon": "🔤", "kind": "placeholder"},
            {
                "id": "verb-basics-rm",
                "title": "Verb Conjugation Basics",
                "icon": "🈂",
                "kind": "link",
                "link_endpoint": "verbs_list",
            },
            {"id": "adjectives-opposites-rm", "title": "Adjectives & Opposites", "icon": "⚖️", "kind": "placeholder"},
            {"id": "counters-rm", "title": "Counters", "icon": "🔟", "kind": "placeholder"},
            {"id": "sentence-patterns", "title": "Basic Sentence Patterns", "icon": "📝", "kind": "placeholder"},
            {"id": "te-form-basics", "title": "The て-form", "icon": "🔗", "kind": "placeholder"},
            {"id": "potential-form", "title": "Saying \"Can Do\"", "icon": "💪", "kind": "placeholder"},
        ],
    },
    {
        "id": "toward-fluency",
        "title": "Toward Fluency",
        "blurb": "Bridging into real reading and the JLPT.",
        "chapters": [
            {"id": "countries-nationalities", "title": "Countries & Nationalities", "icon": "🌍", "kind": "placeholder"},
            {"id": "foreign-languages-travel", "title": "Foreign Languages & Travel", "icon": "✈️", "kind": "placeholder"},
            {
                "id": "n5-kanji-checkpoint",
                "title": "JLPT N5 Kanji Checkpoint",
                "icon": "漢",
                "kind": "link",
                "link_endpoint": "jlpt_index",
            },
            {
                "id": "real-conversations-rm",
                "title": "Real Conversations",
                "icon": "💬",
                "kind": "link",
                "link_endpoint": "conversations_list",
            },
            {
                "id": "real-stories-rm",
                "title": "Real Stories",
                "icon": "📖",
                "kind": "link",
                "link_endpoint": "stories_list",
            },
        ],
    },
]


# ---------------------------------------------------------------------------
# Lessons for the remaining sections, filled in section by section.
#
# Vocab comes either from data/picture_dict.json (the categorized word list
# already in the app: pd("Category", ["word", ...]) picks specific entries
# from it, so nothing is retyped) or is written inline with v(). Example
# sentences are original and written for this app. Each sentence's `blank`
# must exactly match one vocab item's `jp`.
# ---------------------------------------------------------------------------

_PD = json.load(open("data/picture_dict.json", encoding="utf-8"))


def pd(category, words):
    by_word = {e["word"]: e for e in _PD if e["category"] == category}
    out = []
    for w in words:
        e = by_word[w]  # KeyError here = a typo in the word list, on purpose
        out.append(v(e["word"], e["reading"], e["romaji"], e["meaning"]))
    return out


LESSONS = {
    # ------------------------------------------------ Section 2: Everyday Life
    "my-family": {
        "vocab": pd("Family & People", ["家族", "お父さん", "お母さん", "お兄さん", "お姉さん", "息子", "娘", "両親", "夫", "妻", "孫"]),
        "sentences": [
            s("私の___は四人です。", "わたしの___はよにんです。", "Watashi no ___ wa yonin desu.", "There are four people in my family.", "家族"),
            s("___は会社で働いています。", "___はかいしゃではたらいています。", "___ wa kaisha de hataraite imasu.", "My father works at a company.", "お父さん"),
            s("___は料理が上手です。", "___はりょうりがじょうずです。", "___ wa ryōri ga jōzu desu.", "My mother is good at cooking.", "お母さん"),
            s("___は大学生です。", "___はだいがくせいです。", "___ wa daigakusei desu.", "My older brother is a university student.", "お兄さん"),
            s("私には___が一人います。", "わたしには___がひとりいます。", "Watashi ni wa ___ ga hitori imasu.", "I have one daughter.", "娘"),
            s("私の___は京都に住んでいます。", "わたしの___はきょうとにすんでいます。", "Watashi no ___ wa Kyōto ni sunde imasu.", "My parents live in Kyoto.", "両親"),
        ],
    },
    "my-house": {
        "vocab": pd("House & Furniture", ["部屋", "台所", "寝室", "窓", "椅子", "机", "ベッド", "冷蔵庫", "テレビ", "玄関", "浴室", "本棚"]),
        "sentences": [
            s("___で料理を作ります。", "___でりょうりをつくります。", "___ de ryōri o tsukurimasu.", "I cook in the kitchen.", "台所"),
            s("___で寝ます。", "___でねます。", "___ de nemasu.", "I sleep in the bedroom.", "寝室"),
            s("___を開けてください。", "___をあけてください。", "___ o akete kudasai.", "Please open the window.", "窓"),
            s("牛乳は___に入っています。", "ぎゅうにゅうは___にはいっています。", "Gyūnyū wa ___ ni haitte imasu.", "The milk is in the refrigerator.", "冷蔵庫"),
            s("私の___は二階にあります。", "わたしの___はにかいにあります。", "Watashi no ___ wa nikai ni arimasu.", "My room is on the second floor.", "部屋"),
            s("靴は___で脱ぎます。", "くつは___でぬぎます。", "Kutsu wa ___ de nugimasu.", "You take off your shoes at the entrance.", "玄関"),
        ],
    },
    "human-body": {
        "vocab": pd("Health & Body", ["頭", "顔", "首", "肩", "腕", "胸", "腹", "膝", "脚", "歯", "唇", "指"]),
        "sentences": [
            s("___が痛いです。", "___がいたいです。", "___ ga itai desu.", "I have a headache.", "頭"),
            s("毎朝、___を洗います。", "まいあさ、___をあらいます。", "Maiasa, ___ o araimasu.", "I wash my face every morning.", "顔"),
            s("食べたあと、___をみがきます。", "たべたあと、___をみがきます。", "Tabeta ato, ___ o migakimasu.", "After eating, I brush my teeth.", "歯"),
            s("___が痛くて歩けません。", "___がいたくてあるけません。", "___ ga itakute arukemasen.", "My leg hurts and I can't walk.", "脚"),
            s("ピアノを弾くとき、___を使います。", "ぴあのをひくとき、___をつかいます。", "Piano o hiku toki, ___ o tsukaimasu.", "I use my fingers when I play the piano.", "指"),
            s("寒いので、___を温めます。", "さむいので、___をあたためます。", "Samui node, ___ o atatamemasu.", "It's cold, so I keep my neck warm.", "首"),
        ],
    },
    "daily-routines": {
        "vocab": [
            v("起きる", "おきる", "okiru", "to wake up"),
            v("寝る", "ねる", "neru", "to sleep"),
            v("朝ご飯", "あさごはん", "asagohan", "breakfast"),
            v("昼ご飯", "ひるごはん", "hirugohan", "lunch"),
            v("晩ご飯", "ばんごはん", "bangohan", "dinner"),
            v("働く", "はたらく", "hataraku", "to work"),
            v("勉強する", "べんきょうする", "benkyō suru", "to study"),
            v("帰る", "かえる", "kaeru", "to go home"),
            v("散歩する", "さんぽする", "sanpo suru", "to take a walk"),
            v("掃除する", "そうじする", "sōji suru", "to clean"),
            v("歯をみがく", "はをみがく", "ha o migaku", "to brush one's teeth"),
        ],
        "sentences": [
            s("毎朝六時に___。", "まいあさろくじに___。", "Maiasa rokuji ni ___.", "I wake up at six every morning.", "起きる"),
            s("毎朝、___を食べます。", "まいあさ、___をたべます。", "Maiasa, ___ o tabemasu.", "I eat breakfast every morning.", "朝ご飯"),
            s("___は十二時に食べます。", "___はじゅうにじにたべます。", "___ wa jūniji ni tabemasu.", "I eat lunch at twelve.", "昼ご飯"),
            s("今晩の___は何ですか。", "こんばんの___はなんですか。", "Konban no ___ wa nan desu ka.", "What's for dinner tonight?", "晩ご飯"),
            s("毎日、日本語を___。", "まいにち、にほんごを___。", "Mainichi, nihongo o ___.", "I study Japanese every day.", "勉強する"),
            s("夕方、公園を___。", "ゆうがた、こうえんを___。", "Yūgata, kōen o ___.", "In the evening, I take a walk in the park.", "散歩する"),
        ],
    },
    "telling-time": {
        "vocab": [
            v("今", "いま", "ima", "now"),
            v("何時", "なんじ", "nanji", "what time"),
            v("一時", "いちじ", "ichiji", "one o'clock"),
            v("四時", "よじ", "yoji", "four o'clock"),
            v("七時", "しちじ", "shichiji", "seven o'clock"),
            v("九時", "くじ", "kuji", "nine o'clock"),
            v("十二時", "じゅうにじ", "jūniji", "twelve o'clock"),
            v("半", "はん", "han", "half past"),
            v("午前", "ごぜん", "gozen", "morning, a.m."),
            v("午後", "ごご", "gogo", "afternoon, p.m."),
            v("正午", "しょうご", "shōgo", "noon"),
        ],
        "sentences": [
            s("___、何時ですか。", "___、なんじですか。", "___, nanji desu ka.", "What time is it now?", "今"),
            s("会議は___に始まります。", "かいぎは___にはじまります。", "Kaigi wa ___ ni hajimarimasu.", "The meeting starts at nine.", "九時"),
            s("私は___に起きます。", "わたしは___におきます。", "Watashi wa ___ ni okimasu.", "I get up at seven.", "七時"),
            s("三時___に会いましょう。", "さんじ___にあいましょう。", "Sanji ___ ni aimashō.", "Let's meet at half past three.", "半"),
            s("___は朝から昼までです。", "___はあさからひるまでです。", "___ wa asa kara hiru made desu.", "A.M. is from morning until noon.", "午前"),
            s("___に昼ご飯を食べます。", "___にひるごはんをたべます。", "___ ni hirugohan o tabemasu.", "I eat lunch at noon.", "正午"),
            s("授業は___三時に終わります。", "じゅぎょうは___さんじにおわります。", "Jugyō wa ___ sanji ni owarimasu.", "Class ends at three in the afternoon.", "午後"),
        ],
    },
    "days-dates": {
        "vocab": [
            v("月曜日", "げつようび", "getsuyōbi", "Monday"),
            v("火曜日", "かようび", "kayōbi", "Tuesday"),
            v("水曜日", "すいようび", "suiyōbi", "Wednesday"),
            v("木曜日", "もくようび", "mokuyōbi", "Thursday"),
            v("金曜日", "きんようび", "kin'yōbi", "Friday"),
            v("土曜日", "どようび", "doyōbi", "Saturday"),
            v("日曜日", "にちようび", "nichiyōbi", "Sunday"),
            v("今日", "きょう", "kyō", "today"),
            v("明日", "あした", "ashita", "tomorrow"),
            v("昨日", "きのう", "kinō", "yesterday"),
            v("今週", "こんしゅう", "konshū", "this week"),
            v("来週", "らいしゅう", "raishū", "next week"),
        ],
        "sentences": [
            s("___は休みです。", "___はやすみです。", "___ wa yasumi desu.", "Sunday is a day off.", "日曜日"),
            s("___は雨でした。", "___はあめでした。", "___ wa ame deshita.", "It rained yesterday.", "昨日"),
            s("___は友達に会います。", "___はともだちにあいます。", "___ wa tomodachi ni aimasu.", "I'm meeting a friend tomorrow.", "明日"),
            s("今日は___です。", "きょうは___です。", "Kyō wa ___ desu.", "Today is Wednesday.", "水曜日"),
            s("___は忙しいです。", "___はいそがしいです。", "___ wa isogashii desu.", "Next week is busy.", "来週"),
            s("私は___に買い物に行きます。", "わたしは___にかいものにいきます。", "Watashi wa ___ ni kaimono ni ikimasu.", "I go shopping on Saturday.", "土曜日"),
        ],
    },
    # ---------------------------------------------- Section 3: Out and About
    "around-town": {
        "vocab": [
            v("銀行", "ぎんこう", "ginkō", "bank"),
            v("郵便局", "ゆうびんきょく", "yūbinkyoku", "post office"),
            v("駅", "えき", "eki", "station"),
            v("病院", "びょういん", "byōin", "hospital"),
            v("学校", "がっこう", "gakkō", "school"),
            v("公園", "こうえん", "kōen", "park"),
            v("図書館", "としょかん", "toshokan", "library"),
            v("店", "みせ", "mise", "shop"),
            v("交番", "こうばん", "kōban", "police box"),
            v("空港", "くうこう", "kūkō", "airport"),
            v("町", "まち", "machi", "town"),
            v("橋", "はし", "hashi", "bridge"),
        ],
        "sentences": [
            s("___でお金を下ろします。", "___でおかねをおろします。", "___ de okane o oroshimasu.", "I withdraw money at the bank.", "銀行"),
            s("___で手紙を出します。", "___でてがみをだします。", "___ de tegami o dashimasu.", "I mail a letter at the post office.", "郵便局"),
            s("電車は八時に___に着きます。", "でんしゃははちじに___につきます。", "Densha wa hachiji ni ___ ni tsukimasu.", "The train arrives at the station at eight.", "駅"),
            s("子供が___で遊んでいます。", "こどもが___であそんでいます。", "Kodomo ga ___ de asonde imasu.", "The children are playing in the park.", "公園"),
            s("___で本を借ります。", "___でほんをかります。", "___ de hon o karimasu.", "I borrow books at the library.", "図書館"),
            s("具合が悪いときは、___に行きます。", "ぐあいがわるいときは、___にいきます。", "Guai ga warui toki wa, ___ ni ikimasu.", "When I feel unwell, I go to the hospital.", "病院"),
        ],
    },
    "asking-directions-rm": {
        "vocab": pd("Directions & Position", ["どこ", "ここ", "あそこ", "北", "南", "東", "西"]) + [
            v("右", "みぎ", "migi", "right"),
            v("左", "ひだり", "hidari", "left"),
            v("まっすぐ", "まっすぐ", "massugu", "straight ahead"),
            v("曲がる", "まがる", "magaru", "to turn"),
            v("近い", "ちかい", "chikai", "near"),
        ],
        "sentences": [
            s("駅は___ですか。", "えきは___ですか。", "Eki wa ___ desu ka.", "Where is the station?", "どこ"),
            s("銀行は___にあります。", "ぎんこうは___にあります。", "Ginkō wa ___ ni arimasu.", "The bank is over there.", "あそこ"),
            s("次の角を___に曲がってください。", "つぎのかどを___にまがってください。", "Tsugi no kado o ___ ni magatte kudasai.", "Please turn right at the next corner.", "右"),
            s("この道を___行ってください。", "このみちを___いってください。", "Kono michi o ___ itte kudasai.", "Please go straight along this road.", "まっすぐ"),
            s("太陽は___から昇ります。", "たいようは___からのぼります。", "Taiyō wa ___ kara noborimasu.", "The sun rises in the east.", "東"),
            s("駅はここから___です。", "えきはここから___です。", "Eki wa koko kara ___ desu.", "The station is near from here.", "近い"),
        ],
    },
    "transportation": {
        "vocab": [
            v("電車", "でんしゃ", "densha", "train"),
            v("バス", "ばす", "basu", "bus"),
            v("タクシー", "たくしー", "takushī", "taxi"),
            v("自転車", "じてんしゃ", "jitensha", "bicycle"),
            v("飛行機", "ひこうき", "hikōki", "airplane"),
            v("船", "ふね", "fune", "ship, boat"),
            v("切符", "きっぷ", "kippu", "ticket"),
        ] + pd("Transportation", ["車", "新幹線", "オートバイ", "運転手"]),
        "sentences": [
            s("毎朝、___で会社に行きます。", "まいあさ、___でかいしゃにいきます。", "Maiasa, ___ de kaisha ni ikimasu.", "I go to work by train every morning.", "電車"),
            s("雨が降っているので、___に乗ります。", "あめがふっているので、___にのります。", "Ame ga futte iru node, ___ ni norimasu.", "It's raining, so I'll take a taxi.", "タクシー"),
            s("東京から大阪まで___で行きます。", "とうきょうからおおさかまで___でいきます。", "Tōkyō kara Ōsaka made ___ de ikimasu.", "I go from Tokyo to Osaka by bullet train.", "新幹線"),
            s("天気がいい日は___で学校に行きます。", "てんきがいいひは___でがっこうにいきます。", "Tenki ga ii hi wa ___ de gakkō ni ikimasu.", "On nice days I go to school by bicycle.", "自転車"),
            s("___を買ってからホームに行きます。", "___をかってからほーむにいきます。", "___ o katte kara hōmu ni ikimasu.", "I buy a ticket and then go to the platform.", "切符"),
            s("夏休みに___で北海道へ行きます。", "なつやすみに___でほっかいどうへいきます。", "Natsuyasumi ni ___ de Hokkaidō e ikimasu.", "I'm going to Hokkaido by plane in the summer break.", "飛行機"),
        ],
    },
    "going-shopping-rm": {
        "vocab": pd("Money & Shopping", ["値段", "割引", "安い", "高い", "現金", "クレジットカード", "領収書", "Mサイズ"]) + [
            v("買う", "かう", "kau", "to buy"),
            v("店員", "てんいん", "tenin", "shop assistant"),
            v("袋", "ふくろ", "fukuro", "bag"),
        ],
        "sentences": [
            s("この服の___はいくらですか。", "このふくの___はいくらですか。", "Kono fuku no ___ wa ikura desu ka.", "What is the price of these clothes?", "値段"),
            s("今日は全部___です。", "きょうはぜんぶ___です。", "Kyō wa zenbu ___ desu.", "Everything is on discount today.", "割引"),
            s("このかばんはとても___です。", "このかばんはとても___です。", "Kono kaban wa totemo ___ desu.", "This bag is very cheap.", "安い"),
            s("___で払います。", "___ではらいます。", "___ de haraimasu.", "I'll pay in cash.", "現金"),
            s("___は使えますか。", "___はつかえますか。", "___ wa tsukaemasu ka.", "Can I use a credit card?", "クレジットカード"),
            s("___をください。", "___をください。", "___ o kudasai.", "Please give me a receipt.", "領収書"),
            s("わからないことは___に聞いてください。", "わからないことは___にきいてください。", "Wakaranai koto wa ___ ni kiite kudasai.", "Please ask a shop assistant if you don't understand.", "店員"),
        ],
    },
    "talking-about-money-rm": {
        "vocab": pd("Money & Shopping", ["お金", "円", "紙幣", "硬貨", "小銭", "千円", "一万円", "貯金", "税金", "借金", "預金"]),
        "sentences": [
            s("今日は___がありません。", "きょうは___がありません。", "Kyō wa ___ ga arimasen.", "I have no money today.", "お金"),
            s("これは百___です。", "これはひゃく___です。", "Kore wa hyaku ___ desu.", "This is one hundred yen.", "円"),
            s("財布に___があまりありません。", "さいふに___があまりありません。", "Saifu ni ___ ga amari arimasen.", "I don't have much small change in my wallet.", "小銭"),
            s("毎月、少し___をします。", "まいつき、すこし___をします。", "Maitsuki, sukoshi ___ o shimasu.", "I save a little every month.", "貯金"),
            s("日本の___は高いですか。", "にほんの___はたかいですか。", "Nihon no ___ wa takai desu ka.", "Are taxes high in Japan?", "税金"),
            s("銀行に___があります。", "ぎんこうに___があります。", "Ginkō ni ___ ga arimasu.", "I have a deposit at the bank.", "預金"),
        ],
    },
    # -------------------------------------------- Section 4: People & Culture
    "seasons-weather": {
        "vocab": pd("Seasons & Holidays", ["春", "夏", "秋", "冬", "四季", "暖かい"]) + [
            v("天気", "てんき", "tenki", "weather"),
            v("雨", "あめ", "ame", "rain"),
            v("雪", "ゆき", "yuki", "snow"),
            v("晴れ", "はれ", "hare", "sunny weather"),
            v("曇り", "くもり", "kumori", "cloudy weather"),
            v("風", "かぜ", "kaze", "wind"),
        ],
        "sentences": [
            s("___は桜が咲きます。", "___はさくらがさきます。", "___ wa sakura ga sakimasu.", "Cherry blossoms bloom in spring.", "春"),
            s("___は暑いので、海に行きます。", "___はあついので、うみにいきます。", "___ wa atsui node, umi ni ikimasu.", "Summer is hot, so I go to the sea.", "夏"),
            s("___は紅葉がきれいです。", "___はこうようがきれいです。", "___ wa kōyō ga kirei desu.", "The autumn leaves are beautiful in autumn.", "秋"),
            s("___は雪がたくさん降ります。", "___はゆきがたくさんふります。", "___ wa yuki ga takusan furimasu.", "It snows a lot in winter.", "冬"),
            s("日本には___があります。", "にほんには___があります。", "Nihon ni wa ___ ga arimasu.", "Japan has four seasons.", "四季"),
            s("今日は___ですから、散歩に行きましょう。", "きょうは___ですから、さんぽにいきましょう。", "Kyō wa ___ desu kara, sanpo ni ikimashō.", "It's sunny today, so let's go for a walk.", "晴れ"),
            s("___が降っています。", "___がふっています。", "___ ga futte imasu.", "It's raining.", "雨"),
        ],
    },
    "holidays-festivals": {
        "vocab": pd("Seasons & Holidays", ["新年", "花火", "誕生日", "夏休み", "冬休み", "クリスマス", "祝日", "七夕", "お餅", "運動会", "節分", "ひな祭り"]),
        "sentences": [
            s("___にお餅を食べます。", "___におもちをたべます。", "___ ni omochi o tabemasu.", "I eat rice cakes at New Year.", "新年"),
            s("夏の夜に___を見ました。", "なつのよるに___をみました。", "Natsu no yoru ni ___ o mimashita.", "I watched fireworks on a summer night.", "花火"),
            s("今日は私の___です。", "きょうはわたしの___です。", "Kyō wa watashi no ___ desu.", "Today is my birthday.", "誕生日"),
            s("___に家族で旅行します。", "___にかぞくでりょこうします。", "___ ni kazoku de ryokō shimasu.", "We travel as a family during summer vacation.", "夏休み"),
            s("十二月二十五日は___です。", "じゅうにがつにじゅうごにちは___です。", "Jūnigatsu nijūgonichi wa ___ desu.", "December 25th is Christmas.", "クリスマス"),
            s("子供たちは___で走ります。", "こどもたちは___ではしります。", "Kodomotachi wa ___ de hashirimasu.", "The children run at the sports day event.", "運動会"),
            s("___に短冊に願いを書きます。", "___にたんざくにねがいをかきます。", "___ ni tanzaku ni negai o kakimasu.", "At the Star Festival, we write wishes on paper strips.", "七夕"),
        ],
    },
    "hobbies-music": {
        "vocab": pd("Music", ["ギター", "琴", "三味線", "バイオリン", "ピアノ", "踊る"]) + pd("Sports & Fitness", ["テニス", "水泳", "スキー", "卓球", "山登り", "ゴルフ"]),
        "sentences": [
            s("毎日___を練習します。", "まいにち___をれんしゅうします。", "Mainichi ___ o renshū shimasu.", "I practice the piano every day.", "ピアノ"),
            s("友達と公園で___をします。", "ともだちとこうえんで___をします。", "Tomodachi to kōen de ___ o shimasu.", "I play tennis with my friends in the park.", "テニス"),
            s("冬は北海道で___をします。", "ふゆはほっかいどうで___をします。", "Fuyu wa Hokkaidō de ___ o shimasu.", "In winter I go skiing in Hokkaido.", "スキー"),
            s("週末は家族と___をします。", "しゅうまつはかぞくと___をします。", "Shūmatsu wa kazoku to ___ o shimasu.", "On weekends I go mountain climbing with my family.", "山登り"),
            s("夏は毎日プールで___をします。", "なつはまいにちぷーるで___をします。", "Natsu wa mainichi pūru de ___ o shimasu.", "In summer I swim at the pool every day.", "水泳"),
            s("みんなで楽しく___。", "みんなでたのしく___。", "Minna de tanoshiku ___.", "Everyone dances happily together.", "踊る"),
            s("私の趣味は___です。", "わたしのしゅみは___です。", "Watashi no shumi wa ___ desu.", "My hobby is table tennis.", "卓球"),
        ],
    },
    "at-work-rm": {
        "vocab": pd("Work & Jobs", ["仕事", "会社", "事務所", "同僚", "出勤する", "残業する", "アルバイト", "秘書", "管理職", "エンジニア", "歯医者", "農家"]),
        "sentences": [
            s("私は毎朝八時に___。", "わたしはまいあさはちじに___。", "Watashi wa maiasa hachiji ni ___.", "I go to work at eight every morning.", "出勤する"),
            s("今日は忙しいので、___。", "きょうはいそがしいので、___。", "Kyō wa isogashii node, ___.", "I'm busy today, so I'll work overtime.", "残業する"),
            s("私の___は優しい人です。", "わたしの___はやさしいひとです。", "Watashi no ___ wa yasashii hito desu.", "My colleague is a kind person.", "同僚"),
            s("父は大きな___で働いています。", "ちちはおおきな___ではたらいています。", "Chichi wa ōkina ___ de hataraite imasu.", "My father works at a big company.", "会社"),
            s("弟は___でコンビニで働いています。", "おとうとは___でこんびにではたらいています。", "Otōto wa ___ de konbini de hataraite imasu.", "My younger brother works at a convenience store part-time.", "アルバイト"),
            s("兄は___です。", "あには___です。", "Ani wa ___ desu.", "My older brother is an engineer.", "エンジニア"),
            s("虫歯が痛いので、___に行きます。", "むしばがいたいので、___にいきます。", "Mushiba ga itai node, ___ ni ikimasu.", "My tooth hurts, so I'm going to the dentist.", "歯医者"),
        ],
    },
    "at-school-rm": {
        "vocab": pd("School & Learning", ["先生", "生徒", "教室", "宿題", "試験", "数学", "科学", "体育", "辞書", "黒板", "クラスメート", "教授"]),
        "sentences": [
            s("私の___は優しいです。", "わたしの___はやさしいです。", "Watashi no ___ wa yasashii desu.", "My teacher is kind.", "先生"),
            s("この学校には二百人の___がいます。", "このがっこうにはにひゃくにんの___がいます。", "Kono gakkō ni wa nihyaku-nin no ___ ga imasu.", "This school has two hundred students.", "生徒"),
            s("明日は___があります。", "あしたは___があります。", "Ashita wa ___ ga arimasu.", "There is an exam tomorrow.", "試験"),
            s("___をやってから寝ます。", "___をやってからねます。", "___ o yatte kara nemasu.", "I go to bed after doing my homework.", "宿題"),
            s("___の授業は計算が多いです。", "___のじゅぎょうはけいさんがおおいです。", "___ no jugyō wa keisan ga ōi desu.", "There is a lot of calculation in math class.", "数学"),
            s("先生は___に字を書きます。", "せんせいは___にじをかきます。", "Sensei wa ___ ni ji o kakimasu.", "The teacher writes characters on the blackboard.", "黒板"),
            s("分からない言葉は___で調べます。", "わからないことばは___でしらべます。", "Wakaranai kotoba wa ___ de shirabemasu.", "I look up words I don't know in a dictionary.", "辞書"),
        ],
    },
    # ------------------------------------------------ Section 5: Food & Drink
    "japanese-food": {
        "vocab": [
            v("寿司", "すし", "sushi", "sushi"),
            v("味噌汁", "みそしる", "misoshiru", "miso soup"),
            v("卵", "たまご", "tamago", "egg"),
        ] + pd("Food & Drink", ["ご飯", "そば", "定食", "箸", "茶碗", "野菜", "豚肉", "鶏肉", "魚介類"]),
        "sentences": [
            s("朝は___を食べます。", "あさは___をたべます。", "Asa wa ___ o tabemasu.", "In the morning I eat rice.", "ご飯"),
            s("毎朝、___を飲みます。", "まいあさ、___をのみます。", "Maiasa, ___ o nomimasu.", "I drink miso soup every morning.", "味噌汁"),
            s("日本人は___で食べます。", "にほんじんは___でたべます。", "Nihonjin wa ___ de tabemasu.", "Japanese people eat with chopsticks.", "箸"),
            s("昼は___を食べました。", "ひるは___をたべました。", "Hiru wa ___ o tabemashita.", "For lunch I ate soba noodles.", "そば"),
            s("私は___が好きです。", "わたしは___がすきです。", "Watashi wa ___ ga suki desu.", "I like sushi.", "寿司"),
            s("私は___を食べません。", "わたしは___をたべません。", "Watashi wa ___ o tabemasen.", "I don't eat pork.", "豚肉"),
            s("___はスーパーで買います。", "___はすーぱーでかいます。", "___ wa sūpā de kaimasu.", "I buy eggs at the supermarket.", "卵"),
        ],
    },
    "fruits-veg-drinks": {
        "vocab": pd("Food & Drink", ["みかん", "柿", "ほうれん草", "もやし", "牛乳", "水", "コーラ", "フルーツジュース", "豆乳"]) + [
            v("りんご", "りんご", "ringo", "apple"),
            v("いちご", "いちご", "ichigo", "strawberry"),
            v("コーヒー", "こーひー", "kōhī", "coffee"),
        ],
        "sentences": [
            s("___は冬の果物です。", "___はふゆのくだものです。", "___ wa fuyu no kudamono desu.", "Mandarin oranges are a winter fruit.", "みかん"),
            s("朝、___を飲みます。", "あさ、___をのみます。", "Asa, ___ o nomimasu.", "In the morning I drink milk.", "牛乳"),
            s("暑いので、冷たい___が飲みたいです。", "あついので、つめたい___がのみたいです。", "Atsui node, tsumetai ___ ga nomitai desu.", "It's hot, so I want to drink cold water.", "水"),
            s("___は体にいいです。", "___はからだにいいです。", "___ wa karada ni ii desu.", "Spinach is good for your body.", "ほうれん草"),
            s("私は___が好きです。", "わたしは___がすきです。", "Watashi wa ___ ga suki desu.", "I like strawberries.", "いちご"),
            s("___を一杯ください。", "___をいっぱいください。", "___ o ippai kudasai.", "One cup of coffee, please.", "コーヒー"),
            s("___は秋に食べます。", "___はあきにたべます。", "___ wa aki ni tabemasu.", "Persimmons are eaten in autumn.", "柿"),
        ],
    },
    "at-the-market-rm": {
        "vocab": [
            v("市場", "いちば", "ichiba", "market"),
            v("魚", "さかな", "sakana", "fish"),
            v("肉", "にく", "niku", "meat"),
            v("果物", "くだもの", "kudamono", "fruit"),
            v("新鮮", "しんせん", "shinsen", "fresh"),
            v("いくら", "いくら", "ikura", "how much"),
            v("全部", "ぜんぶ", "zenbu", "all, everything"),
            v("半分", "はんぶん", "hanbun", "half"),
            v("重い", "おもい", "omoi", "heavy"),
            v("軽い", "かるい", "karui", "light (weight)"),
            v("おまけ", "おまけ", "omake", "a little extra thrown in"),
        ],
        "sentences": [
            s("毎週日曜日、___に行きます。", "まいしゅうにちようび、___にいきます。", "Maishū nichiyōbi, ___ ni ikimasu.", "I go to the market every Sunday.", "市場"),
            s("この___は新鮮でおいしいです。", "この___はしんせんでおいしいです。", "Kono ___ wa shinsen de oishii desu.", "This fish is fresh and delicious.", "魚"),
            s("この___はいくらですか。", "この___はいくらですか。", "Kono ___ wa ikura desu ka.", "How much is this fruit?", "果物"),
            s("このトマトはとても___です。", "このとまとはとても___です。", "Kono tomato wa totemo ___ desu.", "These tomatoes are very fresh.", "新鮮"),
            s("___でいくらですか。", "___でいくらですか。", "___ de ikura desu ka.", "How much is it for everything?", "全部"),
            s("りんごを___に切ってください。", "りんごを___にきってください。", "Ringo o ___ ni kitte kudasai.", "Please cut the apple in half.", "半分"),
            s("この袋は___です。", "このふくろは___です。", "Kono fukuro wa ___ desu.", "This bag is heavy.", "重い"),
        ],
    },
    # -------------------------------------------------- Section 6: Modern Life
    "computers-internet": {
        "vocab": [
            v("パソコン", "ぱそこん", "pasokon", "personal computer"),
            v("インターネット", "いんたーねっと", "intānetto", "the internet"),
            v("メール", "めーる", "mēru", "email"),
            v("ファイル", "ふぁいる", "fairu", "file"),
            v("パスワード", "ぱすわーど", "pasuwādo", "password"),
            v("画面", "がめん", "gamen", "screen"),
            v("キーボード", "きーぼーど", "kībōdo", "keyboard"),
            v("マウス", "まうす", "mausu", "computer mouse"),
            v("ウェブサイト", "うぇぶさいと", "webusaito", "website"),
            v("印刷する", "いんさつする", "insatsu suru", "to print"),
            v("保存する", "ほぞんする", "hozon suru", "to save (a file)"),
            v("検索する", "けんさくする", "kensaku suru", "to search online"),
        ],
        "sentences": [
            s("毎日___を使います。", "まいにち___をつかいます。", "Mainichi ___ o tsukaimasu.", "I use a computer every day.", "パソコン"),
            s("___でニュースを見ます。", "___でにゅーすをみます。", "___ de nyūsu o mimasu.", "I read the news on the internet.", "インターネット"),
            s("友達に___を送りました。", "ともだちに___をおくりました。", "Tomodachi ni ___ o okurimashita.", "I sent my friend an email.", "メール"),
            s("___を忘れてしまいました。", "___をわすれてしまいました。", "___ o wasurete shimaimashita.", "I forgot my password.", "パスワード"),
            s("作った資料を___。", "つくったしりょうを___。", "Tsukutta shiryō o ___.", "I save the document I made.", "保存する"),
            s("___が壊れたので、打てません。", "___がこわれたので、うてません。", "___ ga kowareta node, utemasen.", "The keyboard is broken, so I can't type.", "キーボード"),
            s("知らない言葉をネットで___。", "しらないことばをねっとで___。", "Shiranai kotoba o netto de ___.", "I search online for words I don't know.", "検索する"),
        ],
    },
    "smartphones-apps": {
        "vocab": [
            v("スマホ", "すまほ", "sumaho", "smartphone"),
            v("アプリ", "あぷり", "apuri", "app"),
            v("メッセージ", "めっせーじ", "messēji", "message"),
            v("通知", "つうち", "tsūchi", "notification"),
            v("充電器", "じゅうでんき", "jūdenki", "charger"),
            v("電池", "でんち", "denchi", "battery"),
            v("動画", "どうが", "dōga", "video"),
            v("ダウンロードする", "ダウンロードする", "daunrōdo suru", "to download"),
            v("電源", "でんげん", "dengen", "power (switch)"),
            v("電話番号", "でんわばんごう", "denwa bangō", "phone number"),
            v("無料", "むりょう", "muryō", "free of charge"),
        ],
        "sentences": [
            s("___で写真を撮りました。", "___でしゃしんをとりました。", "___ de shashin o torimashita.", "I took a photo with my smartphone.", "スマホ"),
            s("新しい___を入れました。", "あたらしい___をいれました。", "Atarashii ___ o iremashita.", "I installed a new app.", "アプリ"),
            s("友達から___が来ました。", "ともだちから___がきました。", "Tomodachi kara ___ ga kimashita.", "A message came from my friend.", "メッセージ"),
            s("___がなくなりそうです。", "___がなくなりそうです。", "___ ga nakunari sō desu.", "The battery is about to run out.", "電池"),
            s("家に___を忘れました。", "いえに___をわすれました。", "Ie ni ___ o wasuremashita.", "I left my charger at home.", "充電器"),
            s("___を見ながらご飯を食べます。", "___をみながらごはんをたべます。", "___ o minagara gohan o tabemasu.", "I eat while watching a video.", "動画"),
            s("このアプリは___です。", "このあぷりは___です。", "Kono apuri wa ___ desu.", "This app is free.", "無料"),
        ],
    },
    "health-doctor": {
        "vocab": pd("Health & Body", ["医者", "看護師", "患者", "熱", "薬", "風邪をひく", "咳が出る", "病気になる", "注射", "錠剤", "健康", "血圧"]),
        "sentences": [
            s("具合が悪いので、___に診てもらいます。", "ぐあいがわるいので、___にみてもらいます。", "Guai ga warui node, ___ ni mite moraimasu.", "I feel unwell, so I'll see a doctor.", "医者"),
            s("今日は___があります。", "きょうは___があります。", "Kyō wa ___ ga arimasu.", "I have a fever today.", "熱"),
            s("___を飲んで、寝ます。", "___をのんで、ねます。", "___ o nonde, nemasu.", "I take medicine and go to bed.", "薬"),
            s("冬は___ことが多いです。", "ふゆは___ことがおおいです。", "Fuyu wa ___ koto ga ōi desu.", "In winter I often catch a cold.", "風邪をひく"),
            s("夜になると、___。", "よるになると、___。", "Yoru ni naru to, ___.", "At night, I cough.", "咳が出る"),
            s("___はとても大切です。", "___はとてもたいせつです。", "___ wa totemo taisetsu desu.", "Health is very important.", "健康"),
            s("___は痛いです。", "___はいたいです。", "___ wa itai desu.", "Injections hurt.", "注射"),
        ],
    },
    "the-environment": {
        "vocab": pd("Environment & Nature", ["空気", "公害", "太陽エネルギー", "風力", "電気自動車", "海", "川", "草", "庭", "嵐", "稲妻", "静か"]),
        "sentences": [
            s("山の___はきれいです。", "やまの___はきれいです。", "Yama no ___ wa kirei desu.", "The mountain air is clean.", "空気"),
            s("工場の___が問題になっています。", "こうじょうの___がもんだいになっています。", "Kōjō no ___ ga mondai ni natte imasu.", "Pollution from factories has become a problem.", "公害"),
            s("___は環境にやさしいです。", "___はかんきょうにやさしいです。", "___ wa kankyō ni yasashii desu.", "Electric cars are kind to the environment.", "電気自動車"),
            s("夏は___で泳ぎます。", "なつは___でおよぎます。", "Natsu wa ___ de oyogimasu.", "In summer I swim in the ocean.", "海"),
            s("私の家の近くに___があります。", "わたしのいえのちかくに___があります。", "Watashi no ie no chikaku ni ___ ga arimasu.", "There is a river near my house.", "川"),
            s("___は自然のエネルギーです。", "___はしぜんのえねるぎーです。", "___ wa shizen no enerugī desu.", "Solar energy is a natural energy source.", "太陽エネルギー"),
            s("昨日の夜は___でした。", "きのうのよるは___でした。", "Kinō no yoru wa ___ deshita.", "Last night was a thunderstorm.", "嵐"),
        ],
    },
    # ---------------------------------------------- Section 7: Grammar Foundations
    "particles-wa-ga-o": {
        "vocab": [
            v("は", "は", "wa", "topic marker (\"as for...\")"),
            v("が", "が", "ga", "subject marker"),
            v("を", "を", "o", "object marker"),
            v("の", "の", "no", "possessive (\"'s\", \"of\")"),
            v("も", "も", "mo", "\"also, too\""),
            v("と", "と", "to", "\"and, with\""),
        ],
        "sentences": [
            s("私___学生です。", "わたし___がくせいです。", "Watashi ___ gakusei desu.", "I am a student.", "は"),
            s("誰___来ましたか。", "だれ___きましたか。", "Dare ___ kimashita ka.", "Who came?", "が"),
            s("水___飲みます。", "みず___のみます。", "Mizu ___ nomimasu.", "I drink water.", "を"),
            s("これは私___本です。", "これはわたし___ほんです。", "Kore wa watashi ___ hon desu.", "This is my book.", "の"),
            s("私___行きます。", "わたし___いきます。", "Watashi ___ ikimasu.", "I'll go too.", "も"),
            s("友達___映画を見ます。", "ともだち___えいがをみます。", "Tomodachi ___ eiga o mimasu.", "I watch a movie with a friend.", "と"),
        ],
    },
    "particles-ni-de-e": {
        "vocab": [
            v("に", "に", "ni", "at (a time), to, in (existence)"),
            v("で", "で", "de", "at (where an action happens), by means of"),
            v("へ", "へ", "e", "toward (a direction)"),
            v("から", "から", "kara", "from"),
            v("まで", "まで", "made", "until, as far as"),
            v("より", "より", "yori", "than"),
        ],
        "sentences": [
            s("七時___起きます。", "しちじ___おきます。", "Shichiji ___ okimasu.", "I get up at seven.", "に"),
            s("図書館___勉強します。", "としょかん___べんきょうします。", "Toshokan ___ benkyō shimasu.", "I study at the library.", "で"),
            s("学校___行きます。", "がっこう___いきます。", "Gakkō ___ ikimasu.", "I go to school.", "へ"),
            s("九時___五時まで働きます。", "くじ___ごじまではたらきます。", "Kuji ___ goji made hatarakimasu.", "I work from nine to five.", "から"),
            s("月曜日から金曜日___です。", "げつようびからきんようび___です。", "Getsuyōbi kara kin'yōbi ___ desu.", "It's Monday through Friday.", "まで"),
            s("私は兄___背が低いです。", "わたしはあに___せがひくいです。", "Watashi wa ani ___ se ga hikui desu.", "I am shorter than my older brother.", "より"),
        ],
    },
    "adjectives-opposites-rm": {
        "vocab": [
            v("大きい", "おおきい", "ōkii", "big"),
            v("小さい", "ちいさい", "chiisai", "small"),
            v("新しい", "あたらしい", "atarashii", "new"),
            v("古い", "ふるい", "furui", "old (things)"),
            v("長い", "ながい", "nagai", "long"),
            v("短い", "みじかい", "mijikai", "short (length)"),
            v("速い", "はやい", "hayai", "fast"),
            v("遅い", "おそい", "osoi", "slow, late"),
            v("難しい", "むずかしい", "muzukashii", "difficult"),
            v("忙しい", "いそがしい", "isogashii", "busy"),
            v("嬉しい", "うれしい", "ureshii", "happy, glad"),
            v("悲しい", "かなしい", "kanashii", "sad"),
        ],
        "sentences": [
            s("この犬は___です。", "このいぬは___です。", "Kono inu wa ___ desu.", "This dog is big.", "大きい"),
            s("___家に引っ越しました。", "___いえにひっこしました。", "___ ie ni hikkoshimashita.", "I moved into a new house.", "新しい"),
            s("この道は___です。", "このみちは___です。", "Kono michi wa ___ desu.", "This road is long.", "長い"),
            s("この電車はとても___です。", "このでんしゃはとても___です。", "Kono densha wa totemo ___ desu.", "This train is very fast.", "速い"),
            s("日本語の漢字は___です。", "にほんごのかんじは___です。", "Nihongo no kanji wa ___ desu.", "Japanese kanji are difficult.", "難しい"),
            s("合格して、とても___です。", "ごうかくして、とても___です。", "Gōkaku shite, totemo ___ desu.", "I passed, and I'm very happy.", "嬉しい"),
            s("今週はとても___です。", "こんしゅうはとても___です。", "Konshū wa totemo ___ desu.", "I'm very busy this week.", "忙しい"),
        ],
    },
    "counters-rm": {
        "vocab": [
            v("一つ", "ひとつ", "hitotsu", "one thing (general)"),
            v("二人", "ふたり", "futari", "two people"),
            v("三枚", "さんまい", "sanmai", "three flat things"),
            v("二本", "にほん", "nihon", "two long thin things"),
            v("一台", "いちだい", "ichidai", "one machine or vehicle"),
            v("二杯", "にはい", "nihai", "two cups or glasses"),
            v("三匹", "さんびき", "sanbiki", "three small animals"),
            v("一冊", "いっさつ", "issatsu", "one book"),
            v("五個", "ごこ", "goko", "five small objects"),
        ],
        "sentences": [
            s("友達が___来ました。", "ともだちが___きました。", "Tomodachi ga ___ kimashita.", "Two friends came.", "二人"),
            s("紙を___ください。", "かみを___ください。", "Kami o ___ kudasai.", "Please give me three sheets of paper.", "三枚"),
            s("お茶を___ください。", "おちゃを___ください。", "Ocha o ___ kudasai.", "Two cups of tea, please.", "二杯"),
            s("庭に犬が___います。", "にわにいぬが___います。", "Niwa ni inu ga ___ imasu.", "There are three dogs in the garden.", "三匹"),
            s("この店で本を___買いました。", "このみせでほんを___かいました。", "Kono mise de hon o ___ kaimashita.", "I bought one book at this shop.", "一冊"),
            s("りんごを___食べました。", "りんごを___たべました。", "Ringo o ___ tabemashita.", "I ate five apples.", "五個"),
            s("駐車場に車が___あります。", "ちゅうしゃじょうにくるまが___あります。", "Chūshajō ni kuruma ga ___ arimasu.", "There is one car in the parking lot.", "一台"),
        ],
    },
    "sentence-patterns": {
        "vocab": [
            v("たいです", "たいです", "tai desu", "want to (do)"),
            v("ませんか", "ませんか", "masen ka", "won't you...? (invitation)"),
            v("ましょう", "ましょう", "mashō", "let's..."),
            v("てください", "てください", "te kudasai", "please do..."),
            v("ています", "ています", "te imasu", "is doing..."),
            v("ません", "ません", "masen", "does not..."),
            v("ました", "ました", "mashita", "did..."),
            v("てもいいですか", "てもいいですか", "te mo ii desu ka", "may I...?"),
        ],
        "sentences": [
            s("お茶が飲み___。", "おちゃがのみ___。", "Ocha ga nomi ___.", "I want to drink tea.", "たいです"),
            s("一緒に映画を見に行き___。", "いっしょにえいがをみにいき___。", "Issho ni eiga o mi ni iki ___.", "Won't you go to see a movie with me?", "ませんか"),
            s("そろそろ帰り___。", "そろそろかえり___。", "Sorosoro kaeri ___.", "Let's head home soon.", "ましょう"),
            s("ここに名前を書い___。", "ここになまえをかい___。", "Koko ni namae o kai ___.", "Please write your name here.", "てください"),
            s("今、勉強し___。", "いま、べんきょうし___。", "Ima, benkyō shi ___.", "I'm studying now.", "ています"),
            s("私は肉を食べ___。", "わたしはにくをたべ___。", "Watashi wa niku o tabe ___.", "I don't eat meat.", "ません"),
            s("昨日、友達に会い___。", "きのう、ともだちにあい___。", "Kinō, tomodachi ni ai ___.", "Yesterday I met a friend.", "ました"),
            s("ここで写真を撮っ___。", "ここでしゃしんをとっ___。", "Koko de shashin o tot ___.", "May I take a photo here?", "てもいいですか"),
        ],
    },
    "te-form-basics": {
        "vocab": [
            v("食べて", "たべて", "tabete", "eat (て-form)"),
            v("飲んで", "のんで", "nonde", "drink (て-form)"),
            v("見て", "みて", "mite", "look, watch (て-form)"),
            v("行って", "いって", "itte", "go (て-form)"),
            v("来て", "きて", "kite", "come (て-form)"),
            v("書いて", "かいて", "kaite", "write (て-form)"),
            v("聞いて", "きいて", "kiite", "listen, ask (て-form)"),
            v("待って", "まって", "matte", "wait (て-form)"),
            v("話して", "はなして", "hanashite", "speak (て-form)"),
            v("帰って", "かえって", "kaette", "go home (て-form)"),
            v("して", "して", "shite", "do (て-form)"),
        ],
        "sentences": [
            s("ご飯を___ください。", "ごはんを___ください。", "Gohan o ___ kudasai.", "Please eat your meal.", "食べて"),
            s("水を___ください。", "みずを___ください。", "Mizu o ___ kudasai.", "Please drink some water.", "飲んで"),
            s("ここで少し___ください。", "ここですこし___ください。", "Koko de sukoshi ___ kudasai.", "Please wait here a moment.", "待って"),
            s("この字を___ください。", "このじを___ください。", "Kono ji o ___ kudasai.", "Please write this character.", "書いて"),
            s("ゆっくり___ください。", "ゆっくり___ください。", "Yukkuri ___ kudasai.", "Please speak slowly.", "話して"),
            s("早く家に___ください。", "はやくいえに___ください。", "Hayaku ie ni ___ kudasai.", "Please come home early.", "帰って"),
            s("こちらを___ください。", "こちらを___ください。", "Kochira o ___ kudasai.", "Please take a look at this.", "見て"),
        ],
    },
    "potential-form": {
        "vocab": [
            v("食べられる", "たべられる", "taberareru", "can eat"),
            v("飲める", "のめる", "nomeru", "can drink"),
            v("行ける", "いける", "ikeru", "can go"),
            v("読める", "よめる", "yomeru", "can read"),
            v("書ける", "かける", "kakeru", "can write"),
            v("話せる", "はなせる", "hanaseru", "can speak"),
            v("泳げる", "およげる", "oyogeru", "can swim"),
            v("作れる", "つくれる", "tsukureru", "can make"),
            v("見られる", "みられる", "mirareru", "can see"),
            v("来られる", "こられる", "korareru", "can come"),
            v("できる", "できる", "dekiru", "can do"),
        ],
        "sentences": [
            s("私は漢字が___。", "わたしはかんじが___。", "Watashi wa kanji ga ___.", "I can write kanji.", "書ける"),
            s("私は日本語が少し___。", "わたしはにほんごがすこし___。", "Watashi wa nihongo ga sukoshi ___.", "I can speak a little Japanese.", "話せる"),
            s("私は辛い料理が___。", "わたしはからいりょうりが___。", "Watashi wa karai ryōri ga ___.", "I can eat spicy food.", "食べられる"),
            s("弟は速く___。", "おとうとははやく___。", "Otōto wa hayaku ___.", "My younger brother can swim fast.", "泳げる"),
            s("明日は一緒に___。", "あしたはいっしょに___。", "Ashita wa issho ni ___.", "Tomorrow I can go together.", "行ける"),
            s("姉は上手に料理が___。", "あねはじょうずにりょうりが___。", "Ane wa jōzu ni ryōri ga ___.", "My older sister can cook well.", "できる"),
            s("この漢字は私にも___。", "このかんじはわたしにも___。", "Kono kanji wa watashi ni mo ___.", "I can read this kanji too.", "読める"),
        ],
    },
    # --------------------------------------------- Section 8: Toward Fluency
    "countries-nationalities": {
        "vocab": pd("Countries", ["韓国", "中国", "インド", "イタリア", "オーストラリア", "カナダ", "フランス", "ドイツ", "イギリス", "ロシア", "スイス", "タイ"]),
        "sentences": [
            s("ピザは___の料理です。", "ぴざは___のりょうりです。", "Piza wa ___ no ryōri desu.", "Pizza is a dish from Italy.", "イタリア"),
            s("___の首都はパリです。", "___のしゅとはぱりです。", "___ no shuto wa Pari desu.", "The capital of France is Paris.", "フランス"),
            s("私の友達は___から来ました。", "わたしのともだちは___からきました。", "Watashi no tomodachi wa ___ kara kimashita.", "My friend came from Canada.", "カナダ"),
            s("___の首都はベルリンです。", "___のしゅとはべるりんです。", "___ no shuto wa Berurin desu.", "The capital of Germany is Berlin.", "ドイツ"),
            s("___は人口が多い国です。", "___はじんこうがおおいくにです。", "___ wa jinkō ga ōi kuni desu.", "India is a country with a large population.", "インド"),
            s("___はカンガルーで有名です。", "___はかんがるーでゆうめいです。", "___ wa kangarū de yūmei desu.", "Australia is famous for kangaroos.", "オーストラリア"),
        ],
    },
    "foreign-languages-travel": {
        "vocab": pd("Languages", ["英語", "フランス語", "スペイン語"]) + pd("Travel", ["ホテル", "地図", "旅行者", "荷物", "パスポート", "観光地", "搭乗券", "カメラ", "スーツケース"]),
        "sentences": [
            s("私は___が少し話せます。", "わたしは___がすこしはなせます。", "Watashi wa ___ ga sukoshi hanasemasu.", "I can speak a little English.", "英語"),
            s("___を予約しました。", "___をよやくしました。", "___ o yoyaku shimashita.", "I booked a hotel.", "ホテル"),
            s("___を見せてください。", "___をみせてください。", "___ o misete kudasai.", "Please show me your passport.", "パスポート"),
            s("この___は重いです。", "この___はおもいです。", "Kono ___ wa omoi desu.", "This suitcase is heavy.", "スーツケース"),
            s("この町の有名な___は古いお寺です。", "このまちのゆうめいな___はふるいおてらです。", "Kono machi no yūmei na ___ wa furui otera desu.", "This town's famous tourist spot is an old temple.", "観光地"),
            s("___は空港でもらいます。", "___はくうこうでもらいます。", "___ wa kūkō de moraimasu.", "You get your boarding pass at the airport.", "搭乗券"),
            s("旅の思い出に___で写真を撮ります。", "たびのおもいでに___でしゃしんをとります。", "Tabi no omoide ni ___ de shashin o torimasu.", "I take photos with a camera as travel memories.", "カメラ"),
        ],
    },
}


GUIDES = {
    "particles-wa-ga-o": {
        "intro": "Particles are tiny words that come right after a word and tell you its job in the sentence. Japanese puts them after the word, not before it.",
        "points": [
            {"pattern": "は (wa)", "note": "Marks the topic: what the sentence is about.", "jp": "私は学生です。", "en": "As for me, I'm a student."},
            {"pattern": "が (ga)", "note": "Marks the subject, often new information or a question word.", "jp": "誰が来ましたか。", "en": "Who came?"},
            {"pattern": "を (o)", "note": "Marks what an action is done to.", "jp": "水を飲みます。", "en": "I drink water."},
            {"pattern": "の (no)", "note": "Links two nouns, like 's or of.", "jp": "私の本", "en": "my book"},
            {"pattern": "も (mo)", "note": "Means also or too, and takes the place of は, が or を.", "jp": "私も行きます。", "en": "I'll go too."},
            {"pattern": "と (to)", "note": "Means and, or together with.", "jp": "友達と行きます。", "en": "I go with a friend."},
        ],
    },
    "particles-ni-de-e": {
        "intro": "These particles answer where and when. The tricky pair is に and で: に points at a place you arrive or exist in, で is where an action takes place.",
        "points": [
            {"pattern": "に (ni)", "note": "A point in time, or a destination or place of existence.", "jp": "七時に起きます。", "en": "I get up at seven."},
            {"pattern": "で (de)", "note": "Where an action happens, or the means you use.", "jp": "図書館で勉強します。", "en": "I study at the library."},
            {"pattern": "へ (e)", "note": "Direction of movement. Written へ, spoken \"e\".", "jp": "学校へ行きます。", "en": "I go to school."},
            {"pattern": "から / まで", "note": "From and until, for both time and place.", "jp": "九時から五時まで", "en": "from nine until five"},
            {"pattern": "より (yori)", "note": "Used to compare: than.", "jp": "私は兄より背が低いです。", "en": "I'm shorter than my brother."},
        ],
    },
    "adjectives-opposites-rm": {
        "intro": "Learning adjectives in opposite pairs is the fastest way to remember them. Every adjective here is an い-adjective: it ends in い and can sit right before a noun.",
        "points": [
            {"pattern": "い-adjective + noun", "note": "Put the adjective straight in front of the noun.", "jp": "新しい家", "en": "a new house"},
            {"pattern": "い-adjective + です", "note": "Adding です makes it polite and complete.", "jp": "この犬は大きいです。", "en": "This dog is big."},
            {"pattern": "〜くないです", "note": "Drop the final い and add くないです to say it isn't so.", "jp": "大きくないです。", "en": "It isn't big."},
            {"pattern": "Opposite pairs", "note": "大きい ↔ 小さい, 新しい ↔ 古い, 長い ↔ 短い, 速い ↔ 遅い, 嬉しい ↔ 悲しい.", "jp": "", "en": ""},
        ],
    },
    "counters-rm": {
        "intro": "Japanese counts things with a number plus a small counter word that depends on what you are counting. Some numbers change sound when they meet a counter, so learn each phrase as a whole.",
        "points": [
            {"pattern": "〜人 (nin)", "note": "People. One and two are special: ひとり, ふたり.", "jp": "二人", "en": "two people"},
            {"pattern": "〜枚 (mai)", "note": "Flat things: paper, tickets, shirts.", "jp": "三枚", "en": "three sheets"},
            {"pattern": "〜本 (hon)", "note": "Long thin things. The sound shifts: いっぽん, にほん, さんぼん.", "jp": "二本", "en": "two long things"},
            {"pattern": "〜匹 / 〜杯 / 〜冊 / 〜台 / 〜個", "note": "Small animals, cups of drink, books, machines, small round things.", "jp": "三匹", "en": "three small animals"},
            {"pattern": "Where the counter goes", "note": "It comes right after the noun and its particle, before the verb.", "jp": "お茶を二杯ください。", "en": "Two cups of tea, please."},
        ],
    },
    "sentence-patterns": {
        "intro": "Much of everyday Japanese is a verb stem plus a small ending. The stem is the polite ます-form without ます: 飲みます becomes 飲み.",
        "points": [
            {"pattern": "stem + たいです", "note": "I want to do it.", "jp": "お茶が飲みたいです。", "en": "I want to drink tea."},
            {"pattern": "stem + ませんか", "note": "A polite invitation.", "jp": "一緒に行きませんか。", "en": "Won't you come along?"},
            {"pattern": "stem + ましょう", "note": "Let's do it.", "jp": "帰りましょう。", "en": "Let's go home."},
            {"pattern": "て-form + ください", "note": "Please do it.", "jp": "書いてください。", "en": "Please write it."},
            {"pattern": "て-form + います", "note": "Is doing it right now.", "jp": "勉強しています。", "en": "I'm studying."},
            {"pattern": "て-form + もいいですか", "note": "May I do it?", "jp": "撮ってもいいですか。", "en": "May I take one?"},
        ],
    },
    "te-form-basics": {
        "intro": "The て-form joins actions, makes requests and unlocks many patterns. You build it from the dictionary form, and the ending decides how.",
        "points": [
            {"pattern": "る-verbs: drop る, add て", "note": "The simplest group.", "jp": "食べる → 食べて", "en": "eat"},
            {"pattern": "う / つ / る → って", "note": "The ending becomes a small っ plus て.", "jp": "待つ → 待って, 帰る → 帰って", "en": "wait, go home"},
            {"pattern": "む / ぶ / ぬ → んで", "note": "The ending becomes ん plus で.", "jp": "飲む → 飲んで", "en": "drink"},
            {"pattern": "く → いて, す → して", "note": "The ending changes, and 行く is the exception: 行って.", "jp": "書く → 書いて, 話す → 話して", "en": "write, speak"},
            {"pattern": "Irregular verbs", "note": "Only two.", "jp": "する → して, 来る → 来て", "en": "do, come"},
        ],
    },
    "potential-form": {
        "intro": "The potential form means can do. It works like a new verb, and the thing you can do usually takes が instead of を.",
        "points": [
            {"pattern": "る-verbs: add られる", "note": "Drop る and add られる.", "jp": "食べる → 食べられる", "en": "can eat"},
            {"pattern": "う-verbs: last sound u → e, then る", "note": "Change the final kana to its え-row partner and add る.", "jp": "書く → 書ける, 話す → 話せる", "en": "can write, can speak"},
            {"pattern": "Irregular verbs", "note": "する uses a different verb entirely.", "jp": "する → できる, 来る → 来られる", "en": "can do, can come"},
            {"pattern": "が instead of を", "note": "What you can do is usually marked with が.", "jp": "漢字が書ける。", "en": "I can write kanji."},
        ],
    },
}


def apply_lessons():
    ids = {c["id"]: c for sec in SECTIONS for c in sec["chapters"]}
    for cid, content in LESSONS.items():
        ch = ids[cid]
        ch["kind"] = "lesson"
        ch["vocab"] = content["vocab"]
        ch["sentences"] = content["sentences"]
        if cid in GUIDES:
            ch["guide"] = GUIDES[cid]
        # every blank must be one of the chapter's own vocab words
        words = {x["jp"] for x in ch["vocab"]}
        for sent in ch["sentences"]:
            assert sent["blank"] in words, (cid, sent["blank"])
            assert "___" in sent["jp"], (cid, sent["jp"])


apply_lessons()

def apply_v29():
    """v2.9: fuller word lists, Radicals section, new grammar chapters,
    Grand Review. See roadmap_extra.py."""
    import roadmap_extra as X
    ids = {c["id"]: c for sec in SECTIONS for c in sec["chapters"]}
    for cid, block in X.EXTRA_VOCAB.items():
        ch = ids[cid]
        have = {w["jp"] for w in ch["vocab"]}
        for w in block if isinstance(block, list) else X.parse(block):
            if w["jp"] not in have:
                ch["vocab"].append(w)
                have.add(w["jp"])
    # new grammar chapters go at the end of Grammar Foundations
    gram = next(sec for sec in SECTIONS if sec["id"] == "grammar-foundations")
    existing = {c["id"] for c in gram["chapters"]}
    for ch in X.NEW_GRAMMAR:
        if ch["id"] not in existing:
            gram["chapters"].append(ch)
    for ch in X.NEW_GRAMMAR:
        words = {w["jp"] for w in ch["vocab"]}
        for sent in ch["sentences"]:
            assert sent["blank"] in words, (ch["id"], sent["blank"])
            assert "___" in sent["jp"], (ch["id"], sent["jp"])
    # Radicals: right after First Steps (kana first, then radicals, then the rest)
    if not any(sec["id"] == "radicals" for sec in SECTIONS):
        SECTIONS.insert(1, X.build_radical_section(None))
    for sec in SECTIONS:
        if sec["id"] == "radicals":
            for ch in sec["chapters"]:
                if ch["kind"] == "lesson":
                    words = {w["jp"] for w in ch["vocab"]}
                    for sent in ch["sentences"]:
                        assert sent["blank"] in words, (ch["id"], sent["blank"])
    # Hiragana / Katakana practice chapters (MCQ with instant feedback) sit
    # right after the two chart links at the top of First Steps
    first = next(sec for sec in SECTIONS if sec["id"] == "first-steps")
    if not any(c.get("kana") for c in first["chapters"]):
        kana = X.build_kana_chapters()
        chs = first["chapters"]
        i_h = next(i for i, c in enumerate(chs) if c["id"] == "hiragana")
        chs[i_h + 1:i_h + 1] = kana["hiragana"]
        i_k = next(i for i, c in enumerate(chs) if c["id"] == "katakana")
        chs[i_k + 1:i_k + 1] = kana["katakana"]
    # a 50-question Section Review closes every section
    for sec in SECTIONS:
        if sec["id"] != "grand-review" and not any(c["kind"] == "review" for c in sec["chapters"]):
            sec["chapters"].append({"id": sec["id"] + "-review", "title": sec["title"] + " — Section Review",
                                    "icon": "🏁", "kind": "review", "count": 50, "scope": sec["id"]})
    if not any(sec["id"] == "grand-review" for sec in SECTIONS):
        SECTIONS.append(X.GRAND_REVIEW_SECTION)
    # one jp string must not carry two different meanings inside a chapter
    for sec in SECTIONS:
        for ch in sec["chapters"]:
            seen = {}
            for w in ch.get("vocab", []):
                assert w["jp"] not in seen, ("duplicate in chapter", ch["id"], w["jp"])
                seen[w["jp"]] = w["meaning"]


apply_v29()


if __name__ == "__main__":
    with open("data/roadmap.json", "w", encoding="utf-8") as f:
        json.dump(SECTIONS, f, ensure_ascii=False, indent=2)

    total = sum(len(sec["chapters"]) for sec in SECTIONS)
    lessons = sum(1 for sec in SECTIONS for c in sec["chapters"] if c["kind"] == "lesson")
    links = sum(1 for sec in SECTIONS for c in sec["chapters"] if c["kind"] == "link")
    placeholders = total - lessons - links
    print(f"sections: {len(SECTIONS)}, chapters: {total} "
          f"(lesson: {lessons}, link: {links}, placeholder: {placeholders})")
