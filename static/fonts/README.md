# Bundled fonts (optional)

The app asks Google Fonts for Zen Old Mincho, Noto Serif JP and Source
Serif 4. That works fine in a browser. **It never works inside the APK**,
because the packaged app has no network access at all — the Flask server
it talks to is running in the same process on `127.0.0.1`.

So on a phone the app currently falls back to whatever serif the system
provides (on Android, usually Noto Sans CJK for the Japanese glyphs).
Everything stays readable; it just isn't the Mincho look.

## Making it self-contained

Drop two `woff2` files in this directory:

| File                  | Used for                                   |
| --------------------- | ------------------------------------------ |
| `kotoba-mincho.woff2` | Japanese glyphs — headings, kana, kanji    |
| `kotoba-serif.woff2`  | Latin body text                            |

`static/css/style.css` already declares `@font-face` rules for these
under their own family names (`Kotoba Mincho`, `Kotoba Serif`), listed
first in `--serif-jp` and `--serif-body`. Nothing else needs changing:

- files present → they're used, offline, with no network request
- files absent → the browser skips them and falls through to the next
  family in the stack

Then run `python sync_android.py` so the APK copy picks them up.

## Picking the files

Both Zen Old Mincho and Noto Serif JP are open-licensed (SIL OFL), so
they can be redistributed inside the app as long as the licence text
ships with it.

Watch the file size. A full Japanese font covering every CJK glyph runs
to several megabytes, which is a lot to add to an APK. Subsetting it to
the characters the app actually uses is worth doing — the kana charts,
`data/kanji_data.json`, and the vocabulary and story files between them
define the whole set. Something like:

```bash
pip install fonttools brotli
pyftsubset ZenOldMincho-Medium.ttf \
  --text-file=used-characters.txt \
  --flavor=woff2 \
  --output-file=kotoba-mincho.woff2
```

One caveat specific to Writing Practice: the tracing pad draws its guide
character and its scoring mask with the *same* font, so it stays accurate
whichever font ends up resolving. But a subset that's missing a character
would render a blank guide square for it — so build the subset from the
app's own data files rather than a hand-written list.
