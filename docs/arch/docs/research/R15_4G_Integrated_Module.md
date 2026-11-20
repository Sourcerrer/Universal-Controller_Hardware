# R15 - 4G + Ethernet + Wi-Fi on one card: integrated modules, cheap-router teardowns, lean BOM

Date: 2026-11-14. FX: 1 USD = INR 93.9. Prices are ex-GST unless stated. Builds on R02 (modem survey), R09 (Linux/MT7628), R11 (PHY/RJ45), R06 (power), R14 (connector/enclosure), R01 (MTCTE). Their facts are cited as [R0x], not repeated.

Owner rules applied: Ethernet from a MAC inside a chip (no SPI Ethernet); no more than one processor on the card; owner decision 2026-11-14: **no ESP32 or other separate host or Wi-Fi chip next to the modem; the target is ONE 4G module or router board with Ethernet and Wi-Fi built in**. The only extra parts allowed are those the module needs externally (PHY, magnetics, RJ45), plus power, the bus connector and the enclosure. No Mornsun parts. Parts must be easy to buy in India.

---

## 1. Summary and recommendation

1. **No cellular module or LTE SoC with a built-in Wi-Fi AP radio was found at a usable price.** Every cheap MiFi or CPE pairs its LTE SoC with a separate Wi-Fi chip. Examples: ASR1803S + ASR5803W [S18]; ZX297520V3 + Realtek RTL8192-class [S14][S15][S17]; ASR1803S + AIC8800D [S20]; ASR1828 + RTL8192FR/QCA6174A [S19]. UNISOC 8910DM and V8850 (the chips inside EC200U, EG800 and similar) have Wi-Fi *scan* only, for positioning [S23]. Modules that do contain Wi-Fi are Android "smart modules" (Quectel SC200E/SC200R). They cost USD 55-120 (INR 5,200-11,300) and have no RMII [S36]. So the owner's "one module with Wi-Fi built in" is met by nothing affordable, at any vendor checked.
2. **Best option that meets the rules (closest to "one module"): Quectel EC200A-CN in QuecOpen mode, using Quectel's own reference design.** The QuecOpen Reference Design V1.2 [S1] shows the modem as the only processor. It drives a Motorcomm **YT8512H** 10/100 PHY over RMII and a Realtek **RTL8192ES-CG** 2.4 GHz 802.11n Wi-Fi chip over SDIO. The EC200A-CN covers India LTE FDD B1/3/5/8 and TDD B40/41 (plus B34/38/39), WCDMA, and GSM B3/B8 fallback, at -40..+85 °C [S2][R02]. The RTL8192ES has no user-programmable CPU: it is a radio peripheral like the PHY. **It is still a separate Wi-Fi chip, so this option needs an explicit owner ruling (section 6, risk 1).**
3. **Lean BOM for that option: about INR 1,650 at 1k** (range 1,560-2,400, driven by the unquoted modem price). Adding the optional Li-ion backup (+INR 90, cell excluded) and a DIN enclosure (+INR 110) gives **about INR 1,850, against the current INR 2,697 (-INR 845, -31 %)**. The savings come from the RJ45 and PHY (-454), the 40-pin connector (-376), the removed ESP32 (-109 net) and the power block. The modem costs about +600 more (Cat-4 + 2G + MAC + SDIO, against Cat-1 bis). Finished cost (x1.4) is about INR 2,590.
4. **Firmware.** **Zephyr is not possible** on any integrated option: there is no Zephyr port for ASR1803, ZX297520V3 or UNISOC LTE SoCs. EC200A gives firmware control through QuecOpen. Delta FOTA is supported [S2], but the SDK is under NDA, available on request [S6]. Some EC200A builds run Linux and others an RTOS [S5]. Quectel publishes no security-patch commitment (UNVERIFIED). Get a written SDK + patch commitment before design-in.
5. **Off-the-shelf router boards** (LTE + Wi-Fi + 1 LAN on one PCBA): the cheapest found are about USD 12.5-16 at sample quantity, which is INR 1,170-1,500. Examples: AF107 51 x 38 mm and GW486 [S29][S30][S31]. **None was confirmed under INR 1,000 at 1k.** Volume quotes might reach USD 9-11 (UNVERIFIED). **All of them fail the owner's rules:**
   - locked vendor firmware with no SDK, so no own security updates (the ZTE kernel sources for ZX297520V3 are incomplete and do not boot [S14]);
   - no UART exposed, so the only link to the baseboard is the one LAN port;
   - consumer temperature range, -25..+50 °C;
   - no India or CE certificates stated;
   - unbranded Chinese origin.

   They are useful only as a price benchmark (section 5).
6. **Why cheap routers cost less:**
   - one LTE SoC does modem, router CPU and Ethernet MAC, plus a USD 1-1.3 Wi-Fi chip;
   - Chinese domestic chip pricing at 100k+ volume;
   - consumer-grade magnetics and antennas, 5 V/12 V adapter input, no surge protection, no bus connector, no industrial enclosure;
   - no long-term firmware maintenance;
   - operator bundling.

   In India, the TL-MR100 sells for INR 2,500-3,700 and the Tenda 4G03 for INR 3,400-4,000 [S24][S25]. The under-INR-2,000 devices are MiFis (JioFi JMR1040, about INR 1,800-2,150, no Ethernet [S26]) or white-label IndiaMART routers (INR 1,300-2,500 [S38]).
