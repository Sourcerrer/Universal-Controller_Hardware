# R18 — Tier-2 Standalone Industrial 4G Router (Linux)

Date: 2026-11-14. FX: 1 USD = INR 93.9. Status: COMPLETE WITH GAPS.

Markers:
- **UNVERIFIED**: not confirmed by a primary source.
- **E**: an engineering estimate.
- **INFERRED**: deduced from other facts.

Numbered sources are in section 11. Internal reports are cited as [R01], [R09] and so on.

Scope: a standalone RUT200-class industrial LTE router for India first and global markets later. It sits beside the Zephyr gateway family. Owner rules applied:
- Linux only;
- Yocto preferred, OpenWrt as the proven alternative;
- reliability and safety first, then cost;
- no Mornsun parts;
- no SPI Ethernet controllers;
- TEC, WPC and BIS for India; CRA-grade security for the global phase.

Background that is not repeated here:
- RUT200 internals: [R16];
- Linux SoC prices and the CIP kernel: [R09];
- EC200A: [R15];
- market and price floor: [R10];
- CRA, RED and MTCTE detail: [R01].

---

## 1. Summary and recommendation

1. **Recommended platform: ST STM32MP133C, chip-down, running Yocto 6.0 "Wrynose" LTS.**
   - The SoC is the secure-boot "C" line, Cortex-A7, two Ethernet MACs and a USB HS host, in the LFBGA289 package with 0.8 mm ball pitch.
   - Memory: 256 MB DDR3L and 256 MB SPI-NAND.
   - Updates: RAUC A/B, signed.
   - Boot chain: TF-A, then OP-TEE, then U-Boot, then a signed FIT image.
   - Kernel: a CIP-maintained 6.12 kernel.
   - Cellular: a Quectel EC200A-CN Cat 4 modem over USB.
   - Ethernet: two 10/100 PHYs.
   - Wi-Fi: an optional 2.4 GHz Wi-Fi 4 chip or module that has a mainline AP-mode driver.

   Reasons:
   - This is the only option that meets the owner's preferred OS (Yocto), open documentation, hardware secure boot, a published longevity commitment (10-year rolling programme [R09]) and a 0.8 mm-pitch package all at once.
   - **The same board also runs upstream OpenWrt.** OpenWrt has had an `stm32/stm32mp1` target since 24.10.0 [24], and Bootlin maintains an ST OpenWrt feed (24.10.6 with ST BSP v6.2, July 2026) [25]. If building a router feature set on Yocto overruns, the OS choice can be reversed without a respin.
2. **MT7628AN + OpenWrt (the exact RUT200 pattern) is the cheapest option: about INR 8,200 ex-works against about INR 11,400.** It is rejected as the main platform:
   - It has no hardware root of trust or secure boot [R09], so it cannot meet the owner's CRA list (secure boot) for the global phase.
   - It is a 2014 part [18] that appears in neither of MediaTek's published longevity programmes [17].
   - Its 128 MB DDR2 is the memory type hit hardest by the 2026 legacy-DRAM shortage [39].

   It remains a fast India-only fallback (section 4).
3. **MT7981 (Filogic 820) + OpenWrt** is technically strong:
   - ARM A53 cores and a Wi-Fi 6 MAC, with an MT7976 RF companion chip.
   - BootROM/eFuse secure boot [20].
   - Core cost close to the STM32MP13 + Wi-Fi option.

   But its documents are under NDA, MediaTek publishes no longevity commitment for it, and in practice it runs OpenWrt only. Yocto on MT7628 or MT7981 is possible on a mainline kernel but impractical (section 3.4).
4. **BOM, recommended base SKU** (Wi-Fi, one SIM, isolated RS-485, 2 DI / 2 DO, 9–36 V input, aluminium DIN case): **about INR 5,370**.
   - Finished cost (×1.5): INR 8,050.
   - Plus INR 750 royalty: INR 8,800.
   - Plus 30 % profit: **ex-works about INR 11,440**.
   - **Lite SKU** (no Wi-Fi, non-isolated RS-485, plastic case): about INR 9,310.
   - **Lite SKU with a Cat-1 bis modem**: about INR 8,530.
   - **GNSS/vehicle SKU**: about INR 13,600.
5. **Price position: we do not undercut the RUT200 like for like.**
   - The RUT200 sells at INR 7,569–8,500 from IndiaMART dealers [3][4][5] and INR 13,700 at ThinkRobotics [6].
   - The USR-G806w is INR 8,008 ex-GST and the USR-G809 INR 10,528 ex-GST at Hubtronics [8][10].
   - Under the ×1.5 + royalty + 30 % model at 1k volume, our ex-works price lands between the RUT200's dealer and retail prices. Channel margin then comes on top.
   - **We win on specification instead:**
     - isolated RS-485 (the RUT200 has none);
     - 2 DI / 2 DO;
     - 9–36 V input;
     - -40 to +75 °C (USR is -20 to +70 °C [7][9]);
     - dual SIM;
     - a NavIC GNSS option;
     - verified secure boot and signed A/B updates;
     - Indian support.
   - The like-for-like competitor is a RUT200 plus RS-485 and GNSS, i.e. Teltonika TRB245 / RUT956 class at INR 16,000–24,000 [R10][R16].
   - Cost-down paths are listed in section 5.4.
6. **GNSS: yes, as a variant (SKU "-G"). AIS-140: no, not in this router.**
   - The -G variant adds a Quectel L89HA GPS + NavIC L1/L5 receiver on a UART, an ignition-sense input and the vehicle power front end. It targets fleet and asset location, not regulatory tracking.
   - AIS-140 requires features that do not fit a DIN-rail router, and needs CMVR type approval at ARAI or ICAT [47]:
     - embedded SIM;
     - internal GNSS antenna;
     - 4-hour internal battery;
     - IP65;
     - accelerometer and gyroscope;
     - 4 DI / 2 AI / 1 serial port;
     - sleep current ≤ 20 mA;
     - ISO/TS 16949 manufacturing.

   If AIS-140 is a business goal, make a separate tracker product (section 8).
7. **Certification, India.**
   - TEC MTCTE: "Router" is a Phase IV product (ER TEC37682308) [50][51]. Wi-Fi equipment (2.4/5 GHz), "IoT Gateway" and "Tracking Device" are Phase III [51].
   - WPC ETA: self-declaration on Saral Sanchar for 2.4 GHz Wi-Fi, INR 10,000 per model [53].
   - BIS CRS: consultants list routers under CRS (IS 13252-1 or IS/IEC 62368-1) [54]. This is UNVERIFIED against the official order.
   - Global phase: CE-RED, then the **CRA as an Important Class I product (routers, Annex III item 12)**, which means a notified body unless a harmonised standard is cited [R01].

---

## 2. Reference products: features and India prices

### 2.1 Competitor table

Prices are listings at quantity 1. "ex" means ex-GST.

