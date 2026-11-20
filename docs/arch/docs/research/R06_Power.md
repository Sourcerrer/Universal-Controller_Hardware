# R06 — Power Architecture: Component Selection Report

> **Owner decision 2026-11-14: Mornsun parts are banned (PRD COMP-6).** Every Mornsun part recommended below is withdrawn; see the PRD for replacements.


Status: COMPLETE (with UNVERIFIED items flagged); finished 2026-11-14
Date: 2026-11-14
Scope: module power block (12–24 V + single-cell Li-ion), baseboard AC-DC and DC front end, stacked pass-through bus power distribution, hold-up, RTC backup, power budget.

Conventions
- Prices are unit prices at about 1k quantity unless stated, with distributor and date. INR conversion rate: about INR 93.7 per USD (section 11).
- Anything not confirmed against a primary source is marked UNVERIFIED.
- Finished cost = BOM x 1.4 (product-owner decision, 2026-11-13).

## 1. Executive summary and recommendation

1. Module power block, two stages on every card: wide-VIN buck to 5 V, then a single-cell charger whose power path feeds the 3.3 V rail. Lowest-cost tier: Schottky diode-OR (terminal + bus), PTC, SMBJ33A, Diodes AP64200 (40 V, 2 A, USD 0.48), TP4056-class charger, DW01A+FS8205A if raw cells, 3.3 V LDO. About INR 90-100 per non-cellular card.
2. Cellular "4G + Ethernet + Wi-Fi" card: the power-path SYS rails of BQ24074 (4.4 V) and BQ25185 (4.5 V) are above the 4.3 V VBAT limit of Cat-1 modems. Use TI LMR51430 (36 V, 3 A, USD 0.50) to 5 V, then TI BQ25601 NVDC charger (3 A, VSYS 3.5 V-VBAT, JEITA, USD 0.47) feeding modem VBAT directly. About INR 160. A no-battery SKU can use LMR51430 set to 3.8 V (about INR 70).
3. Preferred-vendor tier (TI throughout): LM74700 ideal-diode inputs, optional TPS26621 module eFuse (INR 152 at 3k), LMR51420/51430, BQ25185 or BQ25601/BQ25622, BQ29700, optional MAX17048. About INR 250-305 without options and 530-585 with them. This does not fit the Wi-Fi card's INR 430 BOM, so use it selectively.
4. AC-DC (assembly option): Mean Well IRM-20-24, which has IEC/UL 62368-1, 4.2 kVAC isolation, EN 55032 Class B with no extra parts and 2 kV surge. DigiKey India lists it at INR 799 for 25 pcs but it is out of stock until Jan-2027. Second source: Mornsun LDE20-20B24 (IEC 62368-1, 4 kVAC, Class B, -40..+70 C, USD 8.5-9.1). No BIS registration was found for any PCB-mount module. Hi-Link has no verified certification, so use it for prototypes only.
5. Baseboard DC front end: SMCJ33A, then TPS2660 eFuse (60 V, reverse polarity to -60 V, OVP cut-off at about 33 V to protect the 36-40 V bucks; INR 196 at 2k), then the CM/pi EMI filter, then VBUS.
6. Stacked bus: the first joint carries the whole stack's current, up to 0.83 A at 24 V, 1.67 A at 12 V and 2.22 A at 9 V. Use 4 VBUS + 4 GND contacts and prefer a 24 V bus. Voltage drop over 6 modules is 0.1-0.3 V. Every input is diode-ORed so no module back-feeds the bus. Live insertion should be "not supported but survivable".
7. Hold-up: the Li-ion cell (when fitted) is the last-gasp source. No-battery SKUs need 2 x 10 F supercaps plus a buck-boost (about 40 J, more than 10 s; about INR 260-300). PFAIL comparator on the baseboard input drives a bus line.
8. RTC: CR2032 on the baseboard only (INR 87.5). Power budget: about 9 W average and 15-20 W peak for a 6-card stack, so a 24 V / 20 W supply is enough with charging limited by firmware (otherwise 30 W).
9. Main risks: LCSC prices are search snapshots; 26-week TI eFuse lead times; Li-ion charging is blocked in 60-70 C cabinets; surge margin of 36-40 V bucks in standalone use.

## 2. Module power block

### 2.1 Wide-VIN buck converters

- TI LMR36506: 3-65 V in, 0.6 A, 2x2 mm VQFN-HR, 4 uA Iq, Tj -40..150 C, ACTIVE; datasheet Rev C Jan 2026 [S1, S2]. 1ku price NOT on TI page; aggregator values conflict (~USD 0.75-1.55) so UNVERIFIED.
- TI LMR51420: 4.5-36 V, 2 A, 40 uA Iq, SOT-23-6 (DDC), ACTIVE [S10]. LCSC C5383002 1k+ ~USD 0.60-0.64 (two snapshots, one out of stock; seen via search 2026-11-14) [S11].
- TI LMR51430: 4.5-36 V, 3 A, SOT-23-6 [S12]. LCSC C5185863 (XDDCR) 1k+ USD 0.4962 (8,872 stock, snapshot; another snapshot 100+ USD 0.58) [S13]. Best fit for the 3.8 V / 2 A-peak cellular rail.
- TI TPS560430: 4-36 V, 0.6 A, 80 uA Iq, SOT-23-6, Active [S14]. Price not captured.
- Diodes AP64200SP-13: 3.8-40 V, 2 A, SO-8EP; LCSC C3192345 1k+ USD 0.4846 [S15]. AP63205WU-7 (fixed 5 V, 3.8-32 V, TSOT-23-6) LCSC 1k+ USD 0.1878 - 32 V max is too low for 24 V systems with surge.
- ST L6983 (3.5-38 V, 3 A, QFN): RS UK 1000+ GBP 1.146 (L6983N50QTR, out of stock, restock Sep-2026 per listing); RS IE EUR 1.708-1.764 [S16]. ST L6981 (3.5-38 V, 1.5 A, SO-8, 20 uA Iq): LCSC C3192320 100+ USD 2.42 (11 in stock) [S17]. ST L7983 (60 V, 0.3 A, DFN10): DigiKey USD 2.26-2.38 (1 pc); element14 CN CNY 10.14 at 2500+ [S18]. ST parts are 2-4x the TI/Diodes price at this level.
- Low-cost Asian: Silergy SY8303AIC LCSC C97054 100+ USD 0.39 (17k stock; package and VIN not confirmed in this run, UNVERIFIED) [S19]; SCT SCT2432STER (3.8-40 V, 3.5 A, ESOP-8) LCSC ~USD 0.78-1.31 (1 pc) [S19].
- Design note: with a 33 V TVS (SMBJ33A clamps at ~53 V at Ipp) a 36-40 V buck is NOT protected by the TVS alone; it must sit behind an eFuse/OVP cut-off (e.g. TPS2660 OVP pin) or be a 60-65 V part (LMR36506/LMR36503, L7983). See 3.2.
### 2.2 Single-cell Li-ion chargers

