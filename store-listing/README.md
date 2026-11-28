# Meet Bundle store listings (English + Thai)

Copy lives in `listing.json`, one block per language. Every field is within the store limit
(checked when written; re-check after editing).

| Field | Where it goes | Limit |
|---|---|---|
| `app_name` | Play: App name · App Store: Name | 30 |
| `play_short_description` | Play: Short description | 80 |
| `description` | Play: Full description · App Store: Description | 4000 |
| `app_store_subtitle` | App Store: Subtitle | 30 |
| `app_store_promotional_text` | App Store: Promotional text (can change without a new build) | 170 |
| `app_store_keywords` | App Store: Keywords, comma separated, no spaces | 100 |

## Graphics

Rendered from `videos/thai/scene.html` (composition `store`) and saved in
`store-screenshots/meet-bundle/<lang>/`:

| Folder | Size | Use |
|---|---|---|
| `google-play/1-free.png` … `7-chat.png` | 1080×1920 | Play phone screenshots |
| `google-play/feature-graphic-1024x500.png` | 1024×500 | Play feature graphic |
| `app-store/1-free.png` … `7-chat.png` | 1290×2796 | App Store 6.9″ iPhone screenshots |

Re-render after a change (needs Node, Playwright's Chromium and ffmpeg):

    cd videos/thai
    node render.js store gp --lang en --shot 1 --stills 0.5   # gp = Play, as = App Store, fg = feature graphic
    # output lands in videos/thai/stills/, copy it into store-screenshots/meet-bundle/

The real-person photos the frames use (`assets/shachar-real*`, `assets/omer-*`) are kept out of git,
so a fresh checkout cannot re-render frames 2, 4 and 6 or the feature graphic until they are added.

## Upload checklist

1. **Play Console → Store presence → Main store listing:** English (default) and add Thai (th-TH)
   under *Manage translations*. Paste the fields, upload the 7 screenshots and the feature graphic per language.
2. **App Store Connect → App Information:** Name and Subtitle per localization (English, Thai).
   **Version page:** Description, Keywords, Promotional text and the 7 screenshots (6.9″ display) per localization.
3. The Thai screenshots show the app's interface in Thai. Check that the wording matches the
   app's real Thai strings before uploading, since both stores expect screenshots to show the actual app.
