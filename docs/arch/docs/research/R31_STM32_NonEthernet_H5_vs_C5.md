# R31 — STM32H5 and STM32C5 parts for the Fieldbus model without Ethernet

Owner request, 2026-11-26: "check for other stm32h5 offernings for non ethernet fieldbus with zephyr support overall pricing & availability" / "compare with c5".

Rules for the model without Ethernet:
- CAN (1 port used; classic accepted)
- ≥ 144 MHz
- MCU below INR 500 at 100
- Chip upstream in Zephyr (FW-1)
- 100-pin package for the ≈ 90-signal MCU-card interface

Today that model uses the same STM32C5A3VGT6 card as the model with Ethernet, with the Ethernet parts not fitted.

## Correction 2026-11-26 — H5 pin compatibility and H562 vs H563 (owner: "stm32h562 vs 563")

ST AN5959 ("Migrating within the STM32H5 MCUs"): the STM32H523/533 in LQFP64, LQFP100 and LQFP144 have the same pins as the STM32H563/573 and STM32H562. So **one H5 MCU card takes the H523, H533, H562, H563 and H573**. The verdict line below that the H523/H533 "needs its own card" was wrong: they fit the H5 card (`mcu-card-stm32h5`).

H562 vs H563:
- Same datasheet (DS14258), same core (Cortex-M33 250 MHz, TrustZone), up to 2 MB flash and 640 KB SRAM.
- Neither has AES; the H573 adds AES / PKA / OTFDEC.
- **The H562 has no Ethernet MAC** (ST AN5688: "without Ethernet"); the H563 has 10/100 Ethernet.
- FDCAN: ST lists two FDCANs on the H562 (H562IG page); Zephyr's `stm32h562.dtsi` defines only `fdcan1`, so a second port would need a devicetree overlay. One port is enough for the Fieldbus controller.

Sources: AN5959 — https://www.st.com/resource/en/application_note/an5959-migrating-within-the-stm32h5-mcus-stmicroelectronics.pdf ; AN5688 — https://www.st.com.cn/resource/en/application_note/an5688-migrating-microcontroller-applications-from-stm32f427437-and-stm32f429439-to-stm32h573563-and-stm32h562-mcus-stmicroelectronics.pdf ; DS14258 — https://st.com/resource/en/datasheet/stm32h562vg.pdf ; STM32H562IG — https://www.st.com/en/microcontrollers-microprocessors/stm32h562ig.html

## Verdict

- **Cheapest fit: STM32C562VET6**, ≈ INR 212. It has 144 MHz, AES, FDCAN, LQFP100 and Zephyr (`nucleo_c562re`), and is in stock at ST. It saves ≈ 70–100 per unit against the C5A3 on the model without Ethernet.
  - If it is pin-compatible with the C5A3 in LQFP100, the same MCU card PCB takes it as a BOM variant. **To confirm in the datasheet pinouts.**
  - Limits: 128 KB RAM and 512 KB flash, enough without a TCP/IP stack, to be sized. One FDCAN (two on the C5A3).
- **Best H5 without Ethernet: STM32H523VET6 / H533VET6.**
  - 250 MHz, 2 × FDCAN, 272 KB RAM, Zephyr.
  - H523 ≈ INR 300–375. The H533 (≈ 380–450) adds AES and holds a PSA L3 certificate, but Zephyr has no TF-M board for it.
  - Fits the H5 MCU card (same pins as H563 / H573, AN5959; corrected above), not the C5 card.
- **STM32H562** (1–2 MB, 1 × FDCAN, no AES) ≈ INR 375–450: no gain over the H523 for this use.
- **STM32H503**: out (64 pins max, 32 KB RAM).
- **Supply flag:** the STM32C5A3VGT6 itself is thin right now: DigiKey 0 (90 due 29-Jan-2027, 52-week lead time), ST eStore out of stock, TME 1. Its stock was better on 2026-11-22. The C562 is in stock at ST. Secure STM32C5A3 supply through ST India / distributors before the pilot.

## Comparison (prices ESTIMATE, INR at 100, 93.9 per USD)

