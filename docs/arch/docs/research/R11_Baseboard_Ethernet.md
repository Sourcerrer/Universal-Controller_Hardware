# R11 — Baseboard Ethernet Assembly Option (MCU MAC + RMII PHY + RJ45)

Status: COMPLETE WITH GAPS (2026-11-14). Every price and spec has a source [Sn] (§8); items marked UNVERIFIED or (est.) must be checked before the BOM is frozen. Owner rules applied: Ethernet only from a MAC inside the host chip (no SPI Ethernet); reliability and safety first, cost second.

Builds on R08 (baseboard MCU), R05 §5 (Ethernet short table), R01 (EMC levels), R02/R03 (4G and Wi-Fi modules) and R09 (flash sizing). Prices: DigiKey India INR list prices fetched 2026-11-14 unless stated (upper bounds); other distributors converted at **1 USD = INR 93.9**. Finished cost = BOM x 1.4.

## 1. Executive summary and recommendation

1. **The R08 MCU (STM32H533RET6) has no Ethernet MAC, nor does the H523 or STM32C5.** Confirmed from ST's CubeMX pin database [S1]. The Ethernet-capable equivalents are **STM32H563** (no crypto) and **STM32H573** (crypto + SESIP3/PSA L3, the security twin of the H533). Both bond out the full RMII set in **LQFP64 and LQFP100** [S1].
2. **Recommended ST MCU: STM32H573RIT6 on every baseboard** (2 MB flash / 640 KB RAM, 2x FDCAN, 8 U(S)ART + LPUART, USB FS, Ethernet MAC). DigiKey India INR 582 @500, which is **+INR 204 BOM / +INR 286 finished** over the H533 [S8]. Most of this premium is justified even without Ethernet: R09 sizes the baseboard at ≥ 2 MB flash and ≥ 640 KB RAM. At LCSC/Future 1k prices the H563 is no dearer than the H533 [S7], so the real premium may be near zero (UNVERIFIED). **Move to LQFP100 (STM32H573VIT6) if the CubeMX pin plan shows LQFP64 is too tight.** RMII takes 9 pins, 6 of them ADC-capable, out of 49 I/O (§2.2). That is likely; budget ~+INR 396 finished vs the H533. The new STM32H543/H553 (1 MB, Ethernet) is not yet at distributors (status "Evaluation") [S2][S4] and should be watched for a later cost-down.
3. **Recommended NXP MCU: MCXN947VKLT** (2 MB) or **MCXN946VKLT** (1 MB). Both HLQFP100, ENET-QoS RMII, 2x CAN-FD, EdgeLock, Active, 13-week lead time. DigiKey India INR 844 / 806 @500 [S12][S15]. **Do not use the VNLT order codes** (MCXN947VNLT is discontinued at DigiKey; VKLT is the manufacturer-recommended substitute) [S16]. The MCX N236 in R08 lists no ENET in its feature set (UNVERIFIED against the pin-mux table). No PSA/SESIP certificate was found for MCX N [S18].
4. **PHY (reliability-first): Microchip LAN8742AI-CZ-TR.** It is industrial grade (-40…85 °C), has a dedicated Zephyr driver, and is the PHY on ST's NUCLEO-H563ZI. DigiKey India has 66,628 in stock with a 4-week lead time, at INR 145–178 [S20][S21]. **EMC upgrade / alternate: TI DP83826E** (-40…105 °C; its datasheet specifies IEC 61000-4-2 ±8 kV contact and -4-4 ±4 kV) at INR 182 [S24][S25]. **Cost-down second sources** with dedicated Zephyr drivers: TI DP83825I (INR 83) and Microchip KSZ8081RNAIA (INR 96).
5. **RJ45 (reliability-first): Würth 7499010121A** integrated jack (-40…85 °C, DigiKey India stock), INR 477 @500 [S32]. The popular HanRun HR911105A (INR 85) is listed at **0–70 °C**, so it is not recommended for an industrial port [S35]. The **cheapest sensible alternative is discrete Pulse HX1188NL (-40…85 °C) + a plain shielded RJ45**, about INR 120–280 [S37]. Protection is a TI TPD4E05U06 (INR 12) + Bob-Smith network to chassis. A GDT is optional for long or outdoor runs.
6. **Extra cost of the Ethernet assembly option (fitted only when ordered):**
   - **≈ INR 702 BOM / ≈ INR 983 finished** with the Würth jack.
   - **≈ INR 395–555 BOM / ≈ INR 553–777 finished** with discrete magnetics.
   - **Plus, on every baseboard:** +INR 286 finished for the H533 → H573 change (+~396 if LQFP100 is needed).
7. **Same MCU on every baseboard: yes.** Fit the H573 to all baseboards so that the Ethernet option is purely a placement change (PHY, crystal, jack, TVS, passives). This keeps one firmware image, one Zephyr board, one MCUboot/TF-M flow and one CRA SBOM. The RMII pins are then reserved on every board.
8. **Other routes:**
   - **SPI Ethernet** is excluded by the owner.
   - **The 4G card sold without the modem** (route D) would cost ≈ INR 2,500 finished, against ≈ INR 980 for the baseboard option. It only makes sense if the customer also wants Wi-Fi.
   - **Capacitive (transformerless) coupling** is not acceptable on an industrial field port because it gives no 1500 Vrms isolation.
9. **4G + Ethernet + Wi-Fi module host (§6A): reliability-first choice is the same STM32H573/H563 + LAN8742AI**, with a pre-certified **ESP32-C6-MINI-1U** as the Wi-Fi co-processor (Zephyr `esp_hosted` / `esp_at` host drivers are upstream).
   - **ESP32-S31:** RMII + RGMII, mass production from Jul 2026, but Zephyr support is only an open PR from 2026-11-12 and no module certificate was found. Too new.
   - **RW612:** BGA package and a 52-week lead time.
   - **EC200A as host:** QuecOpen only, no Zephyr, out of stock.

## 2. MCU with on-chip Ethernet MAC

### 2.1 STM32H5: which parts and packages have the MAC (from ST's own pin database)

Method: ST publishes the CubeMX pin/peripheral database as XML (STM32_open_pin_data on GitHub) [S1]. I checked the instance list and the ETH signals bonded to pins for each package. This is the same data CubeMX uses, so it is a primary source. The ST datasheet PDFs could not be downloaded (st.com reset the connection).

