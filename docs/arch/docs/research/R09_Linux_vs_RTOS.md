# R09 — Linux vs RTOS (Zephyr / ThreadX) and processor strategy

Status: COMPLETE (first full version 2026-11-14). Items marked UNVERIFIED still need confirmation; datasheet downloads were blocked (see datasheets/linux_soc/INDEX.md).

Scope decisions applied (product-owner update of 2026-11-13):
- Baseboard "brain" = low-cost secure MCU + secure element (owns IO/ADC, routes data, holds keys, power-cycles modules). Linux on the baseboard is a possible later "Pro" variant only.
- Unit (b) = one combined "4G (LTE Cat-1, GSM fallback) + Ethernet + Wi-Fi" module, finished cost <= INR 1,000 (BOM <= ~INR 714; finished cost = BOM x 1.4).
- Wi-Fi + BLE module BOM <= ~INR 430; LoRa module BOM <= ~INR 714.
- Separate Ethernet card dropped; CAN / CAN-FD + RS-485 hosted by the baseboard MCU or a small fieldbus card (undecided — both covered).
- Stackable DIN-rail modules, each in its own enclosure, common 40-pin pass-through bus.

## 1. Executive summary and recommendation

1. **Verdict: MCU + Zephyr is the baseline for every UC product, including the INR 1,000 "4G + Ethernet + Wi-Fi" module. Linux is justified only for a later "Pro" baseboard (or Pro add-on module) on the same 40-pin bus.**
2. Linux does not fit the combined module: the cheapest credible Linux silicon (MT7628 router module, INR ~740–800 retail) alone exceeds the INR ~714 BOM before adding a Cat-1 modem; an ST/NXP Linux core (SoC + DDR + PMIC + flash) is ~INR 1,200–1,700 (estimate) and pushes the finished module to ~INR 3,800–4,500 (section 6).
3. OpenLinux LTE modules (Quectel EC25 / SIMCom SIM7600, MDM9607) run a vendor Linux 3.18 kernel (EOL upstream for years) and cost ~INR 2,900 at 1k - unacceptable under the CRA support-period obligations and the budget. Use LTE modules as AT/PPP modems only (section 5).
4. CRA makes Linux expensive to own: >= 5-year support period, updates kept available >= 10 years, SBOM; the Linux kernel now issues ~50–90 CVEs/week. Only CIP SLTS 6.12 (to mid-2035) covers a 2027 launch + 8 years; vendor BSP kernels do not (sections 3.1, 8).
5. Zephyr has a real but much smaller CVE stream (network/BLE stacks), Apache-2.0 licence, MCUboot + TF-M upstream, but no safety certificate yet (IEC 61508 work in progress). Only Zephyr 3.7 is an LTS today (to 07/2029); plan to move to 4.6 LTS (target 04/2027) before freeze.
6. ThreadX (MIT) is a credible second choice only on ST (STM32CubeH5/U5 bundle ThreadX; ST bulletin SB0067 still patches it) and NXP i.MX RT (MCUXpresso Azure RTOS delivery); it is **not** viable on Nordic, Espressif or RW612 radios. Safety certificates are Microsoft-era (6.1.x); transfer to Eclipse not verified.
7. **Baseboard brain:** STM32H573 (TrustZone, TF-M `/ns` target upstream, FDCAN, Ethernet MAC, HASH/RNG) keeps both Zephyr and ThreadX open; NXP MCX N947 is the Zephyr-only-verified alternative. STM32G0B1 (M0+) is too small for TF-M/A-B OTA as the brain but suits a cheap fieldbus card.
8. **Combined module:** Zephyr on an MCU host (e.g. STM32H5 with Ethernet MAC, or RW612 with Ethernet + Wi-Fi 6 on-chip) driving a Cat-1 modem via `modem_cellular` (PPP/CMUX). RW612 removes a chip but is Zephyr/FreeRTOS only.
9. **Linux "Pro" core, if built:** lowest-cost credible = **STM32MP131/MP133** (USD 3.85–4.43 @1k; 2x GbE on MP133/135, 2x FDCAN, secure boot, tamper, OP-TEE; ThreadX or Zephyr also run on its A7; 10-year rolling longevity). Chip-down core ~INR 1,200–1,700; or MYiR MYC-YF135 SoM (USD 16–29) / Toradex OSM i.MX 91 (USD 25.55 volume) to avoid DDR/BGA layout. i.MX 91 is the NXP choice (15-year longevity, EdgeLock enclave) at ~USD 8–9.
10. Firmware sizing rule for every MCU: >= 2x (application slot) + MCUboot (32–64 KB) + TF-M (~100–250 KB if used) + settings/storage; i.e. 1 MB internal flash minimum for a TF-M + A/B node, 2 MB for the baseboard, or external QSPI/OSPI flash for the secondary slot (section 9).
11. Key open items: India 1k pricing for MP13x/i.MX 91 and DDR (DRAM prices volatile, UNVERIFIED); ThreadX safety certificate status; Zephyr 4.6 LTS timing; whether fieldbus lives on the baseboard MCU or a G0B1 card.

## 2. Scored decision matrix

Scores 1 (poor) – 5 (best) for the UC context; weights reflect the brief (cost, security/CRA, manufacturability first). Scores are the author's judgement based on the sourced facts in sections 3–9.

### 2a. Combined "4G + Ethernet + Wi-Fi" module (BOM <= INR 714) and baseboard brain

| Criterion (weight) | MCU + Zephyr | MCU + ThreadX | Linux on MT7628 (OpenWrt) | Linux on STM32MP13 / i.MX 91 (Yocto/Buildroot) | OpenLinux LTE module |
|---|---|---|---|---|---|
| BOM cost vs target (20) | 5 | 5 | 2 | 1 | 1 |
| Security / CRA maintainability (20) | 4 | 3 | 2 (no HW root of trust, old SoC) | 3 (strong HW, heavy patch load) | 1 (3.18 kernel) |
| Manufacturability / PCB (10) | 5 (QFN/LQFP, 4-layer) | 5 | 3 (module) | 2 chip-down / 4 SoM | 4 (LGA module) |
| Capabilities (VPN, web UI, containers, Python) (10) | 2 | 2 | 4 | 5 | 2 |
| Power / battery / boot time (10) | 5 | 5 | 2 | 2 | 3 |
| Determinism / safety path (5) | 4 | 4 (cert. legacy) | 1 | 2 | 1 |
| Vendor / radio driver coverage (10) | 5 | 2 (no Nordic/ESP/RW612) | 3 | 4 | 2 |
| Dev effort & talent (India) (5) | 3 | 3 | 4 | 4 | 2 |
| Licensing (5) | 5 (Apache-2.0) | 5 (MIT) | 3 (GPL obligations) | 3 (GPL) | 2 (GPL + vendor NDA SDK) |
| Longevity (5) | 4 | 3 | 2 | 5 (10–15 yr programmes) | 2 |
| **Weighted total (/500)** | **430** | **375** | **250** | **280** | **185** |

