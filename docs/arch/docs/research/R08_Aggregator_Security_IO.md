# R08 — Baseboard (Aggregator) MCU, Secure Element, Shared IO Front End, Storage and Stack Bus

Status: COMPLETE WITH GAPS (2026-11-14). The shared web-search budget ran out part-way. The MCU section is sourced. The secure-element, IO-cost and storage sections rely in part on figures marked **UNVERIFIED**, which must be confirmed before freezing the BOM (see section 8). Every sourced fact carries [Sn] (section 9).

Date of research: 2026-11-13 / 2026-11-14. Currency: USD→INR = 94.0 (mid-market 93.93 on 2026-11-08 per currencybeacon [S1], rounded up as a margin). Prices are distributor catalogue prices (DigiKey India, INR, fetched 2026-11-14) unless stated otherwise. They are upper bounds: franchised 1k-quantity quotes are normally lower.

## 1. Executive summary and recommendation

1. **Primary aggregator MCU: STM32H533RET6** (Cortex-M33 250 MHz, 512 KB flash, ~272 KB RAM, LQFP64). It has 4 USART + 2 UART + 1 LPUART, **2x FDCAN**, 2x I3C and USB FS [S2]. It holds **PSA Certified Level 3** (Apr 2025) [S4], and ST relies on the H573's SESIP3 certificate for it [S5]. Price: INR 377 @500 at DigiKey India [S24]; LCSC ~USD 4.7–4.9 @100 (≈ INR 445–457) [S32]. It is the only shortlisted LQFP part that combines a certified PSA L3 security level with 2x CAN-FD and 7 UARTs, so it can also host the fieldbus (1x CAN-FD + 2x RS-485) directly. **Risk:** DigiKey shows 0 stock and a 52-week standard lead time [S24].
2. **Same-footprint cost-down: STM32H523RET6** (same pin-out, no crypto or security services). INR 326 @500 [S23]. Acceptable only if the secure element holds all keys.
3. **Alternate vendor: NXP MCX N236 (MCXN236VKLT, HLQFP100).** 8x LP_FLEXCOMM (UART/SPI/I2C), 2x CAN-FD, EdgeLock Secure Enclave [S16]. INR 604 @540 [S27]. No PSA/SESIP certificate was found (UNVERIFIED). Caution: the older MCXN236**VNLT** order code is **obsolete** [S28], and MCXN947VNLT is discontinued at DigiKey [S29]. NXP LPC55S16 (PSA L2 / SESIP L2 [S20][S21], 1x CAN-FD, but only 256 KB flash) is the conservative NXP fallback at INR 434 @640 [S30].
4. **Lowest cost: STM32C5A3RGT6** (new in 2026: Cortex-M33 144 MHz, 1 MB / 256 KB, 4 USART + 3 UART + LPUART, up to 2 FDCAN, USB FS, DPA-resistant AES + PKA + HUK) [S11][S12]. INR 229 @640 [S26]; ST's 10k resale price is USD 1.36 ≈ INR 128 [S11]. **It has no TrustZone** [S13], so TF-M cannot run on it. Use it only together with a secure element, and accept that the MCU itself carries no PSA L3 certification.
5. **Nordic nRF54L15 does not fit as the brain** (no CAN, no USB, only 5 serial instances [S37]). STM32U545 (5 UARTs, 1 FDCAN [S8]; INR 521 [S25]) and STM32U3 (1 FDCAN [S9]) offer fewer interfaces for more money.
6. **Secure element (the product owner has decided one will be fitted):** the shortlist is **NXP SE050E** (CC EAL6+, EdgeLock 2GO remote provisioning, I2C, -40…105 °C [S38]) and **Microchip ATECC608B Trust&GO** or **ST STSAFE-A110** (both pre-provisioned, cheaper; their details and prices are UNVERIFIED in this run). A pre-provisioned SE means the contract manufacturer needs **no HSM and no key injection**: it only places the part and records serial numbers. This is the main reason to keep the SE even though the H533 has PSA L3.
7. **Stack bus (pass-through, 40 pins):** a multi-drop 3.3 V UART as the default data path. CAN-FD is an optional second transport for parts that have it; ESP32-C6 has only classic CAN (TWAI) [R03 S52] and nRF54L has none [S37]. I2C carries discovery and the module-ID EEPROM. A daisy-chained token line handles auto-addressing, and per-position power-enable and chip-select lines are carried on rotated pins. The pin budget is in section 4.
8. **IO mix (baseboard): 4 universal AI + 4 isolated DI + 4 protected DO + independent window watchdog.**
   - AI: discrete, using the MCU ADC plus a shared ADS1115 for PT1000 [S43].
   - DI: 2x ISO1212, IEC 61131-2 Type 1/2/3, ±60 V [S39].
   - DO: 2x TPS272C45, 24 V, 45 mΩ, adjustable 0.7–4 A limit [S40].
   - Watchdog: TPS3430 window watchdog gating the DO enables [S42].
   - Estimated added BOM ≈ **INR 1,050–1,500 for 12 channels (≈ INR 90–125 per channel)**. These IO prices are **UNVERIFIED budget estimates**.
9. **Storage / RTC:** 128 Mbit SPI NOR for A/B images and logs, a small FRAM for counters, and the MCU RTC on VBAT (tamper pins). Add an external RTC (RV-3028 class) only if long holdover on a coin cell is required. Part prices here are UNVERIFIED.

## 2. Requirements used for this selection (after the 2026-11-13 update)

Baseboard MCU = the gateway "brain": owns all configurable IO and ADC inputs, routes data between modules on a stackable pass-through bus, holds keys (with a secure element), power-cycles hung modules, and may host the wired fieldbus directly (1x CAN-FD + 2x RS-485).

