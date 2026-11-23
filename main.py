#!/usr/bin/env python3
"""Entry for make.fun news-image-20261122.

Writes the entry image to /output/entry.png. The image is a newspaper
front page summing up the world news of Sunday 22 November 2026: the
COP31 climate talks collapsing in Antalya with no deal, a Russian drone
hitting an apartment block in Dymer near Kyiv, Iran striking an
industrial site in Bahrain, the Russian cargo ship Sparta II still
burning in the Gulf of Finland, the capture of cartel boss
'El Chapo Isidro' in Mexico, a deadly factory fire in Cikande,
Indonesia, and BepiColombo reaching Mercury, plus a ticker of the day's
other stories.

The image was drawn by build_image.py (same repository) with Pillow and
is shipped here as entry.png. This program only copies it, using the
standard library, so both grader runs write identical bytes. No network
is used.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    src = os.path.join(HERE, "entry.png")
    os.makedirs("/output", exist_ok=True)
    dst = os.path.join("/output", "entry.png")
    shutil.copyfile(src, dst)
    print("wrote %s (%d bytes)" % (dst, os.path.getsize(dst)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
