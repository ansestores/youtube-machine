"""auth.py — one OAuth helper, shared by the scripts in this folder.

Setup (once):
  1. Google Cloud Console -> APIs & Services -> Enable "YouTube Data API v3"
  2. Credentials -> OAuth client ID -> Desktop app -> download the JSON
  3. Save it next to these scripts as: client_secret.json

The first run opens a browser once and writes token.json beside it.
Every run after that is silent. Never commit either file.
"""
import sys
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

HERE = Path(__file__).resolve().parent
TOKEN = HERE / "token.json"
CLIENT_SECRET = HERE / "client_secret.json"
SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]


def get_service():
    creds = None
    if TOKEN.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CLIENT_SECRET.exists():
                sys.exit(f"Missing {CLIENT_SECRET}\n"
                         "Download the OAuth client JSON from Google Cloud Console "
                         "and save it to that exact path (see the README).")
            creds = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET), SCOPES).run_local_server(port=0)
        TOKEN.write_text(creds.to_json())
    return build("youtube", "v3", credentials=creds)