| Part (package) | Flash / RAM | ETH instance | RMII pins bonded (all 9: REF_CLK, MDIO, MDC, CRS_DV, RXD0/1, TX_EN, TXD0/1) | FDCAN | U(S)ART + LPUART | USB FS | Source |
|---|---|---|---|---|---|---|---|
| STM32H523RET6 (LQFP64) | 512 KB / 272 KB | **none** | — | 2 | 6 + LP | yes | [S1] |
| STM32H533RET6 (LQFP64) | 512 KB / 272 KB | **none** | — | 2 | 6 + LP | yes | [S1] |
| STM32H543RGT6 (LQFP64) — new 2026 | 1 MB / 304 KB | yes | **yes** | 2 | 7 + LP | yes | [S1][S2] |
| STM32H553RGT6 (LQFP64) — new 2026, crypto | 1 MB / 304 KB | yes | **yes** | 2 | 7 + LP | yes | [S1][S2] |
| STM32H563RIT6 / RGT6 (LQFP64) | 2 MB (RI) or 1 MB (RG) / 640 KB | yes | **yes** | 2 | 8 + LP | yes | [S1] |
| STM32H573RIT6 (LQFP64) | 2 MB / 640 KB | yes | **yes** | 2 | 8 + LP | yes | [S1] |
| STM32H563VIT6 / H573VIT6 (LQFP100) | 2 MB / 640 KB | yes | yes | 2 | 11 + LP | yes | [S1] |

- **H523 / H533 lack Ethernet** (no ETH instance in any of their packages checked) — confirmed [S1].
- **STM32C5 lacks Ethernet**: R08 lists its peripherals (USART/UART/LPUART, FDCAN, USB FS, no Ethernet) [R08 S11][R08 S12]; the C5 is not yet in the open pin database, so this rests on ST's C5 product pages as summarised in R08 (no ETH listed) — treat as confirmed by omission, re-check the C5 datasheet.
- **LQFP64 RMII pin-out (H563/H573/H553):** PA1 REF_CLK, PA2 MDIO, PC1 MDC, PA7 CRS_DV, PC4 RXD0, PC5 RXD1, PA5 TX_EN, PB15 TXD1, PB12 or PC10 TXD0 [S1]. Note ST erratum: TXD1 is on PB15, not PB13 (DS14258 rev 5), and PB13/PB14 cannot be used for ETH [S3].
- **Pin-cost of RMII in LQFP64 (important):** PA1, PA2, PA5, PA7, PC1, PC4, PC5 are also ADC inputs and PA2 is USART2_TX. Using RMII in LQFP64 takes 9 of ~49 GPIOs and about 6 ADC-capable pins. The baseboard needs ≥ 8 ADC channels, 5+ UARTs, 2 FDCAN, 2 SPI, 2 I2C, USB, SWD, VBAT/tamper, plus stack-bus control lines (R08 §4). **LQFP64 is very likely too tight once RMII is reserved; plan LQFP100** (STM32H563VIT6/H573VIT6, or STM32H553VGT6 when available). This must be confirmed with a CubeMX pin plan (open decision D1).
- **New STM32H543/H553 (1 MB / 304 KB, Ethernet, 2 FDCAN, TrustZone):** announced mid-2026; ST says "Available at distribution later this year – contact ST sales for samples"; it *targets* PSA L3 / SESIP3 (not yet certified) [S2]. ST's product page shows the H553RG at "Evaluation" status (search snippet, page timed out) [S4]. Not buyable at distribution today — a watch item, not a design-in choice for the first build.

### 2.2 STM32H5 price, stock and lead time (fetched 2026-11-14)

| Part | DigiKey India (INR, tray) | Stock / lead time (DigiKey IN) | Other 1k-class price | Source |
|---|---|---|---|---|
| STM32H533RET6 (no ETH, R08 baseline) | 377.31 @500 | 0 / 52 wk | LCSC ~USD 4.73–4.86 @100 | [R08 S24][R08 S32] |
| STM32H563RGT6 (1 MB, ETH) | 458.90 @500 | 0 / 52 wk; Active | — | [S5] |
| STM32H563RIT6 (2 MB, ETH) | 528.99 @500 | 0 (1 due 10-Feb-2027) / 52 wk; Active | Future Electronics USD 3.42 @960, 15 wk factory LT; LCSC C20619634 USD 4.10 @100, 473 in stock; DigiKey MX USD 4.56 @1k | [S6][S7] |
| STM32H573RIT6 (2 MB, ETH, crypto, SESIP3/PSA L3) | 581.56 @500 | 0 (1 due 16-Dec-2026) / 52 wk; Active | DigiKey US ~USD 4.63 @1k | [S8][S9] |
| STM32H563VIT6 (LQFP100, 2 MB, ETH) | 608.05 @540 | 0 (90 due 19-May-2027) / 52 wk; Active | — | [S10] |
| STM32H573VIT6 (LQFP100) | not fetched | — | DigiKey US listing exists (STM32H573VIT6TR) | [S9] |
| STM32H553RGT6 / H543RGT6 | no distributor listing found | "Evaluation" status | — | [S2][S4] |

DigiKey's "52 weeks" is its default for non-stocked ST parts; Future's 15-week factory LT and LCSC's 473 pcs in stock suggest normal supply (UNVERIFIED for 1k).

Price delta (no-MAC H533RET6 → MAC parts), DigiKey India @500: H563RGT6 +INR 82; H563RIT6 +INR 152; H573RIT6 +INR 204; H563VIT6 (LQFP100) +INR 231. On LCSC the H563RIT6 (USD 4.10 @100) is actually *cheaper* than the H533RET6 (USD 4.73–4.86 @100), so at real 1k franchised prices the delta is small, roughly INR 0–150 (UNVERIFIED until quoted).

ADC/GPIO budget check from [S1]: H563 LQFP64 has 49 I/O of which 16 are ADC-capable; RMII uses 6 of those 16 (PA1, PA2, PA5, PA7, PC1, PC4, PC5 minus one), leaving ~10 ADC pins. LQFP100 has 80 I/O with the same 16 ADC pins, but the extra 31 GPIOs relieve the UART/SPI/stack-bus pressure, and LQFP100 adds 3 more UARTs. 10 ADC pins is enough for 4 universal AI + housekeeping only if nothing else needs those pins.

### 2.3 Security and software (ST)

- STM32H573: SESIP3 (SESIP-2300042-01) and PSA L3 per ST [R08 S5]; TF-M upstream platform STM32H573I-DK [R08 S35]. The H563 is the same die *without* the crypto accelerator/ST security services (as H523 vs H533), so it has TrustZone but no certified level of its own (UNVERIFIED that no H563 certificate exists).
- H533 PSA L3 is for "H533 with Security Services" [R08 S4]; the H563/H573 pair is the Ethernet-capable equivalent of H523/H533.
- Zephyr: an upstream Zephyr commit states Ethernet support "is already available" for nucleo_h563zi and stm32h573i_dk but was missing from the board feature table [S13]. Driver = ST's common `st,stm32-ethernet` driver used on H7/H5 (driver name UNVERIFIED in this run).
- Longevity: ST lists STM32H523/H533 to Jan 2035 (per ST staff, R05 [S15]); H563/H573 are on ST's 10-year rolling programme (per-part year UNVERIFIED). The new H543/H553 would start a fresh 10-year window.

### 2.4 NXP options with Ethernet MAC + CAN-FD + security

