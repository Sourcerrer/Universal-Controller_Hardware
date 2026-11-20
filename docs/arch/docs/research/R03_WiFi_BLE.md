# R03 — Wi-Fi + BLE module selection

Status: COMPLETE for the ESP32-C6 module choice; NXP / Nordic / ST covered as a short upgrade-path note (SYS-6) per product-owner decision of 2026-11-14. Open items are marked UNVERIFIED.
Date of research: 2026-11-13 / 2026-11-14 (prices and stock read 2026-11-14 unless stated).
FX rate: **USD 1 = INR 93.9** (mid-market 2026-11-08 [S1]; 93.74 in early trade 2026-11-09 [S2]). DigiKey India quotes INR directly (GST extra).
BOM limit: INR 600 finished / 1.4 = **INR 428**.

## 1. Executive summary and recommendation

1. **Decision (product owner, 2026-11-14): pre-certified Espressif ESP32-C6 modules, not chip-down.** This is the first-version baseline (PRD WB-2).
2. **Option A (lowest cost, recommended baseline): ESP32-C6-MINI-1U-N4** (U.FL connector, 4 MB flash, 13.2 x 12.5 mm, -40..85 C) at **INR 240.63 @ 650 reel** (DigiKey India, 513 in stock, Active). The PCB-antenna twin **ESP32-C6-MINI-1-N4** is INR 237.78 @ 650 (4,492 in stock) for plastic-enclosure standalone nodes [S9][S10].
3. **Option B ("trusted source", same silicon and firmware): u-blox NORA-W40** (ESP32-C6 inside) at ~USD 5.19 @ 500 (= INR 487) — does **not** fit the INR 428 BOM; or Espressif ESP32-C6-WROOM-1U-N8 if more flash at 85 C is needed (~INR 268 for the -1-N4 at 650; N8 price UNVERIFIED) [S12][S38][S39].
4. **Cost fit:** the module takes ~INR 241 of the INR 428 BOM, leaving ~INR 187 for the 40-pin stackable connector, 12–24 V buck, Li-ion charger/power-path, protection/ESD, U.FL pigtail + antenna and the PCB. That is tight but plausible; the external antenna and the per-module enclosure are the items most likely to break it (section 8). Chip-down would save only ~INR 45 and adds a full radio certification.
5. **Certifications (ESP32-C6-MINI-1/-1U):** CE-RED (Art. 3.1a/3.1b/3.2), FCC, ISED, SRRC, NCC both variants; MIC (TELEC), KCC, RCM, ANATEL, Wi-Fi Alliance only on MINI-1 (PCB antenna) [S3][S4]. **No EN 18031 module certificate** and **no WPC ETA** from Espressif; India ETA is self-declared by us on SaralSanchar using the module RF test reports [S45][S46].
6. **Security:** Secure Boot v2, XTS-AES flash encryption, HMAC/Digital-Signature peripherals, eFuse keys, TEE/APM; **PSA Certified Level 2** with ESP-TEE (2025-02-20) [S5][S6][S52]. Espressif has a published CRA position, PSIRT/advisories, SBOM tool and an EN 18031 self-assessment tool [S8][S15][S50].
7. **RTOS:** Zephyr supports ESP32-C6 Wi-Fi, BLE (HCI) and 802.15.4 with Espressif binary blobs [S16]; ESP-IDF (FreeRTOS) is the mature fallback and is required for ESP-Hosted/ESP-AT co-processor firmware. ThreadX: not supported (UNVERIFIED absence).
8. **Longevity:** ESP32-C6 committed to 2035-01-01 (12 years) [S7] — meets >= 5 years.
9. **Reuse in 4G + Ethernet + Wi-Fi module:** use the **same ESP32-C6-MINI-1U module**. ESP32-C6 (and C5) have **no Ethernet MAC**; Ethernet needs an SPI Ethernet controller (DM9051 / W5500 class) [S52][S55]. Of all candidates only **NXP RW612/RW610** has an RMII Ethernet MAC [S20].
10. **Upgrade path (SYS-6, short):** NXP RW612 (PSA L3, Ethernet MAC, dual-band, 15-yr longevity) is ~INR 1,010 chip / ~INR 1,261 module — **2.4–3x the whole BOM**; stock is thin (52-wk DigiKey lead time) [S24][S30]. ESP32-C5 (dual-band Wi-Fi 6) modules at ~INR 318 @ 650 are the cheapest "latest generation" step-up [S19]. Nordic and ST options cost more and have weaker India stock.
11. **Key risks:** EN 18031 / CRA conformity is on us; external-antenna gain must stay within the certified antenna's gain (2.33 dBi for MINI-1U FCC test) [S47]; ESP32-C6 Zephyr Wi-Fi depends on binary blobs.

## 2. Scope and constraints (from brief + 2026-11-13/14 updates)

- Plug-in Wi-Fi + BLE module for a modular industrial IoT gateway; must also work standalone as a remote node, each module in its own enclosure, stackable side-by-side on DIN rail with a 40-pin pass-through bus.
- Finished cost <= INR 600 (BOM x 1.4, so BOM <= INR 428), including 40-pin connector, 12–24 V input stage with single-cell Li-ion support, and antenna connector.
- Gateway brain (secure MCU + secure element) is on the baseboard; the module is a network co-processor over UART/SPI.
- The same Wi-Fi solution should be reused inside the combined 4G + Ethernet + Wi-Fi module (finished <= INR 1,000, BOM <= ~INR 714).
- Product-owner decisions 2026-11-14: pre-certified ESP32-C6 modules (no chip-down); RW612 / Nordic / ST only as a short upgrade-path note.

