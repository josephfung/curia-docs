"""Curia's multi-agent architecture. Used on agents/multi-agent-architecture.

People reach the Coordinator; it delegates to specialists inside the Bullpen; agents
ask the execution layer to run tools; every agent shares the knowledge graph, the
OKF documents and the audit log.
"""
from kit import *  # noqa: F403

OUT = "multi-agent-architecture.svg"
W, H = 1100, 690
DESC = (
    'You and your contacts reach Curia over its channels, and only the Coordinator talks to people. '
    'Inside the Bullpen, the Coordinator delegates to specialists: Calendar, Contacts, CEO Inbox, '
    'Research analyst, Meeting debrief, Diagnostics, Setup guide, and any you add. Agents ask the '
    'execution layer to run tools, sending tool.invoke and getting tool.result back; it checks each '
    "call against the tool's manifest and the autonomy score. It holds about 150 tools: Curia's "
    'bundles such as calendar, email, contacts, memory and web, plus Google Workspace tools from an '
    'MCP server. Every agent shares one knowledge graph and one store of OKF documents, and every '
    'delegation and tool call is in the audit log.'
)


def build(square=False):
    s = Svg(W, H, "Curia's multi-agent architecture", DESC, square=square)
    text, rect, path, label = s.text, s.rect, s.path, s.label

    def chip(x, y, wd, title, mcp=False):
        """A bundle chip in monospace: teal for Curia's tools, sand for MCP tools."""
        if mcp:
            rect(x, y, wd, 28, fill=SAND, stroke=SAND_LINE, rx=6)
            tc = INK
        else:
            rect(x, y, wd, 28, fill=TEAL, stroke=TEAL, rx=6)
            tc = LIGHT
        text(x + wd / 2, y + 18.5, title, size=12, fill=tc, family=MONO, weight="600")

    # Legend (top left)
    for i, (kind, lbl) in enumerate([("curia", "Curia's tools"), ("mcp", "Tools from an MCP server"), ("own", "Add your own")]):
        y = 26 + i * 24
        if kind == "curia":
            rect(30, y, 28, 16, fill=TEAL, stroke=TEAL, rx=4)
        elif kind == "mcp":
            rect(30, y, 28, 16, fill=SAND, stroke=SAND_LINE, rx=4)
        else:
            rect(30, y, 28, 16, fill="none", stroke=TEAL, sw=1.3, rx=4, dash="5 4")
        text(66, y + 12.5, lbl, size=12, anchor="start")

    # People
    CXM = W / 2
    label(CXM, 30, "PEOPLE")
    for t, sub, x in [("You", "the principal", CXM - 180), ("Your contacts", "anyone Curia deals with", CXM + 20)]:
        rect(x, 42, 160, 46, fill="none", stroke=MUTE, sw=1.2, rx=23)
        text(x + 80, 62, t, size=14, family=SERIF, weight="500")
        text(x + 80, 77, sub, size=10.5, fill=MUTE)
    path(f"M{CXM - 100},88 C{CXM - 100},112 {CXM},104 {CXM},124", arrow=False)
    path(f"M{CXM + 100},88 C{CXM + 100},112 {CXM},104 {CXM},124", arrow=False)

    # Bullpen region
    BX, BY, BW, BH = 30, 120, W - 60, 300
    rect(BX, BY + 10, BW, BH, fill=SERVER, stroke=TEAL, sw=1.5, rx=14)
    label(BX + 22, BY + 36, "THE BULLPEN", fill=TEAL, anchor="start")

    text(CXM + 14, 152, "email · Signal · Slack · SMS · phone app · voice", size=11, fill=MUTE, anchor="start")

    path(f"M{CXM},124 L{CXM},176")

    # Coordinator
    CW_, CH_ = 280, 80
    cx0 = CXM - CW_ / 2
    rect(cx0, 180, CW_, CH_, fill=TEAL, stroke=TEAL, rx=10)
    text(CXM, 207, "Coordinator", size=19, fill=LIGHT, family=SERIF, weight="500")
    text(CXM, 227, "plans · delegates · replies", size=12, fill=LIGHT_SUB)
    text(CXM, 246, "the only agent that talks to people", size=11, fill=LIGHT_SUB, italic=True)

    # Specialists
    specs = [("Calendar", "scheduling, invites"), ("Contacts", "people, relationships"), ("CEO Inbox", "your inbox"),
             ("Research analyst", "web research"), ("Meeting debrief", "after your meetings"),
             ("Diagnostics", "“why did that happen?”"), ("Setup guide", "helps set Curia up"), ("Your own", "one YAML file each")]
    SW_, GAP = 116, 10
    total = len(specs) * SW_ + (len(specs) - 1) * GAP
    sx0 = CXM - total / 2
    SY_ = 306
    centers = [sx0 + i * (SW_ + GAP) + SW_ / 2 for i in range(len(specs))]
    path(f"M{CXM},{180 + CH_} L{CXM},284", arrow=False)
    path(f"M{centers[0]},284 L{centers[-1]},284", arrow=False)
    for i, (t, sub) in enumerate(specs):
        x = sx0 + i * (SW_ + GAP)
        path(f"M{centers[i]},284 L{centers[i]},{SY_ - 4}")
        own = t == "Your own"
        if own:
            rect(x, SY_, SW_, 66, fill="none", stroke=TEAL, sw=1.3, dash="6 5")
        else:
            rect(x, SY_, SW_, 66)
        text(x + SW_ / 2, SY_ + 29, t, size=14, family=SERIF, weight="500", fill=TEAL if own else INK)
        text(x + SW_ / 2, SY_ + 47, sub, size=10.5, fill=MUTE)
    text(CXM, BY + BH - 6, "Agents delegate, hand off and escalate here. Every exchange is logged, and each agent can use only the skills it is given.",
         size=11.5, fill=MUTE, italic=True)

    # Execution layer
    EY = 490
    EX, EW, EH = 30, 720, 170
    path(f"M{CXM - 175},{BY + BH + 10} L{CXM - 175},{EY - 4}")
    text(CXM - 185, 466, "tool.invoke", size=11, fill=MUTE, anchor="end", family=MONO)
    path(f"M{CXM - 135},{EY} L{CXM - 135},{BY + BH + 14}")
    text(CXM - 125, 466, "tool.result", size=11, fill=MUTE, anchor="start", family=MONO)
    rect(EX, EY, EW, EH, fill=CARD, stroke=LINE, rx=14)
    label(EX + 22, EY + 28, "EXECUTION LAYER", fill=TEAL, anchor="start")
    text(EX + EW - 20, EY + 28, "checks every call against the tool's manifest and the autonomy score", size=11.5, fill=MUTE, anchor="end")
    row1 = ["calendar", "email", "contacts", "memory", "web"]
    row2 = ["secrets", "scheduler", "tasks"]
    for i, t in enumerate(row1):
        chip(EX + 22 + i * 132, EY + 46, 120, t)
    for i, t in enumerate(row2):
        chip(EX + 22 + i * 132, EY + 84, 120, t)
    chip(EX + 22 + 3 * 132, EY + 84, 252, "google-workspace · MCP", mcp=True)
    text(EX + 22, EY + 140, "About 150 tools in all, grouped in skill bundles. Agents only ask: the execution layer is what acts.",
         size=11.5, fill=MUTE, italic=True, anchor="start")

    # Shared by every agent
    RX, RW = 780, 290
    label(RX + RW / 2, EY - 2, "SHARED BY EVERY AGENT")
    path(f"M{RX + RW / 2},{BY + BH + 10} L{RX + RW / 2},{EY - 18}", arrow=False)
    for i, (t, sub, dark) in enumerate([("Knowledge graph", "people, facts and relationships", True),
                                        ("OKF documents", "projects, meetings, shared notes", True),
                                        ("Audit log", "every delegation and every tool call", False)]):
        y = EY + 8 + i * 54
        if dark:
            rect(RX, y, RW, 46, fill=DARK, stroke=DARK, rx=10)
        else:
            rect(RX, y, RW, 46)
        text(RX + RW / 2, y + 20, t, size=15, fill=LIGHT if dark else INK, family=SERIF, weight="500")
        text(RX + RW / 2, y + 36, sub, size=10.5, fill="#C9C4B8" if dark else MUTE)

    return s.render()
