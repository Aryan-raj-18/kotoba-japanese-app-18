# -*- coding: utf-8 -*-
"""
Generates data/radicals.json - every radical (bushu) used by the kanji in
the app, how each one is formed, where it sits inside a kanji, and which
kanji use it.

The set of "core" radicals (book=True) follows the radical-first approach:
learn the ~59 most productive radical *forms* first (they appear in the
large majority of everyday kanji), then read unknown kanji by spotting the
radical. All explanations, mnemonics and examples below are original
wording written for this app.

Run:  python gen_radicals.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent

# position codes -> (label, plain-English explanation)
POSITIONS = {
    "hen":     ("hen · left side",        "sits on the LEFT of the kanji"),
    "tsukuri": ("tsukuri · right side",   "sits on the RIGHT of the kanji"),
    "kanmuri": ("kanmuri · crown",        "sits on the TOP like a roof or crown"),
    "ashi":    ("ashi · legs",            "sits at the BOTTOM like legs"),
    "tare":    ("tare · hanging cover",   "hangs from the top-left and covers the rest"),
    "nyo":     ("nyō · wraps around",     "sweeps along the left and bottom"),
    "kamae":   ("kamae · enclosure",      "forms a frame that surrounds the rest"),
    "whole":   ("whole kanji",            "can stand alone or fill most of the kanji"),
}

# glyph, kana name, romaji, meaning, position, strokes, how it was formed, core?
# `forms` (optional) = related shapes of the same radical.
R = []


def rad(glyph, name, romaji, meaning, pos, strokes, origin, core=False, forms=""):
    R.append(dict(glyph=glyph, name=name, romaji=romaji, meaning=meaning,
                  position=pos, strokes=strokes, origin=origin,
                  core=core, forms=forms))


# ---- people & body -------------------------------------------------------
rad("亻", "にんべん", "ninben", "person", "hen", 2, "A squashed version of 人 (a person walking) so it fits on the left side of a kanji. Kanji with it are about people and what people do.", True, "人")
rad("人", "ひと・ひとがしら", "hito / hitogashira", "person", "kanmuri", 2, "A picture of a person seen from the side, legs apart. On top of a kanji it looks like a roof (ひとやね).", True, "亻")
rad("口", "くち・くちへん", "kuchi", "mouth", "hen", 3, "A square open mouth. It shows up in kanji about speaking, eating, naming and asking.", True)
rad("心", "こころ", "kokoro", "heart", "ashi", 4, "A picture of a heart with its chambers. Kanji with it are about feelings and thoughts.", True, "忄 ⺗")
rad("忄", "りっしんべん", "risshinben", "heart", "hen", 3, "心 stood on its side as a left-hand radical: feelings and states of mind.", True, "心")
rad("手", "て", "te", "hand", "whole", 4, "A hand with fingers and wrist. Alone it means hand.", True, "扌")
rad("扌", "てへん", "tehen", "hand", "hen", 3, "手 shortened to fit on the left. Kanji with it are actions done by hand: push, hit, hold, pick.", True, "手")
rad("目", "め", "me", "eye", "whole", 5, "An eye turned on its side and drawn upright. About seeing and looking.", True)
rad("耳", "みみ", "mimi", "ear", "whole", 6, "The outline of an ear. About hearing and listening.")
rad("足", "あし", "ashi", "foot / leg", "whole", 7, "A foot with a knee above it. About legs, feet and walking.")
rad("身", "み", "mi", "body", "whole", 7, "A side view of a body (a pregnant figure in the oldest form). About the body.")
rad("女", "おんな・おんなへん", "onna", "woman", "hen", 3, "A kneeling woman with folded arms. Appears in kanji about women, family and relatives.", True)
rad("子", "こ・こへん", "ko", "child", "whole", 3, "A baby with big head and arms. About children and learning.")
rad("力", "ちから", "chikara", "power", "tsukuri", 2, "A flexed arm muscle. About strength and effort.", True)
rad("又", "また", "mata", "again / right hand", "tsukuri", 2, "A hand reaching out. Shows in kanji about grasping and friends.")
rad("寸", "すん", "sun", "inch / measure", "ashi", 3, "A hand with a mark on the wrist to feel the pulse - a small measure. Kanji with it often relate to rules, hands and measuring.", True)
rad("首", "くび", "kubi", "neck / head", "whole", 9, "A head with hair on top. About heads and necks.")
rad("頁", "おおがい", "ōgai", "page / head", "tsukuri", 9, "A head (見 shape) on a body. Kanji with it are about the head and face.")
rad("鼻", "はな", "hana", "nose", "whole", 14, "自 (a nose pointed at oneself) plus 畀 for sound.")
rad("自", "みずから", "mizukara", "self / nose", "whole", 6, "Originally a nose - people point at their nose to say 'me'. Now means self.")
rad("肉", "にく", "niku", "meat", "whole", 6, "Sliced meat with fibres.")
rad("⺼", "にくづき", "nikuzuki", "flesh / body part", "hen", 4, "肉 squeezed into the moon shape. Kanji with it name body parts: back, chest, arm.", True, "肉 月")
rad("歹", "がつへん・かばねへん", "gatsuhen", "death / decay", "hen", 4, "A broken bone. About death and what is left over.")
rad("疒", "やまいだれ", "yamaidare", "sickness", "tare", 5, "A person lying on a bed under a roof. About illness and pain.", True)
rad("矢", "や", "ya", "arrow", "whole", 5, "An arrow with feather and tip.")
rad("老", "おいかんむり", "oikanmuri", "old age", "kanmuri", 6, "An old person with a cane.")

# ---- nature & things -----------------------------------------------------
rad("木", "き・きへん", "ki", "tree", "hen", 4, "A trunk with branches above and roots below. Kanji with it are about wood, plants and things made of wood.", True)
rad("水", "みず", "mizu", "water", "whole", 4, "Streams of flowing water.", True, "氵 氺")
rad("氵", "さんずい", "sanzui", "water", "hen", 3, "Three drops of water on the left. Kanji with it are about liquids, seas, rivers and washing.", True, "水")
rad("火", "ひ", "hi", "fire", "whole", 4, "Flames rising from a hearth.", True, "灬")
rad("灬", "れんが・れっか", "renga", "fire (dots below)", "ashi", 4, "Four flames along the bottom. Kanji with it are about heat and cooking.", True, "火")
rad("土", "つち・つちへん", "tsuchi", "earth", "hen", 3, "A little plant sprouting from the ground. About soil, land and places.", True)
rad("日", "ひ・ひへん", "hi", "sun / day", "hen", 4, "The sun as a box with a line for its glow. About days, time and brightness.")
rad("月", "つき・つきへん", "tsuki", "moon", "hen", 4, "A crescent moon. About the moon, months and time.", True)
rad("夕", "ゆう", "yū", "evening", "whole", 3, "A moon half-hidden by cloud at dusk.")
rad("山", "やま・やまへん", "yama", "mountain", "whole", 3, "Three peaks, the middle tallest.", True)
rad("川", "かわ", "kawa", "river", "whole", 3, "Three streams flowing.")
rad("石", "いし・いしへん", "ishi", "stone", "hen", 5, "A stone (口) under a cliff (厂).", True)
rad("雨", "あめ", "ame", "rain", "kanmuri", 8, "Drops falling from a cloud under the sky line. Weather kanji: snow, electricity.", True)
rad("風", "かぜ", "kaze", "wind", "whole", 9, "A sail-like frame with an insect (虫) inside - the winds carried illness.")
rad("气", "きがまえ", "kigamae", "steam / air", "kamae", 4, "Wisps of rising vapour.")
rad("艹", "くさかんむり", "kusakanmuri", "grass / plant", "kanmuri", 3, "Two sprouts (屮 屮) on top of a kanji. Kanji with it name plants, flowers, tea and herbs.", True)
rad("竹", "たけ・たけかんむり", "take", "bamboo", "kanmuri", 6, "Two bamboo stalks with leaves. Kanji with it name bamboo objects and things like counting slips.", True)
rad("米", "こめ", "kome", "rice", "hen", 6, "Grains of rice radiating from a stalk.")
rad("禾", "のぎ・のぎへん", "nogi", "grain", "hen", 5, "A plant with a heavy ear bending. About grain, crops and seasons.", True)
rad("生", "うまれる", "umareru", "life / birth", "whole", 5, "A shoot growing out of earth.")
rad("田", "た", "ta", "rice field", "whole", 5, "A field divided into plots by paths.", True)
rad("里", "さと", "sato", "village", "whole", 7, "A field (田) on the earth (土): a village.")
rad("玉", "たま・おうへん", "tama", "jewel / king", "hen", 5, "Three jade beads on a string. On the left it loses its dot and looks like 王.", True, "王")
rad("王", "おう", "ō", "king", "hen", 4, "Three levels - heaven, people, earth - joined by one ruler. As a left radical it means jewel.", True, "玉")
rad("金", "かね・かねへん", "kane", "gold / metal", "hen", 8, "Nuggets of ore inside the earth under a roof. Kanji with it are metals and money.", True)
rad("虫", "むし", "mushi", "insect", "whole", 6, "A snake or worm curled up.")
rad("羊", "ひつじ", "hitsuji", "sheep", "kanmuri", 6, "A sheep's head with horns.")
rad("牛", "うし・うしへん", "ushi", "cow", "hen", 4, "A cow's head and horns.")
rad("犬", "いぬ", "inu", "dog", "whole", 4, "A dog with an ear and a tail.", True, "犭")
rad("犭", "けものへん", "kemonohen", "animal", "hen", 3, "犬 on the left. Kanji with it are animals and animal-like traits.", True, "犬")
rad("馬", "うま", "uma", "horse", "whole", 10, "A horse with mane, four legs and tail.")
rad("魚", "さかな", "sakana", "fish", "whole", 11, "A fish with head, body and tail fin (the four dots).")
rad("鳥", "とり", "tori", "bird", "whole", 11, "A bird with beak, body and feet.")
rad("貝", "かい・かいへん", "kai", "shell", "hen", 7, "A cowrie shell - once used as money. Kanji with it are about money, buying and value.", True)
rad("糸", "いと・いとへん", "ito", "thread", "hen", 6, "Twisted skeins of silk thread. Kanji with it are about thread, cloth and connecting.", True)
rad("衣", "ころも", "koromo", "clothing", "whole", 6, "A collar and sleeves.", False, "衤")
rad("衤", "ころもへん", "koromohen", "clothing", "hen", 5, "衣 on the left: clothing and dress.", True, "衣")
rad("示", "しめす", "shimesu", "show / altar", "kanmuri", 5, "An altar table where offerings are shown to the gods.", True, "礻")
rad("礻", "しめすへん", "shimesuhen", "altar / spirit", "hen", 4, "示 on the left: gods, festivals and blessings.", True, "示")
rad("酉", "とり・さけのとり", "sake no tori", "alcohol jar", "hen", 7, "A wine jar. Kanji with it are about alcohol and things that ferment.", True)
rad("食", "しょく・しょくへん", "shoku", "eat / food", "hen", 9, "A lid over a bowl of rice. About eating and food.", True, "飠")
rad("車", "くるま・くるまへん", "kuruma", "vehicle / wheel", "hen", 7, "A cart seen from above: axle and two wheels.", True)
rad("斗", "とます", "tomasu", "measure", "tsukuri", 4, "A ladle for measuring.")
rad("斤", "おのづくり", "onozukuri", "axe", "tsukuri", 4, "An axe head on a handle.")
rad("戈", "ほこづくり", "hokozukuri", "spear", "tsukuri", 4, "A spear with a hook.")
rad("弋", "しきがまえ", "shikigamae", "stake / ceremony", "kanmuri", 3, "A wooden stake.")
rad("弓", "ゆみ・ゆみへん", "yumi", "bow", "hen", 3, "A bow with a string. About bows, and often 'strong' or 'pull'.", True)
rad("刀", "かたな", "katana", "sword", "whole", 2, "A blade with a curved back.", True, "刂")
rad("刂", "りっとう", "rittō", "knife", "tsukuri", 2, "刀 stood upright on the right. Kanji with it are about cutting and dividing.", True, "刀")
rad("網", "あみ・あみがしら", "ami", "net", "kanmuri", 5, "A net hung to dry. Shown as 罒 on top of a kanji.")
rad("网", "あみがしら", "amigashira", "net", "kanmuri", 5, "The net radical (also written 罒).")
rad("用", "もちいる", "mochiiru", "use", "whole", 5, "A container that is put to use.")
rad("音", "おと", "oto", "sound", "whole", 9, "立 (stand) over 日 (say): a note or sound.")
rad("面", "めん", "men", "face / mask", "whole", 9, "An outline of a face with a nose in the middle.")
rad("色", "いろ", "iro", "colour", "whole", 6, "A person (儿) leaning on another - shown by their colour and flush.")
rad("赤", "あか", "aka", "red", "whole", 7, "土 over 火: fire on the earth glows red.")
rad("青", "あお", "ao", "blue / green", "whole", 8, "A plant (生) growing on a well (丹): the fresh green-blue of spring.")
rad("黄", "き", "ki", "yellow", "whole", 11, "A field with a torch: yellow light.")
rad("黒", "くろ", "kuro", "black", "whole", 11, "Soot over a fire: black.")
rad("白", "しろ", "shiro", "white", "whole", 5, "A bright ray of sunlight.")
rad("非", "あらず", "arazu", "not / wrong", "whole", 8, "Two wings pushing apart: opposition, negation.")
rad("飛", "とぶ", "tobu", "fly", "whole", 9, "A bird with wings spread.")
rad("止", "とめる", "tomeru", "stop", "whole", 4, "A footprint (foot planted): stop. Kanji with it are about steps and stopping.")
rad("欠", "あくび", "akubi", "yawn / lack", "tsukuri", 4, "A person opening their mouth wide - lacking breath.")
rad("方", "ほう・かたへん", "hō", "direction", "hen", 4, "Two boats lashed together: a direction, a side.")
rad("毋", "なかれ", "nakare", "mother / do not", "whole", 4, "女 with two dots for breasts: mother.")
rad("父", "ちち", "chichi", "father", "whole", 4, "A hand holding a stick: the head of a household.")
rad("小", "しょう", "shō", "small", "whole", 3, "Three small dots.")
rad("大", "だい", "dai", "big", "whole", 3, "A person with arms stretched wide: big.", True)
rad("文", "ぶん", "bun", "writing", "whole", 4, "A tattooed chest: patterns, later writing.")
rad("工", "こう", "kō", "craft", "whole", 3, "A carpenter's square.")
rad("巾", "はば・はばへん", "haba", "cloth", "hen", 3, "A cloth hanging from a belt. Kanji with it are cloth and things made of cloth.", True)
rad("广", "まだれ", "madare", "building / grotto", "tare", 3, "A roof with a wall on the left. Kanji with it are shops and public buildings.", True)
rad("尸", "しかばね・しゃくかね", "shikabane", "body / roof", "tare", 3, "A person sitting: the body. Kanji with it are homes, rooms and offices.", True)
rad("宀", "うかんむり", "ukanmuri", "roof", "kanmuri", 3, "The roof of a house. Kanji with it are homes, rooms and shelter.", True)
rad("冖", "わかんむり", "wakanmuri", "cover", "kanmuri", 2, "A cloth thrown over something.")
rad("冫", "にすい", "nisui", "ice", "hen", 2, "Two drops of ice. Kanji with it are cold.")
rad("冂", "どうがまえ・けいがまえ", "dōgamae", "frame", "kamae", 2, "A border or open box.")
rad("囗", "くにがまえ", "kunigamae", "enclosure", "kamae", 3, "A wall around something: a country, a garden or a boundary.", True)
rad("匚", "はこがまえ", "hakogamae", "box", "kamae", 2, "An open box on its side.")
rad("戸", "と", "to", "door", "tare", 4, "One leaf of a door.")
rad("彳", "ぎょうにんべん", "gyōninben", "walk / step", "hen", 3, "Half of 行 (crossroads): a step. Kanji with it are about going and roads.", True)
rad("行", "ぎょう・ゆきがまえ", "yukigamae", "go / street", "kamae", 6, "A crossroads seen from above.")
rad("辶", "しんにょう・しんにゅう", "shinnyō", "road / move on", "nyo", 3, "A foot on a road, curled at the bottom left. Kanji with it are about roads, moving and travelling.", True)
rad("攵", "のぶん・ぼくにょう", "nobun", "strike / do", "tsukuri", 4, "A hand holding a stick. Kanji with it are actions done to something.", True, "攴")
rad("走", "はしる・そうにょう", "hashiru", "run", "nyo", 7, "A person swinging their arms above a foot.")
rad("癶", "はつがしら", "hatsugashira", "footsteps apart", "kanmuri", 5, "Two feet spread out.")
rad("夊", "ふゆがしら・すいにょう", "fuyugashira", "go slowly", "ashi", 3, "A foot dragging behind.")
rad("厶", "む", "mu", "private", "whole", 2, "A small loop.")
rad("匕", "ひ・さじ", "hi", "spoon / change", "whole", 2, "A spoon; also a person changed (化).")
rad("儿", "ひとあし", "hitoashi", "legs", "ashi", 2, "Two legs of a person under something.")
rad("入", "いる・いりがしら", "iru", "enter", "whole", 2, "An arrow entering an opening.")
rad("八", "はち・はちがしら", "hachi", "eight / divide", "whole", 2, "Two strokes moving apart.")
rad("十", "じゅう", "jū", "ten", "whole", 2, "A cross: complete.", True)
rad("亠", "なべぶた", "nabebuta", "lid", "kanmuri", 2, "A lid on a pot.")
rad("二", "に", "ni", "two", "whole", 2, "Two lines.")
rad("一", "いち", "ichi", "one", "whole", 1, "A single stroke.", True)
rad("丨", "たてぼう", "tatebō", "line / down stroke", "whole", 1, "A vertical line.")
rad("丶", "てん", "ten", "dot", "whole", 1, "A dot.")
rad("丿", "の", "no", "slash", "whole", 1, "A sweep to the left.")
rad("乙", "おつ", "otsu", "second / hook", "whole", 1, "A curved hook.")
rad("亅", "はねぼう", "hanebō", "hook", "whole", 1, "A vertical stroke with a hook.")
rad("干", "かん・いちじゅう", "kan", "dry / shield", "whole", 3, "A forked shield or pole.")
rad("艮", "こん・ねづくり", "kon", "stopping / boundary", "whole", 6, "A person turning to look back.")
rad("比", "くらべる", "kuraberu", "compare", "whole", 4, "Two people side by side.")
rad("曰", "ひらび・いわく", "iwaku", "say", "whole", 4, "A mouth with a tongue speaking.")
rad("襾", "にし・おおいかんむり", "nishi", "west / cover", "kanmuri", 6, "A basket with a lid.")
rad("穴", "あな・あなかんむり", "ana", "hole", "kanmuri", 5, "A hole under a roof: a cave.")
rad("立", "たつ", "tatsu", "stand", "whole", 5, "A person standing on the ground.")
rad("隹", "ふるとり", "furutori", "short-tailed bird", "tsukuri", 8, "A small bird.")
rad("羽", "はね", "hane", "feather / wings", "whole", 6, "Two wings.")
rad("辛", "からい", "karai", "bitter / spicy", "whole", 7, "A tattooing needle: pain and sharpness.")
rad("邑", "おおざと", "ōzato", "city / village", "tsukuri", 3, "A walled town (口) with a person beside it (巴). On the right it is written 阝.", True, "阝")
rad("阜", "こざとへん", "kozatohen", "hill / mound", "hen", 3, "Steps of a mountain seen from the side. On the left it is written 阝.", True, "阝")
rad("長", "ながい", "nagai", "long", "whole", 8, "A person with long flowing hair.")
rad("門", "もん", "mon", "gate", "kamae", 8, "Two swinging doors. Kanji with it are about gates, openings and spaces between.")
rad("見", "みる", "miru", "see", "whole", 7, "An eye (目) on legs (儿): seeing.")
rad("言", "ごん・ごんべん", "gonben", "say / word", "hen", 7, "A mouth with sound waves rising. Kanji with it are about words, talk and language.", True)
rad("高", "たかい", "takai", "tall", "whole", 10, "A tall tower with a gate.")
rad("老", "おい", "oi", "old age", "kanmuri", 6, "An old person with a stick.")
rad("凵", "うけばこ", "ukebako", "open box", "kamae", 2, "A dish or pit that is open at the top.")
rad("士", "さむらい", "samurai", "samurai / scholar", "kanmuri", 3, "A man with an axe head: a gentleman-warrior or scholar.")
rad("彡", "さんづくり", "sanzukuri", "hair / pattern", "tsukuri", 3, "Three strokes of hair or decoration: shape, pattern.")

# ---- v2.9.1: extra radicals so every JLPT kanji can be broken down --------
rad("勹", "つつみがまえ", "tsutsumigamae", "wrap", "kamae", 2, "A person bending to wrap something up. Kanji with it are about wrapping and enclosing.")
rad("卩", "ふしづくり", "fushizukuri", "seal / kneeling person", "tsukuri", 2, "A person kneeling. Shows up in kanji about stamps, orders and danger.")
rad("厂", "がんだれ", "gandare", "cliff", "tare", 2, "A cliff overhang. Kanji with it are about cliffs, stone and origins.")
rad("尢", "だいのまげあし", "dai no mageashi", "lame / bent leg", "nyo", 3, "A person with a bent leg. Rare; seen in 就.")
rad("巛", "かわ", "kawa", "river (flowing)", "kanmuri", 3, "Flowing streams, used on top of some kanji such as 巣.")
rad("己", "おのれ", "onore", "oneself", "whole", 3, "A coiled thread. Means self; appears in 巳 巴 巽.")
rad("幺", "いとがしら", "itogashira", "tiny thread", "hen", 3, "A small twist of thread: tiny, young.")
rad("廴", "えんにょう", "ennyō", "long stride", "nyo", 3, "A long step. Kanji with it are about building and extending.")
rad("廾", "にじゅうあし", "nijūashi", "two hands", "ashi", 3, "Two hands lifting something up.")
rad("彐", "けいがしら", "keigashira", "pig's head", "kanmuri", 3, "A pig's snout; in modern kanji it is just a shape on top.")
rad("几", "つくえ・かぜかんむり", "tsukue", "table / wind", "kamae", 2, "A small table or a wind shape.")
rad("爪", "つめ・つめかんむり", "tsume", "claw / nail", "kanmuri", 4, "A claw reaching down (also written with four strokes on top, ⺤).")
rad("支", "しにょう・えだ", "shinyō", "branch / support", "whole", 4, "A hand holding a branch: to support.")
rad("无", "なし・むにょう", "nashi", "without", "tsukuri", 4, "An old form of 'not having'.")
rad("毛", "け", "ke", "hair / fur", "whole", 4, "A strand of hair or fur.")
rad("氏", "うじ", "uji", "clan / family name", "whole", 4, "A spoon-like shape used in clan names.")
rad("殳", "るまた・ほこづくり", "rumata", "weapon / strike", "tsukuri", 4, "A hand holding a club. Kanji with it are about hitting and tools.")
rad("片", "かた・かたへん", "kata", "one side / slice", "hen", 4, "Half of a tree 木 cut lengthwise: a slice or a board.")
rad("牙", "きば", "kiba", "fang", "whole", 4, "Interlocking teeth.")
rad("玄", "げん", "gen", "mysterious / dark", "whole", 5, "A twisted thread under a lid: deep, dark.")
rad("甘", "あまい", "amai", "sweet", "whole", 5, "A tongue with something sweet inside the mouth.")
rad("疋", "ひき", "hiki", "cloth roll / animal counter", "whole", 5, "A leg and foot; a counter for small animals.")
rad("皮", "かわ・けがわ", "kawa", "skin / hide", "whole", 5, "A hand stripping the skin off an animal.")
rad("皿", "さら", "sara", "dish", "ashi", 5, "A flat dish on a stand. Kanji with it are about plates and vessels.")
rad("矛", "ほこ", "hoko", "halberd", "whole", 5, "A long spear with a blade.")
rad("而", "しこうして", "shikōshite", "and then / beard", "whole", 6, "A beard hanging down; today a connecting word.")
rad("耒", "らいすき", "raisuki", "plough", "hen", 6, "A plough. Kanji with it are about farming.")
rad("聿", "ふでづくり", "fudezukuri", "brush", "whole", 6, "A hand holding a brush.")
rad("臣", "しん", "shin", "retainer / minister", "whole", 6, "An eye looking down in respect: a servant of the king.")
rad("臼", "うす", "usu", "mortar", "ashi", 6, "A mortar for pounding rice.")
rad("舌", "した", "shita", "tongue", "hen", 6, "A tongue sticking out of a mouth.")
rad("舛", "まいあし", "maiashi", "opposite feet", "ashi", 6, "Two feet pointing apart, as when dancing.")
rad("舟", "ふね・ふねへん", "fune", "boat", "hen", 6, "A little boat. Kanji with it are about ships and transport.")
rad("虍", "とらかんむり", "toragashira", "tiger", "kanmuri", 6, "A tiger's head and stripes on top of a kanji.")
rad("血", "ち", "chi", "blood", "whole", 6, "A dish (皿) with a drop of blood.")
rad("角", "つの・つのへん", "tsuno", "horn / corner", "hen", 7, "An animal horn. Also means an angle or corner.")
rad("豆", "まめ", "mame", "bean", "hen", 7, "A tall dish with beans; also a ritual bowl.")
rad("豕", "ぶた・いのこ", "buta", "pig", "hen", 7, "A pig with belly and tail.")
rad("辰", "しんのたつ", "shin no tatsu", "dragon (zodiac)", "whole", 7, "A clam with its foot out; later the dragon sign.")
rad("釆", "のごめ", "nogome", "rice grains / discern", "hen", 7, "Grains separated by hand: to tell apart.")
rad("革", "かわ・かくのかわ", "kawa", "leather", "hen", 9, "A hide stretched out to dry. Kanji with it are about leather goods.")
rad("香", "かおり", "kaori", "fragrance", "whole", 9, "Millet (黍) and sweetness (甘/日): a pleasant smell.")
rad("骨", "ほね", "hone", "bone", "hen", 10, "A bone (冎) with flesh (月) on it.")
rad("鬥", "とうがまえ", "tōgamae", "fight", "kamae", 10, "Two people facing off.")
rad("鬼", "おに", "oni", "demon / ghost", "whole", 10, "A ghost with a big head and a tail. Kanji with it are about spirits.")
rad("鹿", "しか", "shika", "deer", "whole", 11, "A deer with antlers and four legs.")
rad("麦", "むぎ", "mugi", "wheat / barley", "whole", 7, "A wheat plant with roots.")
rad("麻", "あさ", "asa", "hemp", "whole", 11, "Hemp plants drying under a shelter.")
rad("鼓", "つづみ", "tsuzumi", "drum", "whole", 13, "A hand beating a drum.")
rad("歯", "は", "ha", "tooth", "whole", 12, "Teeth in a mouth with a sound part on top.")
rad("龍", "りゅう", "ryū", "dragon", "whole", 16, "A dragon with head, body and claws. Shortened to 竜 in everyday use.")
rad("亀", "かめ", "kame", "turtle", "whole", 11, "A turtle with shell and legs.")
rad("至", "いたる", "itaru", "arrive", "hen", 6, "An arrow that has hit the ground: to reach.")
rad("卜", "ぼく・うらない", "boku", "divination", "whole", 2, "A crack in a turtle shell read by fortune-tellers.")

# Fix accidental duplicates: keep last definition per glyph
_seen = {}
for r_ in R:
    _seen[r_["glyph"]] = r_
R = list(_seen.values())
# 網 is not a real radical form - drop it; keep 网
R = [r_ for r_ in R if r_["glyph"] != "網"]
BY = {r_["glyph"]: r_ for r_ in R}

# ---- which kanji (from the app) sit under which radical -----------------
MEMBERS = {
    "一": "一三上下不世両七万", "二": "二五", "八": "六八公", "十": "十千半午南卒単", "囗": "四回国困図園",
    "冂": "円内", "亠": "京", "亻": "何休体住伝信低働使仕作係側便", "人": "人今会以", "入": "入全", "儿": "先元兄", "冫": "冬冷",
    "力": "力勉動", "匕": "化北", "匚": "医区", "厶": "去", "又": "友反受取", "口": "口右古名味台問品商員号同",
    "土": "土場地", "夕": "夕多外夜", "大": "大天太夫失", "女": "女好姉妹始婚婦", "子": "子学字", "宀": "家寝安室宿実寒",
    "寸": "寺対専", "小": "小少", "尸": "屋局", "山": "山島", "川": "川州", "工": "工左", "巾": "帰市", "干": "年平",
    "广": "広店度庭", "弓": "弟強引", "彡": "形", "彳": "待後", "心": "心思悪忘急意必", "忄": "忙", "戈": "成", "戸": "所",
    "手": "手", "扌": "持指接授打払", "攵": "教数", "斤": "新", "方": "方旅族", "日": "日時早明春昼晩暗暑晴曜昔昨",
    "曰": "書最", "月": "有朝期服", "木": "木校来林森東楽様未横機橋末村本", "欠": "次歌", "止": "止正歩歳", "歹": "残", "毋": "母毎",
    "水": "水氷", "氵": "洋漢泳法治活泣温海池港泊洗決注", "火": "火", "灬": "無然熱", "点": "点", "父": "父", "牛": "牛物特",
    "犬": "犬", "玉": "玉理現", "王": "王", "田": "田男番町留画界由", "疒": "病痛", "癶": "発登", "白": "白百皆的", "目": "目着県相",
    "矢": "知短", "石": "石研", "示": "祭", "禾": "私科秋", "穴": "究空", "立": "立", "竹": "節答笑第", "米": "米",
    "糸": "紙絵練組終結線続", "羊": "羊美", "老": "考", "耳": "耳聞", "肉": "肉", "⺼": "背育", "自": "自", "色": "色",
    "艹": "草花若茶薬荷落", "虫": "虫", "行": "行術", "襾": "西要", "見": "見親", "言": "言語話説試読記計", "貝": "買贈貸",
    "赤": "赤", "走": "走起", "足": "足", "身": "身", "車": "車転", "辛": "辞", "辶": "近道週速遅運選通遊進遠達送",
    "邑": "部都", "阜": "院降際階", "酉": "酒配", "里": "野重", "金": "銀", "長": "長", "門": "門開閉間関", "隹": "集雑難",
    "雨": "雨雪電", "青": "青静", "非": "非", "面": "面", "音": "音", "頁": "題頭顔願", "風": "風", "飛": "飛", "食": "食飯飲館",
    "首": "首", "馬": "馬駅験", "魚": "魚", "鳥": "鳥", "鼻": "鼻", "黄": "黄", "黒": "黒", "气": "気", "网": "置", "斗": "料",
    "用": "用", "生": "生", "弋": "式", "亅": "事", "丶": "主", "丿": "乗", "乙": "九", "比": "比", "艮": "良", 
    "丨": "中", "冖": "写", "夊": "夏", "凵": "出", "士": "売", "文": "文", "高": "高", "羽": "習", "礻": "礼神", "刀": "前初券切", "刂": "制別利",
}
# a few kanji sit under a radical listed above as a *form*; fix forms where the
# radical glyph in the kanji is a variant of a listed one
MEMBERS["点"] = ""  # 点 is filed under 火/灬 in dictionaries; keep it in 灬
MEMBERS["灬"] += "点"
del MEMBERS["点"]
# 玉 as a left radical looks like 王
MEMBERS["玉"] = "玉理現"

EXTRA = {
    "犭": "狭猫独犯猛獣", "衤": "複被補裕", "礻": "社福祝禁", "刂": "刊列判割副", "衣": "表袋裏装",
    "羽": "翌", "刀": "刃分", "文": "斉", "高": "", "口": "回可各合向君告和員喜", "扌": "投折抜押拾持報提",
    "亻": "代付借像億億任", "氵": "湖油流波深消済液", "艹": "英菜芸苦", "言": "詩談課調論", "糸": "細経約絡",
    "木": "板柱植根", "土": "坂型堂", "心": "念恩感情", "日": "映星昨暮", "金": "鉄鏡針", "食": "養",
    "貝": "貨貿財質", "車": "軽輪", "示": "票", "疒": "痛病", "禾": "程積", "雨": "雲雷", "石": "破確",
    "力": "助加功", "大": "奈", "宀": "客宮官", "辶": "追送連違", "女": "姓娘", "月": "望", "田": "細",
}

# ---- composition notes: kanji -> (parts, story). Original wording. --------
STORY = {
    "休": ("亻 + 木", "A person leaning on a tree: taking a rest."),
    "体": ("亻 + 本", "A person and their root/base: the body."),
    "何": ("亻 + 可", "A person asking about something possible: what?"),
    "住": ("亻 + 主", "A person who is the master of a place: to live."),
    "信": ("亻 + 言", "A person whose words are true: trust, belief."),
    "作": ("亻 + 乍", "A person suddenly getting to work: to make."),
    "使": ("亻 + 吏", "A person in service: to use, a messenger."),
    "働": ("亻 + 動", "A person + moving: to work."),
    "仕": ("亻 + 士", "A person who serves: work, to serve."),
    "低": ("亻 + 氐", "A person lowered to the ground: low."),
    "伝": ("亻 + 云", "A person passing something along: to convey."),
    "係": ("亻 + 系", "A person linked by a thread: connection, duty."),
    "便": ("亻 + 更", "A person changing things for comfort: convenient."),
    "側": ("亻 + 則", "A person beside a rule: the side."),
    "明": ("日 + 月", "Sun and moon together: bright."),
    "森": ("木 + 木 + 木", "Three trees: a forest, deeper than 林."),
    "林": ("木 + 木", "Two trees: a grove."),
    "校": ("木 + 交", "Wood crossed together: a school building."),
    "休み": ("", ""),
    "好": ("女 + 子", "A woman with a child: fondness, to like."),
    "姉": ("女 + 市", "A woman of the town: older sister."),
    "妹": ("女 + 未", "A woman who is not yet grown: younger sister."),
    "始": ("女 + 台", "A woman with a stand: the beginning."),
    "婚": ("女 + 昏", "A woman at dusk: marriage."),
    "家": ("宀 + 豕", "A roof over a pig (once kept at home): house."),
    "安": ("宀 + 女", "A woman under a roof: peace, cheap."),
    "室": ("宀 + 至", "A roof where you arrive: a room."),
    "寒": ("宀 + 冫", "Under a roof, with ice: cold."),
    "宿": ("宀 + 人 + 百", "A place under a roof where people stay."),
    "実": ("宀 + 夫?", "A full house: truth, fruit."),
    "国": ("囗 + 玉", "A jewel (or king) inside a wall: a country."),
    "図": ("囗 + 冬?", "Something drawn inside a frame: a diagram."),
    "園": ("囗 + 袁", "A walled place: park, garden."),
    "回": ("囗 + 囗", "A whirl inside a whirl: turn, times."),
    "四": ("囗 + 儿", "Four legs inside a frame: four."),
    "時": ("日 + 寺", "The sun measured at the temple: time."),
    "間": ("門 + 日", "Sun shining between the gate doors: a gap, between."),
    "開": ("門 + 开", "Two hands lifting the bar of a gate: open."),
    "閉": ("門 + 才", "A gate with a latch: closed."),
    "聞": ("門 + 耳", "An ear at the gate: to hear, to ask."),
    "問": ("門 + 口", "A mouth at the gate: to ask."),
    "話": ("言 + 舌", "Words and tongue: to talk."),
    "語": ("言 + 吾", "Words (言) with the sound 'go' (吾): language."),
    "読": ("言 + 売", "Words that are sold as sounds: to read."),
    "説": ("言 + 兑", "Words that unwrap an idea: explain."),
    "記": ("言 + 己", "Words about oneself: to record."),
    "計": ("言 + 十", "Words counted in tens: to measure."),
    "試": ("言 + 式", "Words tried according to a form: to test."),
    "言": ("口 + 辛", "Words rising from the mouth."),
    "思": ("田 + 心", "A field in the heart: to think."),
    "急": ("刍 + 心", "A heart in a hurry: hurry."),
    "意": ("音 + 心", "The sound of the heart: meaning, intention."),
    "悪": ("亜 + 心", "A heart that is second-rate: bad."),
    "忘": ("亡 + 心", "The heart loses it: to forget."),
    "忙": ("忄 + 亡", "A heart that has lost its calm: busy."),
    "必": ("心 + 丿", "A heart with a slash through it: certain, must."),
    "持": ("扌 + 寺", "A hand at the temple: to hold."),
    "指": ("扌 + 旨", "A hand that points: finger."),
    "打": ("扌 + 丁", "A hand striking a nail: to hit."),
    "接": ("扌 + 妾", "A hand joining things: to connect."),
    "授": ("扌 + 受", "A hand handing something over: to give, teach."),
    "払": ("扌 + 厶", "A hand pushing away: to pay, to sweep."),
    "海": ("氵 + 毎", "Water that comes every day: the sea."),
    "池": ("氵 + 也", "Water in a hollow: pond."),
    "泳": ("氵 + 永", "Water that goes on and on: to swim."),
    "洗": ("氵 + 先", "Water first: to wash."),
    "泣": ("氵 + 立", "Water standing on the face: to cry."),
    "温": ("氵 + 昷", "Warm water in a dish: warm."),
    "法": ("氵 + 去", "Water flowing away in one direction: law, method."),
    "活": ("氵 + 舌", "Water on the tongue: lively."),
    "港": ("氵 + 巷", "Water with a lane: harbour."),
    "漢": ("氵 + 莫", "The Han river: China, Chinese characters."),
    "洋": ("氵 + 羊", "Water wide as a flock: ocean, Western."),
    "治": ("氵 + 台", "Water brought under control: to rule, to cure."),
    "決": ("氵 + 夬", "Water breaking through a bank: to decide."),
    "注": ("氵 + 主", "Water poured by the master: to pour, to pay attention."),
    "泊": ("氵 + 白", "Water made pale: to stay (at a shore)."),
    "近": ("辶 + 斤", "Walking a road with an axe: coming near."),
    "道": ("辶 + 首", "A head that walks the road: path."),
    "週": ("辶 + 周", "A road that goes around: week."),
    "速": ("辶 + 束", "Bound together on the road: fast."),
    "遅": ("辶 + 犀", "Walking slow like a rhino: late."),
    "運": ("辶 + 軍", "Army moving on the road: to carry, fate."),
    "選": ("辶 + 巽", "Moving on to pick: to choose."),
    "通": ("辶 + 甬", "Passing along a road: to go through."),
    "遊": ("辶 + 斿", "Walking with flags: to play."),
    "進": ("辶 + 隹", "A bird going forward: to advance."),
    "遠": ("辶 + 袁", "A long trailing road: far."),
    "送": ("辶 + 关", "Sending someone off along the road."),
    "達": ("辶 + 幸", "Passing on to arrive: reach, plural marker."),
    "草": ("艹 + 早", "Plants at early morning: grass."),
    "花": ("艹 + 化", "A plant that changes: flower."),
    "茶": ("艹 + 余", "A plant leaf: tea."),
    "薬": ("艹 + 楽", "Plants that bring comfort: medicine."),
    "荷": ("艹 + 何", "A plant load someone carries: cargo."),
    "落": ("艹 + 洛", "A leaf falling: to drop."),
    "若": ("艹 + 右", "A plant reaching out: young."),
    "紙": ("糸 + 氏", "Fibres pressed into a sheet: paper."),
    "絵": ("糸 + 会", "Threads brought together: a picture."),
    "終": ("糸 + 冬", "The thread at winter's end: to finish."),
    "練": ("糸 + 東", "Silk boiled soft: to practise."),
    "組": ("糸 + 且", "Threads piled up: group."),
    "結": ("糸 + 吉", "A lucky knot: to tie, to conclude."),
    "線": ("糸 + 泉", "A thread like a spring: line."),
    "続": ("糸 + 売", "Threads sold in a row: to continue."),
    "買": ("网 + 貝", "A net catching shells (money): to buy."),
    "売": ("士 + 冖 + 儿", "Goods going out: to sell."),
    "贈": ("貝 + 曽", "Adding to shells (money): to present a gift."),
    "貸": ("代 + 貝", "Shell-money handed to a substitute: to lend."),
    "銀": ("金 + 艮", "A metal that stops and stays white: silver."),
    "食": ("人 + 良", "Something good for people: to eat."),
    "飯": ("食 + 反", "Food that comes back to you each day: rice, a meal."),
    "飲": ("食 + 欠", "Food with a wide-open mouth: to drink."),
    "館": ("食 + 官", "A house with food for officials: a hall."),
    "酒": ("氵 + 酉", "Water from a jar: alcohol."),
    "配": ("酉 + 己", "Sake poured to a person: distribute."),
    "雪": ("雨 + ヨ", "Rain you can sweep away: snow."),
    "電": ("雨 + 申", "Rain with a lightning flash: electricity."),
    "雨": ("一 + 冂 + 水", "Drops falling under the clouds."),
    "病": ("疒 + 丙", "Illness in bed: sickness."),
    "痛": ("疒 + 甬", "Illness that runs through: pain."),
    "院": ("阝 + 完", "A completed hill-house: institution, hospital."),
    "降": ("阝 + 夅", "Walking down a slope: to fall (rain), to get off."),
    "階": ("阝 + 皆", "Everyone on the steps: floor of a building."),
    "際": ("阝 + 祭", "The meeting at a hill's edge: occasion."),
    "部": ("咅 + 阝", "A section of a town."),
    "都": ("者 + 阝", "A town where many people gather: capital."),
    "朝": ("十日十 + 月", "The sun rising with the moon still up: morning."),
    "期": ("其 + 月", "A moon that returns on schedule: a period."),
    "服": ("月 + 卩 + 又", "Wearing something on the body: clothes, to obey."),
    "有": ("ナ + 月", "A hand holding meat: to have."),
    "背": ("北 + ⺼", "Body parts turned north: the back."),
    "育": ("𠫓 + ⺼", "A child fed by its body: to raise."),
    "教": ("孝 + 攵", "A stick in the hand of a teacher: to teach."),
    "数": ("婁 + 攵", "Striking off items to count: number."),
    "新": ("立 + 木 + 斤", "An axe cutting a fresh tree: new."),
    "旅": ("方 + 从", "People marching under a banner: travel."),
    "族": ("方 + 矢", "People under a banner with arrows: a clan."),
    "歌": ("哥 + 欠", "A wide-open mouth: to sing."),
    "次": ("冫 + 欠", "Yawn after yawn: next."),
    "知": ("矢 + 口", "Words that hit the mark like an arrow: to know."),
    "短": ("矢 + 豆", "Arrow-short: short."),
    "研": ("石 + 幵", "Polishing a stone: to research."),
    "神": ("礻 + 申", "The altar where lightning is worshipped: god."),
    "礼": ("礻 + 乚", "Bowing at the altar: courtesy."),
    "祭": ("月 + 又 + 示", "Offering meat by hand at the altar: festival."),
    "私": ("禾 + 厶", "Grain kept for oneself: I, private."),
    "秋": ("禾 + 火", "Grain turning red like fire: autumn."),
    "科": ("禾 + 斗", "Grain measured by a ladle: a subject."),
    "笑": ("竹 + 夭", "Bamboo bending: a laughing face."),
    "答": ("竹 + 合", "Bamboo slips matched together: an answer."),
    "節": ("竹 + 即", "A bamboo joint: season, node."),
    "第": ("竹 + 弟", "A bamboo tally in order: number (ordinal)."),
    "男": ("田 + 力", "Power in the fields: man."),
    "町": ("田 + 丁", "Fields with a road: town."),
    "画": ("田 + 凵", "A field drawn with boundaries: a picture."),
    "界": ("田 + 介", "A field between: boundary, world."),
    "留": ("田 + 卯", "A field where you stay: to stop."),
    "番": ("釆 + 田", "Rice field turns: number, turn."),
    "由": ("田 + 丨", "A shoot from a field: reason."),
    "野": ("里 + 予", "The village where fields are laid out: the plain."),
    "重": ("千 + 里", "Loaded over a thousand villages: heavy."),
    "医": ("匚 + 矢", "A box for arrows (healing): doctor."),
    "区": ("匚 + ㄡ", "A box divided up: ward, district."),
    "馬": ("馬", "A horse with mane and tail."),
    "駅": ("馬 + 尺", "A relay stop for horses: station."),
    "験": ("馬 + 僉", "Testing a horse: examination."),
    "石": ("厂 + 口", "A stone under a cliff."),
    "車": ("車", "A cart seen from above."),
    "転": ("車 + 云", "Wheels going round: to turn."),
    "犬": ("大 + 丶", "A big dog with an ear."),
    "牛": ("牛", "A cow's head with horns."),
    "物": ("牛 + 勿", "Things you can trade for cows: object."),
    "特": ("牛 + 寺", "A cow set apart at the temple: special."),
    "魚": ("魚", "A fish with four fin-dots."),
    "鳥": ("鳥", "A bird with beak and legs."),
    "虫": ("虫", "A worm curled up."),
    "米": ("米", "Grains on a stalk."),
    "羊": ("羊", "A sheep's horns."),
    "美": ("羊 + 大", "A big sheep: beautiful, pleasing."),
    "雑": ("九 + 木 + 隹", "Birds mixed in a tree: miscellaneous."),
    "集": ("隹 + 木", "Birds gather on a tree: to collect."),
    "難": ("莫 + 隹", "A bird in trouble: difficult."),
    "東": ("木 + 日", "The sun rising behind a tree: east."),
    "来": ("木 + 人", "A wheat plant that arrives: to come."),
    "未": ("木 + 一", "A tree whose top hasn't grown yet: not yet."),
    "楽": ("白 + 幺 + 木", "Drums on a stand: music, comfort."),
    "様": ("木 + 羊 + 水", "A pattern of wood: appearance, form."),
    "橋": ("木 + 喬", "Wood high above water: bridge."),
    "村": ("木 + 寸", "Wood measured out for a village."),
    "機": ("木 + 幾", "A wooden loom: machine, chance."),
    "横": ("木 + 黄", "A yellow wooden bar: sideways."),
    "末": ("木 + 一", "A tree with the top marked: the tip, the end."),
    "見": ("目 + 儿", "An eye on legs: to see."),
    "親": ("立 + 木 + 見", "One who stands in a tree and watches you: parent."),
    "相": ("木 + 目", "Eyes on a tree: to look at each other."),
    "着": ("羊 + 目", "Sheep-wool worn before the eyes: to wear, arrive."),
    "県": ("目 + 厶", "A head hanging: a prefecture."),
    "白": ("白", "A bright ray of the sun."),
    "百": ("一 + 白", "One + white: one hundred."),
    "的": ("白 + 勺", "A white mark to aim at: target, -like."),
    "皆": ("比 + 白", "Two people together: everyone."),
    "空": ("穴 + 工", "A cave made by craft: empty, sky."),
    "究": ("穴 + 九", "A cave explored to its end: to investigate."),
    "立": ("立", "A person standing on the ground."),
    "発": ("癶 + 弓 + 殳", "An arrow released: to emit."),
    "登": ("癶 + 豆", "Feet climbing up a stand: to climb."),
    "冬": ("夂 + 冫", "Slow steps with ice: winter."),
    "夏": ("百 + 夊", "Feet moving under a hot sun: summer."),
    "春": ("三 + 人 + 日", "The sun over plants growing: spring."),
    "昼": ("尺 + 日", "The sun at its full length: daytime."),
    "晩": ("日 + 免", "The sun leaving: evening."),
    "暗": ("日 + 音", "The sun's sound gone quiet: dark."),
    "暑": ("日 + 者", "The sun over people: hot."),
    "晴": ("日 + 青", "A blue sun: fine weather."),
    "曜": ("日 + 翟", "A bright feathered sun: day of the week."),
    "昔": ("廿 + 日", "Days piled up: long ago."),
    "昨": ("日 + 乍", "The day that suddenly passed: yesterday."),
    "早": ("日 + 十", "The sun just above the horizon: early."),
    "時": ("日 + 寺", "Sun at the temple: time."),
    "屋": ("尸 + 至", "A body arrives at a roof: house, shop."),
    "局": ("尸 + 句", "A body in a section: a bureau."),
    "広": ("广 + 厶", "A building with open space: wide."),
    "店": ("广 + 占", "A building where goods are displayed: shop."),
    "度": ("广 + 庶", "A building where measures are made: degree, times."),
    "庭": ("广 + 廷", "The court beside a building: garden."),
    "帰": ("帚 + 巾", "A woman with a broom returns home: to return."),
    "市": ("亠 + 巾", "Cloth held up at a market: city."),
    "弟": ("弓 + ノ", "A bow wound in order: younger brother."),
    "強": ("弓 + 虫", "A strong bow: strong."),
    "引": ("弓 + 丨", "A string pulled from a bow: to pull."),
    "待": ("彳 + 寺", "Walking to the temple and waiting: to wait."),
    "後": ("彳 + 幺 + 夊", "Dragging steps: behind, after."),
    "形": ("开 + 彡", "A pattern with strokes: shape."),
    "成": ("戈 + 丁", "A spear that finishes: to become."),
    "所": ("戸 + 斤", "A door with an axe: a place."),
    "書": ("聿 + 曰", "A brush that speaks: to write."),
    "最": ("曰 + 取", "Taking the top: most."),
    "母": ("母", "A woman with two dots: mother."),
    "毎": ("人 + 母", "Every mother: every."),
    "残": ("歹 + 戔", "Remains of the dead: to remain."),
    "止": ("止", "A footprint: to stop."),
    "正": ("一 + 止", "One step forward: correct."),
    "歩": ("止 + 少", "A few steps: to walk."),
    "歳": ("止 + 戌", "Years marching by: age, year."),
    "氷": ("水 + 丶", "Water with a drop of frost: ice."),
    "冷": ("冫 + 令", "An order that freezes: cold."),
    "点": ("占 + 灬", "A fire that marks a spot: point."),
    "無": ("無", "Dance in a gathering: nothing."),
    "然": ("月 + 犬 + 灬", "A dog roasted over fire: so, of course."),
    "力": ("力", "A flexed arm."),
    "勉": ("免 + 力", "Escaping with strength: to endeavour."),
    "動": ("重 + 力", "Heavy load with strength: to move."),
    "天": ("一 + 大", "One above the big man: sky."),
    "太": ("大 + 丶", "Big with an extra dot: thick."),
    "夫": ("一 + 大", "A man with a hairpin: husband."),
    "失": ("丿 + 夫", "Something slipping from a man's hand: to lose."),
    "多": ("夕 + 夕", "Evening on evening: many."),
    "外": ("夕 + 卜", "A divination at dusk: outside."),
    "夜": ("亠 + 亻 + 夕", "A person under the evening: night."),
    "友": ("又 + 又", "Two hands joined: friend."),
    "反": ("厂 + 又", "A hand pushing back on a cliff: opposite."),
    "受": ("爪 + 冖 + 又", "One hand handing over to another: to receive."),
    "取": ("耳 + 又", "A hand taking an ear (in battle): to take."),
    "寺": ("土 + 寸", "Measured ground: a temple."),
    "対": ("文 + 寸", "Matched exactly by hand: opposite, versus."),
    "専": ("十 + 寸", "Hands with skill: exclusively."),
    "場": ("土 + 昜", "Earth in the sun: a place."),
    "地": ("土 + 也", "Earth that spreads: ground."),
    "工": ("工", "A carpenter's square."),
    "左": ("ナ + 工", "A left hand with a tool: left."),
    "右": ("ナ + 口", "A right hand with a mouth: right."),
    "円": ("冂 + 一", "A round coin: yen, circle."),
    "内": ("冂 + 入", "Something entering a frame: inside."),
    "京": ("亠 + 口 + 小", "A tall tower over a gate: the capital."),
    "去": ("土 + ム", "Earth that has been left: to go away."),
    "化": ("亻 + 匕", "A person changed: to change."),
    "北": ("北", "Two people back to back: north."),
    "主": ("王 + 丶", "A lamp on a stand: master."),
    "事": ("一 + 口 + 亅", "A hand holding a brush: a matter."),
    "乗": ("禾 + 北", "A person climbing on a tree: to ride."),
    "式": ("工 + 弋", "A craftsman's rule: ceremony, style."),
    "理": ("王 + 里", "Jade ordered in the village: reason."),
    "現": ("王 + 見", "Jewel seen: appear, present."),
    "気": ("气 + 米", "Steam rising from cooking rice: spirit."),
    "首": ("首", "A neck with hair."),
    "非": ("非", "Two wings pulled apart: not."),
    "面": ("面", "A face outline with the nose."),
    "音": ("立 + 日", "A voice standing up in the sun: sound."),
    "願": ("原 + 頁", "The head that wants the source: to wish."),
    "題": ("是 + 頁", "The head of the matter: topic."),
    "顔": ("彦 + 頁", "A handsome head: face."),
    "頭": ("豆 + 頁", "A bean-shaped head: head."),
    "風": ("風", "Wind carried by an insect."),
    "飛": ("飛", "A bird taking wing."),
    "青": ("生 + 月", "A fresh green: blue."),
    "静": ("青 + 争", "A fresh green struggle ends: quiet."),
    "赤": ("土 + 火", "Fire on the ground: red."),
    "色": ("色", "A person bending to another: colour."),
    "黄": ("廿 + 田 + 八", "Yellow of a field."),
    "黒": ("里 + 灬", "Soot over a fire: black."),
    "長": ("長", "A person with long hair: long."),
    "門": ("門", "Two swinging doors."),
    "耳": ("耳", "An ear."),
    "足": ("足", "A foot below a knee."),
    "身": ("身", "A side view of a body."),
    "手": ("手", "A hand with fingers."),
    "目": ("目", "An eye turned upright."),
    "口": ("口", "An open mouth."),
    "心": ("心", "A heart."),
    "鼻": ("自 + 畀", "A nose plus a sound part: nose."),
    "自": ("自", "A nose: I / self."),
    "肉": ("肉", "Meat with fibres."),
    "考": ("耂 + 丂", "An old person thinking: to think."),
    "料": ("米 + 斗", "Rice measured with a ladle: ingredients, fee."),
    "用": ("用", "A tool at work: to use."),
    "生": ("生", "A shoot growing from earth: life."),
    "写": ("冖 + 与", "Something copied under a cover: to copy."),
    "夏": ("百 + 夊", "Feet moving under a hot sun: summer."),
    "術": ("行 + 朮", "A skill on the streets: technique."),
    "行": ("行", "A crossroads: to go."),
    "西": ("襾", "A bird settling in its nest: west."),
    "要": ("襾 + 女", "A woman with her waist covered: essential."),
    "置": ("网 + 直", "A net set down straight: to put."),
    "式": ("工 + 弋", "A craftsman's rule."),
    "州": ("川 + 丶", "Islands in a river: state, province."),
    "川": ("川", "Three streams."),
    "山": ("山", "Three peaks."),
    "島": ("鳥 + 山", "A bird resting on a mountain in the sea: island."),
    "田": ("田", "A field divided into plots."),
    "力": ("力", "A flexed arm."),
    "子": ("子", "A baby with big head and arms."),
    "女": ("女", "A kneeling woman."),
    "字": ("宀 + 子", "A child under a roof: a character (that grows)."),
    "学": ("⺍ + 冖 + 子", "A child under a roof learning."),
    "夫": ("一 + 大", "A grown man with a hairpin."),
    "婦": ("女 + 帚", "A woman with a broom: wife."),
    "年": ("干 + 丿", "A person harvesting: year."),
    "平": ("干 + 八", "Flat and even."),
    "父": ("父", "A hand holding a stick."),
    "小": ("小", "Three small dots."),
    "少": ("小 + ノ", "Small with a bit missing: few."),
    "大": ("大", "A person with arms wide."),
    "夕": ("夕", "A moon at dusk."),
    "日": ("日", "The sun."),
    "火": ("火", "Flames."),
    "水": ("水", "Streams of water."),
    "木": ("木", "A tree."),
    "土": ("土", "A sprout in earth."),
    "王": ("王", "Heaven, people and earth joined by a ruler."),
    "玉": ("玉", "Three jade beads on a string."),
    "人": ("人", "A person walking."),
    "入": ("入", "An entrance."),
    "出": ("凵 + 屮", "A sprout leaving its pot: to go out."),
    "全": ("入 + 王", "A king entering a jewel: whole."),
    "会": ("人 + 云", "People gathering: to meet."),
    "今": ("人 + 一", "A roof over one moment: now."),
    "以": ("以", "Using a plough: by means of."),
    "写": ("冖 + 与", "Something copied under a cover: to copy."),
    "十": ("十", "A cross: ten."),
    "千": ("丿 + 十", "Ten hundreds: a thousand."),
    "半": ("八 + 牛", "Dividing a cow in two: half."),
    "午": ("午", "A pestle: noon."),
    "南": ("十 + 冂 + 羊", "A warm tent facing the sun: south."),
    "卒": ("十 + 衣", "Clothing marked at the end: to graduate."),
    "単": ("⺍ + 甲", "Simple single thing."),
    "一": ("一", "One line."),
    "三": ("三", "Three lines."),
    "上": ("一 + 卜", "A mark above the line: up."),
    "下": ("一 + 卜", "A mark below the line: down."),
    "不": ("不", "A bird trying to fly up: not."),
    "世": ("十 + 廿", "Three tens: a generation, world."),
    "両": ("一 + 冂 + 山", "Two balanced things: both."),
    "二": ("二", "Two lines."),
    "五": ("二 + 又", "Two lines crossed: five."),
    "六": ("亠 + 八", "A lid over a division: six."),
    "八": ("八", "Two strokes moving apart."),
    "公": ("八 + 厶", "Opening up the private: public."),
    "九": ("九", "A hooked arm: nine."),
    "中": ("口 + 丨", "A line through the middle: middle."),
    "七": ("一 + 乚", "A cross with a bent stroke: seven."),
    "万": ("一 + 勹", "A hundred times a hundred: ten thousand."),
    "方": ("方", "Two boats tied together: direction, way."),
    "先": ("生 + 儿", "A person who steps ahead: earlier, previous."),
    "本": ("木 + 一", "A tree with its root marked: origin, book."),
    "文": ("文", "Patterns on a chest: writing, sentence."),
    "良": ("艮", "A grain sifted clean: good."),
    "元": ("二 + 儿", "The top of a person: origin."),
    "走": ("土 + 止", "Feet moving over the ground: to run."),
    "起": ("走 + 己", "A person who gets going: to rise, to wake."),
    "寝": ("宀 + 爿 + 又", "A bed under a roof: to sleep."),
    "古": ("十 + 口", "Words passed down ten generations: old."),
    "高": ("高", "A tall tower: high."),
    "前": ("䒑 + 月 + 刂", "A boat with a blade cutting forward: front."),
    "名": ("夕 + 口", "A voice calling in the dusk: a name."),
    "兄": ("口 + 儿", "A mouth on legs: the older brother who speaks."),
    "味": ("口 + 未", "Something not yet swallowed on the mouth: taste."),
    "初": ("衤 + 刀", "Cutting cloth for a new garment: first."),
    "習": ("羽 + 白", "Young bird's wings flapping: to learn by practice."),
    "制": ("牛 + 巾 + 刂", "Trimming with a blade: to control."),
    "台": ("厶 + 口", "A platform for speaking: stand, counter for machines."),
    "辞": ("舌 + 辛", "Bitter words: to resign, a word."),
    "品": ("口 + 口 + 口", "Many mouths: goods, refinement."),
    "商": ("章 + 冏", "Words at the market: trade."),
    "員": ("口 + 貝", "A person with a mouth and money: a member."),
    "比": ("比", "Two people side by side: compare."),
    "関": ("門 + 关", "A gate with a bar: barrier, relation."),
    "困": ("囗 + 木", "A tree in a box: trouble."),
    "熱": ("埶 + 灬", "Planting with fire: heat."),
    "券": ("龹 + 刀", "A slip cut with a blade: ticket."),
    "切": ("七 + 刀", "A blade cutting: to cut."),
    "号": ("口 + 丂", "A shouted signal: number, signal."),
    "別": ("口 + 力 + 刂", "Cutting apart: separate."),
    "同": ("冂 + 一 + 口", "Everyone speaking within one frame: same."),
    "利": ("禾 + 刂", "A blade for cutting grain: profit, sharp."),
}


def main():
    valid = {r["glyph"] for r in R}
    jl = {e["kanji"] for e in json.loads((ROOT / "data" / "jlpt_kanji.json").read_text(encoding="utf-8"))}
    kanji_to_rad = {}
    for g, chars in MEMBERS.items():
        if g not in valid:
            raise SystemExit(f"member radical not defined: {g}")
        for ch in chars:
            kanji_to_rad.setdefault(ch, g)
    for g, chars in EXTRA.items():
        for ch in chars:
            if ch in jl:
                kanji_to_rad.setdefault(ch, g)
    import radical_map_extra as _X
    for g, chars in _X.PAIRS:
        if g not in valid:
            continue          # stray/empty keys in the map are ignored
        for ch in chars:
            if ch in jl:
                kanji_to_rad.setdefault(ch, g)
    # every core radical should have an id
    out_rads = []
    for i, r in enumerate(R, 1):
        r = dict(r)
        r["id"] = f"r{i:03d}"
        r["position_label"] = POSITIONS[r["position"]][0]
        r["position_note"] = POSITIONS[r["position"]][1]
        r["kanji"] = [k for k, g in kanji_to_rad.items() if g == r["glyph"]]
        out_rads.append(r)
    data = {
        "positions": {k: {"label": v[0], "note": v[1]} for k, v in POSITIONS.items()},
        "radicals": out_rads,
        "kanji_to_radical": kanji_to_rad,
        "stories": {k: {"parts": v[0], "story": v[1]} for k, v in STORY.items() if v[0]},
    }
    p = ROOT / "data" / "radicals.json"
    p.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    kd = json.loads((ROOT / "data" / "kanji_data.json").read_text(encoding="utf-8"))
    missing = [e["kanji"] for e in kd if e["kanji"] not in kanji_to_rad]
    print(f"wrote {p.name}: {len(out_rads)} radicals, {len(kanji_to_rad)} kanji mapped, "
          f"{sum(1 for r in out_rads if r['core'])} core; kanji without radical: {''.join(missing) or 'none'}")


if __name__ == "__main__":
    main()
