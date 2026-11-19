"""Shared palette and shapes for the docs diagrams.

The look follows the "Where your data goes" diagram on meetcuria.com/governance
(curia-website, src/components/DataFlowDiagram.jsx): a cream background, cream
cards, a teal region for the main subject, small-caps group labels, and dashed
outlines for anything outside it. Every diagram draws its own background, so it
reads the same in the docs site's light and dark themes.

Fonts are named, not embedded. The SVGs load as <img>, so a viewer without Lora
or Inter falls back to Georgia and the system sans.
"""
from xml.sax.saxutils import escape

# Palette. Keep in step with the website's governance diagram.
TEAL = "#265058"        # primary: arrows, regions, Curia's own code
INK = "#1F1F1F"         # body text
MUTE = "#6E6A62"        # secondary text, notes, group labels
ACCENT = "#8A3B2E"      # warnings and "what happens if not"
CARD = "#FFFDF8"        # card fill
LINE = "rgba(31,31,31,0.18)"  # card outline
DARK = "#1F2622"        # emphasis fill (data stores, "back this up")
BG = "#ECE5D6"          # diagram background
SERVER = "#E4ECE8"      # tinted region (a server, the Bullpen)
SAND = "#F1E8D6"        # chip fill (open-source parts, components)
SAND_LINE = "#CDBE9F"   # chip outline
LIGHT = "#F4EFE6"       # text on teal or dark
LIGHT_SUB = "#C9D8D4"   # secondary text on teal

SERIF = "Lora, Georgia, 'Times New Roman', serif"
SANS = "Inter, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"


class Svg:
    """An SVG under construction. Draw with the methods, then call render().

    square=True pads the viewBox to a square. That is only for previews:
    macOS Quick Look crops thumbnails to a square, and a padded canvas shows
    the whole diagram. Never write a square render to assets/.
    """

    def __init__(self, w, h, title, desc, square=False):
        self.w, self.h = w, h
        vh = w if square else h
        self.out = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {vh}" width="{w}" height="{vh}" role="img" aria-labelledby="t d">',
            f'<title id="t">{escape(title)}</title>',
            f'<desc id="d">{escape(desc)}</desc>',
            '<defs>'
            f'<marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,1 L9,5 L0,9 z" fill="{TEAL}"/></marker>'
            f'<marker id="arra" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,1 L9,5 L0,9 z" fill="{ACCENT}"/></marker>'
            '</defs>',
        ]
        self.rect(0, 0, w, h, fill=BG, stroke="none", rx=16)

    # --- primitives -------------------------------------------------------

    def text(self, x, y, s, size=12, fill=INK, anchor="middle", family=SANS, weight=None, italic=False, spacing=None):
        a = [f'x="{x}"', f'y="{y}"', f'font-size="{size}"', f'fill="{fill}"', f'text-anchor="{anchor}"', f'font-family="{family}"']
        if weight:
            a.append(f'font-weight="{weight}"')
        if italic:
            a.append('font-style="italic"')
        if spacing:
            a.append(f'letter-spacing="{spacing}"')
        self.out.append(f'<text {" ".join(a)}>{escape(s)}</text>')

    def rect(self, x, y, wd, ht, fill=CARD, stroke=LINE, sw=1, rx=8, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.out.append(f'<rect x="{x}" y="{y}" width="{wd}" height="{ht}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def path(self, d, arrow=True, color=TEAL, dash=None):
        """A 1.5px line. arrow=True puts an arrowhead at the end, in the line's colour (teal or accent)."""
        m = f' marker-end="url(#{"arra" if color == ACCENT else "arr"})"' if arrow else ""
        da = f' stroke-dasharray="{dash}"' if dash else ""
        self.out.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="1.5"{da}{m}/>')

    def circle(self, cx, cy, r, fill=TEAL, stroke=None):
        s = f' stroke="{stroke}" stroke-width="1.2"' if stroke else ""
        self.out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"{s}/>')

    def line(self, x1, y1, x2, y2, stroke=LINE):
        self.out.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="1"/>')

    # --- shapes -----------------------------------------------------------

    def label(self, x, y, s, fill=MUTE, anchor="middle"):
        """A small-caps group label, e.g. "YOUR SERVER". Pass the text in capitals."""
        self.text(x, y, s, size=11.5, fill=fill, anchor=anchor, weight="700", spacing="0.12em")

    def num(self, cx, cy, n):
        """A numbered step badge."""
        self.circle(cx, cy, 9)
        self.text(cx, cy + 4, str(n), size=11, fill=LIGHT, weight="700")

    def chip(self, x, y, wd, title, kind="sand", ht=26, size=12, family=SANS):
        """A one-line component chip. kind="teal" for Curia's own code, "sand" otherwise."""
        if kind == "teal":
            self.rect(x, y, wd, ht, fill=TEAL, stroke=TEAL, rx=6)
            tc = LIGHT
        else:
            self.rect(x, y, wd, ht, fill=SAND, stroke=SAND_LINE, rx=6)
            tc = INK
        self.text(x + wd / 2, y + ht / 2 + size * 0.36, title, size=size, fill=tc, weight="600", family=family)

    def pill(self, x, y, wd, title, sub=None, ht=46):
        """A hollow rounded box: a person, or a person's device."""
        self.rect(x, y, wd, ht, fill="none", stroke=MUTE, sw=1.2, rx=ht / 2)
        if sub:
            self.text(x + wd / 2, y + 20, title, size=14, family=SERIF, weight="500")
            self.text(x + wd / 2, y + 35, sub, size=10.5, fill=MUTE)
        else:
            self.text(x + wd / 2, y + ht / 2 + 5, title, size=14, family=SERIF, weight="500")

    def ext(self, x, y, wd, title, sub=None, ht=40, faint=False):
        """A dashed box for something outside the main subject (an outside service)."""
        self.rect(x, y, wd, ht, fill="none", stroke=MUTE if faint else TEAL, sw=1.3, dash="6 5")
        tc = MUTE if faint else TEAL
        if sub:
            self.text(x + wd / 2, y + 17, title, size=13, fill=tc, family=SERIF, weight="500")
            self.text(x + wd / 2, y + 31, sub, size=10.5, fill=MUTE)
        else:
            self.text(x + wd / 2, y + ht / 2 + 5, title, size=13, fill=tc, family=SERIF, weight="500")

    def render(self):
        return "\n".join(self.out + ["</svg>"]) + "\n"
