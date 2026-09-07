# Ep 12 — Measure search demand before you build

`uv run titlescan.py phrases.txt` — for each phrase: search 50 results, divide each video's views by its channel's subscribers, keep channels with 100–200,000 subs, read the 90th percentile.
Bands: >=100x build · 30–100x judgement · <30x skip. Cost: 100 API units per phrase (10,000/day).
`python3 dupecheck.py "Title"` — word-overlap check against your own channel so you never build a topic twice.
Needs a YouTube Data API OAuth client (`client_secret.json`) next to the scripts.