### 2b. Future "Pro" baseboard (budget open, needs edge apps)

Linux on STM32MP13 / i.MX 91 wins (capabilities 5, longevity 5, cost acceptable at Pro price point); keep a Zephyr MCU (the same secure MCU + secure element) for IO/ADC and module power control so that the Linux side is never safety- or real-time-critical.

## 3. Linux vs Zephyr vs ThreadX — comparison

### 3.1 Maintenance and regulatory facts (sourced)

- **Kernel.org LTS** (as of 2026-11): 6.18 (EOL Dec 2028), 6.12 (Dec 2028), 6.6 (Dec 2027), 6.1 (Dec 2027), 5.15 and 5.10 (Dec 2026). New LTS kernels start with a ~2-year projected window, extendable; dates "not set in stone" [S48].
- **CIP SLTS** (Linux Foundation Civil Infrastructure Platform): 10-year maintenance - linux-4.4-cip to 2027, 4.19-cip to 2029, 5.10-cip to 2031, 6.1-cip to 2033, 6.12-cip to mid-2035 (first release 2025-05-20). CIP maintains a subset of architectures / reference hardware only; SoC-specific drivers outside CIP reference boards are the integrator's (or vendor's) burden [S49][S50]. Which ST/NXP SoCs are CIP reference hardware: UNVERIFIED.
- **Linux kernel CVE volume**: the kernel became its own CNA in 2024 and issued ~4,300–4,450 CVEs in 2024; ~50/week in 2025 and ~2,300 in H1-2026 (~88/week); per-release fix counts >1,000 since Linux 7.0 (secondary sources) [S51][S52]. A Linux product therefore needs automated CVE triage against its SBOM; manual review does not scale.
- **Zephyr CVE volume**: tens of CVEs per year, concentrated in network/BLE stacks (section 8) [S3] - orders of magnitude smaller, but non-zero.
- **EU CRA (Reg. 2024/2847)**: support period "shall be at least five years" (Art. 13(8)), longer if the product's expected use is longer; each security update must remain available for a minimum of 10 years or the rest of the support period, whichever is longer (Art. 13(9)) [S53]. Annex I Part II(1): SBOM in a commonly used machine-readable format covering at least top-level dependencies (not public, on request of authorities) [S54]. Reporting obligations apply from 2026-09-11; main obligations from 2027-12-11 [S13].
### 3.2 Qualitative comparison

| Aspect | Embedded Linux (Yocto / Buildroot / OpenWrt / Debian) | Zephyr | Eclipse ThreadX |
|---|---|---|---|
| Containers, Node-RED, Python, OPC UA servers, SQL DBs, full VPN/firewall/routing, web UI | Yes (standard packages) | No containers/Python/Node-RED; OPC UA only via third-party stacks (UNVERIFIED); WireGuard present in 4.4 (CVE-2026-10666 shows it exists) [S5]; basic HTTP server | NetX Duo TCP/IP, web server/MQTT add-ons; no containers |
| Remote management / OTA | RAUC / SWUpdate / Mender (A/B rootfs) - mature (not separately sourced here) | MCUboot A/B + mcumgr/SMP, hawkBit client | vendor or custom bootloader; MCUboot can be used |
| Secure boot chain | ROM -> TF-A/OP-TEE -> U-Boot -> FIT -> dm-verity; ST/NXP provide it (ST OP-TEE wiki [S30]) | ROM/TF-M -> MCUboot (signed images) | depends on vendor (ST SBSFU / MCUboot) |
| CVE volume | very high (~50–90 kernel CVEs/week) [S51][S52] | low tens/year [S3] | low; ST had to issue SB0067 for ThreadX vulnerabilities in 2026 [S56] |
| Licence | GPL-2.0 kernel, mixed userspace (source-offer obligations) | Apache-2.0 (FAQ/standard, not re-sourced) | MIT [S8] |
| Determinism / safety | PREEMPT_RT possible; no practical certification route | no certificate yet, IEC 61508 concept approval [S6][S7] | legacy SIL 4 / ASIL D certificates (6.1.x) [S9][S10] |
| Boot time / power | seconds; DDR self-refresh, tens–hundreds of mW (typical, not sourced) | ms; µA sleep | ms; µA sleep |
| Hardware | BGA SoC + DDR + PMIC + eMMC/NAND; 4–6 layer with DDR routing | QFN/LQFP MCU, 4-layer | same as Zephyr |

- **Consequence for OS choice**: the support period is likely 5–10 years for industrial gear. A Linux image must be rebased onto a kernel that is still maintained for that whole period (CIP SLTS 6.12 to 2035 is the only option covering a 2027 launch + 8 years) or the manufacturer back-ports fixes itself. Vendor BSP kernels (ST OpenSTLinux, NXP LF) follow the vendor's yearly release, not 10-year SLTS (UNVERIFIED per vendor; see section 4).

## 4. Linux-capable processors, SiPs and SoMs (ST / NXP)

FX rate used in this report: **USD 1 = INR 94.0** (mid-market 93.93 on 2026-11-08; PTI reports 93.74–94.86 in 2026-11-02..09) [S17][S18]. EUR prices converted at EUR 1 = USD ~1.10 (UNVERIFIED rate, used only for rough orientation).

Price findings (distributor web listings, search snapshots 2026-11-14, ex-tax, ex-shipping):

| Part | Distributor / tier | Price | INR @94 | Source |
|---|---|---|---|---|
| STM32MP131AAG3 (MP131, 650 MHz, TFBGA289 9x9) | ST eStore, 1000–10000 tier | USD 3.85 | 362 | [S19] |
| STM32MP131AAG3 | DigiKey, 1,000 pcs | USD 3.98 | 374 | [S20] |
| STM32MP131DAG7 (1 GHz) | DigiKey, 1,000 pcs | USD 4.43 | 417 | [S20] |
| STM32MP135DAG7 (MP135, 1 GHz) | Farnell, 250+ | USD 6.12 (1k tier not shown) | ~575 | [S21] |
| STM32MP215FAM3 (MP21x) | DigiKey, qty 1 | USD 16.44 (1k UNVERIFIED) | 1,545 (qty 1) | [S22] |
| MIMX9131CVVXJAB (i.MX 91, 11x11 BGA) | Avnet, 704+ tier | USD 8.82 | 829 | [S23] |
| MIMX9131DVVXJAA (i.MX 91) | Avnet, 880+ tier | USD 8.03 | 755 | [S23] |
| MIMX9352CVVXMAC (i.MX 93, 11x11 LFBGA306) | DigiKey, 528 tier | USD 14.94 | 1,404 | [S24] |
| MCIMX6Y2CVM05AB (i.MX 6ULL, 528 MHz, MAPBGA289 14x14) | DigiKey MX, 608 tier | USD 8.98 | 844 | [S25] |

