#!/usr/bin/env python3
"""Client / sales video of the Universal Controller family (PIL frames -> ffmpeg).

Scenes: the family, inside each module, specs, applications, reliability, safety, security.
Written for customers and sales staff: plain language, no internal codes or prices.

Usage: python build_video.py <ffmpeg-binary> <output.mp4>
"""
import sys, math, subprocess
from PIL import Image, ImageDraw, ImageFont

FFMPEG, OUT = sys.argv[1], sys.argv[2]
W, H, FPS = 1280, 720, 30
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONTB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
_fc = {}


def font(size, bold=False):
    k = (size, bold)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(FONTB if bold else FONT, size)
    return _fc[k]


BG = (246, 248, 250)
INK = (27, 31, 36)
MUTED = (74, 85, 96)
ENCL = (232, 236, 240)
ENCL_EDGE = (35, 48, 61)
PCB = (34, 120, 72)
PCB_EDGE = (20, 80, 48)
CHIP = (30, 33, 38)
TERM = (91, 102, 112)
GOLD = (212, 160, 23)
BLUE = (47, 95, 179)
ORANGE = (230, 126, 34)
GREEN = (46, 204, 113)
PURPLE = (124, 77, 255)
TEAL = (31, 127, 140)


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease(x):
    x = clamp(x)
    return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2


def prog(t, t0, t1):
    return ease((t - t0) / (t1 - t0)) if t1 > t0 else float(t >= t0)


def text_center(d, cx, cy, s, size, bold=False, fill=INK):
    f = font(size, bold)
    lines = s.split("\n")
    lh = size + 3
    y = cy - lh * len(lines) / 2
    for ln in lines:
        w = d.textlength(ln, font=f)
        d.text((cx - w / 2, y), ln, font=f, fill=fill)
        y += lh


# ------------------------------------------------------------------ stack scene
RAIL_Y = 612
TOP_Y = 180
EH = RAIL_Y - TOP_Y
X0, GAP = 40, 12
PCB_H = 262
DESIGN_PCB_H = 312

MODS = [
    dict(key="base", name="FIELDBUS CONTROLLER", sub="the brain · 90 mm", w=280, dw=310,
         top=["DC IN", "RS-485", "CAN-FD"], bottom=["AI", "DI", "FAST", "RELAYS"], sma=[],
         comps=[("PIC32CK\nsecure MCU", 18, 16, 96, 92, "chip"), ("ETH\nPHY", 128, 20, 58, 38, "chip"),
                ("RJ45\nEthernet", 200, 20, 72, 46, "eth"), ("4 AI", 18, 126, 78, 52, "ic"),
                ("10 DI\nisolated", 106, 126, 78, 52, "ic"), ("8 RELAYS\n10 A", 194, 126, 78, 52, "ic"),
                ("RS-485\nisolated", 18, 184, 78, 40, "ic"), ("CAN-FD\nisolated", 106, 184, 78, 40, "ic"),
                ("4 FAST\nOUTPUTS", 194, 184, 78, 40, "ic"), ("POWER", 18, 254, 254, 46, "pwr")]),
    dict(key="4g", name="4G + GPS", sub="cloud link · 45 mm", w=190, dw=210,
         top=["DC IN"], bottom=[], sma=["LTE", "GPS"],
         comps=[("Quectel\nEC200U\n4G + GPS", 14, 16, 112, 96, "chip"), ("SIM", 136, 18, 42, 44, "ic"),
                ("MODEM\nPOWER", 14, 128, 164, 50, "ic"), ("POWER", 14, 254, 164, 46, "pwr")]),
    dict(key="wifi", name="WI-FI + BLE", sub="45 mm · with IO", w=140, dw=160,
         top=["DC IN"], bottom=["RS-485 + CAN + IO"], sma=["Wi-Fi"],
         comps=[("ESP32-C6\nmodule", 14, 16, 112, 80, "can"), ("6 DI · 4 DO · 4 AI\n2 RELAYS", 14, 106, 112, 46, "ic"),
                ("RS-485 + CAN\nisolated", 14, 160, 112, 40, "ic"), ("POWER", 14, 254, 112, 46, "pwr")]),
    dict(key="lora", name="LORA", sub="45 mm · with IO", w=140, dw=160,
         top=["DC IN"], bottom=["RS-485 + IO"], sma=["LoRa"],
         comps=[("STM32WLE5\nLoRa radio", 14, 16, 112, 66, "can"), ("4 DI · 4 AI\n4 DO", 14, 94, 112, 46, "ic"),
                ("RS-485", 14, 150, 112, 36, "ic"), ("POWER", 14, 254, 112, 46, "pwr")]),
]
xs = []
x = X0
for m in MODS:
    xs.append(x)
    x += m["w"] + GAP
STACK_END = xs[-1] + MODS[-1]["w"]
PANEL_X = STACK_END + 36


def dashed_rect(d, box, fill, step=8):
    x0, y0, x1, y1 = box
    for k in range(int(x0), int(x1), step):
        d.line([k, y0, min(k + 4, x1), y0], fill=fill, width=2)
        d.line([k, y1, min(k + 4, x1), y1], fill=fill, width=2)
    for k in range(int(y0), int(y1), step):
        d.line([x0, k, x0, min(k + 4, y1)], fill=fill, width=2)
        d.line([x1, k, x1, min(k + 4, y1)], fill=fill, width=2)


