# R05 — Industrial Wired (Fieldbus) Module: Selection and Costing

> **Owner decision 2026-11-14: Mornsun parts are banned (PRD COMP-6).** Every Mornsun part recommended below is withdrawn; see the PRD for replacements.


Status: COMPLETE WITH GAPS (2026-11-14). Gaps: RMII PHY / PoE / RS-232 / M-Bus / 10BASE-T1L prices, PCB/terminal/crystal prices, J1939/DLMS stacks, ThreadX SDK support on low-end MCUs — the web-search budget ran out; these are marked UNVERIFIED.
Date: 2026-11-14

Scope after the 2026-11-13 product-owner update:
- Ethernet is REMOVED from this module (it now lives on the combined 4G + Ethernet + Wi-Fi module). Section 5 keeps only a short PHY / SPI-Ethernet / RJ45 table for that other module.
- Wired fieldbus = CAN-FD + RS-485 (optional RS-232), costed for two architectures:
  - (A) hosted directly by the baseboard MCU (only transceivers, protection, terminals added to the baseboard);
  - (B) a small enclosed "fieldbus module" with its own low-cost MCU (ST track and NXP track), usable standalone as a Modbus / CAN remote node.
- Three isolation variants each: V1 non-isolated but well protected, V2 group-isolated, V3 per-port isolated.
- Cost basis: finished cost = BOM x 1.4. Target for this module: finished <= INR 1,000 (BOM <= ~INR 714).

## 1. Executive summary and recommendation

- Ethernet is gone from this card. The fieldbus job (CAN-FD plus 2x RS-485) needs only a cheap MCU, so the MCUs are now ranked on cost.
- **ST primary: STM32G0B1** (M0+ 64 MHz, 2x FDCAN, 6 USART, 144 KB RAM, Zephyr FDCAN supported). The 128 KB CBT6 costs ~USD 1.11-1.20 @1k (LCSC) = **~INR 104-113**. Use the 256-512 KB CC/CE version for dual-slot OTA (price not checked). **ST cheapest: STM32C092** (1 FDCAN, 4 USART, 36 KB RAM), ~EUR 0.82-0.86 @0.5-1.5k = **~INR 85**, KCU6 USD 1.71 @1k.
- **NXP primary and cheapest: MCXA156** (M33 96 MHz, 1 MB / 128 KB, 1 FlexCAN-FD, 5 LPUART, Zephyr `nxp,flexcan-fd`): USD 2.07-2.13 @~1k = **~INR 194-200**. Lead times are long. MCX N236 (~INR 800) and MCX A34x (~INR 225 at volume) cost more for no fieldbus benefit.
- Transceivers: RS-485 **SIT3485EESA** (~INR 17), with TI THVD1450 (+/-18 kV IEC ESD, ~INR 142-187) when certification margin matters. CAN-FD **NXP TJA1051T/3** (~INR 33), with TI TCAN1044V (~INR 63) as second source. The external protection network (SM712-class TVS + PPTC, ~INR 20/port) is what meets IEC 61000-4-5.
- Isolation: V2 group isolation = CA-IS3082W-class RS-485 + TI ISO1042 CAN-FD + Mornsun B0505S-1WR3. V3 per-port isolation = Chipanalog CA-IS2092A (RS-485 + DC-DC) + CA-IS2062A (CAN-FD + DC-DC, datasheet preliminary).
- BOM, Architecture B (own MCU, enclosed): ST **V1 ~INR 507 / V2 ~697 / V3 ~830**. NXP **V1 ~595 / V2 ~785 / V3 ~918**. Target is <= 714. V1 fits on both tracks. V2 fits only on ST, by ~INR 17. V3 does not fit.
- BOM adder, Architecture A (baseboard MCU hosts the ports): **V1 ~INR 177 / V2 ~367 / V3 ~500**.
- Recommendation: make V1 (non-isolated, well protected) the standard and sell V2 as a premium "-ISO" assembly variant. Fit one RS-485 by default with the second as an assembly option (saves ~INR 45-70). Use the ST G0B1 track and keep MCXA156 as the NXP alternative. Consider a hybrid: one RS-485 on the baseboard plus an optional enclosed fieldbus module.
- Biggest risks: the pass-through stacking bus may need two connectors per module (+INR 60). The low-cost MCUs have no TrustZone or crypto, so the module relies on the baseboard secure element and signed firmware. Many supporting prices are UNVERIFIED (see status line).

## 2. Exchange rate and pricing method

- Rate used: **1 USD = INR 93.9** (mid-market dashboard 93.93 on 2026-11-08 [S1]; PTI/HDFC Sky reports 93.74-94.86 in early Nov 2026 [S2]). Same rate as R03 / R10 for consistency. EUR prices converted at 1 EUR ~ 1.08 USD (approx, UNVERIFIED).
- Prices are unit prices at ~1k qty where a 1k break exists; otherwise the nearest break is stated. Distributor price pages are dynamic: most figures below come from cached distributor listings surfaced by search between 2026-11-13 and 2026-11-14 (date of capture not shown on the page), so treat them as **budgetary +/-15 %** and re-quote before ordering. LCSC price tiers could not be fetched directly (rendered client-side), so LCSC figures are from search-indexed snapshots of the product page.
- INR figures exclude GST and import duty (BCD on ICs into India is typically 0-10 % — UNVERIFIED per HS code; add ~18 % GST, recoverable for a registered manufacturer).

