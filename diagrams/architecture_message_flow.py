"""How a message flows through Curia. Used on core-concepts/architecture.

The four domain layers as columns, the seven numbered events of a round trip
(numbered to match the page's steps), the message bus and the system layer.
"""
from kit import *  # noqa: F403

OUT = "architecture-message-flow.svg"

W, H = 1100, 560


def build(square=False):
    s = Svg(W, H, "How a message flows through Curia",
            "A message arrives on a channel. 1: the channel layer publishes inbound.message. 2: the dispatch layer checks trust, "
            "rate limits and prompt injection, then publishes agent.task. 3: the agent layer (the Coordinator and specialists) "
            "reasons and publishes tool.invoke. 4: the execution layer checks permissions, runs the tool and publishes tool.result. "
            "5: the agent publishes agent.response. 6: dispatch applies PII redaction and publishes outbound.message. 7: the channel "
            "delivers the reply. Every arrow is a typed event on the message bus, and each layer may publish only its own event "
            "types. The system layer (audit logger, memory engine, scheduler, dream engine) may publish and read every event; the "
            "audit logger writes each event before anyone else receives it.",
            square=square)

    CW, G, X0 = 180, 107, 30
    CY, CH = 112, 222
    xs = [X0 + i * (CW + G) for i in range(4)]
    cols = [
        ("CHANNEL LAYER", "translates each platform", [("Email", "sand"), ("Signal", "sand"), ("Slack · SMS", "sand"), ("Console · voice", "sand")]),
        ("DISPATCH LAYER", "routes and enforces policy", [("Trust scoring", "sand"), ("Rate limits", "sand"), ("Injection scan", "sand"), ("PII redaction", "sand")]),
        ("AGENT LAYER", "reasons, then asks for tools", [("Coordinator", "teal"), ("Specialists", "sand")]),
        ("EXECUTION LAYER", "runs tools, checks permissions", [("Permission check", "sand"), ("Tool handlers", "sand"), ("MCP clients", "sand"), ("Output sanitizer", "sand")]),
    ]
    for x, (name, role, chips) in zip(xs, cols):
        s.rect(x, CY, CW, CH, rx=10)
        s.label(x + 16, CY + 26, name, fill=TEAL, anchor="start")
        s.text(x + 16, CY + 44, role, size=11, fill=MUTE, italic=True, anchor="start")
        for i, (t, k) in enumerate(chips):
            s.chip(x + 16, CY + 58 + i * 32, CW - 32, t, kind=k)
    s.text(xs[2] + CW / 2, CY + 140, "both read and write", size=10.5, fill=MUTE, italic=True)
    s.text(xs[2] + CW / 2, CY + 155, "the knowledge graph", size=10.5, fill=MUTE, italic=True)

    # Outside: someone on any channel
    ox = xs[0]
    s.pill(ox, 22, CW, "Someone writes", "on any channel")
    cin, cout = ox + CW / 2 - 34, ox + CW / 2 + 34
    s.path(f"M{cin},68 L{cin},{CY - 4}")
    s.path(f"M{cout},{CY} L{cout},72")
    s.num(cout + 18, 92, 7)
    s.text(cout + 32, 96, "the reply goes out", size=11, fill=MUTE, anchor="start")

    # Event arrows between columns
    YIN, YOUT = 172, 300
    inbound = [(1, "inbound.message"), (2, "agent.task"), (3, "tool.invoke")]
    outbound = [(6, "outbound.message"), (5, "agent.response"), (4, "tool.result")]
    for i in range(3):
        a, b = xs[i] + CW, xs[i + 1]
        mid = (a + b) / 2
        n, ev = inbound[i]
        s.path(f"M{a},{YIN} L{b - 4},{YIN}")
        s.num(mid, YIN - 30, n)
        s.text(mid, YIN - 9, ev, size=10, fill=INK, family=MONO)
        n, ev = outbound[i]
        s.path(f"M{b},{YOUT} L{a + 4},{YOUT}")
        s.num(mid, YOUT - 30, n)
        s.text(mid, YOUT - 9, ev, size=10, fill=INK, family=MONO)

    # Message bus
    BY = 368
    for x in xs:
        s.path(f"M{x + CW / 2},{CY + CH} L{x + CW / 2},{BY}", arrow=False)
    s.rect(X0, BY, W - 2 * X0, 36, fill=TEAL, stroke=TEAL, rx=8)
    s.text(X0 + 20, BY + 23, "MESSAGE BUS", size=11.5, fill=LIGHT, weight="700", anchor="start", spacing="0.12em")
    s.text(W - X0 - 20, BY + 23, "typed events, recorded in Postgres", size=12, fill=LIGHT_SUB, anchor="end")
    s.text(W / 2, BY + 58, "Every numbered arrow is an event on the bus. A layer may publish only its own event types: a channel can't invoke a tool.",
           size=11.5, fill=MUTE, italic=True)

    # System layer
    SY = 448
    for x in (X0 + 60, W - X0 - 60):
        s.path(f"M{x},{BY + 36} L{x},{SY}", arrow=False)
    s.rect(X0, SY, W - 2 * X0, 88, rx=10)
    s.label(X0 + 20, SY + 26, "SYSTEM LAYER", fill=TEAL, anchor="start")
    s.text(W - X0 - 20, SY + 26, "trusted: may publish and read every event type", size=11.5, fill=MUTE, anchor="end")
    cx = X0 + 20
    for t, wd in [("Audit logger · writes each event first", 290), ("Memory engine", 150), ("Scheduler", 130), ("Dream engine", 140)]:
        s.chip(cx, SY + 44, wd, t, ht=28)
        cx += wd + 12

    return s.render()
