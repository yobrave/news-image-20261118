#!/usr/bin/env python3
"""Entry program for the make.fun bounty news-image-20261118.

Copies entry.png (located next to this script) into the directory named by
the MAKEFUN_OUTPUT_DIR environment variable, so the grader finds an
entry.png that is byte-for-byte identical to the one in this repository.
After copying, the SHA-256 digests of source and destination are compared
and any mismatch aborts with a non-zero exit code.
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path

ENTRY_FILENAME = "entry.png"
OUTPUT_DIR_ENV = "MAKEFUN_OUTPUT_DIR"


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    # resolve() anchors the source to this script's directory, so the copy
    # works no matter which working directory the grader invokes us from.
    source = Path(__file__).resolve().parent / ENTRY_FILENAME

    output_dir_raw = os.environ.get(OUTPUT_DIR_ENV, "").strip()
    if not output_dir_raw:
        print(
            f"error: environment variable {OUTPUT_DIR_ENV} is not set; "
            "cannot determine where to write entry.png "
            "(the grading environment defaults it to /output)",
            file=sys.stderr,
        )
        return 2

    if not source.is_file():
        print(f"error: entry image not found at {source}", file=sys.stderr)
        return 1

    output_dir = Path(output_dir_raw)
    destination = output_dir / ENTRY_FILENAME
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
    except OSError as exc:
        print(f"error: cannot write {destination}: {exc}", file=sys.stderr)
        return 3

    source_digest = sha256_of(source)
    dest_digest = sha256_of(destination)
    if source_digest != dest_digest:
        print(
            f"error: copy verification failed, digests differ "
            f"(source {source_digest}, destination {dest_digest})",
            file=sys.stderr,
        )
        return 4

    size = destination.stat().st_size
    print(f"copied {source} -> {destination} ({size} bytes, sha256 {source_digest})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
