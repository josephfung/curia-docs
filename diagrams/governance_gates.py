"""Curia's five governance gates. Used on core-concepts/layers-model.

The gates in order, what each checks, and (in the accent colour) what happens
when a message doesn't pass.
"""
from kit import *  # noqa: F403

OUT = "governance-gates.svg"

W, H = 1100, 448


def build(square=False):
    s = Svg(W, H, "Curia's five governance gates",
            "A message passes five gates in order before Curia acts or replies. 1, channel trust: how strong the channel's proof "
            "of identity is; a weak channel starts with lower trust. 2, dispatch policy: trust score, rate limits and an injection "
            "scan; an unknown sender gets read-only handling and a flood is dropped and logged. 3, agent autonomy: the autonomy band "
            "and a review of each send; if the band doesn't allow it, Curia asks you first. 4, tool action risk: the score must "
            "meet the tool's floor (none 0, low 60, medium 70, high 80, critical 90); if not, the call is blocked and an approval "
            "request is filed. 5, outbound safety: PII redaction, content rules and a leak check; unsafe content is redacted or held. "
            "A message must pass every gate to become an action.",
            square=square)

    GW, GG, X0 = 188, 24, 32
    GY, GH = 104, 222
    xs = [X0 + i * (GW + GG) for i in range(5)]
    gates = [
        ("Channel trust", ["How strong is the channel's", "proof of who's writing?"],
         ["Signal, CLI: high", "HTTP API: medium", "Email: low"], ["Starts with lower", "trust, and goes on"]),
        ("Dispatch policy", ["Who sent it, and is it", "safe to handle?"],
         ["Trust score", "Rate limits", "Injection scan"], ["Unknown sender: read-only.", "Flood: dropped and logged."]),
        ("Agent autonomy", ["What may Curia do on", "its own right now?"],
         ["Autonomy band", "Review of each send"], ["Curia asks", "you first"]),
        ("Tool action risk", ["Does the score meet", "this tool's floor?"],
         ["none 0 · low 60", "medium 70 · high 80", "critical 90"], ["Blocked, and an approval", "request is filed"]),
        ("Outbound safety", ["Is the reply safe", "to send?"],
         ["PII redaction", "Content rules", "Leak check"], ["Redacted,", "or held"]),
    ]
    for i, (x, (title, q, chips, fail)) in enumerate(zip(xs, gates)):
        s.rect(x, GY, GW, GH, rx=10)
        s.num(x + 24, GY + 27, i + 1)
        s.text(x + 40, GY + 32, title, size=15.5, family=SERIF, weight="500", anchor="start")
        s.text(x + GW / 2, GY + 60, q[0], size=11.5, fill=MUTE, italic=True)
        s.text(x + GW / 2, GY + 76, q[1], size=11.5, fill=MUTE, italic=True)
        for j, c in enumerate(chips):
            s.chip(x + 14, GY + 96 + j * 34, GW - 28, c, size=11.5 if i == 3 else 12, family=MONO if i == 3 else SANS, ht=28)
        # what happens if it doesn't pass
        fy = GY + GH + 34
        s.path(f"M{x + GW / 2},{GY + GH} L{x + GW / 2},{fy - 4}", color=ACCENT)
        s.rect(x, fy, GW, 62, fill="none", stroke=ACCENT, sw=1.2, dash="5 4", rx=8)
        s.text(x + GW / 2, fy + 26, fail[0], size=12, fill=ACCENT)
        s.text(x + GW / 2, fy + 43, fail[1], size=12, fill=ACCENT)
        if i < 4:
            s.path(f"M{x + GW},{GY + GH / 2} L{x + GW + GG - 4},{GY + GH / 2}")
    s.text(xs[0] - 6, GY + GH + 22, "if it doesn't pass", size=10.5, fill=ACCENT, italic=True, anchor="start")

    # in and out
    s.pill(xs[0], 20, GW, "A message arrives")
    s.path(f"M{xs[0] + GW / 2},66 L{xs[0] + GW / 2},{GY - 4}")
    s.pill(xs[4], 20, GW, "Curia acts or replies")
    s.path(f"M{xs[4] + GW / 2},{GY} L{xs[4] + GW / 2},70")
    s.text(W / 2, 50, "A message must pass every gate to become an action. No single gate is “the security layer”.",
           size=12, fill=MUTE, italic=True)

    return s.render()
