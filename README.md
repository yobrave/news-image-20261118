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

`entry.png` is laid out like a classic broadsheet front page on a
cream background with bold black serif headlines and red accents:

- **Masthead** — kicker line "ONE PAGE · EVERY TIME ZONE · WEDNESDAY",
  the title **THE DAY IN BRIEF**, and the subtitle
  "WORLD NEWS — 18 NOVEMBER 2026".
- **Six story cards** in a 2×3 grid, each with a red accent bar and icon:
  - *China · APEC Summit* — "Trump and Putin set for summit with Xi"
  - *Iran · Gulf Escalation* — "Iran widens Gulf strikes to Kuwait and Bahrain"
  - *Tech · Nvidia* — "Nvidia beats on earnings, but Huang will not return"
  - *United States · Midterms* — "Peltola flips Alaska Senate seat"
  - *Ukraine · War* — "Zelenskyy protests Starshield curbs"
  - *Climate · COP31* — "COP31 enters decisive week over money"
- **Footer bar** — "ALSO TODAY" one-liners: Haiti rallies behind Bukele as
  Salvadoran troops battle gangs · Ebola doubles in DR Congo · US loses
  measles-free status · Japan exports surge 20.5%.

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
`6965d58da5029fc09d1aedc07699d450bbf94f3280dd240ee917e30454556920` for
the current `entry.png` (129,804 bytes). Requires Python 3.6+; no
third-party dependencies.

## Repository layout

| File         | Purpose                                              |
| ------------ | ---------------------------------------------------- |
| `entry.png`  | The contest image (1024×1024 PNG).                   |
| `main.py`    | Entry program; copies `entry.png` to the output dir. |
| `LICENSE`    | MIT License.                                         |

---

This is an entry for the make.fun bounty **news-image-20261118**.
