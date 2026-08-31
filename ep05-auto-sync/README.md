# Ep. 5 — Cut Clips to the Exact Second of Narration

The heart of the machine: faster-whisper gives every WORD of the narration an exact timestamp. Walk the word list by each scene's word count and you know precisely when each visual must cut — no manual editing, no drift.

▶ **Watch:** [How My Videos Edit Themselves — Whisper Auto-Sync](https://youtu.be/EiRFwKAa6po)

```bash
uv init --bare && uv add faster-whisper
uv run python sync.py narration.mp3
# then cut each scene: ffmpeg -ss <start> -t <len> -i clip.mp4 scene1.mp4
```