| Requirement | Value used |
|---|---|
| UART | ≥ 1 stack-bus UART (multi-drop RS-485-style), debug, 2x RS-485 fieldbus, spare → ≥ 5 U(S)ARTs; 6+ preferred |
| CAN | ≥ 1 CAN-FD (fieldbus); a 2nd CAN-FD is attractive as an optional stack-bus transport |
| SPI / I2C | ≥ 2 SPI (stack bus + flash/ADC), ≥ 2 I2C (or I3C) (module-ID EEPROM/discovery + local sensors/SE) |
| ADC | ≥ 8 channels, ≥ 12 bit |
| RTC | VBAT + tamper inputs |
| USB | FS device (service port) |
| Security | TrustZone-M, secure boot, crypto accel., protected key storage, PSA/SESIP level stated |
| Memory | ≥ 512 KB–1 MB flash (A/B update), ≥ 256 KB RAM (relaxed to ≥ 128 KB for cost-tier options) |
| Package | LQFP/QFN only |
| Software | Zephyr (+TF-M, MCUboot), ThreadX |
| Cost | Very cost-sensitive; finished cost = BOM x 1.4 |

## 3. Aggregator MCU candidates

### 3.0 Comparison table

"Fit" means the part covers 1 stack-bus UART + 2 RS-485 + debug + spare (≥ 5 UART), ≥ 1 CAN-FD, and USB FS, in LQFP/QFN.

| Candidate | Core / flash / RAM | UART | CAN-FD | USB FS | TrustZone / certified level | Pkg | Price (INR, DigiKey IN) | Fit |
|---|---|---|---|---|---|---|---|---|
| **STM32H533RET6** | M33 250 MHz / 512 KB / ~272 KB | 4+2+LP [S2] | 2 [S2] | yes [S2] | Yes; **PSA L3 certified** [S4]; SESIP3 via H573 (ST statement) [S5] | LQFP64 | 377 @500 [S24] | **Primary** |
| STM32H523RET6 | M33 250 MHz / 512 KB / 272 KB [S6] | as H533 (UNVERIFIED for H523; same die family) | 2 [S2] | yes | Yes; no crypto/certification found | LQFP64 | 326 @500 [S23] | Cost-down |
| STM32H563/H573 | M33 250 MHz / up to 2 MB | UNVERIFIED | UNVERIFIED | yes | H573 SESIP3 + PSA L3 (per [S5]); TF-M platform STM32H573I-DK [S35] | LQFP64+ | not fetched | Upsize option |
| STM32U545RET6Q | M33 160 MHz / 512 KB | 2+2+LP [S8] | 1 [S8] | yes [S8] | Yes; PSA L3 + SESIP3 listed by ST [S8] | LQFP64 | 521 @640 [S25] | Marginal (5 UART) |
| STM32U585 | M33 160 MHz / 2 MB | UNVERIFIED | 1 (UNVERIFIED) | yes | PSA L3/SESIP3 (ST PR [S8 family]); TF-M B-U585I-IOT02A [S35][S36] | LQFP | not fetched | Too costly |
| STM32U375/U385 | M33 ULP / up to 1 MB | UNVERIFIED | 1 [S9] | UNVERIFIED | Yes, DPA AES/PKA [S9]; no cert found; TF-M U3C5 [S35] | 32–100 pin | ~USD 4.05 @100 (ST eStore) ≈ 381 [S10] | Marginal |
| STM32L5 (L552/L562) | M33 110 MHz / 512 KB | UNVERIFIED | 1 (UNVERIFIED) | yes (UNVERIFIED) | Yes; TF-M upstream [S35][S36] | LQFP | not fetched | Superseded by H5/U5 |
| **STM32C5A3RGT6** | M33 144 MHz / 1 MB / 256 KB [S12] | 4+3+LP [S11][S12] | up to 2 [S11] | yes [S12] | **No TrustZone** [S13]; AES/PKA/HUK; PSA L3/SESIP3 only "targeted" (UNVERIFIED) [S12] | LQFP64 | 229 @640 [S26]; USD 1.36 @10k ST [S11] | **Lowest cost (with SE)** |
| STM32C562RET6 | M33 144 MHz / 512 KB / 128 KB [S12] | 4+3+LP (series) [S12] | 0–1 [S12] | yes | No TrustZone; AES [S12] | LQFP64 | USD 1.39 @5,120 (DigiKey US) ≈ 131 [S34] | Cheapest, RAM-limited |
| STM32G0B1 / STM32C0 | M0+ | — | G0B1: yes (UNVERIFIED) | — | No TrustZone | — | not fetched | Replaced by C5 as cost baseline |
| STM32G5 | M33 280 MHz mixed-signal | 2+3+LP [S15] | 1 [S15] | — | — | 32–80 pin | "Preview" status [S15] | Too new |
| **MCX N236 (MCXN236VKLT)** | M33 150 MHz / 1 MB | 8 FlexComm [S16] | 2 [S16] | UNVERIFIED | Yes; EdgeLock Secure Enclave Core Profile [S16]; no cert found | HLQFP100 | 604 @540 [S27] | **NXP alternate** |
| MCX N547/N947 | dual M33 150 MHz / 2 MB | FlexComm ×10 (UNVERIFIED) | 2 (UNVERIFIED) | yes | Yes; ELS S50 [S18]; cert not found [S19]; TF-M FRDM-MCXN947 [S35] | HLQFP100 | N947: 889 @180; **discontinued at DigiKey** [S29] | Too costly |
| MCX A (e.g. MCXA577) | M33 | UNVERIFIED | UNVERIFIED | UNVERIFIED | FRDM-MCXA577 is a TF-M platform, so has TrustZone [S35] | — | not fetched | Re-check (promising, not researched) |
| LPC55S16JBD64E | M33 150 MHz / 256 KB | 8 FlexComm (UNVERIFIED) | 1 [S22] | yes (UNVERIFIED) | Yes; **PSA L2 + SESIP L2** [S20][S21] | HTQFP64 | 434 @640 [S30] | Fallback (flash tight for A/B) |
| LPC55S36 / S69 | M33 / 256–640 KB | UNVERIFIED | S36: yes (UNVERIFIED) | yes | S69: TF-M LPCXpresso55S69 [S35] | — | not fetched | — |
| i.MX RT (RT1050/1060…) | M7, external flash, mostly BGA (UNVERIFIED) | — | — | — | No TrustZone-M (UNVERIFIED) | BGA | — | Rejected (BGA, no TZ-M) |
| nRF54L15 | M33 128 MHz / 1.5 MB / 256 KB [S37] | 5 serial total [S37] | **none** [S37] | **no** [S37] | TrustZone, tamper, side-channel crypto [S37]; PSA level not found | QFN48 | 305 @1k [S31] | Does not fit |
| nRF54H20 | multi-core, WLCSP (UNVERIFIED) | — | — | — | — | not LQFP/QFN (UNVERIFIED) | — | Rejected |

