# /// script
# requires-python = ">=3.11"
# dependencies = ["google-api-python-client","google-auth-oauthlib","google-auth-httplib2"]
# ///
"""subs_by_video — which of your videos actually earned subscribers (YouTube Analytics API).
Sort by subscribersGained, not views. Needs an OAuth token with the yt-analytics.readonly scope.
  uv run subs_by_video.py [--since 2026-07-01]
"""
import sys, datetime as dt
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
since = sys.argv[sys.argv.index("--since")+1] if "--since" in sys.argv else (dt.date.today()-dt.timedelta(days=90)).isoformat()
creds = Credentials.from_authorized_user_file("token.json")
ya = build("youtubeAnalytics", "v2", credentials=creds); yt = build("youtube", "v3", credentials=creds)
r = ya.reports().query(ids="channel==MINE", startDate=since, endDate=dt.date.today().isoformat(), dimensions="video",
                       metrics="views,subscribersGained,averageViewPercentage", sort="-subscribersGained", maxResults=200).execute()
rows = r.get("rows", []); ids = [x[0] for x in rows]; title = {}
for i in range(0, len(ids), 50):
    for it in yt.videos().list(part="snippet", id=",".join(ids[i:i+50])).execute()["items"]:
        title[it["id"]] = it["snippet"]["title"]
print(f"{'subs':>4} {'views':>6} {'per1k':>5} {'avg%':>5}  title")
for vid, views, subs, avp in rows:
    print(f"{int(subs):>4} {int(views):>6} {1000*subs/max(views,1):5.1f} {avp:5.1f}  {title.get(vid,'?')[:70]}")
