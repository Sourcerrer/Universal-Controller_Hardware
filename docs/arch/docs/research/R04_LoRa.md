# R04 — LoRa plug-in module: selection report

Status: COMPLETE (first issue) — items marked UNVERIFIED or EST still need confirmation
Date: 2026-11-14

## 1. Executive summary and recommendation

- **Option A (recommended): STM32WLE5CC.** Pilot/first production on the pre-certified **RAKwireless RAK3172-T** (STM32WLE5CC + TCXO, −40…85 °C, 1.69 µA sleep, CE/FCC/ISED/UKCA/RCM/WPC) [S10, S15]. For volume, switch to a **chip-down STM32WLE5CCU6 (QFN48)** running the same firmware. The chip-down design is the only option that fits BOM ≤ INR 714 (≈ INR 554–825 estimated).
- **Option B: Semtech SX1262 + Nordic nRF54L15**, prototyped on RAK4630/RAK4631 (nRF52840 + SX1262, in-tree Zephyr board). It is the most secure option (TrustZone, tamper detection) and adds BLE commissioning, but at verified Indian distributor prices the two ICs alone cost INR 1,036. **It does not fit the cost target** unless volume quotes come in at about USD 2–3 per IC.
- **Cost-fit verdict:** RAK3172 costs INR 562–659 per module (RAK list price / DigiKey India @900), which takes up 79–92 % of the BOM. The module BOM then comes to INR 817–1,119 and the finished cost to INR 1,144–1,567, so **over target**. Chip-down STM32WL is **feasible but marginal** at LCSC-class pricing (USD 2.44–2.72). At DigiKey India pricing (INR 587) it is not feasible. Chip-down also needs one-time CE-RED and WPC ETA radio certification. Non-radio lines are engineering estimates until R06/R07 report.
- **India rules:** G.S.R. 853(E) (10-Dec-2021, 865–868 MHz) superseded the old "1 W / 4 W EIRP" RFID rules. Industrial sensors and data acquisition get **500 mW e.r.p. with mandatory adaptive power control (APC), duty cycle ≤ 2.5 % (nodes) / ≤ 10 % (network access points) and ≤ 200 kHz bandwidth**. Otherwise the limit is 25 mW e.r.p. with 1 % duty cycle. ETA is required [S1]. LoRaWAN RP002 IN865 still says "no duty cycle" and +30 dBm EIRP [S2], so firmware must enforce the gazette rules. The RAK3172's Indian ETA covers only 0.0244 W e.r.p. [S15].
- **EU:** ERC/REC 70-03 sets 25 mW e.r.p. at 1 % (865–868.6 MHz) and 500 mW e.r.p. at 10 % (869.4–869.65 MHz), with EN 300 220 as the harmonised standard [S4]. **One hardware build covers IN865 and EU868.** Region, power, APC and duty cycle are firmware settings.
- **Gateway:** the same single-channel module gives a **private LoRa star network, not a LoRaWAN gateway**. Capacity per channel is about 6,400 (SF7) to about 270 (SF12) 20-byte uplinks/hour at 10 % load. A LoRaWAN gateway needs an SX1302/SX1303 concentrator (RAK5146, RAK2287, WM1302 from USD 25) plus a **Linux host**. Recommended wording is in section 6.4.
- **Key risks:** cost, chip-down certification NRE, the India duty-cycle interpretation, Zephyr's LoRaWAN backend transition (LoRaMac-node is deprecated by Semtech), 20–52-week lead times, and whether the enclosure falls inside the INR 1,000 target.

## 2. Scope and constraints

- LoRa plug-in module for the UC: an individually enclosed, stackable DIN-rail module with a 40-pin pass-through bus connector (Hirose/Würth). The same module runs on the gateway and as a standalone battery or 12–24 V node.
- Own power: 12–24 V DC input plus single-cell Li-ion. Battery nodes must be low power.
- Finished cost ≤ INR 1,000 = BOM × 1.4, so BOM ≤ ~INR 714. The BOM includes the connector, power stage and antenna connector.
- Gateway brain = low-cost secure MCU + secure element on the baseboard (owns IO/ADC and keys, can power-cycle modules). IO/ADC are not on modules, so a standalone node needs its own minimal interfaces (section 10).
- Vendors ST/NXP/Nordic preferred; Zephyr preferred, ThreadX second; India first (WPC ETA, BIS), CE/RED and CRA later.

## 3. Option A — STM32WL (chip-down vs pre-certified modules)

Conventions: USD→INR = 93.9 (CurrencyBeacon mid-market, 2026-11-08) [S5]. DigiKey India prices are quoted directly in INR excl. GST. "LCSC (search index)" means the price was read from the search-engine snapshot of the LCSC page because the live LCSC page loads prices by script; treat as indicative.

### 3.1 Chip-down STM32WL

| Part | Package | Notes | Price ~1k | Source |
|---|---|---|---|---|
| STM32WLE5CCU6 | UFQFPN48 7x7 mm | 256 KB flash, single Cortex-M4 + SX126x-class radio; easiest to assemble (QFN) | DigiKey India INR 587.41 @1,040 (tray), 3,390 in stock, 52-week factory lead time, Active (2026-11-14). LCSC (search index): USD 2.44 @1,040+ tray (≈ INR 229); USD 2.72 @1,000+ reel (≈ INR 255) | [S11, S12] |
| STM32WLE5JC | UFBGA73 5x5 mm | Same die as CC; BGA needs finer PCB rules / X-ray inspection | not priced (BGA rejected for DFM) | — |
| STM32WL55JC | UFBGA73 | Dual core (M4 + M0+), adds AES/PKA "secure" split; only in BGA | not priced (BGA, more than needed) | — |

The very large spread between DigiKey (≈ USD 6.3) and LCSC (≈ USD 2.4–2.7) is typical for ST parts; budgetary ST pricing at volume should be requested from an ST franchised distributor in India. UNVERIFIED: ST's official budgetary price (st.com pages timed out from this environment).

