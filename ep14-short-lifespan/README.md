# Ep 14 — How long does a Short actually keep getting views?

Everyone repeats a rule of thumb. Your own Analytics knows the real answer for *your* channel.

```
uv run lifespan.py
```

## What it found here (real output)

```
   day0   day1   day2   day3  d0 share  title
   1302    455     38     30      71%  Saturn Just Grew a 10-Sided Shape 🪐
    641    444     24      8      57%  Artemis III: Why Is a 1998 Shuttle E
    552    440     31      9      53%  Tsar Bomba: The Biggest Explosion Hu
    969     36      9     18      94%  Why Do Cats Knead? 🐱
    614    343     14      8      63%  How Do Tornadoes Form? 🌪️
     21    804     39     13       2%  Thwaites Glacier: 245 Icequakes
      5    666      5      0       1%  Blind Spot Test: There's a HOLE
     12    279    366      4       2%  What Happens in Space Without a Suit

median share arriving on publish day: 55%
```

Two things fall out of this, and the second one is the useful one.

**1. A Short is finished after about 48 hours.** Day 2 and day 3 are noise — 38, 30, 24, 9, 5, 0. Checking a video on day 5 tells you nothing you did not already know on day 2.

**2. The publish day tells you almost nothing.** Look at the bottom three rows. *Blind Spot Test* took **5 views on its publish day and 666 the next**. *Thwaites Glacier* took 21, then 804. If you had judged either one after a few hours you would have called it a failure and changed the wrong thing.

So: **never judge a Short before 48 hours.** Not after four hours, not on publish day. The median video front-loads 55% of its views, but the variance is so wide that the first day is not a signal at all.

## Notes

Analytics lags about three days, so the script only looks at videos whose full four-day window has been published. Videos newer than that are skipped rather than reported as zeroes — Analytics returns a 500 for a window it cannot fill yet.
