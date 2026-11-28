# Meet Bundle promo videos (Thai)

Thai versions of the Bundle promo videos, rebranded **Meet Bundle**. The originals had no
project source, so these are rebuilt as an HTML animation (`scene.html`) and rendered frame by
frame with Playwright and ffmpeg. They match the originals' size, length and frame rate (30 fps, no audio).

| File | Size | Length |
|---|---|---|
| `out/meet-bundle-3d-free-dating-16x9-th.mp4` | 1920×1080 | 15.5 s (feed: Nami, Lina, Maya) |
| `out/meet-bundle-3d-free-dating-16x9-th_1.mp4` | 1920×1080 | 15.5 s (feed: Lina, Nami, Maya) |
| `out/meet-bundle-3d-free-dating-9x16-th.mp4` | 1080×1920 | 15.5 s |
| `out/meet-bundle-intro-16x9-th.mp4` | 1920×1080 | 9.6 s |
| `out/meet-bundle-intro-9x16-th.mp4` | 1080×1920 | 9.6 s |
| `out/meet-bundle-spark-16x9-th.mp4` / `-en.mp4` | 1920×1080 | 15 s |
| `out/meet-bundle-spark-9x16-th.mp4` / `-en.mp4` | 1080×1920 | 15 s |

The Spark video ("Sometimes, you just need a spark in your life. Stand out for free.") is in Thai and English.

Re-render (needs Node, Playwright's Chromium and ffmpeg):

    node render.js fd 169 out/meet-bundle-3d-free-dating-16x9-th.mp4
    node render.js fd 169 out/meet-bundle-3d-free-dating-16x9-th_1.mp4 --v a
    node render.js fd 916 out/meet-bundle-3d-free-dating-9x16-th.mp4
    node render.js intro 169 out/meet-bundle-intro-16x9-th.mp4
    node render.js intro 916 out/meet-bundle-intro-9x16-th.mp4
    node render.js spark 169 out/meet-bundle-spark-16x9-th.mp4
    node render.js spark 916 out/meet-bundle-spark-9x16-th.mp4
    node render.js spark 169 out/meet-bundle-spark-16x9-en.mp4 --lang en
    node render.js spark 916 out/meet-bundle-spark-9x16-en.mp4 --lang en

Preview single frames: `node render.js fd 169 --stills 3,7.5,11` (written to `stills/`, git-ignored).

All copy lives in `scene.html`. Wording follows the Thai website (`i18n/th.json`): Wink, Like,
Spark and Pass stay in English as feature names, and everything else is Thai. Every profile
picture is a real photo from the avatar pool in `assets/` (Maya, Shachar, Lina, Nami), rotated
across the feed, Likes, Matches, chat and match screens (`PEOPLE` in `scene.html`). Fonts (Noto Sans Thai,
Roboto, Outfit; SIL OFL) are bundled in `fonts/` so renders don't depend on the network.
