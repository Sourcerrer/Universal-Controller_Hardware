# R23 — Stack-bus, battery-board and 18650 connectors for 10 g vibration

Status: v1, 2026-11-20. Replaces the connector part of R07 (40-pin Hirose FX18 study). R07 is obsolete for the bus since the bus became 4 pins (SYS-11, MECH-3, 2026-11-16).

Owner request (2026-11-20): "finalize the connectors that will be used. Regularly available, flexible, automotive & industrial grade connectors that can sustain up to 10 g of vibration."

Scope: (1) the 4-pin stack bus between modules, (2) the connector between a module's logic PCB and the optional battery + charger board, (3) 18650 cell retention. Field connectors are out of scope (R24).

Price basis: 100 units, INR, **USD 1 = INR 94.0** (same rate as R07). LCSC prices were read from the LCSC product API on 2026-11-20. LCSC prices exclude freight and Indian duty (ESTIMATE +15–25 % landed). No DigiKey prices are used (owner rule).

How "flexible" was read: as tolerant of module width, order and misalignment, and usable both in a stack and standalone. A short flexible jumper meets this better than a rigid bridge. If the owner meant something else (e.g. a flexible PCB), see §6 question 1.

## 1. Executive summary

| Position | Recommended | Lower-cost alternative | Rejected |
|---|---|---|---|
| **Stack bus (4 pins)** | **Molex Micro-Fit 3.0**, 4-circuit dual row. Two right-angle headers **43045-0400** per module (left and right), joined by a short flexible jumper: 2 × receptacle **43025-0400** + 8 × crimp terminal **43030-0001** (reel) / **43030-0007** (bag) + 4 × 20 AWG. ≈ **INR 85 per module** | (a) Chinese Micro-Fit-compatible header **HCTL HC-MX3.0-2\*2AW** with the same Molex jumper: ≈ INR 61. (b) One header plus a captive pigtail per module: ≈ INR 44 | Phoenix TBUS (5 g, 25 cycles, ≈ INR 950–1,270 each); pluggable 3.81 mm COMBICON (5 g); pogo pins (no lock); rigid bridge plugs; Hirose FX18 |
| **Battery board ↔ logic PCB** | **2 × 4, 2.54 mm gold board-to-board**: socket **CJT A2541HWV-2x4P** on the logic PCB, gold pin header on the battery board, board fixed by M3 standoffs (PC/104 practice). ≈ **INR 27** incl. standoffs | **CONNFLY DS1023-2\*4SF11** socket, same layout: ≈ INR 21. Automotive-rated option at higher cost: **Molex DuraClik** 6-pos pigtail (3 A, LV214 claim) ≈ INR 50–58 | JST GH (1 A per contact); JST PUD (only −25 °C); friction-lock JST PH / XH |
| **18650 holder** | **MYOUNG BH-18650-A5BJ001-2D** through-hole holder (LCSC C19184083, ≈ INR 45) + nylon cable tie through two PCB slots + foam pad on the cover | Indian generic through-hole holder (≈ INR 16–22 retail, unbranded) with the same tie and pad | Keystone 1042 / 1043 (INR 460) and MPD BK-18650-PC2 (INR 259): fine parts, but 2–5× the whole board budget; glue or potting (blocks cell replacement, SAF-6) |

Key findings:

1. **10 g is about 10× the PLC standard.** IEC 61131-2 asks for 1 g (8.4–150 Hz). The DIN-rail bus parts made for PLCs are rated for 5 g only: Phoenix TBUS and Phoenix pluggable COMBICON, both IEC 60068-2-6, 0.35 mm / 5 g [S1][S5].
2. **No 4-pin bus connector found has a published 10 g sine rating and a positive lock.** Mill-Max spring contacts publish 10 g sine and random (IEC 60068-2-6 Fc / 60068-2-34), 50 g shock and no event > 1 µs [S15], but they have no lock and cost far more than the budget. Molex Micro-Fit 3.0 publishes random vibration to EIA-364-28 condition VII-D and 50 g shock (EIA-364-27 H), with no event > 1 µs [S7]. Its latch gives positive retention.
3. **So a datasheet alone cannot prove 10 g.** The proof must be a system test: a full stack on a DIN rail, energised, IEC 60068-2-6 at 10 g, with event detection on the bus. This needs an Indian test lab quote (§6).
4. **Cost gap (rule 1: reliability first, gap reported).** Today's BOM line "4-pin bus connectors + bridge share + RS-485 transceiver + ESD" is INR 58–59. That leaves only ≈ INR 27 for connectors and bridge (ESTIMATE). The recommended Micro-Fit bus costs ≈ INR 85: **+INR 58 BOM per module, +INR 87 finished cost (× 1.5)**. A 4-module stack adds ≈ INR 232 BOM. The battery board rises ≈ INR 54 (≈ INR 259 vs the owner's "below 200 rupees" including the cell).
5. **Sourcing.** Micro-Fit 3.0 is the most widely copied 3.0 mm power connector. Molex stock at LCSC is ≈ 48,000 headers and ≈ 47,000 housings. Intermateable sources: Würth WR-MPC3 (in stock at Lion Circuits, INR 60.28 at 100) [S14], Amphenol Minitek Pwr 3.0 (UNVERIFIED this session), and Chinese makers (HCTL and others). The same Molex header costs INR 143 at 100 from Lion Circuits [S13], against ≈ INR 25 at LCSC, so import through LCSC or a Molex franchise quote is needed.

## 2. Requirements

None of these values is in the PRD yet, except where a PRD ID is given. Proposed IDs are for the main session to add; this report does not edit the PRD.

