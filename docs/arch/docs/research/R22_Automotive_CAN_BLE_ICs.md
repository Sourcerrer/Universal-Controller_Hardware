# R22 — Automotive CAN-FD + BLE ICs for a vehicle module

Date: 2026-11-16. FX: 1 USD = INR 93.9. Prices are ex-GST distributor list prices on the date shown. Square-bracket numbers are sources (list at the end). **UNVERIFIED** marks anything not confirmed from a primary source in this run. Earlier internal reports used here: R05 (CAN / RS-485 transceivers), R08 / R12 (STM32H533, PSA L3), R17 (4G card, GNSS / AIS-140), R03 (ESP32-C6 Wi-Fi + BLE module).

**Owner hard filters (added during this run), applied to every candidate:**
- **F1 CAN:** on-chip CAN, ideally CAN-FD.
- **F2 BLE.**
- **F3 RS-485:** at least 2 UART-capable ports free, one for RS-485 (with DE / RE control) and one for the stack bus, alongside CAN-FD.
- **F4 Security:** Cortex-M33 (or equivalent) with TrustZone-M, secure boot, a hardware root of trust or secure enclave, and secure key storage. PSA Certified L2 / L3 or SESIP is preferred.

---

## 1. Summary and recommendation

1. **Few single chips combine CAN-FD, BLE and automotive grade.** Five families do in 2026:
   - **NXP KW45**: 1 CAN-FD.
   - **NXP KW47**: 2 CAN-FD, BLE 6.0 with Channel Sounding.
   - **TI CC2745R10-Q1**: 1 CAN-FD, BLE 6.0.
   - **Infineon CYW89829**: 1 CAN-FD, BLE 5.4, but no internal flash and no TrustZone stated.
   - **Microchip PIC32CX-BZ6**: 2 CAN-FD, BLE 6.0, Cortex-M4F, so no TrustZone.

   NXP's industrial twins (MCX W71, MCX W72) have the same CAN-FD and run from -40 to +125 °C, but they are **not AEC-Q100** [1][4][6][9][16][33][37].
2. **Nordic and ST have no BLE + CAN chip.** No nRF52, nRF53 or nRF54 part, and no STM32WB, WB0 or WBA part, has a CAN controller. ST's automotive MCUs (SPC5 / Stellar) have no BLE [19][21][23]. With either vendor, the design needs a second chip: an external CAN-FD controller, or a BLE co-processor.
3. **Parts that pass all four filters (F1–F4)** are listed below. Every other candidate fails at least one filter (§3).

   | Part | Single chip or two chips | Automotive grade | Certificate | Zephyr |
   |---|---|---|---|---|
   | **KW47** | single | AEC-Q100 G2 | PSA L2 | via MCX W72 SoC support |
   | **KW45** | single | AEC-Q100 G2 | PSA L2 + SESIP L2 | via MCX W71 SoC support |
   | **MCX W72 / W71** | single | industrial | PSA L2 | upstream boards |
   | **CC2745R10-Q1** | single | AEC-Q100 G2 | none found | **no Zephyr**; only 2 UARTs, so no spare port |
   | **nRF54L15 + TCAN4550-Q1** | two chips | not AEC-Q100 | PSA **L1** only | best Zephyr maturity |
   | **STM32WBA + TCAN4550-Q1** | two chips | not AEC-Q100 | PSA **L3** + SESIP 3 | upstream |
   | **STM32H533 + BLE co-processor** | two chips | not AEC-Q100 | PSA L3 on the H533 | upstream |
4. **Recommendation: NXP KW47, option (b), a separate "BLE + CAN-FD vehicle module".** Use KW47B42ZB3AFTBR (2 MB, CAN, no LCE), or KW47B42ZB7AFTBR if Channel Sounding (digital key) is planned. The module sits beside the existing ESP32-C6 Wi-Fi + BLE module.
   - **Why KW47:** It is the only part that passes all four filters with:
     - **two CAN-FD channels**, enough for J1939 and OBD-II / ISO 15765 at the same time;
     - AEC-Q100 Grade 2 and -40 to +105 °C ambient;
     - BLE 6.0 with Channel Sounding;
     - TrustZone-M plus the EdgeLock Secure Enclave, with a **PSA Certified L2** certificate;
     - NXP's 15-year longevity statement;
     - a preferred vendor.
   - **Price:** INR 693–767 per chip at 2k on a DigiKey India reel [1][3][10][11].
   - **Prototype now on FRDM-MCXW72.** The MCX W727C is the same 2-CAN-FD silicon family, and Zephyr already supports CAN on it. Move to KW47 for automotive builds. Running Zephyr on a KW47 board through the MCX W72 SoC code is **UNVERIFIED** and should be the first engineering task.
5. **Runner-up: nRF54L15 + TCAN4550-Q1.** Choose it if Zephyr maturity and Nordic matter more than automotive qualification. The CAN controller (TCAN4550-Q1) is AEC-Q100 Grade 1, but the nRF54L15 is not automotive grade and holds **PSA L1 only**.
   - With one CAN-FD channel, the chips cost about the same as KW47 (INR 305 + 262 = 567, plus about INR 63 for an RS-485-side part).
   - A second CAN-FD channel needs a second TCAN4550 (+INR 262), which makes it more expensive than KW47.
6. **Do not replace the ESP32-C6, and do not put the chip on the 4G card.**
   - Replacing the C6 (option a) drops Wi-Fi 6 and Thread / Zigbee.
   - R17 fixes the 4G card as a modem-only card with no processor of ours (option c).
   - Adding BLE to the STM32H533 IO controller (option c) works only as a two-chip design, and the H533 is -40 to +85 °C industrial, not AEC-Q100.
7. **Vehicle tracking needs more than BLE + CAN.** Whichever BLE + CAN chip is chosen, vehicle tracking also needs **GNSS (with NavIC + GAGAN for AIS-140) and cellular**. Both come from the existing 4G modem card with its GNSS option (R17). The vehicle module only adds vehicle-bus data (J1939 / OBD), BLE sensors (TPMS, temperature tags, driver ID, digital key) and RS-485.

---

## 2. Comparison table

Prices are DigiKey India unless stated. The quantity break used is shown in brackets.

