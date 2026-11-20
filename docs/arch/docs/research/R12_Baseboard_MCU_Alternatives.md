# R12 — Baseboard MCU: alternatives to the STM32H573 (multi-vendor)

Status: COMPLETE WITH GAPS (2026-11-14). Every price, stock figure, spec and certificate claim carries a source [Sn] (§8). Anything without a fetched primary source is marked UNVERIFIED.

Builds on R11 (STM32H573 recommendation, MCX N947 as the NXP option, PHY/RJ45 choice), R08 (requirements, SE050) and R09 §7 (RTOS support matrix). This report does not repeat that work. Prices are DigiKey India INR list prices fetched 2026-11-14 unless stated. These are upper bounds; franchised 1k quotes are normally lower. Other currencies are converted at 1 USD = INR 93.9 (as R05/R11). Finished cost = BOM x 1.4 (R11 convention).

## 1. Executive summary and ranked recommendation

**The problem is real.** The STM32H573VIT6 (LQFP100, the R11 pick) is INR 633.75 @500 at DigiKey India with 0 stock, a 52-week lead time and 1 piece due 12-May-2027 [S1]. ST's own eStore lists every STM32H573VI order code as Out of Stock (USD 6.23 @10k) and warns that "shipments may be delayed" [S2]. An ST community thread from 8-Oct-2026 reports no STM32H563VIT6 stock at DigiKey, Mouser or element14 either, and ST answered only "contact sales/FAE" [S4]. One LCSC/TME/element14 snapshot showed 0 stock or incoming-only [S3]. The H5 supply gap is therefore not just a DigiKey artefact.

**Ranked shortlist** (reliability and availability first, then cost):

| Rank | Part (package) | Why | DigiKey India INR | Stock / LT (2026-11-14) |
|---|---|---|---|---|
| **1** | **Renesas RA8M1 — R7FA8M1AHECFP#BA0** (LQFP100) | The only alternative with **the same certificate class as the H573: PSA Certified Level 3 RoT Component + SESIP3**, plus FIPS 140-3 L2 [S9][S10]. 2 MB / 1 MB SRAM, Ethernet RMII, 2x CAN FD, TrustZone, RSIP-E51A [S12]. **In stock in India now.** Zephyr has upstream Ethernet + CAN FD on the EK-RA8M1 [S23]. Renesas longevity: up to 15 years [S20]. | **861.97 @500** (922.80 @100) [S15] | **720 in stock**, 18 wk [S15] |
| **2** | **NXP MCX N947 — MCXN947VKLT** (HLQFP100) | The most mature Zephyr port of the non-ST options (`frdm_mcxn947`: Ethernet, CAN, flash, TF-M `/ns`) [S26][R09]. 2 MB / 512 KB, ENET-QoS RMII, 2x CAN FD, EdgeLock. **No PSA/SESIP certificate found.** | 843.72 @500 [R11 S15] | DigiKey IN 0 / 13 wk; Mouser India 189 (snapshot) [S36] |
| **3** | **ST STM32H573VIT6** (LQFP100) — keep as co-primary only if an ST franchise quote commits ≤ 20 weeks | It is still technically the best fit: PSA L3/SESIP3, the most mature Zephyr + TF-M + ThreadX support, and the cheapest certified part. It is ranked 3rd **only because it cannot be bought today** [S1][S2][S4]. | 633.75 @500 [S1] | 0 everywhere checked; 52 wk |
| 4 | **Renesas RA6M5 — R7FA6M5BH3CFP#BA0 / #AA0** (LQFP100) — cost-down | 2 MB / 512 KB, Ethernet RMII, 2x CAN FD, 10 SCI, 20 ADC ch, TrustZone + SCE9, -40…105 °C [S14]. Only **PSA L1** [S9]. In Zephyr the Ethernet driver is enabled, **but the CAN FD node is missing from the RA6M5 SoC devicetree** [S23]. | **476.03 @720** (#BA0); 639.29 @540 (#AA0) [S18][S19] | #AA0: **342 in stock**; 18 wk |
| 5 | Renesas RA8E1 — R7FA8E1AFDCFP#BA0 (LQFP100) | 1 MB / 544 KB, Ethernet, 2x CAN FD, PSA L1 + **CRA extension** [S9][S11][S13]. Needs external flash for the second update slot. Tj max is only 105 °C. | 691.34 @720 [S17] | 0 (#UA0: 18 pcs) / 18 wk |
| 6 | Microchip PIC32CK SG01 — PIC32CK2051SG01100-I/4SB (TQFP100-EP) | The cheapest and best-stocked part: 2 MB / 512 KB, Ethernet, 2x CAN FD, 8 SERCOM, HSM + TrustZone [S28][S29]. **Fails the Zephyr requirement**: upstream has UART/GPIO/watchdog only, with no Ethernet, CAN or ADC drivers [S25]. No certificate found [S31]. | 332.89 (1 pc); 474.56 @1k (E-grade reel) [S29] | **170 in stock**, 8 wk |

**Recommendation:**
1. **Design the first build around the Renesas RA8M1 (R7FA8M1AHECFP) as the primary baseboard MCU.** It keeps the security story R08/R11 relied on (PSA L3 + SESIP3, the same level as the H573), it is in stock in India today with an 18-week factory lead time, it is a newer generation (Cortex-M85; launch year UNVERIFIED in this run), and the RAM headroom (1 MB) is larger than the H573's. It costs about **+INR 228 BOM / +INR 319 finished** over the H573VIT6 list price.
2. **Keep the NXP MCX N947VKLT as the qualified second source** in the architecture. It has the strongest Zephyr support after ST and a 13-week lead time, at about the same price as the RA8M1. Use it if the RA8M1 Zephyr bring-up (§4.1) slips.
3. **Re-quote the STM32H573VIT6 from an ST franchise (Arrow / Avnet / WPG India).** If ST commits ≤ 20 weeks, the H573 is still the cheapest certified option. Do not wait for it.
4. **Cost-down path: RA6M5** (INR 476 @720). The same Renesas toolchain and Ethernet driver apply, but it has only PSA L1 and needs a small Zephyr CAN FD devicetree addition. The SE050 still holds the device keys (R08), so a PSA L1 MCU is acceptable if cost presses.

