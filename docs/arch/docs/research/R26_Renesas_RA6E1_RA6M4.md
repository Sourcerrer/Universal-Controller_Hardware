# R26 — Renesas RA6E1 / RA6M4 as the Fieldbus MCU

Owner request, 2026-11-25: "check for Renesas R7FA6E10D2CFP#AA0 / R7FA6M4AF3CFP#AA0 suitability and availability".
Checked against the Fieldbus MCU rules (PRD BASE-1, BASE-9, BASE-10, FB-1, FW-1; `docs/arch/CLAUDE.md` part rules).

## Update 3 2026-11-25 — Renesas RA6 budgetary prices (owner screenshot of the Renesas RA6 selector)

All RA6 groups are Active, longevity Dec 2041, and "In Stock" at Renesas. The selector gives budgetary prices at 1,000 units; converted here at × 1.3 (100-unit rule) and INR 93.9 per USD. ESTIMATES.

| Group | Core | Ethernet | CAN | Zephyr (upstream) | ≈ INR at 100 | Fit for the Fieldbus MCU card |
|---|---|---|---|---|---|---|
| RA6E2 | M33 200 MHz, 128–256 KB flash, 40 KB RAM | No | 1 × CAN-FD | Yes — `ek_ra6e2`, `fpb_ra6e2`, CAN-FD node upstream | ≈ 247 | Model without Ethernet only. **64-pin max** and 40 KB RAM: likely too few pins for the ≈ 90-signal card interface. Pin count to check. |
| RA6T2 | M33 240 MHz (motor control), up to 512 KB | No | CAN-FD on some variants | No board found upstream (chip support to confirm) | ≈ 383 | Model without Ethernet only, LQFP100 available; Zephyr chip support unconfirmed |
| RA6E1 | M33 200 MHz | Yes | 1 × classic | Chip yes; CAN driver ours | ≈ 339 | Both models; no crypto engine |
| RA6M5 | M33 200 MHz, TrustZone + crypto, 2 MB | Yes | 2 × CAN-FD | Chip yes (`ek_ra6m5`); CAN-FD node to confirm | ≈ 558 | Best feature match, but **over the INR 500 cap** |
| **RA6M4** | M33 200 MHz, TrustZone + crypto, 1 MB | Yes | 2 × classic | Chip yes; CAN driver ours | **≈ 425** | **Option card (BASE-10 update 6): +125 over the STM32C5A3** |
| RA6M1 / RA6M2 / RA6M3 | M4 120 MHz | M2 / M3 yes | classic | — | ≈ 400–780 | Fail the ≥ 144 MHz rule |

Sources: Renesas RA6 selector (owner screenshot, 2026-11-25); RA6E2 — https://www.renesas.com/en/products/ra6e2/part-details/r7fa6e2bb3cfm-aa0 , Zephyr EK-RA6E2 — https://docs.zephyrproject.org/boards/renesas/ek_ra6e2/doc/index.html ; RA6T2 — https://www.renesas.com/ra6t2 ; Zephyr `renesas,ra-canfd` binding — https://docs.zephyrproject.org/latest/build/dts/api/bindings/can/renesas%2Cra-canfd.html ; Zephyr EK-RA6M5 — https://docs.zephyrproject.org/latest/boards/renesas/ek_ra6m5/doc/index.html

## Update 2 2026-11-25 — owner: "Each MCU: Zephyr or ThreadX" / "Chip upstream, drivers ours"

**Both parts now pass FW-1.** Both chips are in upstream Zephyr (boards `fpb_ra6e1`, `ek_ra6m4`, with Ethernet), and Renesas FSP includes a ThreadX port. The missing piece is a Zephyr driver for the classic CAN block, which we would write ourselves on top of the FSP `r_can` module, following the existing `can_renesas_ra.c`.

What still separates them:
- **RA6E1 (R7FA6E10D2CFP):** ≈ INR 400–500, no crypto engine (weaker than the STM32C5A3: no hardware AES / ECC / SHA for secure boot and TLS), 1 × CAN, −40…85 °C.
- **RA6M4 (R7FA6M4AF3CFP):** ≈ INR 475–505 (at or over the INR 500 cap), crypto engine + TrustZone (no PSA certificate found), 2 × CAN, −40…105 °C.
- Both: 200 MHz, Ethernet MAC, LQFP100; stock in the hundreds, 14–18-week lead times.

