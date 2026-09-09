"""Ep.9 — Schedule a week of uploads and file each one into the right playlist.

The upload from Ep.8 puts one video up. This turns that into a slate:
a JSON plan in, a scheduled + sorted channel out.

    python schedule.py slate.json
"""
import os, sys, json, datetime as dt
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ep08-auto-upload"))
from upload import get_service, upload            # reuse Ep.8 verbatim


def resolve_playlists(yt):
    """title -> playlistId for every playlist on the channel."""
    out, tok = {}, None
    while True:
        r = yt.playlists().list(part="snippet", mine=True,
                                maxResults=50, pageToken=tok).execute()
        for p in r["items"]:
            out[p["snippet"]["title"]] = p["id"]
        tok = r.get("nextPageToken")
        if not tok:
            return out


def add_to_playlist(yt, video_id, playlist_id):
    yt.playlistItems().insert(part="snippet", body={"snippet": {
        "playlistId": playlist_id,
        "resourceId": {"kind": "youtube#video", "videoId": video_id},
    }}).execute()


def run(slate_path):
    with open(slate_path) as f:
        slate = json.load(f)

    yt = get_service()
    known = resolve_playlists(yt)

    # Fail BEFORE uploading anything if a playlist name is wrong. A typo here
    # silently creates nothing and you find out days later that a video is orphaned.
    missing = {i["playlist"] for i in slate if i.get("playlist") and i["playlist"] not in known}
    if missing:
        raise SystemExit(f"no such playlist(s): {sorted(missing)}\nhave: {sorted(known)}")

    for item in slate:
        when = dt.datetime.fromisoformat(item["publish_at"]).astimezone(dt.timezone.utc)
        if when <= dt.datetime.now(dt.timezone.utc):
            raise SystemExit(f"{item['file']}: publish_at is in the past")

        print(f"\n{item['file']}  ->  {when:%Y-%m-%d %H:%M UTC}")
        vid = upload(item["file"], item["title"], item.get("description", ""),
                     item.get("tags", []),
                     publish_at=when.strftime("%Y-%m-%dT%H:%M:%SZ"))

        if item.get("playlist"):
            add_to_playlist(yt, vid, known[item["playlist"]])
            print(f"  filed under: {item['playlist']}")


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else "slate.json")
