# R14 — Baseboard costed BOM (v0, 1k units)

Status: COMPLETE WITH GAPS (2026-11-14). Line-by-line BOM in `docs/bom/baseboard_bom_v0.csv`. Every price carries a distributor, date and source. Conversion: 1 USD = INR 93.9; EUR prices at 1 EUR = 1.08 USD (approximate). Prices exclude GST, import duty and freight (GST is recoverable for a registered manufacturer). LCSC figures are search-indexed page snapshots of 2026-11-14, because LCSC pages and its API could not be read directly in this run; they are marked as such in the CSV.

Scope change applied (owner, 2026-11-14, via coordinator): **no Ethernet on the baseboard** (Ethernet comes from the 4G module), **no external secure element**, **fieldbus module removed** (the baseboard keeps 1× isolated RS-485). The MCU therefore no longer needs an Ethernet MAC, and the Ethernet and SE050 option lines are dropped. A QSPI NOR holds the second firmware image.

## 1. Summary

| Item | Value |
|---|---|
| **Baseboard BOM, all required functions** | **INR 1,720.46** |
| Hard limit | INR 2,000 |
| Headroom | **INR 279.54 (14 %)** |
| Finished cost (BOM × 1.5) | INR 2,580.69 |
| Share SOURCED by value | **91.3 %** (INR 1,571.46) |
| Share ESTIMATE by value | 8.7 % (INR 149.00, 14 small lines: passives, discretes, generic protection) — under the 20 % rule |
| Lines | 49 |

Per-block subtotals (INR): MCU, memory, RTC 364.66 · Analog inputs 145.37 · Digital inputs 98.38 · Digital outputs + watchdog 220.12 · Isolated RS-485 171.83 · Power 366.04 · USB-C + LEDs 18.46 · Stack bus connector + ESD 61.31 · Field terminals 134.73 · PCB 79.06 · Passives and misc 60.50.

**The INR 2,000 limit is met with every required function, galvanic isolation on RS-485 and on the digital inputs, a hardware window watchdog on the outputs, and protection on every terminal.** Two choices make it fit: (1) the 2.54 mm shrouded box header instead of the Hirose FX18 for the stack bus (FX18 would add INR 126–387, see §4), and (2) Cixi Kefa pluggable terminals instead of Degson (Degson adds INR 138).

