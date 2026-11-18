"""Copy the repository's entry.png into the directory named by MAKEFUN_OUTPUT_DIR.

The evaluator runs this script with MAKEFUN_OUTPUT_DIR pointing at the output
directory; the file must land there as entry.png, byte-identical to the copy
that sits next to this script.
"""

import os
import shutil
import sys
from pathlib import Path

SOURCE_NAME = "entry.png"
OUTPUT_NAME = "entry.png"


def main() -> int:
    # Anchor on this script's own location, not the process CWD, so the entry
    # works no matter where the evaluator invokes it from.
    source = Path(__file__).resolve().parent / SOURCE_NAME

    if not source.is_file():
        print(f"error: source image not found: {source}", file=sys.stderr)
        return 1

    raw_out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not raw_out_dir:
        print(
            "error: MAKEFUN_OUTPUT_DIR is not set "
            "(e.g. MAKEFUN_OUTPUT_DIR=out python main.py)",
            file=sys.stderr,
        )
        return 1

    # The output directory may not exist yet (default is /output); create it,
    # including any missing parents, instead of failing.
    out_dir = Path(raw_out_dir)
    destination = out_dir / OUTPUT_NAME
    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
    except OSError as exc:
        print(f"error: cannot write {destination}: {exc}", file=sys.stderr)
        return 1

    print(f"copied {source} -> {destination}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
