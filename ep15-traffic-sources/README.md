# Ep 15 — Where do your views actually come from?

Every view has a **traffic source**. One Analytics API report, grouped by `insightTrafficSourceType`, tells you which.

```
uv run sources.py            # Shorts
uv run sources.py --longs    # long videos
```

## Real output from this channel (3 weeks)

```
Shorts: 31,388 views
Shorts feed               26,994   86.0%
YouTube search             2,404    7.7%
your channel page            934    3.0%
subscribers' home feed       102    0.3%

longs: 1,560 views
subscribers' home feed     1,069   68.5%
your channel page            196   12.6%
YouTube search               127    8.1%
suggested videos              63    4.0%
```

**Shorts live in the feed**, in front of strangers — your subscriber count does almost nothing for them.
**Long videos flip completely:** two thirds from subscribers, and only 4% suggested by YouTube. On a small
channel the recommendation engine is barely showing your long videos to anyone new yet.

Uses the Analytics scope — if you have a `token.json` from before Ep 13, delete it once so the browser re-consents.