| Part | BLE | CAN | UART-capable ports (RS-485 DE) | Grade / temp (ambient unless noted) | Core / flash / RAM (application side) | TrustZone + RoT | Security certificate | Zephyr | Price, INR | Stock / lead time | Pre-certified module | F1–F4 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **NXP KW47B42ZB3 / ZB7** | 6.0, Channel Sounding (LCE on ZB7 / Z97) [1] | **2x CAN-FD** [1] | 2 LPUART (LIN) + FlexIO UART emulation [1]; LPUART RTS-based DE (UNVERIFIED) | **AEC-Q100 G2**, -40…105 °C [1] | CM33 96 MHz; 2 MB + 264 KB (radio side: CM33, 512 KB + 171 KB) [1] | Yes; EdgeLock Secure Enclave, secure boot, tamper pins [1] | **PSA L2** (cert 0632793520481-10000, 23-Dec-2025, includes TF-M 2.1.1) [3] | No KW47 board; same family as the MCX W72 boards (CAN supported) [19][20] | **766.64 (ZB3) / 761.57 (ZB7) @2k reel**; Z83 (1 MB / 136 KB) 693.04 [11] | DigiKey 0 stock, "check lead time" [11] | None found | **PASS** |
| **NXP KW45B41Z83 / Z53** | 5.3 at launch; DS Rev. 10 states "6.3" radio (software-upgradeable); no Channel Sounding (UNVERIFIED) [5][6] | **1x CAN-FD** [6] | 2 LPUART (LIN) + FlexIO [6] | **AEC-Q100 G2**, -40…105 °C [6] | CM33 96 MHz; 1 MB + 128 KB (radio side: CM3, 256 KB + 88 KB) [5] | Yes; EdgeLock Secure Enclave [5] | **PSA L2** (0632793519423-10142, 25-May-2024) [7]; **SESIP L2** (DEKRA) [8] | Via MCX W71 SoC (same certified family) [7][19]; KW45 board UNVERIFIED | **636.26 @2k reel** [12]; LCSC USD 5.864 @1k = 550.7 [13] | DigiKey lead time 39 wk [12] | u-blox NINA-B50 is now MCX W71-based, industrial, -40…85 °C; the automotive KW45 variant is no longer listed [38][39] | **PASS** |
| NXP MCX W727C (industrial KW47) | 6.0 + 802.15.4, CS [4] | 2x CAN-FD (727C only) [4] | 2 LPUART + FlexIO [4] | Industrial, -40…125 °C, **not AEC-Q100** [4] | as KW47 | Yes | PSA L2 (shared with KW47) [3] | **frdm_mcxw72 / mcxw72_evk upstream; CAN yes; no TF-M (_ns) target** [19] | 866.45 (tier not shown) [15] | not shown | None found | PASS, but not automotive |
| NXP MCX W716C (industrial KW45) | 5.3 + 802.15.4 [9] | 1x CAN-FD (option) [9] | 2 LPUART [9] | Industrial, -40…125 °C; 15-yr longevity [9] | as KW45 | Yes | PSA L2 + SESIP L2 [7][8] | **frdm_mcxw71 upstream, CAN yes** [20] | 554.39 @2k reel [14] | Not stocked; lead time 30 wk [14] | u-blox NINA-B501-10B / B506-10B (with CAN): FCC / ISED / RED / UKCA / MIC / KC / NCC / ACMA; **no WPC listed** [38] | PASS, but not automotive |
| **TI CC2745R10-Q1** | **Core 6.0 qualified**, Channel Sounding + APU [16] | 1x CAN-FD (ISO 16845-1 conformance) [16] | **2 UART** (LIN; UART0 has RTS / CTS) [16]; no spare port | **AEC-Q100 G2**, Tj -40…125 °C [16] | CM33 96 MHz; 1 MB / 162 KB [16] | Yes; HSM, secure boot, VGM, ISO 21434 process [16] | None found (UNVERIFIED) | **None.** Zephyr has only the CC23x0 SoC [19] | **502.76 @1k**; 467.95 @4k [18] | 0 stock, 4k due 17-May-2027; lead time 26 wk [18] | None found | Passes, but no spare UART and no Zephyr |
| TI CC2744R7-Q1 | 6.0 | **no CAN** [16] | 2 UART | AEC-Q100 G2 | CM33 | Yes | — | none | — | — | — | FAIL F1 |
| **Nordic nRF54L15** + TI **TCAN4550-Q1** | 6.x, CS [21] | none on-chip; TCAN4550-Q1 adds **1x CAN-FD** (8 Mbps, SPI at 18 MHz, transceiver and 5 V LDO built in) [25] | 5 serial instances (1 HS + 4 shared SPI / TWI / UART; one goes to TCAN SPI) [21]; DE by GPIO (no hardware DE, UNVERIFIED) | nRF: -40…105 °C, **no AEC-Q100** [21][23]; TCAN: **AEC-Q100 G1**, -40…125 °C [25] | CM33 128 MHz + RISC-V; 1.5 MB / 256 KB [21] | Yes; tamper detection, side-channel-protected crypto [21] | **PSA L1** only (0632793520627-13101, 15-Jan-2026); L3 is a design target [22] | **Best:** nrf54l15dk incl. cpuapp_ns (TF-M); `can_tcan4x5x` driver upstream [19] | nRF **305.33 @1k** (230.64 @3k) [24] + TCAN **262.22 @500** (238.73 @3k) [26] = **~567** | nRF 294 in stock, lead time 16 wk; TCAN 0 stock, lead time 26 wk | Raytac, Fanstel, Minew, u-blox nRF54L modules exist (not researched here, UNVERIFIED) | PASS (two chips) |
| nRF54L15 + **Microchip MCP2518FD** (+ transceiver) or **MCP251863** | as above | 1x CAN-FD per chip; MCP251863 includes the transceiver | as above | MCP parts: -40…125 °C ("E" grade); AEC-Q100 status UNVERIFIED | — | — | — | `can_mcp251xfd` upstream [19] | MCP2518FD 155.71 @25 / 140.76 @6k [27] + TCAN1044V 63 (R05); MCP251863 156.93 @3.3k [28] | MCP2518FD 0 stock, lead time 49 wk; MCP251863 1,275 in stock, lead time 48 wk | — | PASS (two chips) |
| **ST STM32WBA55 / WBA65** + TCAN4550-Q1 | 5.4 (WBA5); 802.15.4 | none on-chip (no fdcan node in the Zephyr devicetree) [19]; TCAN4550 adds 1 | USART1 + LPUART1 (+ USART3 on WBA65) [19]; STM32 USART has hardware DE (UNVERIFIED for WBA) | Industrial, no AEC-Q100 | CM33 100 MHz; up to 1 MB (WBA55) / 2 MB (WBA65) | Yes | **PSA L3** (WBA6: 0632793520375-10100, 12-Aug-2025; WBA52 TF-M: 0632793519485-10100) [29][30]; **SESIP 3** [31] | nucleo_wba55cg, nucleo_wba65ri (incl. _ns, TF-M) [19] | WBA55CGU6 573.51 / WBA65RIV7 541.55 (tier not shown) [32] + TCAN 262 = **~800–835** | not shown | ST STM32WB5MMG-class modules exist for WB55; WBA modules UNVERIFIED | PASS (two chips) |
| **ST STM32H533** (existing IO controller) + BLE co-processor | from co-processor | **2x FDCAN** on H533 (R12) | 4 USART + 2 UART + LPUART (R12) | -40…85 °C, no AEC-Q100 | CM33 250 MHz, 512 KB / 272 KB (R12) | Yes | PSA L3 (R08) | nucleo_h533re upstream [19]; BLE via HCI over UART to a WBA, WB0 or nRF54L | H533 already in the BOM (INR 296, R12) + BLE co-processor (nRF54L15 305, or STM32WB05 UNVERIFIED) | — | — | PASS (two chips) |
| Microchip PIC32CX-BZ6 | Core 6.0 + 802.15.4 [33] | **2x CAN-FD** [33] | 6 SERCOM (USART / SPI / I2C) [33] | **AEC-Q100 G1** (reduced parameters) / G2 [33] | **CM4F** 128 MHz; 2 MB / 512 KB [33] | **No TrustZone**; secure boot ROM, eFuse keys [33] | none found | **None** [19] | 361.42 (single listed tier) [34] | 158 in stock [34] | PIC32WM-BZ6 module (not researched) | **FAIL F4** |
| Infineon CYW89829 | 5.4 [37] | 1x CAN-FD + LIN [37] | SCB: at most 2 UARTs at once [37] | **AEC-Q100 G2** [37] | CM33 96 MHz, **no internal flash** (XIP from external QSPI), 256 KB SRAM [37] | TrustZone **not stated**; ROM secure boot, eFuse [37] | CYW20829 has a PSA listing (level not checked) | cyw920829m2evk_02 (CYW20829) upstream [19] | not found | — | — | **FAIL F4** (and needs external flash) |
| Renesas RA4W1 | 5.0 [35] | CAN 2.0B (not FD) [35] | SCI (count not stated) | not stated | CM4 48 MHz, 512 KB / 96 KB | **No** | none | ek_ra4w1 board exists [19] | USD 3.839 = 360.5 [35] | **Not recommended for new designs** [35] | — | **FAIL** |
| Renesas RX23W | 5.0 [36] | CAN (ISO 11898-1, 1 Mbps) [36] | SCI | -40…85 °C [36] | RXv2 54 MHz, 512 KB / 64 KB | **No** (TSIP-Lite) | none | none | USD 3.12–9.20 [36] | **Last time buy** [36] | RX23W module (FCC / CE / Japan) [36] | **FAIL** |
| Espressif ESP32-C6 (current) | 5.x | 2x TWAI (CAN 2.0 only) [ESP-C6] | 2 UART + LP UART | not AEC-Q100 | RISC-V | No TrustZone (PMP / TEE) | PSA L2 (R03) | yes | (R03) | — | many | **FAIL F4** and not automotive |
| Espressif ESP32-C5 | **Core 6.0 certified** [ESP-C5] | **2x CAN-FD** (ISO 11898-1:2015) [ESP-C5] | 2 UART + LP UART | not AEC-Q100 | RISC-V | No TrustZone (TEE) | none yet (R03) | yes | (R03) | — | ESP32-C5 modules | **FAIL F4**, not automotive; it does give Wi-Fi 6 + CAN-FD on the Wi-Fi module |