Longevity: ST and NXP both run 10-year (or longer) longevity programmes. NXP's states "minimum of 10 years" for participating products [S38]. The per-part commitment for H5/C5/MCX N was **not verified in this run**; check ST's longevity list and NXP's Product Longevity page.

Zephyr / ThreadX: Zephyr TF-M non-secure targets cover U5, L5 and LPC55S69 [S36], and upstream TF-M also covers H5 (H573I-DK), U3, MCX N947 and MCX A577 [S35]. For the H523/H533 itself: the Zephyr board port, MCUboot and ThreadX (STM32CubeH5 / X-CUBE-AZRTOS) were not individually verified in this run (UNVERIFIED). ST positions TF-M/STM32Trust on the H5 [S4][S5].

Why the H533 rather than H573: the H533 already has PSA L3, 2x FDCAN and enough UARTs. The H573 adds 2 MB flash. Move up only if 512 KB is too small for TF-M + MCUboot + an A/B application. That needs sizing: plan ~64 KB bootloader, ~128–160 KB TF-M, and 2 × ~150 KB app slots (an engineering estimate). If it does not fit, put the secondary slot in external SPI NOR (MCUboot "swap/overwrite with external secondary slot" is supported — UNVERIFIED for this exact target).

### 3.1 Findings so far (with sources)

- STM32H523/H533 (Cortex-M33, 250 MHz): H533 lists 4 USART + 2 UART + 1 LPUART, 2x FDCAN, 2x I3C [S2]; packages LQFP48/UFQFPN48/LQFP64/LQFP100/LQFP144 [S2][S3]. H533 holds PSA Certified Level 3 (cert. 0632793520047-10100, issued 04/03/2025, lab SGS Brightsight) for "STM32H533xx with Security Services" [S4]. ST states H533 has no separate SESIP certificate; it relies on STM32H573 SESIP3 (SESIP-2300042-01) — ST community statement, treat as vendor position [S5]. STM32H523RCT6 (LQFP64, 256 KB flash, 274 KB RAM) Future Electronics ~USD 2.15 @250+ [S6]; DigiKey IE STM32H523RCT6 ~EUR 2.26 @100 [S7].
- STM32U545 (Cortex-M33 ULP): 2 USART + 2 UART + 1 LPUART, 1 FDCAN, USB FS; ST lists PSA Level 3 and SESIP Level 3 [S8].
- STM32U375/U385 (STM32U3): TrustZone, DPA-resistant AES + PKA, CCB, 1 FDCAN, I3C, 32–100 pins [S9]; no PSA certificate found (UNVERIFIED); ST eStore STM32U385CGT6 ~USD 4.05 @100–499 [S10].
- NEW: STM32C5 series (2026, Cortex-M33 144 MHz, entry-level): 4 USART + 3 UART + 1 LPUART, up to 2 FDCAN, up to 3x 12-bit ADC (up to 28 ext. ch.), USB FS host/device, LQFP32…LQFP144 and UFQFPN [S11][S12]. C5A3 = 1 MB flash/256 KB RAM, AES (dual, DPA-resistant), PKA, HUK; C59x = ECDSA, HUK [S12]. **No TrustZone**: Keil device DB lists STM32C5A3KG as "NO_TZ" [S13]; ST pages describe only MPU [S11]. ST recommended resale: C5A3 USD 1.36 @10k, C531 USD 0.64 @10k [S11]. "Now entering production" (March 2026) [S12]; Zephyr has nucleo_c5a3zg and xiao_stm32c5 boards [S14]. CNX reports SESIP3/PSA L3 as a *target* for the series (UNVERIFIED, no certificate found) [S12].
- NEW: STM32G5 series (announced 2026-11): 280 MHz Cortex-M33 mixed-signal, status "Preview" — too new to design in [S15].
- NXP MCX N23x (MCXN236): 8x LP_FLEXCOMM (each UART/SPI/I2C), 2x FlexCAN-FD, EdgeLock Secure Enclave (Core Profile), HLQFP100 [S16]; element14 SG MCXN236VNLT SGD 8.45 @250+ [S17]. No PSA certificate found (UNVERIFIED).
- NXP MCX N947: TrustZone, secure boot ROM, ELS S50 secure subsystem [S18]; NXP markets MCX as "supporting" SESIP3/PSA L3/FIPS 140-3 but no N947 certificate found [S19] (UNVERIFIED).
- NXP LPC55S16: PSA Certified Level 2 + SESIP Level 2 (Brightsight, 2020) [S20][S21]; CAN-FD [S22].

### 3.2 DigiKey India price snapshot (INR, fetched 2026-11-14, catalogue price incl. no GST; highest break shown)