| Product | Cellular | LAN / WAN | Wi-Fi | SIM | Serial | DI / DO | GNSS | Power input | Temp. | VPN / features | Case | India price (INR) | Src |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Teltonika RUT200** | Cat 4 (EC200A [R16]) | 1 WAN + 1 LAN, 10/100 | 11n 2.4 GHz AP/STA, 50 users | 1× 2FF | none | 1 DI / 1 DO | no | 9–30 V, reverse-polarity protection, surge >31 V 10 µs; <6.5 W | -40..+75 °C | OpenVPN, IPsec, PPTP, L2TP, DMVPN, ZeroTier, WireGuard, Tinc; Modbus TCP master/slave; MQTT gateway; data-to-server; RMS | Aluminium + plastic, IP30 | 7,569 / 8,000 / 8,500 (IndiaMART dealers); 13,699.99 (ThinkRobotics) | [1][3][4][5][6] |
| **Teltonika RUT241** | Cat 4 | 1 WAN + 1 LAN | 11n, plus 802.11s/r/k/v | 1× 2FF + eSIM (SGP.22) | none | 1 / 1 | no | 9–30 V, <6.5 W | -40..+75 °C | as RUT200 plus eSIM | as RUT200 | 23,999 (ThinkRobotics) | [2][6] |
| **USR-G806w** | 4G (-43 suffix = China/India) | 1 WAN/LAN + 2 LAN, 1.5 kV isolation | 11n 2×2 300 Mbps, AP/STA/repeater | 1× 4FF | none (G806s variant has RS-485) | — | no | 9–36 V, reverse-polarity protection; 260 mA avg @12 V | -20..+70 °C | IPsec, PPTP, L2TP, OpenVPN, GRE; SNMP, VLAN; IEC 61000-4-2/-4/-5 level 3; hardware watchdog | Metal, IP30 | 8,007.63 ex / 9,449 incl. (Hubtronics) | [9][10] |
| USR-G806s | 4G | 1 WAN/LAN + 1 LAN | AP | 1 | RS-485 | — | no | 9–36 V | -20..+70 °C | as G806w | Metal | 10,949.99 (ThinkRobotics) | [9][11] |
| **USR-G809** | 4G | 1 WAN + 4 LAN, 10/100, 1.5 kV | 11n 150 Mbps AP (5.8 GHz optional) | 1× 2FF | RS-232 / RS-485 (one or the other) | 2 DI (dry contact) / 2 DO OC 36 V 300 mA | optional | 9–36 V, reverse-polarity protection | -20..+70 °C | PPTP, L2TP, IPsec, OpenVPN, GRE; Modbus RTU↔TCP; hardware + software watchdog | DIN / ear mount | 10,527.97 ex / 12,423 incl. (Hubtronics, 0 stock) | [7][8] |
| Robustel R1510 | Cat 4 | 2× 100M, 1.5 kV | 2×2 11n | — | — | 1 / 1 | — | 9–36 V | -25..+70 °C | RobustOS | — | 18,000–20,000 (IndiaMART, Thane dealer) | [12][R16] |
| InHand IR302 | Cat 1 / Cat 4 | 2× 100M | 11n | — | RS-232/485 | — | — | 9–36 V | — | InHand Linux | — | no India price; MSRP USD 169 = 15,869 | [13][R16] |
| Four-Faith F3426 | 3G (older) | 1 LAN + 1 WAN | — | — | — | — | — | 5–36 V | -35..+75 °C | VPN | — | no India price | [14] |
| Silbo RF44-P (Indian brand) | 4G | — | 150 Mbps | 1 | — | — | — | — | — | DDoS protection | IP30 | 5,049 (IndiaMART) | [15] |
| Silbo X-21 / XNS-020 (Indian) | 4G (X-21 = EC200A + MT7628 [R15]) | 4–5 ports | 150 Mbps | — | — | — | — | X-21: 9–30 V | — | — | — | XNS-020: 6,887.66 | [16][R15] |
| Teltonika TRB245 (gateway, no Wi-Fi) | Cat 4, dual SIM | 1 LAN | none | 2 | RS-232 + RS-485 | 3 configurable I/O + 1 AI | yes | 9–30 V | -40..+75 °C | RutOS | — | about 18,600 (EUR 174) | [R10] |

Notes:
- Datasheets disagree with some listings: the USR-G809 datasheet gives 1 SIM while some listings say dual SIM. Treat the datasheet as authoritative [7].
- IndiaMART prices are dealer listings with GST treatment unclear, and they may be grey imports.
- The RUT200 regulatory line lists only "CB" [1]. Whether Teltonika's RUT2xx holds TEC MTCTE certification is UNVERIFIED.

### 2.2 Feature set we must match or beat

| Feature | Market reference | Our target (base / option) | Position |
|---|---|---|---|
| Cellular | Cat 4 (RUT200, USR) | Cat 4 EC200A-CN (India FDD B1/3/5/8, TDD B34/38/39/40/41, GSM fallback [R15]); Lite: Cat 1 bis | match |
| LAN / WAN | 1 WAN + 1 LAN (RUT200); 1 + 4 (G809) | 2× 10/100, WAN/LAN configurable, 1.5 kV magnetics | match RUT200 (a 4-LAN variant would need an Ethernet switch; not in v1) |
| Wi-Fi | 11n 2.4 GHz AP/STA | 11n 2.4 GHz AP/STA (option) | match |
| SIM | 1 (RUT200); SIM + eSIM (RUT241) | 1× 2FF; dual-SIM option (second holder or MFF2 eSIM) with failover | beat RUT200 |
| Serial | none (RUT200); RS-485 non-isolated (USR) | **RS-485, 2-wire, galvanically isolated**, software-switched termination | beat |
| DI / DO | 1/1 (RUT200); 2/2 (G809) | 2 DI (opto, 0–6 V low / 8–36 V high) + 2 DO (OC 36 V / 300 mA) | beat RUT200, match G809 |
| Power | 9–30 V (Teltonika); 9–36 V (USR) | 9–36 V, reverse-polarity, EN 61000-4-5 ±1 kV; "-V" option: 24 V load dump (ISO 7637-2 5a at AIS-140 levels) | beat |
| Temperature | -40..+75 °C (Teltonika); -20..+70 °C (USR) | -40..+75 °C | match Teltonika, beat USR |
| GNSS | none (RUT200/241); optional (G809) | "-G" SKU: GPS + NavIC L1/L5 | beat |
| VPN | OpenVPN, IPsec, WireGuard, L2TP, GRE, ZeroTier | OpenVPN, IPsec (strongSwan, IKEv2), WireGuard, L2TP/IPsec, GRE. PPTP not offered (insecure) | match |
| Firewall | zone firewall, NAT, port forwarding, DMZ, DoS | nftables zone firewall, NAT, port forwarding, DMZ, rate limits, IP/MAC filters | match |
| Web UI / management | HTTPS UI, SSH, SNMP, RMS cloud | HTTPS UI with unique per-device password, SSH keys, SNMPv3, cloud/bulk FW + config over MQTT/LwM2M or hawkBit | match (cloud is extra work) |
| Industrial protocols | Modbus TCP master/slave, Modbus↔MQTT, data-to-server | Modbus RTU↔TCP gateway, Modbus polling → MQTT/HTTPS, MQTT client | match |
| Security | signed FW (UNVERIFIED enforcement on RUT2xx [R16]) | **secure boot, signed A/B updates with rollback, SBOM, published CVEs** | beat (CRA-ready) |

---

## 3. Platform options

### 3.1 Comparison table

Prices are at 1k unless stated. Core BOM = SoC + memory + SoC power + Ethernet front end + Wi-Fi + crystals; modem, IO and case are excluded (they are the same for all options).

