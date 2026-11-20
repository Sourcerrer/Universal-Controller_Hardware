# R17 — Tier-1 4G modem card: modem, Ethernet link to the baseboard, GNSS / AIS-140, costed BOM

Date: 2026-11-14. FX: 1 USD = INR 93.9. Prices are ex-GST, at 1k where a source gives one. Builds on R02 (modem survey), R06 (power), R07 (bus mechanics), R11 (PHYs, RJ45), R14 (baseboard BOM, box header), R15 (EC200A lean card), R16 (router references). Their facts are cited as [R0x] / [R1x] and not repeated.

Owner rules applied (2026-11-14): the card carries only a Quectel 4G modem with Quectel's **standard** firmware (no application processor, no firmware of ours, no Wi-Fi); the card-to-baseboard link is Ethernet-level (about 100 Mbit/s), not the bus UART; no SPI Ethernet controllers; no Mornsun; reliability and safety first, then cost; India first (TEC MTCTE, WPC). New: GNSS for vehicle tracking, and a check against AIS-140.

---

## 1. Summary and recommendation

1. **Modem: Quectel EC200A-CN** (Cat 4, ASR1803, LCC 29 × 32 mm). It is the only Quectel module found whose **standard (AT) firmware** hardware design lists an **RMII** Ethernet port (1.8/3.3 V) for an external 10/100 PHY [1]. RGMII is marked "under development" in the same document [1]. Quectel support staff say RMII is enabled with `AT+QXGMIICFG="enable"` and that they tested it with the **Motorcomm YT8512H** PHY [2]. **This command is not in any public AT manual, and one user could not make it work on a QuecPython/OpenCPU build** [2]. Written confirmation from Quectel (firmware version, NAT/DHCP router behaviour, supported PHYs) is the first action. EC200A-CN covers the Indian LTE bands (FDD B1/3/5/8, TDD B34/38/39/40/41) with WCDMA and GSM 900/1800 fallback, at -35..+75 °C (normal) and -40..+85 °C (extended) [1]. **It has no GNSS** [1].
2. **Rejected modems.** EG25-G / EC25 (MDM9607) have an Ethernet MAC on **SGMII**, plus GNSS without NavIC [4]. But Quectel supports only the AR8033 PHY [R16], which is hard to buy. They also cost about 2.5–3.5× more (EG25-G about INR 3,500 [13]). The UNISOC and ASR1606 Cat-1 modules (EG800K, EC800M, EG915U, EC200U) have no MAC [R15]. **Second source:** no SIMCom, Fibocom or MeiG module with RMII in standard firmware was found. The closest family is the MDM9607 SGMII parts, SIMCom SIM7600G-H [8] and Quectel EC25/EG25-G [4]; they need a different card variant with an SGMII PHY. GosuncnWelink GM520 (ASR1803, RMII/RGMII) is an UNVERIFIED lead [R15].
3. **Link: option (a), 100BASE-TX PHY-to-PHY, capacitively coupled, over two pairs through the box header and bridge plugs.** On the card a YT8512H PHY sits on the modem's RMII. On the baseboard a PHY sits on the MCU's RMII MAC. **It uses 4 bus pins:** ex-CAN_H/CAN_L (15/16) and ex-I²C (27/28). The other options fail:
   - **(b) RMII MAC-to-MAC** needs 9 pins (5 are free). It carries 50 MHz single-ended signals through 2–10 header transitions. Quectel says a direct STM32 connection is not possible [2].
   - **(c) 10BASE-T1S** has no Quectel firmware support for LAN867x and runs at only 10 Mbit/s.
   - **(d) USB 2.0 HS** is impossible because the STM32H5 has USB FS only [R11].
4. **Baseboard: fit a Microchip KSZ8863RLLI 3-port switch on the Ethernet variant instead of the single LAN8742AI.** The switch has 2 PHYs and 1 RMII MAC port, is rated -40..+85 °C, and comes in LQFP-48 [32]. It costs about **+INR 207** for the parts on the Ethernet variant. One PHY feeds the RJ45, the other the bus link, and the MCU MAC uses a Zephyr `ethernet-phy-fixed-link` at 100 M full duplex [30]. **Zephyr removed its KSZ8xxx DSA driver on 2026-03-23** [29], so the switch must run **unmanaged from strap pins**. That is acceptable for a 3-port forwarding switch. The either/or assembly option is about INR 25 but loses the RJ45 port whenever the 4G card is fitted. That is not acceptable for a gateway that reads Modbus-TCP devices.
5. **Control path (needed even with Ethernet).** The baseboard still needs AT commands for SMS (AIS-140 SMS fallback), signal and cell data, FOTA and GNSS. Use the modem's main UART, attached to the bus UART only while the baseboard asserts the card's slot-own **CS1** line (3-state translator 1.8 ↔ 3.3 V). Wire the modem's MAIN_RI to the shared IRQ_N. This also replaces the SYS-7 handshake on this processor-less card: identity comes from ATI/IMEI, and hardware revision from a resistor divider read with `AT+QADC` [1].
6. **GNSS / AIS-140.**
   - **AIS-140 requires NavIC/IRNSS + GAGAN.** It also requires an embedded SIM, 8–32 V operation, a 4 h internal battery, IP65, a 3-axis accelerometer **and** 3-axis gyroscope, emergency-button inputs, SMS fallback, ARAI/ICAT type approval and ISO/TS 16949 manufacturing [18].
   - **No Quectel LTE module with Ethernet and NavIC was found.** The only LTE module with NavIC found is the Fibocom L610-IN (Cat 1 bis, no Ethernet known) [16].
   - **GNSS option on the card:** a separate Quectel NavIC GNSS module, LC29HAIMD (L1 + NavIC L5, INR 813 at 250) [17], with its NMEA output on the 5th freed pin (ex-SPARE, pin 40) to a baseboard UART RX.
   - **The IMU (LSM6DSOX, INR 131 [35]), ignition sense and emergency-button inputs go on the baseboard**, where the application runs.
7. **Card BOM:**
   - **About INR 2,157** with Li-ion cell, DIN enclosure and bridge plug (finished × 1.5 ≈ INR 3,235). Without the cell: about INR 1,931.
   - The **GNSS/AIS-140 add-on is about +INR 1,015** (NavIC module, SMA and bias, MFF2 eSIM).
   - **Compared with the R15 lean card (≈ INR 1,760): about +INR 400**, mostly the cell (+226), an eFuse and ideal-diode inputs (+182), SMA instead of U.FL connectors (+45) and a second box header (+24). A lean power front end brings it back to about INR 1,975 with the cell (≈ 1,749 without).
   - **COST-1 (≤ INR 1,000 finished) cannot be met:** the modem alone is about INR 1,000.
