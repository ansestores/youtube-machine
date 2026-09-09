# Ep.9 — Schedule a whole week, and file every video automatically

```bash
python schedule.py slate.json
```

## Why `publishAt` beats uploading at 9am

You are asleep at 9am somewhere. Set `status.publishAt` and the video sits private
until the second you named. The rest of the pipeline can run whenever it likes.

Two rules the API will not tell you:

- **`publishAt` only works while `privacyStatus` is `private`.** Set it to `public`
  alongside a publish time and the video goes live immediately. Ep.8's `upload()`
  forces this for you.
- **The time must be in the future** at the moment the request lands. A slate built
  the night before, uploaded slowly, can walk past its own first slot — so this
  script checks every timestamp up front.

## Playlists resolve by NAME, not id

`resolve_playlists()` builds a title -> id map and the script dies before uploading
if a name in the slate does not exist. Learned the hard way: rename a playlist in
the YouTube UI and every later run quietly stops filing videos into it.
