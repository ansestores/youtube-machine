# Ep. 7 — Thumbnails Designed by Code

One PIL script turns any frame from the video into a finished thumbnail: auto-wrapping bold text, a highlighted keyword, and the exact 16:9 / 9:16 sizes YouTube wants. No design tool, no manual export — the same script makes every cover on this channel.

▶ **Watch:** [Auto-Generate YouTube Thumbnails with Python](https://youtu.be/QE8cbQzQ9UI)

```bash
# grab a frame from the video itself, then draw on it
ffmpeg -ss 3 -i video.mp4 -frames:v 1 -update 1 bg.jpg
python3 thumb.py bg.jpg thumb.jpg "WHY DO CATS PURR?" 1280x720 PURR
```
