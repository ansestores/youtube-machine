import sys
from faster_whisper import WhisperModel

model = WhisperModel("small", device="cpu", compute_type="int8")
segments, _ = model.transcribe(sys.argv[1], word_timestamps=True)

words = [w for seg in segments for w in seg.words]
for w in words[:8]:
    print(f"{w.start:6.2f}s → {w.end:6.2f}s   {w.word}")
print(f"... {len(words)} words total, each with exact timestamps")
