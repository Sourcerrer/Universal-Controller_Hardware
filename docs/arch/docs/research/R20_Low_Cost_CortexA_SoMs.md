# R20 — STM32MP13 Chip-down vs Low-cost SoMs for the Tier-2 Router (with a brief cross-vendor check)

Date: 2026-11-15. FX: 1 USD = INR 93.9. Status: COMPLETE WITH GAPS.

Markers:
- **UNVERIFIED**: not confirmed by a primary source.
- **E**: an engineering estimate.
- **INFERRED**: deduced from other facts.

Numbered sources are in section 11. Internal reports are cited as [R09], [R16], [R18], [R19].

Ex-works formula (owner): BOM × 1.5, plus INR 750 royalty, then × 1.3 (30 % profit).

Scope:
- The owner's decisions during this study set the scope:
  - The Tier-2 processor is the **ST STM32MP13 family**.
  - The clock must be **1–1.2 GHz**.
  - The dual-core preference was dropped.
- So the main question is **STM32MP13 chip-down vs an STM32MP13 SoM** (sections 2–6).
- Other vendors are kept to one brief table (section 7) and the Qualcomm answer (section 8).
- SoM prices are module-only (Linux processor, RAM and flash). The INR 2,500 budget is about USD 26.6.

---

## 1. Summary and recommendation

1. **Which STM32MP13 parts fit (ST nomenclature, confirmed [1]).**

   | Suffix | Clock | Security |
   |---|---|---|
   | A | 650 MHz | basic |
   | C | 650 MHz | secure boot + crypto |
   | D | 1 GHz | basic |
   | F | 1 GHz | secure boot + crypto |

   - 1 GHz parts exist only with temperature code **7** (Tj −40 to +105 °C) [1].
   - **The owner's rule (1 GHz plus secure boot) therefore means an "F…7" part.**
   - MP131 has one Ethernet MAC; MP133 and MP135 have two [9]. **MP131F is therefore out.**
2. **Correction to R18 and R19.**
   - R18 specified "STM32MP133CAF3, LFBGA289 0.8 mm". In ST's order codes:
     - **AE** = LFBGA289 14 × 14 mm, **0.8 mm** pitch;
     - **AF** = TFBGA320 11 × 11 mm, **0.5 mm** pitch;
     - **AG** = TFBGA289 9 × 9 mm, 0.5 mm pitch [2][3].
   - So the **CAF3 is a 0.5 mm-pitch, 650 MHz part**.
   - R18's 6-layer, non-HDI board plan holds only for an **xAE** part.
3. **Cheapest 1 GHz secure part with two MACs in the 0.8 mm package: STM32MP135FAE7.**
   - DigiKey: **USD 7.59 at 714 units, 614 in stock** (30-week factory lead time) [6]. ST eStore: USD 7.40 (10k tier), in stock [3].
   - It undercuts the STM32MP133FAE7 in distribution today:
     - DigiKey USD 8.49 at 714, not stocked, 30 weeks [5];
     - ST eStore USD 7.94 at 500, out of stock [2];
     - Avnet about USD 5.95 at 714 with a 105-week lead time, UNVERIFIED [8].
   - The MP135 adds LCD and camera blocks, which the router does not use. Keep the MP133FAE7 as a pin-compatible alternative and quote both. INFERRED: same package and ball-out family; confirm in the datasheet.
4. **No verified STM32MP13 SoM meets 1 GHz + secure boot + two Ethernet ports + −40 °C at or below INR 2,500.**
   - Under budget, but each fails at least one rule:
     - **Ka-Ro QSMP-1351**: EUR 23 starting, about INR 2,500 (FX UNVERIFIED). It uses the 650 MHz MP135**C**, brings out one Ethernet port and is rated −25 °C [11].
     - **MYiR MYC-YF135** standard: about USD 19 in volume, about INR 1,784. It uses the MP135**D**, which has **no secure boot** [10].
     - **Ebyte ECK10-135A5M5M-I**: INR 2,319 ex-GST at Hubtronics. It uses a 650 MHz **A** part with no secure boot [16].
   - Meet the rules, but cost more:
     - **MYiR MYC-YF135F**: MP135FAF7, 512 MB DDR3L, 4 GB eMMC, sample USD 46 = INR 4,319 [10]. Volume price UNVERIFIED; E: USD 28–32 = INR 2,630–3,000.
     - **DH electronics DHCOR STM32MP13**: MP135F, mainline Linux, dual GbE; price on quote only [12].
     - **iWave OSM**: Bangalore-made, MP135F; USD 62.13 at 1 [14].
     - **Engicam MicroGEA**: price not published [13].
5. **Chip-down or SoM?**
   - **Chip-down with the STM32MP135FAE7 (0.8 mm LFBGA, 16-bit DDR3L, 6 layers) for production at both 1k and 5k per year.**
   - A SoM, preferably the MYiR MYC-YF135F (same MP135F and DDR3L, so the same Yocto BSP), for EVT, pilot and the first ≤ 300–500 units.
   - The SoM premium is about **INR 1,000 per unit of BOM (E)**, about INR 1,970 at ex-works.
   - Chip-down adds about **INR 10–15 lakh of one-time engineering (E)**.
   - Break-even is about **1,000–1,500 units**: roughly one year at 1k per year, or one quarter at 5k per year (section 5).
6. **Updated Tier-2 BOM (chip-down MP135FAE7 + STM32H533 companion): INR 5,858, ex-works INR 12,398.**
   - That is +INR 228 BOM and +INR 444 ex-works vs R19's INR 5,630 / 11,954, caused by the 1 GHz secure part.
   - SoM build (MYiR YF135F at an estimated volume price): BOM about INR 6,910, **ex-works about INR 14,450**. At the sample price it is about INR 17,400.
   - Competitors [R18]:
     - RUT200: INR 7,569–8,500 (dealer), INR 13,700 (retail);
     - USR-G806w: INR 8,008 ex-GST.
   - The chip-down router stays below RUT200 retail. The SoM build does not.
7. **The owner's Qualcomm question (section 8, short answer).**
   - Qualcomm's router SoCs (QCA953x, IPQ40xx/50xx/53xx) are in many routers. Teltonika's RUTX11 uses IPQ4018 and TRB245 uses QCA9531 [R16].
   - But datasheets, SDKs and secure-boot signing tools are behind Qualcomm's licensed-customer portals [R19 §2].
   - Volume terms are negotiated, and small OEMs in practice buy **modules** from Compex or 8devices (USD 60 to 250+) [28].
   - None of those beats an STM32MP13 for open software, secure boot with public tools, and longevity.