| | (a) MT7628AN + OpenWrt | (b) MT7981B + OpenWrt | (c1) **STM32MP133C + Yocto** (recommended) | (c2) NXP i.MX6ULL / i.MX91 / i.MX93 | (c3) Microchip SAMA7D65 | (d) Yocto on MT7628 / MT7981 |
|---|---|---|---|---|---|---|
| CPU | MIPS 24KEc 580 MHz | 2× Cortex-A53 1.3 GHz [23] | Cortex-A7 650 MHz / 1 GHz | A7 528 MHz (6ULL); A55 (91/93) | Cortex-A7 1 GHz | as (a) / (b) |
| SoC price | USD 2.26 (LCSC 100+) = INR 212 [R09] | MT7981BA USD 6.89 @147+ = INR 647 (LCSC, 2 in stock) [19] | MP133CAF3T USD 5.16 @2k (Avnet); DigiKey DE EUR 5.12 @960 = about INR 485 [32] | 6ULL USD 8.98 (INR 844); i.MX91 USD 8.0–8.8 (INR 755–829); i.MX93 USD 14.94 (INR 1,404) [R09] | SoC 14.49 @260 at RS AU (currency likely AUD, UNVERIFIED); SiP with DDR3L, price not found [36] | as (a) / (b) |
| DDR / flash | 128 MB DDR2 + 16–32 MB SPI NOR (RUT200 pattern [R16]); DDR2 under heavy 2026 price pressure [39] | 512 MB–1 GB DDR3/DDR4 + 128–256 MB SPI-NAND (OpenWrt One: 1 GB DDR4, 256 MB NAND, 16 MB NOR [23]) | 256 MB DDR3L (16-bit; ST routing note AN5692 [33]) + 256 MB SPI-NAND | DDR3L (6ULL); **LPDDR4 only** (i.MX91/93 [R09]) | **DDR3L inside the SiP** (SAMA7D65D2G, up to 2 Gbit) [36]: no DDR layout | as (a) / (b) |
| Wi-Fi | **integrated 2×2 11n** | integrated Wi-Fi 6 MAC/BB + **MT7976C** RF companion (2.4 + 5 GHz) [23] | **none: needs a chip or module** (USB/SDIO, mainline AP driver) | none | none | as (a) / (b) |
| Ethernet | integrated 5-port 10/100 switch and PHYs | 1 GbE internal PHY + SGMII (second port needs an external PHY, e.g. 2.5G EN8811H on OpenWrt One [23]) | 2 MACs (MP133/135) + 2 external 10/100 PHYs | 2 ENET + PHYs | 2× GbE MAC with TSN [36] | — |
| USB for modem | USB 2.0 host | USB 2.0 (USB 3 lanes shared [23]) | USB 2.0 HS host with HS PHY [R09] | yes | yes | — |
| Secure boot | **none in hardware** (no TrustZone or root of trust [R09]) | BootROM verifies BL2 against eFuse key hash; TF-A verifies FIP; U-Boot verifies FIT (MediaTek chain [20]); MT798x-specific docs under NDA (UNVERIFIED) [21] | ROM ECDSA authentication, key revocation, anti-rollback; OP-TEE; **secure boot exists only on secure-line part numbers** (C/F suffix INFERRED, confirm in datasheet) [34] | HAB / AHAB, EdgeLock enclave (91/93) [R09] | secure bootloader, TrustZone, AES/SHA/RSA/ECC [36] | as (a) / (b) |
| OS support | OpenWrt ramips/mt76x8, 25.12 on kernel 6.12 [26] | OpenWrt mediatek/filogic; mainline DTS for MT7981B queued for 6.19 [22]; mt76 MT7981 Wi-Fi upstream since 2023 [22] | Yocto meta-st (OpenSTLinux), **plus upstream OpenWrt stm32 target since 24.10.0** [24], plus Bootlin feed [25] | Yocto (NXP LF); OpenWrt imx target for 6UL/ULL (UNVERIFIED) | Yocto / Buildroot (Linux4Microchip); no OpenWrt target found | mainline kernel boots both; no maintained Yocto BSP layer found (UNVERIFIED) |
| Long-term kernel | OpenWrt has **no LTS**: each series is supported until about 6 months after the next one (24.10 ended Sep 2026) [26][27] | same | Yocto 6.0 LTS to **Apr 2030** [30] + CIP 6.12 SLTS to mid-2035 [R09]. STM32MP13 is **not a CIP reference board** [31] | same as c1; no i.MX on the CIP reference list [31] | same; not on the CIP list [31] | — |
| CRA route | sysupgrade signature (usign/ucert/fwtool) exists but is **optional unless enforced** [28]; CycloneDX SBOM [29]; no secure boot, so integrity cannot be anchored in hardware | as (a) plus hardware secure boot; enforced signed sysupgrade; A/B not native to OpenWrt | secure boot + OP-TEE; RAUC/SWUpdate signed A/B with rollback; dm-verity; Yocto SPDX SBOM and CVE tooling [30] | as c1 | as c1 | — |
| Longevity | none published; launched 2014 [17][18] | none published (MediaTek longevity pages list Genio and modems only [17]) | **10-year rolling (since 2023)** [R09] | i.MX91: 15 years [R09] | not found (UNVERIFIED) | — |
| Package / PCB | DRQFN-156, 4-layer feasible (RUT200 class) | BGA, DDR4 → 6-layer (E) | LFBGA289 14×14 **0.8 mm pitch** [33]; discrete power allowed (AN5586) [33]; 6-layer chosen (E) | 6ULL 0.8 mm (14×14); i.MX91/93 **0.5 mm** → SoM [R09] | SiP removes DDR routing | — |
| Core BOM (E) | about INR 950 | about INR 2,500 (MT7976C price UNVERIFIED) | about INR 2,525 with Wi-Fi; about 1,925 without | about 2,860 (6ULL); higher for 91/93 (LPDDR4) | SiP price unknown | — |
| SoM alternative | HLK-7628N USD 7.9–8.5 = INR 740–800 [R09] | Acelink SM81 USD 39 [19] | MYiR MYC-YF135 USD 16–29 [R09]; iWave (Bangalore) STM32MP13 OSM module, price UNVERIFIED [35] | Toradex OSM i.MX91 USD 25.55 [R09] | SAMA7D65 SiP module GBP 53.89 @21 (RS UK) [36] | — |
| Engineering effort (E, engineer-months) | HW 4–6, SW 6–10 (LuCI branding, IO, Modbus) | HW 7–10, SW 6–10 | HW 7–10 chip-down (3–5 with SoM); SW **18–30 on Yocto** (router stack + UI) or 9–14 on OpenWrt | as c1, +2 for LPDDR4 / SoM | as c1, minus DDR work | SW 20–30, with no vendor support |
| Main risk | fails the CRA secure-boot requirement; EOL; DDR2 price | NDA, longevity, OpenWrt only | Wi-Fi chip choice; Yocto router feature effort; DRAM price | LPDDR4 cost; 0.5 mm pitch | thin ecosystem; no OpenWrt | the OpenWrt router stack is lost and nothing replaces it |

### 3.2 (a) MT7628AN + OpenWrt

- **Proven.** It is the RUT200/RUT241/RUT956 pattern [R16], and upstream OpenWrt has the Teltonika RUT2xx device trees [R16]. The RUT200 cost structure is reachable.
- **Longevity.** MediaTek's longevity pages cover Genio IoT SoCs and modems only [17]. MT7628 is not listed, and no EOL notice was found. The part was launched in September 2014 [18]. **EOL status is UNVERIFIED**; ask MediaTek or a distributor for a last-time-buy notice policy.
- **Security.**
  - There is no hardware root of trust, so integrity rests on software only.
  - OpenWrt can sign sysupgrade images (`SIGNED_IMAGES`, `CHECK_SIGNATURE`, `REQUIRE_IMAGE_SIGNATURE`), but the check is optional unless the firmware enforces it [28].
  - The bootloader can be replaced over UART or SPI by anyone with physical access.
  - Under the CRA, Annex I asks for integrity protection rather than naming "secure boot" [R01]. **The owner's own list requires secure boot**, so (a) fails it.
- **OS.** OpenWrt 25.12 runs kernel 6.12.71 on all targets [26]. OpenWrt supports only the two newest series, so we must rebase every year [27]; Teltonika does this with RutOS.

### 3.3 (b) MT7981 + OpenWrt