Not applied: a Renesas MCU card would be a new card on the BASE-11 interface. The default cards stay STM32C5A3 (standard) and STM32H573 (option).

## Update 2026-11-25 — owner: "add RENESAS to the list. can instead of canfd isfine"

With Renesas now a preferred vendor and classic CAN accepted, both parts pass on vendor and CAN. **They still fail FW-1 (upstream Zephyr for every peripheral we use).** Zephyr's only Renesas RA CAN driver is `drivers/can/can_renesas_ra.c` (`DT_DRV_COMPAT renesas_ra_canfd`, Kconfig `CAN_RENESAS_RA_CANFD`). It is built on the FSP `r_canfd` module for the CAN-FD block. Nothing uses the classic `r_can` block that the RA6E1 and RA6M4 have. The RA6 SoC devicetree files (`ra6-cm33-common.dtsi`, `r7fa6m4ax.dtsi`, `r7fa6m4af3cfb.dtsi`, `r7fa6e10x.dtsi`, `r7fa6e10f2cfp.dtsi`) have no CAN node at all [S8].

Ways forward: (a) write a classic-CAN driver ourselves and get it upstream, which is effort and doesn't meet "upstream" until it is merged; (b) Renesas parts with the CAN-FD block and upstream Zephyr support: RA8E1 / RA8M1 (≈ INR 764, over the INR 500 cap, D-38). RA6M5 with CAN-FD: its upstream Zephyr CAN node is unconfirmed (R12 found none).

## Verdict (before the update)

**Neither part fits as a Fieldbus controller MCU: neither has CAN-FD.** Renesas's own part pages list "CAN-FD (ch) 0" for both [S1][S2]. The Fieldbus controller's CAN port is CAN-FD (FB-1), and the current MCU cards (STM32C5A3, STM32H573) both have 2 × FDCAN. A classic CAN 2.0B controller handles J1939 and classic CANopen, but it cannot send or receive CAN-FD frames, and on a mixed bus it flags FD frames as errors.

If Renesas is wanted, the RA6M5 with the "B" order code (R7FA6M5BH3CFP, CAN-FD, already covered in R12) is the family member that fits. Renesas is outside the preferred vendors (ST, NXP, Nordic).

## Comparison