Notes on the table:
- **Fewer chips with CAN than ordering codes:** only some ordering codes have CAN.
  - KW47: B42ZB7, B42Z97, B42ZB3 and B42Z83 have CAN; ZB6, Z96 and ZB2 do not [1].
  - KW45: Z83 and Z53 have CAN; Z82 and Z52 do not [6].
  - MCX W72: only the 727C has CAN [4].
  - TI: the CC2744R7-Q1 has no CAN [16].

  **Order the CAN variant explicitly.**
- **Silicon Labs EFR32 BG / MG and Renesas DA14531 / DA14535 / DA1469x / DA1470x:** no CAN controller in any of these families (from product knowledge; **UNVERIFIED** in this run). DA1469x and DA1470x are Cortex-M33 without TrustZone (**UNVERIFIED**).
- **BlueNRG-332:** a third-party listing claims an AEC-Q100 BlueNRG-332 (BLE 5.3), but it has no CAN (**UNVERIFIED**).

---

## 3. Filter pass / fail

| Candidate | F1 CAN | F2 BLE | F3 RS-485 + bus UART | F4 TrustZone + RoT | Automotive (AEC-Q100) | Preferred vendor | Verdict |
|---|---|---|---|---|---|---|---|
| NXP KW47 | 2x FD | 6.0 | Yes: 2 LPUART + FlexIO | Yes, PSA L2 | **G2** | Yes | **Recommended** |
| NXP KW45 | 1x FD | 5.3 / 6.x | Yes: 2 LPUART + FlexIO | Yes, PSA L2 + SESIP L2 | **G2** | Yes | Fallback (cheaper, 1 CAN) |
| NXP MCX W72 (727C) / W71 | 2x / 1x FD | 6.0 / 5.3 | Yes | Yes, PSA L2 | Industrial only | Yes | **Prototyping / industrial SKU** |
| TI CC2745R10-Q1 | 1x FD | 6.0 | Marginal: exactly 2 UARTs, none spare | Yes, no PSA / SESIP found | **G2** | No | Fails "Zephyr preferred" |
| nRF54L15 + TCAN4550-Q1 | 1x FD (external) | 6.x | Yes: 4 ports spare | Yes, **PSA L1** | Only the CAN chip | Yes | Runner-up |
| STM32WBA + TCAN4550-Q1 | 1x FD (external) | 5.4 | Yes | Yes, **PSA L3 / SESIP 3** | No | Yes | Strongest security, but costliest and not automotive |
| STM32H533 + BLE co-processor | 2x FD | via co-processor | Yes | Yes, PSA L3 | No | Yes | Fits only if BLE goes on the IO controller |
| PIC32CX-BZ6 | 2x FD | 6.0 | Yes | **No TrustZone** | G1 / G2 | No | Fails F4 |
| Infineon CYW89829 | 1x FD | 5.4 | Max 2 UARTs | **TrustZone not stated**; external flash | G2 | No | Fails F4 |
| Renesas RA4W1 / RX23W / DA14xxx | 2.0B / 2.0 / none | 5.0 / 5.x | — | **No** | No | No | **No Renesas part passes all filters**; RA4W1 is NRND and RX23W is in last-time-buy |
| ESP32-C6 / C5 | TWAI / 2x FD | 5.x / 6.0 | Yes | **No** | No | No | Fails F4 and is not automotive |