8. **Vehicle power:** 9–24 V is not enough.
   - **AIS-140 demands 8–32 V operation**, a reverse-polarity test (14 V / 27 V for 2 min), and a tri-voltage test at 9/13.5/16 V and 18/27/32 V from -25 to +80 °C [18].
   - ISO 16750-2 load dump: Test B (central suppression) reaches **35 V (12 V systems) / 58 V (24 V systems)**. Unsuppressed Test A reaches **79–101 V / 151–202 V** for up to 400 ms [22].
   - **Recommended input: 8–32 V operating.** Keep 60 V-class parts (TPS26600 eFuse with OVP cut-off at about 34–35 V). On the vehicle SKU use an SM8S36A load-dump TVS (INR 64 [25]) instead of the SMCJ33A, which covers Test B. Unsuppressed 24 V Test A needs a bigger clamp (option).
9. **Recommendation on AIS-140 itself:** a DIN-rail modular stack is a poor fit for an AIS-140 VLTD. The VLTD is approved as one sealed device: IP65, IS 9000 vibration and drop tests, harness connector per Annexure C, internal GNSS antenna, IATF 16949 production [18]. **Offer GNSS on the Tier-1 card for general asset and vehicle tracking.** Treat AIS-140 certification as a separate owner decision: a sealed variant of baseboard + card in one housing, or a later product.

---

## 2. Modem comparison (Ethernet in standard firmware, GNSS, NavIC)

Legend: Y = yes, N = no, ? = UNVERIFIED.

| Module (chip) | LTE cat | India bands | GSM fallback | Ethernet in **standard** firmware | GNSS / NavIC | Temp (°C) | India price / stock | FOTA / security | Longevity | Verdict | Src |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **Quectel EC200A-CN** (ASR1803) | Cat 4 (150/50) | FDD B1/3/5/8; TDD B34/38/39/40/41; WCDMA B1/5/8 | **Y** 900/1800 | **RMII Y** (HD lists RMII 1.8/3.3 V; RGMII "*" = under development) [1]. Enable with `AT+QXGMIICFG="enable"`, YT8512H tested (Quectel staff, forum) [2]. Not in a public AT manual. NAT/DHCP router behaviour on Ethernet **?** | **N / N** | -35..+75 normal, -40..+85 extended [1] | Hubtronics INR 1,250–1,454 single, **out of stock** [10]; 1k ≈ 1,000 **?** | DFOTA + USB upgrade [1]; Quectel PSIRT with CVE advisories, claims SBOM/VEX and CRA readiness [15] | Series active; no EOL notice found ?; Avnet lead times very long (EU variant shows 372 weeks) [11] | **Recommended** (confirm RMII in writing) | [1][2][10][11] |
| Quectel EC200A-EU | Cat 4 | FDD B1/3/5/7/8/20/28, TDD B38/40/41 (covers India except B34/39) | Y 900/1800 | RMII as EC200A-CN [1] | N | as above | USD 21.54 @100 Avnet (INR 2,023); USD 24.51 single Openelab (INR 2,302) [11][12] | as above | as above | Candidate single India + EU SKU (CE later) if it costs nearly the same as CN | [1][11][12] |
| Quectel EG25-G (MDM9607) | Cat 4 | FDD B1/3/5/8, TDD B38/39/40/41 (+ global) | Y quad | **SGMII Y** (integrated MAC; AR8033 reference) [4]. SGMII application note listed on product page [5]. Only AR8033 supported; DP83867 refused [6][R16]. No IPPT in standard firmware; ECM mode NATs [7] | **GPS/GLO/BDS/GAL/QZSS, NavIC N** [4] | -35..+75 / -40..+85 [4] | EG25GLGD-128 AUD 57.2 @250 DigiKey AU (≈ INR 3,500, rate UNVERIFIED), not stocked, 14 weeks [13] | DFOTA [4]; PSIRT [15] | MDM9607 platform mature; EOL ? | Fallback only: cost + AR8033 lock-in | [4][5][6][7][13] |
| Quectel EC25-E (MDM9607) | Cat 4 | B1/3/5/7/8/20/38/40/41 | Y | SGMII (as EG25-G family) | optional GNSS, no NavIC | as EG25 | Evelta INR 2,695 single (snippet); ichome USD 70.19 @500 (INR 6,591) [14] | DFOTA | — | Fallback; cost | [14] |
| SIMCom SIM7600G-H / SIM7600EI (MDM9607) | Cat 4 | India variant EI ? | Y | **SGMII with embedded MAC, "default closed, contact SIMCom"** [8]; older LAN route was HSIC + LAN9730 [9] | GNSS Y (no NavIC ?) | ? | ? | ? | ? | **Second-source family for an SGMII card variant** | [8][9] |
| SIMCom A7600/A7608 (ASR1803) | Cat 4 | TDD 34/38/39/40/41; India variant ? | ? | **No RMII in HDG** [R15] | ? | — | — | — | — | Fails Ethernet | [R15] |
| GosuncnWelink GM520 (ASR1803) | Cat 4 | ? | ? | RMII/RGMII listed (snippet) | ? | ? | ? | ? | ? | UNVERIFIED second-source lead | [R15] |
| Fibocom L610-IN (UNISOC Cat 1 bis) | Cat 1 bis | India | ? | none known | **GNSS with IRNSS/NavIC, "AIS140" claimed**; pin-compatible with Fibocom L716 / NL668 Cat 4 | ? | ? | ? | ? | Only LTE module with NavIC found; fails Ethernet | [16] |
| Quectel EG800K / EC800M / EG915U / EC200U (UNISOC / ASR1606) | Cat 1 / 1 bis | Y | some | **No MAC** | EC200U-GNSS variants, no NavIC | — | INR 320–950 [R02] | — | — | Fails Ethernet | [R02][R15] |

Notes:
- **What "standard firmware Ethernet" means here.** The modem routes LTE to Ethernet itself, much as it does for USB ECM (DHCP server, NAT). The baseboard is a DHCP client behind it. This matches what Quectel staff describe for ECM on EG25-G [7] and what Teltonika does with EC200A over USB ECM [R16]. For EC200A over RMII it is **UNVERIFIED**. Ask Quectel for the RMII application note and the default LAN subnet, NAT and IP-passthrough options.
- **PHY lock-in.** The modem firmware drives the PHY over MDIO. YT8512H is the only PHY Quectel names for EC200A [2][R15]. Its industrial temperature grade is UNVERIFIED (YT8512C is 0–70 °C [R11]). Ask Quectel for an industrial PHY, such as KSZ8081 or LAN8742, if YT8512H is commercial grade.
- **EC200A USIM:** one (U)SIM interface, 1.8/3.0 V, with hot-plug detection [1]. An MFF2 eSIM (AIS-140) shares these lines: fit either the eSIM or the nano-SIM holder.

---

## 3. Link options across the stack bus