- Wi-Fi 6 (2.4 + 5 GHz) and GbE are more than a Cat 4 (150 Mbps) router needs.
- The secure-boot chain exists [20]. The MT798x eFuse procedure and the MT7976C datasheet and price are not public (UNVERIFIED).
- Mainline support is arriving: the MT7981B OpenWrt One device tree was queued for v6.19 [22]. OpenWrt runs ahead with its own 6.12 patches.
- Cost is close to (c1), but the open-hardware and Yocto preference are not met.

### 3.4 (d) Yocto on MT7628 / MT7981

- Both SoCs boot mainline kernels (mt76 covers MT7628 and MT7981 Wi-Fi [22]).
- No maintained Yocto BSP layer was found (UNVERIFIED). MediaTek's Filogic SDK is OpenWrt-based (INFERRED from the OpenWrt-centred ecosystem).
- Yocto here keeps the closed SoC and throws away OpenWrt's router stack (netifd, firewall4, mwan3, LuCI). **Not practical: on these SoCs, OpenWrt is the only realistic OS.**

### 3.5 (c) ARM + Yocto: why STM32MP133C over the others

- **i.MX6ULL** is an older A7 that costs more (USD 8.98) than MP133.
- **i.MX91/93** need LPDDR4 and 0.5 mm-pitch BGA. That pushes the design to a SoM (USD 25–33), which is fine for a "Pro" gateway [R09] but not for a cost router.
- **SAMA7D65** is attractive because its SiP removes DDR routing and it has two GbE MACs. But its SiP 1k price was not found, it has no OpenWrt target, and its ecosystem is smaller.
- **STM32MP133C** wins on all of these:
  - lowest SoC price;
  - two MACs;
  - 0.8 mm pitch;
  - published discrete-power and DDR-routing notes [33];
  - documented secure boot [34];
  - 10-year longevity;
  - the only ARM option with **both** Yocto and upstream OpenWrt [24][25].
- **Chip-down or SoM?**
  - Chip-down is recommended at 1k+ per year. The 0.8 mm-pitch LFBGA plus one x16 DDR3L following ST's reference layout is a moderate-risk layout (E). The PCB rule needs to be checked with the fab.
  - For a fast first build or volumes under 500, use a solder-down SoM: the MYiR MYC-YF135, USD 16–29 [R09], or iWave's Indian-made STM32MP13 OSM module [35]. This adds about INR 50–1,250 per unit (section 5.3).

---

## 4. Recommendation

**Hardware:** STM32MP133CAF3 (secure line, LFBGA289 0.8 mm, -40 °C rated part; check the temperature code in the ordering table), 256 MB DDR3L, 256 MB SPI-NAND, 2× industrial 10/100 PHY, EC200A-CN over USB, optional Wi-Fi 4 on USB or SDIO, isolated RS-485, 2 DI / 2 DO, and a 9–36 V front end. The "-V" option adds a load-dump front end.

**OS: Yocto 6.0 Wrynose LTS (owner preference), with OpenWrt kept as a ready fallback on the same PCB.**

Why Yocto first:
- **A/B updates with automatic rollback (RAUC):** this matters most for unattended sites, where a bricked unit costs a site visit.
- 4-year LTS framework [30] plus a CIP 6.12 kernel to 2035 [R09]. OpenWrt, by contrast, needs a rebase every year [27].
- First-class SBOM and CVE tooling [30].
- Clean OP-TEE and secure-boot integration from ST's meta layer.

Cost of Yocto:
- The router function has to be assembled: nftables, ModemManager or our own EC200A ECM manager (`AT+QNETDEVCTL` [R16]), strongSwan, WireGuard, OpenVPN, a failover daemon, mosquitto/MQTT, libmodbus, and **our own web UI**.
- This costs about 18–30 engineer-months, against 9–14 on OpenWrt (E).

Decision gate: if the Yocto router stack and UI are not at RUT200 parity (table 2.2) by the EVT build, switch to OpenWrt 25.12 on the upstream stm32 target [24]. Then add TF-A/OP-TEE secure boot from the ST feed [25], enforced signed sysupgrade [28], and a U-Boot dual-image scheme. The hardware does not change.

India-only fallback: if security is waived for India v1 and price must match the RUT200, use the MT7628 + OpenWrt RUT200 pattern at about INR 8,200 ex-works (section 5.3). Do this **only** if the global SKU is accepted as a separate later platform.

---

## 5. BOM and ex-works price

### 5.1 Recommended base SKU (STM32MP133C, Wi-Fi, one SIM, isolated RS-485, aluminium case)

Prices are in INR at 1k, ex-GST.

Status codes:
- **S**: sourced price;
- **R**: taken from an internal report;
- **E**: estimate.

| # | Block / part | INR | Range | Status / basis |
|---|---|---|---|---|
| 1 | SoC STM32MP133CAF3 | 485 | 480–890 | S: Avnet USD 5.16 @2k; DigiKey DE EUR 5.12 @960; Mouser 1 GHz F-line USD 8.46 @960 [32] |
| 2 | DDR3L 2 Gbit (128M×16) | 560 | 375–940 | E: 2026 legacy-DRAM surge [39]; RS EUR 10.46 @198 (stale) [41]. **UNVERIFIED, get a quote** |
| 3 | SPI-NAND 2 Gbit (W25N02KV) | 235 | 100–490 | S: LCSC snapshots USD 1.06–5.21 at 1k tiers [40] |
| 4 | SoC power, discrete (AN5586 [33]): 3 bucks + LDOs + inductors | 150 | 120–200 | E (TLV62569 USD 0.11 [R14]) |
| 5 | Crystals (24 MHz, 32.768 kHz, 25 MHz) | 25 | 20–35 | E |
| 6 | Ethernet ×2: KSZ8081RNAIA ×2 (INR 96 each), HX1188NL ×2 (INR 102 each), plain shielded RJ45 ×2, TPD4E05U06 ×2, Bob-Smith network | 470 | 300–560 | R [R11] |
| 7 | Modem Quectel EC200A-CN (Cat 4, India bands, GSM fallback), LCC | 1,150 | 1,000–1,454 | S/E: Hubtronics EC200A-CNTA INR 1,454 ex-GST single [42]; 1k price UNVERIFIED |
| 8 | Modem VBAT buck 3.8 V / 2 A + 470 µF bulk + USB ESD + control lines | 120 | 100–150 | R [R15] (LMR51430 USD 0.50) |
| 9 | SIM holder 2FF + ESD | 15 | 10–20 | R [R02] |
| 10 | Wi-Fi 4 2.4 GHz with mainline AP driver: MT7612UN chip-down (USD 4.53 @260) + RF parts, or a pre-certified module | 600 | 450–940 | S/E: MT7612UN [38]; Murata 1DX is NRND [37]. **Driver, certification and part choice open** (section 10) |
| 11 | Power input 9–36 V: fuse, SMCJ33A, -60 V P-FET reverse protection, π-filter, 60 V buck (LMR36015 class) to 5 V | 165 | 140–200 | R/E [R14][R06] |
| 12 | 2 DI (opto, TLP293) + 2 DO (OC MOSFET 60 V + TVS, 300 mA) | 90 | 70–120 | R/E [R14] |
| 13 | RS-485 isolated: CA-IS2092W + SM712 + PTC + switchable termination | 166 | 150–180 | R [R14] |
| 14 | External window watchdog (TPS3431 class) | 30 | 20–40 | E |
| 15 | Pluggable terminals 3.81 mm, 10 poles | 50 | 40–90 | R [R14] (Kefa; Degson costs more) |
| 16 | SMA bulkhead ×3 + U.FL pigtails | 120 | 90–160 | E |
| 17 | Antennas in box: 2× LTE stick + 1× Wi-Fi | 220 | 150–350 | E (UNVERIFIED) |
| 18 | LEDs, reset button, light pipes | 30 | 20–40 | E |
| 19 | PCB 6-layer, about 100×80 mm | 150 | 120–200 | E (4-layer INR 79 [R14] × about 1.9) |
| 20 | Passives and miscellaneous | 120 | 100–150 | E |
| 21 | Aluminium extruded DIN/wall enclosure + end panels + DIN clip | 375 | 250–500 | E (UNVERIFIED; plastic ABS DIN case INR 85–110, V-0 not confirmed [R14]) |
| 22 | Packaging, power pigtail, label | 40 | 30–60 | E |
| | **BOM total** | **5,366** | about 4,400–6,900 | |

