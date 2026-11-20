# R24 — Field connectors (terminals, RJ45, USB-C, SMA, SIM, DC input, vehicle CAN port)

Status: COMPLETE WITH GAPS (2026-11-20). Owner request 2026-11-20: "finalize the connectors that will be used. Regularly available, flexible, automotive & industrial grade connectors that can sustain up to 10 g of vibration." Added the same day: "Connections will be made on site" and "For vehicular CAN, an OBD-II or better port is needed — for the Fieldbus controller and the Wi-Fi + BLE module."

Scope: the field-facing connectors of the four modules. The 4-pin stack-bus connector (D-9) is not covered here.

Rules used: prices at 100 units only, in INR. 1 USD = INR 93.9 and 1 EUR = 1.08 USD (same as R14–R22). No DigiKey prices. LCSC prices were read from the live product pages on 2026-11-20 (the ladder step that covers 100 pieces). Prices exclude GST, duty and freight. ESTIMATE / UNVERIFIED where no 100-unit price was seen. Raw findings are in Appendix A.

## 1. Executive summary

**How "10 g" is read.** 10 g peak, sinusoidal, per IEC 60068-2-6 (test Fc), 3 axes. A practical severity is 0.75 mm below ≈ 57 Hz and 10 g from ≈ 57 to 500 Hz. That is about 10 × the IEC 61131-2 PLC level (1 g) [S17]. Only two connector families in this study publish test data at or above 10 g: WAGO picoMAX latched push-in plugs (20 g) [S3] and TE DEUTSCH DT sealed connectors (20 g) [S12]. Phoenix publishes 5 g for its screw-flange plugs [S1]. The Chinese makers publish no vibration data. So **every connector below needs one shaker test of a complete, wired module** before release (section 5, Q1).

**"Connections will be made on site"** favours pluggable terminals. The installer pre-wires the plug, and a failed module is swapped without touching a single wire. With fixed terminals every wire must be undone and redone on a swap, which is where wiring errors happen.