---

## 4. Per-candidate notes

### 4.1 NXP KW47 (recommended)
- **Data sheet** Rev. 4, 18 Dec 2025 [1]:
  - BLE 6.0 radio with a Localization Compute Engine for Channel Sounding.
  - **Two FlexCAN with CAN FD** (ISO 11898-1); two LPUARTs with LIN; one FlexIO (UART / SPI / I2C emulation); 2 LPSPI, 2 LPI2C, 1 I3C; 29 GPIO.
  - Application CM33 at 96 MHz with TrustZone-M, up to 2 MB flash with ECC and 264 KB SRAM.
  - Radio side: separate CM33 with 512 KB flash and 171 KB SRAM, so the BLE controller does not use application memory.
  - EdgeLock Secure Enclave: secure boot and debug, TRDC, key generation and storage, TRNG, 4 tamper pins, factory root of trust, encrypted flash with on-the-fly decryption.
  - Supply 1.86–3.6 V. RX 5.2 mA; TX 5.38 mA at 0 dBm and 15.75 mA at +10 dBm.
  - 48-HVQFN 7 × 7 mm with wettable flanks (good for automotive AOI).
- **PSA Certified Level 2** for KW47 / MCX W72, issued 23 Dec 2025 by DEKRA. The certified build includes EdgeLock Enclave 1.3.0, mbedTLS 3.5.0 and **TF-M 2.1.1** [3]. No KW47 SESIP certificate was found (UNVERIFIED).
- **Longevity:** NXP's product page shows the Product Longevity program (10 years, 15 years for automotive) [2]. A web-search summary of NXP's KW47 material says KW47 "will be part of NXP's 15-year Product Longevity program" [10]. I did not open that page myself, and it is not a formal longevity listing, so treat it as **UNVERIFIED** until it is confirmed on NXP's longevity list.
- **Zephyr:** there is no `kw47` SoC or board. Upstream has `frdm_mcxw72` / `mcxw72_evk` on the `mcxw727c` SoC, with CAN, FlexIO, UART and OpenThread support. BLE needs NXP binary blobs, and there is no `_ns` (TF-M) board variant [19][20]. NXP's MCUXpresso SDK supports KW47 (kw47loc release notes). Bringing up KW47 on the mcxw72 SoC code is **UNVERIFIED**: ordering code, fuses and the radio firmware image may differ.
- **Stock:** DigiKey India lists 14 KW47 ordering codes at INR 693–797 per unit at 1.3k–2k, with **0 stock** [11]. Plan on factory lead time; ask NXP India / Avnet / Arrow for allocation.

### 4.2 NXP KW45
- **Data sheet** Rev. 10.0 (21 Oct 2026) [6]:
  - The introduction now says "Bluetooth Low Energy version **6.3** radio", a software upgrade of the original 5.3. Channel Sounding needs KW47-class hardware, so KW45 has no Channel Sounding (UNVERIFIED).
  - **One** FlexCAN FD, 2 LPUART with LIN, FlexIO.
  - AEC-Q100 Grade 2, -40 to 105 °C.
  - Application side 1 MB + 128 KB; radio side CM3 with 256 KB + 88 KB [5].
- **Certificates:** KW45 / K32W148 / MCX W71 hold **PSA L2** [7] and **SESIP L2** (DEKRA, per the GPT_SPE_150 profile) [8].
- **Price:** about INR 551–636 per unit at 1k–2k [12][13].
- **Fit:** the best choice if one CAN-FD channel is enough and cost matters. It is a 2022 design, one generation older than KW47.

### 4.3 NXP MCX W71 / MCX W72 (industrial twins)
- Same security architecture as KW45 / KW47; they add 802.15.4 (Thread / Zigbee / Matter).
- Ambient range -40…125 °C, but **not AEC-Q100** [4][9].
- MCX W71 has a stated 15-year longevity [9].
- These have **real upstream Zephyr boards with CAN** [19][20]. Use FRDM-MCXW72 for firmware bring-up before KW47 parts arrive.

### 4.4 TI CC2745R10-Q1
- **Data sheet** SWRS304D [16]:
  - Bluetooth Core 6.0 qualified, Channel Sounding with an APU for post-processing.
  - 1 CAN-FD with ISO 16845-1 conformance; 2 UART (LIN); 2 SPI; 1 I2C; 23 GPIO.
  - CM33 at 96 MHz with TrustZone-M; HSM with DPA countermeasures; voltage glitch monitor; ISO 21434 process.
  - AEC-Q100 Grade 2. 40-QFN 6 × 6 mm with wettable flanks.
- **Price:** the cheapest automotive single chip with stock pricing, INR 502.76 at 1k [18].
- **Against it:**
  - It is not in upstream Zephyr; Zephyr's TI SimpleLink code covers only CC23x0 [19]. That breaks the family's Zephyr rule.
  - It has only two UARTs, so RS-485 plus the stack bus uses both, leaving no spare.
  - No PSA / SESIP certificate was found.
  - DigiKey has no stock; the next delivery is May 2027 [18].
  - TI is not a preferred vendor.

