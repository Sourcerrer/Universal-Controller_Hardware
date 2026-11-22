#!/usr/bin/env python3
"""Generate the Universal Controller architecture diagram (3 SVG pages, A3 landscape)."""
import sys, textwrap, html, os, json

OUT = sys.argv[1]
W, H = 1680, 1188          # A3 landscape at 4 px per mm
FONT = "DejaVu Sans, Arial, sans-serif"
CW = 0.58                  # average glyph width in em

COL = {   # fill, stroke
    "mcu":   ("#dbe8ff", "#2f5fb3"),
    "radio": ("#ece0ff", "#6b3fb3"),
    "power": ("#ffe8cf", "#c46a00"),
    "io":    ("#dcf3e0", "#2e8540"),
    "sec":   ("#ffdcdc", "#b32f2f"),
    "mem":   ("#eceff3", "#5a6470"),
    "eth":   ("#d6f1f5", "#1f7f8c"),
    "conn":  ("#e4e4e4", "#3a3a3a"),
}
INK = "#1b1f24"
REV = "Draft C.11 · 2026-11-22 · PRD 0.5 · prices at 100 units"


def esc(s):
    return html.escape(s, quote=True)


def wrap(s, width_px, size):
    n = max(8, int(width_px / (size * CW)))
    return textwrap.wrap(s, n) or [""]


class Page:
    def __init__(self, title, subtitle):
        self.p = []
        self.p.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="420mm" height="297mm" '
                      f'viewBox="0 0 {W} {H}" font-family="{FONT}">')
        self.p.append('<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
                      'markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#33414f"/></marker></defs>')
        self.rect(0, 0, W, H, "#ffffff", "none", rx=0)
        self.rect(20, 20, W - 40, H - 40, "none", "#33414f", rx=0, sw=1.5)
        self.text(40, 58, title, 26, "bold")
        for k, ln in enumerate(wrap(subtitle, 1150, 12.5)[:2]):
            self.text(40, 80 + k * 16, ln, 12.5, fill="#4a5560")
        self.text(W - 40, 58, "Universal Controller", 16, "bold", "end")
        self.text(W - 40, 82, REV, 12, anchor="end", fill="#4a5560")

    def rect(self, x, y, w, h, fill, stroke, rx=6, sw=1.4, dash=False):
        d = ' stroke-dasharray="7 4"' if dash else ""
        self.p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" '
                      f'stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def text(self, x, y, s, size=12, weight="normal", anchor="start", fill=INK, italic=False):
        st = ' font-style="italic"' if italic else ""
        self.p.append(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" '
                      f'text-anchor="{anchor}" fill="{fill}"{st}>{esc(s)}</text>')

    def line(self, x1, y1, x2, y2, color="#33414f", sw=1.6, arrow=None, dash=False):
        m = ""
        if arrow in ("end", "both"):
            m += ' marker-end="url(#ar)"'
        if arrow in ("start", "both"):
            m += ' marker-start="url(#ar)"'
        d = ' stroke-dasharray="6 4"' if dash else ""
        self.p.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
                      f'stroke-width="{sw}"{m}{d}/>')

    def para(self, x, y, w, lines, size=11, lh=None, weight="normal", fill=INK, bullet=False):
        """Wrapped text; returns the y after the last line."""
        lh = lh or size * 1.32
        for s in lines:
            prefix = "• " if bullet else ""
            parts = wrap(s, w - (12 if bullet else 0), size)
            for i, ln in enumerate(parts):
                xx = x + (12 if bullet and i else 0)
                self.text(xx, y, (prefix if i == 0 else "") + ln, size, weight, fill=fill)
                y += lh
        return y

    def block_h(self, w, title, lines, size=10.5):
        n = sum(len(wrap(s, w - 16, size)) for s in lines)
        t = len(wrap(title, w - 16, 11.5))
        return 10 + t * 15 + n * size * 1.3 + 6

    def block(self, x, y, w, kind, title, lines, dash=False, size=10.5):
        fill, stroke = COL[kind]
        h = self.block_h(w, title, lines, size)
        self.rect(x, y, w, h, fill, stroke, dash=dash, sw=1.6 if not dash else 1.8)
        yy = y + 17
        for t in wrap(title, w - 16, 11.5):
            self.text(x + 8, yy, t, 11.5, "bold", fill=stroke)
            yy += 15
        yy -= 1
        for s in lines:
            for ln in wrap(s, w - 16, size):
                self.text(x + 8, yy, ln, size)
                yy += size * 1.3
        return y + h

    def save(self, name):
        self.p.append("</svg>")
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write("\n".join(self.p))


