import json

# Common everyday words that a kanji-focused textbook skips entirely
# (they're written in hiragana/katakana, not built around a lesson
# kanji) but that people constantly search for by English meaning -
# fruits, animals, food, electronics, clothing, etc. word == reading
# for plain hiragana entries; katakana loanwords use their katakana
# form as "word" and a hiragana-style reading field left blank (the
# katakana IS the reading for loanwords).

COMMON = [
 # fruits
 ("りんご", "りんご", "ringo", "apple", "Food & Drink"),
 ("バナナ", "", "banana", "banana", "Food & Drink"),
 ("オレンジ", "", "orenji", "orange", "Food & Drink"),
 ("いちご", "いちご", "ichigo", "strawberry", "Food & Drink"),
 ("ぶどう", "ぶどう", "budō", "grape", "Food & Drink"),
 ("もも", "もも", "momo", "peach", "Food & Drink"),
 ("メロン", "", "meron", "melon", "Food & Drink"),
 ("レモン", "", "remon", "lemon", "Food & Drink"),
 ("すいか", "すいか", "suika", "watermelon", "Food & Drink"),
 ("なし", "なし", "nashi", "pear", "Food & Drink"),
 ("マンゴー", "", "mangō", "mango", "Food & Drink"),
 ("パイナップル", "", "painappuru", "pineapple", "Food & Drink"),
 ("キウイ", "", "kiui", "kiwi fruit", "Food & Drink"),
 ("さくらんぼ", "さくらんぼ", "sakuranbo", "cherry", "Food & Drink"),
 # vegetables
 ("トマト", "", "tomato", "tomato", "Food & Drink"),
 ("じゃがいも", "じゃがいも", "jagaimo", "potato", "Food & Drink"),
 ("にんじん", "にんじん", "ninjin", "carrot", "Food & Drink"),
 ("たまねぎ", "たまねぎ", "tamanegi", "onion", "Food & Drink"),
 ("きゃべつ", "きゃべつ", "kyabetsu", "cabbage", "Food & Drink"),
 ("きゅうり", "きゅうり", "kyūri", "cucumber", "Food & Drink"),
 ("なす", "なす", "nasu", "eggplant", "Food & Drink"),
 ("ピーマン", "", "pīman", "green pepper", "Food & Drink"),
 ("とうもろこし", "とうもろこし", "tōmorokoshi", "corn", "Food & Drink"),
 ("だいこん", "だいこん", "daikon", "daikon radish", "Food & Drink"),
 ("ほうれんそう", "ほうれんそう", "hōrensō", "spinach", "Food & Drink"),
 ("にんにく", "にんにく", "ninniku", "garlic", "Food & Drink"),
 # food & drink
 ("パン", "", "pan", "bread", "Food & Drink"),
 ("たまご", "たまご", "tamago", "egg", "Food & Drink"),
 ("チーズ", "", "chīzu", "cheese", "Food & Drink"),
 ("ラーメン", "", "rāmen", "ramen", "Food & Drink"),
 ("すし", "すし", "sushi", "sushi", "Food & Drink"),
 ("てんぷら", "てんぷら", "tempura", "tempura", "Food & Drink"),
 ("カレー", "", "karē", "curry", "Food & Drink"),
 ("ピザ", "", "piza", "pizza", "Food & Drink"),
 ("ハンバーガー", "", "hanbāgā", "hamburger", "Food & Drink"),
 ("スパゲッティ", "", "supagetti", "spaghetti", "Food & Drink"),
 ("コーヒー", "", "kōhī", "coffee", "Food & Drink"),
 ("ジュース", "", "jūsu", "juice", "Food & Drink"),
 ("ミルク", "", "miruku", "milk", "Food & Drink"),
 ("ビール", "", "bīru", "beer", "Food & Drink"),
 ("ワイン", "", "wain", "wine", "Food & Drink"),
 ("アイスクリーム", "", "aisukurīmu", "ice cream", "Food & Drink"),
 ("ケーキ", "", "kēki", "cake", "Food & Drink"),
 ("チョコレート", "", "chokorēto", "chocolate", "Food & Drink"),
 ("バター", "", "batā", "butter", "Food & Drink"),
 ("さとう", "さとう", "satō", "sugar", "Food & Drink"),
 ("しお", "しお", "shio", "salt", "Food & Drink"),
 # animals
 ("ぞう", "ぞう", "zō", "elephant", "Animals"),
 ("ライオン", "", "raion", "lion", "Animals"),
 ("とら", "とら", "tora", "tiger", "Animals"),
 ("うさぎ", "うさぎ", "usagi", "rabbit", "Animals"),
 ("くま", "くま", "kuma", "bear", "Animals"),
 ("さる", "さる", "saru", "monkey", "Animals"),
 ("パンダ", "", "panda", "panda", "Animals"),
 ("きりん", "きりん", "kirin", "giraffe", "Animals"),
 ("ペンギン", "", "pengin", "penguin", "Animals"),
 ("くじら", "くじら", "kujira", "whale", "Animals"),
 ("いるか", "いるか", "iruka", "dolphin", "Animals"),
 ("ねずみ", "ねずみ", "nezumi", "mouse", "Animals"),
 ("かえる", "かえる", "kaeru", "frog", "Animals"),
 ("へび", "へび", "hebi", "snake", "Animals"),
 ("かめ", "かめ", "kame", "turtle", "Animals"),
 ("きつね", "きつね", "kitsune", "fox", "Animals"),
 ("しか", "しか", "shika", "deer", "Animals"),
 ("こあら", "こあら", "koara", "koala", "Animals"),
 # electronics / objects
 ("パソコン", "", "pasokon", "computer", "Everyday Objects & Ideas"),
 ("でんわ", "でんわ", "denwa", "telephone", "Everyday Objects & Ideas"),
 ("スマートフォン", "", "sumātofon", "smartphone", "Everyday Objects & Ideas"),
 ("カメラ", "", "kamera", "camera", "Everyday Objects & Ideas"),
 ("テレビ", "", "terebi", "television", "Everyday Objects & Ideas"),
 ("インターネット", "", "intānetto", "internet", "Everyday Objects & Ideas"),
 ("じてんしゃ", "じてんしゃ", "jitensha", "bicycle", "Out & About"),
 ("ひこうき", "ひこうき", "hikōki", "airplane", "Out & About"),
 ("タクシー", "", "takushī", "taxi", "Out & About"),
 ("ふね", "ふね", "fune", "ship, boat", "Out & About"),
 ("かさ", "かさ", "kasa", "umbrella", "Everyday Objects & Ideas"),
 ("とけい", "とけい", "tokei", "clock, watch", "Everyday Objects & Ideas"),
 ("かばん", "かばん", "kaban", "bag", "Everyday Objects & Ideas"),
 ("めがね", "めがね", "megane", "glasses", "Everyday Objects & Ideas"),
 ("いす", "いす", "isu", "chair", "Everyday Objects & Ideas"),
 ("つくえ", "つくえ", "tsukue", "desk", "Everyday Objects & Ideas"),
 ("ノート", "", "nōto", "notebook", "Everyday Objects & Ideas"),
 ("ペン", "", "pen", "pen", "Everyday Objects & Ideas"),
 ("かぎ", "かぎ", "kagi", "key", "Everyday Objects & Ideas"),
 # clothing
 ("シャツ", "", "shatsu", "shirt", "Everyday Objects & Ideas"),
 ("ズボン", "", "zubon", "pants", "Everyday Objects & Ideas"),
 ("くつ", "くつ", "kutsu", "shoes", "Everyday Objects & Ideas"),
 ("ぼうし", "ぼうし", "bōshi", "hat", "Everyday Objects & Ideas"),
 ("スカート", "", "sukāto", "skirt", "Everyday Objects & Ideas"),
 ("くつした", "くつした", "kutsushita", "socks", "Everyday Objects & Ideas"),
 ("コート", "", "kōto", "coat", "Everyday Objects & Ideas"),
 ("てぶくろ", "てぶくろ", "tebukuro", "gloves", "Everyday Objects & Ideas"),
 # weather
 ("はれ", "はれ", "hare", "sunny", "Nature & Weather"),
 ("くもり", "くもり", "kumori", "cloudy", "Nature & Weather"),
 ("たいふう", "たいふう", "taifū", "typhoon", "Nature & Weather"),
 ("かみなり", "かみなり", "kaminari", "thunder", "Nature & Weather"),
 ("にじ", "にじ", "niji", "rainbow", "Nature & Weather"),
 # sports
 ("サッカー", "", "sakkā", "soccer", "Everyday Objects & Ideas"),
 ("やきゅう", "やきゅう", "yakyū", "baseball", "Everyday Objects & Ideas"),
 ("テニス", "", "tenisu", "tennis", "Everyday Objects & Ideas"),
 ("バスケットボール", "", "basukettobōru", "basketball", "Everyday Objects & Ideas"),
 ("すいえい", "すいえい", "suiei", "swimming", "Everyday Objects & Ideas"),
 # places
 ("レストラン", "", "resutoran", "restaurant", "Places & Buildings"),
 ("ホテル", "", "hoteru", "hotel", "Places & Buildings"),
 ("くうこう", "くうこう", "kūkō", "airport", "Places & Buildings"),
 ("ぎんこう", "ぎんこう", "ginkō", "bank", "Places & Buildings"),
 ("びょういん", "びょういん", "byōin", "hospital", "Places & Buildings"),
 ("こうばん", "こうばん", "kōban", "police box", "Places & Buildings"),
 ("びじゅつかん", "びじゅつかん", "bijutsukan", "art museum", "Places & Buildings"),
 # family (extended, not in the kanji book's basic set)
 ("そふ", "そふ", "sofu", "grandfather", "Family & People"),
 ("そぼ", "そぼ", "sobo", "grandmother", "Family & People"),
 ("おじ", "おじ", "oji", "uncle", "Family & People"),
 ("おば", "おば", "oba", "aunt", "Family & People"),
 # colors (extended beyond the book's basic set)
 ("ピンク", "", "pinku", "pink", "Colors"),
 ("むらさき", "むらさき", "murasaki", "purple", "Colors"),
 ("オレンジいろ", "オレンジいろ", "orenji-iro", "orange (color)", "Colors"),
 ("ちゃいろ", "ちゃいろ", "chairo", "brown", "Colors"),
 ("はいいろ", "はいいろ", "haiiro", "gray", "Colors"),
]

out = []
for word, reading, romaji, meaning, category in COMMON:
    out.append({
        "word": word,
        "reading": reading or word,
        "romaji": romaji,
        "meaning": meaning,
        "category": category,
    })

with open("data/common_words.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)

print(len(out), "common words saved")