## 3. Comparison table

| Criterion | **ESP32-C6-MINI-1U-N4** (Option A) | ESP32-C6-WROOM-1(U)-N4/N8 | u-blox NORA-W40 (ESP32-C6) | ESP32-C5-WROOM-1-N4 | NXP RW612 (chip / IRIS-W101) | Nordic nRF54L15 + nRF7002 | ST ST67W611M1 |
|---|---|---|---|---|---|---|---|
| Radios | Wi-Fi 6 2.4 GHz, BLE 5, 802.15.4 | same | same | Wi-Fi 6 2.4+5 GHz, BLE 5, 802.15.4 | Wi-Fi 6 2.4+5 GHz, BLE 5.4, 802.15.4 | BLE 6 + Wi-Fi 6 2.4+5 GHz (two chips) | Wi-Fi 6 2.4 GHz + BLE (co-processor) |
| Price, INR (qty, source) | **240.63 (650, DigiKey IN)** | ~268 for -1-N4 (650, DigiKey MX, USD 2.85) | ~487 (500, Future, USD 5.19) | ~318 (650, DigiKey US, USD 3.39) | 1,010 chip (2k) / 1,261 module (250), DigiKey IN | nRF54L15 ~GBP 2.32 @3k + nRF7002 UNVERIFIED; no stocked combo module found | ~413–571 (USD 4.40 @10 Future; 6.08 @50 ST eStore) |
| Fits BOM <= 428 with ~190 for rest? | **Yes (tight)** | Yes (tighter) | No (module alone ~114 % of BOM) | Marginal (leaves ~110) | **No** (chip 2.4x, module 3x BOM) | No (two chips + RF + certification) | No |
| India stock (2026-11-14) | DigiKey IN 513 (MINI-1-N4: 4,492) | DigiKey stocked (regional) | Mouser IN listed, small qty | DigiKey (regional, low) | RW612 chip: no stock shown, 52 wk; IRIS-W101: 386 | nRF54L15 stocked; nRF7002 UNVERIFIED | element14/RS stocked; Future 0 |
| Pre-certified (module) | CE-RED, FCC, ISED, SRRC, NCC | CE, FCC, ISED, (-1: MIC, KCC, SRRC, WFA) | RED/UKCA/FCC listed "pending" in 2024 summary (UNVERIFIED now) | CE, FCC, IC, MIC, KCC, SRRC, NCC | IRIS-W10: RED, UKCA, FCC, ISED (+others planned) | Raytac AN7002Q pre-certified (claimed) | CE etc. UNVERIFIED; **has India WPC ETA** |
| EN 18031 module cert | No | No | No (UNVERIFIED) | No | No (UNVERIFIED) | No (UNVERIFIED) | UNVERIFIED |
| Security cert | PSA L2 (chip, with ESP-TEE) | PSA L2 | PSA L2 (chip) | none yet (ESP-TEE planned) | **PSA L3 + SESIP3 (claimed)** | nRF54L: UNVERIFIED in this report | UNVERIFIED |
| Zephyr | Yes (Wi-Fi, BT HCI, 15.4; blobs) | Yes | Yes (same chip) | Partial/UNVERIFIED | Yes, frdm_rw612 "Maintained" (Wi-Fi, BLE, ENET, USB; blobs) | Best-in-class (nRF Connect SDK) | No (AT/host driver for STM32Cube) UNVERIFIED |
| ThreadX | No | No | No | No | No (UNVERIFIED) | No | STM32 host side only |
| Ethernet MAC | **No** | No | No | No | **Yes (RMII 10/100, IEEE 1588)** | No | No |
| Longevity | to 2035 | to 2035 | u-blox UNVERIFIED | to 2037 | to Feb 2039 (NXP PLP) | UNVERIFIED | ST 10-yr programme UNVERIFIED |

## 4. Espressif: ESP32-C6 (modules vs chip-down), ESP32-C5, ESP32-C61

### 4.1 Certifications held by ESP32-C6 modules (Espressif certificate index, read 2026-11-14 [S3])

| Module | CE-RED | FCC | ISED (IC) | Japan MIC (TELEC) | KCC | SRRC | NCC | Other |
|---|---|---|---|---|---|---|---|---|
| ESP32-C6-MINI-1 | Yes (2025-12-18) | Yes (2023-09-14) | Yes (2023-09-14) | Yes (2024-09-05) | Yes (2025-10-27) | Yes (2025-07-09) | Yes (2024-12-19) | RCM, ANATEL, Wi-Fi Alliance, BQB |
| ESP32-C6-MINI-1U | Yes (2025-12-18) | Yes (2025-08-19) | Yes (2025-08-20) | not listed | not listed | Yes (2025-07-09) | Yes (2025-10-27) | BQB |
| ESP32-C6-WROOM-1 | Yes (2025-12-18) | Yes (2023-09-14) | Yes (2023-09-14) | Yes (2024-01-08) | Yes (2024-02-08) | Yes (2025-08-20) | not listed | ANATEL, Wi-Fi Alliance, BQB |
| ESP32-C6-WROOM-1U | Yes (2025-12-18) | Yes (2025-08-19) | Yes (2025-08-20) | not listed | not listed | not listed | not listed | BQB |