Bus context: pass-through bus with BUS-IN / BUS-OUT box headers on every module and bridge plugs between modules [R07][R14]. Free pins: 15 CAN_H, 16 CAN_L, 27 I2C_SDA, 28 I2C_SCL, 40 SPARE (5 pins). The 4G card may sit 1 to 5 slots from the baseboard. The link therefore crosses up to 10 header transitions and about 0.3–0.5 m of trace (estimate).

| | (a) 100BASE-TX PHY-to-PHY, capacitive | (b) RMII MAC-to-MAC | (c) 10BASE-T1S multidrop (LAN8670/1 RMII) | (d) USB 2.0 HS |
|---|---|---|---|---|
| Bus pins | **4** (2 pairs) | 9 (REF_CLK, CRS_DV, RXD0/1, TX_EN, TXD0/1, MDIO, MDC). **Exceeds 5** | 2 (1 pair, all modules) | 2 (+VBUS optional) |
| Modem support (standard firmware) | **Y**: RMII + YT8512H tested by Quectel [2] | **N**: Quectel: "direct connection [to STM32] not possible" [2] | **N**: no LAN867x support in Quectel firmware (PLCA set-up needs a driver) | Y (USB ECM/RNDIS), but needs a HS host |
| Baseboard support | STM32H573 RMII MAC + PHY or switch port (Zephyr OK) | needs PHY-less fixed-link on both ends | Zephyr `microchip,t1s-phy` supports LAN8670/1/2 Rev C1/C2/D0 [30] | **STM32H5 has USB FS only (12 Mbit/s)** [R11]; Zephyr USB-host ECM class UNVERIFIED |
| Throughput | 100 Mbit/s full duplex | 100 Mbit/s | 10 Mbit/s shared, half duplex | 480 Mbit/s (FS fallback 12) |
| Signal integrity | MLT-3 at 125 Mbaud (31.25 MHz fundamental), differential, PHY adaptive equalizer built for 100 m cable. TI: ≥ 33 nF blocking caps, verify links > 1 m [26] | 50 MHz single-ended, 4 ns setup / 2 ns hold class, skew across many headers. **Poor** | robust, differential, 10 Mbit/s | 90 Ω pairs through 2.54 mm headers: weak [R07] |
| EMC | low (differential, low CM) | **worst** (7 single-ended 50 MHz lines on an unshielded bridge) | best | moderate |
| Extra BOM per gateway | card PHY ≈ 46 + baseboard switch Δ ≈ 207 (or second PHY) | none, but not feasible | 2 × LAN8671 ≈ 2 × 310 [33] + every module needs one | ULPI PHY + different MCU |
| **Verdict** | **Recommended** | Fails (pins, SI, modem) | Fails (modem, 10 Mbit/s) | Fails (MCU) |

### 3.1 Option (a) schematic detail

```
4G CARD                                         BUS (pass-through on every module)            BASEBOARD (Ethernet variant)
EC200A RMII (3.3 V domain) ── YT8512H ── TX± ──[C 100 nF/100 V]×2── pin 15/16 (pair A) ──[C 100 nF/100 V]×2── KSZ8863 port-2 RX±
                       25 MHz xtal     RX± ──[C 100 nF/100 V]×2── pin 27/28 (pair B) ──[C 100 nF/100 V]×2── KSZ8863 port-2 TX±
                       bias/termination per PHY datasheet          GND 14/17 and 26 adjacent              bias per KSZ8863 datasheet
                       TPD4E05U06 at PHY side                                                            TPD4E05U06 at switch side
                                                                                                          KSZ8863 port-1 ── HX1188NL ── RJ45 (Bob-Smith, TVS) [R11]
                                                                                                          KSZ8863 port-3 RMII ── STM32H573 MAC (fixed-link 100FD)
```

- **Blocking caps:** two in series per line, one on each end, so either module can be removed without leaving DC on the pins. Use **≥ 33 nF** (TI minimum for IEEE impedance [26]); 100 nF X7R is proposed. Rate them **100 V**. A misaligned bridge plug or an end-of-chain receptacle could put BUS_V (up to 58 V under vehicle load dump) on a data pin, and the caps then block the DC.
- **Bias:** current-mode PHYs (KSZ, LAN87xx class) keep their 49.9 Ω pull-ups to AVDD on the PHY side of the caps. Voltage-mode PHYs need none. Check the YT8512H datasheet (UNVERIFIED).
- **Auto-negotiation:**
  - Microchip AN1900 says auto-negotiation and Auto-MDIX **must be disabled** in transformerless links [27]. TI recommends forced 100 Mb/s [26].
  - Both ends must match: if only one side is forced, parallel detection gives a duplex mismatch.
  - **Plan A:** force 100 FD with straps on both the YT8512H and KSZ8863 port 2. Whether the strap options exist and the modem firmware keeps them is UNVERIFIED.
  - **Plan B:** both ends auto-negotiate, validated on the prototype.
  - **Plan C (fallback footprint, DNP):** an SMD 10/100 transformer (HX1188NL class, INR ≈ 102 [R11]) on the card, which restores a standard IEEE MDI.
- **Layout:** 100 Ω differential on every module, no stubs, pairs straight through IN → OUT. 15/16 and 27/28 are opposite-row pairs in the 2×20 header. GND pins 14, 17 and 26 sit next to them. Pin 13 (UART_RX) and pins 25/29/30 (CS5, IRQ_N, TOKEN) are close, but these are slow signals. **When the pinout is frozen, move pair B so that a GND pin sits on each side** (proposal only).
- **EMC:** optional CM-choke footprint (DNP) on the baseboard side. Keep the 4G card in slot 1 where possible; this is advice, not a rule.
- **Validation (UNVERIFIED until done):** iperf3 at 100 Mbit/s for 24 h through a 5-module stack, from -25 to +80 °C, with frame-error counters. Then IEC 61000-4-2 on the end-of-chain receptacle, and radiated emissions with the stack in its enclosures.

### 3.2 Connector pin usage (proposal)

| Pin | Old | New on Tier-1 stack | Notes |
|---|---|---|---|
| 15 / 16 | CAN_H / CAN_L (optional 2nd transport) | ETH pair A (card TX → base RX) | CAN on the bus is given up; keep CAN on the baseboard field terminal |
| 27 / 28 | I²C SDA/SCL (spare) | ETH pair B (base TX → card RX) | I²C was already spare (SYS-7) |
| 40 | SPARE | GNSS_NMEA (card → baseboard UART RX, 3.3 V, 9600–115200 Bd) | Only on the GNSS SKU. 74LVC1G125 driver, enabled only when the GNSS option is fitted |
| 21 (CS1, rotated) | SPI chip select | MODEM_SEL: connects the modem main UART to bus UART_TX/RX | Card has no SPI. Baseboard pin used as GPIO |
| 29 IRQ_N | shared open-drain | modem MAIN_RI (URC/SMS) via open-drain FET | baseboard selects the card and reads |
| 31 (PWR_EN1, rotated) | slot power enable | enable of the card eFuse (BASE-4 power cycle) | |
| 30 TOKEN | daisy chain | passed straight through (no MCU to re-drive it) | **R08 must allow a passive slot**; the baseboard detects the card by sending "AT" on each slot's CS |