## 3. MCU options (Architecture B fieldbus module; notes for Architecture A)

No Ethernet MAC is needed any more, so the MCUs are re-ranked on cost. Needs for Architecture B: >= 1 CAN-FD, >= 3 UARTs (2x RS-485 + RS-232/debug), SPI/I2C, enough flash for Modbus RTU + CANopen + secure bootloader (MCUboot) + A/B or swap image, LQFP/QFN, Zephyr support for CAN-FD and UART.

### 3.1 Candidate table

| MCU (package) | Core / MHz | Flash / RAM | CAN-FD | UARTs | Security | Zephyr CAN-FD | Price ~1k (USD) | INR | Notes |
|---|---|---|---|---|---|---|---|---|---|
| **ST STM32C092KBT6 / KCT6** (LQFP32/48, UFQFPN) | M0+ / 48 | 128-256 KB / up to 36 KB (30 KB on some) [S3] | 1 FDCAN (C092 only) [S3] | 4 USART [S3] | Flash protection + securable area only; no TrustZone, no crypto HW [S3] | Yes: nucleo_c092rc lists `st,stm32-fdcan` [S6] | KBT6 EUR 0.82-0.86 @500-1.5k (DigiKey DE) ~USD 0.91; KCU6 USD 1.71 @1k (DigiKey CA) [S4] | ~85-160 | Cheapest ST with CAN-FD; RAM is tight but enough for RTU+CANopen; in full production (datasheet DS14720, Apr 2025) |
| **ST STM32G0B1CBT6** (LQFP48) | M0+ / 64 | 128 KB / 144 KB (datasheet DS13560 rev 6, Feb 2026) [S17] | 2 FDCAN [S7][S17] | 6 USART + 2 LPUART [S17] | RDP, securable memory area, no TrustZone, no crypto HW (UNVERIFIED) | Yes: nucleo_g0b1re lists `st,stm32-fdcan` x2 [S7] | USD 1.11-1.20 @1k (LCSC C2847904, two snapshots) [S5] | ~104-113 | Best ST value: 2x FDCAN, many UARTs, lots of RAM |
| ST STM32H503CBT6 (LQFP48) | M33 / 250 | 128 KB / 32 KB [S18] | 1 FDCAN [S18] | 3 USART + 1 LPUART [S18] | "secure life cycle management", write-protect and hide-protect areas [S18]; TrustZone not confirmed (UNVERIFIED) | Yes (STM32H5 FDCAN driver; nucleo_h503rb) (UNVERIFIED) | USD 1.71-1.74 @1k (LCSC C17700273); Mouser USD 1.95 @1k (via findchips) [S8] | ~160-183 | Fast M33 but small RAM; no benefit over G0B1 for this job |
| ST STM32G431CBT6 (LQFP48) | M4F / 170 | 128 KB / 32 KB (UNVERIFIED) | 1 FDCAN (UNVERIFIED) | 3 USART + LPUART (UNVERIFIED) | No TrustZone | Yes (G4 FDCAN) | USD 1.89 @1k (LCSC C529355; other snapshot 2.10) [S9] | ~177 | No advantage for fieldbus |
| **NXP MCXA156VLL / VLH / VFT** (LQFP100 / LQFP64 / HVQFN48) | M33 / 96 | 1 MB / 128 KB [S11] | 1 FlexCAN FD [S11] | 5 LPUART [S11] | M33 without TrustZone-enabled security subsystem listed in Zephyr page (crypto not listed) [S11]; UNVERIFIED | Yes: frdm_mcxa156 lists `nxp,flexcan-fd` [S11] | VLL: USD 2.13 @720, 2.07 @1440 (Avnet); USD 2.07 @1530 (Future) [S10] | ~194-200 | Cheapest NXP with CAN-FD found; long lead times quoted (Avnet 112 wk factory LT) |
| NXP MCX A34x (e.g. MCXA346) | M33 / 180 | up to 1 MB / 256 KB [S12] | 1 FlexCAN FD [S12] | 6 LPUART [S12] | — | UNVERIFIED | launch: USD 4.41 @1, USD 2.40 @3,200 tray [S12] | ~225 | Motor-control part; more expensive than A156 |
| NXP MCX N236 (HLQFP100 / VFBGA184) | M33 / 150 | 1 MB / 352 KB [S13] | 2 CAN FD [S13] | many | TrustZone, EdgeLock secure enclave (UNVERIFIED) | Yes (frdm_mcxn236) (UNVERIFIED) | GBP 6.96 @100 (RS UK); 91-week LT at Avnet; Farnell JP shows "No Longer Manufactured" for VDFT [S13] | ~800 | Too expensive for a fieldbus card; only if baseboard MCU role |

NXP MCX A family table (NXP series page): A13x no CAN; A14x/A15x "optional CAN"; A17x/A25x/A34x/A35x/A36x 1x CAN; A18x/A26x/A28x/A5x 2x CAN; all Cortex-M33 [S14]. MCX A pages state they are covered by NXP's Product Longevity programme (minimum 10 years; 15 years for designated parts) but the per-part years were not visible without the live table [S14][S16].

