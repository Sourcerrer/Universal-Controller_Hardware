#!/usr/bin/env python3
"""3D concept renders of the Universal Controller (pure PIL, no 3D package needed).

Usage: python render_3d.py <output-dir>
Writes UC_3D_Stack.png, UC_3D_Exploded.png, UC_3D_Baseboard_PCB.png.
Stack and exploded views use a cabinet projection (fronts undistorted, depth receding up-right);
the PCB view uses an isometric projection.
"""
import sys, math, os
from PIL import Image, ImageDraw, ImageFont

OUTDIR = sys.argv[1]
W, H = 1920, 1080
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONTB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
_fc = {}


def font(size, bold=False):
    k = (size, bold)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(FONTB if bold else FONT, size)
    return _fc[k]


def shade(c, f):
    return tuple(max(0, min(255, int(v * f))) for v in c[:3])


INK, MUTED, ACC = (27, 31, 36), (74, 85, 96), (47, 95, 179)


class Scene:
    def __init__(self, mode, ox, oy, s, bg=(241, 244, 247)):
        self.mode, self.ox, self.oy, self.s = mode, ox, oy, s
        self.img = Image.new("RGBA", (W, H), bg + (255,))
        g = ImageDraw.Draw(self.img)
        for y in range(H):
            g.line([0, y, W, y], fill=shade(bg, 1.0 - 0.07 * y / H) + (255,))
        self.d = ImageDraw.Draw(self.img)

    def p(self, x, y, z):
        if self.mode == "cab":  # y = depth (back), front face y = 0
            k, a = 0.5, math.radians(35)
            return (self.ox + (x + y * k * math.cos(a)) * self.s, self.oy - (z + y * k * math.sin(a)) * self.s)
        c, s_ = math.cos(math.radians(30)), 0.5
        return (self.ox + (x - y) * c * self.s, self.oy + (x + y) * s_ * self.s - z * self.s)

    def box(self, x, y, z, w, d, h, col, outline=(40, 45, 52), top=None, front=None, side=None):
        P = self.p
        if self.mode == "cab":
            fr = [P(x, y, z), P(x + w, y, z), P(x + w, y, z + h), P(x, y, z + h)]
            tp = [P(x, y, z + h), P(x + w, y, z + h), P(x + w, y + d, z + h), P(x, y + d, z + h)]
            rt = [P(x + w, y, z), P(x + w, y + d, z), P(x + w, y + d, z + h), P(x + w, y, z + h)]
            self.d.polygon(rt, fill=side or shade(col, 0.72), outline=outline)
            self.d.polygon(tp, fill=top or shade(col, 1.06), outline=outline)
            self.d.polygon(fr, fill=front or col, outline=outline)
        else:
            rt = [P(x + w, y, z), P(x + w, y + d, z), P(x + w, y + d, z + h), P(x + w, y, z + h)]
            fr = [P(x, y + d, z), P(x + w, y + d, z), P(x + w, y + d, z + h), P(x, y + d, z + h)]
            tp = [P(x, y, z + h), P(x + w, y, z + h), P(x + w, y + d, z + h), P(x, y + d, z + h)]
            self.d.polygon(rt, fill=side or shade(col, 0.70), outline=outline)
            self.d.polygon(fr, fill=front or shade(col, 0.86), outline=outline)
            self.d.polygon(tp, fill=top or col, outline=outline)

    def rect_front(self, x0, x1, z0, z1, y, col, outline=None):
        P = self.p
        self.d.polygon([P(x0, y, z0), P(x1, y, z0), P(x1, y, z1), P(x0, y, z1)], fill=col, outline=outline)

    def dot(self, x, y, z, r, col):
        cx, cy = self.p(x, y, z)
        self.d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col, outline=(30, 30, 30))

    def cyl(self, x, y, z, r, h, col):
        cx, cy = self.p(x, y, z)
        _, ty = self.p(x, y, z + h)
        rr = r * self.s
        self.d.rectangle([cx - rr, ty, cx + rr, cy], fill=shade(col, 0.82))
        self.d.ellipse([cx - rr, ty - rr * 0.45, cx + rr, ty + rr * 0.45], fill=col, outline=shade(col, 0.6))

    def text_at(self, x, y, z, txt, size, col, bold=True, center=False):
        px, py = self.p(x, y, z)
        f = font(size, bold)
        if center:
            px -= self.d.textlength(txt, font=f) / 2
        self.d.text((px, py), txt, font=f, fill=col)

    def text_top_iso(self, x, y, z, txt, size, col):
        """Text lying on a horizontal surface in the isometric view (reads along +x)."""
        ox, oy = self.p(x, y, z)
        c, s_ = math.cos(math.radians(30)), 0.5
        f = font(size, True)
        tw = int(self.d.textlength(txt, font=f)) + 4
        timg = Image.new("RGBA", (tw, size + 8), (0, 0, 0, 0))
        ImageDraw.Draw(timg).text((2, 2), txt, font=f, fill=col + (255,))
        data = (1 / (2 * c), 1 / (2 * s_), -(ox / (2 * c) + oy / (2 * s_)), -1 / (2 * c), 1 / (2 * s_), ox / (2 * c) - oy / (2 * s_))
        self.img.alpha_composite(timg.transform((W, H), Image.AFFINE, data, resample=Image.BICUBIC))

    def callout(self, xyz, tx, ty, title, sub=None, align="left", size=21):
        px, py = self.p(*xyz)
        self.d.line([px, py, tx, ty], fill=MUTED, width=2)
        self.d.ellipse([px - 6, py - 6, px + 6, py + 6], fill=ACC, outline=(255, 255, 255), width=2)
        f, fs = font(size, True), font(size - 5)
        w1 = self.d.textlength(title, font=f)
        w2 = self.d.textlength(sub, font=fs) if sub else 0
        xx = tx + 8 if align == "left" else tx - 8 - max(w1, w2)
        self.d.text((xx, ty - size - 2), title, font=f, fill=INK)
        if sub:
            self.d.text((xx, ty + 4), sub, font=fs, fill=MUTED)

    def title(self, t, sub):
        self.d.text((60, 44), t, font=font(40, True), fill=INK)
        self.d.text((60, 98), sub, font=font(20), fill=MUTED)
        note = "Universal Controller · concept render · not to scale"
        self.d.text((W - 60 - self.d.textlength(note, font=font(16)), H - 42), note, font=font(16), fill=(120, 130, 140))

    def save(self, name):
        self.img.convert("RGB").save(os.path.join(OUTDIR, name), optimize=True)