### 5.2 Ex-works price (owner formula)

Formula: finished cost = BOM × 1.5; add the firmware royalty (INR 750); then add 30 % profit on (cost + royalty).

| SKU | BOM | Finished (×1.5) | + Royalty 750 | **Ex-works (×1.3)** |
|---|---|---|---|---|
| **Base** (as 5.1) | 5,366 | 8,049 | 8,799 | **11,439** |
| Base without Wi-Fi (-600 chip, -80 connector and antenna) | 4,686 | 7,029 | 7,779 | 10,113 |
| **Lite** (no Wi-Fi, non-isolated RS-485 -146, plastic case -265) | 4,275 | 6,413 | 7,163 | **9,311** |
| Lite with Cat-1 bis modem (about -400; Cat 1 range INR 320–950 [R02]) | 3,875 | 5,813 | 6,563 | **8,531** |
| Dual-SIM option: + second holder + SIM analog switch (EC200A dual-SIM support UNVERIFIED) | +60 | +90 | — | about +117 |
| **"-G/-V" GNSS + vehicle** = base + L89HA (INR 600 at 1k E; Hubtronics INR 677 ex-GST single [45]) + active GNSS antenna and SMA (240) + SM8S36A load-dump TVS (INR 180 [49]) + 100 V buck instead of 60 V (+60) + ignition-sense input (10) | 6,456 | 9,684 | 10,434 | **13,564** |

**Royalty check.** OpenWrt and Yocto carry no licence fee. The INR 750 is internal recovery of software cost.
- Example (E, UNVERIFIED): about INR 60 lakh of Yocto router development plus about INR 30 lakh per year of CVE and maintenance work over a 5-year support period gives about INR 2.1 crore.
- At 5,000 units per year (25,000 units), that is about INR 840 per unit.
- **At 1,000 units per year, INR 750 under-recovers by about 4×.** Keep INR 750 only if volume reaches about 5k per year; otherwise the royalty, or the support-subscription pricing, must rise.
- Cellular SEP licensing is assumed to be covered by the module price (UNVERIFIED).

### 5.3 Comparison with alternatives and competitors

| Item | BOM | Ex-works | Note |
|---|---|---|---|
| (a) MT7628 + OpenWrt, same IO/case/modem: SoC 212, DDR2 128 MB 300 E, NOR 32 MB 60, power 60, magnetics/RJ45/ESD 278, RF 30, PCB 4-layer 85, Wi-Fi built in | about 3,706 | **about 8,200** | cheapest, but no secure boot or longevity |
| (c1) STM32MP133C base (recommended) | 5,366 | **11,439** | |
| (c1) with MYiR MP135 SoM instead of lines 1–5 (USD 16–29 = INR 1,500–2,700 vs 1,455) | 5,410–6,610 | 11,500–13,840 | for a fast EVT or low volume |
| (b) MT7981 + OpenWrt | about 5,350 E | about 11,400 E | MT7976C price UNVERIFIED |
| RUT200 India | — | 7,569–8,500 (dealer) / 13,700 (retail) | [3][4][5][6] |
| RUT241 India | — | 23,999 | [6] |
| USR-G806w / G806s / G809 | — | 8,008 ex / 10,950 / 10,528 ex | [10][11][8] |
| Robustel R1510 | — | 18,000–20,000 | [12] |
| Silbo (Indian) | — | 5,049–6,888 | [15][16] |

### 5.4 Cost-down levers, in order of size

1. **Volume and quotes for the modem and DRAM.** The modem is 21 % of BOM and DRAM 10 %. Both are 1k estimates and DRAM is inflated in 2026 [39].
2. **Make Wi-Fi a SKU option.** Many industrial users only need Ethernet, RS-485 and LTE.
3. **Cat-1 bis Lite SKU.** About 10 Mbps is enough for Modbus/MQTT telemetry.
4. Plastic V-0 DIN case for the Lite SKU.
5. YT8512H PHYs (INR 40 each [R11]) instead of KSZ8081, if their industrial grade is confirmed.
6. Revisit the ×1.5 factor at 5k+ per year.

---

## 6. Security and OS plan (CRA-grade)

| CRA need [R01] | Implementation on STM32MP133C + Yocto | OpenWrt fallback |
|---|---|---|
| Secure boot / integrity | ROM ECDSA-authenticates TF-A BL2 against the key hash in OTP; key revocation and anti-rollback in ROM [34]. TF-A verifies OP-TEE + U-Boot (FIP). U-Boot verifies a signed FIT (kernel, DTB, initramfs). Rootfs is read-only squashfs with dm-verity. **Close the debug port in the product lifecycle state.** | Same TF-A/OP-TEE chain from the ST feed [25]; signed FIT; `REQUIRE_IMAGE_SIGNATURE=1` [28] |
| Signed updates, A/B, rollback | **RAUC** (or SWUpdate): two rootfs slots in UBI on 256 MB SPI-NAND; CMS-signed bundles; U-Boot bootcount fallback; anti-rollback version in OTP. Modem firmware via Quectel DFOTA packed in the bundle [R15][R16] | sysupgrade is single-image by default; A/B needs custom U-Boot and partition work (E 2–3 engineer-months) |
| Confidential storage | Configuration and keys on a separate UBIFS volume, encrypted (fscrypt) with a key sealed by OP-TEE secure storage | same, less mature |
| Secure defaults | Unique per-device admin password and TLS key provisioned at end-of-line; no telnet; SSH key-only; HTTPS only; services off by default; PPTP not offered | same |
| SBOM | Yocto SPDX SBOM per image [30]; publish it with each release | CycloneDX `bom.cdx.json` per image and package (`JSON_CYCLONEDX_SBOM`) [29] |
| CVE handling | Yocto CVE check / VEX on every build; CIP 6.12 kernel; monthly patch release, critical fixes within 14 days; PSIRT, security.txt, CRA Art. 14 reporting (24 h / 72 h / 14 d) [R01] | OpenWrt security advisories + annual rebase [27] |
| Support period | Declare **≥ 5 years, target 8–10**: Wrynose LTS to Apr 2030 [30], then rebase to the next LTS; kernel on CIP 6.12 to 2035 [R09]. STM32MP13 is not a CIP reference board [31], so we carry the board-specific patches. | about 12–18 months per OpenWrt series [26][27]; yearly rebase is mandatory |
| Logging, deletion | Persistent security log (rate-limited); factory reset wipes the encrypted volume (deletes the key) | same |

Kernel note: Wrynose ships Linux 6.18 [30]; ST's OpenWrt feed uses BSP v6.2 on the 6.6 kernel [25]. Choosing **CIP 6.12** means checking how much STM32MP13 support is upstream in 6.12 (DSI/LTDC not needed; ETH, USBH, SPI-NAND, crypto). That is UNVERIFIED. **Do this check before the OS freeze.**

---

## 7. Certification