---

## 4. Baseboard side: switch versus either/or

| | (i) KSZ8863RLLI 3-port switch (recommended) | (ii) Either/or assembly (LAN8742AI to RJ45 **or** bus) | (iii) Davicom DM8603IEP / DM8806 | Realtek RTL8305 class |
|---|---|---|---|---|
| Function | RJ45 **and** 4G link together; hardware forwarding at 100 M | one at a time | 3-port (DM8603I, industrial claimed) / 6-port | 5-port |
| Temp | -40..+85 °C, LQFP-48 [32] | LAN8742AI -40..+85 [R11] | DM8603I industrial (snippet) [34] | ? |
| Zephyr | **No DSA driver** (KSZ8xxx removed 2026-03-23 [29]). Use unmanaged straps + `ethernet-phy-fixed-link` 100FD on the MAC [30]; port status readable over MDIO by app code | `microchip,lan8742` driver [R11] | DM8806: Zephyr `davicom,dm8806-phy` driver exists [30]; price / grade ? | none |
| Price | LCSC C631675 / C5229506 USD 3.64–4.25 single (INR 342–399); Mouser USD 5.16–5.28 @100 (INR 485–496) [32] | 0 extra | ? | ? |
| Δ BOM vs R11 Ethernet option | **≈ +INR 207** (342 − 160 LAN8742AI + 20 coupling/ESD + 5 straps) | ≈ +INR 25 (coupling network + 0 Ω steering) | ? | ? |
| Risk | REFCLK and strap details per datasheet (50 MHz RMII clock output from the switch, forced-mode straps per port: verify) | loses RJ45 whenever the 4G card is fitted | supply, documentation | grade, documentation |

**STM32H573 RMII pins** [R11][31]: PA1 REF_CLK, PA2 MDIO, PC1 MDC, PA7 CRS_DV, PC4 RXD0, PC5 RXD1, TX_EN PA5 (LQFP64 table) or PG11 (Nucleo-H563ZI, LQFP144), TXD0 PB12/PC10 (PG13 on Nucleo), **TXD1 PB15 (ST erratum: not PB13)**. Port G is not bonded in LQFP100, so the LQFP100 TX pins must come from the CubeMX pin plan (UNVERIFIED). The switch works with any RMII MAC, so the D-17 MCU alternatives (RA8M1, MCXN947) are unaffected.

**Recommendation:** KSZ8863RLLI on every Ethernet-variant baseboard. Field port on port 1, bus link on port 2, unmanaged. A Tier-1 4G gateway therefore always needs the Ethernet-variant baseboard (+INR 588 per BASE-9, +207 for the switch).

---

## 5. GNSS on the card and AIS-140

### 5.1 What AIS-140 requires (finalized draft AIS-140/DF1, May 2017 [18]; amended text not retrieved)

| Clause | Requirement | Consequence for us |
|---|---|---|
| 3.1.1.1 a–b | GNSS with **NAVIC/IRNSS** support (devices installed from 1 Apr 2018) and **GAGAN** SBAS | separate NavIC GNSS module (EC200A has no GNSS) |
| 3.1.1.1 c–e | ≤ 2.5 m CEP (or 6 m 2DRMS); acquisition ≤ -148 dBm; tracking ≤ -165 dBm | module datasheet check (UNVERIFIED for LC29HAIMD) |
| 3.1.1.1 f | **internal antenna**; external only where fitment prevents it | internal active patch option (+ about INR 200, UNVERIFIED) |
| 3.1.1.2 | 4 digital in, 2 analogue in, 1 serial | baseboard IO covers this [R14] |
| 3.1.1.3 / 3.1.1.21 | GSM/GPRS, multi-slot class 10+, SMS | EC200A GSM 900/1800 [1]; "quad-band" wording in the draft (UNVERIFIED in final text) |
| 3.1.1.6 / 3.1.5 | emergency alert (Alert ID 10) to server, **SMS fallback** | AT path to the modem (section 3.2) |
| 3.1.1.7 | **internal battery, 4 h** at 60 s reporting | Li-ion on card + baseboard (both modules must run) |
| 3.1.1.14 / 3.1.1.21 | **embedded SIM**, 10-year life, multi-network OTA switching | MFF2 eSIM footprint (cost UNVERIFIED) |
| 3.1.1.15 | **8–32 V DC** operation for 12/24 V vehicles | input range change (section 7) |
| 3.1.1.16 | sleep current ≤ 20 mA (dedicated device) | difficult for a 2-module stack; budget needed |
| 3.1.1.19 | hot < 5 s, warm < 30 s, cold < 40 s | GNSS backup supply from always-on rail |
| 3.1.1.20 | NMEA 0183 output | NMEA line to baseboard |
| 3.1.1.22 | **IP65**, dust/temp/vibration; tamper proof | DIN enclosure does not meet it |
| 3.1.1.23 | ISO/TS 16949 (now IATF 16949) manufacturing | CM qualification |
| 3.1.1.24 | A-GPS | modem/GNSS assistance via baseboard |
| 3.1.1.26 | **3-axis accelerometer and 3-axis gyroscope** (harsh braking, acceleration, rash turning) | 6-axis IMU on baseboard |
| 3.1.2.3 | emergency buttons **normally closed** | DI with wire-break detection |
| Sec. 4 | protocol: login / tracking / health packets, alert IDs, SMS format, 2 IP endpoints, store-and-forward 40,000 records (LIFO) | baseboard firmware + storage (BASE-6) |
| Table 6B | AIS 004 Part 3 EMC; reverse polarity 14 V / 27 V for 2 min; IS 9000 vibration; 500 mm drop; tri-temp × tri-voltage from **-25 to +80 °C** at 9/13.5/16 V and 18/27/32 V | +80 °C exceeds the EC200A normal range (extended range only [1]) and Li-ion charging limits |

- Certification: component approval by test agencies such as ARAI and ICAT. ARAI's list of approved VLTDs (16 Jul 2026) refers to AIS 140:2016 amended up to **Amendment No. 3 (04/2026)** and lists "GPS + IRNSS (NAVIC)" devices (snippet; the PDF could not be fetched because of a TLS certificate error) [19]. State SOPs (Tamil Nadu 2025, Puducherry VLTD-2022) describe the VLTD as a GNSS (IRNSS) logger with 2G/3G/4G/5G communication [20].
- NavIC health: one secondary 2026 source says only 3 first-generation IRNSS satellites were still working by mid-2026, with NVS-03 due on 30 Oct 2026 (UNVERIFIED) [21]. Use GPS + NavIC + GAGAN together, never NavIC alone.

