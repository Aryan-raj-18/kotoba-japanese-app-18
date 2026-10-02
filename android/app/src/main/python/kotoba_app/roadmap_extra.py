# -*- coding: utf-8 -*-
"""
Roadmap v2.9 additions, merged into data/roadmap.json by gen_roadmap.py:

  * EXTRA_VOCAB   - fuller word lists for every existing lesson chapter
                    (all colours & shapes, all months, all family members...)
  * RADICAL section (intro + 7 learning chapters + explorer) built from
    data/radicals.json
  * NEW_GRAMMAR   - five grammar chapters: noun modification, ながら,
                    giving reasons, plans/intentions, てみる/ておく/てしまう
                    (topics follow a typical intermediate grammar workbook;
                    every explanation and example sentence is original)
  * GRAND REVIEW  - final section: a 40-question mixed practice

One vocab line = jp|reading|romaji|meaning
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent


def parse(block):
    out = []
    for line in block.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        jp, reading, romaji, meaning = [p.strip() for p in line.split("|")]
        out.append({"jp": jp, "reading": reading, "romaji": romaji, "meaning": meaning})
    return out


EXTRA_VOCAB = {}

EXTRA_VOCAB["greetings-intro"] = """
いってきます|いってきます|ittekimasu|I'm off (leaving home)
いってらっしゃい|いってらっしゃい|itterasshai|see you later (to someone leaving)
ただいま|ただいま|tadaima|I'm home
おかえりなさい|おかえりなさい|okaerinasai|welcome home
いただきます|いただきます|itadakimasu|thanks for the food (before eating)
ごちそうさまでした|ごちそうさまでした|gochisōsama deshita|thanks for the meal (after eating)
おやすみなさい|おやすみなさい|oyasuminasai|good night
どういたしまして|どういたしまして|dō itashimashite|you're welcome
ごめんなさい|ごめんなさい|gomennasai|I'm sorry
いらっしゃいませ|いらっしゃいませ|irasshaimase|welcome (in a shop)
お久しぶりです|おひさしぶりです|ohisashiburi desu|long time no see
お願いします|おねがいします|onegai shimasu|please
"""

EXTRA_VOCAB["numbers-1-100"] = """
零|れい|rei|zero
十一|じゅういち|jūichi|eleven
十五|じゅうご|jūgo|fifteen
二十五|にじゅうご|nijūgo|twenty-five
三十|さんじゅう|sanjū|thirty
四十|よんじゅう|yonjū|forty
五十|ごじゅう|gojū|fifty
六十|ろくじゅう|rokujū|sixty
七十|ななじゅう|nanajū|seventy
八十|はちじゅう|hachijū|eighty
九十|きゅうじゅう|kyūjū|ninety
九十九|きゅうじゅうきゅう|kyūjūkyū|ninety-nine
二百|にひゃく|nihyaku|two hundred
三百|さんびゃく|sanbyaku|three hundred
千|せん|sen|one thousand
一万|いちまん|ichiman|ten thousand
"""

EXTRA_VOCAB["colors-shapes"] = """
オレンジ色|オレンジいろ|orenji iro|orange
ピンク|ピンク|pinku|pink
紫|むらさき|murasaki|purple
灰色|はいいろ|hai iro|gray
水色|みずいろ|mizu iro|light blue
金色|きんいろ|kin iro|gold
銀色|ぎんいろ|gin iro|silver
赤い|あかい|akai|red (adjective)
青い|あおい|aoi|blue (adjective)
黄色い|きいろい|kiiroi|yellow (adjective)
白い|しろい|shiroi|white (adjective)
黒い|くろい|kuroi|black (adjective)
茶色い|ちゃいろい|chairoi|brown (adjective)
濃い|こい|koi|dark, deep (colour)
薄い|うすい|usui|light, pale (colour)
円形|えんけい|enkei|circle
星|ほし|hoshi|star
ハート|ハート|hāto|heart shape
長方形|ちょうほうけい|chōhōkei|rectangle
正方形|せいほうけい|seihōkei|square (regular)
楕円|だえん|daen|oval
ひし形|ひしがた|hishigata|diamond, rhombus
五角形|ごかっけい|gokakkei|pentagon
六角形|ろっかくけい|rokkakukei|hexagon
球|きゅう|kyū|sphere
立方体|りっぽうたい|rippōtai|cube
直線|ちょくせん|chokusen|straight line
曲線|きょくせん|kyokusen|curve
点|てん|ten|dot, point
"""

EXTRA_VOCAB["my-family"] = """
祖父|そふ|sofu|grandfather (my)
祖母|そぼ|sobo|grandmother (my)
おじいさん|おじいさん|ojīsan|grandfather / old man
おばあさん|おばあさん|obāsan|grandmother / old woman
父|ちち|chichi|father (my)
母|はは|haha|mother (my)
兄|あに|ani|older brother (my)
姉|あね|ane|older sister (my)
弟|おとうと|otōto|younger brother
妹|いもうと|imōto|younger sister
兄弟|きょうだい|kyōdai|siblings, brothers
姉妹|しまい|shimai|sisters
おじさん|おじさん|ojisan|uncle
おばさん|おばさん|obasan|aunt
いとこ|いとこ|itoko|cousin
子供|こども|kodomo|child
赤ちゃん|あかちゃん|akachan|baby
親戚|しんせき|shinseki|relatives
夫婦|ふうふ|fūfu|married couple
"""

EXTRA_VOCAB["my-house"] = """
居間|いま|ima|living room
階段|かいだん|kaidan|stairs
屋根|やね|yane|roof
壁|かべ|kabe|wall
床|ゆか|yuka|floor
天井|てんじょう|tenjō|ceiling
ドア|ドア|doa|door
トイレ|トイレ|toire|toilet
ソファ|ソファ|sofa|sofa
エアコン|エアコン|eakon|air conditioner
洗濯機|せんたくき|sentakuki|washing machine
電子レンジ|でんしレンジ|denshi renji|microwave oven
鏡|かがみ|kagami|mirror
畳|たたみ|tatami|tatami mat
布団|ふとん|futon|futon bedding
カーテン|カーテン|kāten|curtain
引き出し|ひきだし|hikidashi|drawer
鍵|かぎ|kagi|key
ベランダ|ベランダ|beranda|balcony
"""

EXTRA_VOCAB["human-body"] = """
目|め|me|eye
耳|みみ|mimi|ear
鼻|はな|hana|nose
口|くち|kuchi|mouth
髪|かみ|kami|hair
手|て|te|hand
足|あし|ashi|foot, leg
背中|せなか|senaka|back
腰|こし|koshi|waist, lower back
舌|した|shita|tongue
喉|のど|nodo|throat
爪|つめ|tsume|nail
肘|ひじ|hiji|elbow
手首|てくび|tekubi|wrist
足首|あしくび|ashikubi|ankle
額|ひたい|hitai|forehead
頬|ほお|hō|cheek
顎|あご|ago|chin, jaw
骨|ほね|hone|bone
血|ち|chi|blood
体|からだ|karada|body
"""

EXTRA_VOCAB["daily-routines"] = """
顔を洗う|かおをあらう|kao o arau|wash one's face
シャワーを浴びる|シャワーをあびる|shawā o abiru|take a shower
お風呂に入る|おふろにはいる|ofuro ni hairu|take a bath
着替える|きがえる|kigaeru|change clothes
出かける|でかける|dekakeru|go out
通勤する|つうきんする|tsūkin suru|commute to work
料理する|りょうりする|ryōri suru|cook
洗濯する|せんたくする|sentaku suru|do laundry
買い物する|かいものする|kaimono suru|go shopping
昼寝する|ひるねする|hirune suru|take a nap
目が覚める|めがさめる|me ga sameru|wake up
テレビを見る|テレビをみる|terebi o miru|watch TV
宿題をする|しゅくだいをする|shukudai o suru|do homework
"""

EXTRA_VOCAB["telling-time"] = """
二時|にじ|niji|two o'clock
三時|さんじ|sanji|three o'clock
五時|ごじ|goji|five o'clock
六時|ろくじ|rokuji|six o'clock
八時|はちじ|hachiji|eight o'clock
十時|じゅうじ|jūji|ten o'clock
十一時|じゅういちじ|jūichiji|eleven o'clock
一分|いっぷん|ippun|one minute
五分|ごふん|gofun|five minutes
十五分|じゅうごふん|jūgofun|fifteen minutes
三十分|さんじゅっぷん|sanjuppun|thirty minutes
秒|びょう|byō|second
時間|じかん|jikan|hour, time
何分|なんぷん|nanpun|how many minutes
朝|あさ|asa|morning
昼|ひる|hiru|noon, daytime
夕方|ゆうがた|yūgata|evening
夜|よる|yoru|night
遅刻|ちこく|chikoku|being late
時計|とけい|tokei|clock, watch
"""

EXTRA_VOCAB["days-dates"] = """
一月|いちがつ|ichigatsu|January
二月|にがつ|nigatsu|February
三月|さんがつ|sangatsu|March
四月|しがつ|shigatsu|April
五月|ごがつ|gogatsu|May
六月|ろくがつ|rokugatsu|June
七月|しちがつ|shichigatsu|July
八月|はちがつ|hachigatsu|August
九月|くがつ|kugatsu|September
十月|じゅうがつ|jūgatsu|October
十一月|じゅういちがつ|jūichigatsu|November
十二月|じゅうにがつ|jūnigatsu|December
一日|ついたち|tsuitachi|the 1st (of the month)
二日|ふつか|futsuka|the 2nd / two days
十日|とおか|tōka|the 10th
二十日|はつか|hatsuka|the 20th
毎日|まいにち|mainichi|every day
毎週|まいしゅう|maishū|every week
先週|せんしゅう|senshū|last week
今月|こんげつ|kongetsu|this month
来月|らいげつ|raigetsu|next month
今年|ことし|kotoshi|this year
去年|きょねん|kyonen|last year
来年|らいねん|rainen|next year
一昨日|おととい|ototoi|the day before yesterday
明後日|あさって|asatte|the day after tomorrow
週末|しゅうまつ|shūmatsu|weekend
何日|なんにち|nannichi|what day of the month
"""

EXTRA_VOCAB["around-town"] = """
コンビニ|コンビニ|konbini|convenience store
スーパー|スーパー|sūpā|supermarket
デパート|デパート|depāto|department store
レストラン|レストラン|resutoran|restaurant
映画館|えいがかん|eigakan|movie theater
美術館|びじゅつかん|bijutsukan|art museum
薬局|やっきょく|yakkyoku|pharmacy
本屋|ほんや|hon'ya|bookstore
花屋|はなや|hanaya|flower shop
市役所|しやくしょ|shiyakusho|city hall
動物園|どうぶつえん|dōbutsuen|zoo
駐車場|ちゅうしゃじょう|chūshajō|parking lot
喫茶店|きっさてん|kissaten|coffee shop
信号|しんごう|shingō|traffic light
交差点|こうさてん|kōsaten|intersection
歩道|ほどう|hodō|sidewalk
"""

EXTRA_VOCAB["asking-directions-rm"] = """
上|うえ|ue|above, up
下|した|shita|below, down
前|まえ|mae|front, before
後ろ|うしろ|ushiro|behind
隣|となり|tonari|next to
横|よこ|yoko|beside, side
中|なか|naka|inside
外|そと|soto|outside
間|あいだ|aida|between
向かい|むかい|mukai|opposite, across
角|かど|kado|corner
遠い|とおい|tōi|far
歩く|あるく|aruku|to walk
渡る|わたる|wataru|to cross
戻る|もどる|modoru|to go back
突き当たり|つきあたり|tsukiatari|end of the road
真ん中|まんなか|mannaka|the middle
"""

EXTRA_VOCAB["transportation"] = """
地下鉄|ちかてつ|chikatetsu|subway
ホーム|ホーム|hōmu|station platform
改札|かいさつ|kaisatsu|ticket gate
乗る|のる|noru|to ride, get on
降りる|おりる|oriru|to get off
乗り換える|のりかえる|norikaeru|to transfer
片道|かたみち|katamichi|one way
往復|おうふく|ōfuku|round trip
時刻表|じこくひょう|jikokuhyō|timetable
運賃|うんちん|unchin|fare
定期券|ていきけん|teikiken|commuter pass
トラック|トラック|torakku|truck
道路|どうろ|dōro|road
高速道路|こうそくどうろ|kōsoku dōro|expressway
徒歩|とほ|toho|on foot
渋滞|じゅうたい|jūtai|traffic jam
"""

EXTRA_VOCAB["going-shopping-rm"] = """
試着|しちゃく|shichaku|trying on clothes
試着室|しちゃくしつ|shichakushitsu|fitting room
売り切れ|うりきれ|urikire|sold out
レジ|レジ|reji|cash register
財布|さいふ|saifu|wallet
おつり|おつり|otsuri|change (money back)
商品|しょうひん|shōhin|product
サイズ|サイズ|saizu|size
返品|へんぴん|henpin|returning goods
会計|かいけい|kaikei|checkout, bill
税込み|ぜいこみ|zeikomi|tax included
払う|はらう|harau|to pay
買い物|かいもの|kaimono|shopping
包む|つつむ|tsutsumu|to wrap
"""

EXTRA_VOCAB["talking-about-money-rm"] = """
給料|きゅうりょう|kyūryō|salary
口座|こうざ|kōza|bank account
振り込み|ふりこみ|furikomi|bank transfer
両替|りょうがえ|ryōgae|currency exchange
利子|りし|rishi|interest
値上げ|ねあげ|neage|price increase
節約|せつやく|setsuyaku|saving, thrift
支払い|しはらい|shiharai|payment
請求書|せいきゅうしょ|seikyūsho|invoice
暗証番号|あんしょうばんごう|anshō bangō|PIN number
百円|ひゃくえん|hyakuen|100 yen
五百円|ごひゃくえん|gohyakuen|500 yen
"""

EXTRA_VOCAB["seasons-weather"] = """
梅雨|つゆ|tsuyu|rainy season
台風|たいふう|taifū|typhoon
桜|さくら|sakura|cherry blossom
紅葉|こうよう|kōyō|autumn leaves
暑い|あつい|atsui|hot (weather)
寒い|さむい|samui|cold (weather)
涼しい|すずしい|suzushii|cool, refreshing
蒸し暑い|むしあつい|mushiatsui|hot and humid
気温|きおん|kion|temperature
天気予報|てんきよほう|tenki yohō|weather forecast
傘|かさ|kasa|umbrella
虹|にじ|niji|rainbow
雷|かみなり|kaminari|thunder
雲|くも|kumo|cloud
霧|きり|kiri|fog
"""

EXTRA_VOCAB["holidays-festivals"] = """
お正月|おしょうがつ|oshōgatsu|New Year holiday
初詣|はつもうで|hatsumōde|first shrine visit of the year
成人の日|せいじんのひ|seijin no hi|Coming of Age Day
お花見|おはなみ|ohanami|cherry blossom viewing
子供の日|こどものひ|kodomo no hi|Children's Day
母の日|ははのひ|haha no hi|Mother's Day
お盆|おぼん|obon|Obon (summer ancestors' festival)
大晦日|おおみそか|ōmisoka|New Year's Eve
お祭り|おまつり|omatsuri|festival
七五三|しちごさん|shichigosan|7-5-3 children's festival
神社|じんじゃ|jinja|Shinto shrine
お寺|おてら|otera|Buddhist temple
"""

EXTRA_VOCAB["hobbies-music"] = """
趣味|しゅみ|shumi|hobby
読書|どくしょ|dokusho|reading
映画|えいが|eiga|movie
写真|しゃしん|shashin|photograph
料理|りょうり|ryōri|cooking
釣り|つり|tsuri|fishing
旅行|りょこう|ryokō|travel
野球|やきゅう|yakyū|baseball
サッカー|サッカー|sakkā|soccer
バスケットボール|バスケットボール|basukettobōru|basketball
歌う|うたう|utau|to sing
音楽|おんがく|ongaku|music
太鼓|たいこ|taiko|drum
柔道|じゅうどう|jūdō|judo
空手|からて|karate|karate
剣道|けんどう|kendō|kendo
"""

EXTRA_VOCAB["at-work-rm"] = """
社長|しゃちょう|shachō|company president
部長|ぶちょう|buchō|department manager
課長|かちょう|kachō|section manager
会議|かいぎ|kaigi|meeting
名刺|めいし|meishi|business card
出張|しゅっちょう|shutchō|business trip
休暇|きゅうか|kyūka|vacation, leave
履歴書|りれきしょ|rirekisho|résumé
面接|めんせつ|mensetsu|interview
書類|しょるい|shorui|documents
契約|けいやく|keiyaku|contract
営業|えいぎょう|eigyō|sales
会社員|かいしゃいん|kaishain|office worker
上司|じょうし|jōshi|boss, superior
部下|ぶか|buka|subordinate
締め切り|しめきり|shimekiri|deadline
"""

EXTRA_VOCAB["at-school-rm"] = """
授業|じゅぎょう|jugyō|class, lesson
学期|がっき|gakki|school term
卒業|そつぎょう|sotsugyō|graduation
入学|にゅうがく|nyūgaku|entering school
制服|せいふく|seifuku|uniform
鉛筆|えんぴつ|enpitsu|pencil
ノート|ノート|nōto|notebook
教科書|きょうかしょ|kyōkasho|textbook
消しゴム|けしゴム|keshigomu|eraser
歴史|れきし|rekishi|history
国語|こくご|kokugo|Japanese (school subject)
美術|びじゅつ|bijutsu|art (school subject)
給食|きゅうしょく|kyūshoku|school lunch
校長|こうちょう|kōchō|principal
成績|せいせき|seiseki|grades
質問|しつもん|shitsumon|question
答え|こたえ|kotae|answer
"""

EXTRA_VOCAB["japanese-food"] = """
刺身|さしみ|sashimi|sashimi
天ぷら|てんぷら|tenpura|tempura
うどん|うどん|udon|udon noodles
ラーメン|ラーメン|rāmen|ramen
焼き鳥|やきとり|yakitori|grilled chicken skewers
すき焼き|すきやき|sukiyaki|sukiyaki
おにぎり|おにぎり|onigiri|rice ball
納豆|なっとう|nattō|fermented soybeans
漬物|つけもの|tsukemono|pickles
豆腐|とうふ|tōfu|tofu
海苔|のり|nori|seaweed sheet
醤油|しょうゆ|shōyu|soy sauce
味噌|みそ|miso|miso
弁当|べんとう|bentō|boxed lunch
餃子|ぎょうざ|gyōza|dumplings
和食|わしょく|washoku|Japanese cuisine
"""

EXTRA_VOCAB["fruits-veg-drinks"] = """
バナナ|バナナ|banana|banana
ぶどう|ぶどう|budō|grapes
桃|もも|momo|peach
すいか|すいか|suika|watermelon
レモン|レモン|remon|lemon
トマト|トマト|tomato|tomato
きゅうり|きゅうり|kyūri|cucumber
にんじん|にんじん|ninjin|carrot
じゃがいも|じゃがいも|jagaimo|potato
玉ねぎ|たまねぎ|tamanegi|onion
キャベツ|キャベツ|kyabetsu|cabbage
大根|だいこん|daikon|daikon radish
ビール|ビール|bīru|beer
ワイン|ワイン|wain|wine
日本酒|にほんしゅ|nihonshu|sake
お茶|おちゃ|ocha|green tea
紅茶|こうちゃ|kōcha|black tea
"""

EXTRA_VOCAB["at-the-market-rm"] = """
八百屋|やおや|yaoya|greengrocer
魚屋|さかなや|sakanaya|fishmonger
肉屋|にくや|nikuya|butcher
値切る|ねぎる|negiru|to haggle
旬|しゅん|shun|in season
特売|とくばい|tokubai|special sale
賞味期限|しょうみきげん|shōmi kigen|best-before date
冷凍|れいとう|reitō|frozen
冷たい|つめたい|tsumetai|cold (to touch)
温かい|あたたかい|atatakai|warm (food, drinks)
美味しい|おいしい|oishii|delicious
甘い|あまい|amai|sweet
辛い|からい|karai|spicy
酸っぱい|すっぱい|suppai|sour
苦い|にがい|nigai|bitter
"""

EXTRA_VOCAB["computers-internet"] = """
ノートパソコン|ノートパソコン|nōto pasokon|laptop
プリンター|プリンター|purintā|printer
ソフト|ソフト|sofuto|software
ログインする|ログインする|roguin suru|to log in
ユーザー|ユーザー|yūzā|user
ケーブル|ケーブル|kēburu|cable
無線|むせん|musen|wireless
クリックする|クリックする|kurikku suru|to click
送信する|そうしんする|sōshin suru|to send
削除する|さくじょする|sakujo suru|to delete
画像|がぞう|gazō|image
文書|ぶんしょ|bunsho|document
接続する|せつぞくする|setsuzoku suru|to connect
"""

EXTRA_VOCAB["smartphones-apps"] = """
着信|ちゃくしん|chakushin|incoming call
電波|でんぱ|denpa|signal, radio wave
音量|おんりょう|onryō|volume
バッテリー|バッテリー|batterī|battery
充電する|じゅうでんする|jūden suru|to charge
連絡する|れんらくする|renraku suru|to contact
既読|きどく|kidoku|read (message status)
スタンプ|スタンプ|sutanpu|sticker (chat)
ゲーム|ゲーム|gēmu|game
写真を撮る|しゃしんをとる|shashin o toru|to take a photo
"""

EXTRA_VOCAB["health-doctor"] = """
頭痛|ずつう|zutsū|headache
熱がある|ねつがある|netsu ga aru|have a fever
診察|しんさつ|shinsatsu|medical examination
処方箋|しょほうせん|shohōsen|prescription
入院する|にゅういんする|nyūin suru|to be hospitalized
手術|しゅじゅつ|shujutsu|surgery
予約|よやく|yoyaku|appointment, reservation
保険|ほけん|hoken|insurance
体温|たいおん|taion|body temperature
アレルギー|アレルギー|arerugī|allergy
症状|しょうじょう|shōjō|symptom
けが|けが|kega|injury
休む|やすむ|yasumu|to rest
痛い|いたい|itai|painful
"""

EXTRA_VOCAB["the-environment"] = """
森|もり|mori|forest
山|やま|yama|mountain
湖|みずうみ|mizūmi|lake
自然|しぜん|shizen|nature
地球|ちきゅう|chikyū|the Earth
温暖化|おんだんか|ondanka|global warming
リサイクル|リサイクル|risaikuru|recycling
ごみ|ごみ|gomi|trash
節電|せつでん|setsuden|saving electricity
資源|しげん|shigen|resources
動物|どうぶつ|dōbutsu|animal
植物|しょくぶつ|shokubutsu|plant
環境|かんきょう|kankyō|environment
汚染|おせん|osen|pollution
"""

EXTRA_VOCAB["particles-wa-ga-o"] = """
か|か|ka|question marker
や|や|ya|and (a non-exhaustive list)
ね|ね|ne|isn't it? (seeking agreement)
よ|よ|yo|I tell you (emphasis)
だけ|だけ|dake|only, just
しか|しか|shika|nothing but (with negative)
"""

EXTRA_VOCAB["particles-ni-de-e"] = """
ぐらい|ぐらい|gurai|about, approximately
ごろ|ごろ|goro|around (a time)
ずつ|ずつ|zutsu|each, at a time
"""

EXTRA_VOCAB["adjectives-opposites-rm"] = """
多い|おおい|ōi|many
少ない|すくない|sukunai|few
強い|つよい|tsuyoi|strong
弱い|よわい|yowai|weak
明るい|あかるい|akarui|bright
暗い|くらい|kurai|dark
広い|ひろい|hiroi|spacious
狭い|せまい|semai|narrow, cramped
太い|ふとい|futoi|thick
細い|ほそい|hosoi|thin, slender
易しい|やさしい|yasashii|easy
楽しい|たのしい|tanoshii|fun
面白い|おもしろい|omoshiroi|interesting
つまらない|つまらない|tsumaranai|boring
きれい|きれい|kirei|pretty, clean
汚い|きたない|kitanai|dirty
賑やか|にぎやか|nigiyaka|lively
有名|ゆうめい|yūmei|famous
便利|べんり|benri|convenient
"""

EXTRA_VOCAB["counters-rm"] = """
一回|いっかい|ikkai|once, one time
二階|にかい|nikai|second floor
三足|さんぞく|sanzoku|three pairs (shoes, socks)
四羽|よんわ|yonwa|four birds
五軒|ごけん|goken|five houses/shops
六頭|ろくとう|rokutō|six large animals
七歳|ななさい|nanasai|seven years old
何人|なんにん|nannin|how many people
何個|なんこ|nanko|how many pieces
何本|なんぼん|nanbon|how many long objects
何枚|なんまい|nanmai|how many flat objects
"""

EXTRA_VOCAB["sentence-patterns"] = """
ほしいです|ほしいです|hoshii desu|want (a thing)
ないでください|ないでください|naide kudasai|please don't ...
ことがあります|ことがあります|koto ga arimasu|have done ... before
なければなりません|なければなりません|nakereba narimasen|must, have to
でしょう|でしょう|deshō|probably
つもりです|つもりです|tsumori desu|intend to
"""

EXTRA_VOCAB["te-form-basics"] = """
買って|かって|katte|buy (te-form)
読んで|よんで|yonde|read (te-form)
泳いで|およいで|oyoide|swim (te-form)
遊んで|あそんで|asonde|play (te-form)
立って|たって|tatte|stand (te-form)
会って|あって|atte|meet (te-form)
作って|つくって|tsukutte|make (te-form)
言って|いって|itte|say (te-form)
貸して|かして|kashite|lend (te-form)
開けて|あけて|akete|open (te-form)
閉めて|しめて|shimete|close (te-form)
教えて|おしえて|oshiete|teach, tell (te-form)
"""

EXTRA_VOCAB["potential-form"] = """
買える|かえる|kaeru|can buy
会える|あえる|aeru|can meet
使える|つかえる|tsukaeru|can use
走れる|はしれる|hashireru|can run
歌える|うたえる|utaeru|can sing
飛べる|とべる|toberu|can fly
待てる|まてる|materu|can wait
持てる|もてる|moteru|can hold
立てる|たてる|tateru|can stand up
"""

EXTRA_VOCAB["countries-nationalities"] = """
アメリカ|アメリカ|amerika|America
ブラジル|ブラジル|burajiru|Brazil
メキシコ|メキシコ|mekishiko|Mexico
エジプト|エジプト|ejiputo|Egypt
スペイン|スペイン|supein|Spain
ベトナム|ベトナム|betonamu|Vietnam
フィリピン|フィリピン|firipin|Philippines
インドネシア|インドネシア|indoneshia|Indonesia
トルコ|トルコ|toruko|Turkey
オランダ|オランダ|oranda|Netherlands
日本|にほん|nihon|Japan
アメリカ人|アメリカじん|amerikajin|American person
日本人|にほんじん|nihonjin|Japanese person
外国|がいこく|gaikoku|foreign country
外国人|がいこくじん|gaikokujin|foreigner
世界|せかい|sekai|the world
"""

EXTRA_VOCAB["foreign-languages-travel"] = """
日本語|にほんご|nihongo|Japanese language
中国語|ちゅうごくご|chūgokugo|Chinese language
韓国語|かんこくご|kankokugo|Korean language
ドイツ語|ドイツご|doitsugo|German language
通訳|つうやく|tsūyaku|interpreter
翻訳|ほんやく|hon'yaku|translation
観光|かんこう|kankō|sightseeing
出発|しゅっぱつ|shuppatsu|departure
到着|とうちゃく|tōchaku|arrival
税関|ぜいかん|zeikan|customs
入国|にゅうこく|nyūkoku|entering a country
旅館|りょかん|ryokan|Japanese inn
"""


# ------------------------------------------------------------------ radicals --
def build_radical_section(v_fn):
    data = json.loads((ROOT / "data" / "radicals.json").read_text(encoding="utf-8"))
    rads = {r["glyph"]: r for r in data["radicals"]}
    kd = json.loads((ROOT / "data" / "kanji_data.json").read_text(encoding="utf-8"))
    kmean = {e["kanji"]: e["meaning"] for e in kd}
    stories = data["stories"]
    core = [r["glyph"] for r in data["radicals"] if r["core"]]

    groups = [
        ("radicals-people", "People & Strength", "🧍", "亻 人 女 力 口 寸"),
        ("radicals-body", "Heart, Hand & Body", "🫀", "心 忄 手 扌 目 ⺼ 疒"),
        ("radicals-nature", "Sun, Earth & Water", "🌊", "木 水 氵 火 灬 土 月 山 石 雨"),
        ("radicals-plants", "Plants, Fields & Animals", "🌾", "艹 竹 禾 田 玉 王 犬 犭"),
        ("radicals-things", "Money, Cloth & Tools", "🧵", "貝 金 糸 衤 巾 刀 刂 弓 車"),
        ("radicals-words", "Food, Words & Rituals", "🍚", "食 酉 言 示 礻"),
        ("radicals-movement", "Roofs, Roads & Frames", "🏠", "宀 广 尸 囗 彳 辶 攵 阜 邑 大 十 一"),
    ]
    used = set()
    chapters = []
    for cid, title, icon, glyphs in groups:
        glyph_list = glyphs.split()
        used.update(glyph_list)
        chapters.append(radical_chapter(cid, title, icon, glyph_list, rads, stories, kmean, v_fn))
    leftovers = [g for g in core if g not in used]
    if leftovers:
        chapters[-1] = radical_chapter("radicals-movement", "Roofs, Roads & Frames", "🏠",
                                       groups[-1][3].split() + leftovers, rads, stories, kmean, v_fn)


    kanji_basics = {
        "id": "kanji-basics", "title": "What Is Kanji?", "icon": "漢", "kind": "lesson",
        "vocab": parse("""
漢字|かんじ|kanji|Chinese characters
ひらがな|ひらがな|hiragana|hiragana (native syllable script)
カタカナ|カタカナ|katakana|katakana (script for foreign words)
ローマ字|ローマじ|rōmaji|Latin alphabet spelling
文字|もじ|moji|letter, character
単語|たんご|tango|word
読み方|よみかた|yomikata|way of reading
意味|いみ|imi|meaning
書き順|かきじゅん|kakijun|stroke order
画数|かくすう|kakusū|number of strokes
送り仮名|おくりがな|okurigana|kana ending after a kanji
熟語|じゅくご|jukugo|compound word of kanji
常用漢字|じょうようかんじ|jōyō kanji|the 2,136 everyday kanji
"""),
        "sentences": [
            _s("日本語は___、カタカナ、漢字を使います。", "にほんごは___、カタカナ、かんじをつかいます。", "Nihongo wa ___, katakana, kanji o tsukaimasu.", "Japanese uses hiragana, katakana and kanji.", "ひらがな"),
            _s("外国の言葉は___で書きます。", "がいこくのことばは___でかきます。", "Gaikoku no kotoba wa ___ de kakimasu.", "Foreign words are written in katakana.", "カタカナ"),
            _s("「山」は「やま」と読む___です。", "「やま」は「やま」とよむ___です。", "'Yama' wa 'yama' to yomu ___ desu.", "山 is a kanji read 'yama'.", "漢字"),
            _s("この漢字の___が分かりません。", "このかんじの___がわかりません。", "Kono kanji no ___ ga wakarimasen.", "I don't know how to read this kanji.", "読み方"),
            _s("漢字の___を教えてください。", "かんじの___をおしえてください。", "Kanji no ___ o oshiete kudasai.", "Please tell me the meaning of the kanji.", "意味"),
            _s("「日」は四つの___で書きます。", "「ひ」はよっつの___でかきます。", "'Hi' wa yottsu no ___ de kakimasu.", "日 is written with four strokes.", "画数"),
            _s("「食べる」の「べる」は___です。", "「たべる」の「べる」は___です。", "'Taberu' no 'beru' wa ___ desu.", "The 'beru' in 食べる is okurigana.", "送り仮名"),
        ],
        "guide": {
            "intro": "Japanese is written with three scripts at once. Hiragana and katakana are sound scripts (46 letters each). Kanji are Chinese-origin characters that each carry a MEANING, so one kanji can replace a whole word. Learning kanji is easier once you know they are built from parts (radicals).",
            "points": [
                {"pattern": "Three scripts together", "note": "Kanji give the core meaning of nouns, verbs and adjectives; hiragana adds grammar endings and small words; katakana writes foreign words and emphasis.", "jp": "私はコーヒーを飲みます。", "en": "I drink coffee. (私, 飲 = kanji; は, を, み, ます = hiragana; コーヒー = katakana)"},
                {"pattern": "One kanji = one idea, several readings", "note": "A kanji keeps its meaning but can be read in different ways depending on the word it is in.", "jp": "山 = やま / サン", "en": "mountain"},
                {"pattern": "Okurigana (送り仮名)", "note": "Hiragana that follows a kanji stem to show the verb or adjective ending.", "jp": "食べる・食べます・食べた", "en": "eat / eats / ate — the kanji stays, the kana changes"},
                {"pattern": "Stroke order (書き順)", "note": "Write top to bottom, left to right. A horizontal line usually comes before a vertical one that crosses it. Outside frames come before insides, and the bottom line of a box is written last.", "jp": "十・口・国", "en": "ten, mouth, country"},
                {"pattern": "How many kanji?", "note": "About 2,136 common-use (常用) kanji cover newspapers and books. JLPT N5 needs around 100, N4 around 300, N3 around 650.", "jp": "日・月・火・水・木・金・土", "en": "start with the days of the week"},
                {"pattern": "Why radicals help", "note": "Most kanji are a radical (meaning hint) plus another part (often a sound hint). Learn the ~57 common radicals and you can guess the topic of thousands of kanji.", "jp": "海 = 氵 (water) + 毎", "en": "sea"},
            ],
        },
    }

    intro = {
        "id": "radicals-intro", "title": "What Are Radicals?", "icon": "部", "kind": "lesson",
        "vocab": parse("""
漢字|かんじ|kanji|Chinese characters
部首|ぶしゅ|bushu|radical
偏|へん|hen|left-side radical position
旁|つくり|tsukuri|right-side radical position
冠|かんむり|kanmuri|top (crown) radical position
脚|あし|ashi|bottom (legs) radical position
垂れ|たれ|tare|top-left covering radical position
繞|にょう|nyō|left-and-bottom wrapping position
構え|かまえ|kamae|enclosing radical position
画|かく|kaku|stroke
画数|かくすう|kakusū|stroke count
意味|いみ|imi|meaning
音読み|おんよみ|on'yomi|Chinese-style reading
訓読み|くんよみ|kun'yomi|Japanese-style reading
"""),
        "sentences": [
            {"jp": "「休」の___は「にんべん」です。", "reading": "「やすむ」の___は「にんべん」です。",
             "romaji": "'Yasumu' no ___ wa 'ninben' desu.", "english": "The radical of 休 is ninben.", "blank": "部首"},
            {"jp": "「海」の左側の___は「さんずい」です。", "reading": "「うみ」のひだりがわの___は「さんずい」です。",
             "romaji": "'Umi' no hidarigawa no ___ wa 'sanzui' desu.", "english": "The left-side radical of 海 is sanzui.", "blank": "偏"},
            {"jp": "「家」の上の部分は「うかんむり」という___です。", "reading": "「いえ」のうえのぶぶんは「うかんむり」という___です。",
             "romaji": "'Ie' no ue no bubun wa 'ukanmuri' to iu ___ desu.", "english": "The top part of 家 is the crown-position radical called ukanmuri.", "blank": "冠"},
            {"jp": "「日」は四つの___で書きます。", "reading": "「ひ」はよっつの___でかきます。",
             "romaji": "'Hi' wa yottsu no ___ de kakimasu.", "english": "日 is written with four strokes.", "blank": "画"},
            {"jp": "この___は「ニチ」「ジツ」と読みます。", "reading": "この___は「ニチ」「ジツ」とよみます。",
             "romaji": "Kono ___ wa 'nichi' 'jitsu' to yomimasu.", "english": "This reading is 'nichi' and 'jitsu' - the Chinese-style reading.", "blank": "音読み"},
            {"jp": "この漢字の___は「木」です。", "reading": "このかんじの___は「き」です。",
             "romaji": "Kono kanji no ___ wa 'ki' desu.", "english": "The radical of this kanji is 木 (tree).", "blank": "部首"},
        ],
        "guide": {
            "intro": "Most kanji are built from smaller parts. One of those parts - the radical (部首, bushu) - hints at the meaning. Learn a few dozen radicals and new kanji stop looking like random strokes.",
            "points": [
                {"pattern": "Radical = meaning hint", "note": "The radical tells you the topic of the kanji. Water radical 氵 = liquids and seas.", "jp": "海・泳・洗", "en": "sea, swim, wash - all water"},
                {"pattern": "Radicals change shape", "note": "On the side of a kanji some radicals squash: 人→亻, 水→氵, 心→忄, 手→扌, 犬→犭.", "jp": "休・海・忙・持", "en": "rest, sea, busy, hold"},
                {"pattern": "Six positions", "note": "hen (left), tsukuri (right), kanmuri (top), ashi (bottom), tare (hanging), nyō (wrapping), kamae (enclosing).", "jp": "何・欠・家・思・病・道・国", "en": "one example per position"},
                {"pattern": "The other half hints at sound", "note": "In many kanji the non-radical part gives a sound hint. 青 is 'sei' so 静, 晴, 清 are also 'sei'.", "jp": "青・静・晴", "en": "blue, quiet, fine weather"},
                {"pattern": "On-yomi and kun-yomi", "note": "Each kanji has a Chinese-style reading (on) used in compounds and a Japanese-style reading (kun) used alone with hiragana endings.", "jp": "水 = スイ / みず", "en": "water"},
            ],
        },
    }


    reading_ch = {
        "id": "radicals-reading", "title": "How to Read Kanji", "icon": "読", "kind": "lesson",
        "vocab": parse("""
音読み|おんよみ|on'yomi|Chinese-style reading
訓読み|くんよみ|kun'yomi|Japanese-style reading
送り仮名|おくりがな|okurigana|kana ending after a kanji
熟語|じゅくご|jukugo|compound word of kanji
部首|ぶしゅ|bushu|radical
形声文字|けいせいもじ|keisei moji|phonetic-semantic kanji
意味|いみ|imi|meaning
音|おん|on|sound
読む|よむ|yomu|to read
書く|かく|kaku|to write
当てる|あてる|ateru|to guess, to match
"""),
        "sentences": [
            _s("「水」の___は「みず」です。", "「みず」の___は「みず」です。", "'Mizu' no ___ wa 'mizu' desu.", "The kun reading of 水 is 'mizu'.", "訓読み"),
            _s("「水」の___は「スイ」です。", "「みず」の___は「スイ」です。", "'Mizu' no ___ wa 'sui' desu.", "The on reading of 水 is 'sui'.", "音読み"),
            _s("「水曜日」のように漢字が二つ以上あるときは、ふつう___で読みます。", "「すいようび」のようにかんじがふたつ いじょうあるときは、ふつう___でよみます。", "Suiyōbi no yō ni kanji ga futatsu ijō aru toki wa, futsū ___ de yomimasu.", "When a word has two or more kanji, you usually read it with the on reading.", "音読み"),
            _s("漢字が一つで___があるときは、訓読みで読みます。", "かんじがひとつで___があるときは、くんよみでよみます。", "Kanji ga hitotsu de ___ ga aru toki wa, kun'yomi de yomimasu.", "When a single kanji has okurigana after it, read it with the kun reading.", "送り仮名"),
            _s("「学校」のような二つの漢字の言葉を___と言います。", "「がっこう」のようなふたつのかんじのことばを___といいます。", "'Gakkō' no yō na futatsu no kanji no kotoba o ___ to iimasu.", "Words made of two kanji like 学校 are called jukugo.", "熟語"),
            _s("漢字の___を見ると、意味がだいたい分かります。", "かんじの___をみると、いみがだいたいわかります。", "Kanji no ___ o miru to, imi ga daitai wakarimasu.", "If you look at the radical of a kanji, you can roughly tell the meaning.", "部首"),
        ],
        "guide": {
            "intro": "Every kanji can have two kinds of readings. The on-yomi (音読み) came from Chinese; the kun-yomi (訓読み) is the original Japanese word for the same idea. Two simple rules tell you which one to use most of the time.",
            "points": [
                {"pattern": "Rule 1 - alone + okurigana = kun", "note": "A kanji standing alone, especially with hiragana after it, is read with the kun-yomi.", "jp": "水 (みず)・食べる (たべる)・大きい (おおきい)", "en": "water, eat, big"},
                {"pattern": "Rule 2 - two+ kanji together = on", "note": "In a compound of two or more kanji the on-yomi is usual.", "jp": "水曜日 (すいようび)・学校 (がっこう)", "en": "Wednesday, school"},
                {"pattern": "Exceptions exist", "note": "Some compounds use kun readings (手紙 てがみ, 朝日 あさひ) and some single kanji use on readings (本 ほん, 力 ちから is kun). Learn them as whole words.", "jp": "手紙・朝日・本", "en": "letter, morning sun, book"},
                {"pattern": "Sound hints (形声)", "note": "The non-radical part of a kanji often tells you the on reading. 青 is 'sei', so 静 晴 清 精 are all 'sei'.", "jp": "青・静・晴・清・精", "en": "blue, quiet, fine weather, pure, spirit"},
                {"pattern": "More sound families", "note": "方 is 'hō': 放 訪 房 防 share it. 交 is 'kō': 校 効 郊. 古 is 'ko': 湖 固 個 枯. 同 is 'dō': 洞 胴 銅. 包 is 'hō': 泡 抱 砲.", "jp": "方・放・訪・防", "en": "direction, release, visit, defend"},
                {"pattern": "Radical + sound = most kanji", "note": "Radical tells the topic; the other part tells the sound. 海 = 氵 (water) + 毎 (mai): a water word read 'kai'. It is not perfect, but it makes guessing much easier.", "jp": "河・湖・油・流", "en": "river, lake, oil, flow - all water words"},
            ],
        },
    }

    explore = {"id": "radicals-explore", "title": "Explore All Radicals", "icon": "🔎",
               "kind": "link", "link_endpoint": "radicals_page"}
    return {"id": "radicals", "title": "Radicals",
            "blurb": "The building blocks of kanji - learn how kanji are formed and how to read them.",
            "chapters": [kanji_basics, intro] + chapters + [reading_ch, explore]}


def radical_chapter(cid, title, icon, glyph_list, rads, stories, kmean, v):
    vocab, points, ids = [], [], []
    for g in glyph_list:
        r = rads[g]
        meaning = r["meaning"]
        if r["position"] == "hen" and r["forms"]:
            meaning += " (left-side form)"
        vocab.append({"jp": g, "reading": r["name"].split("・")[0], "romaji": r["romaji"].split(" /")[0], "meaning": meaning})
        ids.append(r["id"])
        ex = next((k for k in r["kanji"] if k in stories and k in kmean), None)
        pt = {"pattern": f"{g}  {r['name']} ({r['romaji']})", "note": f"{r['meaning'].capitalize()}. {r['origin']} It {r['position_note']}."}
        if ex:
            pt["jp"] = f"{ex} = {stories[ex]['parts']}"
            pt["en"] = kmean[ex]
        points.append(pt)
    return {"id": cid, "title": title, "icon": icon, "kind": "lesson", "vocab": vocab, "sentences": [],
            "radicals": ids,
            "guide": {"intro": "Learn each radical's shape, its Japanese name and its meaning. The quiz also shows you real kanji and asks which radical is inside.",
                      "points": points}}


# ---------------------------------------------------------- new grammar chapters --
def _s(jp, reading, romaji, english, blank):
    return {"jp": jp, "reading": reading, "romaji": romaji, "english": english, "blank": blank}


NEW_GRAMMAR = [
    {
        "id": "noun-modification", "title": "Verbs & Adjectives Describe Nouns", "icon": "🧩", "kind": "lesson",
        "vocab": parse("""
昨日買った|きのうかった|kinō katta|(that I) bought yesterday
本を読んでいる|ほんをよんでいる|hon o yonde iru|(who is) reading a book
朝ご飯を食べない|あさごはんをたべない|asagohan o tabenai|(who) doesn't eat breakfast
母が作った|ははがつくった|haha ga tsukutta|(that) my mother made
大阪に住んでいる|おおさかにすんでいる|ōsaka ni sunde iru|(who) lives in Osaka
静かな|しずかな|shizuka na|quiet (before a noun)
有名な|ゆうめいな|yūmei na|famous (before a noun)
きれいな|きれいな|kirei na|pretty, clean (before a noun)
毎日使う|まいにちつかう|mainichi tsukau|(that I) use every day
去年行った|きょねんいった|kyonen itta|(where I) went last year
"""),
        "sentences": [
            _s("これは私が___本です。", "これはわたしが___ほんです。", "Kore wa watashi ga ___ hon desu.", "This is the book I bought yesterday.", "昨日買った"),
            _s("あの___人は田中さんです。", "あの___ひとはたなかさんです。", "Ano ___ hito wa Tanaka-san desu.", "The person over there reading a book is Ms. Tanaka.", "本を読んでいる"),
            _s("___人はあまりいません。", "___ひとはあまりいません。", "___ hito wa amari imasen.", "There aren't many people who don't eat breakfast.", "朝ご飯を食べない"),
            _s("___料理はとてもおいしいです。", "___りょうりはとてもおいしいです。", "___ ryōri wa totemo oishii desu.", "The dish my mother made is very delicious.", "母が作った"),
            _s("___友達がいます。", "___ともだちがいます。", "___ tomodachi ga imasu.", "I have a friend who lives in Osaka.", "大阪に住んでいる"),
            _s("ここは___町です。", "ここは___まちです。", "Koko wa ___ machi desu.", "This is a quiet town.", "静かな"),
            _s("これは私が___かばんです。", "これはわたしが___かばんです。", "Kore wa watashi ga ___ kaban desu.", "This is the bag I use every day.", "毎日使う"),
            _s("___京都はとてもきれいでした。", "___きょうとはとてもきれいでした。", "___ Kyōto wa totemo kirei deshita.", "Kyoto, where I went last year, was very beautiful.", "去年行った"),
        ],
        "guide": {
            "intro": "In Japanese a describing phrase always comes BEFORE the noun - even a long one. English uses 'that / who / which' after the noun; Japanese just puts the whole clause in front.",
            "points": [
                {"pattern": "Verb (plain form) + noun", "note": "Use the plain form of the verb (not ます) directly before the noun.", "jp": "食べる人 / 食べない人", "en": "a person who eats / doesn't eat"},
                {"pattern": "Past clause + noun", "note": "The tense of the clause is the tense of the action described.", "jp": "昨日買った本", "en": "the book I bought yesterday"},
                {"pattern": "が / の marks the subject inside the clause", "note": "Inside a describing clause the subject takes が (or の), not は.", "jp": "母が作った料理", "en": "the dish my mother made"},
                {"pattern": "い-adjective + noun", "note": "The plain adjective sits before the noun, no extra word needed.", "jp": "安い店", "en": "a cheap shop"},
                {"pattern": "な-adjective + な + noun", "note": "な-adjectives need な before the noun.", "jp": "静かな町・有名な歌手", "en": "a quiet town, a famous singer"},
            ],
        },
    },
    {
        "id": "nagara", "title": "Doing Two Things at Once (〜ながら)", "icon": "🎧", "kind": "lesson",
        "vocab": parse("""
ながら|ながら|nagara|while (doing)
歩きながら|あるきながら|aruki nagara|while walking
音楽を聞きながら|おんがくをききながら|ongaku o kiki nagara|while listening to music
ご飯を食べながら|ごはんをたべながら|gohan o tabe nagara|while eating
運転しながら|うんてんしながら|unten shi nagara|while driving
歌いながら|うたいながら|utai nagara|while singing
友達と話しながら|ともだちとはなしながら|tomodachi to hanashi nagara|while chatting with a friend
笑いながら|わらいながら|warai nagara|while laughing
"""),
        "sentences": [
            _s("___スマホを使わないでください。", "___スマホをつかわないでください。", "___ sumaho o tsukawanai de kudasai.", "Please don't use your smartphone while walking.", "歩きながら"),
            _s("私はよく___勉強します。", "わたしはよく___べんきょうします。", "Watashi wa yoku ___ benkyō shimasu.", "I often study while listening to music.", "音楽を聞きながら"),
            _s("___テレビを見ます。", "___テレビをみます。", "___ terebi o mimasu.", "I watch TV while eating.", "ご飯を食べながら"),
            _s("___電話をしてはいけません。", "___でんわをしてはいけません。", "___ denwa o shite wa ikemasen.", "You must not talk on the phone while driving.", "運転しながら"),
            _s("彼女は___踊ります。", "かのじょは___おどります。", "Kanojo wa ___ odorimasu.", "She dances while singing.", "歌いながら"),
            _s("___帰りました。", "___かえりました。", "___ kaerimashita.", "I went home chatting with a friend.", "友達と話しながら"),
            _s("彼は___話しました。", "かれは___はなしました。", "Kare wa ___ hanashimashita.", "He talked while laughing.", "笑いながら"),
        ],
        "guide": {
            "intro": "〜ながら joins two actions done at the same time by the same person. The action that comes right before ながら is the background action; the main action is at the end of the sentence.",
            "points": [
                {"pattern": "Verb ます-stem + ながら", "note": "Drop ます from the polite form and add ながら.", "jp": "歩きます → 歩きながら", "en": "while walking"},
                {"pattern": "Main action comes last", "note": "The final verb is the main action; the ながら verb is the side action.", "jp": "音楽を聞きながら勉強します。", "en": "I study while listening to music."},
                {"pattern": "Same subject only", "note": "Both actions must be done by the same person. For two different people use 間に or a て-form.", "jp": "食べながら話す", "en": "talk while eating"},
                {"pattern": "Don't do it while...", "note": "Combine with ないでください for polite requests.", "jp": "歩きながら使わないでください。", "en": "Please don't use it while walking."},
            ],
        },
    },
    {
        "id": "giving-reasons", "title": "Giving Reasons (から・ので)", "icon": "❓", "kind": "lesson",
        "vocab": parse("""
ので|ので|node|because (softer, polite)
ですから|ですから|desu kara|therefore
どうして|どうして|dōshite|why
雨が降っているので|あめがふっているので|ame ga futte iru node|because it is raining
忙しいので|いそがしいので|isogashii node|because I'm busy
頭が痛かったので|あたまがいたかったので|atama ga itakatta node|because I had a headache
安いので|やすいので|yasui node|because it's cheap
風邪をひいたので|かぜをひいたので|kaze o hiita node|because I caught a cold
疲れたので|つかれたので|tsukareta node|because I'm tired
"""),
        "sentences": [
            _s("___、家にいます。", "___、いえにいます。", "___, ie ni imasu.", "Because it's raining, I'll stay home.", "雨が降っているので"),
            _s("___、行けません。", "___、いけません。", "___, ikemasen.", "Because I'm busy, I can't go.", "忙しいので"),
            _s("___、病院に行きました。", "___、びょういんにいきました。", "___, byōin ni ikimashita.", "Because I had a headache, I went to the hospital.", "頭が痛かったので"),
            _s("___、たくさん買いました。", "___、たくさんかいました。", "___, takusan kaimashita.", "Because it was cheap, I bought a lot.", "安いので"),
            _s("___、今日は休みます。", "___、きょうはやすみます。", "___, kyō wa yasumimasu.", "Because I caught a cold, I'll rest today.", "風邪をひいたので"),
            _s("___、早く寝ます。", "___、はやくねます。", "___, hayaku nemasu.", "Because I'm tired, I'll go to bed early.", "疲れたので"),
        ],
        "guide": {
            "intro": "Japanese gives the reason first and the result second. から is direct and can sound personal; ので is softer and more polite, so it's the better choice with a teacher or a boss.",
            "points": [
                {"pattern": "Reason + から", "note": "Plain or polite form + から. Direct and conversational.", "jp": "安いからたくさん買いました。", "en": "It was cheap, so I bought a lot."},
                {"pattern": "Reason + ので", "note": "Plain form + ので. Softer; used for explanations and excuses.", "jp": "忙しいので行けません。", "en": "I'm busy, so I can't go."},
                {"pattern": "な-adjective / noun + なので", "note": "Before ので, だ turns into な.", "jp": "雨なので / 静かなので", "en": "because it's rain / quiet"},
                {"pattern": "ですから", "note": "Starts a new sentence and means 'therefore'.", "jp": "ですから、行きません。", "en": "Therefore, I won't go."},
                {"pattern": "どうして...か", "note": "Ask for a reason. Answer with から.", "jp": "どうして遅れましたか。", "en": "Why were you late?"},
            ],
        },
    },
    {
        "id": "plans-intentions", "title": "Plans & Decisions (つもり・ことにする)", "icon": "🗓️", "kind": "lesson",
        "vocab": parse("""
行くつもりです|いくつもりです|iku tsumori desu|I intend to go
会う予定です|あうよていです|au yotei desu|I'm scheduled to meet
買うことにしました|かうことにしました|kau koto ni shimashita|I decided to buy
始めようと思っています|はじめようとおもっています|hajimeyō to omotte imasu|I'm thinking of starting
やめることにしました|やめることにしました|yameru koto ni shimashita|I decided to quit
留学するつもりです|りゅうがくするつもりです|ryūgaku suru tsumori desu|I plan to study abroad
予定|よてい|yotei|plan, schedule
計画|けいかく|keikaku|plan, project
決める|きめる|kimeru|to decide
"""),
        "sentences": [
            _s("夏休みに京都へ___。", "なつやすみにきょうとへ___。", "Natsuyasumi ni Kyōto e ___.", "I plan to go to Kyoto during summer vacation.", "行くつもりです"),
            _s("明日、友達に___。", "あした、ともだちに___。", "Ashita, tomodachi ni ___.", "Tomorrow I'm scheduled to meet a friend.", "会う予定です"),
            _s("新しいパソコンを___。", "あたらしいパソコンを___。", "Atarashii pasokon o ___.", "I decided to buy a new computer.", "買うことにしました"),
            _s("来月からジムに通うことを___。", "らいげつからジムにかようことを___。", "Raigetsu kara jimu ni kayou koto o ___.", "I've decided to go to the gym from next month.", "決める"),
            _s("体に悪いので、たばこを___。", "からだにわるいので、たばこを___。", "Karada ni warui node, tabako o ___.", "Because it's bad for my health, I decided to quit smoking.", "やめることにしました"),
            _s("来年、日本に___。", "らいねん、にほんに___。", "Rainen, Nihon ni ___.", "Next year I plan to study abroad in Japan.", "留学するつもりです"),
        ],
        "guide": {
            "intro": "Three patterns cover most talk about the future: what you intend (つもり), what is arranged (予定) and what you have decided (ことにする).",
            "points": [
                {"pattern": "Dictionary form + つもりです", "note": "Your own intention. The negative is ないつもりです.", "jp": "留学するつもりです。", "en": "I intend to study abroad."},
                {"pattern": "Noun / verb + 予定です", "note": "Something already arranged or scheduled.", "jp": "会う予定です。", "en": "I'm scheduled to meet."},
                {"pattern": "Dictionary form + ことにしました", "note": "A decision YOU made. ことになりました means it was decided for you.", "jp": "やめることにしました。", "en": "I decided to quit."},
                {"pattern": "Volitional + と思っています", "note": "Softer: 'I'm thinking of doing...'. Volitional of ru-verbs: drop る + よう.", "jp": "始めようと思っています。", "en": "I'm thinking of starting."},
            ],
        },
    },
    {
        "id": "te-extras", "title": "Try, Prepare & Finish (てみる・ておく・てしまう)", "icon": "🔧", "kind": "lesson",
        "vocab": parse("""
食べてみます|たべてみます|tabete mimasu|I'll try eating
着てみます|きてみます|kite mimasu|I'll try wearing
予約しておきます|よやくしておきます|yoyaku shite okimasu|I'll book in advance
調べておきます|しらべておきます|shirabete okimasu|I'll look it up beforehand
忘れてしまいました|わすれてしまいました|wasurete shimaimashita|I forgot (oh no)
壊してしまいました|こわしてしまいました|kowashite shimaimashita|I broke it (oh no)
てみる|てみる|te miru|try doing
ておく|ておく|te oku|do in advance
てしまう|てしまう|te shimau|finish; do regrettably
"""),
        "sentences": [
            _s("この料理を___。", "このりょうりを___。", "Kono ryōri o ___.", "I'll try this dish.", "食べてみます"),
            _s("この服を___。", "このふくを___。", "Kono fuku o ___.", "I'll try this outfit on.", "着てみます"),
            _s("旅行の前に、ホテルを___。", "りょこうのまえに、ホテルを___。", "Ryokō no mae ni, hoteru o ___.", "Before the trip, I'll book the hotel in advance.", "予約しておきます"),
            _s("会議の前に、資料を___。", "かいぎのまえに、しりょうを___。", "Kaigi no mae ni, shiryō o ___.", "Before the meeting, I'll check the materials beforehand.", "調べておきます"),
            _s("すみません、宿題を___。", "すみません、しゅくだいを___。", "Sumimasen, shukudai o ___.", "I'm sorry, I forgot my homework.", "忘れてしまいました"),
            _s("ごめんなさい、カメラを___。", "ごめんなさい、カメラを___。", "Gomennasai, kamera o ___.", "I'm sorry, I broke the camera.", "壊してしまいました"),
        ],
        "guide": {
            "intro": "Add a helper verb to the て-form to say how an action is done: as a trial, as preparation, or completely (often with regret).",
            "points": [
                {"pattern": "て-form + みる", "note": "Try doing something to see what it's like.", "jp": "食べてみます。", "en": "I'll try eating it."},
                {"pattern": "て-form + おく", "note": "Do something in advance, for later.", "jp": "予約しておきます。", "en": "I'll book in advance."},
                {"pattern": "て-form + しまう", "note": "Finish something completely, or do it by mistake.", "jp": "忘れてしまいました。", "en": "I forgot it (oh no)."},
                {"pattern": "Casual: ちゃった", "note": "In conversation てしまった often becomes ちゃった.", "jp": "忘れちゃった。", "en": "Oops, I forgot."},
            ],
        },
    },
]

GRAND_REVIEW_SECTION = {
    "id": "grand-review", "title": "Grand Review",
    "blurb": "Everything you learned in one mixed practice - 50 questions.",
    "chapters": [
        {"id": "grand-review", "title": "Grand Review — 50 Questions", "icon": "🏆", "kind": "review", "count": 50, "scope": "all"}
    ],
}


# ------------------------------------------------------------------ kana --
import unicodedata

_ROW_NAMES = {"vowel": "vowel (A)", "k": "K", "s": "S", "t": "T", "n": "N", "h": "H", "m": "M", "y": "Y",
              "r": "R", "w": "W", "n-special": "N", "g": "G", "z": "Z", "d": "D", "b": "B", "p": "P"}
_BASE_OF_GROUP = {"g": "k", "z": "s", "d": "t", "b": "h", "p": "h"}


def build_kana_chapters():
    """Four practice chapters per script (hiragana, katakana) for First Steps.
    Each has a guidebook of the rows it covers and a quiz that asks both
    'which sound?' and 'which kana?' with instant right/wrong + explanation."""
    out = {"hiragana": [], "katakana": []}
    for script, label in (("hiragana", "Hiragana"), ("katakana", "Katakana")):
        data = json.loads((ROOT / "data" / f"{script}.json").read_text(encoding="utf-8"))
        parts = [
            ("1", "Vowels + K S T N", "あ" if script == "hiragana" else "ア",
             lambda e: e["type"] == "basic" and e["group"] in ("vowel", "k", "s", "t", "n")),
            ("2", "H M Y R W + N", "は" if script == "hiragana" else "ハ",
             lambda e: e["type"] == "basic" and e["group"] in ("h", "m", "y", "r", "w", "n-special")),
            ("3", "Voiced Sounds (゛ ゜)", "が" if script == "hiragana" else "ガ", lambda e: e["type"] == "dakuten"),
            ("4", "Combination Sounds", "きゃ" if script == "hiragana" else "キャ", lambda e: e["type"] == "yoon"),
        ]
        for num, name, icon, pred in parts:
            items = [e for e in data if pred(e)]
            basic_by_group = {}
            for e in data:
                if e["type"] == "basic":
                    basic_by_group.setdefault(e["group"], []).append(e)
            rows = {}
            for e in items:
                rows.setdefault(e["group"], []).append(e)
            vocab = [{"jp": e["char"], "reading": "", "romaji": e["romaji"],
                      "meaning": f"sounds like \u201c{e['romaji']}\u201d"} for e in items]
            points = []
            for g, es in rows.items():
                rowname = _ROW_NAMES.get(g, g)
                points.append({"pattern": f"{rowname} row" if g in _ROW_NAMES else f"{g}- sounds",
                               "note": " ".join(x["char"] for x in es),
                               "jp": " ".join(x["char"] for x in es),
                               "en": " ".join(x["romaji"] for x in es)})
            tips = {
                "1": "Take it a row at a time: say each sound out loud while you look at the shape. Hiragana are soft and curvy; katakana are sharp and angular.",
                "2": "The Y row has only three letters (ya yu yo) and the W row only two (wa wo). ん is the lone consonant: 'n'.",
                "3": "Two small marks (゛ dakuten) make a sound 'voiced': k→g, s→z, t→d, h→b. A small circle (゜ handakuten) turns h into p.",
                "4": "A small や ゆ よ (ゃ ゅ ょ) after an i-sound blends into ONE syllable: き + ゃ = きゃ (kya), not ki-ya.",
            }
            if script == "katakana":
                tips[num] += " Katakana is used for foreign words (コーヒー), names and emphasis."
            out[script].append({
                "id": f"{script}-{num}", "title": f"{label} {num}: {name}", "icon": icon, "kind": "lesson",
                "kana": script, "vocab": vocab, "sentences": [],
                "guide": {"intro": tips[num] + f" (Open the {label} chart above any time to practise writing.)",
                          "points": points},
            })
    return out


def kana_explain(script, entry, data):
    """Explanation shown after a kana quiz answer."""
    c, r, t, g = entry["char"], entry["romaji"], entry["type"], entry["group"]
    name = "hiragana" if script == "hiragana" else "katakana"
    if t == "basic":
        row = [x for x in data if x["type"] == "basic" and x["group"] == g]
        rowtxt = " ".join(x["char"] for x in row) + " (" + " ".join(x["romaji"] for x in row) + ")"
        return f"{c} is {name} for \u201c{r}\u201d. It sits in the {_ROW_NAMES.get(g, g)} row: {rowtxt}."
    if t == "dakuten":
        base = unicodedata.normalize("NFD", c)[0]
        b = next((x for x in data if x["char"] == base), None)
        mark = "a small circle (handakuten \u309c)" if g == "p" else "two small marks (dakuten \u309b)"
        if b:
            return f"{c} is {b['char']} ({b['romaji']}) plus {mark}, which changes the sound to \u201c{r}\u201d."
        return f"{c} is {name} for \u201c{r}\u201d (a voiced sound)."
    first, small = c[0], c[1:]
    b = next((x for x in data if x["char"] == first), None)
    if b:
        return f"{c} = {first} ({b['romaji']}) + small {small}: the two blend into one syllable, \u201c{r}\u201d."
    return f"{c} is {name} for \u201c{r}\u201d."