### 7.1 India

| Scheme | Applicability | Notes | Src |
|---|---|---|---|
| **TEC MTCTE: Router ER (TEC37682308)** | yes, core product | Router is **Phase IV**. DoT exempted the 5G NR parameters in Nov 2023. The scheme (GCS or SCS) and the current mandatory date are UNVERIFIED (Phase III/IV dates were extended several times) | [50][51] |
| TEC MTCTE: "Equipment operating in 2.4 GHz and 5 GHz" | Wi-Fi SKUs | Phase III | [51] |
| TEC MTCTE: IoT Gateway ER (sample TEC24492408, SCS, fee group B) | if marketed as an "IoT gateway" | Phase III, mandatory 1 Jan 2024 per the 2024 list | [51][52] |
| TEC MTCTE: Tracking Device | "-G" SKU if marketed for tracking | Phase III. Market it as "router with GNSS" to avoid this ER, if acceptable to TEC (UNVERIFIED) | [51] |
| NCCS security assurance (ITSAR) for routers | possibly | A security-testing deadline for routers was extended to 1 Jul 2024 per a consultant summary; ITSAR scope for our class is UNVERIFIED | [51] |
| **WPC ETA** | Wi-Fi 2.4 GHz | Self-declaration via Saral Sanchar; RF report from an NABL lab if the radio is not pre-approved; INR 10,000 per model. For the LTE module, ETA scope is UNVERIFIED | [53] |
| **BIS CRS** | UNVERIFIED for the router | Consultant blogs list routers under IS 13252-1 or IS/IEC 62368-1; the official 2021 order was not checked. Any bundled adapter needs CRS. Plan for IS/IEC 62368-1 testing anyway | [54][R01] |

Design rule: build to the EN set below from day 1, so that the same lab data serves TEC (EMC, safety) and CE.

### 7.2 Global (CE, later)

- **RED 2014/53/EU**:
  - EN 301 908-1/-13 (LTE) and EN 301 511 (GSM);
  - EN 300 328 (Wi-Fi);
  - **EN 303 413** (GNSS SKU);
  - EN 301 489-1/-19/-52;
  - EN IEC 62368-1;
  - EN 62311 / EN 50665 [R01].
- **EN 18031-1/-2** applies to products placed before 11 Dec 2027.
- **CRA** after that date: router = **Important Class I (Annex III item 12)**. Use Module B+C with a notified body unless an EN 40000-series standard is cited and applied in full [R01].
- Vehicle-installed EU sales would also need UN ECE R10 E-marking (UNVERIFIED, not researched).

---

## 8. GNSS / AIS-140 variant

### 8.1 What AIS-140 demands

Source: the May 2017 finalized-draft text [47]. The official ARAI PDF was blocked in this run, so check it against the current amended version.

- GNSS with **NavIC/IRNSS** support (devices installed from 1 Apr 2018) and **GAGAN**. Accuracy 2.5 m CEP. Acquisition -148 dBm, tracking -165 dBm. **Internal antenna** (external only when fitment prevents it). Hot/warm/cold start < 5 s / 30 s / 40 s. NMEA 0183. A-GPS.
- At least **4 digital inputs, 2 analogue inputs and 1 serial port**. NC-type emergency button(s), with an emergency alert to the server and SMS fallback.
- PVT reporting every 5 s minimum to **2 IP addresses** (regulatory + emergency). Store-and-forward of **40,000 positional logs**. OTA software and configuration updates.
- **Embedded SIM** (automotive grade, 10-year life, OTA network switching). Multi-slot GPRS.
- **8–32 V operation**, sleep current ≤ 20 mA, **4-hour internal backup battery**.
- **IP65**, tamper-proof, 3-axis accelerometer + 3-axis gyroscope. Manufactured under **ISO/TS 16949**.
- Tests:
  - EMC per AIS-004;
  - IS 9000 environmental tests;
  - **load dump ISO 7637-2 pulse 5a: 65 V / 4 Ω / 200 ms (12 V systems), 123 V / 8 Ω / 200 ms (24 V systems), functional class A**;
  - 36 V for 60 min on 24 V systems (ISO 16750-2);
  - reverse polarity;
  - harness flammability per IS 2465.
- **CMVR type approval** by a test agency: ARAI or ICAT. An ISRO deck counted 52 ARAI-approved IRNSS devices [48].

### 8.2 Decision

A DIN-rail router with external antennas, no battery and IP30 fails at least six of these requirements. Adding them would turn it into a different product: a sealed IP65 case, a Li-ion battery, an IMU, eSIM-only connectivity, and IATF 16949 manufacturing. **Do not pursue AIS-140 with this router.**

Instead:
1. **"-G/-V" router SKU** (fleet, mining, construction-equipment, cold-chain and genset location; non-regulatory):
   - Quectel **L89HA** dual-band GPS + NavIC L1/L5 receiver on a UART (Hubtronics INR 677 ex-GST single [45]). Quectel's L89-S90 is marked NRND at Mouser [45]; **check the L89HA lifecycle**, with Quectel LC76G-class AG3335 parts as the alternative (NavIC support UNVERIFIED).
   - EC200A has no integrated GNSS (EC200A-EU spec [43]), so a separate receiver is needed in any case.
   - Ignition-sense DI.
   - **Vehicle power front end that covers the AIS-140 load-dump levels**: SM8S36A 6.6 kW TVS (58.1 V clamp at 114 A, 10/1000 µs; AEC-Q101) [49], -100 V reverse FET, and a 100 V-rated buck. Pulse-5a margin must be confirmed by test; the 10/1000 µs rating is not the pulse-5a waveform [49].
2. **The base SKU does NOT cover vehicle load dump.** It covers EN 61000-4-5 ±1 kV surge with a TVS clamp just above 36 V.
3. If AIS-140 is a business goal: a **separate tracker product** with these components, as its own project:
   - Cat-1 bis + NavIC module, e.g. Fibocom L610-IN, which advertises IRNSS + NavIC and AIS-140 compliance [46]; or EC200U + L89;
   - Li-ion battery;
   - IMU;
   - eSIM.

---

## 9. Risks

1. **Router software effort on Yocto (highest risk).** RUT200-parity firmware (UI, VPNs, failover, Modbus/MQTT, remote management) is 18–30 engineer-months (E). Mitigation: the OpenWrt fallback on the same hardware (section 4 gate).
2. **Wi-Fi chip for STM32MP13.**
   - Murata 1DX (the ST reference Wi-Fi) is NRND [37].
   - MT7612UN is out of stock at LCSC [38].
   - MT7601U is a 2.4 GHz STA part (AP support UNVERIFIED).
   - Chip-down Wi-Fi means a full radio certification.

   Pick a pre-certified module with a mainline AP-mode driver (mt76, brcmfmac or mwifiex families) and confirm its lifecycle.
3. **DRAM and NAND prices in 2026.** DDR2 contracts rose about 55–60 % in Q2 and 35–40 % in Q3 2026; DDR3 4 Gbit was about USD 12.75 in July 2026; shortages are expected into 2027 [39]. This hits every option, including the RUT200 pattern. Get quotes before price commitments.
4. **Kernel and CIP fit.** STM32MP13 is not a CIP reference board [31]. The ST BSP is on 6.6 [25]. The 6.12 upstream coverage is UNVERIFIED.
5. **Price position.** The ex-works price is above RUT200 dealer prices. Success depends on the spec advantages and local support (section 5.4).
6. **EC200A.**
   - The 1k price is UNVERIFIED and Hubtronics was out of stock earlier [R15].
   - Dual-SIM support is UNVERIFIED.
   - A Cat-1 bis second source is needed for the Lite SKU.