| | STM32C5A3VGT6 (standard card) | R7FA6E10D2CFP#AA0 (RA6E1) | R7FA6M4AF3CFP#AA0 (RA6M4) |
|---|---|---|---|
| Core / speed | Cortex-M33, 144 MHz | Cortex-M33, 200 MHz | Cortex-M33, 200 MHz |
| Flash / RAM | 1 MB | 512 KB + 8 KB data flash / 256 KB | 1 MB + 8 KB data flash / 256 KB |
| Ethernet MAC | Yes | Yes, 1 × 10/100 | Yes, 1 × 10/100 |
| CAN | 2 × CAN-FD | **1 × CAN 2.0B, no CAN-FD** | **2 × CAN 2.0B, no CAN-FD** |
| Crypto | Hardware crypto, no TrustZone | TrustZone, TRNG, unique ID — **no crypto engine** | TrustZone + Secure Crypto Engine (AES, ECC, RSA, SHA-2, tamper) |
| PSA certification | — | None found | None found |
| Temperature | −40…85 °C | −40…85 °C | −40…105 °C |
| Package | LQFP100 | LQFP100 14 × 14 mm | LQFP100 14 × 14 mm |
| Lifecycle | Active | Active, longevity 2041 (family) | Active (the #BA0 tray version lists longevity Dec 2041) |
| Zephyr upstream | Yes | Board `fpb_ra6e1`: Ethernet listed [S4] | Board `ek_ra6m4`: Ethernet listed; Ethernet buffers must sit in non-secure RAM [S3] |

Not confirmed: upstream Zephyr support for the classic CAN controller on RA6E1 and RA6M4. The board pages don't list it.

## Availability and price (100 units, INR at 93.9 per USD)

| Part | Stock seen (2026-11-25) | Price | ≈ INR |
|---|---|---|---|
| R7FA6E10D2CFP#AA0 | DigiKey 68–90 (18-week lead time); Mouser 200; Flip Electronics 10,064 (broker; treat with caution) | DigiKey USD 7.16 at 1, 4.28 at 540; Renesas budgetary USD 4.28 | ≈ 400–500 (no 100-unit break seen; ESTIMATE) |
| R7FA6M4AF3CFP#AA0 | Mouser 166–450 (14-week lead time); DigiKey 80–224 (18-week lead time); Farnell 90–124 (Farnell marks it "no longer stocked / no longer manufactured", but Renesas shows it Active) | Mouser USD 8.85 at 1, 5.01 at volume; DigiKey USD 5.06 at 1,080; Renesas budgetary USD 5.38 | ≈ 475–505 at volume, more at 100 — **at or over the INR 500 cap** (ESTIMATE) |

India: a one-off listing (Tanotis) shows the RA6M4 at INR 1,521 for a single unit, including tax. No Indian franchise stock was found for either part.

## Fit against the rules

- **CAN-FD (FB-1): fails, both parts.** This alone rules them out.
- Ethernet MAC on chip (BASE-9): passes, both.
- Speed ≥ 144 MHz: passes, both (200 MHz).
- Price below INR 500: RA6E1 likely passes; RA6M4 is borderline.
- Security: the RA6E1 has no crypto engine, which is weaker than the STM32C5A3. The RA6M4 has one, but no PSA certificate was found, so it doesn't replace the STM32H573 (PSA L3).
- Zephyr (FW-1): the boards exist upstream with Ethernet; CAN is unconfirmed.
- Vendor list: Renesas is outside ST / NXP / Nordic.

## Sources

- [S1] Renesas, R7FA6E10D2CFP#AA0 part page — https://www.renesas.com/en/products/ra6e1/part-details/r7fa6e10d2cfp-aa0 ; RA6E1 family page (CAN 2.0B, TrustZone / TRNG / unique ID) — https://www.renesas.com/en/products/ra6e1
- [S2] Renesas, R7FA6M4AF3CFP#AA0 part page — https://www.renesas.com/en/products/ra6m4/part-details/r7fa6m4af3cfp-aa0 ; #BA0 — https://www.renesas.com/en/products/ra6m4/part-details/r7fa6m4af3cfp-ba0
- [S3] Zephyr, EK-RA6M4 board — https://docs.zephyrproject.org/latest/boards/renesas/ek_ra6m4/doc/index.html
- [S4] Zephyr, FPB-RA6E1 board — https://docs.zephyrproject.org/latest/boards/renesas/fpb_ra6e1/doc/index.html
- [S5] DigiKey, R7FA6E10D2CFP#AA0 — https://www.digikey.com/en/products/detail/renesas-electronics-corporation/R7FA6E10D2CFP-AA0/16008853
- [S6] Mouser, R7FA6M4AF3CFP#AA0 — https://www.mouser.com/ProductDetail/Renesas-Electronics/R7FA6M4AF3CFPAA0?qs=DPoM0jnrROVnmhqAEXvmNw%3D%3D ; DigiKey — https://www.digikey.com/en/products/detail/renesas-electronics-america-inc/R7FA6M4AF3CFP-AA0/13619868 ; Farnell — https://at.farnell.com/en-AT/renesas/r7fa6m4af3cfp-aa0/mcu-32-bit-200mhz-lqfp-100/dp/4147311
- [S8] Zephyr main: https://github.com/zephyrproject-rtos/zephyr/blob/main/drivers/can/can_renesas_ra.c ; https://github.com/zephyrproject-rtos/zephyr/blob/main/drivers/can/Kconfig.renesas_ra ; https://github.com/zephyrproject-rtos/zephyr/tree/main/dts/arm/renesas/ra/ra6
- [S7] Tanotis (India), R7FA6M4AF3CFP#AA0 — https://www.tanotis.com/products/renesas-r7fa6m4af3cfp-aa0-r7fa6m4af3cfp-aa0-arm-mcu-ra-family-ra6-series-ra6m4-group-microcontrollers-cortex-m33-32-bit-200-mhz-new
