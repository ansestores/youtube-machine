# Ep.10 — Find out which videos actually worked

```bash
python analytics.py --days 28
```

## The API nobody mentions

`youtube` and `youtubeAnalytics` are **two different services** sharing one set of
credentials. Everyone finds the Data API; the Analytics one is where the numbers live.

```python
build("youtube",          "v3", credentials=creds)   # upload, metadata
build("youtubeAnalytics", "v2", credentials=creds)   # views, retention, traffic
```

## The one table worth reading

`insightTrafficSourceType` tells you WHERE views came from, and it changes what you
should do next:

| source | meaning |
|---|---|
| `SHORTS` | the Shorts feed found you — the only surface that reaches strangers cheaply |
| `YT_SEARCH` | people typed something; your titles are doing work |
| `RELATED_VIDEO` | suggested next to other videos — needs watch history to exist at all |
| `YT_CHANNEL` | they were already on your channel page |

A channel with high `YT_CHANNEL` and near-zero `RELATED_VIDEO` is not being
distributed — no amount of better titles fixes that.

## Two traps

**Analytics lags 2-3 days.** Query today and today is missing. If you need same-hour
numbers, poll `videos.list(part="statistics")` per video instead — that counter is
close to live.

**`insightTrafficSourceDetail` needs a filter.** Ask for it without
`filters="insightTrafficSourceType==YT_SEARCH"` and you get an error, not the
search terms.