- TI BQ24074: power-path charger, up to 1.5 A, NTC input, input OVP, battery supplements system on load peaks [S5]. IN is a 5-6 V class input (not 12-24 V): needs a pre-regulated 5 V rail. (Confirm exact IN abs max in datasheet; datasheet saved.)
- TI BQ25185: 3.0-18 V in, 30 uA input Iq sleep, selectable 100/500/1100 mA input limit, power-path [S6]. 18 V max means it also needs a buck pre-regulator at 24 V systems.
- Corrections/confirmations from the local datasheets (2026-11-14): BQ24074 IN abs max 28 V, VOVP 10.5 V (10.2-10.8 V) for the '74 variant (6.6 V for '72/'73/'75), OUT regulated at 4.4 V, BAT discharge 5 A, charge 1.5 A max [S5]. BQ25185: VIN operating 3.6-18 V, abs max 25 V, SYS regulation 4.5 V, IQ_BAT 4-5 uA, 3.2 uA in factory (ship) mode, BAT-to-SYS discharge 3.125 A [S6].
- Important for the cellular module: power-path SYS rails of BQ24074 (4.4 V) and BQ25185 (4.5 V) exceed the typical LTE Cat-1 VBAT maximum of 4.3 V (Quectel EG915U: 3.3-4.3 V, see R02). The modem must therefore run from an NVDC switching charger (VSYS tracks the battery) or from a dedicated 3.8 V buck ORed with the cell.
- Prices (LCSC unless noted; from search snapshots 2026-11-14, USD):
  - TP4056 (TOP POWER, C16581, ESOP-8): 500+ 0.106, 2500+ 0.089; clones (GOODWORK C21713961, JSMSEMI C22470410, TDSEMIC C42422118) 1k+ about 0.029-0.032 [S20]. Caveats: input abs max 8 V (UNVERIFIED in this run), no power path, no input OVP, NTC window fixed by resistor divider, quality varies by clone maker.
  - TI BQ25170DSGR (C5208201): ACTIVE on TI (one LCSC snapshot shows an NRND flag; TI product page says ACTIVE) [S21]; 3-6.5 V operating, 30 V tolerant input, 6.6 V OVP, up to 800 mA, Li-ion/LiFePO4, NTC hot/cold (JEITA in BQ25170J), 350 nA battery leakage, no power path (load in parallel with cell); LCSC 1k+ about 0.32-0.34; BQ25170J (JEITA, C3682876) 1k+ 0.533 [S21, S22].
  - Microchip MCP73831T-2ACI/OT (C424093): 1k+ 0.374-0.435 (two snapshots) [S23]. 6 V-class input, no power path, no NTC.
  - Microchip MCP73871 (power path, QFN-20): LCSC -1CCI/ML 1k+ 3.97 (outlier); findchips 1k about 1.77 [S24]. Too expensive.
  - ST L6924D013TR (C155635): 1k+ about 0.395-0.455 (snapshots) [S25]. ST STBC15: NRND per ST page and only 40 mA (thin-film batteries) - not suitable [S26].
  - TI BQ24074RGTR (C54313): 1k+ 0.9858 (only 191 in stock in snapshot) [S27].
  - TI BQ25185DLHR (C19725033): 1k+ about 1.12 [S28].
  - TI BQ25620/BQ25622: I2C, 3.5 A, max 18 V input, NVDC power path, WQFN-18; ACTIVE; price not found in this run (UNVERIFIED) [S29].
- TI BQ25601RTWR (C468236): ACTIVE; I2C 1-cell 3 A buck charger, NVDC power path, VIN 3.9-13.5 V (VBUS abs max 22 V, limited to 1 h per datasheet [S60]), VSYSMIN 3.5 V programmable, JEITA, WQFN-24 4x4; TI names BQ25622 as the newer version (different pin-out). LCSC 1k+ USD 0.4723 (one snapshot; other snapshots higher) [S30, S31]. BQ25620RYKR LCSC 100+ USD 1.34 [S31]. NVDC keeps VSYS between VSYSMIN and ~VBAT, which matches the 3.3-4.3 V VBAT window of Cat-1 modems - the right topology for the cellular module, but VIN max 13.5 V means a pre-buck (to 5 V) is still required from 12-24 V.

### 2.3 Cell protection

| Option | What it is | Price (LCSC, USD, snapshot 2026-11-14) | Notes |
|---|---|---|---|
| DW01A + FS8205A (dual N-FET, 20 V) | classic 1-cell protector + dual FET | DW01A 0.012-0.023 (200-600+, Slkor/HL/YONGYUTAI); FS8205A (TECH PUBLIC) 300+ 0.033, 3000+ 0.032 [S32] | many clone vendors; thresholds (OV ~4.3 V, UV ~2.4 V, OC by FET Rds) vary by clone - pick one vendor and qualify; short-circuit response is fine for small cells |
| TI BQ29700 (BQ2970 family) + external dual FET | 1-cell protector, WSON-6 1.5x1.5 | DSER 500+ 0.17-0.26; DSET 1k+ 0.48 (snapshots disagree); DigiKey ~0.71 [S33] | tight thresholds, TI longevity; FET extra (~0.03-0.10) |
| Protected 18650 cell (PCM inside the can or tab-welded PCM) | cell maker's PCM | cost difference UNVERIFIED | simplest for IEC 62133-2 if the pack is bought certified; avoids on-board PCM |

Recommendation: put the protector on the battery pack (cell + PCM + NTC + polarised connector) bought as an IEC 62133-2 / UN 38.3 certified pack, and keep the board-side charger's own protections (OVP, timers, TS) as the second layer. If raw cells are used, DW01A+FS8205A (lowest cost) or BQ29700 + dual FET (preferred vendor) on the module.

### 2.5a Fuel gauges (prices)

| Part | Type | Price (LCSC 1k+, USD, snapshot) | Notes |
|---|---|---|---|
| ADI/Maxim MAX17048G+T10 | ModelGauge (voltage based), no sense resistor, I2C, TDFN-8 2x2 | LCSC "from" 1.345 (5.2k stock); Mouser top break 1.86 [S34] | ~3 uA hibernate (from datasheet, UNVERIFIED in this run) |
| TI BQ27441-G1A | Impedance Track, sense resistor, SON-12 | 1k+ 0.83 (G1A), 1.07 (G1B); Mouser 1k 1.26 [S35] | best accuracy; more firmware setup |
| Cellwise CW2015CHBD | voltage-based gauge, I2C | 1k+ 0.66 (0 stock at capture) [S36] | cheapest dedicated gauge; Chinese vendor, check longevity |
| No gauge: MCU ADC + divider (switched) | voltage monitor | ~0.01 | adequate for "battery OK / low / critical"; the baseboard MCU or module MCU already has an ADC |

Recommendation: lowest-cost tier uses a switched resistor divider into the module MCU ADC (FET-switched to avoid ~uA drain); preferred tier fits MAX17048 only on battery/solar remote-node SKUs (assembly option).

### 2.4 Ideal diode / OR-ing / reverse polarity

