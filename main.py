#!/usr/bin/env python3
"""Copy the front page into the grader's output folder.

The picture itself is drawn by build_image.py and stored next to this
file as entry.png. All this script does is place an exact copy at
/output/entry.png, using only the standard library, so the two runs the
grader performs produce byte-identical files without any network use.
"""
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "entry.png"
TARGET = Path("/output") / "entry.png"


def main() -> int:
    if not SOURCE.is_file():
        print(f"missing: {SOURCE}")
        raise SystemExit(2)
    payload = SOURCE.read_bytes()
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_bytes(payload)
    print(f"entry.png -> {TARGET} ({len(payload)} bytes)")
    return 0


raise SystemExit(main())