- The MINI-1 CE document lists RED Art. 3.1a (safety), 3.1b (EMC) and 3.2 (radio) test reports [S4]. The CE entries do **not** cover EN 18031 (RED Art. 3.3 d/e/f). No EN 18031 certificate exists for any ESP32-C6 module in the index. Espressif states EN 18031 applies to the complete end product, not to a module [S8].
- FCC IDs: MINI-1U = 2AC7Z-ESPC6MINIU; FCC test report lists a sleeve-monopole test antenna of **2.33 dBi** [S47].
- India: no WPC ETA and no BIS entry for any ESP32-C6 module in the Espressif index [S3]. WPC ETA must be self-declared by the product maker/importer (section 9).
- Chip-level: PSA Certified Level 2 (ESP32-C6 + ESP-TEE v1.0, cert 0632793520245-10010, 2025-02-20, lab Applus+) [S5][S6]; Thread 1.4 certified (2025-03-18); Zigbee 3.0 R23 compliant platform [S3].
- ESP32-C5 modules: WROOM-1 holds FCC (2.4+5 GHz), IC, MIC, KCC, SRRC, NCC, CE, ANATEL, WFA; MINI-1 holds FCC, CE, WFA (2026) [S3].

### 4.2 Module variants (datasheets in docs/datasheets/wifi_ble/) [S51][S56]

| Module | Antenna | Flash | Temp | Size (mm) |
|---|---|---|---|---|
| ESP32-C6-MINI-1-N4 / -H4 / -H8 | PCB | 4 / 4 / 8 MB (in-package, ESP32-C6FH4/FH8) | N: -40..85 C; H: -40..105 C | 13.2 x 16.6 x 2.4 |
| ESP32-C6-MINI-1U-N4 / -H4 / -H8 | U.FL connector | 4 / 4 / 8 MB | N: 85 C; H: 105 C | 13.2 x 12.5 x 2.4 |
| ESP32-C6-WROOM-1-N4 / N8 / N16 | PCB | 4 / 8 / 16 MB | -40..85 C | 18.0 x 25.5 x 3.1 |
| ESP32-C6-WROOM-1U-N4 / N8 / N16 | U.FL | 4 / 8 / 16 MB | -40..85 C | 18.0 x 19.2 x 3.2 |

Note: on MINI modules 8 MB is only offered as the 105 C "H8" grade; WROOM offers 8/16 MB at 85 C.

### 4.3 Prices and India stock (read 2026-11-14)

| Part | 1 pc | 100 pcs | 650 (full reel, nearest to 1k) | Stock / status | Source |
|---|---|---|---|---|---|
| ESP32-C6-MINI-1-N4 (DigiKey India, INR) | 430.85 | 324.75 | **237.78** | 4,492, Active, 8 wk LT | [S9] |
| ESP32-C6-MINI-1U-N4 (DigiKey India, INR) | 435.60 | 328.03 | **240.63** | 513, Active, 8 wk LT | [S10] |
| ESP32-C6-MINI-1-N4 (DigiKey US, USD) | 4.53 | 3.41 | 2.50 (= INR 235) | 4,492, Active | [S11] |
| ESP32-C6-WROOM-1-N4 (DigiKey Mexico, USD) | — | — | 2.85 (= INR 268) | Active | [S12] |
| ESP32-C6FH4 chip (QFN32; DigiKey US) | 2.26 | — | 2.06 @ 5k (= INR 193) | 0 stock; 4,989 due 2026-11-16; 26 wk LT | [S18] |
| ESP32-C5-WROOM-1-N4 (DigiKey US, USD) | 4.99 | 3.57 @250 | 3.39 (= INR 318) | low/regional | [S19] |

- DigiKey has no 1,000-pc break; the 650 reel price is used as the ~1k price. A broker aggregator shows MINI-1-N4 USD 1.84 @1k (= INR 173) without naming the distributor: UNVERIFIED [S13]. A direct Espressif / Indian franchised-distributor quote at 1k–5k is likely lower than DigiKey reel price (UNVERIFIED).
- Prior run noted Mouser India single-unit MINI-1-N4 ~INR 432.80 and MINI-1-H8 ~INR 521.65 (URL not recorded: UNVERIFIED).
- Third-party ESP32-C6 modules: Ai-Thinker ESP32-C6 module price/certs not found (LCSC hit "Ai-M62-12F" is a different chip): UNVERIFIED. AzureWave ESP32-C6 module: not found. u-blox NORA-W40 (ESP32-C6 based) — see Option B; its 2024 product summary listed RED/UKCA/FCC and BLE qualification as "pending" (current status UNVERIFIED) [S38]; Future Electronics NORA-W406-10B USD 5.19 @500, 0 stock, 20 wk LT [S39].

### 4.4 Chip-down vs module (cost fit)

- Chip-down saves at most ~INR 45/unit (INR 193 chip vs INR 238 module) but adds 40 MHz crystal, RF matching, antenna/U.FL, shield/layout risk, and a **full** radio certification (CE-RED radio + EMC tests, FCC, WFA/BQB listings), WPC ETA on our own RF report. At < 10k units/year this does not pay back; the product owner has decided on modules.

### 4.5 Longevity, security, RTOS