def draw_module(d, m, x, y, lit=1.0, scale=1.0):
    w = m["w"]
    n = len(m["sma"])
    for k, lab in enumerate(m["sma"]):
        cx = x + w * (k + 1) / (n + 1)
        d.rectangle([cx - 6, y - 26, cx + 6, y - 2], fill=GOLD, outline=(138, 106, 0))
        d.rectangle([cx - 9, y - 8, cx + 9, y], fill=(184, 134, 11))
        text_center(d, cx, y - 36, lab, 11, True, (138, 106, 0))
    d.rounded_rectangle([x, y, x + w, y + EH], radius=12, fill=ENCL, outline=ENCL_EDGE, width=3)

    def strip(labels, yy, label_y):
        if not labels:
            return
        seg = (w - 20) / len(labels)
        for k, lab in enumerate(labels):
            sx = x + 10 + k * seg
            d.rounded_rectangle([sx + 3, yy, sx + seg - 3, yy + 18], radius=3, fill=TERM, outline=(43, 49, 56))
            npins = max(2, int((seg - 12) // 13))
            for p in range(npins):
                px = sx + 9 + p * ((seg - 18) / max(1, npins - 1))
                d.ellipse([px - 4, yy + 5, px + 4, yy + 13], fill=(213, 217, 221), outline=(43, 49, 56))
            text_center(d, sx + seg / 2, label_y, lab, 10, True, (43, 49, 56))

    strip(m["top"], y + 10, y + 38)
    d.rounded_rectangle([x + 6, y + 50, x + w - 6, y + 92], radius=6, fill=(35, 48, 61))
    d.text((x + 14, y + 54), m["name"], font=font(15, True), fill=(255, 255, 255))
    d.text((x + 14, y + 74), m["sub"], font=font(11), fill=(207, 216, 226))
    for k, col in enumerate([GREEN] if m["key"] == "lora" else [GREEN, BLUE]):   # LoRa: one RUN LED only
        d.ellipse([x + w - 38 + k * 15, y + 60, x + w - 29 + k * 15, y + 69], fill=col if lit > 0.5 else (90, 90, 90))
    px, py, pw, ph = x + 10, y + 100, w - 20, PCB_H
    sx_ = pw / (m["dw"] - 20)
    sy_ = PCB_H / DESIGN_PCB_H
    # logic PCB stops above the separate power PCB (common part, PWR-10)
    p_top = py + 246 * sy_
    d.rounded_rectangle([px, py, px + pw, p_top - 10], radius=6, fill=PCB, outline=PCB_EDGE, width=2)
    for k in range(4):
        ty = py + 26 + k * 50
        d.line([px + 6, ty, px + pw - 6, ty], fill=(52, 150, 92), width=1)
    for lab, rx, ry, rw, rh, kind in m["comps"]:
        cx0, cy0 = px + rx * sx_, py + ry * sy_
        rw2, rh2 = rw * sx_, rh * sy_
        box = [cx0, cy0, cx0 + rw2, cy0 + rh2]
        fs = 10 if rw2 > 60 else 9
        if kind == "chip":
            d.rectangle(box, fill=CHIP, outline=(10, 10, 10))
            for p in range(0, int(rw2) - 6, 8):
                d.line([cx0 + 4 + p, cy0 - 3, cx0 + 4 + p, cy0], fill=(190, 190, 190))
                d.line([cx0 + 4 + p, cy0 + rh2, cx0 + 4 + p, cy0 + rh2 + 3], fill=(190, 190, 190))
            text_center(d, cx0 + rw2 / 2, cy0 + rh2 / 2, lab, fs, True, (235, 235, 235))
        elif kind == "can":
            d.rectangle(box, fill=(200, 205, 210), outline=(120, 120, 120))
            text_center(d, cx0 + rw2 / 2, cy0 + rh2 / 2, lab, fs, True, (40, 40, 40))
        elif kind == "pwr":
            # power stage on the module PCB (solid) + optional plug-in battery board (dashed)
            bw_ = pw * 0.56
            pbox = [px, p_top, px + bw_, py + ph]
            d.rounded_rectangle(pbox, radius=5, fill=(255, 232, 207), outline=(196, 106, 0), width=3)
            text_center(d, px + bw_ / 2, (p_top + py + ph) / 2, "POWER +\nPROTECTION" if bw_ > 120 else "POWER", 10 if bw_ > 120 else 9, True, (150, 80, 0))
            bb = [px + bw_ + 6, p_top, px + pw, py + ph]
            dashed_rect(d, bb, (196, 106, 0))
            text_center(d, (bb[0] + bb[2]) / 2, (p_top + py + ph) / 2, "BATTERY\n(option)" if bb[2] - bb[0] > 80 else "BATT.\nopt.", 9, True, (150, 80, 0))
        elif kind == "eth":
            d.rectangle(box, fill=(214, 241, 245), outline=TEAL, width=2)
            text_center(d, cx0 + rw2 / 2, cy0 + rh2 / 2, lab, fs, True, TEAL)
        elif kind == "dash":
            dashed_rect(d, box, (230, 230, 230))
            text_center(d, cx0 + rw2 / 2, cy0 + rh2 / 2, lab, fs, True, (235, 235, 235))
        else:
            d.rectangle(box, fill=(52, 60, 70), outline=(15, 15, 15))
            text_center(d, cx0 + rw2 / 2, cy0 + rh2 / 2, lab, fs, True, (235, 235, 235))
    # USB-C (right, under the PCB) and bottom terminals
    d.rounded_rectangle([x + w - 50, y + EH - 64, x + w - 18, y + EH - 54], radius=5, fill=(201, 206, 211), outline=(43, 49, 56))
    d.text((x + 14, y + EH - 66), "USB-C", font=font(9, True), fill=(43, 49, 56)) if not m["bottom"] else None
    strip(m["bottom"], y + EH - 28, y + EH - 40)
    d.rectangle([x + 4, y - 5, x + 40, y + 5], fill=(20, 22, 25))
    d.rectangle([x + w - 40, y - 5, x + w - 4, y + 5], fill=(20, 22, 25))
    d.rectangle([x + w / 2 - 24, y + EH - 4, x + w / 2 + 24, y + EH + 8], fill=(43, 49, 56))


def draw_bridge(d, i, lift):
    x1 = xs[i] + MODS[i]["w"] - 36
    x2 = xs[i + 1] + 36
    yy = TOP_Y - 14 - lift * 90
    d.rounded_rectangle([x1, yy, x2, yy + 16], radius=4, fill=(123, 135, 148), outline=(43, 49, 56), width=2)


def wrap(d, s, width, f):
    words, cur, out = s.split(), "", []
    for w_ in words:
        test = (cur + " " + w_).strip()
        if d.textlength(test, font=f) > width:
            out.append(cur)
            cur = w_
        else:
            cur = test
    out.append(cur)
    return out


def caption(d, t, t0, t1, title, lines, step=None):
    a = clamp((t - t0) / 0.5) * clamp((t1 - t) / 0.5)
    if a <= 0:
        return
    col = lambda c: tuple(int(BG[k] + (c[k] - BG[k]) * a) for k in range(3))
    x, y = PANEL_X, 150
    width = W - PANEL_X - 30
    if step:
        d.ellipse([x, y, x + 32, y + 32], fill=col(BLUE))
        text_center(d, x + 16, y + 16, step, 15, True, col((255, 255, 255)))
    tl = wrap(d, title, width - 44, font(19, True))
    ty = y + 4
    for ln in tl:
        d.text((x + 44, ty), ln, font=font(19, True), fill=col(INK))
        ty += 24
    yy = max(y + 50, ty + 14)
    for ln in lines:
        wl = wrap(d, ln, width - 16, font(14))
        d.ellipse([x, yy + 6, x + 6, yy + 12], fill=col(BLUE))
        for k, s in enumerate(wl):
            d.text((x + 14, yy), s, font=font(14), fill=col(INK if k == 0 else MUTED))
            yy += 20
        yy += 7


def pulses(d, t, xa, xb, y, color, speed=220, spacing=60, r=4):
    if xb <= xa:
        return
    p = xa + (t * speed) % spacing
    while p < xb:
        d.ellipse([p - r, y - r, p + r, y + r], fill=color)
        p += spacing


# ------------------------------------------------------------------ field-node scene
def node_icon(d, cx, cy, color, label, sub, ant=True, scale=1.0, alpha=1.0):
    if alpha <= 0:
        return
    w, h = 54 * scale, 78 * scale
    x0, y0 = cx - w / 2, cy - h / 2
    if ant:
        d.rectangle([cx - 3, y0 - 16, cx + 3, y0], fill=GOLD)
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=7, fill=ENCL, outline=ENCL_EDGE, width=2)
    d.rounded_rectangle([x0 + 4, y0 + 6, x0 + w - 4, y0 + 22], radius=3, fill=color)
    d.rounded_rectangle([x0 + 6, y0 + 28, x0 + w - 6, y0 + h - 10], radius=3, fill=PCB)
    d.rectangle([cx - 12, y0 + 36, cx + 12, y0 + 56], fill=CHIP)
    text_center(d, cx, y0 + h + 14, label, 12, True, INK)
    if sub:
        text_center(d, cx, y0 + h + 30, sub, 10, False, MUTED)


def link(d, p0, p1, t, p, color, dashed=False, width=2, packet=True):
    if p <= 0:
        return
    x0, y0 = p0
    x1, y1 = x0 + (p1[0] - x0) * p, y0 + (p1[1] - y0) * p
    if dashed:
        L = math.hypot(x1 - x0, y1 - y0)
        n = int(L // 10)
        for k in range(n):
            if k % 2 == 0:
                a, b = k / max(n, 1), (k + 1) / max(n, 1)
                d.line([x0 + (x1 - x0) * a, y0 + (y1 - y0) * a, x0 + (x1 - x0) * b, y0 + (y1 - y0) * b], fill=color, width=width)
    else:
        d.line([x0, y0, x1, y1], fill=color, width=width)
    if packet and p >= 1:
        f = (t * 0.6) % 1.0
        px, py = x0 + (p1[0] - x0) * f, y0 + (p1[1] - y0) * f
        d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=color)




# ================================================================== timeline (seconds)
T_TITLE = (0.0, 4.0)
T_BASE = (4.0, 6.0)
T_BASE_INFO = (6.0, 12.0)
T_IN = {"4g": (12.0, 13.4), "wifi": (17.0, 18.4), "lora": (22.0, 23.4)}
T_BR = {"4g": (13.4, 14.2), "wifi": (18.4, 19.2), "lora": (23.4, 24.2)}
T_RUN = (27.0, 32.0)
T_STACK_END = 32.0
T_PCB = (32.0, 54.0)        # 4 close-ups x 5.5 s
T_SPEC = (54.0, 68.0)
T_FIELD = (68.0, 82.0)
T_APPS = (82.0, 94.0)
T_REL = (94.0, 106.0)
T_SAFE = (106.0, 117.0)
T_SEC = (117.0, 129.0)
T_END = (129.0, 134.0)
DUR = T_END[1]
ORDER = ["4g", "wifi", "lora"]
SCENES = [T_STACK_END, T_PCB[1], T_SPEC[1], T_FIELD[1], T_APPS[1], T_REL[1], T_SAFE[1], T_SEC[1]]


def header(d, title, sub):
    d.text((40, 26), title, font=font(26, True), fill=INK)
    d.text((40, 62), sub, font=font(15), fill=MUTED)


# ------------------------------------------------------------------ 1 · the family on the rail
def stack_frame(t):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    header(d, "Universal Controller — one family, click-together modules",
           "Front view on a DIN rail · covers removed to show the boards · not to scale")
    ra = prog(t, T_TITLE[1] - 0.6, T_BASE[0] + 0.6)
    d.rectangle([30, RAIL_Y + 4, 30 + (STACK_END + 20 - 30) * ra, RAIL_Y + 22], fill=(184, 190, 198), outline=(123, 135, 148))
    if ra > 0.9:
        d.text((38, RAIL_Y + 6), "35 mm DIN rail", font=font(11, True), fill=(51, 65, 79))
    pb = prog(t, *T_BASE)
    if pb > 0:
        draw_module(d, MODS[0], xs[0], TOP_Y - (1 - pb) * 260, lit=1.0 if t > T_BASE[1] else 0.0)
    if T_BASE_INFO[0] <= t < T_BASE_INFO[1]:
        k = int((t - T_BASE_INFO[0]) / 0.6)
        comps = MODS[0]["comps"]
        if k < len(comps):
            lab, rx, ry, rw, rh, kind = comps[k]
            m = MODS[0]
            sx_ = (m["w"] - 20) / (m["dw"] - 20)
            sy_ = PCB_H / DESIGN_PCB_H
            px, py = xs[0] + 10, TOP_Y + 100
            d.rectangle([px + rx * sx_ - 4, py + ry * sy_ - 4, px + (rx + rw) * sx_ + 4, py + (ry + rh) * sy_ + 4], outline=(241, 196, 15), width=4)
    for i, key in enumerate(ORDER):
        m = MODS[i + 1]
        p = prog(t, *T_IN[key])
        if p <= 0:
            continue
        x_slot = xs[i + 1]
        x_now = x_slot + (1 - p) * (W + 40 - x_slot)
        draw_module(d, m, x_now, TOP_Y, lit=1.0 if t > T_BR[key][1] else 0.0)
        pbr = prog(t, *T_BR[key])
        if pbr > 0 and pbr < 1.0 or t >= T_BR[key][1]:
            draw_bridge(d, i, 1 - pbr)
    if t >= T_BR["4g"][1]:
        right = xs[1] + MODS[1]["w"] / 2
        if t >= T_BR["wifi"][1]:
            right = xs[2] + MODS[2]["w"] / 2
        if t >= T_BR["lora"][1]:
            right = xs[3] + MODS[3]["w"] / 2
        yb = TOP_Y - 6
        d.line([xs[0] + MODS[0]["w"] / 2, yb, right, yb], fill=(123, 135, 148), width=2)
        pulses(d, t, xs[0] + MODS[0]["w"] / 2, right, yb, BLUE, speed=180, spacing=46, r=4)
        d.ellipse([40, H - 48, 50, H - 38], fill=BLUE)
        d.text((56, H - 51), "4-pin bridge plug between modules: power + data", font=font(12), fill=MUTED)
    caption(d, t, T_BASE[0], T_BASE_INFO[1], "Fieldbus controller — the brain",
            ["Reads sensors and switches machines: 4 analog and 10 digital inputs, 8 relays, 4 fast outputs",
             "Talks to meters, drives and PLCs over isolated RS-485, CAN and Ethernet",
             "Logs data and keeps working even when the internet is down"], step="1")
    caption(d, t, T_IN["4g"][0], T_IN["wifi"][0], "Add 4G + GPS",
            ["Sends data to the cloud over the mobile network — no Wi-Fi needed",
             "Built-in GPS knows where the site or vehicle is"], step="2")
    caption(d, t, T_IN["wifi"][0], T_IN["lora"][0], "Add Wi-Fi + Bluetooth",
            ["Connects over the site's Wi-Fi", "Set up and check it from a phone over Bluetooth",
             "Has its own inputs, outputs, 2 relays, RS-485 and CAN"], step="3")
    caption(d, t, T_IN["lora"][0], T_RUN[0], "Add LoRa",
            ["Reaches tanks, pumps and meters kilometres away — no SIM card, no monthly fee",
             "Its own inputs, outputs and RS-485 at the remote site"], step="4")
    caption(d, t, T_RUN[0], T_STACK_END + 0.5, "Click together — work as one",
            ["Slide onto the rail, press in the bridge plug, done",
             "Buy only the modules a site needs; add more later",
             "Every module also works on its own as a remote node"], step="5")
    return img


# ------------------------------------------------------------------ 2 · inside each module
PCB_NOTES = {
    "base": ["The brain: a secure processor with a built-in vault for its keys",
             "26 field connections, each with its own status light",
             "8 relays (10 A, AC or DC) and 4 fast 24 V outputs that measure their own current",
             "Isolated RS-485 and CAN: electrical noise stays outside",
             "Ethernet port for the plant network",
             "Its own power supply with surge and wrong-wiring protection; battery optional"],
    "4g": ["Quectel 4G modem with GPS on one chip — a proven, certified radio",
           "Nano-SIM slot and screw-on antennas for LTE and GPS",
           "Its own power stage handles the modem's current bursts",
           "Battery optional: keeps reporting during a power cut"],
    "wifi": ["Espressif ESP32-C6 module: Wi-Fi 6 and Bluetooth LE, pre-certified",
             "6 inputs, 4 outputs, 4 analog inputs and 2 relays on the same board",
             "Isolated RS-485 and CAN for meters and machines",
             "Its own protected power supply; battery optional"],
    "lora": ["ST STM32WLE5: processor and LoRa radio in one chip",
             "Long range on 865–867 MHz with an external antenna",
             "4 inputs, 4 analog inputs, 4 outputs and RS-485",
             "Built for battery life: one small status light, microamp sleep"],
}
PCB_TITLES = {"base": "Inside the Fieldbus controller", "4g": "Inside the 4G + GPS module",
              "wifi": "Inside the Wi-Fi + Bluetooth module", "lora": "Inside the LoRa module"}


def pcb_frame(t):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    seg = (T_PCB[1] - T_PCB[0]) / 4
    k = min(3, int((t - T_PCB[0]) / seg))
    m = MODS[k]
    t0 = T_PCB[0] + k * seg
    header(d, PCB_TITLES[m["key"]], "What is on the boards — every module has its own enclosure, power supply and protection")
    tw, th = m["w"] + 40, EH + 80
    tmp = Image.new("RGB", (tw, th), BG)
    td = ImageDraw.Draw(tmp)
    draw_module(td, m, 20, 56, lit=1.0)
    s = min(1.3, (H - 130) / th, 520 / tw)
    big = tmp.resize((int(tw * s), int(th * s)), Image.LANCZOS)
    a = clamp((t - t0) / 0.5) * clamp((t0 + seg - t) / 0.4)
    bx = int(60 + (1 - a) * -40)
    base = Image.new("RGB", big.size, BG)
    img.paste(Image.blend(base, big, a), (bx, 100))
    x = 640
    y = 150
    for j, note in enumerate(PCB_NOTES[m["key"]]):
        aj = clamp((t - t0 - 0.5 - j * 0.6) / 0.4) * clamp((t0 + seg - t) / 0.4)
        if aj <= 0:
            continue
        col = lambda c: tuple(int(BG[q] + (c[q] - BG[q]) * aj) for q in range(3))
        d.ellipse([x, y, x + 28, y + 28], fill=col(BLUE))
        text_center(d, x + 14, y + 14, str(j + 1), 14, True, col((255, 255, 255)))
        for q, ln in enumerate(wrap(d, note, W - x - 80, font(18))):
            d.text((x + 42, y + 2 + q * 24), ln, font=font(18), fill=col(INK))
        y += 30 + 24 * len(wrap(d, note, W - x - 80, font(18)))
    return img


# ------------------------------------------------------------------ 3 · specifications at a glance
SPEC_ROWS = [
    ("Fieldbus controller", "The brain of the site",
     "4 analog in (0–10 V, 4–20 mA, PT1000) · 10 digital in · 8 relays 10 A (AC / DC) · 4 fast 24 V outputs with current monitoring · isolated RS-485 + CAN · Ethernet · data logging"),
    ("4G + GPS", "Cloud link, location",
     "4G LTE with 2G fallback · GPS / BeiDou / GLONASS / Galileo · nano-SIM · works standalone as a tracker"),
    ("Wi-Fi + Bluetooth", "Local wireless, phone set-up",
     "Wi-Fi 6 · Bluetooth LE · 6 digital in · 4 digital out · 4 analog in · 2 relays · isolated RS-485 + CAN"),
    ("LoRa", "Long-range remote sites",
     "865–867 MHz · kilometres of range · 4 digital in · 4 analog in · 4 digital out · RS-485 · battery friendly"),
    ("Every module", "Power and mounting",
     "5–32 V DC or USB-C · optional plug-in 18650 battery · 35 mm DIN rail · modules click together with a 4-pin bridge"),
]


def spec_frame(t):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    header(d, "Specifications at a glance", "Four modules — use one on its own or stack them into a gateway")
    x0, y0 = 40, 110
    cols = [("Module", 230), ("What it is for", 260), ("Key specifications", W - 80 - 490)]
    d.rectangle([x0, y0, W - 40, y0 + 36], fill=(35, 48, 61))
    cx = x0
    for name, w_ in cols:
        d.text((cx + 12, y0 + 9), name, font=font(16, True), fill=(255, 255, 255))
        cx += w_
    y = y0 + 36
    colors = [(35, 48, 61), ORANGE, PURPLE, TEAL, (196, 106, 0)]
    for j, (a_, b_, c_) in enumerate(SPEC_ROWS):
        aj = clamp((t - T_SPEC[0] - 0.4 - j * 0.9) / 0.5)
        lines = wrap(d, c_, cols[2][1] - 24, font(16))
        h = max(64, 18 + 22 * len(lines))
        if aj > 0:
            col = lambda c: tuple(int(BG[q] + (c[q] - BG[q]) * aj) for q in range(3))
            d.rectangle([x0, y, W - 40, y + h], fill=col((255, 255, 255) if j % 2 else (238, 242, 246)), outline=col((201, 208, 216)))
            d.rectangle([x0, y, x0 + 8, y + h], fill=col(colors[j]))
            d.text((x0 + 20, y + 12), a_, font=font(18, True), fill=col(INK))
            for q, ln in enumerate(wrap(d, b_, cols[1][1] - 24, font(16))):
                d.text((x0 + cols[0][1] + 12, y + 12 + q * 22), ln, font=font(16), fill=col(MUTED))
            for q, ln in enumerate(lines):
                d.text((x0 + cols[0][1] + cols[1][1] + 12, y + 12 + q * 22), ln, font=font(16), fill=col(INK))
        y += h
    return img


# ------------------------------------------------------------------ 4a · applications on a map
def field_frame(t):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    T0 = T_FIELD[0]
    header(d, "One system from the plant floor to remote sites",
           "The same modules stacked as a gateway or installed on their own in the field")
    cx, cy = 640, 140
    for dx, dy, r in [(-50, 8, 34), (0, -8, 44), (52, 8, 34), (0, 18, 36)]:
        d.ellipse([cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r], fill=(220, 230, 245))
    text_center(d, cx, cy + 6, "Cloud / SCADA / app", 15, True, BLUE)
    gx, gy = 640, 400
    if prog(t, T0, T0 + 0.8) > 0:
        widths = [56, 38, 26, 26]
        cols = [(35, 48, 61), ORANGE, PURPLE, TEAL]
        x = gx - sum(widths) / 2 - 6
        for w_, c in zip(widths, cols):
            d.rounded_rectangle([x, gy - 52, x + w_, gy + 52], radius=5, fill=ENCL, outline=ENCL_EDGE, width=2)
            d.rectangle([x + 3, gy - 46, x + w_ - 3, gy - 34], fill=c)
            d.rectangle([x + 3, gy - 28, x + w_ - 3, gy + 44], fill=PCB)
            x += w_ + 2
        d.rectangle([gx - 90, gy + 54, gx + 90, gy + 62], fill=(184, 190, 198))
        text_center(d, gx, gy + 80, "Gateway in the control panel", 14, True, INK)
        text_center(d, gx, gy + 97, "Controller + 4G + Wi-Fi/Bluetooth + LoRa", 11, False, MUTED)
        link(d, (gx, gy - 56), (cx, cy + 44), t, prog(t, T0 + 0.5, T0 + 1.2), ORANGE, width=3)
        d.text((gx + 10, (gy - 56 + cy + 44) / 2 - 8), "4G or Ethernet to the cloud", font=font(12, True), fill=ORANGE)
    lora = [(130, 300, "Water tank"), (110, 470, "Borewell pump"), (300, 600, "Energy meter")]
    t1 = T0 + 1.6
    for k, (x, y, lab) in enumerate(lora):
        if prog(t, t1 + k * 0.35, t1 + k * 0.35 + 0.5) > 0:
            node_icon(d, x, y, TEAL, "LoRa node", lab, scale=0.9)
            link(d, (x + 30, y), (gx - 90, gy), t + k * 0.3, prog(t, t1 + 0.4 + k * 0.35, t1 + 1.2 + k * 0.35), TEAL, dashed=True)
    if t > t1 + 1.0:
        d.text((40, 160), "LoRa: kilometres of range,", font=font(14, True), fill=TEAL)
        d.text((40, 180), "no SIM card, runs on a battery", font=font(13), fill=MUTED)
    mesh = [(980, 270, "Shop floor"), (1130, 300, "Cold room"), (1040, 430, "Office")]
    t2 = T0 + 4.0
    for k, (x, y, lab) in enumerate(mesh):
        if prog(t, t2 + k * 0.3, t2 + k * 0.3 + 0.5) > 0:
            node_icon(d, x, y, PURPLE, "Wi-Fi node", lab, scale=0.85)
            link(d, (x - 28, y + 10), (gx + 90, gy - 20), t + k * 0.2, prog(t, t2 + 0.5 + k * 0.3, t2 + 1.3 + k * 0.3), PURPLE, dashed=True)
    if t > t2 + 1.2:
        d.text((900, 160), "Wi-Fi + Bluetooth: inside buildings,", font=font(14, True), fill=PURPLE)
        d.text((900, 180), "set up from a phone", font=font(13), fill=MUTED)
    t3 = T0 + 7.0
    ex, ey = 1060, 600
    if prog(t, t3, t3 + 0.5) > 0:
        node_icon(d, ex, ey, (35, 48, 61), "Controller", "machines, PLCs, drives", ant=False)
        d.rounded_rectangle([830, 570, 930, 606], radius=6, fill=(255, 255, 255), outline=MUTED, width=2)
        text_center(d, 880, 588, "Plant network", 12, True, INK)
        link(d, (ex - 30, ey - 10), (930, 588), t, prog(t, t3 + 0.4, t3 + 1.0), BLUE, width=3)
        link(d, (880, 570), (gx + 60, gy + 50), t, prog(t, t3 + 0.8, t3 + 1.4), BLUE, width=3)
    t4 = T0 + 9.0
    fx, fy = 450, 250
    if prog(t, t4, t4 + 0.5) > 0:
        node_icon(d, fx, fy, ORANGE, "4G + GPS", "vehicle or remote site", scale=0.95)
        link(d, (fx + 30, fy - 30), (cx - 70, cy + 20), t, prog(t, t4 + 0.4, t4 + 1.0), ORANGE, width=3)
    return img


# ------------------------------------------------------------------ 4b · application tiles
def icon(d, kind, cx, cy, col, r=26):
    if kind == "drop":
        d.polygon([(cx, cy - r), (cx - r * 0.7, cy + r * 0.2), (cx + r * 0.7, cy + r * 0.2)], fill=col)
        d.ellipse([cx - r * 0.72, cy - r * 0.25, cx + r * 0.72, cy + r * 0.9], fill=col)
    elif kind == "factory":
        d.rectangle([cx - r, cy, cx + r, cy + r * 0.8], fill=col)
        d.polygon([(cx - r, cy), (cx - r * 0.3, cy - r * 0.5), (cx - r * 0.3, cy), (cx + r * 0.4, cy - r * 0.5), (cx + r * 0.4, cy)], fill=col)
        d.rectangle([cx + r * 0.55, cy - r, cx + r * 0.85, cy], fill=col)
    elif kind == "leaf":
        d.ellipse([cx - r * 0.9, cy - r * 0.5, cx + r * 0.9, cy + r * 0.5], fill=col)
        d.line([cx - r, cy + r * 0.6, cx + r * 0.6, cy - r * 0.3], fill=BG, width=3)
    elif kind == "sun":
        d.ellipse([cx - r * 0.5, cy - r * 0.5, cx + r * 0.5, cy + r * 0.5], fill=col)
        for a_ in range(8):
            ang = a_ * math.pi / 4
            d.line([cx + math.cos(ang) * r * 0.7, cy + math.sin(ang) * r * 0.7, cx + math.cos(ang) * r, cy + math.sin(ang) * r], fill=col, width=4)
    elif kind == "snow":
        for a_ in range(3):
            ang = a_ * math.pi / 3
            d.line([cx - math.cos(ang) * r, cy - math.sin(ang) * r, cx + math.cos(ang) * r, cy + math.sin(ang) * r], fill=col, width=4)
    elif kind == "truck":
        d.rectangle([cx - r, cy - r * 0.5, cx + r * 0.3, cy + r * 0.4], fill=col)
        d.polygon([(cx + r * 0.35, cy - r * 0.2), (cx + r * 0.8, cy - r * 0.2), (cx + r, cy + r * 0.1), (cx + r, cy + r * 0.4), (cx + r * 0.35, cy + r * 0.4)], fill=col)
        for wx in (cx - r * 0.6, cx + r * 0.6):
            d.ellipse([wx - r * 0.22, cy + r * 0.3, wx + r * 0.22, cy + r * 0.74], fill=INK)
    elif kind == "lock":
        d.arc([cx - r * 0.5, cy - r, cx + r * 0.5, cy], 180, 360, fill=col, width=5)
        d.line([cx - r * 0.5, cy - r * 0.5, cx - r * 0.5, cy], fill=col, width=5)
        d.line([cx + r * 0.5, cy - r * 0.5, cx + r * 0.5, cy], fill=col, width=5)
        d.rounded_rectangle([cx - r * 0.75, cy - r * 0.1, cx + r * 0.75, cy + r * 0.85], radius=4, fill=col)
        d.ellipse([cx - 4, cy + r * 0.25, cx + 4, cy + r * 0.25 + 8], fill=BG)
    else:   # glyph
        text_center(d, cx, cy, kind, int(r * 1.3), True, col)


APPS = [("drop", BLUE, "Water and borewells", "Tank levels, pump control, flow meters — alerts before a tank runs dry"),
        ("factory", (35, 48, 61), "Factories and machines", "Machine status, energy meters, Modbus drives and PLCs to one dashboard"),
        ("leaf", (46, 160, 90), "Agriculture", "Soil moisture and irrigation valves across large farms over LoRa"),
        ("sun", ORANGE, "Solar and energy", "Inverters, DG sets and meters monitored remotely, power cuts reported"),
        ("snow", TEAL, "Cold chain", "Cold-room and freezer temperatures with alarms by SMS or app"),
        ("truck", PURPLE, "Vehicles and fleets", "GPS position and vehicle CAN data from trucks, tractors and buses")]


def apps_frame(t):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    header(d, "Where it is used", "Typical applications — one hardware family, configured per site")
    tw_, th_ = 380, 250
    for j, (ic, col, title, line) in enumerate(APPS):
        aj = clamp((t - T_APPS[0] - 0.3 - j * 0.6) / 0.5)
        if aj <= 0:
            continue
        r_, c_ = divmod(j, 3)
        x = 40 + c_ * (tw_ + 20)
        y = 110 + r_ * (th_ + 20)
        cl = lambda c: tuple(int(BG[q] + (c[q] - BG[q]) * aj) for q in range(3))
        d.rounded_rectangle([x, y, x + tw_, y + th_], radius=12, fill=cl((255, 255, 255)), outline=cl((201, 208, 216)), width=2)
        d.ellipse([x + 24, y + 24, x + 104, y + 104], fill=cl((238, 242, 246)))
        icon(d, ic, x + 64, y + 64, cl(col))
        d.text((x + 24, y + 126), title, font=font(20, True), fill=cl(INK))
        for q, ln in enumerate(wrap(d, line, tw_ - 48, font(16))):
            d.text((x + 24, y + 160 + q * 22), ln, font=font(16), fill=cl(MUTED))
    return img


# ------------------------------------------------------------------ 5–7 · reliability, safety, security
REL = ("Built to keep running", (46, 160, 90), [
    ("↻", "Restarts itself if it ever hangs", "A separate watchdog circuit checks the processor all the time and resets it automatically."),
    ("⚡", "Rides through power cuts", "Plug in the optional battery board and the module keeps working — and tells you the mains has gone."),
    ("✔", "Shrugs off electrical noise", "Isolated RS-485 and CAN ports keep noise and earth faults from motors and drives outside."),
    ("⚙", "Protected against wiring mistakes", "Every power input survives reverse wiring, surges and short circuits."),
    ("⌂", "One fault does not stop the rest", "Each module has its own power supply, so a problem in one module stays in that module."),
])
SAFE = ("Safe by design", ORANGE, [
    ("⚠", "Mains kept apart", "The modules run on safe low voltage from a certified adapter; relays that switch mains loads are walled off by 5 kV isolation."),
    ("✔", "Outputs switch off on their own", "If the controller stops or loses power, every output turns off by itself — machines never stay on by accident."),
    ("⚡", "Short-circuit protection", "Fast outputs limit their own current; every relay has its own replaceable fuse."),
    ("☀", "Safe battery charging", "Replaceable 18650 cell with a protection circuit; it charges only within safe temperatures."),
])
SEC = ("Secure from the first power-on", BLUE, [
    ("lock", "Runs only genuine software", "Secure boot: the device checks a digital signature before it starts any software."),
    ("↻", "Safe remote updates", "Updates are signed and encrypted; if an update fails, the device goes back to the last good version."),
    ("★", "No shared passwords", "Every unit has its own digital identity built into its chip — nothing common to guess or leak."),
    ("lock", "Encrypted all the way", "Data to the cloud travels over encrypted connections, like online banking."),
    ("✔", "No fake modules", "Modules prove who they are to each other before they share any data."),
])


def promise_frame(t, span, spec):
    title, color, rows = spec
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    header(d, title, "In plain words — what it means for your site")
    d.rectangle([40, 96, 140, 100], fill=color)
    y = 124
    rh = (H - 150) / len(rows)
    for j, (ic, head, line) in enumerate(rows):
        aj = clamp((t - span[0] - 0.4 - j * 0.9) / 0.5)
        if aj > 0:
            cl = lambda c: tuple(int(BG[q] + (c[q] - BG[q]) * aj) for q in range(3))
            cy = y + rh / 2 - 6
            d.ellipse([60, cy - 30, 120, cy + 30], fill=cl(color))
            icon(d, ic, 90, cy, cl((255, 255, 255)), r=20)
            d.text((150, cy - 30), head, font=font(22, True), fill=cl(INK))
            for q, ln in enumerate(wrap(d, line, W - 220, font(17))):
                d.text((150, cy + 2 + q * 22), ln, font=font(17), fill=cl(MUTED))
        y += rh
    return img


# ------------------------------------------------------------------ assembly
def scene(t):
    if t < T_STACK_END:
        return stack_frame(t)
    if t < T_PCB[1]:
        return pcb_frame(t)
    if t < T_SPEC[1]:
        return spec_frame(t)
    if t < T_FIELD[1]:
        return field_frame(t)
    if t < T_APPS[1]:
        return apps_frame(t)
    if t < T_REL[1]:
        return promise_frame(t, T_REL, REL)
    if t < T_SAFE[1]:
        return promise_frame(t, T_SAFE, SAFE)
    return promise_frame(t, T_SEC, SEC)


def frame(t):
    img = scene(t)
    for b in SCENES:                      # short cross-fade at every scene change
        if b - 0.4 <= t < b:
            img = Image.blend(img, scene(b + 0.01), (t - (b - 0.4)) / 0.4)
    a = 1 - clamp((t - (T_TITLE[1] - 0.6)) / 0.6)
    if a > 0:
        ov = Image.new("RGB", (W, H), (35, 48, 61))
        od = ImageDraw.Draw(ov)
        text_center(od, W / 2, H / 2 - 36, "Universal Controller", 50, True, (255, 255, 255))
        text_center(od, W / 2, H / 2 + 28, "Modular industrial IoT controller and gateway — made for India", 22, False, (207, 216, 226))
        img = Image.blend(img, ov, a)
    a = clamp((t - T_END[0]) / 0.8)
    if a > 0:
        ov = Image.new("RGB", (W, H), (35, 48, 61))
        od = ImageDraw.Draw(ov)
        text_center(od, W / 2, H / 2 - 50, "Universal Controller", 40, True, (255, 255, 255))
        text_center(od, W / 2, H / 2 + 4, "Fieldbus controller · 4G + GPS · Wi-Fi + Bluetooth · LoRa", 20, False, (207, 216, 226))
        text_center(od, W / 2, H / 2 + 40, "Reliable · Safe · Secure — stack them as a gateway or install them on their own", 18, False, (207, 216, 226))
        text_center(od, W / 2, H / 2 + 84, "Concept animation · November 2026 · not to scale · specifications may change", 13, False, (160, 172, 184))
        img = Image.blend(img, ov, a)
    return img


if __name__ == "__main__" and len(sys.argv) > 3 and sys.argv[3] == "--stills":
    for tt in [2, 9, 15, 30, 36, 50, 60, 72, 90, 100, 112, 125, 132]:
        frame(tt).save(f"{OUT}_{tt:03d}.png")
    sys.exit(0)

cmd = [FFMPEG, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
       "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "medium", "-movflags", "+faststart", OUT]
proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
n = int(DUR * FPS)
for i in range(n):
    proc.stdin.write(frame(i / FPS).tobytes())
proc.stdin.close()
err = proc.stderr.read().decode(errors="ignore")
rc = proc.wait()
if rc != 0:
    print(err[-2000:])
    sys.exit(rc)
print("frames", n, "->", OUT)
