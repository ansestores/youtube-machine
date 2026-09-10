# /// script
# requires-python = ">=3.10"
# dependencies = ["google-api-python-client", "google-auth-oauthlib"]
# ///
"""Ep.14 — how long does a Short actually keep earning views?

Everyone guesses. Your own Analytics knows. This pulls each Short's views for
the day it published and the three days after, so you can see the decay curve
for YOUR channel instead of repeating someone else's rule of thumb.

    uv run lifespan.py            # last 30 days
    uv run lifespan.py --days 60

Why it matters: if a Short is finished after 48 hours, then judging it on day 5
is pointless, and so is re-checking it. You learn the result, change the next
video, and move on.
"""
import argparse, datetime as dt, statistics
from googleapiclient.discovery import build
from auth import get_credentials


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=30)
    a = ap.parse_args()

    creds = get_credentials()
    yt = build("youtube", "v3", credentials=creds)
    ya = build("youtubeAnalytics", "v2", credentials=creds)

    # Analytics lags ~3 days; a Short needs 4 days of history to show its curve.
    newest = dt.date.today() - dt.timedelta(days=4)
    oldest = newest - dt.timedelta(days=a.days)

    rows = ya.reports().query(
        ids="channel==MINE", startDate=str(oldest), endDate=str(newest),
        dimensions="video", metrics="views",
        filters="creatorContentType==shorts", sort="-views",
        maxResults=200).execute().get("rows", [])
    ids = [r[0] for r in rows]

    pub = {}
    for i in range(0, len(ids), 50):
        for it in yt.videos().list(part="snippet", id=",".join(ids[i:i + 50])).execute()["items"]:
            pub[it["id"]] = it["snippet"]["publishedAt"][:10]

    print(f"{'day0':>7}{'day1':>7}{'day2':>7}{'day3':>7}   {'d0 share':>9}  title")
    shares = []
    for vid, total in rows[:15]:
        p = pub.get(vid)
        if not p:
            continue
        p = dt.date.fromisoformat(p)
        if p + dt.timedelta(days=3) > newest:
            continue        # its 4-day window runs past what Analytics has published
        try:
            r = ya.reports().query(
                ids="channel==MINE", startDate=str(p), endDate=str(p + dt.timedelta(days=3)),
                dimensions="day", metrics="views", filters=f"video=={vid}").execute()
        except Exception:
            continue        # Analytics returns a 500 for windows it cannot fill yet
        byday = {d: v for d, v in r.get("rows", [])}
        got = [byday.get(str(p + dt.timedelta(days=k)), 0) for k in range(4)]
        s = sum(got)
        if s < 20:
            continue
        shares.append(got[0] / s)
        name = next((i["snippet"]["title"] for i in
                     yt.videos().list(part="snippet", id=vid).execute()["items"]), vid)
        print(f"{got[0]:7d}{got[1]:7d}{got[2]:7d}{got[3]:7d}   {got[0]/s:8.0%}  {name[:38]}")

    if shares:
        print(f"\nmedian share of views arriving on publish day: {statistics.median(shares):.0%}")
        print("BUT check the day0 column: some Shorts take ~0 views on publish day")
        print("and explode on day 1. Never judge a Short before 48 hours.")


if __name__ == "__main__":
    main()
