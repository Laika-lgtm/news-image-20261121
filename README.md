# The World Today — Saturday 21 November 2026

[![make.fun](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/Laika-lgtm/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/Laika-lgtm/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121)

A one-page newspaper front page summing up Saturday 21 November 2026:
35 stories across 7 regions, led by three pictured top stories — COP31
spilling into overtime in Antalya, three missiles downed over Riyadh,
and the M6.8 Peru quake — with a stat strip, colour-coded region pills,
a dense "World in Brief" list with UTC timestamps, and a DATE CHECK box
naming the Friday news deliberately left out.

The three photos (COP31 summit hall, interceptor trails over Riyadh,
residents outdoors in Lima) are ChatGPT images. Everything else is
drawn with PIL.

## Run

```sh
python3 render_frontpage.py   # builds entry.jpg (1024x1024, JPEG q82)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` copies `entry.jpg` (rendered at build time by the PIL
renderer) to the output directory. It uses only the standard library
and writes identical bytes on every run.

## Sources

See [SOURCES.md](SOURCES.md) for the 35 stories and where each was
verified. Every story happened, or was first reported, on Saturday
21 November 2026, in some time zone; all times are UTC.
