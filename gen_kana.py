import json

# Standard hiragana chart: (char, romaji, group)
hiragana_basic = [
 ("あ","a","vowel"),("い","i","vowel"),("う","u","vowel"),("え","e","vowel"),("お","o","vowel"),
 ("か","ka","k"),("き","ki","k"),("く","ku","k"),("け","ke","k"),("こ","ko","k"),
 ("さ","sa","s"),("し","shi","s"),("す","su","s"),("せ","se","s"),("そ","so","s"),
 ("た","ta","t"),("ち","chi","t"),("つ","tsu","t"),("て","te","t"),("と","to","t"),
 ("な","na","n"),("に","ni","n"),("ぬ","nu","n"),("ね","ne","n"),("の","no","n"),
 ("は","ha","h"),("ひ","hi","h"),("ふ","fu","h"),("へ","he","h"),("ほ","ho","h"),
 ("ま","ma","m"),("み","mi","m"),("む","mu","m"),("め","me","m"),("も","mo","m"),
 ("や","ya","y"),("ゆ","yu","y"),("よ","yo","y"),
 ("ら","ra","r"),("り","ri","r"),("る","ru","r"),("れ","re","r"),("ろ","ro","r"),
 ("わ","wa","w"),("を","wo","w"),("ん","n","n-special"),
]
hiragana_dakuten = [
 ("が","ga","g"),("ぎ","gi","g"),("ぐ","gu","g"),("げ","ge","g"),("ご","go","g"),
 ("ざ","za","z"),("じ","ji","z"),("ず","zu","z"),("ぜ","ze","z"),("ぞ","zo","z"),
 ("だ","da","d"),("ぢ","ji","d"),("づ","zu","d"),("で","de","d"),("ど","do","d"),
 ("ば","ba","b"),("び","bi","b"),("ぶ","bu","b"),("べ","be","b"),("ぼ","bo","b"),
 ("ぱ","pa","p"),("ぴ","pi","p"),("ぷ","pu","p"),("ぺ","pe","p"),("ぽ","po","p"),
]
hiragana_yoon = [
 ("きゃ","kya"),("きゅ","kyu"),("きょ","kyo"),
 ("しゃ","sha"),("しゅ","shu"),("しょ","sho"),
 ("ちゃ","cha"),("ちゅ","chu"),("ちょ","cho"),
 ("にゃ","nya"),("にゅ","nyu"),("にょ","nyo"),
 ("ひゃ","hya"),("ひゅ","hyu"),("ひょ","hyo"),
 ("みゃ","mya"),("みゅ","myu"),("みょ","myo"),
 ("りゃ","rya"),("りゅ","ryu"),("りょ","ryo"),
 ("ぎゃ","gya"),("ぎゅ","gyu"),("ぎょ","gyo"),
 ("じゃ","ja"),("じゅ","ju"),("じょ","jo"),
 ("びゃ","bya"),("びゅ","byu"),("びょ","byo"),
 ("ぴゃ","pya"),("ぴゅ","pyu"),("ぴょ","pyo"),
]

def to_katakana(h):
    # map hiragana char(s) to katakana via unicode offset trick for basic single chars
    out = ""
    for ch in h:
        code = ord(ch)
        if 0x3041 <= code <= 0x3096:
            out += chr(code + 0x60)
        else:
            out += ch
    return out

hiragana_data = []
for ch, r, g in hiragana_basic:
    hiragana_data.append({"char": ch, "romaji": r, "group": g, "type": "basic"})
for ch, r, g in hiragana_dakuten:
    hiragana_data.append({"char": ch, "romaji": r, "group": g, "type": "dakuten"})
for ch, r in hiragana_yoon:
    hiragana_data.append({"char": ch, "romaji": r, "group": ch[0], "type": "yoon"})

katakana_data = []
for ch, r, g in hiragana_basic:
    katakana_data.append({"char": to_katakana(ch), "romaji": r, "group": g, "type": "basic"})
for ch, r, g in hiragana_dakuten:
    katakana_data.append({"char": to_katakana(ch), "romaji": r, "group": g, "type": "dakuten"})
for ch, r in hiragana_yoon:
    katakana_data.append({"char": to_katakana(ch), "romaji": r, "group": to_katakana(ch[0]), "type": "yoon"})

# fix known irregular katakana forms not covered by simple offset (none needed for standard set)
# katakana ヲ(wo) and ン(n) offsets work fine with +0x60 trick since it's a consistent block shift.

with open("data/hiragana.json","w",encoding="utf-8") as f:
    json.dump(hiragana_data, f, ensure_ascii=False, indent=1)
with open("data/katakana.json","w",encoding="utf-8") as f:
    json.dump(katakana_data, f, ensure_ascii=False, indent=1)

print(len(hiragana_data), len(katakana_data))
print(katakana_data[:5], katakana_data[45:50])