| Part | Package | Status / stock / lead time | Highest break shown | Source |
|---|---|---|---|---|
| STM32H523RET6 (512 KB) | LQFP64 | Active, 0 stock, 52 wk | INR 326.38 @500 | [S23] |
| STM32H533RET6 (512 KB, crypto/SE services) | LQFP64 | Active, 0 stock (960 due 21-Dec-2026), 52 wk | INR 377.31 @500 | [S24] |
| STM32U545RET6Q (512 KB) | LQFP64 | Active, 0 stock, 52 wk | INR 521.31 @640 | [S25] |
| STM32C5A3RGT6 (1 MB/256 KB, no TrustZone) | LQFP64 | Active, 0 stock, 52 wk | INR 229.33 @640 (T&R) | [S26] |
| MCXN236VKLT (1 MB) | HLQFP100 | Active, 0 stock, 13 wk (MCXN236VNLT is **obsolete**) | INR 603.70 @540 | [S27][S28] |
| MCXN947VNLT (2 MB dual-core) | HLQFP100 | **Discontinued at DigiKey**, 285 stock | INR 889.36 @180 | [S29] |
| LPC55S16JBD64E (256 KB) | HTQFP64 | Active, 17 stock, 39 wk | INR 434.02 @640 | [S30] |
| nRF54L15-QFAA-R (1.5 MB RRAM, BLE) | QFN48 | Active, 304 stock, 16 wk | INR 305.33 @1k (CT); INR 230.64 @3k reel | [S31] |

Other price points: LCSC STM32H533RET6 (C26082149) ~USD 4.73–4.86 @100+ (search snapshot, live page did not show price) [S32]; TME STM32C5A3VGT6 USD 2.51 @1,080 (search snapshot) [S33]; DigiKey US STM32C562RET6 ~USD 1.39 @5,120 (search snapshot) [S34]; ST recommended resale @10k: STM32C5A3 USD 1.36, STM32C562 USD 0.98, STM32C531 USD 0.64 [S11].
Software: upstream TF-M platform list (2026-11) includes STM32U5 (B-U585I-IOT02A), STM32L5, STM32U3 (Nucleo-U3C5ZI-Q), STM32H5 (STM32H573I-DK), LPCXpresso55S69, FRDM-MCXN947, FRDM-MCXA577; Nordic only nRF5340/nRF9160/nRF9161 (nRF54L is handled in the nRF Connect SDK, not upstream TF-M — UNVERIFIED) [S35]. Zephyr's TF-M doc lists b_u585i_iot02a, nucleo_l552ze_q, stm32l562e_dk, lpcxpresso55s69 as non-secure targets [S36].
nRF54L15: Cortex-M33 128 MHz + RISC-V coprocessor, 1.5 MB NVM/256 KB RAM, 5 serial instances total (1 HS SPI/UART + 4 SPI/TWI/UART), **no CAN, no USB**, ADC 8 ch 10-bit (14-bit oversampled), TrustZone, tamper detection, side-channel-protected crypto; QFN40/48/52 [S37].
Note: DigiKey catalogue prices are well above negotiated 1k prices from ST/NXP franchised distributors in India; treat them as an upper bound.

## 4. Inter-module stack bus and 40-pin budget

Constraint: modules are enclosed and stacked side by side with a pass-through bus (R07), so star-wired "one UART per slot" is impossible. Every bus line is shared unless position-specific lines are created by pin rotation.

### 4.1 Transport options against the MCUs used on modules

| Option | Baseboard H533 | ESP32-C6 (Wi-Fi/BLE, 4G combo host) | Nordic nRF54L | STM32/NXP module MCUs | Verdict |
|---|---|---|---|---|---|
| Multi-drop UART, 3.3 V (host TX broadcast; module TX tri-stated or open-drain; addressed frames + CRC) | 7 U(S)ARTs [S2] | yes (UART available; count not checked here) | yes, 5 serial [S37] | yes | **Default data path.** Works on every MCU. Use 1–4 Mbaud with short stack traces; real limit UNVERIFIED (depends on stack length and capacitance) |
| CAN / CAN-FD (logic-level or with transceivers) | 2x FDCAN [S2] | **classic CAN only (TWAI)**; ESP32-C5 has CAN-FD [R03 S52/S57] | **none** [S37] | most STM32/MCX parts have it | Optional second transport. Cannot be mandatory because nRF54L and ESP32-C6 lack CAN-FD |
| SPI with per-position chip-select (rotated pins) or daisy-chained CS | 3+ SPI | yes | yes | yes | High-throughput path for the 4G + Ethernet + Wi-Fi card. Needs per-position CS lines |
| I2C (or I3C on H533 [S2]) | yes | yes | yes | yes | **Discovery and module-ID EEPROM** (24LC04B-class, INR 32 @25 at DigiKey India [S45]). Fixed EEPROM address per module, made unique through the token-enabled address pin or by enabling only one module at a time |
| Daisy-chained token (TOKEN_IN → TOKEN_OUT) | GPIO | GPIO | GPIO | GPIO | **Auto-addressing**: each module takes the next address while its TOKEN_IN is active, then passes the token on |
| Shared open-drain IRQ_n | GPIO | GPIO | GPIO | GPIO | Attention line. The host then polls for the source |
| Per-position PWR_EN / RESET (rotated pins) | GPIO | — | — | — | Lets the brain **power-cycle a hung module** without that module's cooperation. Must be hardware: a module-side load switch driven from its own rotated pin |

Pin rotation: each module connects its input pin k to output pin k−1 for a group of N lines. The module therefore always uses "pin 1" of the group, yet sees a line that is unique to its position. This is a design proposal, not sourced. It costs N pins per signal type, where N is the maximum number of modules (5).

### 4.2 Recommended 40-pin budget

