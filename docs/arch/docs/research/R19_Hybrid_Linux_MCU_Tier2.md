# R19 — Hybrid Linux-MPU + Real-Time-MCU Platforms for the Tier-2 Router (Arduino UNO Q and equivalents)

Date: 2026-11-15. FX: 1 USD = INR 93.9. Status: COMPLETE WITH GAPS.

Markers:
- **UNVERIFIED**: not confirmed by a primary source.
- **E**: an engineering estimate.
- **INFERRED**: deduced from other facts.

Numbered sources are in section 10. Internal reports are cited as [R09], [R18] and so on. This report builds on R18 (STM32MP133C + Yocto Tier-2 router, BOM INR 5,366, ex-works INR 11,439) and R16 (router reference architectures), and does not repeat them.

Ex-works formula (owner): BOM × 1.5, plus INR 750 royalty, then × 1.3 (30 % profit).

---

## 1. Summary and recommendation

1. **The Arduino UNO Q is not a good base for an industrial 4G router. Its retail price is no longer USD 44–55.**
   - **Price.** Arduino raised the price on 6 July 2026, citing memory costs: 2 GB/16 GB went from USD 44 to **USD 59 (INR 5,540)** and 4 GB/32 GB from USD 59 to **USD 79 (INR 7,418)** [6]. Indian shops still list some older stock at INR 4,150–4,420 ex-GST [10].
   - **No Ethernet MAC.** The QRB2210 has no Ethernet MAC and no PCIe. Its high-speed I/O is one USB 3.1 port, SDIO, MIPI CSI and MIPI DSI [11]. On the UNO Q, Ethernet is reachable only through a USB-C dongle [1].
     - A router therefore needs a USB hub plus USB-to-Ethernet bridge chips, all sharing one USB port with the 4G modem.
     - This is not an SPI controller, but it breaks the intent of the owner rule "Ethernet from a MAC inside a chip" (meaning the SoC) and adds a single point of failure.
   - **Consumer temperature range.** The board is rated **-10 to +60 °C ambient** [2]. The SoC is rated Tj -30 to +95 °C [11]. Our target is -40 to +75 °C [R18].
   - **Secure boot is gated by Qualcomm.** QRB2210 secure boot uses QFPROM fuses, and the signing tools (SecTools) are "available to licensed users with authorized access" through Qualcomm ChipCode [14]. Arduino ships the board open, with no secure boot enabled [5].
   - **Cost.** A UNO Q plus a router carrier gives a BOM of about **INR 8,710** and an ex-works price of about **INR 17,960**. That is 57 % above R18 (INR 11,439) and above RUT200 retail (INR 13,700) (section 5.1).
   - **Chip-down is not realistic.** The QRB2210 is a 0.4 mm-pitch BGA with LPDDR4X. Arduino's own CAD release shows an **8-layer HDI board with stacked microvias** [4].
   - **QRB2210 parts and modules can be bought, but none fixes the core problem.**
     - The bare chip is USD 14.55 at quantity 1 from DigiKey, with a 28-week lead time [17].
     - eInfochips Aikri SoM: USD 44.66 at Arrow [19]. Lantronix Open-Q 2210RB: USD 87.92 at 21+ [20].
     - Both modules ship Yocto Dunfell on kernel 5.4 [19][20], an end-of-life stack, and still have no Ethernet.
   - **What the UNO Q gets right:**
     - QRB2210 longevity to May 2034 [11][12];
     - upstream kernel device tree [15];
     - Debian 13 and Yocto support [11];
     - CC BY-SA 4.0 design files [4];
     - WPC listed among its certifications [1].

   **Use:** a lab or demo board, or an "edge-AI companion" next to the router. Do not use it as the router itself.
2. **The hybrid idea is sound. Build it on ST parts that have Ethernet MACs inside.**
   - **Recommended for Tier 2 v1: "two-chip hybrid".** This is R18's STM32MP133C (Linux: routing, VPN, firewall, web UI, containers) plus an **STM32H533 running Zephyr** as the real-time companion. It is the same MCU and firmware base as the baseboard [R14].
   - The companion owns:
     - DI / DO and their defined safe states from power-on;
     - RS-485 / Modbus RTU timing;
     - a staged watchdog of the Linux side: MPU reset, modem power-cycle, then full power-cycle.
   - BOM **INR 5,630** (+264 vs R18); **ex-works INR 11,954** (+515).
3. **Single-chip upgrade path ("Pro" or v2): STM32MP231C / MP233C.**
   - 1–2 × Cortex-A35 at 1.5 GHz plus a Cortex-M33 at 400 MHz;
   - **2 × GbE MAC with TSN**, 16-bit DDR3L/DDR4/LPDDR4, 0.8 mm-pitch TFBGA361, Tj -40 to +125 °C, secure boot, 10-year longevity [22].
   - Today it costs USD 12.77 at 504 units (Future) [24] against USD 5.16 for the MP133C. That gives BOM **INR 6,180**, **ex-works INR 13,026**. The family "from USD 8.46 @1k" figure [22] would bring this to about INR 12,240.
   - Choose it when arm64, Debian or more CPU is needed.
4. **Stack option ("Linux compute module").**
   - An MP133C module with its own EC200A plugs into the 40-pin stack. It replaces the Tier-1 modem card and links to the baseboard over the 100 Mbit capacitor-coupled Ethernet link.
   - Module BOM **INR 3,427**, ex-works INR 7,658. Full stack system (baseboard + module + case): BOM INR 5,712, **ex-works INR 12,113**.
   - Good for customers who already have the baseboard. Not cheaper than the standalone router.
