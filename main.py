"""Copy the pre-rendered front page to the output directory.

The entry image is stored in this repository as entry.jpg. The grader
runs this program twice in a fresh container with a read-only copy of
the repository and a writable output directory, and expects the output
file to be named entry.png (the name stays entry.png even though the
bytes are a JPEG). Outside the grader, MAKEFUN_OUTPUT_DIR stands in
for /output.
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    source = Path(__file__).resolve().parent / "entry.jpg"
    if not source.is_file():
        print(f"error: {source} is missing", file=sys.stderr)
        return 1
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    shutil.copyfile(source, target)
    if _sha256(target) != _sha256(source):
        print(f"error: {target} differs from {source}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
