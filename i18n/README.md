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