5. **Software: Debian vs Yocto.**
   - Debian (NetworkManager, ModemManager, nftables, WireGuard, strongSwan, OpenVPN, a Cockpit-based UI) built with **isar-cip-core** (Debian packages, CIP kernel, SWUpdate A/B, secure boot [33]): **13–22 engineer-months (E)** against R18's 18–30 on Yocto. It saves about 4–8 engineer-months, about INR 10–20 lakh.
   - The cost: Debian needs about 512 MB RAM and eMMC instead of 256 MB DDR3L plus SPI-NAND, about **+INR 705 BOM** (E). At 1k units a year that is about INR 10.6 lakh a year of finished cost, so the saving is used up in 1–2 years.
   - **Recommendation:**
     - keep Yocto, with the OpenWrt gate, on the MP133C cost router [R18];
     - use Debian (isar-cip-core) only on an arm64 Pro variant (MP23x or i.MX93).
   - Support periods (CRA):
     - Debian 13: security support to about Aug 2028, then LTS to 30 Jun 2030 [32].
     - Yocto 6.0: to Apr 2030, plus CIP 6.12 to 2035 [R18].
6. **Price position vs competitors.** None of the hybrid options beats RUT200 dealer prices (INR 7,569–8,500) or USR-G806w (INR 8,008 ex-GST) [R18]. The recommended option sits at R18's level (INR 11,954) and wins on specification, as R18 explains.

---

## 2. Arduino UNO Q: facts

| Item | Fact | Src |
|---|---|---|
| SKUs | ABX00162: 2 GB LPDDR4X + 16 GB eMMC. ABX00173: 4 GB + 32 GB | [2] |
| MPU | Qualcomm Dragonwing **QRB2210**: 4 × Cortex-A53 at 2.0 GHz, Adreno 702 GPU at 845 MHz (Mesa freedreno/turnip; Vulkan 1.0 driver), dual ISP, Hexagon DSP, 1080p30 H.264/H.265 | [2][7][11] |
| MCU | **ST STM32U585** (Cortex-M33, 160 MHz, 2 MB flash, 786 kB SRAM) running the Arduino core on **Zephyr**. Upstream Zephyr board `arduino/uno_q`. The MPU and MCU talk through "Bridge" RPC over UART, SPI or USB CDC | [2][21] |
| Memory parts (schematic) | Micron **MT53E512M32D1ZW** LPDDR4X (single rank, 32-bit), EMMC16G-MW28 eMMC, PMIC **PM4125** | [3] |
| Wi-Fi / BT | **WCBN3536A module (Qualcomm WCN3980)**: Wi-Fi 5 dual-band + BT 5.1. Wi-Fi over SDIO, BT over UART, **on-board PCB antenna only** | [2] |
| Ethernet | **None.** The QRB2210 brief lists no Ethernet MAC [11]. Arduino lists Ethernet only through a USB-C dongle [1] | [1][11] |
| USB | **One USB-C**: USB 3.1 with role switching, plus DisplayPort Alt-Mode through an ANX7625 bridge. USB data speed drops when DP is active. The SoC lists only one "USB 3.1" interface | [2][11] |
| PCIe | **None** (not in the SoC brief) | [11] |
| Power input | USB-C 5 V / 3 A (PD requests 5 V / 3 A only); **VIN 7–24 V** on a header (buck, Schottky diode-OR); or 5 V on 5V_SYS | [2] |
| Temperature | **-10 to +60 °C ambient** (board); SoC Tj -30 to +95 °C | [2][11] |
| Certifications listed | CE, UKCA, FCC (DTS / DSS / NII), ISED, **WPC**, ICASA, Anatel, IMDA, NCC, KC, SRRC, OFCA. These are radio and board approvals; no MTCTE (a host-product scheme) | [1] |
| OS | Arduino ships **Debian 13 "trixie"** (arm64). Qualcomm's brief: "Yocto Linux and Debian Trixie 13", upstream kernel; launch image on **kernel 6.16** | [11][16] |
| Upstream kernel | `qrb2210-arduino-imola.dts` is in mainline Linux (series by Arduino, Nov 2025; display bridge and audio added by Qualcomm in 2026). Armbian builds Debian trixie on mainline 7.1 for it | [15][16] |
| Security-update policy | Arduino updates the board image through App Lab [2]. **No published support period or security-update commitment was found for the UNO Q Linux image (UNVERIFIED).** Arduino's model is "shared responsibility": hardening is the developer's job | [2][5] |
| Secure boot / TrustZone | QRB2210 lists secure boot, secure debug, TrustZone/TEE and a hardware keystore (secondary sources [13]). Secure boot means blowing QFPROM fuses with Qualcomm **SecTools v2**: "The SecTools guides are available to licensed users with authorized access" through ChipCode. The OEM ID comes from Qualcomm [14]. **The UNO Q ships with no locked boot or restricted debug** [5] | [5][13][14] |
| Boot chain | Qualcomm PBL → XBL → TZ/HYP → ABL → U-Boot → Linux (Armbian notes). XBL, TZ, Wi-Fi and DSP firmware are **closed Qualcomm binaries** (INFERRED, typical for Qualcomm) | [16] |
| Open hardware | Schematics PDF, pinout, STEP and CAD zip are published. The CAD zip carries `License.txt`: "**Creative Commons Attribution-ShareAlike 4.0**". The board file is **Cadence Allegro `.brd`**. Drill files for layer pairs 1-2, 2-3, 3-6, 6-7 and 7-8 mean **8-layer HDI with microvias** | [1][3][4] |
| Price (retail) | Launch Oct 2025: USD 44 (2 GB); 4 GB USD 59 (Jan 2026). **From 6 Jul 2026: USD 59 (2 GB) / USD 79 (4 GB)**, because "memory component costs have more than doubled" | [6][7][8] |
| Price (India) | ABX00162: INR 4,151.69 ex-GST (MakerBazar), INR 4,417 ex-GST (Electropi), INR 4,652 (Robocraze). Probably pre-increase stock (UNVERIFIED) | [10] |
| Volume / OEM pricing | **None published** (UNVERIFIED). The blog post mentions no business pricing [6] | [6] |
| Commercial use | "Arduino boards are designed primarily as development and prototyping environments and can also serve as a basis for production solutions". Security is a shared responsibility, and enabling secure boot or a secure element is "the developer's responsibility" [5]. The CC BY-SA licence requires a derived *design* to be shared alike. Using the "Arduino" name needs Arduino's trademark permission (UNVERIFIED, policy not fetched) | [4][5] |
| Ownership | Qualcomm announced its acquisition of Arduino in Oct 2025 (subject to approval at the time). Arduino keeps its brand and multi-vendor support | [7] |
| QRB2210 longevity | Qualcomm Product Longevity Programme: **May 2034** ("subject to change without notice") | [11][12] |
| QRB2210 package | **12 × 12.4 × 0.91 mm, 0.4 mm pitch**; memory 2 × 16-bit LPDDR4X at 1804 MHz or 32-bit LPDDR3; eMMC 5.1; SD 3.0 | [11] |