### 5.2 GNSS block on the card (GNSS SKU)

- **Receiver:** Quectel **LC29HAIMD**, dual-band L1 + NavIC L5 with LNA, Indian-market part. Mouser India quotes INR 813.46 at 250, not stocked, 10-week lead time [17]. Alternatives: L89HB-S90 (L1 + NavIC, Airoha AG3335) at INR 928.07 for 1k [17]; L89HA-S90 at USD 10.96 for 250 (INR 1,029) [17]; LC79D at INR 1,401.57 at low quantity [17]. Datasheet values for GAGAN, sensitivity and TTFF must be checked against AIS-140 (UNVERIFIED).
- **Antenna:** SMA (edge-mount) for an external active L1/L5 antenna. Bias: 3.3 V from the always-on rail through a ferrite, 10 Ω and 47 nH, with a current limit or short detection (≈ INR 45, estimate). An internal patch antenna is optional (AIS-140 clause f).
- **LNA / SAW:** the module's own LNA plus the active antenna's LNA and SAW are normally enough. Keep a DNP SAW footprint for co-location with LTE B3/B40 uplink at 23 dBm (UNVERIFIED need; confirm in the prototype desense test).
- **Backup:** feed V_BCKP from the VSYS-derived 3.3 V, which stays on while the Li-ion cell has charge. This gives hot starts under 5 s.
- **Data path:** GNSS UART TX goes through a 74LVC1G125 to **bus pin 40** and on to a baseboard UART RX (NMEA 0183, one-way). The receiver runs its default configuration. Any reconfiguration is done once at production through test pads. Alternatives rejected: NMEA through the modem (standard firmware does not forward an external receiver), and NMEA over Ethernet (needs a processor on the card).
- **Accelerometer / gyro:** required by AIS-140 3.1.1.26 and common in fleet trackers. Put an **LSM6DSOX** on the baseboard on I²C/SPI to the MCU: LCSC USD 1.3929 at 1k = INR 131 (another snapshot USD 1.774) [35]. The card has no host.
- **Ignition sense (baseboard note):** one DI rated for 8–32 V with ISO 7637-2 pulse margin (TVS, divider, threshold about 6–7 V). It must also wake the MCU from sleep. The emergency-button inputs are NC-type DIs with wire-break detection [18].

---

## 6. BOM — Tier-1 4G card (EC200A-CN), 1k

S = sourced, E = estimate (UNVERIFIED), R = from an earlier report.

| # | Item | Part | INR | Basis |
|---|---|---|---|---|
| 1 | LTE Cat 4 modem, India bands + GSM, RMII | Quectel EC200A-CN (LCC) | 1,000 | R/E: retail INR 1,250–1,454, out of stock [10]; 1k UNVERIFIED |
| 2 | RMII PHY + 25 MHz crystal | Motorcomm YT8512H (Quectel-tested) | 46 | R: LCSC ≈ USD 0.44 [R11][R15] |
| 3 | Link coupling: 4 × 100 nF/100 V X7R + bias | — | 8 | E |
| 4 | Link ESD | TI TPD4E05U06 | 12 | R [R11] |
| 5 | Modem UART 1.8 ↔ 3.3 V translator with OE (CS1-gated) + RI open-drain FET + PWRKEY/RESET transistors | SN74AVC2T245 class + 2N7002 | 35 | E |
| 6 | Nano-SIM holder + SIM ESD | push-push holder + 3-ch TVS | 18 | E [R15] |
| 7 | 2 × SMA edge connectors (LTE main + diversity) | generic | 70 | E (antennas are customer accessories, ≈ INR 150–300 each, UNVERIFIED) |
| 8 | Input: fuse + TVS + 2 × ideal-diode OR (bus / terminal) | SMCJ33A + 2 × LM74700-Q1 + N-FET | 111 | S: SMCJ33A 15.57 [R14]; LM74700 USD 0.3736 [R06]; FET E |
| 9 | Card eFuse (60 V, current limit, OVP ≈ 34–35 V, EN = PWR_EN1) | TI TPS26600 | 105 | S [R14] (LCSC USD 1.1234) |
| 10 | Buck 36 V → 5 V, 3 A + passives | TI LMR51430 | 65 | S/E [R06] |
| 11 | NVDC charger, **standalone** (no host on the card) + inductor + NTC | TI BQ25606 (standalone sister of BQ25601) | 70 | E (BQ25601 USD 0.472 [R06]; BQ25606 price UNVERIFIED) |
| 12 | VBAT bulk ≥ 1000 µF total + 4.7 V TVS | polymer caps | 30 | E [R06]; supply must give ≥ 2.8 A [1] |
| 13 | 3.3 V LDO from VSYS (PHY, translator, GNSS bias) | TLV757 class | 10 | E |
| 14 | Cell holder / leads | — | 25 | R [R14] |
| 15 | 2 × 2.54 mm 2×20 box header (BUS-IN, BUS-OUT) | BXCONN 2.54JN-2-20-Z | 48 | S [R14] (INR 23.76 each) |
| 16 | Local DC terminal (standalone use) | 2-pin pluggable | 18 | E |
| 17 | PCB 4-layer about 70 × 90 mm | — | 60 | E [R15] |
| 18 | Passives, LEDs, test pads (USB D+/D− and USB_BOOT for Quectel recovery and logs) | — | 50 | E |
| | **Card electronics** | | **≈ 1,781** | |
| 19 | Bridge plug (one per module) | 2×20 bridge | 40 | E |
| 20 | DIN enclosure | Electrocom EC7060 ABS | 110 | R [R14][R15] |
| 21 | Li-ion cell 18650 2600 mAh, BIS | — | 226 | R [R14] |
| | **Card total** | | **≈ 2,157** (≈ 1,931 without cell) | finished × 1.5 ≈ **3,235** |

**Options**

| Option | Δ INR | Basis |
|---|---|---|
| GNSS / AIS-140 SKU: LC29HAIMD 813 + GNSS SMA and bias 45 + NMEA driver 5 + V_BCKP 2 + MFF2 eSIM about 150 | **+1,015** | [17]; eSIM E |
| — DNP SAW pre-filter fitted / internal active patch antenna | +15 / +200 | E |
| Vehicle front end: SM8S36A instead of SMCJ33A (load dump Test B) | +48 | [25] (USD 0.6829 = INR 64) |
| Lean front end: Schottky OR + PTC instead of 2 × LM74700 + TPS26600 (as in R15) | −182 | [R06] (gives up per-module fault isolation, PWR-6) |
| Fallback DNP transformer for the link (HX1188NL) | +102 | [R11] |
| EC200A-EU instead of -CN (India + EU bands) | +≈ 1,000 at 100 pcs | [11] |

**Baseboard additions for a Tier-1 4G gateway**

