# /// script
# requires-python = ">=3.11"
# dependencies = ["google-api-python-client","google-auth-oauthlib","google-auth-httplib2"]
# ///
"""titlescan v2 — measure audience demand for a search phrase, stably.

v1 took the MAXIMUM views/subs ratio from 8 search results. One outlier video
appearing or not appearing between calls swung the answer up to 30x
("what happens on the sun": 4209x, then 128x, hours apart on 2026-09-03).
Decisions were being made on sampling noise.

v2 changes three things:
  * 50 results instead of 8 — same 100-unit quota cost, far more signal
  * the MEDIAN qualifying ratio, not the maximum — one outlier cannot move it
  * reports N and the spread, so low-confidence answers are visible as such

Usage:  uv run titlescan.py phrases.txt
"""
import statistics, sys, datetime as dt
from auth import get_service

MAX_SUBS  = 200_000   # ignore huge channels; we cannot learn from them
MIN_SUBS  = 100       # below this, ratios explode meaninglessly
MIN_VIEWS = 1_000     # drop the dead results YouTube pads the page with
MIN_N     = 5         # fewer qualifying results than this = low confidence
PCTILE    = 0.90      # "what a GOOD video on this topic achieves"
                      # max = one outlier, wildly unstable (v1: 4209x -> 128x)
                      # median = dominated by weak videos, everything scores skip
                      # p90 = the realistic upside, and it moves little between runs

yt = get_service()
SINCE = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=365)).strftime("%Y-%m-%dT%H:%M:%SZ")
PHRASES = [p.strip() for p in open(sys.argv[1]).read().splitlines() if p.strip()]

rows = []
for q in PHRASES:
    try:
        r = yt.search().list(part="id", q=q, type="video", videoDuration="short",
                             order="viewCount", publishedAfter=SINCE, maxResults=50).execute()
    except Exception as e:
        print(f"!! quota/err on '{q}': {str(e)[:90]}"); break
    ids = [i["id"]["videoId"] for i in r.get("items", [])]
    if not ids:
        print(f"{q:<40} no results"); continue

    ratios, best = [], None
    for i in range(0, len(ids), 50):
        v = yt.videos().list(part="statistics,snippet", id=",".join(ids[i:i+50])).execute()
        chans = list({it["snippet"]["channelId"] for it in v["items"]})
        subs = {}
        for j in range(0, len(chans), 50):
            c = yt.channels().list(part="statistics", id=",".join(chans[j:j+50])).execute()
            subs.update({it["id"]: int(it["statistics"].get("subscriberCount", 0) or 0)
                         for it in c["items"]})
        for it in v["items"]:
            s = subs.get(it["snippet"]["channelId"], 0)
            vw = int(it["statistics"].get("viewCount", 0) or 0)
            if MIN_SUBS <= s < MAX_SUBS and vw >= MIN_VIEWS:
                ratios.append(vw / s)
                if best is None or vw / s > best[0]:
                    best = (vw / s, vw, s, it["snippet"]["title"][:44])
    if not ratios:
        print(f"{q:<40} (all channels too big or too small)"); continue
    rs = sorted(ratios)
    idx = min(len(rs) - 1, int(len(rs) * PCTILE))
    score = rs[idx]                      # 90th percentile
    rows.append((score, q, len(rs), statistics.median(rs), rs[-1], best))

rows.sort(reverse=True)
print(f"\n{'p90':>8} {'verdict':<10} {'n':>3} {'median':>8} {'max':>9}  phrase")
for score, q, n, med, mx, best in rows:
    verdict = "BUILD" if score >= 100 else ("judgement" if score >= 30 else "skip")
    if n < MIN_N:
        verdict = "low-conf"
    print(f"{score:8.0f}x {verdict:<10} {n:>3} {med:>7.0f}x {mx:>8.0f}x  {q}")
print(f"\n90th-PERCENTILE ratio among channels {MIN_SUBS}-{MAX_SUBS:,} subs with {MIN_VIEWS:,}+ views.")
print("BANDS (calibrated 2026-09-04 against known outcomes):")
print("  >=100x  build      ocean 4453 | battery 277 | deepest hole 114")
print("  30-100x judgement  BCI 63 | lab meat 30   -> build if it fits the vertical mix")
print("  <30x    skip       lab-grown organs 11 | birds 7 | room-temp superconductor 6")
print(f"n < {MIN_N} = low confidence, too few comparable channels to trust.")
print("Ratio is a FILTER on what to BUILD — never a reason to cut finished work.")