**Takeaway.** The UNO Q is a good, open and well-documented SBC with excellent upstream Linux. As a router base it lacks Ethernet MACs, a second USB host, an industrial temperature range, an external-antenna option and an open secure-boot flow.

---

## 3. Hybrid platform comparison

Prices are distributor figures as listed; "@N" is the quantity tier.

| Platform | App cores + real-time core | Ethernet MACs in SoC | DRAM type | Package / pitch | Temp. | Secure boot | Longevity | OS (Linux / Zephyr on RT core) | Chip price | SoM price | Src |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **Qualcomm QRB2210** (UNO Q) | 4 × A53 2.0 GHz; **no on-die MCU** (UNO Q adds an STM32U585) | **0** (USB 3.1 × 1) | LPDDR4X / LPDDR3 | 12 × 12.4, **0.4 mm** | Tj -30..+95 °C | QFPROM; SecTools for licensed users | May 2034 | Debian 13, Yocto, mainline DTS / Zephyr on the U585 | USD 14.55 @1 (DigiKey, 28 wk) | eInfochips Aikri 3 GB/32 GB USD 44.66 (Arrow; Yocto Dunfell, kernel 5.4; -30..85 °C); Lantronix Open-Q 2210RB USD 87.92 @21+ (35 × 35 LGA, -25..85 °C, Dunfell 5.4, 26 wk) | [11][12][14][17][19][20] |
| **ST STM32MP133C** (R18) | 1 × A7 1 GHz; no RT core | **2** (10/100/1000) | DDR3L 16-bit | LFBGA289 **0.8 mm** | industrial | ROM ECDSA, OP-TEE | 10-year rolling | Yocto, OpenWrt / – | USD 5.16 @2k | MYiR MYC-YF135 USD 16–29 | [R18][R09] |
| **ST STM32MP231C / 233C** | 1–2 × A35 1.5 GHz + **M33 400 MHz** | **2 × GbE, TSN** | **DDR3L / DDR4 / LPDDR4, 16-bit**, up to 4 GB | TFBGA361 16 × 16 **0.8 mm** (also 0.5 mm options) | **Tj -40..+125 °C** | secure boot, TrustZone A and M, tamper; SESIP 3 in progress | 10-year | Yocto (OpenSTLinux); Debian UNVERIFIED for MP23 / Zephyr on M33: MP25/MP21 boards upstream [R09], **MP23 UNVERIFIED** | MP231CAJ3 **USD 12.77 @504** (Future), USD 12.96 (Octopart); MP233CAJ3 USD 26.35 @500 (ST eStore); family "from USD 8.46 @1k" | none found for MP23 | [22][23][24] |
| ST STM32MP25x | 2 × A35 + M33 | up to 3 × GbE (MP23 is "down from three") | DDR4 / LPDDR4 (UNVERIFIED for DDR3L) | BGA | industrial | as MP23 | 10-year [R09] | Yocto; MYiR ships **Debian 12** on its MP25 SoM / Zephyr M33 upstream | not fetched (higher than MP23) | MYiR MYC-LD25X EUR 159 @1 (DigiKey marketplace) | [22][30][R09] |
| **NXP i.MX93** | 2 × A55 + **M33** + NPU | **2 × GbE** (one TSN) | **LPDDR4/4X only** | **0.5 mm** | industrial variants | AHAB + EdgeLock enclave | NXP long-term (15-year for i.MX91 [R09]; i.MX93 UNVERIFIED) | Yocto (NXP LF); Debian community / Zephyr M33 upstream [R09] | USD 14.94 [R09] | Toradex OSM USD 28.20 volume; Variscite DART from USD 39 [R09] | [29][R09] |
| NXP i.MX91 | 1 × A55, **no RT core** | 2 × GbE | LPDDR4 | 0.5 mm | industrial | AHAB + EdgeLock | 15-year [R09] | Yocto / – | USD 8.0–8.8 [R09] | Toradex OSM USD 25.55 [R09] | [29] |
| NXP i.MX8M Mini | 4 × A53 1.6 GHz + **M4** | **1** × GbE | DDR3L / DDR4 / LPDDR4 | LFBGA486 14 × 14 (0.5 mm, UNVERIFIED) | -40..105 °C (CVT part) | HAB | NXP programme (date UNVERIFIED) | Yocto, Debian community / Zephyr M4 (UNVERIFIED) | MIMX8MM6CVTKZAA **USD 20.92 @1k** (Future); USD 33–35 @304 (DigiKey) | many (Toradex, Variscite, MYiR) | [28] |
| NXP i.MX8M Nano | 1–4 × A53 + M7 | 1 × GbE | DDR3L / DDR4 / LPDDR4 | 0.5 mm | industrial | HAB | UNVERIFIED | Yocto | not fetched | – | – |
| **TI AM62x** (AM6231 / AM6232) | 1–2 × A53 1.0–1.4 GHz + **M4F** | **2 × GbE** (CPSW3G, TSN) | DDR4 / LPDDR4 | FCCSP425 13 × 13 (pitch UNVERIFIED, about 0.5 mm) | -40..105 °C (S grade) | HS-SE devices; key-programming flow terms UNVERIFIED | UNVERIFIED | Yocto (TI SDK), **Debian (BeagleBoard images, UNVERIFIED here)** / **Zephyr `sk_am62/am6254/m4` upstream** | AM6231 USD 7.31 @1k, AM6232 USD 8.96 @1k (aggregator); DigiKey USD 13.88 @119 | **Toradex Verdin AM62 from USD 31.90 volume** | [25][26][27] |
| Seeed / Radxa | Their Linux SBCs and CMs are RPi CM / Rockchip based, with no on-die RT core and commercial temperature (UNVERIFIED, not researched in depth) | – | – | – | – | – | – | – | – | – | – |
| iWave (Bangalore) | STM32MP13 OSM [R18]; i.MX93 / AM62 SoMs exist (UNVERIFIED); prices not published | – | – | – | – | – | – | – | – | UNVERIFIED | [R18] |