7. **Certification ambiguity.** Router vs IoT gateway vs tracking-device ERs, BIS CRS coverage and NCCS ITSAR scope are all UNVERIFIED. Get a TEC CAB pre-assessment.
8. **CRA Class I.** A notified body is needed until EN 40000 standards are cited [R01]. Budget for it.
9. **L89HA lifecycle**: a sibling L89 part is NRND [45].
10. **MT7628 fallback**: EOL status is UNVERIFIED [17].

### Open decisions for the owner

1. Yocto first with the OpenWrt gate (recommended), or OpenWrt first?
2. Is Wi-Fi in the base SKU, or an option?
3. Is a Cat-1 bis Lite SKU acceptable?
4. Chip-down (recommended) or SoM for EVT?
5. Isolated RS-485 as standard (recommended, reliability-first), or as an option?
6. Royalty and pricing at the expected volume (section 5.2 check).
7. Is AIS-140 wanted at all? If so, it is a separate product.
8. Does the India launch need a TEC Router certificate before the first sale (check the current Phase IV date)?

---

## 10. What could not be verified

- 1k prices for: EC200A-CN, DDR3L 2 Gbit, MT7976C, SAMA7D65 SiP, the iWave MP13 SoM, antennas and the aluminium enclosure.
- The MT7628 EOL notice.
- MediaTek's MT798x secure-boot specifics.
- The STM32MP13 suffix mapping for secure boot (C/F INFERRED).
- Upstream 6.12 coverage for MP13.
- Yocto layers for MediaTek.
- The current MTCTE dates and scheme for Router, BIS CRS coverage of routers, and NCCS ITSAR.
- The official ARAI AIS-140 text (blocked; the 2017 draft was used).
- The InHand and Four-Faith India prices.
- Software effort and royalty figures are estimates.

---

## 11. Sources

