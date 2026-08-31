#!/usr/bin/env bash
# Ep. 3 — free unlimited AI voice with edge-tts

uv tool install edge-tts

edge-tts --list-voices | grep en-US | head

edge-tts --text "This voice cost exactly zero dollars." \
  --voice en-US-AndrewNeural --write-media sample.mp3

# pacing = emotion: fast for hooks, slow for reveals
edge-tts --text "Same voice, ten percent faster." \
  --voice en-US-AndrewNeural --rate=+10% --write-media fast.mp3
edge-tts --text "Same voice, slower, for the reveal." \
  --voice en-US-AndrewNeural --rate=-10% --write-media slow.mp3
