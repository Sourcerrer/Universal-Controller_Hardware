# R07 — 40-pin Bus Connector, Stackable DIN-Rail Mechanics, Enclosures and DFM/DFT

Status: v1 2026-11-14. Complete in structure. Items marked UNVERIFIED could not be confirmed: the session's web-search budget ran out, and Mouser/DigiKey/element14/RS/Hirose/Würth blocked automated access. See §10 item 8.

Scope (per brief + 2026-11-13 update): stackable PLC-style system of individually enclosed DIN-rail modules joined by a 40-pin pass-through bus connector (Hirose / Würth preferred); enclosure survey; DFM/DFT rules; assembly-cost model; field connectors.

## 1. Executive summary and recommendation

1. **Fine-pitch mezzanines are the wrong tool for enclosure-to-enclosure mating.** Hirose DF40 (0.4 mm: 30 cycles, 30 V), DF12N (0.5 mm: 50 cycles), DF17 (0.5 mm) and Würth WR-BTB 0.8 mm (30 cycles, 50 V) have almost no lead-in. They are fine only inside one enclosure [S16][S17][S21][S22].
2. **Primary recommendation: Hirose FX18 40-pin (0.8 mm) in a bridge topology.** Each module has two right-angle receptacles **FX18-40S-0.8SH** (BUS-IN/BUS-OUT) on its top edge. A small bridge PCB with two **FX18-40P-0.8SV** headers joins neighbours, like the RevPi PiBridge or Arduino Opta AUX plug.
3. FX18 ratings: 0.5 A per signal contact; 3 A multi-function guide-post contacts for power/GND, which make first; 100 V AC; 500 cycles; ±1 mm lead-in; guides prevent reverse mating; −55…+85 °C; marketed for 10 Gbps [S18][S19].
4. **Alternate:** a 2.54 mm 2×20 shrouded box header (Würth WR-BHD or generic) with a rigid bridge or short IDC jumper. Cheapest and multi-sourced, but bulky and weak for USB-HS. Part numbers and prices are UNVERIFIED. A direct side-wall FX18 parallel stack (SV10 + SV10 = 20 mm, about 21.6–22.4 mm module pitch) is possible but needs modules slid together; not recommended for v1.
5. **Price:** FX18-40P-0.8SH is USD 2.05 at ≥980 pcs on LCSC (≈ INR 193 at INR 94/USD), stock 0 on 2026-11-14 [S20]. The full pair is estimated at INR 350–450 (UNVERIFIED). This is the single biggest threat to the INR 430 Wi-Fi BOM.
6. **Power:** a pass-through bus accumulates current. Cap the total at 2–3 A at 24 V, fed by a baseboard eFuse, with a per-module load switch driven by a per-slot PWR_EN line so the brain can power-cycle a hung module. Use pin rotation so identical modules get per-slot CS/PWR_EN lines.
7. **Signals:** USB 2.0 HS point-to-point to slot 1 only, so the 4G + Ethernet + Wi-Fi module sits next to the baseboard. SPI ≤ 20 MHz multi-drop. No RMII on the bus. DETECT chain for enumeration; SWD on the bus for a universal test jig.
8. **Safety/ESD:** use polarised guides and an asymmetric bridge, and put protection (TVS + reverse/over-voltage) at each bus input. Cap exposed end-of-chain receptacles. The bus is not hot-pluggable.
9. **Mechanics:** 22.5 mm modules (Wi-Fi, LoRa, fieldbus), a 45 mm combined cellular module and a 45–67.5 mm baseboard. Phoenix ME 22.5 + TBUS (5-pole, 8 A) is the verified off-the-shelf precedent [S10][S11]. Other enclosure families and prices are UNVERIFIED.
10. **DFM:** 4-layer for radio/USB modules, 0402 minimum, single-sided top SMT with the bus connector on top, ENIG, AOI, Data Matrix serials, IPC-A-610 Class 2.
11. **Cost check:** the illustrative model gives conversion cost of about INR 208 at 1k and INR 154 at 10k for the Wi-Fi module. Against 40 % × 430 = INR 172, the target is tight at 1k and fine at 10k; it is comfortable for the INR 714-BOM modules. All rates are UNVERIFIED assumptions.

## 2. How stackable PLC-style systems pass a bus from module to module

Exchange rate used throughout: **USD 1 = INR 94.0** (mid-market 93.93 on 2026-11-08 per CurrencyBeacon [S1]; ~94–95 range early Nov 2026 per PTI/HDFC Sky [S2]). Rounded to 94.0.