**Reading the table for a router:**
- Only the ST MP13 / MP23 parts give **two Ethernet MACs, DDR3L and a 0.8 mm pitch** together, so chip-down is feasible on a 6-layer board without HDI [R18].
- **MP23 is the only one of those with an on-die M33.**
- i.MX93 and AM62x are good hybrids but need LPDDR4/DDR4 and 0.5 mm BGAs, so in practice a SoM (USD 28–32 at volume). That adds about INR 1,200–1,600 over the R18 core (INR 1,455 + PCB).
- i.MX91 has no real-time core. i.MX8M Mini has one MAC and costs USD 21.

---

## 4. Architecture options

### 4.1 (a) Embed the UNO Q as-is: pilot only

Block description:
- **Supply:** 9–36 V DC goes through a fuse, TVS, reverse-polarity FET and π-filter to a 5 V / 3 A buck, which feeds the UNO Q **5V_SYS** pin (bypassing its 7–24 V input).
- **Carrier USB:**
  - a right-angle USB-C plug into the UNO Q's single port;
  - a 4-port USB 2.0 hub;
  - port 1: EC200A (USB, ECM/QMI);
  - ports 2–3: 2 × RTL8152B USB 10/100 Ethernet, each with magnetics and RJ45.
- **Carrier IO:** UNO Q header GPIO and UART from the STM32U585 drive isolated RS-485 and 2 DI / 2 DO.
- **Watchdog:** an external supervisor resets the QRB2210 PMIC through the JCTL reset pin [2].
- **Wi-Fi:** the UNO Q's own WCN3980, PCB antenna only, so a **plastic case with an RF window** is needed.

Problems:
- A USB-C plug-in interconnect is a vibration risk.
- All WAN and LAN traffic shares one USB 2.0 hub.
- -10..60 °C rating.
- No external Wi-Fi antenna.
- No secure boot without a Qualcomm licence.

### 4.2 (b) Own QRB2210 board or SoM

- **Chip-down:**
  - 0.4 mm BGA, 32-bit LPDDR4X and the PM4125 PMIC.
  - Arduino's reference uses 8-layer HDI with stacked microvias [4]. Indian HDI fab and assembly capability for 0.4 mm is UNVERIFIED and expensive (E).
  - Core cost (E, UNVERIFIED): SoC INR 1,050–1,370 [17] + LPDDR4X 2 GB about INR 1,400–2,350 (2026 shortage) + eMMC 16 GB INR 470–750 + PMIC about INR 300 + HDI PCB INR 600–900. That is about **INR 3,800–5,700**, against INR 1,605 for R18's core plus PCB.
  - Ethernet would still be over USB.
  - The design could start from Arduino's CC BY-SA files [4], but the files are in Allegro and the derived design must be shared alike.
- **SoM:**
  - eInfochips Aikri (USD 44.66 = INR 4,194) [19] or Lantronix Open-Q 2210RB (USD 87.92 = INR 8,256) [20].
  - Both ship Yocto Dunfell with kernel 5.4. A move to mainline / Debian 13 would be our own work.
  - Thundercomm's C2210 SoM is quote-only [18].
- **Verdict: rejected.**

### 4.3 (c) Equivalent hybrid: recommended forms

**(i) Standalone router, "two-chip hybrid" (RECOMMENDED for v1).**

```
 5–36 V DC ─► fuse/TVS/rev-FET/π ─► buck 3.8 V (modem) ─► buck 5 V ─► SoC rails (AN5586 discrete)
                                                     │
            ┌─────────────── STM32MP133C (A7, Linux, Yocto/OpenWrt) ────────────────┐
            │ ETH MAC1 ─RMII─► KSZ8081 ─► magnetics ─► RJ45 WAN/LAN1                │
            │ ETH MAC2 ─RMII─► KSZ8081 ─► magnetics ─► RJ45 LAN2                    │
            │ USB HS host ─► EC200A-CN (Cat 4) ─► SIM, 2× SMA                       │
            │ USB/SDIO ─► Wi-Fi 4 (option, mainline AP driver) ─► SMA               │
            │ DDR3L 256 MB, SPI-NAND 256 MB; TF-A ► OP-TEE ► U-Boot ► signed FIT     │
            │ UART (RPC, MCUmgr) + nRST/BOOT lines ◄──────────────┐                 │
            └──────────────────────────────────────────────────────┼─────────────────┘
                                                                   │
            STM32H533 (M33, Zephyr, same code base as the baseboard)
              ├─ 2 DI (opto) / 2 DO (OC 36 V) — safe state from power-on, held if Linux dies
              ├─ isolated RS-485 (Modbus RTU timing in Zephyr; Linux sees Modbus TCP/RPC)
              ├─ supervises Linux heartbeat: MPU reset ► modem PWRKEY/VBAT cycle ► full power cycle
              └─ LEDs, reset button, power-fail detect, RTC backup
```