| # | Requirement | Value | Basis |
|---|---|---|---|
| C-1 | Bus contacts | 4: BUS_V, GND, RS485_A, RS485_B, passed straight through every module | SYS-11, MECH-3 (O) |
| C-2 | Current per power contact | ≥ 3 A continuous at +85 °C ambient. Load through the first jumper ≈ 1.7 A at 12 V, 2.2 A at 9 V | SYS-11 (O), PWR-8 |
| C-3 | Voltage | ≥ 50 V DC (bus 5–32 V; TVS clamp ≈ 40 V); SELV only | PWR-1, PWR-10 |
| C-4 | **Vibration** | **10 g** (owner, 2026-11-20). Proposed test: IEC 60068-2-6 Fc, sine 10–500 Hz, 0.75 mm below ≈ 57.6 Hz, 10 g above, 10 sweep cycles per axis, 3 axes, energised. Bus monitored for interruptions > 1 µs (IEC 60512-2-5 / EIA-364-87). Plus shock IEC 60068-2-27, 30 g / 11 ms (proposed) | New, proposed MECH-7 (O for 10 g, P for the test profile) |
| C-5 | Retention | Positive latch or screw. Must not unmate during C-4 | Owner, 2026-11-20 |
| C-6 | Polarisation | Keyed; cannot mate rotated or offset (a BUS_V ↔ GND swap would short the stack supply) | Safety |
| C-7 | Mating cycles | ≥ 25 (installation and service only; not hot-pluggable) | R07 §5, RevPi precedent |
| C-8 | Temperature | Connector rating ≥ −40…+105 °C (includes self-heating at 3 A) | Industrial practice |
| C-9 | Supply | Easy to buy in India; ≥ 2 intermateable sources; ≥ 5 years longevity | Part rule 5 (CLAUDE.md) |
| C-10 | Touch and ESD | Exposed bus header on a standalone or end module is covered | EMC-3 (P) |
| C-11 | Cost | Stay near today's ≈ INR 27 per module for connectors + bridge (ESTIMATE); report the gap | Cost rules |
| B-1 | Battery-board signals | 5 V (≤ 2 A), GND, SDA, SCL, INT_N, DETECT_N (6 minimum; 8 with doubled power pins) | PWR-2 |
| B-2 | Battery board retention | Screwed or latched; meets C-4 | Owner, 2026-11-20 |
| H-1 | 18650 retention | Cell stays in contact at 10 g. Cell mass ≈ 45–48 g, so the inertial load is ≈ 4.6 N | C-4 |
| H-2 | User-replaceable cell | No glue or potting on the cell | SAF-6 (P), REG-7 |
| H-3 | Holder material | Flame-retardant (UL 94 V-0 preferred) next to a Li-ion cell | IEC 62368-1 practice |

What "10 g" means in datasheets:
- The classic connector test (MIL-STD-202 method 201, and many JST, Hirose and JAE datasheets) is 10–55 Hz with 1.52 mm total excursion. At 55 Hz that is ≈ 9.3 g peak. It is often quoted as "10 g" (recalled; not re-checked this session).
- EIA-364-28 condition VII-D (Micro-Fit) is a random profile, ≈ 3.1 g rms over 20–500 Hz (level recalled; verify against EIA-364-28F). Random peaks reach ≈ 3σ ≈ 9 g. It is not equivalent to a 10 g sine dwell.
- IEC 60068-2-6 Fc with a 0.75 mm / 10 g crossover at ≈ 57.6 Hz is the IEC form of the same "10 g" level. C-4 uses it.

## 3. Comparison tables

### 3.1 Stack bus (4 positions)

| Part | Maker | Pitch | Current per contact | Vibration rating + standard | Locking | Cycles | Temp | 100-unit INR | Source | India | Second source |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **Micro-Fit 3.0 R/A header 43045-0400 (tin)** + housing 43025-0400 + terminal 43030-0001 | Molex | 3.0 mm, 2 × 2 | 5 A IEC / 8 A UL (43045) | Random EIA-364-28 VII-D, 15 min/axis; shock 50 g EIA-364-27 H; < 1 µs | Latch on housing; snap-in PCB pegs | 30 (tin) | −40…+105 °C | Header 25.3; housing 7.4; terminal 1.4 | LCSC C122413, C122417, C259786 [S8][S9][S11] | Lion Circuits header INR 143 [S13]; element14 / Mouser India | Würth WR-MPC3; Amphenol Minitek Pwr 3.0 (UNVERIFIED); HCTL and other Chinese |
| Same, **gold**: header 43045-0401 + terminal 43030-0002 | Molex | 3.0 mm | 5 A IEC / 7 A terminal | As above | As above | > 30 (gold; Molex figure not checked) | −40…+105 °C | Header 67.3; terminal 4.7 | LCSC C585880, C246762 [S10][S11] | As above | As above |
| WR-MPC3 66200421022 (R/A, 2 × 2, pegs) | Würth | 3.0 mm | 5 A | Not in sources read | Micro-Fit-compatible latch | Not checked | Not checked | **60.28 (India)** | Lion Circuits [S14] | In stock, 7–10 days | Molex |
| HC-MX3.0-2\*2AW (R/A, 2 × 2) | HCTL (China) | 3.0 mm | Not checked | None published | Micro-Fit-compatible latch | Not checked | Not checked | 13.7 | LCSC C3294383 [S12] | Import | Many Chinese |
| DuraClik 4-pos | Molex | 2.0 mm | 3.0 A | "High vibration"; meets LV214 (Arrow) | Inner/outer latch, TPA | 30 | −40…+105 / +125 °C | ≈ 30 header + 7.5 housing | LCSC [S18] | Import | None intermateable |
| ME 22,5 TBUS 1,5/5-ST-3,81 (2707437 / 2713722) + ME TBUS PST strip | Phoenix Contact | 3.81 mm, rail-mounted | 8 A (parallel contacts) | **5 g**, IEC 60068-2-6, 10–150 Hz; shock 15 g | None; held by the housing on the rail | **25** | −40…+105 °C | **≈ 950–1,270 each** (USD 10.12–13.49, single units) | TTI / Mouser via myMectronic [S4] | Phoenix India | Weidmüller CH20M BUS (not intermateable; 5 A, 63 V; vibration not found [S6]) |
| MC 1,5/4-STF-3,81 plug + MCV 1,5/4-GF-3,81 header (screw flange) | Phoenix Contact | 3.81 mm | 8 A | **5 g**, IEC 60068-2-6, 10–150 Hz | Screw flange | Not stated | −40…+100 °C | ≈ 60–120 per pair (ESTIMATE, UNVERIFIED) | Phoenix datasheets [S5] | Phoenix India | Degson, Dinkle (fit not guaranteed) |
| Spring-loaded (pogo) strip + gold pads | Mill-Max | 2.54 mm | 2 A cont. / 3 A peak | **10 g sine (IEC 60068-2-6 Fc) and 10 g random (IEC 60068-2-34); 50 g shock; < 1 µs at 0.5 A** | **None**; needs rail end clamps to hold modules together | 1,000,000 | −55…+125 °C | ≈ 300–700 for 6 pins (ESTIMATE, UNVERIFIED) | Mill-Max test report [S15] | Mouser India | CFE, Preci-Dip; Chinese pogo (kinghelm KH-A25010-06P ≈ INR 18.8, no ratings) [S16] |
| FX18 (R07 choice) | Hirose | 0.8 mm | 0.5 A signal / 3 A guide | 10–55 Hz, 0.75 mm (≈ 9 g) | Guide posts, no latch | 500 | −55…+85 °C | ≈ 211 per header | LCSC C598060, stock 0 [S17] | Poor | None |