| System | How the bus crosses between modules | Contacts / ratings | Module pitch | Lesson for UC |
|---|---|---|---|---|
| WAGO 750/753 | Blade (knife) contacts on the left side wall, spring contacts on the right; power jumper contacts make automatically when modules are snapped together on the rail. WAGO warns the blade contacts are sharp-edged. [S3][S4] | Power jumper contacts max 10 A [S4] | 12 mm (e.g. 750-622 datasheet) [S5] | Contacts integrated into the housing side walls, slide-in mating along the rail — needs custom moulded contacts; not an off-the-shelf PCB connector. |
| Beckhoff EtherCAT / Bus Terminals | "The E-bus is led through from the Bus Coupler through all the terminals via six contacts on the terminals' side walls"; separate power contacts are interrupted by power-feed terminals. [S6][S7] | 6 E-bus spring contacts (data + electronics supply) [S6] | 12 mm / 24 mm [S6] | Very few contacts (6) — only possible because the bus is a serial differential link (EtherCAT LVDS). A 40-pin parallel bus is the opposite design choice. |
| Siemens ET 200SP | I/O modules plug into BaseUnits; BaseUnits carry a backplane bus and **self-assembling voltage buses** (P1, P2, AUX). Light BUs open a new potential group; dark BUs forward it. [S8][S9] | ≤10 A per potential group [S9] | 15 mm BaseUnit (BU15 …, 15 × 141 mm) [S8] | Separating "bus/base" from "electronics module" lets the electronics be replaced without breaking the bus. |
| Phoenix Contact ME / ICS / ME-IO with TBUS | Bus connector **snaps into the DIN rail** (ME 22,5 TBUS 1,5/ 5-ST-3,81 GN, order no. 2707437); each enclosure's PCB has a mating header that plugs down into it, so modules are connected through the rail, not through the side walls. [S10][S11] | 5 positions, 3.81 mm pitch, 8 A, 150 V, UL recognised [S10][S11] | 22.5 mm | Best off-the-shelf precedent for "own enclosure + bus". Only 5 poles though — a 40-pin rail bus would need a custom rail-insert PCB. |
| Revolution Pi (KUNBUS) | Separate **PiBridge plug** (black jumper plug) pushed into sockets on the **top** of adjacent housings after both are on the rail; base ↔ I/O modules over a 20-pin system connector carrying RS-485 + 2 Ethernet channels; I/O modules forward the RS-485 channel; gateways (terminating) must be on the outermost slot. Separate grey "ConBridge" for Con modules — mixing them can damage devices. Power is to be connected last. [S12][S13] | 20 pins [S12] | ~22.5 mm | A **removable bridge** between two identical sockets is the most robust way to join enclosed modules: no blind mating through side walls, generous tolerance, each module can be removed without sliding neighbours. Lesson: give different bus generations visibly different bridges. |
| Arduino Opta + expansions | AUX port on left and right side of each module; port is freed by **breaking off a plastic cover**, then a **connection plug** is added between each device; max 5 expansions; bus = shared I2C + UART-like line (base Tx to all expansion Rx) + DETECT IN / DETECT OUT chain for enumeration. [S14][S15] | n/a (not published in sources read) | 1 DIN unit per expansion | Same bridge-plug idea at side wall; breakable cover protects unused port; DETECT daisy-chain = geographic addressing, which UC should copy for module-position ID. |

Conclusion for UC: the two practical off-the-shelf patterns are (a) a **bridge/jumper plug** between two identical sockets (RevPi top-side, Opta side-wall), and (b) a **DIN-rail-embedded bus connector** (Phoenix TBUS, Camdenboss/Italtronic rail-bus variants — see §6). Direct enclosure-wall-to-enclosure-wall blind mating of a plug and receptacle (WAGO/Beckhoff style) needs moulded spring/blade contacts and tight enclosure tolerances; it is not realistic with a fine-pitch SMT mezzanine connector.

## 3. 40-pin connector evaluation (Hirose / Würth first)

### 3.1 Hirose DF40 (0.4 mm) — reference point (datasheet downloaded)
From the Hirose DF40 catalogue PDF in `datasheets/connectors/Hirose_DF40_datasheet.pdf` (note: the copy on file is the 03/2012 edition) [S16]:
- 40-pin parts: receptacle DF40C-40DS-0.4V(51) (1.5 mm stack), DF40C(2.0)-40DS-0.4V(51) (2.0 mm), DF40HC(2.5)-40DS-0.4V(51), DF40HC(3.0)…, DF40HC(4.0)-40DS-0.4V(51) (listed "reserved for product expansion" in that edition); header DF40C-40DP-0.4V(51). Stacking heights 1.5–4.0 mm.
- Current 0.3 A per contact; voltage 30 V AC/DC; contact resistance 90 mΩ max; durability **30 insertion/withdrawal cycles**; operating temperature −35 … +85 °C (includes self-heating); withstanding voltage 100 V AC / 1 min.
- Corner contacts are solder brackets only and must not carry current.
- Assessment: excellent for a permanent mezzanine inside one enclosure (CM4/Portenta style), **unsuitable** for enclosure-to-enclosure mating: 0.4 mm pitch, ~1.5–4 mm stack height means zero tolerance for two separately moulded housings; only 30 cycles; 30 V rating leaves no margin over a 24 V bus with surge/transients.

