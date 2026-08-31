# Ep. 4 — Free Stock Footage: 3 APIs

Pexels + Pixabay (free keys) and NASA's public-domain vault (no key). The API matches WORDS, not meaning — read every slug, and verify with a contact sheet.

▶ **Watch:** [Free Stock Footage for YouTube Videos — 3 APIs](https://youtu.be/PVfTayA7jpE)

```bash
# search (free key from pexels.com/api)
curl "https://api.pexels.com/videos/search?query=eagle&per_page=3" \
  -H "Authorization: YOUR_KEY" -H "User-Agent: Mozilla/5.0"

# NASA — no key at all
curl "https://images-api.nasa.gov/search?q=apollo 11 launch&media_type=video"

# verify everything: one frame per clip, tiled into a contact sheet
ffmpeg -ss 3 -i clip.mp4 -frames:v 1 thumb.png
```