7. **Options that fail the rules:**

   | Option | Rule failed |
   |---|---|
   | MT7628 + LTE module (TL-MR100 style, SILBO X-21, HLK-7628N) [S21][S35][R09] | 2 processors |
   | ESP32 + modem (current design) | 2 processors; owner decision |
   | Quectel FC41D / FGM842D | MCU Wi-Fi modules, a second processor [S7] |
   | EC200U / EG800 / EC800M / Cavli C16QS | no Wi-Fi AP, no MAC [R02] |
   | SIMCom A7600C / A7608 "MIFI" versions | SDIO Wi-Fi present, but no Ethernet MAC found in the HDG [S12] |
   | MDM9607 OpenLinux modules | Linux 3.18 and about INR 2,900 [R09] |
   | Smart modules | cost |
   | Router PCBAs | firmware control, certification, temperature |

**Recommendation:**
- **If the owner accepts an SDIO Wi-Fi chip as a "part the module needs externally":** build the EC200A-CN + YT8512H + RTL8192ES card from Quectel's reference design, and buy 1k quotes for EC200A-CN.
- **If not:** no compliant single-chip option exists today. Choose one of:
  - (a) accept a router PCBA and give up firmware control, security updates and industrial ratings (not recommended);
  - (b) move Wi-Fi to the existing Wi-Fi/BLE card and make this card 4G + Ethernet with EC200A-CN + PHY (BOM about INR 1,510; it drops the RTL8192ES and its RF);
  - (c) pay for a smart module (INR 5,000+).

---

## 2. Integrated LTE + Ethernet MAC + Wi-Fi options

Legend: Y = meets, N = fails, ? = UNVERIFIED.

| Option | LTE / India bands / 2G | Wi-Fi | Ethernet | Processors on card | SDK / OS | Security updates | Certs | Price (INR) | Stock / longevity | Verdict | Src |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **Quectel EC200A-CN** (ASR1803 [R02]) + YT8512H + RTL8192ES | Cat 4; FDD B1/3/5/8, TDD B34/38/39/40/41; WCDMA; GSM B3/B8 | SDIO 3.0 WLAN port; reference chip RTL8192ES (2.4 GHz 11n); QuecOpen only; one source says only on EC200A-AU (conflict) | RMII/RGMII MAC in module, external PHY (reference YT8512H) | 1 (modem) | QuecOpen (NDA). Some EC200A run Linux, others an RTOS. No Zephyr | DFOTA yes; patch policy ? | EC200A-CN: SRRC/NAL/CCC only [R02]; MTCTE is for our product | Modem 1,250-1,454 single (Hubtronics, out of stock) [R02]; 1k ? (~1,000 est.) | Hubtronics out of stock; Quectel series active; ASR1803 roadmap ? | **Best fit; separate Wi-Fi chip needs owner OK** | [S1][S2][S3][S4][S5][S6] |
| Gosuncn (GosuncnWelink) GM520 | Cat 4, ASR1803, LCC 29x32 | ? | RMII/RGMII listed | 1 | ? | ? | ? | ? | ? | Possible second source to EC200A (check bands and SDIO) | [S13] |
| SIMCom A7600C / A7608E-H, "MIFI" versions (MIFIA/MIFIN/MIFIK) | Cat 4; TDD B34/38/39/40/41 listed; India variant ? | SDIO 2.0 WLAN; supports ASR5803 (W76-L module), SV6318, AIC8800DW | **No RMII/RGMII found in the HDG** | 1 | SIMCom firmware; MIFI build | ? | ? | ? | ? | **Fails Ethernet** | [S12] |
| Quectel EC200U / EG800 / EC800M (UNISOC 8910DM / 8850, ASR1606) | Cat 1 / 1 bis, India bands, GSM optional | scan only | none | 1 | QuecOpen RTOS | ? | — | 320-950 [R02] | — | **Fails Wi-Fi AP, MAC** | [R02][S23] |
| UNISOC 8910DM / V8850 chip | Cat 1 bis | "Wi-Fi SCAN" positioning only | — | — | — | — | — | — | — | **Fails** | [S23] |
| ZTE/Sanechips ZX297520V3 (chip) | Cat 4 class LTE (ZSP880 DSP) + Cortex-A53 (arm32) | external SDIO RTL8192-type, 2.4 GHz | 100M Ethernet + switch on some CPEs | 1 SoC | vendor Linux; ZTE sources incomplete, do not boot | none practical | — | not sold to small OEMs ? | — | **Fails firmware control** | [S14] |
| ASR1803S + ASR5803W (chip set) | Cat 4; FDD 1/3/5/7/8/20/28, TDD 38/39/40/41 (customisable) | ASR5803W 11n, 72 Mbps, 10 users | ? | 1 SoC | vendor | ? | — | chip-level design-in ? | — | Reference only; use via EC200A/GM520 | [S18] |
| ASR1828 | Cat 6/7 | external (RTL8192FR + QCA6174A) | CPE LAN | 1 SoC | vendor | ? | — | — | — | Overkill | [S19] |
| MDM9607 OpenLinux (EC25, SIM7600, MeiG SLM750, Neoway N720) | Cat 4 | external SDIO on some | RGMII on some ? | 1 | Linux 3.18 | weak | various | about 2,900 (EC25 1k) [R09]; SLM750 USD 109 retail = 10,235 | — | **Fails cost and patches** | [R09][S37] |
| Smart modules (Quectel SC200E/SC200R) | Cat 4 | in module | no RMII (USB) | 1 | Android | vendor | yes | USD 55-120 = 5,200-11,300 | — | **Fails cost** | [S36] |
| Quectel FC41D / FGM842D / FCU741R | — | Wi-Fi modules (FC41D, FGM842D have their own MCU) | — | +1 | — | — | — | — | — | **Fails (2nd processor)** | [S7] |
| MT7628 + LTE module (TL-MR100, SILBO X-21 = EC200A + MT7628, HLK-7628N) | via module | MT7628 2.4 GHz 2x2 | 5-port switch on-SoC | 2 | OpenWrt 25.12 maintained [R09] | Y (OpenWrt) | — | HLK-7628N 740-800 + modem [R09] | — | **Fails 1-processor rule** | [S21][S35][R09] |