- TI LM74700-Q1: 3.2-65 V, -65 V reverse rating, 80 uA Iq, external N-FET, active ORing [S7]. LCSC C2941042 (LM74700QDBVRQ1) 1k+ USD 0.3736 (6.6k stock); DigiKey 1k USD 0.99 [S37]. Plus a 60 V N-FET (~USD 0.05-0.15, UNVERIFIED generic estimate).
- ADI/Maxim MAX40200 (1 A ideal diode, 1.5-5.5 V only): LCSC MAX40200AUK+T 1k+ USD 0.31; ANS+T 1k+ 0.41 [S38]. Only usable on the low-voltage side (e.g. ORing the Li-ion cell with a 3.8-5 V rail at <= 1 A), NOT on the 12-24 V input. For the 2 A GSM rail a P-FET + driver is needed.
- Discrete P-FET reverse-polarity (gate to GND via resistor, 12-15 V zener gate clamp): needs a -60 V part because a 24 V bus with a 33 V TVS can see ~50 V. Example Diodes DMP6023LE-13 (-60 V, SOT-223) LCSC from USD 0.24 at 5k [S39]; DMP6023LFGQ-7 1k+ 0.287 [S39]. -30 V AO3407-class parts (LCSC ~0.016) are NOT adequate for 24 V systems [S39].
- Trade-off: P-FET costs about USD 0.25 + zener + resistor and has no reverse-current blocking (back-feed); LM74700 + N-FET costs about USD 0.45-0.55 but blocks reverse current in < 1 us, which also solves back-feeding into the bus when a module is powered locally (section 4).
- Cheapest of all: a Schottky diode-OR (one diode from the 2-pin terminal, one from the bus) gives reverse polarity protection, OR-ing and back-feed blocking in one part, at ~0.3-0.5 V drop (0.15-0.25 W at 0.5 A). Acceptable for modules drawing < 0.5 A from the input (Wi-Fi, LoRa, fieldbus). Use a 60 V, 2-3 A SMA/SMB Schottky (e.g. SS36/SS56 class; price about USD 0.01-0.03 - UNVERIFIED in this run, search budget exhausted).

### 2.5 Fuel gauges
See table 2.5a above.

### 2.6 Recommended block — "lowest cost" tier

Block diagram (non-cellular modules: Wi-Fi/BLE, LoRa, fieldbus):

    2-pin terminal --Schottky--+
                               +-- PTC -- SMBJ33A -- AP64200 buck (5.0 V) -- TP4056-class charger (BAT) -- protected cell pack
    40-pin bus V+ --Schottky---+                                   |               |
                                                                   +-- P-FET load-share (5 V -> SYS) / cell -> SYS (Schottky or P-FET)
                                                                                    SYS (3.0-5 V) -- 3.3 V LDO (0.5-1 A) -- radio + MCU
                                                                    switched divider -> MCU ADC (battery voltage)

Costed BOM, non-cellular, lowest cost (1k qty; INR at 93.7/USD)

| Item | Part | USD | INR | Source |
|---|---|---|---|---|
| OR / reverse diodes (2x) | 60 V Schottky SMA | 0.04 | 4 | UNVERIFIED estimate |
| Input PTC | 0.5-1 A, 30-60 V class | 0.03 | 3 | UNVERIFIED estimate |
| TVS | SMBJ33A (GOODWORK) | - | 3 | [S51] |
| Buck to 5 V | Diodes AP64200SP-13 (40 V, 2 A) | 0.485 | 45 | [S15] |
| Buck passives | inductor 4.7-10 uH, caps, FB divider | 0.15 | 14 | UNVERIFIED estimate |
| Charger | TP4056 clone (or TOP POWER original 0.09-0.11) | 0.03-0.10 | 3-10 | [S20] |
| Load-share P-FET + Schottky + NTC | generic | 0.05 | 5 | UNVERIFIED estimate |
| 3.3 V LDO 1 A low-dropout | generic SOT-223/SOT-89 | 0.06 | 6 | UNVERIFIED estimate |
| Cell protection (if raw cell) | DW01A + FS8205A | 0.05 | 5 | [S32] |
| Battery monitor | switched divider to ADC | 0.01 | 1 | - |
| Total power block (excluding connectors, cell) | | | about INR 90-100 | |

Caveats: TP4056 has no power path and no input OVP (rely on the buck); the 5 V buck must be sized for charge current + load (AP64200 2 A is ample). Below VBAT ~3.4 V the LDO drops out; set the firmware cut-off at 3.4-3.5 V.

Cellular "4G + Ethernet + Wi-Fi" module, lowest cost:

    terminal/bus --Schottky-OR (3 A)-- SMBJ33A -- LMR51430 (5.0 V, 3 A) -- BQ25601 NVDC charger (3 A) -- VSYS 3.5-4.35 V -> modem VBAT (+ >= 470 uF low-ESR bulk)
                                                                                     |                         \-- 3.3 V buck/LDO -> Wi-Fi SoC, Ethernet PHY
                                                                               protected cell (optional)

| Item | Part | USD | INR | Source |
|---|---|---|---|---|
| OR diodes (2x, 3 A, 60 V) | Schottky SMB/SMC | 0.06 | 6 | UNVERIFIED estimate |
| TVS | SMBJ33A | - | 3 | [S51] |
| Buck 5 V / 3 A | TI LMR51430 | 0.496 | 46 | [S13] |
| Buck passives | | 0.20 | 19 | UNVERIFIED estimate |
| NVDC charger | TI BQ25601 | 0.472 | 44 | [S31] |
| Charger inductor 1-2.2 uH + caps | | 0.20 | 19 | UNVERIFIED estimate |
| Modem bulk caps (470-1000 uF tantalum/polymer) | | 0.15 | 14 | UNVERIFIED estimate |
| 3.3 V rail (buck or LDO, 0.6 A) | | 0.08 | 8 | UNVERIFIED estimate |
| Total | | | about INR 160 | |

Without a battery the BQ25601 can still power VSYS from VBUS (NVDC "instant-on with no battery" [S29, S30]); a "no-battery" SKU can drop the charger and run the modem from LMR51430 set to 3.8 V (about INR 70 total).

### 2.7 Recommended block — "preferred vendor" tier

Same topology with TI parts throughout and better protection:
- Input: LM74700-Q1 + 60 V N-FET on the bus input and on the terminal input (true ideal-diode OR, < 1 us reverse blocking, ~mV drop) [S7, S37]; TPS26621 eFuse (60 V, 0.88 A, auto-retry, IEC 62368-1 certified, UL 2367) on modules that must survive a downstream short without taking the bus down [S52, S53].
- Buck: LMR51420 (5 V, 2 A) for non-cellular, LMR51430 (5 V, 3 A) for cellular [S10-S13]. ST alternative: L6983 (38 V, 3 A) at ~2-3x the price [S16].
- Charger: non-cellular BQ25185 (power path, 18 V/25 V abs, 1.1 A input limit, TS, 3.2 uA ship mode) [S6, S28] or BQ25170J (JEITA, no power path, cheaper) [S22]; cellular BQ25601 / BQ25622 (NVDC, JEITA) [S30].
- Protection: protected certified pack; on-board BQ29700 + dual FET if raw cells [S33].
- Gauge: MAX17048 on battery SKUs [S34].