### 3.2 Hirose DF12N (0.5 mm)
From Hirose DF12N catalogue (09/2020 edition, mirror) [S17]:
- 40-pin parts (3.0 mm stack): receptacle **DF12NC(3.0)-40DS-0.5V(51)** + header **DF12NC(3.0)-40DP-0.5V(51)**; headers also at 3.5 / 4.0 / 5.0 mm (DF12NC(3.5/4.0/5.0)-40DP-0.5V(51)); DF12NB variants have bosses.
- Current 0.3 A/contact; voltage 50 V AC; contact resistance 50 mΩ max; durability **50 mating cycles**; operating −55 … +125 °C.
- Assessment: internal mezzanine only. Same objections as DF40 for enclosure-to-enclosure mating (tiny lead-in, 50 cycles, 3–5 mm stack).

### 3.3 Hirose FX18 (0.8 mm, "FunctionMAX") — best Hirose fit for a module-to-module bus
From Hirose FX18 catalogue (1/2014 edition, mirror) [S18]:
- 40, 60, 80, 100, 120, 140 positions; connection types **coplanar, right-angle and parallel (10–45 mm)**.
- 40-pin parts: right-angle receptacle **FX18-40S-0.8SH** (CL579-0009-4), right-angle header **FX18-40P-0.8SH** (CL579-0002-5), straight header **FX18-40P-0.8SV** (CL579-0016-0) and **FX18-40P-0.8SV10** (CL579-0022-2), straight receptacles **FX18-40S-0.8SV10 / -SV15 (CL579-0026-3) / -SV20 (CL579-0030-0)**, interposer FX18-40PS-0.8H15.
- Mating combinations: coplanar = SH receptacle + SH header; right-angle (perpendicular boards) = SH receptacle + SV header; parallel 2-piece stack heights 10 / 15 / 20 mm (SV header) or 20 / 25 / 30 mm (SV10 header) with SV10/15/20 receptacles; 3-piece with interposer 25–45 mm.
- Ratings: 0.5 A per signal contact; **3.0 A per MF (multi-functional guide-post) contact** usable as power/ground; AC 100 V; withstanding AC 300 V/1 min; contact resistance 90 mΩ max (100 mΩ after tests); **500 mating cycles**; operating −55 … +85 °C (incl. self-heating); vibration 10–55 Hz, 0.75 mm half-amplitude; shock 490 m/s².
- Mechanical: guide posts on both sides; **lead-in ±1 mm**; guides **prevent inverse mating**; 2.0 mm effective signal wipe; MF contacts are sequenced (MF A 2.5 mm, MF B 1.5 mm) — i.e. ground/power make first.
- Marketed for up to 10 Gbps [S19].
- LCSC lists FX18-40P-0.8SH as C598060 (0.5 A, 100 V, −55…+85 °C) [S20]; price/stock: see §3.x table.
- Assessment: **the only Hirose family surveyed with both the lead-in (±1 mm), polarisation, 500 cycles, 100 V rating and a high-current power contact needed for enclosure-to-enclosure or bridge mating.** Caveat: the catalogue on file is dated 2014; lifecycle must be confirmed at a distributor (see table).

### 3.4 Hirose DF17 (0.5 mm)
- 40-pin pair (per distributor listings): header **DF17(2.0)-40DP-0.5V(57)** + receptacle **DF17(4.0)-40DS-0.5V(57)** [S22]. 0.3 A / contact, 50 V AC, operating −35 … +85 °C [S22]. Mating-cycle rating: **UNVERIFIED** (not found in the sources read). Mated-height code meaning: UNVERIFIED (listings disagree).
- Assessment: internal mezzanine only; same verdict as DF40/DF12N.

### 3.5 Hirose FX8 / FX8C (0.6 mm)
- **Not researched — UNVERIFIED.** The web-search budget for this session ran out before FX8/FX8C could be checked (including whether a 40-position version exists at all). As a 0.6 mm fine-pitch mezzanine it would fall under the same "internal mezzanine only" verdict; it adds nothing FX18 does not already offer for this use.

### 3.6 Würth WR-BTB 0.8 mm
- 40-pin parts found: female shrouded vertical receptacle **658807713040** (7.75 mm height; 30 mating cycles; 500 V AC withstanding; 50 mΩ) [S21]; receptacle **658801103040** [S21]; male header **658855603040** (0.5 A, 50 V) [S21]. Family: 40/64/80/100 positions, 0.8 mm and 1.0 mm pitch, 0.5 A rating [S21].
- Assessment: **only 30 mating cycles and 50 V** — not suitable for a user-separable bus between enclosures. It works as an internal mezzanine. The Würth series datasheet (we-online.com) returned "Access Denied" to scripted download, so it was **not downloaded**.

### 3.7 Würth WR-PHD / WR-BHD / WR-MM and generic 2.54 mm 2×20
- **Not verified in this session (search budget exhausted): part numbers, ratings and prices are UNVERIFIED.** Würth sells 2.54 / 2.0 / 1.27 mm pin and socket headers (WR-PHD) and shrouded box headers (WR-BHD) in 2×20 sizes, and Micro-MaTch-style WR-MM. A shrouded 2×20 box header is keyed and the most robust, cheapest bus option if pin pitch and size do not matter. Confirm exact Würth order codes, current ratings (2.54 mm headers are typically quoted at about 3 A per pin) and mating cycles before using these figures.