Notes on rejected options:
- **Phoenix TBUS.** It is the cleanest topology (the bus sits in the rail; any module can be lifted out). But it is rated 5 g and 25 cycles. It costs about INR 1,000 per module. It also forces a Phoenix-style housing interface on the INR 100–180 Indian enclosures.
- **Pluggable 3.81 mm terminal blocks with screw flange.** Positive lock, but rated 5 g like all Phoenix COMBICON parts found. Bulky for 4 pins.
- **Pogo pins on a side wall.** The only 10 g data found, and 1 M cycles. But there is no lock: contact depends on the DIN-rail end clamps pressing the modules together. Exposed gold pads collect dust in Indian cabinets. Two pins per power rail are needed (2 A each). Branded parts blow the budget; Chinese parts have no data.
- **Rigid bridge plug (RevPi / Opta style).** Two modules clipped to a rail move slightly against each other at 10 g. A rigid bridge passes this motion into the contacts and causes fretting. A flexible jumper does not.
- **JST VH / XH / PH.** Friction lock only, not positive lock.

### 3.2 Battery board ↔ logic PCB (6–8 positions, ≤ 2 A)

| Part | Maker | Pitch | Current per contact | Vibration rating + standard | Locking | Cycles | Temp | 100-unit INR | Source | India | Second source |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **A2541HWV-2x4P socket (gold, brass)** + 2 × 4 gold pin header + M3 standoffs | CJT (China) | 2.54 mm | ≈ 3 A (2.54 mm class) | None published; retention by standoffs (PC/104 practice) | Screws | Not checked | Not checked | Socket 12.9; header ≈ 4 (EST); standoffs + screws ≈ 10 (EST) | LCSC C239344 [S22] | Import; generic parts sold everywhere | Any 2.54 mm maker |
| DS1023-2\*4SF11 socket | CONNFLY (China) | 2.54 mm | ≈ 3 A | None published | Screws | Not checked | Not checked | 8.5 | LCSC C92271 [S22] | Import | Any |
| TSW-104-07-G-D header + SSW-104-01-G-D socket | Samtec | 2.54 mm | ≈ 3 A | Samtec publishes test reports (not checked here) | Screws | Not checked | −55…+125 °C (typ., not checked) | 68.2 header + ≈ 80 socket (EST) | LCSC C3333874 [S22] | Mouser India | Harwin M20 (3 A; 300 cycles gold; catalogue 3.13 g random 50–2000 Hz, 30 g shock) [S21] |
| DuraClik 6-pos: header 5023520600 (R/A SMD) or 5600200620 (vertical SMD) + housing 5023510600 | Molex | 2.0 mm | 3.0 A | "High vibration"; LV214 (Arrow) | Inner/outer latch + TPA | 30 | −40…+105 / +125 °C | 29.9 or 34.3 + 7.5 + 6 terminals ≈ 15 (EST) | LCSC C114106, C177237, C294024 [S18] | Import | None intermateable |
| Micro-Fit 3.0 2 × 3: header 43045-0600 + housing 43025-0600 | Molex | 3.0 mm | 5 A IEC | Random EIA-364-28 VII-D; 50 g shock | Latch | 30 | −40…+105 °C | 37.9 + 8.9 + 6 × 1.4 | LCSC C127367, C293525 [S29] | As bus | As bus |
| GH 8-pos | JST | 1.25 mm | 1.0 A (AWG 26) | Not in catalogue | "Secure lock" | Not checked | −40…+105 °C | Not priced | JST catalogue [S20] | Robu clones | Chinese GH clones |
| PUD 2 × 4 | JST | 2.0 mm | 3 A (AWG 22) | Catalogue: "strong lock against vibration" (no level) | Lock | Not checked | **−25…+85 °C** | Not priced | JST catalogue [S20] | Limited | — |
| Micro-Lock Plus 2.0 | Molex | 2.0 mm | 4.7 A (AWG 22) | None published | Positive latch | Not checked | −40…+105 °C | Not priced | Molex datasheet [S19] | Import | — |

### 3.3 18650 holder and retention

| Part | Maker | Mount | Contacts | Body | Vibration data | Temp | 100-unit INR | Source | India | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| **BH-18650-A5BJ001-2D** | MYOUNG | Through-hole | Ni-plated | Not stated | None | −10…+100 °C | **45.0** (stock 513) | LCSC C19184083 [S26] | Import | Recommended with strap + pad |
| BH-18650-A6AJ022 | MYOUNG | Through-hole, posts | Ni, double negative spring | PA46 | None | Not checked | 72.6 (stock 14) | LCSC C51883817 [S26] | Import | Stronger spring; stock too low |
| BH-18650-B1BA002 | MYOUNG | SMT | Gold on phosphor bronze | PBT / PA66 / PPA / PA9T options | None | −25…+85 °C | 96.1 (stock 1,717) | LCSC C2988620 [S26] | Import | SMT tabs are weaker than THT pins at 10 g |
| 1042 (SMT) / 1043 (THT) | Keystone | SMT / THT | 1042: gold | Not checked | None | Not checked | **460.09** (1042) | Lion Circuits [S23] | In stock | Premium |
| BK-18650-PC2 | MPD | THT | Ni-plated steel | PP | None | Not checked | **259.43** | Lion Circuits [S24] | In stock | 21.4 mm high |
| BH-18650-PC | MPD | THT | 302 SS spring temper, Ni, dual pressure | PBT, UL 94 V-0 | None | −40…+180 °C (MPD page) | Not priced | MPD [S25] | Lion Circuits lists it | Best material data found |
| Generic PCB holder | Unbranded (India) | THT | Spring steel | Unknown | None | Unknown | ≈ 16–22 retail incl. GST | Makerbazar, Hubtronics, Majestronicz, Robu [S27] | Local | No material or force data |

Retention options (all ESTIMATE prices):

| Method | Cost | Effect at 10 g | Cell still user-replaceable? |
|---|---|---|---|
| Nylon 66 cable tie through 2 PCB slots around cell + holder | ≈ INR 1–3 | Clamps the cell radially; friction adds axial hold | Yes (cut and replace; ship a spare or use a releasable tie) |
| Hook-and-loop strap through slots | ≈ INR 4–6 | Same, reusable | Yes, easiest |
| EPDM / PU foam pad (2–3 mm) on the inside of the cover, pressing on the cell | ≈ INR 2–4 | Stops lift-out; damps | Yes |
| Moulded rib in the cover | INR 0 (tooling) | Same as pad, but hard contact | Yes |
| RTV silicone or hot-melt dabs | ≈ INR 2 | Good | **No** — conflicts with SAF-6 |
| Tabbed cell soldered to the PCB | — | Best | **No** — conflicts with SAF-6 |