### 4.5 Nordic nRF54L15 / L10 / L05 (owner question: why not Nordic?)
- **Facts:**
  - Channel Sounding supported; CM33 at 128 MHz with TrustZone plus a RISC-V co-processor; 1.5 MB NVM / 256 KB RAM.
  - 5 serial instances; -40…105 °C; 1.7–3.6 V; QFN48 / QFN52 / CSP47 / QFN40 [21].
  - L10 and L05 are smaller-memory parts of the same series (not separately verified).
- **No CAN on any nRF52 / nRF53 / nRF54 part.** The nRF54L15 product page lists no CAN [21]. Nordic's automotive page names older nRF51824 / nRF52 parts, says nothing about nRF54L, and mentions no CAN [23].
- **No AEC-Q100 nRF54L** was found; we believe none exists [23].
- **Security:** **PSA Certified L1** only (15 Jan 2026); L3 is a design target [22]. That is weaker than KW47 (L2) and STM32WBA (L3).
- **Zephyr / NCS: the best of all candidates.** Upstream `nrf54l15dk` includes `cpuapp_ns` TF-M targets. The `can_tcan4x5x` and `can_mcp251xfd` drivers are upstream [19].
- **Price and stock:** INR 305.33 at 1k; 294 in stock at DigiKey India; lead time 16 weeks [24].
- **Modules:** Raytac (MDBT50Q-class successors), Fanstel, Minew and u-blox nRF54L modules exist. WPC status was **not researched (UNVERIFIED)**.
- **Pairing with an external CAN-FD controller:**
  - **TI TCAN4550-Q1:** SPI CAN-FD controller with a built-in transceiver, 8 Mbps, SPI up to 18 MHz, built-in 5 V LDO (70 mA spare), local and bus wake (WUP). **AEC-Q100 Grade 1**, -40…125 °C, 4.5 × 3.5 mm VQFN-20 [25]. INR 262.22 at 500, 238.73 at 3k. Stock 0, lead time 26 weeks [26].
  - **Microchip MCP2518FD:** controller only; add a TCAN1044V-Q1 (about INR 63, R05). INR 140.76–155.71 [27].
  - **Microchip MCP251863:** controller + transceiver, INR 156.93 at 3.3k, 1,275 in stock [28].

  Both Microchip parts use Zephyr `mcp251xfd`.

### 4.6 ST (owner question: why not STM32?)
- **No STM32 has both BLE and CAN.**
  - Zephyr devicetrees for STM32WB, WB0 (WB05 / 06 / 07 / 09) and WBA (WBA23 / 25 / 52 / 55 / 65) have no FDCAN or bxCAN node [19].
  - A web search found no ST BLE SoC with CAN. ST's automotive SPC5 / Stellar MCUs have CAN but no BLE [23-search].
  - One search summary claimed the STM32WB10CC lists "CAN (FD)". The st.com page timed out, and the WB devicetree has no CAN, so treat that claim as an error (**UNVERIFIED**).
- **(a) STM32WBA + TCAN4550-Q1:**
  - Best certificates: **PSA L3** and **SESIP 3** [29][30][31]. TF-M `_ns` target upstream [19].
  - UARTs: USART1 + LPUART1 (+ USART3 on WBA65). STM32 USART normally has a hardware DE pin (UNVERIFIED for WBA).
  - Not AEC-Q100.
  - Chips ≈ INR 573 (WBA55, tier unknown) + 262 = **≈ INR 835**, the most expensive option. It still has only one CAN-FD channel.
- **(b) STM32H533 (IO controller) + BLE co-processor:**
  - The H533 already gives 2x FDCAN, TrustZone, PSA L3 and many USARTs (R08, R12).
  - Adding an STM32WB05 / WBA or nRF54L15 as a BLE co-processor over HCI-UART costs about INR 300 extra.
  - This turns the IO controller into a vehicle unit. The H533 is not AEC-Q100 and runs -40…85 °C only.
  - Good for an industrial CAN + BLE SKU, not for under-dash automotive.

### 4.7 Renesas (owner question)
- **RA4W1:** Cortex-M4 at 48 MHz, BLE 5.0, **CAN 2.0B (not FD)**, SCE crypto, **no TrustZone**. Status **Not Recommended for New Designs** [35].
- **RX23W:** RXv2 at 54 MHz, BLE 5.0, CAN (ISO 11898-1, 1 Mbps), TSIP-Lite, -40…85 °C. Status **Last Time Buy** [36]. A pre-certified RX23W module exists (Japan / FCC / ISED / CE) [36].
- **DA14531 / DA14535 / DA1469x / DA1470x** (ex-Dialog): BLE-only SoCs with **no CAN** (UNVERIFIED in this run). DA1469x / DA1470x are Cortex-M33 without TrustZone (UNVERIFIED). Zephyr boards exist for DA1469x [19].
- **No newer Renesas BLE MCU with CAN-FD, AEC-Q100 or TrustZone was found.** **No Renesas part passes the owner's filters.**

### 4.8 Others
- **Microchip PIC32CX-BZ6** (launched Oct 2025):
  - Strong hardware: 2x CAN-FD, BLE 6.0, Ethernet, USB, AEC-Q100 Grade 1, 2 MB flash; 158 in stock in India [33][34].
  - **Fails TrustZone** (Cortex-M4F) and has **no Zephyr support**.
  - Worth watching only if the TrustZone rule is relaxed.
- **Infineon CYW89829:** AEC-Q100 Grade 2, BLE 5.4, 1x CAN-FD, LIN. It needs an **external QSPI flash**, at most 2 UARTs at once, and TrustZone is not stated [37]. **Fails.**
- **Espressif ESP32-C5:** **two CAN-FD controllers** and BLE 6.0 certification [ESP-C5], which corrects the assumption that it has TWAI only. The C6 has two TWAI (CAN 2.0) [ESP-C6].
  - Neither is AEC-Q100, and neither has TrustZone.
  - A C5 upgrade on the Wi-Fi module could give **industrial** CAN-FD + Wi-Fi 6 + BLE 6.0 cheaply. It is not an automotive answer.

### 4.9 Head-to-head for vehicle use