- The MCU firmware is updated from Linux with signed MCUboot images through MCUmgr over UART.
- The bridge protocol can follow the UNO Q "Bridge" idea (an RPC over UART) [2], or plain Modbus RTU.

**(i′) Single-chip hybrid (Pro / v2).**
- Same block diagram. The STM32MP231C/233C replaces the MP133C plus H533: the M33 takes the companion role through remoteproc / RPMsg.
- Keep an **external** window watchdog. The M33 shares the die, supply and reset with the A35, so it cannot be the last line of defence.
- arm64, so Debian 13 / isar-cip-core is practical.

**(ii) Linux compute module on the 40-pin stack.**

```
 Baseboard (STM32H573, Zephyr, field IO, RS-485, AI, power, case) 
      │ 40-pin stack: 5 V/power, 100 Mbit capacitor-coupled Ethernet (PHY–PHY), I2C/GPIO
      ▼
 Linux module: STM32MP133C + DDR3L + SPI-NAND
      MAC2 ─► PHY ─► caps ─► stack link to baseboard
      MAC1 ─► PHY ─► magnetics ─► front RJ45 (LAN/WAN)
      USB host ─► EC200A + SIM + 2× SMA   (module replaces the Tier-1 modem card)
```

- **(ii-a, recommended form):** the module carries its own EC200A and replaces the Tier-1 card.
- **(ii-b):** the module keeps the Tier-1 card and has no modem.
  - The stack link is point-to-point, so this needs a 3-port switch (KSZ8863 class, about INR 250 E, UNVERIFIED).
  - Otherwise the module's second MAC is used up and the front LAN would need USB Ethernet.
  - Not recommended.
- Power from the stack follows the owner rule (5–32 V and USB-C PD at module level).

---

## 5. BOM and ex-works price

INR at 1k, ex-GST. Status codes: **S** sourced, **R** from an internal report, **E** estimate.

### 5.1 Option (a): UNO Q embedded router

| # | Block | INR | Status / basis |
|---|---|---|---|
| A1 | Arduino UNO Q 2 GB (ABX00162) | 5,540 | S: USD 59 [6]; India ex-GST INR 4,152–4,417 [10] |
| A2 | 9–36 V input, protection, 5 V / 3 A buck (15 W) | 220 | R/E: R18 line 11 (165), scaled for current |
| A3 | USB-C plug interconnect + retention bracket | 80 | E |
| A4 | USB 2.0 4-port hub IC + crystal | 100 | E (UNVERIFIED) |
| A5 | 2 × RTL8152B USB 10/100 Ethernet | 162 | S: LCSC USD 0.858 @980 [31]; industrial temperature grade UNVERIFIED |
| A6 | 2 × magnetics + RJ45 + ESD + Bob-Smith network | 278 | R: R18 line 6 minus the PHYs |
| A7 | EC200A-CN + VBAT buck + SIM | 1,285 | R: R18 lines 7–9 |
| A8 | Isolated RS-485 / 2 DI + 2 DO / terminals | 306 | R: R18 lines 12, 13, 15 |
| A9 | Supervisor on the JCTL PMIC reset | 30 | E |
| A10 | 2 × SMA + pigtails, 2 × LTE antennas | 230 | E (Wi-Fi uses the on-board PCB antenna) |
| A11 | LEDs, carrier PCB 4-layer, passives | 190 | E |
| A12 | Plastic DIN case with RF window | 250 | E (aluminium would block the PCB antenna) |
| A13 | Packaging | 40 | E |
| | **BOM** | **8,711** | (7,323 at INR 4,152 retail) |

### 5.2 Summary table

