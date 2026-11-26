# R33 — Fieldbus controller (model with Ethernet): draft part-level BOM, sources

Status: v1, 2026-11-26. Pre-schematic part selection for the quote round with local Indian suppliers. BOM: `hardware/modules/fieldbus-controller/bom/draft-bom-with-ethernet.csv` (92 lines, no prices; prices go only in `bom/prices.csv`).

Method: every MPN was checked on a distributor or maker page on 2026-11-26, mostly DigiKey India (`digikey.in`, prices in INR), plus LCSC, Würth, TI, Panasonic and others where named. LCSC's product API and the ST, Nexperia and Phoenix sites were not reachable in this session. Stock and lead times are snapshots. Prices: 100-unit break where one was shown, otherwise the nearest break seen (marked); USD 1 = INR 93.9; all **ESTIMATE**. Relays and fuses: no online price (owner rule).

MCU note: the earlier standard card MCU **STM32C5A3VGT6 is not listed**. It has 1 MB flash / 256 KB RAM, which does not meet BASE-10 update 10 (model with Ethernet: ≥ 2 MB / ≥ 640 KB).

## 1. Sources per line

DK-IN = DigiKey India product or search page, `https://www.digikey.in/en/products/result?keywords=<MPN>` unless a detail URL is given.

### MCU card
| Item | Part | Source | Lifecycle / temp | India availability seen | Notes |
|---|---|---|---|---|---|
| 1 | STM32H563VIT6 (alt STM32H573VIT6) | https://www.digikey.in/en/products/detail/stmicroelectronics/STM32H563VIT6/18110514 ; https://www.digikey.in/en/products/detail/stmicroelectronics/STM32H573VIT6/21348909 ; ST community post Oct 2026 (no stock at major distributors) | Active, −40…85 °C | DK-IN 0 stock, 52 wk, 90 due May-2027; INR 660.58 @90. H573: 0 stock, INR 682.15 @100. Future Electronics USD 4.31 @90 (≈ INR 405); LCSC 145 pcs | **TBC**: supply. At DigiKey India the price is above the INR 500 MCU cap. Get a local ST distributor quote. |
| 2 | Murata XRCGB25M000F0Z00R0 (HSE 25 MHz, 6 pF) | https://www.digikey.in/en/products/detail/murata-electronics/XRCGB25M000F0Z00R0/8323978 | Active, −40…105 °C | 4,278, 17 wk, INR 21.40 @100 | Chosen over the 18 pF PHY crystal. With 18 pF and ESR 60 Ω the oscillator gm is ≈ 2.6 mA/V, above the ≈ 1.5 mA/V usual for STM32 HSE (AN2867; the H5 value was not read). **TBC**: alternate, and confirm gain margin in the schematic. HSE can use 25 MHz, and USB can run from HSI48 + CRS. |
| 3 | Abracon ABS07-32.768KHZ-7-T (LSE) | DigiKey listing 1236859 (search) | Active, −40…85 °C, 7 pF | DigiKey ≈ 457k stock | Alternate TBC |
| 4 | Winbond W25Q128JVSIQ; alts GD25Q128ESIGR, MX25L12833FM2I-10G | DK-IN search; DigiKey 5803943 | All Active, −40…85 °C | Winbond INR 569.71 @1. GD 11,201 stock, INR 245.17 @100. MX 25,173 stock, INR 466.90 @92. All three marked "constrained supply, no backorders" | 2026 NOR market is tight: quote early. |
| 5 | Microchip LAN8720AI-CP-TR (alt LAN8742AI-CZ-TR) | https://www.digikey.in/en/products/detail/microchip-technology/LAN8720AI-CP-TR/3872110 ; …/LAN8742AI-CZ-TR/4079932 | Active, −40…85 °C (Octopart: Production) | 44,891 stock, 4 wk, INR 119.31 @25. LAN8742AI: 65,947 stock, INR 177.51 @25 | LAN8742A is the Zephyr-tested PHY (R11) |
| 6 | Abracon ABM8G-25.000MHZ-18-D2Y-T (PHY) | https://www.digikey.in/en/products/detail/abracon-llc/ABM8G-25-000MHZ-18-D2Y-T/2218021 | Active, −40…85 °C, 18 pF ±20 ppm | 12,631 stock, 16 wk, INR 35.03 @100 | Alternate TBC |
| 7 | Würth 7499010121A (alts Abracon ARJM11A1-009-AB-EW2, Bel SI-46014-F) | https://www.digikey.in/en/products/detail/w%C3%BCrth-elektronik/7499010121A/1639054 ; …/abracon-llc/ARJM11A1-009-AB-EW2/7675230 | Active, −40…85 °C, tab up | 886 stock, 12 wk, INR 533.01 @100. Abracon: 3,623 stock, 18 wk, INR 244.69 @100 | The brief's 7499010211A is **0…70 °C** (DK-IN). HR911105A is 0…70 °C. HanRun HR915310AE is listed −40…85 °C at JLCPCB, but its magnetics and speed were not confirmed. **TBC**: no −40…85 °C jack found below INR 100; D-28. |
| 8 | TI TPD4E05U06DQAR (alt Semtech RClamp0524PATCT) | https://www.digikey.in/en/products/detail/texas-instruments/TPD4E05U06DQAR/3996774 | Active, −40…125 °C | 0 stock, 3,000 due 14-Dec-2026, 26 wk, INR 32.64 @100 | |
| 9 | GCT USB4105-GF-A | DK-IN search; GCT datasheet via Arrow (static6.arrow.com usb4105.pdf) | −40…85 °C | INR 76.09 @1 | Alternate HRO TYPE-C-31-M-12 (LCSC C165948, R14) changes the footprint, and its temperature rating is TBC |
| 10 | ST USBLC6-2SC6 | DK-IN search; DigiKey 1040559 | Active, −40…150 °C Tj | INR 51.36 @1. DigiKey US 226k stock, 25 wk | Pin-compatible UMW USBLC6-2SC6 is listed at DK-IN |
| 11 | Keystone 3034 | https://www.digikey.in/en/products/detail/keystone-electronics/3034/4499289 | Active | 67,562 stock, 11 wk, INR 31.29 @100 | Alt MPD BU2032SM-HD-G: Active, 201,127 stock, INR 91.43 @100 |
| 12 | Panasonic CR2032 (alts Maxell CR2032HR, Renata) | Panasonic datasheets: https://energy.panasonic.com/dam/master/pdf/en/datasheet/lithium/CR2032_Datasheet_EN.pdf (−30…85 °C) and CR2032A (−40…125 °C); Maxell CR2032HR (−40…125 °C, maxell.eu) | — | Not stocked at DK-IN; buy from a local battery distributor | **TBC**: the standard cell is rated only to −30 °C |
| 13, 61–63 | Würth 150060GS/RS/YS75000 (alts Kingbright APT1608SGC/EC/SYCK) | DK-IN search; datasheets.com (−40…85 °C) | Active | 177k / 236k / 91k stock, INR 11.78 @100 | |
| 14, 55 | Samtec TSW-125-07-G-D + SSW-125-01-G-D (alt Sullins PBC25DAAN + PPPC252LFBN-RC) | https://www.digikey.in/en/products/detail/samtec-inc/SSW-125-01-G-D/1112033 ; DK-IN PBC25DAAN, PPPC252LFBN-RC | Active. SSW: −55…125 °C, 20 µin gold, 8.51 mm insulator. PPPC: gold flash, 8.51 mm, −40…105 °C. PBC25DAAN: 10 µin gold, 2.54 mm insulator, 5.84 mm post | SSW: 86 stock (+750 factory), INR 614.34 @100. TSW: INR 501.23 @1. PPPC252: 14,745 stock, INR 179.84 @100. PBC25DAAN: 248 stock, INR 259.05 @100. IBS Electronics India lists SSW-125 (510 pcs) | **Mated board spacing 8.51 + 2.54 = 11.05 mm.** Both pairs are far above the ≈ INR 40 budget. A local gold-flash "berg strip" pair is the cost route (owner's choice). |