| | **NXP KW47** | NXP KW45 | nRF54L15 + TCAN4550-Q1 | STM32WBA55 + TCAN4550-Q1 | STM32H533 + nRF54L15 co-processor | Renesas (any) |
|---|---|---|---|---|---|---|
| Chips | 1 | 1 | 2 | 2 | 2 (H533 already in family) | — |
| CAN-FD | **2** | 1 | 1 (2 with a second TCAN, +INR 262) | 1 | **2** | CAN 2.0 only |
| Silicon cost, 1 CAN channel | INR 693–767 | INR 551–636 | **≈ INR 567** | ≈ INR 835 | ≈ INR 600 | — |
| Silicon cost, 2 CAN channels | **INR 693–767** | n/a | ≈ INR 830 | ≈ INR 1,100 | ≈ INR 600 | — |
| Automotive grade | **AEC-Q100 G2** | **AEC-Q100 G2** | TCAN only (G1) | none | none | none |
| Security certificate | PSA L2 | PSA L2 + SESIP L2 | PSA L1 | **PSA L3 + SESIP 3** | PSA L3 (H533) | none |
| Zephyr maturity | Medium: via MCX W72 SoC code, BLE blobs, no TF-M board | Medium: via MCX W71 | **High**: TF-M ns, tcan4x5x driver | High: TF-M ns | High (HCI) | low / EOL |
| Power | 1.86–3.6 V, RX 5.2 mA | similar | nRF 1.7–3.6 V; TCAN draws VSUP and supplies 5 V for the CAN bus | 1.71–3.6 V (UNVERIFIED) | — | — |
| Supply risk | 0 stock, factory lead time | 39-week lead time | nRF in stock; TCAN 26-week lead time | unknown | H533 OK (R12) | NRND / LTB |
| Longevity | 15 yr (stated) [10] | NXP program | Nordic, not stated | ST 10 yr (UNVERIFIED) | — | ending |

---

## 5. Fit in our family

### (a) Replace the ESP32-C6 on the Wi-Fi + BLE module: **not recommended**
- KW47 has **no Wi-Fi and no 802.15.4**; MCX W72 has 802.15.4 but no Wi-Fi.
- Replacing the C6 drops:
  - Wi-Fi 6 site connectivity: local commissioning, Wi-Fi backhaul, and the PRD Wi-Fi provisioning flow;
  - Thread / Zigbee, unless MCX W72 is used, which is not automotive;
  - the IDF Wi-Fi stack the module already uses.
- A vehicle needs no Wi-Fi in most fleets, since cellular backhaul comes from the 4G card. But the Wi-Fi + BLE module serves the whole family, not only vehicles.
- If CAN-FD on the Wi-Fi module is the real need, the **ESP32-C5** (2x CAN-FD) is the cheap industrial path. It is not automotive.

### (b) Separate "BLE + CAN-FD vehicle module" alongside the Wi-Fi + BLE module: **recommended**
- **Chip:** KW47B42ZB3AFTBR (or ZB7 for Channel Sounding / digital key).
  - CAN-FD #1 for J1939 (250 / 500 kbit/s, 24 V trucks and buses).
  - CAN-FD #2 for OBD-II / ISO 15765-4 or a second body bus.
  - LPUART0 for the stack bus; LPUART1 for RS-485 (fuel sensors, tachograph-type peripherals, displays).
  - FlexIO UART for a console, or for LIN on an LPUART.
  - BLE 6.0 for TPMS, temperature and door sensors, driver ID tags and a phone key.
- **Tracking:** GNSS + cellular come from the 4G card's GNSS option (R17).
- **Rough BOM delta** (module PCB parts, INR, at 1–2k; prices from this report and R05, others estimated):

| Item | Part (example) | INR |
|---|---|---|
| BLE + 2x CAN-FD MCU | KW47B42ZB3AFTBR [11] | 767 |
| 32 MHz + 32.768 kHz crystals | automotive-grade crystals | ~40 (UNVERIFIED estimate) |
| RF match + antenna | chip antenna or U.FL to an external vehicle antenna | ~50 (UNVERIFIED estimate) |
| 2x CAN-FD transceiver | TCAN1044V-Q1 (R05: ~63 each) or NXP TJA1462 / TJA1443 | 126 |
| CAN protection ×2 | ESD2CAN24-Q1-class TVS + split termination | ~30 (R05 range, UNVERIFIED) |
| RS-485 transceiver + protection | THVD1450 (R05: 142–187) or SIT3485 (~17) + TVS / PTC | 60–200 |
| Local 3.3 V regulator (from the baseboard rail) | AEC-Q100 LDO / buck | ~30 (UNVERIFIED) |
| **Subtotal, module electronics** | | **≈ INR 1,100–1,250** |
| Optional, if the module powers itself from the vehicle (ISO 7637-2 / ISO 16750-2 front end: reverse diode / ideal diode, SM8S-class load-dump TVS, 40–60 V AEC-Q100 buck) | | +INR 250–400 (UNVERIFIED) |

- **Alternatives at the same module level:**
  - KW45 (1 CAN): ≈ INR 130–200 less.
  - nRF54L15 + 1× TCAN4550-Q1: ≈ INR 200 less for one CAN; ≈ INR 60 more for two CANs. The TCAN4550 removes the separate CAN transceiver and LDO, so with two TCANs the totals are roughly equal.

### (c) Put the BLE + CAN-FD chip on the IO controller or the 4G card: **not recommended**
- **4G card:** R17 fixes it as a modem-only card with standard Quectel firmware and no processor of ours. Adding a KW47 breaks that rule and puts automotive I/O on a card meant to be swappable.
- **IO controller (STM32H533):** it already has 2x FDCAN, TrustZone and PSA L3. Adding a BLE co-processor (≈ INR 300) gives BLE + CAN-FD with the best Zephyr story. But the H533 is not AEC-Q100 and is -40…85 °C only, and it mixes vehicle-bus wiring into the general IO card. This is acceptable for an industrial "CAN + BLE" SKU, not for an under-dash vehicle product.

---

## 6. Automotive qualification path

1. **Silicon:** use AEC-Q100 parts on the vehicle path.
   - KW47 / KW45: Grade 2.
   - TCAN1044V-Q1 / TCAN4550-Q1: Grade 1.
   - Automotive-grade passives (AEC-Q200) and wettable-flank QFNs for AOI.
   - The module as a whole is not "automotive qualified" without AEC-Q104 or OEM validation. For aftermarket telematics, ISO 16750 + ISO 7637 + EMC testing is the norm.