Feature findings (batch 2):
- STM32MP135: 2x Gigabit Ethernet ports, 2x FDCAN, USB 2.0 HS host with HS PHY (2x HS host option), 16-bit LPDDR2/LPDDR3/DDR3/DDR3L up to 533 MHz, max 1 GB; secure boot, TrustZone peripherals, 12 tamper pins incl. 5 active tampers [S26]. The STM32MP135F-DK reference uses the STPMIC1 PMIC + 4 Gbit DDR3L in a TFBGA320 package [S27]. MP131 = single Ethernet, MP133 adds CAN-FD + 2nd Ethernet, MP135 adds display/camera (ST product line split; detailed per-line counts UNVERIFIED in this run - datasheet download blocked).
- STM32MP13 longevity: 10-year programme started March 2023, renewed every year (ST staff answer + ST presentation) [S28][S29].
- STM32MP13 RTOS on the same device: STM32CubeMP13 package supports bare-metal or RTOS on the Cortex-A7 with Azure RTOS / Eclipse ThreadX pre-integrated; OP-TEE supported in OpenSTLinux (STM32MP13 OP-TEE overview) [S29][S30].
- i.MX 91: 1x Cortex-A55 up to 1.4 GHz, LPDDR4 (inline ECC) - DDR4 not mentioned; 2x Gigabit Ethernet (one TSN), 2x USB 2.0, 2x CAN-FD, 8x LPUART; EdgeLock Secure Enclave (lifecycle, tamper detection, secure boot); 11x11 mm and 9x9 mm FCBGA, both 0.5 mm pitch; 11x11 is pin-compatible with i.MX 93 11x11; no Cortex-M core [S31][S32].
- i.MX 93: 2x Cortex-A55 + 1x Cortex-M33 (+ NPU), EdgeLock Secure Enclave [S14]. Zephyr upstream supports both the M33 (`imx93_evk/mimx9352/m33`) and the A55 (`imx93_evk/mimx9352/a55`, booted from U-Boot); also Variscite VAR-SOM-MX93 / DART-MX93 and FRDM-i.MX93 boards [S33].
- NXP i.MX 91 longevity: 15 years (NXP blog) [S15].

SoM / SiP findings (batch 3):

| SoM / SiP | SoC | Memory | Price | Source |
|---|---|---|---|---|
| MYiR MYC-YF135-256N256D-100-I | STM32MP135 | 256 MB DDR3L + 256 MB NAND (4 GB eMMC option), 32 kbit EEPROM | DigiKey MX qty 1 USD 29.00 (other DigiKey regions ~USD 16–21; launch headline "USD 19") | [S34] |
| Variscite DART-MX91 / VAR-SOM-MX91 | i.MX 91 | config-dependent | "starting from" USD 35 / 34 (other snapshots USD 55 / 54); volume | [S35] |
| Variscite DART-MX93 | i.MX 93 | config-dependent | "starting from" USD 39 (alpha, production qty) / 59 | [S35] |
| Toradex OSM (solder-down, 30x30 mm) | i.MX 91 / i.MX 93 | config-dependent | USD 25.55 / 28.20 in volume (2026 launch) | [S36] |
| Toradex Lino (B2B) | i.MX 91 / i.MX 93 | config-dependent | USD 30.65 / 33.35 large orders | [S36] |
| Octavo OSD32MP2 | STM32MP25 + DDR4 + EEPROM + passives, 21x21 mm SiP; OSD32MP2-PM 9x14 mm variant | - | price not found (UNVERIFIED) | [S37] |
| Octavo OSD32MP157C-512M-BAA | STM32MP157 + DDR3 + PMIC | 512 MB | reseller qty 1 ~USD 62 (indicative only) | [S38] |

- STM32MP25: Zephyr supports only the Cortex-M33 (`stm32mp257f_ev1/stm32mp257fxx/m33`, 400 MHz); the Cortex-A35 side is not supported in Zephyr and Linux on the A35 must set up the M33 first [S39]. Family-level 10-year rolling longevity (DigiKey highlight; ST table not checked) [S40].

Notes: i.MX 91 lead times quoted at 16 weeks (DigiKey) and a 182-week factory lead time on one Avnet listing; MIMX9131CVVXJAA marked obsolete at DigiKey (replaced by the -JAB suffix) [S23]. STM32MP215 is listed as "Design Win"/new on some ST pages, i.e. early in availability; core count for MP215 is conflicting between listings (UNVERIFIED) [S22].

### 4.x Recommendation and core BOM estimate (Linux "Pro" variant)

Lowest-cost credible Linux core: **STM32MP131/MP133** (MP133 if two Ethernet ports + CAN-FD are needed on the Linux side; MP131 if the Zephyr MCU keeps fieldbus). Reasons: USD 3.85–4.43 @1k [S19][S20], secure boot + tamper + OP-TEE [S26][S30], ThreadX (STM32CubeMP13) and upstream Zephyr (`stm32mp135f_dk`, Ethernet/PTP/UART/SPI) on the same A7 [S29][S55], 10-year rolling longevity [S28]. NXP alternative: i.MX 91 (~USD 8–9, EdgeLock secure enclave, 2x GbE, 2x CAN-FD, 15-year longevity, LPDDR4 only) [S15][S23][S31].

| Core item | Estimate | INR @94 | Status |
|---|---|---|---|
| STM32MP131/133 | USD 3.9–4.5 (MP133 1k price not found) | 365–425 | MP131 sourced; MP133 UNVERIFIED |
| DDR3L 4 Gbit x16 | USD 3–6 | 280–560 | UNVERIFIED (not priced in this run; DRAM market volatile) |
| PMIC (STPMIC1) or discrete bucks/LDOs | USD 1.5–3 | 140–280 | UNVERIFIED |
| SPI-NAND 256 MB / eMMC 4 GB | USD 2–4 | 190–375 | UNVERIFIED |
| Crystals, passives, extra 2 layers (6-layer vs 4) | USD 2–3 | 190–280 | estimate |
| **Total chip-down core** | **USD 12.5–20** | **~1,200–1,900** | estimate |
| Alternative: MYiR MYC-YF135 SoM (MP135 + 256 MB + 256 MB NAND) | USD 16–29 qty 1 | 1,500–2,700 | sourced [S34] |
| Alternative: Toradex OSM i.MX 91 (solder-down) | USD 25.55 volume | 2,400 | sourced [S36] |

