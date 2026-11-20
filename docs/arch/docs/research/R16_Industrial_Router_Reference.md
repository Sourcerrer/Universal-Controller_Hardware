# R16 — Industrial Cellular Router / Gateway Reference Architectures

Date: 2026-11-14. Status: COMPLETE WITH GAPS. FX: 1 USD = INR 93.9. Numbered sources are in section 9.
Markers: **INFERRED** = deduced from clock speed, family or photos, not from a document that names the part. **UNVERIFIED** = not confirmed by any source.

Scope: how established industrial router makers (Teltonika, Robustel, InHand, Milesight, USR, Four-Faith, Advantech, Digi, Moxa, Sierra/Semtech) build their products, as a reference for our modular gateway. Module selection and the cheap-router price survey are in R15. Linux and RTOS trade-offs are in R09. CRA and RED rules are in R01. This report cites those reports and does not repeat them.

Access limits in this run:
- fccid.io, fcc.report and apps.fcc.gov were blocked by Cloudflare or Akamai. FCC exhibit lists could be read, but internal-photo PDFs could not be opened.
- The Teltonika wiki and CDN were also blocked. Teltonika datasheets were read from distributor mirrors instead (axilogi, gowifi).
- Chip IDs therefore come from OpenWrt commits and device trees, TechInfoDepot, FCC "contains FCC ID" notes, vendor datasheets and developer or forum logs. No part was identified from photos.

---

## 1. Summary of lessons

1. **Two main architectures cover almost every product.**
   - **(A) Router SoC + cellular module.** The modem is a plain USB data pipe (QMI or ECM). This is the dominant pattern.
     - SoCs: MT7628, QCA9531, IPQ4018, NXP i.MX6UL-class, ARM926.
     - Wi-Fi and the Ethernet switch come from the router SoC.
   - **(B) "Gateway board": the router firmware runs on the modem's own application core.** Teltonika's whole TRB1 line works this way: TRB140/141/142/145, plus TRB160 and TRB500. So does Sierra/Semtech's FX30.
     - **No pattern-B product found has Wi-Fi.**
     - Ethernet is one port, through the modem's SGMII and an external PHY.
2. **Pattern B is confirmed for the TRB140, not just guessed.** The evidence:
   - Teltonika's TRB1 SDK builds an `openwrt-gpl-mdm9x07` target [3].
   - A TRB140 kernel log shows RutOS on Linux **5.4.302** with `mdm9607` regulator drivers [4].
   - Another log shows the device-tree model "Teltonika TRB14X" [5].
   - The datasheet CPU line, "ARM Cortex-A7 1.2 GHz, 128 MB DDR2", is the MDM9x07 app core [1]. Early datasheets even said "OpenLinux based OS … Yocto SDK" [2].

   Teltonika forward-ported the MDM9607 BSP from Quectel's 3.18 kernel [28] to 5.4. Without that, a CRA-grade support life would not be possible. That is a large engineering effort.
3. **Teltonika adds a separate router SoC whenever it needs Wi-Fi, RS-232/RS-485 plus I/O, or more than one Ethernet port.**
   - The RUT200 uses an **EC200A** as a *USB modem* next to an MT7628 [19]. The EC200A is the same module R15 proposes to run alone in QuecOpen mode. So the market leader does not use EC200A QuecOpen for Wi-Fi + Ethernet.
   - No established industrial product was found that uses a modem's SDIO Wi-Fi plus its RMII/SGMII Ethernet together. The pattern exists only in cheap MiFi/CPE gear (R15 §3).
4. **The cheapest industrial product is not the single-chip one.**
   - In Indian retail, the RUT200 (MT7628 + EC200A + Wi-Fi + 2 Ethernet) sells for INR 7,569–13,700 [51][52].
   - The TRB140 (single chip, EC25, no Wi-Fi) sells for INR 20,000 [51].
   - The modem's price dominates. An MDM9607 OpenLinux module costs about INR 2,900 at 1k [R09]. An EC200A plus an MT7628 (USD 2.26, about INR 212 [R09]) costs less.
   - Pattern B saves the SoC, DDR and flash, but only if the modem that can host Linux is not itself more expensive.
5. **The same modem footprint is reused across SKUs and suppliers.**
   - The RUT241 has shipped with a MeigLink SLM750 [18], and its FCC filing records a change from EC25-AF to EG25-G [24].
   - The RUT906 and RUT956 share one board, with a Meig SLM770A or a Quectel EC25-EUX [20].
   - The RUTX11 moved from EG06 to EG060K [26].

   Pattern A lets vendors swap modems freely. Our 4G card should keep that freedom: an LGA family footprint, and a firmware layer that does not depend on one vendor's SDK.
6. **Power input: most products accept 9–30 V or more, with reverse-polarity and surge protection.** Teltonika uses 9–30 V on the TRB/RUT2/RUT9 lines and 9–50 V on the RUTX. Robustel and InHand use 9–36 V, Milesight and Advantech 9–48 V, Robustel R2000 Dual 9–57 V.
   - **Our 9–24 V module input is narrower than every reference.**
   - Typical draw is 1–2 W idle and 3.5–7 W peak for Cat-4 routers without PoE.
7. **Security and update practice to match for the CRA:**
   - public per-release CVE lists, with "Stable" and "Latest" channels (Teltonika) [45];
   - a security centre or PSIRT [46];
   - IEC 62443-4-1 process certification [48];
   - EN 18031-1/-2 and EN 303 645 on radio products [47];
   - authenticated boot, encrypted storage and signed updates (Digi TrustFence [42]).

   Even Teltonika ships high-severity CVEs regularly: CVE-2023-32349 (CVSS 8.0) on 18 RUT/RUTX models [50], and 9 CVEs fixed in RutOS 7.24 [45]. Plan for monthly-scale patching.
8. **Recommendation for our 4G card:** follow the TRB14x pattern (modem as the only processor, Ethernet MAC in the modem, one PHY, one port) and **leave Wi-Fi to the existing ESP32-C6 card**. Section 6 gives the details and the fallback.

