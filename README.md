# The World Today — Saturday 21 November 2026

[![make.fun](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/Laika-lgtm/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/Laika-lgtm/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121)

A one-page newspaper front page summing up Saturday 21 November 2026:
31 stories across 6 regions, drawn with PIL — a stat strip, three lead
stories with flat illustrations, ten more stories, a dotted world map
with region counts, a numbered "Also on Saturday" list, and a DATE CHECK
box naming the Friday news deliberately left out.

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` copies `entry.png` (rendered at build time by the PIL renderer)
to the output directory. It uses only the standard library and writes
identical bytes on every run.

## Sources

See [SOURCES.md](SOURCES.md) for the 31 stories and where each was
verified. Every story happened, or was first reported, on Saturday
21 November 2026.