Notes:
- **Which Wi-Fi chips EC200A supports.** The only documented one is RTL8192ES-CG, in Quectel's reference schematic (sheet 20 "WLAN Design (RTL8192)", U.FL output) [S1]. FC41D, FGM842D and FCU741R are not SDIO-slave Wi-Fi for EC200A. FC41D and FGM842D are standalone MCU Wi-Fi modules [S7]. FCU741R is a Wi-Fi 4 dual-band module whose EC200A driver support was not found (UNVERIFIED).
- **AP + STA.** MiFi products prove AP mode on ASR1803. Whether EC200A QuecOpen supports STA (Wi-Fi as WAN) and AP+STA concurrency is UNVERIFIED. Ask Quectel.
- **SDIO Wi-Fi availability by variant.** One EC200A-AU datasheet says only EC200A-AU supports QuecOpen with SDIO Wi-Fi [S4]. The QuecOpen HDG V1.1 shows the WLAN SDIO port for the series [S3]. **This conflict must be closed with Quectel for EC200A-CN before design-in.**
- **Reference PHYs.** RMII PHY YT8512H and RGMII PHY YT8521SC are in the reference [S1]. Another PHY (e.g. KSZ8081, DP83825) needs QuecOpen driver support (UNVERIFIED).

---

## 3. Cheap 4G routers and MiFis: chipsets and why they are cheap

| Device (India price) | LTE / router SoC | Wi-Fi | Ethernet | Notes | Src |
|---|---|---|---|---|---|
| TP-Link TL-MR100 (INR 2,499-3,699; typical 2,690-2,899) | **MediaTek MT7628NN** router SoC + separate "TP-LINK LTE MODULE" (QMI), 8 MB NOR, 64 MB DDR | MT7628 2.4 GHz 2x2 11n | MT7628 switch, 2 ports | Two processors; OpenWrt support exists (TFTP flash); LTE module chip not identified (UNVERIFIED) | [S21][S24] |
| Tenda 4G03 / 4G05 / 4G06 (4G03 INR 3,400-3,999) | "880 MHz 28 nm processor", Cat 4; SoC not named (UNVERIFIED; GPL tarball or FCC photos needed) | 2.4 GHz 11n N300 | 1-2 ports | — | [S22][S25] |
| JioFi JMR1040 (INR 1,809-2,459, about 2,100; JioFi range "from Rs 999" in operator bundles) | Cat 4; chipset not found (UNVERIFIED); made by Fuhong (Vietnam) / Newtronics (China) | yes | **none** | Battery, no Ethernet; replacement battery Rs 449 | [S26][S27] |
| Airtel 4G Hotspot E5573Cs-609 / AMF-311WW | E5573 = Huawei (imported via Beetel); AMF-311WW maker Rayson; chipsets not found (UNVERIFIED) | yes | none | MiFi | [S28] |
| ZTE MF927U / MF833U1 | **ZX297520V3**, apps CPU 624 MHz | Realtek 8192 | none (MiFi/dongle) | — | [S15][S16] |
| OEM "B315 Pro" CPE | **ZX297520V3** | **RTL8192ES** | RJ45 LAN | — | [S17] |
| L410A MiFi / D140 UFI (OEM) | **ASR1803S** Cat 4 | **ASR5803W** 11n 72 Mbps | none | USB 5 V, -10..55 °C | [S18] |
| Iron-shell CPE (OEM) | **ASR1803S** | **AIC8800D** Wi-Fi 6 | LAN | — | [S20] |
| VSOL / OEM Cat 6 CPE | **ASR1828** | RTL8192FR + QCA6174A | 2 GE | DC 12 V | [S19] |
| ZTE / Sanechips class generally | ZX297520V3: A53 (arm32) + ZSP880 + M0, 64 MB RAM, 128 MB NAND | SDIO RTL8192-type 2.4 GHz | 100M + switch on CPEs | Image signature check usually disabled | [S14] |

Published BOM or teardown cost for a current 4G MiFi or CPE: **none found** (UNVERIFIED). The only dated reference points are IHS teardowns of 2009-2010 3G devices: MiFi 2352 USD 86.89, Huawei E5830 USD 58.56 [S40]. Today's finished-goods FOB prices set an upper bound:
- generic 150 Mbps 4G Wi-Fi router USD 17.9 at 3,000-4,999 pcs, USD 16.5 at 10k (INR 1,550-1,680);
- ASR1803 Type-C 4G router USD 19.97 at 1k-9,999, USD 17.96 at 10k;
- JIMI MiFi USD 17.5 at 5k [S33] (snippet-level).

These prices include the case, adapter or battery, and margin. The PCBA BOM inside is therefore probably USD 9-12 (INR 850-1,130, estimate, UNVERIFIED).

**Where the low price comes from** (comparison with the current design):

