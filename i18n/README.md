# Website translations

English pages in `docs/` are the source. Each language lives in `i18n/<code>.json`, a list of
translated strings in the same order as `i18n/en.json`.

After editing any English page or translation, rebuild:

    python3 i18n/build.py

This regenerates `i18n/en.json`, every `docs/<code>/` folder and `docs/sitemap.xml`.
New or changed English text is appended to the end of `en.json`; append its translation to
the end of every language file (the build stops and tells you if a file is out of step).

Language choice: first visit to an English page redirects to the visitor's phone/browser
language when we have it; the footer switcher overrides and remembers the choice.

## Pages in some languages only
`LIMITED` in `build.py` lists pages offered in a subset of languages (currently the Asia
landing pages `/free-dating-app/` and `/safe-dating/` in en, zh, ja, vi, th). Their hreflang,
sitemap entries, footer links and language switcher only include those languages; switching
to another language goes to that language's homepage. To add a language to them, translate
the page's strings and add the code to `ASIA` (or the page's list).

## Traditional Chinese
`zh-hant.json` is generated from `zh.json` by `zh_hant.py` (Taiwan wording, then character
conversion) every time the build runs. Edit Simplified Chinese, not `zh-hant.json`. To change a
Traditional-only word, add it to the phrase list `PH` in `zh_hant.py`.
