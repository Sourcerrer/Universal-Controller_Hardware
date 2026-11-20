# R21 — Nordic nRF91 series (nRF9151 / nRF9161 / nRF9160): fit for the India-first product family

Date: 2026-11-15. FX: 1 USD = INR 93.9. Prices are ex-GST. Background (not repeated): R02 (cellular survey; nRF9151 noted as LTE-M/NB-IoT only), R17 (Tier-1 EC200A card, GNSS / AIS-140), R09 (Zephyr support; nRF91 modem library lives in nRF Connect SDK, not upstream Zephyr), PRD CELL-1…CELL-11, PWR-1/2/5/9. Internal reports are cited as [R0x]/[R1x].

Legend: **UNVERIFIED** = not confirmed from a primary source in this run. "E" in BOM tables = engineering estimate.

---

## 1. Summary verdict

1. **The nRF9151 is the only nRF91 part to design with today.** The nRF9161 page says "Discontinued" and points to the nRF9151 [3]. The nRF9160 is still in production, but Nordic recommends the nRF9151 for new designs [4]. It is also declared feature-complete in nRF Connect SDK v3.4 LTS [9].
2. **India network verdict: an nRF91 product cannot be sold as a general "works anywhere in India" cellular product today.**
   - The nRF91 supports **LTE-M and NB-IoT only**. It has **no 2G/GSM, no LTE Cat 1 and no Cat 4** [1][2].
   - **LTE-M: no commercial LTE-M network was found in India** [23][24][25][26].
   - **NB-IoT exists:**
     - **Jio:** about 95 % population coverage [23]. A 2026 user report says it works with the nRF9160/9151 in 7–8 states [25].
     - **Airtel:** described as "nationwide NB-IoT" [24], but reported as poor in Bangalore [25].
     - **Vi:** pilots only (2019) [28].
     - **BSNL:** nothing found.
   - **SIMs:** NB-IoT needs **enterprise M2M SIMs**. Production SIMs need IP/port whitelisting with Jio [25], and buying SIMs needs a company and GST registration [26]. Consumer SIMs are not a route.
   - **Where it works:** a product limited to Jio NB-IoT (with Airtel as a second option) can be sold for **static, low-data devices** where coverage is checked on site.
3. **Correcting the "GSM" assumption:** the nRF91 has no GSM fallback of any kind [1][2]. Jio is 4G-only and has no 2G anyway [23]. With no LTE-M in India, an nRF91 device in India is in practice an **NB-IoT-only device: 30 kbit/s down / 60 kbit/s up (Cat-NB1)** [12], with no network fallback.
4. **Owner target, a cellular + GPS stack card for under INR 600 BOM, is not reachable with any nRF91 part.**
   - **The SiP alone costs more than the target:**
     - About **INR 1,480 at 1k** (Future Electronics USD 15.78 @200+ [17]; DigiKey India INR 1,535 @500 [15]).
     - About **INR 1,290 at 5k**, using the lowest public listing (USD 13.75 [16]). Nordic volume pricing is UNVERIFIED.
   - **Minimal card** (SiP, SIM, LTE + GNSS connectors and LNA, 5–32 V / USB-C PD power, Li-ion, bus headers, PCB, enclosure):
     - At 1k: **≈ INR 2,460**, or ≈ 2,235 without the cell.
     - At 5k: **≈ INR 2,175**, or ≈ 1,960 without the cell.
   - **Gap: ≈ INR 1,575–1,860 over target** (full card with cell). The lowest realistic nRF91 card is **≈ INR 1,740** (5k, lean power front end, U.FL, no cell, no enclosure).
   - Details are in section 2.
5. **Role-by-role fit:**
   - **(a) Tier-1 4G card: NO.** It runs at roughly 1/1000 of the EC200A's Cat 4 throughput in India, has no Ethernet, and gives NB-IoT-only coverage.
   - **(b) Standalone low-power node / data logger running our Zephyr app on the modem: YES (best fit), conditional on Jio NB-IoT coverage at the site.** It is the cellular twin of the LoRa node.
   - **(c) Vehicle / AIS-140 tracker: NO.** It has GPS + QZSS only (no NavIC, no GAGAN stated), and NB-IoT has no handover for moving vehicles [2][12]. **Static or slow asset tracking: partial.**
   - **(d) Backup / low-cost uplink for the baseboard: weak.** It is NB-IoT only and costs about INR 1,000 more than a Cat 1 bis card that works on every Indian LTE network [R02].
6. **Best-fit product: "Cellular node" (nRF9151, Zephyr app on the SiP, GPS, RS-485 + 2 DI, Li-ion, 5–32 V / USB-C PD, DIN enclosure).**
   - **BOM ≈ INR 2,860 at 1k** (≈ 2,515 at 5k).
   - **Ex-works ≈ INR 5,840** (5k: ≈ 5,160), using BOM × 1.5 + INR 200 royalty + 30 % profit.
   - Recommendation: build it as a **pilot SKU** only after a Jio NB-IoT site survey. **Do not add the nRF91 to the gateway stack.**