### Base card — power, watchdog
| Item | Part | Source | Lifecycle / temp | India availability seen | Notes |
|---|---|---|---|---|---|
| 15 | Bourns MF-LSMF185/33X-2 (alt Littelfuse 2920L185DR) | https://www.digikey.in/en/products/detail/bourns-inc/MF-LSMF185-33X-2/2514264 | Active, −40…85 °C, 1.85 A hold, 33 V | 13,165 stock, INR 51.12 @100 | No 2 A / ≥ 33 V SMD PTC was found; 1.85 A is the nearest |
| 16 | Diodes DMP6023LE-13 | DK-IN | Active, −60 V, 28 mΩ | 1,667 stock, INR 57.19 @100 | Second unit protects the field 24 V supply (IO-5). **Alternate TBC.** |
| 17 | Diodes B360B-13-F (alt onsemi MBRS360T3G, SMC) | DK-IN | Active | INR 63.72 @1. MBRS360T3G: 46,480 stock | Third diode is the USB VBUS power path (flagged) |
| 18 | TI LMR51420XDDCR (alts AP64200SP-13, SY8303AIC) | ti.com/product/LMR51420 ; datasheet ti.com/lit/ds/symlink/lmr51420.pdf ; DK-IN | Active. **Abs max VIN 38 V**; operating 4.5–36 V | XFDDCR: 0 stock (3,000 past due), 26 wk, INR 83.30 @100. XDDCR: 428 stock | Orderables: X = 500 kHz, Y = 1.1 MHz, F = FPWM. **TPS62933 (named in the brief) is a 30 V part and fails 32 V input**, so the alternates are AP64200 (3.8–40 V, SO-8EP, Active; Future, LCSC) and SY8303A (4.5–40 V, TSOT-23-8, LCSC C97054). |
| 19 | Würth 74437346100 (alt Coilcraft XAL6060-103MEC) | https://www.digikey.in/en/products/detail/w%C3%BCrth-elektronik/74437346100/2790952 | Active, −40…125 °C | 2,325 stock, INR 177.29 @100 | 10 µH per TI Table 9-1 (500 kHz, 5 V, 2 × 22 µF) |
| 20 | TI TLV75733PDYDR (alt AP7361C-33E-13) | TI datasheet ti.com/lit/ds/symlink/tlv757p.pdf (package addendum: PDYDR Active) | Active, −40…125 °C Tj | DBV: 0 stock, 26 wk, INR 32.34 @1. DYD stock not checked | **Substitution**: TLV75733PDBVR has RθJA 231 °C/W. At ≈ 0.25 A (5 V → 3.3 V, 0.43 W) that is a +98 °C rise and Tj > 125 °C at 85 °C ambient. DYD is 92.5 °C/W (JEDEC) / 60 °C/W (EVM). An SOT-223 or a 3.3 V buck is safer still. |
| 21 | TI TPS3430WDRCR | DK-IN | Active, −40…125 °C | 2,997 stock, 26 wk, INR 156.89 @100 | No pin-compatible second source (**TBC**) |
| 22 | TI SN74LVC08APWR (alt Nexperia 74LVC08APW,118) | DK-IN | Active | 88,021 / 17,126 stock | Gating: the 4 high-side EN lines are AND-ed with watchdog-OK. The relay coil 5 V is cut by P-FET item 23, driven by one N-FET (item 24). The TPS274160B has no global enable. |
| 23, 24 | AOS AO3401A / AO3400A (alts UMW, Diodes DMG2305UX-7 / DMN3404L-7) | DK-IN | Active (DMG2305UX-7: 1,334 stock, INR 15.27 @100; DMN3404L-7: 0 stock, 40 wk) | AOS INR 49.46 @1; UMW also listed | **Substitution** vs "2N7002 class": a 2N7002 has ohms of Rds(on), an error > 1 % on a 100 Ω shunt. AO3400A is < 50 mΩ at 2.5 V gate (AOS datasheet). It is 30 V, so the AI TVS must clamp below 30 V (item 29 does). |