ENCL = (228, 232, 237)
GOLD = (212, 160, 23)
TERM_GREEN = (58, 158, 88)
TERM_GREY = (112, 120, 130)
MODS = [
    dict(name="BASEBOARD", sub="controller", w=67.5, band=(35, 48, 61), top=["DC IN", "RS-485", "CAN-FD"], bot=["AI", "DI", "DO"], ant=[], ports=["usb", "rj45"]),
    dict(name="4G MODEM", sub="Tier 1", w=45.0, band=(230, 126, 34), top=["DC IN"], bot=[], ant=["LTE", "GNSS"], ports=["usb", "sim"]),
    dict(name="WI-FI", sub="+ BLE", w=22.5, band=(124, 77, 255), top=["DC"], bot=[], ant=["Wi-Fi"], ports=["usb"]),
    dict(name="LORA", sub="", w=22.5, band=(31, 127, 140), top=["DC"], bot=["IO"], ant=["LoRa"], ports=["usb"]),
]
HZ, DY, RF = 90.0, 58.0, 6.0  # height, depth, raised-front depth


def module(sc, m, x, y=0.0, z=0.0):
    w = m["w"]
    sc.box(x, y, z, w, DY, HZ, ENCL)
    # raised front block (typical DIN profile)
    sc.box(x + 1.2, y - RF, z + 20, w - 2.4, RF, HZ - 40, shade(ENCL, 1.03))
    yf = y - RF
    sc.rect_front(x + 2.4, x + w - 2.4, z + HZ - 36, z + HZ - 25, yf, m["band"])
    fs = 17 if w > 30 else 12
    sc.text_at(x + 3.6, yf, z + HZ - 26, m["name"], fs, (255, 255, 255))
    if m["sub"]:
        sc.text_at(x + 3.6, yf, z + HZ - 38.5, m["sub"], 11 if w < 30 else 13, MUTED, bold=False)
    for k, c in enumerate([(46, 204, 113), (52, 152, 219), (241, 196, 15)]):
        sc.dot(x + 5 + k * 5, yf, z + HZ - 46, 6, c)
    for k, kind in enumerate(m["ports"]):
        px = x + 4 + k * 17
        if kind == "usb":
            sc.rect_front(px, px + 9, z + 25, z + 28.5, yf, (190, 195, 200), outline=(40, 40, 40))
        elif kind == "rj45":
            sc.rect_front(px, px + 15, z + 23, z + 35, yf, (40, 44, 50), outline=(10, 10, 10))
            sc.rect_front(px + 4, px + 11, z + 33, z + 35, yf, (15, 15, 15))
        elif kind == "sim":
            sc.rect_front(px, px + 14, z + 26, z + 28, yf, (15, 15, 15))

    def terms(labels, z0):
        if not labels:
            return
        seg = (w - 3) / len(labels)
        for k, lab in enumerate(labels):
            bx = x + 1.5 + k * seg + 0.5
            sc.box(bx, y, z0, seg - 1.0, 13, 8, TERM_GREEN if k % 2 == 0 else TERM_GREY)
            npins = max(2, int((seg - 3) // 5))
            for p in range(npins):
                sc.dot(bx + 2.5 + p * ((seg - 6) / max(1, npins - 1)), y, z0 + 4, 4, (220, 224, 228))
    terms(m["top"], z + HZ)
    terms(m["bot"], z - 8)


def antennas(sc, m, x, y=0.0, z=0.0):
    for k, lab in enumerate(m["ant"]):
        ax = x + m["w"] * (k + 1) / (len(m["ant"]) + 1)
        sc.cyl(ax, y + 30, z + HZ, 2.6, 6, GOLD)
        sc.cyl(ax, y + 30, z + HZ + 6, 1.7, 30, (48, 48, 52))
        sc.text_at(ax, y + 30, z + HZ + 44, lab, 16, (138, 106, 0), center=True)


def bridge(sc, xj, y=0.0, z=0.0, lift=0.0):
    sc.box(xj - 9, y + 34, z + HZ + lift, 18, 18, 4.5, (122, 134, 147))


def rail(sc, x0, x1):
    sc.box(x0, DY - 4, 30, x1 - x0, 4, 35, (178, 184, 192))


def render_stack():
    sc = Scene("cab", ox=430, oy=960, s=5.4)
    sc.title("Universal Controller — assembled stack",
             "Baseboard + 4G modem + Wi-Fi/BLE + LoRa on a 35 mm DIN rail, joined by 40-pin bridge plugs")
    xs, x = [], 0.0
    for m in MODS:
        xs.append(x)
        x += m["w"]
    rail(sc, -22, x + 26)
    for m, x0 in zip(MODS, xs):
        module(sc, m, x0)
    for k in range(1, len(MODS)):
        bridge(sc, xs[k])
    for m, x0 in zip(MODS, xs):
        antennas(sc, m, x0)
    sc.callout((xs[0] + 34, 0, HZ + 6), 60, 220, "Pluggable terminals", "DC IN · RS-485 · CAN-FD (top)", align="left")
    sc.callout((xs[0] + 34, -RF, 45), 60, 470, "Baseboard (controller)", "STM32H5 · 16 IO · RS-485 · CAN-FD", align="left")
    sc.callout((xs[0] + 6, -RF, 26), 60, 700, "USB-C on every module", "service port + USB-PD power", align="left")
    sc.callout((xs[0] + 34, 0, -4), 60, 930, "Field IO terminals", "AI · DI · DO (bottom)", align="left")
    sc.callout((xs[2], 43, HZ + 4.5), 1450, 200, "Bridge plug", "joins the 40-pin bus")
    sc.callout((xs[1] + 22, -RF, 55), 1450, 380, "4G modem card", "Quectel EC200A · LTE Cat 4 · GPS option")
    sc.callout((xs[2] + 11, -RF, 55), 1450, 520, "Wi-Fi + BLE", "ESP32-C6 · Wi-Fi 6 · BLE · Thread")
    sc.callout((xs[3] + 11, -RF, 55), 1450, 660, "LoRa", "STM32WLE5 · RS-485 + 2 DI")
    sc.save("UC_3D_Stack.png")


def render_exploded():
    sc = Scene("cab", ox=200, oy=930, s=4.6)
    sc.title("Inserting and removing modules",
             "Clip the module onto the rail beside the stack, then press a bridge plug across the two 40-pin connectors")
    gap = 30.0
    xs, x = [], 0.0
    for m in MODS:
        xs.append(x)
        x += m["w"] + gap
    rail(sc, -22, x + 4)
    for m, x0 in zip(MODS, xs):
        if m["name"] == "LORA":
            continue
        module(sc, m, x0)
    # LoRa module pulled forward (off the rail)
    lx = xs[3]
    module(sc, MODS[3], lx + 8, y=-34, z=4)
    for k in range(1, len(MODS)):
        xj = xs[k] - gap / 2
        lift = 34 if k < 3 else 44
        bridge(sc, xj, lift=lift)
        a0 = sc.p(xj, 43, HZ + lift - 1)
        a1 = sc.p(xj, 43, HZ + 9)
        sc.d.line([a0, a1], fill=ACC, width=5)
        sc.d.polygon([(a1[0] - 10, a1[1] - 16), (a1[0] + 10, a1[1] - 16), (a1[0], a1[1])], fill=ACC)
    for m, x0 in zip(MODS[:3], xs[:3]):
        antennas(sc, m, x0)
    antennas(sc, MODS[3], lx + 8, y=-34, z=4)
    # arrow: LoRa slides back onto the rail
    b0 = sc.p(lx + 19, -34 - RF, 22)
    b1 = sc.p(lx + 11, -6, 30)
    sc.d.line([b0, b1], fill=(230, 126, 34), width=7)
    ang = math.atan2(b1[1] - b0[1], b1[0] - b0[0])
    tip = b1
    l, wdt = 22, 11
    sc.d.polygon([tip, (tip[0] - l * math.cos(ang) + wdt * math.sin(ang), tip[1] - l * math.sin(ang) - wdt * math.cos(ang)),
                  (tip[0] - l * math.cos(ang) - wdt * math.sin(ang), tip[1] - l * math.sin(ang) + wdt * math.cos(ang))], fill=(230, 126, 34))
    px0 = 1430
    sc.d.rounded_rectangle([px0 - 20, 170, W - 40, 560], radius=12, fill=(255, 255, 255), outline=(201, 208, 216), width=2)
    sc.d.text((px0, 190), "To insert a module", font=font(22, True), fill=INK)
    yy = 232
    for k, ln in enumerate(["Clip it onto the rail beside the stack (orange arrow)", "Press a bridge plug down across both 40-pin connectors (blue arrows)", "Power up: the baseboard finds and authenticates it"]):
        words, cur, lines = ln.split(), "", []
        for w_ in words:
            test = (cur + " " + w_).strip()
            if sc.d.textlength(test, font=font(17)) > 380:
                lines.append(cur)
                cur = w_
            else:
                cur = test
        lines.append(cur)
        for j, part in enumerate(lines):
            sc.d.text((px0 + (0 if j == 0 else 22), yy), (f"{k + 1}. " if j == 0 else "") + part, font=font(17), fill=MUTED)
            yy += 23
        yy += 8
    sc.d.text((px0, 400), "To remove a module", font=font(22, True), fill=INK)
    for k, ln in enumerate(["Power the stack down", "Lift the bridge plug", "Unclip the module from the rail"]):
        sc.d.text((px0, 440 + k * 30), f"{k + 1}. {ln}", font=font(17), fill=MUTED)
    sc.save("UC_3D_Exploded.png")


def render_pcb():
    sc = Scene("iso", ox=930, oy=260, s=9.2)
    sc.title("Baseboard PCB — component placement concept",
             "Secure STM32H5 controller · 16 field IO · isolated RS-485 · CAN-FD · 5–32 V / USB-C PD power · 40-pin stack bus")
    PW, PD, Z = 85.0, 60.0, 1.6
    sc.box(0, 0, 0, PW, PD, Z, (34, 120, 72), outline=(20, 70, 40))
    for k in range(9):
        a, b = sc.p(4, 6 + k * 6, Z + 0.02), sc.p(PW - 4, 6 + k * 6, Z + 0.02)
        sc.d.line([a, b], fill=(52, 150, 92), width=1)
    parts = [
        # x, y, w, d, h, colour, label, label size (drawn back-to-front by x+y)
        (4, 0, 10, 8, 10, (112, 120, 130), "", 0),        # DC IN terminal
        (16, 0, 14, 8, 10, (58, 158, 88), "", 0),         # RS-485 terminal
        (32, 0, 14, 8, 10, (112, 120, 130), "", 0),       # CAN-FD terminal
        (8, 10, 26, 14, 3.0, (255, 232, 207), "POWER", 13),
        (38, 16, 14, 14, 1.6, (28, 30, 34), "STM32H5", 13),
        (56, 16, 8, 6, 1.2, (28, 30, 34), "NOR", 10),
        (68, 14, 10, 12, 6.0, (205, 210, 215), "", 0),     # CR2032 holder
        (56, 26, 10, 8, 1.2, (28, 30, 34), "ETH*", 10),
        (8, 28, 20, 8, 2.0, (52, 60, 70), "4 AI", 12),
        (30, 28, 20, 8, 2.0, (52, 60, 70), "4 DO", 12),
        (8, 38, 20, 8, 2.0, (52, 60, 70), "8 DI", 12),
        (52, 38, 14, 8, 2.4, (236, 236, 236), "RS-485", 10),
        (68, 38, 10, 8, 1.6, (52, 60, 70), "CAN", 10),
        (PW - 3, 6, 3, 30, 8, (24, 24, 28), "", 0),        # 40-pin stack header (right edge)
        (4, PD - 9, 18, 9, 10, (58, 158, 88), "", 0),      # AI terminals
        (24, PD - 9, 20, 9, 10, (112, 120, 130), "", 0),   # DI terminals
        (46, PD - 9, 16, 9, 10, (58, 158, 88), "", 0),     # DO terminals
        (PW - 13, PD - 7, 9, 7, 3.2, (190, 195, 200), "", 0),  # USB-C
    ]
    for x0, y0, w_, d_, h_, col, lab, fs in sorted(parts, key=lambda p: (p[0] + p[2] / 2) + (p[1] + p[3] / 2)):
        sc.box(x0, y0, Z, w_, d_, h_, col)
        if lab:
            sc.text_top_iso(x0 + 1.5, y0 + 2.2, Z + h_, lab, fs, (245, 245, 245) if sum(col) < 400 else (70, 45, 10))
    L, R = 110, 1810
    sc.callout((45, 23, Z + 1.6), 1250, 210, "STM32H5 secure MCU", "TrustZone · PSA Certified Level 3 · Zephyr", align="left")
    sc.callout((PW - 1.5, 20, Z + 8), R, 430, "40-pin stack bus", "to the bridge plug and the next module", align="right")
    sc.callout((73, 20, Z + 6), R, 330, "RTC with CR2032 backup", "", align="right")
    sc.callout((59, 42, Z + 2.4), R, 560, "Isolated RS-485 · CAN-FD", "Modbus RTU · J1939 · CANopen", align="right")
    sc.callout((PW - 8.5, PD - 3.5, Z + 3.2), R, 820, "USB-C", "service port + USB-PD power input", align="right")
    sc.callout((21, 17, Z + 3), L, 300, "Power", "5–32 V · USB-C PD · Li-ion charger · eFuse", align="left")
    sc.callout((9, 4, Z + 10), L, 190, "DC IN · RS-485 · CAN-FD", "pluggable screw terminals", align="left")
    sc.callout((18, 32, Z + 2), L, 520, "Field IO front ends", "4 AI · 8 DI isolated · 4 DO protected", align="left")
    sc.callout((24, PD - 4, Z + 10), L, 800, "Field IO terminals", "AI · DI · DO", align="left")
    sc.callout((61, 30, Z + 1.2), 1250, 140, "Ethernet switch", "*Ethernet variant only", align="left")
    sc.save("UC_3D_Baseboard_PCB.png")


render_stack()
render_exploded()
render_pcb()
print("ok")