| Position | Recommended | INR at 100 | Lower-cost alternative | INR at 100 | Trade-off of the alternative |
|---|---|---|---|---|---|
| Field IO + DC IN terminals (all modules) | 3.81 mm pluggable, **plug with screw flange + header with threaded flange** (Phoenix MC 1,5/..-STF-3,81 style): Cixi Kefa KF2EDGKM-3.81-xP plug + Ningbo Kangnex WJ15EDGRM-3.81-xP header; 2nd source Degson 15EDGKM | ≈ 9–11 per pole | Fixed 3.81 mm screw terminals, Kefa KF128L-3.81 (2nd source MAX MX128H, Dorabo DB125) | ≈ 5.3–6.6 per pole | No pre-wiring; every wire re-terminated on a module swap; more on-site wiring errors |
| DO terminals (≈ 4 A per output) | Same 3.81 mm family (8 A per pole); **one L+ feed pole per output group, ≤ 8 A per L+ pole** | in the above | — | — | See Q3: 10 outputs × 4 A cannot go through one L+ pole |
| RJ45 + magnetics (Fieldbus controller only) | HanRun HR911105A (10/100, LEDs, shielded THT) — meets the owner's < INR 100 cap, **0…70 °C only** | 95.7 | — (it is the cheapest) | — | If D-28 asks for −20/−40 °C: industrial jack (Pulse JX3V-9015NL / LINK-PP LPJ4011 class, −40…85 °C) ≈ INR 160, **+64, over the INR 100 cap** |
| USB-C (5 V + service) | GCT USB4105-GF-A: 4 through-hole shell stakes, −40…85 °C, 20,000 cycles | 60.4 | Korean Hroparts TYPE-C-31-M-12 (today's part): 4 shell legs, −30…80 °C | 14.0 | Narrower temperature range, no published cycle data. Neither holds a cable at 10 g: USB-C is for service, not for permanent power in vibrating installs |
| SMA antenna (LTE, GNSS, LoRa) | **Board-mounted right-angle SMA jack, barrel through the enclosure wall with nut + lock washer, RF trace from the radio pad — no pigtail.** Kinghelm KH-SMA-K513-G | 36.8 | Edge-mount SMA HenryTech HL-SMA-KE-02 | 20.6 | Needs the PCB edge right at the wall; thread length to check |
| SMA on Wi-Fi + BLE (option, MINI-1U) | MINI-1U has only a U.FL socket, so a pigtail is unavoidable: U.FL → SMA bulkhead pigtail, **U.FL staked with adhesive and cable tied down** | ≈ 35 ESTIMATE | Keep the PCB-antenna MINI-1 (standard today) | 0 | No external antenna in metal cabinets |
| Nano-SIM (4G card) | **Hinged (flip-top) holder behind a front door**: XUNPU SMN-305; 2nd source Shou Han NANO SIM XG6P | 16.0 | Shou Han NANO SIM XG6P | 11.0 | Same type; smaller maker. Avoid push-push and push-pull holders |
| eSIM (option) | MFF2 eSIM soldered, as SIM 2 (if the EC200U dual-SIM mode is confirmed) | UNVERIFIED | — | — | Operator profile and price to quote |
| DC input | **No separate locking connector**: the 2-pole member of the same flanged family, black and coded so it cannot be swapped with an IO plug | 34.0 | Fixed 2-pole screw terminal Kefa KF128L-3.81-2P | 12.3 | No pre-wiring |
| Vehicle CAN port (Fieldbus controller, Wi-Fi + BLE) | **M12 A-coded 5-pin male, CiA 303-1 pinout** (CAZN M12-P5A-GPBM12), plus accessory cables M12 → OBD-II (J1962) Y-cable and M12 → J1939 9-pin Y-cable | 158.6 | **DB9 male, CiA 303-1 pinout, with 4-40 jackscrews** (CONNFLY DS1037-09M class), with off-the-shelf OBD-II / J1939-to-DB9 cables | ≈ 35 ESTIMATE | Not sealed (IP20); jackscrews must be tightened; some "OBD-II to DB9" cables use a different pinout |

**Cost impact (BOM, INR at 100 units; detail in section 4).** Today's costing under-prices the terminals: it assumes INR 2 per pole, but fixed 3.81 mm terminals cost INR 5.3–6.6 per pole at 100 units on LCSC. Even keeping today's choices costs more than the model says.

| Module | Today (identifiable connector cost) | Recommended set | Δ | Lower-cost set | Δ |
|---|---|---|---|---|---|
| Fieldbus controller | ≈ 176 | ≈ 733 | **+557** (incl. +159 vehicle port) | ≈ 361 | +185 (incl. +35 vehicle port) |
| 4G modem card + GPS | ≈ 113 ESTIMATE | ≈ 184 | +71 | ≈ 79 | −35 |
| Wi-Fi + BLE | ≈ 64 ESTIMATE | ≈ 491 | **+427** (incl. +159 vehicle port) | ≈ 191 | +127 (incl. +35 vehicle port) |
| LoRa | ≈ 96 ESTIMATE | ≈ 328 | **+232** | ≈ 152 | +56 |

Finished cost moves by 1.5 × these deltas. **Reliability vs cost (owner's call):** the recommended set pushes the Fieldbus controller BOM from ≈ INR 2,496 to ≈ 3,053 (INR 2,000 hard limit) and the LoRa BOM from ≈ 1,127 to ≈ 1,359 (needs ≤ 754 for the INR 1,600 selling price). The lower-cost set is mostly a correction of today's under-priced terminals. The single biggest driver is the flanged pluggable terminal (≈ +INR 4–5 per pole over fixed terminals).

## 2. Requirements used

| # | Requirement | Source | Value used here |
|---|---|---|---|
| 1 | Vibration | Owner 2026-11-20 | 10 g; read as sine, IEC 60068-2-6, 3 axes (Q1 asks whether random vibration per ISO 16750-3 was meant) |
| 2 | Field wiring done on site | Owner 2026-11-20 | Pluggable, pre-wireable plugs preferred; tool use with a 2.5 mm screwdriver is acceptable; clear labels and coding against mis-plugging |
| 3 | Vehicle CAN port, "OBD-II or better" | Owner 2026-11-20 | On the Fieldbus controller (CAN-FD) and Wi-Fi + BLE (CAN 2.0); "better" read as also covering J1939 trucks and CANopen machines |
| 4 | Pole counts | Diagram page 1 (build_architecture.py) | Fieldbus: DC 2, RS-485 3, CAN-FD 3, AI 8, DI 11, DO 12 (39; today's costing says 32). Wi-Fi + BLE: DC 2, RS-485 3, CAN 3, DI 7, DO 5, AI 5 (25). LoRa: DC 2, RS-485 3, DI 5, AI 5, DO 6 (21). 4G: DC 2 |
| 5 | DO current | Owner (task brief) | Up to ≈ 4 A per output. Note: the TPS274160B in the costing limits at 0.5–2.5 A per channel (IO-1), so 4 A also needs a different switch (outside this report) |
| 6 | Wire range | Engineering default | 0.5–1.5 mm² (AWG 20–16) for IO; 0.75–1.5 mm² for DC IN and DO |
| 7 | Voltage | PRD PWR-5 | SELV only: 5–32 V DC in, 24 V IO |
| 8 | Temperature | PRD D-28 (open) | Shown per part; −40…85 °C preferred |
| 9 | RJ45 | Owner 2026-11-19 | Würth or HanRun, integrated magnetics, < INR 100 |
| 10 | USB-C | PRD PWR-9 | Plain 5 V + service, no PD |
| 11 | Sourcing | CLAUDE.md | Easy to buy in India, second source where possible, no Mornsun, prices at 100 units |

## 3. Comparison tables

### 3.1 Field terminals (IO, RS-485, CAN, DC IN)

| Part (3.81 / 3.5 mm) | Maker | Type | Rating | Vibration (published) | Retention / locking | Temp | INR per pole at 100 (plug + header) | Source | India | 2nd source |
|---|---|---|---|---|---|---|---|---|---|---|
| **KF2EDGKM-3.81 plug + WJ15EDGRM-3.81 header** | Cixi Kefa + Ningbo Kangnex | Pluggable, screw clamp, **screw flange** | 8 A, 300 V, 16–28 AWG | None published — own test needed | Two M2 flange screws lock plug to header | −40…105 °C | ≈ 9–11 (e.g. 6P 47.0 + 13.6 = 60.5) | LCSC C441118–C441125, C160125–C160129 [S20] | LCSC; IndiaMART traders | Degson 15EDGKM (6P INR 71.0, LCSC C506999) |
| MC 1,5/..-STF-3,81 + MC 1,5/..-GF-3,81 | Phoenix Contact | Same, screw flange | 8 A, 160–320 V, 0.14–1.5 mm² | **5 g**, IEC 60068-2-6, 10–150 Hz, 2.5 h/axis [S1] | Flange screws | not read (UNVERIFIED) | ≈ 90 per pole for the plug alone (RS Ireland €2.65 per 3P plug, box of 250) [S5] | RS | Phoenix Contact India (quote needed) | — |
| picoMAX 3.5 (2091 series) | WAGO | Push-in, **latched** female into shrouding header | 10 A, UL 1059 300 V, 0.2–1.5 mm² | **20 g**, EN 60068-2-6, 5–2000 Hz, no failure [S3] | Integrated latches | not read (UNVERIFIED) | ≈ 80–150 ESTIMATE (4P plug S$8.09 one-off at element14 SG) [S4] | element14 SG | WAGO India (quote needed) | — |
| 15EDGKNH-3.5 | Degson | Push-in pluggable | 3.5 mm, ≈ 8 A | None published | Friction; latch / flange versions listed on degson.com, not on LCSC | — | ≈ 15–17 plug only (4P INR 61.8, C7603448) | LCSC | DNA Tech, Robu | Kefa, Kangnex push-in (not priced) |
| KF2EDGK-3.81 plug + KF2EDGR-3.81 header | Cixi Kefa | Pluggable, no flange | 7–8 A, 250–300 V | None published | **Friction only** — not for 10 g | −40…105 °C | ≈ 5.5–9 (8P 29.9 + 13.9) | LCSC C440864, C441188 | LCSC | Kangnex WJ15EDGK (8P INR 34.1) |
| **KF128L-3.81 (fixed)** | Cixi Kefa | Fixed screw, stackable 2P/3P | 8 A, 300 V | None published | No mating interface | — | **≈ 5.3–6.1** (2P 12.3, 3P 16.0) | LCSC C474932, C474933 | LCSC | MAX MX128H (3P INR 15.2), Dorabo DB125-12P (INR 79.2) |

Notes:
- IEC 60947-7-4 (PCB terminal blocks) and UL 1059 test pull-out force and temperature rise, not vibration [S18]. Vibration figures are maker extras.
- **Screw vs push-in.** Push-in keeps a constant spring force and does not loosen under vibration. It needs ferrules on stranded wire and costs 2–3 × (Chinese) to 10 × (WAGO). Screw clamps take any wire without a ferrule, installers in India know them, and they cost least; the screw must be tightened to torque (≈ 0.22–0.25 N·m for 3.81 mm, Phoenix value) and a loose screw is the main vibration risk. **Recommendation: screw clamp with screw flange** for cost; WAGO picoMAX as the premium option for vehicle and rail customers who need proven ≥ 10 g.
- **Wire range on site.** 3.81 mm takes 0.14–1.5 mm² solid or stranded, but only up to ≈ 0.75 mm² with an insulated ferrule. Specify 0.75 mm² ferruled wire for IO and DO in the manual.
- **Mis-plugging.** The Fieldbus controller would have four 6-pole plugs (2 × DI, 2 × DO). A DO plug pushed into a DI header puts 24 V outputs onto inputs. Use plug colours (DO orange, DI green, power black — availability to confirm with Kefa / Kangnex), printed labels, and coding pins where the family offers them (Q4).
- **Stock.** LCSC stock of the 7-pole and larger flange plugs is thin (3–294 pieces). Keep plugs at ≤ 6 poles where possible, or buy from Kefa / Kangnex directly.

### 3.2 RJ45 with magnetics (Fieldbus controller only; the 4G card has no RJ45 since CELL-13)

| Part | Maker | Rating | Vibration / retention | Temp | INR at 100 | Source | India | 2nd source |
|---|---|---|---|---|---|---|---|---|
| **HR911105A** | HanRun | 10/100, LEDs, shielded, THT, tab-up | IEC 60603-7 class jack: plug latch holds 50 N for 60 s; vibration test with no interruption > 10 µs (standard level; not maker-tested data) [S19] | **0…70 °C** | **95.7** | LCSC C12074, 57,640 stock | LCSC; common at Indian resellers (UNVERIFIED) | LINK-PP LPJES101-0AGNL (SMD) INR 90.8, C53281908 |
| JX3V-9015NL | Pulse | 10/100, 1 port | same | −40…85 °C | ≈ 159 at 220+ (USD 4.25 below 220); 0 stock | LCSC C6885266 | Quote needed | LINK-PP LPJ4011 (−40…85 °C [S6]; price UNVERIFIED) |
| HR911297CE / HR915410AE | HanRun | gigabit, multi-port | same | −40…85 °C | 340 / 409 | LCSC | — | — |
| 7499010211A | Würth | 10/100 | same | industrial | ≈ 760 (RS Germany €7.48 at 62+) [S7] | RS | Würth India | — |

Vibration measures for any RJ45: tab-down or tab-up THT jack with soldered shield pegs; shield tied to the enclosure ground; a cable tie point on the enclosure or DIN rail within ≈ 100 mm so the cable mass does not hang on the latch. M12 D-coded Ethernet is the true high-vibration answer but costs ≈ INR 400–700 more per port (ESTIMATE); keep it as a later option only.

### 3.3 USB-C receptacle (plain 5 V + service)

| Part | Maker | Mounting | Rating | Retention | Temp | INR at 100 | Source | India | 2nd source |
|---|---|---|---|---|---|---|---|---|---|
| **USB4105-GF-A** | GCT | SMT contacts + 4 through-hole shell stakes (0.95 mm; -060 / -120 variants 0.6 / 1.2 mm) | VBUS 5 A, 48 V, 20,000 cycles | Mating 5–20 N, un-mating 6–20 N after test (USB-C spec range) | −40…85 °C | **60.4** | LCSC C3020560, 9,467 stock; drawing saved [S8] | LCSC, Mouser India | Molex 217175 / Amphenol 12401610E4 class (not priced) |
| TYPE-C-31-M-12 | Korean Hroparts | SMT + 4 shell legs | 16-pin, 20 V | USB-C spec range | −30…80 °C | **14.0** | LCSC C165948, 482,825 stock | LCSC | Shou Han TYPE-C16PIN |

A USB-C plug has no lock, so no USB-C cable stays reliably mated at 10 g. In vibrating installs the module must be powered from the flanged DC IN plug; USB-C is for service. The USB-IF screw-locking Type-C exists but is costly and the cables are rare; not recommended.

### 3.4 SMA and the U.FL problem

| Option | Part | Retention under vibration | Temp | INR at 100 | Source | Fits |
|---|---|---|---|---|---|---|
| **Board-mounted R/A SMA, nut on the wall, RF trace on PCB** | Kinghelm KH-SMA-K513-G | Threaded; nothing inside to come loose | −55…155 °C | **36.8** | LCSC C411575, 9,607 stock | LoRa (STM32WLE5 chip-down), 4G LTE + GNSS (EC200U-CN LCC pads) |
| Edge-mount SMA | HenryTech HL-SMA-KE-02 | Same | −55…125 °C | **20.6** | LCSC C20617215, 10,280 stock | Same, if the PCB edge sits at the wall |
| U.FL / MHF I pigtail to SMA bulkhead | generic | MHF I un-mating 5 N min, 3 N after 30 cycles [S9]; Hirose asks to be consulted for automotive use [S10] | — | ≈ 30–50 ESTIMATE | — | Only where the radio module has a U.FL socket (ESP32-C6-MINI-1U) |
| I-PEX MHF I LK (locking) | I-PEX | **20 N min initial, 10 N after 30 cycles**; used by automotive antenna makers [S9] | — | UNVERIFIED | — | Only on our own PCB (not on the MINI-1U) |

The vertical PCB of a DIN module puts its top edge right under the top wall, so a board-mounted SMA can pass straight through. Check the barrel thread length against the wall (2–3 mm) plus nut and lock washer; if too short, use a long-thread bulkhead version of the same jack (Q6). Where a U.FL is unavoidable: keep the pigtail short, stake the U.FL with a dot of adhesive (RTV or UV-cure), and tie the cable to the PCB.

### 3.5 Nano-SIM holder

| Type | Part | Behaviour at 10 g | Temp | INR at 100 | Source | Notes |
|---|---|---|---|---|---|---|
| **Hinged (flip-top)** | XUNPU SMN-305 | Metal lid closes over the card and latches; card cannot slide out | −25…85 °C | **16.0** | LCSC C266890, 54,685 stock | Needs access from above: place it behind a small front door or under a removable cover (MECH-5) |
| Hinged | Shou Han NANO SIM XG6P H1.35 | Same | −20…85 °C | 11.0 | LCSC C7529386, 41,715 stock | 2nd source |
| Hinged (branded) | GCT SIM8060-6-1-14-00-A | Same; GCT publishes a vibration test with ≤ 1 µs discontinuity limit for its SIM range (SIM5060) | −20…85 °C | 151.8 | LCSC C2943124 | Premium; Molex also has hinge-type nano-SIM for car infotainment (datasheet not downloadable) |
| Push-push | — | Heart-cam latch can release on shock; card can walk out | — | ≈ 10–15 | — | Avoid |
| Push-pull / tray | Shou Han NANO SIM TL6P (push-pull) | Friction hold only | −20…60 °C | 15.0 | LCSC C7529385 | Avoid |
| **MFF2 eSIM (soldered)** | operator part (Airtel / Jio / Vi IoT) | Nothing to come loose; automotive-grade parts exist | −40…105 °C class | UNVERIFIED | — | Needs operator profile; India M2M rules apply. Quectel documents dual-SIM single-standby on the EC200U (AT+QDSIM), but a Quectel forum reply says the reference design needs a switch circuit — to verify [S11] |

### 3.6 DC input

A separate locking DC connector is not needed. The 2-pole member of the flanged terminal family is locked by its flange screws, takes 0.5–1.5 mm² wire and is rated 8 A, far above the ≈ 1.7 A drawn through the first bridge at full stack load. Make it a different colour (black) and coded, so an IO plug cannot go into it. Cost ≈ INR 34 (plug 25.5 + header ≈ 8.5 ESTIMATE). Lower-cost: fixed 2-pole screw terminal, INR 12.3.

If the module is powered from a vehicle (directly or through the CAN port), the input front end must survive ISO 16750-2 load dump (12 V systems ≈ 35 V suppressed, 24 V systems ≈ 58 V suppressed) and 24 V jump-start (≈ 48 V). Today's 5–32 V input with an SMCJ33A-class TVS does not cover 24 V trucks. This is a power-stage change, flagged in Q8.

### 3.7 Vehicle CAN port (new, owner 2026-11-20)

Signals the port should carry: CAN_H, CAN_L, CAN_GND (signal ground), shield (optional), and vehicle battery + (optional, to power the module). SAE J1962 (OBD-II) has **no ignition pin** (pins 4 / 5 ground, 6 CAN_H, 14 CAN_L, 16 battery +) [S16]; J1939-13 9-pin has battery ± on A / B, CAN_H / CAN_L on C / D [S16]. Ignition state is therefore best derived from battery voltage (charging voltage > ≈ 13.2 V / 26.4 V) or CAN traffic, as most telematics boxes do. A hard-wired ignition input, if wanted, can use one DI on the terminal block.

| Option | On-module part | Pins (CiA / SAE) | Vibration / sealing | Panel space | INR at 100 | India | Verdict |
|---|---|---|---|---|---|---|---|
| **M12 A-coded 5-pin male (CiA 303-1)** | CAZN M12-P5A-GPBM12 (PCB, rear-mount, M12 thread); 2nd: Amphenol M12A-05P class, Phoenix / Lapp / Binder | 1 shield, 2 V+, 3 GND, 4 CAN_H, 5 CAN_L [S15] | Threaded coupling, IP67; maker vibration data not published (CAZN) | ≈ Ø 16 mm hole, ≈ 20 mm square — fits 45 mm and 67.5 mm modules | **158.6** (LCSC C7423416, 45 stock; −25…80 °C) | M12 cordsets sold by Phoenix, Lapp, Murrelektronik India; Chinese via LCSC | **Recommended** |
| DB9 male (CiA 303-1) with 4-40 jackscrews | CONNFLY DS1037-09M class (R/A PCB) | 2 CAN_L, 3 GND, 7 CAN_H, 9 V+ (opt.) [S15] | Jackscrews hold the plug; IP20, not sealed | 31 × 12.5 mm flange — fits 45 mm, uses most of the width | **≈ 35 ESTIMATE** (siblings INR 31.8–36.4) | Everywhere | **Lower-cost alternative** |
| SAE J1962 (OBD-II) on the module | J1962 16-pin | 6 CAN_H, 14 CAN_L, 16 Batt +, 4/5 GND | Not designed as a panel connector; vehicle side is the female socket | ≈ 44 × 20 mm — does not fit a 45 mm front with other parts | — | — | Use only as the far end of our cable |
| TE DEUTSCH DT04-6P (flange) / DTM | TE | free (6 pins) | **20 g sine 10–2000 Hz**, IP68 / IP69K [S12] | ≈ 30 mm flange (ESTIMATE) | ≈ 750+ genuine (DT04-2P USD 8.0 at 100 on LCSC); Amphenol AT and clones cheaper (UNVERIFIED) | TE India, traders | Too costly; crimp tool and pigtail harness needed |
| Deutsch HD10-9-1939 (J1939 Type II) | TE | A/B battery, C/D CAN, E shield | Rugged, sealed | ≈ 35–40 mm round flange (ESTIMATE) — too big for 45 mm | High (UNVERIFIED) | Traders | Use only as the far end of our J1939 cable |
| Molex MX150 sealed header | Molex | free | USCAR-2 class, IP67 | Medium | UNVERIFIED | Molex India | Not needed; no off-the-shelf vehicle cables |

**Recommended arrangement:**
- Fit an M12 A-coded 5-pin male (CiA 303-1) on the front of the Fieldbus controller and the Wi-Fi + BLE module.
- Supply two accessory cables, priced separately: (a) M12 female → J1962 male OBD-II Y-cable with a pass-through J1962 female for the workshop scanner; (b) M12 female → J1939 9-pin Y-cable (Type II green, 500 kbit/s). Price ESTIMATE INR 400–1,500 each; quotes needed.
- **Keep the existing 3-pole CAN screw terminal in parallel.** Both connect to the same isolated CAN channel (CA-IS2062A on the Fieldbus controller, CA-IS2062A on the Wi-Fi + BLE module). The terminal serves industrial daisy-chains; the M12 serves vehicles and CANopen drop cables. Only one end of the bus may have termination on; the existing termination switch covers this.
- The M12 pin 2 (V+) may power the module from the vehicle only if the load-dump front end of Q8 is added; otherwise leave pin 2 unconnected and power the module from DC IN.
- Use the DB9 alternative if the owner prefers the lowest cost. Specify the CiA 303-1 pinout in the manual: popular "OBD-II to DB9" cables (e.g. SparkFun, CAN on DB9 pins 3 / 5) are not CiA-compatible [S13].

## 4. Per-module connector BOM (INR at 100 units)

Basis: plug + header prices from section 3.1 (2P 34.0 · 3P 34.5 · 5P 50.7 · 6P 60.5 · 7P 67.3 · 8P 72.9; 2P, 5P, 7P and 8P header prices are interpolated, ESTIMATE). Fixed terminals: 3P 16.0, 2P 12.3. "Today" = what can be identified in `build_architecture.py`: terminals at INR 2 per pole, USB-C at INR 14, RJ45 ≈ 96 inside the Ethernet line, SMA / pigtail / SIM inside lump lines (ESTIMATE).

### 4.1 Fieldbus controller (67.5–90 mm)

| Position | Recommended | INR | Lower-cost | INR | Today |
|---|---|---|---|---|---|
| X1 DC IN | 2P flanged, black | 34.0 | KF128L 2P | 12.3 | in 66 |
| X2 RS-485 (A, B, GND_iso) | 3P flanged | 34.5 | KF128L 3P | 16.0 | in 66 |
| X3 CAN-FD (H, L, GND_iso) | 3P flanged | 34.5 | KF128L 3P | 16.0 | in 66 |
| X4 AI1–AI4 (2 poles each) | 8P flanged | 72.9 | KF128L 2P + 2 × 3P | 44.3 | in 66 |
| X5–X6 DI1–5 + COM, DI6–10 + COM | 2 × 6P flanged (one extra COM pole) | 121.0 | 4 × KF128L 3P | 64.0 | in 66 |
| X7–X8 DO1–5 + L+1, DO6–10 + L+2 | 2 × 6P flanged | 121.0 | 4 × KF128L 3P | 64.0 | in 66 |
| *Terminals subtotal (40 poles)* | | *417.9* | | *216.6* | *66 (32 poles × 2)* |
| RJ45 | HanRun HR911105A | 95.7 | same | 95.7 | ≈ 96 |
| USB-C | GCT USB4105-GF-A | 60.4 | Hroparts TYPE-C-31-M-12 | 14.0 | 14 |
| Vehicle CAN port (new) | M12 A-coded 5-pin | 158.6 | DB9 male + jackscrews | ≈ 35 | — |
| **Total** | | **≈ 733** | | **≈ 361** | **≈ 176** |
| **Δ vs today** | | **+557** | | **+185** | |

BOM effect: ≈ INR 2,496 → ≈ 3,053 (recommended) or ≈ 2,681 (lower-cost), against the INR 2,000 hard limit (already over by ≈ 496). If D-28 needs −40 °C: RJ45 +64.

### 4.2 4G modem card + GPS (45 mm)

| Position | Recommended | INR | Lower-cost | INR | Today (ESTIMATE) |
|---|---|---|---|---|---|
| DC IN | 2P flanged | 34.0 | KF128L 2P | 12.3 | ≈ 4 |
| USB-C | GCT USB4105-GF-A | 60.4 | Hroparts | 14.0 | 14 |
| LTE SMA | Board-mounted KH-SMA-K513-G, no pigtail | 36.8 | Edge SMA HL-SMA-KE-02 | 20.6 | ≈ 40 (SMA + pigtail, inside the 604 lump) |
| GNSS SMA | Same | 36.8 | Same | 20.6 | ≈ 40 (inside the 130 lump) |
| Nano-SIM | Hinged XUNPU SMN-305 behind a door | 16.0 | Shou Han XG6P | 11.0 | ≈ 15 (inside the 604 lump) |
| **Total** | | **≈ 184** | | **≈ 79** | **≈ 113** |
| **Δ vs today** | | **+71** | | **−35** | |

Option: MFF2 eSIM as SIM 2 (price UNVERIFIED), if the EC200U dual-SIM mode is confirmed.

### 4.3 Wi-Fi + BLE (45 mm)

| Position | Recommended | INR | Lower-cost | INR | Today (ESTIMATE) |
|---|---|---|---|---|---|
| DC IN | 2P flanged | 34.0 | KF128L 2P | 12.3 | ≈ 50 for all 25 poles at INR 2 |
| RS-485 | 3P flanged | 34.5 | KF128L 3P | 16.0 | |
| CAN | 3P flanged | 34.5 | KF128L 3P | 16.0 | |
| 6 DI + COM | 7P flanged (or 2 × 4P if 7P stock is short: +15) | 67.3 | 2 × KF128L 2P + 3P | 40.6 | |
| 4 DO + L+ | 5P flanged | 50.7 | KF128L 2P + 3P | 28.3 | |
| 4 AI + COM | 5P flanged | 50.7 | KF128L 2P + 3P | 28.3 | |
| *Terminals subtotal (25 poles)* | | *271.7* | | *141.5* | *≈ 50* |
| USB-C | GCT USB4105-GF-A | 60.4 | Hroparts | 14.0 | 14 |
| Vehicle CAN port (new) | M12 A-coded 5-pin | 158.6 | DB9 male | ≈ 35 | — |
| External antenna (option, MINI-1U) | U.FL → SMA pigtail, staked | ≈ 35 ESTIMATE | PCB antenna (standard) | 0 | 0 |
| **Total (standard)** | | **≈ 491** | | **≈ 191** | **≈ 64** |
| **Δ vs today** | | **+427** | | **+127** | |

BOM effect: ≈ INR 1,809 → ≈ 2,236 (recommended) or ≈ 1,936 (lower-cost). The INR 600 finished-cost target is already missed (D-5).

### 4.4 LoRa (45 mm)

| Position | Recommended | INR | Lower-cost | INR | Today (ESTIMATE) |
|---|---|---|---|---|---|
| DC IN | 2P flanged | 34.0 | KF128L 2P | 12.3 | ≈ 42 for all 21 poles at INR 2 |
| RS-485 | 3P flanged | 34.5 | KF128L 3P | 16.0 | |
| 4 DI + COM | 5P flanged | 50.7 | KF128L 2P + 3P | 28.3 | |
| 4 AI + COM | 5P flanged | 50.7 | KF128L 2P + 3P | 28.3 | |
| 4 DO + 24 V + 0 V | 6P flanged | 60.5 | 2 × KF128L 3P | 32.0 | |
| *Terminals subtotal (21 poles)* | | *230.4* | | *116.9* | *≈ 42* |
| USB-C | GCT USB4105-GF-A | 60.4 | Hroparts | 14.0 | 14 |
| LoRa SMA | Board-mounted KH-SMA-K513-G, RF trace from the STM32WLE5 | 36.8 | Edge SMA | 20.6 | ≈ 40 (inside the 78 line incl. antenna) |
| **Total** | | **≈ 328** | | **≈ 152** | **≈ 96** |
| **Δ vs today** | | **+232** | | **+56** | |

BOM effect: ≈ INR 1,127 → ≈ 1,359 (recommended) or ≈ 1,183 (lower-cost). The INR 1,600 selling price needs a BOM ≤ ≈ 754 (D-31). For remote LoRa nodes on a wall or pole (no vibration), the lower-cost set is reasonable.

## 5. Open questions for the owner

1. **Vibration profile.** Is "10 g" sine (IEC 60068-2-6) or random (ISO 16750-3, vehicle body)? Either way, budget one shaker test of each module, fully wired, with contact monitoring (no interruption > 1 µs), before release. Indian labs quote ≈ INR 30,000–80,000 per run (ESTIMATE, UNVERIFIED). The Chinese terminal, SMA, SIM and M12 parts have no published vibration data.
2. **Terminals: reliability vs cost.** Flanged pluggable (recommended, ≈ INR 9–11 per pole) or fixed screw terminals (≈ INR 5.3–6.6 per pole)? The difference is ≈ +201 on the Fieldbus controller, +130 on Wi-Fi + BLE, +114 on LoRa, +22 on the 4G card. A middle path to evaluate: non-flanged plugs (≈ INR 5.5–9 per pole) held in place by a hinged terminal cover moulded into the enclosure; needs the shaker test.
3. **DO current.** At 4 A per output, one L+ pole cannot feed 5 outputs (20 A vs an 8 A pole). Choose: (a) limit each L+ group to 8 A total; (b) one L+ pole per 2 outputs (+3 poles on the Fieldbus controller, ≈ +INR 30); (c) a 5.08 mm power plug for L+. Also, the TPS274160B limits at 0.5–2.5 A per channel (IO-1), so 4 A outputs need a different switch.
4. **Mis-plug protection.** Accept plug colours + labels, or also pay for coding pins (≈ INR 1–3 per plug, ESTIMATE)?
5. **RJ45 temperature (D-28).** HanRun HR911105A (INR 95.7, 0…70 °C) or an industrial −40…85 °C jack (≈ INR 160, over the INR 100 cap)?
6. **SMA thread length.** Confirm the enclosure wall thickness so the board-mounted SMA can take a nut and lock washer; otherwise a long-thread version (price to check).
7. **SIM access and eSIM.** OK to put the hinged nano-SIM behind a small front door? Add an MFF2 eSIM footprint as SIM 2 (depends on the EC200U dual-SIM test and an operator offer)?
8. **Vehicle power.** Should the vehicle port also power the module? Then the input front end needs ISO 16750-2 load-dump and 24 V jump-start protection (≥ 60 V rated parts; ≈ +INR 30–80 per module, ESTIMATE). Otherwise the M12 carries CAN only.
9. **Vehicle port standard or option.** The M12 adds ≈ INR 159 BOM to two modules. Standard (as asked) or an assembly option?

## 6. Sources

1. [S1] Phoenix Contact MC 1,5/3-STF-3,81 (1827716), MC 1,5/5-STF-3,81 (1743171), FMC 1,5/2-STF-3,81 (1748354), SPTAF 1/10-3,5 (1862013) product PDFs (vibration values via search snippets; direct download blocked) — https://www.phoenixcontact.com/us/products/1827716/pdf ; https://www.phoenixcontact.com/us/products/1743171/pdf
2. [S2] WAGO 2091-1127 picoMAX 3.5 data sheet — https://cdn.soselectronic.com/productdata/fd/59/d0e4242b/2091-1127.pdf (saved)
3. [S3] WAGO picoMAX pluggable connection system brochure, p. 5 and p. 77 (vibration test) — https://automationdistribution.com/content/Wago-Pluggable-Connection-System-picoMAX.pdf (2 pages saved)
4. [S4] element14 Singapore, WAGO 2091-1104 — https://sg.element14.com/wago/2091-1104/terminal-block-pluggable-4pos/dp/3278523
5. [S5] RS Ireland, Phoenix MC 1.5/3-STF-3.81 — https://ie.rs-online.com/web/p/pluggable-terminal-blocks/1703919
6. [S6] LINK-PP LPJ4011 data sheet — https://cdn.l-p.com/file/datasheet/lpj4011-8g44s0r.pdf
7. [S7] Würth 7499010211A at Bürklin / RS Germany — https://www.buerklin.com/en/p/wuerth-elektronik-eisos/modular-connectors/7499010211a/73F2285
8. [S8] GCT USB4105 drawing — https://gct.co/files/drawings/usb4105.pdf (saved)
9. [S9] I-PEX MHF I LK / MHF 4L LK — https://www.i-pex.com/product/rf/robust-design-integrated-locking-features ; https://www.futureelectronics.com/ftm/industrial-robotics-industry-5-0/i-pex-mhf-i-lk-and-mhf-4l-lk-micro-rf-connectors/
10. [S10] Hirose U.FL series — https://www.hirose.com/product/series/U.FL ; Amphenol AMC (SV Microwave) — https://www.svmicrowave.com/ufl-rf-series
11. [S11] Quectel EC200U series page — https://www.quectel.com/product/lte-ec200u-series ; Quectel forum, EC200U dual SIM — https://forums.quectel.com/t/ec200u-dual-sim-support/13101
12. [S12] TE DEUTSCH DT product spec (108-151009) — https://www.mouser.com/pdfdocs/TE-DEUTSCH-DT-Connectors-ProductSpec.pdf ; TE DT inline catalogue — https://www.te.com/content/dam/te-com/documents/industrial-and-commercial-transportation/global/dt-inline-catalog.pdf
13. [S13] SparkFun OBD-II to DB9 cable at Tanotis India — https://tanotis.com/collections/cables/products/genuine-sparkfun-obd-ii-to-db9-cable ; CSS Electronics M12–DB9 CiA 303-1 cable — https://www.csselectronics.com/products/m12-db9-cable-5-pin
14. [S14] DNA Tech India, Degson — https://www.dnatechindia.com/degson.html ; IndiaMART pluggable plugs — https://m.indiamart.com/impcat/terminal-block-pluggable-plug.html
15. [S15] HMS Ixxat CAN connector pinouts (CiA 303-1 DB9) — https://www.hms-networks.com/de/support/tech-support/kb-articles/26602569633426-CAN-Steckerbelegung ; WIKA manual, M12 CiA 303-1 pinout — https://www.manualslib.de/manual/1099893/Wika-F5301.html?page=24 ; CiA 303 series — https://www.can-cia.org/can-knowledge/cia-303-series-canopen-related-documents
16. [S16] SAE J1939/13 (2024) — https://saemobilus.sae.org/standards/j193913_202408-off-board-diagnostic-connector ; Copperhill J1939-13 pinout — https://copperhilltech.com/blog/tag/SAE+J1939-13 ; Deutsch HD10 Type II — https://www.oemoffhighway.com/electronics/connectors/electrical-electronic-components/product/10716129/deutsch-industrial-connectors-hd10-series-j193913-type-ii-diagnostic-connectors ; J1962 pinout as shown on the SparkFun OBD-II cable page — https://www.sparkfun.com/obd-ii-to-de9-cable.html
17. [S17] IEC 61131-2 vibration levels as quoted by a PLC maker — https://cimon.atlassian.net/wiki/spaces/PLC/pages/4694737834 ; ISO 16750-3:2023 — https://standards.iteh.ai/catalog/standards/iso/948d0715-7e28-448b-82f1-d0d5f31bac0c/iso-16750-3-2023
18. [S18] Phoenix Contact, mechanical tests for terminal blocks — https://www.phoenixcontact.com/en-sg/quality-tests/quality-tests-for-terminal-blocks/basic-principles-quality-testing-for-terminal-blocks/mechanical-tests-terminal-blocks ; IEC 60947-7-4:2019 — https://webstore.iec.ch/publication/60186
19. [S19] IEC 60603-7 plug retention (50 N, 60 s) and vibration (≤ 10 µs) as cited in a jack data sheet — https://www.farnell.com/datasheets/2663125.pdf
20. [S20] LCSC product pages, read 2026-11-20 — https://www.lcsc.com/product-detail/<C-number>.html for C441118–C441125, C3040571, C160125–C160129, C440856–C440864, C441184–C441188, C506990–C506999, C528716, C5632693, C7244, C7247, C14234, C474932, C474933, C5188455, C2838108, C7603448, C12074, C50933, C6885266, C3179562, C53281908, C3020560, C165948, C411575, C20617215, C2943124, C266890, C7529386, C7529385, C7423416, C7423411, C21340040, C77831–C77837, C5341785
21. [S21] Degson 15EDGKM-3.81 product page (12 A / 250 V) — https://fr.degson.com/content/details_552_2761721.html

## Appendix A — raw findings (saved during the search)

- [N1] Phoenix MC 1,5/..-STF-3,81 (pluggable, screw flange): vibration per IEC 60068-2-6:2007-12, 10–150–10 Hz, 0.35 mm (10–60.1 Hz) / **5 g** (60.1–150 Hz), 2.5 h per axis. Same 5 g for FMC 1,5 push-in and SPTAF push-in 3.5 mm. Phoenix site blocks scripted download (Access Denied); values from search snippets of Phoenix PDFs 1827716, 1743171, 1748354, 1862013. [S1]
- [N2] WAGO picoMAX 3.5 (2091 series): push-in CAGE CLAMP, female plug latches into a shrouding male header. Tested to EN 60068-2-6, 5–2000 Hz, 10 g → 14 → 16 → **20 g, no failure** (criterion: < 50 % or < 5 mΩ contact-resistance rise, no interruption > 20 ns), with 1.5 / 2.5 mm² wires. 10 A IEC / 10 A UL 1059 (Use B and D, 300 V), 160 V III/3, 0.2–1.5 mm² (24–14 AWG), strip 8–9 mm, PPA GF V0, CrNi spring, tin-plated Cu. Not hot-pluggable under load (IEC 61984). [S2][S3]
- [N3] LCSC live product pages read 2026-11-20 (price at the 100-unit ladder step, or the step that covers 100; USD × 93.9):
  - Cixi Kefa KF2EDGK-3.81 plug (no flange): 2P USD 0.1278 = INR 12.0 (C440858); 8P USD 0.3189 = INR 29.9 (C440864, 7,631 stock); 12P USD 0.4809 = INR 45.2 (C440856). Rated 7–8 A, 250–300 V, 16–28 AWG, −40…105 °C.
  - Kefa KF2EDGR-3.81 right-angle header: 4P INR 8.0 (C441184), 5P INR 11.5 (C441185), 8P INR 13.9 (C441188).
  - Degson 15EDGKM-3.81 plug with screw flange: 2P INR 34.7 (C528716), 3P INR 46.9 (C506996), 4P INR 58.6 (C506997), 6P INR 71.0 (C506999). Degson 15EDGKDM-3.81-06P INR 107.3 (C5632693). Degson plain 15EDGK-3.81-06P INR 65.7 (C506990).
  - Ningbo Kangnex WJ15EDGK-3.81 plug: 4P INR 24.5 (C7244, 64,925 stock), 6P INR 29.2 (C7247), 8P INR 34.1 (C14234); WJ15EDGKA-3.81-04P INR 36.6 (C8405).
  - Fixed screw terminals 3.81 mm: Kefa KF128L-3.81-2P INR 12.3 (C474932), 3P INR 16.0 (C474933); MAX MX128H-3.81-03P INR 15.2 (C5188455); Dorabo DB125-3.81-12P INR 79.2 (C2838108). Fixed 3.81 mm ≈ INR 5.3–6.6 per pole at 100 units, not INR 2 as in today's costing.
  - Dorabo DB2EVM-3.81-12P header with flange INR 36.1 (C430351); DB2ERH-3.81-2×12P INR 141.3 (C2826460).
  - Weidmüller 1235920000 on LCSC: USD 26 at 1 / 10.4 at 200, 0 stock.
- [N4] WAGO 2091-1104 (picoMAX 3.5 4P plug): element14 Singapore S$8.09 each (≈ INR 580, one-off). Mouser / element14 India pages could not be read (scripted access blocked). [S4]
- [N5] Degson / Kefa / Kangnex publish no IEC 60068-2-6 vibration data in the listings and pages found; Degson's own page gives 12 A / 250 V vs LCSC 8 A / 300 V for 15EDGKM [S21].
- [N6] Push-in pluggable (Chinese): Degson 15EDGKNH-3.5-04P plug INR 61.8 (C7603448, 420 stock); 15EDGKN-3.5-05P INR 82.6 (C7603443). Degson lists latch and flange push-in variants (15EDGKNHB…, 15EDGKNHM) on degson.com, not on LCSC.
- [N7] Phoenix MC 1,5/3-STF-3,81 (1827716): RS Ireland €662.25 per box of 250 = €2.65 each (≈ INR 270 per 3-pole plug). Phoenix Contact India quote needed. [S5]
- [N8] RJ45 magjacks (LCSC live): HanRun HR911105A INR 95.7, 0…70 °C, 57,640 stock (C12074); HR911130C INR 169 (C50933); HR911130A INR 164 (C54408); HR911103A INR 112 (C375844); HR851178A INR 163 (C2931908); HanRun "E" suffix −40…85 °C only on gigabit / multi-port parts (HR911297CE INR 340, HR915410AE INR 409); Pulse JX3V-9015NL −40…85 °C USD 1.6953 at 220+, 0 stock (C6885266); Bel V895-1001-AW USD 3.29 at 200+, 0 stock (C3179562); USAKRO DGUK411Q199DB2A1DP INR 286 (C19725137); LINK-PP LPJES101-0AGNL INR 90.8 (C53281908). Würth 7499010211A ≈ €7.48 at 62+ at RS Germany. [S6][S7]
- [N9] USB-C: GCT USB4105-GF-A — VBUS 5 A, 48 V, −40…85 °C, 20,000 cycles, mating 5–20 N, un-mating 6–20 N after test, stainless shell, through-hole shell stakes; LCSC INR 60.4 (C3020560); 16-pin -120 variant INR 49.6 (C5184243, 0 stock). Hroparts TYPE-C-31-M-12 INR 14.0 (C165948), −30…80 °C, 20 V. [S8]
- [N10] SMA (LCSC live): Kinghelm KH-SMA-K513-G R/A THT INR 36.8 (C411575); HenryTech HL-SMA-KE-02 edge INR 20.6 (C20617215); DreamLNK SMA-KWE901 (RP-SMA) INR 54.0 (C914553); RF Solutions CON-SMA-EDGE-S INR 177 (C5356059, 0 stock).
- [N11] Micro-RF retention: I-PEX MHF I un-mating 5 N min initial, 3 N after 30 cycles; MHF I LK 20 N min, 10 N after 30 cycles; MHF 4L LK 23 N lock-engaged; Hirose U.FL: consult Hirose for automotive; Amphenol AMC withdrawal 1.5 lbf. [S9][S10]
- [N12] Nano-SIM (LCSC live): GCT SIM8060 hinged INR 151.8 (C2943124); Shou Han XG6P flip-top INR 11.0 (C7529386); hanxia XG6P INR 11.5 (C19189033, −40…70 °C); XUNPU SMN-305 INR 16.0 (C266890); BXCONN SIM303-GZ6P INR 5.1 (C36936578); Shou Han TL6P push-pull INR 15.0 (C7529385). Molex hinge nano-SIM datasheet 987652-0671 not downloadable.
- [N13] EC200U dual SIM: Quectel dual-SIM single-standby application note (AT+QDSIM) exists; a Quectel forum reply says a switching circuit is needed. [S11]
- [N14] TE DEUTSCH DT: 10–2000 Hz sine, 20 g, 12 h (MIL-STD-1344 M2005.1), no unlocking; DT inline catalogue: 21 g RMS. LCSC: DT04-2P-RT02 ≈ USD 8.0 at 100 (C5341785); DT04-6P-EP14 USD 28 (C17333311). [S12]
- [N15] D-sub (CONNFLY, LCSC live): DS1037-15MNCKT74 R/A plug INR 36.4 (C77837); DS1037-15FNAKT76 INR 34.2 (C77836); DS1034-09FUNSi44 9-pos INR 31.8 (C77831).
- [N16] M12 A-coded 5-pin male PCB receptacle (LCSC live): CAZN M12-P5A-GPBM12 INR 158.6 (C7423416, 45 stock), M12-P5A-GPFM16 INR 168.1 (C7423411, 174 stock); IP67, 4 A, 60 V, −25…80 °C. Amphenol M12A-05PFFC-SF8C15 USD 2.92 at 200+, 0 stock (C21340040); XKB TFA.M12.P05.NPAE INR 513 (C7549019).
- [N17] OBD-II ↔ DB9 cables: SparkFun (DB9 3 CAN-H, 5 CAN-L, not CiA) ₹1,240 at Tanotis India; CSS Electronics DB9-OBD2 adapter USD 65. [S13]
- [N18] Kefa KF2EDGKM-3.81 flange plugs: 2P INR 25.5 (C441118), 3P 25.0 (C441119), 4P 30.6 (C441120), 5P 38.7 (C441121), 6P 47.0 (C441122), 7P 52.3 (C441123, 3 stock), 8P 56.9 (C441124, 294 stock), 9P 62.6 (C441125), 14P 90.9 (C3040571, 2 stock). Kangnex WJ15EDGRM-3.81 flange headers: 3P 9.5 (C160129), 4P 10.6 (C160127), 6P 13.6 (C160126), 10P 18.5 (C160125).
- [N19] India: Degson 3.81 mm via DNA Tech (Rs 6.46 + GST per 2-pin plug), Robu, Electronicscomp; IndiaMART 2-pin 3.81 mm plugs at ₹4–8.30 (unbranded, no traceability). [S14]
- [N20] Pinouts: CiA 303-1 M12 (1 shield, 2 V+, 3 GND, 4 CAN_H, 5 CAN_L), DB9 (2 CAN_L, 3 GND, 7 CAN_H, 9 V+); J1939-13 (A batt −, B batt +, C CAN_H, D CAN_L, E shield, Type I black 250 k, Type II green 500 k); J1962 (4 / 5 GND, 6 CAN_H, 14 CAN_L, 16 batt +). [S15][S16]
- [N21] IEC 61131-2 ≈ 1 g (9–150 Hz); ISO 16750-3:2023 test VII commercial vehicle sprung mass (values not retrieved). [S17]
- [N22] IEC 60947-7-4 relies on IEC 60999 pull-out tests (Phoenix report: 1.5 mm² > 40 N); no vibration test found in it. [S18]
- [N23] IEC 60603-7: plug retention 50 N for 60 s (§6.6.2); vibration with no discontinuity > 10 µs (§7.7.2.5). [S19]
