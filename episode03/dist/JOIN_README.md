# EP03 FINAL MASTER — join instructions

The 1080p animated master (`EP03_FINAL_FILM_1080p.mp4`, 361,259,141 bytes, 11:13.98)
is stored here in 4 parts because GitHub caps files at 100 MB.

## Join — Linux / macOS / Android (Termux)
```bash
cat EP03_FINAL_FILM_1080p.mp4.partaa EP03_FINAL_FILM_1080p.mp4.partab \
    EP03_FINAL_FILM_1080p.mp4.partac EP03_FINAL_FILM_1080p.mp4.partad \
    > EP03_FINAL_FILM_1080p.mp4
```

## Join — Windows (Command Prompt)
```cmd
copy /b EP03_FINAL_FILM_1080p.mp4.partaa + EP03_FINAL_FILM_1080p.mp4.partab + EP03_FINAL_FILM_1080p.mp4.partac + EP03_FINAL_FILM_1080p.mp4.partad EP03_FINAL_FILM_1080p.mp4
```

## Verify (optional)
`sha256sum EP03_FINAL_FILM_1080p.mp4` must equal the hash in `EP03_FINAL_1080p.sha256`:
```
f3a867d1e370c4f839896fb80f03bbafe3d673a86463c46a5ed8f37d807cc6f8
```

## Direct download links (raw.githubusercontent)
- https://raw.githubusercontent.com/kl2400032185/youtube1/arena/01a109dc-youtube1/episode03/dist/EP03_FINAL_FILM_1080p.mp4.partaa
- https://raw.githubusercontent.com/kl2400032185/youtube1/arena/01a109dc-youtube1/episode03/dist/EP03_FINAL_FILM_1080p.mp4.partab
- https://raw.githubusercontent.com/kl2400032185/youtube1/arena/01a109dc-youtube1/episode03/dist/EP03_FINAL_FILM_1080p.mp4.partac
- https://raw.githubusercontent.com/kl2400032185/youtube1/arena/01a109dc-youtube1/episode03/dist/EP03_FINAL_FILM_1080p.mp4.partad

Prefer a single file? Use the committed 720p animated preview instead:
https://raw.githubusercontent.com/kl2400032185/youtube1/arena/01a109dc-youtube1/episode03/EP03_PREVIEW_LIVE_720p.mp4
