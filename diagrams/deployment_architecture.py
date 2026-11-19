"""What a Curia install deploys. Used on get-started/deployment.

Columns: what connects in (left), the server and its containers (middle), outside
services (right). Inside each container, chips show what runs there: teal for
Curia's code, sand for open-source software Curia ships.
"""
from kit import *  # noqa: F403

OUT = "deployment-architecture.svg"
W, H = 1180, 790
HDR = 14  # extra container header height for the image-name line
DESC = (
    'One server runs six containers: caddy (HTTPS), livekit (calls), curia (the runtime, console and '
    'phone app, the Google Workspace MCP server and the embedding model), postgres, speech and '
    "browser. Only Caddy's ports 80 and 443 and LiveKit's media ports 7881 and 7882 are open to the "
    'internet. The console, the phone app and Telnyx SMS webhooks connect in; email, Slack and Signal'
    ' connect out. Curia calls an AI model provider, Nylas, Google Workspace, Slack, Tavily and Web '
    'Push; the browser reaches the open web. Only the pgdata volume needs backing up. signal-cli, '
    "custom agents and skills, a VPN or proxy for the browser's traffic and single sign-on are not "
    'deployed by the installer.'
)


def build(square=False):
    s = Svg(W, H, "What a Curia install deploys", DESC, square=square)
    text, rect, path, label, ext = s.text, s.rect, s.path, s.label, s.ext

    def chip(x, y, wd, title, sub=None, curia=False, ht=None):
        """A chip with an optional second line; teal (curia=True) for Curia's code."""
        ht = ht or (40 if sub else 26)
        if curia:
            rect(x, y, wd, ht, fill=TEAL, stroke=TEAL, rx=6)
            tc, sc = LIGHT, LIGHT_SUB
        else:
            rect(x, y, wd, ht, fill=SAND, stroke=SAND_LINE, rx=6)
            tc, sc = INK, MUTE
        cx = x + wd / 2
        if sub:
            text(cx, y + 17, title, size=12.5, fill=tc, weight="600")
            text(cx, y + 31, sub, size=10.5, fill=sc)
        else:
            text(cx, y + 17, title, size=12, fill=tc, weight="600")

    def container(x, y, wd, ht, name, image):
        rect(x, y, wd, ht, fill=CARD, stroke=LINE, rx=10)
        text(x + 12, y + 22, name, size=16, family=SERIF, anchor="start", weight="500")
        text(x + 12, y + 37, image, size=10, fill=MUTE, anchor="start", family=MONO)

    def note(x, y, txt):
        text(x, y, txt, size=10.5, fill=MUTE, italic=True)

    def badge(x, y, txt, wd):
        rect(x - wd / 2, y - 11, wd, 22, fill=TEAL, stroke=TEAL, rx=11)
        text(x, y + 4, txt, size=10.5, fill=LIGHT, family=MONO, weight="600")

    # ---- Legend -------------------------------------------------------------
    ly = 26
    lx = 28
    rect(lx, ly, 28, 16, fill=TEAL, stroke=TEAL, rx=4)
    text(lx + 36, ly + 12.5, "Curia's code", size=12, anchor="start", fill=INK)
    lx += 140
    rect(lx, ly, 28, 16, fill=SAND, stroke=SAND_LINE, rx=4)
    text(lx + 36, ly + 12.5, "Open-source software Curia ships", size=12, anchor="start", fill=INK)
    lx += 258
    text(lx, ly + 12.5, "curia-*", size=11, anchor="start", fill=MUTE, family=MONO)
    text(lx + 54, ly + 12.5, "image published with each Curia release", size=12, anchor="start", fill=INK)
    lx += 318
    rect(lx, ly, 28, 16, fill="none", stroke=TEAL, sw=1.3, rx=4, dash="5 4")
    text(lx + 36, ly + 12.5, "Outside your server", size=12, anchor="start", fill=INK)
    lx += 180
    rect(lx, ly, 28, 16, fill="none", stroke=MUTE, sw=1.2, rx=8)
    text(lx + 36, ly + 12.5, "A person's device", size=12, anchor="start", fill=INK)

    # ---- Server region --------------------------------------------------------
    SX, SY, SW, SH = 280, 96, 664, 584
    label(SX + 20, SY - 12, "YOUR SERVER", fill=TEAL, anchor="start")
    text(SX + SW - 16, SY - 12, "4 vCPU · 8 GB RAM · Docker Compose", size=11.5, fill=MUTE, anchor="end")
    rect(SX, SY, SW, SH, fill=SERVER, stroke=TEAL, sw=1.5, rx=14)

    # Left column: caddy + livekit
    LX, LW = SX + 26, 172
    CAD_Y, CAD_H = 122, 134
    container(LX, CAD_Y, LW, CAD_H, "caddy", "caddy")
    chip(LX + 14, CAD_Y + 38 + HDR, LW - 28, "Caddy", "HTTPS reverse proxy")
    note(LX + LW / 2, CAD_Y + 114, "certificates: Let's Encrypt")

    LK_Y, LK_H = 344, 134
    container(LX, LK_Y, LW, LK_H, "livekit", "livekit-server")
    chip(LX + 14, LK_Y + 38 + HDR, LW - 28, "LiveKit", "real-time call server")
    note(LX + LW / 2, LK_Y + 114, "audio over WebRTC")

    # Curia
    CX, CY, CW, CH = LX + LW + 24, 122, 420, 180
    container(CX, CY, CW, CH, "curia", "curia")
    cw2 = (CW - 28 - 12) / 2
    chip(CX + 14, CY + 38 + HDR, cw2, "Curia runtime", "agents · channels · scheduler", curia=True)
    chip(CX + 14 + cw2 + 12, CY + 38 + HDR, cw2, "Console & phone app", "served on :3000", curia=True)
    chip(CX + 14, CY + 86 + HDR, cw2, "workspace-mcp", "Google Workspace MCP server")
    chip(CX + 14 + cw2 + 12, CY + 86 + HDR, cw2, "Embedding model", "all-MiniLM-L6-v2, in-process")
    note(CX + CW / 2, CY + 162, "holds the vault key: the only container that can read your secrets")

    # Row 2: postgres, speech, browser
    RY, RH = 344, 210
    bw = (CW - 2 * 14) / 3
    xs = [CX, CX + bw + 14, CX + 2 * (bw + 14)]
    container(xs[0], RY, bw, RH, "postgres", "curia-postgres")
    for i, t in enumerate(["PostgreSQL 16", "pgvector", "pgAudit"]):
        chip(xs[0] + 12, RY + 38 + HDR + i * 32, bw - 24, t)
    note(xs[0] + bw / 2, RY + 168, "memory, vault, audit log")
    note(xs[0] + bw / 2, RY + 184, ":5432 on loopback only")

    container(xs[1], RY, bw, RH, "speech", "curia-speech")
    chip(xs[1] + 12, RY + 38 + HDR, bw - 24, "Speech service", curia=True)
    for i, t in enumerate(["Parakeet STT", "Pocket TTS", "Silero VAD"]):
        chip(xs[1] + 12, RY + 70 + HDR + i * 32, bw - 24, t)
    note(xs[1] + bw / 2, RY + 198, "no internet access")

    container(xs[2], RY, bw, RH, "browser", "curia-browser")
    chip(xs[2] + 12, RY + 38 + HDR, bw - 24, "Chromium", "headful, on Xvfb")
    chip(xs[2] + 12, RY + 86 + HDR, bw - 24, "Egress guard", "no private addresses", curia=True)
    note(xs[2] + bw / 2, RY + 168, "own network:")
    note(xs[2] + bw / 2, RY + 184, "no secrets, no database")

    # Internal connections
    path(f"M{LX + LW},{CAD_Y + 67} L{CX - 4},{CAD_Y + 67}")
    path(f"M{LX + LW / 2},{CAD_Y + CAD_H} L{LX + LW / 2},{LK_Y - 4}")
    text(LX + LW / 2 + 8, (CAD_Y + CAD_H + LK_Y) / 2 + 4, "/rtc", size=10.5, fill=MUTE, anchor="start", family=MONO)
    # curia -> livekit (voice agent joins the call)
    path(f"M{CX},{CY + 162} L{(LX + LW + CX) / 2},{CY + 162} L{(LX + LW + CX) / 2},{LK_Y + 67} L{LX + LW + 4},{LK_Y + 67}")
    for x, lab in zip(xs, ["SQL", "WebSocket", "DevTools"]):
        mx = x + bw / 2
        path(f"M{mx},{CY + CH} L{mx},{RY - 4}")
        text(mx + 7, (CY + CH + RY) / 2 + 4, lab, size=10.5, fill=MUTE, anchor="start")

    # Volumes
    VY = 598
    label(LX, VY - 8, "VOLUMES", anchor="start")
    vx = LX
    vols = [("pgdata · back this up", 150, True), ("speech models", 102, False), ("browser profile", 106, False),
            ("Google tokens", 100, False), ("Caddy certificates", 120, False)]
    for name, vw, keep in vols:
        if keep:
            rect(vx, VY, vw, 28, fill=DARK, stroke=DARK, rx=14)
            text(vx + vw / 2, VY + 18.5, name, size=11, fill=LIGHT, weight="600")
        else:
            rect(vx, VY, vw, 28, fill=CARD, stroke=LINE, rx=14)
            text(vx + vw / 2, VY + 18.5, name, size=11, fill=INK)
        vx += vw + 10
    note(SX + SW / 2, VY + 52, "Only pgdata holds anything you can't recreate. The rest come back by re-downloading or signing in again.")

    # ---- People (left) --------------------------------------------------------
    PX, PW = 24, 150
    label(PX + PW / 2, SY - 12, "CONNECTS IN")
    CAD_MID, LK_MID = CAD_Y + 67, LK_Y + 67
    BX = (PX + PW + SX) / 2  # port badges sit in the gap, outside the server
    for t, s_, y in [("Console", "web browser", CAD_MID - 23), ("Phone app", "installed PWA", (CAD_MID + LK_MID) / 2 - 23)]:
        rect(PX, y, PW, 46, fill="none", stroke=MUTE, sw=1.2, rx=23)
        text(PX + PW / 2, y + 20, t, size=14, family=SERIF, weight="500")
        text(PX + PW / 2, y + 35, s_, size=10.5, fill=MUTE)
    PH = (CAD_MID + LK_MID) / 2
    path(f"M{PX + PW},{CAD_MID} L{BX - 37},{CAD_MID}", arrow=False)
    TY = SY + 6
    ext(PX, TY, PW, "Telnyx", "SMS webhooks", ht=40)
    path(f"M{PX + PW},{TY + 20} C{PX + PW + 30},{TY + 20} {PX + PW + 10},{CAD_MID} {BX - 37},{CAD_MID}", arrow=False)
    text(PX + PW / 2, LK_MID + 70, "Email, Slack and Signal", size=10.5, fill=MUTE, italic=True)
    text(PX + PW / 2, LK_MID + 85, "connect out instead:", size=10.5, fill=MUTE, italic=True)
    text(PX + PW / 2, LK_MID + 100, "no open port needed", size=10.5, fill=MUTE, italic=True)
    path(f"M{PX + PW},{PH} C{PX + PW + 30},{PH} {PX + PW + 10},{CAD_MID} {BX - 37},{CAD_MID}", arrow=False)
    path(f"M{PX + PW},{PH} C{PX + PW + 30},{PH} {PX + PW + 10},{LK_MID} {BX - 56},{LK_MID}", arrow=False)
    text(PX + PW - 2, PH + 62, "calls", size=10.5, fill=MUTE, anchor="end")
    badge(BX, CAD_MID, ":80 :443", 74)
    badge(BX, LK_MID, ":7881 :7882/udp", 112)
    path(f"M{BX + 37},{CAD_MID} L{LX - 4},{CAD_MID}")
    path(f"M{BX + 56},{LK_MID} L{LX - 4},{LK_MID}")
    text(BX, LK_MID + 28, "open on your firewall", size=10, fill=MUTE, italic=True)

    # ---- Outside services (right) --------------------------------------------
    EX, EW = SX + SW + 46, 180
    label(EX + EW / 2, SY - 12, "OUTSIDE SERVICES")
    svcs = [("AI model provider", "Anthropic, OpenRouter, …"), ("Nylas", "email and calendar"),
            ("Google Workspace", "Docs, Sheets, Drive"), ("Slack", "Socket Mode, outbound"),
            ("Tavily", "web search, keyless"), ("Web Push", "phone app notifications")]
    ys = []
    for i, (t, sub) in enumerate(svcs):
        y = 122 + i * 44
        ext(EX, y, EW, t, sub, ht=38)
        ys.append(y + 19)
    BUS = SX + SW + 24
    path(f"M{CX + CW},{CY + 70} L{BUS},{CY + 70}", arrow=False)
    path(f"M{BUS},{ys[0]} L{BUS},{ys[-1]}", arrow=False)
    for y in ys:
        path(f"M{BUS},{y} L{EX - 4},{y}")
    ext(EX, RY + 66, EW, "The open web", "pages the browser visits")
    path(f"M{xs[2] + bw},{RY + 86} L{EX - 4},{RY + 86}")
    ext(EX, RY + 124, EW, "Deepgram · Cartesia", "optional cloud speech", faint=True)
    text(EX + EW / 2, RY + 182, "instead of local speech", size=10.5, fill=MUTE, italic=True)

    # ---- Not deployed --------------------------------------------------------
    NY = SY + SH + 26
    rect(14.5, NY, W - 29, 56, fill="none", stroke=LINE, dash="4 4")
    text(W / 2, NY + 23, "Not deployed by the installer", size=13, fill=INK, weight="700")
    text(W / 2, NY + 42, "signal-cli for Signal  ·  your own agents and skills  ·  a VPN or proxy for the browser's traffic  ·  "
         "single sign-on in front of the console  ·  backups of pgdata", size=12, fill=MUTE)

    return s.render()