Longevity: ST runs a 10-year rolling longevity programme for STM32, renewed annually; STM32C0 explicitly covered at launch [S15]; STM32H523/H533 listed to Jan 2035 per ST staff [S15]. Per-part G0B1 entry not verified (UNVERIFIED, ST site timed out).

## 4. RS-485, CAN-FD, isolation and protection parts

All INR at 93.9/USD. "@1k" = 1,000+ break unless stated. LCSC figures are search-indexed snapshots (see section 2).

### 4.1 RS-485 — non-isolated (3.3 V)

| Part | Key specs | Price | INR | Source |
|---|---|---|---|---|
| SIT SIT3485ESA (SOP-8) | 3.3 V, 12 Mbps half-duplex, 256 nodes; IEC ESD not stated for this suffix (SIT3485E variants list +/-15 kV HBM) | USD 0.149 @2.5k reel; 0.165-0.18 @150+ | ~15-17 | [S20] |
| SIT SIT3485EESA (SOIC-8) | as above, "ESD protect +/-15 kV" | ~ same class (price not captured) | ~15-20 (UNVERIFIED) | [S20] |
| TI THVD1450 (SOIC-8 / VSSOP / SON) | 3.3-5 V, 50 Mbps, 16-18 kV IEC ESD (package dependent) | USD 1.51 @1k (TI direct), 1.85 @1k (DigiKey), DigiKey THVD1450D USD 1.99 @1,050 | ~142-187 | [S21] |
| TI THVD1424 / THVD24xx | 3.3-5 V, integrated switchable termination (THVD1424), IEC ESD; price not found | UNVERIFIED | — | [S21] |

Recommendation: V1 uses SIT3485EESA-class (or MaxLinear SP3485E / TI THVD1406-class) behind an external TVS + PTC/series-resistor network (4.6), because the external network, not the transceiver, provides the IEC 61000-4-5 surge rating. TI THVD14xx is ~10x the price and only worth it if a single-chip IEC-rated solution is needed for certification margin.

### 4.2 CAN-FD — non-isolated

| Part | Key specs | Price | INR | Source |
|---|---|---|---|---|
| NXP TJA1051T/3/1J (SO-8) | CAN FD up to 5 Mbps, VIO pin (/3) for 3.3 V MCU | USD 0.349 @1k (LCSC C38695; other snapshot 0.322 @2.5k) | ~30-33 | [S22] |
| TI TCAN1044VDRQ1 (SOIC-8) | CAN FD 8 Mbps, VIO 1.8-5 V, AEC-Q100 | USD 0.668 @1k (LCSC C1852061); 0.70 @1k (findchips) | ~63-66 | [S23] |
| SIT SIT1044T (SOP-8) | CAN FD 5 Mbps, 5 V supply (no VIO on this suffix; /3 suffix has VIO) | USD 0.247 @1k (LCSC C2922539); SIT1044T/3 USD 0.667 @1 | ~23 (T) / ~40-50 (T/3, UNVERIFIED @1k) | [S24] |
| JSMSEMI TJA1051T/3-JSM, HGSEMI TJA1051-3M (clones) | CAN FD 5 Mbps, ISO 11898-2:2016 claimed | USD 0.46-0.48 @1 | ~40 @1 | [S22] |
| NXP TJA1441 / TJA1462, TI TCAN3413 | not priced in this run | UNVERIFIED | — | — |

Recommendation: NXP TJA1051T/3 (genuine, ~INR 33) as default; TCAN1044V as second source. Clone parts are cheaper at qty 1 but not cheaper than genuine NXP at 1k on LCSC.

### 4.3 RS-485 — isolated

| Part | Isolation / integration | Price | INR | Source |
|---|---|---|---|---|
| Chipanalog CA-IS3082W (SOIC-16 WB) | 5 kVrms, half/full duplex; needs external isolated 5 V/3.3 V supply | not shown on LCSC; CA-IS3082WX USD 1.00-1.07 @10+; CA-IS3082WNX (SOIC-16 WB(W)) USD 0.53 @1 | ~50-100 | [S25] |
| Chipanalog CA-IS2092W / CA-IS2092VW (SOIC-16 WB) | isolated RS-485 **with integrated DC-DC** (no external module needed) | CA-IS2092W USD 1.63 @1k (another snapshot ref. 1.44); CA-IS2092VW USD 1.44 @1k | ~135-153 | [S26] |
| Novosense NSI83086 (LCSC C917445) | isolated RS-485; integrated power not confirmed in snippet | USD 1.65 @100 | ~155 @100 | [S26] |
| **Chipanalog CA-IS2092A (LGA-16 ~5.2x4.65 mm)** | half-duplex isolated RS-485 **with internal isolated DC-DC** (3.3/5 V bus side, up to 100 mA), UL 1577 2.5 kVrms, 0.5 Mbps, -40..125 C | USD 1.98 @1; LCSC ref. "from USD 1.00" (stock fluctuates 0-610) | ~94-186 | [S29] |
| TI ISO14xx / ISOW14xx, ADI ADM2587E / ADM2867E | not priced in this run; ADM2587E-class integrated-power parts are typically several USD (UNVERIFIED) | UNVERIFIED | — | — |

### 4.4 CAN / CAN-FD — isolated

