# R02 — Cellular 4G module selection and the combined "4G + Ethernet + Wi-Fi" module

Status: COMPLETE WITH GAPS (2026-11-14). Gaps are listed in section 2.3 and marked UNVERIFIED in the text.
Date of research: 2026-11-13 / 2026-11-14
Cost basis: finished cost = BOM x 1.4. Target for the combined "4G + Ethernet + Wi-Fi" module: finished <= INR 1,000 (BOM <= ~INR 714).

## 1. Executive summary and recommendation

1. **INR 1,000 finished (BOM 714) is NOT achievable** for a module that has LTE Cat-1 + 10/100 Ethernet + Wi-Fi STA/AP + 12-24 V/Li-ion power + 40-pin bus, using the prices found. The cheapest costed build is a BOM of about INR 1,050-1,465 (finished **INR 1,470-2,050**) without 2G, and about INR 1,400-1,900 (finished **INR 1,950-2,700**) with 2G fallback (section 3.2). Even with a chip-down ESP32-C6 the BOM stays at about INR 910 (finished about INR 1,270).
2. **Recommended architecture (option B):** a low-cost India-band LTE Cat-1/Cat-1 bis modem driven over UART (AT + CMUX + PPP), plus a **pre-certified ESP32-C6-MINI-1** as the host and the Wi-Fi STA/AP radio, plus a **WCH CH390H** (or WIZnet W5500) SPI Ethernet MAC+PHY and an RJ45 with magnetics. This uses parts with proven Indian stock: ESP32-C6-MINI-1-N4 costs INR 318.62 at 1k from Lion Circuits (in stock).
3. **Modem choice.** Without 2G: Quectel EG800K-CN / EC800M-CN class (Cat-1 bis / Cat-1, B1/3/5/8/34/38/39/40/41, LCC 17.7x15.8 mm). These cost about INR 320 (USD 3.41 at 100) to INR 499 (Hubtronics retail). With 2G: SIMCom A7672S (B1/3/5/8/40/41 + GSM 900/1800, INR 700-950 retail). The A7672S is also the best fit for Zephyr, because the in-tree `modem_cellular` driver supports A76xx. Alternate with 2G: Quectel EC200U-CN, where GSM is optional per order code (IndiaMART about INR 670).
4. **Cheapest modem prices.** Cat-1 bis without 2G: about INR 320-500 per part. Cat-1 with 2G: about INR 610-950 per part (retail or IndiaMART, single unit). Firm 1k quotes from Quectel/SIMCom India channels are still needed. The old INR 500 modem-part ceiling is only met **without** 2G.
5. **Ways to reach INR 1,000.** Drop one of the three interfaces: 4G + Ethernet only is about INR 1,010 finished, and 4G + Wi-Fi only is about INR 1,250. Alternatively, put Wi-Fi on the existing Wi-Fi/BLE card when stacked, which gives up the standalone Wi-Fi requirement. Dropping 2G saves about INR 300-450 BOM. Dropping Li-ion saves only part of the INR 90 power block.
6. **Other routes.** (a) EC200A-CN (Cat-4 + 2G, RMII and SDIO-Wi-Fi in QuecOpen) costs INR 1,250-1,454 retail for the modem alone. Its Wi-Fi chip support is undocumented, so the BOM is about INR 1,750 and the software risk is high. (c) NXP RW612 is a later upgrade only: the SoC alone is about INR 997, and Ethernet is on TFBGA only. (d) Linux router-SoC routes cost more and add an old-kernel CRA burden.
7. **Certification.** None of the cheap China/India module variants lists Indian TEC certification; their datasheets list SRRC/NAL/CCC only. The host still needs TEC MTCTE ("IoT Gateway", mandatory since 1 Jan 2024, per R01). It also needs the Wi-Fi radio's WPC/ETA, and for the EU, RED with EN 18031 until 11 Dec 2027 and CRA Class I (router/modem) after that.
8. **Trusted source.** No official notice was found that applies India's NSCS trusted-source regime to IoT modules (UNVERIFIED). For government or utility tenders, keep a non-Chinese fallback footprint in mind, such as Cavli C16QS-IN (India-designed, no 2G; volume price UNVERIFIED).

## 2. Scope, method and conventions

### 2.1 Method
- Primary manufacturer datasheets were downloaded and read (docs/datasheets/cellular/INDEX.md). Indian distributor pages (Hubtronics, Lion Circuits, Evelta, Quartz, IndiaMART) and global distributors (DigiKey, LCSC, TME, Future) were used for prices, seen 2026-11-14 unless noted.
- FX: **1 USD = INR 93.9** (Currencybeacon mid-market, 2026-11-08; PTI reported 93.74 on 2026-11-09) [42]. Sibling reports use 93.7-93.9.
- Prices are ex-GST unless stated. Most Indian prices are single-unit retail. A true 1k price was found only for ESP32-C6-MINI-1 (Lion Circuits) and from global distributors for the Ethernet chips.

### 2.2 Conventions
UNVERIFIED = not confirmed against a primary or distributor source in this run. "Est." = engineering estimate with no source.

### 2.3 What could not be completed (the web-search budget ran out on 2026-11-14)
- Not researched: Fibocom, MeiG, Neoway, Telit Cinterion, Sequans-based modules, and the status of u-blox's cellular business.
- India LTE-M/NB-IoT network availability for nRF9151: not verified. Nordic's page lists certified LTE-M/NB-IoT bands 1-5, 8, 12, 13, 17-20, 25, 26, 28, 65, 66, 85, no B40/B41 and no India mention [44].
- No lifecycle/EOL pages were checked for any cellular module. Longevity is UNVERIFIED for every modem. ESP32-C6 longevity to 2035 comes from R03.
- Operator (Jio/Airtel/Vi/BSNL) device-onboarding rules and the M2M numbering/KYC/eSIM rules: from background knowledge only, marked UNVERIFIED in section 8.
- Firm 1k prices from the Quectel/SIMCom India channels; the price of an SDIO Wi-Fi chip supported by EC200A QuecOpen; MT7628 module prices.
- SIMCom A7672S datasheet PDF: download blocked (403 / TLS error).

## 3. Main question — lowest-cost combined "4G + Ethernet + Wi-Fi" module

### 3.1 Candidate architectures