PCB: the chip-down route means a BGA (0.5 mm pitch for MP13 TFBGA 9x9 and i.MX 91; 0.8 mm LFBGA 14x14 also offered for MP13 - pitch UNVERIFIED from datasheet) plus DDR length matching; a solder-down SoM (Toradex OSM, MYiR stamp-hole) keeps the carrier at 4 layers. For a low-volume Pro variant the SoM route is recommended.

Datasheets: direct downloads from st.com (HTTP/2 stream error, then timeout) and nxp.com (404 "page not available") were blocked from this environment, so no SoC datasheet PDFs were saved (see datasheets/linux_soc/INDEX.md).

## 5. Ultra-low-cost Linux: router SoCs and OpenLinux LTE modules

| Part | Type | Price (date, distributor) | INR @94 | Linux / OpenWrt status | Source |
|---|---|---|---|---|---|
| MediaTek MT7628NN | MIPS 24KEc 580 MHz router SoC, 2.4 GHz 2x2 802.11n, 5-port 10/100 switch (DRQFN-156) | LCSC 100+ USD 2.26 (1+ USD 2.39) | 212 | OpenWrt target ramips/mt76x8, built in 25.12.x releases (25.12.3, May 2026) | [S41][S43] |
| Hi-Link HLK-7628N module | MT7628NN + 128 MB DDR2 + 32 MB SPI NOR, stamp-hole module | LCSC 1+ USD 7.9–8.5 (one snapshot USD 21) | 740–800 | Vendor states Linux/OpenWrt support; third-party wiki "Supported" | [S42] |
| Quectel EC25-E (EC25EUXGR) | LTE Cat 4, Qualcomm MDM9607 (Cortex-A7), QuecOpen/OpenLinux option | Arrow 1000+ USD 31.37 (14-week lead time) | 2,949 | QuecOpen SDK = Linux 3.18 (GCC 4.9, Ubuntu 12.04/14 host, 2017 presentation; devices boot 3.18.20). SDK not public; obtained via sales/FAE. No upstream MDM9607 support in mainline (community 5.11 port exists only for PinePhone modem) | [S44][S45][S46] |
| Quectel EG25-G | LTE Cat 4, MDM9607 | retail ~USD 98–102 (qty 1, mPCIe/LGA) | ~9,300 | same platform as EC25 | [S46] |
| SIMCom SIM7600 series | LTE Cat 1/Cat 4, MDM9607, "Open Linux" | not researched (similar class to EC25) | - | SIMCom Open Linux guide references mdm9607.dtsi; kernel version not stated in public docs; community reports "3.18.120 (mdm9607)" (UNVERIFIED) | [S47] |

Key points:
- MT7628 class is the only Linux SoC that fits the INR 714 module budget on silicon cost (chip ~INR 212, module ~INR 740–800 retail incl. DDR2 + NOR). But: MIPS 24K, no TrustZone/secure enclave, no hardware secure boot, 2.4 GHz Wi-Fi 4 only, no LTE (needs a separate Cat-1 modem), 10/100 Ethernet; MT7628 is a 2014-era part with no published longevity programme (UNVERIFIED). OpenWrt itself is maintained (25.12 series), but 8 MB flash / 64 MB RAM devices are flagged as "limited" for extra packages (unofficial warning page) [S43].
- OpenLinux LTE modules (EC25/SIM7600) run a vendor 3.18 kernel. Linux 3.18 reached end-of-life in 2017 on kernel.org (see section 3 sources). Under the CRA the manufacturer must handle vulnerabilities for the whole support period (>= 5 years typically) - shipping a 3.18-based application processor exposed to the network is effectively unsupportable unless the vendor backports fixes; Quectel/SIMCom publish no such kernel security SLA (none found: UNVERIFIED). Price (~INR 2,900 at 1k for EC25) is also ~4x the module BOM.
- Practical conclusion: use LTE modules as modems (AT/PPP/CMUX or USB ECM) under an MCU host; do not put customer application code into the modem's Linux.

## 6. Is Linux feasible on the INR 1,000 "4G + Ethernet + Wi-Fi" module?

**No.** Indicative BOMs (INR, @94/USD; modem and Wi-Fi prices are retail/qty-1 figures from R02/R03, not 1k quotes):

| Block | MCU + Zephyr | Linux, MT7628 (OpenWrt) | Linux, STM32MP13 chip-down |
|---|---|---|---|
| Compute + Wi-Fi | RW612 (Wi-Fi 6 + BLE + Ethernet MAC) or MCU + ESP32-C6 module (~433 qty 1 [R03]) | HLK-7628N module 740–800 (Wi-Fi 4 + 10/100 switch + DDR2 + NOR) [S42] | core 1,200–1,900 (section 4) + Wi-Fi 300–430 |
| LTE Cat-1 modem | A7672S-class ~700 (IndiaMART, retail) [R02] | same ~700 | same ~700 |
| Ethernet PHY + magnetics/RJ45 | ~100–200 (UNVERIFIED) | in SoC (PHY) + magnetics | PHY + magnetics |
| Power, connector, enclosure-side parts | ~150–250 (UNVERIFIED) | same | same + PMIC |
| **BOM** | **~1,000–1,400 at retail; must fall to <= 714 at 1k volume** | **~1,750–2,000** | **~2,600–3,400** |
| Finished (x1.4) | ~1,400–1,950 retail-priced; target 1,000 needs volume pricing | ~2,450–2,800 | ~3,600–4,800 |

Observations:
- Even the MCU option only meets INR 1,000 finished if the Cat-1 modem is bought well below its retail INR ~700 (check R02 for 1k quotes). Linux adds INR 750–2,000 of BOM on top and cannot meet the target.
- MT7628 is also a poor CRA fit: no hardware root of trust / secure boot, 2014-era MIPS core, no longevity commitment found [S41][S42].
- A realistic Linux variant of this module (e.g. "Pro router" with i.MX 91 / MP13 SoM) would be a separate SKU at roughly INR 3,500–5,000 finished.

## 7. RTOS support matrix (Zephyr / ThreadX per MCU)

Method: Zephyr upstream `main` was inspected directly (sparse clone of github.com/zephyrproject-rtos/zephyr, commit 7cd4b562b30a, 2026-11-13, VERSION 4.5.99 = 4.6 development) [S55]. "Y" = a devicetree node with an in-tree driver binding exists for the SoC and an upstream board exists; "-" = no node / no on-chip peripheral; "(sw)" = software only. Presence of a DT node proves upstream driver support, not production maturity. Board names are the upstream Zephyr board directories.