| Part | Isolation / integration | Price | INR | Source |
|---|---|---|---|---|
| TI ISO1042DWVR (SOIC-8 WB / -16) | 5 kVrms class, CAN FD 5 Mbps; needs isolated bus-side 5 V | USD 0.82 @1k (LCSC C2671714), 1.53 @1 | ~77 | [S27] |
| Chipanalog CA-IS3062W | 5 kVrms, **1 Mbps classic CAN only (not FD)**; LCSC lists under "with power" | USD 2.45 @1k (snapshot; ref. 2.16) | ~203-230 | [S27] |
| Chipanalog CA-IS2062W | isolated CAN with power (listed) — price not captured | UNVERIFIED | — | [S27] |
| **Chipanalog CA-IS2062A (LGA-16 4.7x5.2)** | isolated **CAN FD 5 Mbps with built-in DC-DC**, 2.5 kVrms, 150 kV/us CMTI; Chinese datasheet marked *Preliminary* | LCSC ref. from USD 1.00; HQOnline USD 1.32 @100, 0.96 @30 (other listing) | ~94-124 | [S30] |
| TI ISOW1044 (integrated DC-DC) | isolated CAN FD with integrated power; TI flags newer ISOW1050 as cost-effective successor | ~USD 4.4 @1ku (Edinventory aggregator, UNVERIFIED) | ~413 | [S31] |
| Novosense NSiP1042 | isolated CAN with integrated DC-DC (datasheet found; no LCSC price) | UNVERIFIED | — | [S27] |
| HopeRF CMT1042 | isolated CAN (listed on LCSC) | USD 0.99 @1 | ~93 @1 | [S27] |

### 4.5 Isolated DC-DC for group isolation

| Part | Spec | Price | INR | Source |
|---|---|---|---|---|
| Mornsun B0505S-1WR3 (SIP) | 5 V -> 5 V 1 W, unregulated, 1.5 kVDC (class) | USD 0.888 @43+ (LCSC C131038), USD 1.13 @1; Mouser USD 0.63 @43 (findchips) | ~59-83 | [S28] |
| Clones (GTL-POWER, VISOM, JETEKPS, TESL-A B0505S-1WR3) | same footprint | ref. from USD 0.51 (GTL, out of stock) | ~48 | [S28] |

Group isolation (V2) = 1x B0505S-1WR3 (or 3.3 V variant) + 1x CA-IS3082W-class isolated RS-485 per port (or 1 per port if 2 ports share the module output) + 1x ISO1042 isolated CAN FD, all sharing one isolated "field ground". Note: one 1 W module (200 mA @ 5 V) easily supplies two RS-485 + one CAN transceiver at typical (non-fully-loaded) bus currents, but a fully loaded 32-unit-load RS-485 bus at 54 ohm can draw ~60 mA per driver while transmitting — verify the budget (UNVERIFIED rule of thumb).
Per-port isolation (V3) = CA-IS2092A (RS-485 + DC-DC) per RS-485 port + CA-IS2062A (CAN FD + DC-DC) — no external module, smallest area, but LGA packages (inspect with X-ray/AOI) and the CA-IS2062A datasheet is still marked preliminary.

### 4.6 Surge/ESD protection, termination and bias (per port)

Target IEC 61000-4-2 (+/-8 kV contact), -4-4 (+/-2 kV burst, capacitive clamp) and -4-5 +/-1 kV line-to-ground on RS-485 and CAN.

- Littelfuse layered recommendation for RS-485: indoor/intra-building = resettable PPTC + SM712 TVS array; outdoor/harsh = PPTC + GDT (+ SIDACtor/TVS), with PPTC resistance chosen for coordination [S32].
- TI THVD2412/THVD2442 datasheet gives a 1 kV IEC 61000-4-5 surge protection circuit using bidirectional SMAJ30CA-class 400 W TVS [S33]. TI TIDA-060027 uses PTC (160 mA trip) + SIDAC to survive 70 V DC / 120 V AC mis-wiring [S33].
- SM712 (asymmetric -7/+12 V, 400 W SOT-23, made for RS-485): LCSC second-source parts USD 0.03-0.06 (DOWO C293966 USD 0.030 @100, 217k stock; TDSEMIC USD 0.063 @10; JUXING USD 0.029 @20); Semtech original GBP 0.73 @250 (RS UK) [S34]. Clamping voltages differ by maker — check datasheet.
- For CAN: use a CAN-specific 2-line TVS (e.g. NUP2105L / ESD2CAN class, SOT-23) — price not captured (UNVERIFIED, assume ~INR 3-6).

Per-port protection budget used in section 6 (V1, non-isolated): SM712-class TVS (~INR 3-5) + 2x PPTC or 2x 10 ohm pulse-rated resistors (~INR 4-8) + common-mode choke optional (not included) + switchable 120 ohm termination via 2-pole DIP switch or FET (~INR 6-10, UNVERIFIED) + 2x bias resistors (~INR 0.3) = **~INR 15-25 per port** (component prices UNVERIFIED except SM712). A GDT stage (outdoor/long-line variant) adds ~INR 10-20 per port (UNVERIFIED).

## 5. Ethernet short table (for the combined 4G + Ethernet + Wi-Fi module)

