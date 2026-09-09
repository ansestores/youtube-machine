# /// script
# requires-python = ">=3.10"
# dependencies = ["google-api-python-client", "google-auth-oauthlib"]
# ///
"""Ep.13 — engaged views: the free metric that beats views.

A VIEW is counted when a Short is shown and starts playing. An ENGAGED VIEW is
counted only when the person did not immediately swipe away. Divide one by the
other and you get the share of people who actually gave the video a chance.

It is one extra metric name on the Analytics call you are already making
(Ep.10), so it costs no extra quota.

    uv run engaged.py                 # channel median + writes engaged.csv
    uv run engaged.py --split 600     # do 600+ view videos engage better?

WARNING: Shorts only. On long videos the most-viewed one often has the WORST
engagement and the BEST watch time, because browse traffic is low-intent.
Judge longs by minutes watched, not by this.
"""
import argparse, csv, datetime as dt, statistics
from googleapiclient.discovery import build
from auth import get_credentials

SHORTS = "creatorContentType==shorts"        # the only correct long/short filter


def rows(days, content_type):
    creds = get_credentials()
    ya = build("youtubeAnalytics", "v2", credentials=creds)
    end = dt.date.today() - dt.timedelta(days=3)      # Analytics lags ~3 days
    start = end - dt.timedelta(days=days)
    r = ya.reports().query(
        ids="channel==MINE", startDate=str(start), endDate=str(end),
        dimensions="video", filters=content_type,
        metrics="views,engagedViews,averageViewPercentage",
        sort="-views", maxResults=200).execute()
    return r.get("rows", [])


def titles(video_ids):
    creds = get_credentials()
    yt = build("youtube", "v3", credentials=creds)
    out = {}
    for i in range(0, len(video_ids), 50):
        chunk = video_ids[i:i + 50]
        for it in yt.videos().list(part="snippet", id=",".join(chunk)).execute()["items"]:
            out[it["id"]] = it["snippet"]["title"]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=90)
    ap.add_argument("--split", type=int, help="compare videos above/below N views")
    a = ap.parse_args()

    data = rows(a.days, SHORTS)
    if not data:
        print("no Shorts data in the window"); return
    name = titles([r[0] for r in data])

    recs = []
    for vid, views, engaged, avp in data:
        if views:
            recs.append(dict(views=views, engaged=engaged,
                             rate=engaged / views, completion=avp,
                             title=name.get(vid, vid)))

    print("metric: engagedViews / views  (Analytics API)")
    print(f"channel median: {statistics.median(r['rate'] for r in recs):.0%}")

    with open("engaged.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["views", "engaged", "rate", "title"])
        for r in recs:
            w.writerow([f"{r['views']:5d}", f"{r['engaged']:7d}",
                        f"{r['rate']:4.0%}", r["title"]])

    if a.split:
        hi = [r for r in recs if r["views"] >= a.split]
        lo = [r for r in recs if r["views"] < a.split]
        if hi and lo:
            med = lambda g, k: statistics.median(r[k] for r in g)
            print(f"\n{a.split}+ views   median engaged {med(hi,'rate'):.0%}")
            print(f"under {a.split}    median engaged {med(lo,'rate'):.0%}")
            print(f"\ncompletion   {med(hi,'completion'):.0f}% vs "
                  f"{med(lo,'completion'):.0f}%  <- barely separates")


if __name__ == "__main__":
    main()