---

## 2. Reference product table

Legend:
- "FW on modem" = router OS runs on the cellular module's application core.
- RAM/flash are totals.
- Prices are retail snapshots, qty 1, undated unless stated, converted at INR 93.9/USD.

| Product | Main SoC / CPU | Cellular module | FW on modem | Wi-Fi | Ethernet | RAM / flash | Power input, protection, draw | IO / serial | OS | Price | Src |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **Teltonika TRB140** | none separate. Cortex-A7 1.2 GHz = Qualcomm MDM9607 in the modem (log shows `mdm9607`) | Quectel EC25 (EC25-AU, EC25-EU seen in field) | **Yes** | none | 1x 10/100/1000. SGMII + external PHY; PHY "chip update" PCN 2025. PHY part UNVERIFIED; AR8033 is the only EC25-supported PHY per Quectel [29] | 128 MB DDR2 / 512 MB | 9–30 V, rev-pol, surge >31 V 10 µs; <5 W | 1 DI (0–6 V low, 8–30 V high), 1 DO OC 30 V/300 mA | RutOS (OpenWrt-based), kernel 5.4 on MDM9607 | INR 19,999 (ThinkRobotics); USD 247.97 = INR 23,284 (Walmart) | [1][2][3][4][27][51][53] |
| TRB141 | same MDM9x07 core | Cat 1 module, part UNVERIFIED (EC21 class INFERRED) | **Yes** | none | none (micro-USB virtual NIC only) | 128 / 512 MB | 9–30 V, same protection; <5 W | 3 DI (1 isolated, 7.3–71 V = "1"), 1 AI 0–30 V or 4–20 mA, 2 relays (one latching), 1 OC DO | RutOS | — | [6] |
| TRB142 / TRB145 | same | Cat 1, UNVERIFIED | **Yes** | none | none listed (micro-USB virtual NIC) | 128 / 512 MB | 9–30 V; <5 W | TRB142 RS-232 DB9; TRB145 RS-485 2/4-wire | RutOS | — | [7][8] |
| TRB160 | "Qualcomm 1.2 GHz Cortex-A7" (modem app core INFERRED) | Cat 6 module UNVERIFIED | **Yes** (INFERRED) | none | 1x GbE | 128 / 256 MB | 9–30 V class | 1 DI / 1 DO | RutOS | — | [9] |
| TRB500 (5G) | "single-core Cortex-A7 1.5 GHz" (= SDX55 app core INFERRED) | 5G module UNVERIFIED | **Yes** (INFERRED) | none | 1x GbE | 256 / 512 MB | 9–30 V, rev-pol, surge ±1 kV 50 µs; idle <3 W, max <6 W | 1 DO | RutOS | — | [10] |
| TRB245 | Qualcomm QCA9531 MIPS 24Kc 650 MHz (vendor "Qualcomm, MIPS 24kc, 650 MHz") | Cat 4, part UNVERIFIED | No | none (TRB2 family: no Wi-Fi, no USB [56]) | 1x 10/100 | 64 MB DDR2 / 16 MB SPI NOR | 9–30 V, rev-pol, surge ±1 kV 50 µs; idle <1.2 W, max <5 W | 3 DIO, 1 AI 0–30 V, RS-232 + RS-485 (16-pin) | RutOS | — | [11] |
| TRB246 | MediaTek 580 MHz MIPS 24KEc (MT7628 INFERRED) | Cat 4 UNVERIFIED | No | none | 1x 10/100 | 128 / 16 MB | 9–30 V; idle <1.5 W, max <3.5 W | as TRB245 | RutOS | — | [12] |
| **RUT200** | **MediaTek MT7628AN** | **Quectel EC200A** (USB, ECM via `AT+QNETDEVCTL`) | No | MT7628 2.4 GHz 11n | MT7628 switch, 2x 100M | 128 MB EtronTech EM68C16CWQG / 16 MB Winbond W25Q128 | 9–30 V, rev-pol, surge >31 V 10 µs | 1 DI / 1 DO | RutOS; also upstream OpenWrt | INR 7,569 (IndiaMART) to 13,700 (ThinkRobotics) | [14][19][51][52] |
| **RUT241** | MT7628AN | MeigLink SLM750 (hw ≤ v4); FCC PC: EC25-AF to EG25-G | No | MT7628 | 2x 100M | 128 / 16 MB (same chips) | 9–30 V; <6.5 W | 1 DI / 1 DO | RutOS / OpenWrt | INR 23,999 (ThinkRobotics) | [15][18][24][51] |
| **RUT956** | MT7628AN | Quectel EC25-EUX (RUT906: Meig SLM770A); FCC ID 2AET4RUT956AF | No | MT7628 2x2 11n | 4x 100M | 128 / 16 MB | 9–30 V, rev-pol, surge; idle <2 W, max <7 W; passive PoE in | RS-232 via Cypress USB-UART (ttyACM0); RS-485 on SoC UART with GPIO TX/RX enable, 2- or 4-wire; IO via 74HC595 (spi-gpio), ADC MCP3221 or TI TLA2021; 1 dry DI, 1 isolated DI 0–30 V, 1 AI 0–24 V, DOs | RutOS / OpenWrt | USD 169–257.90 = INR 15,869–24,217 | [16][20][25][53] |
| RUTX11 | Qualcomm IPQ4018 4x A7 717 MHz | Quectel EG06-A (FCC XMR201807EG06A), changed to EG060K (PCN 2024) | No | IPQ4018 integrated 2.4 + 5 GHz, Wi-Fi 5 | QCA8075 PHY, 4x GbE | 256 MB DDR3 / 256 MB SPI-NAND XTX XT26G02A + 16 MB NOR XT25F128B | **9–50 V**, rev-pol, surge; passive PoE 9–50 V; 16 W max | 1 DI / 1 DO | RutOS (OpenWrt EOL for it) | USD 366 = INR 34,367 | [17][22][23][26][53] |
| OTD140 (outdoor) | MediaTek 580 MHz MIPS 24KEc (MT7628 INFERRED) | Cat 4 UNVERIFIED | No | none | 2x 100M, PoE-in 802.3af/at, PoE-out 15 W | 128 / 16 MB | PoE 42.5–57 V, rev-pol, surge; idle <2.5 W, max <6 W (PoE max <21 W) | — | RutOS | — | [13] |
| Robustel R1510 | "Qualcomm" MIPS 650 MHz (QCA9531 INFERRED) | UNVERIFIED | No | 2x2 11n 300 Mbps (SoC radio INFERRED) | 2x 100M, 1.5 kV magnetic isolation | 128 / 16 MB (SDK: 64 MB / 4 MB) | 9–36 V; idle 100 mA @ 12 V (1.2 W) | 1 DI / 1 DO | RobustOS (Linux + C/C++ SDK) | — | [32][33] |
| Robustel R2000 | not published | — | No | — | — | SDK 16 MB / 4 MB | 9–36 V (Ent); 9–57 V (Dual) | RS-232/RS-485 shared on one RJ11 | RobustOS | — | [34] |
| InHand IR302 | 580 MHz (MT7628 INFERRED) | Cat 1 or Cat 4, UNVERIFIED | No | 2.4 GHz 11n | 2x 100M, 1.5 kV isolation transformers | 128 MB DDR2 / 32 MB SPI | 9–36 V, over-current + reverse protection; 2–5 W typ, <10 W peak | RS-232/RS-485 combo | InHand Linux | USD 160–180 = INR 15,024–16,902 | [35][55] |
| InHand IR615-S | not found | — | No | 11n | — | — | 9–26 V; 150–320 mA @ 12 V | — | — | — | [36] |
| Milesight UR35 (UR32 same core) | NXP Cortex-A7 528 MHz (i.MX6UL/ULL INFERRED) | Cat 4 UNVERIFIED | No | 2.4 GHz 11n optional (separate chip INFERRED: i.MX6UL has no radio) | UR35 5x FE (UR32 2x), optional 802.3af/at PSE | 128 MB DDR3 / 128 MB + microSD | 9–48 V, surge + reverse; HW watchdog | RS-232 + RS-485 (2x 485 option); DI dry, DO wet, galvanically isolated | Linux + Python SDK | UR32 Pro USD 184 = INR 17,278; Lite USD 138 = INR 12,958 | [37][38][54] |
| Milesight UG65 (LoRaWAN GW) | NXP quad A53 1.5 GHz (i.MX8M Mini/Nano INFERRED) | optional Cat 4 | No | 2.4 GHz 11n | 1x GbE, PoE PD 802.3af | 512 MB DDR4 / 8 GB eMMC | 9–24 V jack or PoE; 2.9 W typ, 4.2 W max | — (SX1302 LoRa concentrator) | Linux, Node-RED, Python, built-in LNS | USD 340–467.5 = INR 31,926–43,898 | [39][54] |
| USR-G806 | 580 MHz (MT7628 INFERRED) | Cat 4 + TD-SCDMA + GSM, UNVERIFIED | No | 2.4 GHz | 1 WAN + 1 LAN 10/100 | — | **5–36 V**; 150 mA avg, 385 mA max @ 12 V | — | vendor Linux | — | [31] |
| Four-Faith F3826 | "industrial 32-bit CPU" | — | No | 11n | — | 128 MB / 16 MB | family 5–35 V (F3824), rev + over-voltage | — | — | — | [40] |
| Advantech ICR-2431 | ARM926EJ-S 600 MHz | Cat 4 UNVERIFIED | No | none | 2x 100M | 128 MB / 64 MB NOR | 9–48 V on 6-pin with IO; idle 2 W, avg 3.5 W, peak 10 W; EN 61000-4-2..-11, EN 62368-1 | RS-232 + RS-485, DI 36 V, DO open-drain 36 V/100 mA; HW watchdog | Linux + Router Apps (C, Python) | — | [41] |
| Digi IX10 | not published | Cat 4 | No | none | 1x Eth | 256 / 256 MB | 9–30 V, rev-pol, 1 A max; 1.5 W light, 3.5 W peak | RS-232/485 | DAL OS; TrustFence: authenticated boot, encrypted storage, secure updates | — | [42] |
| Sierra/Semtech FX30 | none separate: app on WP7702 module (A7 1.3 GHz) | WP7702 (Cat-M1/NB1) | **Yes** | none | Ethernet *or* RS-232/485, depending on variant | 128 MB RAM / 256 MB for app | 4.75–32 V | 3 IO | Legato LTS Linux | — | [43] |
| Moxa OnCell G3150A-LTE | not published | Cat 4 | No | none | 2x Eth | — | dual inputs, isolated, rev-pol; 0.7 A @ 12 V, 0.2 A @ 48 V | RS-232/422/485 | Moxa OS, "IEC 62443-based" features; phased out for G4302 | — | [44] |