Ethernet is no longer on this module. The web-search budget for this run ran out before the RMII PHYs could be priced, so this table reuses figures already sourced in R02 (same session family) and marks the rest UNVERIFIED.

| Option | Type | Price | INR | Notes / source |
|---|---|---|---|---|
| WCH CH390H (QFN-32) | SPI 10/100 MAC+PHY | LCSC USD 0.97 @490; HQOnline USD 0.82 @490 | ~77-91 | Cheapest SPI Ethernet; ESP-IDF driver exists; Zephyr driver status UNVERIFIED [R02 ref 38] |
| WIZnet W5500 | SPI, hardwired TCP/IP + MAC + PHY | ~USD 1.75-2.09 @1k | ~164-196 | Zephyr driver upstream (`wiznet,w5500`) — UNVERIFIED in this run [R02 ref 39] |
| RMII PHY (LAN8720A / LAN8742A / DP83825I / RTL8201F / YT8512 / IP101GR / KSZ8081) | needs MCU with RMII MAC | not priced in this run | UNVERIFIED | Only relevant if the 4G+Eth+Wi-Fi module host MCU has a MAC |
| HanRun HR911105A RJ45 w/ magnetics | connector | Hubtronics INR 74.58 + GST (1 pc); Evelta INR 150.63 (10-99) | ~75 (1 pc); 1k price UNVERIFIED | [R02 ref 40] |
| Ethernet ESD/surge, PoE-PD | — | not researched in this run | UNVERIFIED | — |

R02 sources: https://www.lcsc.com/product-detail/C7498452.html ; https://www.lcsc.com/product-detail/C32843.html ; https://hubtronics.in/connectors/modular-sockets-rj45-rj11/1815

## 6. Costed BOMs — Architecture A and Architecture B, variants V1 / V2 / V3

Basis: INR at 93.9/USD; 1k qty; finished = BOM x 1.4; target BOM <= ~INR 714 (finished <= INR 1,000). Given assumptions from the brief: 40-pin connector INR 60, local power stage (12-24 V buck + Li-ion charger/protection + 3.3 V) INR 90. Lines marked * are estimates that could not be source-checked in this run (search budget exhausted): crystal, terminals, PCB, passives, CAN TVS, PPTC/termination switch.

Per-port protection used: ~INR 20 per port (SM712-class TVS or CAN TVS + 2x PPTC / pulse resistors + switchable 120 ohm termination + bias) — section 4.6.

### 6.1 Architecture B — enclosed fieldbus module with own MCU (CAN-FD + 2x RS-485)

| Line | V1 non-isolated, protected | V2 group-isolated | V3 per-port isolated |
|---|---|---|---|
| MCU — ST track STM32G0B1 (C2847904, ~INR 109) | 109 | 109 | 109 |
| Crystal 8 MHz + caps* (CAN-FD needs accurate clock) | 6 | 6 | 6 |
| RS-485 x2 | 2x SIT3485EESA = 34 | 2x CA-IS3082W(NX)-class ~50 = 100 | 2x CA-IS2092A ~140 = 280 |
| CAN-FD x1 | TJA1051T/3 = 33 | ISO1042 = 77 | CA-IS2062A ~110 |
| Isolated DC-DC | — | B0505S-1WR3 ~70 + isolated-side LDO* 5 = 75 | integrated (0) |
| Protection 3 ports | 60 | 60 | 60 |
| Field terminals (3x 3-pin pluggable + power 2-pin)* | 40 | 40 | 40 |
| 40-pin bus connector (given) | 60 | 60 | 60 |
| Power stage 12-24 V + Li-ion + 3.3 V (given) | 90 | 90 | 90 |
| 4-layer PCB ~50x60 mm @1k* | 40 | 40 | 40 |
| Passives, LEDs, debug header, misc* | 35 | 40 | 35 |
| **BOM — ST track (G0B1)** | **~507** | **~697** | **~830** |
| Finished (x1.4) | ~710 | ~976 | ~1,162 |
| **BOM — ST cheapest (C092, ~INR 85)** | ~483 | ~673 | ~806 |
| **BOM — NXP track (MCXA156VLL ~INR 197)** | **~595** | **~785** | **~918** |
| Finished NXP (x1.4) | ~833 | ~1,099 | ~1,285 |

Fits <= INR 714 BOM: V1 on both tracks (ST with ~INR 200 margin, NXP with ~INR 120); V2 only on the ST track and only just (~INR 17 margin — no headroom for price swings, RS-232 or a second bus connector); V3 does not fit on either track.

### 6.2 Architecture A — fieldbus hosted by the baseboard MCU (adder to the baseboard)

Only transceivers, protection, terminals and some extra PCB area are added; no MCU, crystal, connector, power stage or enclosure.

| Line | V1 | V2 | V3 |
|---|---|---|---|
| RS-485 x2 | 34 | 100 | 280 |
| CAN-FD x1 | 33 | 77 | 110 |
| Isolated DC-DC + LDO | — | 75 | — |
| Protection 3 ports | 60 | 60 | 60 |
| Terminals (3x 3-pin)* | 30 | 30 | 30 |
| Extra baseboard PCB area + passives* | 20 | 25 | 20 |
| **BOM adder** | **~177** | **~367** | **~500** |
| Finished adder (x1.4) | ~248 | ~514 | ~700 |