| Group | Pins | Notes |
|---|---|---|
| Bus power (regulated intermediate rail, value decided in R06) | 6 | 40-pin candidates are rated 0.3–0.5 A/contact and 30–50 V (R07). 6 × 0.5 A = 3 A total, so **do not put raw 24 V plus surges on DF40 (30 V rating)** |
| GND | 8 | Interleaved between the fast signals |
| UART (HOST_TX, BUS_RX) | 2 | Multi-drop |
| CAN-FD (TXD/RXD logic level, or CANH/CANL) | 2 | Optional transport; can be left unpopulated |
| SPI (SCK, MOSI, MISO) | 3 | Shared |
| SPI CS, rotated | 5 | One per position |
| I2C / I3C (SDA, SCL) | 2 | Discovery, ID EEPROM |
| IRQ_n (open-drain) | 1 | Shared |
| TOKEN (in → out) | 1 | Auto-address chain |
| PWR_EN / RESET, rotated | 5 | Hardware power-cycle of each module |
| SYNC / PPS | 1 | Time sync (e.g. 4G/GNSS PPS) |
| Spare / keying / bus-version ID | 4 | Reserve |
| **Total** | **40** | |

If a fieldbus card is used (rather than the baseboard hosting CAN-FD + 2x RS-485 directly), it is simply another bus module. Hosting the fieldbus on the baseboard costs the H533 one FDCAN and two UARTs, all of which are available [S2].

## 5. Secure element / authenticator

### 5.1 Options

| Part | Certification | Interface / package | Provisioning service | Zephyr / driver | Price @1k | Status |
|---|---|---|---|---|---|---|
| **NXP SE050E** (SE050 family) | **CC EAL6+ (to OS level)**; SE050F adds FIPS 140-2 L3 [S38] | I2C up to 3.4 Mbit/s, HX2QFN20 3×3 mm, -40…105 °C, 50 kB user flash, ECC/RSA-4096/AES [S38] | **EdgeLock 2GO** on SE050E/F (remote credential provisioning and OTA key management) [S38] | NXP Plug & Trust middleware; Zephyr integration UNVERIFIED | UNVERIFIED (not shown on NXP page) | Active [S38] |
| NXP SE051 / SE052F / A5000 / A30 | UNVERIFIED (A5000 believed CC EAL6+) | I2C | EdgeLock 2GO (UNVERIFIED) | Plug & Trust | UNVERIFIED | A5000 product page returned 404 in this run |
| Microchip ATECC608B (Trust&GO / TrustFLEX / TrustCUSTOM) | No CC certificate (UNVERIFIED) | I2C/1-wire, SOIC-8/UDFN | **Trust&GO**: pre-provisioned device certificate; manifest for cloud onboarding (UNVERIFIED) | cryptoauthlib; Zephyr has an ATECC driver (UNVERIFIED) | ~USD 0.7–1.0 (UNVERIFIED) | Product page HTTP 403 |
| Microchip ECC204 / TA100 | ECC204: UNVERIFIED; TA100: CC (UNVERIFIED level) | I2C / SPI | Trust&GO-style (UNVERIFIED) | cryptoauthlib | UNVERIFIED | Product page HTTP 403 |
| ST STSAFE-A110 / A120 | CC EAL5+ (UNVERIFIED) | I2C, SO8N/UFDFPN8 | Pre-personalised with a device certificate (UNVERIFIED) | STSAFE-A middleware; X-CUBE-SAFEA1 | UNVERIFIED | st.com unreachable in this run |
| ST STSAFE-TPM (TPM 2.0) | CC EAL4+ / FIPS (UNVERIFIED) | SPI/I2C | TPM EK certificate | Linux-oriented | UNVERIFIED | — |
| Infineon OPTIGA Trust M (SLS32AIA) | CC EAL6+ hardware (UNVERIFIED) | I2C, USON-10 | Pre-provisioned X.509 certificate (UNVERIFIED) | optiga-trust-m host library | UNVERIFIED | Product page fetched but contained only navigation |

### 5.2 Is a discrete SE still needed when the MCU has PSA L3?

- PSA Certified Level 3 (H533 [S4]) is evaluated against software and physical attacks on the RoT. It is not a smart-card-grade Common Criteria EAL6+ certificate like the SE050 [S38]. Long-term device identity keys therefore sit better in the SE.
- **CRA / EN 18031:** both require protected storage of security parameters and secure updates. Neither mandates a discrete SE (the exact clauses are UNVERIFIED in this run; see R01). A PSA-L3 MCU alone can meet this "state of the art" if keys are injected securely.
- **IEC 62443-4-2:** hardware-backed key protection becomes expected at SL3/SL4 (hardware security requirement enhancements). An SE gives the easiest argument (clause numbers UNVERIFIED; see R01).
- **The decisive argument is manufacturing.** Without an SE, unique keys and certificates must be generated or injected at the CM with a secured flow, for example ST Secure Firmware Install with an HSM or NXP's equivalent (process details UNVERIFIED). That adds HSM logistics and trust in the CM. A **pre-provisioned SE** (EdgeLock 2GO, Trust&GO, STSAFE pre-personalised) arrives with its identity already inside. The CM only places it and programs firmware, and the identity manifest comes from the SE vendor for cloud registration.
- **Recommendation:** STM32H533 (secure boot, TF-M, firmware-encryption keys) + **SE050E with EdgeLock 2GO** if the CC EAL6+ story matters for EU/62443 tenders. Otherwise use **ATECC608B Trust&GO** or **STSAFE-A110** as the cheapest pre-provisioned identity (prices UNVERIFIED; get quotes). If the STM32C5A3 lowest-cost MCU is chosen, the SE becomes **mandatory** because the C5 has no TrustZone [S13].

## 6. Shared configurable IO front end

### 6.1 Sourced device facts