Engineering check: a 45–48 g cell at 10 g pulls with ≈ 4.6 N. Open holders grip the cell radially only by a light snap, and no holder maker publishes spring force. So the strap or pad is mandatory. Axially, the spring preload should be ≥ 2 × 4.6 ≈ 9 N, or the strap friction must make up the difference. Measure the spring force on samples before freezing the holder.

## 4. Recommendation and BOM delta

### 4.1 Stack bus — Molex Micro-Fit 3.0, two headers per module plus a flexible jumper

- Each module carries two identical **43045-0400** right-angle headers (BUS-L, BUS-R). All four pins are joined on the PCB, so the bus passes straight through. Any module order works.
- Each module ships with **one jumper** sized for its own width: ≈ 70 mm for 45 mm modules and ≈ 110 mm for the wider Fieldbus controller. It joins its own BUS-R to the right neighbour's BUS-L.
- Jumper: 2 × **43025-0400** housings, 8 × **43030-0001 / -0007** tin terminals, 4 × UL1007 20 AWG, 105 °C. Twist BUS_V with GND and RS485_A with RS485_B.
- Pin map (proposal): 1 BUS_V, 2 GND, 3 RS485_A, 4 RS485_B. The Micro-Fit peg shapes stop rotated mating.
- Crimping: Molex hand tool 63819-0000 for prototypes [S32]; an Indian harness shop with an applicator for production. Pull-test each lot (Molex minimum 57.8 N for 20 AWG [S7]).
- **Tin first, gold if the test shows fretting.** Molex's vibration and shock results in PS-43045 apply to the series [S7]. Tin can fret under long vibration. If the 10 g test shows contact resistance rising by more than 20 mΩ (Molex's limit), change to gold: header 43045-0401 and terminal 43030-0002 (+INR 110 per module). Never mix tin and gold halves.
- The end module's open header gets an **empty 43025-0400 housing as a cap** (INR 7.4). It latches on and covers the pins (EMC-3).
- 30 mating cycles is enough. The bus is not hot-pluggable and each jumper is plugged only at installation and service.

Bill of materials per module (LCSC, 100 units):

| Item | Qty | Unit INR | INR |
|---|---|---|---|
| Header 43045-0400 | 2 | 25.3 | 50.6 |
| Housing 43025-0400 | 2 | 7.4 | 14.8 |
| Terminal 43030-0001 | 8 | 1.4 | 11.2 |
| 20 AWG UL1007, 4 × ≈ 80 mm | — | — | ≈ 2 (EST) |
| Crimping, insertion and continuity test, 8 crimps | — | — | ≈ 6 (EST) |
| **Total** | | | **≈ 85** |

Lower-cost alternatives:
- **(a) Chinese Micro-Fit-compatible headers** (HCTL HC-MX3.0-2\*2AW, INR 13.7) with the Molex jumper: **≈ INR 61 (+34)**. Trade-off: no published vibration, plating or durability data. The fit to Molex housings is by dimension, not certified. Use it only if the same 10 g system test passes with it.
- **(b) Captive pigtail**: one header (BUS-L) per module, and BUS-R is a short cable soldered into the PCB with a 43025-0400 housing on its end: **≈ INR 44 (+17)**. Trade-off: a damaged cable means opening the module. The pigtail dangles on standalone and end modules and needs a parking clip. The cable exit through the housing needs strain relief.
- Indian-distributor sourcing for comparison: Würth WR-MPC3 headers at INR 60.28 from Lion Circuits give ≈ INR 155 per module; Molex headers from Lion Circuits give ≈ INR 320.

### 4.2 Battery board ↔ logic PCB

- **Recommended:** a 2 × 4, 2.54 mm gold board-to-board pair. Socket **CJT A2541HWV-2x4P** (LCSC C239344, INR 12.9) on the logic PCB; a gold 2 × 4 pin header on the battery board. Pins: 5 V × 2, GND × 2, SDA, SCL, INT_N, DETECT_N.
- Fix the battery board with **M3 standoffs**: two within ≈ 15 mm of the connector and two at the cell end. The standoffs carry the ≈ 70 g board-plus-cell mass (≈ 7 N at 10 g). The connector then sees almost no relative motion. This is the PC/104 practice for vehicles. Cost ≈ INR 27 including standoffs and screws (ESTIMATE).
- **Lower-cost:** CONNFLY DS1023-2\*4SF11 socket (INR 8.5) in the same footprint: ≈ INR 21. Trade-off: less documentation on gold thickness.
- **Automotive-rated alternative** (if the battery board cannot sit over the logic PCB, or if the test shows fretting): a Molex DuraClik 6-pos pigtail from the battery board to a 5023520600 header (3 A, latch + TPA, −40…+125 °C, LV214 claim): ≈ INR 50–58. A Micro-Fit 2 × 3 pigtail (≈ INR 61) keeps one connector family for the whole product.
- This connector is not "automotive grade" by name. Its robustness comes from the screwed mounting. The owner should accept this explicitly, or pay ≈ INR 30 more for DuraClik.

### 4.3 18650 cell

- **Recommended:** MYOUNG BH-18650-A5BJ001-2D through-hole holder (INR 45). Its PCB pins are soldered through, which is stronger than SMT tabs at 10 g. Add a nylon cable tie (or hook-and-loop strap) through two PCB slots around the cell, and a 2–3 mm foam pad on the cover. Retention ≈ INR 4.
- Before freezing it: measure the spring force (needs ≈ 9 N, H-1) and ask MYOUNG for the body material and UL 94 rating (H-3). The MYOUNG SMT variant lists PBT / PA66 / PPA / PA9T bodies.
- **Lower-cost:** an Indian generic through-hole holder (≈ INR 16–22 retail) with the same tie and pad. Trade-off: unknown plastic, unknown spring force, no traceability.
- **Premium:** MPD BH-18650-PC (PBT V-0, dual pressure contacts) or Keystone 1043 (INR 460 for the 1042 SMT twin).

### 4.4 Per-module connector BOM delta (100 units, ESTIMATE)

Today's bus line is INR 58–59 per module, including the RS-485 transceiver (≈ 26) and ESD (≈ 6). That leaves ≈ INR 27 for connectors and bridge (assumed baseline). The battery board line "18650 holder + small PCB + connector" is INR 32; the assumed split is holder ≈ 15, PCB ≈ 10, connector ≈ 7.

