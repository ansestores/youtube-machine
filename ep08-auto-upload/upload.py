"""Ep.8 — Upload a finished video to YouTube from Python. No browser, no clicking.

Setup once:
  1. console.cloud.google.com -> new project -> enable "YouTube Data API v3"
  2. Credentials -> OAuth client ID -> Desktop app -> download as client_secret.json
  3. pip install google-api-python-client google-auth-oauthlib

First run opens a browser once and writes token.json. Every run after that is silent.
"""
import os, json, argparse
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload",
          "https://www.googleapis.com/auth/youtube"]
HERE = os.path.dirname(os.path.abspath(__file__))
TOKEN = os.path.join(HERE, "token.json")
SECRET = os.path.join(HERE, "client_secret.json")


def get_service():
    creds = None
    if os.path.exists(TOKEN):
        creds = Credentials.from_authorized_user_file(TOKEN, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())          # silent: no browser
        else:
            flow = InstalledAppFlow.from_client_secrets_file(SECRET, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN, "w") as f:
            f.write(creds.to_json())
    return build("youtube", "v3", credentials=creds)


def upload(path, title, description, tags, privacy="private", publish_at=None):
    yt = get_service()
    body = {
        "snippet": {
            "title": title[:100],            # YouTube hard-caps titles at 100 chars
            "description": description[:5000],
            "tags": tags[:30],
            "categoryId": "28",              # 28 = Science & Technology
        },
        "status": {"privacyStatus": privacy, "selfDeclaredMadeForKids": False},
    }
    if publish_at:                            # ISO-8601 UTC, e.g. 2026-09-07T13:00:00Z
        body["status"]["privacyStatus"] = "private"
        body["status"]["publishAt"] = publish_at

    media = MediaFileUpload(path, chunksize=4 * 1024 * 1024, resumable=True)
    req = yt.videos().insert(part="snippet,status", body=body, media_body=media)

    response = None
    while response is None:
        status, response = req.next_chunk()   # resumable: survives a dropped wifi
        if status:
            print(f"  uploading... {int(status.progress() * 100)}%")
    vid = response["id"]
    print(f"done -> https://youtu.be/{vid}")
    return vid


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("file")
    p.add_argument("--title", required=True)
    p.add_argument("--desc", default="")
    p.add_argument("--tags", default="")
    p.add_argument("--at", default=None, help="publish time, e.g. 2026-09-07T13:00:00Z")
    a = p.parse_args()
    upload(a.file, a.title, a.desc,
           [t.strip() for t in a.tags.split(",") if t.strip()],
           publish_at=a.at)