Not covered: InHand IG502, Siemens SCALANCE M804PB and Four-Faith F3426 internals. No usable documents were reachable within the search budget.

---

## 3. Architecture patterns

### 3.1 Pattern A — router SoC + USB cellular module (most products)

- **Silicon.** MT7628AN (RUT200/241/956, TRB246, OTD140; INFERRED for IR302 and USR-G806), QCA9531 (TRB245; INFERRED for R1510), IPQ4018 (RUTX11), NXP i.MX6UL-class (Milesight UR3x, INFERRED), ARM926 (Advantech ICR-2000).
  - MT7628 includes a 580 MHz MIPS core, a 2.4 GHz 2x2 11n MAC/BB/radio and a 5-port 10/100 switch [57].
  - The SoC supplies the Ethernet MAC/switch and, on MT7628/QCA9531/IPQ4018, the Wi-Fi radio too. One chip does router + switch + Wi-Fi.
- **Modem link.** USB 2.0, with the modem as a QMI (EC25, uqmi) or CDC-ECM (EC200A, Meig) network device [19][20]. The SoC controls the modem through GPIOs: power key, reset, SIM select, eSIM select and status [20].
- **IO extension.** The RUT956 drives its DI/DO and LEDs through a 74HC595 chain on bit-banged SPI. Its analogue input uses an I²C ADC (MCP3221, or TI TLA2021 as a second source). RS-232 is a USB-to-UART bridge, and RS-485 sits on a SoC UART with GPIO driver and receiver enables [20]. Cheap SoC, cheap glue logic.
- **Memory.** MT7628 products use 128 MB DDR2 and 16 MB SPI NOR [18][19][20]. This is enough for OpenWrt today, and upstream OpenWrt supports these boards (commits 2025) [18].
- **Why it wins in industry.** The modem is replaceable (Meig to Quectel, EC25 to EG25 to EC200A) without touching the OS. One OS (RutOS) runs on every SoC. Upstream OpenWrt gives long-lived security fixes. The cost is a second processor plus DDR and flash.