| Part (package) | Flash / RAM | ENET | CAN-FD | UARTs | Security | DigiKey India (INR) | Stock / LT | Status | Source |
|---|---|---|---|---|---|---|---|---|---|
| **MCXN946VKLT** (HLQFP100) | 1 MB / 352 KB | 1x 10/100 ENET-QoS, RMII | 2 | up to 10 LP_FLEXCOMM (UART/SPI/I2C shared) | TrustZone, EdgeLock Secure Enclave Core Profile, PUF, PRINCE, tamper | 806.30 @500 | 0 (past due, est. 27-Oct-2026) / 13 wk | Active | [S11][S12][S14] |
| **MCXN947VKLT** (HLQFP100) | 2 MB / 512 KB | as above | 2 | as above | as above | 843.72 @500 | 0 / 13 wk | Active | [S11][S15] |
| MCXN947VNLT (HLQFP100) | 2 MB | yes | 2 | — | — | 889 @180 (R08) | — | **Discontinued at DigiKey; MFR-recommended substitute MCXN947VKLT** | [S16][R08 S29] |
| MCXN946VNLT / MCXN546VNLT / MCXN547VNLT | — | — | — | — | — | — | — | VNLT codes being replaced by VKLT (same package; VKLT is -40…105 °C vs VNLT -40…125 °C) — treat all **VNLT as do-not-use** | [S16][S17] |
| MCXN547VKLT / MCXN546VKLT (HLQFP100) | 2 MB / 1 MB | yes | 1 (family table, UNVERIFIED) | — | as N94x | Avnet MCXN547VKLT USD 8.55 @900, 0 stock, 112 wk factory LT | — | Active | [S17] |
| MCX N236 (R08 NXP choice) | 1 MB | **no ENET** (UNVERIFIED — not in N23x feature list [R08 S16]) | 2 | 8 | ELS Core | 604 @540 | — | — | [R08 S27] |

- PSA/SESIP: **no certificate found for MCX N94x/N54x** (PSA Certified directory search returned only MCX W23, KW45/MCX W71, LPC55S16) [S18]. NXP markets EdgeLock Secure Enclave but the certified level is UNVERIFIED.
- Zephyr: frdm_mcxn947 board supports the on-chip ENET-QoS (`nxp,enet-qos` MAC + MDIO driver) [S19]; one NXP community report of the Zephyr 4.3 http_server sample failing on 1 of 3 boards (fixed by more DMA descriptors) [S19]. TF-M platform FRDM-MCXN947 upstream [R08 S35].
- Longevity: MCX N is in NXP's Product Longevity programme (minimum 10 years); NXP states MCX N is "available for new designs with a targeted lead time of 16 weeks" [S14].
- Other NXP: i.MX RT10xx with ENET are mostly BGA and lack TrustZone-M (R08) — rejected. LPC546xx/LPC54S018 have ENET but are older Cortex-M4 without TrustZone (not researched; not "latest generation").
- **Price gap:** the NXP Ethernet option (MCXN946VKLT INR 806) costs ~INR 280 more than the ST H563RIT6 (INR 529) at DigiKey India, and ~INR 200 more than the non-Ethernet MCX N236 used in R08.

## 3. RMII PHYs (ranked reliability first, cost second — owner priority 2026-11-14)

### 3.1 Zephyr support (checked in the Zephyr main tree, 2026-11-14) [S20]

- **Dedicated Zephyr PHY drivers exist for:** Microchip **KSZ8081** (`microchip,ksz8081`), Microchip **LAN8742** (`microchip,lan8742`, added by ST in 2025), TI **DP83825** (`ti,dp83825`, by NXP). Others in the folder are gigabit/T1 parts (DP83867, RTL8211F, YT8521/YT8531, AR8031, VSC8541, ADIN, TJA11xx).
- **All other 10/100 PHYs** (LAN8720A, DP83826, RTL8201F, IP101GR, JL1101, YT8512) run only on the generic IEEE 802.3 Clause-22 driver `ethernet-phy` (`phy_mii.c`) — autoneg and link status work, but no vendor errata handling, no interrupt-pin support, no strap/RMII-clock-mode setup.
- Reference boards: Zephyr's **nucleo_h563zi** board (LAN8742A on board) declares the PHY as generic `ethernet-phy` at address 0 with RMII pins PC4/PC5/PA1/PA7/PA2/PC1 [S20]; **frdm_mcxn947** also uses generic `ethernet-phy` [S20]. So LAN8742A on an STM32H5 is the most-tested Zephyr path (ST's own Nucleo PHY).

### 3.2 Comparison

INR at DigiKey India unless stated (fetched 2026-11-14). USD→INR 93.9.

| Rank | PHY (industrial order code) | Temp | Port robustness (datasheet) | Zephyr | Price ~1k | India stock | Longevity / track record | Source |
|---|---|---|---|---|---|---|---|---|
| **1** | **Microchip LAN8742AI-CZ-TR** (SQFN24 4x4) | -40…85 °C | Industrial grade; HBM rating not captured (UNVERIFIED) | **Dedicated driver** + ST Nucleo-H563ZI reference PHY | DigiKey IN INR 177.5 @25 CT, **145.0 @5k reel**; LCSC C621425 USD 1.02–1.57 @1k (≈ INR 96–147) | DigiKey IN 66,628 stock, 4 wk LT | Microchip (SMSC) part, ~10+ years in ST reference designs; Microchip longevity policy (no formal EOL date) | [S21][S22][S23] |
| **2** | **TI DP83826ERHBR** (VQFN32 5x5) / DP83826IRHBR | **E: -40…105 °C**; I: -40…85 °C | **IEC 61000-4-2 ±8 kV contact / ±15 kV air, IEC 61000-4-4 ±4 kV EFT, CISPR 22 Class B** — the only PHY here with system-level EMC figures in the datasheet | generic `ethernet-phy` only (no dedicated driver) | DigiKey IN **INR 181.9 @1k** (E) | 11,948 stock, 26 wk LT | TI industrial PHY, datasheet rev I Aug 2025 | [S24][S25] |
| **3** | **TI DP83825IRMQR** (WQFN24 3x3) | -40…85 °C | HBM ±5 kV on MDI, ±1.5 kV other pins | **Dedicated driver** (used by NXP boards) | DigiKey IN **INR 82.8 @1k**; LCSC C783599 USD 0.19 @500+ (suspiciously low — grey-market risk) | 3,736 stock, 26 wk LT | Datasheet rev C Apr 2026 (actively maintained) | [S26][S27] |
| **4** | **Microchip KSZ8081RNAIA-TR** (QFN24 4x4) | -40…85 °C | HBM not captured (UNVERIFIED) | **Dedicated driver** (NXP i.MX RT EVKs) | DigiKey IN **INR 95.5 @1k reel**; LCSC USD 0.75 @1k (≈ INR 70) | 31,567 stock, 6 wk LT | Micrel/Microchip, very long track record in NXP EVKs | [S28] |
| 5 | Microchip LAN8720AI-CP-TR (QFN24) | -40…85 °C | — | generic only | LCSC C17146 USD 0.575 @1k (≈ INR 54); another snapshot USD 1.54 | LCSC 25,676 | Widely used (ESP32/STM32 hobby boards); older than LAN8742A, which Microchip positions as its successor (UNVERIFIED) | [S29] |
| 6 | Realtek RTL8201FI-VC-CG (QFN32, industrial) | -40…85 °C | — | generic only | LCSC C2763557 USD 0.44–0.50 @980 (≈ INR 42–47) | LCSC ~3,766 | Commodity PHY; RTL8201F-VB-CG is 0–70 °C only (do not use) | [S30] |
| 7 | Motorcomm YT8512H (QFN32) | not confirmed; YT8512C is 0–70 °C | — | generic only (Zephyr has YT8521/8531 gigabit drivers only) | LCSC C2685350 USD 0.42–0.44 @1k (≈ INR 40) | LCSC 16–44k | Chinese domestic PHY; industrial grade UNVERIFIED | [S31] |
| — | IC Plus IP101GR, JLSemi JL1101 / JL1111 | — | — | generic only | not found on LCSC/DigiKey in this run (UNVERIFIED) | — | Not shortlisted | — |

