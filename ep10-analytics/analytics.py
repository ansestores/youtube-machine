"""Ep.10 — Ask YouTube which of your videos actually worked, from Python.

Uploading is solved (Ep.8) and scheduling is solved (Ep.9). This closes the loop:
pull real numbers so you stop guessing which videos are working.

    pip install google-api-python-client google-auth-oauthlib
    python analytics.py            # last 28 days
    python analytics.py --days 7
"""
import argparse, datetime as dt, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "ep08-auto-upload"))
from upload import get_service                      # reuse Ep.8's OAuth verbatim
from googleapiclient.discovery import build


def analytics(creds):
    # NOTE: a different API to the Data API. Same credentials, different service.
    return build("youtubeAnalytics", "v2", credentials=creds)


def report(days=28):
    yt = get_service()
    ya = analytics(yt._http.credentials)
    end = dt.date.today()
    start = end - dt.timedelta(days=days)

    def q(**kw):
        return ya.reports().query(ids="channel==MINE", startDate=str(start),
                                  endDate=str(end), **kw).execute()

    r = q(metrics="views,estimatedMinutesWatched,subscribersGained,averageViewPercentage")
    v, mins, subs, avp = r["rows"][0]
    print(f"last {days} days: {v} views | {mins} watch-min | +{subs} subs | {avp:.1f}% avg viewed")

    # WHERE the views came from — the single most useful table on the platform
    print("\ntraffic sources:")
    r = q(metrics="views", dimensions="insightTrafficSourceType", sort="-views")
    total = sum(x[1] for x in r.get("rows", []))
    for src, n in r.get("rows", []):
        print(f"  {src:<24}{n:>6}  {n/max(total,1)*100:>5.1f}%")

    # what people actually typed to find you
    print("\nsearch terms that found you:")
    r = q(metrics="views", dimensions="insightTrafficSourceDetail",
          filters="insightTrafficSourceType==YT_SEARCH", sort="-views", maxResults=10)
    for term, n in r.get("rows", []):
        print(f"  {n:>4}  {term}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--days", type=int, default=28)
    report(p.parse_args().days)