### 3.8 Comparison summary (40 positions)

| Family | Pitch | 40-pin pair | I / contact | V | Cycles | Lead-in / polarity | Temp | Enclosure-to-enclosure suitability |
|---|---|---|---|---|---|---|---|---|
| Hirose DF40 | 0.4 | DF40C-40DP-0.4V(51) / DF40C-40DS-0.4V(51) (1.5 mm), up to DF40HC(4.0) | 0.3 A | 30 V | 30 | minimal | −35…+85 | **No** [S16] |
| Hirose DF12N | 0.5 | DF12NC(3.0)-40DP-0.5V(51) / DF12NC(3.0)-40DS-0.5V(51) | 0.3 A | 50 V AC | 50 | minimal | −55…+125 | **No** [S17] |
| Hirose DF17 | 0.5 | DF17(2.0)-40DP-0.5V(57) / DF17(4.0)-40DS-0.5V(57) | 0.3 A | 50 V | UNVERIFIED | minimal | −35…+85 | **No** [S22] |
| Hirose FX8/FX8C | 0.6 | UNVERIFIED | — | — | — | — | — | not researched |
| **Hirose FX18** | 0.8 | FX18-40S-0.8SH + FX18-40P-0.8SV (right-angle) or SV10/SV20 parallel or SH/SH coplanar | 0.5 A signal, **3 A MF** | **100 V AC** | **500** | **±1 mm lead-in, guides stop reverse mating** | −55…+85 | **Yes (bridge or slide-mate)** [S18] |
| Würth WR-BTB 0.8 | 0.8 | 658855603040 / 658807713040 | 0.5 A | 50 V | 30 | shrouded/chamfered | UNVERIFIED | No (cycles) [S21] |
| 2.54 mm 2×20 box header + IDC/bridge (Würth WR-BHD or generic) | 2.54 | UNVERIFIED | ~3 A typical (UNVERIFIED) | UNVERIFIED | UNVERIFIED | shroud key | UNVERIFIED | Yes (low cost, large, low SI) |

**Prices.** Only one price could be confirmed. LCSC **FX18-40P-0.8SH (C598060): USD 2.0502 at ≥980 pcs (≈ INR 193)**, stock **0**, read from the LCSC product page on 2026-11-14 [S20]. Mouser, DigiKey, element14 India, RS and Future Electronics either blocked automated access or timed out. All other prices, and stock at Mouser/DigiKey/element14 India, are **UNVERIFIED**. Working estimate for an FX18 40-pin mated pair is about INR 350–450 at 1k (**UNVERIFIED**, extrapolated from the single LCSC header price). This is significant against a INR 430 BOM for the Wi-Fi module. Get distributor quotes before freezing the design.

**Lifecycle.** The FX18 catalogue on file is dated 1/2014. LCSC and JLCPCB still list the part (JLCPCB as an "Extended" library part) [S20][S23], but Hirose's lifecycle status was **not verified** (hirose.com returned 403).

**Second sources.** No pin-compatible second source for FX18 was verified (**UNVERIFIED**). For 2.54 mm box headers, many makers are footprint-compatible (generic), which is a real cost and availability advantage.

### 3.9 Recommendation (connector)
Fine-pitch mezzanine connectors (0.4–0.5 mm: DF40, DF12N, DF17, WR-BTB) are **unsuitable** for mating between two separately moulded enclosures. Their lead-in is a few tenths of a mm, they are rated for only 30–50 cycles, and they are rated 30–50 V. The housing-to-housing tolerance stack (rail position, snap fit, moulding) is easily ±0.5 mm or more.

- **Primary: Hirose FX18, 40-pin, in a "bridge" topology (RevPi/Opta style).**
  - Each module PCB carries **two FX18-40S-0.8SH right-angle receptacles**, BUS-IN and BUS-OUT, on the top or rear edge, reachable through slots in the housing.
  - A small rigid **bridge PCB** carries **two FX18-40P-0.8SV straight headers** (Hirose "right-angle connection type") and joins module *n* OUT to module *n+1* IN.
  - Modules snap onto the rail individually, and any module can be removed without sliding its neighbours.
  - The ±1 mm lead-in and guide posts absorb housing tolerance and prevent reversed insertion. The MF contacts carry power and ground and make first.
  - Rated 500 cycles and 100 V.
- **Alternate A (lower cost, larger): 2.54 mm 2×20 shrouded box headers in the same bridge topology**, with a rigid bridge or a 25 mm IDC ribbon jumper. This is the cheapest, keyed, multi-sourced option, but bulky, and USB-HS signal integrity is poorer. Part numbers and price: **UNVERIFIED**.
- **Alternate B (no bridge part): direct side-wall mating with FX18 parallel stack**, using FX18-40P-0.8SV10 + FX18-40S-0.8SV10 for a 20 mm stack. Module pitch is then 20 mm + PCB thickness: 21.6 mm with a 1.6 mm board, or 22.4 mm with a 2.4 mm board, which is close to a 22.5 mm housing.
  - Modules must be slid together along the rail.
  - A middle module cannot be removed without sliding its neighbours apart.
  - The receptacle is exposed on the end module.
  - Possible, but it needs tighter housing tolerances. It is not recommended for v1.