### 3.2 Pattern B — router firmware on the modem's application core ("single-chip")

| Product | Module / core | Ethernet | Wi-Fi | Evidence |
|---|---|---|---|---|
| Teltonika TRB140/141/142/145 | Quectel EC25 / Cat 1 family, MDM9607 A7 1.2 GHz | TRB140: 1x GbE via SGMII + PHY; others: none (RS-232, RS-485 or IO instead) | none | SDK target `mdm9x07` [3]; kernel 5.4.302 log with `mdm9607` drivers [4]; "TRB14X" device tree [5]; datasheet CPU line [1] |
| Teltonika TRB160 | Qualcomm A7 1.2 GHz, Cat 6 | 1x GbE | none | datasheet [9]; module UNVERIFIED |
| Teltonika TRB500 | A7 1.5 GHz (SDX55 INFERRED), 5G | 1x GbE | none | datasheet [10] |
| Sierra/Semtech FX30 | WP7702, A7 1.3 GHz, Legato Linux | Ethernet *or* serial variant | none | datasheet [43] |

What the module offers (Quectel EC25/EC21/EC20 QuecOpen R2.0) [28]:
- Cortex-A7 up to 1.2 GHz, about 100 MB RAM and 100 MB flash free for user code;
- Linux 3.18 with the LK bootloader;
- **1x SGMII** (Ethernet PHY) and **2x SDIO**, one meant for Wi-Fi (Quectel FC20), the other for SD/eMMC.
- Quectel staff say the standard EC25 supports only the **AR8033** PHY. Other PHYs need a driver ported in OpenLinux [29], and DP83867 was refused on the EG25-G [30].

**So yes: a Linux/OpenCPU cellular module can drive Ethernet and Wi-Fi alone.**
- MDM9607 modules have SGMII + SDIO: EC25, EG25-G, EC21 R2.0, SIM7600 and MeiG SLM750 [28][R09].
- ASR1803 modules have RMII/RGMII + SDIO in QuecOpen mode, per Quectel's reference design (R15 §2): EC200A, and possibly Gosuncn GM520.
- UNISOC Cat-1 modules (EC200U, EG800, EC800M) have **no** Ethernet MAC and no Wi-Fi AP (R15).

**But no established vendor ships pattern B with Wi-Fi.** Teltonika uses pattern B only for single-purpose "gateway boards": one Ethernet port *or* one serial port, no Wi-Fi. It moves to pattern A as soon as Wi-Fi or a switch is needed, even with a modem (EC200A) that has SDIO.

Likely reasons (INFERRED):
- Wi-Fi driver support inside the vendor BSP is thin.
- Running Wi-Fi AP work on the same core as the modem stack risks the modem.
- Wi-Fi + LTE coexistence in one module needs extra RF certification.
- Router SoCs with integrated Wi-Fi cost about USD 2.3 [R09].

**What pattern B costs Teltonika.** It maintains its own BSP: RutOS on a 5.4 kernel instead of Quectel's 3.18 [4][28]. It also handles modem firmware as a separately packaged image. A TRB140 user needed Quectel to supply an EC25-AU image and Teltonika to repackage it, after 3G shutdown broke SMS [4]. A Q4 2023 PCN changed the modem firmware on all new TRB140s [27].

### 3.3 Pattern C — application gateway (edge computing)

Milesight UG65 (quad A53, 512 MB DDR4, 8 GB eMMC, Node-RED, Python, built-in LoRaWAN NS) [39]. Milesight UR3x and Advantech ICR also offer Python and C SDKs [37][41]. This pattern costs the most and is not a cost reference for our modules. Its lesson is software: customers expect a scripting or SDK layer and a remote-management cloud (DeviceHub, RMS, RCMS, WebAccess/DMP).

### 3.4 Modular / stackable

None of the products studied is a side-by-side stackable system. All are fixed-function boxes, with variety handled by **SKU families on one shared board**:
- RUT906 and RUT956 share one PCB and one DTS [20];
- RUT200 and RUT241 share `rut2xx.dtsi` [18][19];
- TRB141/142/145 differ only in IO.

Expansion-port products (Advantech ICR-3200 expansion ports, Siemens SCALANCE M) were not researched and are UNVERIFIED. Our modular stack is therefore a differentiator. It cannot rely on a proven industrial precedent for the bus, hot-plug, ESD at exposed connectors or multi-firmware updates (see R01 and R07).

### 3.5 Where Ethernet and Wi-Fi come from

| Source of Ethernet | Products |
|---|---|
| Router-SoC switch, internal PHYs (100M) | MT7628 / QCA9531 products |
| SoC MAC + external PHY or switch (GbE) | RUTX11 (QCA8075) |
| Modem SGMII + external GbE PHY | TRB140/160/500 |
| Modem RMII + 10/100 PHY | Only in Quectel's EC200A QuecOpen reference and cheap CPEs (R15); no industrial product found |

| Source of Wi-Fi | Products |
|---|---|
| Integrated in router SoC | MT7628, QCA9531, IPQ4018 |
| Separate chip on host SoC | Milesight (INFERRED) |
| From modem SDIO | No industrial product found |

