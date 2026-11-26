# R29 — Microchip / Atmel options for the Fieldbus MCU card (full sweep)

Owner request, 2026-11-26: "have you fully checked atmel + microchip". Earlier checks were partial:
- PIC32CK (R12, R25, D-32)
- SAM E54 (R12)
- SAM E70 2 MB part only (PRD §5, 2026-11-22: ≈ INR 1,245)
- PIC32MZ-W1 (PRD §5, 2026-11-22)

This sweep covers every Microchip 32-bit family with an Ethernet MAC or CAN, against the rules as they stand on 2026-11-26:
- Ethernet MAC on chip (BASE-9)
- CAN, classic accepted (FB-1)
- ≥ 144 MHz
- MCU below INR 500 at 100 units
- Zephyr or ThreadX, Zephyr chip upstream, drivers may be ours (FW-1)
- QFP package

Microchip is not a preferred vendor (COMP-1: ST, NXP, Nordic, Renesas).

## Verdict

**No Microchip / Atmel part fits.**
- **The ≥ 144 MHz parts cost ≈ 2–3 × the cap:** SAM E70, SAM V71, PIC32MZ EF, PIC32CZ CA all have Ethernet and CAN.
- **The affordable parts all run at 120 MHz:** PIC32CK, PIC32CX SG, SAM E5x, SAM4E. With classic CAN and the relaxed Zephyr rule, **the speed rule is now the only thing keeping the PIC32CK out**. Its missing Zephyr drivers (Ethernet, CAN, ADC) would be ours to write.

The closest fit is the SAM E70: 300 MHz, Ethernet and CAN-FD, mature Zephyr, LQFP100, crypto engine but no TrustZone. It costs ≈ INR 1,000–1,050, so about +700–750 BOM over the STM32C5A3.

## Families

| Family / part | Core | Ethernet | CAN | Package | Zephyr upstream | ≈ INR at 100 (ESTIMATE) | Fit |
|---|---|---|---|---|---|---|---|
| **SAM E70** ATSAME70N19B (512 KB) / N20B (1 MB) / N21B (2 MB) | Cortex-M7 300 MHz; AES, TRNG, SHA (ICM); no TrustZone | Yes (GMAC) | 2 × CAN-FD (MCAN) | LQFP100 | Yes: `sam_e70_xplained`, GMAC Ethernet. CAN-FD listed on the sister `sam_v71_xult`, same MCAN block. | N19 ≈ 1,000; N20 ≈ 1,045 (DigiKey 100-unit price); N21 ≈ 1,245 | Fails the cap (≈ 2 ×); stock is uneven (N20B tray restocks Jan 2027, tape-and-reel in stock) |
| SAM V70 / V71 | Same die, automotive grade | Yes | CAN-FD | LQFP100 / 144 | Yes: `sam_v71_xult` | > SAM E70 | Fails the cap |
| SAM S70 | Cortex-M7 300 MHz | No | No | — | — | — | Fails Ethernet and CAN |
| **PIC32MZ EF** (PIC32MZ2048EFM100, EFH100, EFG100) | MIPS M-class 200 / 252 MHz; crypto on EFM | Yes | 2 × classic | TQFP100 | No (MIPS); ThreadX through MPLAB Harmony (not verified) | ≈ 1,275 | Fails the cap (≈ 2.5 ×); MIPS core |
| **PIC32CZ CA80 / CA90** | Cortex-M7 300 MHz; CA90 adds an HSM | Gigabit | Up to 6 × CAN-FD | TQFP100 … BGA208 | Not found (MPLAB Harmony only) | > 1,400 (launch price was for the BGA208 part) | Fails the cap and Zephyr |
| PIC32CK SG / GC | Cortex-M33 **120 MHz**; HSM + TrustZone | Yes | 2 × CAN-FD | TQFP100 | Chip yes (`pic32ck_sg01_cult`); no Ethernet / CAN / ADC drivers | ≈ 300–400 (R12) | Fails ≥ 144 MHz only |
| PIC32CX SG41 / 60 / 61, SAM E53 / E54 | Cortex-M4F **120 MHz** | Yes | CAN-FD (E54, SG61) | TQFP100 | SAM E54 yes (`sam_e54_xpro`) | ≈ 665 (SAM E54, R12) | Fails ≥ 144 MHz |
| SAM4E | Cortex-M4 **120 MHz** | Yes | classic | LQFP100 | Yes (`sam4e_xpro`) | — | Fails ≥ 144 MHz |
| PIC32MZ-W1 | MIPS 200 MHz, Wi-Fi | Yes | CAN-FD | — | No | — | Checked 2026-11-22; no Zephyr |
| PIC32CM, SAM D2x / D5x / C2x | M0+ / M23 / M4 ≤ 120 MHz | No | some | — | — | — | Fail speed and Ethernet |

Prices: research prices × 1.3 to 100 units, INR 93.9 per USD. Source quantities as quoted:
- ATSAME70N19B: USD 8.31 at 1,080 (Findchips).
- ATSAME70N20B-AN: DigiKey USD 11.11 at 100.
- PIC32MZ2048EFM100: USD 13.59 at 100.
- PIC32CZ CA80: launch USD 14.80 at 10,000 (BGA208).

## Sources

- SAM E70 prices — https://www.digikey.com/en/products/detail/microchip-technology/ATSAME70N20B-AN/ATSAME70N20B-AN-ND/9342105 ; https://www.findchips.com/search/atsame70n19b-an ; https://octopart.com/part/microchip/ATSAME70N19B-AN
- Zephyr SAM E70 Xplained — https://docs.zephyrproject.org/latest/boards/atmel/sam/sam_e70_xplained/doc/index.html ; SAM V71 Xplained Ultra — https://docs.zephyrproject.org/latest/boards/atmel/sam/sam_v71_xult/doc/index.html
- PIC32CZ CA — https://www.microchip.com/en-us/products/microcontrollers/32-bit-mcus/pic32-sam/pic32cz-ca ; launch release — https://www.microchip.com/en-us/about/news-releases/products/new-32-bit-mcu-features-an-embedded-hardware-security-module ; CNX — https://www.cnx-software.com/2023/10/12/microchip-pic32cz-ca-300-mhz-arm-cortex-m7-mcu-hardware-security-module-hsm/ ; Mouser — https://cz.mouser.com/en/new/microchip/microchip-pic32cz-ca80-ca90-mcus
- PIC32MZ EF — https://www.mouser.com/ProductDetail/Microchip-Technology/PIC32MZ2048EFM100-I-PT?qs=sGAEpiMZZMua3V2yDfsb6SWKwEzV11pUakBdFMpB8QY%3D ; https://octopart.com/pic32mz2048efh100-i/pt-microchip-59298425
- Earlier: R12 (PIC32CK, SAM E54 prices and Zephyr), R25 (PIC32CK speed), PRD §5 rows of 2026-11-22