## 4. Pin allocation, power derating and signal-integrity guidance

**Power accumulates along a pass-through bus.** Five modules at about 1 A each means up to **5 A through the first bridge**.
- FX18 signal contacts are rated 0.5 A. Derate to about 0.3 A each at +70/85 °C; that derating is an engineering rule of thumb, UNVERIFIED as a Hirose figure.
- FX18 MF contacts are rated 3 A each [S18]. The number of MF contacts per connector must be confirmed from the drawing.
- Recommendations:
  - Distribute power at 24 V and keep the **total bus current ≤ 2–3 A**: 24 V × 2 A = 48 W, ample for five radio modules.
  - Put the 24 V and GND returns on MF contacts plus ≥ 4 signal pins each.
  - Give the baseboard an **eFuse per bus output**, so it can also power-cycle the chain.
  - Give each module its own **load switch on its bus input**, controlled by a per-slot PWR_EN line. This meets the update's requirement that the brain can power-cycle a hung module.
- 24 V nets need a surge/TVS design: up to 33–40 V clamp. FX18 (100 V) has margin. DF40 (30 V) would not.

**Per-slot lines with identical modules: use pin rotation ("pin shifting").** Each module consumes slot line S1 at its BUS-IN and routes IN-S2…S5 to OUT-S1…S4. Identical modules then each receive their own CS, PWR_EN and IRQ lines, with no DIP switches. This only works with a daisy-chain (IN/OUT) topology, which is the bridge approach.

Indicative 40-pin map (**proposal, not a standard**):

| Group | Pins | Notes |
|---|---|---|
| 24 V_BUS | 4 (+ MF A) | paralleled |
| GND | 10 (+ MF B) | interleaved between signal groups and around the USB pair |
| USB D+/D− | 2 | point-to-point to **slot 1 only** |
| SPI SCK/MOSI/MISO | 3 | shared |
| SPI_CS_S1…S5 | 5 | rotated per slot |
| PWR_EN_S1…S5 | 5 | rotated per slot |
| I2C SDA/SCL | 2 | management/ID EEPROM |
| UART TX/RX | 2 | shared, or point-to-point to slot 1 |
| IRQ (open-drain, shared) | 1 | |
| DETECT_IN/OUT chain | 1 | Opta-style enumeration [S15] |
| RESET_N (shared) | 1 | |
| SWDIO/SWCLK (test/programming) | 2 | universal test jig |
| Spare | 2 | |

Signal integrity:
- **USB 2.0 HS (480 Mb/s)** must be point-to-point. Multi-drop or stubbed USB across five modules will not work. Each hop adds two connectors and two board traversals. FX18 is marketed for 10 Gbps [S19], so the connector itself is fine, but run USB-HS only to the slot next to the baseboard. Place the combined 4G + Ethernet + Wi-Fi module there, or use a hub per slot (not recommended on cost).
- **SPI at 20–40 MHz** multi-drop over up to 10 connectors and about 20–30 cm of total trace is marginal at 40 MHz. Plan on **≤ 20 MHz**, with series termination at the source, ground pins next to SCK, and clock-out/clock-back if 40 MHz is needed.
- **RMII (50 MHz REF_CLK)** should **not** cross the bus. The update puts Ethernet on the combined cellular module, so this is now moot.
- The 2.54 mm IDC alternate is acceptable for SPI ≤ 10–20 MHz, UART, I2C and USB FS. USB-HS over ribbon is not recommended (engineering judgement, UNVERIFIED by test).

## 5. Lessons from existing modular systems

- **Fine-pitch mezzanines (Portenta/Nicla, CM4/CM5 with Hirose DF40)** are assembled once inside a product and retained by screws/standoffs. DF40 is rated only 30 cycles [S16]. The specific Portenta/CM4 pin counts in the brief were not re-verified this session (UNVERIFIED).
- **M.2-edge systems (SparkFun MicroMod, Particle M.2)** and **mikroBUS/Feather headers** are not researched here (UNVERIFIED). Edge connectors need a screw retention point. 2.54 mm headers tolerate misalignment but have no keying unless shrouded.
- **PLC practice** (section 2):
  - Bus contacts sit in the side walls (WAGO, Beckhoff) or in the rail (Phoenix TBUS), or a removable bridge is used (RevPi, Opta).
  - Opta closes unused ports with **break-off covers** and enumerates modules with a DETECT chain [S14][S15].
  - RevPi warns that mixing bridge types damages devices and that **power must be connected last** [S13]. The UC bus is therefore specified as **not hot-pluggable**.
