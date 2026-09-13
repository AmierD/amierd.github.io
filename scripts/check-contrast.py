#!/usr/bin/env python3
"""
WCAG contrast checker for the Quartz palette in quartz.config.yaml.

  python3 scripts/check-contrast.py              # audit the current palette
  python3 scripts/check-contrast.py '#ffd85b'    # find AA-safe variants of a color

Thresholds (WCAG 2.1):
  AA  normal text  4.5:1   <- links and body text must clear this
  AA  large/UI     3.0:1   <- 18pt+, or bold 14pt+, and UI borders
  AAA normal text  7.0:1
"""
import re, sys, os, colorsys

CFG = os.path.join(os.path.dirname(__file__), "..", "quartz.config.yaml")

def lum(h):
    h = h.lstrip("#")[:6]
    r, g, b = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)

def ratio(fg, bg):
    a, b = sorted([lum(fg), lum(bg)], reverse=True)
    return (a + 0.05) / (b + 0.05)

def grade(r):
    if r >= 7.0:  return "AAA"
    if r >= 4.5:  return "AA"
    if r >= 3.0:  return "AA-large only"
    return "FAIL"

def parse_palette():
    text = open(CFG).read()
    out = {}
    for mode in ("lightMode", "darkMode"):
        m = re.search(rf"{mode}:(.*?)(?=\n      \w+Mode:|\nplugins:)", text, re.S)
        if not m: continue
        out[mode] = dict(re.findall(r'(\w+):\s*"?(#[0-9a-fA-F]{6,8})"?', m.group(1)))
    return out

# roles that render as TEXT on the page background, so AA applies
TEXT_ROLES = {
    "darkgray":  "body text",
    "dark":      "headings, icons",
    "secondary": "LINKS, current graph node",
    "tertiary":  "link hover, visited nodes",
}

def audit():
    pal = parse_palette()
    if not pal:
        sys.exit("could not parse colors from quartz.config.yaml")
    worst = []
    for mode, cols in pal.items():
        bg = cols.get("light")
        print(f"\n\033[1m{mode}\033[0m  (page background {bg})")
        print(f"  {'role':11} {'hex':9} {'vs bg':>8}  {'verdict':16} what it controls")
        print("  " + "-" * 74)
        for role, desc in TEXT_ROLES.items():
            c = cols.get(role)
            if not c: continue
            r = ratio(c, bg)
            g = grade(r)
            mark = "\033[32m" if r >= 4.5 else ("\033[33m" if r >= 3.0 else "\033[31m")
            print(f"  {role:11} {c:9} {r:>6.2f}:1  {mark}{g:16}\033[0m {desc}")
            if r < 4.5: worst.append((mode, role, c, r))
    if worst:
        print("\n\033[31mBelow AA:\033[0m")
        for mode, role, c, r in worst:
            print(f"  {mode}.{role} = {c} at {r:.2f}:1 — run: "
                  f"python3 scripts/check-contrast.py '{c}'")
    else:
        print("\n\033[32mAll text roles pass WCAG AA.\033[0m")

def suggest(hexc):
    """Show how a color must change to clear AA on each background."""
    pal = parse_palette()
    print(f"\nMaking \033[1m{hexc}\033[0m clear AA 4.5:1\n")
    for mode, cols in pal.items():
        bg = cols.get("light")
        base = ratio(hexc, bg)
        print(f"\033[1m{mode}\033[0m (bg {bg}) — as given: {base:.2f}:1  {grade(base)}")
        if base >= 4.5:
            print("   already passes, use as-is\n"); continue
        h = hexc.lstrip("#")
        r, g, b = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
        hh, ll, ss = colorsys.rgb_to_hls(r, g, b)
        for label, hue_shift, sat in (("keep hue", 0.0, ss),
                                      ("keep hue, full saturation", 0.0, 1.0),
                                      ("nudge toward orange", -0.02, min(1.0, ss * 1.1))):
            found = None
            for i in range(1000):
                l = ll * (1 - i / 1000)
                rr, gg, bb = colorsys.hls_to_rgb((hh + hue_shift) % 1.0, l, sat)
                cand = "#%02x%02x%02x" % (round(rr*255), round(gg*255), round(bb*255))
                if ratio(cand, bg) >= 4.5:
                    found = cand; break
            if found:
                print(f"   {label:28} {found}   {ratio(found, bg):.2f}:1")
        print()

if __name__ == "__main__":
    if len(sys.argv) > 1: suggest(sys.argv[1])
    else: audit()