| Module | Baseline connectors | Recommended | Δ BOM | Δ finished (× 1.5) | Lower-cost (a) | Δ BOM | Lower-cost (b) pigtail | Δ BOM |
|---|---|---|---|---|---|---|---|---|
| Fieldbus controller | 27 | 86 (longer jumper) | +59 | +89 | 62 | +35 | 45 | +18 |
| 4G modem card (bus headers inside the INR 604 line; D-29) | 27 | 85 | +58 | +87 | 61 | +34 | 44 | +17 |
| Wi-Fi + BLE | 27 | 85 | +58 | +87 | 61 | +34 | 44 | +17 |
| LoRa | 27 | 85 | +58 | +87 | 61 | +34 | 44 | +17 |
| Battery board (optional, per module): connector + holder + retention | 7 + 15 + 0 | 27 + 45 + 4 | **+54** (board ≈ INR 259) | +81 | 21 + 18 + 4 | +21 (board ≈ INR 226) | — | — |

### 4.5 Check against cost targets

- **Fieldbus controller (BOM ≤ INR 2,000, hard limit):** every option adds cost to a module that is already over the limit (PRD COST-5, D-30). +INR 59 with the recommendation, +INR 18 with the pigtail.
- **Wi-Fi + BLE, 4G, LoRa:** +INR 58 BOM (+87 finished) each. The LoRa selling-price target of INR 1,600 is the tightest of these. The main session should check it against the current totals in `build_architecture.py`.
- **Battery board ("below 200 rupees" with the cell):** ≈ INR 259 recommended, ≈ INR 226 lower-cost. Both are over target. The holder alone (INR 45) is above the INR 32 that the BOM allows for holder + PCB + connector.
- **Recommendation to the owner:** take the recommended Micro-Fit bus (+58) and test it. If the test passes with Chinese headers, move to option (a) (+34) as the cost-down.

## 5. Mechanical notes

**Where the headers sit.** The logic PCB stands vertically, parallel to the side walls. A connector on each side wall would need a second board or a flex near the far wall. So put both right-angle headers on the PCB's top (or upper front) edge, mating face out through a recessed pocket in the housing, like the RevPi PiBridge sockets [S30]. The jumper lies in a moulded channel across the top of the neighbouring housings. A snap-on channel cover holds it down at 10 g and covers the contacts (EMC-3). Keep the pocket 2–3 mm deep so the latch can still be pressed.

**Why not side-wall mating.** Opta-style side ports [S31] and WAGO / Beckhoff side-wall spring contacts need tight moulding tolerances and slide-together mounting. A middle module then cannot be removed without sliding its neighbours. These systems are also rated near the PLC 1–5 g levels, not 10 g.

**DIN rail at 10 g.** The connector is not the only weak point.
- Fit an end clamp on both ends of every stack (Phoenix CLIPFIX / E/UK class or a Chinese equivalent; ≈ INR 10–60 each, ESTIMATE). Clamps stop the modules sliding and opening the jumpers.
- Give the housings interlocking ribs on the side walls so neighbours cannot rock against each other.
- The DIN latch needs enough preload; plastic latches made for 1 g may chatter at 10 g. Offer two M4 screw ears for wall or panel mounting in high-vibration sites (pumps, vehicles, gensets).
- Fix the rail every ≤ 100 mm.

**Inside each module.**
- Screw the logic PCB at ≥ 4 points.
- Use through-hole or THR parts for anything heavy: headers, inductors, bulk capacitors, the 18650 holder.
- Stake tall electrolytic capacitors and the 4G card's ≥ 1000 µF bulk with RTV or adhesive.
- Use selective gold or ENIG on the board.

**DIN-rail precedents.**

| System | Bus link | Rating found | Lesson |
|---|---|---|---|
| Phoenix ME + TBUS | 5-pole bus in the rail | 5 g, 25 cycles [S1] | Clean, but 5 g and ≈ INR 1,000 per module |
| Revolution Pi | Removable PiBridge plug on the housing face [S30] | Not checked | Individual modules removable; power last; not hot-pluggable |
| Arduino Opta | Side AUX port + plug, breakable cover [S31] | Not checked | Covers unused ports; DETECT chain |
| WAGO 750 / Beckhoff | Side-wall blade / spring contacts (R07) | Not checked | Needs custom moulded contacts |
| **UC (proposed)** | Flexible Micro-Fit jumper between headers on each module | Connector: EIA-364-28 VII-D + 50 g shock; system test at 10 g pending | Decouples module rocking; cheap; second-sourced |

## 6. Open questions

1. **Define "10 g" exactly.** Sine or random? Frequency range? Operating or transport only? The proposed C-4 is IEC 60068-2-6 Fc, 10–500 Hz, 0.75 mm / 10 g, 10 sweep cycles per axis, energised. Also confirm the reading of "flexible" (§ header).
2. **Accept +INR 58 per module** for the recommended bus, or go straight to option (a) +34 or (b) +17?
3. **Test before freezing.** Get a quote from an Indian lab (e.g. ETDC / ERTL under STQC, or a private lab) for a stack-level vibration test with event detection. Test tin Molex, Chinese headers and the pigtail in the same run.
4. **Tin or gold** — decide after the test (+INR 110 per module for gold).
5. **Jumper per module or per stack**, and its lengths (Fieldbus width 67.5 or 90 mm, IO-1).
6. **Header position** (top or front face) and the channel cover. Settle with the enclosure design, since this changes the tooling.
7. **4G modem card bus interface** is still open (D-29). The connector cost applies regardless.
8. **Battery board over budget** (≈ 226–259 vs "below 200"). Options: drop the screws and use a latched pigtail; or accept the gap.
9. **18650 holder data.** MYOUNG spring force and UL 94 rating; samples of MPD BH-18650-PC for comparison.
10. **Items not verified this session:** the EIA-364-28 VII-D level and the MIL-STD-202 figure (recalled); Amphenol Minitek Pwr 3.0 part numbers and India stock; Würth WR-MPC3 vibration data; Weidmüller CH20M vibration; JST GH / PUD product specs; Samtec TSW / SSW test report; DuraClik terminal price; Phoenix MC pair price; Mill-Max multi-pin price; Chinese TBUS clones (none found).
11. **Landed cost.** LCSC is 2.4–5.7× cheaper than Indian distributors for the same Molex part. Get a 100-unit quote from a Molex franchise in India (Arrow, Avnet, element14) before deciding the import route.

## Sources

