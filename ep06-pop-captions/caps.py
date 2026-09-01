import sys
from faster_whisper import WhisperModel

def ts(t):
    h, m = int(t // 3600), int(t % 3600 // 60)
    return f"{h:02}:{m:02}:{t % 60:06.3f}".replace(".", ",")

model = WhisperModel("small", device="cpu", compute_type="int8")
segments, _ = model.transcribe(sys.argv[1], word_timestamps=True)
words = [w for seg in segments for w in seg.words]

with open("captions.srt", "w") as f:
    for i, w in enumerate(words, 1):
        f.write(f"{i}\n{ts(w.start)} --> {ts(w.end)}\n{w.word.strip().upper()}\n\n")
print(f"captions.srt written — {len(words)} word-timed captions")
