# Ep.11 — Run it every day without you

```bash
chmod +x daily.sh
# Linux
crontab -e         # 0 4 * * * /home/you/yshorts/daily.sh
# macOS
cp com.creator.daily.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.creator.daily.plist
```

## The three things that break unattended pipelines

**No lock.** Two runs overlap, both write the same files, and you get a corrupt
upload. `flock` does not exist on macOS — `mkdir` is atomic on every Unix and works
as a lock on both.

**cron has almost no environment.** No `PATH` to your Python, no virtualenv, no
`HOME` you expect. A script that works in your shell fails silently at 4am. Use
absolute paths, and set `PIPELINE_ROOT` explicitly.

**Nothing is logged.** When it fails at 4am you need to know why at 9am. Everything
goes to a dated log via `exec > >(tee -a ...)`, so both stdout and stderr are kept.

## macOS: launchd, not cron

cron still works but launchd is the supported path, and it will run a missed job
when the machine wakes. A Mac that was asleep at 4am simply skips a cron job.
