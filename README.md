# The Day in Brief — World News, 18 November 2026

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/yobrave/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/yobrave/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

This repository is a contest entry for the make.fun bounty
**news-image-20261118**. It ships a single 1024×1024 image, `entry.png`,
that summarizes the world news of 18 November 2026 in the style of a
newspaper front page, plus a small entry program (`main.py`) that the
grader runs to collect the image.

## The image

`entry.png` is laid out like a classic broadsheet front page on a cream
background — masthead, three illustrated lead stories, numbered regional
briefs, a "Where It Happened" world map, and an "Also on Wednesday"
strip:

- **Masthead** — kicker row "THE DAY IN BRIEF · LATE EDITION" /
  "40 STORIES · 6 CONTINENTS · ALL FROM WEDNESDAY", then the date line
  **WEDNESDAY 18 NOVEMBER 2026** as the page's largest element.
- **Three illustrated heroes** (01–03), each in a framed panel with
  deterministic vector art: the APEC summit flags table (Trump–Putin–Xi
  in Shenzhen), a schematic Gulf theatre map with strike markers (Iran
  attacks Kuwait and Bahrain), and the Nvidia chip with rising futures
  bars.
- **Six regional sections** (04–34) — Americas, Europe & Russia, Middle
  East, Asia, Africa, Oceania — every brief numbered and color-coded by
  continent (red / blue / orange / purple / green / teal).
- **Where It Happened** — an equirectangular world map with numbered
  pins (colored by continent) marking the lead story for 17 locations.
- **Also on Wednesday** (35–40) — six one-line briefs (Bond casting,
  Anthropic's crypto bet, college playoff, Rickelton's century, the
  withdrawn FDA nominee, "Dancing With The Stars").
- **Attribution rail** — source credits (AP · BBC · FT · WSJ · Guardian ·
  Reuters · Al Jazeera · Bloomberg · NYT · CBS · ESPN) and a method line:
  every item was first reported or followed up on Wednesday, claims
  attributed to source.

Every fact on the page is documented with publisher and timestamp in
[`notes.md`](notes.md).

## How the image is built

`render.py` draws the entire page deterministically with Pillow vector
primitives and system fonts (no randomness, no network): run it twice and
the PNG bytes are identical, which satisfies the bounty's double-run
byte-consistency requirement. The graded program is still `main.py`; the
repository ships the pre-rendered `entry.png` it copies.

```sh
python render.py   # rebuilds entry.png (requires Pillow)
```

## How the grader runs it

The entry program reads the output directory from the `MAKEFUN_OUTPUT_DIR`
environment variable (defaults to `/output` in the grading environment) and
writes `entry.png` there, byte-for-byte identical to the copy in this
repository. It creates the output directory if it does not exist yet and
uses only the Python 3 standard library.

```sh
MAKEFUN_OUTPUT_DIR=/output python main.py
```

## Run it locally

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python main.py
```

The program verifies its own output: after copying, it compares the
SHA-256 digests of the source and the written file and exits non-zero on
any mismatch. To double-check from the shell:

```sh
sha256sum entry.png out/entry.png
```

Both digests must match —
`64fefbadb5fd09b95f0eccb3103918f9577ce2bb50aab202296b023b8d44d710` for
the current `entry.png` (192,914 bytes). Requires Python 3.6+; no
third-party dependencies for the graded run.

## Repository layout

| File         | Purpose                                              |
| ------------ | ---------------------------------------------------- |
| `entry.png`  | The contest image (1024×1024 PNG).                   |
| `main.py`    | Entry program; copies `entry.png` to the output dir. |
| `render.py`  | Deterministic Pillow renderer that builds `entry.png`. |
| `notes.md`   | Fact base: all 40 stories with publisher + timestamp. |
| `LICENSE`    | MIT License.                                         |

---

This is an entry for the make.fun bounty **news-image-20261118**.