---

## 4. Power input design

| Range | Products |
|---|---|
| 5–36 V / 5–35 V | USR-G806 [31], Four-Faith family [40] |
| 4.75–32 V | Sierra FX30 [43] |
| **9–30 V** | Teltonika TRB/RUT2xx/RUT9xx [1][11][14][16], Digi IX10 [42], TRB500 [10] |
| 9–36 V | Robustel R1510, R2000 Ent [32][34]; InHand IR302 [35] |
| 9–48 V | Milesight UR3x [37], Advantech ICR-2431 [41] |
| 9–50 V | Teltonika RUTX11 (+ passive PoE 9–50 V) [17] |
| 9–57 V | Robustel R2000 Dual [34] |
| 9–24 V | Milesight UG65 (indoor, jack + PoE) [39] |
| 9–26 V | InHand IR615 [36] |

Protection as stated:
- **Reverse polarity** on every product with a published spec.
- Surge stated in two ways:
  - Teltonika older TRB/RUT: "**>31 VDC 10 µs max**", i.e. a TVS clamp just above the 30 V maximum [1][14];
  - Teltonika newer TRB2/TRB500: "**±1 kV 50 µs**", the EN 61000-4-5 test level [10][11].
- InHand adds **over-current** protection [35]. Moxa uses dual, isolated inputs [44]. InHand and Robustel use 1.5 kV Ethernet magnetics [32][35].
- EMC test lists are similar everywhere: EN 61000-4-2/-3/-4/-5/-6/-11 [11][41]. Robustel R1510 claims only **Level 2** ESD/RS/EFT [32]; Teltonika and Advantech list the standards without levels in the lines read.

Consumption (Cat-4 class, no PoE):
- idle about 1.2–2.5 W: TRB245 <1.2 W, R1510 1.2 W, RUT956 <2 W, ICR 2 W, OTD140 <2.5 W;
- peak about 3.5–7 W: TRB246 3.5 W, IX10 3.5 W, TRB140 <5 W, TRB500 <6 W, RUT956 <7 W;
- RUTX11 (IPQ4018 + Cat 6 + Wi-Fi 5) reaches 16 W [17].

The modem's TX bursts set the peak. Size each module's regulator and backup cell for about 2 A at 3.8 V peaks (see R06).

---

## 5. Lowest-BOM pattern and what it means for our 4G + Ethernet + Wi-Fi module