| Item | Non-cellular (INR) | Cellular (INR) | Source |
|---|---|---|---|
| TVS SMBJ33A | 3 | 3 | [S51] |
| 2x LM74700 + 2x N-FET | 88 (UNVERIFIED FET price) | 88 | [S37] |
| TPS26621 eFuse (optional, per module) | (152) | (152) | [S53] |
| Buck + passives | LMR51420 58 + 14 | LMR51430 46 + 19 | [S11, S13] |
| Charger + passives | BQ25185 105 + 5 | BQ25601 44 + 19 | [S28, S31] |
| 3.3 V rail | 8 | 8 | estimate |
| Cell protection (raw cell) | BQ29700 + FET ~25 | ~25 | [S33] |
| Fuel gauge (optional) | (126) | (126) | [S34] |
| Total without options | about INR 305 | about INR 250 | |
| Total with eFuse + gauge | about INR 585 | about INR 530 | |

Conclusion: the preferred-vendor block does not fit the Wi-Fi module (BOM <= INR 430 for everything). Use the lowest-cost block on Wi-Fi and LoRa cards, and preferred-vendor parts selectively (LM74700 on the bus input, BQ25601/BQ25622 charger) on the cellular card. A middle option for non-cellular: BQ25170 (TI, ~INR 31, 30 V tolerant input, NTC) instead of TP4056 adds ~INR 25 and removes the clone-quality risk [S21].

### 2.8 Li-ion compliance and alternatives

- IEC 62368-1 Annex M (equipment containing batteries): the equipment must keep charging voltage, current and temperature within the cell maker's limits under normal and single-fault conditions, and prevent reverse charging / excessive discharge. Practically: charger OVP + safety timer + TS (NTC) + independent protector (PCM) = two independent layers; documented single-fault analysis. (Clause content from general knowledge of the standard - UNVERIFIED in this run.)
- Cells/packs: IEC 62133-2 certified cells and packs; UN 38.3 test summary for transport (UN3480 shipped alone, UN3481 packed with/contained in equipment). India: Li-ion cells/packs fall under BIS CRS against IS 16046 (Part 2) (Indian adoption of IEC 62133-2) - UNVERIFIED in this run; check R01.
- Temperature: typical Li-ion cell datasheets allow charging 0..+45 C and discharging -20..+60 C (UNVERIFIED generic values). In a +60..+70 C panel the charger must inhibit charging (JEITA/TS) and the cell will sit at high temperature at high state of charge, which shortens life sharply. Mitigations: charge to 4.0-4.1 V instead of 4.2 V, place the cell away from heat sources, use JEITA chargers (BQ25170J, BQ25601/22) - and for hot-cabinet SKUs prefer the alternatives below.
- Alternatives:
  - LiFePO4 (3.2 V nominal, 3.6 V charge): better thermal stability and cycle life; BQ25170 and BQ25185 support LiFePO4 [S6, S21]; same 0..45 C charging window typically (UNVERIFIED).
  - LTO (2.4 V nominal): charges down to about -30 C, very long cycle life, low energy density, needs a 2.8 V charge setting and a boost for 3.3 V (UNVERIFIED generic).
  - Supercapacitors: -40..+65/85 C, no Annex M battery hazards, but only seconds of hold-up and lifetime falls fast with temperature (section 5).
  - Li-SOCl2 primary (3.6 V): -55..+85 C, very low self-discharge, ideal for ultra-low-power LoRa nodes; non-rechargeable (UN3090/UN3091), poor pulse capability (needs a hybrid layer capacitor or supercap for radio bursts) - UNVERIFIED generic.

## 3. Baseboard power

### 3.1 AC-DC mains modules

Mean Well IRM-20-24 (24 V, 0.9 A, 21.6 W; 85-305 VAC):
- Safety: IEC62368-1, IEC61558-1/-2-16, UL62368-1, TUV EN62368-1, EAC; Class II, 4.2 kVac I/P-O/P; EN55032 Class B conducted and radiated without extra parts; surge EN61000-4-5 level 4 (2 kV L-N), criteria A; 52.4x27.2x24 mm; working temp -30..+85 C with derating (DigiKey lists -30..70 C) [S3, S4].
- Price/availability: DigiKey India INR 903.55 (1 pc), 798.92 (25 pcs), OUT OF STOCK, 17 weeks lead time, next stock 15-Jan-2027 (seen 2026-11-14) [S4]. Larger-qty price UNVERIFIED. BIS registration of this model UNVERIFIED.
- LCSC C194964 lists IRM-20-24 at about USD 5.53 (1 pc, 240-pc pack) - a far lower price than DigiKey India; buy from franchised channels only because Mean Well modules are widely counterfeited (counterfeit risk: general industry knowledge, UNVERIFIED for LCSC specifically) [S40].
- Mean Well PCN says IRM-01...IRM-60 are getting a TUV EN 61558-1 label; no BIS label is mentioned for IRM, while BIS labels are listed for other Mean Well series (XLG, LPH/LPV, NGE, DIN-rail MDR/HDR/EDR/NDR) [S41]. IRM BIS status: UNVERIFIED / probably none.

RECOM RAC20-K (RAC20-24SK, 24 V / 0.84 A, 20 W) - datasheet read 2026-11-14 [S42]:
- Safety: IEC/EN/UL 62368-1 (2nd and 3rd ed.), IEC/EN 60335-1, IEC/EN 61558-1/-2-16, IEC 61347; "/NE/W" wired versions OVC III up to 5000 m.
- Isolation I/P-O/P 3 kVAC (4 kVAC for /NE/W), 1 GOhm, 100 pF.
- EMC: EN 55032 Class B WITHOUT external filter (floating output); surge EN 61000-4-5 L-N 0.5/1 kV, L-PE/N-PE 1/2 kV, Criteria A.
- Temperature: -40..+85 C with derating (full power to about +60 C for /NE/W; see derating graph). 3-year warranty. Internal fuse; /NE/W uses T2A slow-blow.
- Price: RS UK GBP 12.34 (1 pc), Buerklin EUR 14.45, Octopart USD 11.20 [S43]. 1k price UNVERIFIED. BIS UNVERIFIED (none found).

Mornsun LDE20-20B24 (24 V / 0.833 A, 20 W) - datasheet (Oct 2024) read 2026-11-14 [S44]:
- IEC/EN/BS EN 62368-1 approved, "design refer to UL 62368-1", CB report; 4000 VAC I/O isolation, reinforced insulation.
- CISPR32/EN55032 Class B CE and RE; surge IEC 61000-4-5 L-L +/-2 kV Criteria B (with the datasheet application circuit for harsh EMC: fuse, MOV, caps, TVS).
- -40..+70 C ambient with derating; external fuse required (3.15 A/250 V slow-blow).
- Price LCSC C970743: USD 11.07 (1), 9.10 (35+), 8.47 (105+), stock 0 in one snapshot [S45]. Mornsun LM50 series lists BIS among its approvals (so Mornsun does hold BIS for some series) [S46]; LDE20 BIS UNVERIFIED.

