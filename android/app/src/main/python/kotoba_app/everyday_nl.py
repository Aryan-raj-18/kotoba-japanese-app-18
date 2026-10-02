# -*- coding: utf-8 -*-
"""
Natural-sounding example sentences and mini-conversations for the Everyday
Life word list (v2.9).

The old builder dropped every word into one template per category, which
gave sentences like 「田中さんのくじらです」 or 「駅は内の方です」. This module first
CLASSIFIES each word (is it really a drink? a body part? a verb? an
adjective?) and only uses a specific pattern when the word actually fits it.
Anything that does not fit falls back to one of a few neutral patterns that
are grammatical for any noun ("Let's talk about X", "I learned the word X").

Sentence patterns follow everyday textbook usage: ~ことができます, ~が好きです,
~を飲みます, ~がいます / あります, ~について, etc.
"""
import re

# ----------------------------------------------------------------- helpers --

def cap(s):
    return s[:1].upper() + s[1:] if s else s


def clean_meaning(meaning):
    """'to take' -> 'take'; 'friend, friends' -> 'friend';
    'silver (color)' -> 'silver'; 'is black' -> 'black'."""
    m = meaning.strip()
    m = re.sub(r"\s*\([^)]*\)?", "", m)          # drop (...) notes, even unbalanced
    m = m.split(",")[0].split(";")[0].split(" / ")[0].strip()
    m = re.sub(r"^(to|is|are)\s+", "", m, flags=re.I).strip()
    m = m.rstrip(")").strip()
    if len(m) > 1 and m[0].isupper() and m[1].islower() and " " not in m and m[0] != "I":
        m = m[0].lower() + m[1:]
    return m or meaning.strip()


def _dir(en):
    """English for a position word: 'east' -> 'to the east', 'front' -> 'at the front',
    anything else -> 'in the "next to" position' so it never reads as broken grammar."""
    if en in ("east", "west", "south", "north", "left", "right"):
        return f"to the {en}"
    if en in ("front", "back", "middle", "corner", "top", "bottom", "side", "center"):
        return f"at the {en}"
    return f"in the \u201c{en}\u201d position"


def article(word):
    w = word.strip()
    low = w.lower()
    if low in MASS or low.endswith("s") or " and " in low:
        return w
    return ("an " if low[:1] in "aeiou" else "a ") + w


MASS = {"bread", "rice", "cheese", "milk", "coffee", "juice", "tea", "meat", "water", "sugar",
        "salt", "butter", "change", "money", "software", "information", "beef", "pork", "ice cream", "curry", "soup", "fish", "chicken",
        "beer", "wine", "sake", "cola", "soda", "oil", "vinegar", "miso", "soy sauce"}


def words(m):
    return set(re.findall(r"[a-z']+", m.lower()))


DRINKS = {"tea", "coffee", "juice", "milk", "water", "beer", "wine", "sake", "cola", "soda",
          "drink", "liquor", "alcohol", "whisky", "whiskey", "cocktail", "lemonade", "smoothie"}
SEASONINGS = {"salt", "sugar", "pepper", "sauce", "oil", "vinegar", "miso", "seasoning", "spice",
              "mayonnaise", "ketchup", "mustard", "wasabi", "honey"}
BODY = {"head", "face", "neck", "shoulder", "arm", "chest", "stomach", "belly", "back", "leg",
        "foot", "feet", "hand", "finger", "eye", "ear", "nose", "mouth", "tooth", "teeth",
        "tongue", "throat", "knee", "waist", "thigh", "elbow", "heart", "hair", "lip", "lips",
        "wrist", "ankle", "toe", "cheek", "chin", "forehead", "body", "skin", "bone", "hip"}
PEOPLE_FAMILY = {"mother", "father", "brother", "sister", "son", "daughter", "husband", "wife",
                 "parent", "parents", "child", "children", "grandfather", "grandmother", "uncle",
                 "aunt", "family", "relative", "relatives", "cousin", "friend", "baby", "grandchild",
                 "grandson", "granddaughter", "nephew", "niece"}