Condition: the baseboard MCU (R08) must have >= 1 CAN-FD controller and >= 3 free UARTs; field wiring then lands on the baseboard enclosure.

### 6.3 Trade-off recommendations

1. **Isolation as a premium assembly variant**: ship V1 (well protected, non-isolated) as standard; V2 group isolation as a "-ISO" variant on the same PCB (footprints for isolated parts on a separate field-ground island, or a pin-compatible daughter footprint). V3 only on request (finished > INR 1,000).
2. **One RS-485 by default** saves ~INR 45-55 BOM in V1 (transceiver + protection + terminal) and ~INR 70 in V2; keep the second port as an assembly option. Most remote-node use cases (Modbus RTU master to one field bus) need one port.
3. **Architecture A is the cheapest per system** (~INR 177 BOM adder for V1) but puts field wiring and surge energy on the baseboard and couples the brain to the fieldbus; Architecture B (~INR 500-600 BOM) gives a standalone Modbus/CAN remote node and keeps surges away from the secure brain. A pragmatic split: baseboard hosts **one** non-isolated RS-485 (A-V1, ~INR 70 adder), and the enclosed fieldbus module (B) is sold for CAN-FD + 2x RS-485 + isolation.
4. **Stacking-bus connector risk**: with pass-through stacking each module probably needs two connectors (in + out). At INR 60 each this adds ~INR 60 to every B variant (V1 ST ~567, NXP ~655 — still fits; V2 ST ~757 — no longer fits). See R07.
5. **Ethernet removed**: no PHY/RJ45/magnetics on this module saves roughly INR 150-270 versus the original brief (CH390H/W5500 + RJ45 figures from section 5).

## 7. Protocol stacks and memory sizing

No Ethernet on this module, so TCP/IP-based stacks (Modbus TCP, EtherNet/IP, PROFINET, OPC UA, IEC 60870-5-104, BACnet/IP, MQTT/TLS) belong on the baseboard or the 4G + Ethernet + Wi-Fi module, not here. The fieldbus module needs serial and CAN stacks only.

| Stack | Zephyr | ThreadX | License / type | Notes / source |
|---|---|---|---|---|
| Modbus RTU (client + server) | **Upstream** subsystem; RTU over serial (RS-485/RS-232); TCP not implemented directly, helper functions + TCP-to-serial gateway sample exist [S35] | Not native; third-party/commercial (UNVERIFIED) | Apache-2.0 | Footprint not published [S35] |
| CANopen | CANopenNode via CANopenNodeZephyr glue, pulled in as an external west project (not in-tree) [S36] | CANopenNode is RTOS-agnostic (port effort UNVERIFIED) | Apache-2.0 (both) [S36] | CAN-FD (CANopen FD) not mentioned [S36] |
| J1939 | No upstream Zephyr stack found (UNVERIFIED); commercial stacks exist (UNVERIFIED) | — | — | — |
| BACnet MS/TP | bacnet-stack supports MS/TP and BACnet/IP; Zephyr port lives in a separate repository [S37] | port effort UNVERIFIED | GPL-2.0-or-later WITH GCC exception (linking exception) [S37] | No footprint figures [S37] |
| DLMS/COSEM | not researched (UNVERIFIED; e.g. Gurux open-source, commercial stacks) | — | — | Usually on a metering gateway, not this module |
| OPC UA (open62541) | — (needs TCP/IP, not on this module) | — | MPL-2.0, "free of charge – even for commercial use" [S38] | No footprint figure on site [S38] |
| ThreadX itself | — | Eclipse ThreadX, MIT licence, actively maintained repo (docs for 6.5.1) [S39] | MIT | Certifications not stated on repo page [S39] |

Memory sizing (estimates, UNVERIFIED — no footprint figures are published by the stack projects):
- Zephyr kernel + UART + CAN drivers + Modbus RTU + CANopenNode + MCUboot-compatible image: plan ~80-120 KB flash, ~20-32 KB RAM per image.
- Secure field update needs MCUboot (~32-48 KB) + two image slots (or swap) -> **>= 256 KB flash recommended, 512 KB comfortable; >= 32 KB RAM minimum, 64 KB+ preferred** (CANopen OD + Modbus buffers + 2x UART DMA buffers + logging).
- Consequences: STM32G0B1**CB** (128 KB) is too small for dual-slot OTA — use **STM32G0B1CC (256 KB) or CE (512 KB)** (price delta UNVERIFIED, expect +INR 10-30); STM32C092**KC/CC** (256 KB) fits flash but its 36 KB RAM is tight; MCXA156 (1 MB / 128 KB) is comfortable.

## 8. RS-232 and other wired interfaces (cost notes)

Not priced in this run (search budget exhausted) — all figures UNVERIFIED estimates:
- **RS-232 assembly option**: 3.3 V charge-pump transceiver (MAX3232/SP3232-class, ~INR 10-25) + TVS + 3-pin terminal ~INR 25-40 BOM; uses a third UART (G0B1: 6 USART, C092: 4, MCXA156: 5 LPUART — all sufficient). Can share terminals with RS-485 #2 as a "RS-485/RS-232 selectable" assembly option.
- **Second Ethernet / switch**: belongs on the 4G + Ethernet + Wi-Fi module (e.g. 3-port switch), not here.
- **M-Bus (meter bus) master**: needs a ~36 V bus supply and level converter (TI TSS721A is slave-only; master front-ends are discrete) — typically INR 150-300 extra; separate option card recommended.
- **10BASE-T1L**: single-pair Ethernet PHYs (ADI ADIN1100/ADIN1110 class) are several USD and need a MAC/SPI — cost likely > INR 300; future premium card, not this module.