| Part | Function | Key facts | Source |
|---|---|---|---|
| TI ISO1211 / **ISO1212** | Isolated DI receiver (1 / 2 ch) | IEC 61131-2 Type 1/2/3; current limit 2.2–2.47 mA (Type 3), adjustable up to 6.5 mA; ±60 V input with reverse-polarity protection; no field-side supply needed; 4 Mbps; UL 1577 2500 Vrms; ISO1212 in SSOP-16; Active | [S39] |
| TI **TPS272C45** | Dual 24 V high-side switch | 45 mΩ; 6–36 V; current limit fixed 5.8 A or adjustable 0.7–4 A (±25 %); output clamp for inductive loads; thermal shutdown; load-current sense; open-load detection; QFN-24 5×4 mm; UL 2367; Active | [S40] |
| TI TPS4H160-Q1 | Quad 160 mΩ high-side switch | 3.4–40 V, adjustable current limit, automotive (AEC-Q100). Cheaper per channel, but a 40 V rating on a 24 V bus leaves little surge margin, so needs a TVS | [S41] |
| TI **TPS3430** | Window watchdog | Standalone window WDT; ±2.5 % timing; programmable window and reset delay; 1.6–6.5 V; 10 µA; open-drain WDO; VSON-10; disable via SET pins; Active | [S42] |
| TI **ADS1115** | 16-bit ADC | 4 single-ended / 2 differential channels; PGA ±0.256 to ±6.144 V; 8–860 SPS; internal reference; I2C with 4 addresses; Active; ADS1015 is the 12-bit version | [S43] |
| TI ISO6741 | Quad reinforced digital isolator | 5 kVrms; 50 Mbps; ±8 kV IEC 61000-4-2 across the barrier; ±150 kV/µs CMTI | [S44] |
| ADI AD74412R/AD74413R/AD74115H, MAX22000, MAX22190/22199, MAX14906, ST CLT03-2Q3/CLT01-38SQ7, IPS1025H/IPS2050H/IPS160H/VNI/ISO808, Infineon ITS/ISO1H, MCP346x, SGM58031, Chipanalog/Novosense isolators | — | **Not verified in this run** (analog.com and st.com were unreachable from the tooling; the search budget was exhausted) | — |

### 6.2 Circuit choices

- **Universal input (0–10 V / 0/4–20 mA / dry contact / NTC / PT1000), discrete:**
  - Per channel: a TVS and series PTC for ±36 V miswiring, then a MOSFET-switched 100–250 Ω precision shunt for current mode, a high-impedance divider for 0–10 V, and a switched pull-up for dry contact or NTC. The signal goes into the MCU's 12-bit ADC.
  - PT1000 and precision 4–20 mA: route through a shared ADS1115 [S43] with ratiometric excitation.
  - A 24 V loop supply with a current limit (PTC or eFuse) powers 2-wire transmitters.
  - The universal-IO ICs (AD74413R class) give software-defined IO with diagnostics, but are widely reported to cost ~USD 10+ per quad (UNVERIFIED). That is roughly 3× the discrete cost per channel, so keep them for a premium IO module.
- **Digital inputs:**
  - Isolated: ISO1212 handles 2 channels per IC, needs no field supply and limits current itself [S39].
  - Lowest cost: an optocoupler plus a resistor/zener current-limit network meeting Type 1/3 (UNVERIFIED price), or an ST CLT03-2Q3 (UNVERIFIED).
- **Digital outputs:**
  - 2x TPS272C45 gives 4 channels at up to 2 A with adjustable limit and diagnostics [S40].
  - A relay option (dry contact, 5 A) costs ~INR 40–60 per channel plus a driver (UNVERIFIED).
  - The MAX14906 class (configurable DI/DO) is UNVERIFIED.
- **Fail-safe:**
  - The TPS3430 WDO [S42] and an MCU "OUT_ARM" GPIO feed an AND gate (or a load switch on the high-side-switch supply). A hung MCU, or a watchdog fed outside its window, therefore removes the enable from all DOs, and the outputs drop to OFF.
  - Re-arming needs a deliberate software sequence.
  - The default-low output-enable is held by pull-downs during reset.
- **Isolation:** isolate the field-IO domain as a group (ISO6741 class [S44] for SPI/GPIO, plus an isolated DC-DC) rather than per channel. Chipanalog/Novosense equivalents are expected to be cheaper (UNVERIFIED).

### 6.3 Recommended IO mix and budget (baseboard)

**All IO prices below are UNVERIFIED engineering estimates (no 1k distributor quote could be fetched). Get LCSC / DigiKey India quotes before committing.**

| Block | Implementation | Est. INR per channel | Channels | Est. INR total |
|---|---|---|---|---|
| Universal AI | Discrete front end (TVS, PTC, shunt + MOSFET, divider, RC) into the MCU ADC; shared ADS1115 for PT1000/precision | 60–90 + ADS1115 share (~INR 60–75/ch) | 4 | 480–660 |
| DI (isolated, IEC 61131-2 Type 3) | 2x ISO1212 + input resistors + TVS | 90–120 | 4 | 360–480 |
| DI (alternative, non-isolated low-cost) | Resistor/zener current limiter + optocoupler | 15–30 | 4 | 60–120 |
| DO 24 V high-side, 0.5–2 A | 2x TPS272C45 + TVS + sense resistor | 100–150 | 4 | 400–600 |
| Fail-safe | TPS3430 + AND gate | — | 1 | 50–80 |
| 24 V loop supply limit | PTC/eFuse | — | 1 | 20–60 |
| **Total (isolated DI variant)** | | **≈ 110–150 per channel** | 12 | **≈ INR 1,300–1,900** |
| **Total (low-cost DI variant)** | | **≈ 85–125 per channel** | 12 | **≈ INR 1,000–1,500** |

Protection targets (from R01, UNVERIFIED levels):
- IEC 61000-4-2: ±8 kV contact / ±15 kV air at the terminals.
- IEC 61000-4-4: ±2 kV on signal lines.
- IEC 61000-4-5: ±1 kV CM on lines longer than 30 m, ±2 kV design margin.