SCENERY = {"sky", "sea", "ocean", "mountain", "river", "flower", "flowers", "moon", "sun", "snow",
           "star", "stars", "forest", "lake", "blossoms", "blossom", "garden", "view", "rainbow",
           "scenery", "clouds", "cloud", "waterfall", "beach", "field", "tree", "trees", "pond"}
VEHICLES = {"train", "bus", "taxi", "bicycle", "bike", "car", "plane", "airplane", "ship", "subway",
            "motorcycle", "shinkansen", "ferry", "boat", "tram", "helicopter"}
HOLIDAY = {"day", "festival", "holiday", "season", "spring", "summer", "autumn", "fall", "winter",
           "year", "obon", "week", "christmas", "birthday", "vacation", "break"}
TRAVEL_ITEMS = {"luggage", "passport", "camera", "map", "ticket", "bag", "suitcase", "baggage",
                "visa", "guidebook", "umbrella", "wallet", "money", "souvenir", "souvenirs"}
NATURE_CARE = {"environment", "nature", "forest", "river", "sea", "ocean", "mountain", "air", "earth",
               "water", "tree", "trees", "resources", "planet", "wildlife", "animals", "plants"}
DIRECTIONS = {"east", "west", "south", "north", "left", "right", "above", "below", "front", "back",
              "behind", "inside", "outside", "middle", "beside", "up", "down", "top", "bottom",
              "center", "centre", "corner", "opposite", "side", "next"}
SIZE_ADJ = {"big", "small", "large", "little", "long", "short", "many", "few", "wide", "narrow",
            "thick", "thin", "heavy", "light", "tall", "high", "low", "deep", "shallow", "huge",
            "tiny", "much", "vast", "broad"}
SCHOOL_SUBJ_SUFFIX = ("学", "語", "科", "史", "術", "楽", "育", "文")
PERSON_SUFFIX = ("員", "者", "士", "師", "家", "長", "官", "生", "人", "主")
PLACE_BAD = {"master", "chief", "manager", "worker", "person", "member", "staff", "principal",
             "president", "clerk", "guide", "officer", "owner"}