External parts needed for chip-down (from ST reference designs; datasheet download from st.com failed in this session, so details below are from module datasheets/application notes and are marked accordingly): 32 MHz TCXO (or crystal; TCXO recommended for SF11/SF12 and −40 °C operation), 32.768 kHz crystal (LSE, for RTC in sleep), RF switch (SPDT/SP3T for RFO_HP / RFO_LP / RFI paths, controlled by GPIOs), RFO_HP matching/low-pass filter network, balun/matching for RX, SMPS inductor for the internal DC-DC. Plus full RF layout and CE-RED/ETA radio testing of the whole module. UNVERIFIED in this report: exact component list per ST AN5457 / MB1389 reference design.

### 3.2 Pre-certified STM32WL modules

| Module | SoC | Size | Bands / variant | TX max | Sleep | Antenna | Certifications | Price ~1k / India | Source |
|---|---|---|---|---|---|---|---|---|---|
| **RAKwireless RAK3172 / RAK3172-T** | STM32WLE5CC (-T = TCXO ±2.5 ppm, -TE ±0.5 ppm) | 15.5 x 15 mm, stamp holes | "H" (800 MHz) variant covers EU868, IN865, RU864 (+US915/AU915/AS923/KR920 on 900 MHz SKU) | "20 dBm" test condition; 87 mA @ 20 dBm 868 MHz | 1.69 µA @ 3.3 V | IPEX (I) or RF pad (NI) | ANATEL, CE, FCC, ISED, JRL, KC, LoRa Alliance, RCM, RSM, UKCA, **WPC** | DigiKey India RAK3172-8-SM-NI: INR 698.32 @300, 672.79 @600, **658.55 @900**, 444 in stock, 20-week lead time, Active (2026-11-14). RAK store list price USD 5.99–6.99 (search snippet, store page rate-limited) ≈ INR 562–656 | [S10, S13, S14, S15] |
| RAKwireless RAK3172-F | STM32WLE5JCI6 + TCXO | — | as above | — | 2.2 µA @ 3.3 V | — | — | not priced | [S10] |
| RAKwireless RAK3172-SiP | STM32WLE5 in SiP | — | — | — | — | — | RAK cert page exists [S16] | see 3.3 | [S16] |
| **Ebyte E77-900M22S** | STM32WLE5CCU6 | 14 x 20 mm | 868–930 MHz; firmware regions EU868, US915, AU915, AS923, **IN865**, KR920, RU864 | 21.5 dBm per datasheet (retailer says 22 dBm); 32 MHz **crystal, not TCXO** [S35] | 3 µA (software shutdown) [S35] | IPEX or stamp-hole RF pin | CE: UNVERIFIED (not found); FCC statement in manual only | Hubtronics (India) INR 483.90 + GST (single unit, out of stock 2026-11-14); Ebyte store USD 5.58 (out of stock); LCSC from USD 5.91 | [S17, S18] |
| Seeed Wio-E5 (ex LoRa-E5) | STM32WLE5JC | 12 x 12 mm | EU868/US915 etc. | 20.8 dBm (UNVERIFIED) | — | RF pad | CE/FCC (UNVERIFIED in this session) | Indian retailer ≈ INR 1,100 single; SparkFun has retired its Grove LoRa-E5 listing; no Seeed EOL notice found | [S19] |

**RAK3172 India WPC ETA — what it really covers.** The RAK3172 ETA (self-declaration) is Registration No. ETA-SD-20240707058, dated 23-07-2024, model RAK3172 only, 865–868 MHz, **max ERP 0.0244 W (≈ 13.9 dBm e.r.p.)**, under G.S.R. 853(E) of 10-12-2021, RF test report TÜV Rheinland Shenzhen CN21QZKR 001 [S15]. So the module's Indian approval is at the 25 mW e.r.p. "non-specific SRD" (Table I) level, i.e. 1 % duty cycle. The certificate is "for a single model"; using the module inside the UC LoRa module does not remove the need for the UC product's own WPC ETA (self-declaration route), but it supplies an accredited RF test report that can be referenced, and it keeps the cost low. Running at 500 mW e.r.p. (Table II) would need new testing and an ETA at that power.

### 3.3 STM32WL longevity

ST product longevity programme: 10 years for STM32, a rolling commitment renewed annually [S20]. ST's STM32WL5x product-line overview and launch PR state STM32WL is in the 10-year longevity programme [S20, S21]. The exact "available until" date per part number must be read from st.com/longevity (site not reachable from this environment: UNVERIFIED date). Module vendors (RAK, Ebyte, Seeed) do not publish formal longevity commitments (none found) — module-level longevity is a risk; mitigate by keeping footprint compatibility between RAK3172 and a chip-down STM32WLE5CCU6 layout, or by second-sourcing E77.

### 3.4 Software support for STM32WL

- **Zephyr**: the STM32WL sub-GHz radio is a supported device (`st,stm32wl-subghz-radio` via SUBGHZ SPI); Zephyr has an in-tree board `rak3272s` (RAK3272S breakout carrying the RAK3172) with STM32 AES accelerator, RNG, OTP, flash/NVMEM drivers [S22]. Zephyr's LoRaWAN subsystem default backend is Semtech LoRaMac-node "included as a Zephyr module", supporting all regions including `CONFIG_LORAWAN_REGION_IN865` and EU868; a newer "Native" Zephyr LoRaWAN 1.0.x Class A backend exists but supports only EU868 today. Zephyr notes that "LoRaMac-node has been deprecated by Semtech in favor of LoRa Basics Modem" and that porting to LoRa Basics Modem "is in progress" (docs "latest", source updated 15-Apr-2026; releases 4.4.0/4.5.0, LTS 3.7.0) [S23]. Consequence: Zephyr LoRaWAN works today on STM32WL/SX126x via LoRaMac-node, but the backend is in transition — a medium-term maintenance risk for any option.
- **STM32Cube / ThreadX**: STM32CubeWL (HAL + LoRaWAN middleware based on LoRaMac-node + Sigfox + SubGHz_Phy) is ST's native package; ThreadX (Eclipse ThreadX) is offered in X-CUBE-AZRTOS for many STM32 series — STM32WL inclusion UNVERIFIED (could not confirm; web search budget exhausted).
- **RAK RUI3** firmware on RAK3172 gives an AT-command modem (UART, 115200 baud) and RUI3 user-app API; LoRaWAN 1.0.4 Class A/B/C [S10]. For the UC, either (a) keep RUI3 and drive the module by AT commands from the baseboard MCU (fast, but proprietary firmware), or (b) flash Zephyr on the RAK3172 (the module is a plain STM32WLE5CC; SWD pads exposed).

