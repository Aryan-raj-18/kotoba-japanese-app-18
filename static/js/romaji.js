// Romaji -> kana conversion. Produces hiragana; katakana is derived by
// shifting each hiragana codepoint by the standard +0x60 block offset
// (the same trick used server-side in gen_kana.py), so one table
// covers both scripts.

const KANA_MAP = {
  // vowels
  a: 'あ', i: 'い', u: 'う', e: 'え', o: 'お',
  // k
  ka: 'か', ki: 'き', ku: 'く', ke: 'け', ko: 'こ',
  kya: 'きゃ', kyu: 'きゅ', kyo: 'きょ',
  // g
  ga: 'が', gi: 'ぎ', gu: 'ぐ', ge: 'げ', go: 'ご',
  gya: 'ぎゃ', gyu: 'ぎゅ', gyo: 'ぎょ',
  // s
  sa: 'さ', si: 'し', shi: 'し', su: 'す', se: 'せ', so: 'そ',
  sha: 'しゃ', shu: 'しゅ', sho: 'しょ',
  sya: 'しゃ', syu: 'しゅ', syo: 'しょ',
  // z
  za: 'ざ', zi: 'じ', ji: 'じ', zu: 'ず', ze: 'ぜ', zo: 'ぞ',
  ja: 'じゃ', ju: 'じゅ', jo: 'じょ',
  jya: 'じゃ', jyu: 'じゅ', jyo: 'じょ',
  // t
  ta: 'た', ti: 'ち', chi: 'ち', tu: 'つ', tsu: 'つ', te: 'て', to: 'と',
  cha: 'ちゃ', chu: 'ちゅ', cho: 'ちょ',
  tya: 'ちゃ', tyu: 'ちゅ', tyo: 'ちょ',
  // d
  da: 'だ', di: 'ぢ', du: 'づ', de: 'で', do: 'ど',
  dya: 'ぢゃ', dyu: 'ぢゅ', dyo: 'ぢょ',
  // n
  na: 'な', ni: 'に', nu: 'ぬ', ne: 'ね', no: 'の',
  nya: 'にゃ', nyu: 'にゅ', nyo: 'にょ',
  // h
  ha: 'は', hi: 'ひ', hu: 'ふ', fu: 'ふ', he: 'へ', ho: 'ほ',
  hya: 'ひゃ', hyu: 'ひゅ', hyo: 'ひょ',
  fa: 'ふぁ', fi: 'ふぃ', fe: 'ふぇ', fo: 'ふぉ',
  // b
  ba: 'ば', bi: 'び', bu: 'ぶ', be: 'べ', bo: 'ぼ',
  bya: 'びゃ', byu: 'びゅ', byo: 'びょ',
  // p
  pa: 'ぱ', pi: 'ぴ', pu: 'ぷ', pe: 'ぺ', po: 'ぽ',
  pya: 'ぴゃ', pyu: 'ぴゅ', pyo: 'ぴょ',
  // m
  ma: 'ま', mi: 'み', mu: 'む', me: 'め', mo: 'も',
  mya: 'みゃ', myu: 'みゅ', myo: 'みょ',
  // y
  ya: 'や', yu: 'ゆ', yo: 'よ',
  // r
  ra: 'ら', ri: 'り', ru: 'る', re: 'れ', ro: 'ろ',
  rya: 'りゃ', ryu: 'りゅ', ryo: 'りょ',
  // w
  wa: 'わ', wo: 'を', wi: 'うぃ', we: 'うぇ',
  // v (loanwords)
  va: 'ゔぁ', vi: 'ゔぃ', vu: 'ゔ', ve: 'ゔぇ', vo: 'ゔぉ',
  '-': 'ー',
};

const SMALL_TSU_CONSONANTS = 'kstpgzjdbcf';

function hiraganaToKatakana(str) {
  let out = '';
  for (const ch of str) {
    const code = ch.codePointAt(0);
    out += (code >= 0x3041 && code <= 0x3096) ? String.fromCodePoint(code + 0x60) : ch;
  }
  return out;
}

/**
 * Convert a romaji string to hiragana. Greedy longest-match (3, then 2,
 * then 1 character), with doubled-consonant -> small tsu (っ) and a
 * trailing/standalone "n" -> ん.
 */
function romajiToHiragana(input) {
  const s = input.toLowerCase();
  let out = '';
  let i = 0;
  while (i < s.length) {
    let matched = false;
    for (const len of [3, 2, 1]) {
      const chunk = s.substr(i, len);
      if (KANA_MAP[chunk]) {
        out += KANA_MAP[chunk];
        i += len;
        matched = true;
        break;
      }
    }
    if (matched) continue;

    // doubled consonant -> small tsu, e.g. "kko" -> っこ
    if (i + 1 < s.length && s[i] === s[i + 1] && SMALL_TSU_CONSONANTS.includes(s[i])) {
      out += 'っ';
      i += 1;
      continue;
    }
    // "n" not part of a na/ni/... or nya/... cluster -> ん
    if (s[i] === 'n') {
      out += 'ん';
      i += 1;
      continue;
    }
    // unrecognised character (space, punctuation, digit) - pass through
    out += s[i];
    i += 1;
  }
  return out;
}

function romajiToKatakana(input) {
  return hiraganaToKatakana(romajiToHiragana(input));
}