- Longevity: ESP32-C6 12 years, 2023-01-01 to 2035-01-01; ESP32-C5 2025-01-01 to 2037-01-01 [S7].
- Security (chip datasheet v1.6 [S52]): Secure Boot (Secure Boot v2 in ESP-IDF, RSA-3072/ECDSA), flash encryption (XTS-AES), HMAC, RSA Digital Signature peripheral, AES-128/256, ECC, SHA, eFuse key storage, TEE controller + Access Permission Management (APM). ESP-TEE in ESP-IDF v5.5+ on ESP32-C6, planned for C5/C61 [S14][S54].
- Zephyr: board esp32c6_devkitc lists on-chip Wi-Fi (espressif,esp32-wifi), Bluetooth HCI (espressif,esp32-bt-hci) and 802.15.4 (espressif,esp32-ieee802154) on the HP core; requires Espressif HAL binary blobs [S16] (read by earlier run; Zephyr support of ESP32-C6 secure boot/flash encryption via MCUboot not verified: UNVERIFIED).
- ESP-IDF (FreeRTOS): fully supported; required for ESP-Hosted and ESP-AT co-processor firmware [S48].
- ThreadX: no Espressif or Eclipse ThreadX port for ESP32-C6 found (UNVERIFIED absence).
- Wi-Fi / BLE / 802.15.4 coexistence: the three radios coexist and share one antenna (time-division, single RF path) [S52]. Practical effect: simultaneous Thread + Wi-Fi throughput drops; Thread border-router use needs care (UNVERIFIED quantitatively).
- Fieldbus side-note: ESP32-C6 has two TWAI (CAN 2.0) controllers; ESP32-C5 has CAN FD [S52][S57].

### 4.6 ESP32-C5 and ESP32-C61 (latest Espressif parts)

- ESP32-C5: RISC-V, dual-band 2.4/5 GHz Wi-Fi 6, BLE 5, 802.15.4, SDIO slave, CAN FD, no Ethernet MAC [S57]; longevity to 2037 [S7]; modules certified (4.1); ESP32-C5-WROOM-1-N4 USD 3.39 @650 = INR 318 [S19]. Good step-up when 5 GHz is needed (crowded 2.4 GHz plants); leaves only ~INR 110 for the rest of the BOM.
- ESP32-C61: 2.4 GHz Wi-Fi 6 + BLE, cost-down part; distributor price and module availability not found: UNVERIFIED.

## 5. NXP: RW612 / RW610 (upgrade path only — SYS-6)

Status per product owner 2026-11-14: short upgrade-path note only.

- **Features** [S20][S21]: 260 MHz Cortex-M33 + TrustZone-M, 1.2 MB SRAM, FlexSPI XIP with on-the-fly decryption; 1x1 20 MHz Wi-Fi 6 2.4 + 5 GHz; BLE 5.4; 802.15.4 (RW610 = without 15.4); **IEEE 1588 RMII 10/100 Ethernet MAC**; HS USB 2.0 OTG; up to 5 Flexcomm (UART/SPI/I2C/I2S); SDIO 3.0. Package 145-TFBGA 8 x 8 mm [S24].
- **Security:** EdgeLock Secure Enclave (Core Profile), secure boot/debug/update, PUF key storage, EdgeLock 2GO [S20]. **PSA Certified Level 3**, cert 0632793519591-10000, 2024-03-20, Riscure, RW61x A1/A2 [S26]. SESIP Level 3 claimed by NXP, certificate not found: UNVERIFIED [S27].
- **Zephyr:** frdm_rw612 "Maintained": Wi-Fi (nxp,wifi), BLE (nxp,hci-ble), ENET + PTP, USB device/host; 802.15.4 only as HDLC RCP interface; Wi-Fi/BLE blobs required [S23]. MCUXpresso SDK supports Wi-Fi/BLE/OpenThread/Matter on FreeRTOS [S28]. ThreadX: not found.
- **Lifecycle:** NXP status Active [S20]; NXP Product Longevity: launch Feb 2024, end Feb 2039 [S25].
- **Availability evidence (2026-11-14)** — the owner's "too new to have stock" view is **largely correct for the chip**:
  - RW612ET/A2IY (reel) DigiKey India: Active, stock not shown, **52-week** lead time, INR 1,010.24 @ 2,000 [S24]; RW612ET/A2IK (tray): Active, stock not shown, 52 wk, INR 1,017.28 @ 1,740 [S37].
  - element14 Malaysia RW612ET/A2IK: "available to order", **29-week** lead time [S34]. Future Electronics RW612ET/A2IY: global stock 0, 16-week factory lead time [S35]. LCSC: only the FRDM-RW612 board (5 pcs), no chip [S36].
  - Module: u-blox IRIS-W101-00B DigiKey India **386 in stock**, Active, 20 wk LT, INR 1,543.64 @1, INR 1,261.39 @250 [S30]. Murata Type 2FR / AzureWave AW-CU570: no stock/price found (UNVERIFIED).
  - RW610ET/A2IY: Mouser India INR 1,367.88 @1 with ~868 in stock (search snippet, UNVERIFIED snapshot date) [S29].
- **Modules / certifications:** IRIS-W10: RED, UKCA, FCC, ISED (+MIC, NCC etc. "additional") [S32]; AzureWave AW-CU570: FCC, CE, NCC, IC, Japan, AU/NZ per NXP partner table (secondary) [S33]; Murata LBES0ZZ2FR-580: FCC/IC, ETSI, TELEC per DigiKey [S31]. No EN 18031 or WPC ETA found.
- **Cost fit:** chip INR 1,010 = 2.4x the INR 428 BOM (over by ~INR 582 before anything else); IRIS-W101 INR 1,261 = 2.9x (over by ~INR 833). Also over the 4G-combo BOM (~INR 714). **Does not fit**; only a large NXP volume quote could change this.
- **Host capability:** Ethernet RMII + USB + 5 Flexcomm + SDIO means RW612 *could* be the single Wi-Fi + Ethernet host on the combined module — the only candidate that can. Keep as the premium/v2 path.
- IW610 / IW612 companion radios: not researched further per owner decision (need a host MCU, so no cost advantage): UNVERIFIED.

