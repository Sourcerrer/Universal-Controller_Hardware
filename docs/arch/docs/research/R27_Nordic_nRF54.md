# R27 — Nordic nRF54 as the Fieldbus MCU

Owner request, 2026-11-25: "also check for nrf54 parts". Checked as Fieldbus controller MCU-card candidates against BASE-9 (Ethernet MAC on chip), FB-1 (CAN; classic CAN 2.0B accepted since 2026-11-25), FW-1 (upstream Zephyr), speed ≥ 144 MHz, MCU below INR 500, and the manufacturing rule (standard packages, no fine-pitch BGA).

## Verdict

**No nRF54 part fits either Fieldbus model.**
- **Model with Ethernet:** no nRF54 part has an Ethernet MAC. Nordic has no MCU with one, and SPI Ethernet is banned.
- **Model without Ethernet:** the nRF54L parts run at 128 MHz (under 144 MHz) and have no CAN. The nRF54H20 has CAN-FD and 320 MHz, but it comes only in a chip-scale package, and Nordic restricts its supply to selected customers.

Zephyr support is strong across the nRF54 range (Nordic's own SDK is Zephyr), so FW-1 is not the problem here.

## Parts

| Part | Core | Ethernet | CAN | Package | Price / stock (2026-11-25) | Fit |
|---|---|---|---|---|---|---|
| nRF54L15 (and the pin-compatible nRF54L10 / L05) | Cortex-M33 128 MHz + RISC-V coprocessor; BLE 6, 802.15.4 | No | No | QFN48 6 × 6 mm, WLCSP | Mouser NRF54L15-QFAA-R USD 4.15 at 1, 2.37 on a 3,000 reel; DigiKey USD 4.85 at 1; ≈ USD 2.89 at 1,000 → ≈ INR 300–390 at 100 (ESTIMATE). Mouser shows 6,000 on order. | Fails speed, CAN and Ethernet |
| nRF54LM20A | Cortex-M33 128 MHz; USB HS | No | No | QFN52 | ≈ USD 3.56 at 1,000 (third-party comparison) | Same as the nRF54L15 |
| nRF54LV10 | Low-voltage variant, runs from a 1.5 V cell | No | No | — | No price found | Same as the nRF54L15 |
| nRF54H20 | Multi-core: Cortex-M33 320 MHz application core + radio core + RISC-V cores | No | CAN-FD | Chip-scale (CKAA), not LQFP / QFN | Symmetry USD 7.55 at 1, 6.50 at 1,000 (≈ INR 610–710); Future: 32-week lead time; DigiKey: no longer available. Nordic focuses it on selected customers and applications (Ezurio has withdrawn its nRF54H20 modules). | Fails package, supply and Ethernet |

## Elsewhere in the family

The nRF54L15 would suit a BLE-only or very-low-power node: Bluetooth LE 6 with a 14-bit ADC, at about INR 300. Our Wi-Fi + BLE module needs Wi-Fi, which the nRF54 doesn't have (Nordic pairs it with the nRF7002 companion chip). Not proposed; noted only.

## Sources

- Nordic, nRF54L15 — https://www.nordicsemi.com/Products/nRF54L15 ; nRF54L peripherals comparison — https://academy.nordicsemi.com/courses/nrf54l-series-express-course/lessons/lesson-3-peripherals-and-system-components/topic/nrf54l-series-peripherals-comparison/
- Mouser, NRF54L15-QFAA-R — https://www.mouser.com/ProductDetail/Nordic-Semiconductor/NRF54L15-QFAA-R?qs=QpmGXVUTftHTOlr7aJcAUw%3D%3D ; DigiKey nRF54L15 — https://www.digikey.com/en/product-highlight/n/nordic-semi/nrf54l15-multiprotocol-soc
- nRF54 price comparison (blog) — https://blog.mbedded.ninja/programming/microcontrollers/nordic/nrf54/
- nRF54H20: Ezurio BL54H20 (CAN-FD; module withdrawn, restricted SoC supply) — https://www.ezurio.com/product/bl54h20-series-multi-core-bluetooth-le-80215-4-nfc ; Symmetry — https://www.symmetryelectronics.com/products/nordic-semiconductor/nrf54h20-ckaa-r/ ; Future — https://www.futureelectronics.com/p/semiconductors--wireless-rf--transceiver-ics/nrf54h20-ckaa-r-nordic-semiconductor-6204794 ; DigiKey — https://www.digikey.com/en/products/detail/nordic-semiconductor-asa/NRF54H20-CKAA-R/24773454