7. **Worth knowing: Nordic nRF93M1 (Cat 1 bis module, 2026).**
   - It covers India's FDD and TDD LTE bands (B1/3/5/8/28, B40/41 on the LABA variant) at 10/5 Mbit/s [21].
   - It works on every Indian 4G network, but **it does not run customer code and has no GNSS** [21].
   - It costs about USD 13.5 (≈ INR 1,270) [22], which is 2.5–4 × a Quectel EG800K / EC800M Cat 1 bis [R02].
   - It is not a cost answer. It is an option only if a Nordic-only toolchain becomes a rule.

---

## 2. HEADLINE — owner concept: nRF91 cellular + GPS stack card under INR 600 BOM

Concept (owner, 2026-11-15) is an all-Zephyr gateway:
- STM32H573 baseboard (secure brain, IO)
- ESP32-C6 (Wi-Fi + BLE)
- STM32WLE5 (LoRa)
- nRF91 (cellular + GPS)

The modules talk over the stack bus (UART / SPI, no Ethernet).

### 2.1 Can the SiP, or a minimal card, reach INR 600 BOM?

**No, at either volume.** INR 600 is USD 6.39, and the SiP alone is about 2.1–2.5 × that.

| Source | Part | Qty | Unit | INR | Ref |
|---|---|---|---|---|---|
| DigiKey US | NRF9151-LACA-R7 | 500 | USD 18.28 | 1,717 | [13] |
| DigiKey US | NRF9151-LACA-R (CT) | 500 | USD 16.89 | 1,586 | [14] |
| DigiKey US | NRF9151-LACA-R (T&R) | 2,000 | USD 17.07 | 1,603 | [14] |
| **DigiKey India** | NRF9151-LACA-R7 | 500 | **INR 1,535.15** (0 in stock on that listing; 2,196 on the -R7 sister listing) | 1,535 | [15] (search snippet) |
| Future Electronics | NRF9151-LACA-R7 | 200+ | USD 15.78 | 1,482 | [17] (search snippet) |
| Rutronik | NRF9151-LACA-R7 | n/s | USD 16.48 | 1,547 | [16] |
| Braemac (lowest public) | NRF9151-LACA-R/-R7 | n/s (0 stock) | USD 13.75 | 1,291 | [16] |
| Nordic direct volume (5k+) | — | 5k | **UNVERIFIED** (no public figure) | — | — |

Planning prices:
- **1k: INR 1,480.**
- **5k: INR 1,290.** This is the lowest public figure. A Nordic quote could be lower, but even USD 10 (INR 939, UNVERIFIED) leaves no room under INR 600.

### 2.2 No GSM: what the nRF91 lacks, and what it means in India

- **Modes:** the nRF9151 modem supports Cat-M1, Cat-NB1/NB2 and IoT-NTN (satellite) only [2]. There is **no GSM/GPRS, no WCDMA and no LTE Cat 1/4**. The nRF9160 and nRF9161 are the same in this respect [4][8].
- **India today:**
  - **LTE-M:** no operator network was found.
  - **NB-IoT:** Jio (about 95 % population) and Airtel (claimed nationwide, uneven in field reports).
  - **Effect:** the card has **NB-IoT as its only working mode**, and no fallback when NB-IoT is absent or the SIM is not NB-IoT provisioned [23][24][25].
- **The EC200A card is different:** it falls back to WCDMA and GSM 900/1800 and works on every Indian LTE band [R17].

### 2.3 Minimal stack card BOM (nRF9151 + GPS, UART/SPI to baseboard)