## 6. Nordic: nRF7002 + nRF54L15 / nRF5340 (upgrade path only)

- Two-chip architecture (BLE host SoC + nRF7002 Wi-Fi 6 companion over SPI/QSPI). Nordic released the nRF7002 EBII board for nRF54L DKs (availability Q1 2026) [S41]; Nordic's nRF54L15 + nRF7002 compact reference design is marked "shielding not tested" — not a certified module.
- Pre-certified Wi-Fi module: Raytac AN7002Q (nRF7002) pairs with Raytac's nRF5340 MDBT53 module; Raytac claims WFA and regulatory pre-certification [S40]. No pre-certified single module combining nRF54L15 + nRF7002 found.
- BLE-only low-cost option: nRF54L15 chip ~GBP 2.32 @3,000 (DigiKey UK, ~INR 280 at an assumed GBP/INR ~121: UNVERIFIED conversion) [S42]; Raytac nRF54L15 modules claimed FCC/IC/CE/TELEC/NCC/SRRC (Tindie listing, secondary) [S40].
- nRF7002 price: not found: UNVERIFIED. Two chips + two radios' certification make it more expensive than ESP32-C6 for this BOM. Zephyr (nRF Connect SDK) support is best-in-class. No Ethernet MAC.

## 7. ST: ST67W611M1, STM32WBA (short note)

- ST67W611M1 exists: Wi-Fi 6 + BLE co-processor module (SPI/UART) for STM32 hosts; variants BTR/PTR/UTR [S43]. Price: ST eStore USD 6.08 @50 (= INR 571); Future Electronics USD 4.40 (10+), 0 stock, 26-wk LT; element14/RS stock the PTR variant [S43].
- **Notable: ST67W611M1A holds an India WPC ETA self-declaration certificate** (ETA-SD-20250705939) [S44] — the only candidate with a published WPC ETA found.
- Does not fit the INR 428 BOM with the rest of the module. STM32WBA (BLE-only) not priced in this run: UNVERIFIED.

## 8. Cost fit against BOM <= INR 428 (Option A)

| Item | INR | Basis |
|---|---|---|
| ESP32-C6-MINI-1U-N4 | 240.63 | DigiKey India @650 [S10] |
| Remaining for 40-pin stackable connector, 12–24 V buck + TVS/reverse-polarity, Li-ion charger + power-path + cell holder/connector, U.FL pigtail + external antenna, ESD, PCB, passives | **~187** | 428 – 241 |

- The non-module items are priced in R06 (power) and R07 (connector); not re-priced here. Engineering estimate (UNVERIFIED): 40-pin Hirose/Wuerth B2B pair INR 60–120, buck + protection INR 40–70, charger + power-path INR 20–40, PCB + passives INR 30–50, external dipole + pigtail INR 60–150. Sum ~INR 210–430, so **Option A fits only at the low end**.
- If it does not fit, trim in this order: (1) use MINI-1-N4 PCB antenna for standalone/plastic variants and offer the U.FL antenna kit as a separately priced accessory; (2) drop the on-module Li-ion charger and accept battery only on a dedicated battery variant; (3) source the module from an Indian franchised distributor / Espressif direct at 1k–5k (aggregator suggests ~INR 173, UNVERIFIED); (4) cheaper single-row connector on standalone builds.
- Option B (NORA-W40, ~INR 487) does not fit: over the whole BOM by ~INR 59 before any other part.

## 9. Antenna strategy and certification impact; India WPC ETA

- Metal cabinets: PCB antenna inside a metal enclosure will not work; use **MINI-1U (U.FL)** with a cable to a bulkhead SMA/RP-SMA and an external antenna outside the cabinet. Keep MINI-1 (PCB antenna) for standalone nodes in plastic enclosures.
- Certification impact: a module grant is valid only with antennas of the same type and equal or lower gain than tested. MINI-1U FCC test antenna: sleeve monopole 2.33 dBi [S47]; MINI-1 PCB antenna ~3.96 dBi (per a test report snippet, UNVERIFIED). A higher-gain or different-type antenna requires a class II permissive change (FCC) / additional RED radio testing (EU) — UNVERIFIED for exact Espressif terms; confirm antenna list in the FCC grant and the module integration manual. Cable loss to a bulkhead connector helps keep EIRP within the tested limit.
- Also note MINI-1U lacks Japan MIC and KCC certificates (MINI-1 has them) [S3] — matters only for export.
- **India WPC ETA:** 2.4 GHz Wi-Fi/BLE are licence-exempt; ETA is by self-declaration on the SaralSanchar portal (live since 2019-04-12) [S46]. DoT clarification: the ETA can be based on the **RF test reports of the module(s) fitted in the model, without alteration, plus the manufacturer's undertaking** [S45] — so Espressif's module RF test reports can be reused; Raspberry Pi files ETAs this way [S53]. The applicant is liable for wrong declarations [S53]. Processing time "2–4 weeks" is a consultant claim: UNVERIFIED. BIS: wireless modules themselves are not in the CRS list per R01 (see R01; not re-verified here).

## 10. Host-interface options and throughput