| | (a) Modem OpenCPU host (EC200A-CN) | (b) Cat-1 modem + ESP32-C6 + SPI Ethernet | (c) Cat-1 modem + NXP RW612 | (d) Linux router SoC (MT7628 class) + Cat-1 modem |
|---|---|---|---|---|
| LTE | Cat 4 + WCDMA + GSM B3/B8 [22] | Cat-1/1bis, with or without GSM (choice) | same as (b) | same as (b), via USB ECM/RNDIS [2] |
| Ethernet | RMII/RGMII MAC + external PHY [28] | CH390H or W5500 over SPI [38][39] | on-chip RMII MAC + PHY, TFBGA only [24] | on-SoC switch/PHY (UNVERIFIED) |
| Wi-Fi STA/AP | external SDIO Wi-Fi chip; supported chips undocumented (UNVERIFIED) [28] | ESP32-C6 on-chip 2.4 GHz Wi-Fi 6, pre-certified module | on-chip dual-band Wi-Fi 6 | on-SoC 2.4 GHz (UNVERIFIED) |
| OS | QuecOpen RTOS (vendor SDK) | Zephyr or ESP-IDF on C6 | Zephyr | OpenWrt/Linux |
| Pre-certified radios | modem only (China certs only on CN variant) | modem + ESP32-C6 module (CE-RED per R03) | modem only (chip-down Wi-Fi) | modem only |
| BOM (INR), see 3.2 | ~1,755 (est.) | 1,047-1,465 (no 2G); 1,397-1,916 (2G) | ~1,860 (est.) | ~1,300-1,500 (est., UNVERIFIED) |
| Verdict | High software risk, highest modem cost | **Recommended** | Later upgrade option (3.x) | Not recommended (cost, kernel/CRA burden) |

### 3.2 Costed BOM, option (b) (INR, ex-GST, 1k qty where available)

| Item | Low | High | Basis |
|---|---|---|---|
| LTE modem, no 2G (EC800M-CN / EG800K-CN) | 320 | 499 | USD 3.41 @100 Unikeyic [33]; Hubtronics EG800AK-CN 499.15 single [30] |
| ESP32-C6-MINI-1-N4 (pre-certified) | 319 | 413 | Lion Circuits 1k / 100-500 [37] |
| CH390H SPI Ethernet MAC+PHY | 77 | 91 | USD 0.82-0.97 @490 [38] |
| RJ45 with magnetics (HR911105A class) | 45 | 75 | Hubtronics 74.58 single [40]; 1k figure est. |
| 12-24 V + Li-ion power block | 90 | 90 | brief assumption |
| 40-pin bus connector | 60 | 60 | brief assumption |
| PCB, 4-layer, ~60x80 mm | 50 | 80 | est. |
| SIM holder | 8 | 12 | est. |
| RF connector(s): LTE u.FL/SMA (Wi-Fi uses module antenna) | 15 | 40 | est. |
| 1.8 V to 3.3 V level shifting (modem UART/control) | 8 | 15 | est.; needed per HDG [23] |
| Modem 3.8 V / 2 A rail + 100-470 uF bulk | 25 | 40 | est.; 2 A requirement per HDG [23] |
| ESD/TVS, passives, crystals | 30 | 50 | est. |
| **BOM total** | **1,047** | **1,465** | |
| **Finished (x1.4)** | **1,466** | **2,051** | target 1,000 |
| Variant with 2G modem (A7672S / EC200U-CN, INR 670-950 [8][32][7]) | BOM 1,397 | BOM 1,916 | finished 1,956 / 2,682 |
| Variant with chip-down ESP32-C6FH4 (~INR 154 + ~25 for RF/xtal) instead of module | BOM ~907 | | finished ~1,270; loses module pre-certification |

The enclosure is not included, because the brief's BOM list does not name it (DIN-rail enclosure cost: UNVERIFIED). External antennas are not included either.

### 3.3 Other options costed (est.)
- (a) EC200A-CN: modem INR 1,250-1,454 single retail (Hubtronics, out of stock) [43], assume ~1,000 at volume. Add RMII PHY ~60 (est.), SDIO Wi-Fi chip ~200 (est., chip UNVERIFIED), RJ45 60, power 90, connector 60, PCB 80, SIM 10, 3 RF connectors 60, passives 60, rail 25, misc 10. BOM ~1,755, finished ~2,460.
- (c) RW612 (TFBGA): SoC 997 [27] + QSPI flash ~40 + PHY ~60 + modem 320 + RJ45 45 + power 90 + connector 60 + 6-layer PCB ~120 + SIM 8 + RF 40 + passives 50 + rail 25 + level shifting 8. BOM ~1,863, finished ~2,610.
- (d) MT7628-class Linux module + EC800M over USB: module price UNVERIFIED (est. INR 500-700). BOM ~1,300-1,500, finished ~1,800-2,100. This route also brings a Linux kernel/OpenWrt maintenance stream (CRA).

### 3.4 What to cut to approach INR 1,000 finished
| Cut | BOM saving (INR) | Resulting finished (from option (b) low) |
|---|---|---|
| Keep no-2G modem (already in low case) | 300-450 vs 2G modem | 1,466 |
| Chip-down ESP32-C6 (needs own RED/WPC radio tests) | ~140 | ~1,270 |
| Drop Wi-Fi (4G + Ethernet only; modem or small MCU hosts the CH390H) | ~320 | ~1,010 |
| Drop Ethernet (4G + Wi-Fi only) | ~120-165 | ~1,250 |
| Drop Li-ion charging (part of the 90 power block) | ~20-40 (est.) | small |
| Remove magnetics (not acceptable for industrial Ethernet isolation/EMC) | n/a | not recommended |

Realistic figure: **~INR 1,450-1,600 finished** without 2G, using purchased modules and a careful 1k-quantity buy. With 2G: **~INR 2,000**.

### 3.5 Software path for option (b)
- ESP-IDF: `esp_modem` supports PPP to SIMCom A76xx (example exists; known CMUX-exit issue) [21]. Espressif's CH390 Ethernet driver component exists [38]. Wi-Fi AP + STA and lwIP NAPT (routing LTE to Wi-Fi/Ethernet) are standard ESP-IDF features (not re-verified this run: UNVERIFIED).
- Zephyr: `modem_cellular` supports SIMCom A76xx and Quectel EG800Q but not EC800M/EG800K/EC200U (out-of-tree definitions possible) [19][20]. ESP32-C6 Wi-Fi under Zephyr, SoftAP support and IPv4 NAT/forwarding in Zephyr are UNVERIFIED. Zephyr may serve as an application-level gateway rather than an IP router. If a Zephyr build is required, pair it with **A7672S** (in-tree driver) and prefer W5500 (Zephyr in-tree driver, UNVERIFIED this run) over CH390H.