- **Keying and polarity (safety).** FX18 guide posts prevent inverse mating [S18]. Additionally:
  - Make the bridge mechanically asymmetric so it cannot be rotated 180°.
  - Put 24 V on pins whose reversed or offset partner is GND or another 24 V pin, never a logic pin.
  - Add reverse/over-voltage protection (ideal diode + TVS) at each module's bus input, so a one-pin offset cannot put 24 V onto 3.3 V logic.
- **ESD on exposed connectors.**
  - Unplugged modules and the last module in a chain expose a receptacle. Fit a snap-in **blanking cap**, Opta-style.
  - Fit low-capacitance ESD arrays (TVS) on every bus signal at the connector, on both IN and OUT.
  - Route a chassis/GND ring around the connector.
  - IEC 61000-4-2 contact discharge applies to accessible parts (standards: see R01).

## 6. Module outline options and enclosure survey

Proposed outlines (**design proposals**; housing dimensions to be fixed once an enclosure family is chosen):

| Option | Width (rail pitch) | Use | Field-connector zone (front face) | Bus |
|---|---|---|---|---|
| A — 22.5 mm | 22.5 mm (Phoenix ME 22.5 class [S10]) | Wi-Fi/BLE, LoRa, fieldbus card | 1 × 3.5/3.81 mm pluggable terminal block (power + RS-485/CAN), 1 SMA, status LEDs | FX18 bridge on top edge |
| B — 45 mm (2 × 22.5) | 45 mm | combined 4G + Ethernet + Wi-Fi | RJ45, nano-SIM (behind door), 2–3 SMA, power terminal | FX18 bridge |
| C — 45–67.5 mm | 45–67.5 mm | baseboard / brain: MCU + secure element + IO/ADC terminals | 2–3 pluggable terminal rows | BUS-OUT only on the right; left side blanked |

- Keep the PCB vertical, parallel to the side walls. Board size is about the housing depth × height minus terminals (on the order of 90 × 100 mm for ME-class housings, UNVERIFIED).
- Keep the zone 1–2 mm around the bridge slot free of components taller than the bridge headers.

Enclosures:
- **Phoenix Contact ME 22.5 with TBUS (2707437)** is the verified precedent [S10][S11]. Its TBUS is only 5 poles (3.81 mm, 8 A, 150 V). It could carry 24 V/GND plus RS-485 as a parallel, rail-based power path, while the 40-pin FX18 bridge carries the signals.
- **Camdenboss CNMB, Italtronic Modulbox, Hammond 1597DIN, Indian makers, and their prices / UL 94 V-0 / IP20 data were not researched; the session's search budget ran out (UNVERIFIED).** Next step: request quotes for 1k housings with a top-face slot for the bridge.
- **Outdoor standalone nodes:** an IP65/IP67 polycarbonate box with SMA bulkhead, cable glands and a pressure-equalisation vent membrane. In a sealed box, budget for the 4G modem's dissipation and solar gain. Not researched in detail (UNVERIFIED).
- **Custom injection-mould tooling in India:** **UNVERIFIED** order of magnitude, INR 3–10 lakh for a simple two-part ABS/PC housing tool. Get quotes.

## 7. DFM / DFT guidelines

These are standard industry practice and engineering judgement; values not tied to a source are marked UNVERIFIED.

1. **Stack-up.** Use **4-layer** for every module with USB-HS, a 4G modem or Wi-Fi: solid ground plane for EMC and 90 Ω USB impedance. A 2-layer board is acceptable only for a simple fieldbus card.
2. **Design rules.** Stay inside JLCPCB/PCBWay "standard price" capability, e.g. ≥ 0.127 mm (5 mil) track/space, ≥ 0.3 mm drill, 1.6 mm FR-4, HASL-LF or ENIG. Use ENIG when fine-pitch or FX18 coplanarity matters. These are typical values: **UNVERIFIED**, check the fab's current capability page.
3. **Component size.** 0402 minimum. Do not use 0201 or BGA < 0.5 mm pitch except inside certified radio modules.
4. **Assembly sides.**
   - Single-sided SMT, top only, including the FX18 right-angle receptacles at the board edge.
   - THT parts (terminal blocks, RJ45) by selective/wave or hand soldering, or choose SMT/THR versions so that a single reflow pass suffices.
   - Never place the bus connector on the bottom side.
5. **Panelisation and fiducials.**
   - 5 mm rails with tooling holes.
   - 3 global fiducials per panel and 2 local fiducials near FX18.
   - V-score is acceptable except where right-angle connectors overhang the edge. Use tab-routing with mouse bites there; FX18-SH overhangs the edge.
6. **Inspection and rework.** AOI on all boards. FX18 0.8 mm leads are visible; DF40-class 0.4 mm parts would need X-ray or tighter process control.
7. **Test points and universal jig.**
   - Bring SWD, UART, I2C, the per-slot lines, 24 V and GND to the 40-pin bus. **One universal jig** (a baseboard-like fixture with an FX18 bridge) can then program, ID-write and functionally test every module type.
   - Add ≥ 1.0 mm test pads at ≥ 2.54 mm pitch for internal rails only.