**One-line verdict per vendor:**
- **ST:** the right chip, but unavailable. The H5 family is 0 stock with 52-week lead times; the H7 (H723/H733) has no TrustZone and the same supply problem; the H543/H553/H5E5/H5F5 are still in evaluation or development.
- **Renesas:** the best alternative today. RA8M1 is certified and in stock; RA6M5 is the cost-down.
- **NXP:** MCX N947 is a solid Zephyr second source (no certificate). i.MX RT is BGA. S32K3 is automotive-priced (INR 1,388) with a 39-week lead time.
- **Microchip:** PIC32CK SG has excellent hardware, price and stock, but upstream Zephyr is not ready. SAM E54 has only 256 KB RAM and no TrustZone.
- **TI:** no fit. The Sitara AM26x/AM24x MCUs are BGA only, and the TM4C129 is old with no CAN FD.
- **Nordic:** no Nordic part has an Ethernet MAC; Zephyr has no Nordic Ethernet binding [S22][S40].
- **Infineon:** XMC4800 has classic CAN only (no FD, UNVERIFIED). XMC7000/TRAVEO T2G have Ethernet + CAN FD, but Zephyr has no Ethernet driver for them.
- **GigaDevice and other Chinese parts:** GD32H759 has strong hardware (Ethernet, 3x CAN FD) but no Zephyr Ethernet/CAN support and no security certificate. Not consistent with reliability-first.

## 2. Comparison table (all candidates against the required features)

Legend: Y = meets, P = partial, N = fails. Zephyr status = upstream main on 2026-11-14 [S22][S23][S25][S26].