### 3.x NXP RW612 as module host — LATER UPGRADE OPTION (short feasibility and cost note)

Product-owner direction (2026-11-14): RW612 is treated as a later upgrade, not the main recommendation; stock and price checks are covered by the Wi-Fi/BLE researcher (R03). Module-host angle only:
- Interfaces (datasheet Rev. 9.0, 30 Jul 2026) [24]: 260 MHz Cortex-M33 + TrustZone-M, 1.2 MB SRAM, no internal flash (external QSPI XIP flash via FlexSPI with on-the-fly decryption, up to 128 MB), 5x FlexComm (UART/SPI/I2C/I2S), HS USB 2.0 OTG with PHY, SDIO 3.0, IEEE 1588 RMII 10/100 Ethernet MAC (external PHY), EdgeLock (secure boot, PUF, TRNG, AES/SHA/ECC/RSA, tamper detection), -40..+85 C.
- IMPORTANT package finding: the Ethernet RMII signals appear in the TFBGA145 (8x8 mm, 0.5 mm pitch) signal diagram (datasheet Figure 23) but NOT in the HVQFN116 signal diagram (Figure 24); HVQFN also has only Flexcomm 0-3 and 41 GPIOs. So "RW612 + Ethernet" requires the TFBGA145 package (fine-pitch BGA, more PCB layers/via-in-pad, X-ray inspection) [24]. (Check pin-mux tables in the full datasheet before final decision; the signal diagrams are the evidence used here.)
- Zephyr support: frdm_rw612 board lists on-chip ENET (nxp,enet + MDIO + PTP) with KSZ8081 PHY, on-chip Wi-Fi (nxp,wifi, binary blob from hal_nxp), BLE HCI, USB device and EHCI host, LPC USART [11]. LTE modem would be attached over a FlexComm UART using Zephyr `modem_cellular` (CMUX + PPP) [19]; USB-host CDC-ECM to a modem under Zephyr is not shown anywhere found (UNVERIFIED, assume UART/PPP; UART caps throughput at a few Mbit/s, adequate for Cat-1).
- RAM/flash: Zephyr board target exposes 960 KiB RAM to the application [11]; NXP block diagram lists a separate Wi-Fi CPU with its own RAM (search-level, UNVERIFIED) and NXP SDK notes Wi-Fi driver heap ~60-70 KB [25]. Wi-Fi + Ethernet + PPP + TLS (mbedTLS ~40-60 KB heap per session, typical, UNVERIFIED) should fit in ~960 KiB; external QSPI flash 4-8 MB needed for code + Wi-Fi firmware + dual-slot OTA (MCUboot). Technically feasible; RAM is not the bottleneck.
- Maturity risk: NXP community report of FRDM-RW612 resetting when Ethernet link drops with BLE active under Zephyr 4.3.0 [26].
- Price: DigiKey (MX site, USD) RW612ET-A2IY (TFBGA145, T&R) USD 10.62 at 2,000 pcs, Active, 52-week standard lead time (seen 2026-11-14) [27] = ~INR 997 at 93.9 INR/USD. The SoC alone exceeds the whole module BOM budget (INR 714) before modem, PHY, flash, RJ45, power. NOT viable for the INR 1,000 finished target; realistic finished cost with RW612 host ~INR 2,500+ (estimate, see BOM table).
- Sharing the same RW612 with the Wi-Fi + BLE module: (1) firmware - one Zephyr board/SoC port, one Wi-Fi driver/blob, one MCUboot/EdgeLock key-provisioning flow and one CRA vulnerability-handling stream for two products (real saving in software and SBOM maintenance); (2) certification - a chip-down RW612 design is NOT pre-certified: each product needs its own RED radio tests (EN 300 328 / EN 301 893 for 5 GHz / EN 300 440) plus WPC ETA in India; using one identical pre-certified RW612 module (e.g. third-party u-blox/Murata modules, see R03) in both cards lets both reuse the module's radio reports, with only host-level EMC/safety/RED Art. 3.3 (d/e/f) cybersecurity (EN 18031) and co-location (Wi-Fi + LTE simultaneous transmit) assessment per product. The 4G card adds LTE co-location, so its RF assessment cannot simply copy the Wi-Fi card's.

## 4. LTE Cat-1 / Cat-1 bis module survey (India bands)

Findings so far (batch 1, 2026-11-14; web-search summaries, datasheets not yet cross-checked):

| Module | Chipset / class | Bands / 2G | Notes | Source |
|---|---|---|---|---|
| Quectel EC800M-CN | ASR1606, Cat 1 | China/India region variant | 17.7x15.8x2.4 mm LCC/LGA; cost-optimised | [1][2] |
| Quectel EG800K-CN | Cat 1 bis | China/India region variant; compatible with EC800M/EC800K | same 17.7x15.8x2.4 mm | [3] |
| Quectel EG915U-EU | Cat 1 bis (UNISOC) | LTE B1/B3/B5/B7/B8/B20/B28 + GSM 850/900/1800/1900; BT / Wi-Fi-scan optional. NO B40/B41 (UNVERIFIED for India variants) | VBAT 3.3-4.3 V typ 3.8; design for 1 A VBAT_BB + 2.5 A VBAT_RF; supply >= 3 A recommended | [4][5] |
| SIMCom A7682E | Cat 1 bis | LTE B1/3/5/7/8/20 + GSM 900/1800 | 19.6x19.6x2.4 mm, pin compatible with SIM800C/SIM868 | [6] |
| SIMCom A7683E | Cat 1 bis, LTE only | B1/3/5/7/8/20/28, no GSM | 15.7x17.6x2.4 mm | [6] |
| SIMCom A7672S (module-board listings) | Cat 1 | India variant (S) | Indian retail: Hubtronics INR 950+GST (A7672S-FASE with GNSS); IndiaMART ~INR 700/pc; Robu board INR 2,799 incl GST (breakout board, not bare module). Retail, not 1k price. | [7][8] |

Batch 2 additions:

