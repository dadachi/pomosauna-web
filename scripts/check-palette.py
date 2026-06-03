#!/usr/bin/env python3
"""Fail if a file uses any colour outside Refactoring UI Palette 6.

Only the RGB base is checked; alpha (opacity) is ignored, since transparency is
compositing rather than a distinct colour. Covers hex literals and rgb()/rgba()
triples (including the static triples inside template literals).

Usage: python3 scripts/check-palette.py [file ...]   (defaults to index.html)
"""
import re
import sys

# Refactoring UI — Palette 6 (Red, Yellow, Warm Grey, Cyan, Lime Green) plus the
# Palette 8 scales now used by the Palette-8 reskin: Blue (Vivid), Orange, Cool
# Grey. Light Blue (Vivid) + #0B4F71 remain for the legacy waterfall themes.
# See docs-private/palette-6.md and palette-8.md.
PALETTE_HEX = """
610404 780A0A 911111 A61B1B BA2525 D64545 E66A6A F29B9B FACDCD FFEEEE
8D2B0B B44D12 CB6E17 DE911D F0B429 F7C948 FADB5F FCE588 FFF3C4 FFFBEA
27241D 423D33 504A40 625D52 857F72 A39E93 B8B2A7 D3CEC4 E8E6E1 FAF9F7
044E54 0A6C74 0E7C86 14919B 2CB1BC 38BEC9 54D1DB 87EAF2 BEF8FD E0FCFF
2B4005 42600C 507712 63921A 7BB026 94C843 ABDB5E C7EA8F E2F7C2 F2FDE0
035388 0B69A3 127FBF 1992D4 2BB0ED 40C3F7 5ED0FA 81DEFD B3ECFF E3F8FF
0B4F71
002159 01337D 03449E 0552B5 0967D2 2186EB 47A3F3 7CC4FA BAE3FF E6F6FF
572508 77340D 8C3D10 AB4E19 C65D21 E67635 EF8E58 FAB38B FFD3BA FFEFE6
1F2933 323F4B 3E4C59 52606D 616E7C 7B8794 9AA5B1 CBD2D9 E4E7EB F5F7FA
""".split()


def to_rgb(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


PALETTE_HEX_SET = set(h.upper() for h in PALETTE_HEX)
PALETTE_RGB_SET = set(to_rgb(h) for h in PALETTE_HEX)


def check(path):
    src = open(path, encoding="utf-8").read()
    bad = set()
    for m in set(re.findall(r"#[0-9a-fA-F]{3,8}\b", src)):
        h = m.lstrip("#")
        if len(h) in (3, 6):
            norm = ("".join(c * 2 for c in h) if len(h) == 3 else h).upper()
            if norm not in PALETTE_HEX_SET:
                bad.add(m)
        else:
            bad.add(m)  # 4-/8-digit hex (alpha baked in) — review manually
    for m in set(re.findall(r"rgba?\((\d+)\s*,\s*(\d+)\s*,\s*(\d+)", src)):
        if tuple(int(x) for x in m) not in PALETTE_RGB_SET:
            bad.add("rgb(%s,%s,%s)" % m)
    return sorted(bad)


def main(paths):
    failed = False
    for p in paths:
        bad = check(p)
        if bad:
            failed = True
            print("✗ off-palette colours in %s:" % p)
            for b in bad:
                print("    ", b)
        else:
            print("✓ all colours in %s are within Palette 6" % p)
    if failed:
        print("\nAllowed colours are the 50 listed in this script (Refactoring UI Palette 6).")
        print("Alpha may vary freely; only the RGB base must be in-palette.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:] or ["index.html"]))