- [S1] Phoenix Contact ME 22,5 TBUS 1,5/5-ST-3,81 KM (2713722) datasheet, mirror — https://static.chipdip.ru/lib/693/DOC040693508.pdf (saved: `docs/datasheets/connectors/Phoenix_TBUS_ME22-5_2713722_datasheet.pdf`)
- [S2] Phoenix 2200244 (YE) datasheet, RSP Supply mirror — https://rspsupply.com/images/downloads/Phoenix/2/Phoenix%202200244/Phoenix%20Data%20Sheet.pdf
- [S3] Phoenix 2707437 datasheet (2020 edition), Farnell — https://www.farnell.com/datasheets/3098443.pdf
- [S4] myMectronic price aggregator, Phoenix 2707437 (TTI, Mouser offers; 2026-11-19) — https://www.mymectronic.com/part-detail/Phoenix-Contact/2707437
- [S5] Phoenix FMC 1,5/4-STF-3,81 (1748370) and MC 1,5/5-STF-3,81 (1743171) datasheets (search snippets) — https://www.phoenixcontact.com/us/products/1748370/pdf ; https://www.phoenixcontact.com/us/products/1743171/pdf
- [S6] Weidmüller CH20M BUS 4.50/05 (search snippet; site blocks scripted access) — https://datasheet.weidmueller.com/pdf/en/1248240000/scope/1
- [S7] Molex PS-43045 Micro-Fit 3.0 product specification (2017-10-27), mirror — https://cdn.eicom.ru/media/PDF/183992.pdf (saved: `Molex_MicroFit3_PS-43045_spec.pdf`)
- [S8] LCSC C122413 Molex 430450400 — https://www.lcsc.com/product-detail/C122413.html ; C277721 430450412 — https://www.lcsc.com/product-detail/C277721.html
- [S9] LCSC C122417 Molex 430250400 — https://www.lcsc.com/product-detail/C122417.html
- [S10] LCSC C585880 Molex 430450401 — https://www.lcsc.com/product-detail/C585880.html ; Heilind description (gold) — https://heilind.com/mol43045-0401.html
- [S11] LCSC C246762 Molex 430300002 (gold) — https://www.lcsc.com/product-detail/C246762.html ; C259786 430300001 (tin) — https://lcsc.com/product-detail/Line-Pressing-Terminals_MOLEX-430300001_C259786.html
- [S12] LCSC C3294383 HCTL HC-MX3.0-2\*2AW — https://www.lcsc.com/product-detail/C3294383.html
- [S13] Lion Circuits, Molex 0430450400 (INR 143.09 at 100) — https://www.lioncircuits.com/parts/0430450400
- [S14] Lion Circuits, Würth 66200421022 WR-MPC3 (INR 60.28 at 100) — https://www.lioncircuits.com/parts/66200421022
- [S15] Mill-Max Spring Loaded Contact Mechanical and Climatic Test Report rev 2.0 — https://www.mill-max.com/sites/default/files/external/assets/2017-07/Mill-Max-Spring-Loaded-Contact-Mechanical-and-Climatic-Test-Report_ver2.0.pdf (saved)
- [S16] LCSC pogo connectors C49424460 (kinghelm KH-A25010-06P), C49451500 (CHIN-BAN PG2541-02-002P) — https://www.lcsc.com/product-detail/C49424460.html ; https://www.lcsc.com/product-detail/C49451500.html
- [S17] Hirose FX18 (R07 [S18]) and LCSC C598060 — https://www.lcsc.com/product-detail/C598060.html
- [S18] Molex DuraClik 560020 part sheet, mirror — https://static.chipdip.ru/lib/821/DOC031821715.pdf (saved) ; LV214 claim, Arrow — https://www.arrow.com/en/products/5600200222/molex ; LCSC C177237, C114106, C294024 — https://www.lcsc.com/product-detail/C177237.html ; https://www.lcsc.com/product-detail/C114106.html ; https://lcsc.com/product-detail/Housings-Wire-To-Board-Wire-To-Wire_MOLEX-5023510600_C294024.html
- [S19] Molex Micro-Lock Plus datasheet 987651-4888 (search snippet) — https://www.molex.com/content/dam/molex/molex-dot-com/en_us/pdf/datasheets/987651-4888.pdf
- [S20] JST GH and PUD catalogues — https://www.jst-mfg.com/product/pdf/eng/eGH.pdf ; https://www.jst-mfg.com/product/pdf/eng/ePUD.pdf (saved)
- [S21] Harwin M20 datasheet and catalogue (search snippets) — https://cdn.sparkfun.com/assets/3/e/a/9/b/C001XX_M20_Series_Connectors.pdf ; https://dtsheet.com/doc/1289250/harwin-connector-catalog
- [S22] LCSC 2.54 mm parts: C239344 CJT A2541HWV-2x4P, C92271 CONNFLY DS1023-2\*4SF11, C18078143 Bossie, C3333874 Samtec TSW-104-07-G-D — https://www.lcsc.com/product-detail/C239344.html ; https://www.lcsc.com/product-detail/C92271.html ; https://www.lcsc.com/product-detail/C3333874.html
- [S23] Lion Circuits, Keystone 1042 (INR 460.09 at 100) — https://www.lioncircuits.com/parts/1042
- [S24] Lion Circuits, MPD BK-18650-PC2 (INR 259.43 at 100) — https://www.lioncircuits.com/parts/BK-18650-PC2
- [S25] MPD 18650 holder product page — https://products.memoryprotectiondevices.com/?page_id=67
- [S26] LCSC MYOUNG holders C19184083, C51883817, C2988620 — https://www.lcsc.com/product-detail/C19184083.html ; https://www.lcsc.com/product-detail/C51883817.html ; https://lcsc.com/product-detail/MYOUNG-BH-18650-B1BA002_C2988620.html (drawings saved)
- [S27] Indian retail holders — https://makerbazar.in/products/18650-li-ion-battery-case-pcb-mountable-holder ; https://hubtronics.in/18650-1s-holder ; https://majestronicz.in/products/18650-1cell-holder ; https://stg.robu.in/product/18650-battery-holder-smd-smt
- [S28] Internal: `docs/research/R07_Connector_Mechanical_DFM.md`; PRD rows SYS-11, MECH-3, D-9, PWR-2, PWR-10, SAF-6, EMC-3; `docs/diagram/build_architecture.py` BOM lines (2026-11-20)
- [S29] LCSC C127367 Molex 430450600, C293525 430250600 — https://www.lcsc.com/product-detail/C127367.html ; https://www.lcsc.com/product-detail/C293525.html
- [S30] Revolution Pi PiBridge — https://revolutionpi.com/en/blog/pibridge
- [S31] Arduino Opta expansions (AUX port, breakable cover) — https://docs.arduino.cc/hardware/opta-digital-exp/
- [S32] Molex 43030-0007 part page (tooling 63819-0000) — https://www.molex.com/en-us/products/part-detail/430300007

## Appendix A — working notes (raw findings, kept for traceability)