| Option | BOM | ×1.5 | +750 | **Ex-works (×1.3)** | vs R18 |
|---|---|---|---|---|---|
| R18 base (MP133C, Yocto) [R18] | 5,366 | 8,049 | 8,799 | **11,439** | — |
| **(i) R18 + STM32H533 Zephyr companion (recommended)**: + H533RET6 INR 269 [R14] + crystal / SWD / decoupling 25, − external watchdog TPS3431 30 | **5,630** | 8,445 | 9,195 | **11,954** | +515 |
| (i′) STM32MP231C single-chip hybrid, Yocto: SoC 485 → 1,199 (USD 12.77 [24]); more rails +100 (E); external watchdog kept | 6,180 | 9,270 | 10,020 | **13,026** | +1,587 |
| (i′) at the family "from USD 8.46" price [22] (SoC 794) | 5,775 | 8,663 | 9,413 | 12,236 | +797 |
| (i′) MP231C + **Debian**: 512 MB DDR3L (+440 E) + 8 GB eMMC instead of SPI-NAND (+265 E) | 6,885 | 10,328 | 11,078 | **14,401** | +2,962 |
| (i) MP133C + Debian (same memory change, armhf) | 6,335 | 9,503 | 10,253 | 13,328 | +1,889 |
| (ii-a) **Linux module for the stack** (module only): SoC + DDR + NAND + power + crystals 1,455 [R18]; 2 × KSZ8081 192; one magnetics + RJ45 set 139; coupling caps 10; EC200A + VBAT + SIM 1,285; 2 × SMA 80; 6-layer PCB 110; stack connector + ESD 61 [R14]; passives 80; LEDs 15 | 3,427 | 5,141 | 5,891 | **7,658** | — |
| (ii-a) **full stack system**: baseboard 1,720 [R14] + module 3,427 + aluminium case 375 + antennas 150 + packaging 40 | 5,712 | 8,568 | 9,318 | **12,113** | +674 (adds the baseboard's 16 IO + AI) |
| (a) UNO Q embedded | 8,711 | 13,067 | 13,817 | **17,961** | +6,522 |
| (a) at INR 4,152 India retail | 7,323 | 10,985 | 11,735 | 15,255 | +3,816 |
| (b) QRB2210 SoM (Aikri USD 44.66) instead of R18's core (−1,455) + USB-Ethernet / hub (+262) | about 8,370 | 12,555 | 13,305 | about 17,300 | +5,860 |

Competitors [R18]:
- RUT200: INR 7,569–8,500 (dealer), INR 13,700 (retail).
- USR-G806w: INR 8,008 ex-GST.
- USR-G809: INR 10,528 ex-GST.

Only R18 and the recommended option (i) stay below RUT200 retail. None reaches dealer prices; R18 §5.4 has the cost-down levers.

---

## 6. Software effort and CRA

### 6.1 Effort

| Work package (engineer-months, E) | R18 Yocto on MP133C | Debian (isar-cip-core) on MP23x / MP133C | UNO Q (Arduino Debian) |
|---|---|---|---|
| BSP, kernel, image build | 3–4 | 2–3 (isar-cip-core, CIP kernel) [33] | 2–3 (mainline DTS [15]) |
| Secure boot + signed A/B (RAUC / SWUpdate) | 2–3 | 2–3 (SWUpdate + signing docs in isar-cip-core) | **blocked without Qualcomm SecTools licence** [14] |
| Cellular and WAN failover (ModemManager / own EC200A manager, mwan) | 2–4 | 1.5–3 (Debian packages; EC200A support in ModemManager UNVERIFIED) | 1.5–3 |
| Firewall (nftables zones), VPN (WireGuard, strongSwan, OpenVPN) | 2–3 | 1–2 | 1–2 |
| **Web UI** | 5–8 (own UI) | **3–5** (Cockpit with its NetworkManager page plus our own pages for cellular, firewall zones, IO and Modbus; Cockpit cellular support UNVERIFIED [35]) | 3–5 |
| Modbus / MQTT gateway, data-to-server | 1–2 | 1–2 | 1–2 |
| Companion MCU (Zephyr) + bridge | (IO on Linux) | 1–2 (reuses baseboard drivers) | 1–2 |
| CRA process: SBOM, CVE triage, PSIRT | 2–3 | 1.5–2.5 (Debian Security Tracker; SBOM tooling for Debian/Isar UNVERIFIED) | 1.5–2.5 |
| **Total** | **18–30** [R18] | **13–22** | **14–24 + Qualcomm licence (unknown)** |
| OpenWrt fallback on MP133C | 9–14 [R18] | — | — |

Notes:
- Debian saves mainly on the UI and on package integration. It costs RAM and flash (section 5.2: +INR 705 BOM).
- At R18's implied rate of about INR 2.5 lakh per engineer-month (INR 60 lakh for the development [R18]), the 4–8 engineer-month saving is INR 10–20 lakh once.
- The BOM premium is about INR 1,058 per unit in finished cost, about INR 10.6 lakh a year at 1k units.
- On a single 1 GHz Cortex-A7 (MP133C), Debian armhf plus Cockpit performance is UNVERIFIED (E: usable but slow). Debian fits better on arm64 MP23x / i.MX93 / AM62x.

### 6.2 CRA

| CRA item | Yocto (R18) | Debian |
|---|---|---|
| Support period | Yocto 6.0 to Apr 2030; CIP 6.12 kernel to about 2035 [R18] | Debian 13: security team support for **3 years from release** (released Aug 2025, so to about Aug 2028) [32]; **LTS 9 Aug 2028 – 30 Jun 2030** (LTS architectures for trixie "to be determined"; bookworm LTS covers armhf and arm64) [32]; paid ELTS beyond that (UNVERIFIED [34]). A rebase to Debian 14 is needed during a 5–10-year support period |
| SBOM | Yocto SPDX per image | Debian/Isar SBOM generation exists in the ecosystem (UNVERIFIED which tool); package-level traceability through Debian source packages |
| CVE handling | `cve-check` / VEX | Debian Security Tracker + DSA/DLA feed; fixes come as binary packages, fewer own rebuilds |
| Secure boot | ST ROM → TF-A → OP-TEE → U-Boot FIT [R18] | Same ST ROM chain. isar-cip-core adds UEFI secure boot (EFI Boot Guard / signed images) and SWUpdate [33]. On QRB2210 the chain needs Qualcomm SecTools [14] |
| Class | Router = Important Class I [R01] | same |

---

## 7. Risks

1. **UNO Q / QRB2210 (if pursued despite this report):**
   - no Ethernet MAC;
   - -10..60 °C board rating;
   - secure boot gated by a Qualcomm licence;
   - no published Linux support period or volume price;
   - DRAM-driven price rises (+34 % in July 2026 [6]);
   - CC BY-SA share-alike on derived designs;
   - the Qualcomm acquisition may change terms (UNVERIFIED);
   - closed boot and Wi-Fi firmware.
2. **Chip-down in India:**
   - 0.4 mm (QRB2210) and 0.5 mm (i.MX93, AM62x, i.MX8M) BGAs with LPDDR4 need HDI or via-in-pad, 8 or more layers, and X-ray-inspected assembly. Indian fab and EMS capability and yield are UNVERIFIED (E: high risk).
   - 0.8 mm BGA with DDR3L (MP133C, MP23x TFBGA361) is the safe class [R18].
3. **Memory prices:** LPDDR4X and DDR3L prices are still rising in 2026 [6][R18]. Get quotes.
4. **STM32MP23 maturity:**
   - The ST eStore shows MP233 out of stock at 500 units [23]; the price spread is USD 8.46–27 [22][23][24].
   - Zephyr support for the MP23 M33 is UNVERIFIED.
   - Debian on MP23 is UNVERIFIED.
5. **Companion-MCU supply:** H5 lead times of up to 52 weeks [R14]. A shared part with the baseboard helps volume but concentrates risk. Second source: STM32G0B1 [R09].
6. **USB-Ethernet** (if ever used): RTL8152B temperature grade is UNVERIFIED, and it shares the USB bus with the modem.
7. **Software:**
   - EC200A support in ModemManager is UNVERIFIED.
   - Cockpit has no router-grade cellular or firewall pages (UNVERIFIED), so the UI saving may shrink.
8. **Stack module (ii):** the point-to-point stack link limits topologies. Thermal coupling of the modem and MPU inside a stacked case is UNVERIFIED.

### Open decisions for the owner

1. Accept that the UNO Q is a lab and demo board only, not the router base?
2. Add the STM32H533 Zephyr companion to R18 (+INR 515 ex-works)?
3. Is an MP23x "Pro" router (Debian, arm64, TSN) wanted as a second SKU?
4. Is the stack Linux module (ii-a) wanted alongside the standalone router?
5. Is USB-attached Ethernet ever acceptable under the "MAC inside a chip" rule? This report assumes not.

---

## 8. What could not be verified

- UNO Q: volume / OEM pricing, official Linux support period, whether shipped units have any fuse or secure-boot state, Arduino trademark terms for commercial carriers, and the kernel in the current official image (6.16 at launch).
- QRB2210: Qualcomm's own datasheet security section (secondary sources only); 1k chip price; PM4125 and LPDDR4X 2026 prices; eInfochips and Lantronix SoM specs from primary datasheets (eInfochips PDF blocked).
- STM32MP23: real 1k price for the C (secure) parts, RMII support for 10/100 PHYs, Zephyr M33 board, Debian support.
- AM62x: package pitch, secure-boot key-programming terms, longevity. i.MX8M Nano price. i.MX93 longevity date. Variscite AM62 and iWave i.MX93 / AM62 prices.
- 512 MB DDR3L and 8 GB eMMC 1k prices; USB hub price.
- Cockpit cellular support; ModemManager support for the EC200A; Debian/Isar SBOM tool; Freexian ELTS terms.
- All software efforts are estimates.

---

## 9. Internal references

R01 (CRA, MTCTE), R09 (Linux SoCs, SoMs, CIP, Zephyr support), R14 (baseboard BOM, STM32H533 price, stack connector), R16 (router reference architectures), R17 (Tier-1 modem card), R18 (Tier-2 router: STM32MP133C, Yocto, BOM, competitors).

## 10. Sources

1. Arduino UNO Q hardware page (specs, certifications, downloads) — https://docs.arduino.cc/hardware/uno-q/
2. Arduino UNO Q datasheet ABX00162 / ABX00173 (rev. modified 13/11/2026; power inputs, -10..60 °C, interfaces, Bridge, JCTL) — https://docs.arduino.cc/resources/datasheets/ABX00162-datasheet.pdf ; https://docs.arduino.cc/resources/datasheets/ABX00173-datasheet.pdf
3. Arduino UNO Q schematics (MT53E512M32D1ZW, PM4125, WCBN3536A, STM32U585AII6TR, ANX7625; "as is" reference design) — https://docs.arduino.cc/resources/schematics/ABX00162-schematics.pdf
4. Arduino UNO Q CAD files (License.txt: CC BY-SA 4.0; Allegro .brd; HDI drill pairs) — https://docs.arduino.cc/static/757d9262f8a7b1c02a77636ec1906780/ABX00162-cad-files.zip
5. Arduino, "Intended Use and Security Model" v1.2 (03/07/2026) — https://docs.arduino.cc/tutorials/security/intended-use-and-security-model/
6. Arduino blog, UNO Q pricing change (26 Jun 2026; USD 44→59, 59→79 from 6 Jul) — https://blog.arduino.cc/2026/06/26/a-heads-up-on-the-arduino-uno-q-board-pricing-straight-from-marcello-majonchi/
7. CNX Software, "Qualcomm acquires Arduino, introduces Arduino UNO Q" (Oct 2025) — https://www.cnx-software.com/2025/10/07/qualcomm-acquires-arduino-introduces-arduino-uno-q-dual-brain-sbc/
8. CNX Software, UNO Q 4 GB at USD 59 (Jan 2026) — https://www.cnx-software.com/2026/01/21/arduino-uno-q-4gb-board-with-4gb-ram-32gb-storage-available-59/
9. DigiKey ABX00173 — https://www.digikey.com/en/products/detail/arduino/ABX00173/27526618 ; Mouser Arduino computing (USD 59 / 79 snapshot) — https://www.mouser.com/c/embedded-solutions/computing/?m=Arduino
10. India retail ABX00162: Electropi (INR 4,417 ex-GST) — https://www.electropi.in/official-arduino-uno-q-single-board-computer-abx00162 ; MakerBazar (INR 4,151.69 ex-GST) — https://makerbazar.in/products/arduino-uno-q-ai-single-board-computer ; Robocraze (INR 4,652) — https://robocraze.com/products/official-arduino-uno-q-sbc
11. Qualcomm Dragonwing QRB2210 Product Brief, Rev D (no Ethernet / PCIe listed; 0.4 mm pitch; Tj -30..95 °C; longevity May 2034; Debian 13 / Yocto; kernel 6.16) — https://docs.qualcomm.com/doc/87-61720-1/87-61720-1_REV_D_Qualcomm_Dragonwing_QRB2210_Processor_Product_Brief.pdf
12. Qualcomm Product Longevity Program — https://www.qualcomm.com/internet-of-things/products/product-longevity-program
13. QRB2210 security features (secondary): datasheets.com — https://datasheets.com/qualcomm/qrb2210 ; Thundercomm RB1 — https://thundercomm.com/product/qualcomm-robotics-rb1-platform
14. Qualcomm Dragonwing docs, "Enable secure boot" (QFPROM, SecTools v2 for licensed users, ChipCode, OEM ID) — https://dragonwingdocs.qualcomm.com/System/Security/enable-secure-boot
15. Mainline DTS `qrb2210-arduino-imola.dts` — https://kernelsources.org/source/xref/linux/arch/arm64/boot/dts/qcom/qrb2210-arduino-imola.dts ; patch series v3 — https://patchew.org/linux/20251120155825.121483-1-r.mereu.kernel@arduino.cc ; DSI/DP bridge — https://lkml.iu.edu/hypermail/linux/kernel/2602.1/07343.html
16. Armbian UNO Q (Debian trixie, mainline 7.1 edge) — https://www.armbian.com/boards/arduino-uno-q ; Arduino forum (Debian 13.4, kernel 6.16) — https://forum.arduino.cc/t/have-no-hdmi-log-in-after-doing-full-upgrade/1443461
17. DigiKey QRB-2210-0-NSP752-MT-00-0 (USD 14.55 @1, 1,561 stock, 28 wk) — https://www.digikey.com/en/products/detail/qualcomm/QRB-2210-0-NSP752-MT-00-0/27904332
18. Thundercomm TurboX C2210 SoM (quote only) — https://www.thundercomm.com/product/c2210-som/
19. eInfochips Aikri-22X-10LS-3 QRB2210 SoM: Arrow (USD 44.66, "supplier unconfirmed", -30..85 °C) — https://www.arrow.com/en/products/aikri-22x-10ls-3/einfochips-limited ; product page (Yocto Dunfell, kernel 5.4) — https://www.einfochips.com/products/aikri-qrb2210-aikri-22x-10ls-3/
20. Lantronix Open-Q 2210RB SiP: Arrow QC-SIP-2210RB-A (USD 87.92 @21+, 26 wk) — https://www.arrow.com/en/products/qc-sip-2210rb-a/lantronix ; Open-Q 2200 series brief (-25..85 °C, 35 × 35 LGA) — https://cdn.lantronix.com/wp-content/uploads/pdf/LAN-OpenQ-2200-SIP-PB-MPB-00160B-US-031323-2.pdf
21. Zephyr board Arduino UNO Q — https://docs.zephyrproject.org/latest/boards/arduino/uno_q/doc/index.html
22. CNX Software, STM32MP23 (A35 + M33, 2 × GbE TSN, 16-bit DDR3L/DDR4/LPDDR4, -40..125 °C, 0.8 mm packages, 10-year, from USD 8.46 @1k) — https://www.cnx-software.com/2025/04/08/stmicro-stm32mp23-cortex-a35-m33-mpu-features-a-600-gops-npu-for-industrial-iot-and-ml-applications/
23. ST eStore STM32MP233 (USD 18.63–27.17 @500, out of stock) — https://estore.st.com/en/products/microcontrollers-microprocessors/stm32-arm-cortex-mpus/stm32mp2-series/stm32mp233.html ; ST STM32MP233D — https://www.st.com/en/microcontrollers-microprocessors/stm32mp233d.html
24. STM32MP231CAJ3: Future Electronics (USD 12.77 @504) — https://www.futureelectronics.com/p/semiconductors--microprocessors--digital-signal-processors/stm32mp231caj3-stmicroelectronics-4205122 ; Octopart (USD 12.96) — https://octopart.com/part/stmicroelectronics/STM32MP231CAJ3
25. TI AM623x prices (aggregator; 1ku): AM6232ATGGHAALW — https://www.edinventory.com/parts/am6232atgghaalw_texas-instruments ; AM6231ASGGGAALW — https://www.edinventory.com/parts/am6231asgggaalw_texas-instruments ; DigiKey AM6231ASGGGAALW — https://www.digikey.com.mx/en/products/detail/texas-instruments/AM6231ASGGGAALW/17748395
26. Zephyr SK-AM62 M4F (`sk_am62/am6254/m4`) — https://docs.zephyrproject.org/latest/boards/ti/sk_am62/doc/index.html
27. Toradex Verdin AM62 (volume from USD 31.90) — https://toradex.com/computer-on-modules/verdin-arm-family/ti-am62
28. i.MX8M Mini MIMX8MM6CVTKZAA: Future (USD 20.92 @1k) — https://www.futureelectronics.com/p/semiconductors--microprocessors--embedded-processors/mimx8mm6cvtkzaar-nxp-5166441 ; DigiKey — https://www.digikey.co.uk/en/products/detail/nxp-usa-inc/MIMX8MM6CVTKZAA/9857781
29. i.MX91 vs i.MX93 (i.MX91 has no M33; both 2 × GbE): CNX — https://www.cnx-software.com/2023/05/30/nxp-i-mx-91-single-core-cortex-a55-soc-to-power-linux-based-cost-optimized-edge-devices/ ; NXP AN14012 — https://nxp.com/docs/en/application-note/AN14012.pdf ; PHYTEC — https://www.phytec.de/en/produkte/system-on-modules/phycore-imx-91-93/
30. MYiR MYC-LD25X (STM32MP25, Debian 12): CNX — https://cnx-software.com/2024/09/26/myir-tech-myc-ld25x-a-compact-stm32mp25-system-on-module-running-debian-12 ; DigiKey BG (EUR 159.35 @1) — https://www.digikey.bg/en/products/detail/myir-tech-limited/MYC-LD257-8E2D-150-I/25928197
31. LCSC RTL8152B-VB-CG C50656 (USD 0.858 @980) — https://www.lcsc.com/product-image/C50656.html
32. Debian security FAQ (3 years from release) — https://www.debian.org/security/faq ; Debian LTS (trixie LTS 2028-08-09 to 2030-06-30) — https://wiki.debian.org/LTS
33. CIP isar-cip-core (Debian + CIP kernel; secure boot, SWUpdate, signing docs) — https://gitlab.com/cip-project/cip-core/isar-cip-core ; README — https://gitlab.com/cip-project/cip-core/isar-cip-core/-/raw/master/README.md
34. Freexian Extended LTS (not fetched; UNVERIFIED) — https://www.freexian.com/lts/extended/
35. Cockpit project (not fetched; feature claims UNVERIFIED) — https://cockpit-project.org/
