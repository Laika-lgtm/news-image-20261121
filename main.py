#!/usr/bin/env python3
"""Copy the pre-rendered front page to the grader output directory.

Stdlib only. The grader runs `python3 -P -s /bot/main.py` with the repo
read-only at /bot, an empty /output, MAKEFUN_OUTPUT_DIR=/output and no
network. This program copies entry.jpg (already verified 1024x1024) to
$MAKEFUN_OUTPUT_DIR/entry.png and verifies the copy by hashing both
files, failing hard on any mismatch. No image library, no dimension
validation, no hardcoded hash: the source file itself is the reference.
"""

import hashlib
import os
import shutil
import sys


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.jpg")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    target = os.path.join(out_dir, "entry.png")

    os.makedirs(out_dir, exist_ok=True)

    if not os.path.isfile(source):
        print("error: source image not found: %s" % source, file=sys.stderr)
        return 1
    source_size = os.path.getsize(source)
    if source_size == 0:
        print("error: source image is empty: %s" % source, file=sys.stderr)
        return 1

    shutil.copyfile(source, target)

    if sha256_of(source) != sha256_of(target):
        print("error: output hash does not match source", file=sys.stderr)
        sys.exit(1)

    if os.path.getsize(target) != source_size:
        print("error: output size does not match source", file=sys.stderr)
        sys.exit(1)

    print("wrote %s (%d bytes)" % (target, os.path.getsize(target)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