1. **One integrated SoC.** ASR1803S and ZX297520V3 contain the LTE modem, an application CPU running the router stack, and an Ethernet MAC (ZX297520V3 CPEs also have a switch). They need only a Wi-Fi chip (RTL8192ES USD 1.28 at 1k [S10]; ASR5803W) and a PHY (YT8512H USD 0.44 [S11]). The current design pays separately for a modem module, an ESP32 module, and an industrial PHY + Würth jack (INR 667).
2. **Chip-down at the factory, not modules.** Router makers buy the SoC, not a Quectel module, so they avoid the module maker's margin and the LCC packaging.
3. **Volume and channel.** Router makers ship 100k-1M units per year at Chinese domestic chip prices. Our parts are priced at Indian retail or distributor level (e.g. EC200A INR 1,250-1,454 single [R02]).
4. **Consumer grade:**
   - 0..40 °C or -10..55 °C ratings;
   - HanRun-class magnetics (INR 85, 0-70 °C [R11]) instead of Würth (INR 477);
   - PCB or stamped-metal antennas instead of SMA/U.FL;
   - 5 V USB or a 12 V wall-adapter input, with no 12-24 V surge, reverse-polarity or EFT protection;
   - no Li-ion power path (MiFi batteries are simple single-cell packs);
   - no bus connector (INR 400 in our design) and a snap-fit plastic case instead of a DIN enclosure.
5. **No long-term software cost.** Firmware is frozen at launch. There is no secure boot, no SBOM or patch stream, and no CRA or ITSAR effort (signature checks are disabled on most ZX297520V3 devices [S14]).
6. **Operator subsidy and bundling.** JioFi models have been offered from Rs 999 with plans [S26]. The "under INR 2,000" price is mostly MiFis without Ethernet. An Ethernet router like the TL-MR100 sells for INR 2,500-3,700 in India [S24].
7. **Retail arithmetic.** A retail price of INR 2,000 is INR 1,695 ex-GST, which suggests an ex-factory price of about INR 1,200-1,400 and a BOM of about INR 900-1,100 (estimate). That is close to our lean core BOM without the industrial parts (section 4).

---

## 4. Lean BOM: EC200A-CN + YT8512H + RTL8192ES (one processor, Quectel reference design)

1k quantity where a source exists, otherwise marked as an estimate.

| # | Item | INR (base) | Range | Basis / source |
|---|---|---|---|---|
| 1 | Quectel EC200A-CN (Cat 4, India bands, GSM B3/B8, RMII, SDIO-WLAN), LCC 29x32 | 1,000 | 1,000-1,454 | Hubtronics single 1,250-1,454 ex-GST (out of stock) [R02]; 1k ~1,000 **UNVERIFIED** (western EU/AU variants USD 21.5-27.7 at 100 [S9]) |
| 2 | Motorcomm YT8512H RMII PHY + 25 MHz crystal | 46 | 46-100 | YT8512H LCSC C2685350 ~USD 0.435 (41) [S11] + crystal ~5 est.; the KSZ8081 industrial alternative is 70-96 [R11] but needs driver confirmation |
| 3 | Realtek RTL8192ES-CG SDIO Wi-Fi + 40 MHz crystal + balun/filter + match | 140 | 140-160 | RTL8192ES LCSC C2686915 USD 1.2751 at 1,040 (120) [S10]; RF parts ~20 est. |
| 4 | 10/100 magnetics + RJ45, -40..85 °C (Pulse HX1188NL + plain shielded RJ45) | 150 | 120-280 | [R11] discrete route. HanRun HR911105A (INR 85) is only 0-70 °C [R11] |
| 5 | Ethernet ESD (TI TPD4E05U06) + Bob-Smith network (75 R x4 + 1 nF/2 kV) | 17 | 17 | TPD4E05U06 INR 12 [R11] + ~5 est. |
| 6 | 12-24 V input: SMBJ33A + PTC + reverse protection + TI LMR51430 buck set to 3.8 V (VBAT, >= 2 A peaks) | 90 | 70-100 | LMR51430 USD 0.50; no-battery block about INR 70 [R06] + protection ~20 est. |
| 7 | 3.3 V LDO for PHY + Wi-Fi | 10 | 8-15 | est. |
| 8 | VBAT bulk (470 uF + 100 uF low-ESR) + TVS | 20 | 15-30 | EC200A HDG needs >= 2 A and 470 uF [R02] |
| 9 | UART level shift (modem 1.8 V I/O to 3.3 V bus) | 10 | 8-15 | est. (EC200A I/O voltage 1.8 V: UNVERIFIED in this run) |
| 10 | 40-pin 2.54 mm 2x20 box header | 24 | 24-40 | BXCONN 2.54JN-2-20-Z LCSC C53207293 USD 0.253 at 50 [R14] |
| 11 | Nano-SIM holder | 10 | 8-12 | [R02] est. |
| 12 | RF connectors: 3x U.FL (LTE main, LTE diversity, Wi-Fi) | 25 | 15-40 | est.; SMA bulkhead pigtails and antennas extra (about 60-100 each, UNVERIFIED) |
| 13 | PCB 4-layer about 60 x 70 mm (RMII + SDIO + RF) | 60 | 50-80 | [R02] est.; [R14] JLCPCB 4L USD 70.6/m² |
| 14 | Passives, LEDs, misc | 50 | 40-60 | est. |
| | **Core BOM (no battery, no enclosure)** | **≈ 1,652** | **≈ 1,560-2,400** | |
| O1 | Option: Li-ion backup (TI BQ25601 NVDC charger + inductor + NTC + cell holder; **cell excluded**) | +90 | +90-110 | BQ25601 USD 0.47; cellular block about 160 vs 70 without battery [R06] |
| O2 | Option: DIN enclosure (Electrocom EC7060 ABS) | +110 | 85-110 (CamdenBoss CNMB/4 INR 878) | IndiaMART [R14] |
| | **Core + Li-ion + DIN** | **≈ 1,852** | | Finished x1.4 ≈ **2,590** |

