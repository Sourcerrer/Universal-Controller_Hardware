# R28 — Infineon options for the Fieldbus MCU card

Owner request, 2026-11-26: "check for options from infinion for fieldbus". Checked against the Fieldbus MCU-card rules:
- Ethernet MAC on chip (BASE-9, model with Ethernet)
- CAN, classic accepted (FB-1, 2026-11-25)
- ≥ 144 MHz
- MCU below INR 500 at 100 units
- Zephyr or ThreadX, with the chip upstream in Zephyr; missing drivers may be ours (FW-1, 2026-11-25)
- LQFP / TQFP, no fine-pitch BGA
- Vendor list: Infineon is **not** a preferred vendor today (ST, NXP, Nordic, Renesas — COMP-1)

**Closed 2026-11-26 — owner: "drop infineon".**

## Verdict

**No Infineon part is a better choice than the STM32C5A3 (standard) or the Renesas RA6M4 (option).**
- Every Infineon MCU with an Ethernet MAC in a QFP package costs about 2.5–3.5 × the INR 500 cap.
- The cheap Infineon parts (PSoC Control C3) have no Ethernet.

If Infineon were wanted anyway:
- **XMC4700** is the only one with the chip, Ethernet and CAN all in upstream Zephyr, at ≈ INR 1,500–1,850.
- **PSoC Control C3** is the only one near the cap, and it suits only the model without Ethernet.

Not proposed; Infineon stays off the vendor list unless the owner adds it.

## Families

| Family / part | Core | Ethernet | CAN | Package | Zephyr upstream | ≈ INR at 100 (ESTIMATE) | Fit |
|---|---|---|---|---|---|---|---|
| **XMC4700-F100K2048** (XMC4800 = same + EtherCAT slave) | Cortex-M4F 144 MHz, 2 MB flash | Yes, 10/100 | 6 × classic (MultiCAN) | LQFP-100 | **Yes: chip, Ethernet (`eth_xmc4xxx`) and CAN (`can_xmc4xxx`)**, board `xmc47_relax_kit` | ≈ 1,500–1,850 | Fails the cap (≈ 3–3.7 ×). No TrustZone and no crypto engine, so weaker security than the STM32C5A3. Exactly 144 MHz. |
| XMC4500 / XMC4400 | Cortex-M4F 120 MHz | Yes | classic | LQFP-100 | XMC4500 yes (`xmc45_relax_kit`) | ≈ 500–700 | Fails ≥ 144 MHz |
| **XMC7100-F100** (K1088 / K2112 / K4160) | Cortex-M7 250 MHz (dual-core "D" versions), crypto | Yes, 10/100 | Up to 8 × CAN-FD | TQFP-100 | XMC7200 kit only (`kit_xmc72_evk`); no XMC7100 board or Ethernet driver found upstream | ≈ 1,250 (4 MB part; smaller flash not priced) | Fails the cap (≈ 2.5 ×); XMC7100 chip support in Zephyr unconfirmed |
| XMC7200 | Cortex-M7 350 MHz, 2 × Gigabit Ethernet, CAN-FD | Yes | CAN-FD | BGA-272 (TQFP-176 up) | Kit upstream | higher | Fails package and cap |
| **PSoC Control C3 (PSC3M5)** | Cortex-M33 180 MHz, crypto, 256 KB flash / 64 KB SRAM | **No** | 2 × CAN-FD | QFN / TQFP, ≤ 80 pins (to confirm) | Yes: `kit_psc3m5_evk`, MCAN CAN-FD driver | ≈ 500–700 (single-unit prices only seen) | Model without Ethernet only. Near the cap. Pin count and 64 KB RAM tight for the ≈ 90-signal card interface; to check. |
| PSoC Edge E84 | Cortex-M55 + M33 | No | CAN-FD | BGA | Board upstream | — | Fails Ethernet and package |
| AURIX TC3xx / TRAVEO T2G | TriCore / Cortex-M7 automotive | Yes | CAN-FD | LQFP / BGA | AURIX: no upstream Zephyr | high | Fails cap; AURIX fails FW-1 |

Prices: research prices × 1.3 to 100 units, INR 93.9 per USD (R14 rate). Source quantities as quoted:
- XMC4700: DigiKey USD 14.36 at 540, other distributors USD 12.50–15.23 at 1,000.
- XMC7100-F100K4160: Infineon budgetary EUR 9.57 at 1,000.
- PSC3M5: DigiKey USD 7–12 single unit.

## Sources

- Infineon XMC7100-F100K4160AA — https://www.infineon.com/part/XMC7100-F100K4160AA ; XMC7100D-F100K4160AA — https://www.infineon.com/part/XMC7100D-F100K4160AA ; XMC7000 overview (Future) — https://www.futureelectronics.com/npi/infineon-xmc7000-arm-cortex-m7-industrial-microcontroller ; Newark XMC7100 Lite — https://www.newark.com/infineon-xmc7100-lite
- XMC4700 prices — https://www.digikey.com/en/products/detail/infineon-technologies/XMC4700F100K2048AAXQMA1/5725049 ; https://www.findchips.com/search/xmc4700 ; XMC4800 — https://octopart.com/part/infineon/XMC4800F100K2048AAXQMA1 ; XMC4500 (CAN Wiki) — https://can-wiki.info/doku.php?id=controllers%3Ainfineon
- Zephyr XMC47 Relax Kit — https://docs.zephyrproject.org/latest/boards/infineon/xmc47_relax_kit/doc/index.html ; Ethernet driver — https://pigweed.googlesource.com/third_party/github/zephyrproject-rtos/zephyr/+/4344b8bc05dc9f5cd8edb9e3aa4e54f03ab8045d/drivers/ethernet/eth_xmc4xxx.c ; CAN binding — https://docs.zephyrproject.org/latest/build/dts/api/bindings/can/infineon,xmc4xxx-can-node.html
- Zephyr KIT_XMC72_EVK — https://docs.zephyrproject.org/latest/boards/infineon/kit_xmc72_evk/doc/index.html
- Zephyr PSoC Control C3M5 — https://docs.zephyrproject.org/latest/boards/infineon/kit_psc3m5_evk/doc/index.html ; PSoC Control C3 at DigiKey — https://www.digikey.com/en/product-highlight/i/infineon/psoc-control-c3-microcontrollers ; Mouser overview — https://www.mouser.in/new/infineon/infineon-psoc-control-c3-performance-mcus
- Zephyr PSoC Edge E84 — https://docs.zephyrproject.org/latest/boards/infineon/kit_pse84_eval/doc/index.html
