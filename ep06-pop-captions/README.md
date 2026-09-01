# Ep. 6 — Pop-Word Captions, Timed by Whisper

Whisper's word timestamps become captions automatically: one caption per WORD, each on screen for exactly as long as it is spoken. The simplest output is an SRT (works everywhere, uploadable to YouTube); our channel renders the same timestamps as styled, popping text.

▶ **Watch:** [Auto Captions — Word-Perfect, Free](https://youtu.be/Chu2dlfhOH8)

```bash
uv init --bare && uv add faster-whisper
uv run python caps.py narration.mp3   # -> captions.srt, one entry per word
```