**Comparison with the current INR 2,697 design**

| Block | Current (INR) | Lean (INR) | Δ | Why |
|---|---|---|---|---|
| Modem | 400 (EC800M-CN Cat 1) | 1,000 | +600 | EC800M has no MAC and no SDIO WLAN. EC200A adds Cat 4, 2G and WCDMA fallback, RMII and SDIO. It is the cheapest Quectel part found with both [R02][S2] |
| Host + Wi-Fi | 249 (ESP32-WROOM-32UE) | 140 (RTL8192ES + RF) | -109 | Modem is the only processor. The Wi-Fi chip has no user CPU. Loses ESP32 pre-certification (risk 4) |
| PHY + RJ45 | 667 (LAN8742AI + Würth 7499010121A) | 213 (YT8512H + discrete magnetics + ESD) | -454 | The Würth integrated jack (477) is the biggest single saving. YT8512H is Quectel's reference PHY |
| Power incl. Li-ion | 364 | 90 core + 90 option = 180 | -184 | Single buck to VBAT (3.8 V) plus LDO; NVDC charger only on the battery SKU [R06] |
| 40-pin bus connector | 400 (fine-pitch mezzanine) | 24 (2.54 mm 2x20 box header) | -376 | Box header plus ribbon or stacking instead of FX18-class board-to-board [R07][R14]. A mechanical decision: changes the stacking concept |
| Enclosure | 200 | 110 | -90 | IndiaMART ABS DIN case |
| Other (PCB, SIM, RF, level shift, passives) | ≈ 417 (implied: 2,697 minus listed items) | 155 + VBAT bulk 20 + LDO 10 = 185 | -232 | Mostly estimates on both sides |
| **Total** | **2,697** | **≈ 1,852** | **≈ -845** | |

Further cuts:
- HanRun HR911105A instead of discrete magnetics: -65, but 0-70 °C.
- Drop the diversity U.FL: -8. Cat 4 without diversity antenna degrades throughput.
- Without Wi-Fi (Wi-Fi moved to the Wi-Fi/BLE card): -140, core about INR 1,510.

---

## 5. Off-the-shelf router modules (LTE + Wi-Fi + Ethernet on one board) under INR 1,000?

| Board | Price found | MOQ | India LTE / 2G | Wi-Fi | Ethernet | Other I/O | Power | Size | Firmware | Certs | Temp | Src |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **AF107** "4G indoor communication module" (OEM, Shenzhen) | USD 12.49-15.99 = **INR 1,173-1,502** (listing, date ?) | ? | TDD B38/39/40/41 shown; FDD per variant ?; DC-HSPA+ (3G), 2G ? | 802.11b/g/n | 1x 100M LAN | none listed (no UART) | DC 5-12 V | 51 x 38 x 7.8 mm | locked vendor web UI; chipset not stated (DC-HSPA+ suggests a ZX297520V3-class SoC, UNVERIFIED) | none stated | -25..+50 °C | [S29][S31] |
| **GW486** CPE PCBA (OEM) | USD 15.44-16.25 = **INR 1,450-1,526** | ? | FDD B1/3/5/8; DC-HSPA+ | 802.11b/g/n | LAN (count ?) | none listed | DC 5-12 V, < 3 W | 72.5 x 52 x 20 mm | locked | none stated | -25..+50 °C; battery option | [S30][S31] |
| Habolink **AF207** PCBA | USD 15.84 = **INR 1,487** | 5 pcs (3,000 for custom) | Cat 4; bands ? | dual-band 11n/ac (page inconsistent) | 2-4 (inconsistent) | ? | ? | 60 x 60 mm | ? | "FCC, CE" claimed, varies by model | ? | [S32] |
| AF790D mini 4G board | USD 18.98-20.99 = INR 1,780-1,970 | ? | ? | yes | 2 LAN | ? | ? | ? | ? | ? | ? | [S31] snippet |
| USR IoT **USR-RM02** (Hubtronics India) | INR 2,682 ex-GST (3,165 incl.), 0 stock | 1 | "2/3/4G switching"; bands ? | WLAN | 1x 10/100 | watchdog input; UART ? | DC 5-16 V | ? | USR web UI + VPN; chipset ? | ? | ? | [S34] |
| Generic pocket-Wi-Fi PCB | USD 1-5 (tiered) | 1k for USD 1 | ? | ? | none | — | — | — | — | — | — | Alibaba snippet; implausible for a 4G board, ignore (UNVERIFIED) |

