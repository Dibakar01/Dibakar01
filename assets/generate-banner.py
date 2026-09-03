#!/usr/bin/env python3
"""Build the light/dark banner pair, and the buddy mark they carry.

Every file here comes from this one source, so nothing can drift apart.
Stdlib only. Run it, commit what it writes:  python3 assets/generate-banner.py
"""

import pathlib
import xml.dom.minidom

W, H = 1200, 200
BAR = 8                          # accent rule down the left edge
PAD_L = 56                       # text starts here
PAD_R = 56                       # nothing may cross this far from the right
MARK = 96                        # the buddy mark, drawn square
GAP = 36                         # clear space between text and mark
BOX = W - PAD_L - PAD_R - MARK - GAP   # the container every text run must fit

ACCENT = "#d92819"               # Qalakaar red, read off qalakaar.com

THEMES = {
    "light": {"ground": "#ffffff", "ink": "#141413", "muted": "#6b6663"},
    "dark":  {"ground": "#0d1117", "ink": "#f0f6fc", "muted": "#9198a1"},
}

FONT = ('ui-sans-serif,-apple-system,BlinkMacSystemFont,"Segoe UI",'
        'Helvetica,Arial,sans-serif')

# (text, baseline y, size, weight, colour key)
RUNS = [
    ("Dibakar Upadhyaya",       92, 46, 700, "ink"),
    ("Chief Operating Officer, Qalakaar · artist", 132, 21, 400, "muted"),
]


def buddy(ox, oy, size):
    """The coding buddy: a German Shepherd, front on. Loyal, and there with you.

    Drawn in a 64x64 local space, in the same language as the sibling repos'
    marks: solid brand red, white cut-outs, no outlines.

    Getting here took several wrong animals, so save yourself the trip. A wide
    head with drop ears reads as a bear. A side profile with a pointed ear
    reads as a fox, which the sibling repo already owns, and one with a
    tapering snout reads as a bird. A full sitting body reads as a seal,
    because the straight foreleg and curved back are exactly a seal's line.

    Three things make this a shepherd rather than a fox or a cat. The ears are
    large and broad at the base, not needle points. The cheeks are full rather
    than tapering to a muzzle. And the mask narrows to a bridge between the
    eyes before widening over the muzzle, which is the breed's real signature
    and the part to keep if you edit anything.

    Nothing crosses the outer silhouette, so the white cut-outs stay white on
    any ground and the mark needs no per-theme variant.
    """
    s = size / 64
    return (
        f'<g transform="translate({ox} {oy}) scale({s:.5f})">'
        f'<g fill="{ACCENT}">'
        '<path d="M12 33 C11 21 13.5 8 18 4.5 C23.5 8.5 29.5 16 31.5 23.5 Z"/>'
        '<path d="M52 33 C53 21 50.5 8 46 4.5 C40.5 8.5 34.5 16 32.5 23.5 Z"/>'
        '<path d="M13 28 C13 40 17 49 24 55 C27 57.5 30 58.5 32 58.5 '
        'C34 58.5 37 57.5 40 55 C47 49 51 40 51 28 C47 20 40 17 32 17 '
        'C24 17 17 20 13 28 Z"/>'
        '</g>'
        f'<g fill="#ffffff">'
        '<path d="M18.5 27.5 C18 19.5 19 13 20.5 11 C23.5 14 26 18.5 27 23 Z"/>'
        '<path d="M45.5 27.5 C46 19.5 45 13 43.5 11 C40.5 14 38 18.5 37 23 Z"/>'
        '<path d="M29 27 C27 30 25 34 24 40 C23.5 48 27 54 32 57 '
        'C37 54 40.5 48 40 40 C39 34 37 30 35 27 Z"/>'
        '<ellipse cx="23.5" cy="31" rx="3.1" ry="2.2" transform="rotate(-20 23.5 31)"/>'
        '<ellipse cx="40.5" cy="31" rx="3.1" ry="2.2" transform="rotate(20 40.5 31)"/>'
        '</g>'
        f'<ellipse cx="32" cy="48" rx="3.6" ry="2.9" fill="{ACCENT}"/>'
        '</g>'
    )


def width_of(text, size, weight):
    """Estimated rendered width in px.

    ponytail: naive per-character metric, no font file is parsed. It runs a few
    percent wide of a real sans stack, which is the safe direction for an
    overflow guard. Swap in fontTools if this ever needs tight typesetting.
    """
    per = 0.58 if weight >= 700 else 0.54
    return len(text) * size * per


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build(theme):
    c = THEMES[theme]
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" role="img" '
        f'aria-label="Dibakar Upadhyaya. Chief Operating Officer at Qalakaar, and an artist.">',
        f'<rect width="{W}" height="{H}" fill="{c["ground"]}"/>',
        f'<rect width="{BAR}" height="{H}" fill="{ACCENT}"/>',
    ]
    for text, y, size, weight, key in RUNS:
        out.append(
            f'<text x="{PAD_L}" y="{y}" fill="{c[key]}" font-family=\'{FONT}\' '
            f'font-size="{size}" font-weight="{weight}">{esc(text)}</text>'
        )
    out.append(buddy(W - PAD_R - MARK, (H - MARK) / 2, MARK))
    out.append("</svg>")
    return "\n".join(out) + "\n"


def build_buddy():
    """The mark on its own, transparent, for use as an avatar."""
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128" '
        'viewBox="0 0 128 128" role="img" aria-label="A dog, the coding buddy">'
        + buddy(12, 12, 104) +
        '</svg>\n'
    )


def check():
    """The one runnable check. Fails loudly if anything here is broken."""
    # 1. Every run fits its container. The container is not the canvas: the
    #    buddy mark and the right padding are both carved out of it first.
    for text, _, size, weight, _ in RUNS:
        w = width_of(text, size, weight)
        assert w <= BOX, f"{text!r} needs {w:.0f}px, container is {BOX}px"
    # 2. Text and mark cannot collide.
    assert PAD_L + BOX + GAP <= W - PAD_R - MARK + 1e-9, "text box overruns the mark"
    # 3. The pair genuinely differs. A copy would silently defeat dark mode.
    assert build("light") != build("dark"), "light and dark are identical"
    # 4. Everything parses as XML.
    for theme in THEMES:
        xml.dom.minidom.parseString(build(theme))
    xml.dom.minidom.parseString(build_buddy())
    # 5. The banner and the standalone file carry the same mark, not two
    #    drawings that can drift. Compare the shapes with the placement
    #    transform stripped off.
    shapes = lambda g: g[g.index('>') + 1:]
    assert shapes(buddy(0, 0, 64)) == shapes(buddy(9, 9, 40)), \
        "mark geometry differs by placement"


if __name__ == "__main__":
    check()
    here = pathlib.Path(__file__).parent
    for theme in THEMES:
        (here / f"banner-{theme}.svg").write_text(build(theme), encoding="utf-8")
        print(f"wrote banner-{theme}.svg")
    (here / "buddy.svg").write_text(build_buddy(), encoding="utf-8")
    print("wrote buddy.svg")
    print("checks passed")