2. **Power** (the baseboard or vehicle power supply unit, see R17 / R06):
   - ISO 7637-2 pulses 1, 2a, 3a/b and 5a: load dump 65 V on 12 V systems, 123 V on 24 V systems, unless centrally suppressed.
   - ISO 16750-2: 8–32 V operation, 36 V for 60 min on 24 V systems, reverse polarity, cranking profiles.
   - If the vehicle module is fed from the baseboard 3.3 V / 5 V rail, these tests stay on the baseboard.
3. **EMC:** CISPR 25 and ISO 11452-x for OEM fitment. For India aftermarket: AIS-004 Part 3 (EMC for vehicles) via ARAI / ICAT. The exact applicability is UNVERIFIED.
4. **AIS-140 (India VLTD):** the whole tracker is type-approved, not the BLE / CAN chip. R17 lists the requirements: NavIC + GAGAN GNSS, embedded SIM, 8–32 V, 4 h internal battery, IP65, accelerometer + gyroscope, emergency button, SMS fallback, ARAI / ICAT approval, ISO / TS 16949 manufacturing. These are met by the 4G card + baseboard + enclosure. The vehicle module adds CAN / OBD data (optional for AIS-140) and must not break the IP65 / EMC result.
5. **Radio certification:** WPC ETA for 2.4 GHz BLE (license-exempt under GSR 45(E)). A chip-down KW47 design needs its own WPC ETA and RF test. The only CAN-capable NXP module found (u-blox NINA-B50) lists no India / WPC certificate [38]. TEC MTCTE applicability for BLE-only modules is UNVERIFIED.
6. **Cyber:**
   - Our evidence for the EU CRA: KW47 PSA L2 (TF-M in the certified build) [3].
   - For OEM projects, ISO 21434 work products from NXP. TI states ISO 21434 compliance for CC274x [16]; NXP's equivalent is UNVERIFIED.
   - UN R155 / R156 apply to vehicle OEMs, not to aftermarket trackers (UNVERIFIED for India).

---

## 7. Risks and open decisions

1. **Stock and lead time.** Every automotive candidate shows 0 DigiKey India stock:
   - KW47 (lead time unknown); KW45 (39 weeks); CC2745 (26 weeks, next delivery May 2027); TCAN4550 (26 weeks).
   - Ask NXP India / Avnet / Arrow for KW47 allocation before committing.
   - Second source: KW45 (1 CAN, same pin family, 48-HVQFN). Pin compatibility with KW47 is UNVERIFIED.