| Item | Δ INR | Basis |
|---|---|---|
| Ethernet variant (H573 + PHY + RJ45 per BASE-9) | +588 | PRD BASE-9 |
| KSZ8863RLLI instead of LAN8742AI, + coupling/ESD + straps | +207 | [32] |
| Vehicle option: LSM6DSOX IMU + ignition-sense input | +141 | [35] + E |

**Comparison with the R15 lean card (≈ INR 1,760, 4G + Ethernet without Wi-Fi, with charger, without cell)**

| Block | R15 lean | R17 | Δ | Why |
|---|---|---|---|---|
| Modem | 1,000 | 1,000 | 0 | same EC200A-CN |
| PHY + Ethernet port | 213 (PHY + magnetics + RJ45 + ESD) | 66 (PHY + caps + ESD) | −147 | no RJ45 or magnetics on the card (link only) |
| Wi-Fi | 0 (moved out in the no-Wi-Fi variant) | 0 | 0 | |
| Power incl. charger | 180 (Schottky OR + PTC + buck + BQ25601) | 416 (2 ideal diodes, eFuse, buck, standalone charger, bulk, LDO, holder) | +236 | per-module fault isolation (PWR-6), OVP for 32 V vehicles |
| Bus connector | 24 (1 header) | 48 + 40 bridge | +64 | BUS-IN + BUS-OUT + bridge |
| RF connectors | 25 (U.FL) | 70 (SMA) | +45 | CELL-7 external antennas, no pigtails |
| UART gate, SIM, PCB, DC terminal, misc | ≈ 208 | ≈ 181 | −27 | |
| Enclosure | 110 | 110 | 0 | |
| **Total without cell** | **≈ 1,760** | **≈ 1,931** | **+171** | |
| Cell | excluded | 226 | +226 | PWR-2 |

---

## 7. Vehicle-tracking power input

| Source | Requirement |
|---|---|
| AIS-140 3.1.1.15 [18] | operate **8–32 V DC** on 12 V and 24 V vehicles |
| AIS-140 Table 6B [18] | reverse polarity without fuse: **-14 V (12 V) / -27 V (24 V) for 2 min**; tri-voltage 9/13.5/16 V and 18/27/32 V at -25 °C, room temperature and +80 °C; EMC per **AIS 004 Part 3** (contents not retrieved; UNVERIFIED whether ISO 7637-2 pulses are included) |
| ISO 16750-2 load dump [22] | Test A (unsuppressed): Us **79–101 V (12 V), 151–202 V (24 V)**, Ri 0.5–4 Ω / 1–8 Ω, td 40–400 ms / 100–350 ms. Test B (central suppression): **35 V (12 V) / 58 V (24 V)** (the Diotec table prints 65 V for 24 V, its text says 58 V). 10 pulses, 1 min apart |
| ISO 7637-2:2011 [24] (secondary summary) | pulse 1: -75 to -150 V (12 V), -300 to -600 V (24 V); 2a: +37 to +112 V; 3a: -112 to -220 V / -150 to -300 V; 3b: +75 to +150 V / +150 to +300 V |
| ISO 16750-2 jump start | 24 V for 12 V systems; 36 V for 24 V systems (UNVERIFIED, not retrieved) |

**What this means for the 9–24 V input:**
1. Change the vehicle SKU rating to **8–32 V operating**. Keep 9–24 V on the industrial label, but design every module to 8–32 V; the parts already allow it (TPS26600 60 V, LMR51430 36 V behind the OVP cut-off).
2. **Survive Test B 58 V and ISO 7637-2** with an SM8S36A load-dump TVS (VWM 36 V, clamp 58.1 V at 114 A) [25] in front of the 60 V eFuse. Above about 34–35 V the eFuse disconnects, and the Li-ion cell carries the card through jump-start or dump events.
3. **Unsuppressed 24 V Test A (up to 202 V, 350 ms)** is beyond a single SM8S. If it is required, add an option of two SM8S in parallel or a high-energy TVS with a series surge stopper (UNVERIFIED sizing). TI and ADI describe TVS clamping and MOSFET isolation as the common approaches [23].
4. **Cranking dips:** with the NVDC charger the cell carries the modem through cold-crank drops below 8 V. No extra hold-up is needed when the cell is fitted.
5. **Reverse polarity to -27 V:** LM74700-Q1 is rated -65 V [R06], so this passes.
6. **+80 °C:** at this temperature Li-ion charging must be inhibited (JEITA/NTC). The cell needs a high-temperature rating or a LiFePO4 alternative. This is a safety item for R06/R13 (UNVERIFIED cell choice).

---

## 8. Risks and open items

1. **RMII in standard EC200A firmware is confirmed only by a Quectel forum answer** [2], with a datasheet listing [1]. The command, firmware version, NAT/DHCP behaviour and PHY list need Quectel's written confirmation before layout. If it fails, the fallback is an SGMII card variant (EG25-G / SIM7600 + AR8033-class PHY), about INR 2,500 more per card.
2. **Auto-negotiation over capacitive coupling:** vendor notes say disable it [26][27], but the modem firmware controls the YT8512H. Prototype first, with the DNP transformer fallback.
3. **YT8512H temperature grade** is unknown, and Quectel names it as the only tested PHY.
4. **EC200A supply:** out of stock at Hubtronics; Avnet shows very long lead times [10][11]. The 1k price is UNVERIFIED. Get Quectel India distributor quotes for -CN and -EU.
5. **Zephyr:** no DSA driver for any Microchip switch since 2026-03-23 [29]. The unmanaged strap configuration must be validated, and port-link monitoring done in application code over MDIO.
6. **Bus protocol changes (R08):** the card is passive on TOKEN and needs a CS1-gated AT channel. Unsolicited AT messages arrive only via IRQ_N plus a poll.
7. **AIS-140 fit:** IP65, internal GNSS antenna, harness per Annexure C, IATF 16949 manufacturing, sleep current ≤ 20 mA and +80 °C testing do not fit the DIN-rail stack. **Owner decision needed.**
8. **NavIC constellation health** (secondary source) [21]: always run multi-GNSS.
9. **Second source:** no RMII-in-standard-firmware module from SIMCom, Fibocom or MeiG was found. The second source is an SGMII board variant, not a drop-in.
10. **Security / CRA:** modem firmware and its CVE patches belong to Quectel. A PSIRT exists and advisories are promised with CVE and fixed version [15]. Contract for a support period and DFOTA delta availability.
11. **COST-1 (≤ INR 1,000 finished) is impossible** with any Ethernet-capable modem. Report the gap to the owner: the card is about INR 3,235 finished.