Earlier estimate was INR 4,645. The main savings are: no Ethernet / secure element (the MCU's PSA L3 key storage replaces the SE050), a mid-range MCU (STM32H533, INR 296 vs RA8M1 INR 862), a TI quad high-side switch at LCSC 1k price (INR 108) instead of four discrete switches, opto-isolated digital inputs (INR 66 for 8 channels) instead of ISO1212s, an integrated isolated RS-485 transceiver from Chipanalog (INR 153) instead of a transceiver + Mornsun DC-DC, and the box header.

Sensitivity (each applied alone to the INR 1,720.46 baseline):

| Change | Δ INR | New total |
|---|---|---|
| Degson 15EDGK/15EDGRC terminals instead of Kefa (recommended upgrade if quotes allow) | +138.25 | 1,858.71 |
| Hirose FX18-40S-0.8SH at LCSC price (USD 1.59 @100; only 61 in stock) | +125.54 | 1,846.00 |
| Hirose FX18-40S-0.8SH at DigiKey India (INR 411.22 @1,050; 578 in stock) | +387.46 | **2,107.92 (over)** |
| MCU at DigiKey India list (INR 473.04 @500) instead of Future USD 3.15 | +177.25 | 1,897.71 |
| ST VNI4140KTR instead of TI TPS4H160 (2nd source) | +110.63 | 1,831.09 |
| CA-IS2092W at the lower LCSC reference price (USD 1.44) | −17.84 | 1,702.62 |
| Baseline + Degson + FX18 (LCSC price) | +263.79 | 1,984.25 (just inside) |

## 2. MCU selection (no Ethernet)

Required: TrustZone, PSA Certified Level 3, ≥ 1 CAN-FD, ≥ 5 UARTs, USB FS; no Ethernet MAC needed.

| Part (package) | Fit | Price (1k-class) | Stock / lead time (2026-11-14) | Source |
|---|---|---|---|---|
| **ST STM32H533VET6 (LQFP100) — PICKED** | M33 250 MHz, 512 KB flash, 272 KB RAM, TrustZone, AES/PKA/HUK, **PSA L3** (R08), 2× FDCAN, 4 USART + 2 UART + LPUART, USB FS, OCTOSPI, -40…85 °C | **Future USD 3.15 @150+ = INR 295.79**; DigiKey India INR 473.04 @500 | Future: 514 global, 15 wk factory LT (snapshot; a second Future page shows 0); DigiKey India 0, 535 due 29-Mar-2027, 52 wk | [1][2] |
| ST STM32H533RET6 (LQFP64) | Same die. Too few pins for 16 IO + stack bus + RS-485 + QSPI without a 16-bit I/O expander (≈ INR 25, est.) | Future USD 2.86 @200+ = INR 268.6; DigiKey India INR 377.31 @500; LCSC USD 4.86 @100 (6 pcs) | DigiKey India 0, 960 due 21-Dec-2026, 52 wk; Future also shows 52+ wk | [3][4] |
| ST STM32U585VIT6Q / RIT6Q | M33 160 MHz, 2 MB flash, TrustZone, **PSA L3 (U585 TF-M certificate)**, 1 FDCAN, 4 USART + 2 UART, USB FS. 2 MB flash would hold both images internally | Future USD 5.22 @1k (VIT6Q) = INR 490; DigiKey USD 5.64 @960 (RIT6Q) = INR 530 | Future 0 / 13 wk; Arrow 4,133 (aggregator snapshot); DigiKey FI 717 | [5][6] |
| ST STM32C5A3 / C562 | PSA L3 iSE/SE certificate (24-Apr-2026) but **no TrustZone** (R08) — fails the TrustZone requirement | INR 229 @640 DigiKey India (R08) | 0 / 52 wk (R08) | [7] |
| ST STM32U535/U545 | TrustZone; **no PSA L3 certificate found** (only a NIST entropy certificate) | INR 521 @640 (U545, R08) | 0 / 52 wk (R08) | [6] |
| ST STM32L552/L562 | PSA L2 only (ST AN5156) — fails | not priced | — | [6] |
| NXP MCX N236 / LPC55S6x | No PSA L3 certificate found (R08, R11) — fails | INR 604 (N236, R08) | 13 wk | R08 |
| Renesas RA8M1 | PSA L3 + SESIP3, but has Ethernet and costs INR 862 @500 | — | 720 stock (R12) | R12 |

**Pick: STM32H533VET6.** It is the cheapest part that meets every requirement, and LQFP100 avoids an I/O expander (one less failure point, no shared I2C dependency for output-related signals). The price basis is a Future Electronics snapshot; DigiKey India's list price is INR 177 higher and still keeps the total at INR 1,898. **Second source:** STM32H533RET6 (same die, different footprint — assembly variant with an I/O expander) and STM32U585VIT6Q (PSA L3, 2 MB; pin compatibility with the H533 LQFP100 is UNVERIFIED). **Biggest risk:** H5 supply (52-week lead time at DigiKey). Get an ST franchise 1k quote (Future / Arrow / Avnet India) before freezing.

Second firmware image: the H533 has 512 KB flash, so MCUboot runs with the secondary (download) slot in the external 128 Mbit QSPI NOR (W25Q128JV, 16 MB — far more than one 512 KB image; the rest buffers data when the uplink is down). Because the slot is off-chip, images must be signed and encrypted (MCUboot encrypted images); whether the H533's OTFDEC can decrypt on the fly is UNVERIFIED and not needed for this scheme. Keys stay in the H533 (HUK, secure storage, PSA L3), which is why no external secure element is needed (owner decision).

## 3. BOM by block

Src: S = SOURCED (distributor price with URL in the CSV), E = ESTIMATE.

**1 MCU, memory, RTC**

| Ref | Description | Manufacturer | MPN | Qty | Unit INR | Ext INR | Src | Distributor / note |
|---|---|---|---|---|---|---|---|---|
| U1 | MCU Cortex-M33 250 MHz, 512 KB flash, 272 KB RAM, TrustZone, AES/PKA/HUK, PSA Certified L3, 2x FDCAN, 4 USART + 2 UART + LPUART, USB FS, -40..85 C, LQFP100 (no Ethernet) | ST | STM32H533VET6 | 1 | 295.79 | 295.79 | S | Future Electronics; USD 3.15 @150+, 514 global stock, 15 wk factory LT (search snapshot 2026-11-14; another Future page shows 0). DigiKey India INR 473.04 @500, 0 stock, 535 due 29-Mar-2027, 52 wk. Alt: STM32H533RET6 (LQFP64) + I/O expander |
| Y1 | Crystal 24 MHz 3225 20 pF +/-10 ppm (MCU main clock) | YXC | X322524MSB4SI | 1 | 4.09 | 4.09 | S | LCSC C15643; USD 0.0436 @300, 0.036 @3k; 92,820 stock (snapshot) |
| Y2 | Crystal 32.768 kHz 3215 12.5 pF (RTC) | YXC / Epson | X1E0000210xx class | 1 | 6.00 | 6.00 | E | LCSC; not priced in this run; typical USD 0.05-0.07 |
| U2 | QSPI NOR flash 128 Mbit, 133 MHz, -40..85 C, SOIC-8 | Winbond | W25Q128JVSIQ | 1 | 32.87 | 32.87 | S | LCSC C97521; USD ~0.35 @1k (cached), 0.33-0.37 @100 live; 21k-151k stock. 2nd source GigaDevice GD25Q128E |
| BT1 | CR2032 holder, SMD | Q&J | CR2032-BS-6-1 | 1 | 9.20 | 9.20 | S | LCSC C70377; USD 0.098 @500, 0.094 @2.5k |
| BT1-cell | CR2032 Li-MnO2 coin cell 225 mAh (RTC backup, MCU VBATT) | EVE | CR2032 | 1 | 16.71 | 16.71 | S | TME; USD 0.178-0.274 by qty (search snapshot); Panasonic CR2032 DigiKey USD 0.36 @1, 1.1M stock as 2nd source |
| | **Subtotal** | | | | | **364.66** | | |

**2 Analog inputs (4x 0-10 V / 4-20 mA / PT1000)**

| Ref | Description | Manufacturer | MPN | Qty | Unit INR | Ext INR | Src | Distributor / note |
|---|---|---|---|---|---|---|---|---|
| U10 | Quad op-amp RRIO, 10 MHz, buffers + anti-alias for 4 AI | TI | TLV9064IPWR | 1 | 24.39 | 24.39 | S | LCSC C779410; USD 0.2597 @1k; 4,887-7,689 stock |
| U11 | Voltage reference 2.5 V 0.1 % shunt (ADC VREF+ + PT1000 excitation, ratiometric) | TI | LM4040AIM3X-2.5/NOPB | 1 | 36.62 | 36.62 | S | LCSC C111866; USD 0.39-0.418 @1k; ~6,500 stock |
| R-AI | Precision resistors 0.1 % 25 ppm 0603 (divider x2, 120 R shunt, 4.99k excitation, spare) x5 per channel | Yageo | RT0603BRD07xxxxL | 20 | 1.62 | 32.40 | S | LCSC C122970; USD 0.0173 @600, 0.0157 @5k; 198,960 stock (100R value) |
| F10-F13 | PTC resettable fuse 30 V 50 mA hold, 1210 (reverse-polarity / overload) | TECHFUSE (LCSC) | nSMD005-30V 1210 class | 4 | 4.49 | 17.96 | S | LCSC; USD 0.0478 @100, 0.0329 @4.5k (snapshot) |
| Q10-Q17 | Mode-select MOSFETs (shunt enable N-FET, excitation enable P-FET) SOT-23 | generic (AO3400A / AO3401A class) | AO3400A/AO3401A | 8 | 1.00 | 8.00 | E | LCSC; ~USD 0.01 each |
| Q18-Q21 | 25 mA two-transistor current limiter per channel, SOT-89 pass transistor (survives 24 V on terminal in mA mode) | generic | BCX56 / BC847 class | 4 | 4.00 | 16.00 | E | LCSC; ~USD 0.04 per channel |
| D10-D13 | Bidirectional TVS 15 V SOD-123FL + BAT54S rail clamp per channel | generic | SMF15CA + BAT54S | 4 | 2.50 | 10.00 | E | LCSC; ~USD 0.025 per channel |
| | **Subtotal** | | | | | **145.37** | | |

**3 Digital inputs (8x 24 V Type 1/3, 2 isolated groups)**

| Ref | Description | Manufacturer | MPN | Qty | Unit INR | Ext INR | Src | Distributor / note |
|---|---|---|---|---|---|---|---|---|
| U20-U21 | Quad phototransistor optocoupler 3.75 kVrms, SO16 (one per group of 4) | Toshiba | TLP293-4(GB-TP,E | 2 | 33.19 | 66.38 | S | LCSC C112623; USD 0.335-0.373 @1k; 2,000/reel. 2nd source Lite-On LTV-247 / Everlight EL3H7 x4 |
| DI-FE | Per-channel Type 3 front end: 3 mA current limiter, 6.8 V threshold zener, reverse diode, filter (x8) | generic | BC847/BZT52C6V8/1N4148W/1206 | 8 | 4.00 | 32.00 | E | LCSC; ~USD 0.04 per channel |
| | **Subtotal** | | | | | **98.38** | | |

**4 Digital outputs (4x 24 V high-side) + window watchdog**

| Ref | Description | Manufacturer | MPN | Qty | Unit INR | Ext INR | Src | Distributor / note |
|---|---|---|---|---|---|---|---|---|
| U30 | Quad high-side switch 40 V, 160 mOhm, adjustable current limit 0.5-2.5 A, short/thermal/open-load diagnostics | TI | TPS4H160AQPWPRQ1 | 1 | 108.16 | 108.16 | S | LCSC C485918; USD 1.1116-1.1519 @1k, 6,391 stock; DigiKey India INR 226.28 @500, 0 stock, 26 wk. 2nd source ST VNI4140KTR USD 2.33 @1k (Future) |
| U31 | Window watchdog timer, independent RC timebase, WDO gates all output enables | TI | TPS3430WDRCR | 1 | 70.02 | 70.02 | S | LCSC C2870545; USD 0.6818-0.7457 @1k, 637-1,255 stock; DigiKey India INR 142.03 @1k, 3,114 stock |
| U32 | Quad 2-input AND (MCU enable AND watchdog-OK) to TPS4H160 EN pins | TI / Nexperia | 74LVC08APW | 1 | 4.00 | 4.00 | E | LCSC; ~USD 0.04 |
| D30-D34 | TVS 600 W 33 V SMB on each output and on L+ | generic (GOODWORK / MDD) | SMBJ33A | 5 | 3.08 | 15.40 | S | DigiKey India (R06 S51); INR 3.08 (GOODWORK) - 15.9 (MDD), R06 2026-11-14 |
| Q30 | Reverse-polarity P-FET -60 V on output supply L+ | Diodes | DMP6023LE-13 | 1 | 22.54 | 22.54 | S | LCSC (R06 S39); USD 0.24 @5k (R06); 1k price ~USD 0.29 (DMP6023LFGQ) |
| | **Subtotal** | | | | | **220.12** | | |

**5 RS-485 isolated**

| Ref | Description | Manufacturer | MPN | Qty | Unit INR | Ext INR | Src | Distributor / note |
|---|---|---|---|---|---|---|---|---|
| U40 | Isolated RS-485 half-duplex transceiver with integrated isolated DC-DC, 5 kVrms, 0.5 Mbps, -40..125 C, SOIC-16W | Chipanalog | CA-IS2092W | 1 | 153.06 | 153.06 | S | LCSC C5121950; USD 1.63 @1k (61 stock) / ref USD 1.44 (2,465 stock) snapshots. 2nd source CA-IS2092VW (C7422559) or TI ISOW1412 |
| D40 | RS-485 TVS -7/+12 V 600 W SOT-23 | FUXINSEMI | SM712 | 1 | 2.77 | 2.77 | S | LCSC C908219; USD 0.0295 @100; 166,210 stock |
| F40-F41 | Series PTC / pulse resistors on A and B | generic | 10R 1206 pulse / PTC 1206 | 2 | 4.00 | 8.00 | E | LCSC; R05 budget INR 4-8 for pair |
| SW40 | Termination 120 R + bias enable, 2-pole DIP switch + resistors | generic | DIP-2 SMD | 1 | 8.00 | 8.00 | E | LCSC; R05 budget INR 6-10 |
| | **Subtotal** | | | | | **171.83** | | |

**6 Power**

| Ref | Description | Manufacturer | MPN | Qty | Unit INR | Ext INR | Src | Distributor / note |
|---|---|---|---|---|---|---|---|---|
| F1 | Input fuse 3 A slow, 1812 / 2410 SMD | generic (Littelfuse 0466 class) | 3 A SMD fuse | 1 | 5.00 | 5.00 | E | LCSC; ~USD 0.05 |
| D1 | Input TVS 1500 W 33 V SMC | Littelfuse | SMCJ33A | 1 | 15.57 | 15.57 | S | LCSC C224049; USD 0.1658 @500, 0.1528 @3k; 5,145 stock. 2nd source JieJie SMCJ33A USD 0.1016 @1k |
| Q1 | Reverse-polarity P-FET -60 V on main input (+ 12 V gate zener, resistor) | Diodes | DMP6023LE-13 | 1 | 22.54 | 22.54 | S | LCSC (R06 S39); USD 0.24 @5k (R06) |
| C1-L1 | Input bulk electrolytic 47 uF 63 V + pi filter (ferrite/inductor + 2x 2.2 uF 100 V 1210) | generic |  | 1 | 12.00 | 12.00 | E | LCSC; ~USD 0.13 |
| U3 | Stack-bus feed eFuse 60 V, 2.2 A adjustable current limit, OVP cut-off, reverse-current block; PGTH/PGOOD comparator used as power-fail detector | TI | TPS26600PWPR | 1 | 105.49 | 105.49 | S | LCSC C544399; USD 1.1234 @1k, 3,203 stock; JLCPCB USD 0.8907 @1k; DigiKey India INR 196.10 @2k, 0 stock |
| U4 | Buck 60 V in, 0.6 A, to 5 V (charger input, RS-485 iso supply) | TI | LMR36006FSCQRNXRQ1 | 1 | 74.12 | 74.12 | S | LCSC C2869760; USD 0.7893 @1k; 2,886 stock. 2nd source LMR36006CRNXR USD 1.31 @1k |
| L2-L3 | Power inductor 4.7 uH 2 A 4x4 shielded (5 V and 3.3 V bucks) | Sunlord | SWPA4030S4R7MT | 2 | 3.33 | 6.66 | S | LCSC C57269; USD 0.0348-0.0368 @300; 38k-87k stock |
| U5 | 1-cell Li-ion charger 1.5 A with power path (SYS), TS/NTC input for 0-45 C charge window, safety timer | TI | BQ24074RGTR | 1 | 92.57 | 92.57 | S | LCSC C54313; USD 0.9858 @1k; 191-986 stock (snapshots). 2nd source BQ24072RGTR |
| U6 | Independent Li-ion protector (OV/UV/OC/short) | TI | BQ29700DSER | 1 | 15.04 | 15.04 | S | LCSC C183096; USD 0.1491-0.1602 @1k |
| Q6 | Dual N-MOSFET for protector, TSSOP-8 | HXY MOSFET | 8205A | 1 | 2.75 | 2.75 | S | LCSC C5148694; USD 0.0293 @1k; 40,660 stock |
| U7 | Buck 2 A, 100 % duty, to 3.3 V from charger SYS | TI | TLV62569DBVR | 1 | 10.30 | 10.30 | S | DigiKey (US); USD 0.1097 @1k; LCSC C141836 USD 0.0392 @500, 78,915 stock |
| J5 | Battery connector 2-pin + 10k NTC (cell pack plugs in, user-replaceable) | JST / generic | PH 2.0 + NCP18XH103 | 1 | 4.00 | 4.00 | E | LCSC; ~USD 0.04 |
| | **Subtotal** | | | | | **366.04** | | |

**7 USB-C service port and status LEDs**

| Ref | Description | Manufacturer | MPN | Qty | Unit INR | Ext INR | Src | Distributor / note |
|---|---|---|---|---|---|---|---|---|
| J6 | USB Type-C 16-pin receptacle, SMD | Korean Hroparts | TYPE-C-31-M-12 | 1 | 9.20 | 9.20 | S | LCSC C165948; USD 0.098 @1k; 125,255 stock |
| U8 | USB ESD protection, 2-line + VBUS | ST | USBLC6-2SC6 | 1 | 7.26 | 7.26 | S | LCSC C7519; USD 0.0773 @500, 0.0734 @3k; 54,100 stock |
| LED1-4 | Status LEDs 0603 (power, run, fault, comms) | generic | 0603 LED | 4 | 0.50 | 2.00 | E | LCSC; ~USD 0.005 each |
| | **Subtotal** | | | | | **18.46** | | |

**8 Stack bus connector and protection**

| Ref | Description | Manufacturer | MPN | Qty | Unit INR | Ext INR | Src | Distributor / note |
|---|---|---|---|---|---|---|---|---|
| J1 | 40-pin 2x20 2.54 mm shrouded box header (keyed), THT - BASELINE (FX18 alternative see report) | BXCONN | 2.54JN-2-20-Z | 1 | 23.76 | 23.76 | S | LCSC C53207293; USD 0.253 @50, 0.32 @5; 40 stock; many makers (BOOMELE C50980, CONNFLY) |
| U9a-c | ESD arrays on exposed stack-bus lines, 4-ch | TI | TPD4E05U06DQAR | 3 | 12.05 | 36.15 | S | Lion Circuits (R11 S39); INR 12.05 @1k; Farnell USD 0.149 @1k |
| R-PE | Per-slot power-enable outputs (5 GPIO, series 100 R + pull-down) and bus series resistors | UNI-ROYAL | 0603WAF series | 20 | 0.07 | 1.40 | S | LCSC C25804; USD 0.0007 @1k |
| | **Subtotal** | | | | | **61.31** | | |

**9 Field terminals**

| Ref | Description | Manufacturer | MPN | Qty | Unit INR | Ext INR | Src | Distributor / note |
|---|---|---|---|---|---|---|---|---|
| J20-J24 plugs | Pluggable terminal plugs 3.81 mm, 27 poles total (5P DC+RS-485, 6P DO+L+/M, 5P DI grp1, 5P DI grp2, 6P AI) | Cixi Kefa | KF2EDGK-3.81-xP | 27 | 3.61 | 97.47 | S | LCSC C440864; USD 0.3079 @1k for 8P (= USD 0.0385/pole); 8,450 stock. Degson 15EDGK USD 0.0761/pole |
| J20-J24 headers | Mating PCB headers 3.81 mm right-angle, 27 poles total | Cixi Kefa | KF2EDGR-3.81-xP | 27 | 1.38 | 37.26 | S | LCSC C441185; USD 0.0735 @500 for 5P (= USD 0.0147/pole); 1,935 stock |
| | **Subtotal** | | | | | **134.73** | | |

**10 PCB**

| Ref | Description | Manufacturer | MPN | Qty | Unit INR | Ext INR | Src | Distributor / note |
|---|---|---|---|---|---|---|---|---|
| PCB | 4-layer FR4 1.6 mm, ~100 x 80 mm, HASL LF, 1 oz, 1k qty; JLCPCB volume rate USD 84.2/m2 all-in (USD 421.10 per 5 m2) / 0.8 panel use | JLCPCB (CN); cross-check Indian fab | 4L 100x80 | 1 | 79.06 | 79.06 | S | JLCPCB; Rate dated 2024-03; Aug-2026 notice removes volume surcharges (no new figures). IndiaMART 4L INR 0.65-0.85/cm2 = INR 52-68. Shipping/duty not included |
| | **Subtotal** | | | | | **79.06** | | |

**11 Passives and misc**

| Ref | Description | Manufacturer | MPN | Qty | Unit INR | Ext INR | Src | Distributor / note |
|---|---|---|---|---|---|---|---|---|
| C-misc | MLCC 0603 100 nF / 1 nF / 10 nF X7R, ~90 pcs | Yageo | CC0603KRX7R9BB104 and similar | 90 | 0.17 | 15.30 | S | LCSC C14663; USD 0.0012-0.0018 @4k; 385k-13M stock |
| R-misc | Resistors 0603 1 %, ~160 pcs | UNI-ROYAL | 0603WAF series | 160 | 0.07 | 11.20 | S | LCSC C25804; USD 0.0007 @1k; 1.46M stock |
| C-bulk | Bulk MLCC 10-22 uF 0805/1206 (25-50 V where needed), ~14 pcs | Samsung / Murata | CL21A106 / CL31 class | 14 | 2.00 | 28.00 | E | LCSC; ~USD 0.02 each |
| FB-misc | Ferrite beads, test points, 1N4148W/BZT52 extras | generic |  | 1 | 6.00 | 6.00 | E | LCSC;  |
| | **Subtotal** | | | | | **60.50** | | |

**Total baseboard BOM: INR 1,720.46**


## 4. Stack bus connector: FX18 versus 2.54 mm box header

| Option | Part | Price | Stock | Notes |
|---|---|---|---|---|
| **Baseline: 2.54 mm 2×20 shrouded box header** | BXCONN 2.54JN-2-20-Z (LCSC C53207293); many makers (BOOMELE, CONNFLY) | **INR 23.76** (USD 0.253 @50) | 40 at LCSC for this MPN; commodity part with many sources | 3 A per pin, keyed shroud (meets SAF-3 polarisation), THT so mechanically strong, easy for Indian CMs. Bigger (≈ 51 × 9 mm) and fewer mating cycles than FX18; does not give FX18's blind-mate guide. |
| Hirose FX18-40S-0.8SH (right-angle receptacle) | DigiKey India | INR 411.22 @1,050 | 578 in stock, 16 wk | +INR 387 → total INR 2,108 (over the limit) |
| Hirose FX18-40S-0.8SH | LCSC C5360360 | INR 149.30 (USD 1.59 @100) | 61 (snapshot) | +INR 126 → INR 1,846. 1k availability at this price not confirmed; Hirose global stock page lists Mouser 3,804 at USD 4.67 @1 |

Recommendation: freeze the box header for the first build unless an FX18 franchise quote at ≤ USD 2 for 1k arrives; the FX18 fits the budget only at the LCSC-level price. Both choices need the R07 bridge/mating concept settled (D-9); the mating half sits on the modules or the bridge, not in this BOM.

## 5. Key design choices and their reliability / safety rationale

- **Input protection (9–36 V):** 3 A SMD fuse → SMCJ33A 1500 W TVS → –60 V P-FET reverse-polarity switch → pi filter. All downstream parts are rated ≥ 60 V (LMR36006 buck 60 V, TPS26600 eFuse 60 V), so the TVS clamp (~53 V) never exceeds a rating. P-FET instead of a diode keeps loss low; reverse polarity to –60 V is blocked.
- **Stack-bus feed through TPS26600 eFuse:** adjustable current limit (set ≈ 2 A, PS2 class with margin), OVP cut-off, reverse-current blocking and auto-retry. A short on the bus or in one module trips the eFuse but never the baseboard's own supply, so the baseboard MCU can log the fault and power-cycle modules (BASE-4, PWR-6). Its independent PGTH/PGOOD comparator monitors the raw input and is used as the **power-fail detector** (interrupt to the MCU) at no extra cost; the MCU also reads VIN through a divider.
- **Per-slot power-enable outputs:** five MCU GPIOs with series resistors and pull-downs (modules default OFF), each module switches its own supply (R06). Exposed bus lines carry TPD4E05U06 ESD arrays (EMC-3).
- **Li-ion:** BQ24074 power-path charger (TS input enforces the 0–45 °C charge window, safety timer) plus an **independent** BQ29700 protector with its own dual FET, so a charger fault is caught by a second device (PWR-7, single-fault safe per IEC 62368-1 Annex M intent). The cell is a plug-in pack (user-replaceable, SAF-6). The 3.3 V buck (TLV62569, 100 % duty) runs from the charger's SYS rail, so the MCU, RTC and power-fail logging keep running on the cell.
- **Digital outputs:** TI TPS4H160 quad high-side switch: per-channel current limit set to ≈ 0.7 A (adjustable 0.5–2.5 A), thermal shutdown, short-to-battery and open-load diagnostics, internal inductive clamp. Outputs are fed from their own L+ terminal through a –60 V P-FET (reverse polarity) and a TVS, so the outputs can run from plant 24 V while the board runs from the 12 V adapter. Not isolated (common 0 V with the board) — standard for low-cost PLC outputs.
- **Hardware window watchdog (IO-4, SAF-4):** TPS3430 with its own RC timebase; its WDO output is ANDed (74LVC08) with every MCU enable line, so a hung, too-fast or reset MCU, or a lost 3.3 V rail, forces all four outputs OFF independent of firmware. TPS4H160 inputs have internal pull-downs, so an unpowered gate also means OFF.
- **Digital inputs:** two groups of four, each on one TLP293-4 quad optocoupler (3.75 kVrms), with a per-channel 3 mA current limiter and 6.8 V threshold zener so the input meets IEC 61131-2 Type 1/3 thresholds from 11–30 V with low dissipation (≈ 90 mW per channel at 30 V), plus a reverse diode. 24 V on any input is the normal ON state; reverse polarity is blocked. Group isolation protects the MCU from ground loops on field wiring. Two channels can be pulse counters (TLP293 switching ≈ tens of µs, so ≤ ~2 kHz; UNVERIFIED for this coupler).
- **RS-485:** CA-IS2092W integrated isolated transceiver with on-chip isolated DC-DC (5 kVrms, -40…125 °C), SM712 TVS and series PTC/pulse resistors on A/B, DIP-switch termination and bias. One part replaces the transceiver + isolator + Mornsun-type module (banned).
- **Analog inputs:** see §6. Each terminal survives 24 V and reverse polarity: a PTC (50 mA hold) in series trips on reverse current through the clamp; in mA mode a 25 mA two-transistor limiter keeps shunt power at ≈ 75 mW and the SOT-89 pass transistor at ≈ 0.55 W continuous; in 0–10 V and PT1000 mode the input is high-impedance (130 kΩ divider) and diode-clamped after a series resistor.
- **MCU security:** PSA L3 MCU holds the device keys (no secure element, owner decision). MCUboot with signed, encrypted images, rollback counters; debug locked in production (SEC-2…4).
- **USB-C service port:** USBLC6-2SC6 ESD on D+/D– and VBUS; device mode only, 5.1 kΩ CC pull-downs.
- **Terminals:** 27 poles, 3.81 mm pluggable (Phoenix MC 1,5-compatible pitch): 5P DC in + RS-485 (V+, V–, A, B, ISO-GND), 6P DO (4 + L+ + M), 5P + 5P DI (4 + COM per isolated group), 6P AI (4 + 2 AGND).
- **PCB:** 4-layer gives solid ground and power planes for EMC; isolation barriers (DI groups, RS-485) get ≥ 2.5 mm creepage with a board slot under the isolators.

## 6. Analog input accuracy (MCU 12-bit ADC)

Reference: LM4040A-2.5 (0.1 % initial) drives the H533 VREF+ pin (available on LQFP100) and the PT1000 excitation, so PT1000 is ratiometric. Inputs are buffered by a TLV9064 quad op-amp with an RC anti-alias filter. LSB = 2.5 V / 4096 = 0.61 mV. STM32H5 ADC total unadjusted error assumed ±4 LSB (UNVERIFIED for H533; check the datasheet).

| Mode | Scaling | Resolution | Accuracy (estimate) |
|---|---|---|---|
| 0–10 V | 0.1 % divider ≈ 0.24 → 10 V = 2.4 V; Rin ≈ 130 kΩ | ≈ 2.5 mV | ±0.5 % FS over 0–60 °C uncalibrated (ratio 0.2 %, reference drift ≤ 100 ppm/°C × 35 °C ≈ 0.35 %, ADC 0.1 %); ±0.2–0.3 % FS at 25 °C with a one-point factory calibration |
| 4–20 mA | 120 Ω 0.1 % shunt (20 mA = 2.4 V), sensed Kelvin so the mode FET's RDS(on) does not enter | ≈ 5 µA | ±0.5 % FS uncalibrated; ±0.3 % FS calibrated. Burden ≈ 2.4 V + limiter ≈ 3.5 V at 20 mA |
| PT1000 (2-wire) | 0.42 mA from 2.5 V via 4.99 kΩ 0.1 %; ≈ 1.34 mV/°C at 0 °C; range –50…+200 °C | 0.46 °C/LSB raw, ≈ 0.12 °C with 16× oversampling | ±1.5 °C uncalibrated-ADC, ±1 °C after one-point calibration (excitation resistor 0.1 % ≈ 0.26 °C, ADC INL ≈ 1–2 °C raw, reduced by oversampling); lead resistance adds +0.26 °C per Ω (2-wire); self-heating 0.18 mW, negligible |

If ±0.1 % / ±0.3 °C is needed later, add a 16-bit ΔΣ ADC (ADS1115 / ADS1220 class) as an assembly option — not priced here.

## 7. Optional lines (NOT in the INR 2,000)

| Option | Part | INR | Source / note |
|---|---|---|---|
| Li-ion cell, 18650 2600 mAh (plug-in pack with leads; holder/leads ≈ INR 25, est.) | BIS-certified cell, retail | **≈ 226 + 25 = 251** | ThinkRobotics INR 225.99 (described as BIS certified) [38] |
| — cost-down cell | DMEGC / generic 18650 2600 mAh | 72–190 | TradeIndia INR 72 @MOQ 1,000 (BIS not stated); Makerbazar INR 115 (DMEGC); Hubtronics INR 189.80 + GST [38]. BIS (IS 16046-2) registration must be checked per supplier on the BIS CRS portal |
| Enclosure, Indian | Electrocom Connectors EC7060 / EC7060-1 ABS DIN-rail enclosure | **85–110** | IndiaMART [39]. Width, module count and flame rating not stated; ABS is often UL94 HB, so ask for a UL94 V-0 grade (SAF-5) |
| Enclosure, Chinese | 4-module DIN-rail meter case | **≈ 470** (USD 5 @1k–2,999) | Alibaba [39]. V-0 not stated |
| Enclosure, branded reference | CamdenBoss CNMB/4/KIT, PC, UL94 V-0, 71 × 90 × 58 mm | 878.09 @1k | DigiKey India, 40 stock, 6 wk [39] |
| CAN-FD port (not required in the brief; fieldbus module removed) | NXP TJA1051T/3 + CAN TVS + 3-pole terminal | ≈ 33 + 5 + 15 | R05 (LCSC USD 0.349 @1k). Decide whether the baseboard needs a CAN terminal now that the fieldbus module is gone |
| FX18 stack connector instead of box header | Hirose FX18-40S-0.8SH | +126 to +387 | §4 |

Note on the 67.5 mm DIN width: the enclosures found are 4-module (70–72 mm). A 67.5 mm (3 × 22.5 mm) family was not found priced in India or China in this run; ask Indian makers (Gaurang MD series lists UL94 V-0 PC/ABS covers) for a quote.

Dropped on owner instruction: Ethernet option (PHY + RJ45 + ESD, was INR ≈ 300–650 per R11) and the NXP SE050 secure element (Farnell EUR 1.86 @1k ≈ INR 189).

## 8. Cut options (only if quotes come in high)

The baseline is INR 279.54 under the limit, so no cut is needed. If franchise quotes push the total over INR 2,000, cut in this order (lowest impact on reliability and safety first):

| Rank | Cut | Saves INR | Impact |
|---|---|---|---|
| 1 | Use the LCSC price for TLV62569 and JieJie SMCJ33A; CA-IS2092W at USD 1.44 | ≈ 30 | None (same function; JieJie is a well-known TVS maker) |
| 2 | Chinese 4-ch ESD arrays (≈ INR 3) instead of TI TPD4E05U06 on the stack bus | ≈ 27 | Very low; check IEC 61000-4-2 rating in the datasheet |
| 3 | LM4040C (0.5 %) or TL431 reference with factory calibration | ≈ 25–30 | Low: AI drift over temperature rises from ≈ 0.35 % to ≈ 0.5–1 % FS |
| 4 | Replace TPS3430 by a discrete charge-pump "dynamic enable" watchdog (MCU must toggle a pin within a frequency band) | ≈ 65 | Moderate: still firmware-independent and fail-safe, but less precise window and more parts to verify |
| 5 | Non-isolated digital inputs (resistor/zener front end, no optocouplers) | ≈ 60 | High: loses ground-loop and surge isolation on 8 field lines |
| 6 | Non-isolated RS-485 (SIT3485E + SM712 + PTC, ≈ INR 20) | ≈ 135 | High: long RS-485 cables are the most common field failure; keep isolation unless forced |

## 9. Risks

1. **MCU supply:** DigiKey India shows 0 stock and 52 weeks for both H533 packages (incoming 960 RET6 on 21-Dec-2026, 535 VET6 on 29-Mar-2027). The INR 296 price is a Future snapshot that conflicts with a second Future page. Get an ST franchise quote; keep the RET6 + I/O-expander variant and the U585 as fall-backs.
2. **LCSC snapshot prices:** most passive, power and interface prices are LCSC page snapshots that disagree by 5–30 % between captures. A +15 % error on all LCSC lines adds ≈ INR 120, which still fits.
3. **Pin budget of LQFP100:** ≈ 76 signals counted (16 IO, 8 AI mode selects, RS-485, stack bus 18, QSPI 6, USB, CAN, LEDs, charger/eFuse status) against ≈ 80 GPIO. Do the pin plan before layout.
4. **TPS4H160 voltage margin:** the L+ TVS clamp must stay below the switch's absolute maximum supply rating (UNVERIFIED in this run); choose the TVS (SMBJ30A/33A) after checking the datasheet.
5. **Chinese single-source parts:** CA-IS2092W (Chipanalog) and Kefa terminals. Second sources: CA-IS2092VW / TI ISOW1412 (more expensive); Degson terminals (+INR 138). Check UL/VDE files for the chosen terminal series.
6. **Off-chip second image:** needs MCUboot image encryption and a tested power-fail-safe swap; the 512 KB internal flash must fit TF-M/MCUboot + application (R09 flagged it as tight).
7. **PCB price** uses a JLCPCB 2024 rate (Aug-2026 changes not quantified) and excludes freight/duty; Indian fabs quote INR 52–68 for 80 cm² (IndiaMART), so the INR 79 line is reasonable.
8. **Costs not in the BOM:** GST, import duty, freight, assembly, test, the mating bus connector on modules, and the enclosure.

## 10. Not verified in this run

STM32H533 ADC accuracy figures; TPS4H160 absolute-maximum supply voltage; TLP293-4 switching speed for pulse inputs; exact 1k prices at LCSC (only snapshots); FX18 1k franchise price; BIS registration of any Li-ion cell; enclosure dimensions and flame ratings for the Indian and Chinese listings; pin compatibility H533 ↔ U585; 32.768 kHz crystal, LEDs, small discretes and bulk capacitors (ESTIMATE lines).

## 11. Sources (accessed 2026-11-14)

1. Future Electronics STM32H533VET6 (USD 3.15 @150+, 514 stock, 15 wk; second page 0 stock) — https://www.futureelectronics.com/p/semiconductors--microcontrollers--32-bit/stm32h533vet6-stmicroelectronics-9188274
2. DigiKey India STM32H533VET6 (INR 473.04 @500, 0 stock, 535 due 29-Mar-2027, 52 wk) — https://www.digikey.in/en/products/detail/stmicroelectronics/STM32H533VET6/22519649
3. DigiKey India STM32H533RET6 (INR 377.31 @500, 0 stock, 960 due 21-Dec-2026, 52 wk) — https://www.digikey.in/en/products/detail/stmicroelectronics/STM32H533RET6/22519671
4. Future STM32H533RET6 (USD 2.86 @200+; other page 52+ wk) — https://www.futureelectronics.com/p/semiconductors--microcontrollers--32-bit/stm32h533ret6-stmicroelectronics-3186130 ; LCSC C26082149 (USD 4.86 @100, 6 stock) — https://www.lcsc.com/product-image/C26082149.html
5. STM32U585 prices: Future (VIT6Q USD 5.22 @1k, 0 stock, 13 wk) — https://www.futureelectronics.com/p/1163081 ; DigiKey (RIT6Q USD 5.64 @960) — https://www.digikey.com/en/products/detail/stmicroelectronics/STM32U585RIT6Q/18085397 ; findchips — https://www.findchips.com/search/u585
6. PSA certificates and ST security levels: STM32U585 TF-M PSA L3 — https://products.psacertified.org/products/stm32u585-tfm/certificates ; ST AN5156 (L5 = PSA L2; U5/H5 certifiable to L3) — https://www.st.com/content/st_com/en/technical-documents/an5156-introduction-to-security-for-stm32-mcus-stmicroelectronics_asset/chunk-005-topic-an5156-arm-tf-m-solution.html ; NIST ESV U535/U545 — https://csrc.nist.gov/projects/cryptographic-module-validation-program/entropy-validations/certificate/158 ; H533 PSA L3: R08 [S4]
7. PSA Certified STM32C5 series (Level 3 iSE/SE, 24-Apr-2026) — https://products.psacertified.org/products/stm32c5-series-advanced-arm-based-32-bit-mcus
8. Earlier Ethernet-MCU candidates checked before the scope change: DigiKey India R7FA6M5BH3CFP#BA0 (INR 476.03 @720, 18 wk) — https://www.digikey.in/en/products/detail/renesas-electronics-corporation/R7FA6M5BH3CFP-BA0/21410198 ; #AA0 (INR 639.29 @540, 342 stock) — https://www.digikey.in/en/products/detail/renesas-electronics-corporation/R7FA6M5BH3CFP-AA0/13918502 ; DigiKey India STM32H563VIT6 (INR 608.05 @540, 0 stock, 52 wk) — https://www.digikey.in/en/products/detail/stmicroelectronics/STM32H563VIT6/18110514 ; LCSC STM32H573VIT6 C7545121 (0 stock) — https://lcsc.com/product-detail/microcontrollers-mcu-mpu-soc_stmicroelectronics-stm32h573vit6_C7545121.html
9. TPS4H160AQPWPRQ1: LCSC C485918 (USD 1.11–1.15 @1k, 6,391 stock) — https://www.lcsc.com/product-detail/power-distribution-switches_texas-instruments-tps4h160aqpwprq1_C485918.html ; DigiKey India (INR 226.28 @500, 0 stock, 26 wk) — https://www.digikey.in/en/products/result?keywords=TPS4H160AQPWPRQ1
10. VNI4140K: ST product page (budgetary USD 2.73 @1k, Mouser stock) — https://st.com/ja/power-management/vni4140k.html ; Future (USD 2.33 @1k) — https://futureelectronics.com/p/semiconductors--analog--power-switches/vni4140ktr-stmicroelectronics-4023965
11. TPS3430WDRCR: LCSC C2870545 (USD 0.68–0.75 @1k) — https://www.lcsc.com/product-detail/C2870545.html ; DigiKey India (INR 142.03 @1k, 3,114 stock) — https://www.digikey.in/en/products/result?keywords=TPS3430WDRCR
12. CA-IS2092W: LCSC C5121950 — https://lcsc.com/product-detail/Isolated-RS-485-422-Transceivers-with-power_Chipanalog-CA-IS2092W_C5121950.html ; datasheet listing (USD 1.63 @1k) — https://datasheet.lcsc.com/lcsc/2207281800_Chipanalog-CA-IS2092W_C5121950.pdf ; CA-IS2092VW C7422559 — https://www.lcsc.com/product-detail/C7422559.html
13. SM712 FUXINSEMI C908219 — https://www.lcsc.com/product-detail/C908219.html
14. TLP293-4(GB-TP,E C112623 — https://www.lcsc.com/product-detail/C112623.html
15. TLV9064IPWR C779410 — https://www.lcsc.com/product-detail/C779410.html
16. LM4040AIM3X-2.5/NOPB C111866 — https://www.lcsc.com/product-detail/C111866.html
17. Yageo RT0603BRD07 0.1 % C122970 — https://www.lcsc.com/product-detail/C122970.html
18. PTC resettable fuses, LCSC category (1210 50 mA 30 V TECHFUSE) — https://www.lcsc.com/category/127.html
19. TPS26600PWPR: LCSC C544399 — https://www.lcsc.com/product-image/C544399.html ; JLCPCB — https://jlcpcb.com/partdetail/TexasInstruments-TPS26600PWPR/C544399 ; DigiKey India — https://www.digikey.in/en/products/result?keywords=TPS26600PWPR
20. LMR36006FSCQRNXRQ1 C2869760 — https://lcsc.com/product-detail/DC-DC-Converters_Texas-Instruments-LMR36006FSCQRNXRQ1_C2869760.html
21. Sunlord SWPA4030S4R7MT C57269 — https://lcsc.com/product-detail/Power-Inductors_Sunlord-SWPA4030S4R7MT_C57269.html
22. BQ24074RGTR C54313 — https://www.lcsc.com/product-image/C54313.html
23. BQ29700DSER C183096 — https://www.lcsc.com/product-detail/C183096.html ; HXY 8205A C5148694 — https://www.lcsc.com/datasheet/lcsc_datasheet_2209201730_HXY-MOSFET-8205A_C5148694.pdf
24. TLV62569DBVR: DigiKey — https://www.digikey.com/en/products/detail/texas-instruments/TLV62569DBVR/7688370 ; LCSC C141836 — https://www.lcsc.com/product-image/C141836.html
25. SMCJ33A: Littelfuse C224049 — https://www.lcsc.com/product-image/C224049.html ; JieJie C356786 — https://datasheet.lcsc.com/lcsc/2304140030_Jiangsu-JieJie-Microelectronics-SMCJ33A_C356786.pdf
26. R06 (this repo): SMBJ33A DigiKey India INR 3.08–15.9 [R06 S51]; DMP6023LE LCSC USD 0.24 @5k [R06 S39]
27. W25Q128JVSIQ C97521 — https://www.lcsc.com/product-detail/C97521.html
28. YXC X322524MSB4SI C15643 — https://lcsc.com/datasheet/lcsc_datasheet_2409301532_YXC-Crystal-Oscillators-X322524MSB4SI_C15643.pdf
29. CR2032 holder Q&J C70377 — https://lcsc.com/datasheet/lcsc_datasheet_2409302302_Q-J-CR2032-BS-6-1_C70377.pdf ; EVE CR2032 225 mAh at TME (search snapshot, USD 0.178–0.274; listing URL not captured) ; Panasonic CR2032 DigiKey — https://www.digikey.com/en/products/detail/CR2032/P189-ND/31939
30. TYPE-C-31-M-12 C165948 — https://www.lcsc.com/product-image/C165948.html ; USBLC6-2SC6 C7519 — https://www.lcsc.com/product-image/C7519.html
31. TPD4E05U06DQAR, Lion Circuits INR 12.05 @1k (R11 S39) — https://lioncircuits.com/parts/TPD4E05U06DQAR
32. Box header BXCONN 2.54JN-2-20-Z C53207293 — https://www.lcsc.com/product-detail/C53207293.html ; BOOMELE C50980 — https://www.lcsc.com/product-detail/C50980.html
33. FX18-40S-0.8SH: DigiKey India (INR 411.22 @1,050, 578 stock, 16 wk) — https://www.digikey.in/en/products/detail/hirose-electric-co-ltd/FX18-40S-0-8SH/2349550 ; LCSC C5360360 — https://lcsc.com/product-detail/Board-to-Board-and-Backplane-Connector_HRS-Hirose-FX18-40S-0-8SH_C5360360.html ; Hirose distributor stock — https://www.hirose.com/en/product/global-stock-information/CL0579-0009-4-00
34. Cixi Kefa KF2EDGK-3.81-8P C440864 — https://lcsc.com/product-detail/Pluggable-System-Terminal-Block_Cixi-Kefa-Elec-KF2EDGK-3-81-8P_C440864.html ; KF2EDGR-3.81-5P C441185 — https://lcsc.com/product-detail/Pluggable-System-Terminal-Block_Cixi-Kefa-Elec-KF2EDGR-3-81-5P_C441185.html
35. Degson 15EDGK-3.81-04P C506988 — https://lcsc.com/product-detail/Pluggable-System-Terminal-Block_DEGSON-15EDGK-3-81-04P-14-00A-H_C506988.html ; 15EDGRC-3.81-03P C507006 — https://lcsc.com/product-detail/Pluggable-System-Terminal-Block_DEGSON-15EDGRC-3-81-03P-14-00A-H_C507006.html ; IndiaMART Degson / 15EDGRC listings — https://m.indiamart.com/proddetail/15edgrc-3-81-3p-14-00a-h-pluggable-terminal-block-2853741650762.html
36. JLCPCB 4-layer rate (USD 70.6/m², 5 m² = USD 421.10, Mar-2024) — https://jlcpcb.com/blog/special-discount-on-quality-4-layers-pcbs ; JLCPCB Aug-2026 price adjustment — https://jlcpcb.com/news/jlcpcb-fr4-pcb-price-adjustment-august2026 ; IndiaMART multilayer PCB — https://m.indiamart.com/impcat/multilayer-pcb.html
37. Passives: Yageo 100 nF C14663 — https://www.lcsc.com/product-detail/_YAGEO-_C14663.html ; UNI-ROYAL 0603 1 % C25804 — https://www.lcsc.com/product-detail/Chip-Resistor-Surface-Mount_UNI-ROYAL-Uniroyal-Elec-0603WAF1002T5E_C25804.html
38. Li-ion 18650: TradeIndia — https://www.tradeindia.com/products/lithium-ion-battery-cell-18650-2600mah-9264058.html ; ThinkRobotics — https://thinkrobotics.com/collections/batteries-online/products/18650-battery-3-7v-2600mah ; Hubtronics — https://hubtronics.in/18650-2600mAh?tag=INDIA ; Makerbazar — https://makerbazar.in/products/lithium-ion-18650-rechargeable-cell-3-7v-2600mah
39. Enclosures: DigiKey India CamdenBoss CNMB/4/KIT — https://www.digikey.in/en/products/detail/camdenboss-ltd/CNMB-4-KIT/17180748 ; IndiaMART Electrocom Connectors — https://m.indiamart.com/electrocomconnectors ; Alibaba 4P DIN meter case — https://www.alibaba.com/product-introduction/4P-Din-Rail-Mounting-Meter-Case_62007665788.html ; Gaurang MD-22.5 (UL94 V-0 cover) — https://www.aajjo.com/product/modular-din-rail-enclosures-md-225-in-mumbai-gaurang-electronic-industries
40. R05 (this repo): TJA1051T/3 LCSC USD 0.349 @1k; RS-485 protection budget. R07: FX18 plug LCSC USD 2.05 @980. R11: Ethernet option costs (dropped).