### Base card — IO
| Item | Part | Source | Lifecycle / temp | India availability seen | Notes |
|---|---|---|---|---|---|
| 25 | TI TLV9064IPWR (alt ST TSV914IPT) | DK-IN | Active, −40…125 °C | 37,861 stock, 26 wk, INR 103.60 @100 | |
| 26 | TI LM4040AIM3X-2.5/NOPB (alts ADI ADR5041BRTZ-REEL7, TI LM4040A25IDBZR) | DK-IN | Active, ±0.1 %, −40…85 °C | 16,501 stock, 26 wk, INR 164.89 @100. ADR5041B: 818 stock | No Diodes or ST 0.1 % LM4040 found; ADI ADR5041B (±0.1 %, pin-compatible) is the true second source |
| 27 | Vishay TNPW1206100RBEEA | DK-IN | Active, 0.1 %, 25 ppm, 0.52 W | 23,104 stock, INR 30.91 @100 | Shunt 100 Ω gives 20 mA → 2.0 V with a 2.5 V reference |
| 28 | Bourns MF-USMF005-2 | DK-IN | Active, 50 mA hold, 30 V, −40…85 °C | 126,354 stock, INR 23.20 @100 | **TBC** (alternate; miswire check) |
| 29 | Littelfuse SMF12CA (alts Diotec, Eaton) | DK-IN | Active | Several makers listed | |
| 30 | Nexperia BAT54S,215 | DK-IN | Active | INR 13.32 | |
| 31 | Lite-On LTV-217-TP1-B-G (alt Everlight EL3H7(B)(TA)-VG) | DK-IN; DigiKey 2675688 (EL3H7) | Active, −55…110 °C, CTR 130–260 % | 4,460 stock (LTV-217-G 41,386) | B rank for a defined Type 3 threshold |
| 32 | Panasonic ERJ-P08F3901V (alt Vishay CRCW12063K90FKEAHP) | DK-IN | Active, pulse withstanding, 0.66 W | 4,877 / 6,445 stock | |
| 33 | Diodes 1N4148W-7-F | DK-IN | Active | INR 17.12 @1 | |
| 34 | Hongfa HF115F/005-1ZS3 (alts G2RL-1 DC5, JW1FSN-DC5V, G5Q-14-EU DC5) | LCSC C9225 (16 A 250 VAC, 400 mW, **5 kV**, −40…85 °C); Panasonic AJW4219 page (10 A, 5,000 Vrms, **−40…+60 °C**); DK-IN G2RL-1 DC5, G5Q-14-EU DC5 (Active, 10 A, −40…85 °C, 4,519 stock) | Active | Owner local quote | Omron relays now sold as **Aratas (formerly Omron Components)**. JW1FSN is only rated to 60 °C ambient. |
| 35 | TI TPL7407LDR (alt ST ULN2003D1013TR) | DK-IN | Active, −40…125 °C | 0 stock, 2,500 due 21-Jan-2027, 26 wk | **Substitution**: DK-IN lists TI ULN2803ADWR/ADW as **Obsolete**. TI's page says not in production; its replacement ULN2803CDWR is SOIC-20 and not pin-compatible. Micros.com.pl (2026-03-26): TI and Toshiba dropped SOP-18; only Chinese makers continue. TPL7407L has 7 MOSFET channels (6 needed) and a low output drop, which helps the 5 V coils when the 5 V rail sags at low input. |
| 36, 37 | Würth 890324023023 X2 0.1 µF 275 VAC + Vishay PR01000101000JR500 | DigiKey 5039008; DK-IN PR01 (Active, 26,133 stock) | Active | | **Substitution** vs one-part RC: KEMET PMR209 is marked **Not for New Design** (and 250 VAC). CDE 104M06QC100 is INR 1,113 @100. Fit per load. |
| 38 | Littelfuse 0215010.MXP (alt Schurter 0001.2514) | littelfuse.com 215 series; DigiKey 777449; Schurter fuse kit page | Active, T10A 250 V, 1,500 A breaking | Owner local quote | |
| 39 | Würth 696309001002 (alts 696310001002, Schurter 0031.3551 FAB) | DK-IN; https://www.we-online.com/catalog/en/FSH_THT_PCB_TURN_AND_LOCK_COVER_6963XX001002_2 | Active, lifetime > 10 years; 10 A VDE / 20 A UL, 250 VAC; **−30…+120 °C** | 13,414 stock (owner local quote) | Vertical PCB holder, turn-and-lock cover, shock-safe. Front access depends on the housing (D-37). Schurter FAB: Rapid lists it as discontinued; DK-IN shows Active, 498 stock. |
| 40 | TI TPS274160BRLHR | DK-IN; datasheet mirror e2e.ti.com TPS274160.PDF | Active, 5–36 V, abs max 48 V (400 ms load dump; product page says 50 V); 1.35 A current limit per DK-IN | 2,906 stock, 26 wk, INR 232.22 @100 | Package is WQFN-28 4 × 5 mm only. Reverse polarity per TI: GND network (diode ∥ 1 kΩ) or blocking; this BOM blocks with P-FET item 16. GND-network parts are not added. |
| 41, 42 | SMBJ33A (Littelfuse, alt Vishay SMBJ33A-E3/52); Vishay SMBJ33CA-E3/52 | DK-IN | Active; Vrwm 33 V, Vbr 36.7 V, Vc 53.3 V @ 11.3 A | Vishay 8,890 / 13,142 stock; INR 19.08 / 20.25 @100. Littelfuse SMBJ33A: 0 stock at DK-IN | **Clamp flag**: 53.3 V is above the LMR51420 abs max (38 V) and the TPS274160B abs max (48 V). See open points. |