| Part | Core | Flash / RAM | CAN | Crypto | Zephyr | ≈ INR at 100 | Stock (2026-11-26) |
|---|---|---|---|---|---|---|---|
| **STM32C562VET6** | M33 144 MHz | 512 KB / 128 KB | FDCAN (ST: "FDCAN"; C5A3: "Dual FDCAN") | AES (`stm32c5_crypt.dtsi`), HASH, RNG | Yes: `nucleo_c562re` | **≈ 212** (ST eStore USD 2.26 at 100–249) | ST eStore in stock |
| STM32C5A3VGT6 (current card) | M33 144 MHz, Ethernet | 1 MB / 256 KB | 2 × FDCAN | AES, HASH, RNG | Yes: `nucleo_c5a3zg` | ≈ 280–315 (TME USD 2.96 at 90; DigiKey USD 3.36 at 540) | **Thin:** DigiKey 0 (52 wk), ST out, TME 1 |
| STM32C593VGT6 | M33 144 MHz | 1 MB / 256 KB | 2 × FDCAN | to confirm | SoC file `stm32c593.dtsi` | not priced | ST out of stock |
| **STM32H523VET6** | M33 250 MHz | 512 KB / 272 KB | 2 × FDCAN | HASH, RNG; no AES | Yes: SoC file; board `nucleo_h533re` (same die + crypto) | ≈ 300–375 (DigiKey / Mouser); LCSC ≈ 575 | Mouser 1,259; DigiKey intermittent |
| STM32H533VET6 | M33 250 MHz, TrustZone | 512 KB / 272 KB | 2 × FDCAN | AES (`stm32h5_crypt.dtsi`); PSA L3 certificate | Yes: `nucleo_h533re`; no TF-M board | ≈ 380–450 | DigiKey 184, 15-week lead time |
| STM32H562VGT6 / VIT6 | M33 250 MHz, TrustZone | 1–2 MB / 640 KB | 1 × FDCAN | HASH, RNG; no AES | Yes: SoC file | ≈ 375–450 | Arrow 6,916 (VGT6); DigiKey 52-week lead time |
| STM32H503RBT6 | M33 250 MHz | 128 KB / 32 KB | FDCAN | — | Yes: `nucleo_h503rb` | — (ST: 80+ "contact sales") | ST in stock |

Not confirmed: C562 FDCAN count and pin compatibility with the C5A3 (datasheet pinouts); C593 crypto and price (the ST C5 series page timed out); every price above is from search snapshots or model-extracted store pages, so recheck before quoting.

## Sources

- ST eStore — https://estore.st.com/en/stm32c562vet6-cpn.html ; https://estore.st.com/en/stm32c5a3vgt6-cpn.html ; https://estore.st.com/en/stm32h503rbt6-cpn.html
- ST product pages — https://www.st.com/en/microcontrollers-microprocessors/stm32c562ve.html ; https://www.st.com/en/microcontrollers-microprocessors/stm32c5a3vg.html
- STM32C5A3VGT6 — DigiKey https://www.digikey.com/en/products/detail/stmicroelectronics/STM32C5A3VGT6/29285829 ; TME https://www.tme.com/us/en-us/details/stm32c5a3vgt6/st-microcontrollers/stmicroelectronics/ ; RS https://uk.rs-online.com/web/p/microcontrollers/0800448
- STM32H523VET6 — LCSC https://www.lcsc.com/product-detail/C27338462.html ; Octopart https://octopart.com/part/stmicroelectronics/STM32H523VET6 ; DigiKey UK https://www.digikey.co.uk/en/products/detail/stmicroelectronics/STM32H523VET6/22519682
- STM32H533VET6 — DigiKey CA https://www.digikey.ca/en/products/detail/stmicroelectronics/STM32H533VET6/22519649
- STM32H562 — LCSC https://www.lcsc.com/product-detail/C22452133.html ; Arrow https://www.arrow.com/en/products/stm32h562vgt6/stmicroelectronics ; DigiKey https://www.digikey.com/en/products/detail/stmicroelectronics/STM32H562VIT6/21348980
- Zephyr main: `dts/arm/st/h5/stm32h503.dtsi`, `stm32h523.dtsi`, `stm32h533.dtsi`, `stm32h562.dtsi`; `dts/arm/st/c5/stm32c562.dtsi`, `stm32c593.dtsi`; boards `nucleo_h503rb`, `nucleo_h533re`, `nucleo_c562re`, `nucleo_c542rc` — https://github.com/zephyrproject-rtos/zephyr/tree/main/boards/st