1. Teltonika RUT200 datasheet (distributor mirror) — https://download.axilogi.com/Teltonika/Datasheet/RUT200.pdf
2. Teltonika RUT241 datasheet (mirror) — https://download.axilogi.com/Teltonika/Datasheet/RUT241.pdf
3. IndiaMART, Gacrux Automation, RUT200 INR 7,569 — https://m.indiamart.com/gacruxautomation/teltonika-router.html
4. IndiaMART, Prosoftek Corporation, RUT200 INR 8,000 — https://m.indiamart.com/prosoftekcorporation/industrial-router.html
5. IndiaMART, PodGrid Control, RUT200 INR 8,500 — https://m.indiamart.com/podgrid-control/teltonika-router.html
6. ThinkRobotics RUT200 INR 13,699.99 — https://thinkrobotics.com/products/rut200-industrial-cellular-router-1 ; RUT241 INR 23,999 (via R16) — https://thinkrobotics.com/es/products/rut241-industrial-cellular-router-1
7. USR-G809 datasheet — https://cdn.shopify.com/s/files/1/1386/3791/files/Datasheet_USR-G809_Datasheet.pdf
8. Hubtronics USR-G809 (INR 10,527.97 ex-GST) — https://hubtronics.in/usr-g809
9. USR-G806w specifications (G806/G806w/G806s ordering table) — https://cdn.shopify.com/s/files/1/1386/3791/files/USR-G806w_Specifications.pdf
10. Hubtronics USR-G806w (INR 8,007.63 ex-GST) — https://hubtronics.in/usr-g806w
11. ThinkRobotics USR-G806s (INR 10,949.99; search snippet, page returned HTTP 429) — https://thinkrobotics.com/products/4g-industrial-router-usr-g806s-1
12. IndiaMART, Nimbus Technologies, Robustel R1510-4L INR 18,000–20,000 — https://m.indiamart.com/nimbus-technologies-thane/modem-with-serial-and-ethernet-interface.html
13. InHand IR302: Novotech line card (MSRP from USD 169) — https://novotech.com/line-card/inhand-networks.html ; Embedded Works IR302-FQ38-WLAN USD 175 — https://embeddedworks.net/product/wwan1451/
14. Four-Faith F3426 (Maritex) — https://www.maritex.eu/en/product/four-faith-f3426-industrial-communication
15. IndiaMART, Om Automation (Silbo RF44-P INR 5,049; RG44 INR 14,930) — https://m.indiamart.com/om-automation/industrial-router.html
16. lntsufin Silbo X-21 — https://lntsufin.com/product/silbo-x-21-4g-4-150-mbps-wifi-routers/16940-1416 ; XNS-020 INR 6,887.66 — https://lntsufin.com/product/silbo-xns-020-4g-5-150-mbps-wifi-routers/16934-4686
17. MediaTek longevity programmes — https://www.mediatek.com/iot-longevity ; https://www.mediatek.com/modem-iot-longevity
18. MediaTek MT7628 launch press release (Sept 2014) — https://www.mediatek.com/press-room/mediatek-launches-mt7628-industrys-first-802.11n-2t2r-ap-soc-for-home-router-smart-router-and-iot-gateway
19. LCSC MT7981BA/A C45354767 (USD 6.89 @147+) — https://www.lcsc.com/product-image/C45354767.html ; Acelink SM81 SoM USD 39 — https://www.cnx-software.com/2024/07/18/acelink-sm81-mediatek-filogic-820-wifi-6-system-on-module-openwrt-23-05-debian-11/
20. MediaTek secure-boot chain (BootROM → BL2 → TF-A FIP → U-Boot FIT; eFuse) — https://mediatek.gitlab.io/aiot/doc/aiot-dev-guide/sw/yocto/secure-boot.html
21. OpenWrt forum, "Secure boot and mtk_uartboot" — https://forum.openwrt.org/t/secure-boot-and-mtk-uartboot/244199
22. linux-mediatek, "arm64: dts: mediatek: Add Openwrt One AP functionality" (v5, applied to v6.19-next) — https://lkml.iu.edu/2601.0/07054.html ; mt76 MT7981 support patch — https://lore.kernel.org/linux-mediatek/ZGENDwGXkuhrCGFY@pidgin.makrotopia.org/T/
23. OpenWrt One hardware (MT7981B, MT7976C, 1 GB DDR4, 256 MB NAND) — https://docs.banana-pi.org/en/OpenWRT-One/BananaPi_OpenWRT-One ; https://itsfoss.com/news/openwrt-one/ ; https://techinfodepot.shoutwiki.com/wiki/OpenWrt_One
24. OpenWrt 24.10.0 stm32/stm32mp1 target (STM32MP135F-DK images) — https://archive.openwrt.org/releases/24.10.0/targets/stm32/stm32mp1 ; 24.10.5 — https://archive.openwrt.org/releases/24.10.5/targets/stm32/stm32mp1
25. Bootlin, "Updated OpenWrt support for STM32 platforms, OpenWrt 24.10.6 with ST BSP v6.2" (6 Jul 2026) — https://bootlin.com/blog/author/thomas-richard/
26. OpenWrt 25.12.0 release announcement (kernel 6.12.71; 24.10 EOL Sept 2026) — https://lists.openwrt.org/pipermail/openwrt-devel/2026-March/044621.html
27. OpenWrt release table (two most recent series supported) — https://aparcar.codeberg.page/openwrt-org/releases/
28. OpenWrt image signing: RFC "check signatures of sysupgrades via ucert" — https://lists.infradead.org/pipermail/openwrt-devel/2019-April/022445.html ; "build: separate signing logic" — https://lists.infradead.org/pipermail/openwrt-devel/2019-November/025756.html ; release signing — https://openwrt.org/docs/guide-user/security/release_signatures
29. OpenWrt "build: add CycloneDX SBOM JSON support" — https://git.freifunk-franken.de/mirror/openwrt/commit/d604a07225c5
30. Yocto Project 6.0 Wrynose release notes — https://docs.yoctoproject.org/6.0/migration-guides/release-notes-6.0.html ; CNX (support to Apr 2030, Linux 6.18, SBOM/CVE) — https://www.cnx-software.com/2026/05/14/yocto-project-6-0-wrynose-released-with-linux-6-18-lts/
31. CIP reference hardware — https://wiki.linuxfoundation.org/civilinfrastructureplatform/ciptesting/cipreferencehardware
32. STM32MP133 prices: DigiKey DE STM32MP133CAF3 — https://www.digikey.de/en/products/detail/stmicroelectronics/STM32MP133CAF3/21348925 ; Avnet STM32MP133CAF3T — https://www.avnet.com/americas/product/stmicroelectronics/stm32mp133caf3t/evolve-64854597 ; Findchips STM32MP133DAF7 — https://www.findchips.com/search/STM32MP133DAF7 ; ST eStore — https://estore.st.com/en/stm32mp133caf3-cpn.html (figures from search snapshots)
33. ST AN5692 DDR routing for STM32MP13x — https://www.st.com/resource/ja/application_note/an5692-ddr-memory-routing-guidelines-for-stm32mp13x-product-lines--stmicroelectronics.pdf ; AN5586 discrete power — https://www.st.com/resource/en/application_note/an5586-stm32mp13x-mpu-product-line-discrete-power-supply-hardware-integration-stmicroelectronics.pdf
34. ST wiki: STM32 MPU ROM code secure boot — https://wiki.st.com/stm32mpu/wiki/STM32_MPU_ROM_code_secure_boot ; How to perform Secure Boot — https://wiki.st.com/stm32mpu/wiki/How_to_perform_Secure_Boot_from_Distribution_Package
35. iWave iW-RainboW-G54M STM32MP13x OSM module datasheet — https://iwavesystems.com/wp-content/uploads/2023/10/iW-RainboW-G54M_STM32MP13x_OSM_Module-Datasheet-R2.0-REL0.1.pdf
36. Microchip SAMA7D65D2G — https://microchip.com/en-us/product/SAMA7D65D2G ; RS AU SAMA7D65-V/7EW — https://au.rs-online.com/web/p/microprocessors/0775442 ; RS UK SiP module — https://uk.rs-online.com/web/p/microprocessors/0775444 ; CNX — https://www.cnx-software.com/2025/04/09/microchip-sama7d65-cortex-a7-mpu-comes-in-soc-and-sip-packages-with-up-to-2gbit-integrated-ddr3l-memory/
37. DigiKey Murata LBEE5KL1DX-883 (USD 8.56 @1k, NRND) — https://www.digikey.com/en/products/detail/murata-electronics/LBEE5KL1DX-883/6043961
38. LCSC MT7612UN C45354764 — https://www.lcsc.com/product-detail/C45354764.html ; MT7601UN C45354765 — https://www.lcsc.com/product-detail/RF-Transceiver-ICs_MTK-MT7601UN_C45354765.html
39. TrendForce consumer DRAM press release (2026-04-07) — https://www.trendforce.com/presscenter/news/20260407-13001.html ; Evertiq — https://evertiq.com/news/2026-04-08-limited-capacity-and-order-shifts-push-consumer-dram-prices-higher ; Wccftech DDR4/DDR3 Q3 2026 — https://wccftech.com/memory-shortages-drive-ddr4-prices-over-50-in-q3-2026-ddr3-also-impacted-by-higher-costs/amp/
40. LCSC W25N02KVZEIR — https://www.lcsc.com/product-detail/C3010298.html ; tape and reel — https://lcsc.com/product-detail/NAND-FLASH_Winbond-Elec-W25N02KVZEIR-TR_C17626844.html
41. RS Alliance AS4C128M16D3LC-12BAN DDR3L 2 Gbit — https://ie.rs-online.com/web/p/sdram/0425280
42. Hubtronics Quectel EC200A-CNTA-D10-UGASA (INR 1,454.24 ex-GST) — https://hubtronics.in/quectel-ec200a-cnta-d10-ugasa
43. Openelab EC200A-EU (no integrated GNSS per spec V1.6; USD 25.68) — https://openelab.io/products/quectel-ec200a-eu-4g-lte-cat4-lcc-module
44. Hubtronics EC200U-CN GNSS (INR 1,785.59 ex-GST) — https://hubtronics.in/wireless-modules/ec200u-cn-4g-gnss-modem
45. Hubtronics Quectel L89HA-S90 (INR 677.12 ex-GST) — https://hubtronics.in/wireless-modules/quectel-l89ha-s90-dual-band-gnss-module ; Mouser India Quectel GNSS (L89-S90 NRND) — https://www.mouser.in/c/rf-wireless/wireless-modules/gnss-gps-modules/?m=Quectel
46. Fibocom L610-IN with IRNSS / NavIC, AIS-140 — https://www.everythingrf.com/news/details/20068-fibocom-unveils-the-first-lte-cat-1-bis-module-with-irnss-and-navic-for-india
47. AIS-140 finalized draft (May 2017), copy — https://trackobit.com/wp-content/uploads/2025/05/AIS-140-regarding-Intelligent-Transportation-Systems.pdf ; official ARAI file (blocked in this run) — https://hmr.araiindia.com/Control/AIS/14201910518PMAIS-140.pdf
48. ISRO / ICG-14 presentation on NavIC in AIS-140 — https://www.unoosa.org/documents/pdf/icg/2019/icg14/20.pdf
49. Vishay SM8S36AHE3 (58.1 V clamp, 114 A, AEC-Q101): DigiKey — https://www.digikey.in/en/products/detail/vishay-general-semiconductor-diodes-division/SM8S36AHE3-A-I/6709964 ; Farnell (EUR 1.74 @1000+) — https://it.farnell.com/en-IT/vishay/sm8s36ahe3-a-i/tvs-diode-aec-q101-6-6kw-36v-do218ab/dp/2765631
50. DoT MTCTE notifications (Router ER TEC37682308, 5G NR exemption 29/11/2023) — https://eservices.dot.gov.in/mtcte?page=2
51. Certification-India, list of 32 products (ERs) under MTCTE Phase III/IV (Router Phase 4; IoT Gateway, Tracking Device, 2.4/5 GHz equipment Phase 3) — https://www.certification-india.com/en/extension-of-mandatory-certification-date-for-32-products-ers-covered-under-phase-lll-iv-of-mtcte
52. TEC IoT Gateway ER sample (TEC24492408, SCS) — https://devzone.nordicsemi.com/cfs-file/__key/communityserver-discussions-components-files/4/TEC24492408_5F00_IoT.pdf
53. Granite River Labs WPC/ETA guide — https://www.graniteriverlabs.com/en-us/market-access-services/country/india/wpc-mark ; DoT ETA page (INR 10,000) — https://eservices.dot.gov.in/equipment-type-approval-eta
54. BIS Scheme-II (CRS) — https://www.bis.gov.in/product-certification/products-under-compulsory-certification/scheme-ii-registration-scheme ; consultant list naming routers (secondary) — https://blogs.seyecs.com/bis-certification-for-electronic-products/
55. RAUC — https://rauc.io/ ; SWUpdate — https://sbabic.github.io/swupdate/ (project homes, not fetched in this run)

Internal: R01 (CRA, RED, MTCTE), R02 (modems, SIM), R06 (power), R09 (Linux SoCs, CIP, SoMs), R10 (market, competitor prices), R11 (PHY, magnetics), R14 (IO, RS-485, power, terminals, PCB, enclosure prices), R15 (EC200A), R16 (RUT200 internals, references).