### Base card — comms, bus, connectors, passives
| Item | Part | Source | Lifecycle / temp | India availability seen | Notes |
|---|---|---|---|---|---|
| 43 | Chipanalog CA-IS2092W (alt TI ISOW1412DFMR) | LCSC C5121950 | −40…125 °C, **2.5 kVrms**, 500 kbit/s, 3–5.5 V | LCSC (PRD FB-1: USD 1.89 @100). ISOW1412: DK-IN 0 stock, INR 714 @250 | Older notes said 5 kV; it is 2.5 kVrms |
| 44 | Semtech SM712.TCT (alt Littelfuse SM712-02HTG) | DK-IN | Active, −55…125 °C | 25,955 stock, INR 117.96 @100 | |
| 45 | Bourns MF-USMF010-2 | DK-IN | Active, 100 mA hold, 30 V | 130,410 stock | Added for IO-5 (24 V on A/B). **Alternate TBC.** |
| 46, 49 | CTS 219-3MSTR / 219-2MSTR (alts Würth 418121270803 / 802) | DK-IN | Würth: Active, −40…85 °C | Würth 803: 1,080 stock, INR 135.63 @100; 802: 0 stock | |
| 47 | Chipanalog CA-IS2062A (alts CA-IS2062W, TI ISOW1044DFMR) | LCSC C22438481 | −40…125 °C, 2.5 kVrms, CAN FD 5 Mbit/s, **VDDP 5 V only** | LCSC (FB-1: USD 1.16 @100) | **TBC**: the package is **LGA-16 4.7 × 5.2 mm**. CA-IS2062W is SOIC-16W but classic CAN only (FB-1 allows it). Check that the bus-pin fault rating is ≥ ±30 V; if not, add PTCs. |
| 48 | TI ESD2CANFD24DBZR (alt Nexperia PESD2CANFD24UT-QR) | DK-IN | Active | Nexperia 2,544 stock | |
| 50 | Molex 43650-0400 / 0436500400 (alt Würth 66200411022) | DK-IN detail WM1862-ND; DK-IN 66200411022 | Active; board lock; tin. Würth: −40…105 °C | 12,436 stock, INR 95.49 @10. Würth: 110 stock, INR 93.21 @1 | **TBC** (D-34). Single row per brief; R23 picked dual-row 43045-0400. Jumper housing changes to 43645-0400. |
| 51 | TI THVD1420DR (alt ST ST3485EBDR) | DK-IN | Active | INR 129.35 / 149.32 @1 | |
| 52, 53 | Molex 43045-0800 (alt Würth 662008231722 SMT) + 2 × TPD4E05U06DQAR | DK-IN | Active | Molex: 0 stock at DK-IN (1,440 past due; marketplace 116k) | **TBC** (D-29). Micro-Fit 2 × 4: positive latch, rated to 105 °C, same crimp family as the bus; the 8-pin layout cannot mate with the 4-pin bus. The cable to the 4G card is not in this BOM. |
| 54 | Samtec SSW-104-01-G-D (alts Sullins PPPC042LFBN-RC, CJT A2541HWV-2x4P) | DK-IN; R23 (LCSC C239344) | Active | Sullins 51,052 stock, INR 46.08 @100 | Battery-board standoffs belong to the battery board |
| 56–59 | Phoenix 1727010 / 1727023 / 1727052 / 1727065 (MKDS 1/ x-3,81) (alts Kefa KF128L-3.81-2P/3P) | DK-IN; RS/Rapid listings; Phoenix 2025 datasheet via search; R24 (LCSC C474932/3) | 1727065 Active (225 stock). 200 V IEC / 300 V UL, 13.5 A (2025 sheet: 17.5 A) | INR 106.52 / 160.74 / 323.37 @1; 309.39 @10 | A Phoenix PCN (CAA230054) references these items; it could not be read (403). Check before ordering. Poles: 2 + 3 + 3 + 6 + 6 + 7 = 27. |
| 60 | Phoenix 1715734 (MKDS 1,5/ 3-5,08) (alt Same Sky TB007-508-03BE) | DK-IN detail 277-1264-ND | Active, 300 V / 15 A UL. TB007: 16 A / 300 V, −40…105 °C | 9,259 stock, INR 133.44 @10 | 18 poles × 5.08 = 91.4 mm, wider than the housing (fit study) |
| 64–80 | Passive groups | DK-IN: RC0603FR-0710KL (2.3 M stock), RT0603BRD0710KL (0 stock, 23 wk), RC1206FR-07120RL, CC0603KRX7R9BB104 (2.58 M), CC0603JRNPO9BN270, CC1206KKX7RDBB102 (1 nF 2 kV, 46,768), CL21B106KAYQNNE / CL31B106KBHNNNE / CL10B104KB8NNNC / CL10B105KA8NNNC (Active, **0 stock, 61 wk**, "market conditions"), EEE-FK1H470P (6,739, −55…105 °C), BLM18PG221SN1D (180k), MMSZ5242BT1G | Active | Samsung MLCCs are short at DigiKey; LCSC and local stock typical | Counts are ESTIMATEs. Supporting parts are flagged in §4. |
| 81–92 | PCBs, housing, labels, fixings, jumper, packaging | CamdenBoss CNMB/5/KIT: DK-IN (Active, PC, UL94 V-0, 88 × 90 × 58 mm, 65 stock, INR 1,128 @10); element14 marks it "no longer stocked". Würth 970110321: DK-IN (Active, 23,206 stock, INR 25.39 @100). Molex 0436450400: DK-IN (57,307 stock). 43030-0001 per R23. | — | — | Nylon Würth screws (97790603111) are unsuitable for 10 g, so steel A2 ISO 7045 + DIN 6798 A were chosen. Housing and PCB size: **per D-37 fit study, TBC**. |