Hi-Link HLK-20M24 (24 V, 20 W):
- India retail Zbotic INR 375 incl. GST (INR 318 + GST); LCSC C465409 USD 4.48 (1), 3.94 (10+) [S47].
- Operating -20..+60 C per Indian reseller [S47]; datasheet V1.1 (2020) [S47]. No CE/UL/IEC 62368 certificate found: UNVERIFIED. Not suitable where a certified safety component is needed (CE/BIS); acceptable only for non-certified prototypes.

Traco TMPS 15-124 (15 W) / XP Power ECE20US24 (20 W): both PCB-mount encapsulated, but expensive: TMPS 15-124 DigiKey AU about USD 42 at 250 (incl. currency effects), ECE20US24 DigiKey SG SGD 57.59 at 100, 13-15 week lead times [S48]. Not recommended on cost. CUI/Same Sky PSK: not researched in this run.

AC-DC comparison (24 V, ~20 W class)

| Module | Safety | Isolation | EMC (no ext. filter) | Surge | Temp | Price | BIS |
|---|---|---|---|---|---|---|---|
| Mean Well IRM-20-24 | IEC/UL 62368-1, IEC 61558 | 4.2 kVAC | EN55032 Class B | L-N 2 kV, crit. A | -30..+85 C (derated) | DigiKey IN INR 799 (25 pc); LCSC ~USD 5.5 (1 pc) | not found |
| RECOM RAC20-24SK | IEC/UL 62368-1, 60335-1, 61558 | 3 kVAC (4 kVAC /NE/W) | Class B | L-N 1 kV crit. A | -40..+85 C (derated) | ~USD 11-16 (1 pc) | not found |
| Mornsun LDE20-20B24 | IEC/EN 62368-1 | 4 kVAC | Class B | L-L 2 kV crit. B | -40..+70 C | LCSC USD 8.5-9.1 (35-105+) | not found for LDE20 |
| Hi-Link HLK-20M24 | none found | not verified | not verified | not verified | -20..+60 C | INR 318 + GST | no |

Recommendation: Mean Well IRM-20-24 (or IRM-30-24 if the stack needs > 18 W continuous) as the default; Mornsun LDE20-20B24 as the low-cost second source with wider temperature. Neither has a confirmed BIS registration; for Indian government orders, the finished gateway (not the module) needs BIS CRS under IS 13252-1 if it falls under the CRS list - see R01.

External parts and creepage/clearance (for all modules):
- Input fuse: slow-blow T2A-T3.15A / 250 VAC (required by Mornsun; RECOM has internal fuse) [S42, S44]; MOV (e.g. 14D471K/10D561K class) across L-N for 4 kV surge if the installation category needs it; NTC only if the datasheet requires it.
- Creepage/clearance for 230 VAC mains, reinforced insulation, pollution degree 2, OVC II, per IEC 62368-1: plan >= 6.4 mm creepage and >= 4 mm clearance primary-to-SELV, >= 2.5 mm L-N before the fuse; add a routed slot under the module (values from general IEC 62368-1 tables - UNVERIFIED in this run, confirm with the test lab). Keep the 40-pin bus and all SELV copper outside the module's primary keep-out.
### 3.2 DC input front end, 9–36 V

- TI TPS2660: 4.2-60 V eFuse (62 V abs max), 0.1-2.23 A adjustable limit, integrated reverse polarity, IEC 61000-4-5 surge-oriented, UL 2367 recognised, 300 uA Iq; datasheet Dec 2019 rev G [S8]. Local datasheet confirms: reverse input polarity down to -60 V, back-to-back FETs 150 mOhm, reverse current blocking, adjustable UVLO / OVP cut-off / slew rate, fixed 38 V OV clamp in TPS26602, fault and current-monitor outputs, circuit-breaker / latch / auto-retry modes [S8].
  - Price: DigiKey India TPS26600PWPR INR 211.87 (500), 196.10 (2,000 reel), 192.19 (4,000); ACTIVE; 0 stock, 2,000 due 14-Dec-2026, 26-week lead time (seen 2026-11-14) [S49]. About USD 2.1 - too expensive for every module; fine as the single baseboard input eFuse.
- TI TPS16630 (60 V, 6 A eFuse, VQFN-24 4x4): DigiKey India INR 300.13 (100), 260.01 (3,000 reel), ACTIVE, 0 stock, 26-week lead time [S50]. Use only if the baseboard input must pass > 2.2 A (e.g. 6 modules at 9 V, see section 7).
- TVS for 24 V DC ports: SMBJ33A (600 W, VRWM 33 V, VBR min 36.7 V, VC ~53 V at Ipp ~11 A - standard JEDEC values, UNVERIFIED against a specific datasheet in this run). DigiKey India list prices INR 3.08 (GOODWORK) to INR 15.9 (MDD) to INR 13.1 (AOS) per piece [S51]. Use SMCJ33A (1500 W) on the baseboard input. Note VRWM 33 V sits above a 28.8-29 V charging 24 V lead-acid bus, so no leakage at float.
- Surge sizing (IEC 61000-4-5 1.2/50 us, DC power port): at 1 kV via 42 Ohm (typical coupling for lines in the industrial generic standard; exact test level for the product family standard UNVERIFIED in this run) the peak current is about (1000 - 53)/42 = 22.5 A, above an SMBJ33A rating -> SMCJ33A on the main input. With 2 Ohm coupling (0.5 kV line-line) it is ~225 A, which needs a 3-5 kW TVS (SMDJ/5.0SMDJ class) or series impedance. Final level to be fixed with the test lab (see R01).
- Architecture: TVS (SMCJ33A) -> TPS2660 (OVP set ~33-34 V, ILIM set, reverse-polarity and reverse-current blocking, UVLO ~8 V) -> pi filter -> 12-24 V bus. The OVP cut-off protects 36 V-rated bucks (LMR51420/51430) on the bus during surges.
- Conducted-emission filter (CISPR 32 Class A/B on DC port, 150 kHz-30 MHz): common-mode choke (e.g. 2x 1-3 mH, 2-3 A) + X caps (1-4.7 uF ceramic, 50 V+) + bulk electrolytic damping (47-100 uF, 50 V) at the input, plus per-buck input pi filter (1-4.7 uH ferrite / inductor + 10 uF ceramics). Class B is needed for residential/light industrial (and for CE-RED on radio modules in most cases); Class A for industrial-only. Component values are design guidance, not sourced; verify by pre-compliance scan.

## 4. Stacked pass-through bus power distribution (replaces per-slot distribution)

Topology: the baseboard (or its AC-DC / DC front end) drives a single 12-24 V rail "VBUS" that passes through every module's 40-pin connector pair. Every module draws from VBUS through its own input stage; nothing downstream is switched by the baseboard except through enable lines.

4.1 Current through chained contacts. The contact pair nearest the baseboard carries the SUM of all downstream modules, not one module's current. Using the budget of section 7 (about 15 W at the bus with cellular bursts smoothed, about 20 W worst-case instantaneous):

| Bus voltage | Total current (15 W) | Total current (20 W) | Pins per rail at 0.3 A/contact (20 W) | Pins per rail at 0.5 A/contact (20 W) |
|---|---|---|---|---|
| 9 V | 1.67 A | 2.22 A | 8 | 5 |
| 12 V | 1.25 A | 1.67 A | 6 | 4 |
| 24 V | 0.63 A | 0.83 A | 3 | 2 |