How the design reaches them: one TVS per field line (SMBJ33A class, with a working voltage above 30 V so ±30 V miswiring does not conduct), series PTC or resistors, the ISO1212's own ±60 V tolerance [S39], and the TPS272C45 output clamp [S40]. ESD to the isolated domain is covered by ISO6741's ±8 kV rating across the barrier [S44].

## 7. Storage and timekeeping

**Not researched with sources in this run (search budget exhausted). The selections below are UNVERIFIED recommendations to confirm.**

| Need | Recommendation | Notes |
|---|---|---|
| A/B images, logs, config | 128 Mbit (16 MB) SPI NOR, quad-SPI, SOIC-8 or WSON-8 (Winbond W25Q128JV / GigaDevice GD25Q128 / Macronix MX25L128 class) | Typically 100k program/erase cycles and 20-year retention; widely stocked at LCSC; ~USD 0.6–1.0 (UNVERIFIED) |
| Long logs / store-and-forward | 1 Gbit SPI NAND (W25N01GV class) only if more than 16 MB is needed | Needs bad-block management (UNVERIFIED) |
| Energy and pulse counters | 16–64 kbit I2C FRAM (Fujitsu MB85RC / Infineon FM24CL class) | ~10^12+ write endurance, no wear levelling (UNVERIFIED) |
| microSD | Avoid on the baseboard: hard to secure, wears unpredictably, vibration contact issues | Optional on a service/logging module |
| RTC | MCU RTC on VBAT with tamper inputs (STM32H5 has RTC + TAMP; UNVERIFIED in this run) | Add an external RV-3028-C7 class RTC (sub-µA, factory calibrated; UNVERIFIED) only if months of holdover on a small cell are required. PCF85263A / PCF2131 if a timestamp/tamper RTC independent of the MCU is wanted (UNVERIFIED) |
| Module identity | 24LC04B-class I2C EEPROM on each module | INR 31.96 @25 at DigiKey India [S45] |

## 8. Risks and open decisions

1. **Supply / lead time:** STM32H533RET6 and H523RET6 show 0 stock at DigiKey India with a 52-week standard lead time [S23][S24]. STM32C5A3 is also 0 stock / 52 weeks [S26]. Get ST distributor (India) commitments, and qualify the NXP MCX N236 alternate [S27] early. Avoid the obsolete MCXN236VNLT [S28].
2. **H533 flash (512 KB)** may be tight for TF-M + MCUboot + A/B. Decide between H573 (2 MB) and an external secondary slot after a firmware-size estimate.
3. **SE choice** (SE050E vs ATECC608B vs STSAFE-A110): prices, CC levels and pre-provisioning terms are **UNVERIFIED**. Request quotes and service terms (minimum order quantity, certificate-chain ownership, manifest delivery).
4. **CAN-FD as the stack bus** is blocked by ESP32-C6 (classic CAN only) and nRF54L (no CAN). Keep UART as mandatory and CAN-FD optional.
5. **Bus power on fine-pitch connectors** (0.3–0.5 A, 30–50 V ratings, R07): the 4G card's peak current needs a dedicated power path or a coarser connector. Coordinate with R06/R07.
6. **IO costs are estimates.** Universal-IO ICs (AD74413R) and MAX22190/MAX14906/ST IPS parts were not verified.
7. **Fieldbus host decision:** the baseboard H533 can host 1x CAN-FD + 2x RS-485 directly (interface count is sufficient [S2]). The alternative is a separate fieldbus card. Decide based on whether the fieldbus isolation and terminals fit the baseboard enclosure.
8. **STM32C5 lowest-cost path:** no TrustZone [S13], and the PSA/SESIP status is only a "target" (UNVERIFIED) [S12]. This weakens the CRA/62443 argument unless the SE carries it.

## 9. Sources

All accessed 2026-11-14 unless noted.

