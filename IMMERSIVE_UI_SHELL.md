# Kotoba Immersive UI Shell

This is a presentation-only wrapper inspired by the supplied mobile UI reference.

## What it changes
- Adds an immersive dark/glass visual layer.
- Adds a floating glass header.
- Adds a mobile bottom navigation bar.
- Restyles existing cards, hero areas, controls, and typography.
- Keeps the existing Flask routes, APIs, templates' content, data files, and page JavaScript intact.

## What it does NOT change
- `app.py` logic/routes
- JSON datasets
- authentication/session logic
- practice/quiz algorithms
- flashcard logic
- page-specific JavaScript
- Android/Chaquopy architecture

## Integration
Only `templates/base.html` is integrated with two new assets:
- `static/css/ui-shell.css`
- `static/js/ui-shell.js`

The original `base.html` is preserved as `templates/base.html.original` in this development copy.

After editing the root web assets, run:

```bash
python sync_android.py
```

That remains the single source of truth for the Android package.