---

## 2. STM32MP13 chip-down: parts, prices and packages

Prices are USD, as listed; "@N" is the quantity tier. INR is at 93.9.

| Order code | Clock / security | Ethernet MACs | Package / pitch | Price | INR | Stock / lead time | Src |
|---|---|---|---|---|---|---|---|
| **STM32MP135FAE7** | 1 GHz / **secure** | **2** | **LFBGA289 14 × 14, 0.8 mm** | DigiKey **7.594 @714** (12.27 @1, 8.24 @100); ST eStore 7.40 @10k | **713** (695) | DigiKey **614 in stock**, 30 wk; eStore in stock | [3][6] |
| STM32MP133FAE7 | 1 GHz / secure | 2 | LFBGA289 0.8 mm | DigiKey 8.489 @714 (UK GBP 6.34); eStore 7.94 @500; Avnet about 5.95 @714 (UNVERIFIED) | 797 / 746 / 559 | DigiKey not stocked, 30 wk; eStore out of stock; Avnet 105 wk | [2][5][8] |
| STM32MP131FAE7 | 1 GHz / secure | **1** | LFBGA289 0.8 mm | DigiKey 7.909 @714 | 743 | not stocked, 30 wk | [7] |
| STM32MP133FAF7 | 1 GHz / secure | 2 | TFBGA320 11 × 11, **0.5 mm** | eStore 5.61 @10k | 527 | in stock | [2] |
| STM32MP133FAG7 | 1 GHz / secure | 2 | TFBGA289 9 × 9, 0.5 mm | eStore 6.15 @500 | 577 | in stock | [2] |
| STM32MP135FAF7 / FAG7 | 1 GHz / secure | 2 | 0.5 mm | eStore 7.19 / 6.61 @500 | 675 / 621 | in stock | [3] |
| STM32MP133DAE7 | 1 GHz / **basic, no secure boot** | 2 | LFBGA289 0.8 mm | eStore 6.46 @500 | 607 | in stock | [2] |
| STM32MP133CAF3 (R18's part) | **650 MHz** / secure | 2 | **TFBGA320 0.5 mm** | eStore 6.65 @500; Avnet 5.16 @2k [R18] | 624 / 485 | eStore out of stock | [2][R18] |
| STM32MP135CAE3 | 650 MHz / secure | 2 | LFBGA289 0.8 mm | eStore 7.11 @500 | 668 | in stock | [3] |

Notes:
- The 0.5 mm parts are about USD 1–2 cheaper. They need finer design rules (via-in-pad or HDI escape under a 0.5 mm BGA, E) and harder assembly and inspection in India. The 0.8 mm **AE** package is the one R18's 6-layer plan assumed.
- 1 GHz is guaranteed only to Tj +105 °C, while 650 MHz parts go to 125 °C [1].
  - At +75 °C ambient inside an aluminium case, the MP13's sub-1 W power (E) leaves margin, but a thermal check is needed.
  - Fallback: run an F part at 650 MHz in firmware if a hot site needs it. The F part supports both clocks (INFERRED).
- Secure boot on F/C parts: ROM authentication of the FSBL, then TF-A, OP-TEE, U-Boot and a signed FIT [R18].
  - ST's key-generation, signing and programming tools (STM32CubeProgrammer, KeyGen, SigningTool) are public downloads [R18].
  - Longevity: ST's 10-year rolling programme [R09].

---

## 3. STM32MP13 SoMs

Ethernet = ports or MAC interfaces brought out to the carrier. "Sample" = vendor's 1–2-piece price.

| SoM | MP13 part (clock / security) | RAM / flash | Ethernet out | Temp. | Mounting | BSP | Longevity | India availability | Price @1 | Price @1k | Fits rules? | Src |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **MYiR MYC-YF135F** | **MP135FAF7 (1 GHz / secure)** | 512 MB DDR3L / 4 GB eMMC | 2 × RGMII (PHYs on carrier) | −40..85 °C | 39 × 37 mm, 10-layer, stamp-hole (castellated) | Yocto (OpenSTLinux), Linux 6.6.78 | "long-term availability" (no years) | Direct from MYiR (export); Mouser India carries MYiR (MP13 SKU UNVERIFIED) | USD 46 = INR 4,319 | **not published**; E USD 28–32 (INR 2,630–3,000) | **Yes**, above budget | [10] |
| MYiR MYC-YF135 (standard) | MP135**D**AF7 (1 GHz / **basic**) | 256 MB / 256 MB NAND … 512 MB / 8 GB | 2 × RGMII | −40..85 °C | as above | as above | as above | as above | USD 29–48 (DigiKey marketplace 16.41) | launch "from USD 19" = INR 1,784 | **No: no secure boot** | [10] |
| **DHCOR STM32MP13** (DH electronics, DE) | **MP135F** (1 GHz / secure) | DDR3L 128 MB–1 GB; eMMC 4–16 GB; SPI boot flash | **2 × GbE** | UNVERIFIED | 29 × 29 × 3.2 mm **LGA, 271 pads, pre-tinned** | **Mainline Linux and U-Boot** (`stm32mp13xx-dhcor-som.dtsi`) | 10+ years | import; no India distributor found | quote only | quote only (UNVERIFIED) | Yes (temperature to confirm) | [12] |
| Engicam MicroGEA STM32MP13 (IT) | MP135, "up to 1 GHz" (security grade UNVERIFIED) | up to 1 GB LPDDR3L / 4 GB eMMC | 2 × 10/100 | −40..125 °C claimed for parts other than the CPU | 25 × 25 mm (mounting type UNVERIFIED) | Yocto (UNVERIFIED) | SoM EOL ≥ 10 years | import | not published | not published | Possibly; LPDDR3L means a different BSP from chip-down DDR3L | [13] |
| **iWave iW-RainboW-G54M** (Bangalore) | MP135F (iW-G54M-OS35-…) | 512 MB / 4 GB eMMC | 2 (UNVERIFIED) | UNVERIFIED (industrial likely) | **OSM Size-S / 0 LGA** (solder-down) | Yocto (UNVERIFIED version) | UNVERIFIED | **Made in India**; DigiKey marketplace | USD 62.13 = INR 5,834 | quote | Yes, price high | [14][R18] |
| Ka-Ro QSMP-1351 | MP135**C** (**650 MHz** / secure) | 256 MB DDR3L / 4 GB eMMC | **1** × 10/100/1000 | **−25..85 °C** | 27 × 27 × 2.3 mm QFN-style, 100 pads at 1 mm (socketed version available) | Yocto Scarthgap, Debian 12, LTS kernel | Long-term supplier's declaration | import (Logic.nl, Direct Insight) | — | **EUR 23 starting** (about INR 2,500, FX UNVERIFIED); "close to GBP 20 volume" | **No**: 650 MHz, one port, −25 °C | [11] |
| Digi ConnectCore MP13 | MP133**C** (650 MHz / secure) | 256 MB / 256 MB NAND (kit) | UNVERIFIED | UNVERIFIED | LGA and/or castellated | Digi Embedded Yocto | UNVERIFIED | distributors | kit USD 99–200 | module price not public | No: 650 MHz | [15] |
| Ebyte ECK10-135A5M5M-I | MP135**AAF3** (650 MHz / **basic**) | 512 MB / 512 MB NAND | 2 MACs, 1 GbE PHY on module | −40..85 °C (carrier spec) | 38 × 32 mm, 128-pin stamp-hole | Linux 6.1.128, Buildroot / Ubuntu 18.04 | not stated | **Hubtronics INR 2,318.64 ex-GST** (0 stock) | USD 26.99 (AliExpress, 2024) | — | **No: no secure boot, 650 MHz** | [16] |
| Seeed ODYSSEY-STM32MP135D | MP135D (1 GHz / basic) | 512 MB / 4 GB | 2 ports (SBC) | UNVERIFIED | **SBC only**, no SoM sold | Yocto / Buildroot | — | robu.in | USD 35 | — | No (SBC, no secure boot) | [17] |
| Forlinx | **No STM32MP13 SoM found** | — | — | — | — | — | — | — | — | — | — | [23] |

What the SoM table shows:
- The **standard** low-cost SKUs (MYiR D-part, Ebyte A-part) save money by dropping secure boot. Under the CRA rule they are not acceptable.
- **MYiR is the only vendor publishing an MP135F price** (sample USD 46).
  - MYiR's "from USD 19" headline is for the D part [10].
  - MYiR states it added the MP135F for CRA-oriented security [10].
  - A 256 MB / 256 MB NAND MP135F variant (cheaper, matching chip-down memory) is not a catalogue SKU. **Ask MYiR for a 1k quote** (UNVERIFIED; E about USD 22–26).
- **DHCOR is the most "upstream" option.** Its device tree and U-Boot support are mainline [12], which helps CRA maintenance. Ask for a 1k quote.
- iWave is the India-local option but listed at USD 62 for one unit [14]. Its volume price is UNVERIFIED and worth a quote, because India-made content and local support matter for MTCTE and service.

---

## 4. Vendor notes (owner request: Toradex, MYiR, Radxa)

### 4.1 Toradex

Prices are from toradex.com's India pages (INR, quantity 1–99 sample tier; GST treatment UNVERIFIED). Volume prices are "Get Volume Quote" for 100–200,000 units [24][25].

| Module | CPU | Ethernet | Temp. | INR @1–99 | Availability | Src |
|---|---|---|---|---|---|---|
| Colibri iMX6ULL 256 MB (0036) | i.MX6ULL | 1 × 10/100 PHY + 1 × RMII | 0–70 °C | 7,508 | 2035 | [24] |
| Colibri iMX6ULL 512 MB IT (0044) | i.MX6ULL | as above | −40..85 °C | 10,511 | 2035 | [24] |
| Colibri iMX6ULL 512 MB Wi-Fi/BT IT (0040) | i.MX6ULL | as above | −40..85 °C | 12,783 | 2035 | [24] |
| Colibri iMX7 | 2 × A7 + M4 | 1 × PHY + 1 × RGMII/RMII | −20..85 °C | 14,687–20,498 | 2035+ | [25] |
| Verdin AM62 Solo 512 MB / Dual 1 GB IT | AM62x | 1 × GbE PHY + 1 × RGMII | 0–70 / −40..85 °C | 12,103 / 19,386 | 2033+ | [25] |
| Verdin iMX8M Mini DualLite 1 GB | i.MX8M Mini | 1 × GbE | 0–70 °C | 18,213 | 2035+ | [25] |
| OSM iMX93 Dual 2 GB IT | i.MX93 | 2 × RGMII (TSN) | −40..85 °C | 20,304 | 2038 | [25] |
| OSM iMX91 2 GB IT | i.MX91 | 2 × RGMII (TSN) | −40..85 °C | not shown; **USD 25.55 volume** (2026 launch) = INR 2,399 | until 2040 | [25][30] |
| Verdin iMX95 | i.MX95 | 2 × GbE | −40..85 °C | from 31,725 | 2039+ | [25] |
| Verdin RK3568J | Rockchip RK3568J | 2 × GbE | −40..85 °C | not shown | — | [25] |

- **Premium.**
  - The cheapest industrial-temperature Toradex module that suits a router (Colibri iMX6ULL 512 MB IT) is **INR 10,511, about 4.2 × the INR 2,500 budget**, at sample quantity.
  - Only the **OSM iMX91** reaches the budget, and only at Toradex's volume price (USD 25.55) [30]. It is not an STM32MP13 and it needs a different BSP.
- **What the premium buys:**
  - published availability dates (2033–2040);
  - a formal PCN / Last-Time-Buy policy [24];
  - Torizon OS (OTA updates, containers) and Yocto BSPs with LTS releases;
  - a Bangalore office (india@toradex.com) [24].
- Toradex secure-boot documentation for HAB/AHAB uses NXP's public CST tool (UNVERIFIED in this pass).

### 4.2 MYiR (sample prices, en.myir.cn ordering tabs)

| SoM | CPU | Ethernet | Mounting | Linux | Sample price (USD) | Volume headline |
|---|---|---|---|---|---|---|
| MYC-Y6ULX-V2 | i.MX6ULL / 6UL, 528 MHz | 2 × 10/100 (1 PHY on module) | 37 × 39 mm, 140-pin 1.0 mm stamp-hole, 10-layer | **6.12.49** | 32 (256/256, I); 46–48 (eMMC) | "from USD 18/19" [18] |
| MYC-YF135 / YF135F | MP135D / **MP135F** | 2 × RGMII | stamp-hole | 6.6.78 | 29–48 / **46** | "from USD 19" (D part) [10] |
| MYC-YA151C-T | MP151A (single A7, 650 MHz) | 1 × RGMII | stamp-hole, 39 × 37 mm | 5.4 | 38 / 52 | — [19] |
| MYC-YA157C-V3 | MP157A (2 × A7 + M4) | 1 × RGMII | 45 × 43 mm, 8-layer | 5.4.31 (Yocto 3.1) | 57–60 | — [19] |
| MYC-YM62X | AM6231 / 6252 / 6254 | 2 × RGMII | 164-pin castellated + 58 LGA | 6.12.35, Debian 12 | 83 / 82 / 188 | — [20] |
| MYC-LMX9X | i.MX9352 | 2 × RGMII | LGA 37 × 39 mm | 6.12, Debian 12 | 143 / 169 | — [20] |
| MYC-C8MMX | i.MX8M Mini | 1 × GbE | **board-to-board** 2 × 100-pin | — | 107 / 121 | — [20] |
| MYC-YT113X / YT113i | Allwinner T113-S3 / T113-i, 2 × A7 1.2 GHz | 1 × RGMII/RMII | stamp-hole (+ 50 LGA on T113i) | — | 21–42 / 27–70 | "USD 14" [21] |
| MYC-YR3506 | RK3506B / J, 3 × A7 + M0 | 2 × RMII | stamp-hole, 8-layer | 6.1.99 | 25 (B, 0–70 °C) / 28 (J, −40 °C) | "USD 12.80" [22] |

- MYiR states that the sample price applies only to the first two pieces, and that larger quantities need a quote [10][18].
- BSP quality:
  - newer kernels on the i.MX6ULL (6.12), AM62x and i.MX93;
  - the MP15 SoMs are stuck on 5.4 (Yocto 3.1, end of life);
  - MP13 is on 6.6.
- Most MYiR SoMs use solderable stamp-hole or LGA mounting, which is good for vibration. India availability is mainly by direct import or Mouser (UNVERIFIED per SKU).

### 4.3 Radxa (brief; not researched further after the owner's refocus)

- **CM3I** (Rockchip RK3568, 4 × A55):
  - India: Hubtronics INR 6,837 ex-GST (2 GB / 8 GB, Wi-Fi) [27];
  - EU: EUR 81–160 [27];
  - datasheet SKU table −40..85 °C (variant mapping UNVERIFIED) [27].
- RK3568 has 2 × GbE MACs. Its secure-boot tools and long-term supply are Rockchip-controlled (not public in the ST/NXP sense, UNVERIFIED).
- ZERO / ROCK boards and the Qualcomm QCS6490 "Dragon" board: **not researched** (UNVERIFIED). They are consumer-temperature SBCs or over budget, and the R19 Qualcomm limits apply.
- **Flag:** reliability (consumer-derived parts), security tooling and longevity are weaker than ST/NXP. All Radxa options are far above INR 2,500.

---

## 5. Chip-down vs SoM at 1k and 5k per year

Comparison basis: the same router (section 6). The STM32MP13 core is either chip-down MP135FAE7 or a solder-down MP135F SoM.

| Item | Chip-down (MP135FAE7) | SoM (MYiR MYC-YF135F) |
|---|---|---|
| Core parts | SoC 713 + DDR3L 2 Gbit 560 + SPI-NAND 235 + power 150 + crystals 25 = **1,683** | **2,800** (E; sample 4,319) |
| PCB | 6-layer, 150 [R18] | 4-layer carrier, about 85 [R14] (−65) |
| Assembly | 0.8 mm BGA + X-ray inspection, about +40 per unit (E, UNVERIFIED) | castellated / LGA, reflow only |
| Per-unit BOM difference | — | **about +1,012 BOM** → about +1,973 at ex-works |
| One-time engineering | DDR3L layout and SI following ST's reference / AN5692, power tree (AN5586), one extra spin (E): **4–6 engineer-months, INR 10–15 lakh** [4][R18][R19] | carrier only (3–5 engineer-months HW, as R18) |
| Risk | DDR bring-up, BGA voiding; India EMS BGA/X-ray capability is common but UNVERIFIED per vendor | single-source module, vendor BSP lag, module EOL tied to vendor |

Break-even:
- **1k per year:** the SoM premium is about INR 10.1 lakh BOM per year (INR 19.7 lakh ex-works). The chip-down NRE (INR 10–15 lakh) is recovered in about **12–18 months** (1,000–1,500 units). Over a 5-year life, chip-down saves about INR 35–40 lakh of BOM.
- **5k per year:** the premium is about INR 50 lakh per year, and chip-down pays back in about **3 months**.

**Recommendation:**
1. **EVT and pilot (first 100–300 units):**
   - Build a carrier for the **MYiR MYC-YF135F** (MP135F + DDR3L, the same silicon and memory type as production, so the same TF-A / OP-TEE / Yocto BSP and signing flow).
   - This de-risks software and certification while chip-down layout proceeds.
   - Alternative: DHCOR (mainline) if its quote is lower.
2. **Production at 1k and at 5k per year: chip-down STM32MP135FAE7 (or MP133FAE7 if quoted lower)**, LFBGA289 0.8 mm, 16-bit DDR3L, 6 layers.
3. Do **not** move to 0.5 mm packages (FAF7 / FAG7, about USD 1–2 cheaper) unless the Indian fab and EMS confirm HDI or via-in-pad yield. That saving (about INR 100–190) is smaller than the yield risk.

---

## 6. Tier-2 router BOM and ex-works price (recommended: chip-down STM32MP135FAE7 + STM32H533)

INR at 1k, ex-GST. Status codes: **S** sourced, **R** from an internal report, **E** estimate.

| # | Block / part | INR | Status / basis |
|---|---|---|---|
| 1 | **STM32MP135FAE7** (1 GHz, secure, 2 MACs, LFBGA289 0.8 mm) | **713** | S: DigiKey USD 7.594 @714, 614 in stock [6]; eStore 7.40 [3]; MP133FAE7 Avnet about 5.95 (INR 559, UNVERIFIED) [8] |
| 2 | DDR3L 2 Gbit (16-bit) | 560 | R/E [R18]; get a quote |
| 3 | SPI-NAND 2 Gbit | 235 | R [R18] |
| 4 | SoC power, discrete (AN5586) | 150 | R/E [R18] |
| 5 | Crystals | 25 | R/E [R18] |
| 6 | 2 × Ethernet: 2 × KSZ8081RNAIA, 2 × HX1188NL magnetics, 2 × RJ45, ESD, Bob-Smith | 470 | R [R18][R11] |
| 7 | Quectel EC200A-CN over USB | 1,150 | S/E [R18] |
| 8 | Modem VBAT buck, bulk, USB ESD | 120 | R [R18] |
| 9 | SIM 2FF + ESD | 15 | R [R18] |
| 10 | Wi-Fi 4 2.4 GHz (the SoC has none) | 600 | S/E [R18]; part choice open |
| 11 | 9–36 V input: fuse, TVS, reverse FET, π-filter, 60 V buck | 165 | R [R18] |
| 12 | 2 DI (opto) + 2 DO (OC 60 V) | 90 | R [R18] |
| 13 | Isolated RS-485 (CA-IS2092W) + protection + termination | 166 | R [R18] |
| 14 | **STM32H533RET6 companion (Zephyr) + crystal, SWD, decoupling**; replaces the external watchdog | 294 | R [R19][R14] |
| 15 | Pluggable terminals | 50 | R [R18] |
| 16 | 3 × SMA + pigtails | 120 | E [R18] |
| 17 | Antennas (2 × LTE + Wi-Fi) | 220 | E [R18] |
| 18 | LEDs, reset button, light pipes | 30 | E [R18] |
| 19 | PCB 6-layer, about 100 × 80 mm | 150 | E [R18] |
| 20 | Passives and miscellaneous | 120 | E [R18] |
| 21 | Aluminium DIN enclosure | 375 | E [R18] |
| 22 | Packaging, power pigtail, label | 40 | E [R18] |
| | **BOM total** | **5,858** | |

### 6.1 Ex-works comparison

| Option | BOM | × 1.5 | + 750 | **Ex-works (× 1.3)** | vs R19 (11,954) |
|---|---|---|---|---|---|
| R19 (i): MP133CAF3 (650 MHz, 0.5 mm) + H533 [R19] | 5,630 | 8,445 | 9,195 | 11,954 | — |
| **R20 recommended: MP135FAE7 chip-down + H533** | **5,858** | 8,787 | 9,537 | **12,398** | **+444** |
| R20 with MP133FAE7 at Avnet's about USD 5.95 (UNVERIFIED) | 5,704 | 8,556 | 9,306 | 12,098 | +144 |
| R20 Lite: no Wi-Fi (−680, as R18) | 5,178 | 7,767 | 8,517 | 11,072 | −882 |
| SoM build: MYiR YF135F at E INR 2,800, 4-layer carrier (core −1,683 +2,800, PCB −65) | 6,910 | 10,365 | 11,115 | **14,450** | +2,496 |
| SoM build at MYiR sample price (USD 46) | 8,429 | 12,644 | 13,394 | 17,412 | +5,458 |
| Ka-Ro QSMP-1351 (EUR 23, about INR 2,500; fails the 1 GHz / 2-port / −40 °C rules) | about 6,610 | 9,915 | 10,665 | about 13,865 | +1,911 |

Competitors [R18]:

| Product | INR |
|---|---|
| RUT200 | 7,569–8,500 dealer; 13,700 retail |
| USR-G806w | 8,008 ex-GST |
| USR-G809 | 10,528 ex-GST |

- The recommended chip-down router (INR 12,398) stays **below RUT200 retail** and offers 1 GHz, secure boot, isolated RS-485, 2 DI / 2 DO and the safety MCU. It does not reach dealer prices.
- The SoM build (INR 14,450) is above RUT200 retail, so it is a pilot-only route.

---

## 7. Other vendors: brief comparison (not researched further, per the owner's refocus)

Module price at 1 unless marked; "vol" = vendor volume headline. INR at 93.9.

| Option | CPU (cores × clock) | Ethernet MACs | Secure boot / public tools | Temp. | Longevity | Price → INR | vs rules | Src |
|---|---|---|---|---|---|---|---|---|
| NXP i.MX6ULL, MYiR MYC-Y6ULX | 1 × A7 528 MHz (800 MHz parts exist) | 2 × 10/100 | HAB; NXP CST public (account) | −40..85 °C | NXP long-term (date UNVERIFIED) | USD 32 sample; vol 19 → 1,784 | Fails the 1–1.2 GHz rule (528 MHz SKU) | [18] |
| Forlinx FETMX6ULL-C / -S | 1 × A7 800 MHz | 2 × 10/100 | HAB | −40..85 °C | not stated | -S USD 26–49 (Alibaba) → 2,441–4,601 | -C is board-to-board and Linux 4.1.15 (old) | [23] |
| Toradex Colibri iMX6ULL IT | 1 × A7 | 1 PHY + 1 RMII | HAB | −40..85 °C | 2035 | INR 10,511 | 4 × budget | [24] |
| Toradex OSM iMX91 | 1 × A55 | 2 × GbE (TSN) | AHAB + EdgeLock | −40..85 °C | to 2040 | vol USD 25.55 → 2,399 | Only non-ST module near budget; LPDDR4, 0.5 mm (module hides it) | [25][30] |
| i.MX93 (MYiR / Toradex OSM) | 2 × A55 + M33 | 2 × GbE | AHAB | −40..85 °C | 2038 (Toradex) | USD 143 / INR 20,304 | Over budget | [20][25] |
| i.MX8M Mini (MYiR / Toradex) | 4 × A53 + M4 | 1 × GbE | HAB | −40..85 °C | 2035+ | USD 107–121 / INR 18,213+ | One MAC, over budget | [20][25] |
| TI AM62x (MYiR / Toradex Verdin) | 1–4 × A53 + M4F | 2 × GbE | HS-SE (terms UNVERIFIED) | −40..85 °C | 2033+ (Toradex) | USD 82–83 / INR 12,103+ / Verdin vol USD 31.90 [R19] | Over budget | [20][25][R19] |
| ST STM32MP151 / 157 (MYiR, Ka-Ro) | 1–2 × A7 650–800 MHz (+ M4) | **1** × GbE | ST ROM (secure only on C/F parts) | −40..85 °C | 10-year rolling | MYiR USD 38–60 (A parts, non-secure); Ka-Ro QSMP-1570 EUR 42 | One MAC, sub-1 GHz, over budget | [19][11] |
| ST STM32MP23 / 25 (Ka-Ro QSMP-20/23/25) | 2 × A35 1.2–1.5 GHz + M33/M4 | 2–3 × GbE | ST secure boot | −25/−40..85 °C | 10-year | not fetched; R19: MP231C chip USD 12.77 | "Pro" path [R19] | [11][R19] |
| Microchip SAMA7D65 SiP module | 1 × A7 1 GHz | 2 × GbE | secure boot | — | UNVERIFIED | GBP 53.89 @21 [R18] | Over budget | [R18] |
| Allwinner T113-S3 / T113-i (MYiR) | 2 × A7 1.2 GHz | **1** | Allwinner secure boot; tools and docs not public (UNVERIFIED) | −40..85 °C | not published | USD 21–27; vol 14 → 1,315 | **Flag:** one MAC, security tooling, longevity | [21] |
| Rockchip RK3506 (MYiR, Forlinx) | 3 × A7 1.2–1.5 GHz + M0 | 2 × 10/100 | Rockchip secure boot; tools partly public (UNVERIFIED) | J: −40..85 °C | not published | MYiR USD 25–28, vol 12.80 → 1,202; Forlinx FET3506J-S USD 20 → 1,878 | **Flag:** Rockchip security, longevity, kernel 6.1 vendor BSP | [22][23] |
| Rockchip RK3568, Radxa CM3I / Toradex Verdin RK3568J | 4 × A55 | 2 × GbE | as above | −40..85 °C | Toradex supports it; Radxa not published | INR 6,837 ex-GST (Hubtronics) | Over budget; flag | [25][27] |
| MediaTek MT7628 / MT7621 / MT7981 (OpenWrt) | MIPS 580–880 MHz / 2 × A53 | switch / 1 + SGMII | MT7628: none; MT7981: chain exists, NDA docs | — | none published | MT7628 module USD 7.9–8.5 [R18] | Fails secure boot (MT7628/7621) and longevity [R18] | [R18] |
| Qualcomm QCA9531 (Compex WPJ531) | MIPS 24Kc 650 MHz | 2 (switch) | none in hardware (INFERRED) | −20..70 °C (HV-A) | — | USD 60 → 5,634 | Fails secure boot and temperature | [28] |
| Qualcomm IPQ4018/4019 (Compex WPJ419, 8devices Habanero) | 4 × A7 717 MHz | 2 (switch, e.g. QCA8075 [R16]) | Qualcomm (licensed tools) | — | — | USD 230–250, MOQ 99 (Alibaba); 8devices quote | Over budget; closed tools | [28] |
| Qualcomm QRB2210 SoMs | 4 × A53 2 GHz | **0** | SecTools licensed only | −30..85 °C | May 2034 | USD 44.66 + [R19] | Rejected in R19 | [R19] |

---

## 8. The Qualcomm question (short answer)

**Which families exist:**
- **Networking (router) SoCs:**
  - legacy Atheros MIPS QCA953x / 956x (e.g. QCA9531: 2.4 GHz 11n, 5-port switch);
  - QCA4531 (8devices Carambola3, −40..85 °C) [28];
  - **IPQ40xx** (4 × Cortex-A7 at 717 MHz, Wi-Fi 5, 2 × GbE MAC via an external switch or PHY);
  - **IPQ50xx** (2 × A53 at 1 GHz, Wi-Fi 6; e.g. DR5018 [28]);
  - **IPQ53xx / IPQ95xx** (Wi-Fi 7).
- **Cellular modems:** MDM9x07 and successors, inside many Quectel modules. Teltonika's TRB140 runs Linux on the modem's own Cortex-A7 (MDM9607) [R16].
- **IoT / "Dragonwing" application processors:**
  - QCS/QCM/QRB (QRB2210 on the Arduino UNO Q, QCS5430, QCS6490);
  - sold through Arrow and partners as SoMs (Thundercomm, eInfochips, Lantronix) [29][R19].

**Where they appear in industrial routers [R16]:**

| SoC | Product | Notes |
|---|---|---|
| QCA9531 | Teltonika TRB245; Robustel R1510 (INFERRED) | |
| IPQ4018 | Teltonika RUTX11 | with a QCA8075 PHY and Wi-Fi 5 |
| MDM9607 (in the modem) | Teltonika TRB14x | |
| MT7628 (MediaTek, not Qualcomm) | RUT200 / 241 / 956, USR-G806 | the cost-leader routers |

**Why they are hard for a small OEM to use directly:**
1. **Documents and tools behind licences.**
   - Datasheets, the QSDK/SPF software, and above all the **secure-boot signing tools (SecTools) and fuse procedures** are available only to licensed customers through Qualcomm's portals (ChipCode / CreatePoint) [R19 §2, R19 src 14].
   - The networking-family equivalent is INFERRED to be the same.
   - Without them, secure boot cannot be enabled, which fails our CRA rule.
2. **Volume-oriented supply.**
   - Router SoCs are sold to ODMs and to high-volume OEMs. Distribution listings are scarce: Octopart shows almost no DigiKey stock for Qualcomm parts [29].
   - Small OEMs buy pre-built **modules** (Compex, 8devices) at USD 60–250+, with MOQ, and those modules carry the same closed toolchain [28].
3. **Software.**
   - OpenWrt supports QCA9531 and IPQ40xx well, but Qualcomm's own SDK is a vendor fork.
   - OpenWrt has no LTS (yearly rebase [R18]), and the Wi-Fi firmware blobs are closed.
4. **Longevity.**
   - Qualcomm's Product Longevity Programme covers selected IoT SoCs (QRB2210 to May 2034 [R19]). Networking SoCs have no public dates (UNVERIFIED).

**Answer to the owner:** Qualcomm has many IoT parts. For a 1k–5k-per-year Indian OEM, though, they bring licence-gated security tooling, MOQ and closed firmware. The STM32MP13 brings public secure-boot tools, 10-year rolling supply, Yocto plus upstream OpenWrt, and distributor stock. Use Qualcomm only indirectly, through the cellular module.

---

## 9. Risks

1. **Part-number error carried from R18.**
   - R18 / R19 name the MP133**CAF3** as 0.8 mm. It is 0.5 mm TFBGA320 at 650 MHz.
   - Fix all documents and order **xAE7** parts for the 6-layer design.
2. **MP13 supply.**
   - DigiKey shows 30-week factory lead times. Only the MP135FAE7 is in DigiKey stock (614).
   - Avnet quotes 105 weeks for MP133FAE7 [5][6][8].
   - Place a forecast or blanket order with an ST franchised distributor (Avnet / Arrow / DigiKey India) early. Quote both MP133FAE7 and MP135FAE7.
3. **1 GHz thermal limit:** Tj max is 105 °C at 1 GHz [1]. Check the case temperature at +75 °C ambient.
4. **SoM pricing not published:**
   - The MYiR MP135F, DHCOR, Engicam and iWave volume prices are UNVERIFIED.
   - The SoM-build figures use E INR 2,800.
5. **DDR3L price inflation in 2026 [R18].** The chip-down DDR3L (INR 560) is an estimate. SoM prices will also move with DRAM.
6. **BSP divergence:** a pilot SoM with LPDDR3L (Engicam) or a different MP13 grade (D / A parts) would not share the production BSP and signing flow. Use an MP135F + DDR3L SoM only.
7. **Indian EMS BGA capability:** 0.8 mm BGA with X-ray is assumed (E). Confirm with two EMS vendors before committing to chip-down.
8. **Chinese SoCs (T113, RK3506, RK3568):**
   - cheap (USD 12.80–28);
   - secure-boot tooling and documents are not public in the ST/NXP sense, and there are no published longevity dates;
   - vendor kernels (6.1) lag.
   - They fail the reliability, security and longevity rules for this product.

### Open decisions for the owner

1. Approve the MP135FAE7 (or MP133FAE7 by quote) as the production part, and correct R18 / R19's MP133CAF3?
2. Approve a MYiR MYC-YF135F pilot carrier (or DHCOR after quotes) for EVT, with chip-down for production?
3. Should Wi-Fi be the default or a SKU option? The Lite SKU without Wi-Fi drops ex-works to about INR 11,072.

---

## 10. What could not be verified

- 1k prices for the MYiR MYC-YF135F, DHCOR STM32MP13, Engicam MicroGEA, iWave G54M and Digi ConnectCore MP13 modules (all quote-only).
- The temperature grade of DHCOR and iWave; the Ethernet count of iWave and Digi; Engicam's MP13 security grade and mounting.
- Avnet's MP133FAE7 USD 5.95 figure (page not fetched).
- An ST franchised 1k quote for the MP133FAE7 / MP135FAE7.
- ST datasheet confirmation of MP131 = 1 MAC (from ST product-family statements, not the datasheet table).
- Toradex INR prices: GST treatment; OSM iMX91 INR price.
- Radxa ZERO / ROCK / Dragon Q6A details; Qualcomm networking-family licence terms (INFERRED from QRB2210 terms).
- EUR→INR rate for Ka-Ro (about 108 assumed).
- Indian EMS BGA / X-ray capability.

---

## 11. Sources

1. ST wiki, STM32MP13 microprocessor (A/C/D/F nomenclature; 1 GHz only with temperature code 7) — https://wiki.st.com/stm32mpu/wiki/STM32MP13_microprocessor ; ST STM32MP1 press presentation (1 GHz only for Tj ≤ 105 °C) — https://www.st.com.cn/resource/en/product_presentation/stm32mp1_press-pres.pdf
2. ST eStore STM32MP133 (order codes, packages AE/AF/AG with pitch, prices, stock) — https://estore.st.com/en/products/microcontrollers-microprocessors/stm32-arm-cortex-mpus/stm32mp1-series/stm32mp133.html
3. ST eStore STM32MP135 — https://estore.st.com/en/products/microcontrollers-microprocessors/stm32-arm-cortex-mpus/stm32mp1-series/stm32mp135.html ; STM32MP131 — https://estore.st.com/en/products/microcontrollers-microprocessors/stm32-arm-cortex-mpus/stm32mp1-series/stm32mp131.html
4. ST AN5692 (DDR routing) and AN5586 (discrete power) for STM32MP13, as cited in [R18 src 33]
5. DigiKey STM32MP133FAE7 (USD 8.489 @714, 30 wk) — https://www.digikey.com/en/products/detail/stmicroelectronics/STM32MP133FAE7/21348888 ; DigiKey UK (GBP 6.34 @714) — https://www.digikey.co.uk/en/products/detail/stmicroelectronics/STM32MP133FAE7/21348888
6. DigiKey STM32MP135FAE7 (USD 12.27 @1 … 7.594 @714; 614 in stock) — https://www.digikey.com/en/products/detail/stmicroelectronics/STM32MP135FAE7/17775601
7. DigiKey STM32MP131FAE7 (USD 7.909 @714) — https://www.digikey.com/en/products/detail/stmicroelectronics/STM32MP131FAE7/21348907
8. Avnet STM32MP133FAE7 (about USD 5.95 @714, 105 wk; search snippet, UNVERIFIED) — https://www.avnet.com/americas/product/stmicroelectronics/stm32mp133fae7/evolve-64854603
9. ST STM32MP135 product page (dual Ethernet) — https://www.st.com/en/microcontrollers-microprocessors/stm32mp135.html ; CNX, STM32MP13 introduction (MP131 one Ethernet, MP133/135 two) — https://www.cnx-software.com/2023/03/10/stmicro-introduces-cost-optimized-stm32mp13-cortex-a7-microprocessor/
10. MYiR MYC-YF13X (ordering table: MP135DAF7 / MP135FAF7, sample prices; Linux 6.6.78; 2 × RGMII; 10-layer) — https://en.myir.cn/STM32MP135/65.html ; launch "USD 19" — https://en.myir.cn/ProductUpdates/52.html ; MP135F CRA SDK notice — https://www.myirtech.com/news_list.asp?id=870 ; DigiKey marketplace USD 16.41 [R09 S34]
11. Ka-Ro QSMP-13 (QSMP-1351: MP135C 650 MHz, 256 MB / 4 GB, −25..85 °C, 27 × 27 QFN-style 100 pads, 1 × GbE, Yocto Scarthgap, Debian 12; selection table incl. QSMP-15/20/23/25) — https://www.karo-electronics.com/qsmp-13/ ; Logic.nl (EUR 23 starting) — https://logic.nl/tools/computer-modules/qs-som-module-family/qsmp-13/ ; Direct Insight ("close to GBP 20") — https://electropages.com/2024/08/low-price-som-wide-range-connectivity-options-suits-rugged-environments
12. DHCOR STM32MP13: ST partner page — https://www.st.com/ja/partner-products-and-services/dhcor-stm32mp13.html ; ST China (271-pin LGA, DDR3L / eMMC options) — https://www.st.com.cn/zh/partner-products-and-services/dhcor-stm32mp13.html ; U-Boot patch (stm32mp135f-dhcor-dhsbc) — https://lists.denx.de/pipermail/u-boot/2024-June/556308.html ; Linux DTS — https://gbmc.googlesource.com/linux/+/06e47dce8fc3ab68c2ea3b5082caab99e8002b80/arch/arm/boot/dts/st/stm32mp13xx-dhcor-som.dtsi ; FHI (10+ years) — https://fhi.nl/dene/solderable-cost-effective-som
13. Engicam MicroGEA STM32MP13 flyer — https://cdn.shopify.com/s/files/1/0246/6129/5209/files/Microgea_STM32MP13_Flyer.pdf ; LinuxGizmos — https://linuxgizmos.com/microsom-features-stm32mp1-series-mcu/
14. iWave STM32MP135F OSM-SF: DigiKey marketplace (USD 62.13 @1) — https://www.digikey.com.br/en/products/detail/iwave-global/iW-G54M-OS35-3D512M-E004G-BIA/21728451 ; product — https://iwave-global.com/product/stm32mp135-osm-sf-lga-system-on-module/ ; datasheet [R18 src 35]
15. Digi ConnectCore MP13 (STM32MP133C) — https://www.digi.com/resources/documentation/digidocs/embedded/dey/4.0/ccmp13/hw_index ; CNX — https://www.cnx-software.com/2023/03/14/digi-connectcore-mp13-som-with-stm32mp13-mpu-embeds-wi-fi-5-and-bluetooth-5-2-module/ ; Farnell CC-WMP133-KIT — https://uk.farnell.com/digi-international/cc-wmp133-kit/development-kit-32bit-arm-cortex/dp/4709708
16. Ebyte ECK10-135A5M5M-I: Hubtronics (INR 2,318.64 ex-GST) — https://hubtronics.in/eck10-135a5m5m-i?tag=SOM ; CNX (MP135AAF3, USD 26.99, Linux 6.1.128) — https://www.cnx-software.com/2024/12/20/stm32mp135-pico-itx-sbc-features-38x32mm-ebyte-cpu-module-with-512mb-ram-512mb-nand-flash/ ; RobotShop ECK10-135D — https://www.robotshop.com/products/ebyte-eck10-135d2-c-256mb-memory-embedded-core-board-low-power-consumption-compact-size-rich-i-o-interface
17. Seeed ODYSSEY-STM32MP135D — https://hackerboards.com/board/seeed-odyssey-stm32mp135d ; DigiKey — https://www.digikey.at/en/products/detail/seeed-technology-co-ltd/102110859/21277010 ; robu.in — https://st.robu.in/product/odyssey-stm32mp135d-cortex-a7-stm32-yocto-buildroot-os-ethernet-ports-with-wol-usb-type-a-csi-lcd-4gb-dram-tf-card-holder-poe
18. MYiR MYC-Y6ULX-V2 (ordering, Linux 6.12.49) — https://en.myir.cn/iMX6UL/10.html ; "from USD 19" — https://en.myir.cn/ProductUpdates/96.html
19. MYiR MYC-YA151C-T — https://en.myir.cn/STM32MP151/64.html ; MYC-YA157C-V3 — https://en.myir.cn/STM32MP157/63.html
20. MYiR MYC-YM62X — https://en.myir.cn/AM62x/62.html ; MYC-LMX9X — https://en.myir.cn/iMX93/57.html ; MYC-C8MMX — https://en.myir.cn/iMX8MMini/50.html
21. MYiR MYC-YT113X — https://en.myir.cn/T113/78.html ; MYC-YT113i — https://en.myir.cn/T113/76.html ; "USD 14" — https://en.myir.cn/ProductUpdates/55.html
22. MYiR MYC-YR3506 — https://en.myir.cn/RK3506/158.html ; Hackster ("from USD 12.80") — https://www.hackster.io/news/make-your-ideal-real-myir-launches-new-low-cost-rockchip-rk3506-rk3562-systems-on-modules-771806b72a3f
23. Forlinx FETMX6ULL-C (B2B, Linux 4.1.15) — https://www.forlinx.net/product/128.html ; Forlinx Alibaba (FETMX6ULL-S USD 26–49) — https://forlinx.en.alibaba.com/ ; DigiKey FET3506J-S (USD 20) — https://www.digikey.com/en/products/detail/forlinx-embedded/FORLINX-FET3506J-S-15512SE8GIB10/27505757
24. Toradex Colibri iMX6ULL (India INR prices, availability 2035, PCN/LTB policy, India office) — https://www.toradex.com/computer-on-modules/colibri-arm-family/nxp-imx6ull
25. Toradex: Verdin iMX8M Mini — https://www.toradex.com/computer-on-modules/verdin-arm-family/nxp-imx-8m-mini-nano ; Verdin AM62 — https://www.toradex.com/computer-on-modules/verdin-arm-family/ti-am62 ; OSM iMX93 — https://www.toradex.com/computer-on-modules/osm-arm-family/nxp-imx93 ; OSM iMX91 — https://www.toradex.com/computer-on-modules/osm-arm-family/nxp-imx91 ; Colibri iMX7 — https://www.toradex.com/computer-on-modules/colibri-arm-family/nxp-freescale-imx7 ; Verdin iMX95 — https://www.toradex.com/computer-on-modules/verdin-arm-family/nxp-imx95 ; Verdin RK3568J — https://www.toradex.com/computer-on-modules/verdin-arm-family/rockchip-rk3568j
26. Seeed NPi i.MX6ULL (legacy SBC, 2019, USD 39–44; not a production SoM) — https://wiki.seeedstudio.com/NPi-i.MX6ULL-Dev-Board-Linux-SBC/ ; https://www.cnx-software.com/2019/09/27/npi-i-mx6ull-industrial-linux-sbc/
27. Radxa CM3I: Hubtronics — https://hubtronics.in/rm118‑d2e8j0w1?tag=CM3 ; neven7 — https://www.neven7.eu/p/radxa-cm3i-rk3568-compute-module ; product brief — https://dl.radxa.com/cm3p/docs/hw/radxa_cm3i_product_brief.pdf
28. Compex QCA9531 / IPQ4019 boards — https://embeddedworks.net/shop/chipmaker-qualcomm/chipmodel-__empty__value__-or-qualcomm-qca9531-or-qualcomm-qca9880/ ; https://electronics.alibaba.com/product/ipq4018 ; 8devices shop (quotes) — https://shop.8devices.com/?p=2080 ; DR5018 IPQ5018 — https://www.cnx-software.com/2021/07/15/low-cost-embedded-router-sbc-2-5-gbe-wifi-6-qualcomm-ipq5018/
29. Qualcomm QCS6490 at Arrow — https://www.arrow.com/products/qcs-6490-1-psp1287-tr-00-0-aa/qualcomm ; Qualcomm QCS6490 — https://www.qualcomm.com/products/internet-of-things/qcs6490 ; Octopart Qualcomm listings — https://octopart.com/manufacturers/qualcomm/integrated-circuits-ics/embedded-processors-and-controllers
30. CNX, Toradex OSM and Lino i.MX91/93 (USD 25.55 / 28.20 volume) — https://www.cnx-software.com/2026/03/31/toradex-osm-and-lino-soms-30x30mm-nxp-i-mx-93-i-mx-91-modules-with-solder-down-or-b2b-connector-designs/