## Update 2026-11-26 — cost-optimised C5 parts in stock (owner: "search for more cost optimised versions of c5 for non ethernet ic that are in stock")

Rules now: ≥ 512 KB flash, ≥ 256 KB RAM (BASE-10 update 9), FDCAN, LQFP100.

C5 line-up, from ST's series page and the STM32C59x / C5A3 datasheet:
- 256 KB RAM only in the C59x / C5A3 lines.
- **C591:** no FDCAN, no Ethernet. Fails CAN.
- **C593:** 1 MB / 256 KB, 2 × FDCAN and Ethernet. Crypto is only SHA2-512 and PKA verify: no AES, no SAES, no HUK.
- **C5A3:** the C593 plus AES / SAES / HUK. Zephyr's `stm32c5a3.dtsi` is `stm32c593.dtsi` + `stm32c5_crypt.dtsi`, so the C593 is very likely a drop-in on the C5A3 card. Confirm the pinout in the datasheet.
- C55x / C56x (and smaller): 128 KB RAM. Fail the RAM rule.

| Part | Flash / RAM | FDCAN | Crypto | ≈ INR at 100 | Stock (2026-11-26) | Meets rules |
|---|---|---|---|---|---|---|
| STM32C5A3VGT6 | 1 MB / 256 KB | 2 | AES, SAES, HUK, PKA | ≈ 280–315 | Thin (DigiKey 0, ST out, TME 1) | Yes |
| **STM32C593VGT6** | 1 MB / 256 KB | 2 | SHA2, PKA verify | not published | **Not in stock anywhere found** (ST eStore out; no distributor listing) | Yes — the only cheaper C5 that does |
| STM32C591 | 1 MB / 256 KB | 0 | — | — | — | No (no CAN) |
| STM32C562VET6 | 512 KB / 128 KB | 1+ | AES | ≈ 212 | DigiKey 145; ST in stock | No (RAM) |
| STM32C552VET6 | 512 KB / 128 KB | yes | — | ≈ 155–165 (ST USD 1.67 at 250–500) | DigiKey 345; ST in stock | No (RAM) |
| STM32C551VET6 | 512 KB / 128 KB | — | — | ≈ 150 | DigiKey 27 | No (RAM, CAN) |

Conclusion:
- No cost-optimised C5 that meets the 256 KB RAM rule is in stock today.
- The C593 is the one to watch: a likely drop-in on the C5A3 card without AES. Software AES is fine for MQTT / TLS rates on the model without Ethernet; that model still ends TLS when it is the coordinator behind the 4G card (SEC-8).
- The in-stock cheap C5 parts (C552 ≈ 160, C562 ≈ 212) all have 128 KB RAM.

Sources: ST STM32C5 series — https://www.st.com/en/microcontrollers-microprocessors/stm32c5-series.html ; products list — https://www.st.com/en/microcontrollers-microprocessors/stm32c5-series/products.html ; STM32C59x / 5A3 — https://www.st.com/en/microcontrollers-microprocessors/stm32c59x-5a3/products.html ; datasheet — https://www.st.com/resource/en/datasheet/stm32c591cg.pdf ; ST C5 training — https://www.st.com/content/ccc/resource/training/technical/product_training/group1/dd/a8/7b/67/4d/f3/4f/85/stm32c5-series-introduction/files/stm32c5-series-introduction.pdf/jcr:content/translations/en.stm32c5-series-introduction.pdf ; DigiKey C552VET6 — https://www.digikey.com/en/products/detail/stmicroelectronics/STM32C552VET6/28948240 ; C562VET6 — https://www.digikey.com/en/products/detail/stmicroelectronics/STM32C562VET6/28948247 ; C551VET6 — https://www.digikey.com/en/products/detail/stmicroelectronics/STM32C551VET6/28948244 ; ST eStore C552VET6 — https://estore.st.com/en/stm32c552vet6-cpn.html