8. **Conformal coating.** Use acrylic or urethane for outdoor nodes and Class 3 customers. Mask the FX18 contacts, terminal blocks, SIM, RF connectors and test pads.
9. **Traceability.** Print a laser or silkscreen Data Matrix with the serial number on each PCB and a QR label on the housing. Store the serial number and keys in the module ID EEPROM and secure element.
10. **IPC-A-610.** Use Class 2 by default. Offer Class 3 inspection as a paid option for critical industrial customers.
11. **IPC-2221 spacing.** For the 24 V bus with surge, design to the 31–50 V class: about **0.6 mm external uncoated** conductor spacing, and 0.1 mm for ≤ 30 V nets. These values are recalled from IPC-2221B Table 6-1 and not re-checked this session (**UNVERIFIED**, verify against the standard). Safety creepage to SELV/PELV requirements belongs in R01.

## 8. Assembly-cost model (India, 1k–10k) — sanity check of "manufacturing = 40 % of BOM"

Illustrative model. **All rates are UNVERIFIED assumptions**; no Indian EMS rate card could be retrieved this session. Replace them with real quotes.

| Item (Wi-Fi/BLE module, ~120 SMT parts, ~400 joints, 4 THT parts) | 1k | 10k |
|---|---|---|
| SMT at INR 0.30 / joint (assumed) | 120 | 100 (volume rate) |
| THT / hand solder (assumed INR 1.5 / joint × 12) | 18 | 15 |
| Stencil + programme + NPI (INR 15k amortised) | 15 | 1.5 |
| Programming + functional test on universal jig (3 min at INR 600/h) | 30 | 20 |
| Enclosure assembly, label, pack (assumed) | 15 | 10 |
| Yield loss / rework / logistics (5 %) | 10 | 7 |
| **Total conversion cost** | **≈ 208** | **≈ 154** |
| 40 % of BOM 430 | 172 | 172 |

- At **1k, 40 % is tight to slightly insufficient** for a INR 430 BOM module. At **10k it is achievable**.
- For the INR 714 BOM modules (LoRa; 4G + Ethernet + Wi-Fi), 40 % = INR 286. That covers conversion comfortably at both volumes.
- **PCB and enclosure must be counted in the BOM**, not in the 40 %.
- **Main cost risk: the bus connector.** An FX18 pair (≈ INR 350–450, UNVERIFIED) plus a bridge PCB would consume most of a INR 430 BOM. Mitigations:
  - (a) Use the 2.54 mm box-header alternate.
  - (b) Negotiate FX18 pricing.
  - (c) Put the IN receptacle on the module and ship the bridge with the next module, so one module carries one receptacle pair, not two.

## 9. Field connectors (low cost, widely available)

**Not completed: no prices or part numbers were verified this session (search budget exhausted).** Categories to source, with LCSC as the first price check:
- Pluggable terminal blocks 3.5 / 3.81 / 5.08 mm (Phoenix Contact MC/MSTB, Würth WR-TBL, Degson, Dinkle). Degson/Dinkle are normally the low-cost choice and are stocked by LCSC (UNVERIFIED).
- RJ45 with integrated magnetics. Only the combined 4G + Ethernet + Wi-Fi module needs it (per the update).
- Edge-mount and bulkhead SMA; U.FL / IPEX MHF pigtails.
- Push-push nano-SIM holder.
- USB-C 16-pin receptacle (service/config port).
- JST PH 2.0 mm 2-pin for the Li-ion pack (avoid reversed-polarity third-party packs; add reverse-polarity protection).
- DIN-rail clips: integral to the housing if an off-the-shelf DIN housing is used.

## 10. Risks and open decisions

1. **Connector cost vs. Wi-Fi module target.** The FX18 pair is about INR 193 per header at LCSC [S20]; the receptacle price is UNVERIFIED. Decide between FX18 and the 2.54 mm box-header alternate after real quotes.
2. **FX18 lifecycle and stock.** LCSC showed 0 stock on 2026-11-14 [S20], and the catalogue on file is from 2014. Confirm Hirose status and distributor stock (Mouser/DigiKey/element14 India were not reachable).
3. **Bus topology decision:**
   - bridge (recommended) vs. side-wall slide-mate vs. rail-embedded bus (custom TBUS-like insert);
   - also whether the fieldbus (CAN/RS-485) lives on the baseboard or on a small card. It is a few pins either way and does not change the connector.
4. **Total bus current budget** (proposed ≤ 2–3 A at 24 V) and per-slot eFuse/load-switch architecture.
5. **USB-HS only to slot 1.** The 4G + Ethernet + Wi-Fi module's position must be fixed.
6. **Enclosure family not yet chosen.** Survey and quotes are still needed (Phoenix ME, Camdenboss, Italtronic, Indian moulders), as is the custom-tool cost.
7. **Not hot-pluggable.** This must be stated in the user manual (RevPi precedent [S13]).
8. **Items left UNVERIFIED in this report:** FX8/FX8C, Würth WR-PHD/BHD/MM data, all prices other than C598060, enclosure data, field connectors, Indian EMS rates and IPC-2221 values.

