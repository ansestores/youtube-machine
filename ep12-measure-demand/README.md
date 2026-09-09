# Ep 12 — Measure search demand before you build

`uv run titlescan.py phrases.txt` — for each phrase: search 50 results, divide each video's views by its channel's subscribers, keep channels with 100–200,000 subs, read the 90th percentile.
Bands: >=100x build · 30–100x judgement · <30x skip. Cost: 100 API units per phrase (10,000/day).
`uv run dupecheck.py "Title"` — word-overlap check against your own channel so you never build a topic twice.
Needs a YouTube Data API OAuth client (`client_secret.json`) next to the scripts.

## Running it

```
uv run titlescan.py phrases.txt      # one search phrase per line
uv run dupecheck.py "A Video Title"  # is this already on your channel?
```

`uv` installs the dependencies automatically from each script's header — nothing to pip install.
On the first run a browser opens once for Google sign-in and writes `token.json` next to the scripts.
Both files (`client_secret.json`, `token.json`) are gitignored: never commit them.
