import json

# Common everyday Japanese words/phrases that a kanji-focused textbook
# doesn't cover well (greetings, basic expressions - mostly kana-only).
# These fill out the "Everyday Life" word list alongside the kanji
# vocabulary already extracted from the book.

everyday_extra = [
 dict(word="こんにちは", reading="こんにちは", romaji="konnichiwa", meaning="hello / good afternoon", category="Greetings & Phrases", difficulty="easy"),
 dict(word="おはようございます", reading="おはようございます", romaji="ohayō gozaimasu", meaning="good morning (polite)", category="Greetings & Phrases", difficulty="easy"),
 dict(word="こんばんは", reading="こんばんは", romaji="konbanwa", meaning="good evening", category="Greetings & Phrases", difficulty="easy"),
 dict(word="さようなら", reading="さようなら", romaji="sayōnara", meaning="goodbye", category="Greetings & Phrases", difficulty="easy"),
 dict(word="おやすみなさい", reading="おやすみなさい", romaji="oyasuminasai", meaning="good night", category="Greetings & Phrases", difficulty="easy"),
 dict(word="ありがとうございます", reading="ありがとうございます", romaji="arigatō gozaimasu", meaning="thank you (polite)", category="Greetings & Phrases", difficulty="easy"),
 dict(word="どういたしまして", reading="どういたしまして", romaji="dō itashimashite", meaning="you're welcome", category="Greetings & Phrases", difficulty="medium"),
 dict(word="すみません", reading="すみません", romaji="sumimasen", meaning="excuse me / sorry", category="Greetings & Phrases", difficulty="easy"),
 dict(word="ごめんなさい", reading="ごめんなさい", romaji="gomen nasai", meaning="I'm sorry", category="Greetings & Phrases", difficulty="easy"),
 dict(word="はじめまして", reading="はじめまして", romaji="hajimemashite", meaning="nice to meet you", category="Greetings & Phrases", difficulty="easy"),
 dict(word="よろしくお願いします", reading="よろしくおねがいします", romaji="yoroshiku onegaishimasu", meaning="please treat me well / thanks in advance", category="Greetings & Phrases", difficulty="medium"),
 dict(word="お願いします", reading="おねがいします", romaji="onegaishimasu", meaning="please (asking a favor)", category="Greetings & Phrases", difficulty="easy"),
 dict(word="いただきます", reading="いただきます", romaji="itadakimasu", meaning="said before eating", category="Greetings & Phrases", difficulty="easy"),
 dict(word="ごちそうさまでした", reading="ごちそうさまでした", romaji="gochisōsama deshita", meaning="said after eating, thanking for the meal", category="Greetings & Phrases", difficulty="medium"),
 dict(word="いってきます", reading="いってきます", romaji="ittekimasu", meaning="I'm heading out (said when leaving home)", category="Greetings & Phrases", difficulty="medium"),
 dict(word="いってらっしゃい", reading="いってらっしゃい", romaji="itterasshai", meaning="see you off / take care (said to someone leaving)", category="Greetings & Phrases", difficulty="medium"),
 dict(word="ただいま", reading="ただいま", romaji="tadaima", meaning="I'm home", category="Greetings & Phrases", difficulty="easy"),
 dict(word="おかえりなさい", reading="おかえりなさい", romaji="okaerinasai", meaning="welcome home", category="Greetings & Phrases", difficulty="easy"),
 dict(word="はい", reading="はい", romaji="hai", meaning="yes", category="Greetings & Phrases", difficulty="easy"),
 dict(word="いいえ", reading="いいえ", romaji="iie", meaning="no", category="Greetings & Phrases", difficulty="easy"),
 dict(word="わかりました", reading="わかりました", romaji="wakarimashita", meaning="understood / got it", category="Greetings & Phrases", difficulty="easy"),
 dict(word="わかりません", reading="わかりません", romaji="wakarimasen", meaning="I don't understand", category="Greetings & Phrases", difficulty="easy"),
 dict(word="大丈夫です", reading="だいじょうぶです", romaji="daijōbu desu", meaning="it's okay / I'm fine", category="Greetings & Phrases", difficulty="medium"),
 dict(word="頑張って", reading="がんばって", romaji="ganbatte", meaning="good luck / do your best", category="Greetings & Phrases", difficulty="medium"),
 dict(word="おめでとうございます", reading="おめでとうございます", romaji="omedetō gozaimasu", meaning="congratulations", category="Greetings & Phrases", difficulty="medium"),
 dict(word="お元気ですか", reading="おげんきですか", romaji="ogenki desu ka", meaning="how are you?", category="Greetings & Phrases", difficulty="medium"),
 dict(word="元気です", reading="げんきです", romaji="genki desu", meaning="I'm doing well", category="Greetings & Phrases", difficulty="easy"),
 dict(word="お先に失礼します", reading="おさきにしつれいします", romaji="osaki ni shitsurei shimasu", meaning="excuse me for leaving first (workplace phrase)", category="Greetings & Phrases", difficulty="hard"),
 dict(word="ちょっと待ってください", reading="ちょっとまってください", romaji="chotto matte kudasai", meaning="please wait a moment", category="Greetings & Phrases", difficulty="medium"),
 dict(word="どうぞ", reading="どうぞ", romaji="dōzo", meaning="please / go ahead (offering something)", category="Greetings & Phrases", difficulty="easy"),
 dict(word="いくらですか", reading="いくらですか", romaji="ikura desu ka", meaning="how much is it?", category="Shopping & Money", difficulty="easy"),
 dict(word="これをください", reading="これをください", romaji="kore o kudasai", meaning="I'll take this, please", category="Shopping & Money", difficulty="easy"),
 dict(word="お会計お願いします", reading="おかいけいおねがいします", romaji="okaikei onegaishimasu", meaning="check, please (at a restaurant)", category="Shopping & Money", difficulty="hard"),
 dict(word="トイレはどこですか", reading="トイレはどこですか", romaji="toire wa doko desu ka", meaning="where is the bathroom?", category="Out & About", difficulty="medium"),
 dict(word="駅はどこですか", reading="えきはどこですか", romaji="eki wa doko desu ka", meaning="where is the station?", category="Out & About", difficulty="medium"),
 dict(word="日本語が話せますか", reading="にほんごがはなせますか", romaji="nihongo ga hanasemasu ka", meaning="can you speak Japanese?", category="Out & About", difficulty="hard"),
 dict(word="英語が話せますか", reading="えいごがはなせますか", romaji="eigo ga hanasemasu ka", meaning="can you speak English?", category="Out & About", difficulty="hard"),
 dict(word="もう一度お願いします", reading="もういちどおねがいします", romaji="mō ichido onegaishimasu", meaning="one more time, please", category="Out & About", difficulty="hard"),
 dict(word="写真を撮ってもいいですか", reading="しゃしんをとってもいいですか", romaji="shashin o tottemo ii desu ka", meaning="may I take a photo?", category="Out & About", difficulty="hard"),
 dict(word="調子はどう", reading="ちょうしはどう", romaji="chōshi wa dō", meaning="how's it going? (casual)", category="Greetings & Phrases", difficulty="medium"),
]

with open("data/everyday_extra.json", "w", encoding="utf-8") as f:
    json.dump(everyday_extra, f, ensure_ascii=False, indent=1)

print(len(everyday_extra), "everyday phrase entries saved")
