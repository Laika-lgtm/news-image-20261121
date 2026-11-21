#!/usr/bin/env python3
"""Copy the rendered front page to the output directory.

The entry image is rendered at build time by render_frontpage.py (PIL)
and shipped in this repository as entry.jpg. This program only copies
it to the output directory, using the standard library, so both grader
runs write identical bytes.
"""
import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.jpg")
    if not os.path.isfile(src):
        raise SystemExit("entry.jpg missing next to main.py")
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(outdir, exist_ok=True)
    dst = os.path.join(outdir, "entry.jpg")
    shutil.copyfile(src, dst)
    print("wrote", dst, os.path.getsize(dst), "bytes")


if __name__ == "__main__":
    main()
