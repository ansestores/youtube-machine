# Ep.8 — Upload to YouTube from Python

One command puts a finished file on your channel:

```bash
pip install google-api-python-client google-auth-oauthlib
python upload.py out.mp4 --title "My Video" --desc "..." --tags "science,facts"
```

## The three things that trip everyone up

1. **`categoryId` is required.** `28` is Science & Technology. Leave it out and the
   API returns a 400 that does not say which field is wrong.
2. **Use a resumable upload.** `chunksize` + `next_chunk()` means a dropped connection
   costs you one 4 MB chunk, not the whole file.
3. **`token.json` is the whole point.** The browser opens once. After that the refresh
   token keeps working forever — which is what makes the pipeline unattended.

## Quota

Every upload costs **1600 units** of a 10,000/day budget. That is 6 uploads a day
before you have to request more. Plan the slate around it.