### 3.3 PHY recommendation

- **Default: Microchip LAN8742AI-CZ-TR.** Reasons: industrial grade, highest DigiKey India stock (66k) and shortest lead time (4 wk), dedicated Zephyr driver, and it is the PHY on ST's own NUCLEO-H563ZI, so the STM32H5 MAC + this PHY + Zephyr is the combination ST and the Zephyr CI exercise. Cost ~INR 145–178.
- **Alternate / EMC upgrade: TI DP83826E.** Choose it if the port must meet IEC 61000-4-2 / -4-4 with margin or -40…105 °C ambient: it is the only shortlisted PHY with system-level ESD/EFT ratings in its datasheet. Cost INR 182 (≈ same as LAN8742AI). Zephyr runs it on the generic driver (works, less tested). Note: different footprint (VQFN32 5x5), so it is a layout decision, not a drop-in.
- **Cost-down second source (same Zephyr maturity as LAN8742): TI DP83825I** (INR 83) or **KSZ8081RNAIA** (INR 96). Saves ~INR 50–95 per fitted port vs LAN8742AI. The owner's reliability-first rule means these are second sources, not the default.
- Not recommended for this product: RTL8201F / YT8512 / IP101 / JL1101 (generic driver only, industrial grade unverified for some, no system-level EMC data); LAN8720A (older generation).

## 4. RJ45 with magnetics and port protection

### 4.1 Target levels (from R01)

R01 sets for Ethernet/signal ports: IEC 61000-4-2 design target ±8 kV contact / ±15 kV air; IEC 61000-4-4 burst (capacitive clamp); IEC 61000-4-5 surge ±1 kV line-to-earth (CM) for lines > 30 m, design target ±2 kV CM on long lines; magnetics with 1.5 kV isolation, Bob-Smith termination to chassis through a 1–2 kV cap, low-capacitance TVS on the PHY side [R01 §EMC table and layout rule 5].

How each part of the port meets it (standard practice, UNVERIFIED as a test result until pre-compliance):
- **CM surge/burst:** taken by the 1500 Vrms magnetics isolation + Bob-Smith network (75 Ω + 1 nF / 2 kV to chassis). This is the main reason for the transformer.
- **DM surge and ESD:** a low-capacitance 4-line TVS array on the PHY side of the magnetics (TI TPD4E05U06, Semtech RClamp0524PA), placed at the transformer centre-tap side.
- **±2 kV CM / outdoor runs:** add a GDT (e.g. 90 V) from the Bob-Smith node to chassis; optional, not in the base BOM.
- The TI DP83826 is the only shortlisted PHY specified in its datasheet for IEC 61000-4-2 ±8 kV contact and IEC 61000-4-4 ±4 kV at the MDI pins [S24], which gives margin if the TVS is undersized.

### 4.2 RJ45 with integrated magnetics

| Part | Speed / features | Operating temp | Isolation | Price | Stock | Source |
|---|---|---|---|---|---|---|
| **Würth 7499010121A** (WE-RJ45LAN, THT, shielded, LEDs, Auto-MDIX) | 10/100 | **-40…85 °C** | 1500 Vrms class (family; per-part UNVERIFIED) | DigiKey IN **INR 476.80 @500**; DigiKey FI EUR 4.07 @500 (≈ INR 410) | DigiKey IN 1,415, 12 wk | [S32][S33] |
| HanRun HR911105A (THT, shielded, LEDs) | 10/100 | **0…+70 °C** per vendor listings (one blog says -25…85 °C; HanRun datasheet value not seen — UNVERIFIED) | 1500 Vrms, OCL 350 µH | LCSC C12074 USD 0.90–0.91 @1k (≈ INR 85); Hubtronics INR 74.58 (1 pc) [R05] | LCSC ~81,000 | [S34][S35] |
| Bel Fuse 0826-1X1T-23-F (MagJack) | 10/100 | **0…70 °C** | — | DigiKey MX USD 4.95 @1k (≈ INR 465); out of stock | 20 wk | [S36] |

**Reliability-first verdict:** the HanRun HR911105A is the cheapest and most common, but no source confirms an industrial temperature rating, and the vendor listings say 0–70 °C. For an industrial gateway rated to -20/-40 °C, use the **Würth 7499010121A** (confirmed -40…85 °C, DigiKey India stock) or the discrete route below. The cost gap is ~INR 390 per fitted port (INR 477 vs 85) at DigiKey India list price; a Würth 1k quote should be nearer INR 350–410 (UNVERIFIED). Open decision D3: ask HanRun for an industrial-grade (-40…85 °C) 10/100 MagJack quote — several HanRun gigabit parts are rated -40…85 °C on JLCPCB [S35], so one may exist.

### 4.3 Route C — discrete magnetics + plain RJ45

| Part | Spec | Price | Source |
|---|---|---|---|
| **Pulse HX1188NL / HX1188NLT** (SMD, 1:1, 10/100) | **-40…85 °C**, 1500 Vrms (Pulse H11xx class) | Arrow HX1188NLT ~USD 1.09 (≈ INR 102); E-Sonic USD 2.75 @7,520; Future USD 3.14 @40; element14 SG SGD 4.31 @500 | [S37] |
| Pulse H1102NL (SMD, 1:1) | 1.5 kV isolation; temp not confirmed (commercial assumed) | TME USD 0.64 @520 (≈ INR 60) | [S38] |
| Plain shielded RJ45 8P8C (no magnetics, THT, LCSC generic) | — | ~INR 10–30 (UNVERIFIED, not priced in this run) | — |