| Module | Detail | Source |
|---|---|---|
| Quectel EC200U-CN (China/India) | LTE-FDD B1/3/5/8; TDD B34/38/39/40/41; GSM B3/B8 (GSM varies by suffix - verify); Wi-Fi is scan only; India retail: Hubtronics EC200U-CN GNSS mini modem INR 1,785.59 + 18% GST (dev board, not 1k part price) | [12][13] |
| Quectel EC200A-CN | Cat 4 (ASR1803), China/India variant; GSM list not found | [14] |
| Cavli C16QS (Qualcomm QCX216, Cat 1 bis) | India variant C16QS-IN-GNAH, India bands 1/3/5/8/40/41, eSIM + GNSS; TME USD 24.41 (WW variant, single piece); claimed < USD 5 OEM at launch (2023, unverified); C10-series Cat 1 USD 48 single piece | [15][16] |

Batch 3 (2026-11-14, primary datasheets downloaded and read):
- EC800M-CN spec V1.2 [2]: region "China/ India"; LTE Cat 1; LTE-FDD B1/3/5/8, LTE-TDD B34/38/39/40/41 (covers all Indian bands); NO GSM; LCC 17.7x15.8x2.4 mm; VBAT 3.4-4.3 V; USIM x2 (2nd optional, DSSS); UART x3, USB 2.0, I2C, 2x ADC; Wi-Fi scan only; GNSS optional; certifications listed: China SRRC/NAL/CCC only (NO TEC/CE/FCC listed); drivers RNDIS/ECM Linux 2.6-6.5; operating -35..+75 C, extended -40..+85 C.
- EC800M-CN QuecOpen HDG V1.1 [23]: SPI (master default, 1.8 V domain) available in QuecOpen; Wi-Fi scan shares the main antenna and cannot run at the same time as the cellular link (receive only).
- EC200A series spec V1.4 [22]: EC200A-CN region "China, India"; LTE Cat 4 (150/50 Mbps); LTE-FDD B1/3/5/8, TDD B34/38/39/40/41, WCDMA B1/5/8, GSM/EDGE B3/B8 (1800/900) => India bands + 2G fallback; LCC 29.0x32.0x2.4 mm; VBAT 3.4-4.5 V; interfaces include RGMII/RMII x1 and SDIO x2 ("for SD card and Wi-Fi") as standard (not QuecOpen-only), SPI QuecOpen-only; 2 antennas (main + Rx diversity); EC200A-CN certifications listed: China SRRC/NAL/CCC only; EC200A-EU: CE/UKCA/KC/NCC/RCM.
- Cavli C16QS spec V2.7 [15]: Cat 1 bis, 3GPP Rel-14; IN variant bands 1/3/5/8/40/41 (no GSM); LGA (and mPCIe) 26.5x22.5x2.3 mm; VBAT 3.4-4.2 V, Tx peak 970 mA @ 23 dBm; UART x3, USB 2.0, I2C, SPI; single USIM (1.8/3.0 V) + optional integrated eSIM; optional GNSS (GPS/BeiDou); certifications listed: GCF, CE, UKCA, NCC, ICASA, PTCRB, ANATEL, RCM, FCC, IC, TELEC (many marked with footnote 3, likely "planned") - India TEC/MTCTE NOT listed; carrier "TBD"; pin compatible with Cavli C42GM. Chipset not stated in the spec (Qualcomm QCX216 per other sources: UNVERIFIED here).

Batch 4 (2026-11-14):
- EC200A QuecOpen HDG V1.1 [28]: one low-power SDIO 3.0 interface + control pins (WLAN_PWR_EN, WLAN_SLP_CLK, WLAN_WAKE) "for WLAN design"; one RGMII/RMII interface "to connect 100/1000 Mbps Ethernet PHYs" (RGMII 1.8 V only; RMII 1.8/3.3 V); EC200A-EL has no RGMII. VBAT_RF needs >= 2.0 A; 470 uF + 100 nF reference, 100 uF low-ESR bypass, never below 3.4 V. Which Wi-Fi chips are supported by the QuecOpen SDK is not stated: UNVERIFIED. Sources conflict on whether SDIO Wi-Fi is available on all variants (Mini PCIe brochure: QuecOpen only; EC200A-AU datasheet: only AU supports QuecOpen) [22][29].
- India prices (retail, single unit, seen 2026-11-14): Hubtronics Quectel EG800AKCN90LC-2I-SNNSA (Cat 1 bis, LTE-FDD B1/3/5/8, TDD B34/38/39/40/41, LGA 17.7x15.8 mm) INR 499.15 + 18 % GST, OUT OF STOCK [30]; Quartz Components "EC800M-CN" INR 1,325 ex-GST, 50 in stock (listing mislabelled GSM/GPRS) [31]; IndiaMART "EC200U CN Quectel module" tile INR 670/pc (seller/variant not shown, UNVERIFIED) [32]; Unikeyic EC800MCNLF-I03 ~USD 3.63 (1 pc) / USD 3.41 (100 pcs) (search-snippet, not re-checked) [33].
- SIMCom broker prices (ichome, undated): A7672SA-LASE USD 15.36 @1k; A7672E-LASE USD 19.25 @1k; DigiKey A7672E-LASE USD 12.27 @800 [34]. These broker prices are far above Chinese-domestic Cat-1 pricing; real 1k quotes must come from SIMCom/Quectel India channel (UNVERIFIED).