| MCU | Zephyr board(s) upstream | UART/SPI/I2C/ADC | CAN-FD | Ethernet | Wireless | USB | Crypto HW in Zephyr | TF-M (`/ns` target) | ThreadX from vendor |
|---|---|---|---|---|---|---|---|---|---|
| STM32H563 / H573 | nucleo_h563zi, stm32h573i_dk | Y | Y (st,stm32-fdcan) | Y (st,stm32h5-ethernet) | - | Y (st,stm32-usb FS) | HASH, RNG (no AES/PKA node) | H573: Y (stm32h573i_dk/ns); H563: no ns target | STM32CubeH5 includes ThreadX/NetX Duo (see 8) |
| STM32H533 | nucleo_h533re | Y | Y | - (no MAC on H533) | - | Y | RNG/HASH inherited (UNVERIFIED for AES) | no ns target | as H5 |
| STM32U5 (U575/U585) | b_u585i_iot02a, nucleo_u575zi_q, ... | Y | Y | - | - | Y | HASH, RNG | U585: Y (b_u585i_iot02a/ns) | STM32CubeU5 includes ThreadX |
| STM32WLE5 | nucleo_wl55jc (WL55), seeed LoRa-E5 boards (WLE5) | Y | - | - | LoRa: st,stm32wl-subghz-radio (sx126x driver) + LoRaWAN (loramac-node / LoRa Basics Modem in drivers/lora) | - | AES, RNG | - | STM32CubeWL: ThreadX not standard (UNVERIFIED) |
| STM32G0B1 | nucleo_g0b1re | Y | Y (2x FDCAN) | - | - | Y (FS + UCPD) | - (G0B1 has no AES; G0C1 does) | - (M0+, no TrustZone) | STM32CubeG0 ThreadX: UNVERIFIED |
| NXP MCX N947 | frdm_mcxn947 (cpu0/cpu1, cpu0/ns) | Y | Y (nxp,flexcan-fd) | Y (nxp,enet-qos) | - | Y (HS EHCI + FS) | ELS + ELS-TRNG | Y (frdm_mcxn947/.../cpu0/ns) | MCUXpresso: UNVERIFIED (see 8) |
| NXP MCX N236 | frdm_mcxn236 (+ns) | Y | Y | - | - | Y | ELS | Y | as above |
| NXP RW612 | frdm_rw612, rd_rw612_bga | Y (flexcomm) | - | Y (nxp,enet 10/100 RMII) | Wi-Fi 6 (nxp,wifi), BLE (nxp,hci-ble), 802.15.4 (HDLC RCP) | Y (EHCI) | TRNG (ELS/PKC not exposed as DT node) | no ns target | n/a |
| NXP i.MX RT1060 | mimxrt1060_evk, mimxrt1064_evk | Y | Y (FlexCAN3 FD) | Y (nxp,enet + PTP) | - | Y (EHCI) | DCP, TRNG | - (M7, no TrustZone-M) | MCUXpresso SDK historically shipped Azure RTOS for RT10xx (current status UNVERIFIED) |
| Nordic nRF54L15 | nrf54l15dk (+ns, FLPR RISC-V core) | Y | - | - | BLE (SW-split LL), 802.15.4 | - | CRACEN (PSA crypto RNG) | Y (nrf54l15dk/.../cpuapp/ns; TF-M nordic platform present) | none (Nordic does not ship ThreadX) |
| Nordic nRF5340 | nrf5340dk (app + net core, +ns) | Y | - | - | BLE, 802.15.4 | Y | CryptoCell-312 | Y | none |
| Nordic nRF52840 | nrf52840dk, dongle | Y | - | - | BLE, 802.15.4 | Y | CryptoCell-310 | - (M4) | none |
| Nordic nRF9151 | nrf9151dk (+ns) | Y | - | - | LTE-M/NB-IoT modem: modem library is in nRF Connect SDK, NOT upstream Zephyr | - | CryptoCell-310, KMU | Y | none |
| Nordic nRF7002 | nrf7002dk (companion IC) | n/a | - | - | Wi-Fi 6 driver upstream (drivers/wifi/nrf_wifi) | - | - | n/a | none |
| Espressif ESP32-C6 | esp32c6_devkitc (hpcore, lpcore) | Y | classic CAN only (TWAI), not FD | - (no MAC) | Wi-Fi (espressif,esp32-wifi, binary blobs), BLE HCI, 802.15.4 | USB-serial/JTAG only | AES, SHA, TRNG | - (RISC-V, no TF-M) | none |
| STM32MP13 (Cortex-A7, for reference) | stm32mp135f_dk | uart, spi (adc not listed) | FDCAN node present | Y (twister lists netif:eth, ptp) | - | - | HASH | - | STM32CubeMP13 ships ThreadX (section 4) |
| STM32MP2 (M33 only) | stm32mp257f_ev1, stm32mp257f_dk, stm32mp215f_dk (m33 targets) | uart/spi/i2c | - | - | - | - | - | - | n/a |
| i.MX 91 / 93 | imx91_evk, frdm_imx91, imx93_evk (A55 + M33), frdm_imx93 | Y | - | - | - | - | - | - | n/a |

