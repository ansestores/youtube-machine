# Ep 13 — Engaged views: the free metric that beats views

A **view** is counted when a Short is shown and starts playing.
An **engaged view** is counted only when the person did not immediately swipe away.

```
engaged rate = engagedViews / views
```

It is one extra metric name on the Analytics call from [Ep 10](../ep10-analytics/), so it costs no extra quota.

## Run it

```
uv run engaged.py                 # channel median, writes engaged.csv
uv run engaged.py --split 600     # do 600+ view Shorts engage better?
```

First run opens a browser once for OAuth. This episode adds the **analytics** scope — if you already have a `token.json` from an earlier episode, delete it once so the browser re-consents.

## What it found on this channel (90 days)

| | |
|---|---|
| channel median engaged rate | 44% |
| Shorts above 600 views | 47% |
| Shorts below 600 views | 41% |
| completion, above vs below | 60% vs 54% |

Engagement separates the winners. **Completion barely does** — which is why "make them watch to the end" turned out to be the wrong thing to optimise.

The most-viewed Short on the channel is not the best-engaged one. Views tell you the feed picked a video; engaged views tell you the viewer agreed with it.

## ⚠ Shorts only

Do **not** apply this to long videos. There the most-viewed long often has the worst engagement and the best watch time, because browse traffic is low-intent. Judge longs by **minutes watched**.
