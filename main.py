#!/usr/bin/env python3
"""Entry for make.fun's "Sum up 25 November's world news in one image" bounty.

Writes one image summing up 25 November 2026 world news to
/output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png).

The image ships in this repository as entry.png: six verified
25 November 2026 stories in one 1024x1024 panel:

  1. Middle East - three tankers hit mines in the Strait of Hormuz
  2. Space - Pakistan's first astronaut reaches Tiangong
  3. Europe - Ukraine says it sank a Russian warship off Libya
  4. Tech - US jury convicts Huawei of stealing trade secrets
  5. Markets - AI sell-off deepens, Nvidia slides 7%
  6. Latin America - all hostages freed in the Cartagena siege

Deterministic: the same input file always produces the same output.
Standard library only, no network access.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def main():
    if not os.path.isfile(SOURCE):
        raise SystemExit("entry.png missing next to main.py")
    with open(SOURCE, "rb") as f:
        magic = f.read(len(PNG_MAGIC))
        header = f.read(17)
    if magic != PNG_MAGIC:
        raise SystemExit("entry.png is not a valid PNG file")
    if len(header) < 17 or header[4:8] != b"IHDR":
        raise SystemExit("entry.png has no IHDR chunk")
    width = int.from_bytes(header[8:12], "big")
    height = int.from_bytes(header[12:16], "big")
    if (width, height) != (1024, 1024):
        raise SystemExit(
            "entry.png must be 1024x1024, got %dx%d" % (width, height)
        )
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, dest)
    size = os.path.getsize(dest)
    print("wrote %s (%d bytes)" % (dest, size))


if __name__ == "__main__":
    sys.exit(main())