## 11. Sources

- [S1] CurrencyBeacon USD/INR — https://currencybeacon.com/rates/USD/INR (accessed 2026-11-14)
- [S2] HDFC Sky / PTI rupee close 94.86 — https://hdfcsky.com/news/rupee-falls-10-paise-to-close-at-94-86-against-us-dollar
- [S3] WAGO 750 manual (blade/spring contacts, sharp edges) — https://www.manualslib.com/manual/1599610/Wago-750-370.html?page=31
- [S4] WAGO power jumper contacts 10 A — https://docs.iba-ag.com/helpsetid=ibaW-750&externalid=W750_leistungskontakte&Language=en-us&publicationversion=1.9
- [S5] WAGO 750-612/622 datasheet (12 mm width) — https://onlinecomponents.com/productfiles/mf-wag/750-612.pdf
- [S6] Beckhoff EL1904 manual (six E-bus contacts, 12/24 mm) — https://www.manualsdir.com/manuals/757384/beckhoff-el1904.html?page=11
- [S7] Beckhoff EL9100 power feed terminal — https://infosys.beckhoff.com/content/1033/el9xxx/1246711051.html
- [S8] Siemens ET 200SP product overview / BaseUnits — https://manualslib.com/manual/1314600/Siemens-Simatic-Et-200sp.html?page=11 ; BaseUnit datasheet https://www.mouser.com/datasheet/3/5917/1/6ES71936BP200DA0_datasheet_en.pdf
- [S9] Siemens ET 200SP BaseUnits manual (light/dark BU, 10 A per potential group) — https://www.manualslib.com/manual/1429852/Siemens-Simatic-Et-200sp.html
- [S10] Phoenix Contact 2707437 ME 22,5 TBUS 1,5/ 5-ST-3,81 GN — https://www.phoenixcontact.com/us/products/2707437
- [S11] Phoenix Contact 2707437 PDF (3.81 mm, 8 A, 150 V) — https://www.phoenixcontact.com/fr/produits/2707437/pdf ; https://www.farnell.com/datasheets/3098443.pdf
- [S12] Revolution Pi blog: PiBridge — https://revolutionpi.com/en/blog/pibridge
- [S13] Revolution Pi tutorial: connecting modules — https://revolutionpi.com/en/tutorials/connecting-revolution-pi-modules
- [S14] Arduino Opta Digital Expansion docs (AUX ports, breakable cover, max 5) — https://docs.arduino.cc/hardware/opta-digital-exp/
- [S15] Arduino Opta Blueprint library README (I2C + UART bus, DETECT IN/OUT) — https://github.com/arduino-libraries/Arduino_Opta_Blueprint
- [S16] Hirose DF40 catalogue (local copy, 03/2012 edition) — datasheets/connectors/Hirose_DF40_datasheet.pdf ; source page https://www.hirose.com/en/product/series/DF40
- [S17] Hirose DF12N catalogue 09/2020 (mirror) — https://static.chipdip.ru/lib/170/DOC011170942.pdf
- [S18] Hirose FX18 catalogue 1/2014 (mirror) — https://cdn.eicom.ru/media/PDF/8172613.pdf ; Hirose product page FX18-40S-0.8SH https://www.hirose.com/product/p/CL0579-0009-4-00
- [S19] Hirose high-speed brochure (FX18 up to 10 Gbps) — https://info.hirose.com/hubfs/US-HS-BRO-18-241-1.0.pdf?hsLang=en
- [S20] LCSC C598060 FX18-40P-0.8SH — https://www.lcsc.com/product-detail/C598060.html
- [S21] Würth WR-BTB 0.8 mm listings: Bürklin 658807713040 https://buerklin.com/en/p/wuerth-elektronik-eisos/pcb-connection-systems/658807713040/09P0239 ; Bürklin 658855603040 https://www.buerklin.com/en/p/wuerth-elektronik-eisos/pcb-connection-systems/658855603040/09P0279 ; Mouser WR-BTB overview https://www.mouser.in/new/wurth-elektronik/wurth-wr-btb-connectors ; element14 2820221 https://in.element14.com/wurth-elektronik/658807713040/connector-rcpt-40pos-2row-0-8mm/dp/2820221 (data seen in search snippets, 2026-11-14)
- [S22] Hirose DF17 40-pin listings: RS 1362298 https://nz.rs-online.com/web/p/pcb-sockets/1362298 ; RS 1360938 https://uk.rs-online.com/web/p/pcb-headers/1360938/ ; Farnell datasheet https://www.farnell.com/datasheets/1286344.pdf
- [S23] JLCPCB part C598060 (Extended library) — https://jlcpcb.com/partdetail/C598060
- Note [S20] price: LCSC page data read 2026-11-14 — ladder 980+ = USD 2.0502, stockNumber 0.