1. **Lowest BOM for "4G + Ethernet only" is pattern B** (TRB14x): modem + PHY + magnetics + RJ45 + power, with no SoC, DDR or flash. This works with an EC200A-class module whose QuecOpen exposes RMII (cheaper than MDM9607; R15 §1 gives about INR 1,510 BOM for the card without Wi-Fi). It also works with an EC25/EG25 via SGMII + AR8033, but the module costs about INR 2,900 [R09].
2. **Lowest BOM for "4G + Ethernet + Wi-Fi" in industrial practice is pattern A** with MT7628 + a cheap USB modem (RUT200). The SoC costs about USD 2.3, but it adds DDR, flash and a second processor, which our current rule forbids (R15 §2).
3. **Pattern B + SDIO Wi-Fi** (EC200A QuecOpen + RTL8192ES, R15's option) is the lowest-part-count way to meet the "one processor" rule. **No established industrial vendor ships it.** It depends on:
   - an NDA SDK;
   - an unpublished security-patch policy;
   - a variant conflict over SDIO support (R15 §2 note);
   - a Linux-or-RTOS uncertainty for EC200A builds (R15 §1).

**Which modules can host Ethernet and Wi-Fi alone?**

| Module family | Ethernet MAC | Wi-Fi port | Notes |
|---|---|---|---|
| EC25 / EG25-G / EC21 R2.0 (MDM9607) | SGMII | SDIO | Linux 3.18, AR8033 PHY [28][29][30] |
| SIM7600 / SLM750 (MDM9607) | same as above, per platform | same as above | [R09] |
| EC200A (ASR1803) | RMII/RGMII | SDIO | QuecOpen; R15 [S1] |
| UNISOC Cat-1 / Cat-1 bis | none | none | R15 |
| WP77xx (Legato) | via its own design | — | Ethernet path UNVERIFIED |

---

## 6. Recommendations

### 6.1 4G + Ethernet (+ Wi-Fi) module

1. **Adopt the TRB14x architecture for the 4G card.** The cellular module is the only processor, with its internal MAC, one PHY (the PHY its SDK supports: YT8512H for EC200A, AR8033 for MDM9607) and one RJ45.
   - Run the card's firmware on the module: QuecOpen, or plain AT with a host-side stack.
   - This meets the "MAC inside a chip" and "no separate host" rules, and matches a product category (Teltonika TRB) that sells in volume.
2. **Do not put Wi-Fi on the 4G card. Use the ESP32-C6 Wi-Fi/BLE card for Wi-Fi.** This matches the reference split: Teltonika's single-chip boards have no Wi-Fi, and Wi-Fi products use a radio-capable SoC.
   - It removes LTE/Wi-Fi co-location from one module.
   - It avoids the unproven EC200A SDIO Wi-Fi path.
   - The stack already has the Wi-Fi radio.
   - The routing then becomes: Wi-Fi client or AP on the C6 card, bridged over the 40-pin bus; LTE and Ethernet on the 4G card. **Define this bus traffic model early.** The bus throughput budget (UART, SPI or USB lanes on the 40-pin connector) is UNVERIFIED against Cat-4 rates.
   - If the owner insists on Wi-Fi on the 4G card, use R15's EC200A-CN + RTL8192ES reference, and treat it as a first-of-kind design with extra certification and SDK risk.
3. **Keep modem freedom (lesson 5).**
   - Lay out the card for one Quectel LGA family footprint (pin compatibility of EC200A with EC25/EG25 is UNVERIFIED, so check the Quectel compatibility note).
   - Keep the application layer behind a thin abstraction, so that an AT/ECM fallback (EC200A as a plain modem, controlled by the baseboard) remains possible if the QuecOpen SDK or patches become unavailable.
4. **Ethernet details from the references.**
   - Use 1.5 kV magnetics (InHand, Robustel).
   - Use 10/100 unless GbE is required: Teltonika's GbE needs SGMII, and only MDM9607 or newer Qualcomm modules have it.
   - Take the MAC address from the module, or from an EEPROM on the card.
5. **Firmware ownership.** Teltonika could ship pattern B only by owning a 5.4 kernel BSP for MDM9607 [4]. We cannot do that.
   - Before design-in, get Quectel's written commitment on QuecOpen security fixes and baseband FOTA for the EC200A-CN.
   - Budget for packaging baseband updates ourselves, as Teltonika's `modem_updater` does [4].

### 6.2 Baseboard

1. **Widen the input range to 9–36 V on all modules** (the 9–30 V Teltonika floor, the 36 V Robustel/InHand standard), with reverse-polarity protection and a TVS clamp just above maximum (Teltonika states >31 V for a 30 V maximum).
   - Choose regulators with at least 60 V absolute-maximum input so that the TVS clamp voltage during EN 61000-4-5 ±1 kV surges stays below their rating. See R06 for parts.
   - A 24 V nominal field supply is common, so 24 V must sit mid-range, not at the limit.
2. **DI.** Use Teltonika-style thresholds (0–6 V low, 8–30 V high) and one wide isolated input type (TRB141: 7.3–71 V) [1][6]. Milesight isolates DI/DO galvanically [37]; our opto inputs (R14) already match.
3. **DO.** Open collector / high-side, 30 V 300 mA (Teltonika) or 36 V 100 mA (Advantech) [1][41]. Our TI quad high-side switch (R14) is at or above this level. Consider one latching relay as a SKU option (TRB141).
4. **AI.** Offer 0–30 V and 4–20 mA on the same input (TRB141) [6]. Use a second-source I²C ADC pair like Teltonika's MCP3221 / TLA2021 [20] if the STM32 ADC is not used.
5. **RS-485.**
   - Teltonika supports both 2-wire and 4-wire [8][16]. Milesight runs 300–230,400 bps [37].
   - None of the reference datasheets read states galvanic isolation on RS-485. **Our isolated RS-485 is above the reference level**, so keep it.
   - Add software-controlled termination and bias. Most references (UNVERIFIED) leave these to the installer.
6. **Hardware watchdog.** It is standard: Robustel, Milesight, Advantech [32][37][41]. Keep the window watchdog (R14).
7. **Temperature.** -40 to +75 °C (Teltonika, Advantech) is the benchmark. Robustel's R1510 is only -25 to +70 °C.

### 6.3 Modular concept

- References handle variety with **one board plus one DTS and SKU population options**, and one OS across all SoCs. Our stack has four firmware stacks (Zephyr on STM32H5, ESP32-C6, STM32WLE5, QuecOpen). **Make the baseboard the single update orchestrator.** It should verify and deliver signed images to each module, with A/B or rollback on each, so that one update and SBOM process covers the whole stack (CRA Annex I Part II, R01 §4).
- Offer a management cloud or remote-management protocol (RMS, DeviceHub, RCMS and DMP are standard features). LwM2M or MQTT-based device management on the baseboard is the low-cost equivalent.

---

## 7. Security and update practice to match (CRA)

| Practice | Reference | Our action |
|---|---|---|
| Public CVE list per firmware release, with severity | Teltonika wiki changelogs: RutOS 7.24 (8 Jul 2026) fixed 9 CVEs, 4 high; 7.24.2 two more [45] | Publish release notes with CVE IDs (CRA Annex I Part II (4)) |
| "Stable" vs "Latest" release channels | Teltonika [45] | Two channels; security fixes back-ported to Stable |
| Security centre / advisories | Teltonika security centre (critical CVE-2026-82104 dated 30 Oct 2026, page content only, not opened) [46]; CVE-2026-8914 command injection in RutOS 7.22–7.23.2 [49] | CVD policy, security.txt, PSIRT contact (CRA reporting since 11 Sep 2026 [R01]) |
| Process certification | Teltonika IEC 62443-4-1 [48]; Moxa "IEC 62443-based" features [44] | Run the SDL to IEC 62443-4-1 now; certify later |
| RED cyber | Teltonika RUTX50: EN 18031-1/-2 and ETSI EN 303 645 (June 2025) [47] | EN 18031-1/-2 for 4G and Wi-Fi SKUs until Dec 2027 [R01] |
| Authenticated boot, encrypted storage, signed updates | Digi TrustFence [42] | Secure boot on STM32H5 (PSA L3), signed images for every module; check the QuecOpen secure-boot option (UNVERIFIED) |
| Vendor signature on firmware | Teltonika tells users to check the digital signature [46]. Yet the OEM web UI accepts upstream OpenWrt factory images that carry only Teltonika metadata [18][19] (INFERRED: no enforced vendor-key check on RUT2xx) | Enforce signatures. If third-party firmware is allowed, make it a deliberate, logged unlock |
| Real-world exposure | CVE-2023-32349 (CVSS 8.0, UCI config utility to code execution) hit 18 RUT/RUTX models up to 00.07.03.4 [50] | Minimise exposed services and keep configuration utilities off the network |
| Support period | No public support-period statement found for Teltonika, Robustel or Milesight (UNVERIFIED) | CRA: declare a support period of at least 5 years [R01]. Pattern-B modules need the module vendor's patch commitment to cover it |

---

## 8. Risks

1. **Pattern B with Wi-Fi has no industrial precedent.** EC200A QuecOpen with SDIO Wi-Fi is unproven in shipped industrial products. Mitigation: Wi-Fi on the C6 card (6.1.2).
2. **SDK and patch dependence on the module vendor.** QuecOpen is NDA-only and has no public patch policy (R15). The MDM9607 path is Linux 3.18 unless a Teltonika-scale port is done [4][28]. This is a CRA risk for a Class I product [R01].
3. **PHY lock-in.** Module SDKs support only specific PHYs: AR8033 on EC25 [29], YT8512H/YT8521SC on EC200A (R15). AR8033 is reported hard to buy [29]. Qualify the PHY together with the module.
4. **Baseband firmware lifecycle.** Network changes such as 3G shutdowns or carrier certification can need modem firmware that only the module vendor can supply. Teltonika needed Quectel images and repackaging [4][27].
5. **Bus throughput for Wi-Fi bridged through the stack** is UNVERIFIED (6.1.2).
6. **Data gaps:**
   - FCC internal photos unreadable;
   - TRB14x PHY part, TRB141/142/145 Cat-1 module, TRB160 and TRB500 modules, all Milesight, InHand, USR and Robustel SoC part numbers are INFERRED or UNVERIFIED;
   - Siemens, Moxa CPU, IG502 and F3426 not covered;
   - prices are undated retail snapshots.

---

## 9. Sources

1. Teltonika TRB140 datasheet (mirror) — https://download.axilogi.com/Teltonika/Datasheet/TRB140.pdf
2. Teltonika TRB140 datasheet v1.2 (2019, "OpenLinux based OS", "Linux OS with Yocto SDK") — https://gowifi.co.nz/specs/Datasheet-TRB140-v1.2.pdf
3. Teltonika wiki, TRB1 Software Development Kit instructions (target `openwrt-gpl-mdm9x07`, output `bin/targets/mdm9x07/generic`; content seen through the search index, direct fetch blocked) — https://wiki.teltonika-networks.com/view/TRB1_Software_Development_Kit_instructions ; GPL list — https://wiki.teltonika-networks.com/view/GPL
4. Teltonika community, TRB140 FW TRB1_R_00.07.21.1 with EC25-AU (kernel 5.4.302, `mdm9607_s3_level_ao` log, modem firmware repackaging) — https://community.teltonika.lt/t/trb140-firmware-trb1-r-00-07-21-1-with-ec25-au-modem-on-ec25aufar06a12m4g-sms-sending-is-broken-in-australia-after-the-3g-shutdown/18109
5. Teltonika community, TRB145 boot log "Machine model: Teltonika TRB14X" — https://community.teltonika.lt/t/trb145-brick-after-firmware-upgrade/4854
6. TRB141 datasheet — https://download.axilogi.com/Teltonika/Datasheet/TRB141.pdf
7. TRB142 datasheet — https://download.axilogi.com/Teltonika/Datasheet/TRB142.pdf
8. TRB145 datasheet — https://download.axilogi.com/Teltonika/Datasheet/TRB145.pdf
9. TRB160 datasheet — https://download.axilogi.com/Teltonika/Datasheet/TRB160.pdf
10. TRB500 datasheet — https://download.axilogi.com/Teltonika/Datasheet/TRB500.pdf
11. TRB245 datasheet — https://download.axilogi.com/Teltonika/Datasheet/TRB245.pdf
12. TRB246 datasheet — https://download.axilogi.com/Teltonika/Datasheet/TRB246.pdf
13. OTD140 datasheet — https://download.axilogi.com/Teltonika/Datasheet/OTD140.pdf
14. RUT200 datasheet — https://download.axilogi.com/Teltonika/Datasheet/RUT200.pdf
15. RUT241 datasheet — https://download.axilogi.com/Teltonika/Datasheet/RUT241.pdf
16. RUT956 datasheet — https://download.axilogi.com/Teltonika/Datasheet/RUT956.pdf
17. RUTX11 datasheet — https://download.axilogi.com/Teltonika/Datasheet/RUTX11.pdf
18. OpenWrt commit "ramips: mt76x8: add support for Teltonika RUT241" (SoC, RAM, flash, SLM750, DTS, factory image metadata) — https://git.openwrt.org/11189ee7fb6f4175dbd006fbe24e53e13e8f1eec
19. OpenWrt commit "add support for Teltonika RUT200" (EC200A, `AT+QNETDEVCTL`) — https://git.openwrt.org/1227e5f54f087d733c05fd5d1dd2b62d12c2facf
20. OpenWrt commit "add Teltonika RUT956/RUT906 support" (EC25-EUX / SLM770A, Cypress RS-232, RS-485 GPIOs, 74HC595, MCP3221 / TLA2021) — https://git.openwrt.org/85e300c93de7c74861e398fce5be7176df0b3fd4
21. OpenWrt commit RUT951/RUT901 (MT7628AN + EC25-EUX) — https://git.openwrt.org/7264a913a39ea161ddfcf9d263150a089880c402
22. TechInfoDepot, Teltonika RUTX11 (IPQ4018, QCA8075, XT26G02A, XT25F128B) — https://techinfodepot.shoutwiki.com/wiki/Teltonika_RUTX11 ; RUT241 — https://techinfodepot.shoutwiki.com/wiki/Teltonika_RUT241 ; RUT956 — https://techinfodepot.shoutwiki.com/wiki/Teltonika_RUT956
23. fccid.io, FCC ID 2AET4RUTX11 ("contains FCC ID: XMR201807EG06A") — https://fccid.io/2AET4RUTX11 ; grantee list — https://fccid.io/2AET4
24. fccid.io, FCC ID 2AET4RUT241AF (permissive change "EC25-AF to EG25-G") — https://fccid.io/2AET4RUT241AF
25. fccid.io, FCC ID 2AET4RUT956AF — https://fccid.io/2AET4RUT956AF
26. Teltonika PCN, RUTX cellular modem change EG06 to EG060K (2024-08-22) — https://wiki.teltonika-networks.com/images/6/62/RUTX10_CELLULAR_MODEM_CHANGE_2024_08_22_pcn.pdf
27. Teltonika wiki, TRB140 Product Change Notifications (Q4 2023 modem FW change; 2025 PHY chip update) — https://wiki.teltonika-networks.com/view/TRB140_Product_Change_Notifications
28. Quectel EC25/EC21/EC20 R2.0 QuecOpen Solution Presentation V1.0 (MDM9x07, kernel 3.18, SGMII x1, SDIO x2, FC20) — https://eicut.com/wp-content/uploads/2025/04/Quectel_EC25EC21EC20-R2.0-QuecOpen_Solution_Presentation_V1.0.pdf
29. Quectel forum, EC25 QuecOpen SGMII support (AR8033 only; DP83867 needs own driver) — https://forums.quectel.com/t/ec25-quecopen-sgmii-support/11492
30. Quectel forum, SGMII with EG25-G — https://forums.quectel.com/t/sgmii-with-eg25g/51223
31. USR-G806 datasheet — https://modtronix.com/mx-m/usr/usr-g806_datasheet.pdf
32. Robustel R1510 datasheet V1.0.7 — https://www.davantel.com/wp-content/uploads/2023/06/DS_R1510_V1.0.7.pdf
33. Robustel R1510 product page — https://www.robustel.com/product/r1510-industrial-cellular-vpn-router
34. Robustel R2000 Ent datasheet — https://www.assured-systems.com/uploads/media/Robustel/datasheet-R2000-Ent-robustel.pdf ; R2000 Dual — https://www.robustel.com/product/r2000-dual-vpn-gateway
35. InHand IR302 datasheet — https://www.egauge.net/media/support/docs/ir302_datasheet.pdf ; product page — https://www.inhand.com/de/products/industrial-routers/ir302
36. InHand IR615-S datasheet — https://shop.thiim.com/TradePoint141/UserFiles/News/2019q4/InRouter615-S_Datasheet.pdf ; https://westwardsales.com/inhand-inrouter615
37. Milesight UR35 datasheet — https://in.spectra.de/media/39/a2/7e/1626428444/Datasheet-UR35-Routers.pdf
38. Milesight UR32 datasheet — https://in.spectra.de/media/49/c9/ce/1624957371/Datasheet-UR32-Routers_ca34b85f.pdf
39. Milesight UG65 datasheet V2.5 — https://lora-alliance.org/wp-content/uploads/2024/05/UG65-Datasheet-V2.5.pdf
40. Four-Faith F3826 listing — https://www.iotglobalnetwork.com/products/single/id/1587/f3826-lte-wcdma-wifi-router
41. Advantech ICR-2431 datasheet — https://www.integral-system.fr/media/product/file/datasheeta4icr243123092021email-6152dcdd4668f.pdf
42. Digi IX10 model page and product page (memory, power, TrustFence) — https://www.digi.com/products/models/ix10-00g4 ; https://www.digi.com/products/networking/cellular-routers/industrial/digi-ix10
43. Sierra Wireless AirLink FX30 datasheet — https://lte.callmc.com/pdf/datasheets/AirLink-FX30-Datasheet.pdf
44. Moxa OnCell G3150A-LTE product page and datasheet — https://www.moxa.com/product/oncell_g3150a-lte.htm ; https://www.moxa.com.cn/getmedia/819bc2a6-0e24-4967-aa96-5986016c63f8/moxa-oncell-g3150a-lte-series-datasheet-v1.2-chs.pdf
45. Ascend, "RutOS Security Updates: 9 CVEs Patched" (RutOS 7.24 / 7.24.2, Stable vs Latest) — https://www.ascend.de/en/blog/rutos-security-updates-7-24-cve-post-quantum/
46. Teltonika security centre — https://teltonika-networks.com/support/security-center ; Teltonika newsroom on firmware signature — https://www.teltonika-networks.com/uk/newsroom/top-iot-security-risk-or-why-you-must-update-router-firmware
47. Teltonika newsroom, RUTX50 RED certified (EN 18031-1/-2) — https://teltonika-networks.com/newsroom/the-rutx50-5g-router-now-red-certified
48. Teltonika security page (IEC 62443-4-1) — https://teltonika-networks.com/security
49. SentinelOne, CVE-2026-8914 — https://www.sentinelone.com/vulnerability-database/cve-2026-8914/
50. CVE-2023-32349 (NVD data mirror) — https://cve.enginsight.com/2023/32349/index.html
51. ThinkRobotics India prices: TRB140 — https://thinkrobotics.com/products/trb140 ; RUT200 — https://thinkrobotics.com/products/rut200-industrial-cellular-router-1 ; RUT241 — https://thinkrobotics.com/es/products/rut241-industrial-cellular-router-1
52. IndiaMART, Gacrux Automation (RUT200 INR 7,569) — https://m.indiamart.com/gacruxautomation/teltonika-router.html
53. Walmart Teltonika listings (RUTX11 USD 366, RUT956 USD 257.90, TRB140 USD 247.97) — https://www.walmart.com/c/brand/teltonika ; wifi-stock (RUT956 USD 169–247.50) — https://wifi-stock.com/manufacturer-products/teltonika-routers.html
54. MCCI store (UR32 Pro USD 184, Lite USD 138, UG65 USD 467.50) — https://store.mcci.com/products/milesight-pro-series-industrial-cellular-router-ur32 ; https://store.mcci.com/products/milesight-ug65-semi-industrial-lorawan-gateway ; reach.dog UG65 USD 340 — https://reach.dog/shop/mcci/products/milesight-ug65-semi-industrial-lorawan-gateway
55. SHI, InHand IR302 (MSRP USD 167.56) — https://www.shi.com/product/45644373/InHand-InRouter302-Wireless-router
56. Teltonika wiki, Gateways Families (TRB2: no USB, no Wi-Fi) — https://wiki.teltonika-networks.com/view/Teltonika_Networks_Gateways_Families
57. MediaTek MT7628 datasheet — https://www.mouser.com/datasheet/2/744/MT7628_datasheet-2006734.pdf

Internal cross-references: R01 (standards, CRA, RED), R06 (power), R07 (connector/DFM), R09 (Linux vs RTOS, MT7628 and EC25 prices), R11 (Ethernet on baseboard), R14 (baseboard BOM), R15 (integrated 4G modules, EC200A reference design, cheap routers).