## 4. Option B — the second option

### 4.1 Candidates

| Candidate | Parts | Bands / TX | Sleep | Certification | Price evidence | Zephyr | Longevity | Source |
|---|---|---|---|---|---|---|---|---|
| (a) SX1262 + nRF54L15 chip-down | Semtech SX1262 + Nordic nRF54L15 | SX1262: 150–960 MHz, +22 dBm | — | none (full module RF certification needed for BOTH radios: CE-RED + WPC ETA for sub-GHz and 2.4 GHz) | SX1262IMLTRT DigiKey India INR 574.75 @1,000 (CT), 542.96 @3,000 (T&R), 17,964 in stock, 26-week lead time, Active (2026-11-14) | SX126x LoRa + LoRaWAN (LoRaMac-node) in-tree; nRF54L15 fully supported in Zephyr/nRF Connect SDK | Semtech: no public longevity programme found (UNVERIFIED); Nordic: nRF54L is current generation | [S24, S23] |
| (b) **RAKwireless RAK4630** (pre-certified) | nRF52840 + SX1262 + TCXO | IN865, EU868, US915, AU915, KR920, RU864, AS923; LoRa 22 dBm; BLE −20…+4 dBm | 4.23 µA | CE, FCC, ISED, KC, RCM, REACH, RoHS — **WPC not listed** | not priced (DigiKey India search page returned no product table; RAK store rate-limited) — UNVERIFIED; typically ~2x RAK3172 | Zephyr board `rak4631` exists (UNVERIFIED in this session) | RAK: no formal commitment | [S25] |
| (c) Semtech LR2021 ("LoRa Plus", newest) | LR2021 transceiver + host MCU | sub-GHz + 2.4 GHz + licensed S-band, LoRa up to 125 kbps, FLRC up to 2.6 Mbps, FSK/OOK/O-QPSK/LR-FHSS, +22 dBm, −141.5 dBm sensitivity, "backward compatible with previous LoRa devices" | not stated | chip only; no pre-certified module verified | DigiKey "Buy Now" link, stock table empty; datasheet v2.2 dated 2026-08-08 | Not listed among Zephyr LoRa drivers (only SX1261/2/72/76 named) | new (2025–26) | [S26, S23] |
| (c') LR1121 / LR1110 | multi-band LoRa + GNSS/Wi-Fi scan (LR1110) | — | — | modules exist (e.g. Seeed Wio-LR1121, RAK RAK3112?) — UNVERIFIED | — | not in Zephyr LoRa driver list [S23] | — | — |
| (d) SX1262 module (Ebyte E22-900M22S, Seeed Wio-SX1262) + small ST MCU (e.g. STM32U0/STM32L0/STM32C0) | module + MCU | +22 dBm | — | Ebyte/Seeed CE status UNVERIFIED | E22 pricing not verified this session | SX126x driver in-tree | Ebyte: none | — |
| (e) NXP / Nordic native LoRa | none: neither NXP nor Nordic sells a sub-GHz LoRa SoC; any NXP/Nordic solution is "host MCU + Semtech radio" = (a)/(b)/(d) | | | | | | | — |

Additional data points: nRF54L15-QFAA-R listed on DigiKey India at INR 461.28 (single price shown, no ladder, 2026-11-14) [S27]; nRF54L15: 1.5 MB NVM, 256 KB RAM, 1.7–3.6 V, QFN40/48/52 and CSP47, sleep 0.7–2.9 µA, TrustZone, tamper detection, crypto engine with side-channel leakage protection [S28]. Ebyte E22-900M22S (SX1262, 850–930 MHz, 22 dBm, IPEX or stamp hole): Hubtronics India INR 541.53 + GST, out of stock (2026-11-14) [S29]. Zephyr board `rak4631/nrf52840` (RAK4631 = RAK4630 in WisBlock form) is in-tree, status "Maintained", SX1262 bound as `semtech,sx1262`, CryptoCell-310 listed [S30].

### 4.2 Recommendation for Option B: (a) Semtech SX1262 + Nordic nRF54L15 (chip-down), prototyped on RAK4630/RAK4631

Reasons:
1. It is the only candidate that is a genuinely different second source from Option A (different radio vendor path, different MCU vendor) while staying inside the preferred-vendor list (Nordic) and Zephyr-first (nRF54L15 is Nordic's lead Zephyr/nRF Connect SDK platform; SX126x is the reference radio of Zephyr's LoRa/LoRaWAN subsystem [S23]).
2. nRF54L15 is current-generation (vs nRF52840 in RAK4630), adds BLE for field commissioning/diagnostics of standalone nodes from a phone, and has the strongest on-chip security of all candidates (TrustZone, tamper detection, side-channel-hardened crypto) [S28].
3. RAK4630 (nRF52840 + SX1262 + TCXO, 22 dBm, 4.23 µA sleep, CE/FCC/ISED/KC/RCM) is the pre-certified fast path for prototypes and pilots, with an in-tree Zephyr board [S25, S30] — but **WPC is not listed for RAK4630** [S25], so an Indian ETA would be needed anyway.

Why not the others: (c) LR2021 is the newest Semtech part (datasheet v2.2, 2026-08-08) but has no Zephyr driver and no verified pre-certified module yet [S26, S23] — re-evaluate in 2027; LR1110/LR1121 add GNSS/Wi-Fi-scan/2.4 GHz features the UC does not need. (d) SX1262 module + small MCU costs about the same as (a) but adds a second vendor's module with unverified CE status. (e) Neither NXP nor Nordic offers a native sub-GHz LoRa SoC.

**Cost caveat (important):** at verified Indian distributor prices, SX1262 (INR 575 @1k) + nRF54L15 (INR 461) = INR 1,036 for the two ICs alone — already above the whole BOM budget. Option B only fits if volume/franchise pricing comes in near USD 2–3 per IC (UNVERIFIED; LCSC/authorised-distributor volume quotes required). See section 7.

## 5. Regulation: India 865–867 MHz and EU868

### 5.1 India — the legal instrument in force is G.S.R. 853(E), 10 Dec 2021 (865–868 MHz)

Important correction to the commonly quoted "1 W / 4 W EIRP, 200 kHz, no duty cycle" India figures: those come from the 2005 RFID rules (G.S.R. 168(E), amended by G.S.R. 564(E) 2008), which were **superseded** by G.S.R. 853(E) of 10-Dec-2021, "Use of Low Power Equipment in the Frequency Band 865-868 MHz for Short Range Devices (Exemption from Licence) Rules, 2021" [S1]. Only equipment already type-approved under the 2005 rules keeps the old limits "till the end of its life" [S1, rule 1(3)]. No later amendment to G.S.R. 853(E) was found (search 2026-11-14); a 2024 amendment (G.S.R. 271(E)) concerns the separate 2018 low-power SRD rules, not this band [S3].

Licence-exempt (non-interference, non-protection, shared, non-exclusive) categories in 865–868 MHz under G.S.R. 853(E) [S1]:

| Table | Use category | Power limit | Channel access / duty cycle | Bandwidth | Standard |
|---|---|---|---|---|---|
| I | Non-specific SRD (telemetry, telecommand, alarms, data) | 25 mW e.r.p. | Duty cycle ≤ 1 % (FHSS: applies to whole transmission) | FHSS: ≤ 50 kHz for ≥ 58 hop channels | EN 300 220 |
| **II** | **Tracking, tracing and data acquisition — explicitly includes meter reading, sensors, actuators, data acquisition and "Wireless Industrial Applications (WIA) … in industrial environments"** | **500 mW e.r.p.** | **Adaptive Power Control (APC) required; duty cycle ≤ 10 % for network access points, ≤ 2.5 % otherwise** | **≤ 200 kHz** | EN 300 220 |
| III | Wideband data transmission | 25 mW e.r.p. | ≤ 10 % network access points, ≤ 2.8 % otherwise | > 600 kHz, ≤ 1 MHz | EN 304 220 |
| IV | RFID interrogators | 2 W e.r.p. (only on 4 channels 865.7/866.3/866.9/867.5 MHz) | ≤ 4 s continuous, ≥ 100 ms gap | ≤ 200 kHz | EN 302 208 |

Further obligations [S1, rule 5]: equipment **must be type approved** (WPC Equipment Type Approval, ETA) and must comply with the respective EN number; safety per ITU/ETSI/ANSI/BIS/ICNIRP.

Consequences for the UC LoRa module:
- The UC fits Table II (industrial sensors/data acquisition). 500 mW e.r.p. = +27 dBm e.r.p. ≈ +29.15 dBm EIRP. With a +22 dBm SX126x-class PA and a ≤ 3 dBi antenna the device is far below the limit, but **APC must be implemented in firmware** (LoRaWAN ADR/TXPower satisfies this; a private protocol must implement link-based power control) and **duty cycle must be enforced: ≤ 2.5 % for nodes, ≤ 10 % for the gateway (network access point)**. LoRa BW 125/250 kHz fits; **LoRa BW 500 kHz is NOT permitted under Table II (≤ 200 kHz)**.
- If APC is not implemented, the device falls back to Table I: 25 mW e.r.p. (+14 dBm e.r.p.) and 1 % duty cycle.
- **LoRaWAN RP002-1.0.4 IN865-867 is out of step with the 2021 rules**: it states "There is no dwell time or duty-cycle limitation for the INDIA 865-867 PHY layer" and a default Max EIRP of +30 dBm [S2]. These reflect the superseded 2005 regime. A product built for India today should enforce the G.S.R. 853(E) duty cycle in firmware regardless of what the LoRaWAN stack's IN865 region allows. (Interpretation; confirm with the WPC/ETA test lab — open item.)
- LoRaWAN IN865-867 band plan [S2]: three mandatory default/join channels 865.0625, 865.4025, 865.985 MHz, 125 kHz, DR0–DR5 (SF12–SF7), optional DR7 FSK 50 kbps; RX2 default 866.550 MHz DR2; end-devices must store ≥ 24 channels; TXPower steps of 2 dB below Max EIRP. All of IN865 is inside 865–867 MHz, i.e. inside the 865–868 MHz G.S.R. 853(E) band.

### 5.2 EU — ERC/REC 70-03 Annex 1 (non-specific SRD), harmonised standard EN 300 220

Current EFIS rendering of ERC/REC 70-03 Annex 1 (retrieved 2026-11-14) [S4]:

| Band | Frequency | Power | Access | Standard |
|---|---|---|---|---|
| h1.3 | 863–865 MHz | 25 mW e.r.p. | ≤ 0.1 % or LBT+AFA | EN 300 220 |
| h1.4 | 865–868 MHz | 25 mW e.r.p. | ≤ 1 % or LBT+AFA | EN 300 220 |
| h1.5 | 868.0–868.6 MHz | 25 mW e.r.p. | ≤ 1 % or LBT+AFA | EN 300 220 |
| h1.6 | 868.7–869.2 MHz | 25 mW e.r.p. | ≤ 0.1 % or LBT+AFA | EN 300 220 |
| h1.7 | 869.4–869.65 MHz | 500 mW e.r.p. | ≤ 10 % or LBT+AFA | EN 300 220 |
| h1.9 / h1.8 | 869.7–870 MHz | 25 mW / 5 mW e.r.p. | ≤ 1 % / none | EN 300 220 |

LoRaWAN EU863-870 [S2]: default channels 868.1/868.3/868.5 MHz (h1.5, < 1 % duty cycle), default Max EIRP +16 dBm (= +14 dBm e.r.p.), RX2 869.525 MHz (h1.7, 10 %); LoRaWAN uses duty-cycle limitation, not LBT. ERC/REC 70-03 Annex 2 also has a 865–868 MHz 500 mW e.r.p. / APC / 2.5 %–10 % entry for tracking, tracing and data acquisition (India's Table II is the same structure) — UNVERIFIED here (EFIS Annex 2 page did not render).

### 5.3 One hardware build for India + EU

Yes. IN865 (865–867 MHz) and EU868 (863–870 MHz) are adjacent and both lie in the 862–870 MHz "800 MHz" variant of every SX126x/STM32WL module (e.g. RAK3172 lists IN865 together with EU868 and RU864 on the same hardware variant [S10]); the SX126x HP PA output (+22 dBm max) is backed off in firmware to region limits. Region (IN865/EU868), TX power, APC and duty cycle are firmware settings. One RF matching network / SAW-less design covers 863–870 MHz. What differs per region is certification paperwork (WPC ETA in India; CE-RED with EN 300 220-2 / EN 301 489-1/-3 / EN 62368-1 / EN 62311 in EU) and the firmware region lock.

## 6. Gateway side: single-channel transceiver vs 8-channel concentrator

### 6.1 What the same single-channel module on the gateway CAN do
- Act as the hub of a **private LoRa star / point-to-multipoint network**: gateway and nodes share one (or a few, time-scheduled) channel(s) and one agreed SF/BW; gateway-scheduled polling or TDMA avoids collisions.
- Use Zephyr's base LoRa P2P API (`lora_config/lora_send/lora_recv`, in-tree for SX126x/STM32WL) [S23, S22] with a UC-defined frame format + AES-CCM authentication/encryption.
- Optionally run a LoRaWAN-*like* MAC (e.g. reuse LoRaWAN frame format and keys) on a fixed channel — but that is a private network, not LoRaWAN-compliant.

### 6.2 What it CANNOT do
- **It is not a LoRaWAN gateway.** An SX126x / STM32WL radio demodulates one packet at a time, on one frequency, at one pre-set SF/BW. LoRaWAN devices pick channels pseudo-randomly from ≥ 3 default channels (IN865: 865.0625/865.4025/865.985 MHz; EU868: 868.1/868.3/868.5 MHz) and SF7–SF12 via ADR [S2]; a single-channel receiver misses most of that traffic, cannot serve ADR properly, and cannot be connected as a regular gateway to public/third-party LoRaWAN network servers. Off-the-shelf LoRaWAN sensors therefore cannot be supported reliably with this module.
- No multi-SF simultaneous reception, no fine timestamp/geolocation, no Class B beacons with GPS timing.
- **Capacity is limited by airtime and duty cycle.** Airtime for a 20-byte payload, BW 125 kHz, CR 4/5, 8-symbol preamble, explicit header, CRC (calculated with the Semtech airtime formula): SF7 56.6 ms, SF9 185 ms, SF10 371 ms, SF12 1,319 ms. Unscheduled ALOHA at 10 % channel load (≈ 82 % success) allows roughly 6,360 (SF7), 970 (SF10) or 270 (SF12) uplinks/hour per channel — e.g. ~100 nodes reporting every minute at SF7, or ~20 nodes every 4–5 minutes at SF12. Gateway-scheduled polling roughly doubles to quadruples usable throughput. Calculation, not a vendor figure.
- **Downlinks are duty-cycle limited at the gateway:** India Table II: ≤ 10 % for network access points [S1]; EU: 869.4–869.65 MHz 10 % (500 mW), 868.0–868.6 MHz 1 % [S4]. In India, nodes ≤ 2.5 % [S1].

### 6.3 8-channel concentrators (for an optional future "LoRaWAN gateway" card)

| Module | Chipset | Interface / host | Bands | Power | Certs | Price | Source |
|---|---|---|---|---|---|---|---|
| RAKwireless RAK5146 | SX1303 + SX1250 (+ SX126x for LBT variants) | mPCIe 52-pin; SPI *or* USB (USB via on-board STM32L412 bridge); 3.3 V ≥ 1 A; GPS ZOE-M8Q for fine timestamp | 8xx variant: EU868/RU864/IN865 | TX 27 dBm 512 mA; RX 81.6 mA typ | ANATEL, CE, FCC, IMDA, ISED, JRL, KC, MIC, NCC, RCM, SIRIM, UKCA, **WPC** … | not verified (store rate-limited) | [S31] |
| RAKwireless RAK2287 | SX1302 + 2x SX1250, GPS | mPCIe; SPI slave (USB variants via STM32L412); firmware for Raspberry Pi 3B+/4 | EU868/IN865/… | TX 27 dBm 511–513 mA; RX 70–101 mA | CE, FCC, ISED, KC, NCC, RCM, **WPC** | not verified; lifecycle not stated | [S32] |
| Seeed WM1302 (SPI, EU868) | SX1302 + SX1250 (+ SX1262 LBT SKU) | mPCIe, SPI (USB version separate) | EU868 | 7.5 mA standby, 415 mA max TX | CE, UKCA | **USD 25.00** (≈ INR 2,348) single, Seeed store 2026-11-14; bulk on request | [S33] |

Host requirement: Semtech's reference `sx1302_hal` + packet forwarder targets a **Linux host** (Raspberry Pi given as the example; cross-compile for arm-linux-gnueabihf); the STM32 on USB variants is only a USB↔SPI bridge, not a host [S34]. There is no Semtech-supported MCU/RTOS host for SX1302/SX1303 — driving one from the baseboard's low-cost MCU would mean porting the HAL and packet forwarder (or Basic Station) to bare-metal/Zephyr: possible in principle but unsupported and a large effort (assessment). Practically, a LoRaWAN-gateway card = concentrator + small Linux SoM (or a gateway card that tunnels raw SPI to a Linux host elsewhere). Concentrator alone (≈ INR 2,300+) already exceeds the INR 1,000 module target.

### 6.4 Recommended requirement wording
- "REQ-LORA-01: The LoRa module shall support a private, gateway-coordinated LoRa star network (point-to-multipoint) in IN865 (865–867 MHz) and EU868, using the same module hardware on the gateway and on field nodes."
- "REQ-LORA-02: The LoRa module on the gateway is a single-channel transceiver; it is NOT a LoRaWAN gateway and need not interoperate with third-party LoRaWAN end devices."
- "REQ-LORA-03: Node firmware shall be able to operate as a LoRaWAN 1.0.4 Class A end device (IN865/EU868) towards third-party LoRaWAN networks." (STM32WL and SX1262 both support this via LoRaMac-node on Zephyr [S23].)
- "REQ-LORA-04 (optional, later): A separate LoRaWAN concentrator card (SX1302/SX1303, 8 channels) with a Linux-capable host may be offered; target cost and host to be defined separately."
- "REQ-LORA-05: Firmware shall enforce regional TX power, adaptive power control and duty cycle (India G.S.R. 853(E): ≤ 2.5 % node / ≤ 10 % gateway at ≤ 500 mW e.r.p. with APC; EU ERC/REC 70-03 per sub-band)."

### 6.5 Open LoRa star / mesh stacks on Zephyr
- In-tree: Zephyr LoRa P2P API (SX1261/2, SX1272/6, STM32WL) and LoRaWAN (LoRaMac-node backend, all regions; native backend EU868 Class A only) [S23].
- No mature open-source LoRa **mesh** stack running on Zephyr was confirmed in this session (web search budget exhausted). Known projects such as Meshtastic and LoRaMesher target Arduino/PlatformIO/ESP-IDF stacks — Zephyr support UNVERIFIED. Recommendation: a thin custom star protocol on Zephyr's LoRa API (gateway-polled, AES-CCM, sequence counters), optionally a single-hop repeater role later; avoid mesh in v1 (duty-cycle limits make mesh relaying expensive).

## 7. Costed BOM estimates vs BOM ≤ ~INR 714

Rate: USD 1 = INR 93.9 [S5]. Lines marked EST are engineering estimates without a source in this report (to be replaced by R06 power-block and R07 connector results); radio lines are sourced.

| Line | A1: RAK3172 (pre-cert) | A2: STM32WLE5CCU6 chip-down | B1: SX1262 + nRF54L15 chip-down | B2: RAK4630 | B3: E22-900M22S + small MCU |
|---|---|---|---|---|---|
| Radio / SoC | 562 (RAK list USD 5.99 [S14]) – 659 (DigiKey IN @900 [S13]) | 229–255 (LCSC snapshot USD 2.44–2.72 [S12]); DigiKey IN 587 [S11] | 575 (SX1262 DigiKey IN @1k [S24]) + 461 (nRF54L15 DigiKey IN [S27]) = 1,036 | UNVERIFIED (not priced) | 542 (E22, Hubtronics single [S29]) + MCU 60–100 EST |
| TCXO/crystals, RF switch, matching, SMPS L | in module | 60–100 EST | 70–110 EST | in module | in module |
| 40-pin stackable B2B connector (module side) | 60–120 EST | 60–120 EST | 60–120 EST | 60–120 EST | 60–120 EST |
| Power: 12–24 V buck + Li-ion charger + protection + reverse-polarity/TVS | 120–200 EST | 120–200 EST | 120–200 EST | 120–200 EST | 120–200 EST |
| Antenna connector (bulkhead SMA + U.FL pigtail or PCB SMA) + RF ESD | 35–70 EST | 35–70 EST | 35–70 EST | 35–70 EST | 35–70 EST |
| PCB (4-layer, small), passives, terminals | 40–70 EST | 50–80 EST | 50–80 EST | 40–70 EST | 40–70 EST |
| **BOM total (INR)** | **≈ 817–1,119** | **≈ 554–825** | **≈ 1,371–1,616** | > 900 (likely) | **≈ 857–1,102** |
| Finished (x1.4) | 1,144–1,567 | 776–1,155 | 1,919–2,262 | > 1,260 | 1,200–1,543 |
| Verdict vs INR 1,000 | **Over** at verified prices; fits only if RAK volume price ≤ ~USD 4 and power block ≤ INR 120 (UNVERIFIED) | **Feasible / marginal** — fits at low end of estimates; adds one-time RF certification (CE-RED + WPC ETA) NRE | **Not feasible** at verified distributor prices; needs volume quotes ≈ USD 2–3 per IC | Not feasible | Not feasible |

Note also the enclosure (every module is individually enclosed, stackable) is not in the BOM ceiling defined in the brief; if the enclosure must come out of the same INR 714, every option is over budget. Open decision.

## 8. Low-power and RF design notes

- **Sleep currents (module/IC level):** RAK3172 1.69 µA @ 3.3 V; RAK3172-F 2.2 µA [S10]; E77-900M22S 3 µA (software shutdown) [S35]; RAK4630 4.23 µA [S25]; nRF54L15 0.7–2.9 µA [S28]. In practice the **power stage dominates**: the 12–24 V buck, charger and fuel-gauge quiescent currents (e.g. LMR36506 4 µA Iq, BQ25185 30 µA input-side sleep — see R06) must be bypassed or disabled on battery. Target total node sleep ≤ 10 µA from the cell: the battery should feed the 3.3 V rail directly through an LDO/buck with ≤ 1 µA Iq, with the 12–24 V path fully off.
- **TCXO vs crystal:** E77-900M22S uses a 32 MHz crystal (not TCXO), max 21.5 dBm per its datasheet [S35]; RAK3172-T/-F use a TCXO (±2.5 ppm, -TE ±0.5 ppm) and are rated −40…85 °C vs −20…85 °C for the crystal RAK3172 [S10]. For industrial temperature range and SF11/SF12 links, specify a TCXO variant (RAK3172-T) or a TCXO in chip-down designs.
- **RF switch control:** STM32WL needs GPIO-driven RF-switch control for RFO_HP / RFO_LP / RX paths (configured in board files; Zephyr's STM32WL radio binding handles it via devicetree [S22]). SX1262 can drive the RF switch from its DIO2 pin (SX126x feature; UNVERIFIED here because the official SX1262 datasheet could not be downloaded). Pre-certified modules integrate this.
- **Antenna ESD:** the enclosed module exposes the antenna on an external connector → IEC 61000-4-2 (±8 kV air / ±4 kV contact minimum, industrial EN 61000-6-2 levels) hits the RF pin. Use a DC-grounded antenna path (shunt inductor at the connector) and/or an ultra-low-capacitance RF TVS (< 0.5 pF at 868 MHz), plus a grounded bulkhead connector bonded to the enclosure/PE. (Design guidance; component choice to be verified.)
- **SMA vs U.FL:** U.FL/IPEX is for board-internal links only (low mating-cycle rating, fragile). An enclosed, standalone module needs a **bulkhead SMA (female) on the enclosure**, fed by a U.FL→SMA pigtail (RAK3172 "I" variant / E77 IPEX) or a PCB edge SMA (RF-pad variants "NI"/stamp hole). The PCB-edge SMA is cheaper and more repeatable in production; the pigtail allows flexible enclosure placement.
- **Pre-certified antenna constraints:** module approvals are valid only with the antenna type/gain and output power tested. The RAK3172 Indian ETA is at **0.0244 W e.r.p.** (≈ 14 dBm e.r.p.) [S15] — higher power or higher-gain antennas need re-testing. In the EU, CE-RED of the end product is the product maker's responsibility; module test reports (EN 300 220-2) can be reused only within the module's tested conditions. Specify one approved antenna list (e.g. ≤ 2–3 dBi dipole) in the product documentation.

## 9. Security: key storage and secure boot

| Option | On-chip security | Key storage options | Secure boot |
|---|---|---|---|
| STM32WLE5 (RAK3172, E77, chip-down) | AES-256 accelerator, TRNG, OTP, flash protection (Zephyr lists `st,stm32-aes`, RNG, OTP) [S22]; no TrustZone on WLE5 (UNVERIFIED in this session) | Keys in protected flash/OTP with readout protection; or external secure element | MCUboot (Zephyr) with signed images; hardware-anchored immutability relies on STM32 write/readout protection — UNVERIFIED details. STM32WL55 (dual core) adds an isolated secure CPU with ST's KMS/SBSFU (UNVERIFIED in this session) |
| nRF54L15 (Option B) | TrustZone, tamper detection, side-channel-protected crypto engine [S28]; secure boot / secure storage / TEE listed for the series [S28] | On-chip secure storage (TrustZone/PSA); external SE optional | MCUboot / nRF Connect SDK secure boot — strongest of the candidates |
| nRF52840 (RAK4630) | CryptoCell-310, AES, RNG [S30] | CryptoCell-protected keys / external SE | MCUboot |

Recommendations:
- On the **gateway**, LoRa network/session keys should live in the **baseboard secure element** (product-owner decision 2026-11-13) — the LoRa module then only needs session keys in RAM; this keeps the module cheap.
- A **standalone node** has no baseboard: either (a) store keys in MCU protected flash with readout protection + signed MCUboot images (lowest cost, adequate for CRA "secure by default" if debug is locked), or (b) add a low-cost secure element footprint as an assembly option (cost UNVERIFIED; check under R08). Recommend (a) for v1 with (b) as an optional footprint.
- Use LoRaWAN 1.0.4 (or 1.1) with per-device root keys provisioned at manufacture; private-star protocol must use per-device keys, AES-CCM with frame counters and replay protection.

## 10. Standalone node: minimal sensor interfaces

Since IO/ADC live only on the baseboard, a standalone LoRa node must bring its own minimal interface on its terminal block. Recommended minimum (optional assembly variant, so the gateway-side build does not carry the cost):
- 1x RS-485 half-duplex (Modbus RTU sensors) with TVS — EST INR 40–70 (transceiver + protection + 3-pin terminal).
- 2x digital inputs (dry contact / pulse counter, wake-from-sleep capable) with series-R/TVS — EST INR 10–20.
- Optionally 1x I2C/3.3 V sensor header (internal temperature/humidity) — EST INR 5–10 (connector only).
- Analog 4–20 mA / 0–10 V input: not recommended on the LoRa module (needs a precision front end; EST INR 40–80); use a Modbus sensor instead.

Total EST INR 55–100 for RS-485 + 2 DI, which pushes A2 to the top of the BOM ceiling; keep it as a "-N" (node) variant. The STM32WLE5 has UART/I2C/SPI/ADC on chip; the RAK3172 exposes UART/I2C/SPI pins [S10, S22].

## 11. Risks and open decisions

1. **Cost:** only the chip-down STM32WLE5CCU6 design fits BOM ≤ INR 714, and only at LCSC-class pricing (USD 2.4–2.7) — verified Indian distributor price (INR 587) breaks it. Need ST-franchise volume quote. RAK3172 at verified prices takes 79–92 % of the BOM.
2. **Certification NRE for chip-down:** full CE-RED (EN 300 220-2, EN 301 489-1/-3, EN 62368-1, EN 62311) and WPC ETA testing for the radio — one-off cost not in BOM; decide pre-cert module (pilot) vs chip-down (volume).
3. **India regulatory mismatch:** LoRaWAN RP002 IN865 says no duty cycle; G.S.R. 853(E) imposes 2.5 %/10 % with APC at 500 mW e.r.p., or 1 % at 25 mW e.r.p. Confirm interpretation with a WPC-recognised lab; RAK3172 ETA is at 25 mW e.r.p.
4. **Zephyr LoRaWAN backend transition:** LoRaMac-node is deprecated by Semtech; Zephyr port to LoRa Basics Modem "in progress" [S23].
5. **Longevity:** ST 10-year rolling commitment for STM32WL [S20, S21]; exact "available until" date unverified. No module vendor longevity commitments found; Semtech SX1262 lifecycle commitment not verified.
6. **Lead times:** STM32WLE5CCU6 52 weeks (DigiKey factory LT), SX1262 26 weeks, RAK3172 20 weeks [S11, S24, S13] — buffer stock needed.
7. **Enclosure cost** and whether it is inside the INR 1,000 target — open.
8. **Gateway capacity:** single-channel private network capacity (section 6.2) must be accepted by product management; LoRaWAN-gateway capability deferred to an optional Linux-hosted concentrator card.
9. **Option B economics:** SX1262 + nRF54L15 does not fit without volume pricing; decide whether Option B is a cost-down path or a premium (BLE-commissioning, higher-security) variant.

## 12. Sources

All accessed 2026-11-14 unless noted.

- S1 G.S.R. 853(E), 10-Dec-2021, "Use of Low Power Equipment in the Frequency Band 865-868 MHz for Short Range Devices (Exemption from Licence) Rules, 2021", Gazette of India (copy hosted by Tripura High Court): https://www.thc.nic.in/Central%20Governmental%20Rules/use%20of%20low%20power%20Equipment%20in%20the%20frequency%20band%20865%20to%20868%20MHz%20for%20Short%20Range%20Devices%20Exemption%20from%20Licence%20Rules,2021.pdf (DoT mirror, not reachable: https://dotws.cdot.in/sites/default/files/The%20use%20of%20low%20power%20equipment%20in%20the%20frequency%20band%20865-867%20MHz%20for%20short%20range%20devices%20%28Exemption%20from%20License%29%20Rules%2C%202021.pdf)
- S2 LoRa Alliance, RP002-1.0.4 LoRaWAN Regional Parameters (sections 2.4 EU863-870, 2.12 IN865-867): https://resources.lora-alliance.org/document/rp002-1-0-4-regional-parameters
- S3 G.S.R. 271(E) 2024 amendment (2018 low-power SRD rules): https://www.preprodeservices.dot.gov.in/sites/default/files/circular-notifications/use-of-low-power-and-very-low-power-short-range-radio-frequency-devices-exemption-from-licensing-requirement-amendment-rules-2024.pdf
- S4 CEPT EFIS, ERC/REC 70-03 Annex 1 Non-specific SRD table (EFIS v11.0.1, 10-Nov-2026): https://efis.cept.org/adhoc_grabber.jsp?annex=4
- S5 CurrencyBeacon USD/INR 93.9306 (2026-11-08): https://currencybeacon.com/rates/USD/INR
- S10 RAK3172 datasheet (RAK docs): https://docs.rakwireless.com/product-categories/wisduo/rak3172-module/datasheet/
- S11 DigiKey India STM32WLE5CCU6: https://www.digikey.in/en/products/detail/stmicroelectronics/STM32WLE5CCU6/13557445
- S12 LCSC STM32WLE5CCU6 C2888218 / C6689612 (search-index snapshot): https://www.lcsc.com/product-detail/C2888218.html , https://www.lcsc.com/product-image/C6689612.html
- S13 DigiKey India RAK3172-8-SM-NI: https://www.digikey.in/en/products/detail/rakwireless-technology-limited/RAK3172-8-SM-NI/17138049
- S14 RAK store RAK3172 (list price from search snippet; page returned HTTP 429): https://store.rakwireless.com/products/wisduo-lpwan-module-rak3172
- S15 RAK3172 WPC ETA certificate ETA-SD-20240707058: https://downloads.rakwireless.com/LoRa/RAK3172/Certification/RAK3172_WPC_Certification.pdf
- S16 RAK3172-SiP certification page: https://docs.rakwireless.com/certification/product-compliance-certification/wisduo/rak3172-sip/
- S17 Hubtronics India E77-900M22S: https://hubtronics.in/e77-900m22s
- S18 Ebyte E77-900M22S store page: https://ebyteiot.com/products/ebyte-oem-odm-e77-900m22s-small-size-anti-interference-868-930mhz-lorawan-module-wireless-communication-module
- S19 Wio-E5 retail/retirement: https://thinkrobotics.com/ar/products/wio-e5-wireless-module-bulk-stm32wle5jc-arm-cortex-m4-and-sx126x-embedded-supports-lorawan-on-eu868-us915 , https://www.sparkfun.com/grove-lora-e5-stm32wle5jc-module.html
- S20 ST community, "How to check STM32 part numbers longevity": https://community.st.com/t5/stm32-mcus/how-to-check-stm32-part-numbers-longevity/ta-p/863108
- S21 ST STM32WL5x product-line overview (10-year longevity): https://www.st.com.cn/resource/en/product_presentation/microcontrollers-stm32wl5x-ex-product-line-overview.pdf
- S22 Zephyr board RAK3272S (RAK3172, STM32WLE5CC): https://docs.zephyrproject.org/latest/boards/rakwireless/rak3272s/doc/index.html
- S23 Zephyr LoRa/LoRaWAN documentation (latest, source updated 15-Apr-2026): https://docs.zephyrproject.org/latest/services/connectivity/lora_lorawan/index.html
- S24 DigiKey India SX1262IMLTRT: https://www.digikey.in/en/products/result?keywords=SX1262IMLTRT
- S25 RAK4630 datasheet (RAK docs): https://docs.rakwireless.com/product-categories/wisduo/rak4630-module/datasheet/
- S26 Semtech LR2021 product page: https://www.semtech.com/products/wireless-rf/lora-plus/lr2021
- S27 DigiKey India nRF54L15-QFAA-R: https://www.digikey.in/en/products/result?keywords=NRF54L15-QFAA-R
- S28 Nordic nRF54L15 product page: https://www.nordicsemi.com/Products/nRF54L15
- S29 Hubtronics India E22-900M22S: https://hubtronics.in/e22-900m22s
- S30 Zephyr board RAK4631: https://docs.zephyrproject.org/latest/boards/rakwireless/rak4631/doc/index.html
- S31 RAK5146 datasheet: https://docs.rakwireless.com/product-categories/wislink/rak5146/datasheet/
- S32 RAK2287 datasheet: https://docs.rakwireless.com/product-categories/wislink/rak2287/datasheet/
- S33 Seeed WM1302 SPI EU868: https://www.seeedstudio.com/WM1302-LoRaWAN-Gateway-Module-SPI-EU868-p-4889.html
- S34 Semtech sx1302_hal (Linux host): https://github.com/Lora-net/sx1302_hal
- S35 Ebyte E77-900M22S datasheet (Chinese, LCSC-hosted; local copy in datasheets/lora): https://atta.szlcsc.com/upload/public/pdf/source/20220808/8D223242895111DB8038AD57273E964F.pdf

Note: the web-search budget ran out part-way through this research. Items marked UNVERIFIED could not be checked against a primary source in this session.
