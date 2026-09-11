# /// script
# requires-python = ">=3.10"
# dependencies = ["google-api-python-client", "google-auth-oauthlib"]
# ///
"""Ep.15 — where do your views actually come from?

Every view has a traffic source: the Shorts feed, search, your channel page, a
subscriber's home feed, an outside link. The Analytics API reports it per video
and per channel, so you can stop guessing where to put your effort.

    uv run sources.py                 # Shorts, last 21 days
    uv run sources.py --longs         # long videos instead
    uv run sources.py --days 60
"""
import argparse, datetime as dt
from googleapiclient.discovery import build
from auth import get_credentials

NAMES = {"SHORTS": "Shorts feed", "YT_SEARCH": "YouTube search", "YT_CHANNEL": "your channel page",
         "YT_OTHER_PAGE": "other YouTube pages", "EXT_URL": "outside links", "SUBSCRIBER": "subscribers' home feed",
         "NOTIFICATION": "notifications", "PLAYLIST": "playlists", "RELATED_VIDEO": "suggested videos",
         "BROWSE": "home / browse", "NO_LINK_OTHER": "direct / unknown"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=21)
    ap.add_argument("--longs", action="store_true")
    a = ap.parse_args()
    ya = build("youtubeAnalytics", "v2", credentials=get_credentials())
    end = dt.date.today() - dt.timedelta(days=3)          # Analytics lags ~3 days
    start = end - dt.timedelta(days=a.days)
    kind = "videoOnDemand" if a.longs else "shorts"
    rows = ya.reports().query(ids="channel==MINE", startDate=str(start), endDate=str(end),
                              dimensions="insightTrafficSourceType", metrics="views",
                              filters=f"creatorContentType=={kind}", sort="-views").execute().get("rows", [])
    total = sum(v for _, v in rows) or 1
    print(f"{'longs' if a.longs else 'Shorts'}: {total:,} views, {start} to {end}\n")
    for src, v in rows[:8]:
        bar = "#" * max(1, round(40 * v / total))
        print(f"{NAMES.get(src, src):24}{v:8,}  {v/total:6.1%}  {bar}")


if __name__ == "__main__":
    main()