- [S1] USD/INR mid-market 93.93 (2026-11-08) — https://currencybeacon.com/rates/USD/INR
- [S2] ST STM32H533CE product page (JP) — https://www.st.com/ja/microcontrollers-microprocessors/stm32h533ce.html ; datasheet DS14539 https://st.com/resource/en/datasheet/stm32h533he.pdf
- [S3] Avnet Silica STM32H523/H533 NPI — https://my.avnet.com/silica/products/new-products/npi/2024/stmicroelectronics-stm32h523-stm32h533/
- [S4] PSA Certified — STM32H533xx with Security Services certificates — https://products.psacertified.org/products/stm32h533xx-with-security-services/certificates
- [S5] ST Community (H533 certification derived from H573) — https://community.st.com/stm32-mcus-security-36/stm32h533-product-state-vulnerability-to-voltage-glitching-146228
- [S6] Future Electronics STM32H523RCT6 — https://futureelectronics.com/p/semiconductors--microcontrollers--32-bit/stm32h523rct6-stmicroelectronics-4186130
- [S7] DigiKey IE STM32H523RCT6 — https://www.digikey.ie/en/products/detail/stmicroelectronics/STM32H523RCT6/22519695
- [S8] ST STM32U545 product pages — https://www.st.com/en/microcontrollers-microprocessors/stm32u545ve.html , https://www.st.com/ja/microcontrollers-microprocessors/stm32u545ce.html
- [S9] ST STM32U375/385 — https://www.st.com/en/microcontrollers-microprocessors/stm32u375-385.html , https://www.st.com/en/microcontrollers-microprocessors/stm32u385rg.html
- [S10] ST eStore STM32U385CGT6 — https://estore.st.com/en/stm32u385cgt6-cpn.html
- [S11] ST STM32C5 series page — https://www.st.com/en/microcontrollers-microprocessors/stm32c5-series.html ; datasheet DS15137 https://www.st.com/resource/en/datasheet/stm32c5a3zg.pdf
- [S12] CNX Software, STM32C5 launch (2026-03-09) — https://www.cnx-software.com/2026/03/09/stmicro-stm32c5-entry-level-144-mhz-cortex-m33-mcu-features-up-to-1mb-flash-256kb-sram-ethernet-can-bus/
- [S13] Arm Keil device DB STM32C5A3KGU3TR — https://www.keil.arm.com/devices/stmicroelectronics-stm32c5a3kgu3tr/processors/
- [S14] Zephyr boards nucleo_c5a3zg / xiao_stm32c5 — https://docs.zephyrproject.org/latest/boards/st/nucleo_c5a3zg/doc/index.html , https://docs.zephyrproject.org/latest/boards/seeed/xiao_stm32c5/doc/index.html
- [S15] CNX Software STM32G5 (2026-11-10) — https://www.cnx-software.com/2026/11/10/280-mhz-stmicro-stm32g5-cortex-m33-mixed-signal-mcu-targets-digital-power-and-motor-control-applications/ ; https://www.st.com/en/microcontrollers-microprocessors/stm32g534hc.html
- [S16] NXP MCX N23x — https://nxp.com/products/MCX-N23X , https://nxp.com/part/MCXN236VPBT
- [S17] element14 SG MCXN236VNLT — https://sg.element14.com/nxp/mcxn236vnlt/mcu-1024kb-150mhz-hlqfp-100/dp/4445654
- [S18] MCXN947 datasheet summary — https://datasheetspdf.com/amp-datasheet/1530520/MCXN947.html
- [S19] NXP MCX security overview — https://www.nxp.com/products/processors-and-microcontrollers/arm-microcontrollers/general-purpose-mcus/mcx-arm-cortex-m:MCX-MCUS
- [S20] NXP newsroom LPC55S16 Level 2 — https://www.nxp.com/company/about-nxp/newsroom/NW-LPC55S16-MCU-AWARDED
- [S21] PSA Certified LPC55S16 — https://products.psacertified.org/products/lpc55s16
- [S22] NXP LPC551x fact sheet — https://Community.freescale.com/docs/en/fact-sheet/LPC551X-FS.pdf
- [S23] DigiKey IN STM32H523RET6 — https://www.digikey.in/en/products/detail/stmicroelectronics/STM32H523RET6/22519674
- [S24] DigiKey IN STM32H533RET6 — https://www.digikey.in/en/products/detail/stmicroelectronics/STM32H533RET6/22519671
- [S25] DigiKey IN STM32U545RET6Q — https://www.digikey.in/en/products/detail/stmicroelectronics/STM32U545RET6Q/20412792
- [S26] DigiKey IN STM32C5A3RGT6 — https://www.digikey.in/en/products/detail/stmicroelectronics/STM32C5A3RGT6/29270420
- [S27] DigiKey IN MCXN236VKLT — https://www.digikey.in/en/products/detail/nxp-usa-inc/MCXN236VKLT/26220967
- [S28] DigiKey TW MCXN236VNLT (obsolete) — https://www.digikey.tw/en/products/detail/nxp-usa-inc/MCXN236VNLT/22539829
- [S29] DigiKey IN MCXN947VNLT — https://www.digikey.in/en/products/detail/nxp-usa-inc/MCXN947VNLT/22039736
- [S30] DigiKey IN LPC55S16JBD64E — https://www.digikey.in/en/products/detail/nxp-usa-inc/LPC55S16JBD64E/11675311
- [S31] DigiKey IN NRF54L15-QFAA-R — https://www.digikey.in/en/products/detail/nordic-semiconductor-asa/NRF54L15-QFAA-R/24773448
- [S32] LCSC STM32H533RET6 C26082149 — https://www.lcsc.com/product-detail/C26082149.html
- [S33] TME STM32C5A3VGT6 — https://www.tme.eu/en/details/stm32c5a3vgt6/st-microcontrollers/stmicroelectronics/
- [S34] DigiKey US STM32C562RET6 — https://www.digikey.com/en/products/detail/stmicroelectronics/STM32C562RET6/28948239
- [S35] TF-M platform list — https://trustedfirmware-m.readthedocs.io/en/latest/platform/index.html
- [S36] Zephyr TF-M requirements — https://docs.zephyrproject.org/latest/services/tfm/requirements.html
- [S37] Nordic nRF54L15 product page — https://www.nordicsemi.com/Products/nRF54L15
- [S38] NXP SE050 product page — https://www.nxp.com/products/SE050
- [S39] TI ISO1211/ISO1212 datasheet SLLSEY7G (Feb 2025) — https://www.ti.com/lit/ds/symlink/iso1212.pdf ; product page https://www.ti.com/product/ISO1212
- [S40] TI TPS272C45 datasheet SLVSF24C — https://www.ti.com/lit/ds/symlink/tps272c45.pdf ; https://www.ti.com/product/TPS272C45
- [S41] TI TPS4H160-Q1 datasheet SLVSCV8E — https://www.ti.com/lit/ds/symlink/tps4h160-q1.pdf
- [S42] TI TPS3430 window watchdog — https://www.ti.com/lit/ds/symlink/tps3430.pdf ; https://www.ti.com/product/TPS3430
- [S43] TI ADS1115 datasheet SBAS444E — https://www.ti.com/lit/ds/symlink/ads1115.pdf ; https://www.ti.com/product/ADS1115
- [S44] TI ISO674x datasheet SLLSFJ6G — https://www.ti.com/lit/ds/symlink/iso6741.pdf
- [S45] DigiKey IN 24LC04B-I/SN — https://www.digikey.in/en/products/detail/microchip-technology/24LC04B-I-SN/218078
- Internal cross-references: R01 (EMC levels, standards), R03 (ESP32-C6 TWAI / ESP32-C5 CAN-FD, its sources S52/S57), R06 (power), R07 (connector ratings: DF40 0.3 A / 30 V; FX18 0.5 A).