# ---------------------------------------------------------------- page 1
def page1():
    pg = Page("Hardware architecture — physical stack view",
              "Front view of the device on a DIN rail, each module shown with its cover removed to expose the electronics. "
              "Every module has its own enclosure, and works standalone on 5–32 V DC or USB-C 5 V. Each module has its own power stage; an optional plug-in battery + charger board per module. Not to scale.")
    TOP, BOT = 202, 1036

    def screws(x, y, w, groups):
        """groups: list of (label, n, dashed). Draws screw terminals and labels below."""
        n_tot = sum(g[1] for g in groups)
        gapw = 10 * (len(groups) - 1)
        pitch = min(20.0, (w - gapw) / n_tot)
        centres = []
        used = n_tot * pitch + gapw
        cx = x + (w - used) / 2
        for label, n, dash in groups:
            gw = n * pitch
            pg.rect(cx, y, gw, 24, "#5b6670" if not dash else "#ffffff", "#2b3138", rx=2, sw=1.2, dash=dash)
            for k in range(n):
                sx = cx + pitch * k + pitch / 2
                pg.p.append(f'<circle cx="{sx:.1f}" cy="{y + 12}" r="{pitch * 0.32:.1f}" fill="#d5d9dd" stroke="#2b3138" stroke-width="1"/>')
                pg.line(sx - pitch * 0.2, y + 12, sx + pitch * 0.2, y + 12, "#2b3138", 1.1)
            for li, ln in enumerate(label.split("\n")):
                pg.text(cx + gw / 2, y + 36 + li * 11, ln, 9, "bold", "middle", fill="#2b3138")
            centres.append(cx + gw / 2)
            cx += gw + 10
        return centres

    def sma(cx, label):
        pg.rect(cx - 7, TOP - 30, 14, 22, "#d4a017", "#8a6a00", rx=2, sw=1)
        pg.rect(cx - 10, TOP - 10, 20, 10, "#b8860b", "#8a6a00", rx=1, sw=1)
        pg.text(cx, TOP - 36, label, 9, "bold", "middle", fill="#8a6a00")

    def leds(x, y, items):
        for k, (lab, col) in enumerate(items):
            lx = x + k * 46
            pg.p.append(f'<circle cx="{lx + 5}" cy="{y}" r="4.5" fill="{col}" stroke="#333" stroke-width="0.8"/>')
            pg.text(lx + 13, y + 3.5, lab, 8.5, fill="#cfd8e2")

    def rj45(x, y, label, dash=False):
        pg.rect(x, y, 44, 36, "#2b3138" if not dash else "#ffffff", "#2b3138", rx=2, dash=dash)
        pg.rect(x + 10, y + 6, 24, 20, "#11161b" if not dash else "#ffffff", "#2b3138", rx=1, sw=1)
        pg.rect(x + 17, y + 26, 10, 5, "#11161b" if not dash else "#ffffff", "#2b3138", rx=0, sw=1)
        pg.text(x + 22, y + 48, label, 9, "bold", "middle", fill="#2b3138")

    def usbc(x, y, label):
        pg.rect(x, y + 10, 34, 13, "#c9ced3", "#2b3138", rx=6.5)
        pg.text(x + 17, y + 48, label, 9, "bold", "middle", fill="#2b3138")

    def sim(x, y, label):
        pg.rect(x, y + 12, 46, 9, "#11161b", "#2b3138", rx=1)
        pg.text(x + 23, y + 48, label, 9, "bold", "middle", fill="#2b3138")

    def switch(x, y, label):
        pg.rect(x, y + 6, 30, 22, "#c0392b", "#2b3138", rx=2)
        for k in range(2):
            pg.rect(x + 5 + k * 11, y + 10, 8, 14, "#ffffff", "#2b3138", rx=1, sw=0.8)
        pg.text(x + 15, y + 48, label, 9, "bold", "middle", fill="#2b3138")

    mods = [
        dict(key="base", name="FIELDBUS CONTROLLER (optional)", sub="90 mm · coordinator when fitted · Ethernet standard · 8 relays + 4 high-side outputs", w=400,
             top=[("DC IN\n5–32 V", 2, False), ("RS-485", 3, False), ("CAN-FD", 3, False)],
             bottom=[("AI1–4", 6, False), ("DI1–10 + COM", 11, False), ("HS 1–4 + 24V", 6, False), ("RELAY 1–8 NO/NC/C", 14, False)],
             leds=[("PWR", "#2ecc71"), ("RUN", "#3498db"), ("ERR", "#e74c3c"), ("BUS", "#f1c40f")],
             front=[("usbc", "USB-C service + 5 V power"), ("rj45", "RJ45 Ethernet")],
             sma=[],
             blocks=[
                 ("mcu", "Controller MCU — 100-pin", ["PIC32CK2051SG01100 TQFP100 (standard for now, owner 2026-11-19): Ethernet MAC, 2× CAN-FD, HSM + TrustZone",
                                            "Cortex-M33 120 MHz · HSM + TrustZone · Zephyr drivers to write (D-32)",
                                            "Alternative: STM32H573VIT6 LQFP100 (PSA L3, Zephyr-ready; own layout)"], False),
                 ("sec", "Security — inside the MCU", ["HSM + TrustZone: unique key, key storage, crypto, secure boot; no PSA certificate (D-32)"], False),
                 ("io", "Field IO — 28 channels", ["6 AI: 0–10 V / 4–20 mA / PT1000 · 10 DI 24 V (2 pulse) · 8 relays 10 A changeover (AC / DC, 5 kV, replaceable fuse each) · 4 fast 24 V high-side with current monitoring",
                                                              "LED per IO · watchdog forces outputs safe · IO image shared (p. 2)"], False),
                 ("io", "RS-485 + CAN-FD", ["1× RS-485 (Modbus RTU) · 1× CAN-FD (J1939, CANopen) · both isolated 2.5 kV (owner, 2026-11-19) · switchable termination"], False),
                 ("eth", "Ethernet — standard (BASE-9)", ["MAC in PIC32CK → LAN8720AI → RJ45 with magnetics"], False),
                 ("mem", "Storage and time", ["64 Mbit QSPI NOR (2nd firmware image, log buffer) · RTC + CR2032"], False),
             ]),
        dict(key="4g", name="4G MODEM + GPS", sub="45 mm · Quectel EC200U-CN: LTE Cat 1 with built-in GPS · Tier 1 dropped (owner, 2026-11-19)", w=300,
             top=[("DC IN 5–32 V", 2, False)],
             bottom=[],
             leds=[("PWR", "#2ecc71"), ("LTE", "#3498db"), ("GNSS", "#9b59b6"), ("LINK", "#f1c40f")],
             front=[("sim", "nano-SIM"), ("usbc", "USB-C 5 V")],
             sma=["LTE", "GNSS"],
             blocks=[
                 ("radio", "Quectel EC200U-CN — standard firmware", ["LTE Cat 1 (10 / 5 Mbps), India bands, GSM fallback; no firmware of ours", "4G + GPS in one module ≈ INR 850 (quote needed)", "Joins the 4-pin RS-485 bus through a small bridge on the card (proposed, D-29)"], False),
                 ("radio", "GPS (CELL-10)", ["Built into the EC200U-CN: GPS, BeiDou, GLONASS, Galileo; no NavIC", "NMEA over the stack bus"], False),
                 ("power", "Modem rail — on this card (PWR-8)", ["Current-limited 3.8 V buck + ≥ 1000 µF for transmit bursts"], False),
             ]),
        dict(key="wifi", name="WI-FI + BLE", sub="45 mm · node IO + 2 relays", w=250,
             top=[("DC IN 5–32 V", 2, False)],
             bottom=[("485", 3, False), ("CAN", 3, False), ("6 DI", 7, False), ("4 DO", 5, False), ("4 AI", 5, False), ("2 RLY", 6, False)],
             leds=[("PWR", "#2ecc71"), ("WIFI", "#9b59b6"), ("BLE", "#3498db")],
             front=[("usbc", "USB-C 5 V power")],
             sma=["Wi-Fi / BLE"],
             blocks=[
                 ("radio", "Radio", ["ESP32-C6-MINI-1-N4, PCB antenna, pre-certified (MINI-1U + external antenna for metal cabinets)",
                                     "Wi-Fi 6 · BLE 5 · 802.15.4 · secure boot"], False),
                 ("io", "Node IO (WB-5, WB-6)", ["6 DI · 4 DO + watchdog · 4 AI · 2 relays 10 A changeover (AC / DC)", "Isolated RS-485 · isolated CAN 2.0 (TWAI) · I²C IO expander · LED per IO"], False),
             ]),
        dict(key="lora", name="LoRa", sub="45 mm · remote IO node: RS-485, 4 DI, 4 AI, 4 DO · long range, +22 dBm", w=250,
             top=[("DC IN 5–32 V", 2, False)],
             bottom=[("RS-485", 3, False), ("4 DI", 5, False), ("4 AI", 5, False), ("4 DO + 24V", 6, False)],
             leds=[("RUN", "#2ecc71")],
             front=[("usbc", "USB-C 5 V power")],
             sma=["LoRa 865–868"],
             blocks=[
                 ("radio", "LoRa radio + MCU", ["STM32WLE5CC chip-down; pre-certified RAK3172-T module for pilots (≈ +INR 455)",
                                                "Private star network; firmware enforces India e.r.p. limits", "Adaptive data rate: ≈ 0.3 kbps (SF12, longest range) to ≈ 37–62 kbps (SF5, 500 kHz); FSK to 300 kbps short range"], False),
                 ("mem", "OTA", ["A/B update inside the 256 KB on-chip flash (firmware ≤ ≈ 100 KB); no external flash"], False),
                 ("io", "Node IO — on the LoRa module (LORA-6)", ["RS-485 · 4 DI 24 V isolated · 4 AI 0–10 V / 4–20 mA · 4 DO 24 V low-power high-side (TPS274160B), watchdog-gated · one small RUN LED, ≈ 0.3 mA via ≈ 4.7 kΩ, short heartbeat blink"], False),
             ]),
    ]
    AW, AGAP, GAP = 132, 30, 14
    x = 40
    ax = x
    x += AW + AGAP
    xs = []
    for m in mods:
        xs.append(x)
        x += m["w"] + GAP
    end = xs[-1] + mods[-1]["w"]

    # ---- stack-bus label bar
    pg.rect(xs[0], 104, end - xs[0], 38, "#33414f", "#33414f", rx=4)
    pg.text(xs[0] + 10, 119, "STACK BUS — 4 pins, inside the enclosures: a 4-pin connector on each side wall, neighbours joined by a bridge plug (part: D-9) · not hot-pluggable", 11, "bold", fill="#ffffff")
    pg.text(xs[0] + 10, 135, "BUS_V · GND · RS485_A · RS485_B — half-duplex RS-485 at ≈ 2 Mbit/s, polled by the elected coordinator · page 3", 10, fill="#dfe6ee")

    # ---- external adapter (DIN-rail PSU)
    pg.rect(ax - 8, 196, AW + 16, BOT - 196 + 6, "none", "#c46a00", rx=10, sw=1.4, dash=True)
    pg.text(ax + AW / 2, BOT - 40, "supplied separately", 10, "bold", "middle", fill="#c46a00")
    pg.text(ax + AW / 2, BOT - 26, "not part of the stack", 9.5, "normal", "middle", fill="#c46a00")
    pg.rect(ax, TOP + 120, AW, 520, "#f2f4f6", "#23303d", rx=8, sw=2.2)
    pg.rect(ax + 10, TOP + 128, AW - 20, 24, "#5b6670", "#2b3138", rx=2)
    for k in range(2):
        sx = ax + AW / 2 - 9 + k * 18
        pg.p.append(f'<circle cx="{sx}" cy="{TOP + 140}" r="5.5" fill="#d5d9dd" stroke="#2b3138"/>')
    pg.text(ax + AW / 2, TOP + 166, "+V  −V  DC out", 9, "bold", "middle", fill="#2b3138")
    pg.rect(ax, TOP + 176, AW, 70, "#23303d", "#23303d", rx=0)
    pg.para(ax + 8, TOP + 196, AW - 16, ["ADAPTER (AC-DC)"], 11, weight="bold", fill="#ffffff")
    pg.para(ax + 8, TOP + 228, AW - 16, ["12 V, 18 W"], 10, fill="#cfd8e2")
    pg.p.append(f'<circle cx="{ax + 14}" cy="{TOP + 262}" r="4.5" fill="#2ecc71" stroke="#333" stroke-width="0.8"/>')
    pg.text(ax + 24, TOP + 266, "DC OK", 8.5, fill="#2b3138")
    pg.para(ax + 8, TOP + 292, AW - 16, [
        "Mains supply stays outside (PWR-3); relay contacts may switch mains, behind 5 kV isolation",
        "IEC 62368-1, BIS CRS, CE (to confirm)",
        "Easy to replace and service",
        "Single modules: any certified 5 V USB-C charger (≥ 15 W)",
        "Part TBD; no Mornsun (COMP-6)"], 9.5, bullet=True)
    pg.rect(ax + 10, TOP + 600, AW - 20, 24, "#5b6670", "#2b3138", rx=2)
    for k in range(3):
        sx = ax + AW / 2 - 18 + k * 18
        pg.p.append(f'<circle cx="{sx}" cy="{TOP + 612}" r="5.5" fill="#d5d9dd" stroke="#2b3138"/>')
    pg.text(ax + AW / 2, TOP + 586, "L   N   ⏚", 9, "bold", "middle", fill="#2b3138")
    pg.text(ax + AW / 2, TOP + 664, "AC 100–240 V in", 9.5, "bold", "middle", fill="#b32f2f")
    pg.line(ax + AW / 2, TOP + 624, ax + AW / 2, TOP + 650, "#b32f2f", 2.5)

    # ---- modules
    for i, m in enumerate(mods):
        x0, w = xs[i], m["w"]
        dash = m["key"] == "fb"
        # bridge plug across the gap to the next module
        if i < len(mods) - 1:
            nx = xs[i + 1]
            pg.rect(x0 + w - 34, TOP - 7, (nx + 34) - (x0 + w - 34), 14, "#7b8794", "#2b3138", rx=3, sw=1.2)
            pg.line((x0 + w + nx) / 2, 142, (x0 + w + nx) / 2, TOP - 7, "#33414f", 1.2)
        pg.rect(x0, TOP, w, BOT - TOP, "#f2f4f6", "#23303d", rx=10, sw=2.4, dash=dash)
        for k, lab in enumerate(m["sma"]):
            sma(x0 + w * (k + 1) / (len(m["sma"]) + 1), lab)
        if i == len(mods) - 1:
            pg.rect(x0 + w - 30, TOP - 7, 22, 14, "#c9ced3", "#2b3138", rx=3, sw=1.2)
            pg.text(x0 + w - 34, TOP - 12, "end cap", 8.5, anchor="end", fill="#4a5560")
        # top terminals
        tc = screws(x0 + 40, TOP + 8, w - 80, m["top"])
        if m["key"] == "base":
            dc_x = tc[0]
        # header band
        hy = TOP + 62
        pg.rect(x0 + 6, hy, w - 12, 70, "#23303d", "#23303d", rx=4)
        pg.text(x0 + 14, hy + 19, m["name"], 13, "bold", fill="#ffffff")
        subl = wrap(m["sub"], w - 28, 9.5)[:2]
        for k, ln in enumerate(subl):
            pg.text(x0 + 14, hy + 35 + k * 12, ln, 9.5, fill="#cfd8e2")
        leds(x0 + 14, hy + 61, m["leds"])
        # PCB (cover removed)
        py0 = hy + 80
        front_h = 62 if m["front"] else 0
        bot_h = 52 if m["bottom"] else 0
        py2 = BOT - 22 - bot_h - front_h - 8          # bottom of the power-PCB zone
        PWH, PWG = 46, 14                             # power PCB height, gap for the B2B connector
        py1 = py2 - PWH - PWG                         # bottom of the logic PCB
        pg.rect(x0 + 8, py0, w - 16, py1 - py0, "#e9f3ea", "#7aa37a", rx=4, sw=1.2)
        pg.text(x0 + w - 14, py0 + 13, "LOGIC PCB", 8.5, "bold", "end", fill="#5f8a5f")
        # separate power PCB (common part, PWR-10) and, on the coordinator, the separate battery board (PWR-2)
        pp0 = py1 + PWG
        pw = (w - 16)
        pg.rect(x0 + 8, pp0, pw, PWH, "#ffe8cf", "#c46a00", rx=4, sw=1.8)
        for bx in (x0 + 8 + pw * 0.3, x0 + 8 + pw * 0.7):
            pg.rect(bx - 14, py1 + 2, 28, PWG - 4, "#2b3138", "#2b3138", rx=1)
        pg.text(x0 + 16, pp0 + 19, "BATTERY + CHARGER BOARD", 10.5, "bold", fill="#c46a00")
        pg.text(x0 + 16, pp0 + 35, "plug-in, optional (PWR-2) →", 9, fill="#7a4a10")
        if False:
            bx0 = x0 + 8 + pw + 8
            bw = (w - 16) - pw - 8
            pg.rect(bx0, pp0, bw, PWH, "#ffffff", "#c46a00", rx=4, sw=1.8, dash=True)
            pg.line(x0 + 8 + pw, pp0 + PWH / 2, bx0, pp0 + PWH / 2, "#c46a00", 3)
            pg.text(bx0 + 8, pp0 + 19, "BATTERY BOARD", 10.5, "bold", fill="#c46a00")
            pg.text(bx0 + 8, pp0 + 35, "1 per gateway (PWR-2) →", 9, fill="#7a4a10")
        y = py0 + 18
        for kind, title, lines, bdash in m["blocks"]:
            y = pg.block(x0 + 16, y, w - 32, kind, title, lines, bdash, size=10) + 6
        if y > py1:
            print(f"WARNING overflow in {m['name']}: {y:.0f} > {py1:.0f}", file=sys.stderr)
        # front-panel connectors
        fy = py2 + 8
        if m["front"]:
            n = len(m["front"])
            for k, (kind, lab) in enumerate(m["front"]):
                cx = x0 + w * (k + 1) / (n + 1)
                if kind == "usbc":
                    usbc(cx - 17, fy, lab)
                elif kind == "rj45":
                    rj45(cx - 22, fy, lab)
                elif kind == "rj45d":
                    rj45(cx - 22, fy, lab, dash=True)
                elif kind == "sim":
                    sim(cx - 23, fy, lab)
                elif kind == "switch":
                    switch(cx - 15, fy, lab)
        # bottom terminals
        if m["bottom"]:
            screws(x0 + 14, BOT - 22 - bot_h + 4, w - 28, m["bottom"])
        # DIN clip
        pg.rect(x0 + w / 2 - 22, BOT - 6, 44, 12, "#2b3138", "#2b3138", rx=2)

    # ---- separate block: the common power parts (right of the stack)
    rx0 = end + 26
    rw = W - 40 - rx0
    pg.rect(rx0 - 8, 150, rw + 16, BOT - 150 + 6, "none", "#c46a00", rx=10, sw=1.4, dash=True)
    pg.text(rx0 + rw / 2, 172, "COMMON POWER PARTS", 11, "bold", "middle", fill="#c46a00")
    pg.text(rx0 + rw / 2, 186, "separate boards", 9.5, "normal", "middle", fill="#c46a00")
    # power PCB drawing
    yb = 204
    pg.rect(rx0, yb, rw, 132, "#ffe8cf", "#c46a00", rx=6, sw=2)
    pg.rect(rx0 + 8, yb + 8, 40, 20, "#5b6670", "#2b3138", rx=2)
    for k in range(2):
        pg.p.append(f'<circle cx="{rx0 + 18 + k * 20}" cy="{yb + 18}" r="5" fill="#d5d9dd" stroke="#2b3138"/>')
    pg.rect(rx0 + 58, yb + 12, 30, 12, "#c9ced3", "#2b3138", rx=6)
    pg.rect(rx0 + rw - 52, yb + 10, 44, 16, "#2b3138", "#2b3138", rx=1)
    pg.text(rx0 + 28, yb + 40, "DC IN", 8, "bold", "middle", fill="#2b3138")
    pg.text(rx0 + 73, yb + 40, "USB-C", 8, "bold", "middle", fill="#2b3138")
    pg.text(rx0 + rw - 30, yb + 40, "to logic PCB", 8, "bold", "middle", fill="#2b3138")
    for k, (lab, xx) in enumerate([("buck", 8), ("5 V", 52), ("3.3 V", 96)]):
        pg.rect(rx0 + xx, yb + 50, 38, 24, "#2b3138", "#2b3138", rx=2)
        pg.text(rx0 + xx + 19, yb + 66, lab, 8, "bold", "middle", fill="#ffffff")
    pg.rect(rx0 + 8, yb + 84, rw - 16, 18, "#ffffff", "#c46a00", rx=2, dash=True)
    pg.text(rx0 + rw / 2, yb + 97, "battery-board socket", 8.5, "bold", "middle", fill="#c46a00")
    pg.text(rx0 + 8, yb + 122, "POWER STAGE", 12, "bold", fill="#c46a00")
    yy = pg.para(rx0, yb + 152, rw, ["On every module PCB (PWR-10)", "Buck regulator: 5–32 V → 5 V + 3.3 V",
        "TVS, reverse FET, PTC, Schottky OR", "≈ INR 85 BOM, in the module price"], 9.5, bullet=True)
    # battery board drawing
    yb = yy + 14
    pg.rect(rx0, yb, rw, 112, "#ffffff", "#c46a00", rx=6, sw=2, dash=True)
    pg.rect(rx0 + 10, yb + 10, rw - 20, 24, "#e8e2d4", "#7a6a4a", rx=12)
    pg.text(rx0 + rw / 2, yb + 27, "18650 ≈ 3000 mAh", 8.5, "bold", "middle", fill="#5a4a2a")
    pg.rect(rx0 + 10, yb + 72, 40, 26, "#2b3138", "#2b3138", rx=2)
    pg.text(rx0 + 30, yb + 89, "chg", 8, "bold", "middle", fill="#ffffff")
    pg.text(rx0 + 58, yb + 90, "BATTERY BOARD", 10.5, "bold", fill="#c46a00")
    pg.para(rx0, yb + 132, rw, ["One per module, optional (PWR-2)", "TI BQ25601 charger, backup + 5 V boost; 18650 ≈ 3000 mAh",
        "I²C status, presence detect", "≈ INR 205 BOM incl. cell"], 9.5, bullet=True)

    # 12 V cable from adapter to baseboard DC IN
    bx = dc_x - 4
    cy = 182
    pg.p.append(f'<polyline points="{ax + AW / 2},{TOP + 128} {ax + AW / 2},{cy} {bx + 4},{cy} {bx + 4},{TOP + 8}" '
                f'fill="none" stroke="#c46a00" stroke-width="3"/>')
    pg.text((ax + AW / 2 + bx) / 2, cy - 5, "DC supply", 9.5, "bold", "middle", fill="#c46a00")

    # DIN rail
    pg.rect(30, BOT + 4, W - 60, 16, "#b8bec6", "#7b8794", rx=2)
    pg.text(40, BOT + 16, "35 mm DIN rail (TS35)", 9.5, "bold", fill="#33414f")

    # legend + notes
    ly = 1084
    items = [("mcu", "MCU"), ("radio", "Radio"), ("eth", "Ethernet"), ("io", "Field IO / RS-485"),
             ("sec", "Security"), ("mem", "Memory / ID"), ("power", "Power")]
    pg.text(40, ly - 8, "Legend", 12, "bold")
    for k, (kind, lab) in enumerate(items):
        cx = 40 + (k % 4) * 132
        cyy = ly + (k // 4) * 24
        pg.rect(cx, cyy, 20, 14, COL[kind][0], COL[kind][1], rx=3)
        pg.text(cx + 27, cyy + 11.5, lab, 10.5)
    pg.rect(40 + 3 * 132, ly + 24, 20, 14, "#ffffff", "#33414f", rx=3, dash=True)
    pg.text(40 + 3 * 132 + 27, ly + 35.5, "fitted to order", 10.5)
    pg.para(40, ly + 62, 540, ["Gold = SMA antenna connector · grey strips = screw terminals · ∥ = diode-ORed supplies · D-x = open decision (PRD §6)"], 10, fill="#4a5560")
    notes = [
        "Reliability and safety before cost (COMP-5). Ethernet only through a MAC inside the host chip. No Mornsun parts. Modules run on safe low voltage; only relay contacts may switch mains, behind 5 kV reinforced isolation.",
        "Every module: its own power stage on its PCB (input protection, OR, buck to 5 V + 3.3 V, PWR-10) and optionally a plug-in battery + charger board with an 18650 cell (PWR-2); each module reports its type, hardware revision and serial over the stack bus (no ID EEPROM); a hung module is reset by its own watchdog.",
        "No baseboard: every module is standalone; in a stack the coordinator is elected Fieldbus controller > Wi-Fi + BLE > LoRa; any module may feed bus power. Each module can take its own battery + charger board (PWR-2). 4G industrial router (RUT200 class): separate product, page 7.",
        "Parts are research proposals, not frozen: confirm stock and 100-unit quotes first.",
    ]
    pg.text(600, ly - 8, "Notes", 12, "bold")
    pg.para(600, ly + 8, W - 40 - 600, notes, 10.5, bullet=True)
    pg.save("UC_Architecture_p1_System.svg")



# ---------------------------------------------------------------- page 2
def page2():
    pg = Page("Field IO and how the modules share it",
              "Each module drives only its own IO; the coordinator (Fieldbus controller, else Wi-Fi + BLE, else LoRa) merges all IO into one image "
              "shared over the stack bus (IO-6). Wi-Fi + BLE adds 6 DI, 4 DO, 4 AI and 2 relays; LoRa adds 4 DI, 4 DO and 4 AI.")
    pg.p.append('<g transform="translate(0,24)">')
    # IO table
    x0, y0 = 40, 112
    cols = [("Channels", 120), ("Count", 60), ("Signal types", 240), ("Front end (R08)", 190), ("Notes", 150)]
    tw = sum(c[1] for c in cols)
    pg.text(x0, y0 - 6, "Field IO on the Fieldbus-controller module — 28 channels", 15, "bold")
    rows = [
        ("AI1–AI6 universal analog", "6", "0–10 V, 4–20 mA or PT1000, selected per channel in software",
         "MCU ADC; quad + dual op-amp buffers, 0.1 % 2.5 V reference (ratiometric PT1000)", "Survive 24 V mis-wiring and reverse polarity (IO-5)"),
        ("DI1–DI10 digital in", "10", "24 V DC, IEC 61131-2 Type 1/3; dry contacts",
         "10× single optocouplers (LTV-217 / EL3H7 class)", "DI1–DI2 also pulse counters (energy / flow meters)"),
        ("RL1–RL8 relay out", "8", "SPDT (NO + NC + COM), 10 A at 230 VAC / 30 VDC, AC or DC loads",
         "Hongfa / Omron / Panasonic, 5 V coil, 5 kV reinforced; ULN2803 driver, watchdog gating", "10 A fuse per relay, replaceable from the front; 300 V terminals kept apart from SELV (SAF-2)"),
        ("HS1–HS4 high-side out", "4", "Fast 24 V high-side switch with current monitoring",
         "TI TPS274160B quad, current sense to the MCU ADC, watchdog gating", "Hardware safe state: off on MCU hang, reset or power loss (IO-4)"),
        ("Internal monitoring", "—", "Supply voltage, Li-ion voltage, board temperature",
         "MCU ADC", "Feeds alarms and last-gasp logic"),
    ]
    y = y0 + 10
    pg.rect(x0, y, tw, 26, "#23303d", "#23303d", rx=0)
    cx = x0
    for name, cw in cols:
        pg.text(cx + 6, y + 18, name, 11.5, "bold", fill="#ffffff")
        cx += cw
    y += 26
    for r_i, row in enumerate(rows):
        hts = [len(wrap(cell, cw - 12, 10.5)) for cell, (_, cw) in zip(row, cols)]
        rh = max(hts) * 14 + 12
        pg.rect(x0, y, tw, rh, "#f4f6f8" if r_i % 2 == 0 else "#ffffff", "#c9d0d8", rx=0, sw=1)
        cx = x0
        for cell, (_, cw) in zip(row, cols):
            pg.para(cx + 6, y + 17, cw - 12, [cell], 10.5, lh=14,
                    weight="bold" if cx == x0 else "normal")
            cx += cw
        y += rh
    pg.rect(x0, y, tw, 24, "#dcf3e0", "#2e8540", rx=0, sw=1)
    pg.text(x0 + 6, y + 17, "Total: 6 analog in + 10 digital in + 8 relays + 4 high-side out = 28 field IO", 11, "bold", fill="#1f5e2d")
    y += 48

    # example flows
    pg.text(x0, y, "Examples", 15, "bold")
    y += 22
    flows = [
        ("Input to cloud", ["DI3 changes → its module timestamps it → the coordinator updates the IO image → reports it at the next poll",
                            "4G module reads the change over the stack bus → publishes MQTT over TLS to the cloud"]),
        ("Cloud command to output", ["Cloud asks for relay RL2 = ON through the 4G module → module sends a write request on the bus",
                                     "Coordinator checks: is the requesting module authenticated (keys in the MCU's TrustZone secure world) and the configured owner of RL2? → drives RL2 → confirms back",
                                     "If the 4G module stops refreshing its ownership lease, RL2 returns to its safe state"]),
        ("Remote IO via LoRa", ["A remote LoRa node reports a tank level → the LoRa module in the stack forwards it to the coordinator",
                                "The coordinator stores it as virtual point V-AI1 in the same image → visible to the cloud like a local input"]),
        ("Modbus to a SCADA", ["The Fieldbus controller's RS-485 port acts as Modbus RTU slave: AI / DI / DO mapped to registers",
                               "Same owner rules apply: SCADA writes reach an output only if the RS-485 interface is its configured owner"]),
    ]
    for t, lines in flows:
        pg.text(x0, y, t, 12, "bold", fill="#2f5fb3")
        y = pg.para(x0 + 12, y + 17, tw - 12, lines, 11, bullet=True) + 8

    # sharing diagram (right)
    rx0 = 840
    pg.text(rx0, y0 - 6, "Sharing model", 15, "bold")
    # field
    pg.rect(rx0, 130, 250, 64, "#dcf3e0", "#2e8540")
    pg.para(rx0 + 10, 152, 235, ["Field: 6 AI · 10 DI · 8 RL · 4 HS", "sensors, meters, actuators"], 11.5, weight="bold", fill="#1f5e2d")
    pg.line(rx0 + 125, 194, rx0 + 125, 236, arrow="both", sw=2)
    # baseboard server
    pg.rect(rx0, 236, 250, 300, "#dbe8ff", "#2f5fb3", sw=2)
    pg.text(rx0 + 10, 258, "Coordinator — IO server", 12.5, "bold", fill="#2f5fb3")
    pg.para(rx0 + 10, 278, 232, ["Samples inputs, drives outputs, runs local logic"], 10.5)
    pg.rect(rx0 + 12, 300, 226, 112, "#ffffff", "#2f5fb3")
    pg.para(rx0 + 20, 320, 212, ["IO process image", "values · timestamps · quality", "local IO + virtual points (LoRa, Modbus)",
                                 "output owner table + lease timers"], 10.5)
    pg.rect(rx0 + 12, 420, 226, 52, "#ffdcdc", "#b32f2f")
    pg.para(rx0 + 20, 440, 212, ["TrustZone secure world: authenticates each module before it may write"], 10.5)
    pg.rect(rx0 + 12, 478, 226, 50, "#ffe8cf", "#c46a00")
    pg.para(rx0 + 20, 498, 212, ["TPS3430 watchdog: relays and outputs off if this MCU hangs"], 10.5)

    # bus spine
    sx = rx0 + 330
    pg.rect(sx, 150, 26, 500, "#33414f", "#33414f", rx=3)
    pg.p.append(f'<text x="{sx + 18}" y="400" font-size="11" fill="#ffffff" font-weight="bold" '
                f'transform="rotate(-90 {sx + 18} 400)" text-anchor="middle">STACK BUS: 4 pins, RS-485</text>')
    pg.line(rx0 + 250, 330, sx, 330, arrow="both", sw=2.2)
    pg.text(sx - 8, 318, "broadcast", 10, anchor="end", fill="#4a5560")
    pg.text(sx - 8, 348, "cyclic + on change", 10, anchor="end", fill="#4a5560")

    mods = [
        ("4G + Ethernet + Wi-Fi", "Uplink: MQTT / HTTPS to cloud, Modbus TCP server on Ethernet, SMS alarms", "radio"),
        ("Wi-Fi + BLE", "Uplink over Wi-Fi; BLE commissioning app reads IO and config", "radio"),
        ("LoRa", "Brings remote node data in as virtual points; sends commands to remote outputs", "radio"),
    ]
    my = 150
    for name, desc, kind in mods:
        fill, stroke = COL[kind]
        pg.rect(sx + 70, my, 330, 104, fill, stroke)
        pg.text(sx + 80, my + 20, name + " module", 12, "bold", fill=stroke)
        pg.para(sx + 80, my + 40, 312, [desc], 10.5)
        pg.para(sx + 80, my + 86, 312, ["reads any input · writes only outputs it owns"], 10, fill="#4a5560")
        pg.line(sx + 26, my + 52, sx + 70, my + 52, arrow="both", sw=2)
        my += 125

    # rules
    ry = 690
    pg.text(rx0, ry, "Sharing rules (proposed — PRD IO-6)", 15, "bold")
    rules = [
        "Local hardware: each module reads and drives only its own IO (Fieldbus controller 28 channels; Wi-Fi + BLE 16 plus RS-485 and CAN; LoRa 12 plus RS-485).",
        "Publish: the coordinator broadcasts the IO process image on the RS-485 stack bus cyclically (rate configurable, for example 100 ms) and immediately on change, in its next transmit turn (≤ ≈ 20 ms).",
        "Read: any fitted module may read any input, status or virtual point.",
        "Write: each output has exactly one owner at a time — coordinator logic or one named module — set by configuration. Writes from any other module are rejected and logged.",
        "Trust: only modules authenticated by the coordinator may write (SEC-5); strongest with the Fieldbus controller's TrustZone (PSA L3). A cloned or rogue module can at most read.",
        "Lease and safe state: the owner refreshes a lease; if it lapses or the bus fails, the output goes to its configured safe state. Independently, the hardware watchdog switches all relays and outputs off if its own MCU hangs (IO-4).",
        "Standalone: a module running alone uses its own IO and interfaces; no other module is needed.",
    ]
    pg.para(rx0, ry + 24, W - 40 - rx0 - 10, rules, 11.5, bullet=True)
    pg.p.append("</g>")
    pg.save("UC_Architecture_p2_IO_Sharing.svg")


# ---------------------------------------------------------------- page 3
def page3():
    pg = Page("Stack bus and power distribution",
              "4-pin stack bus (owner, 2026-11-16): power plus one RS-485 pair, passed straight through every module. "
              "Connector part and pitch: D-9. Protocol details will be fixed in the specification.")
    pg.p.append('<g transform="translate(0,24)">')
    x0, y0 = 40, 118
    pg.text(x0, y0 - 8, "4-pin stack bus (SYS-11)", 15, "bold")
    cols = [(6, "Pin"), (56, "Signal"), (190, "Function"), (520, "Rating")]
    pg.rect(x0, y0, 740, 28, "#23303d", "#23303d", rx=0)
    for cx, lab in cols:
        pg.text(x0 + cx, y0 + 19, lab, 12, "bold", fill="#ffffff")
    pins = [("1", "BUS_V", "5–32 V stack supply, fed by any module (PWR-4)", "≥ 3 A", "#ffe8cf"),
            ("2", "GND", "ground and RS-485 reference", "≥ 3 A", "#e4e4e4"),
            ("3", "RS485_A", "half-duplex stack bus, non-inverting", "≈ 2 Mbit/s", "#dbe8ff"),
            ("4", "RS485_B", "half-duplex stack bus, inverting", "120 Ω at both ends", "#dbe8ff")]
    for k, (n, sig, fn, rt, fill) in enumerate(pins):
        ry = y0 + 28 + k * 34
        pg.rect(x0, ry, 740, 34, fill, "#c9d0d8", rx=0, sw=0.8)
        pg.text(x0 + 10, ry + 22, n, 13)
        pg.text(x0 + 56, ry + 22, sig, 13, "bold")
        pg.text(x0 + 190, ry + 22, fn, 12, fill="#33414f")
        pg.text(x0 + 520, ry + 22, rt, 12, fill="#33414f")
    ny = y0 + 28 + 4 * 34 + 34
    pg.text(x0, ny, "How the modules talk", 13, "bold")
    ny = pg.para(x0, ny + 20, 740, [
        "Each module drives the bus from a spare UART through a small RS-485 transceiver (≈ INR 26). No extra processor on the Fieldbus controller, Wi-Fi + BLE or LoRa module.",
        "The elected coordinator (Fieldbus controller > Wi-Fi + BLE > LoRa, SYS-5) only hands out transmit turns, about every 20 ms, so only one module transmits at a time.",
        "Discovery by each MCU's unique ID; no address switches. Type, hardware revision, serial and firmware version are reported over the bus (SYS-7).",
        "Load: the shared IO image is about 0.1 Mbit/s. Bulk 4G traffic uses the 4G card's own RJ45.",
        "4G card: the modem has no MCU of ours, so how it joins the bus is open — D-29 (recommended: a small bus-bridge MCU on the card).",
        "Why not I3C or CAN-FD: I3C exists only on the STM32H5 and is a short on-board bus; the ESP32-C6 has classic CAN only and the STM32WLE5 has no CAN.",
    ], 11, bullet=True)
    ny += 16
    pg.text(x0, ny, "What the 40-pin bus did — and what replaces it", 13, "bold")
    rows = [("TOKEN slot order", "discovery by unique ID; slot order not known"),
            ("IRQ_N fast events", "published in the module's next turn, ≤ ≈ 20 ms"),
            ("Per-slot PWR_EN", "each MCU's own watchdog; reset command over the bus"),
            ("PFAIL_N", "power-fail message from the battery host"),
            ("SYNC", "time-sync broadcast"),
            ("GNSS_TX pin", "NMEA over the bus (D-29)"),
            ("SWD (factory)", "programming over USB-C (MFG-2)")]
    ty = ny + 10
    for k, (o, r) in enumerate(rows):
        pg.rect(x0, ty + k * 24, 740, 24, "#f6f8fa" if k % 2 == 0 else "#ffffff", "#c9d0d8", rx=0, sw=0.8)
        pg.text(x0 + 8, ty + k * 24 + 16, o, 11, "bold")
        pg.text(x0 + 220, ty + k * 24 + 16, r, 11, fill="#33414f")
    # publish-subscribe (SYS-12)
    py_ = ty + len(rows) * 24 + 34
    pg.text(x0, py_, "Publish–subscribe on the bus (SYS-12)", 13, "bold")
    slots = [("C", "turn grant", "#5a6470"), ("FC", "io/fc/di · io/fc/ai", "#2f5fb3"), ("Wi-Fi", "io/wifi/di", "#6b3fb3"),
             ("LoRa", "lora/node17/level", "#c46a00"), ("4G", "cell/status", "#1f7f8c"), ("C", "turn grant", "#5a6470")]
    sx, sy = x0, py_ + 14
    sw_ = [70, 150, 120, 160, 110, 70]
    for (who, topic, col), w_ in zip(slots, sw_):
        pg.rect(sx, sy, w_ - 6, 44, col, col, rx=4)
        pg.text(sx + 8, sy + 18, who, 11, "bold", fill="#ffffff")
        pg.text(sx + 8, sy + 34, topic, 9.5, fill="#ffffff")
        sx += w_
    pg.line(x0, sy + 56, x0 + 674, sy + 56, "#33414f", 1.4, arrow="end")
    pg.text(x0 + 680, sy + 60, "time", 10, fill="#4a5560")
    pg.text(x0, sy + 74, "one bus cycle ≈ 20 ms: every module gets one turn; every frame is heard by every module", 10, fill="#4a5560")
    pg.para(x0, sy + 98, 740, [
        "In its turn a module publishes frames tagged with a topic (for example io/fc/di). Every module hears every frame on the shared pair and keeps only the topics it subscribes to — no relaying through a hub.",
        "Same model inside each module: Zephyr zbus channels, with selected channels bridged onto the bus; the coordinator maps bus topics to MQTT topics for the cloud.",
        "Every frame carries a sequence number, CRC and a message authentication code with the stack key handed out by the coordinator (SEC-5); output commands are accepted only from the configured owner (IO-6).",
    ], 11, bullet=True)

    # power chain (right)
    px = 830
    pg.text(px, y0 - 8, "Power distribution", 15, "bold")
    def pbox(x, y, w, h, t, lines, kind="power", dash=False):
        fill, stroke = COL[kind]
        pg.rect(x, y, w, h, fill if not dash else "#ffffff", stroke, dash=dash)
        pg.text(x + 8, y + 18, t, 11.5, "bold", fill=stroke)
        pg.para(x + 8, y + 36, w - 16, lines, 10.5, lh=13.5)
    # A. common power PCB
    pg.text(px, y0 + 22, "Power stage — on every module PCB (PWR-10, ≈ INR 85)", 12.5, "bold", fill="#23303d")
    pbox(px, y0 + 32, 165, 130, "Inputs", ["DC terminal 5–32 V", "USB-C 5 V (no PD, owner 2026-11-19)", "BUS_V via TVS + damping (hot-plug ringing ≈ 48 V)"])
    pbox(px + 195, y0 + 32, 170, 130, "Protect + OR", ["TVS, reverse FET, PTC fuse", "Schottky OR: terminal ∥ USB-C ∥ BUS_V"])
    pbox(px + 400, y0 + 32, 175, 56, "Buck regulator", ["5–32 V → 5 V"])
    pbox(px + 400, y0 + 98, 175, 56, "Battery-board socket", ["5 V in / out, I²C, detect"])
    pbox(px + 400, y0 + 164, 175, 56, "Bus feed", ["PTC-limited → BUS_V"])
    pbox(px + 610, y0 + 32, 190, 56, "3.3 V LDO", ["low Iq"])
    pbox(px + 610, y0 + 98, 190, 122, "To the logic PCB", ["5 V, 3.3 V, battery I²C + detect, power-fail signal",
                                                         "4G card adds its own 3.8 V buck + ≥ 1000 µF (PWR-8)"], kind="mem")
    pg.line(px + 165, y0 + 97, px + 195, y0 + 97, arrow="end", sw=2)
    pg.line(px + 365, y0 + 97, px + 382, y0 + 97, sw=2)
    pg.line(px + 382, y0 + 60, px + 382, y0 + 192, sw=2)
    for yy in (60, 126, 192):
        pg.line(px + 382, y0 + yy, px + 400, y0 + yy, arrow="end", sw=2)
    pg.line(px + 575, y0 + 60, px + 610, y0 + 60, arrow="end", sw=2)
    pg.line(px + 705, y0 + 88, px + 705, y0 + 98, arrow="end", sw=2)
    # bus bar
    by = y0 + 244
    pg.rect(px, by, 800, 22, "#33414f", "#33414f", rx=3)
    pg.text(px + 10, by + 16, "4-pin bus through every bridge plug: BUS_V · GND · RS485_A · RS485_B", 11, "bold", fill="#ffffff")
    pg.line(px + 487, y0 + 220, px + 487, by, arrow="end", sw=2)
    pg.line(px + 82, by, px + 82, y0 + 162, arrow="end", sw=2)
    # B. one battery per gateway
    my = by + 62
    pg.text(px, my - 12, "Battery + charger board — optional, one per module (PWR-2)", 12.5, "bold", fill="#23303d")
    pbox(px, my + 14, 150, 70, "Adapter", ["12 V 18 W, into any module"])
    pbox(px + 180, my + 14, 175, 70, "Module", ["its power stage"])
    pbox(px + 385, my, 230, 100, "Battery + charger board", ["TI BQ25601 charger, power path, 5 V boost", "18650 ≈ 3000 mAh (1S) + protector",
                                                  "I²C status, NTC charge limits"], dash=True)
    pbox(px + 645, my + 14, 155, 70, "Other modules", ["each: own power stage, battery board optional"])
    pg.line(px + 150, my + 49, px + 180, my + 49, arrow="end", sw=2)
    pg.line(px + 355, my + 49, px + 385, my + 49, arrow="both", sw=2)
    pg.p.append(f'<polyline points="{px + 267},{my + 84} {px + 267},{my + 122} {px + 722},{my + 122} {px + 722},{my + 88}" '
                f'fill="none" stroke="#c46a00" stroke-width="2.4" marker-end="url(#ar)"/>')
    pg.text(px + 500, my + 117, "BUS_V — stays up on battery", 10.5, "bold", "middle", fill="#c46a00")
    pg.para(px, my + 146, 800, [
        "Mains lost: the BQ25601 power path keeps the cell connected and its boost drives the module's 5 V rail without a dropout; a module with a battery can also feed BUS_V. Each module broadcasts a power-fail message on the bus.",
        "Every module is also a standalone product, so each can take its own battery board (owner, 2026-11-19). In a stack, charging is capped at 0.3 A per board so one 12 V 18 W adapter is enough (PWR-3).",
    ], 10.5, bullet=True)

    cy = my + 232
    pg.text(px, cy, "Bus limits and rules (R06, R07)", 15, "bold")
    rules = [
        "Current through the first bridge carries the whole stack: about 0.83 A at 24 V, 1.67 A at 12 V, 2.22 A at 9 V. Prefer a 24 V bus; at most 4 modules on a 9 V supply.",
        "Power budget (R06, to be recomputed for the 12 V adapter and the integrated 4G module): about 9 W average, 15–20 W peak for a full stack; the 4G module alone peaks near 10.6 W, about 5 W at the bus with local buffering. The external adapter is 12 V 18 W: a 4-module stack needs ≈ 13–14 W with charging capped at 0.3 A per battery board.",
        "The bus is not hot-pluggable. The exposed connector on the end module gets a cap and ESD protection (EMC-3); the bus carries SELV only.",
        "Only power and one RS-485 pair cross the bus; each module's Ethernet, USB and radios stay local.",
        "Li-ion: cells to IEC 62133-2 / UN 38.3 and BIS IS 16046-2; charging only between 0 and 45 °C, blocked in hot cabinets.",
        "A power-fail message gives every module early warning to save state and send a last-gasp message.",
        "4G module: modem bursts (up to about 2 A at 3.8 V) come from ≥ 1000 µF on its 3.8 V rail behind a current-limited buck, so the bus sees a smooth current (PWR-8). Its power stage must pass about 0.9 A at 12 V.",
        "The supply is never mains: a separate certified 12 V adapter is supplied (PWR-3); relay contacts may switch mains loads, isolated by 5 kV from the electronics. With it the bus runs at 12 V (about 1.67 A through the first bridge at full load).",
    ]
    pg.para(px, cy + 22, 800, rules, 11.5, bullet=True)
    pg.p.append("</g>")
    pg.save("UC_Architecture_p3_Bus_Power.svg")


# ---------------------------------------------------------------- page 4
# BOM line items in INR at 100 units (owner, 2026-11-19: all prices at 100 units only) — research prices (R02–R22) × 1.3
# until 100-unit quotes exist, rounded per line so every module total is unchanged. Estimates, not quotes.
MFG, ROY, PROFIT = 0.50, 0.15, 0.30
BOM = {
    "base": ("Fieldbus controller — logic PCB, with Ethernet (R14; 2026-11-19)", [
        ("MCU Microchip PIC32CK2051SG01100 (standard for now, owner 2026-11-19; Ethernet MAC, HSM + TrustZone), TQFP100-EP + 64 Mbit QSPI NOR (2nd image, log buffer) + RTC crystal + CR2032 backup", 402),
        ("Ethernet, standard: LAN8720AI PHY + 25 MHz crystal + RJ45 with magnetics (Würth / HanRun, < INR 100) ≈ 200 (owner, 2026-11-19, ESTIMATE), ESD + passives ≈ 70", 270),
        ("6 analog inputs (owner, 2026-11-22), each 0–10 V / 4–20 mA / PT1000: quad + dual op-amp, 0.1 % resistors, mode FETs, protection, low-cost 0.1 % 2.5 V reference (ESTIMATE)", 218),
        ("10 digital inputs: 10× single optocouplers, LTV-217 / EL3H7 class (ESTIMATE), Type 3 front ends", 84),
        ("8 relay outputs, SPDT (NO + NC), 10 A at 230 VAC / 30 VDC, 5 V coil (owner, 2026-11-20 / 22): Hongfa / Omron / Panasonic, 5 kV reinforced coil-contact isolation, INR 40 each at volume (owner target, 2026-11-22; local quote to follow), ULN2803 driver, watchdog gating, snubber pads (ESTIMATE)", 380),
        ("Replaceable fuse per relay, changed from outside the module (owner, 2026-11-20 / 22): 5×20 mm ceramic time-lag 10 A / 250 V in a front-access, touch-safe holder with screw / bayonet cap, INR 20 each incl. holder (owner, 2026-11-22)", 160),
        ("4 high-speed 24 V high-side outputs with current monitoring (owner, 2026-11-20): TI TPS274160B quad, current sense to the MCU ADC, TVS, reverse FET (ESTIMATE)", 200),
        ("24 relay terminal poles, 5.08 mm, 300 V / 10 A rated, kept apart from the low-voltage terminals (ESTIMATE ≈ INR 3.5 per pole)", 84),
        ("RS-485, isolated as standard (owner, 2026-11-19): Chipanalog CA-IS2092W with integrated isolated DC-DC (LCSC ≈ USD 1.4–2.5; ESTIMATE ≈ 180), SM712 TVS, series PTC, termination switch", 217),
        ("CAN-FD, isolated as standard (owner, 2026-11-19): Chipanalog CA-IS2062A (CAN FD ≤ 5 Mbps, integrated isolated DC-DC; ESTIMATE ≈ 180), protection, switchable termination, 3-pole terminal", 216),
        ("USB-C service port + LEDs", 23),
        ("4-pin bus connectors, bridge share, bus RS-485 transceiver, ESD (ESTIMATE)", 59),
        ("36 fixed 3.81 mm screw terminals, shared analog common (ESTIMATE ≈ INR 2 per pole)", 74),
        ("PCB 4-layer", 103),
        ("Power stage on the module PCB (owner, 2026-11-19: no separate DC-DC board): buck 5–32 V → 5 V (TI LMR51420 / SY8xxx class) + 3.3 V LDO ≈ 45; TVS, reverse FET, PTC fuse, Schottky OR with BUS_V ≈ 40 (ESTIMATE)", 85),
        ("Passives", 79),
        ("Status LED on each of the 28 field IO channels: 6 AI, 10 DI, 8 relays, 4 high-side (ESTIMATE ≈ INR 1.5 each)", 42),
        ("Enclosure 90 mm DIN-rail (8 relays + 4 high-side outputs need the width), Indian ABS, V-0 for mains-switching relays (ESTIMATE)", 210)]),
    "eth": ("Ethernet option on baseboard", [
        ("LAN8742AI + Würth RJ45 + ESD + passives (R11)", 913)]),
    "se": ("Secure element option (D-16)", [
        ("NXP SE050E (UNVERIFIED)", 260)]),
    "4g0": ("4G card, Tier 0 — very low cost: Cat 1 with built-in GPS, no RJ45", [
        ("Tier 1 card as costed (R17 basis), incl. its power stage", 2335),
        ("Quectel EC200U-CN with built-in GNSS (4G + GPS in one module, ≈ 850, India reseller prices; ESTIMATE, quote needed) instead of EC200A (1,300) — owner target < INR 1,000, 2026-11-19", -450),
        ("No Ethernet PHY + crystal", -60),
        ("No own RJ45: magnetics + jack + ESD", -156),
        ("GNSS antenna + SMA for the built-in GPS (ESTIMATE)", 130)]),
    "4g": ("4G modem card — LTE Cat 1 + GPS (Quectel EC200U-CN)", [
        ("Quectel EC200U-CN with built-in GNSS: 4G + GPS in one module (India reseller prices; ESTIMATE, quote needed; owner target < INR 1,000)", 850),
        ("SIM holder, LTE SMA + pigtail, bus headers, PCB, 3.8 V modem buck + ≥ 1000 µF (R17 basis, ESTIMATE)", 604),
        ("Power stage on the module PCB: buck 5–32 V → 5 V + 3.3 V LDO, TVS, reverse FET, PTC fuse, Schottky OR (ESTIMATE)", 85),
        ("GNSS antenna + SMA (ESTIMATE)", 130),
        ("Enclosure 45 mm, Indian ABS (R14)", 130)]),
    "4g_noeth": ("4G modem card without Ethernet — difference", [
        ("No Ethernet PHY + crystal", -60),
        ("No own RJ45: magnetics + jack + ESD", -156)]),
    "4g_gnss": ("GNSS option on 4G card (R17)", [
        ("LC29HAIMD GPS + NavIC receiver, antenna, SMA, support parts (R17)", 1320)]),
    "wifi": ("Wi-Fi + BLE module", [
        ("ESP32-C6-MINI-1-N4, PCB antenna (R03)", 313),
        ("Power stage on the module PCB (owner, 2026-11-19: no separate DC-DC board): buck 5–32 V → 5 V (TI LMR51420 / SY8xxx class) + 3.3 V LDO ≈ 45; TVS, reverse FET, PTC fuse, Schottky OR with BUS_V ≈ 40 (ESTIMATE)", 85),
        ("4-pin bus connectors + bridge share + RS-485 bus transceiver + ESD (ESTIMATE)", 58),
        ("PCB 4-layer, passives, LEDs", 130),
        ("Enclosure 45 mm, Indian ABS (R14)", 130),
        ("Node IO: 6 DI opto, 4 DO high-side + watchdog, 4 AI on ESP32-C6 ADC, terminals (ESTIMATE)", 514),
        ("RS-485 + CAN 2.0, both isolated as standard (owner, 2026-11-19): CA-IS2092W + CA-IS2062A with integrated isolated DC-DC, protection, IO expander, terminals (ESTIMATE)", 558),
        ("Status LED on each of the 16 field IO channels (owner, 2026-11-19; ESTIMATE ≈ INR 1.5 each)", 24),
        ("2 relay outputs (owner, 2026-11-20): SPDT 10 A, 230 VAC / 30 VDC, 5 V coil, Hongfa / Omron / Panasonic 5 kV, INR 40 each at volume (owner, 2026-11-22), driver, 10 A fuse each in a front-access holder at INR 20 (owner, 2026-11-22), 6 terminal poles 300 V (ESTIMATE)", 150)]),
    "lora": ("LoRa module — remote IO node (owner, 2026-11-19)", [
        ("STM32WLE5CCU6 at INR 250 (owner target, high volume, to be negotiated) + TCXO + RF switch + matching; +22 dBm high-power PA (ESTIMATE ≈ 50)", 300),
        ("Power stage on the module PCB: buck 5–32 V → 5 V + 3.3 V LDO, TVS, reverse FET, PTC fuse, Schottky OR (ESTIMATE)", 85),
        ("External antenna + SMA for long range (owner: \"high throughput long range\")", 78),
        ("4-pin bus connectors + bridge share + RS-485 bus transceiver + ESD (ESTIMATE)", 59),
        ("PCB 2-layer (was 4-layer), passives (ESTIMATE)", 78),
        ("Enclosure 45 mm, Indian ABS at the volume-quote target (ESTIMATE)", 100),
        ("Node IO, standard, inputs only: RS-485 + 4 DI (single optocouplers) + 4 AI 0–10 V / 4–20 mA (shared front end), fixed terminals; no DO (ESTIMATE)", 215),
        ("4 DO 24 V high-side (owner, 2026-11-19: remote switching, low power — no relays): 1× TI TPS274160B quad (LCSC USD 1.53 at 100), µA standby, loads fed from the field 24 V, watchdog gating, TVS, terminals; no IO LEDs (ESTIMATE)", 194)]),
    "pwr": ("Power stage — now on every module PCB (no separate board)", [
        ("Counted in each module", 0)]),
    "base_pic": ("STM32H573VIT6 instead of PIC32CK — Fieldbus controller, difference", [
        ("STM32H573VIT6 (LQFP100, PSA L3, Zephyr-ready; own layout) instead of PIC32CK2051SG01100 — ESTIMATE: LCSC USD 7.63 vs RS £3.61 at ≈ 100; quote needed", 265)]),
    "fb_removed": ("Fieldbus module (removed)", [
        ("STM32G0B1 (R05)", 195),
        ("Isolated CAN-FD + RS-485, isolated DC-DC, port protection (R05, no Mornsun)", 429),
        ("Power block, TI tier (R06)", 364),
        ("Bus receptacles + bridge plug (R07 est.)", 520),
        ("PCB, misc.", 182),
        ("Enclosure 22.5 mm (UNVERIFIED)", 195)]),
    "base_noeth": ("Fieldbus controller without Ethernet — difference", [
        ("No PHY + crystal, magnetics + RJ45, ESD", -270)]),
    "t2": ("Tier-2 4G router — MP135F + Zephyr companion MCU (R20)", [
        ("STM32MP135FAE7 (1 GHz secure) + STM32H533 companion, DDR3L, SPI-NAND, EC200A, Wi-Fi, 2× Ethernet, isolated RS-485, DI/DO, aluminium case (R20)", 7615)]),
    "t2lite": ("Tier-2 4G router — Lite (R18)", [
        ("No Wi-Fi, plastic case, non-isolated RS-485 (R18)", 5558)]),
    "t2gnss": ("Tier-2 4G router — GNSS + vehicle power (R18)", [
        ("Base + L89HA GPS/NavIC + ignition + load-dump front end (R18)", 8393)]),
    "batt": ("Battery + charger board — optional, one per module (PWR-2)", [
        ("TI BQ25601 charger: power path, no-dropout backup, NTC / JEITA, I²C status, 5 V boost (LCSC USD 0.60 at 100)", 53),
        ("Cell protector + inductor + passives (ESTIMATE)", 20),
        ("18650 holder + small PCB + connector (ESTIMATE)", 32),
        ("18650 Li-ion cell ≈ 3000 mAh, BIS IS 16046 registered (owner: under INR 100)", 100)]),
    "rut": ("4G industrial router — RUT200 class (MT7628 + EC200A + OpenWrt)", [
        ("MediaTek MT7628AN router SoC: 580 MHz MIPS, 2.4 GHz 2×2 Wi-Fi 4 and 5-port 10/100 switch on chip (R09, R16)", 275),
        ("128 MB DDR2 + 16 MB SPI NOR (RUT200 sizes; DDR2 prices up in 2026, R18)", 450),
        ("SoC power, crystals, Wi-Fi RF matching + U.FL (R18)", 150),
        ("Quectel EC200A-CN LTE Cat 4 on USB, as in the RUT200 (R16)", 1300),
        ("Modem 3.8 V buck + bulk, USB ESD, SIM holder + ESD (R18)", 175),
        ("2× RJ45 with magnetics (Würth / HanRun, < INR 100 each, owner) + ESD", 230),
        ("Power input 9–30 V: fuse, TVS, reverse FET, buck to 5 V (R18)", 215),
        ("1 DI + 1 DO (as RUT200), LEDs, reset button", 100),
        ("SMA ×3 + pigtails; antennas in the box: 2× LTE + 1× Wi-Fi (R18)", 440),
        ("PCB 4-layer ≈ 100 × 80 mm, passives", 240),
        ("Enclosure DIN / wall, plastic V-0 (aluminium ≈ +250); packaging, power pigtail, label", 200)]),
    "adapter": ("Adapter 12 V 18 W, one per gateway or standalone module (bought in)", [
        ("Certified 12 V 18 W adapter (UNVERIFIED)", 520)]),
}


def bom(k):
    vals = [v for _, v in BOM[k][1]]
    return None if any(v is None for v in vals) else sum(vals)



ROY_FIXED = {"4g0": 750, "wifi_lean": 200, "lora_lean": 100, "t2": 750, "t2lite": 750, "t2gnss": 750, "base": 750, "4g": 750, "rut": 750, "4g2g": 750, "lora": 200, "lorac": 100, "wifi": 200}  # owner, 2026-11-14: flat royalties (INR)
ROY_NONE = {"eth", "se", "base_noeth", "4g_gnss", "batt", "adapter", "adapter_m", "pwr", "base_pic", "4g_noeth"}  # hardware-only options and the bought-in adapter


def build_keys(keys):
    t = [0.0] * 6
    for k in keys:
        b = bom(k)
        if b is None:
            return None
        mfg = b * MFG
        cost = b + mfg
        roy = ROY_FIXED.get(k, 0.0 if k in ROY_NONE else cost * ROY)
        prof = (cost + roy) * PROFIT
        for i, v in enumerate((b, mfg, cost, roy, prof, cost + roy + prof)):
            t[i] += v
    return t


def inr(v):
    return f"{v:,.0f}"


MODS = [("base", "Fieldbus controller", "mcu"), ("4g", "4G modem card", "radio"),
        ("wifi", "Wi-Fi + BLE", "eth"), ("lora", "LoRa", "io")]
HEADS = {"base": "Fieldbus\ncontroller", "4g": "4G modem\n+ GPS",
         "wifi": "Wi-Fi +\nBLE", "lora": "LoRa", "pwr": "DC-DC\nboard", "batt": "Battery +\ncharger", "adapter": "Adapter\n12 V 18 W"}
# side-by-side versions (owner, 2026-11-19): column id -> BOM keys
COLKEYS = {"base": ["base"], "4g": ["4g"],
           "wifi": ["wifi"], "lora": ["lora"], "batt": ["batt"], "adapter": ["adapter"]}
COLKIND = {"base": "mcu", "4g": "radio", "wifi": "eth", "lora": "io", "pwr": "power", "batt": "power"}
MODCOL = {"base": "base", "4g": "4g", "wifi": "wifi", "lora": "lora"}   # version used in the combination rows
ROY_INITIAL, INITIAL_N = 2000, 20   # owner, 2026-11-19: firmware royalty INR 2,000 per device for the first 20 devices of every module
TARGET = {"lora": 1600}   # owner, 2026-11-19: LoRa module selling price (price after profit, without battery board and adapter)
# price break-up segments: grey = what it costs us, amber = what we keep
SEGS = [("BOM (100 pcs)", 0, "#33414f"), ("Mfg, packing, logistics 50 %", 1, "#8fa1b3"),
        ("Firmware royalty", 3, "#c46a00"), ("Profit 30 %", 4, "#e9b872")]
HDR, BAND, GRID, MUTED, ALT, HI, SUB = "#23303d", "#e1e7ee", "#c9d0d8", "#8a96a3", "#f6f8fa", "#e8f0fb", "#4a5560"
PRE = "#fbf1e2"   # highlight for "price before profit"
# Fieldbus controller cost-down, owner request 2026-11-19 ("reduce it by 30 %"); savings at 100 units, INR
COSTDOWN = [("Fixed 3.81 mm screw terminals instead of pluggable (incl. CAN port)", 155, "owner"),
            ("10 single optocouplers instead of 3× TLP293-4 quads", 95, "applied"),
            ("TPS2H160 dual for outputs 9–10 instead of a third quad switch", 60, "applied"),
            ("Lower-cost 0.1 % 2.5 V reference instead of LM4040", 35, "applied"),
            ("Shared analog common: 35 → 32 terminal poles", 19, "applied"),
            ("64 Mbit instead of 128 Mbit QSPI NOR", 17, "applied"),
            ("PIC32CK2051SG01 instead of STM32H533 (owner, standard for now; ESTIMATE)", 56, "applied"),
            ("Power stage on the module PCB (≈ 85) instead of the plug-in power module (390); USB-C PD dropped", 305, "applied")]
DECLINED = [("8 DO instead of 10", 92)]


def num(v):
    return ("−" + inr(-v)) if v < -0.5 else inr(v)


def pct(v):
    return f"{v:.0f}".replace("-", "−") + " %"


def table_tools(pg):
    def put(x, w, y, s, h=22, size=10.5, weight="normal", anchor="end", fill=INK):
        tx = {"end": x + w - 8, "start": x + 8, "middle": x + w / 2}[anchor]
        pg.text(tx, y + h / 2 + 4, s, size, weight, anchor, fill)

    def header(x, y, cols, h=36):
        pg.rect(x, y, sum(c[1] for c in cols), h, HDR, HDR, rx=0)
        cx = x
        for name, cw, anc in cols:
            lines = name.split("\n")
            for k, ln in enumerate(lines):
                tx = {"end": cx + cw - 8, "start": cx + 8, "middle": cx + cw / 2}[anc]
                pg.text(tx, y + h / 2 + 4 - (len(lines) - 1) * 6.5 + k * 13, ln, 10.5, "bold", anc, "#ffffff")
            cx += cw
        return y + h

    return put, header


def page4():
    """One page: price build-up per module, options, and all 15 combinations with their break-up."""
    from itertools import combinations
    pg = Page("Prices — every combination, 100 pieces",
              "INR per unit at 100 units. Every module includes its own power stage (buck regulator + input protection, PWR-10); the battery + charger board is optional, one per module. "
              "The adapter is separate. BOMs are research-based estimates (R02–R22), no quotes yet — treat as ±25 %. ")
    put, header = table_tools(pg)
    keys = [k for k, _, _ in MODS]
    order = list(COLKEYS)
    r = {k: build_keys(COLKEYS[k]) for k in order}
    for m, c in MODCOL.items():
        r[m] = r[c]
    pre = {k: r[k][2] + r[k][3] for k in order}

    # ---------------- 1 · build-up per item (left)
    x1, lw, vw = 40, 214, 90
    t1w = lw + len(order) * vw
    y = 146
    pg.text(x1, y - 10, "1 · Price build-up per item", 14, "bold")
    y = header(x1, y, [("Step", lw, "start")] + [(HEADS[k], vw, "end") for k in order])
    for j, k in enumerate(order):                     # colour key, matches the blocks in section 2
        kind = COLKIND.get(k)
        if kind:
            pg.rect(x1 + lw + j * vw, y - 4, vw, 4, COL[kind][1], COL[kind][1], rx=0, sw=0)
    steps = [("BOM (100 pcs)", 0), ("+ Mfg, packing, logistics 50 %", 1), ("= Cost", 2), ("+ Firmware royalty", 3),
             ("= Price before profit", "pre"), ("+ Profit 30 %", 4), ("= Price after profit (ex-works)", 5),
             ("First 20 devices: royalty INR 2,000 instead", "roy20"), ("= Price after profit, first 20 devices", "p20"),
             ("Target selling price (owner)", "target")]
    for i, (lab, idx) in enumerate(steps):
        strong = idx in (5, "pre")
        fill = HI if idx == 5 else PRE if idx == "pre" else (ALT if i % 2 == 0 else "#ffffff")
        pg.rect(x1, y, t1w, 22, fill, GRID, rx=0, sw=0.8)
        put(x1, lw, y, lab, weight="bold" if strong else "normal", anchor="start",
            fill="#b32f2f" if idx == "target" else INK)
        for j, k in enumerate(order):
            if idx in ("roy20", "p20"):
                if k in ("pwr", "batt", "adapter"):
                    put(x1 + lw + j * vw, vw, y, "—", fill=MUTED)
                else:
                    v = ROY_INITIAL if idx == "roy20" else (r[k][2] + ROY_INITIAL) * (1 + PROFIT)
                    put(x1 + lw + j * vw, vw, y, inr(v), weight="bold" if idx == "p20" else "normal", fill="#c46a00")
                continue
            if idx == "target":
                v = TARGET.get(k)
                s, col = (inr(v), "#b32f2f") if v else ("—", MUTED)
                put(x1 + lw + j * vw, vw, y, s, weight="bold" if v else "normal", fill=col)
                continue
            v = pre[k] if idx == "pre" else r[k][idx]
            s = "—" if abs(v) < 0.5 else num(v)
            put(x1 + lw + j * vw, vw, y, s, weight="bold" if strong else "normal", fill=MUTED if s == "—" else INK)
        y += 22
    t1_end = y

    # ---------------- options (right)
    xa = x1 + t1w + 40
    aw = W - 40 - xa
    ya = 146
    pg.text(xa, ya - 10, "Options — add to any row that contains the module", 14, "bold")
    acols = [("Option", aw - 150 - 112, "start"), ("Fits", 150, "start"), ("After profit", 112, "end")]
    ya = header(xa, ya, acols)
    acc = [("STM32H573 instead of PIC32CK (quote needed)", "Fieldbus controller", build_keys(["base_pic"])),
           ("Battery + charger board with 18650 cell", "Per module", build_keys(["batt"]))]
    for i, (lab, fits, v) in enumerate(acc):
        pg.rect(xa, ya, aw, 22, ALT if i % 2 == 0 else "#ffffff", GRID, rx=0, sw=0.8)
        put(xa, acols[0][1], ya, lab, anchor="start")
        put(xa + acols[0][1], acols[1][1], ya, fits, anchor="start", fill=SUB)
        put(xa + acols[0][1] + acols[1][1], acols[2][1], ya, ("+" if v[5] > 0 else "") + num(v[5]), weight="bold")
        ya += 22


    # ---------------- 2 · all 15 combinations, one row each, with the full break-up
    y = t1_end + 44
    pg.text(40, y - 10, "2 · All 15 combinations — battery boards and adapter not included", 14, "bold")
    lx = W - 40                                       # colour legend for the bar, right-aligned on the title line
    for lab, _, colr in reversed(SEGS):
        lx -= len(lab) * 10.5 * CW
        pg.text(lx, y - 10, lab, 10.5, fill=SUB)
        lx -= 17
        pg.rect(lx, y - 20, 12, 12, colr, colr, rx=2, sw=0)
        lx -= 22
    SLOT = 132
    w_mod = 12 + SLOT * len(MODS)
    ncols = [("BOM", 92), ("+ Mfg, packing,\nlogistics 50 %", 112), ("= Cost", 92), ("+ Firmware\nroyalty", 90),
             ("= Price before\nprofit", 112), ("+ Profit\n30 %", 88), ("= Price after\nprofit", 120)]
    w_bar = (W - 80) - w_mod - sum(w for _, w in ncols)
    cols = [("Modules in the stack", w_mod, "start"),
            ("Break-up (bar = price after profit)", w_bar, "start")] + [(n, w, "end") for n, w in ncols]
    xs = [40]
    for _, w, _ in cols:
        xs.append(xs[-1] + w)
    y = header(40, y, cols, h=40)
    top = y
    combos = [c for n in range(1, len(keys) + 1) for c in combinations(keys, n)]
    vals = {c: build_keys([x for m in c for x in COLKEYS[MODCOL[m]]] ) for c in combos}
    vmax = max(v[5] for v in vals.values())
    bw = w_bar - 20
    rh = 30
    groups = [(1, "One module — works standalone"), (2, "Two modules"), (3, "Three modules"),
              (4, "All four modules — full gateway")]
    pcol = COL["power"]
    for size, title in groups:
        pg.rect(40, y, W - 80, 24, BAND, GRID, rx=0, sw=0.8)
        pg.text(48, y + 16, title, 11, "bold", fill=HDR)
        y += 24
        for i, c in enumerate([c for c in combos if len(c) == size]):
            v = vals[c]
            pg.rect(40, y, W - 80, rh, ALT if i % 2 else "#ffffff", GRID, rx=0, sw=0.8)
            pg.rect(xs[6], y, ncols[4][1], rh, PRE, GRID, rx=0, sw=0.8)
            pg.rect(xs[8], y, ncols[6][1], rh, HI, GRID, rx=0, sw=0.8)
            for j, (k, name, kind) in enumerate(MODS):
                sx = 48 + j * SLOT
                if k in c:
                    fill, stroke = COL[kind]
                    pg.rect(sx, y + 4, SLOT - 8, rh - 8, fill, stroke, rx=5, sw=1.3)
                    pg.text(sx + 7, y + 13, {"base": "Fieldbus controller", "4g": "4G modem + GPS"}.get(k, name), 9.5, "bold", fill=stroke)
                    pg.text(sx + 7, y + 23, f"{inr(r[k][5])} after profit", 9, fill=SUB)
                else:
                    pg.rect(sx, y + 4, SLOT - 8, rh - 8, "none", "#d5dbe2", rx=5, sw=1, dash=True)
            bx = xs[1] + 10
            for _, idx, colr in SEGS:
                seg = bw * v[idx] / vmax
                pg.rect(bx, y + 9, seg, 12, colr, colr, rx=0, sw=0)
                bx += seg
            row = [v[0], v[1], v[2], v[3], v[2] + v[3], v[4], v[5]]
            for j, val in enumerate(row):
                strong = j in (4, 6)
                put(xs[2 + j], ncols[j][1], y, inr(val), h=rh, size=12 if j == 6 else 10.5,
                    weight="bold" if strong else "normal")
            for xx in (xs[1], xs[2]):
                pg.line(xx, y, xx, y + rh, "#5a6470", 1.2)
            y += rh
    pg.rect(40, top - 40, W - 80, y - top + 40, "none", "#5a6470", rx=0, sw=1.2)
    pg.para(40, y + 22, W - 80, [
        f"Adapter not included: add one 12 V 18 W adapter per stack or standalone module — {inr(pre['adapter'])} before profit, "
        f"{inr(r['adapter'][5])} after profit. Options add their price to any row that contains their module.",
        f"Each module has its own power stage on its PCB (≈ INR 85 BOM: buck regulator + input protection). Battery + charger board optional, {inr(r['batt'][5])} after profit per module. "
        "Firmware royalty per module — INR 2,000 for each of the first 20 devices of every module (owner, 2026-11-19), then 750 Fieldbus controller, 750 4G modem card, 200 Wi-Fi + BLE, 200 LoRa; "
        "none on the battery board, adapter or options. The rows below use the royalty after the first 20 devices.",
        "Not included: development amortisation (NRE) and distributor margin — see page 5."], 10.5, fill=SUB, bullet=True)
    pg.save("UC_Architecture_p4_Pricing.svg")


def page5():
    """BOM basis: the research line items behind every price on page 4, the Fieldbus cost-down, notes."""
    pg = Page("BOM basis — what the prices are built from",
              "Line items at 100 units, INR — estimates from research R02–R22 (research price × 1.3 until 100-unit quotes exist); "
              "ESTIMATE / UNVERIFIED items still need a quote. Fieldbus controller after the 2026-11-19 cost-down.")
    put, header = table_tools(pg)
    gap, lh, fs = 24, 13, 10
    cw = (W - 80 - 2 * gap) / 3

    def item_lines(k):
        return [wrap(lab, cw - 90, fs) for lab, _ in BOM[k][1]]

    def card_h(k):
        return 64 + sum(len(p) * lh + 4 for p in item_lines(k))

    def card(x, y, k, name, kind):
        fill, stroke = COL[kind]
        h = card_h(k)
        pg.rect(x, y, cw, h, "#ffffff", stroke, rx=0, sw=1.4)
        pg.rect(x, y, cw, 28, fill, stroke, rx=0, sw=1.4)
        pg.text(x + 10, y + 19, name, 12, "bold", fill=stroke)
        pg.text(x + cw - 10, y + 19, f"BOM {inr(bom(k))}", 10.5, "bold", "end", fill=stroke)
        yy = y + 45
        for (lab, v), parts in zip(BOM[k][1], item_lines(k)):
            for i, ln in enumerate(parts):
                pg.text(x + 10, yy + i * lh, ln, fs)
            pg.text(x + cw - 10, yy, num(v), fs, anchor="end")
            yy += len(parts) * lh + 4
        pg.line(x + 8, yy - 8, x + cw - 8, yy - 8, GRID, 1)
        pg.text(x + 10, yy + 8, "Total", fs, "bold")
        pg.text(x + cw - 10, yy + 8, inr(bom(k)), fs, "bold", "end")
        return y + h

    y0 = 118
    columns = [[("base", "Fieldbus controller — with Ethernet", "mcu")],
               [("4g", "4G modem card", "radio"), ("wifi", "Wi-Fi + BLE", "eth")],
               [("lora", "LoRa", "io"), ("batt", "Battery + charger board — optional, per module", "power")]]
    bottom = y0
    for i, col in enumerate(columns):
        yy = y0
        for k, name, kind in col:
            yy = card(40 + i * (cw + gap), yy, k, name, kind) + 14
        bottom = max(bottom, yy)

    # ---------------- options and the adapter
    y = bottom + 18
    pg.text(40, y, "Options and the adapter", 14, "bold")
    y += 10
    acols = [("Item", 330, "start"), ("What is in it — line items", W - 80 - 330 - 3 * 110, "start"),
             ("BOM", 110, "end"), ("Before profit", 110, "end"), ("After profit", 110, "end")]
    y = header(40, y, acols, h=30)
    dw = acols[1][1]
    t0_items = [it for it in BOM["4g0"][1] if not it[0].startswith("Tier 1 card")]
    accs = [("STM32H573 alternative — Fieldbus controller", BOM["base_pic"][1], build_keys(["base_pic"])),
            ("Adapter 12 V 18 W — one per stack, bought in", BOM["adapter"][1], build_keys(["adapter"]))]
    for i, (lab, items, v) in enumerate(accs):
        parts = wrap("; ".join(f"{l} — {num(x)}" for l, x in items), dw - 16, fs)
        h = 20 + (len(parts) - 1) * lh
        pg.rect(40, y, W - 80, h, ALT if i % 2 == 0 else "#ffffff", GRID, rx=0, sw=0.8)
        pg.text(48, y + 14, lab, fs, "bold")
        for j, ln in enumerate(parts):
            pg.text(40 + acols[0][1] + 8, y + 14 + j * lh, ln, fs)
        for j, val in enumerate((v[0], v[2] + v[3], v[5])):
            pg.text(40 + acols[0][1] + dw + (j + 1) * 110 - 8, y + 14, num(val), fs, "bold" if j == 2 else "normal", "end")
        y += h

    # ---------------- bottom: Fieldbus cost-down log (left) and notes (right)
    y += 34
    lw_ = 860
    pg.text(40, y, "Fieldbus controller cost-down — owner request 2026-11-19 (−30 % asked), like for like without Ethernet", 14, "bold")
    ty = header(40, y + 10, [("Change", lw_ - 200, "start"), ("Saving", 110, "end"), ("Status", 90, "start")], h=28)
    for i, (lab, sav, st) in enumerate(COSTDOWN):
        pg.rect(40, ty, lw_, 20, ALT if i % 2 == 0 else "#ffffff", GRID, rx=0, sw=0.8)
        put(40, lw_ - 200, ty, lab, h=20, size=fs, anchor="start")
        put(40 + lw_ - 200, 110, ty, "−" + inr(sav), h=20, size=fs, weight="bold")
        put(40 + lw_ - 90, 90, ty, "your call" if st == "owner" else "applied", h=20, size=fs, anchor="start",
            fill="#c46a00" if st == "owner" else SUB)
        ty += 20
    tot = sum(s for _, s, _ in COSTDOWN)
    enc = [v for l, v in BOM["base"][1] if l.startswith("Enclosure")][0]   # enclosure added 2026-11-19, not in the 2,626 basis
    before, after = 2626, bom("base") + bom("base_noeth") + bom("pwr") - enc   # like for like, without Ethernet; 2,626 = Draft C incl. power
    pg.rect(40, ty, lw_, 22, HI, GRID, rx=0, sw=0.8)
    put(40, lw_ - 200, ty, f"Total: {inr(before)} → {inr(after)} incl. power, excl. enclosure ({pct((after - before) / before * 100)})",
        size=fs, weight="bold", anchor="start")
    put(40 + lw_ - 200, 110, ty, "−" + inr(tot), size=fs, weight="bold")
    ty += 22
    dec = sum(s for _, s in DECLINED)
    pg.para(40, ty + 16, lw_, ["Declined by the owner: " + ", ".join(f"{n} −{s}" for n, s in DECLINED)
                               + f" — together −{dec} more, which would reach {pct((after - dec - before) / before * 100)}."], fs, fill=SUB)

    nx = 40 + lw_ + 40
    pg.text(nx, y, "Notes", 14, "bold")
    lora_ceiling = (TARGET["lora"] / (1 + PROFIT) - ROY_FIXED["lora"]) / (1 + MFG)
    notes = [
        f"LoRa selling price INR 1,600 (owner, 2026-11-19), read as price after profit without battery board and adapter: needs a BOM of ≤ INR {inr(lora_ceiling)} "
        f"at 100 pcs, now {inr(bom('lora'))} — a {pct((1 - lora_ceiling / bom('lora')) * 100)} cut.",
        f"With Ethernet, incl. power stage and enclosure: {inr(bom('base'))} (limit INR 2,000: {'within' if bom('base') + bom('pwr') <= 2000 else 'over by ' + inr(bom('base') + bom('pwr') - 2000)}); the version without Ethernet is dropped (owner, 2026-11-19).",
        "PIC32CK2051SG01 is the standard MCU for now (owner, 2026-11-19). Open points: no PSA / SESIP certificate (BASE-1 not met); Zephyr has no PIC32CK Ethernet, CAN or ADC driver yet (R12) — "
        "drivers to write or ThreadX; STM32H573 stays as the alternative.",
        f"LoRa redesigned as a remote IO node (owner, 2026-11-19): STM32WLE5 at INR 250, 2-layer PCB, no external flash, RS-485 + 4 DI + 4 AI + 4 DO (low-power high-side quad), "
        f"SMA antenna kept for long range — BOM {inr(bom('lora'))}. Tip: volume quotes (≈ −10 %) → ≈ {inr(bom('lora') * 0.9)}; no relays: their coils would drain the battery.",
        "Tip — every module: this is a high-volume product, so negotiate the big parts with distributors (modem, ESP32-C6 module, MCUs, isolated transceivers, enclosures); "
        "the BOMs here are still research prices × 1.3 at 100 units.",
        "Adapter (owner, 2026-11-18): one 12 V 18 W adapter per stack or standalone module; a full 4-module stack peaks at ≈ 13–14 W with charging capped at 0.3 A per battery board.",
        "Not included: development amortisation — at 100 pieces every INR 1 lakh of NRE per module type adds INR 1,000 to its cost and ≈ INR 1,300 "
        "to its price after profit; distributor margin (left to the client / partner).",
    ]
    pg.para(nx, y + 22, W - 40 - nx, notes, fs, bullet=True)
    pg.save("UC_Architecture_p5_BOM_Basis.svg")


# ---------------------------------------------------------------- page 6
def page6():
    pg = Page("Software and security architecture",
              "Firmware on each unit, protocols, IO sharing, updates and the security model. Internal reference — not part of the customer spec sheet.")
    pg.p.append('<g transform="translate(0,24)">')
    x0, y0 = 40, 112
    pg.text(x0, y0 - 8, "Firmware per unit", 15, "bold")
    units = [
        ("Fieldbus-controller module (coordinator when fitted)", "mcu", ["Zephyr RTOS (LTS) on STM32H533 / H573", "TF-M secure world: keys, crypto, attestation (PSA L3)", "MCUboot: signed + encrypted A/B images, anti-rollback",
                                          "IO server, Modbus RTU / TCP, CAN-FD (J1939, CANopen), MQTT / HTTPS client, update orchestrator for all modules"]),
        ("Wi-Fi + BLE module", "radio", ["Zephyr on ESP32-C6", "Secure Boot v2, flash encryption, JTAG disabled by eFuse", "Network co-processor: carries encrypted traffic only"]),
        ("LoRa module", "radio", ["Zephyr on STM32WLE5", "LoRaWAN 1.0.4 Class A / private star network; firmware enforces India e.r.p. and duty limits", "Node IO: RS-485 + 4 DI + 4 DO + 4 AI"]),
        ("4G modem card (Tier 1)", "radio", ["Quectel standard firmware only — no code of ours", "Quectel FOTA for modem updates", "Untrusted pipe: TLS ends in the coordinator (SEC-8)"]),
        ("4G router (Tier 2, standalone)", "eth", ["Linux: Yocto or OpenWrt (R18)", "Secure boot, signed A/B updates (SWUpdate / RAUC or sysupgrade), CIP / LTS kernel", "Router functions: NAT, firewall, VPN, web UI"]),
    ]
    y = y0 + 8
    for name, kind, lines in units:
        y = pg.block(x0, y, 760, kind, name, lines, size=11) + 10

    rx = 840
    pg.text(rx, y0 - 8, "Functions", 15, "bold")
    rows = [
        ("Operating system", "Zephyr RTOS on the Fieldbus controller, Wi-Fi + BLE and LoRa modules, with long-term security maintenance; Quectel firmware on the Tier-1 4G card; Linux only in the Tier-2 router"),
        ("Field protocols", "Modbus RTU and Modbus TCP (master and slave); J1939 and CANopen; LoRaWAN; DLMS client planned"),
        ("Cloud", "MQTT over TLS, HTTPS (JSON), several servers in parallel, SMS alarms, NTP time sync"),
        ("Shared IO", "All controller IO is available to every module; each output has one authorised owner and falls to a safe state on any fault (IO-6, page 2)"),
        ("Updates", "Signed, encrypted over-the-air updates with automatic rollback; the coordinator orchestrates updates for every module"),
        ("Security", "Hardware root of trust, secure boot, unique device identity, mutually authenticated TLS, module authentication, locked debug ports, no default passwords, published vulnerability-handling process"),
    ]
    ty = y0 + 8
    kw, vw = 170, W - 40 - rx - 170
    for k, v in rows:
        n = len(wrap(v, vw - 14, 11))
        rh = n * 15 + 14
        pg.rect(rx, ty, kw, rh, "#eef2f6", "#c9d0d8", rx=0, sw=0.8)
        pg.rect(rx + kw, ty, vw, rh, "#ffffff", "#c9d0d8", rx=0, sw=0.8)
        pg.text(rx + 8, ty + 18, k, 11.5, "bold")
        pg.para(rx + kw + 8, ty + 18, vw - 14, [v], 11, lh=15)
        ty += rh
    ty += 30
    pg.text(rx, ty, "Security lifecycle (SEC-8 to SEC-10)", 15, "bold")
    life = [
        "The coordinator is the trusted element; TLS terminates in it (Fieldbus controller TrustZone, PSA L3; else ESP32-C6, PSA L2); radio modules only carry encrypted traffic.",
        "Modules are enrolled with a key at manufacture and authenticated before they get IO access.",
        "Support period at least 5 years; SBOM per release; CVE monitoring of Zephyr, Mbed TLS, ESP-IDF, vendor HALs and the Quectel firmware.",
        "Security contact and coordinated disclosure; CRA incident reporting (24 h / 72 h) in the global phase.",
        "Secure development process to IEC 62443-4-1; product targets IEC 62443-4-2 SL2 and EN 18031.",
        "Reuse open-source security components: Zephyr, MCUboot, TF-M, Mbed TLS / PSA Crypto, Eclipse hawkBit; on Linux: Yocto meta-security, OP-TEE, CIP kernel, SWUpdate / RAUC.",
    ]
    pg.para(rx, ty + 22, W - 40 - rx, life, 11, bullet=True)
    pg.p.append("</g>")
    pg.save("UC_Architecture_p6_Software_Security.svg")



# ---------------------------------------------------------------- page 7
def page7():
    """RUT200-class 4G industrial router (owner, 2026-11-19: "give me a true RUT200 type router")."""
    pg = Page("4G industrial router — RUT200 class",
              "Separate product beside the module family (owner, 2026-11-19): the RUT200 pattern — MediaTek MT7628 router SoC + Quectel EC200A on USB + OpenWrt. "
              "Prices at 100 units; BOM lines are ESTIMATES from R16 / R18, quotes needed.")
    put, header = table_tools(pg)
    x0, y0 = 40, 118
    ew = 560
    # ---- front view
    pg.text(x0, y0 + 4, "Front view", 15, "bold")
    fy = y0 + 40
    for k, lab in enumerate(["LTE main", "LTE div", "Wi-Fi"]):
        cx = x0 + 90 + k * 150
        pg.rect(cx - 8, fy - 4, 16, 26, "#d4a017", "#8a6a00", rx=2, sw=1)
        pg.text(cx, fy - 10, lab, 9.5, "bold", "middle", fill="#8a6a00")
    pg.rect(x0, fy + 22, ew, 300, "#e9edf1", "#23303d", rx=10, sw=2.4)
    pg.rect(x0 + 10, fy + 36, ew - 20, 60, "#23303d", "#23303d", rx=4)
    pg.text(x0 + 22, fy + 62, "4G INDUSTRIAL ROUTER", 15, "bold", fill="#ffffff")
    pg.text(x0 + 22, fy + 84, "LTE Cat 4 · Wi-Fi 4 · 2 × Ethernet · 1 DI / 1 DO · 9–30 V", 11, fill="#cfd8e2")
    for k, (lab, col) in enumerate([("PWR", "#2ecc71"), ("LTE", "#3498db"), ("SIG", "#3498db"), ("WIFI", "#9b59b6"), ("WAN", "#e67e22"), ("LAN", "#e67e22")]):
        lx = x0 + 22 + k * 86
        pg.p.append(f'<circle cx="{lx + 5}" cy="{fy + 118}" r="5" fill="{col}" stroke="#333" stroke-width="0.8"/>')
        pg.text(lx + 14, fy + 122, lab, 10)
    for k, lab in enumerate(["WAN / LAN", "LAN"]):
        px = x0 + 40 + k * 110
        pg.rect(px, fy + 150, 70, 56, "#2b3138", "#2b3138", rx=3)
        pg.rect(px + 16, fy + 160, 38, 30, "#11161b", "#2b3138", rx=1, sw=1)
        pg.text(px + 35, fy + 224, lab, 9.5, "bold", "middle")
    pg.rect(x0 + 300, fy + 172, 70, 12, "#11161b", "#2b3138", rx=1)
    pg.text(x0 + 335, fy + 224, "SIM", 9.5, "bold", "middle")
    pg.rect(x0 + 420, fy + 160, 100, 36, "#5b6670", "#2b3138", rx=3)
    pg.text(x0 + 470, fy + 224, "DC 9–30 V · DI · DO", 9.5, "bold", "middle")
    pg.rect(x0 + 445, fy + 172, 50, 12, "#11161b", "#2b3138", rx=1)
    # ---- inside
    by = fy + 350
    pg.text(x0, by, "Inside", 15, "bold")
    blocks = [
        ("mcu", "Router SoC", ["MediaTek MT7628AN: 580 MHz MIPS 24KEc; 2.4 GHz 2×2 Wi-Fi 4 and a 5-port 10/100 switch on the chip — one chip does router, switch and Wi-Fi"]),
        ("mem", "Memory", ["128 MB DDR2 · 16 MB SPI NOR (same as the RUT200)"]),
        ("radio", "4G modem", ["Quectel EC200A-CN, LTE Cat 4, India bands, GSM fallback, on USB (ECM) — the RUT200's own modem"]),
        ("eth", "Ethernet", ["2 ports from the MT7628 switch: WAN / LAN + LAN, RJ45 with magnetics"]),
        ("io", "IO", ["1 DI + 1 DO, as on the RUT200"]),
        ("power", "Power", ["9–30 V DC, reverse and surge protected; 12 V adapter supplied separately"]),
    ]
    by += 14
    for kind, t, lines in blocks:
        by = pg.block(x0, by, ew, kind, t, lines, size=10.5) + 6

    # ---- right: BOM, price, comparison
    rx = x0 + ew + 50
    rw = W - 40 - rx
    pg.text(rx, y0 + 4, "BOM at 100 units (INR, ESTIMATE)", 15, "bold")
    yy = header(rx, y0 + 16, [("Line", rw - 90, "start"), ("INR", 90, "end")], h=26)
    for i, (lab, v) in enumerate(BOM["rut"][1]):
        parts = wrap(lab, rw - 110, 10)
        h = 8 + 13 * len(parts) + 2
        pg.rect(rx, yy, rw, h, ALT if i % 2 == 0 else "#ffffff", GRID, rx=0, sw=0.8)
        for k, ln in enumerate(parts):
            pg.text(rx + 8, yy + 15 + k * 13, ln, 10)
        pg.text(rx + rw - 8, yy + 15, inr(v), 10, anchor="end")
        yy += h
    v = build_keys(["rut"])
    steps = [("BOM", v[0], False), ("+ Mfg, packing, logistics 50 %", v[1], False), ("+ Firmware royalty", v[3], False),
             ("= Price before profit", v[2] + v[3], True), ("+ Profit 30 %", v[4], False), ("= Price after profit (ex-works)", v[5], True)]
    for lab, val, strong in steps:
        pg.rect(rx, yy, rw, 22, HI if strong else "#ffffff", GRID, rx=0, sw=0.8)
        put(rx, rw - 90, yy, lab, weight="bold" if strong else "normal", anchor="start")
        put(rx + rw - 90, 90, yy, inr(val), weight="bold" if strong else "normal")
        yy += 22

    yy += 30
    pg.text(rx, yy, "Against the Teltonika RUT200 (India)", 15, "bold")
    yy = header(rx, yy + 12, [("", 170, "start"), ("RUT200", (rw - 170) / 2, "start"), ("Ours", (rw - 170) / 2, "start")], h=26)
    cmp_rows = [("Hardware", "MT7628 + EC200A, 128 / 16 MB", "Same pattern and parts"),
                ("Ethernet / Wi-Fi", "2 × 10/100, Wi-Fi 4 2.4 GHz", "Same"),
                ("Price in India", "INR 7,569–8,500 dealer, 13,700 retail", f"INR {inr(v[5])} ex-works, before dealer margin"),
                ("Software", "RutOS (OpenWrt) + RMS cloud", "OpenWrt (upstream supports the RUT200 board)")]
    cw2 = (rw - 170) / 2
    for i, (a, b, c) in enumerate(cmp_rows):
        lb, lc = wrap(b, cw2 - 16, 10), wrap(c, cw2 - 16, 10)
        h = 8 + 13 * max(len(lb), len(lc)) + 2
        pg.rect(rx, yy, rw, h, ALT if i % 2 == 0 else "#ffffff", GRID, rx=0, sw=0.8)
        pg.text(rx + 8, yy + 15, a, 10, "bold")
        for k, ln in enumerate(lb):
            pg.text(rx + 178, yy + 15 + k * 13, ln, 10)
        for k, ln in enumerate(lc):
            pg.text(rx + 170 + cw2 + 8, yy + 15 + k * 13, ln, 10)
        yy += h
    yy += 26
    pg.text(rx, yy, "Points to decide", 15, "bold")
    pg.para(rx, yy + 18, rw, [
        "Security: the MT7628 has no hardware secure boot or TrustZone. Fine for the India launch; for the CRA (Phase 2) a secure SoC is needed — STM32MP135F or MediaTek MT7981 (R18, R20).",
        "Vendor and longevity: MediaTek is outside the ST / NXP / Nordic list and publishes no longevity programme for the MT7628 (a 2014 part).",
        "Radio approval: Wi-Fi is on the SoC, not a pre-certified module, so we need our own WPC approval; TEC MTCTE applies to the router.",
        "Software: OpenWrt with our web UI, VPN, firewall and remote management — the main engineering cost; the earlier estimate was 18–30 engineer-months for a full router feature set (R18).",
        "Firmware royalty taken as INR 750 per router, as for the modules.",
    ], 10.5, bullet=True)
    pg.save("UC_Architecture_p7_Tier2_Router.svg")


page1()
page2()
page3()
page4()
page5()
page6()
page7()


def export_costs():
    """Write docs/deck/cost.json: every price at 100 units (owner, 2026-11-19)."""
    def row(name, keys):
        v = build_keys(keys)
        return [name, round(v[0]), round(v[2] + v[3]), round(v[5])]
    def delta(name, fits, a, b=None):
        v = build_keys(a) if b is None else [x - y for x, y in zip(build_keys(a), build_keys(b))]
        return [name, fits, round(v[0]), round(v[2] + v[3]), round(v[5])]
    P = []
    data = {
        "items": [row("Fieldbus controller (Ethernet standard)", ["base"]), row("4G modem + GPS (EC200U-CN)", ["4g"]), row("Wi-Fi + BLE", ["wifi"]),
                  row("LoRa", ["lora"]), row("Battery + charger board with 18650 cell — optional, per module", ["batt"]), row("Adapter 12 V 18 W — one per stack", ["adapter"])],
        "options": [delta("STM32H573 instead of PIC32CK (quote needed)", "Fieldbus controller", ["base_pic"])],
        "systems": [row("Fieldbus controller, standalone", ["base"]),
                    row("4G gateway: Fieldbus controller + 4G + GPS", ["base", "4g"]),
                    row("Wi-Fi gateway: Fieldbus controller + Wi-Fi + BLE", ["base", "wifi"]),
                    row("4G + LoRa gateway: Fieldbus controller + 4G + GPS + LoRa", ["base", "4g", "lora"]),
                    row("Full stack: all four modules", ["base", "4g", "wifi", "lora"]),
                    row("LoRa node, standalone", ["lora"]),
                    row("Wi-Fi + BLE node, standalone", ["wifi"]),
                    row("4G + GPS, standalone", ["4g"]),
                    row("4G industrial router, RUT200 class (separate product, page 7)", ["rut"])],
    }
    dst = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "deck", "cost.json")
    with open(dst, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)


export_costs()
print("ok")