| Part (order code, package) | Core | Flash / RAM | ETH RMII in QFP/QFN | CAN-FD | UART / SPI / I2C / USB FS | ADC ch (this pkg) | Security (TZ / crypto / TRNG / cert) | Temp | Zephyr (SoC, ETH, CAN-FD, flash, MCUboot) | ThreadX | INR (DigiKey IN) | Stock / LT | Longevity |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Renesas RA8M1** R7FA8M1AHECFP#BA0 (LQFP100) | M85 480 MHz | 2 MB / 1 MB (896 KB + 128 KB TCM) Y | Y (RMII pins 40–48) [S12] | 2 Y | 6 SCI / 2 SPI / 2 IIC / FS Y | 11 (6+5) Y | TZ, RSIP-E51A, TRNG, secure boot/debug; **PSA L3 RoT + SESIP3 + FIPS 140-3 L2** [S9][S10] | Tj -40…125 °C [S12] | P: SoC in tree (BGA224 dtsi only; LQFP100 dtsi to add), ETH Y, CAN-FD Y, flash Y, MCUboot generic (no slot partitions upstream) [S23][S24] | P: Renesas ThreadX plan "to be determined" [S21] | **861.97 @500** | **720** / 18 wk | PLP up to 15 yr [S20] |
| **NXP MCX N947** MCXN947VKLT (HLQFP100) | 2x M33 150 MHz | 2 MB / 512 KB Y | Y (ENET-QoS RMII) [R11] | 2 Y | 10 LP_FLEXCOMM / FS Y | UNVERIFIED for HLQFP100 | TZ, EdgeLock Secure Enclave (core), PUF, TRNG; **no PSA/SESIP cert found** [R11 S18] | -40…105 °C (VKLT) [R11] | **Y**: frdm_mcxn947 ETH, CAN, flash, TF-M `/ns`, MCUboot [S26][R09] | UNVERIFIED | 843.72 @500 [R11] | 0 / 13 wk (Mouser IN 189, snapshot) [S36] | NXP longevity ≥ 10 yr [R11] |
| **ST STM32H573VIT6** (LQFP100) — baseline | M33 250 MHz | 2 MB / 640 KB Y | Y [R11] | 2 Y | 11 + LP / FS Y | 16 Y | TZ, AES/PKA/HASH, TRNG; **PSA L3 + SESIP3** [R11] | -40…85 °C [S1] | **Y** (best): ETH, FDCAN, flash, MCUboot, TF-M `/ns` [S26][R09] | **Y** (STM32CubeH5) [R09] | 633.75 @500 [S1] | **0** / 52 wk; eStore OOS [S1][S2] | 10 yr from 2026-01-01 (H563 pages) [S5] |
| **Renesas RA6M5** R7FA6M5BH3CFP#BA0 (LQFP100) | M33 200 MHz | 2 MB / 512 KB Y | Y (RMII only) [S14] | 2 Y ("B" code = FD) | **10 SCI** / 2 SPI / 3 IIC / FS Y | **20** (11+9) Y | TZ, SCE9, TRNG; **PSA L1 only** [S9] | Ta -40…105 °C [S14] | P: ETH Y, **CAN-FD node missing** in SoC dtsi, flash Y, MCUboot generic [S23] | P [S21] | **476.03 @720** / 639.29 @540 (#AA0) | #AA0 **342** / 18 wk | PLP up to 15 yr [S20] |
| **Renesas RA8E1** R7FA8E1AFDCFP#BA0 (LQFP100) | M85 360 MHz | **1 MB** / 544 KB P (external flash for slot 2) | Y [S13] | 2 Y | 6 SCI / 2 SPI / 2 IIC / FS Y | 11 (6+5) Y | TZ, RSIP-E51A, TRNG; **PSA L1 + CRA extension** [S9][S11] | **Tj -40…105 °C** P [S13] | P: SoC LQFP100 dtsi in tree with ETH + CAN-FD nodes; dev board (FPB) has no PHY [S23] | P [S21] | 691.34 @720 [S17] | 0 (#UA0 18) / 18 wk | PLP [S20] |
| **Microchip PIC32CK SG01** PIC32CK2051SG01100-I/4SB (TQFP100-EP) | M33 120 MHz | 2 MB / 512 KB Y | Y (MII/RMII) [S27] | 2 Y [S28] | 8 SERCOM / HS+FS Y | 12 SE + 3 diff Y [S28] | TZ + isolated HSM, secure boot; **no cert found** [S31] | -40…85 °C (I) [S29] | **N**: board has UART/GPIO/WDT only; no GMAC/CAN/ADC nodes [S25] | UNVERIFIED | **332.89 (1 pc)**; 474.56 @1k E-grade reel [S29] | **170** / 8 wk | Client-driven obsolescence [S32] |
| ST STM32H563VIT6 (LQFP100) | M33 250 MHz | 2 MB / 640 KB Y | Y | 2 Y | Y | 16 Y | TZ, no crypto accelerator / no PSA L3 [R11] | -40…85 °C | Y | Y | 608.05 @540 [R11 S10] | 0 / 52 wk | 10 yr [S5] |
| Microchip SAM E54 ATSAME54N20A-AU (TQFP100) | M4F 120 MHz | 1 MB / **256 KB N** | Y | 2 Y | Y | Y | **No TrustZone**; AES/TRNG/PUKCC (UNVERIFIED) | -40…85 °C [S33] | **Y**: sam_e54_xpro ETH, MCUboot, flash [S26] | UNVERIFIED | 664.82 @100 [S33] | 41 / 39 wk | [S32] |
| ST STM32H723VGT6 / H733VGT6 (LQFP100) | M7 550 MHz | 1 MB / 564 KB (UNVERIFIED) | Y | 3 (UNVERIFIED) | Y | Y | **No TrustZone**; H733 has crypto | -40…85 °C [S7] | Y: nucleo_h723zg ETH + CAN [S26] | Y | 875.06 / 892.42 @540 [S7][S8] | 0 / 52 wk | ST 10 yr (UNVERIFIED per part) |
| NXP S32K344 S32K344EHT1MPBST (172-QFP 16x16) | M7 160 MHz (lock-step) | 4 MB / 512 KB (UNVERIFIED) | Y (UNVERIFIED pin-out) | 6 FlexCAN-FD (UNVERIFIED) | Y | Y | HSE-B, **no TrustZone**, automotive ISO 21434 | -40…125 °C (UNVERIFIED) | Y: mr_canhubk3 ETH, CAN, flash [S26] | N | **1,387.79 @420** [S34] | 0 / **39 wk** | NXP automotive 15 yr (UNVERIFIED) |
| ST STM32H543/H553, H5E5/H5F5 | M33 250 MHz | 1 MB / 304 KB; 4 MB / 1.5 MB | Y | 2 | Y | Y | H553/H5F5 crypto; PSA L3 *targeted* | — | not yet | Y (Cube) | **not at distribution** | "Evaluation" / "in development" [S6] | new 10-yr window |

## 3. Cost delta versus the R11 baseline (STM32H573VIT6, INR 633.75 @500)

| Option | MCU INR | Δ BOM | Δ finished (x1.4) | Comment |
|---|---|---|---|---|
| RA8M1 R7FA8M1AHECFP#BA0 | 861.97 @500 [S15] (Future USD 9.90 @720 ≈ INR 930, snapshot [S16]) | **+228** | **+319** | Certified like-for-like, in stock |
| MCXN947VKLT | 843.72 @500 [R11] | +210 | +294 | No certificate |
| RA8E1 R7FA8E1AFDCFP#BA0 | 691.34 @720 [S17] | +58 | +81 | Plus external NOR (~INR 40–80, est. UNVERIFIED) for slot 2 |
| RA6M5 R7FA6M5BH3CFP#BA0 | 476.03 @720 [S19] | **−158** | **−221** | PSA L1; Zephyr CAN FD devicetree to add |
| PIC32CK2051SG01100 | 332.89–474.56 [S29] | −159 to −301 | −222 to −421 | Zephyr not ready |

## 4. Per-candidate notes