**Not verified in this run:**
- EC200A 1k price and any EOL notice; the `AT+QXGMIICFG` syntax; EC200A NAT on the RMII port.
- YT8512H strap options and temperature grade; KSZ8863 REFCLK and forced-mode straps.
- BQ25606 price.
- LC29HAIMD GAGAN support, sensitivity and TTFF.
- MFF2 eSIM price; SMA and antenna prices.
- AIS-140 Amendment 3 final text and AIS 004 Part 3 contents; ISO 16750-2 jump-start values.
- DM8603I / DM8806 price and grade; second-source vendor RMII modules.

---

## 9. Sources

All accessed 2026-11-14. "Snippet" = search-result text only; page not opened or blocked.

1. Quectel EC200A Series Hardware Design V1.1 (standard firmware): RMII 1.8/3.3 V, RGMII "*", bands per variant, -35..+75 / -40..+85 °C, DFOTA, 1.8 V UARTs, VBAT_RF 2.0 A, supply ≥ 2.8 A, single (U)SIM, AT+QADC. https://images.quectel.com/python/sites/2/2023/05/Quectel_EC200A_Series_Hardware_Design_V1.1.pdf (saved: datasheets/cellular/Quectel_EC200A_Hardware-Design_V1.1_standard.pdf)
2. Quectel forum, "How to Enable RMII Interface on EC200A Module" (Bean.Wang-Q, 16 Jan 2025: `AT+QXGMIICFG="enable"`, YT8512H tested, no direct STM32 connection; user report 29 Jul 2025 of failure on an OCPU_QPY build). https://forums.quectel.com/t/how-to-enable-rmii-interface-on-ec200a-module/42753
3. QuecPython Ethernet NIC guide (EC200A: RMII PHY yes, SPI Ethernet no) (snippet). https://developer.quectel.com/doc/quecpython/Application_guide/en/network-comm/nic/ethernet/index.html
4. Quectel EG25-G Hardware Design V1.5 (2024-03-19): SGMII + integrated MAC, AR8033 reference, GNSS GPS/GLONASS/BDS/Galileo/QZSS, bands, temperatures. https://quectel.com/content/uploads/2024/04/Quectel_EG25-G_Hardware_Design_V1.5.pdf (saved)
5. Quectel EG25-G product page listing "Quectel_EC2x_Series&EG25-G_SGMII_Application_Note_V1.0" (snippet). https://www.quectel.com/product/lteeg25g
6. Quectel forum, "SGMII with EG25G" (DP83867E not supported, Oct 2025). https://forums.quectel.com/t/sgmii-with-eg25g/51223
7. Quectel forum, "EG25-G IP Passthrough (IPPT)" (Jan 2025: no IPPT in tested firmware; ECM mode runs DHCP/NAT). https://forums.quectel.com/t/eg25-g-ip-passthrough-ippt/42433
8. SIMCom SIM7600G / SIM7600G-H Hardware Design V1.00 (2019-03-29): SGMII with embedded MAC, "SGMII function default closed, contact SIMCom". https://files.waveshare.com/upload/e/e6/SIM7600G_SIM7600G-H_Hardware_Design_V1.00.pdf (saved)
9. SIMCom SIM7600 Series HSIC LAN Application Note V1.00 (LAN9730 over HSIC) (snippet). https://files.waveshare.com/upload/c/cf/SIM7600_Series_HSIC_LAN_Application_Note_V1.00.pdf
10. Hubtronics EC200A listings: EC200A-CNTA-D10-UGASA INR 1,454.24; EC200ACNHA-N06-SNASA INR 1,250.00; EC200ACNHB INR 2,644.92; all out of stock. https://hubtronics.in/index.php?route=product/search&search=EC200A
11. Avnet EC200A-EU (0 stock, 372-week factory lead time, snippet) and EC200A-AU/EU USD 27.69 / 21.54 at 100 [R15 S9]. https://www.avnet.com/americas/product/quectel-wireless-solutions/ec200aeuha-n06-mn0aa/evolve-56847731/ ; https://www.avnet.com/americas/product/quectel-wireless-solutions/ec200aauha-n06-mn0aa/evolve-66504417/
12. Openelab EC200A-EU V1 LCC USD 24.51 (snippet). https://openelab.io/products/quectel-ec200a-eu-v1-4g-lte-cat4-lcc-module
13. DigiKey AU EG25GLGD-128-SGNS AUD 57.19976 at 250, not stocked, 14 weeks (snippet). https://www.digikey.com.au/en/products/detail/quectel/EG25GLGD-128-SGNS/24352418
14. EC25-E: Evelta INR 2,695 ex-GST (snippet; page now 404) https://evelta.com/quectel-ec25-e-lte-category-4-module ; ichome EC25EFA-512-STD USD 70.19 at 500 (snippet) https://ichome.com/product-detail/quectel/ec25efa-512-std
15. Quectel PSIRT policy and product security (advisories with CVE/CWE/CVSS/fixed version; SBOM/VEX; CRA readiness claim). https://www.quectel.com/psirt-policy/ ; https://security.quectel.com/vulnerability/website/psirt-policy ; https://www.quectel.com/product-security
16. Fibocom L610-IN (Cat 1 bis with IRNSS/NavIC, AIS-140, pin-compatible with NL668/L716) (snippets). https://www.prnewswire.com/apac/news-releases/fibocom-unveils-the-first-lte-cat1-bis-module-l610-in-with-irnss-and-navic-for-india-302405351.html ; https://www.everythingrf.com/products/cellular-modules/fibocom/811-761-l610-in
17. Quectel NavIC GNSS prices (snippets): Mouser India LC29HAIMD INR 813.46 at 250 (non-stocked, 10 weeks); L89HB-S90 INR 983.05 at 250, 928.07 at 1,000; L89HA-S90 USD 10.96 at 250; LC79D INR 1,401.57. https://www.mouser.in/c/rf-wireless/wireless-modules/gnss-gps-modules/?m=Quectel ; https://www.mouser.co.il/c/rf-wireless/wireless-modules/gnss-gps-modules/?m=Quectel ; L89HA retail https://www.electronicscomp.com/quectel-l89ha-gnss-module-irnss-enabled
18. AIS-140 Finalized Draft AIS-140/DF1 (May 2017), "ITS — Requirements for Public Transport Vehicle Operation": clauses 3.1.1.1–3.1.1.26, 3.1.2.3, Section 4, Table 6B. https://trackobit.com/wp-content/uploads/2025/05/AIS-140-regarding-Intelligent-Transportation-Systems.pdf (saved: AIS-140_Finalized-Draft_May2017.pdf); MoRTH copy https://morth.nic.in/sites/default/files/Finalized_Draft_AIS_140_regarding_Intelligent_Transportation_Systems_.pdf (not opened)
19. ARAI AIS-140 Amendment No. 2 (Dec 2018, adds clause 8.0 code of practice) (snippet) https://hmr.araiindia.com/Control/AIS/14201910518PMAIS-140.pdf ; ARAI list of AIS-140 approved devices as on 16.07.2026 (Amendment 3, 04/2026; GPS + IRNSS(NAVIC)) (snippet; TLS error) https://www.araiindia.com/wp-content/uploads/2026/07/List-AIS-140-as-on-16.07.2026_Updated.pdf
20. Tamil Nadu STA notice 2025-09-17 (VLTD = GNSS (IRNSS) logger + 2G/3G/4G/5G) https://tnsta.gov.in/whatsnew/whatsnew_tn_3bliNRt_2025_09_17.pdf ; Puducherry VLTD-2022 SOP https://transport.py.gov.in/sites/default/files/All-PDF/VLTD-2022-SOP.pdf (snippets)
21. NavIC constellation status 2026 (secondary, snippet, UNVERIFIED). https://superkalam.com/current-affairs/articles/nvs-03-launch-navic-l1-upgrade
22. Diotec Semiconductor, "Automotive Load Dump Protection" application note V10 (ISO 7637-2 / ISO 16750-2 Test A/B table; 35 V / 58 V suppressed). https://p7f.vogel.de/companies/6a/4e/6a4e52d6c1b9a/app-note-load-dump-protection-v10.pdf
23. TI SNOAAA1 (LM74930-Q1 load-dump brief) https://ti.com/lit/pdf/snoaaa1 ; ADI, "Load-Dump Protection for 24V Automotive Applications" https://www.analog.com/en/resources/technical-articles/loaddump-protection-for-24v-automotive-applications.html (snippets)
24. Noiseken, ISO 7637-2 Ed.3 (2011) test overview (pulse levels for 12/24 V) (snippet). https://www.noiseken.co.jp/home/wp-content/uploads/2023/02/ISO7637-2Ed.32011の試験概要.pdf
25. SM8S36A load-dump TVS: LCSC Yangjie SM8S36AQ C2942616 USD 0.6829 at 750+; JLCPCB SMC SM8S36A C3719675 USD 0.7095; DigiKey 58.1 V clamp, 114 A (snippets). https://lcsc.com/datasheet/lcsc_datasheet_2406141740_Yangzhou-Yangjie-Elec-Tech-SM8S36AQ_C2942616.pdf ; https://jlcpcb.com/partdetail/4287495-SM8S36A/C3719675 ; https://www.digikey.sg/en/products/detail/smc-diode-solutions/SM8S36A/10125576
26. TI AN-1519 "DP83848 PHYTER Transformerless Ethernet Operation", SNLA088A (rev. Apr 2013): ≥ 33 nF caps, forced 100 Mb/s, verify links > 1 m. https://www.ti.com/lit/pdf/snla088 (saved)
27. Microchip AN1900 (DS00001900B, 2015–2016), "Transformerless Applications of Microchip's LAN9250/LAN935x": auto-negotiation and Auto-MDIX must be disabled. https://file.aichiplink.com/static/microchip/documents/2025-06-20/0f3995b1a9af3c1548281802d4d824f0.pdf
28. Microchip (Micrel) AN-120, "Capacitive Coupling Ethernet Transceivers without Using Transformers" (listing, snippet). https://microchip.com/en-us/application-notes/micrelan120capacitivecouplinge
29. Zephyr main: drivers/ethernet/dsa contains only the NXP NETC driver; dsa_ksz8xxx.c last commit "net: dsa: remove NET_DSA_DEPRECATED" (2026-03-20/23). https://github.com/zephyrproject-rtos/zephyr/tree/main/drivers/ethernet/dsa ; https://github.com/zephyrproject-rtos/zephyr/commits/main/drivers/ethernet/dsa/dsa_ksz8xxx.c
30. Zephyr PHY bindings and drivers: `ethernet-phy-fixed-link`, `microchip,t1s-phy` (LAN8650/1 B0/B1, LAN8670/1/2 C1/C2/D0), `davicom,dm8806-phy`, `microchip,lan8742`, `microchip,ksz8081`. https://github.com/zephyrproject-rtos/zephyr/tree/main/dts/bindings/ethernet/phy ; https://github.com/zephyrproject-rtos/zephyr/blob/main/drivers/ethernet/phy/phy_microchip_t1s.c
31. Zephyr nucleo_h563zi.dts RMII pinctrl (PC4, PC5, PA1, PA7, PG11, PG13, PB15, PA2, PC1). https://github.com/zephyrproject-rtos/zephyr/blob/main/boards/st/nucleo_h563zi/nucleo_h563zi.dts
32. Microchip KSZ8863RLLI: LCSC C631675 (LQFP-48, -40..+85 °C; USD 3.9993/3.6394 single, other snapshots USD 2.53–4.58) https://www.lcsc.com/product-detail/Ethernet-ICs_Microchip-Tech-KSZ8863RLLI_C631675.html ; LCSC C5229506 (-TR, USD 4.2462 at 1+) https://www.lcsc.com/product-detail/C5229506.html ; Mouser/DigiKey USD 5.16–5.29 at 100 (aggregator snippets) https://www.findchips.com/search/KSZ8863RLLI-TR
33. LAN8671B1-E/U3B USD 3.3026 at 1,000 (ichome, snippet) https://ichome.com/product-detail/microchip-technology/lan8671b1-e-u3b ; LAN8670B1 USD 3.53 (DigiKey highlight, snippet) https://www.digikey.com/en/product-highlight/m/microchip-technology/lan8670-1-2-family-of-10base-t1s-phy
34. Davicom DM8806 (6-port, RMII) https://datasheetbank.com/preview/DM8806-Davicom ; DM8603IEP industrial 3-port (snippet) https://www.alibaba.co.uk/product-detail/Davicom-DM8603IEP-10-100-Mbps-3_11000026033447.html
35. ST LSM6DSOXTR LCSC C481766: USD 1.3929 at 1,000+ (another snapshot USD 1.774) (snippet). https://lcsc.com/product-detail/Accelerometers_STMicroelectronics-LSM6DSOXTR_C481766.html

Earlier reports: [R02] R02_Cellular_4G.md (EC200A bands, retail prices, Zephyr modem drivers); [R06] R06_Power.md (LMR51430, BQ25601, LM74700 prices; Li-ion temperature); [R07] R07_Connector_Mechanical_DFM.md (bridge topology, USB-HS weakness of 2.54 mm headers); [R08] R08_Aggregator_Security_IO.md (bus protocol); [R11] R11_Baseboard_Ethernet.md (STM32H5 RMII pins and erratum, PHY table, HX1188NL, TPD4E05U06, capacitive coupling only in-box); [R14] R14_Baseboard_Costed_BOM.md (box header, SMCJ33A, TPS26600, cell, enclosure); [R15] R15_4G_Integrated_Module.md (EC200A QuecOpen reference with YT8512H, GM520, A7600 no RMII, lean BOM); [R16] R16_Industrial_Router_Reference.md (AR8033-only on EC25, RUT200 EC200A over USB ECM).