Route C total ≈ INR 115–300 (HX1188NL + plain jack), versus INR 410–477 for the Würth integrated jack. It is cheaper and keeps industrial temperature, but costs ~1.5 cm² more board area, needs careful layout of the isolation gap (≥ 2 mm creepage under the transformer, no copper crossing it), and the Bob-Smith network is placed by us rather than inside the jack. Reliability is equal if the layout is right; EMC risk is slightly higher because the magnetics-to-jack traces are now on our PCB.

### 4.4 ESD/surge protection parts

| Part | Spec | Price | Source |
|---|---|---|---|
| **TI TPD4E05U06DQAR** (4-ch, USON-10) | 0.5 pF, 5.5 V working, IEC 61000-4-2 ±12 kV contact (level 4), IEC 61000-4-5 2.5 A (8/20 µs) per TI datasheet, flow-through for Ethernet pairs | Lion Circuits INR 12.05 @1k; Farnell IL USD 0.149 @1k; DigiKey USD 0.135 @3k | [S39] |
| Semtech RClamp0524PA (4-line, SLP2510) | ultra-low capacitance, Ethernet rated | Future USD 0.31 @3k (≈ INR 29); LCSC USD 0.043 @1k (suspiciously low) | [S40] |
| Bob-Smith: 4x 75 Ω + 1 nF/2 kV 1206/1808 Y-rated cap | CM termination | ~INR 5–10 (UNVERIFIED) | — |
| Optional GDT 90 V (outdoor/long-line SKU) | ±2 kV CM | ~INR 15–25 (UNVERIFIED) | — |

**Capacitive (transformerless) coupling:** not acceptable for an industrial field port. It gives no galvanic isolation (IEEE 802.3 requires 1500 Vrms isolation on the MDI), so ground-potential differences between cabinets and IEC 61000-4-5 CM surge go straight into the PHY; it is only meant for short board-to-board or in-box links.

## 5. Costed add-on BOM (baseboard Ethernet option)

Basis: INR, ~1k quantity where available, DigiKey India list price fetched 2026-11-14 unless stated (upper bound; franchised 1k quotes are normally lower). 1 USD = INR 93.9 (as R05/R03). Finished cost = BOM x 1.4. Items marked (est.) are UNVERIFIED engineering estimates.

### 5.1 Parts fitted only when Ethernet is ordered — recommended (reliability-first) build

| Item | Part | INR | Source |
|---|---|---|---|
| RMII PHY | Microchip LAN8742AI-CZ-TR (industrial) | 160 (145 @5k reel – 178 @25 CT) | [S21] |
| PHY clock | 25 MHz crystal + 2 caps (PHY generates 50 MHz REF_CLK for the MCU) | 10 (est.) | — |
| RJ45 + magnetics | Würth 7499010121A (-40…85 °C, shielded, LEDs) | 477 (@500) | [S32] |
| ESD/DM surge | TI TPD4E05U06DQAR | 12 | [S39] |
| Bob-Smith CM termination | 4x 75 Ω + 1 nF/2 kV cap | 8 (est.) | — |
| PHY passives | decoupling, RBIAS, strap resistors, ferrite bead, LED resistors | 15 (est.) | — |
| Extra assembly | THT jack + QFN placement for the option | 20 (est.) | — |
| **Option BOM** | | **≈ 702** | |
| **Option finished (x1.4)** | | **≈ 983** | |

Variants of the fitted-only part:
- **Route C (discrete magnetics):** replace the Würth jack with Pulse HX1188NL (~INR 102–260 [S37]) + plain shielded RJ45 (~INR 20, est.) → option BOM ≈ INR 395–555, **finished ≈ INR 553–777**. Same -40…85 °C rating and 1500 Vrms isolation; needs a careful isolation-gap layout.
- **EMC upgrade PHY:** DP83826E instead of LAN8742AI: +INR 22 BOM (INR 182 [S25]); -40…105 °C and datasheet IEC 61000-4-2/-4-4 ratings.
- **Cheapest (not recommended):** HanRun HR911105A (0–70 °C, INR 85 [S34]) + DP83825I (INR 83 [S26]) → option BOM ≈ INR 240, finished ≈ INR 336. Saves ~INR 650 finished vs the recommended build, but the jack is not rated for industrial temperature.

### 5.2 Cost carried by EVERY baseboard (MCU change)

| Change from R08 baseline STM32H533RET6 (INR 377 @500) | MCU INR | Δ BOM | Δ finished (x1.4) | Comment |
|---|---|---|---|---|
| → STM32H563RIT6 (LQFP64, 2 MB, no crypto) | 529 | +152 | +213 | Loses H533's crypto/PSA L3 → **not recommended** (security regression) |
| → **STM32H573RIT6** (LQFP64, 2 MB, crypto, SESIP3/PSA L3) | 582 | **+204** | **+286** | Like-for-like security, adds MAC + 2 MB/640 KB |
| → STM32H573VIT6 (LQFP100) | ~660 (est. from H563VIT6 608 + H573 premium; not fetched) | ~+283 | ~+396 | If the CubeMX pin plan shows LQFP64 cannot hold RMII + IO (likely, §2.2) |
| → MCXN947VKLT (NXP, 2 MB) vs MCX N236 (NXP baseline, INR 604) | 844 | +240 | +336 | NXP column |

**Is the bigger MCU needed anyway?** Yes, partly. R09 already sizes the baseboard brain (TF-M + Ethernet/TLS + A/B + fieldbus) at **≥ 2 MB flash and ≥ 640 KB RAM** — exactly the H563/H573 class — or 1 MB + external QSPI flash [R09 §sizing]. The H533 (512 KB / 272 KB) only fits with the secondary slot in external NOR and a tight RAM budget. So the move H533 → H573 is justified by flash/RAM and security headroom on its own, and the MAC comes "free" with it. At LCSC/Future 1k prices the H563RIT6 (USD 3.42–4.10) is no dearer than the H533RET6 (USD 4.73–4.86) [S7][R08 S32], so the real every-board premium may be close to zero (UNVERIFIED until quoted).

## 6. Ethernet routes compared (owner request 2026-11-14)

Owner decisions: Ethernet must come from a MAC inside the host chip; reliability first, cost second.

**Route B (SPI Ethernet: W5500, CH390H, DM9051, LAN9250, ENC424J600) — excluded by the owner.** For the record only: Zephyr has upstream drivers for W5500 and DM9051 but none for CH390 [S20].