## 2. Critical high-value items

Prices are ESTIMATES from distributor breaks seen on 2026-11-26. Most are DigiKey India list prices, many at 1–10 pcs (see the basis column), so they sit well above LCSC and direct-quote levels. Use them for ranking, not costing.

| Item | Part number | Qty/module | Est. unit INR (100 units) | Est. ext. INR/module | Share of priced subtotal | Price basis | Why critical |
|---|---|---|---|---|---|---|---|
| 60 | 1715734 (x6) | 6 | 133.44 | 800.64 | 8.1 % | DigiKey IN @10 | High value; Safety (230 VAC terminals) |
| 1 | STM32H563VIT6 | 1 | 660.58 | 660.58 | 6.6 % | DigiKey IN @90 | High value; Long lead (DigiKey IN 0 stock, 52 wk; ST community Oct-2026: no stock at major distributors) |
| 58 | 1727052 (x2) | 2 | 323.37 | 646.74 | 6.5 % | DigiKey IN @1 | High value |
| 55 | SSW-125-01-G-D | 1 | 614.34 | 614.34 | 6.2 % | DigiKey IN @100 | High value; Open decision (card connector cost vs INR 40 budget) |
| 7 | 7499010121A | 1 | 533.01 | 533.01 | 5.4 % | DigiKey IN @100 | High value; Long lead (12 wk, 886 stock); D-28 temperature |
| 14 | TSW-125-07-G-D | 1 | 501.23 | 501.23 | 5.0 % | DigiKey IN @1 (no 100 break seen) | High value |
| 57 | 1727023 (x2) | 2 | 160.74 | 321.48 | 3.2 % | DigiKey IN @1 | High value |
| 59 | 1727065 | 1 | 309.39 | 309.39 | 3.1 % | DigiKey IN @10 | High value |
| 31 | LTV-217-TP1-B-G (x6) | 6 | 47.56 | 285.36 | 2.9 % | DigiKey IN @1 | Safety (DI isolation) |
| 61 | 150060GS75000 (x22) | 22 | 11.78 | 259.16 | 2.6 % | DigiKey IN @100 | High value (count) |
| 24 | AO3400A (x5) | 5 | 49.46 | 247.30 | 2.5 % | DigiKey IN @1 (AOS) | - |
| 4 | W25Q128JVSIQ | 1 | 245.17 | 245.17 | 2.5 % | alt GD25Q128ESIGR DigiKey IN @100 (Winbond INR 569.71 @1) | High value; Long lead (NOR supply constrained, DigiKey no backorders) |
| 44 | SM712.TCT (x2) | 2 | 117.96 | 235.92 | 2.4 % | DigiKey IN @100 | Safety (surge clamp) |
| 40 | TPS274160BRLHR | 1 | 232.22 | 232.22 | 2.3 % | DigiKey IN @100 | High value; Single source (TI only; A-variant same vendor); Long lead (26 wk) |
| 29 | SMF12CA (x4) | 4 | 58.02 | 232.08 | 2.3 % | DigiKey IN @1 (Littelfuse) | Safety (AI clamp) |
| 17 | B360B-13-F (x3) | 3 | 63.72 | 191.16 | 1.9 % | DigiKey IN @1 | - |
| 50 | 43650-0400 (x2) | 2 | 95.49 | 190.98 | 1.9 % | DigiKey IN @10 | Open decision (D-34) |
| 52 | 43045-0800 | 1 | 184.51 | 184.51 | 1.9 % | DigiKey IN @1 | Open decision (D-29); Long lead (DigiKey IN 0 stock) |
| 43 | CA-IS2092W | 1 | 177.47 | 177.47 | 1.8 % | LCSC USD 1.89 @100 (PRD FB-1, 2026-11-22) | Safety (isolation 2.5 kVrms); Single source (Chipanalog) |
| 19 | 74437346100 | 1 | 177.29 | 177.29 | 1.8 % | DigiKey IN @100 | - |
| 26 | LM4040AIM3X-2.5/NOPB | 1 | 164.89 | 164.89 | 1.7 % | DigiKey IN @100 | Long lead (26 wk) |
| 21 | TPS3430WDRCR | 1 | 156.89 | 156.89 | 1.6 % | DigiKey IN @100 | Safety (output safe state); Single source; Long lead (26 wk) |
| 37 | PR01000101000JR500 (x6) | 6 | 25.68 | 154.08 | 1.6 % | DigiKey IN @1 | - |
| 54 | SSW-104-01-G-D | 1 | 148.37 | 148.37 | 1.5 % | DigiKey IN @1 | - |
| 51 | THVD1420DR | 1 | 129.35 | 129.35 | 1.3 % | DigiKey IN @1 | - |
| 27 | TNPW1206100RBEEA (x4) | 4 | 30.91 | 123.64 | 1.2 % | DigiKey IN @100 | - |
| 5 | LAN8720AI-CP-TR | 1 | 119.31 | 119.31 | 1.2 % | DigiKey IN @25 | - |
| 16 | DMP6023LE-13 (x2) | 2 | 57.19 | 114.38 | 1.2 % | DigiKey IN @100 | Safety (reverse polarity) |
| 47 | CA-IS2062A | 1 | 108.92 | 108.92 | 1.1 % | LCSC USD 1.16 @100 (PRD FB-1) | Safety (isolation 2.5 kVrms); Single source; LGA package |
| 56 | 1727010 | 1 | 106.52 | 106.52 | 1.1 % | DigiKey IN @1 | - |
| 25 | TLV9064IPWR | 1 | 103.60 | 103.60 | 1.0 % | DigiKey IN @100 | Long lead (26 wk) |
| 33 | 1N4148W-7-F (x6) | 6 | 17.12 | 102.72 | 1.0 % | DigiKey IN @1 | - |
| 87 | 970110321 (x4) | 4 | 25.39 | 101.56 | 1.0 % | DigiKey IN @100 | - |
| 28 | MF-USMF005-2 (x4) | 4 | 23.20 | 92.80 | 0.9 % | DigiKey IN @100 | Safety (AI miswire) |
| 35 | TPL7407LDR | 1 | 87.50 | 87.50 | 0.9 % | DigiKey IN @1 | Long lead (DigiKey IN 0 stock, 26 wk) |
| 18 | LMR51420XDDCR | 1 | 83.30 | 83.30 | 0.8 % | DigiKey IN @100 (XFDDCR break; XDDCR INR 141.71 @1) | Long lead (26 wk); Safety (abs max 38 V below TVS clamp) |
| 46 | 219-3MSTR | 1 | 81.79 | 81.79 | 0.8 % | DigiKey IN @1 | - |
| 42 | SMBJ33CA-E3/52 (x4) | 4 | 20.25 | 81.00 | 0.8 % | DigiKey IN @100 | Safety (surge clamp) |
| 9 | USB4105-GF-A | 1 | 76.09 | 76.09 | 0.8 % | DigiKey IN @1 | - |
| 49 | 219-2MSTR | 1 | 71.33 | 71.33 | 0.7 % | DigiKey IN @1 | - |
| 32 | ERJ-P08F3901V (x6) | 6 | 11.13 | 66.78 | 0.7 % | DigiKey IN @10 | - |
| 53 | TPD4E05U06DQAR (x2, base) | 2 | 32.64 | 65.28 | 0.7 % | DigiKey IN @100 | Long lead (0 stock, 26 wk); Open decision (D-29) |
| 48 | ESD2CANFD24DBZR | 1 | 58.97 | 58.97 | 0.6 % | DigiKey IN @1 | - |
| 41 | SMBJ33A (x3) | 3 | 19.08 | 57.24 | 0.6 % | Vishay DigiKey IN @100 | Safety (surge clamp) |
| 30 | BAT54S,215 (x4) | 4 | 13.32 | 53.28 | 0.5 % | DigiKey IN @1 | - |
| 10 | USBLC6-2SC6 | 1 | 51.36 | 51.36 | 0.5 % | DigiKey IN @1 | - |
| 15 | MF-LSMF185/33X-2 | 1 | 51.12 | 51.12 | 0.5 % | DigiKey IN @100 | Safety (input fuse) |
| 23 | AO3401A | 1 | 49.46 | 49.46 | 0.5 % | DigiKey IN @1 (AOS) | Safety (relay safe state) |
| 22 | SN74LVC08APWR | 1 | 38.04 | 38.04 | 0.4 % | DigiKey IN @1 | Safety (output safe state) |
| 6 | ABM8G-25.000MHZ-18-D2Y-T | 1 | 35.03 | 35.03 | 0.4 % | DigiKey IN @100 | - |
| 8 | TPD4E05U06DQAR (MCU) | 1 | 32.64 | 32.64 | 0.3 % | DigiKey IN @100 | Long lead (0 stock, 26 wk) |
| 20 | TLV75733PDYDR | 1 | 32.34 | 32.34 | 0.3 % | DigiKey IN @1 (DBV price; DYD not seen) | - |
| 11 | 3034 | 1 | 31.29 | 31.29 | 0.3 % | DigiKey IN @100 | - |
| 2 | XRCGB25M000F0Z00R0 | 1 | 21.40 | 21.40 | 0.2 % | DigiKey IN @100 | - |
| 13 | 150060GS75000 (MCU) | 1 | 11.78 | 11.78 | 0.1 % | DigiKey IN @100 | - |
| 62 | 150060RS75000 | 1 | 11.78 | 11.78 | 0.1 % | DigiKey IN @100 | - |
| 63 | 150060YS75000 | 1 | 11.78 | 11.78 | 0.1 % | DigiKey IN @100 | - |
| 34 | HF115F/005-1ZS3 (x6) | 6 | not priced | - | - | - | Owner local quote; Safety (5 kV relay) |
| 38 | 0215010.MXP (x6) | 6 | not priced | - | - | - | Owner local quote; Safety |
| 39 | 696309001002 (x6) | 6 | not priced | - | - | - | Owner local quote; Safety; Open decision (D-37 front access) |
| 83 | CNMB/5/KIT | 1 | not priced | - | - | - | High value (DigiKey IN INR 1,128 @10, not used); Open decision (D-37) |
| 81 | custom PCB base card | 1 | not priced | - | - | - | High value; Open decision (D-37 size) |
| 82 | custom PCB MCU card | 1 | not priced | - | - | - | Open decision (D-37) |
| 90 | bus bridge jumper | 1 | not priced | - | - | - | Open decision (D-34) |
| 12 | CR2032 | 1 | not priced | - | - | - | Safety (-30 deg C rating, TBC) |
| 36 | 890324023023 (x6) | 6 | not priced | - | - | - | Safety (X2, fit per load) |
| 45 | MF-USMF010-2 (x2) | 2 | not priced | - | - | - | Safety (RS-485 miswire) |
| 3 | ABS07-32.768KHZ-7-T | 1 | not priced | - | - | - | - |