Recommendation: allocate 4 VBUS + 4 GND contacts (gives 1.2-2.0 A per rail). This covers a full stack at 12-24 V; at 9 V (discharged 12 V battery) limit the stack to 4 modules or limit charging current. Prefer 24 V nominal on the bus. Contact current ratings and resistance must come from the chosen Hirose/Wuerth series datasheet (R07); values here are from the brief (0.3-0.5 A per contact).

4.2 Voltage drop for 6 modules. Assumption (UNVERIFIED, to replace with the R07 connector data): 40 mOhm per mated contact, 4 contacts in parallel per rail, 10 mOhm module-internal copper per rail, so about 20 mOhm per joint per rail, 40 mOhm round trip. With equal load per module the drop to the last module is R x Itotal x (6+5+4+3+2+1)/6 = 3.5 x 0.04 x Itotal: at 9 V/2.2 A = 0.31 V (3.4 %); at 12 V/1.7 A = 0.23 V; at 24 V/0.83 A = 0.12 V. Voltage drop is not the limit; contact heating and contact wear are. GND contacts carry the same current: never return high current through a shield or signal ground.

4.3 Per-module input protection / inrush (on every module, both input paths):
- Lowest cost: Schottky diode-OR (terminal and bus) + PTC + SMBJ33A + <= 10 uF ceramic before the buck plus a 22-47 uF electrolytic for damping (hot-plug ringing on a ceramic-only input can approach 2x VBUS, i.e. ~48 V at 24 V, beyond a 36-40 V buck). Inrush is limited by the small input capacitance and the buck soft-start. Cost about INR 10 per module.
- Preferred: LM74700 + N-FET on the bus input (back-feed blocking) and TPS26621 eFuse (60 V, 25-880 mA limit, adjustable dv/dt, UVLO/OVP, fault and PGOOD outputs, auto-retry) [S52, S53]: about INR 200 per module.
- Baseboard: one TPS2660 eFuse (reverse polarity to -60 V, OVP cut-off, 2.23 A max) on the bus source [S8, S49]; TPS16630 (6 A) if the bus must carry > 2.2 A at 9 V [S50].

4.4 Back-feeding. A module that is also powered from its local terminal or its Li-ion cell must never drive VBUS: otherwise one module's 12 V battery would power the whole stack through its connector and its PTC. Rule: every source enters the module through a diode-OR (Schottky or LM74700) into the module's internal rail only; the bus side is input-only. The Li-ion path is isolated by the charger power path (BQ25601 BATFET / BQ25185 / TP4056 load-share). Only the baseboard (or a dedicated "power feed" module) drives VBUS, through the TPS2660 which also blocks reverse current [S8].

4.5 Module short circuit. Lowest-cost tier: the faulty module's PTC trips (seconds); until then the baseboard eFuse may also trip and drop the whole stack (single fault domain). Preferred tier: the module eFuse (TPS26621, auto-retry) limits within microseconds and isolates the module; the baseboard eFuse stays on. Recommendation: preferred tier on the cellular card (largest load, burst currents), PTC on small cards.

4.6 Hot-plug. Stackable DIN-rail modules are normally assembled unpowered. Recommendation: specify "no live insertion" in the manual, but design so it is survivable: GND contacts first-mate if the connector series allows staggered pins (R07), TVS + damping on every module input, eFuse dv/dt control at the baseboard. Live insertion with the preferred tier (eFuse on the module) is acceptable.

4.7 Power-cycling a hung module (baseboard MCU owns this, per the 2026-11-13 update). On a pass-through bus there is no per-slot switch. Options: (a) one open-drain "PWR_EN" line per slot position driving the module's buck EN (cheapest; costs one bus pin per position, up to 6 pins); (b) an addressed reset/enable via the bus management interface, with the module's eFuse EN (TPS26621) or buck EN driven by a local watchdog/latch. Recommend (a) for up to 6 modules if pins allow, else (b).

## 5. Hold-up / last-gasp

Requirement: keep the 4G module transmitting 5-10 s after loss of input.

Energy: assume about 2.6 W for the cellular module while transmitting a last-gasp message on LTE (0.6 A average at 3.8 V plus 0.3 W logic - UNVERIFIED typical values; check the R02 modem datasheet). 10 s -> 26 J; with 85 % converter efficiency about 31 J needed.

| Option | Sizing | Cost | Comment |
|---|---|---|---|
| Li-ion cell already on the module | 1 Ah cell = 13,000 J | 0 extra | Best: the module already has battery support; last-gasp is free whenever a cell is fitted |
| 2 x 10 F / 2.7 V supercaps in series (5 F, charged to 5.0 V, used down to 2.5 V via buck-boost) | E = 0.5 x 5 x (5.0^2 - 2.5^2) = 47 J, x 0.85 = 40 J -> ~13-15 s at 2.6-3 W | 2 x INR 100.57 (Abracon ADCR 10 F, 600 pcs, DigiKey India) + balancing + charge limiter + buck-boost ~INR 60-100 (UNVERIFIED) = about INR 260-300 [S54] | For no-battery SKUs. Life: 10 F parts rated 1000-1500 h at 65-85 C (Tecate 1000 h @ 85 C, CDE 1500 h @ 85 C, Maxwell 1500 h @ 65 C) [S54]; in a 60-70 C cabinet expect capacitance loss within a few years - keep cell voltage <= 2.5 V and use 85 C-rated parts |
| Bulk electrolytic on the 24 V bus | C = 2E / (V1^2 - V2^2) = 62 / (24^2 - 9^2) = 0.125 F | impractical | Only covers milliseconds; use for ride-through of short dips only |

Early power-fail detection: a comparator (or MCU analog watchdog) on the baseboard input BEFORE the ideal diode/eFuse, threshold about 75-80 % of nominal (e.g. 18 V for a 24 V system, 9.5 V for 12 V), with hysteresis; output drives a dedicated open-drain PFAIL line on the 40-pin bus. Because the TPS2660/LM74700 block reverse current, the bus capacitance cannot be discharged back into the dead source, giving the modules tens of milliseconds to receive PFAIL, and the cellular module's own storage (cell or supercap) carries the transmission. Each module can also detect loss of its own input locally (buck PGOOD / UVLO divider into a GPIO).

## 6. RTC backup