2. **Zephyr on KW47 is not upstream.** We would run it on the MCX W72 SoC support plus NXP BLE blobs, with no TF-M board target. Decide: carry a local board / SoC port, or use the MCUXpresso SDK + FreeRTOS on this one module. The second option breaks the "Zephyr everywhere" preference.
3. **BLE controller blobs.** NXP BLE on Zephyr needs NXP's binary radio firmware. Nordic has the most open and mature stack.
4. **Security level.** KW47 is PSA L2. STM32WBA (L3 / SESIP 3) is stronger but is not automotive and has no CAN. Decide whether PSA L2 is enough for the CRA path (it normally is for "important" class I products; legal view UNVERIFIED).
5. **One CAN vs two CANs.** If one CAN-FD is enough (OBD **or** J1939, not both), KW45 or nRF54L15 + TCAN4550 is cheaper. Decide from the target fleet.
6. **Channel Sounding / digital key:** needs KW47 ZB7 / Z97 (LCE) or CC2745. Decide if it is in scope; it adds about INR 0–5 per chip [11].
7. **Module certification.** A chip-down design means our own WPC ETA, FCC / CE later, and Bluetooth SIG listing (the end product can reference NXP's QDID). No pre-certified KW47 module was found.
8. **Not verified in this run:**
   - KW47 pin compatibility with KW45; KW47 SESIP; KW45 Channel Sounding (assumed none).
   - Hardware RS-485 DE on LPUART, the WBA USART and the nRF54L UARTE.
   - Prices for STM32WBA at 1k, CYW89829, and STM32WB05 as a co-processor.
   - Nordic module WPC status.
   - SiLabs / DA14xxx "no CAN" checks.
   - ESP32-C5 temperature grade.
   - Current u-blox NINA-B50 automotive variant status.

---

## 8. Sources

1. NXP KW47 product data sheet Rev. 4, 18 Dec 2025 — https://www.nxp.com.cn/docs/en/data-sheet/KW47DS.pdf (local copy: ../datasheets/wifi_ble/NXP_KW47_datasheet.pdf)
2. NXP KW47 product page — https://www.nxp.com/products/KW47
3. PSA Certified, KW47 / MCX W72, Level 2 — https://products.psacertified.org/products/kw47-mcx-w72
4. NXP MCX W72 product data sheet Rev. 5, 28 Jul 2026 — https://www.nxp.com/docs/en/data-sheet/MCXW72.pdf
5. NXP KW45 product page — https://www.nxp.com/products/KW45
6. NXP KW45 product data sheet Rev. 10.0, 21 Oct 2026 — https://www.nxp.com.cn/docs/en/data-sheet/KW45.pdf (local copy: ../datasheets/wifi_ble/NXP_KW45_datasheet.pdf)
7. PSA Certified, KW45 / K32W148 / MCX W71, Level 2 — https://products.psacertified.org/products/kw45-k32w148-mcx-w71-product-family-version-01b/certificates
8. DEKRA, SESIP L2 + PSA L2 for KW45 / K32W148 / MCX W71 — https://dekra.com/en/dekra-accredited-laboratory-for-sesip-psa-certifies-nxp
9. NXP MCX W71 product page — https://www.nxp.com/products/MCX-W71X
10. NXP KW47 Knowledge Hub (15-year longevity statement) — https://community.nxp.com/t5/Wireless-Connectivity-Knowledge/KW47-Knowledge-Hub/ta-p/2044608
11. DigiKey India, KW47B42Z search (2026-11-16) — https://www.digikey.in/en/products/result?keywords=KW47B42Z
12. DigiKey India, KW45B41Z83AFTBR — https://www.digikey.in/en/products/result?keywords=KW45B41Z83AFTBR
13. LCSC, KW45B41Z83AFTBR (price from a search snippet) — https://lcsc.com/product-detail/RF-Transceiver-ICs_NXP-Semicon-KW45B41Z83AFTBR_C20234182.html
14. DigiKey India, MCXW716CMFTAR — https://www.digikey.in/en/products/result?keywords=MCXW716CMFTAR
15. DigiKey India, MCXW727CMFTBR — https://www.digikey.in/en/products/result?keywords=MCXW727CMFTBR
16. TI CC274xR-Q1 / CC274xP-Q1 data sheet SWRS304D, Nov 2025 — https://www.ti.com/lit/gpn/CC2745R10-Q1 (local copy: ../datasheets/wifi_ble/TI_CC2745R10-Q1_datasheet.pdf)
17. TI CC2745R10-Q1 product page — https://www.ti.com/product/CC2745R10-Q1
18. DigiKey India, CC2745R10E0WRHARQ1 — https://www.digikey.in/en/products/result?keywords=CC2745R10E0WRHARQ1
19. Zephyr RTOS GitHub main, checked 2026-11-16: boards/nxp, boards/ti, soc/ti/simplelink, boards/nordic/nrf54l15dk, boards/st, boards/infineon, boards/renesas, boards/microchip, drivers/can, dts/arm/st/{wb,wb0,wba} — https://github.com/zephyrproject-rtos/zephyr
20. Zephyr frdm_mcxw71 / frdm_mcxw72 board files (dts `zephyr,canbus = &flexcan0`; yaml "can") — https://github.com/zephyrproject-rtos/zephyr/tree/main/boards/nxp/frdm_mcxw71 and https://github.com/zephyrproject-rtos/zephyr/tree/main/boards/nxp/frdm_mcxw72
21. Nordic nRF54L15 product page — https://www.nordicsemi.com/Products/nRF54L15
22. PSA Certified, nRF54L15 / nRF54L10, Level 1 — https://products.psacertified.org/products/nrf54l15-nrf54l10
23. Nordic automotive page — https://www.nordicsemi.com/Applications/Automotive ; ST search for a BLE + CAN SoC (2026-11-16), no match; ST automotive brochure https://www.st.com/resource/en/brochure/st12630_brautoten1118_lr.pdf
24. DigiKey India, NRF54L15-QFAA-R — https://www.digikey.in/en/products/detail/nordic-semiconductor-asa/NRF54L15-QFAA-R/24773448
25. TI TCAN4550-Q1 product page — https://www.ti.com/product/TCAN4550-Q1
26. DigiKey India, TCAN4550RGYRQ1 — https://www.digikey.in/en/products/result?keywords=TCAN4550RGYRQ1
27. DigiKey India, MCP2518FDT-E/QBB — https://www.digikey.in/en/products/result?keywords=MCP2518FDT-E%2FQBB
28. DigiKey India, MCP251863T-E/9PX — https://www.digikey.in/en/products/result?keywords=MCP251863T-E%2F9PX
29. PSA Certified, STM32WBA6, Level 3 — https://products.psacertified.org/products/stm32wba6/certificates
30. PSA Certified, STM32WBA52 TF-M, Level 3 — https://products.psacertified.org/products/stm32wba52-tfm/certificates
31. ST SG0048, STM32WBA6xxx SESIP Level 3 guidance — https://www.st.com.cn/resource/en/security_guidance/sg0048-stm32wba6xxx-sesip-level-3-certification-stmicroelectronics.pdf
32. DigiKey India, STM32WBA55CGU6 and STM32WBA65RIV7 — https://www.digikey.in/en/products/result?keywords=STM32WBA55CGU6 ; https://www.digikey.in/en/products/result?keywords=STM32WBA65RIV7
33. Microchip PIC32CX-BZ6 family features — https://onlinedocs.microchip.com/oxy/GUID-632D2AAD-E8A7-4655-85D3-738D9951FC09-en-US-1/GUID-F0555D61-1537-4417-B888-1DF7C77E03DC.html
34. DigiKey India, PIC32CX2051BZ62132 — https://www.digikey.in/en/products/result?keywords=PIC32CX2051BZ62132
35. Renesas RA4W1 product page — https://www.renesas.com/en/products/ra4w1
36. Renesas RX23W product page — https://www.renesas.com/en/products/rx23w
37. Infineon CYW89829 data sheet 002-39637 Rev. *C — https://www.infineon.com/assets/row/public/documents/30/49/infineon-cyw89829-datasheet-en.pdf
38. u-blox NINA-B50 product summary UBX-23007102 R08 — https://www.u-blox.com/sites/default/files/documents/NINA-B50_ProductSummary_UBX-23007102.pdf (local copy: ../datasheets/wifi_ble/u-blox_NINA-B50_product_summary.pdf)
39. eeNews Europe, u-blox NINA-B5 (KW45 automotive / K32W148 professional) — https://www.eenewseurope.com/en/bluetooth-le-stand-alone-module-has-automotive-interfaces ; u-blox information note UBXDOC-465451970-3247 (NINA-B50 professional grade release, 18 Mar 2024) — https://www.u-blox.com/sites/default/files/documents/NINA-B50x-00B-IP_IN_UBXDOC-465451970-3247.pdf
- ESP-C6: Espressif ESP32-C6 data sheet v1.6 (local ../datasheets/wifi_ble/Espressif_ESP32-C6_datasheet.pdf): "Two TWAI controllers, compatible with ISO 11898-1 (CAN Specification 2.0)".
- ESP-C5: Espressif ESP32-C5 data sheet v1.5 (local ../datasheets/wifi_ble/Espressif_ESP32-C5_datasheet.pdf): "Two CAN FD controllers, compatible with ISO 11898-1:2015"; "Bluetooth LE: Bluetooth Core 6.0 certified".
- Internal: R05 (TCAN1044V-Q1 ~INR 63, THVD1450 INR 142–187, SIT3485 ~INR 17), R08 / R12 (STM32H533 INR 296, PSA L3, 2x FDCAN), R17 (AIS-140 requirements, 4G card rules, ISO 7637-2 levels), R03 (ESP32-C6 module).