**Priced subtotal (ESTIMATE): INR 9,934 per module** for the 57 priced lines above.

**This is not a BOM total.** These lines are not priced:
- relays (34), fuses (38) and fuse holders (39): owner local quote;
- custom PCBs (81, 82);
- enclosure (83);
- all passive groups (64–80);
- crystal (3), CR2032 (12), X2 capacitors (36), PTC (45);
- labels, fixings except standoffs, jumper and packaging (84–92).

The INR ≈ 9,900 subtotal is driven by small-quantity DigiKey India pricing. Examples: terminals INR 2,400 at 1–10 pcs against R24's ≈ INR 5–6 per pole; the card connector pair INR 1,115. It must not be compared with the INR 2,000 limit until local quotes arrive. Even so, the MCU, RJ45, card connectors and Phoenix terminals are clearly far above the architecture estimate lines (MCU ≈ 300, RJ45 ≈ 200 incl. PHY, connector ≈ 40).

## 3. Substitutions versus the brief
| Brief | BOM | Why |
|---|---|---|
| TI ULN2803ADWR | TI TPL7407LDR (item 35) | ULN2803A is obsolete at TI; DigiKey India lists it Obsolete; the SOIC-18 replacement is not pin-compatible |
| TLV75733PDBVR | TLV75733PDYDR (item 20) | DBV 231 °C/W would exceed Tj at 85 °C ambient |
| 2N7002 / BSS138 mode FET | AO3400A (item 24) | Rds(on) error on a 100 Ω shunt |
| 100 Ω + 100 nF X2 as one part | X2 capacitor + PR01 resistor (36, 37) | KEMET PMR209 is NRND |
| Würth 7499010211A | 7499010121A (item 7) | 0211A is rated 0…70 °C only |
| TPS62933 as alternate buck | AP64200 / SY8303A | TPS62933 is 30 V maximum |
| One 25 MHz crystal for MCU + PHY | Two crystals (2, 6) | STM32 HSE gain margin |