Batch 5 (2026-11-14):
- SIMCom A7672S (Hubtronics listing, A7672S-FASE) [7]: LTE Cat 1, FDD B1/3/5/8, TDD B34/38/39/40/41, GSM/GPRS/EDGE 900/1800 (=> India bands + 2G fallback); VBAT 3.4-4.2 V typ 3.8; -40..+85 C; USB 2.0, UART, USIM 1.8/3 V, I2C, ADC, GPIO, audio; FASE variant has GNSS + BLE; LCC+LGA, compatible with SIM7000/SIM7070 and SIM800A/SIM800F footprints; INR 950 + GST single unit, out of stock (2026-11-14). Search snippet of SIMCom datasheet agrees on bands [35]. SIMCom A7672S datasheet PDF could not be downloaded (Robu 403, Texim TLS error).
- EC200U-CN (Quectel spec V1.4 per search summary): China/India variant LTE-FDD B1/3/5/8, TDD B34/38/39/40/41, GSM B3/B8 OPTIONAL (depends on order code) [36][12].
- Lion Circuits (India, INR, seen 2026-11-14): ESP32-C6-MINI-1-N4 INR 564.71 (1), INR 412.87 (100-500), INR 318.62 (1,000), in stock, ships 7-10 days [37]; SIMCom A7672E (FASE, EU variant) INR 3,068.46 at 100 - EU variants via western channel are 4-6x Chinese-channel prices [37b].
- Ethernet parts: WCH CH390H (10/100 MAC + PHY, SPI, QFN-32) LCSC USD 0.97 @490 (tray), HQOnline USD 0.82 @490 [38]; Espressif maintains an ESP-IDF CH390 driver component [38]. WIZnet W5500 (hardwired TCP/IP + MAC + PHY, SPI) ~USD 1.75-2.09 @1k (LCSC / TME snippets) [39]. RJ45 with magnetics HanRun HR911105A: Hubtronics INR 74.58 + GST (1 pc), Evelta INR 150.63 (10-99) [40].
- ESP32-C6FH4 bare chip: Future Electronics USD 1.64 @5k; DigiKey SG USD 2.83 @5k; Greelly/Tangsemi USD 2.18 @1k (snippet-level) [41]. Chip-down needs own radio certification (not pre-certified).

Batch 6 (2026-11-14):
- EC200U spec V1.4 (downloaded) [36]: EC200U-CN region "China/ India", LCC 28.0x31.0x2.4 mm, LTE-FDD B1/3/5/8, TDD B34/38/39/40/41, **GSM "Optional, B3/8"**, BT 4.2 optional, Wi-Fi scan (11b Rx) optional, UART x3, SPI x1, VBAT 3.3-4.3 V; regulatory listed: China SRRC/NAL/CCC only. This confirms the earlier search-level row.
- EC200A-CN Indian retail (Hubtronics, out of stock): EC200A-CNTA-D10-UGASA INR 1,454.24 ex-GST; EC200ACNHA-N06-SNASA INR 1,250.00 ex-GST [43]. The batch-2 note "GSM list not found" is superseded: GSM B3/B8 is listed [22].
- SIMCom A7670C-LASS (China variant) Hubtronics INR 610.17 ex-GST, out of stock [45].
- Nordic nRF9151 [44]: LTE-M/NB-IoT only (no Cat-1), certified bands 1-5, 8, 12, 13, 17-20, 25, 26, 28, 65, 66, 85 (no B40/B41), 3.0-5.5 V, ~11x12x1 mm LGA SiP. Not a Cat-1 candidate. Its usefulness in India depends on LTE-M/NB-IoT network availability, which is UNVERIFIED.
- Correction: the EC800M chipset "ASR1606" in the batch-1 table is not stated in the Quectel datasheets read here (UNVERIFIED).

Not researched (search budget exhausted): Fibocom, MeiG, Neoway, Telit Cinterion, u-blox (cellular business status), Sequans-based modules.

### 4.1 Consolidated comparison (India-relevant parts)

| Module | Class | India bands | 2G | Wi-Fi | Ethernet | Footprint | VBAT | Certs listed | India price (INR, ex-GST) | Src |
|---|---|---|---|---|---|---|---|---|---|---|
| Quectel EC800M-CN | Cat 1 | B1/3/5/8/34/38/39/40/41 | No | scan only | No (SPI in QuecOpen) | LCC 17.7x15.8 | 3.4-4.3 | SRRC/NAL/CCC | 1,325 retail (Quartz); ~320 (USD 3.41 @100, Unikeyic) | [2][31][33] |
| Quectel EG800K-CN (EG800AK) | Cat 1 bis | same | No | scan | No | LGA 17.7x15.8, EC800M-compatible | n/a | n/a | 499.15 single, OOS | [3][30] |
| Quectel EC200U-CN | Cat 1 | same | Optional B3/B8 | scan (opt.) | No | LCC 28x31 | 3.3-4.3 | SRRC/NAL/CCC | ~670 (IndiaMART tile, UNVERIFIED) | [36][32] |
| Quectel EC200A-CN | Cat 4 | same + WCDMA | B3/B8 | via SDIO chip | RGMII/RMII + PHY | LCC 29x32 | 3.4-4.5 | SRRC/NAL/CCC | 1,250-1,454 single, OOS | [22][28][43] |
| SIMCom A7672S | Cat 1 | B1/3/5/8/34/38/39/40/41 | 900/1800 | No | No | LCC+LGA, SIM7000/SIM800 compatible | 3.4-4.2 | n/a (datasheet not obtained) | 950 single (OOS); ~700 IndiaMART | [7][8] |
| SIMCom A7670C | Cat 1 | China variant (bands UNVERIFIED) | n/a | No | No | n/a | n/a | n/a | 610.17 single, OOS | [45] |
| Cavli C16QS-IN | Cat 1 bis | B1/3/5/8/40/41 | No | No | No | LGA 26.5x22.5 | 3.4-4.2 | GCF/CE/FCC/PTCRB... (no TEC) | TME USD 24.41 single (WW) | [15][16] |
| Quectel EG915U-EU | Cat 1 bis | no B40/B41 | Yes | scan | No | n/a | 3.3-4.3 | n/a | n/a | [4][5] |
| Nordic nRF9151 | LTE-M/NB-IoT | B1/3/5/8 (no TDD) | No | No | No | LGA ~11x12 | 3.0-5.5 | "pre-certified" | not checked | [44] |


## 5. Modem part prices and the 2G fallback question

- Without 2G (Cat-1 bis / Cat-1 LTE-only, China/India variant): the cheapest indications are **~INR 320** (EC800M-CNLF USD 3.41 at 100 pcs, Unikeyic, snippet-level [33]) and **INR 499** (Hubtronics EG800AK-CN single, out of stock [30]). These fit under the old INR 500 ceiling.
- With 2G: SIMCom A7670C-LASS INR 610 [45], EC200U-CN ~INR 670 (UNVERIFIED tile) [32], A7672S ~INR 700 (IndiaMART) to INR 950 (Hubtronics) [7][8]. **INR 500 with 2G was not met by any source found**; 1k-quantity quotes may close the gap (UNVERIFIED).
- EU/global variants bought through western distributors cost 4-6x more: A7672E INR 3,068 @100 (Lion Circuits), USD 12.27 @800 (DigiKey) [37b][34].
- Under the 2026-11-13 update the INR 500 part ceiling no longer applies. 2G adds about INR 300-450 per unit to the BOM, or INR 420-630 to the finished price.
- Recommendation: build the base SKU **without 2G** (Jio has no 2G, and Airtel/Vi are expected to phase it out). Offer a 2G SKU only where field coverage needs it. Note that the EC800M (no 2G) and A7672S (2G) footprints differ, so a second SKU means a second PCB variant unless a dual footprint is designed (open decision).

