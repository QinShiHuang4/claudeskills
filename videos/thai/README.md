# Meet Bundle promo videos (Thai)

Thai versions of the Bundle promo videos, rebranded **Meet Bundle**. The originals had no
project source, so these are rebuilt as an HTML animation (`scene.html`) and rendered frame by
frame with Playwright and ffmpeg. They match the originals' size, length and frame rate (30 fps, no audio).

| File | Size | Length |
|---|---|---|
| `out/meet-bundle-3d-free-dating-16x9-th.mp4` | 1920×1080 | 15.5 s |
| `out/meet-bundle-3d-free-dating-9x16-th.mp4` | 1080×1920 | 15.5 s |
| `out/meet-bundle-intro-16x9-th.mp4` | 1920×1080 | 9.6 s |
| `out/meet-bundle-intro-9x16-th.mp4` | 1080×1920 | 9.6 s |

Re-render (needs Node, Playwright's Chromium and ffmpeg):

    node render.js fd 169 out/meet-bundle-3d-free-dating-16x9-th.mp4
    node render.js fd 916 out/meet-bundle-3d-free-dating-9x16-th.mp4
    node render.js intro 169 out/meet-bundle-intro-16x9-th.mp4
    node render.js intro 916 out/meet-bundle-intro-9x16-th.mp4

Preview single frames: `node render.js fd 169 --stills 3,7.5,11` (written to `stills/`, git-ignored).

All copy lives in `scene.html`. Wording follows the Thai website (`i18n/th.json`): Wink, Like,
Spark and Pass stay in English as feature names, and everything else is Thai. Photos come from
`docs/img`. The cartoon profile pictures are drawn in SVG in `scene.html`. Fonts (Noto Sans Thai,
Roboto, Outfit; SIL OFL) are bundled in `fonts/` so renders don't depend on the network.
