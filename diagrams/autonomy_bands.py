"""The autonomy dial. Used on core-concepts/autonomy.

The five bands are drawn the same width on purpose: to scale, "below 60" would
take most of the bar. The numbers above the bar give the real ranges.
"""
from kit import *  # noqa: F403

OUT = "autonomy-bands.svg"

W, H = 1100, 430


def build(square=False):
    s = Svg(W, H, "The autonomy dial",
            "One score from 0 to 100 sets five bands. Restricted, below 60: proposes and drafts only, and takes no action with an "
            "external effect; only read tools run. Draft Only, 60 to 69: drafts and handles internal logistics in confirmed work, "
            "asks before anything is sent; low-risk tools such as memory and contacts run. Approval Required, 70 to 79, the default "
            "at 75: takes on work and coordinates, asks before speaking or committing for you; sends run. Spot-check, 80 to 89: "
            "speaks for you on routine matters, asks before committing you to dates, terms or introductions; calendar writes and "
            "commitments run. Full, 90 to 100: speaks and commits for you, asks first on payments, pricing, contracts and legal "
            "positions; critical tools run. At every band, an outsider steering Curia is held for you.",
            square=square)

    X0 = 40
    SEG = (W - 2 * X0) / 5
    BY, BH = 92, 62
    bands = [
        ("Restricted", "below 60", "#DCE6E2", INK, MUTE,
         ["proposes and", "drafts only"], ["anything with an", "external effect"], "none: reads, search"),
        ("Draft Only", "60–69", "#B8CCC6", INK, "#4B5A57",
         ["drafts, and internal", "logistics in confirmed work"], ["before anything is sent,", "and to take on new work"], "+ low: memory, contacts"),
        ("Approval Required", "70–79", "#7E9FA0", INK, "#2F3D3D",
         ["takes on work", "and coordinates"], ["before speaking or", "committing for you"], "+ medium: sends"),
        ("Spot-check", "80–89", "#3E6B71", LIGHT, LIGHT_SUB,
         ["routine replies and", "logistics, for you"], ["before committing you to", "dates, terms or intros"], "+ high: calendar, commitments"),
        ("Full", "90–100", TEAL, LIGHT, LIGHT_SUB,
         ["speaks and commits", "for you"], ["payments, pricing,", "contracts, legal positions"], "+ critical: money, irreversible"),
    ]
    for i, (name, rng, fill, tc, sc, own, ask, tools) in enumerate(bands):
        x = X0 + i * SEG
        s.rect(x + 1.5, BY, SEG - 3, BH, fill=fill, stroke=fill, rx=8)
        s.text(x + SEG / 2, BY + 28, name, size=15.5, fill=tc, family=SERIF, weight="500")
        s.text(x + SEG / 2, BY + 47, rng, size=11, fill=sc, family=MONO)
        cx = x + SEG / 2
        s.text(cx, 204, own[0], size=12, fill=INK)
        s.text(cx, 220, own[1], size=12, fill=INK)
        s.text(cx, 270, ask[0], size=12, fill=INK)
        s.text(cx, 286, ask[1], size=12, fill=INK)
        s.chip(x + 8, 330, SEG - 16, tools, ht=28, size=11.5)
        if i:
            s.line(x, 182, x, 296)

    # scale ticks
    for i, v in enumerate(["0", "60", "70", "80", "90", "100"]):
        s.text(X0 + i * SEG, BY - 8, v, size=11, fill=MUTE, family=MONO,
               anchor="start" if i == 0 else "end" if i == 5 else "middle")

    # default marker at 75
    mx = X0 + 2.5 * SEG
    s.out.append(f'<path d="M{mx - 7},{BY - 26} L{mx + 7},{BY - 26} L{mx},{BY - 17} z" fill="{ACCENT}"/>')
    s.text(mx, BY - 34, "Curia starts at 75", size=12, fill=ACCENT, weight="600")

    s.label(X0, 182, "ON ITS OWN", anchor="start")
    s.label(X0, 248, "ASKS YOU FIRST", anchor="start")
    s.label(X0, 320, "TOOLS IT MAY RUN · A HARD GATE", anchor="start")
    s.text(W / 2, 394, "At every band, a send an outsider seems to be steering is held for you, and your own instructions count as approval.",
           size=11.5, fill=MUTE, italic=True)

    return s.render()