Other in-tree pieces relevant to the UC (same commit [S55]): CAN drivers `can_stm32_fdcan`, `can_mcux_flexcan`, `can_mcan`, `can_mcp251xfd` (external CAN-FD controller via SPI), `can_esp32_twai/twaifd`; Ethernet drivers `eth_stm32_hal_v2`, `eth_nxp_enet`, `eth_nxp_enet_qos`, `eth_dm9051`, `eth_enc28j60`, `eth_lan865x` (10BASE-T1S), `wiznet/` (W5500 class) - so Ethernet can be added to MAC-less MCUs over SPI; Wi-Fi drivers `nrf_wifi`, `nxp`, `esp32`, `esp_hosted`, `esp_at`, `st67w611m1` (ST's ST67W Wi-Fi module); cellular `modem_cellular` (+ `cellular_nordic_nrf91_slm` for an nRF91 running Serial Modem as an external modem).

Conclusions on "Zephyr first, ThreadX second":
- Viable for both RTOSes: STM32H5, STM32U5, (likely) STM32G0/WL via STM32Cube ThreadX packages; NXP i.MX RT1060 (if NXP still ships Azure/ThreadX in MCUXpresso - UNVERIFIED).
- Zephyr-only in practice: all Nordic parts (nRF Connect SDK is Zephyr-based; no vendor ThreadX), ESP32-C6 (ESP-IDF is FreeRTOS-based; Zephyr port by Espressif; no ThreadX), RW612 (Wi-Fi/BLE firmware integration exists for Zephyr and FreeRTOS in MCUXpresso; ThreadX would need a custom port of the Wi-Fi driver), nRF9151 (needs nRF Connect SDK, not just upstream Zephyr).
- Best "both" candidate for the baseboard brain: STM32H573 (TrustZone + TF-M upstream, CAN-FD, Ethernet MAC, crypto) or STM32U585 (no Ethernet); MCX N947 is the NXP equivalent on Zephyr (TF-M ns target present), ThreadX status on MCX unverified.

## 8. Zephyr and ThreadX: LTS, security process, safety certification, licences, vendor-SDK alignment

(Findings so far, as of 2026-11-14; sources in section 11.)

**Zephyr releases / LTS**
- LTS cadence 2.5-3 years, each LTS maintained ~5 years; non-LTS releases are supported ~12 months [S1][S2].
- Only LTS currently supported is 3.7 (support to 07/2029). 4.4 (released 2026-04-14) is NOT an LTS (support to 04/2027); 4.5 released 2026-10 (support 12 months); 4.6 is planned as the next LTS, targeted April 2027 [S2]. Implication: a product frozen today must either use 3.7 LTS (older; some newer SoCs such as nRF54L / MCX N / RW612 may need backports or vendor forks, UNVERIFIED per-SoC) or plan to move to 4.6 LTS in 2027.
- Security: Zephyr is a CVE Numbering Authority; the vulnerability list is public [S3]. Many 2026 CVEs hit the 4.4 network stack (ICMPv4/v6, TCP use-after-free, HTTP server path traversal, WireGuard heap overflow CVE-2026-10666, DTLS CID out-of-bounds write CVE-2026-8718); some third-party aggregators say fixes land in 4.5 only, i.e. not all fixes are in every maintained branch (UNVERIFIED, aggregator sources [S4][S5]). Take-away: a Zephyr device exposed to the internet carries real network-stack CVE volume and needs a patch-and-OTA pipeline for the whole support period.

**Zephyr safety certification**
- NOT certified as of 2026-11. Project holds written concept approval for IEC 61508 (SIL 3 / SC 3, Route 3S, limited kernel scope); roadmap presented at Embedded World 2026; the earlier target of end-2023 slipped. No certificate found [S6][S7].

**Eclipse ThreadX**
- Eclipse ThreadX (MIT licence) quarterly releases since Sept 2025, current line 6.5.x; "no LTS branches"; best-effort fixes; confirmed vulnerabilities fixed in next quarterly release or hotfix, goal within 3 months [S8].
- Safety: SGS-TUV Saar certificates (IEC 61508 SIL 4, IEC 62304 Class C, ISO 26262 ASIL D, EN 50128) were issued for Microsoft-era Azure RTOS 6.1.x; Eclipse says the certificate/safety manual are available under licence via the ThreadX Alliance. Transfer of the certificates to Eclipse was still "in process" in 2024 mailing-list replies; completion NOT verified [S9][S10].
- STM32Cube: ST still ships ThreadX as X-CUBE-AZRTOS-xx packages; community report (Apr 2025) that some packages lag upstream (F7 on 6.1.10) while Eclipse only supports 6.4.x+; one 2026 secondary article says H7/H7RS packages were updated mid-2026 while L5/WB/G4 were last updated 2023 (UNVERIFIED) [S11][S12].

**ThreadX in vendor SDKs (2026 status)**
- ST: ThreadX is integrated in STM32CubeH5 and STM32CubeU5 (ThreadX, NetX Duo, FileX/LevelX, USBX); a July 2026 ST moderator reply says ThreadX/FileX are selectable directly in STM32CubeMX for H5 (X-CUBE-AZRTOS-H5 not needed). Eclipse 6.4.x appears only as beta in ST's H5 Eclipse-middleware app repo. ST security bulletin SB0067 (April 2026) says Eclipse ThreadX vulnerabilities apply to STM32Cube packages and advises updating the component from Eclipse's GitHub. A 2025 forum rumour of ST dropping ThreadX for FreeRTOS is unconfirmed [S56][S57].
- NXP: Azure RTOS (ThreadX, NetX Duo, FileX, USBX, LevelX, GUIX) delivered in MCUXpresso SDK since 2.8.5 for i.MX RT1050/1060/1064 via the NXP azure-rtos GitHub repo; current status for MCX N and RW612 not found (UNVERIFIED) [S58].
- Nordic: nRF Connect SDK is Zephyr-based (Zephyr fork + nrfxlib); no ThreadX. Espressif: ESP-IDF is FreeRTOS-based; Espressif maintains Zephyr support (esp32c6_devkitc upstream, binary blobs); no ThreadX (R03 / [S55]).
- Licences: Zephyr Apache-2.0 (project licence - not re-fetched in this run), ThreadX MIT [S8], Linux kernel GPL-2.0.

## 9. Firmware building blocks that drive hardware sizing

| Block | Size / requirement | Source / status |
|---|---|---|
| MCUboot | 32–64 KB boot partition typical (Zephyr board partition tables) | UNVERIFIED as a range; check per board DTS partitions |
| A/B (swap/overwrite) slots | 2 x application image + scratch/swap sector; for 384 KB app => ~800 KB | rule of thumb |
| TF-M | ~100 KB flash / ~60 KB RAM (Profile Medium, Musca-B1 build) up to ~190–255 KB flash in Zephyr/nRF builds | [S59] (forum/mailing-list data, indicative) |
| Settings / NVS / secure storage (ITS/PS) | 16–64 KB | estimate |
| Network stack + TLS (mbedTLS/PSA) | 100–200 KB flash, 40–80 KB RAM for one TLS session | estimate (UNVERIFIED) |

Sizing rules:
1. Baseboard brain (TF-M + Ethernet/TLS + A/B + fieldbus): >= 2 MB flash, >= 640 KB RAM (STM32H563/H573 class: 2 MB / 640 KB; MCX N947: 2 MB / 512 KB - datasheet values from knowledge, UNVERIFIED in this run), or 1 MB internal + 8–16 MB external QSPI/OSPI flash for the secondary slot and logs.
2. Radio modules (Wi-Fi/BLE, LoRa): >= 1 MB flash for MCUboot A/B without TF-M; STM32WLE5 (256 KB) only fits single-slot + small app or needs external SPI flash for the update slot.
3. STM32G0B1 (M0+, no TrustZone): fieldbus card only; MCUboot possible, no TF-M; keys stay on the baseboard secure element.
4. Debug: SWD on every module via a Tag-Connect / pads; disable or lock debug in production (RDP/ debug authentication on H5/U5, APPROTECT on Nordic, ELS lifecycle on MCX) - CRA/EN 18031 expects closed debug interfaces (not separately sourced here).
5. Provide a secure element (or TF-M ITS + HUK) for device identity; Wi-Fi/LoRa modules should not hold long-term fleet keys if the baseboard owns them.

## 10. Risks and open decisions

Risks:
- Zephyr LTS gap: only 3.7 LTS (to 07/2029) today; newer SoCs (nRF54L, MCX N, RW612, H5 features) are better in 4.x; 4.6 LTS targeted 04/2027 [S2]. Decision: develop on 4.5/main, freeze on 4.6 LTS.
- Zephyr network-stack CVEs (2026) - need OTA and CVE monitoring pipeline from day one [S3][S4].
- ThreadX: no LTS branches, best-effort fixes, safety certificate transfer unverified [S8][S9]; vendor packages lag upstream [S11][S56].
- DRAM / BGA supply and price volatility for any Linux variant (prices UNVERIFIED in this run).
- i.MX 91 long factory lead time on one listing (182 weeks) [S23].
- CRA vulnerability handling obligations apply from 2027-12-11, reporting from 2026-09-11 [S13].
- Prices above are distributor web snapshots (DigiKey/Avnet/LCSC, 2026-11), not Indian 1k quotes.

Open decisions:
1. Fieldbus (CAN-FD + RS-485) on the baseboard MCU vs a G0B1 fieldbus card (both feasible on Zephyr: `can_stm32_fdcan`).
2. Combined module host: STM32H5 + external Wi-Fi (ESP32-C6 / nRF7002) vs RW612 single chip.
3. Brain MCU: STM32H573 (Zephyr + ThreadX) vs MCX N947 (Zephyr; ThreadX unverified).
4. Whether a Linux "Pro" baseboard is needed at all, and SoM vs chip-down.
5. RTOS policy: Zephyr-only (simpler) vs keeping ThreadX as a second option only on ST parts.

## 11. Sources

- [S1] https://docs.zephyrproject.org/latest/project/release_process.html
- [S2] https://github.com/zephyrproject-rtos/zephyr/wiki/Release-Management
- [S3] https://docs.zephyrproject.org/latest/security/vulnerabilities.html
- [S4] https://newreleases.io/project/github/zephyrproject-rtos/zephyr/release/v4.4.2 (aggregator)
- [S5] https://nvd.nist.gov/vuln/detail/CVE-2026-10666
- [S6] https://docs.zephyrproject.org/latest/safety/safety_overview.html
- [S7] https://www.inovex.de/en/?p=66655 (Embedded World 2026 Zephyr safety roadmap)
- [S8] https://threadx.io/releases/6.5.1/home/main/releases-and-support.html
- [S9] https://www.eclipse.org/lists/threadx-dev/msg00017.html (certificate transfer, 2024)
- [S10] https://threadx.io/faq/
- [S11] https://community.st.com/stm32-mcus-embedded-software-32/newer-threadx-versions-150225
- [S12] https://www.beningo.com/embedded-technology-atlas/2026/pages/054-eclipse-threadx.html
- [S13] https://digital-strategy.ec.europa.eu/en/policies/cra-reporting (CRA reporting from 2026-09-11; main obligations 2027-12-11)
- [S14] https://www.nxp.com/products/i.MX93 (i.MX 93 features)
- [S15] https://www.nxp.com/company/about-nxp/smarter-world-blog/BL-INTRODUCING-THE-IMX-91-FAMILY (15-year longevity programme)
- [S16] https://www.mouser.sg/en/c/semiconductors/embedded-processors-controllers/microprocessors-mpu/?pg=45&q=80 (aggregated search, STM32MP135 price hints)
- [S17] https://currencybeacon.com/rates/USD/INR (USD/INR 93.93 on 2026-11-08)
- [S18] https://hdfcsky.com/news/rupee-rises-24-paise-to-93-74-against-us-dollar-in-early-trade ; https://hdfcsky.com/news/rupee-falls-10-paise-to-close-at-94-86-against-us-dollar (PTI, Nov 2026)
- [S19] https://estore.st.com/en/stm32mp131aag3-cpn.html
- [S20] https://www.digikey.com/en/products/detail/stmicroelectronics/STM32MP131AAG3/21348963 ; https://www.digikey.com/en/products/detail/stmicroelectronics/STM32MP131DAG7/21348895
- [S21] https://il.farnell.com/stmicroelectronics/stm32mp135dag7/mpu-32bit-1ghz-tfbga-289/dp/4146363
- [S22] https://www.digikey.com.br/en/products/detail/stmicroelectronics/STM32MP215FAM3/28143713 ; https://www.st.com/en/microcontrollers-microprocessors/stm32mp211.html ; https://www.st.com/en/microcontrollers-microprocessors/stm32mp215d.html
- [S23] https://www.avnet.com/americas/product/nxp/mimx9131cvvxjab/evolve-119885897 ; https://www.avnet.com/americas/product/nxp/mimx9131dvvxjaa/evolve-69346545 ; https://www.digikey.dk/en/products/detail/nxp-usa-inc/MIMX9131CVVXJAB/26799364
- [S24] https://www.digikey.com.br/en/products/detail/nxp-usa-inc/MIMX9352CVVXMAC/26730164
- [S25] https://www.digikey.com.mx/en/products/detail/nxp-usa-inc/MCIMX6Y2CVM05AB/7803860
- [S26] https://www.st.com/en/microcontrollers-microprocessors/stm32mp135f.html ; https://www.mouser.in/new/stmicroelectronics/stm-stm32mp1/
- [S27] https://www.farnell.com/datasheets/4019040.pdf (STM32MP135F-DK data brief)
- [S28] https://community.st.com/t5/stm32-mpus-products/hi-stm-team-can-you-suggest-how-long-stm32mp131a-d-mpu-part-will/m-p/53798
- [S29] https://www.st.com.cn/resource/en/product_presentation/stm32mp1_press-pres.pdf ; https://blog.st.com/stm32mp13/
- [S30] https://wiki.st.com/stm32mpu/wiki/STM32MP13_OP-TEE_overview
- [S31] https://nxp.com/docs/en/data-sheet/IMX91CEC.pdf ; https://nxp.com/docs/en/data-sheet/IMX91IEC.pdf (cited via search index; direct download blocked)
- [S32] https://NXP.com/docs/en/fact-sheet/IMX91FAMFS.pdf ; https://www.mouser.se/nxp-imx-91
- [S33] https://docs.zephyrproject.org/latest/boards/nxp/imx93_evk/doc/index.html ; https://docs.zephyrproject.org/latest/boards/variscite/imx93_var_dart/doc/index.html ; https://docs.zephyrproject.org/latest/boards/nxp/frdm_imx93/doc/index.html
- [S34] https://www.digikey.com.mx/en/products/detail/myir-tech-limited/MYC-YF135-256N256D-100-I/20412042 ; https://www.hackster.io/news/myir-launches-a-tiny-yet-feature-packed-19-som-built-around-stmicro-s-new-stm32mp135-chip-9cbaaa363b18 ; https://www.cnx-software.com/2023/06/12/tiny-stm32mp135-system-on-module-comes-with-up-to-512mb-ram-256mb-nand-flash-or-4gb-emmc-flash/
- [S35] https://shop.variscite.com/nxp-i-mx9/ ; https://shop.variscite.com/product/system-on-module/dart-mx93-system-on-module/
- [S36] https://www.cnx-software.com/2026/03/31/toradex-osm-and-lino-soms-30x30mm-nxp-i-mx-93-i-mx-91-modules-with-solder-down-or-b2b-connector-designs/
- [S37] https://octavosystems.com/octavo_products/osd32mp2x/ ; https://www.cnx-software.com/2024/04/11/octavo-osd32mp2-system-in-package-sip-packs-an-stm32mp25-soc-ddr4-eeprom-and-passive-components-into-a-single-chip/
- [S38] https://dasenic.com/product/octavo-systems-llc-osd32mp157c-512m-baa-4571603 (reseller, indicative)
- [S39] https://docs.zephyrproject.org/latest/boards/st/stm32mp257f_ev1/doc/index.html
- [S40] https://www.digikey.com/en/product-highlight/s/stmicroelectronics/stm32mp25-second-generation-application-processors
- [S41] https://www.lcsc.com/product-image/C2762437.html (MT7628NN)
- [S42] https://www.lcsc.com/product-detail/C209920.html ; https://datasheet.lcsc.com/lcsc/1912111437_HI-LINK-HLK-7628N_C209920.pdf ; https://techinfodepot.shoutwiki.com/wiki/Hi-Link_HLK-7628N
- [S43] https://downloads.openwrt.org/releases/25.12.3/targets/ramips/ ; https://forum.openwrt.org/t/tl-mr3020-v3-64mb-ram-complete-travel-router-setup-wireguard-extroot-travelmate-on-25-12-4/250982 ; https://38.54.75.67.sslip.io/supported_devices/864_warning (unofficial mirror of OpenWrt 8/64 warning)
- [S44] https://eicut.com/wp-content/uploads/2025/04/Quectel_EC25EC21EC20-R2.0-QuecOpen_Solution_Presentation_V1.0.pdf ; https://osmocom.org/projects/quectel-modems/wiki/EC25_Linux/6 ; https://forums.quectel.com/t/open-linux-sdk-for-ec25/20289
- [S45] https://projects.osmocom.org/projects/quectel-modems/wiki/Qualcomm_MDM9607/3/annotate
- [S46] https://www.arrow.com/en/products/ec25euxgr-128-sgns/quectel-wireless-solutions-co-ltd ; https://openelab.com/products/quectel-eg25-g-4g-lte-cat4-lga-module ; https://ichome.com/product-detail/quectel/eg25ggb-minipcie
- [S47] https://files.waveshare.com/upload/b/b2/SIM7600_Series_Open_Linux_Development_Guide_V2.00.pdf ; https://e2e.ti.com/support/tools/code-composer-studio-group/ccs/f/code-composer-studio-forum/942844/compiler-arm-gcc
- [S48] https://www.kernel.org/category/releases.html
- [S49] https://wiki.linuxfoundation.org/civilinfrastructureplatform/start
- [S50] https://cip-project.org/blog/2025/05/26/cip-is-now-supporting-five-slts-kernels ; https://cip-project.org/blog/2025/01/13/kernel-6-12-will-have-10-years-support-via-cip-are-all-your-maintenance-problems-solved
- [S51] https://tuxcare.com/blog/the-linux-kernel-cve-flood-continues-unabated-in-2025-2/ ; https://lwn.net/Articles/1049963/
- [S52] https://phoronix.com/news/Linux-Kernel-CVEs-Nearly-2000 ; https://pasqualepillitteri.it/en/news/13977/linux-kernel-2000-cve-per-release-ai-bug-hunters
- [S53] https://www.springlex.eu/en/packages/cra/cra-regulation/article-13/ (OJ L 2024/2847 text, Art. 13(8)-(9); EUR-Lex not reachable from this environment)
- [S54] https://www.cyberresilienceact.eu/analysis.html ; https://anchore.com/sbom/eu-cra/ (secondary, Annex I Part II(1))
- [S56] https://www.st.com/resource/en/security_bulletin/sb0067-applicability-of-threadx-middleware-vulnerabilities-on-stm32cube-packages-stmicroelectronics.pdf ; https://community.st.com/stm32cubemx-mcus-29/stm32cubemx-6-18-0-missing-x-cube-azrtos-h5-166580 ; https://gh.nn.ci/STMicroelectronics/stm32h5-eclipse-coremw-apps (mirror)
- [S57] https://www.st.com/resource/en/data_brief/stm32cubeu5.pdf ; https://www.st.com.cn/resource/en/data_brief/stm32cubeh5.pdf ; https://community.st.com/stm32-mcus-embedded-software-32/stm32u5-family-and-threadx-154731
- [S58] https://community.nxp.com/t5/MCUXpresso-SDK-Knowledge-Base/Using-Azure-RTOS-ThreadX-with-MCUXpresso-SDK/ta-p/1184585 ; https://www.github.com/NXP/azure-rtos
- [S59] https://lists.trustedfirmware.org/archives/list/tf-m@lists.trustedfirmware.org/thread/UAHUZGYI22XDKBQ2E2AZNELAVEQNDVBA/ ; https://devzone.nordicsemi.com/f/nordic-q-a/100869/how-to-reduce-the-code-size-of-tf-m/434911 ; https://nrfconnectdocs.nordicsemi.com/ncs/latest/tfm/configuration/profiles/index.html
- [R02]/[R03] = sibling reports docs/research/R02_Cellular_4G.md and R03_WiFi_BLE.md (their own sources apply)
- [S55] https://github.com/zephyrproject-rtos/zephyr (main, commit 7cd4b562b30a9bcd76a7288ad90d5e71dd6f87d2, 2026-11-13): dts/arm/st/{h5,u5,wl,g0,mp13,mp2}, dts/arm/nxp/{mcx/mcxn,rw,imxrt/imxrt10xx}, dts/arm/nordic + dts/vendor/nordic, dts/riscv/espressif/esp32c6, boards/{st,nxp,nordic,espressif}, drivers/{can,ethernet,wifi,lora,modem}, modules/trusted-firmware-m
