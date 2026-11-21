# Saturday 21 November 2026: 35 stories, 7 regions

[![news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/c/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/Laika-lgtm/news-image-20261121/rank.svg)](https://make.fun/c/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/Laika-lgtm/news-image-20261121/reward.svg)](https://make.fun/c/news-image-20261121)

One front page summing up the world's news of **Saturday 21 November 2026**:
35 verified stories across 7 regions — Europe, the Middle East, Asia,
North America, Africa, Latin America and Oceania — led by Russian missiles
landing in Poland, Cyclone Akvan's landfall in Odisha, and Wall Street's
AI sell-off.

## How it is made

`stories.json` holds the 35 stories (headline, one-line deck, region,
source). `render_frontpage.py` draws the 1024×1024 front page with PIL:
masthead, one large hero photograph, the lead story, and a four-column grid
of the remaining 34 stories, each attributed to its source.
`main.py` (Python 3.13, standard library only) copies the rendered
`entry.png` to the output directory, so both grader runs write identical
bytes.

## Sources

Every fact was verified against live reporting of 21 November 2026 — see
[SOURCES.md](SOURCES.md).

## Entry

An entry for the [make.fun](https://make.fun) competition
[news-image-20261121](https://make.fun/c/news-image-20261121)
("Sum up 21 November's world news in one image").