| Route | (i) Cost on EVERY baseboard (BOM / finished) | (ii) Cost only when Ethernet fitted (BOM / finished) | Reliability / notes |
|---|---|---|---|
| **A. MCU MAC (STM32H573RIT6) + LAN8742AI + Würth integrated jack** | +204 / +286 (H533→H573, LQFP64); ~+283 / ~+396 if LQFP100 | ≈ 702 / ≈ 983 | **Recommended.** Industrial temp throughout, ST reference PHY, mature Zephyr driver. Every-board cost mostly justified by R09 flash/RAM sizing. |
| **C. As A but discrete HX1188NL + plain RJ45** | same as A | ≈ 395–555 / ≈ 553–777 | **Cheapest sensible.** Same temperature and isolation class; needs layout care; ~INR 200–430 finished cheaper per fitted port than A. |
| A-cheap. As A with HanRun HR911105A + DP83825I | same as A | ≈ 240 / ≈ 336 | Not recommended: jack 0–70 °C (UNVERIFIED datasheet). |
| **D. 4G+Ethernet+Wi-Fi card without modem (sold as Ethernet + Wi-Fi card)** | 0 | ≈ 1,800 / ≈ 2,500 (est.: H573 582 + PHY 160 + Würth jack 477 + protection 35 + ESP32-C6-MINI-1U 241 [R03] + power 90 + stack connector 60 + PCB 80 + RF connector 20 + passives 60; enclosure extra) | No new design, but 2.5x the cost of A; only sensible for customers who also want Wi-Fi. |
| MCX N947 (NXP) instead of H573 in A | +240 / +336 vs MCX N236 | as A | NXP option; no PSA/SESIP certificate found; 13 wk LT. |

**Capacitive (transformerless) coupling** — not acceptable for an industrial field port: no 1500 Vrms galvanic isolation, so ground-potential differences and IEC 61000-4-5 CM surge reach the PHY directly (see §4.4).

**Cheapest sensible recommendation:** Route **A with the route-C magnetics** — STM32H573 on every baseboard (premium mostly needed anyway for flash/RAM/security), and, fitted only when ordered, LAN8742AI + Pulse HX1188NL + plain shielded RJ45 + TPD4E05U06 + Bob-Smith network: **≈ INR 553–777 finished per Ethernet board**. If board area or EMC layout risk is a concern, take the Würth integrated jack (≈ INR 983 finished) — the safer default for the first build.

## 6A. Host for the 4G + Ethernet + Wi-Fi module (now needs an on-chip MAC)

The R02/R03 design (ESP32-C6 + SPI Ethernet) is ruled out by the owner decision.

| Option | Ethernet | Cost (key parts, INR) | Stock / lead time | Certification | Zephyr | Reliability view |
|---|---|---|---|---|---|---|
| **(a) STM32H563/H573 host + LAN8742AI + RJ45; ESP32-C6-MINI-1U as Wi-Fi network co-processor (UART/SPI)** | on-chip MAC, RMII | MCU 529–582 + PHY 160 + jack 477 (or ~170 discrete) + C6-MINI-1U 241 [R03] ≈ 1,240–1,460 for these four | MCU: DigiKey IN 0 stock / 52 wk but LCSC 473 pcs, Future 15 wk [S6][S7]; C6-MINI-1U 513 stock, 8 wk [R03] | C6-MINI-1U pre-certified (RED/FCC/etc., R03); host has no radio of its own | MAC + PHY mature (Nucleo-H563ZI); Zephyr host drivers `esp_hosted`, `esp_hosted_mcu`, `esp_at` upstream [S41] | **Recommended.** Same MCU and Zephyr port as the baseboard; every part in production; radio certification stays with the module. |
| (b) Espressif **ESP32-S31** (ESP32-S31-WROOM-3) | on-chip 1 Gb MAC, **RMII and RGMII** (pinout guide; datasheet pre-release v0.5 lists GMAC_RMII_CLK pad) | Hubtronics INR 749 + GST (1 pc) for the module; no 1k price found | Mass production announced Jul 2026 [S42]; Mouser: 0 stock, 423 on order, 13 wk factory LT (search snapshot) [S43] | No certificate found on Espressif's certificate pages (UNVERIFIED) | **Not upstream**: Zephyr PR "esp32s31: add soc, wi-fi, ble and ethernet support" opened 2026-11-12, still open [S41]; ESP-IDF only | Too new: preliminary datasheet (v0.5), no Zephyr, no module certificate seen. Re-evaluate in 2027. |
| (c) NXP RW612 (TFBGA145) | on-chip RMII MAC (TFBGA only) | SoC ~997 alone [R02] | 52 wk LT at DigiKey [R02] | chip-down → own RED/WPC radio tests | frdm_rw612 Ethernet + Wi-Fi in Zephyr, but a reported reset on Ethernet link drop with BLE active (Zephyr 4.3) [R02 ref 26] | Fine-pitch BGA, 52-wk lead time, highest cost — not reliability-first today. |
| (d) LTE modem as host (Quectel EC200A, RMII) | modem RMII (1.8/3.3 V) + external PHY | modem INR 1,250–1,454 retail [R02] | out of stock at Hubtronics [R02] | modem certs: EC200A-CN = SRRC/NAL/CCC only; EU variant separate [R02] | Not Zephyr — QuecOpen RTOS SDK; Wi-Fi over SDIO undocumented [R02] | Vendor-locked firmware, no Zephyr, unclear Wi-Fi support — not recommended. |

**Reliability-first recommendation for the 4G module:** option (a) — STM32H573 (or H563 if the module does not hold keys) + LAN8742AI + industrial magnetics + pre-certified ESP32-C6-MINI-1U as the Wi-Fi co-processor + the Cat-1 modem from R02 over UART/USB. It reuses the baseboard MCU, PHY, Zephyr board port and MCUboot flow, so one Ethernet driver stack serves both products.

## 7. Risks and open decisions

Risks
1. **MCU supply:** DigiKey India shows 0 stock and a 52-week lead time on all STM32H5 parts [S5][S6][S8][S10]. LCSC (473 pcs) and Future (15-week factory LT) look normal [S7]. Get an ST franchised quote (Arrow/Avnet/WPG India) before freezing.
2. **LQFP64 pin budget:** RMII takes PA1/PA2/PA5/PA7/PC1/PC4/PC5/PB15/PB12-or-PC10, which overlaps ADC inputs and USART2 [S1]. The 4 AI + 8+ ADC + 5 UART + 2 FDCAN + stack-bus plan may not fit, so LQFP100 is likely.
3. **H563 vs H573 security:** the H563 lacks crypto/ST security services. Choosing it to save money weakens the PSA L3 position that R08 relied on. The H573 is recommended.
4. **Zephyr maturity:** H5 Ethernet works on Nucleo-H563ZI with the generic PHY driver [S20]. There is an NXP community report of ENET-QoS descriptor tuning on MCX N [S19]. DP83826 has no dedicated Zephyr driver.
5. **RJ45 temperature:** no datasheet-confirmed industrial rating for HanRun 10/100 MagJacks; Würth 7499010121A is confirmed -40…85 °C [S32].
6. **Prices:** LCSC figures come from search-indexed snapshots and some are implausibly low (DP83825I USD 0.19, RClamp USD 0.04), which suggests a grey-market risk. Buy PHYs and TVS from franchised channels.
7. **EMC results:** the port protection follows R01 practice, but no pre-compliance test has been done.