**Verdict:**
1. **No board was confirmed under INR 1,000 at 1k quantity.** The cheapest real listings are INR 1,170-1,500 at sample quantity. A 1k quote of USD 9-11 (INR 850-1,030) is plausible but UNVERIFIED. With our 12-24 V front end (about 50), the 2x20 header (24) and a carrier PCB (about 40), the card would be about INR 960-1,620 before the enclosure.
2. **Firmware control and security updates: fail.** All run closed vendor images. For ZX297520V3 the vendor kernel sources are incomplete and do not boot [S14]. No SDK, no secure boot, no patch stream. This conflicts with CRA and ITSAR obligations [R01][R09].
3. **Baseboard link: fail or awkward.** No UART is exposed. Using the single LAN port to talk to the baseboard leaves no customer Ethernet port.
4. **India certification: fail.** No TEC/MTCTE or WPC documents are listed. We would have to certify a black box we cannot modify or patch. The CE claims are unverified.
5. **Reliability: fail.** Rated -25..+50 °C, a consumer adapter input, and an unknown component grade.
6. **Trusted source: fail.** Unbranded Chinese PCBAs with unknown chipsets give no traceability for government or utility tenders (CEA trusted-source guidance, R01). Our EC200A design is also Chinese-origin (Quectel/ASR, Motorcomm), but it has a named, traceable vendor.
7. **Stock and longevity: high risk.** These are marketplace boards whose design can change between batches (inconsistent spec pages [S32]).

**Compared with designing our own:** the lean EC200A card (about INR 1,650 core) costs up to about INR 700 more than a router PCBA plus carrier (INR 30-700, depending on the PCBA quote). In exchange it gives firmware control (QuecOpen), FOTA, -40..85 °C modem rating, India bands with GSM fallback, a UART link, industrial magnetics and ESD, and a traceable vendor. **None of the off-the-shelf boards meets the owner's rules. Use them only as a cost benchmark and as a possible prototype stand-in.**

---

## 6. Risks and open items

1. **Owner rule conflict.** The EC200A route needs a separate SDIO Wi-Fi chip (RTL8192ES). It is a radio peripheral, not a host, but the 2026-11-14 decision says "no separate Wi-Fi chip". **Owner ruling needed.** No compliant single-chip alternative exists (section 1).
2. **EC200A-CN SDIO Wi-Fi availability.** The QuecOpen HDG shows the WLAN port for the series [S3], but an AU datasheet says only EC200A-AU supports SDIO Wi-Fi in QuecOpen [S4]. Get written confirmation from Quectel for EC200A-CN covering RTL8192ES, AP+STA, the RMII driver for YT8512H, and SDK access [S6].
3. **Firmware and security.** QuecOpen is under NDA, with no Zephyr. Some EC200A builds run Linux, others an RTOS [S5]. The Wi-Fi/NAT stack and its CVE patching belong to Quectel. No published patch policy and no documented secure boot were found (UNVERIFIED). This is a CRA/ITSAR exposure: require a contractual support period.
4. **Radio certification.** RTL8192ES is chip-down, not a pre-certified module, so Wi-Fi needs full CE-RED radio testing and India WPC ETA on our own RF design. The ESP32 module avoided this (R03). A pre-certified SDIO Wi-Fi module would avoid it too, e.g. SIMCom's W76-L (ASR5803) used with A7608 [S12], if Quectel supports one. Price and compatibility are UNVERIFIED.
5. **Temperature grade.** RTL8192ES-CG and YT8512H industrial ratings were not confirmed. YT8512C is 0-70 °C [R11]. The EC200A modem is -40..+85 °C [S2].
6. **Modem price and stock.** The 1k price for EC200A-CN is not quoted (retail INR 1,250-1,454, Hubtronics out of stock [R02]). The whole saving depends on getting about INR 1,000 or less.
7. **EC200A certifications.** The CN variant lists only SRRC/NAL/CCC [R02]. TEC MTCTE "IoT Gateway" is needed for our product [R01]. CE would need the EU variant (EC200A-EU, different bands).
8. **Power.** Cat 4 + GSM bursts need >= 2 A on VBAT with 470 uF bulk [R02]. The current Li-ion and supercap plan must cover this.
9. **Trusted source.** Quectel, ASR and Motorcomm are Chinese-origin. Realtek is Taiwanese. Keep the Cavli or Indian-module fallback (no Wi-Fi/Ethernet) for tender SKUs [R02].
10. **Connector change.** The 2.54 mm box header (INR 24) instead of the INR 400 mezzanine is a stack-mechanics decision [R07].

Not verified in this run: chipsets of JioFi, Tenda 4G03 and Airtel hotspots; the LTE module inside TL-MR100; the EC200A-CN 1k price; whether QuecOpen supports Wi-Fi STA or AP+STA; EC200A secure boot; the chipsets and 1k prices of the router PCBAs; RTL8192ES and YT8512H temperature grades; GM520 SDIO Wi-Fi support.

---

## 7. Sources

All seen 2026-11-14 unless noted. "Snippet" = search-result text only; the page was not opened or was blocked.