Design notes:
- **The SiP runs directly from the Li-ion / charger VSYS** (3.0–5.5 V [1]), so no 3.8 V modem buck is needed.
- **The GNSS input gets an external LNA + SAW** (practice from Nordic's DK; UNVERIFIED in this run) and an SMA with active-antenna bias.
- **Bus link:** UART with RTS/CTS, plus one wake GPIO.
  - The SiP can run Nordic's **Serial Modem** firmware: the baseboard uses Zephyr's in-tree `cellular_nordic_nrf91_slm` driver [R09].
  - Or it can run our own Zephyr app that exposes a message API.

| # | Item | Part | INR @1k | INR @5k | Basis |
|---|---|---|---|---|---|
| 1 | Cellular + GNSS SiP | nRF9151-LACA | 1,480 | 1,290 | [15][16][17] |
| 2 | Nano-SIM holder + ESD (MFF2 eSIM footprint DNP) | push-push + TVS | 18 | 16 | [R17] |
| 3 | LTE SMA + GNSS SMA | edge SMA × 2 | 70 | 60 | [R17] |
| 4 | GNSS LNA + SAW + matching + bias | BGA524N6 class + SAW | 53 | 45 | E |
| 5 | USB-C receptacle + PD sink (≤ 20 V) + 5 V-capable front end | CH224K / STUSB4500 class | 80 | 70 | PWR-9 estimate (PRD) |
| 6 | Input TVS + reverse / ideal-diode OR | SMCJ33A + LM74700 + FET | 61 | 55 | [R17] |
| 7 | Buck 5–32 V → 5 V | LMR51430 | 65 | 58 | [R17] |
| 8 | Standalone NVDC charger + inductor + NTC | BQ25606 | 70 | 62 | [R17] (UNVERIFIED price) |
| 9 | VBAT bulk + 3.3 V LDO (VDD_GPIO, bus level) | — | 25 | 22 | E |
| 10 | 2 × 2×20 box header (BUS-IN/OUT) + bridge plug | BXCONN | 88 | 80 | [R17] |
| 11 | PCB 4-layer about 50 × 70 mm | — | 50 | 42 | E |
| 12 | Passives, LEDs, SWD pads | — | 40 | 35 | E |
| 13 | DIN enclosure | Electrocom EC7060 | 110 | 100 | [R17] |
| 14 | Cell holder + 18650 2600 mAh (BIS) | — | 251 | 240 | [R17] |
| | **Card BOM** | | **≈ 2,461** | **≈ 2,175** | |
| | Without cell | | ≈ 2,235 | ≈ 1,960 | |
| | **Lowest realistic** (lean Schottky/PTC front end −80, U.FL −40/45, no cell, no enclosure) | | ≈ 2,000 | **≈ 1,740** | |

**Gap to INR 600: ≈ INR 1,140 (lowest realistic, 5k) to ≈ INR 1,860 (full card, 1k).**

**Can anything else meet INR 600 with cellular + GPS?**
- **Not with the PWR-1/2/9 power stack, a Li-ion cell and an enclosure.** Those alone are about INR 650–700 (rows 5–9, 14 and 13).
- **Electronics-only floor, India-wide:**
  - Cat 1 bis modem (EG800K / EC800M, INR 320–500 [R02]).
  - A cheap GPS-only receiver: about INR 150–300, UNVERIFIED.
  - Together about **INR 900–1,200** BOM. That is still above INR 600, but it is 40–50 % of the nRF91 card and covers every Indian LTE network.
  - Weakness: it is not an app-on-modem design.

### 2.4 nRF91 card versus the EC200A Tier-1 card

| Criterion | nRF9151 card (this report) | EC200A-CN card [R17] |
|---|---|---|
| BOM (with cell) | ≈ 2,461 (1k), GPS included | ≈ 2,157 card (≈ 2,011 per brief) + GNSS option ≈ 1,015 → **≈ 3,030–3,170 with GNSS** |
| Bandwidth | **NB-IoT 30/60 kbit/s** (DL/UL) in India; LTE-M 300/375 kbit/s (≈ 100 kbit/s application throughput) only where LTE-M exists — not India [12] | Cat 4: 150/50 Mbit/s; 100 Mbit Ethernet link [R17] |
| India coverage | Jio NB-IoT (≈ 95 % pop.), Airtel NB-IoT (uneven); enterprise SIM, no fallback [23][24][25] | All Indian LTE FDD + TDD bands, WCDMA + GSM fallback; any SIM [R17] |
| GNSS | GPS L1 C/A + QZSS, A-GNSS / P-GPS via nRF Cloud or SUPL; **no NavIC**; GNSS time-shared with LTE (LTE idle/PSM) [2][8] | LC29HAIMD option: GPS + **NavIC** L5 (AIS-140 path) [R17] |
| Power | PSM 2.7 µA; eDRX 81.92 s 18 µA (M1) / 32 µA (NB1) at 3.7 V [2] | Cat 4: amps-class peaks; ≥ 1000 µF bulk; mains/vehicle class [R17] |
| App on modem (CELL-11) | **Yes: Zephyr / nRF Connect SDK on the M33** (1 MB / 256 KB, TrustZone, TF-M) [1][8] | QuecOpen under NDA, or none (standard firmware) [R17] |
| Link to baseboard | UART/SPI only (no Ethernet MAC) [1] | 100BASE-TX PHY-to-PHY + AT UART [R17] |
| Certification | GCF, PTCRB, CE, FCC, ISED, UKCA, RCM, ANATEL, NCC, KC, SRRC, IMDA, TDRA, MIC and others; **no India entry** [5] | Quectel CN variant; India MTCTE of the product needed in both cases [R01][R17] |
| Verdict for the gateway stack | **Not a replacement** | Stays the Tier-1 choice |

**Bottom line for the owner's concept:**
- The all-Zephyr idea is sound: the nRF91 is the best app-on-modem Zephyr part on the market.
- In India, though, it gives a costlier, NB-IoT-only and lower-bandwidth stack card with no NavIC, at about **4 × the INR 600 target**.
- For a gateway stack, keep the EC200A (or a Cat 1 bis card if Ethernet bandwidth is not needed).
- Use the nRF9151 where it is strong: **a standalone node** (section 6).

---

## 3. nRF91 facts

| Item | nRF9151 (current) | nRF9161 / nRF9160 | Ref |
|---|---|---|---|
| Status | Active; DigiKey 16-week lead time; recommended for new designs | 9161: **Discontinued**. 9160: in production, "recommend nRF9151" | [1][3][4][13] |
| 3GPP / categories | Rel-14 Cat-M1, Cat-NB1/NB2; Rel-17 IoT-NTN | 9161: Rel-14; 9160: Rel-13 M1/NB1 | [2][8] |
| LTE-M bands | B1, 2, 3, 4, 5, 8, 12, 13, 18, 19, 20, 25, 26, 28, 66, 85, 106 | 9160: B1-5, 8, 12-14, 17-20, 25, 26, 28, 66 certified | [2][4] |
| NB-IoT bands | B1, 2, 3, 4, 5, 8, 12, 13, 17, 19, 20, 25, 26, 28, 65, 66, 85, 106 | — | [2] |
| **India FDD bands B1/B3/B5/B8/B28** | **All covered for both M1 and NB** (no TDD B40/B41, irrelevant for LTE-M/NB-IoT) | Covered (9160) | [2][4] |
| NTN | B23, 249, 252, 255, 256; Skylo certified (Dec 2025) | — | [2][30] |
| Data rates | LTE-M 300 kbit/s DL / 375 kbit/s UL (≈ 100 kbit/s application over IP); NB1 30 kbit/s DL / 60 kbit/s UL; NB2 up to 127/169 kbit/s if the network supports it | same | [12] |
| TX power | Power Class 3 (23 dBm) and Power Class 5 (20 dBm) | 9161 PC3 | [1][2] |
| GNSS | GPS L1 C/A + QZSS L1 C/A; **no Galileo, no NavIC listed**; A-GNSS (nRF Cloud or SUPL), P-GPS (nRF Cloud); GNSS and LTE time-multiplexed | same | [2][8] |
| App core | Arm Cortex-M33 64 MHz, 1 MB flash, 256 KB RAM (shared with modem library/TF-M; free figure UNVERIFIED) | same | [1][2] |
| Security | TrustZone + TF-M, CryptoCell 310, optional secure boot chain (NSIB + MCUboot), SIM/eSIM (SGP.02/.22/.32), nuSIM, SoftSIM | 9160: **PSA Certified Level 2** (+ SESIP L2) | [1][8][11] |
| PSA level, nRF9151 | **UNVERIFIED** (no listing found) | — | [11] |
| SDK | nRF Connect SDK (Zephyr). Modem library is a binary in nrfxlib. **NCS v3.4.0 is the first LTS (≥ 5-year branch, LTS every 3 years)**; nRF9160/nRF9131 feature-complete in v3.4 | — | [8][9][R09] |
| Modem firmware | Signed binary; full update over SWD or FOTA; **delta FOTA** between versions; major updates need ≥ 4 MB external flash. Current nRF91x1 LTE FW 2.0.4 (2.0.0 → 2.0.4 listed; dates not shown); NTN FW 1.0.1 | 9160: 1.3.x line | [7][8] |
| Security advisories | Coordinated disclosure + myNordic notifications; CRA reporting from 11 Sep 2026. No public nRF91 modem CVE found (UNVERIFIED) | — | [10] |
| Power | PSM 2.7 µA; eDRX 81.92 s: 18 µA (M1) / 32 µA (NB1) at 3.7 V, UICC included | — | [2] |
| DECT NR+ | nRF9151/9161: NR+ up to 21 dBm (bands 1, 2, 9, 22), 19 dBm (band 4); Wirepas stack. India spectrum position for NR+ UNVERIFIED | 9160: no | [2][3] |
| Supply / temp | 3.0–5.5 V; −40…+85 °C | — | [1][2] |
| Package | LGA 12.1 × 11.1 × 1.2 mm (113 pads) | 9161: 10 × 16 mm | [2][3] |
| Peripherals | 4 × SPI/UART/I²C, I²S, PDM, 4 PWM, 12-bit ADC (8 ch), 32 GPIO | — | [1] |

**Modules and boards built on the nRF9151.**
- Nordic lists ten third-party modules/boards [18]: LooUQ MTC2-N9151, Circuit Dojo Feather, Conexio Stratus Pro, CTHINGS.CO, EmCraft SOM, Embever, LMT IoT SOM51UF/SOM51C1, Iscatek MB01B (14 × 20.8 mm) and Sercomm TPM530M (14.5 × 14.5 mm).
- **Nordic nRF91M1** is Nordic's own nRF9151 module. It ships with Serial Modem firmware and is host-controlled. No price is public [20].
- **The SiP itself is already pre-certified**, so a module adds cost (connectors, form factor) without adding certification value for us.
- Prices found:
  - Board / dev-kit level: Circuit Dojo Feather EUR 59.11 [19]; Conexio "BYOS" USD 59 [19]; nRF9151-SMA-DK about USD 116–122 [19].
  - **No 1k module price was found** for Fanstel, Actinius or the others (UNVERIFIED).
  - Actinius and Fanstel products found in searches were nRF9160/9161-based (UNVERIFIED).

**India availability.**
- DigiKey India lists the SiP in INR (INR 1,535 @500) [15].
- element14 Asia-Pacific stocks the SiP (7,452 pcs -R) [16].
- No Indian franchised Nordic distributor price was found (UNVERIFIED).

---

## 4. India network fit

| Operator | NB-IoT | LTE-M | Evidence | nRF91 field reports |
|---|---|---|---|---|
| **Jio** | **Yes**, ≈ 95 % population coverage; Jio is 4G-only (no 2G) | **Not found** | GSMA case study 2023 [23] | Works with nRF9160/9151 across 7–8 states (Bangalore, Chennai), APN `jionpiot`, IP mode. Production SIMs: register SIMs + server IPs/ports with Jio. Band/NB-only lock improved attach [25] |
| **Airtel** | **Yes**, "nationwide NB-IoT" (1.3 M Secure Meters smart meters, Bihar, NB-IoT with 2G/4G fallback) | Not found | [24] | Airtel M2M NB-IoT: poor coverage / unstable attach in Bangalore [25] |
| **Vi** | Pilots in 8 cities and a Genus smart-meter PoC (2019); commercial launch not found | Not found | [28] | none |
| **BSNL** | Not found (satellite NB-IoT with Skylo reported earlier, UNVERIFIED) | Not found | — | none |

- **Bands.** NB-IoT is deployed in FDD spectrum. Nordic staff confirmed that B3/B5/B8 (India) are supported [31], and the nRF9151 also covers B1 and B28 [2]. Which band Jio NB-IoT uses in each circle is UNVERIFIED.
- **SIMs.**
  - Consumer SIMs are not NB-IoT provisioned.
  - M2M/IoT SIMs need a company, GST registration and enterprise onboarding [26]. The SIM must be provisioned for NB-IoT data [25].
  - Small R&D quantities come through distributors (one user bought a Jio NB-IoT SIM via an IndiaMART seller) [25].
  - The Nordic DK's bundled SIM (Onomondo / iBasis class) does not work in India [26].
  - An eSIM (SGP.32) is supported by the SiP [1], but an Indian operator eSIM profile for NB-IoT is UNVERIFIED.
- **No fallback.** There is no 2G, Cat 1 or LTE-M fallback [2]. A device outside Jio/Airtel NB-IoT coverage, or deep indoors beyond NB-IoT's margin, is offline.
- **Mobility.** Nordic positions NB-IoT for **static** devices. LTE-M is the mode with full handover [12], and LTE-M is not available in India.

**Plain statement: an nRF91 product cannot be sold across India as a general cellular product today.** It can be sold as a **Jio-NB-IoT (Airtel second) static-telemetry product**, with a pre-installation coverage check and an enterprise SIM bundled or specified. For anything mobile, high-data or "any SIM", it is not fit for India in 2026.

---

## 5. Certification

- **nRF9151 SiP** [5]:
  - GCF (PC3 ID 13740, PC5 ID 12323) and PTCRB (PC3, PC5, NTN, 2026).
  - CE (DoC Mar 2026, NTN certificate), UKCA, FCC, ISED.
  - RCM, ANATEL, ENACOM, NCC, NBTC, IMDA, KC, SRRC, ICASA, TDRA, MIC/TELEC, CRC.
  - DECT NR+ CE/UKCA.
  - **No India (TEC / WPC) entry.**
  - Skylo NTN certified [30].
  - Nordic says most MNOs need only GCF/PTCRB, but some run their own programmes [6]. **No Jio/Airtel approval of the nRF91 was found** (UNVERIFIED).
- **India product certification:**
  - The finished product needs **TEC MTCTE**, likely as "IoT Gateway" or cellular end-device ER; the category for a cellular node is UNVERIFIED [R01].
  - Cellular is licensed-band user equipment, so WPC ETA applies as for any cellular device. The exact route for LTE UE is UNVERIFIED [R01].
  - **DECT NR+** at 1.9 GHz would need its own WPC review. Its India status is UNVERIFIED.
  - Expect no module-level India certificate to inherit. Budget a full MTCTE campaign at a TEC-designated CAB, as for the EC200A card [R01][R17].
- **Operator acceptance:** Jio's process (SIM/IP whitelisting) is operational rather than type-approval [25]. A formal Jio device-approval requirement is UNVERIFIED. Ask Jio IoT before the pilot.

---

## 6. Role-by-role fit

### (a) Tier-1 4G card in the stack — **NO**
- **No Ethernet MAC.** The link to the baseboard is UART/SPI only (a few Mbit/s) [1], against CELL-9's 100 Mbit Ethernet.
- **Air interface in India:** NB-IoT 30/60 kbit/s, about 1/2,500 of Cat 4's 150 Mbit/s downlink, and 1/1,000 even against LTE-M's 300 kbit/s [12][R17].
- **No routing use cases:** no NAT or router role, no remote web UI, no Modbus-TCP tunnelling at useful rates, and no fallback.
- **Cost:** card ≈ INR 2,460 against the EC200A card ≈ 2,157, so no saving.
- Verdict: keep the EC200A.

### (b) Standalone low-power cellular node / data logger — **YES (best fit), conditional on Jio NB-IoT at site**
- **Matches the owner's way of working:** our Zephyr app runs on the M33 next to the modem. TrustZone/TF-M keeps keys in the secure world, and the NCS 3.4 LTS gives a 5-year branch [8][9].
- **Battery life:** PSM 2.7 µA makes multi-year Li-ion operation realistic for 15-minute-to-hourly reports [2].
- **IO:** same pattern as the LoRa node: RS-485 (Modbus RTU sensors) + 2 DI, using the SiP's UART/GPIO/ADC [1][R04].
- **Advantage over LoRa:** no gateway needed where Jio NB-IoT exists.
- **Cost over LoRa:** BOM about 2.5–3 × the LoRa node.
- **Risks:** NB-IoT coverage, enterprise SIM logistics, MTCTE.

### (c) Vehicle / asset tracker — **NO for vehicles / AIS-140; PARTIAL for static or slow assets**
- **GNSS:** GPS + QZSS only, with **no NavIC (IRNSS) and no GAGAN listed** [2]. AIS-140 requires NavIC + GAGAN [R17], so the nRF91 alone cannot be an AIS-140 VLTD. An external NavIC receiver (LC29HAIMD ≈ INR 813 [R17]) would make it a two-GNSS design and remove the cost argument.
- **Mobility:** NB-IoT is meant for static devices, and LTE-M (the mobility mode) is absent in India [12].
- **GNSS/LTE time-sharing:** GNSS works only while LTE is idle/PSM [8], which suits sparse fixes, not continuous tracking.
- **Good for** containers, gensets, tanks and parked equipment reporting a few fixes a day with A-GNSS/P-GPS.

### (d) Backup / low-cost cellular uplink for the baseboard — **WEAK / NO**
- **Data:** alarms and small telemetry work over NB-IoT. A backup for a gateway normally needs the same reach as the primary link, and the nRF91 has only NB-IoT in India.
- **Cost:** card ≈ INR 2,000–2,460, against a Cat 1 bis card at about INR 1,000–1,300 BOM [R02] that works on every Indian LTE network at 10/5 Mbit/s.
- **Better options:**
  - A Quectel EG800K / EC800M Cat 1 bis card (AT over the bus UART, Zephyr `modem_cellular`) [R02].
  - Nordic nRF93M1-LABA (Cat 1 bis, India bands, ≈ INR 1,270 @700 [22]) only if a Nordic stack is mandated. It has no GNSS and does not run our code [21].

---

## 7. Recommendation and best-fit BOM

**Where the nRF91 fits:**
- A new standalone **"Cellular node" SKU**: Zephyr app on the nRF9151, Jio NB-IoT, GPS, RS-485 + 2 DI, Li-ion.
- Use cases: remote meters, tanks, pumps, gensets, cold-chain loggers, and static asset trackers.
- It sits beside the LoRa node and adds no-gateway deployments.

**Where it does not fit:**
- The Tier-1 gateway card.
- The Tier-2 router.
- Vehicle / AIS-140 trackers.
- A general backup uplink.

**What it adds or replaces:** it adds one SKU and replaces nothing in the stack.

**Owner's INR 600 stack card:** not achievable (section 2). Report the gap per COMP-5.

### 7.1 Cellular node BOM (nRF9151, standalone, DIN)

| # | Item | INR @1k | INR @5k | Basis |
|---|---|---|---|---|
| 1 | nRF9151-LACA SiP | 1,480 | 1,290 | [15][16][17] |
| 2 | Nano-SIM holder + ESD (MFF2 eSIM ≈ +150 as option) | 18 | 16 | [R17] |
| 3 | 2 × SMA (LTE, GNSS) | 70 | 60 | [R17] |
| 4 | GNSS LNA + SAW + bias | 53 | 45 | E |
| 5 | USB-C + PD sink + 5 V-capable front end | 80 | 70 | PWR-9 E |
| 6 | Input TVS + ideal-diode reverse protection | 61 | 55 | [R17] |
| 7 | Buck 5–32 V → 5 V | 65 | 58 | [R17] |
| 8 | Charger BQ25606 + inductor + NTC | 70 | 62 | [R17] |
| 9 | Bulk caps + 3.3 V LDO | 25 | 22 | E |
| 10 | Li-ion 18650 2600 mAh (BIS) + holder | 251 | 240 | [R17] |
| 11 | DC terminal (2-pin pluggable) | 18 | 16 | [R17] |
| 12 | RS-485 transceiver + TVS + 3-pin terminal | 60 | 52 | [R04] E |
| 13 | 2 × DI (dry contact / pulse, wake-capable) | 15 | 13 | [R04] E |
| 14 | 3-axis accelerometer (tamper / motion wake) | 40 | 35 | E (UNVERIFIED) |
| 15 | PCB 4-layer about 55 × 75 mm | 55 | 46 | E |
| 16 | Passives, LEDs, SWD / test pads | 40 | 35 | E |
| 17 | DIN enclosure EC7060 | 110 | 100 | [R17] |
| 18 | LTE stubby antenna (SMA) | 150 | 130 | E (UNVERIFIED, R17 range 150–300) |
| 19 | GNSS active antenna (SMA, 3 m lead) | 200 | 170 | E (UNVERIFIED) |
| | **BOM** | **≈ 2,861** | **≈ 2,515** | |

**Ex-works (owner formula; royalty INR 200 for a small node, as instructed):**

| Qty | BOM | × 1.5 | + Royalty 200 | **Ex-works (× 1.3)** |
|---|---|---|---|---|
| 1k | 2,861 | 4,292 | 4,492 | **≈ INR 5,840** |
| 5k | 2,515 | 3,773 | 3,973 | **≈ INR 5,160** |

Not included: the recurring SIM / data plan, and certification NRE (MTCTE, EMC, safety).

**Lower-cost variants:**
- No GNSS (drop the GNSS SMA, row 4 and row 19): about −290.
- No cell (supercap/primary not costed): about −250.
- LTE antenna as a customer accessory: −150.
- **The leanest node is BOM ≈ 2,170, ex-works ≈ 4,500 (1k)** (2,170 × 1.5 + 200 = 3,455; × 1.3).

### 7.2 Actions
1. **Jio IoT:** NB-IoT coverage map / site survey tool, NB-IoT band per circle, SIM onboarding and pricing, IP-whitelisting process, eSIM availability, and any device approval.
2. **Nordic RSM (India):** 1k/5k/10k SiP quote and lead time; India operator test status; PSA level of the nRF9151.
3. **A TEC CAB:** MTCTE category and ER for a standalone NB-IoT node.
4. **Prototype** on an nRF9151 DK + Jio NB-IoT SIM: attach time, PSM current and data cost per day in 2–3 target sites.

---

## 8. Risks

1. **Network:** NB-IoT only in India; Airtel uneven, Vi/BSNL unproven; no LTE-M. Any operator NB-IoT de-prioritisation strands the product.
2. **SIM logistics:** enterprise onboarding and IP whitelisting per deployment [25]; no "drop in any SIM" story for customers.
3. **Cost:** the SiP is ≈ INR 1,300–1,500 against Cat 1 bis modems at INR 320–500. The nRF91 never wins on cost in India.
4. **No NavIC:** excluded from AIS-140 and from Indian tenders that ask for NavIC.
5. **Certification:** no India entry on Nordic's list [5]; full MTCTE campaign at our cost.
6. **Vendor lock:** modem library is binary, NCS-only [R09]. Mitigated by the NCS 3.4 LTS commitment [9].
7. **Lifecycle:** nRF9161 already discontinued after about 2–3 years [3]. The nRF9151's longevity commitment is UNVERIFIED.
8. **GNSS/LTE time-sharing** limits tracking duty cycles [8].

---

## 9. Not verified in this run
- Nordic volume (5k) price, and the free flash/RAM figure for the application.
- PSA Certified level of the nRF9151.
- nRF91 modem security advisories or CVEs, and firmware release dates.
- Jio NB-IoT band(s) and coverage by circle.
- Vi/BSNL NB-IoT status, and LTE-M absence (the GSMA deployment map returned 403).
- Indian operator device approval.
- MTCTE category for a cellular node.
- India NR+ spectrum.
- Fanstel / Actinius / LooUQ module prices.
- Antenna, LNA, PD-sink and accelerometer prices (estimates).

---

## Sources

1. Nordic nRF9151 product page — https://www.nordicsemi.com/Products/nRF9151
2. nRF9151 Product Specification, key features (HTML) — https://docs.nordicsemi.com/r/bundle/ps_nrf9151/page/nrf9151_html5_keyfeatures.html
3. Nordic nRF9161 product page ("Discontinued") — https://www.nordicsemi.com/Products/nRF9161
4. Nordic nRF9160 product page — https://www.nordicsemi.com/Products/nRF9160
5. nRF9151 Global and regulatory certifications — https://nordicsemi.com/Products/Wireless/Low-power-cellular-IoT/nRF91-Series-certifications/nRF9151-Global-and-regulatory
6. nRF91 Series certifications overview — https://www.nordicsemi.com/Products/Wireless/Low-power-cellular-IoT/nRF91-Series-certifications
7. nRF9151 downloads (modem firmware 2.0.4, NTN 1.0.1, product brief v1.2) — https://www.nordicsemi.com/Products/nRF9151/Download
8. nRF Connect SDK, Features of nRF91 Series (updated 13 Nov 2026) — https://nrfconnectdocs.nordicsemi.com/ncs/latest/nrf/app_dev/device_guides/nrf91/nrf91_features.html
9. NCS long-term support releases — https://nrfconnectdocs.nordicsemi.com/ncs/latest/nrf/releases_and_maturity/ncs_release_model/lts_releases.html ; blog https://devzone.nordicsemi.com/nordic/nordic-blog/b/blog/posts/nrf-connect-sdk-gets-long-term-support-with-version-3-4-0
10. Nordic CRA / vulnerability handling — https://www.nordicsemi.com/Products/Technologies/Security/CRA
11. Nordic news, nRF9160 PSA Certified Level 2 — https://www.nordicsemi.com/Nordic-news/2024/03/Nordic-Semiconductor-endorses-CSAs-IoT-Device-Security-Specification-1-and-Certification-Program
12. Nordic, What is cellular IoT (LTE-M / NB-IoT rates, mobility) — https://www.nordicsemi.com/Products/Wireless/Low-power-cellular-IoT/What-is-cellular-IoT
13. DigiKey NRF9151-LACA-R7 — https://www.digikey.com/en/products/detail/nordic-semiconductor-asa/NRF9151-LACA-R7/24713453
14. DigiKey NRF9151-LACA-R — https://www.digikey.com/en/products/detail/nordic-semiconductor-asa/NRF9151-LACA-R/24713452
15. DigiKey India NRF9151-LACA-R7 (INR) — https://www.digikey.in/en/products/detail/nordic-semiconductor-asa/NRF9151-LACA-R7/24713453 (search snippet)
16. FindChips nRF9151 distributor listing — https://www.findchips.com/search/nrf9151
17. Future Electronics NRF9151-LACA-R7 — https://www.futureelectronics.com/p/5204788 (search snippet)
18. Nordic nRF9151 third-party modules — https://www.nordicsemi.com/Products/nRF9151/Modules
19. Conexio Stratus Pro (CNX) — https://www.cnx-software.com/2024/11/15/conexio-stratus-pro-nrf9151-low-power-iot-development-kit-supports-lte-m-nb-iot-dect-nr-gps-connectivity/ ; Circuit Dojo Feather (DigiKey) — https://www.digikey.fi/en/products/detail/circuit-dojo/PASSY-NRF9151-FEATHER/26580618
20. Nordic nRF91M1 module — https://www.nordicsemi.com/Products/nRF91M1
21. Nordic nRF93M1 datasheet v0.5 — https://www.nordicsemi.com/-/media/Software-and-other-downloads/Product-Briefs/nrf93m1_Datasheet_v0.5.pdf
22. nRF93M1 pricing / availability — https://www.cnx-software.com/2026/08/24/60-nordic-semi-nrf93m1-development-kit-dk-targets-lte-cat-1-bis-iot-applications ; https://www.avnet.com/americas/product/nordic-semiconductor/nrf93m1-laca-r/evolve-308741166/ ; https://www.nordicsemi.com/Nordic-news/2026/08/Nordic-takes-nRF93M1-smart-modem-global-developers-gets-an-easy-precertified-path-for-Cat-1-bis-IoT
23. GSMA, IoT and Essential Utility Services: India market case study (2023) — https://www.gsma.com/mobilefordevelopment/wp-content/uploads/2023/04/IoT-and-Essential-Utility-Services-India-market-case-study.pdf
24. RCR Wireless, Airtel 1.3 M NB-IoT smart meters (2023) — https://rcrwireless.com/20230425/internet-of-things-4/airtel-secures-contract-1-million-smart-meters-india
25. Nordic DevZone, "NB-IoT SIM options for nRF9160 in India" (2026) — https://devzone.nordicsemi.com/f/nordic-q-a/128227/nb-iot-sim-options-for-nrf9160-in-india
26. Nordic DevZone, LTE-M / NB-IoT in India for nRF9160/61 — https://devzone.nordicsemi.com/f/nordic-q-a/108743/evaluating-if-we-can-use-nrf9160-61-to-get-nb-iot-or-lte-m-network-connectivity-in-india-is-there-any-carrier-operator-who-has-deployed-lte-m-network-in-india-available-network-esim-providers-in-india/516268
27. Nordic DevZone, Jio NB-IoT SIM not connecting (older, MFW 1.3.0) — https://devzone.nordicsemi.com/f/nordic-q-a/77639/nb-iot-jio-sim-not-connecting-asset-tracker-work-up-to-rrc-connected-and-stuck-there/326559
28. IEEE ComSoc techblog, Airtel / Vi NB-IoT pilots (2019) — https://techblog.comsoc.org/2019/11/03/indias-airtel-vodafone-idea-preparing-for-commercial-nb-iot-after-pilots/
29. GSMA Mobile IoT Deployment Map — https://www.gsma.com/iot/deployment-map (HTTP 403; not read)
30. Nordic news, Skylo certification for nRF9151 (Dec 2025) — https://www.nordicsemi.com/Nordic-news/2025/12/Nordic-Semiconductor-secures-Skylo-certification-for-nRF9151-module-enabling-global-IoT-connectivity
31. Nordic DevZone, nRF9160 Cat-M1/NB1/NB2 support in India (bands 3/5/8) — https://devzone.nordicsemi.com/f/nordic-q-a/50349/nrf9160-cat-m1-nb1-nb2-support-in-india (search snippet)

Internal: [R01] R01_Standards_Certification.md, [R02] R02_Cellular_4G.md, [R04] R04_LoRa.md, [R09] R09_Linux_vs_RTOS.md, [R17] R17_Tier1_4G_Modem_Card.md, PRD 01_Requirements_PRD.md (CELL, PWR).

Datasheets saved to `docs/datasheets/cellular/`: Nordic_nRF9151_SiP_product-brief.pdf, Nordic_nRF93M1_datasheet_v0.5.pdf, GSMA_IoT_Utility_Services_India_case-study_2023.pdf (see INDEX.md).