## 6. 2G sunset outlook in India by operator

Search-level findings (2026-11-14), no official shutdown date found:
- Jio has no 2G network and has lobbied DoT/TRAI for a 2G/3G phase-out policy since early 2024 [9][10].
- Vi opposes a regulatory mandate (low-income users); Airtel and Vi still have large 2G bases (2020 figures: Airtel 135 M, Vi 174 M) [9].
- BSNL 2G is the only connectivity in some areas [9].
- Conclusion (tentative): no sunset date announced; 2G fallback usable for 5+ years on Airtel/Vi/BSNL but not on Jio. To be refined.


## 7. Software path (Zephyr / Linux) and CRA updatability

Findings (2026-11-14):
- Zephyr `modem_cellular` (generic AT + CMUX + PPP driver) officially supports Quectel BG95/BG96, EG25-G, EG800Q; SIMCom SIM7080 and A76xx (A76xx added in a commit tested on A7672SA; other A76xx share one AT manual); u-blox SARA-R4/R5, LARA-R6; Sierra HL7800; Telit ME910G1/ME310G1. Out-of-tree modems can be defined in application code [19][20]. Quectel EC200U/EG915U/EC800M are NOT on the list (could be added out-of-tree; UNVERIFIED effort).
- ESP-IDF `esp_modem` has an A7670 PPP example; known issue: A7670 does not exit CMUX mode cleanly [21].
- Quectel EC200A (ASR1803, Cat 4): Linux USB ECM/RNDIS drivers listed up to kernel ~6.x; Wi-Fi over SDIO only in QuecOpen build and sources conflict on which variants; Ethernet via RGMII/RMII needs external PHY and firmware support (UNVERIFIED). It is an RTOS OpenCPU part, not Linux, so it does NOT natively provide Wi-Fi/Ethernet router function [14][22].
- NXP RW612: 10/100 Ethernet (RMII, IEEE1588) + Wi-Fi 6 + BLE + 802.15.4; Zephyr board support frdm_rw612 with Ethernet (KSZ8081 PHY) [11].
- CRA note: vendor Linux modules (EC25/EG25, SIM7600) ship old kernels; a Zephyr MCU host with a PPP/AT modem avoids carrying a vendor kernel, but modem firmware updates (FOTA) remain the vendor's.


- Linux module routes: EC200A/EC800M are RTOS (QuecOpen) parts. Their USB ECM/RNDIS host drivers are listed for Linux 2.6-6.5 [2][22]. The kernel ages of EC25/EG25 OpenLinux and SIM7600 Linux builds were not verified this run (UNVERIFIED).

## 8. Certification leverage (India TEC/MTCTE/WPC/BIS, EU RED/CRA), operator onboarding, M2M SIM / eSIM rules

India:
- MTCTE: "IoT Gateway" is a Phase-3 product with mandatory certification from 1 Jan 2024. TEC 33010:2025 IoT Gateway GR and TEC 33011:2026 test guide are reported but UNVERIFIED against the Gazette (see R01 sections 5.1/[11][12][13]). DoT states that no MTCTE-notified equipment may be sold or deployed without a certificate [46]. The combined 4G + Ethernet + Wi-Fi module sold standalone is an IoT gateway, so it needs its **own** MTCTE certificate. The China/India modem variants list no Indian certification at all [2][22][36], so there is no module certificate to inherit. Whether TEC accepts the module's RF test reports to reduce host testing is UNVERIFIED.
- WPC: Wi-Fi 2.4 GHz is de-licensed, but an ETA (Equipment Type Approval) is needed for the radio. Whether the ESP32-C6-MINI-1 already holds an ETA is UNVERIFIED (R03 found none).
- BIS CRS: the DC power adapter (if supplied) and the Li-ion cell/battery (IS 16046 Part 2) need registration (R01 [9][10]).

EU (see R01 sections 3-4):
- RED: Art. 3.2 radio tests are inherited from the pre-certified modules (EU variant needed: the CN variants have no CE). The host still needs EMC (EN 301 489 series), safety (EN 62368-1), RF exposure, and a co-location check because LTE and Wi-Fi transmit at the same time. Standard numbers here are from background knowledge (UNVERIFIED this run). EN 18031-1 applies until 10 Dec 2027; from 11 Dec 2027 the CRA applies, and the combined module is probably **CRA Class I, entry 12 (router / cellular modem)** (R01 4.2).
- Consequence: an EU SKU needs an EU-variant modem (EG800K-EU / EG915U-EU / A7672E class), which costs several times more per part (section 5).

Operator onboarding and SIM rules (all UNVERIFIED: background knowledge, not fetched this run, because the search budget was exhausted):
- Indian M2M connections use 13-digit MSISDNs (DoT M2M numbering plan, about 2018). Bulk M2M SIMs are issued against entity KYC to the M2M service provider/enterprise, and end-user KYC is required only for SMS/voice-enabled consumer use cases.
- DoT guidelines (about 2018) allow embedded SIM (eUICC) with OTA profile switching for M2M, under Indian-operator profiles.
- Operator IoT device certification (Jio/Airtel IoT labs) is commercial practice, not a legal requirement, and depends on volume. Confirm directly with the operators.

## 9a. Note on non-Chinese alternatives
- Cavli C16QS-IN: India variant, no 2G, eSIM option, global certifications listed but no TEC [15]. Only a single-piece price was found (TME, WW variant, USD 24.41, about INR 2,290) [16]. Volume price UNVERIFIED.
- Nordic nRF9151: Norwegian, LTE-M/NB-IoT only, not Cat-1 [44].
- Telit Cinterion, u-blox, Sequans: not researched (search budget).

## 9. Trusted source — restrictions on Chinese-origin modules, non-Chinese / made-in-India alternatives