## 4. Parts added beyond the brief (flagged, owner to accept)
- A 3rd Schottky (item 17) for USB VBUS as a power input.
- A 2nd DMP6023LE-13, a 2nd zener and a 2nd 47 µF (items 16, 71, 73) on the field 24 V supply of the high-side outputs (IO-5).
- 2 PTCs on RS-485 A/B (item 45), for IO-5 24 V miswire.
- AO3401A + AO3400A as the relay-supply gate (items 23, 24).
- 1 nF 2 kV Bob-Smith capacitor (item 79), only if the jack lacks it.
- Second ESD array for the 4G link (item 53).
- Static-shielding bag (item 92).

## 5. Open points for the owner
1. **MCU supply and price**: STM32H563VIT6 has 0 stock and a 52-week lead time at DigiKey India, at INR 660 @90. That is over the INR 500 cap. Get an ST distributor quote; the owner already holds 5 pieces for prototypes.
2. **RJ45 at −40…85 °C**: Würth INR 533, Abracon INR 245 @100. Nothing found under INR 100. Decide D-28, or ask HanRun for an industrial MagJack (HR915310AE?).
3. **Input surge**: the SMBJ33A clamp (53 V) exceeds the LMR51420 abs max (38 V), and on the field supply it exceeds the TPS274160B abs max (48 V). Options: a 60 V buck, an OVP/eFuse front end, or SMBJ30A on the 24 V field supply. TPS62933 cannot be the alternate (30 V).
4. **3.3 V LDO heat**: estimate the 3.3 V load. Above ≈ 0.25 A, use an SOT-223 LDO or a 3.3 V buck. Power the CA-IS isolated parts from 5 V.
5. **Card connector**: 2 × 25 gives 50 pins against ≈ 55–60 signals plus power/ground for this model (BASE-11 counted ≈ 90 before savings). This needs a bigger connector, an I²C expander, or a trimmed pin map; settle it in the design spec. Board spacing 11.05 mm is confirmed for SSW + TSW/PBC pairs. Samtec / Sullins cost INR 440–1,115 per pair, so a local gold berg-strip quote is needed.
6. **CA-IS2062A is LGA-16**: confirm the CM can place and inspect it. Otherwise use CA-IS2062W (SOIC, classic CAN only; FB-1 allows it). CA-IS2092W and CA-IS2062A are rated 2.5 kVrms, not 5 kV.
7. **AI 24 V miswire in 4–20 mA mode**: the shunt sees ≈ 1.8 W until the PTC trips. Verify by test, or add a ≈ 25 mA current limiter per channel (not added). Two-wire transmitters need loop power from the user's 24 V; no loop-supply terminal is provided.
8. **DI Type 3 OFF threshold**: needs an LED bypass resistor or zener per channel. Resistors are counted in the passives; a zener is not added.
9. **5 V input**: the buck is in dropout at 5 V in. Check that the relays (5 V coils, ≈ 75 % must-operate) still pull in. USB-C power (500 mA default) cannot run the relays.
10. **Mechanics (D-37)**: 18 relay poles × 5.08 mm = 91.4 mm and 27 SELV poles × 3.81 mm = 103 mm. Neither fits one tier of a 90 mm housing. Fuse-holder caps (rated −30 °C) and DIP switches must reach the front. CNMB/5/KIT is about INR 1,100 and may be end-of-life; quote Indian makers.
11. **Connectors (D-34 / D-29)**: single-row 43650-0400 (brief) vs dual-row 43045-0400 (R23). The 4G link on Micro-Fit 2 × 4 is a proposal. The bus end cap (empty housing, R23) is not added.
12. **Coin cell**: the standard CR2032 is rated −30 °C. Maxell CR2032HR / Panasonic CR2032A cover −40 °C but are not stocked at DigiKey India.
13. **Long-lead / short items**: Samsung MLCCs (61 weeks), TPL7407L, TPD4E05U06, LMR51420, TPS3430, TLV757P (26 weeks), NOR flash (no backorders). Quote these early and allow approved equivalents for passives.
14. **Relays**: the Panasonic JW1FSN alternate is rated −40…60 °C only. Omron relays are now under the Aratas brand.
15. **Phoenix PCN CAA230054** names the MKDS 1/x-3,81 items; read it before ordering.
