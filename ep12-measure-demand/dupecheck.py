"""dupecheck — has this topic already been published?

Written 2026-09-04 after proposing "Why Does Time Speed Up As You Get Older?" as a
NEW video when it had been live since Aug 30. The topic appeared in
topic-ledger.md as a numbered row and I read that as an unbuilt idea in the topic
bank. The ledger is a note file; the CHANNEL is the fact. Never again decide
"is this new?" from a local file.

  uv run --with google-api-python-client --with google-auth-oauthlib \
         --with google-auth-httplib2 python tools/dupecheck.py "Title one" "Title two"

Compares on content words, so wording differences do not hide a real duplicate
("Why Does Time Speed Up As You Get Older?" vs "Why Time Speeds Up As You Get Older").
"""
import sys, re, json, unicodedata
from pathlib import Path
from auth import get_service

STOP = {"the","a","an","is","are","was","were","do","does","did","you","your","we",
        "our","it","its","in","on","of","to","for","and","or","but","that","this",
        "what","why","how","when","who","not","no","so","as","at","by","with","from",
        "up","out","actually","really","just","get","gets","got","be","been","can",
        "cant","will","would","one","two","new","here","there","they","them","their"}

def key(t):
    # Strip accents first: "Déjà" split into 'd' and 'j' under a plain [a-z] match,
    # so the deja-vu duplicate scored as unrelated.
    t = unicodedata.normalize("NFKD", t)
    t = "".join(c for c in t if not unicodedata.combining(c))
    words = re.findall(r"[a-z]+", t.lower())
    # Crude stemming, because the pair that started this ("Time Speed Up" vs
    # "Time Speeds Up") differed by ONE trailing s and read as unrelated.
    out = set()
    for w in words:
        if w in STOP or len(w) <= 2: continue
        if w.endswith("ies") and len(w) > 4: w = w[:-3] + "y"
        elif w.endswith("es") and len(w) > 4: w = w[:-2]
        elif w.endswith("s") and not w.endswith("ss"): w = w[:-1]
        out.add(w)
    return out

def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(2)
    yt = get_service()
    up = yt.channels().list(part="contentDetails", mine=True).execute()[
        "items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    ids, tok = [], None
    while True:
        p = yt.playlistItems().list(part="contentDetails", playlistId=up,
                                    maxResults=50, pageToken=tok).execute()
        ids += [i["contentDetails"]["videoId"] for i in p["items"]]
        tok = p.get("nextPageToken")
        if not tok: break
    ids = list(dict.fromkeys(ids))          # the playlist duplicates rows
    live = []
    for i in range(0, len(ids), 50):
        q = yt.videos().list(part="snippet,status,statistics",
                             id=",".join(ids[i:i+50])).execute()
        for it in q["items"]:
            live.append((it["snippet"]["title"],
                         it["status"].get("publishAt") or it["snippet"]["publishedAt"],
                         it["status"]["privacyStatus"],
                         int(it["statistics"].get("viewCount", 0))))
    print(f"checked against {len(live)} videos on the channel\n")
    bad = 0
    for cand in sys.argv[1:]:
        ck = key(cand)
        scored = []
        for t, when, priv, views in live:
            lk = key(t)
            if not lk or not ck: continue
            shared = ck & lk
            overlap = len(shared) / min(len(ck), len(lk))
            # A ratio alone is useless on short titles: "What Is a Black Hole"
            # reduces to 3 content words, so ONE shared word reads as 33-50% and
            # "Stars Blew a Hole in Space" gets flagged as a duplicate of it.
            # Require real evidence — several shared words, not a lucky one.
            # Two shared content words is the floor — one is coincidence
            # ("hole" in both "Stars Blew a Hole in Space" and "What Is a Black
            # Hole"). The ratio then has to be high as well.
            if len(shared) >= 2 and overlap >= 0.6:
                scored.append((overlap, t, when[:10], priv, views, shared))
        scored.sort(reverse=True)
        if scored:
            bad += 1
            print(f"DUPLICATE  {cand}")
            for o, t, when, priv, views, shared in scored[:3]:
                print(f"     {o:.0%} overlap  {when}  {priv:8s} {views:5d} views  {t}")
                print(f"       shared: {', '.join(sorted(shared))}")
        else:
            print(f"clear      {cand}")
        print()
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main()