Search-level findings (2026-11-14):
- Trusted-source regime: 2020 Cabinet decision + 2021 DoT licence amendment; operators buy only from "trusted sources/products" designated by NSCS (National Security Council Secretariat) [17]. Huawei/ZTE not designated; Ericsson/Nokia/Samsung cleared.
- Reports say scope may extend to IoT, and that India is increasing scrutiny of Chinese IoT module imports (Chinese suppliers > 80 % of Indian IoT module market). No official notification found that applies trusted-source rules to cellular IoT modules: UNVERIFIED [18].
- Non-Chinese / Indian options identified so far: Cavli (India, but Qualcomm/Chinese-fab ODM details unverified), Telit Cinterion, u-blox/Sequans/Nordic (not yet researched).


## 10. Hardware integration requirements

From Quectel EC800M-CN QuecOpen Hardware Design V1.1 [23] (representative of Quectel Cat-1 LCC parts):
- Supply: VBAT 3.4-4.3 V, must never drop below 3.4 V; source must deliver 2 A; LDO if small headroom, buck if large; reference design uses 470 uF + 100 nF at input and output.
- Bulk/decoupling: ~100 uF low-ESR (ESR <= 0.7 ohm) bypass plus MLCC array (1.8 pF, 3.9 pF, 10 pF, 33 pF, 100 nF) close to VBAT pins; VBAT trace >= 2 mm wide; TVS with VRWM 4.7 V at supply front end.
- Do not remove power while running (flash corruption); power down via PWRKEY / API first.
- PWRKEY: low >= 700 ms to turn on, >= 650 ms to turn off; TVS near any push button.
- IO: 1.8 V domain (UART, SPI, I2C, status) -> level translator or transistor level-shifter to 3.3 V host (HDG Figures 19/20).
- USIM: 1.8/3.0 V; holder close to module (< 200 mm); bypass cap on USIM_VDD < 1 uF; TVS array < 15 pF; 0 ohm series resistors; separate DATA and CLK with ground.
- USB: 90 ohm differential; ESD device junction capacitance matters.
- Antennas: 50 ohm; ESD device on antenna port <= 0.05 pF; pi-match network (C1/C2 NM, R1 0 ohm).
- Module ESD rating: VBAT/GND +/-5 kV contact, +/-10 kV air; antenna +/-4/+/-8 kV; other pins only +/-0.5/+/-1 kV -> all external IOs need TVS to reach IEC 61000-4-2 levels.
- Cavli C16QS [15]: VBAT 3.4-4.2 V, Tx peak 970 mA (still design for >= 2 A transient budget, UNVERIFIED in a Cavli HDG).
- Quectel EG915U-EU forum guidance [4]: design 1 A for VBAT_BB + 2.5 A for VBAT_RF; supply >= 3 A recommended (2G burst).
- EC200A QuecOpen HDG [28]: VBAT_RF >= 2.0 A; 100 uF low-ESR bypass; TVS VRWM 4.7 V; PWRKEY low >= 650 ms (open-drain driver recommended); RESET_N low >= 300 ms; USB_BOOT and RGMII/RMII_RST_N must not be pulled up before start-up; RGMII is 1.8 V only, RMII 1.8/3.3 V.
- Design rules for the UC 4G card:
  - Supply the modem from a dedicated 3.8 V / >= 2 A buck (>= 3 A if 2G is fitted), or directly from the Li-ion cell (3.4-4.2 V within range).
  - Add a low-voltage cut-off above 3.4 V and a 4.7 V TVS on VBAT.
  - Let the baseboard MCU control PWRKEY/RESET (it can power-cycle a hung module) and VBAT enable via a load switch, so it can perform a hard power-cycle after a PWRKEY shutdown attempt.
  - Use 1.8 V translators on UART/RI/DTR/STATUS.
  - Fit SIM TVS < 15 pF, RF ESD <= 0.05 pF, and IEC 61000-4-2 TVS on RJ45/USB/bus pins (module "other pins" are rated only +/-0.5 kV).

## 11. Risks and open decisions

Risks:
1. **Cost target miss**: INR 1,000 finished is not reachable with all three interfaces (section 3.4).
2. **Pricing confidence**: most modem prices are single-unit retail or snippet-level. Get 1k quotes from the Quectel and SIMCom India channels and from IndiaMART volume sellers.
3. **Stock**: Hubtronics showed EG800AK-CN, A7672S, EC200A and A7670C all out of stock (2026-11-14). Only ESP32-C6-MINI-1 (Lion Circuits) and EC800M (Quartz, 50 pcs) were seen in stock.
4. **No Indian certification on CN-variant modems**: the full MTCTE burden sits on the host. An EU SKU needs a different, far more expensive modem variant.
5. **Lifecycle** of all modems is UNVERIFIED. Cat-1 bis parts are newest; Cat-1 ASR parts may be phased out earlier.
6. **Zephyr gaps**: no in-tree driver for Quectel EC800M/EG800K; SoftAP/NAT on ESP32-C6 under Zephyr is UNVERIFIED. ESP-IDF is the lower-risk path for a router function.
7. **Trusted-source policy** could extend to IoT modules for government or utility tenders (UNVERIFIED).

Open decisions for the product owner:
- A. Accept about INR 1,500 finished (no 2G), or drop an interface to stay near INR 1,000.
- B. Make the base SKU without 2G, with a 2G SKU as a separate PCB variant or a dual footprint.
- C. Run the 4G card on ESP-IDF (fast router features) or on Zephyr (common RTOS; prefer A7672S + W5500).
- D. Use a module or chip-down ESP32-C6 (pre-certification versus about INR 140 BOM).
- E. Add a non-Chinese modem footprint (Cavli) for tender SKUs.
- F. Decide whether the 4G card's Wi-Fi is redundant when a Wi-Fi/BLE card is in the stack.

## 12. Sources