| Option | Price | Life | Temperature | Shipping | Notes |
|---|---|---|---|---|---|
| CR2032 (Panasonic CR-2032/HSN, PC pins, 225 mAh) | INR 87.50 at 80 pcs, DigiKey India, 63,883 in stock [S55] | 225 mAh / ~1-2 uA RTC drain = > 10 years (self-discharge limits, ~1 %/year - UNVERIFIED) | about -30..+60/70 C (UNVERIFIED) | lithium metal, contained in equipment (UN3091, PI 970); small cells usually shipped as Section II (UNVERIFIED) | No charging circuit allowed; needs reverse-charge protection (MCU VBAT pin switch or series diode/resistor per UL 1642 practice). Holders and tab versions cheaper from LCSC (UNVERIFIED) |
| ML2032 (Panasonic, rechargeable Li-Mn, ~65 mAh) | not found at DigiKey India in this run (UNVERIFIED) | recharged by the system; limited cycles | about -20..+60 C (UNVERIFIED) | lithium metal rules also apply | Needs a 3.1 V class charge circuit; higher cost; not attractive |
| Supercap (Seiko CPH3225A, 11 mF, 3.3 V) | INR 249 (1 pc, DigiKey India) [S56] | t = C x dV / I = 0.011 x 1.8 V / 1 uA = ~5.5 h | per Seiko datasheet (UNVERIFIED) | no dangerous-goods issues | Hours only; 0.1-1 F EDLC gives days but is larger |
| No backup, resync time | 0 | - | - | - | Gateway gets time from NTP / cellular NITZ / LoRaWAN DeviceTimeReq; acceptable if logs can be timestamped after sync |

Recommendation: CR2032 in a holder on the baseboard only (feeds the MCU VBAT/RTC domain); no RTC backup on modules (use the Li-ion cell where fitted). For hot cabinets choose a high-temperature coin cell variant (e.g. -40..+85 C rated CR2032 - UNVERIFIED availability).

## 7. Power budget

Assumptions: converter efficiency 85 %; values at the module input; cellular GSM burst = 2 A at 3.8 V (R02 design guidance: 1 A VBAT_BB + 2.5 A VBAT_RF, >= 3 A supply recommended for Quectel EG915U); ESP32-C6 TX peak 354 mA (802.11b, 21 dBm), RX 78 mA, BLE TX 315 mA at 20 dBm (Espressif ESP32-C6 datasheet v1.6, tables 5-7/5-8) [S57]; SX1262 TX ~118 mA at +22 dBm (Semtech datasheet value, UNVERIFIED in this run; the Semtech product page confirms only RX 4.2-4.6 mA [S58]); Ethernet PHY ~0.2 W (UNVERIFIED); baseboard MCU + secure element + IO logic ~0.5 W average / 1 W peak (UNVERIFIED, see R08). Li-ion charging adds up to 4.2 V x charge current / 0.85 (0.5 A -> 2.5 W; 1 A -> 4.9 W) per module.

| Load | Average (W) | Peak (W) |
|---|---|---|
| Baseboard (MCU, SE, IO logic) | 0.5 | 1.0 |
| 4G + Ethernet + Wi-Fi module | 2.5 | 10.6 instantaneous (GSM burst 7.6 W + PHY 0.2 + Wi-Fi TX 1.2, /0.85); about 5 W seen at the bus with local bulk capacitance |
| Wi-Fi/BLE module | 0.35 (connected, mostly RX) | 1.4 |
| LoRa module | 0.05 | 0.5 |
| Fieldbus card (CAN + RS-485 + small MCU) | 0.3 | 0.6 (RS-485 driving 54 Ohm) |
| Second Wi-Fi or spare module | 0.35 | 1.4 |
| Li-ion charging, 2 modules at 0.5 A | 5.0 | 5.0 |
| Total (6 cards incl. baseboard) | about 9 W | about 15 W smoothed / 20 W instantaneous |

Baseboard supply rating: 24 V / 20 W (Mean Well IRM-20-24, 21.6 W) is adequate with charge current limited to 0.5 A and charging on at most two modules at once (firmware-managed); choose a 30 W module (IRM-30 class) if all modules may charge at 1 A or if field IO outputs are also powered from it. Connector current: see the table in 4.1 (per rail at the first joint 0.63-0.83 A at 24 V, 1.25-1.67 A at 12 V, 1.67-2.22 A at 9 V). A single module's own draw at its connector: cellular 0.42 A (24 V) / 0.88 A (12 V) / 1.18 A (9 V) at 10.6 W instantaneous; Wi-Fi 0.06 / 0.12 / 0.16 A peak.

## 8. Risks and open decisions

1. LCSC prices in this report come from search snapshots (LCSC pages could not be read directly); several snapshots disagree by 20-50 %. Re-quote before committing the BOM.
2. Lead times: TPS2660 and TPS16630 show 0 stock and 26-week lead times at DigiKey India (2026-11-14) [S49, S50]; IRM-20-24 out of stock until Jan-2027 at DigiKey India [S4]. Second sources needed (Mornsun LDE20; for the eFuse, TPS26621 is in stock [S52]).
3. Hot-cabinet Li-ion: charging blocked above ~45 C and fast ageing at 60-70 C. Decide whether hot-cabinet SKUs ship with supercap hold-up instead of Li-ion.
4. Cost conflict: preferred-vendor block (~INR 250-585) does not fit the Wi-Fi module BOM; the lowest-cost block uses clone ICs (TP4056/DW01A) whose quality must be qualified per vendor.
5. 36 V bucks on a 24 V bus rely on the baseboard eFuse OVP; in standalone use on the local terminal they rely on the module TVS only. Decide: 40 V AP64200 + SMBJ33A (clamp up to ~53 V exceeds 40 V during a surge pulse) vs 60-65 V bucks (LMR36506 0.6 A; 60 V 2-3 A parts not priced in this run). This is the main open technical risk for standalone surge compliance.
6. BIS: no BIS registration found for any PCB-mount AC-DC module checked; confirm with R01 whether the finished gateway needs CRS registration and whether a BIS-registered module helps.
7. Connector contact current/resistance and staggered GND pins depend on the R07 connector choice.
8. Ethernet PHY, modem, LoRa currents are typical values, not measured; update the budget when R02-R05 select parts.

## 9. Datasheets downloaded

Folder: docs/datasheets/power/ (index in INDEX.md there). TI_LMR36506, TI_BQ24074, TI_BQ25185, TI_LM74700-Q1, TI_TPS2660, MeanWell_IRM-20 (earlier run); TI_LMR51430, TI_BQ25601 (this run). All verified as PDF with `file`.

## 10. Sources