- [S1] Quectel EC200A Series QuecOpen Reference Design V1.2 (Aug 2023): YT8512H (RMII), YT8521SC (RGMII), RTL8192ES-CG WLAN. https://developer.quectel.com/wp-content/uploads/2024/09/Quectel_EC200A_Series_QuecOpen_Reference_Design_V1.2-1.pdf (saved: datasheets/cellular/Quectel_EC200A_QuecOpen_reference-design.pdf)
- [S2] Quectel EC200A Series LTE Standard Specification V1.4 (DFOTA, bands, -40..85 °C). https://developer.quectel.com/en/wp-content/uploads/sites/2/2024/11/Quectel_EC200A_Series_LTE_Standard_Specification_V1.4.pdf
- [S3] Quectel EC200A Series QuecOpen Hardware Design V1.1 (WLAN SDIO, RGMII/RMII). https://developer.quectel.com/en/wp-content/uploads/sites/2/2024/11/Quectel_EC200A_Series_QuecOpen_Hardware_Design_V1.1.pdf
- [S4] EC200A-AU datasheet (QuecOpen + SDIO Wi-Fi only on AU). https://cdn.soselectronic.com/productdata/3a/19/8be0160f/ec200aauha-n06-mn0aa.pdf ; Mini PCIe brochure https://python.quectel.com/wp-content/uploads/2024/09/Quectel_EC200A系列Mini-PCIe_LTE_Standard_模块产品介绍_V1.2.pdf (snippet)
- [S5] Quectel forum, Bean.Wang-Q, 2025-03-03: "Some EC200A and EC200R also run Linux… The others should run the RTOS." https://forums.quectel.com/t/modules-that-run-linux/44551/2
- [S6] Quectel forum, EC200A SDK request (SDK not public; contact support) (snippet). https://forums.quectel.com/t/ec200a-sdk-request/58426 ; https://developer.quectel.com/doc/shortrange/FC41D/en/Get-Started/Quick-Start-Guide.html
- [S7] Quectel FC41D https://www.quectel.com/product/mcu-wifi-fc41d ; FGM842D https://developer.quectel.com/doc/shortrange/FGM842D/en/Hardware-Manuals/Hardware-Design.html ; FCU741R https://www.quectel.com/product/wi-fi-fcu741r/
- [S8] (reserved)
- [S9] Avnet EC200A-AU USD 27.69 at 100 (84-week lead time); EC200A-EU USD 21.54 at 100 (snippet). https://www.avnet.com/americas/product/quectel-wireless-solutions/ec200aauha-n06-mn0aa/evolve-66504417/ ; https://www.avnet.com/americas/product/quectel-wireless-solutions/ec200aeuha-n06-mn0aa/evolve-56847731/
- [S10] LCSC RTL8192ES-CG C2686915: USD 1.3047 at 520, 1.2751 at 1,040, 64 in stock, QFN-56 (snippet). https://www.lcsc.com/datasheet/lcsc_datasheet_2106070106_Realtek-Semicon-RTL8192ES-CG_C2686915.pdf ; X-On USD 2.45 at 1,040 https://www.xonelec.com/mpn/realtek/rtl8192escg
- [S11] LCSC Motorcomm YT8512H C2685350, about USD 0.435, 16-20k stock, QFN-32 5x5 (snippet). https://lcsc.com/product-detail/Ethernet-Transceivers_Motorcomm-YT8512H_C2685350.html
- [S12] SIMCom A7600C & A7608E-H R4 Hardware Design Manual V1.00, 2024-07-19 (Chinese): MIFI versions support ASR5803 (W76-L), SV6318, AIC8800DW over SDIO 2.0; no RMII found. https://atta.szlcsc.com/upload/public/pdf/source/20260424/D911BAB6FA7ABAEF7E1EA313733F8367.pdf
- [S13] GosuncnWelink GM520 (ASR1803, LCC+LGA 29x32, RMII/RGMII) (snippet). https://en.sekorm.com/news/89962675.html
- [S14] Linux kernel docs, "Booting Linux on ZTE zx297520v3 SoCs". https://docs.kernel.org/arch/arm/zte/zx297520v3.html
- [S15] ZTE MF927U spec sheet (ZX297520V3 + Realtek 8192) (snippet). https://www.comx-computers.co.za/MF927U-specifications-231470.htm
- [S16] Conrad datasheet, ZTE MF833U1 (ZX297520V3, 624 MHz) (snippet). https://asset.conrad.com/media10/add/160267/c1/-/en/002612241DS00/podatkovna-tablica-2612241-zte-mf833u1-4g-internet-kljuc-150-mbits.pdf
- [S17] Sincere One B315 Pro OEM CPE (ZX297520V3 + RTL8192ES, RJ45) (snippet). https://sincereonetech.com/products/oem-4g-cpe-router-b315-pro-support-band-b28/
- [S18] Global Sources spec sheets: L410A MiFi and UFI (ASR1803S + ASR5803W). https://p.globalsources.com/IMAGES/PDT/SPEC/615/K1221163615.pdf ; https://p.globalsources.com/IMAGES/PDT/SPEC/247/K1205347247.pdf (saved in datasheets/cellular)
- [S19] ASR1828 Cat 6 CPE spec (RTL8192FR + QCA6174A-1, 12 V) https://p.globalsources.com/IMAGES/PDT/SPEC/357/K1220874357.pdf ; MikroTik R11e-LTE7 (ASR1828, Cat 7) https://cdn.mikrotik.com/web-assets/product_files/R11e-LTE7_260101.pdf (snippet)
- [S20] ASR1803S + AIC8800D CPE listing (snippet). https://www.walmart.com/ip/19305169958
- [S21] OpenWrt ramips commit, TL-MR100 (MT7628NN, W25Q64, 64 MB, TP-LINK LTE MODULE via QMI) https://git.freifunk-franken.de/mirror/openwrt/src/commit/223eec7e81f8506592fc89cf79a2f14360f5c57b/target/linux/ramips ; OpenWrt forum https://forum.openwrt.org/t/any-possibility-of-the-tp-link-tl-mr100-being-supported/105490 (snippets)
- [S22] SpeedGuide Tenda 4G03 ("880 MHz 28 nm processor") (snippet). https://www.speedguide.net/routers/tenda-4g03-n300-wi-fi-4g-lte-router-4670
- [S23] UNISOC 8910DM https://www.unisoc.com/en/product/WA-IoT/8910DM ; V8850 https://www.unisoc.com/en/product/WA-IoT/V8850 (Wi-Fi scan only) (snippets)
- [S24] TL-MR100 India prices: Golchha INR 2,690 https://golchhacomputer.com/product/7684-tp-link-mr100-300-mbps-wireless-n-4g-lte-router ; PriceBefore (low INR 2,499, current 3,599) https://www.pricebefore.com/tp-link-tl-mr100-300mbps-wireless-n-4g-lte-wi-p496739.html ; Dealsmagnet INR 2,899 (2026-03-05) https://www.dealsmagnet.com/deal/TP-link-TL-MR100-300Mbps-Wireless-4G-WiFi-Router-14QSzmCp (snippets)
- [S25] Tenda 4G03 India: ShopyVision INR 3,999 https://www.shopyvision.com/?p=89912 ; IndiaMART INR 3,400 https://m.indiamart.com/tanishtechnologies/tenda-networking-devices.html (snippets)
- [S26] JioFi JMR1040 prices https://www.pricebefore.com/jio-jiofi-6-jmr1040-wireless-data-card-black-p471029.html ; https://www.smartprix.com/data_cards/jio-brand ; "JioFi models starting at Rs 999" https://telecomtalk.pages.dev/posts/reliance-jio-offers-4-jiofi-models-starting-at-rs-999-which-one-should-you-buy- ; battery Rs 449 https://telecomtalk.info/reliance-jio-mobiles-jiotags-smartdevices-accessories-july2026/1009771/ (snippets)
- [S27] JMR1040 manufacturer listing https://www.desertcart.co.th/products/118993659 ; Cat 4 https://www.newegg.com/p/0E6-01GC-004D7 (snippets)
- [S28] Airtel E5573 = Huawei via Beetel https://telecomtalk.info/?p=136927 ; AMF-311WW maker Rayson https://www.desertcart.co.za/products/232817939-airtel-xstream-wi-fi-digitaltv-amf-311-ww-150-mbps (snippets)
- [S29] AF107 4G Indoor Communication Module product specification. https://file.elecfans.com/web2/M00/2A/D7/poYBAGHNKIyAT6VrAAyyfr6Emn0515.pdf (saved)
- [S30] GW486 4G CPE PCBA specification. https://file.elecfans.com/web2/M00/24/F9/pYYBAGG0CPSAAF6fAAGHeAMBnvU146.pdf (saved)
- [S31] Alibaba-mirror listings (page 403, snippet prices): GW486 https://china.org.ru/product/1600375902240 ; AF107 https://china.org.ru/product/1600411360368 ; AF790D https://china.org.ru/product/1600415327740
- [S32] Habolink AF207 4G router PCBA, USD 15.84, MOQ 5. https://www.alibaba.com/product-introduction/4G-SIM-Router-PCBA-Mini-WIFI_1600824554930.html
- [S33] OEM finished-router FOB prices (snippets): Global Sources 4G router listings https://www.globalsources.com/Wireless-router/4G-LTE-WiFi-Router-1237090857p.htm , JIMI MiFi https://www.globalsources.com/Wireless-router/4G-Router-1229925538p.htm ; ASR1803 router tiers https://www.alibaba.com/product-detail/ST-ASR1803-CPU-Mini-150Mbps-Pocket_1600907675313.html
- [S34] Hubtronics USR-RM02, INR 2,682.20 ex-GST, 0 stock. https://hubtronics.in/usr-rm02
- [S35] SILBO X-21 (EC200A + MT7628, 5 Ethernet ports) (snippet). https://lntsufin.com/product/silbo-x-21-4g-4-150-mbps-wifi-routers/16940-1416
- [S36] Quectel SC200E/SC200R prices (snippets): https://www.findchips.com/detail/sc200ewfna-e56-unnna/Quectel-Wireless-Solutions-Co-Ltd ; https://www.shijiaic.com/productdetail/sc200rnana-e51-ugnda ; https://soselectronic.com/en/products/quectel/sc200eglna-e53-ugnda-397947
- [S37] MeiG SLM750, 4gltemall (USD 109) (snippet). https://www.4gltemall.com/meig-slm750.html
- [S38] IndiaMART 4G SIM router listings, INR 1,300-2,500 (snippet). https://m.indiamart.com/impcat/wireless-router.html
- [S39] (reserved)
- [S40] Electronics360 / IHS teardown: Novatel MiFi 2352 BOM USD 86.89 https://electronics360.globalspec.com/article/3256/novatel-vodafone-mifi-2352-mobile-hotspot-teardown ; Huawei E5830 USD 58.56 https://electronics360.globalspec.com/article/3311/huawei-e5830-wireless-modem-teardown (snippets)
- [R01] R01_Standards_Certification.md (MTCTE IoT Gateway, CEA trusted source); [R02] R02_Cellular_4G.md (EC200A bands/certs/prices, EC800M, Cavli); [R03] R03_WiFi_BLE.md; [R06] R06_Power.md (LMR51430, BQ25601 block costs); [R07] R07_Connector_Mechanical_DFM.md (FX18 connector); [R09] R09_Linux_vs_RTOS.md (MT7628, OpenLinux modules); [R11] R11_Baseboard_Ethernet.md (PHYs, RJ45, ESD); [R14] R14_Baseboard_Costed_BOM.md (2x20 header, DIN enclosure, PCB).