[1] https://python.quectel.com/en/products/ec800m-cn
[2] https://developer.quectel.com/en/wp-content/uploads/sites/2/2024/11/Quectel_EC800M-CN_LTE_Standard_Specification_V1.2.pdf
[3] https://www.quectel.com/product/lte-cat-1-bis-eg800k/
[4] https://forums.quectel.com/t/eg915u-eu-clarification-on-lte-current-peaks-and-burst-duration/46610
[5] https://www.quectel.com/product/lte-cat-1-bis-eg915u-series/
[6] https://en.simcom.com/product/A7683E.html ; https://en.simcom.com/product/A7682E.html
[7] https://hubtronics.in/a7672s-fase-lte-gps-module
[8] https://m.indiamart.com/proddetail/simcom-sim-a7672s-gsm-module-2857534824730.html ; https://stg.robu.in/?p=1535405
[9] https://telecomtalk.info/jio-talks-about-shutting-down-2g-3g/915364/ ; https://telecomtalk.info/2g-is-still-important-to-india-heres-why/979150/
[10] https://www.varindia.com/news/reliance-jio-urges-government-action-to-phase-out-2g-and-3g-networks
[12] https://forums.quectel.com/t/is-ec200u-cn-a-good-choice-for-india-need-info-on-supported-bands-wifi-bluetooth-alternatives/52872
[13] https://hubtronics.in/ec200u-cn-4g-gnss-modem
[14] https://www.quectel.com/product/lte-ec200a-series/
[15] https://shop.mev-elektronik.com/wp-content/uploads/C16QS-Cat1.bis-Technical-Specification-Document-V2.7.pdf
[16] https://www.tme.com/ca/en/katalog/p,cavli-wireless-incorporated_1810/
[17] https://www.dtnext.in/amp/story/news/national/telecom-equipment-from-china-to-face-curbs-as-cabinet-approves-buying-only-from-trusted-source ; https://business-standard.com/article/companies/telcos-can-buy-gear-only-from-trusted-vendors-as-dot-tweaks-licence-norms-121031001687_1.html
[18] https://www.newsminimalist.com/articles/india-tightens-scrutiny-on-chinese-iot-module-imports-over-security-concerns-193a6dba
[19] https://docs.zephyrproject.org/latest/services/connectivity/modem/index.html
[20] https://pigweed.googlesource.com/third_party/github/zephyrproject-rtos/zephyr/+/afc481ab318cce462ad64e6fa3740130b37876df
[21] https://docs.espressif.com/projects/esp-protocols/esp_modem/docs/latest/README.html ; https://gist.github.com/diplfranzhoepfinger/44aa433829e36bc7266f11f1e7fc5ab2
[22] https://developer.quectel.com/en/wp-content/uploads/sites/2/2024/11/Quectel_EC200A_Series_LTE_Standard_Specification_V1.4.pdf
[23] https://developer.quectel.com/en/wp-content/uploads/sites/2/2024/11/Quectel_EC800M-CN_QuecOpen_Hardware_Design_V1.1.pdf
[24] NXP RW612 data sheet Rev. 9.0 (30 Jul 2026), copy at https://www.farnell.com/datasheets/4801023.pdf
[25] https://docs.mcuxpresso.nxp.com/mcuxsdk/25.03.00/html/middleware/wireless/WiFi-Bluetooth-802.15.4/topics/feature_enable_and_memory_impact.html ; https://www.nxp.com/assets/block-diagram/en/RW612.pdf
[26] https://community.nxp.com/t5/Other-NXP-Products/FRDM-RW612-Zephyr-BLE-and-Ethernet-concurrently-error/td-p/2347110
[27] https://www.digikey.com.mx/en/products/detail/nxp-usa-inc/RW612ET-A2IY/22036080
[28] https://developer.quectel.com/en/wp-content/uploads/sites/2/2024/11/Quectel_EC200A_Series_QuecOpen_Hardware_Design_V1.1.pdf
[29] https://python.quectel.com/wp-content/uploads/2024/09/Quectel_EC200A系列Mini-PCIe_LTE_Standard_模块产品介绍_V1.2.pdf ; https://cdn.soselectronic.com/productdata/3a/19/8be0160f/ec200aauha-n06-mn0aa.pdf
[30] https://hubtronics.in/wireless-modules/quectel-eg800akcn90lc-2i-snnsa
[31] https://quartzcomponents.com/products/quectel-ec800m-cn-gsm-gprs-module-smd-lcc-package
[32] https://m.indiamart.com/proddetail/vvm601-esp32-s3-with-quectel-ec200u-4g-lte-gps-module-for-ai-iot-applications-2854906987233.html (related-item tile)
[33] https://www.unikeyic.com/products/4g-3g-2g-nb/ec800mcnlf-i03-snnda/644086767.html
[34] https://ichome.com/product-detail/simcom/a7672sa-lase ; https://ichome.com/product-detail/simcom/a7672e-lase ; https://www.digikey.com/es/products/detail/simcom-wireless-solutions-limited/A7672E-LASE/15841445
[35] SIMCom A7672S Spec (search snippet of https://stgaws.robu.in/wp-content/uploads/2023/03/A7672S_Spec_210324.pdf ; download blocked)
[36] https://python.quectel.com/en/wp-content/uploads/sites/2/2024/11/Quectel_EC200U_Series_LTE_Standard_Specification_V1.4.pdf
[37] https://www.lioncircuits.com/parts/ESP32-C6-MINI-1-N4 ; [37b] https://www.lioncircuits.com/parts/A7672E%20(FASE)
[38] https://www.lcsc.com/product-detail/C7498452.html ; https://www.hqonline.com/products/ethernet-chips-1791 ; https://components.espressif.com/components/espressif/ch390/versions/0.4.1/readme
[39] https://www.lcsc.com/product-detail/C32843.html ; https://www.tme.com/us/en-us/details/w5500/ethernet-interfaces-integrated-circuits/wiznet/
[40] https://hubtronics.in/connectors/modular-sockets-rj45-rj11/1815 ; https://evelta.com/single-port-rj45-connector
[41] https://www.futureelectronics.com/p/esp32-c6fh4-C917616295 ; https://www.digikey.sg/en/products/detail/espressif-systems/ESP32-C6FH4/18587545 ; https://www.greelly.com/productdetail/esp32-c6fh4
[42] https://currencybeacon.com/rates/USD/INR ; https://hdfcsky.com/news/rupee-rises-24-paise-to-93-74-against-us-dollar-in-early-trade
[43] https://hubtronics.in/index.php?route=product/search&search=EC200A (seen 2026-11-14)
[44] https://www.nordicsemi.com/Products/nRF9151
[45] https://hubtronics.in/index.php?route=product/search&search=A7670 (seen 2026-11-14)
[46] https://www.eservices.dot.gov.in/mandatory-testing-certification-telecommunication-equipment-mtcte
[11] NXP RW612 datasheet https://nxp.com/docs/en/data-sheet/RW612.pdf ; Zephyr frdm_rw612 https://docs.zephyrproject.org/latest/boards/nxp/frdm_rw612/doc/index.html