- ESP32-C6 interfaces: UART (up to 5 Mbaud), SPI slave (GP-SPI2, up to 40 MHz as slave per datasheet), **SDIO 2.0 slave**, USB Serial/JTAG (debug only) [S51][S52].
- Firmware options: **ESP-Hosted-MCU** (ESP32-C6 as co-processor; SPI, SDIO, UART transports to an MCU host) [S48]; ESP-AT (AT commands over UART/SPI; Espressif lists it as a pre-certified firmware platform [S8]); custom Zephyr or ESP-IDF firmware with our own protocol.
- Throughput (third-party measurement, ESP32-P4 host + ESP32-C6, indicative) [S49]: SDIO 4-bit @40 MHz ~79.5 Mbps transport; SPI full-duplex @40 MHz ~25 Mbps; UART @921,600 baud ~0.74 Mbps; end-to-end limited by the C6 Wi-Fi PHY ~36 Mbps. Espressif states SDIO is the highest-throughput transport [S48].
- Realistic for this gateway: UART at 1–3 Mbaud gives ~0.8–2.5 Mbps raw (~0.6–2 Mbps payload) — fine for telemetry/MQTT. Use **SPI (~10–25 Mbps)** on the 40-pin bus if firmware updates of other modules or camera/bulk data pass through Wi-Fi. SDIO needs 6 lines and short traces; not recommended across a stackable pass-through bus.
- RW612: SDIO 3.0, SPI/UART via Flexcomm, USB HS [S21]; nRF7002: SPI/QSPI to host; ST67W611M1: SPI/UART [S43].

## 11. Security posture for CRA / EN 18031

| Item | ESP32-C6 | RW612 | Note |
|---|---|---|---|
| Secure boot | Secure Boot v2 [S52] | EdgeLock secure boot [S20] | |
| Encrypted storage | XTS-AES flash encryption + NVS encryption (HMAC-based) [S52] | FlexSPI on-the-fly decryption, PUF [S20] | |
| Key storage | eFuse, DS peripheral (key never exposed) [S52] | PUF + EdgeLock enclave | Baseboard secure element holds gateway keys anyway |
| TEE | ESP-TEE (IDF 5.5+) [S14] | TrustZone-M | |
| Certification | PSA L2 [S5] | PSA L3 [S26], SESIP3 claimed | |
| WPA3 / 802.1X | WPA3-Personal and enterprise supported in ESP-IDF (UNVERIFIED in this run; Zephyr WPA3/enterprise on ESP32-C6 UNVERIFIED) | WPA3 per NXP (UNVERIFIED) | |
| Vendor CRA position | Published: PSIRT, advisories, ESP-IDF Security Dashboard, esp-idf-sbom, RED-DA tool, DoCs for chips/modules once CRA applies [S50][S15] | NXP PSIRT exists (UNVERIFIED in this run) | |

- CRA dates (per Espressif summary) [S50]: reporting obligations from **2026-09-11**; full application incl. CE marking **2027-12-11**. "Compliance is a property of the final product": EN 18031 self-assessment, SBOM, vulnerability handling, update policy are our obligations.
- Espressif vulnerability-handling track record (advisories published on GitHub/website) — positive but includes past fault-injection advisories on older chips (not researched in detail: UNVERIFIED for C6).

## 12. Wi-Fi reuse in the combined 4G + Ethernet + Wi-Fi module; Ethernet MAC availability

- Recommend the **same ESP32-C6-MINI-1U module** (same certs, same firmware, same antenna kit). It can act as the module's local host: Wi-Fi + SPI Ethernet controller (ESP-IDF supports external SPI-Ethernet modules such as DM9051, more in esp-eth-drivers; eth2ap example on C6 bridges Ethernet and Wi-Fi) [S55], plus UART to the LTE Cat-1 modem.
- Ethernet MAC: **ESP32-C6 – no; ESP32-C5 – no** (no Ethernet in either datasheet) [S52][S57]; **RW612/RW610 – yes (RMII, IEEE 1588)** [S20]; nRF54L15/nRF7002 – no; ST67W611M1 – no. With ESP32-C6 the Ethernet path is SPI-limited (~10–20 Mbps practical, UNVERIFIED), adequate for industrial telemetry.
- Budget: ESP32-C6 module INR ~241 inside a BOM of ~INR 714 leaves ~INR 473 for LTE Cat-1 module, SPI Ethernet + magnetics/RJ45, power — see R02.

## 13. Risks and open decisions

Risks
- EN 18031 / CRA conformity is ours; no module carries EN 18031.
- External-antenna gain/type must match the certified antenna (2.33 dBi monopole for MINI-1U FCC) or re-testing is needed.
- ESP32-C6 Wi-Fi in Zephyr depends on Espressif binary blobs; production-grade Zephyr Wi-Fi maturity on C6 vs ESP-IDF not independently verified.
- DigiKey India MINI-1U-N4 stock is 513 pcs only; MINI-1-N4 4,492 pcs. Use an Indian franchised distributor and buffer stock.
- Cost: module + connector + power + external antenna is at the edge of INR 428.

Open decisions
1. Flash size: N4 (4 MB) vs H8 (8 MB, 105 C) for Zephyr + MCUboot dual-slot OTA / Matter. Recommend prototyping on N4 and measuring image size.
2. Firmware: ESP-Hosted / ESP-AT (fast, mature, ESP-IDF) vs custom Zephyr co-processor firmware (RTOS alignment).
3. Host bus on the 40-pin connector: UART only vs UART + SPI.
4. Whether the external antenna is included in module BOM or sold as an accessory.
5. Whether 5 GHz (ESP32-C5, +~INR 78) is needed for some customers.
6. When to bring RW612 in (v2, if Ethernet-MAC host or PSA L3 becomes mandatory and price falls).