NUM_CHARS = set("〇一二三四五六七八九十百千万億兆円")
TIME_KEYS = {"day", "days", "morning", "evening", "night", "week", "month", "year", "tomorrow", "yesterday",
            "today", "weekend", "noon", "afternoon", "midnight", "tonight", "hour", "minute", "sunday",
            "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "now", "daytime", "dawn", "dusk"}
TIME_BAD = {"snack", "period", "meal", "years", "times", "age", "generation"}

# -------------------------------------------------------- neutral fallbacks --
NEUTRAL = [
    ("「{w}」について話しましょう。", "「{r}」についてはなしましょう。",
     "'{rm}' ni tsuite hanashimashō.", "Let's talk about \u201c{en}\u201d.",
     "A handy pattern for bringing up any topic: ～について話しましょう."),
    ("「{w}」という言葉を習いました。", "「{r}」ということばをならいました。",
     "'{rm}' to iu kotoba o naraimashita.", "I learned the word \u201c{en}\u201d.",
     "～という言葉 means 'the word ...'. Use it whenever you mention a new word."),
    ("「{w}」の意味を調べました。", "「{r}」のいみをしらべました。",
     "'{rm}' no imi o shirabemashita.", "I looked up the meaning of \u201c{en}\u201d.",
     "～の意味を調べる = 'to look up the meaning of ...'. Very common when studying."),
]


def neutral_pick(word):
    return NEUTRAL[sum(ord(c) for c in word) % len(NEUTRAL)]


# ------------------------------------------------------------ classification --
OPP_RE = re.compile(r"^(?P<a>.+?)\s*\(opposite of\s+(?P<jp>\S+)\s+(?P<rm>\S+),\s*(?P<en>[^)]+)\)\s*$", re.I)


def is_kana(s):
    return all("\u3040" <= c <= "\u30ff" or c in "ー" for c in s)


def classify(word, reading, meaning, category):
    m = meaning.strip()
    cm = clean_meaning(m)
    ws = words(cm)
    first = m[:1]

    if OPP_RE.match(m):
        return "opposite"
    # verbs: dictionary form ending in a u-row kana
    is_verb_gloss = bool(re.match(r"^to\s+\w", m, re.I)) or category == "Actions & Verbs"
    if is_verb_gloss and word[-1:] in "うくぐすつぬぶむる" and len(word) >= 2 and "(" not in m:
        return "verb"
    if category == "Counters":
        return "counter"
    if category in ("Numbers & Counting",):
        if word and all(c in NUM_CHARS or c in "つ人本枚台匹冊個回歳階杯円" for c in word):
            return "number"
        return "neutral"
    if "(" in m and ")" not in m or m.endswith(")") and "(" not in m:
        return "neutral"
    if len(cm.split()) > 3:
        return "neutral"

    if category == "Animals":
        return "animal" if not (ws & PLACE_BAD) else "neutral"
    if category == "Family & People":
        return "family" if (ws & PEOPLE_FAMILY) else "neutral"
    if category in ("Body & Health", "Health & Body"):
        return "body" if (ws & BODY) and not word.endswith(("長", "員", "者")) else "neutral"
    if category == "Places & Buildings":
        if (ws & PLACE_BAD) or word.endswith(PERSON_SUFFIX):
            return "neutral"
        return "place"
    if category == "Food & Drink":
        if ws & DRINKS:
            return "drink"
        if ws & SEASONINGS:
            return "seasoning"
        return "food"
    if category == "Directions & Position":
        return "direction" if (ws & DIRECTIONS) else "neutral"
    if category == "Colors":
        return "color_adj" if word.endswith("い") else "color"
    if category == "Size & Quantity":
        return "size_adj" if (word.endswith("い") and (ws & SIZE_ADJ)) else "neutral"
    if category == "Shapes & Sizes":
        return "shape" if word.endswith("形") and len(word) > 1 or (is_kana(word) and word.endswith("形")) else "neutral"
    if category == "Time & Calendar":
        return "time" if (ws & TIME_KEYS) and not (ws & TIME_BAD) and ")" not in m and not word.endswith("い") else "neutral"
    if category in ("Money & Shopping", "Shopping & Money"):
        return "shopping"
    if category == "Seasons & Holidays":
        return "holiday" if (ws & HOLIDAY) else "neutral"
    if category == "School & Learning":
        if word.endswith(PERSON_SUFFIX):
            return "neutral"
        return "subject" if word.endswith(SCHOOL_SUBJ_SUFFIX) else "neutral"
    if category == "Work & Jobs":
        return "job" if word.endswith(PERSON_SUFFIX) and not (ws & {"staff", "personnel", "employees", "workers"}) else "neutral"
    if category == "Environment & Nature":
        return "nature_care" if (ws & NATURE_CARE) else "neutral"
    if category == "Sports & Fitness":
        return "hobby" if not word.endswith(("靴", "着", "服")) and "shoes" not in ws and "sneakers" not in ws else "neutral"
    if category == "Travel":
        return "travel_item" if (ws & TRAVEL_ITEMS) else "neutral"
    if category == "Countries":
        return "country" if m[:1].isupper() else "neutral"
    if category == "Languages":
        return "language"
    if category in ("Music", "Hobbies & Music"):
        return "hobby"
    if category == "Transportation":
        return "vehicle" if (ws & VEHICLES) else "neutral"
    if category == "House & Furniture":
        return "house"
    if category == "Nature & Weather":
        return "scenery" if (ws & SCENERY) else "neutral"
    return "neutral"


# ------------------------------------------------------------- sentence bank --
# kind -> (kanji, hiragana, romaji, english, usage)
SENT = {
    "verb": ("{w}ことができますか。", "{r}ことができますか。", "{rm} koto ga dekimasu ka.",
             "Can you {en}?", "～ことができる = 'can do ...'. Put the dictionary form of any verb before こと."),
    "animal": ("あそこに{w}がいます。", "あそこに{r}がいます。", "Asoko ni {rm} ga imasu.",
               "There is {en_a} over there.", "Living things use います (not あります) for 'there is'."),
    "family": ("これは私の{w}です。", "これはわたしの{r}です。", "Kore wa watashi no {rm} desu.",
               "This is my {en}.", "Use this when you introduce someone in your family or a friend."),
    "body": ("{w}が痛いです。", "{r}がいたいです。", "{rm} ga itai desu.",
             "My {en} hurts.", "How to tell a doctor or a friend where it hurts: [body part]が痛いです."),
    "place": ("明日、{w}に行きます。", "あした、{r}にいきます。", "Ashita, {rm} ni ikimasu.",
              "Tomorrow I'm going to the {en}.", "に marks the destination of 行きます."),
    "food": ("昼ご飯に{w}を食べました。", "ひるごはんに{r}をたべました。", "Hirugohan ni {rm} o tabemashita.",
             "I had {en_a} for lunch.", "を marks what you eat; に marks the meal."),
    "drink": ("毎朝、{w}を飲みます。", "まいあさ、{r}をのみます。", "Maiasa, {rm} o nomimasu.",
              "I drink {en} every morning.", "Drinks take 飲む (nomu), not 食べる."),
    "seasoning": ("料理に{w}を使います。", "りょうりに{r}をつかいます。", "Ryōri ni {rm} o tsukaimasu.",
                  "I use {en} in cooking.", "Seasonings are things you 使う (use) in cooking."),
    "direction": ("駅は{w}にあります。", "えきは{r}にあります。", "Eki wa {rm} ni arimasu.",
                  "The station is {en_dir}.", "Position and direction words + にあります tell where something is."),
    "color": ("私は{w}が好きです。", "わたしは{r}がすきです。", "Watashi wa {rm} ga suki desu.",
              "I like {en}.", "Colour nouns (色) take が好きです for preferences."),
    "color_adj": ("{w}かばんを買いました。", "{r}かばんをかいました。", "{rm} kaban o kaimashita.",
                  "I bought a {en} bag.", "い-adjective colours go straight before the noun."),
    "size_adj": ("この部屋は{w}です。", "このへやは{r}です。", "Kono heya wa {rm} desu.",
                 "This room is {en}.", "い-adjectives + です describe things politely."),
    "shape": ("これは{w}です。", "これは{r}です。", "Kore wa {rm} desu.",
              "This is {en_a}.", "これは...です is the basic 'this is ...' pattern."),
    "time": ("{w}はどうですか。", "{r}はどうですか。", "{rm} wa dō desu ka.",
             "How about {en}?", "～はどうですか is the friendly way to suggest a time or a plan."),
    "shopping": ("{w}について教えてください。", "{r}についておしえてください。", "{rm} ni tsuite oshiete kudasai.",
                 "Please tell me about {en_a}.", "～について教えてください: a polite way to ask a shop assistant."),
    "holiday": ("もうすぐ{w}ですね。", "もうすぐ{r}ですね。", "Mō sugu {rm} desu ne.",
                "It will soon be {en}, won't it?", "もうすぐ = 'soon'; ですね invites the listener to agree."),
    "subject": ("学校で{w}を勉強します。", "がっこうで{r}をべんきょうします。", "Gakkō de {rm} o benkyō shimasu.",
                "I study {en} at school.", "で marks the place where the action happens."),
    "job": ("彼は{w}です。", "かれは{r}です。", "Kare wa {rm} desu.",
            "He is {en_a}.", "Use ～は...です to say someone's job."),
    "nature_care": ("{w}を大切にしましょう。", "{r}をたいせつにしましょう。", "{rm} o taisetsu ni shimashō.",
                    "Let's take care of {en}.", "～を大切にする = 'to treasure / take care of'."),
    "hobby": ("私は{w}が好きです。", "わたしは{r}がすきです。", "Watashi wa {rm} ga suki desu.",
              "I like {en}.", "が好きです is the standard pattern for hobbies and things you like."),
    "travel_item": ("旅行に{w}を持って行きます。", "りょこうに{r}をもっていきます。", "Ryokō ni {rm} o motte ikimasu.",
                    "I'll take {en} on the trip.", "持って行く = 'take (something) along'."),
    "country": ("いつか{w}に行きたいです。", "いつか{r}にいきたいです。", "Itsuka {rm} ni ikitai desu.",
                "Someday I want to go to {en}.", "～に行きたいです = 'I want to go to ...'."),
    "language": ("私は{w}を勉強しています。", "わたしは{r}をべんきょうしています。", "Watashi wa {rm} o benkyō shite imasu.",
                 "I'm studying {en}.", "ています shows an activity that is ongoing."),
    "vehicle": ("駅まで{w}で行きます。", "えきまで{r}でいきます。", "Eki made {rm} de ikimasu.",
                "I go to the station by {en}.", "で marks the means of transport; まで marks 'as far as'."),
    "house": ("これは私の{w}です。", "これはわたしの{r}です。", "Kore wa watashi no {rm} desu.",
              "This is my {en}.", "Handy for pointing out rooms and things at home."),
    "scenery": ("{w}がとてもきれいですね。", "{r}がとてもきれいですね。", "{rm} ga totemo kirei desu ne.",
                "The {en} is really beautiful, isn't it?", "Use ですね to share an impression with someone next to you."),
    "number": ("全部で{w}です。", "ぜんぶで{r}です。", "Zenbu de {rm} desu.",
               "That's {en} in total.", "全部で = 'in total'; a common answer when counting or paying."),
}


def build_sentence(word, reading, romaji, meaning, category):
    reading = reading or word
    romaji = romaji or reading
    kind = classify(word, reading, meaning, category)
    cm = clean_meaning(meaning)

    if kind == "opposite":
        mo = OPP_RE.match(meaning.strip())
        a, jp, rm, en2 = mo["a"].strip(), mo["jp"], mo["rm"], mo["en"].strip()
        a = clean_meaning(a)
        return {
            "sentence_kanji": f"「{word}」の反対は「{jp}」です。",
            "sentence_hiragana": f"「{reading}」のはんたいは「{jp}」です。",
            "sentence_romaji": cap(f"'{romaji}' no hantai wa '{jp}' ({rm}) desu."),
            "sentence_en": f"The opposite of \u201c{a}\u201d is \u201c{en2}\u201d.",
            "usage_note": "の反対 = 'the opposite of'. Learning words in opposite pairs doubles what you remember.",
        }
    if kind == "counter":
        desc = re.sub(r"\s*\(.*?\)\s*", " ", meaning).strip()
        desc = desc[:1].lower() + desc[1:] if desc else desc
        return {
            "sentence_kanji": f"物を数えるとき、「{word}」を使います。",
            "sentence_hiragana": f"ものをかぞえるとき、「{reading}」をつかいます。",
            "sentence_romaji": cap(f"Mono o kazoeru toki, '{romaji}' o tsukaimasu."),
            "sentence_en": f"When counting things, we use \u201c{word}\u201d \u2014 {desc}.",
            "usage_note": "Japanese counts different kinds of objects with different counters; pair each counter with its object type.",
        }
    if kind == "neutral":
        k, h, r_, e, u = neutral_pick(word)
    else:
        k, h, r_, e, u = SENT[kind]
    en_arg = cm
    fmt = dict(w=word, r=reading, rm=romaji, en=en_arg, en_a=article(en_arg), en_dir=_dir(en_arg))
    return {
        "sentence_kanji": k.format(**fmt),
        "sentence_hiragana": h.format(**fmt),
        "sentence_romaji": cap(r_.format(**fmt)),
        "sentence_en": cap(e.format(**fmt)),
        "usage_note": u,
    }


# ------------------------------------------------------------ conversations --
def L(sp, k, h, rm, en):
    return (sp, k, h, rm, en)


CONV = {
    "verb": [L("A", "週末、何がしたいですか。", "しゅうまつ、なにがしたいですか。", "Shūmatsu, nani ga shitai desu ka.", "What do you want to do this weekend?"),
             L("B", "{w}ことができたら、うれしいです。", "{r}ことができたら、うれしいです。", "{rm} koto ga dekitara, ureshii desu.", "I'd be happy if I could {en}.")],
    "animal": [L("A", "見て。あそこに{w}がいますよ。", "みて。あそこに{r}がいますよ。", "Mite. Asoko ni {rm} ga imasu yo.", "Look, there's {en_a} over there!"),
               L("B", "本当ですね。かわいいですね。", "ほんとうですね。かわいいですね。", "Hontō desu ne. Kawaii desu ne.", "Oh, so there is. How cute!")],
    "family": [L("A", "この方はどなたですか。", "このかたはどなたですか。", "Kono kata wa donata desu ka.", "Who is this person?"),
               L("B", "私の{w}です。", "わたしの{r}です。", "Watashi no {rm} desu.", "That's my {en}.")],
    "body": [L("A", "どうしましたか。", "どうしましたか。", "Dō shimashita ka.", "What's the matter?"),
             L("B", "昨日から、{w}が痛いんです。", "きのうから、{r}がいたいんです。", "Kinō kara, {rm} ga itain desu.", "My {en} has hurt since yesterday.")],
    "place": [L("A", "明日、どこに行きますか。", "あした、どこにいきますか。", "Ashita, doko ni ikimasu ka.", "Where are you going tomorrow?"),
              L("B", "{w}に行くつもりです。", "{r}にいくつもりです。", "{rm} ni iku tsumori desu.", "I'm planning to go to the {en}.")],
    "food": [L("A", "昼ご飯は何を食べましたか。", "ひるごはんはなにをたべましたか。", "Hirugohan wa nani o tabemashita ka.", "What did you have for lunch?"),
             L("B", "{w}を食べました。おいしかったですよ。", "{r}をたべました。おいしかったですよ。", "{rm} o tabemashita. Oishikatta desu yo.", "I had {en_a}. It was delicious.")],
    "drink": [L("A", "何か飲みますか。", "なにかのみますか。", "Nanika nomimasu ka.", "Would you like something to drink?"),
              L("B", "{w}をお願いします。", "{r}をおねがいします。", "{rm} o onegai shimasu.", "{en}, please.")],
    "seasoning": [L("A", "この料理、おいしいですね。", "このりょうり、おいしいですね。", "Kono ryōri, oishii desu ne.", "This dish is delicious."),
                  L("B", "ありがとう。{w}を少し使いました。", "ありがとう。{r}をすこしつかいました。", "Arigatō. {rm} o sukoshi tsukaimashita.", "Thanks. I used a little {en}.")],
    "direction": [L("A", "すみません、駅はどこですか。", "すみません、えきはどこですか。", "Sumimasen, eki wa doko desu ka.", "Excuse me, where is the station?"),
                  L("B", "{w}にありますよ。", "{r}にありますよ。", "{rm} ni arimasu yo.", "It's {en_dir}.")],
    "color": [L("A", "何色が好きですか。", "なにいろがすきですか。", "Nani iro ga suki desu ka.", "What colour do you like?"),
              L("B", "{w}が好きです。", "{r}がすきです。", "{rm} ga suki desu.", "I like {en}.")],
    "color_adj": [L("A", "どんなかばんがほしいですか。", "どんなかばんがほしいですか。", "Donna kaban ga hoshii desu ka.", "What kind of bag do you want?"),
                  L("B", "{w}かばんがほしいです。", "{r}かばんがほしいです。", "{rm} kaban ga hoshii desu.", "I want a {en} bag.")],
    "size_adj": [L("A", "新しい部屋はどうですか。", "あたらしいへやはどうですか。", "Atarashii heya wa dō desu ka.", "How's your new room?"),
                 L("B", "とても{w}ですよ。", "とても{r}ですよ。", "Totemo {rm} desu yo.", "It's very {en}.")],
    "shape": [L("A", "これは何の形ですか。", "これはなんのかたちですか。", "Kore wa nan no katachi desu ka.", "What shape is this?"),
              L("B", "{w}です。", "{r}です。", "{rm} desu.", "It's {en_a}.")],
    "time": [L("A", "いつ会いましょうか。", "いつあいましょうか。", "Itsu aimashō ka.", "When shall we meet?"),
             L("B", "{w}はどうですか。", "{r}はどうですか。", "{rm} wa dō desu ka.", "How about {en}?")],
    "shopping": [L("A", "いらっしゃいませ。", "いらっしゃいませ。", "Irasshaimase.", "Welcome."),
                 L("B", "すみません、{w}について教えてください。", "すみません、{r}についておしえてください。", "Sumimasen, {rm} ni tsuite oshiete kudasai.", "Excuse me, could you tell me about {en}?")],
    "holiday": [L("A", "もうすぐ{w}ですね。", "もうすぐ{r}ですね。", "Mō sugu {rm} desu ne.", "It'll soon be {en}, won't it?"),
                L("B", "そうですね。楽しみです。", "そうですね。たのしみです。", "Sō desu ne. Tanoshimi desu.", "It will. I'm looking forward to it.")],
    "subject": [L("A", "学校で何を勉強していますか。", "がっこうでなにをべんきょうしていますか。", "Gakkō de nani o benkyō shite imasu ka.", "What are you studying at school?"),
                L("B", "{w}を勉強しています。", "{r}をべんきょうしています。", "{rm} o benkyō shite imasu.", "I'm studying {en}.")],
    "job": [L("A", "あの方のお仕事は何ですか。", "あのかたのおしごとはなんですか。", "Ano kata no oshigoto wa nan desu ka.", "What does that person do?"),
            L("B", "{w}だそうです。", "{r}だそうです。", "{rm} da sō desu.", "I hear he's {en_a}.")],
    "nature_care": [L("A", "私たちにできることは何でしょうか。", "わたしたちにできることはなんでしょうか。", "Watashitachi ni dekiru koto wa nan deshō ka.", "What can we do?"),
                    L("B", "{w}を大切にすることです。", "{r}をたいせつにすることです。", "{rm} o taisetsu ni suru koto desu.", "Taking care of {en}.")],
    "hobby": [L("A", "趣味は何ですか。", "しゅみはなんですか。", "Shumi wa nan desu ka.", "What's your hobby?"),
              L("B", "{w}が好きです。", "{r}がすきです。", "{rm} ga suki desu.", "I like {en}.")],
    "travel_item": [L("A", "旅行の準備はできましたか。", "りょこうのじゅんびはできましたか。", "Ryokō no junbi wa dekimashita ka.", "Are you ready for the trip?"),
                    L("B", "はい。{w}も持って行きます。", "はい。{r}ももっていきます。", "Hai. {rm} mo motte ikimasu.", "Yes. I'll take {en} too.")],
    "country": [L("A", "どこに行きたいですか。", "どこにいきたいですか。", "Doko ni ikitai desu ka.", "Where do you want to go?"),
                L("B", "{w}に行きたいです。", "{r}にいきたいです。", "{rm} ni ikitai desu.", "I want to go to {en}.")],
    "language": [L("A", "何語を勉強していますか。", "なにごをべんきょうしていますか。", "Nanigo o benkyō shite imasu ka.", "Which language are you studying?"),
                 L("B", "{w}を勉強しています。", "{r}をべんきょうしています。", "{rm} o benkyō shite imasu.", "I'm studying {en}.")],
    "vehicle": [L("A", "駅までどうやって行きますか。", "えきまでどうやっていきますか。", "Eki made dō yatte ikimasu ka.", "How do you get to the station?"),
                L("B", "{w}で行きます。", "{r}でいきます。", "{rm} de ikimasu.", "I go by {en}.")],
    "house": [L("A", "これは何ですか。", "これはなんですか。", "Kore wa nan desu ka.", "What is this?"),
              L("B", "私の{w}です。", "わたしの{r}です。", "Watashi no {rm} desu.", "It's my {en}.")],
    "scenery": [L("A", "わあ、見てください。", "わあ、みてください。", "Wā, mite kudasai.", "Wow, look!"),
                L("B", "{w}がきれいですね。", "{r}がきれいですね。", "{rm} ga kirei desu ne.", "The {en} is beautiful, isn't it?")],
    "number": [L("A", "全部でいくつですか。", "ぜんぶでいくつですか。", "Zenbu de ikutsu desu ka.", "How many are there in total?"),
               L("B", "全部で{w}です。", "ぜんぶで{r}です。", "Zenbu de {rm} desu.", "{en} in total.")],
}
NEUTRAL_CONV = [
    [L("A", "「{w}」って何ですか。", "「{r}」ってなんですか。", "'{rm}' tte nan desu ka.", "What does \u201c{w}\u201d mean?"),
     L("B", "「{en}」という意味ですよ。", "「{en}」といういみですよ。", "'{en}' to iu imi desu yo.", "It means \u201c{en}\u201d.")],
    [L("A", "{w}について話しましょうか。", "{r}についてはなしましょうか。", "{rm} ni tsuite hanashimashō ka.", "Shall we talk about {en}?"),
     L("B", "いいですね。", "いいですね。", "Ii desu ne.", "Sounds good.")],
]


def build_conv(word, reading, romaji, meaning, category):
    reading = reading or word
    romaji = romaji or reading
    kind = classify(word, reading, meaning, category)
    cm = clean_meaning(meaning)
    if kind == "opposite":
        mo = OPP_RE.match(meaning.strip())
        a, jp, rm, en2 = clean_meaning(mo["a"]), mo["jp"], mo["rm"], mo["en"].strip()
        tmpl = [L("A", "「{w}」の反対は何ですか。", "「{r}」のはんたいはなんですか。", "'{rm}' no hantai wa nan desu ka.", "What's the opposite of \u201c" + a + "\u201d?"),
                L("B", "「" + jp + "」です。", "「" + jp + "」です。", "'" + jp + "' (" + rm + ") desu.", "It's \u201c" + en2 + "\u201d.")]
    elif kind == "counter":
        tmpl = [L("A", "これは何で数えますか。", "これはなんでかぞえますか。", "Kore wa nan de kazoemasu ka.", "What do you count this with?"),
                L("B", "「{w}」で数えます。", "「{r}」でかぞえます。", "'{rm}' de kazoemasu.", "We count it with \u201c{w}\u201d.")]
    elif kind == "neutral":
        tmpl = NEUTRAL_CONV[sum(ord(c) for c in word) % len(NEUTRAL_CONV)]
    else:
        tmpl = CONV[kind]
    fmt = dict(w=word, r=reading, rm=romaji, en=cm, en_a=article(cm), en_dir=_dir(cm))
    return [{"speaker": sp,
             "kanji": k.format(**fmt), "hiragana": h.format(**fmt),
             "romaji": cap(rm.format(**fmt)), "english": cap(en.format(**fmt))}
            for sp, k, h, rm, en in tmpl]