## 9. Risks and open decisions

Risks
1. **Security on low-cost MCUs**: STM32C0/G0 and MCXA156 have no TrustZone or crypto accelerator found in the sources; the module relies on signed firmware (MCUboot software ECDSA) with keys anchored in the baseboard secure element (product-owner decision 1). CRA: the module must still support secure update and vulnerability handling; document the module as a component of the baseboard's security boundary.
2. **NXP MCXA156 lead time**: Avnet showed 112 weeks factory lead time, Future 16 weeks [S10]; only the LQFP100 price was found. LQFP64/HVQFN48 variants need pricing.
3. **Chipanalog LGA isolated parts**: CA-IS2062A datasheet marked preliminary; LGA needs X-ray/AOI; LCSC stock fluctuates (0-3,000).
4. **Price snapshots**: LCSC tiers could not be fetched live; all distributor prices are search-indexed snapshots (+/-15 %).
5. **Pass-through connector**: two connectors per module may push V2 out of budget (6.3.4).
6. **CA-IS3062W is classic CAN (1 Mbps) only** — do not use it for CAN-FD.

Open decisions
- Architecture A vs B (or the hybrid in 6.3.3).
- One vs two RS-485 ports by default.
- Isolation offering: V1 standard + V2 premium (recommended) vs V3.
- G0B1CC/CE vs C092 for the ST track (flash/RAM vs cost); MCXA156 vs a smaller MCX A14x with CAN for NXP (not priced).
- ThreadX support: ST/NXP SDK support for ThreadX on G0/C0/MCX A not verified — recommend Zephyr-only for this module.

## 10. Sources