### 4.1 Renesas RA8M1 (rank 1)
- **Hardware (datasheet R01DS0417EJ0140 Rev 1.40 [S12]):** Cortex-M85 + Helium, 480 MHz; 2 MB dual-bank code flash with background/SWAP operation (useful for A/B update); 1 MB SRAM (896 KB + 128 KB TCM). LQFP100 (R7FA8M1AxECFP): SCI x6, IIC x2, SPI x2, CANFD x2, USBFS (USBHS only on 176/224-pin packages), ETHERC with RMII group A on pins 40–48, ADC12 unit 0: 6 + unit 1: 5 channels, 70 I/O. Security: RSIP-E51A, secure debug, secure boot from immutable ROM, TrustZone, device lifecycle management. Tj -40…125 °C.
- **Certificates:** PSA Certified Level 3 RoT Component, "RA8M1 Version A", cert 0632793520122-10540, 17-Feb-2025, Applus+ [S10]. Renesas also lists SESIP3 and FIPS 140-3 Level 2 (#5556) and NIST ESV (#E288) for the RA8M1 [S9]. This is the strongest certificate set of all candidates, including the H573.
- **Zephyr:** the `ek_ra8m1` board enables `&eth` (RMII pinctrl, MDIO) and `canfd0`; the shared `ra8x1.dtsi` carries `renesas,ra-ethernet`, 2x `renesas,ra-canfd`, `renesas,ra-rsip-e51a-trng`, ADC12, SPI, I2C and USB FS nodes [S23]. Gaps:
  1. Only the BGA224 SoC variant (`r7fa8m1ahecbd.dtsi`) is in the tree, so our board port must add an LQFP100 package file. This is low effort, because the RA8E1 already has `-100` package files to copy.
  2. No MCUboot slot partitions are defined upstream for ek_ra8m1, though the Zephyr EK-RA8P1 page documents MCUboot via sysbuild [S24].
  3. No TF-M platform for RA was found (UNVERIFIED). Use MCUboot + TrustZone via Renesas FSP, or a non-TF-M Zephyr build with keys in the SE050.
- **ThreadX:** Renesas says its Eclipse ThreadX support strategy is "to be determined" [S21]. Treat ThreadX as unavailable on Renesas, so the RA8M1 is Zephyr-only in practice.
- **Supply:** DigiKey India has 720 in stock (one tray), INR 861.97 @500, 18-week lead time, Active [S15]. The T&R code #HA0 is INR 1,038.47 @1k, 0 stock [S15]. Future Electronics shows 0 stock, 18 weeks, USD 9.90 @720 (snapshot) [S16]. One DigiKey EU snapshot showed 0 stock [S16], so the 720 is one tray and should be bought early if chosen.
- **Pin-budget risk:** 6 SCI covers RS-485, stack-bus UART, console, the 4G/module UART and one spare (≥ 5 UARTs). The 2 dedicated SPI + 2 IIC cover the stack bus and SE050. Only 11 ADC channels remain after RMII, which is enough for 4 AI + housekeeping but tight. If the pin plan fails, move to LQFP144 R7FA8M1AHECFB (ADC 11 + 8 channels, 3 shared; same die) [S12].
- **Longevity:** Renesas PLP up to 15 years, stated per part [S20].

### 4.2 NXP MCX N947VKLT (rank 2)
- Covered in R11 §2.4 (INR 843.72 @500, 13 weeks, HLQFP100, ENET-QoS RMII, 2x CAN FD, EdgeLock, VKLT not VNLT). New in this run:
  - Mouser India listed 189 pieces (INR 1,354.79 @1, falling to INR 917.27 at volume; search snapshot) [S36].
  - Avnet: USD 8.67 @450, 0 stock [S36].
- Zephyr `frdm_mcxn947` lists `can`, `netif:eth`, `flash`, `ptp_clock` as tested features [S26]. TF-M `/ns` target present [R09].
- Weakness: no PSA/SESIP certificate found [R11 S18]. The NXP datasheet copy downloaded is Rev 4 (01/2024); NXP has announced a Rev 8.2 combined MCX N datasheet (Jun 2026), which could not be fetched [S42].

### 4.3 ST STM32H573VIT6 (rank 3, R11 baseline)
- DigiKey India: INR 1,033.85 @1, 682.15 @100, 633.75 @500; 0 stock; 1 due 12-May-2027; 52 weeks [S1].
- ST eStore: all four VI codes (VIT6, VIT6TR, VIT7, VIT3Q) Out of Stock; USD 6.09–6.64 @10k; "shipments may be delayed" [S2].
- An earlier search snapshot showed USD 4.94 @10k "In stock", so ST's eStore price appears to have risen ~26 % (UNVERIFIED trend).
- One DigiKey Japan snapshot showed 1,719 in stock [S3], but the live DigiKey India page shows 0. DigiKey ships from one warehouse, so the JP figure is stale.
- Longevity: ST product pages show a 10-year commitment starting 2026-01-01 for STM32H563 variants (search snippets) [S5].
- **Newer ST options are not buyable yet:**
  - STM32H553VG is at "Evaluation" status [S6].
  - STM32H5E5/H5F5 (4 MB / 1.5 MB, Ethernet; H5F5 adds crypto) have kits since Apr 2026, but the H5E5VJ is "in development" [S6].

### 4.4 Renesas RA6M5 (rank 4, cost-down)
- **Datasheet (Rev 1.50, 13-Mar-2026 [S14]):**
  - Order code R7FA6M5BH3CFP: B = CAN FD feature set (A = classical CAN only, do not order), H = 2 MB, 3 = -40…105 °C, FP = LQFP100.
  - The LQFP100 has 10 SCI, 3 IIC, 2 SPI, 2 CAN FD, USBFS (no USBHS), ETHERC RMII only, ADC12 11 + 9 channels, 75 I/O, and SCE9 + TrustZone.
- **Pricing:** #AA0 (tray) INR 639.29 @540, 342 in stock [S18]. #BA0 (full carton) INR 476.03 @720, not normally stocked [S19]. Both have an 18-week lead time. Same die; only the packing code differs.
- **Certificates:** Renesas lists only PSA Certified Level 1 for the RA6M5 [S9]. Distributor marketing claims "PSA L2 + SESIP1" [S41], but that refers to the RA6M4; treat the RA6M5 as L1.
- **Zephyr:**
  - `ek_ra6m5` enables `&eth` + MDIO [S23].
  - The RA6 SoC dtsi has `renesas,ra-ethernet`, 2x ADC12, 10 SCI UARTs and the SCE9 RNG, but **no `renesas,ra-canfd` node**. The driver exists for RA8, so adding the node is a small upstream change, but it is untested on RA6M5 (UNVERIFIED effort).
- **Generation:** launched in 2021. It is older than the RA8 parts but still active, with the datasheet revised in 2026.

### 4.5 Renesas RA8E1 (rank 5)
- LQFP100 R7FA8E1AFDCFP: 1 MB flash / 544 KB SRAM, 6 SCI, 2 CAN FD, ETHERC (RMII on pin 6 etc.), ADC 6+5, RSIP-E51A [S13].
- The Zephyr SoC files for this exact LQFP100 code are upstream and include the Ethernet + CAN FD nodes [S23].
- PSA L1 with the CRA extension (Applus+, Feb 2025) [S11]. This certificate is aimed specifically at the EU Cyber Resilience Act.
- Downsides:
  - **1 MB flash**, so the second MCUboot slot must go to external QSPI/OSPI NOR (R09).
  - **Tj max 105 °C**, so check that ambient 85 °C at full load is acceptable.
  - Dev board FPB-RA8E1 has no Ethernet PHY.

### 4.6 Microchip PIC32CK SG01 (rank 6, watch)
- **Hardware:** PIC32CK2051SG01100: 8 SERCOM, 2 CAN FD, Ethernet, 12-bit ADC 12 single-ended / 3 differential, USB HS + FS, 69 I/O, 2 MB / 512 KB, HSM, TrustZone (DS60001795H Table 1-2) [S28].
- **Errata:** errata rev E (Apr 2026) includes an Ethernet data-integrity issue when toggling PC01/PC02 (workaround: slew-rate limit) [S30].
- **Price and stock:** DigiKey India -I/4SB INR 332.89 (single break shown), 170 in stock, 8 weeks [S29]. The "-SL3" variant is INR 472.70; the meaning of the suffix is UNVERIFIED. An Indian e-shop (Tanotis) lists the -SL3 (search result only).
- **Blocker: Zephyr.** `pic32ck_sg01_cult` supports only clock/gpio/pinctrl/uart/watchdog, and the SoC dtsi has only SERCOM + flash nodes [S25].
  - Microchip did add a new `microchip,gmac-g1-eth` driver in 2026 [S22], so Ethernet support may follow, but nothing is upstream for PIC32CK today.
  - Revisit in Q2 2027.

### 4.7 Others checked (not shortlisted)
- **STM32H563VIT6:** same supply problem as the H573, and no crypto accelerator or certificate (R11). No gain.
- **STM32H723/H733 (LQFP100):** INR 875/892 @540, 0 stock, 52 weeks [S7][S8], no TrustZone. Worse than the H573 on both security and supply.
- **STM32N6:** no on-chip flash and BGA packages only (UNVERIFIED this run). Not suitable.
- **SAM E54 (ATSAME54N20A-AU):** INR 664.82 @100, 41 in stock, 39 weeks [S33]. Zephyr is very mature (ETH + MCUboot on `sam_e54_xpro` [S26]), but it has **256 KB RAM** and no TrustZone. Fails the requirements.
- **NXP S32K344 (172-QFP):** INR 1,387.79 @420, 0 stock, 39 weeks [S34]. Zephyr `mr_canhubk3` has ETH + CAN + flash [S26]. Automotive part with HSE-B and no TrustZone. Too expensive, and the lead time is too long.
- **NXP i.MX RT1040/1060/1064:** BGA (RT1040 BGA169 [S38], RT1064 196-LFBGA [S38]). RT1020/1024 come in LQFP but have classic FlexCAN only and 256 KB RAM (UNVERIFIED). Rejected.
- **NXP LPC546xx:** Cortex-M4, no TrustZone, older generation. Rejected without further research.
- **TI AM261x/AM243x:** all NFBGA packages (ZCZ 324, ZFG 304, ZEJ 256, ZNC 293) [S37]. Rejected on package.
  - **TM4C129:** Cortex-M4, classic CAN only, 256 KB RAM (UNVERIFIED this run). Old; rejected.
  - **TI C2000 F2838x:** has Ethernet + CAN FD in QFP but no Zephyr support (UNVERIFIED). Not considered.
- **Nordic:** none of Nordic's parts has an Ethernet MAC. Zephyr has no Nordic Ethernet binding [S22][S40].
- **Infineon:**
  - XMC4800: MultiCAN = classical CAN only (UNVERIFIED this run). Zephyr has `xmc4xxx-ethernet` + `xmc4xxx-can` but Cortex-M4, no TrustZone.
  - XMC7000 / TRAVEO T2G: Ethernet + CAN FD in TEQFP (UNVERIFIED). Zephyr has `kit_xmc72_evk` / `kit_t2g_*` boards but no Ethernet binding for them [S22][S40]. Not shortlisted.
- **GigaDevice GD32H759:** Cortex-M7 600 MHz, up to 3.75 MB flash / 1 MB SRAM, 3x CAN FD, Ethernet, LQFP100/144/176 [S39]. Zephyr has GD32F4/E5 boards but no GD Ethernet or CAN FD driver [S40], and there is no PSA/SESIP certificate. Long-term supply and quality data are not comparable to ST/NXP/Renesas. **Flagged against the reliability-first rule; not recommended.** The same applies to other Chinese Arm MCUs with Ethernet (for example WCH CH32), which were not researched.

## 5. Risks

1. **Zephyr maturity on Renesas.** Renesas support in Zephyr is newer than ST's or NXP's.
   - RA8M1 Ethernet + CAN FD are upstream on the EK board, but the LQFP100 package file, MCUboot partitions and TF-M are not.
   - Budget 2–4 engineer-weeks for the board port and an Ethernet/CAN FD soak test on an EK-RA8M1 before committing (estimate, UNVERIFIED).
2. **ThreadX is effectively lost on Renesas** (strategy "to be determined" [S21]). If ThreadX as a fallback RTOS is a hard requirement, only ST (and possibly NXP, UNVERIFIED) keeps it.
3. **Single-tray stock.** The RA8M1's 720 pieces at DigiKey India is one tray [S15]. Production volumes depend on the 18-week factory lead time. Place a franchised order (Renesas India / Future / Avnet) at design freeze.
4. **ST supply may recover.** If ST's lead time drops back to ~15 weeks (as Future quoted for the H563 in R11), the H573 becomes cheaper than the RA8M1 by ~INR 228. Keep the stack-bus and IO architecture vendor-neutral (UART/SPI/I2C + RMII + 2x CAN FD all exist on every shortlisted part).
5. **Certificates are "RoT Component / Version A".** Confirm with Renesas that production silicon of the LQFP100 RA8M1 is covered by the PSA L3 certificate [S10] (UNVERIFIED for package/revision).
6. **Price sources** are DigiKey India list prices. Mouser/Future/LCSC figures marked "snapshot" come from search indexes and may be stale.

## 6. Open decisions

- **D1.** Approve RA8M1 (R7FA8M1AHECFP#BA0) as the primary baseboard MCU, with MCX N947VKLT as the qualified second source, and the H573VIT6 retained only if ST quotes ≤ 20 weeks.
- **D2.** Buy an EK-RA8M1 now and run a Zephyr Ethernet + CAN FD + MCUboot proof (2 weeks) before the schematic is frozen.
- **D3.** Do a pin plan for RA8M1 LQFP100: RMII + 6 SCI + 2 SPI + 2 IIC + 2 CAN FD + 11 ADC. Fall back to LQFP144 (R7FA8M1AHECFB) if it does not fit.
- **D4.** Decide whether ThreadX as a fallback RTOS is still required. If yes, it excludes Renesas as the primary.
- **D5.** Is RA6M5 (PSA L1, INR 476) acceptable for a cost-down SKU, given that the SE050 holds the keys?
- **D6.** Ask ST (via franchise) for H573VIT6 lead time, and for the H553VG/H5F5 production date, plus PSA L3 status.
- **D7.** Recheck PIC32CK Zephyr Ethernet/CAN status in Q2 2027.

## 7. Datasheets downloaded

Saved in `docs/datasheets/mcu_security/` and added to its INDEX.md:
- Renesas_RA8M1_datasheet.pdf
- Renesas_RA6M5_datasheet.pdf
- Renesas_RA8E1_datasheet.pdf
- NXP_MCXN947_datasheet.pdf (Rev 4, DigiKey-hosted copy)

ST (st.com timeout) and Microchip (HTTP 403) datasheets could not be fetched by script.

## 8. Sources

All fetched or searched 2026-11-14. "Snapshot" = search-index data, not a live page.

- [S1] DigiKey India STM32H573VIT6 (INR 1,033.85 @1 … 633.75 @500; 0 stock; 1 due 12-May-2027; 52 wk; Active; -40…85 °C) — https://www.digikey.in/en/products/detail/stmicroelectronics/STM32H573VIT6/21348909
- [S2] ST eStore STM32H573VI (VIT6/VIT6TR/VIT7/VIT3Q all Out of Stock; USD 6.23 @10k VIT6) — https://estore.st.com/en/products/microcontrollers-microprocessors/stm32-32-bit-arm-cortex-mcus/stm32-high-performance-mcus/stm32h5-series/stm32h563-573/stm32h573vi.html
- [S3] STM32H573VIT6 snapshots: LCSC C7545121 (USD 7.63 @100, 0 stock) — https://www.lcsc.com/product-image/C7545121.html ; element14 CN (180 incoming, CNY 40.80 @500) — https://cn.element14.com/en-CN/stmicroelectronics/stm32h573vit6/mcu-32bit-250mhz-lqfp-100/dp/4294777 ; DigiKey JP (1,719 stock, stale) — https://www.digikey.jp/en/products/detail/stmicroelectronics/STM32H573VIT6/21348909 ; TME (0 stock) — https://www.tme.com/us/en-us/details/stm32h573vit6/st-microcontrollers/stmicroelectronics/
- [S4] ST Community, "Availability of STM32H563VIT6" (8-Oct-2026) — https://community.st.com/stm32-mcus-products-25/availability-of-stm32h563vit6-168829
- [S5] ST product pages, Longevity Commitment 10 yr from 2026-01-01 (snippets) — https://www.st.com/en/microcontrollers-microprocessors/stm32h563vg.html ; https://www.st.com/ja/microcontrollers-microprocessors/stm32h563vg.html
- [S6] ST STM32H553VG ("Evaluation") — https://www.st.com/en/microcontrollers-microprocessors/stm32h553vg.html ; STM32H5E5/H5F5 — https://www.st.com/en/microcontrollers-microprocessors/stm32h5e5-5f5.html ; ST community "New STM32H5 lines" — https://community.st.com/stm32-products-and-hardware-tools-164/new-stm32h5-lines-give-developers-more-room-to-scale-166259
- [S7] DigiKey India STM32H723VGT6 (INR 875.06 @540, 0 stock, 52 wk) — https://www.digikey.in/en/products/detail/stmicroelectronics/STM32H723VGT6/13171212
- [S8] DigiKey India STM32H733VGT6 (INR 892.42 @540, 0 stock, 52 wk) — https://www.digikey.in/en/products/result?keywords=STM32H733VGT6
- [S9] Renesas MCU IoT security solutions (certificates by RA group) — https://www.renesas.com/in/en/application/technologies/iot-security/mcu-iot-security-solutions
- [S10] PSA Certified directory, RA8M1 Version A, Level 3 RoT Component, cert 0632793520122-10540, 17-Feb-2025 — https://products.psacertified.org/products/ra8m1-version-a/certificates ; RA8D1 — https://products.psacertified.org/products/ra8d1-version-a/certificates
- [S11] Renesas press release, PSA L1 with CRA extension for RA8E1/RA8E2/RA4L1 (Feb 2025) — https://www.renesas.com/en/about/newsroom/renesas-teams-applus-laboratories-achieve-psa-certified-level-1-cra-extension-three-new-mcu-groups
- [S12] Renesas RA8M1 Group datasheet R01DS0417EJ0140 Rev 1.40 — https://www.renesas.com/en/document/dst/ra8m1-group-datasheet
- [S13] Renesas RA8E1 Group datasheet R01DS0455EJ0110 Rev 1.10 (19-Dec-2025) — https://www.renesas.com/en/document/dst/ra8e1-group-datasheet ; product page — https://www.renesas.com/en/products/ra8e1
- [S14] Renesas RA6M5 Group datasheet R01DS0366EJ0150 Rev 1.50 (13-Mar-2026) — https://www.renesas.com/en/document/dst/ra6m5-group-datasheet
- [S15] DigiKey India R7FA8M1AHECFP#BA0 (INR 1,364.83 @1 … 861.97 @500; 720 stock; 18 wk; Active; Tj -40…125 °C) — https://www.digikey.in/en/products/detail/renesas-electronics-corporation/R7FA8M1AHECFP-BA0/21801076 ; #HA0 (INR 1,038.47 @1000, 0 stock) — https://www.digikey.in/en/products/result?keywords=R7FA8M1AHECFP
- [S16] Future Electronics R7FA8M1AHECFP#BA0 (USD 9.90 @720, 0 stock, 18 wk; snapshot) — https://www.futureelectronics.com/fr/p/semiconductors--microcontrollers--32-bit/r7fa8m1ahecfp-ba0-renesas-3180453 ; DigiKey FR (0 stock, snapshot) — https://www.digikey.fr/en/products/detail/renesas-electronics-corporation/R7FA8M1AHECFP-BA0/21801076
- [S17] DigiKey India R7FA8E1AFDCFP#BA0 (INR 691.34 @720, 18 wk) and #UA0 (INR 1,092.81 @1, 18 stock) — https://www.digikey.in/en/products/detail/renesas-electronics-corporation/R7FA8E1AFDCFP-BA0/25617243 ; https://www.digikey.in/en/products/result?keywords=R7FA8E1AFDCFP
- [S18] DigiKey India R7FA6M5BH3CFP#AA0 (INR 1,035.75 @1 … 639.29 @540; 342 stock; 18 wk; -40…105 °C) — https://www.digikey.in/en/products/detail/renesas-electronics-corporation/R7FA6M5BH3CFP-AA0/13918502
- [S19] DigiKey India R7FA6M5BH3CFP#BA0 (INR 476.03 @720; 0 stock, not normally stocked; 18 wk) — https://www.digikey.in/en/products/detail/renesas-electronics-corporation/R7FA6M5BH3CFP-BA0/21410198
- [S20] Renesas Product Longevity Program for RA (up to / minimum 15 years, per part) — https://update.renesas.cn/products/microcontrollers-microprocessors/product-longevity-program-plp-renesas-32-bit-arm-cortex-mcus ; https://www.renesas.com/in/en/products/microcontrollers-microprocessors/ra-cortex-m-mcus
- [S21] Renesas FSP page (Eclipse ThreadX support strategy "to be determined") — https://www.renesas.com/en/software-tool/flexible-software-package-fsp ; FSP releases — https://github.com/renesas/fsp/releases
- [S22] Zephyr main, dts/bindings/ethernet and dts/bindings/can (incl. renesas,ra-ethernet, renesas,ra-canfd, nxp,enet-qos, st,stm32h5-ethernet, microchip,gmac-g1-eth, infineon,xmc4xxx-ethernet; no Nordic Ethernet binding) — https://github.com/zephyrproject-rtos/zephyr/tree/main/dts/bindings/ethernet ; https://github.com/zephyrproject-rtos/zephyr/tree/main/dts/bindings/can
- [S23] Zephyr Renesas: ek_ra8m1.dts (&eth, canfd0), ek_ra6m5.dts (&eth, no CAN FD), ra8x1.dtsi (ra-ethernet, 2x ra-canfd, rsip-e51a-trng), ra6-cm33-common.dtsi + r7fa6m5xh.dtsi (ra-ethernet, sce9-rng, no ra-canfd), r7fa8e1afdcfp.dtsi (includes ra8x1) — https://github.com/zephyrproject-rtos/zephyr/tree/main/boards/renesas ; https://github.com/zephyrproject-rtos/zephyr/tree/main/dts/arm/renesas/ra
- [S24] Zephyr EK-RA8P1 board doc (MCUboot via sysbuild) — https://nrfconnectdocs.nordicsemi.com/ncs/latest/zephyr/boards/renesas/ek_ra8p1/doc/index.html ; EK-RA6M5 doc — https://docs.zephyrproject.org/latest/boards/renesas/ek_ra6m5/doc/index.html
- [S25] Zephyr Microchip PIC32C boards (pic32ck_sg01_cult.yaml: clock_control, gpio, pinctrl, uart, watchdog) and dts/arm/microchip/pic32c/pic32ck_sg_gc (sercom-g1 + flash only); pic32cz_ca90_cult (adc, entropy, flash, i2c, spi, uart) — https://github.com/zephyrproject-rtos/zephyr/tree/main/boards/microchip/pic32c ; https://docs.zephyrproject.org/latest/boards/microchip/pic32c/pic32ck_sg01_cult/doc/index.html
- [S26] Zephyr board YAMLs: frdm_mcxn947 (can, netif:eth, flash), nucleo_h563zi (can, netif:eth), nucleo_h723zg (can, netif:eth), mr_canhubk3 (can, netif:eth, flash), sam_e54_xpro (netif:eth, mcuboot, flash) — https://github.com/zephyrproject-rtos/zephyr/tree/main/boards
- [S27] Microchip PIC32CK SG/GC family page — https://www.microchip.com/en-us/products/microcontrollers/32-bit-mcus/pic32-sam/pic32ck-sg-gc ; DigiKey highlight (2x CAN FD) — https://www.digikey.fi/en/product-highlight/m/microchip-technology/pic32ck-sg-gc-microcontroller-family
- [S28] Microchip DS60001795H Table 1-2 (PIC32CK SG device features) — https://onlinedocs.microchip.com/oxy/GUID-23E87D1E-D394-4999-8B0C-DC4246E39160-en-US-8/GUID-49687F71-78A0-4501-BFBB-44C0BEAB8C98.html ; migration guide — https://onlinedocs.microchip.com/oxy/GUID-DECE1EB4-32F8-4576-B14C-2FB93B4C0CBC-en-US-1/GUID-3C9ACF60-7069-4DC3-A169-BB3C3F90B7D9.html
- [S29] DigiKey India PIC32CK2051SG01100-I/4SB (INR 332.89, 170 stock, 8 wk, -40…85 °C) — https://www.digikey.in/en/products/detail/microchip-technology/PIC32CK2051SG01100-I-4SB/29216856 ; family search (SL3 INR 472.70; T-E/4SB INR 474.56 @1000) — https://www.digikey.in/en/products/result?keywords=PIC32CK2051SG01100
- [S30] Microchip PCN SYST-02UAXY854 / errata DS80001066 rev E (Apr 2026) — https://www.farnell.com/datasheets/4768388.pdf
- [S31] Microchip MCUs with integrated security (no PIC32CK certificate listed) — https://microchip.com/en-us/products/security/mcus-with-integrated-security/32-bit
- [S32] Microchip product longevity (client-driven obsolescence) — https://www.microchip.com/en-us/about/corporate-overview/product-longevity
- [S33] DigiKey India ATSAME54N20A-AU (INR 799.88 @1, 664.82 @100; 41 stock; 39 wk; 256 KB RAM) — https://www.digikey.in/en/products/detail/microchip-technology/ATSAME54N20A-AU/7390343
- [S34] DigiKey India S32K344EHT1MPBST (172-QFP; INR 1,387.79 @420; 0 stock, 420 est. 16-Aug-2027; 39 wk) — https://www.digikey.in/en/products/result?keywords=S32K344EHT1MPBST
- [S35] R11 MCX N data (DigiKey India MCXN946VKLT/MCXN947VKLT, NXP pages, PSA directory) — R11_Baseboard_Ethernet.md §2.4, sources S11–S19
- [S36] Mouser India MCXN947VKLT (INR 1,354.79 @1, 189 stock; snapshot) — https://www.mouser.in/c/?m=NXP&pg=2 ; Avnet (USD 8.67 @450, 0 stock) — https://www.avnet.com/americas/product/nxp/mcxn947vklt/evolve-119355256
- [S37] TI AM2612 datasheet SPRSPA7C (packages: ZCZ/ZFG/ZEJ/ZNC NFBGA) — https://www.ti.com/document-viewer/AM2612/datasheet/GUID-17B56251-7949-4C7D-93E6-D3D868AD1747
- [S38] NXP AN13592 (RT1040 BGA169) — https://cn.nxp.com/docs/en/application-note/AN13592.pdf ; Arrow MIMXRT1064DVJ6B (196-LFBGA) — https://www.arrow.com/en/products/mimxrt1064dvj6b/nxp-semiconductors
- [S39] GigaDevice GD32H759 — https://www.gigadevice.com/product/mcu/high-performance-mcus/gd32h7xx-series/gd32h759
- [S40] Zephyr boards/infineon, boards/gd, boards/nordic directory listings — https://github.com/zephyrproject-rtos/zephyr/tree/main/boards/infineon ; https://github.com/zephyrproject-rtos/zephyr/tree/main/boards/gd ; https://github.com/zephyrproject-rtos/zephyr/tree/main/boards/nordic
- [S41] Future Electronics RA6M5 marketing ("PSA L2 + SESIP1", conflicts with [S9]) — https://www.futureelectronics.com/ftm/ai-edge-solutions/renesas-ra6m5-microcontrollers/ ; Renesas RA6M5 launch release — https://www.renesas.com/en/about/press-room/new-ra6m5-group-renesas-completes-mainstream-line-ra6-series-arm-cortex-m33-based-mcus
- [S42] NXP MCXNx4x datasheet Rev 4 (01/2024, DigiKey-hosted) — https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/7138/MCXNx4x_Datasheet.PDF ; NXP notice of Rev 8.2 combined datasheet (Jun 2026) — https://www.farnell.com/datasheets/4791352.pdf
- [R09] R09_Linux_vs_RTOS.md §7 (RTOS support matrix: STM32H573 TF-M `/ns`, STM32CubeH5 ThreadX, frdm_mcxn947 TF-M `/ns`)
- [R11] R11_Baseboard_Ethernet.md (STM32H5 pin data, MCX N prices and lead times, PSA directory search)