- S1 https://www.ti.com/product/LMR36506 (ACTIVE, 2x2 mm)
- S2 https://www.ti.com/lit/ds/symlink/lmr36506.pdf (local copy)
- S3 https://www.meanwell.com/Upload/PDF/IRM-20/IRM-20-SPEC.PDF (local copy)
- S4 https://www.digikey.in/en/products/detail/mean-well-usa-inc/IRM-20-24/7704665 (INR prices, stock, 2026-11-14)
- S5 https://www.ti.com/lit/ds/symlink/bq24074.pdf
- S6 https://www.ti.com/lit/ds/symlink/bq25185.pdf
- S7 https://www.ti.com/lit/ds/symlink/lm74700-q1.pdf
- S8 https://www.ti.com/lit/ds/symlink/tps2660.pdf
- S9 https://www.xflowpay.com/tools/currency-converter/usd-to-inr-rate?amount=1
- S10 https://www.ti.com/product/LMR51420
- S11 https://www.lcsc.com/product-detail/C5383002.html (price from search snapshot 2026-11-14)
- S12 https://ti.com/product/LMR51430
- S13 https://www.lcsc.com/product-image/C5185863.html (price from search snapshot 2026-11-14)
- S14 https://www.ti.com/product/TPS560430
- S15 https://www.lcsc.com/product-detail/C3192345.html ; https://www.lcsc.com/product-detail/C2071056.html
- S16 https://uk.rs-online.com/web/p/switching-regulators/2033392 ; https://ie.rs-online.com/web/p/switching-regulators/2033386
- S17 https://lcsc.com/product-detail/DC-DC-Converters_STMicroelectronics-L6981NDR_C3192320.html ; https://estore.st.com/en/l6981ndr-cpn.html
- S18 https://www.st.com/en/product/L7983 ; https://www.element14.cn/en-CN/c/semiconductors-ics/power-management-ics-pmic?st=L7983
- S19 https://lcsc.com/product-detail/image/SY8303AIC_C97054.html ; https://www.lcsc.com/product-detail/C509398.html
- S20 https://www.lcsc.com/product-detail/C16581.html ; https://lcsc.com/product-detail/Battery-Management_JSMSEMI-TP4056_C22470410.html ; https://lcsc.com/product-detail/Battery-Management_GOODWORK-TP4056_C21713961.html
- S21 https://www.ti.com/product/BQ25170 ; https://www.lcsc.com/product-detail/C5208201.html
- S22 https://www.lcsc.com/product-detail/C3682876.html
- S23 https://www.lcsc.com/product-image/C424093.html
- S24 https://lcsc.com/product-detail/Battery-Management_Microchip-Tech-MCP73871-1CCI-ML_C637758.html ; https://origin-www.findchips.com/search/mcp73871t-1cci%2Fml
- S25 https://www.lcsc.com/product-image/C155635.html
- S26 https://www.st.com/en/power-management/stbc15.html
- S27 https://www.lcsc.com/product-image/C54313.html
- S28 https://www.lcsc.com/product-detail/C19725033.html
- S29 https://www.ti.com/product/BQ25622 ; https://www.ti.com/product/BQ25620
- S30 https://www.ti.com/product/BQ25601
- S31 https://www.lcsc.com/product-detail/C468236.html ; https://lcsc.com/product-detail/Battery-Management_Texas-Instruments-BQ25620RYKR_C22448184.html
- S32 https://www.lcsc.com/product-image/C2830320.html ; https://www.lcsc.com/product-image/C42380662.html ; https://www.lcsc.com/product-image/C18164398.html ; https://www.lcsc.com/product-image/C2927799.html
- S33 https://www.lcsc.com/product-detail/C183096.html ; https://www.lcsc.com/product-detail/C2876282.html ; https://www.digikey.sg/en/products/detail/texas-instruments/BQ29700DSER/5973173
- S34 https://lcsc.com/product-detail/image/MAX17048G-T10_C2682616.html ; https://www.findchips.com/search/MAX17048G%2BT10
- S35 https://datasheet.lcsc.com/lcsc/1912272132_Texas-Instruments-BQ27441DRZR-G1A_C473397.pdf ; https://findchips.com/search/BQ27441DRZT-G1A
- S36 https://www.lcsc.com/product-detail/C881838.html
- S37 https://www.lcsc.com/product-image/C2941042.html ; https://www.digikey.com/en/products/detail/texas-instruments/LM74700QDBVRQ1/10434692
- S38 https://lcsc.com/product-detail/ORing-Controllers_MAXIM-MAX40200AUK-T_C2649430.html ; https://www.lcsc.com/product-image/C3227637.html
- S39 https://www.lcsc.com/product-image/C154901.html ; https://www.lcsc.com/product-image/C461094.html ; https://www.lcsc.com/product-image/C181093.html
- S40 https://www.lcsc.com/product-detail/C194964.html
- S41 https://www.meanwell.com/fr/newsInfo.aspx?c=2&i=1446
- S42 https://recom-power.com/pdf/Powerline_AC-DC/RAC20-K.pdf (read 2026-11-14)
- S43 https://uk.rs-online.com/web/p/switching-power-supplies/1834096 ; https://www.buerklin.com/en/p/recom/ac-dc-converters/rac20-24sk/33C6136 ; https://octopart.com/part/recom-power/RAC20-24SK
- S44 https://www.mornsun-power.com/public/uploads/pdf/LDE20-20Bxx.pdf (read 2026-11-14)
- S45 https://www.lcsc.com/datasheet/lcsc_datasheet_2012191234_MORNSUN-Guangzhou-S--T-LDE20-20B24_C970743.pdf ; https://www.lcsc.com/product-detail/C970743.html
- S46 https://datasheet.lcsc.com/lcsc/2004021704_MORNSUN-Guangzhou-S--T-LM50-20B24_C503961.pdf
- S47 https://zbotic.in/product/hlk-20m24-hi-link-24v-20w-ac-to-dc-power-supply-module/ ; https://www.lcsc.com/product-detail/C465409.html ; https://www.dnatechindia.com/hlk-20-m-24-ac-to-dc-20-watts-24-volts-module-india.html ; https://www.tinytronics.nl/product_files/003715_Hi-Link%2020W%20series%20power%20supply%20module%20datasheet%20V1.1.pdf
- S48 https://www.digikey.com.au/en/products/detail/traco-power/TMPS-15-124/15822891 ; https://www.digikey.sg/en/products/detail/xp-power/ECE20US24/4487507
- S49 https://www.digikey.in/en/products/result?keywords=TPS26600PWPR (2026-11-14)
- S50 https://www.digikey.in/en/products/result?keywords=TPS16630RGER (2026-11-14)
- S51 https://www.digikey.in/en/products/result?keywords=SMBJ33A (2026-11-14)
- S52 https://www.ti.com/product/TPS2662
- S53 https://www.digikey.in/en/products/result?keywords=TPS26621 (TPS26621DRCR INR 152.33 at 3,000; 4,539 in stock; 2026-11-14)
- S54 https://www.digikey.in/en/products/result?keywords=supercapacitor%2010F%202.7V (2026-11-14)
- S55 https://www.digikey.in/en/products/result?keywords=CR2032%20battery%20Panasonic (2026-11-14)
- S56 https://www.digikey.in/en/products/result?keywords=CPH3225A (2026-11-14)
- S57 https://www.espressif.com/sites/default/files/documentation/esp32-c6_datasheet_en.pdf (v1.6, tables 5-7 to 5-9)
- S58 https://www.semtech.com/products/wireless-rf/lora-connect/sx1262
- S59 https://www.ti.com/lit/ds/symlink/lmr51430.pdf (local copy)
- S60 https://www.ti.com/lit/ds/symlink/bq25601.pdf (local copy; VBUS 3.9-13.5 V operating, 22 V abs max for <= 1 h, VSYS_MIN 3.5 V, ship mode via QON/BATFET, IBAT 17 uA with BATFET disabled)

## 11. Exchange rate

Rate used: 1 USD = INR 93.7 (xflowpay converter, updated 2026-11-11 19:36 IST, shows 93.66; other converters range 93-95, undated) [S9]. DigiKey India prices are quoted directly in INR (incl. no GST, check at checkout).