## 14. Sources

- [S1] CurrencyBeacon USD/INR — https://currencybeacon.com/rates/USD/INR (2026-11-14)
- [S2] HDFC Sky/PTI, rupee 93.74 — https://hdfcsky.com/news/rupee-rises-24-paise-to-93-74-against-us-dollar-in-early-trade
- [S3] Espressif certificate index (ESP32-C6 / C5) — https://www.espressif.com/en/support/documents/certificates?keys=ESP32-C6 (read 2026-11-14)
- [S4] ESP32-C6-MINI-1 CE certification — https://www.espressif.com/sites/default/files/ESP32-C6-MINI-1%20CE%20Certification.pdf
- [S5] PSA Certified, ESP32-C6 certificate — https://products.psacertified.org/products/esp32-c6/certificates
- [S6] Espressif news, C6 PSA Level 2 — https://www.espressif.com/en/news/C6_PSA_Level2
- [S7] Espressif longevity commitment — https://www.espressif.com/en/products/longevity-commitment
- [S8] Espressif RED-DA / EN 18031 compliance guide — https://developer.espressif.com/blog/2025/04/esp32-red-da-en18031-compliance-guide/
- [S9] DigiKey India ESP32-C6-MINI-1-N4 — https://www.digikey.in/en/products/detail/espressif-systems/ESP32-C6-MINI-1-N4/17885796 (2026-11-14)
- [S10] DigiKey India ESP32-C6-MINI-1U-N4 — https://www.digikey.in/en/products/detail/espressif-systems/ESP32-C6-MINI-1U-N4/21292143 (2026-11-14)
- [S11] DigiKey US ESP32-C6-MINI-1-N4 — https://www.digikey.com/en/products/detail/espressif-systems/ESP32-C6-MINI-1-N4/17885796 (2026-11-14)
- [S12] DigiKey Mexico ESP32-C6-WROOM-1-N4 (search snippet) — https://www.digikey.com.mx/en/products/detail/espressif-systems/ESP32-C6-WROOM-1-N4/17728867
- [S13] Shengyu IC aggregator (unnamed distributor) — https://shengyuic.com/products/detail/Espressif-Systems/ESP32-C6-MINI-1-N4/16365718.html
- [S14] Espressif blog, Matter with ESP-TEE on C6 — https://developer.espressif.com/blog/2025/09/matter_w_esp_tee_c6/
- [S15] Espressif RED-DA assessment tool — https://red-da-assessment-tool.security.espressif.com/ ; RainMaker EN 18031 case study — https://developer.espressif.com/blog/2026/09/esp32-rainmaker-en18031-case-study/
- [S16] Zephyr esp32c6_devkitc board doc — https://docs.zephyrproject.org/latest/boards/espressif/esp32c6_devkitc/doc/index.html (read by earlier run)
- [S18] DigiKey US ESP32-C6FH4 — https://www.digikey.com/en/products/detail/espressif-systems/ESP32-C6FH4/18587545 (2026-11-14)
- [S19] DigiKey US ESP32-C5-WROOM-1-N4 (search snippet) — https://www.digikey.com/en/products/detail/espressif-systems/esp32-c5-wroom-1-n4/27566799
- [S20] NXP RW612 product page — https://www.nxp.com/products/RW612
- [S21] NXP RW612 block diagram — https://www.nxp.com/assets/block-diagram/en/RW612.pdf ; fact sheet — https://www.nxp.com/docs/en/fact-sheet/RW61XFS.pdf
- [S22] CNX Software, RW612 — https://www.cnx-software.com/2024/10/08/nxp-rw612-arm-cortex-m33-wireless-mcu-offers-wi-fi-6-bluetooth-5-4-and-802-15-4-radios/
- [S23] Zephyr frdm_rw612 board doc — https://docs.zephyrproject.org/latest/boards/nxp/frdm_rw612/doc/index.html
- [S24] DigiKey India RW612ET/A2IY — https://www.digikey.in/en/products/detail/nxp-usa-inc/RW612ET-A2IY/22036080 (2026-11-14)
- [S25] NXP Product Longevity — https://www.nxp.com/products/nxp-product-information/nxp-product-programs/product-longevity:PRDCT_LONGEVITY_HM (via search snippet)
- [S26] PSA Certified, RW61x certificate — https://products.psacertified.org/products/rw61x-rw612-rw610/certificates
- [S27] NXP blog, security certifications — https://www.nxp.com/company/about-nxp/smarter-world-blog/BL-NAVIGATING-SECURITY-CERTIFICATIONS
- [S28] MCUXpresso SDK wireless docs — https://mcuxpresso.nxp.com/mcuxsdk/latest/html/middleware/wireless/WiFi-Bluetooth-802.15.4/topics/wireless_certification.html
- [S29] DigiKey UK RW610ET/A2IY — https://www.digikey.co.uk/en/products/detail/nxp-usa-inc/RW610ET-A2IY/22039111 ; Mouser India RW610 (search snippet) — https://www.mouser.in/en/c/rf-wireless/rf-integrated-circuits/?m=NXP
- [S30] DigiKey India u-blox IRIS-W101-00B — https://www.digikey.in/en/products/detail/u-blox/IRIS-W101-00B/22198318 (2026-11-14)
- [S31] DigiKey Murata Type 2FR highlight — https://www.digikey.fi/fi/product-highlight/m/murata-electronics-north-america/type-2fr-hostless-wi-fi-6-bluetooth-le-5-4-802-15-4-tri-radio-module
- [S32] u-blox IRIS-W10 product summary — https://content.u-blox.com/sites/default/files/documents/IRIS-W10_ProductSummary_UBX-23000279.pdf
- [S33] NXP RW610/RW612 Knowledge Hub (partner module table; 403 to fetcher, seen via search) — https://community.nxp.com/t5/Wireless-Connectivity-Knowledge/RW610-RW612-Knowledge-Hub/ta-p/1985071
- [S34] element14 Malaysia RW612ET/A2IK — https://my.element14.com/nxp/rw612et-a2ik/85ak9636/dp/4838967
- [S35] Future Electronics RW612ET/A2IY — https://www.futureelectronics.com/p/semiconductors--analog--power-controllers--pwm-controllers/rw612et-a2iy-nxp-2181144
- [S36] LCSC FRDM-RW612 — https://www.lcsc.com/product-detail/C41561678.html
- [S37] DigiKey India RW612ET/A2IK — https://www.digikey.in/en/products/detail/nxp-usa-inc/RW612ET-A2IK/22039572 (2026-11-14)
- [S38] u-blox NORA-W40 product summary — https://mouser.com/datasheet/2/1025/NORA_W40_ProductSummary_UBX_23009094-3519014.pdf
- [S39] Future Electronics NORA-W406-10B — https://www.futureelectronics.com/p/7192667 ; Mouser India NORA-W40 news — https://www.mouser.in/newsroom/publicrelations-u-blox-nora-w40-modules-2026final/
- [S40] Nordic news, Raytac AN7002Q — https://nordicsemi.com/Nordic-news/2024/09/Raytac-employs-Nordic-nRF7002-Companion-IC ; Raytac nRF54L15 module listing — https://www.tindie.com/products/bluetooth-wifi-module-store/nrf54l15-bt60-ufl-connector-module-raytac-an54lq/
- [S41] Nordic news, nRF7002 EBII — https://www.nordicsemi.com/Nordic-news/2025/12/Nordic-Semiconductor-expands-nRF54L-Series-development-options-with-nRF7002-EBII
- [S42] DigiKey UK nRF54L15-QFAA-R — https://www.digikey.co.uk/en/products/detail/nordic-semiconductor-asa/NRF54L15-QFAA-R/24773455
- [S43] ST ST67W611M1 — https://www.st.com/en/wireless-connectivity/st67w611m1.html ; ST eStore — https://estore.st.com/en/products/wireless-connectivity/short-range/wi-fi-products/st67w611m1.html ; Future — https://www.futureelectronics.com/p/6199229
- [S44] ST67W611M1A WPC ETA certificate — https://www.st.com/resource/en/certification_document/eta-sd-20250705939-st67w611m1a-wpc-cert.pdf
- [S45] DoT clarification on ETA (module test reports) — https://dot.gov.in/sites/default/files/Clarification%20to%20OM%20dated%2026th%20February%2C%202019%20on%20ETA_0.pdf
- [S46] Bureau Veritas, WPC ETA self-declaration (SARAL) — https://cps.bureauveritas.com/newsroom/india-wpc-wing-introduce-equipment-type-approval-eta-through-self-declaration-saral
- [S47] FCC test report 2AC7Z-ESPC6MINIU — https://fcc.report/FCC-ID/2AC7Z-ESPC6MINIU/7149937.pdf ; Espressif MINI-1U FCC certificate — https://www.espressif.com/sites/default/files/ESP32-C6-MINI-1U%20FCC%20Certification.pdf
- [S48] ESP-Hosted-MCU — https://github.com/espressif/esp-hosted-mcu
- [S49] Third-party ESP32-P4 + C6 throughput test — https://github.com/r4d10n/esp32p4-c6-wifi-test
- [S50] Espressif, CRA obligations and deadlines — https://developer.espressif.com/blog/2026/09/esp32-cra-obligations-and-deadlines/
- [S51] ESP32-C6-MINI-1/1U datasheet v1.5 — https://www.espressif.com/sites/default/files/documentation/esp32-c6-mini-1_mini-1u_datasheet_en.pdf
- [S52] ESP32-C6 series datasheet v1.6 — https://www.espressif.com/sites/default/files/documentation/esp32-c6_datasheet_en.pdf
- [S53] Raspberry Pi Pico 2 W India ETA — https://pip-assets.raspberrypi.com/categories/1090-approvals/documents/RP-007910-CF-1-rpi-pico2w%20India.pdf
- [S54] Espressif security certifications — https://docs.espressif.com/projects/esp-product-security/en/latest/security-certifications.html
- [S55] ESP-IDF Ethernet API (ESP32-C6) — https://docs.espressif.com/projects/esp-idf/en/stable/esp32c6/api-reference/network/esp_eth.html
- [S56] ESP32-C6-WROOM-1/1U datasheet v1.4 — https://www.espressif.com/sites/default/files/documentation/esp32-c6-wroom-1_wroom-1u_datasheet_en.pdf
- [S57] ESP32-C5 series datasheet v1.5 — https://www.espressif.com/sites/default/files/documentation/esp32-c5_datasheet_en.pdf (local copy; URL assumed from Espressif naming pattern, UNVERIFIED)

- [S58] NXP RW612 data sheet Rev. 9.0 (2026-07-30) — https://www.nxp.com/docs/en/data-sheet/RW612.pdf (local copy in datasheets/wifi_ble)

(S17 retired: earlier run's ESP32-C5 mass-production source URL was not recorded.)
Local datasheets and their sources: docs/datasheets/wifi_ble/INDEX.md.