Open decisions
- D1. Do a CubeMX pin plan, then choose LQFP64 or LQFP100 for the H573.
- D2. Integrated Würth jack (safer, +~INR 200–430 finished) or discrete HX1188NL + plain jack (cheapest sensible).
- D3. Ask HanRun/other Indian-stocked vendors for an industrial-grade (-40…85 °C) 10/100 MagJack quote.
- D4. Confirm with ST the H543/H553 production date and PSA/SESIP status as a 1 MB cost-down path.
- D5. Choose the NXP alternative: MCXN947VKLT (2 MB, matches R09) or MCXN946VKLT (1 MB + external flash).
- D6. 4G module: confirm that ESP32-C6 as a Wi-Fi co-processor (esp_hosted over SPI) meets throughput, and re-check ESP32-S31 Zephyr/certification status in Q2 2027.

## 8. Sources

All fetched or searched 2026-11-14.

- [S1] STMicroelectronics STM32_open_pin_data (CubeMX MCU XML: STM32H523RETx, H533RETx, H543RGTx, H543VGTx, H553RGTx, H563RITx, H563VITx, H573RITx, H573VITx) — https://github.com/STMicroelectronics/STM32_open_pin_data/tree/master/mcu
- [S2] ST Community, "New STM32H5 lines give developers more room to scale" (H543/H553 1 MB, Ethernet, PSA L3/SESIP3 targeted, "available at distribution later this year") — https://community.st.com/stm32-products-and-hardware-tools-164/new-stm32h5-lines-give-developers-more-room-to-scale-166259 ; ST series page https://www.st.com/en/microcontrollers-microprocessors/stm32h543-h553.html
- [S3] ST Community, STM32H573VI ETH_TXD1 / TX_EN pins (TXD1 on PB15 per DS14258 rev 5; PB13/PB14 erratum) — https://community.st.com/t5/stm32-mcus-products/re-stm32h573vi-eth-txd1-and-eth-tx-en-pins/td-p/731870 ; https://community.st.com/t5/stm32-mcus-products/error-in-the-init-of-ethernet/m-p/665220
- [S4] ST product page STM32H553RG (status "Evaluation", search snippet; page timed out on fetch) — https://www.st.com/en/microcontrollers-microprocessors/stm32h553rg.html
- [S5] DigiKey India STM32H563RGT6 — https://www.digikey.in/en/products/detail/stmicroelectronics/STM32H563RGT6/21348971
- [S6] DigiKey India STM32H563RIT6 — https://www.digikey.in/en/products/detail/stmicroelectronics/STM32H563RIT6/21349009
- [S7] LCSC STM32H563RIT6 C20619634 (search snapshot) — https://www.lcsc.com/product-detail/C20619634.html ; Future Electronics (search snapshot, USD 3.42 @960) — https://www.futureelectronics.com/p/8182407 ; DigiKey MX punchout — https://punchouttest.digikey.com.mx/en/products/detail/stmicroelectronics/STM32H563RIT6/21349009
- [S8] DigiKey India STM32H573RIT6 — https://www.digikey.in/en/products/detail/stmicroelectronics/STM32H573RIT6/21348903
- [S9] DigiKey US STM32H573RIT6 (search snapshot, ~USD 4.63 @1k) — https://www.digikey.com/en/products/detail/stmicroelectronics/STM32H573RIT6/21348903 ; STM32H573VIT6TR — https://www.digikey.com/en/products/detail/stmicroelectronics/STM32H573VIT6TR/21348880
- [S10] DigiKey India STM32H563VIT6 — https://www.digikey.in/en/products/detail/stmicroelectronics/STM32H563VIT6/18110514
- [S11] NXP MCXN946VKLT part page (ENET 10/100 RMII) — https://nxp.com/part/MCXN946VKLT ; NXP MCX N fact sheet — https://www.nxp.com/docs/en/fact-sheet/MCXNFS.pdf ; datasheet https://www.nxp.com/docs/en/data-sheet/MCXNx4xDS.pdf
- [S12] DigiKey India MCXN946VKLT — https://www.digikey.in/en/products/detail/nxp-usa-inc/MCXN946VKLT/26267805
- [S13] Zephyr commit noting Ethernet support for nucleo_h563zi / stm32h573i_dk — https://pigweed.googlesource.com/third_party/github/zephyrproject-rtos/zephyr/+/293cf9150c2e3d299a41379f2856d53feeabe2c4 ; board page https://docs.zephyrproject.org/latest/boards/st/nucleo_h563zi/doc/index.html
- [S14] NXP MCX N94x/N54x product page (ENET-QoS, 2x FlexCAN FD, 10 LP_FLEXCOMM, EdgeLock, longevity programme, 16-wk target LT) — https://www.nxp.com/products/MCX-N94X-N54X
- [S15] DigiKey India MCXN947VKLT — https://www.digikey.in/en/products/detail/nxp-usa-inc/MCXN947VKLT/26267803
- [S16] DigiKey MCXN947VNLT (Discontinued at DigiKey, substitute MCXN947VKLT) — https://www.digikey.de/en/products/detail/nxp-usa-inc/MCXN947VNLT/22039736
- [S17] Avnet MCXN547VKLT (USD 8.55 @900, 112 wk) — https://www.avnet.com/americas/product/nxp/mcxn547vklt/evolve-119355254 ; DigiKey MY MCXN946VKLT (RM 32.67 @1k) — https://www.digikey.my/en/products/detail/nxp-usa-inc/MCXN946VKLT/26267805
- [S18] PSA Certified product directory (NXP MCX W23, KW45/MCX W71 certificates; none for MCX N) — https://products.psacertified.org/products/nhs52s04-mcx-w23-product-family/certificates
- [S19] Zephyr FRDM-MCXN947 board page (ENET-QoS) — https://docs.zephyrproject.org/latest/boards/nxp/frdm_mcxn947/doc/index.html ; NXP community Ethernet issue — https://community.nxp.com/t5/MCX-Microcontrollers/FRDM-MCXN947-Ethernet-Issue/m-p/2312475
- [S20] Zephyr main tree: drivers/ethernet/phy (phy_microchip_ksz8081.c, phy_microchip_lan8742.c, phy_ti_dp83825.c, phy_mii.c), dts/bindings/ethernet (st,stm32h5-ethernet.yaml, nxp,enet-qos.yaml, davicom,dm9051.yaml, wiznet,w5500.yaml, espressif,esp32-eth.yaml), boards/st/nucleo_h563zi/nucleo_h563zi.dts, boards/nxp/frdm_mcxn947 — https://github.com/zephyrproject-rtos/zephyr/tree/main/drivers/ethernet/phy ; https://github.com/zephyrproject-rtos/zephyr/tree/main/dts/bindings/ethernet
- [S21] DigiKey India LAN8742AI-CZ-TR — https://www.digikey.in/en/products/detail/microchip-technology/LAN8742AI-CZ-TR/4079932
- [S22] LAN8742AI-CZ-TR distributor prices (Octopart USD 1.77 @1k; Arrow ~1.60; LCSC C621425 USD 1.02–1.57 @1k, search snapshots) — https://octopart.com/part/microchip/LAN8742AI-CZ-TR ; https://lcsc.com/datasheet/lcsc_datasheet_2410010203_Microchip-Tech-LAN8742AI-CZ-TR_C621425.pdf
- [S23] Microchip LAN8742A/LAN8742Ai datasheet DS00001989A (commercial 0–70 °C, industrial -40–85 °C) — https://ww1.microchip.com/downloads/en/DeviceDoc/DS_LAN8742_00001989A.pdf
- [S24] TI DP83826E/I datasheet SNLS647I (Aug 2025): IEC 61000-4-2 ±8 kV contact/±15 kV air, IEC 61000-4-4 ±4 kV, CISPR 22 Class B; E -40–105 °C, I -40–85 °C — https://www.ti.com/lit/ds/symlink/dp83826i.pdf
- [S25] DigiKey India DP83826ERHBR — https://www.digikey.in/en/products/detail/texas-instruments/DP83826ERHBR/11502202
- [S26] TI DP83825I datasheet SNLS638C (Apr 2026): -40–85 °C, HBM ±5 kV MDI — https://www.ti.com/lit/ds/symlink/dp83825i.pdf
- [S27] DigiKey India DP83825IRMQR — https://www.digikey.in/en/products/detail/texas-instruments/DP83825IRMQR/10715364 ; LCSC C783599 — https://www.lcsc.com/product-detail/C783599.html
- [S28] DigiKey India KSZ8081RNAIA-TR (search snapshot: INR 95.51 @1k, 31,567 stock, 6 wk) — https://www.digikey.in/en/products/detail/microchip-technology/KSZ8081RNAIA-TR/3728496 ; LCSC/Lisle Apex USD 0.71–0.75 @1k — https://www.lisleapex.com/product-ksz8081rnaia-tr
- [S29] LCSC LAN8720AI-CP-TR C17146 (search snapshot) — https://www.lcsc.com/product-image/C17146.html
- [S30] LCSC RTL8201FI-VC-CG C2763557 — https://www.lcsc.com/product-detail/C2763557.html ; RTL8201F-VB-CG C45044 — https://jlcpcb.com/partdetail/RealtekSemicon-RTL8201F_VBCG/C45044
- [S31] LCSC YT8512H C2685350 / YT8512C C2837480 (0–70 °C) — https://lcsc.com/product-detail/Ethernet-Transceivers_Motorcomm-YT8512H_C2685350.html ; https://www.lcsc.com/product-detail/C2837480.html
- [S32] DigiKey India Würth 7499010121A (INR 476.80 @500, -40–85 °C, 1,415 stock, 12 wk) — https://www.digikey.in/en/products/detail/w%C3%BCrth-elektronik/7499010121A/1639054
- [S33] DigiKey FI Würth 7499010121A (EUR 4.07 @500) — https://www.digikey.fi/en/products/detail/würth-elektronik/7499010121A/1639054
- [S34] LCSC HanRun HR911105A C12074 (USD 0.90–0.91 @992+, ~81k stock; search snapshot) — https://www.lcsc.com/product-image/C12074.html ; datasheet summary (1500 Vrms, 350 µH) — https://datasheetcafe.com/hr911105a-datasheet-rj25-connector/
- [S35] HR911105A operating temperature 0–70 °C (vendor listing) — https://www.rj45-modularjack.com/sale-7295822-hr911105a-rj45-magnetic-connector-for-10-100base-t-nic-applications.html ; HanRun HR915310AE -40–85 °C (JLCPCB) — https://jlcpcb.com/partdetail/21045376-HR915310AE/C19724785
- [S36] DigiKey Bel Fuse 0826-1X1T-23-F (0–70 °C) — https://www.digikey.com.mx/en/products/detail/bel-fuse-inc/0826-1X1T-23-F/1635089
- [S37] Pulse HX1188NL (-40–85 °C) — https://sg.element14.com/pulse-electronics/hx1188nl/xfmr-10-100-base-tx-1port-smd/dp/3861173 ; https://www.arrow.com/en/products/hx1188nlt/pulse-electronics-corporation ; https://www.e-sonic.com/en/pulse-electronics/hx1188nl-44806448.html
- [S38] Pulse H1102NL (TME) — https://www.tme.com/ca/en/details/h1102nl/inductors/pulse/
- [S39] TI TPD4E05U06DQAR prices — https://lioncircuits.com/parts/TPD4E05U06DQAR ; https://il.farnell.com/texas-instruments/tpd4e05u06dqar/diode-esd-protection-5-5v-0-5pf/dp/3116511 ; https://www.digikey.com/en/products/detail/texas-instruments/TPD4E05U06DQAR/3996774
- [S39b] TI TPD4E05U06 datasheet (IEC 61000-4-2 ±12 kV contact, IEC 61000-4-5 2.5 A) — https://www.ti.com/lit/ds/symlink/tpd4e05u06.pdf
- [S40] Semtech RClamp0524PA — https://www.semtech.com/products/circuit-protection/low-capacitance/RClamp0524PA ; Future Electronics — https://www.futureelectronics.com/p/2015894 ; LCSC C40960 — https://www.lcsc.com/product-image/C40960.html
- [S41] Zephyr main tree drivers/wifi (esp_at, esp_hosted, esp_hosted_mcu) — https://github.com/zephyrproject-rtos/zephyr/tree/main/drivers/wifi ; open PR #125547 "espressif: esp32s31: add soc, wi-fi, ble and ethernet support" (created 2026-11-12) — https://github.com/zephyrproject-rtos/zephyr/pull/125547 ; PR #123231 — https://github.com/zephyrproject-rtos/zephyr/pull/123231
- [S42] ESP32-S31 mass production news (28 Jul 2026) — https://book.st-hakky.com/en/news/s31-mass-production-start-high-performan ; ESP32-S31 pinout guide (1 Gb MAC, RMII and RGMII) — https://esp32-s31.espressif.com/en/docs/6-Pinout%20%26%20IO%20Introduction/pinout-and-io-allocation ; datasheet — https://documentation.espressif.com/esp32-s31_datasheet_en.pdf ; CNX — https://www.cnx-software.com/2026/03/24/esp32-s31-dual-core-risc-v-mcu-offers-gigabit-ethernet-wifi-bluetooth-and-802-15-4-connectivity/
- [S43] Mouser ESP32-S31-WROOM-3 (new-product page; stock snapshot via search) — https://www.mouser.in/new/espressif/espressif-esp32-s31-wroom-3-modules/ ; Hubtronics INR 749.15 + GST — https://hubtronics.in/espressif-esp32-s31-wroom-3