(accessed 2026-11-13 / 2026-11-14)
- S1 https://currencybeacon.com/rates/USD/INR
- S2 https://hdfcsky.com/news/rupee-rises-24-paise-to-93-74-against-us-dollar-in-early-trade ; https://hdfcsky.com/news/rupee-falls-10-paise-to-close-at-94-86-against-us-dollar
- S3 STM32C091/C092 datasheet DS14720 (Apr 2025), mirror https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/7132/stm32c092rc.pdf ; product page https://www.st.com/en/microcontrollers-microprocessors/stm32c092kb.html
- S4 https://punchouttest.digikey.de/en/products/detail/stmicroelectronics/STM32C092KBT6/25935631 ; https://punchouttest.digikey.ca/en/products/detail/stmicroelectronics/STM32C092KCU6/25935635 ; https://www.digikey.com.br/en/products/detail/stmicroelectronics/STM32C092RCT6/25935639
- S5 https://www.lcsc.com/product-image/C2847904.html ; https://lcsc.com/product-detail/image/STM32G0B1CBT6_C2847904.html
- S6 https://docs.zephyrproject.org/latest/boards/st/nucleo_c092rc/doc/index.html
- S7 https://docs.zephyrproject.org/latest/boards/st/nucleo_g0b1re/doc/index.html
- S8 https://lcsc.com/product-detail/Microcontrollers-MCU-MPU-SOC_STMicroelectronics-STM32H503CBT6_C17700273.html ; https://www.findchips.com/search/stm32h503cbt6
- S9 https://www.lcsc.com/product-detail/C529355.html
- S10 https://www.avnet.com/americas/product/nxp/mcxa156vll/evolve-66937811/ ; https://www.futureelectronics.com/p/electromechanical--power-supplies--ac-dc/mcxa156vll-nxp-C000146498 ; https://www.digikey.es/en/products/detail/nxp-usa-inc/MCXA156VLL/22039743
- S11 https://docs.zephyrproject.org/latest/boards/nxp/frdm_mcxa156/doc/index.html
- S12 https://www.cnx-software.com/2025/08/29/nxp-mcx-a34-mixed-signal-cortex-m33-mcu-delivers-17x-faster-math-acceleration-for-motor-control-and-hvac-systems/ ; https://www.nxp.com/products/MCX-A34
- S13 https://uk.rs-online.com/web/p/microcontrollers/0763084 ; https://jp.farnell.com/en-JP/nxp/mcxn236vdft/mcu-1024kb-150mhz-vfbga-184/dp/4445653 ; https://www.digikey.be/en/product-highlight/n/nxp-semi/mcxn23x-cortex-m33-mcus
- S14 https://www.nxp.com/products/processors-and-microcontrollers/arm-microcontrollers/general-purpose-mcus/mcx-arm-cortex-m/mcx-a-series-microcontrollers:MCX-A-SERIES
- S15 https://newsroom.st.com/?p=7815 (STM32C0 10-year longevity) ; https://community.st.com/t5/stm32-mcus-products/stm32h533-longevity/m-p/767635
- S16 https://nxp.com/products/product-information/product-longevity
- S17 https://www.st.com/resource/en/datasheet/stm32g0b1re.pdf ; https://www.st.com/en/microcontrollers-microprocessors/stm32g0b1kb.html
- S18 https://www.st.com/en/microcontrollers/stm32h503cb.html
- S20 https://www.lcsc.com/product-detail/C313015.html ; https://www.lcsc.com/datasheet/lcsc_datasheet_1810251527_SIT-SIT3485ESA_C313015.pdf ; https://jlcpcb.com/partdetail/SIT-SIT3485EESA/C2846826/C2846826 ; https://www.lcsc.com/product-detail/C50345880.html
- S21 https://www.digikey.com.br/en/products/detail/texas-instruments/THVD1450DGK/10060471 ; https://www.digikey.com.mx/en/products/detail/texas-instruments/THVD1450D/9360695 ; https://www.electronicsdatasheets.com/manufacturers/texas-instruments/parts/thvd1450drb
- S22 https://www.lcsc.com/product-detail/C38695.html ; https://www.lcsc.com/product-detail/C49450397.html ; https://www.lcsc.com/product-detail/C51484082.html
- S23 https://www.lcsc.com/product-detail/C1852061.html ; https://www.findchips.com/search/an1044 ; https://www.tme.com/us/en-us/details/tcan1044vdrq1/can-interfaces-integrated-circuits/texas-instruments/
- S24 https://lcsc.com/product-detail/CAN-Transceivers_SIT-SIT1044T_C2922539.html ; https://lcsc.com/product-detail/CAN-Transceivers_SIT-SIT1044T-3_C2922538.html
- S25 https://lcsc.com/product-detail/RS-485-RS-422-ICs_Chipanalog-CA-IS3082W_C528766.html ; https://lcsc.com/product-detail/Isolated-RS-485-422-Transceivers_Chipanalog-CA-IS3082WX_C970942.html ; https://www.lcsc.com/product-detail/C7422548.html
- S26 https://lcsc.com/product-detail/Isolated-RS-485-422-Transceivers-with-power_Chipanalog-CA-IS2092W_C5121950.html ; https://www.lcsc.com/product-detail/C7422559.html ; https://www.lcsc.com/product-image/C917445.html
- S27 https://www.lcsc.com/product-detail/C2671714.html ; https://lcsc.com/product-detail/Isolated-CAN-Transceivers-with-Power_Chipanalog-CA-IS3062W_C2890050.html ; https://lcsc.com/product-detail/Isolated-CAN-Transceivers-with-Power_Chipanalog-CA-IS2062W_C5121953.html ; https://www.lcsc.com/product-detail/C32710688.html
- S28 https://datasheet.lcsc.com/szlcsc/MORNSUN-Guangzhou-S-T-B0505S-1WR3_C131038.pdf ; https://origin-www.findchips.com/search/B0505S-1WR3 ; https://www.lcsc.com/product-image/C497204.html
- S29 https://www.lcsc.com/product-detail/C18185406.html ; https://datasheet.lcsc.com/lcsc/2401261510_Chipanalog-CA-IS2092A_C18185406.pdf ; https://www.lcsc.com/blog/chipanalog-ca-is2092a-isolated-rs-485-transceivers-with-integrated-dc-dc-converter/
- S30 https://www.lcsc.com/product-detail/C22438481.html ; https://www.hqonline.com/product-detail/isolated-can-transceivers-chipanalog-ca-is2062a-2500421290 ; https://lcsc.com/datasheet/lcsc_datasheet_2405231529_Chipanalog-CA-IS2062A_C22438481.pdf
- S31 https://www.edinventory.com/parts/isow1044bdfmr_texas-instruments ; https://www.ti.com/product/ja-jp/ISOW1044
- S32 https://alternativeenergy.yodify.com/Documentation/Document/ejmnGZ/LFUS-LIN-RS485-and-Ethernet-Protection-Spotlight.pdf
- S33 https://ti.com/document-viewer/THVD2442/datasheet/GUID-4726F0DE-D3DB-49CC-90F9-ACC3892036FF ; https://www.ti.com/tool/TIDA-060027 ; https://ti.com/lit/pdf/TIDUER9
- S35 https://docs.zephyrproject.org/latest/services/connectivity/modbus/index.html
- S36 https://docs.zephyrproject.org/latest/develop/manifest/external/canopennode.html
- S37 https://github.com/bacnet-stack/bacnet-stack
- S38 https://www.open62541.org/
- S39 https://github.com/eclipse-threadx/threadx
- S40 Datasheets downloaded to ../datasheets/industrial/ (see INDEX.md): TI ISO1042 (SLLSF09F, Aug 2026: CAN FD 5 Mbps, 5000 Vrms, +/-16 kV HBM bus ESD, +/-30 V CM), TI THVD1450 (+/-18 kV IEC 61000-4-2 contact, +/-4 kV IEC 61000-4-4), TI TCAN1044V (2/5/8 Mbps), Mornsun B_S-1WR3 (1.5 kVDC, up to 85 % eff.), ST STM32C092 DS14720
- S34 https://www.lcsc.com/product-detail/C293966.html ; https://www.lcsc.com/product-detail/C46956321.html ; https://www.lcsc.com/datasheet/lcsc_datasheet_2305311119_JUXING-SM712_C5243888.pdf ; https://uk.rs-online.com/web/p/tvs-diodes/6910811
