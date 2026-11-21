#!/usr/bin/env python3
"""Entrypoint: copy the rendered front page to the harness output dir.

The image is rendered by render_frontpage.py into entry.jpg next to this
file. This program copies it to $MAKEFUN_OUTPUT_DIR/entry.png (or
/output/entry.png) and verifies the copy is byte-identical to the
source, failing loudly otherwise.
"""
import hashlib
import os
import shutil
import sys


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.jpg")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    if sha256(src) != sha256(dst):
        print("FATAL: output hash does not match entry.jpg", file=sys.stderr)
        sys.exit(1)
    size = os.path.getsize(dst)
    if size > 1048576:
        print("FATAL: entry exceeds 1 MiB (%d bytes)" % size, file=sys.stderr)
        sys.exit(1)
    from PIL import Image
    with Image.open(dst) as im:
        if im.size[0] > 1024 or im.size[1] > 1024:
            print("FATAL: entry exceeds 1024x1024 (%s)" % (im.size,),
                  file=sys.stderr)
            sys.exit(1)
    print("wrote", dst, size, "bytes")


if __name__ == "__main__":
    main()