### N1. Phoenix Contact TBUS (DIN-rail bus connector) — datasheet facts
- ME 22,5 TBUS 1,5/5-ST-3,81 (GN 2707437, KM 2713722, YE 2200244, GY 2201937): 5 positions, 3.81 mm, 8 A (parallel contacts), 125 V (III/2), full gold contacts, PA V0, −40…+105 °C.
- **Vibration: IEC 60068-2-6, 10–150–10 Hz, 0.35 mm (10–60.1 Hz), 5 g (60.1–500 Hz), 2.5 h per axis. Shock 15 g / 11 ms (IEC 60068-2-27).** So only 5 g on paper, not 10 g.
- **Insertion/withdrawal cycles: 25** (IEC 61984). Insertion ≈ 6 N, withdrawal ≈ 5 N per position. No locking (relies on the housing snapping onto the rail).
- PCB side: ME TBUS PST 1,5/5-3,81 pin strip (2279033) or THR version (2914369); note recommends hard-gold pads for bus contact.
- Sources: chipdip mirror of 2713722 datasheet (https://static.chipdip.ru/lib/693/DOC040693508.pdf), RSP Supply mirror of 2200244, Farnell 3098443 (2707437, 2020 edition without vibration data).

### N2. Molex Micro-Fit 3.0 (3.0 mm, dual row) — PS-43045 (rev. 2017-10-27, mirror cdn.eicom.ru/media/PDF/183992.pdf)
- Agency current (single circuit): 43025 receptacle / 43045 header: UL 8 A, CSA 8 A, IEC 5 A. UL 600 V, IEC 250 V. Operating −40…+105 °C.
- **Durability: 30 cycles** (tin). Vibration: **random, EIA-364-28 test condition VII letter D, 15 min per axis, discontinuity < 1 µs** (VII-D ≈ 3.1 g rms, 20–500 Hz — level recalled, verify against EIA-364-28F). **Shock 50 g, 11 ms, EIA-364-27 condition H**. Positive latch on housing.
- Note: the vibration rating is a random profile in g rms, not a 10 g sine; not directly comparable to a 10 g sine test. Must be confirmed in our own enclosure test.
- LCSC API works by C-number (wmsc.lcsc.com/ftps/wm/product/detail?productCode=Cxxxx); search API is blocked.

### N3. What "10 g" usually means in connector datasheets
- Classic Japanese / MIL-STD-202 method 201A test: 10–55 Hz, 1.52 mm total excursion (0.76 mm amplitude), 2 h per axis. Peak acceleration at 55 Hz = (2π·55)² × 0.76 mm ≈ 91 m/s² ≈ **9.3 g**. Many JST / Hirose / JAE datasheets quote this; it is the usual "10 g" claim.
- IEC 60068-2-6 (test Fc) sine sweep with 0.75 mm / 10 g crossover at ≈ 57.6 Hz is the equivalent IEC form. IEC 61131-2 (PLCs) asks only 3.5 mm 5–8.4 Hz / 1 g 8.4–150 Hz, so 10 g is ≈ 10× the PLC standard. Phoenix TBUS is rated 5 g.

### N4. LCSC prices read 2026-11-20 (API, USD at the 100-unit ladder step that applies; ×94)
- C122413 Molex 430450400 Micro-Fit 3.0 2×2 R/A header, TH, PCB snap lock: USD 0.269 (60+) ≈ INR 25.3; stock 48,774.
- C277721 Molex 430450412 (4-pos, TH): USD 0.2611 (30+) ≈ INR 24.5; stock 48,346.
- C585880 Molex 430450401 R/A header: USD 0.7162 ≈ INR 67; stock 1,594 (variant, not needed).
- C122417 Molex 430250400 Micro-Fit receptacle housing 4-pos: USD 0.0785 (50+) ≈ INR 7.4; stock 47,635.
- C587702 Molex 443000400 (Micro-Fit 4-pos housing variant; type not confirmed): USD 0.3186 ≈ INR 30; stock 995.
- C3294383 HCTL HC-MX3.0-2*2AW (Chinese Micro-Fit-compatible 2×2 R/A header): USD 0.1456 (50+) ≈ INR 13.7; stock 44,240.
- India: Lion Circuits lists Würth WR-MPC3 66200421022 (2×2 R/A, Micro-Fit compatible) at INR 65.88 (qty not stated) — https://www.lioncircuits.com/parts/66200421022.

### N5. Phoenix pluggable COMBICON (MC 1,5 / FMC 1,5, 3.81 mm, screw flange)
- FMC 1,5/4-STF-3,81 (1748370) and MC 1,5/5-STF-3,81 (1743171) datasheets: vibration IEC 60068-2-6, 10–150 Hz, 0.35 mm / **5 g**, 2.5 h per axis. Insertion ≈ 6 N, withdrawal ≈ 4 N per position. Same 5 g ceiling as TBUS. (Search snippets of phoenixcontact.com/us/products/1748370/pdf and /1743171/pdf; site blocks scripted download.)

### N6. Mill-Max spring-loaded (pogo) contacts — test report rev 2.0 (saved)
- Brass plunger/sleeve 20 µ" gold over 100 µ" Ni; BeCu spring gold. Force ≈ 25 g / 60 g / 95 g at min / mid / max stroke.
- **2 A continuous, 3 A peak per contact**; 100 V rms; 20 mΩ; −55…+125 °C; **1,000,000 cycles**.
- **T5 sine vibration: IEC 60512-6-4 / IEC 60068-2-6 Fc, 0–200 Hz, 10 g peak; T6 random IEC 60068-2-34, 10 g peak; T7 shock (50 g per product pages). Pass: no spike > 1 µs and > 1.15 V at 0.5 A.** Tested against gold pads. This is the only bus-type contact found with a published 10 g sine result.
- Weidmüller CH20M BUS 4.50/05 (rail bus, 5-pole): 5 A per path, 63 V AC (DIN EN 60664); vibration data not found (datasheet.weidmueller.com blocks scripted access).

### N7. Battery-board connector candidates (first pass)
- Harwin M20 2.54 mm (catalogue): 3 A per contact, 300 cycles gold / 50 tin; vibration 50–2000 Hz 3.13 g, shock 30 g (catalogue level, not part level). No lock — needs screws/standoffs.
- Molex Micro-Lock Plus 2.0 mm: 4.7 A (AWG 22) single row, −40…+105 °C, positive latch; no published vibration standard found.
- **Molex DuraClik 2.0 mm (560020 headers; housings 502351 / 560123 / 505151):** 3.0 A per contact, −40…+105/125 °C, 30 cycles, positive lock (inner/outer), TPA option; marketed for "high vibration"; Arrow says it meets **LV214** (German OEM connector standard). LCSC C177237 Molex 5600200620 (6-pos SMD vertical header): USD 0.3646 at 100 ≈ **INR 34.3**, stock 4,504.
- JST PUD 2.0 mm dual row: 3 A (AWG 22), "strong lock against vibration and prying", but only −25…+85 °C (catalogue).
- JST GH 1.25 mm: 1 A per contact (AWG 26), −40…+105 °C, secure lock; would need 2 pins per 2 A rail.

### N8. 18650 holder prices (100 units)
- Keystone 1042 (SMT, gold contacts): Lion Circuits **INR 460.09 at 100** (https://www.lioncircuits.com/parts/1042). Keystone 1043 (THT) is the PC-pin twin.
- MPD BK-18650-PC2 (PP body, Ni-plated steel contacts, PC pins, 21.4 mm high): Lion Circuits **INR 259.43 at 100** (https://www.lioncircuits.com/parts/BK-18650-PC2). MPD BH-18650-PC: PBT, dual pressure contacts, 302 stainless spring temper Ni-plated, −40…+180 °C, UL94 V-0 (MPD product page).
- LCSC MYOUNG BH-18650-A5BJ001-2D (DIP, Ni contacts): USD 0.4787 at 90+ ≈ **INR 45**, stock 513 (C19184083). MYOUNG BH-18650-B1BA002 (SMT, gold): USD 1.0224 ≈ **INR 96**, stock 1,717 (C2988620). MYOUNG BH-18650-A6AJ022 (PA46, double negative spring): USD 0.77 ≈ INR 73, stock 14 (C51883817).
- None of these holders publishes a vibration rating. Keystone C5249310 (LCSC listing for 1042) returned no data.

### N9. More LCSC prices (2026-11-20)
- C585880 Molex **430450401** = Micro-Fit 3.0 2×2 R/A header, snap-in PCB lock, **gold**, glow-wire (Heilind description): USD 0.7162 (30+) ≈ INR 67.3; stock 1,594.
- C246762 Molex **430300002** Micro-Fit female crimp terminal, 20–24 AWG, **select gold**, 7 A max: USD 0.0499 (100+) ≈ INR 4.7; stock 187,800.
- C259786 Molex **430300001** same, **tin** (reel version of 43030-0007): USD 0.0152 (100+) ≈ INR 1.4; stock 2.1 M. 43030-0007 (tin, bag): 30 cycles, 7 A max per contact (Molex/Arrow).
- Per-module stack-bus cost drafts (two headers + one jumper share; jumper = 2 housings + 8 terminals + 4 × 70 mm 20 AWG + 8 crimps ≈ INR 6 labour, ESTIMATE): Molex gold ≈ INR 195; Molex tin ≈ INR 85; Chinese header + Molex tin jumper ≈ INR 61. Implied current budget for connectors + bridge share ≈ INR 27 (BOM line 58–59 minus RS-485 transceiver ≈ 26 and ESD ≈ 6; ESTIMATE).

### N10. Indian retail 18650 holders (search snapshots, single units, incl./excl. GST as stated)
- Makerbazar PCB-mount spring holder INR 22 incl. GST (18.64 + GST); Hubtronics 1S PCB holder INR 22 + GST; Majestronicz INR 16; Robu SMD single holder INR 33–49 incl. GST; Electronicspices sells THT holders in packs of 100. Unbranded: no material (UL94) or contact data.

### N11. Phoenix TBUS price (aggregator myMectronic, 2026-11-19 snapshot, not DigiKey)
- 2707437: TTI USD 10.12 (stock 0), Mouser USD 13.49 (stock 5), single-unit prices; no 100-unit break shown → **≈ INR 950–1,270 per TBUS segment (UNVERIFIED at 100)**, plus the PCB-side pin strip (ME TBUS PST, not priced). One segment per module → about 15–40× the current connector budget. No LCSC listing found; no Chinese TBUS-compatible clone found in this session (UNVERIFIED that one exists at a stated rating).

### N12. Battery-board connector prices (LCSC API, 2026-11-20)
- C3333874 Samtec TSW-104-07-G-D (2×4 2.54 mm header, gold): USD 0.7257 at 100 ≈ INR 68.2; stock 285. Samtec SSW-104-01-G-D socket not priced (ESTIMATE ≈ INR 80).
- C92271 CONNFLY DS1023-2*4SF11 (2×4 2.54 mm socket, TH): USD 0.09 (50+) ≈ INR 8.5; stock 37,110. C239344 CJT A2541HWV-2x4P (2×4 socket, gold, brass): USD 0.1371 ≈ INR 12.9; stock 10,295. C18078143 Bossie BX-PM2.54-2-4PY socket: ≈ INR 11.2.
- C294024 Molex 5023510600 DuraClik 6-pos housing: USD 0.0793 ≈ INR 7.5. C114106 Molex 5023520600 DuraClik 6-pos R/A SMD header: USD 0.3183 ≈ INR 29.9. C177237 5600200620 vertical SMD header ≈ INR 34.3. DuraClik crimp terminal not priced (ESTIMATE ≈ INR 2–3).
- Harwin M20 (2.54 mm): 3 A per contact, 300 cycles gold.

### N13. India distributor prices (Lion Circuits, Bengaluru; 2026-11-20)
- Molex 0430450400 (Micro-Fit 2×2 R/A, tin): **INR 143.09 at 100**, in stock, ships 7–10 days (https://www.lioncircuits.com/parts/0430450400). LCSC is ≈ INR 25 before duty and freight.
- Würth WR-MPC3 66200421022 (2×2 R/A, 5 A, snap-in pegs, Micro-Fit compatible): **INR 60.28 at 100**, in stock, 7–10 days (https://www.lioncircuits.com/parts/66200421022).
- Chinese pogo connectors on LCSC (no ratings published): kinghelm KH-A25010-06P 6-pos ≈ INR 18.8 (stock 15); CHIN-BAN PG2541-02-002P 2-pos ≈ INR 26.

### N14. Micro-Fit 6-pos and holder datasheet data
- C127367 Molex 430450600 (Micro-Fit 2×3 R/A header, TH): USD 0.4028 (30+) ≈ INR 37.9; stock 37,855. C293525 Molex 430250600 (2×3 housing): USD 0.0942 ≈ INR 8.9; stock 54,875.
- MYOUNG BH-18650-B1BA002 drawing: body material options PBT / PA66 / PPA / PA9T; gold-plated phosphor bronze, −25…+85 °C. BH-18650-A5BJ001-2D: Ni-plated, −10…+100 °C (LCSC parameters) — the −10 °C lower limit is below what an outdoor node needs.
