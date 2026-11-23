# R25 — Fieldbus controller MCU at ≥ 250 MHz: NXP MCX check and alternatives

Status: desk check, 2026-11-22. No prices (owner rule COST-6: no online prices).

Owner requests, 2026-11-22: "check for MCX Industrial and IoT Microcontrollers"; "need 250 mhz and above for fieldbus". Context: the MCU now sits on a removable control card (BASE-11) because MCU sourcing is unstable.

## Requirement set for the control-card MCU

≥ 250 MHz (owner) · on-chip Ethernet MAC, RMII (BASE-9, never SPI Ethernet) · CAN-FD, 2 preferred (FB-1) · ≥ 4 UART · ≥ 10 ADC inputs (6 AI + 4 current sense) · TrustZone with certified key storage, PSA L3 / SESIP3 target (BASE-1) · ≥ 2 MB flash, ≥ 512 KB RAM (R09) · LQFP ≤ 144 pins, no fine-pitch BGA (MFG-1) · Zephyr support (FW-1) · ≥ 5-year longevity · −40…85 °C.

## NXP MCX family against the requirement

| Series | Core, max clock | Ethernet | CAN-FD | Non-BGA package | Security | Status | Verdict |
|---|---|---|---|---|---|---|---|
| MCX N94x / N54x (MCXN947, N946, N547, N546) | 2× Cortex-M33, 150 MHz | 1× ENET with QoS | 2× FlexCAN FD | HLQFP100 (78 GPIO on N947) — "preliminary, pending qualification" in our datasheet copy; no USB HS in HLQFP100 | TrustZone, EdgeLock S50 secure enclave (ELS), secure boot ROM; 2 tamper pins on HLQFP100 | In production (VFBGA184) | **Fails: 150 MHz** |
| MCX N24 | 1× Cortex-M33, 150 MHz | yes | yes | — | — | — | **Fails: 150 MHz** |
| MCX N23 | 1× Cortex-M33, 150 MHz | no | yes | — | — | — | Fails: clock, no Ethernet |
| **MCX A5 (MCXA577 …)** | Cortex-M33, **240 MHz** | ENET + 10BASE-T1S PHY (MCXA557 has none) | yes | LQFP100, LQFP144 listed | EdgeLock accelerator, secure boot with PQC hybrid, secure debug, external-flash encryption, tamper monitors; no PSA / SESIP certificate found | **Sampling; general availability expected Q4 2026, not confirmed**; FRDM board not yet seen | **Near miss: 240 MHz; brand new** |
| MCX A14x / A15x | Cortex-M33, 48–96 MHz | no | some | — | — | — | Fails |
| MCX W, L, E | wireless (W), 96 MHz low power (L) | no | — | — | — | — | Fails |

**No MCX part reaches 250 MHz.** The MCX A5 at 240 MHz is the only near miss (−4 % clock, same Cortex-M33 core as the STM32H573), and it is too new to count as a stable source today.

## Other ≥ 250 MHz parts with Ethernet + CAN-FD

| Part | Core, clock | Ethernet | CAN-FD | Package | Security | Verdict |
|---|---|---|---|---|---|---|
| **ST STM32H573VIT6** | Cortex-M33, 250 MHz | yes | 2 | LQFP100 | TrustZone, PSA L3 / SESIP3 | **Meets everything**; sourcing was the problem (D-17) |
| ST STM32H563VIT6 | Cortex-M33, 250 MHz | yes | 2 | LQFP100 | TrustZone, no crypto accelerators | Meets except hardware crypto / PSA L3 |
| ST STM32H723 / H743 / H753 | Cortex-M7, 550 / 480 MHz | yes | 3 / 2 | LQFP100 | no TrustZone (M7) | Fails BASE-1; same vendor as H573 |
| **Renesas RA8M1** | Cortex-M85, 480 MHz | yes | 2 | LQFP100 / 144 / 176 | TrustZone, PSA L3 / SESIP3 (R12) | Meets; outside the preferred vendors (COMP-1) |
| **Renesas RA8E1** | Cortex-M85, 360 MHz | yes | 2 | LQFP100 / 144 | TrustZone (certification level to check) | Meets clock; outside the preferred vendors |
| NXP i.MX RT1040 | Cortex-M7, 600 MHz | yes | 1 FD + 2 classic | LFBGA169, 0.65 mm only | no TrustZone | Fails MFG-1 (fine-pitch BGA) |
| NXP i.MX RT1024 | Cortex-M7, 500 MHz | yes | classic CAN only (to verify) | LQFP100 | no TrustZone | Fails CAN-FD |
| Microchip PIC32CK2051SG01100 (current standard) | Cortex-M33, **120 MHz** | yes | 2 | TQFP100 | HSM + TrustZone, no certificate | **Fails: 120 MHz** |
| Microchip SAM E70 (from memory) | Cortex-M7, 300 MHz | yes | 2 MCAN | LQFP100 | no TrustZone | Fails BASE-1; Microchip is fallback-only |

RA8M1 / RA8E1 facts from the datasheets on file (`datasheets/mcu_security/`); MCX N facts from `NXP_MCXN947_datasheet.pdf`; STM32 facts from R08 / R11 / R12.

## Conclusions

1. The 250 MHz rule removes the PIC32CK (120 MHz) and every MCX part.
2. Within ST / NXP / Nordic, only the **STM32H573VIT6** meets 250 MHz + Ethernet + CAN-FD + LQFP100 + PSA L3. It goes back to being the main control card.
3. A second control card needs one rule relaxed: **NXP MCX A5 at 240 MHz** (preferred vendor, but new and not yet confirmed in volume) or **Renesas RA8M1 / RA8E1** (≥ 360 MHz, in production, LQFP100, but outside the preferred vendors). STM32H7 is the same vendor and has no TrustZone, so it is a weak second source.
4. The control card (BASE-11) makes either choice a card swap, not a base-card redesign; each new card still needs its own Zephyr port, secure-boot set-up and EMC test.

## Update 2026-11-22 — speed rule lowered

Owner: "reducing speed requirement to 180mhz" / "or 150 mhz dual speed" / "also can consider rpi pico 2". New rule (BASE-10): ≥ 180 MHz on one core, or ≥ 150 MHz on each of two cores.

| Part | Clock | Verdict under the new rule |
|---|---|---|
| STM32H573VIT6 | 250 MHz | Qualifies — main card |
| **NXP MCX N94x (MCXN947, HLQFP100)** | 2 × 150 MHz | **Qualifies — proposed second card**: preferred vendor, in production, mature Zephyr, Ethernet + 2× CAN-FD + 16-bit ADC + EdgeLock + NPU; no PSA / SESIP certificate found; HLQFP100 ordering code to confirm (VKLT per R11) |
| NXP MCX A5 | 240 MHz | Qualifies on clock; new (sampling), keep for later |
| Renesas RA8M1 / RA8E1 / RA6M5 | 480 / 360 / 200 MHz | Qualify on clock; outside the preferred vendors |
| Microchip PIC32CK | 120 MHz | Out (clock, Zephyr drivers) |
| Raspberry Pi RP2350 (Pico 2) | 2 × 150 MHz (Cortex-M33 or Hazard3 RISC-V) | Out: no Ethernet MAC (SPI Ethernet banned), no CAN / CAN-FD, 4 ADC inputs (QFN-60) or 8 (QFN-80), external QSPI flash; Zephyr supports it and TrustZone + secure boot are present |

## Update 2026-11-22 — Zephyr check and ESP32-S31

Owner: "check for nxp stm, rpi" / "what about esp32s31" / "is there a zephyr port for it". Zephyr support is a must (FW-1).

Zephyr main branch, read from the GitHub API on 2026-11-22:
- Espressif SoCs: esp32, esp32c2, esp32c3, esp32c5, esp32c6, esp32c61, esp32h2, esp32p4, esp32s2, esp32s3 — **no esp32s31**.
- Boards for our candidates: `stm32h573i_dk`, `nucleo_h563zi` (ST H5); `nucleo_h723zg`, `nucleo_h743zi`, `nucleo_h753zi`, `nucleo_h7s3l8`, `stm32h7s78_dk` (ST H7); `frdm_mcxn947`, `frdm_mcxa577` (NXP MCX N, MCX A5); `mimxrt1020_evk`, `mimxrt1024_evk`, `mimxrt1040_evk` (NXP RT); `ek_ra8m1`, `fpb_ra8e1`, `ek_ra6m5` (Renesas); `rpi_pico`, `rpi_pico2` (Raspberry Pi). A board in the tree does not prove every peripheral we use (Ethernet, CAN-FD, ADC) is supported on it — confirm per board before layout.

| Part | Clock | Ethernet MAC | CAN-FD | Zephyr board | Package | TrustZone | Verdict |
|---|---|---|---|---|---|---|---|
| ST STM32H573VIT6 | 250 MHz | yes | 2 | yes | LQFP100 | yes, PSA L3 | **Main card** |
| NXP MCXN947 | 2 × 150 MHz | yes | 2 | yes | HLQFP100 | yes, EdgeLock | **Second card** |
| NXP MCX A5 (MCXA577) | 240 MHz | yes | yes | yes (new) | LQFP100 / 144 | EdgeLock, PQC boot | Later (new silicon) |
| ST STM32H7 (H723 / H743 / H753 / H7S3) | 480–600 MHz | yes | yes | yes | LQFP100 | no | Partial (no TrustZone); same vendor as main |
| Renesas RA8M1 / RA8E1 / RA6M5 | 480 / 360 / 200 MHz | yes | 2 | yes | LQFP100 | yes | Outside preferred vendors |
| Raspberry Pi RP2350 (Pico 2) | 2 × 150 MHz | no | no | yes | QFN-60 / 80 | yes | Out |
| Espressif ESP32-S31 | 2 × 320 MHz (RISC-V) | yes, 1 Gb | yes | **no** | QFN80 8 × 8 mm | no | Out: no Zephyr port, pre-release (datasheet v0.5), Espressif tolerated only for Wi-Fi + BLE |

## Update 2026-11-22 — MCU below INR 500

Owner: "MCXN947VKLT is very costly need mcu below 500 rs". Prices come from the owner's local quotes (COST-6); this list only says which parts meet the technical rules.

Zephyr main branch SoC list (`soc/nxp/mcx/soc.yml`, 2026-11-22): MCX N — mcxn947, mcxn946, mcxn547, mcxn546, mcxn236, mcxn235; MCX A — including mcxa577, mcxa567, mcxa557, mcxa537 (and 6-suffix variants), mcxa457, mcxa287. **MCX N52x / N53x are not in the list.**

| Part | Clock | Ethernet | CAN-FD | Package | Zephyr SoC | Note |
|---|---|---|---|---|---|---|
| NXP MCXA577VLL (MCX A5) | 180–240 MHz (Keil lists 180 MHz for VLL; NXP 240 MHz) | yes, + 10BASE-T1S | yes | LQFP100 | yes | Cost-optimised MCX A line; new silicon (sampling, GA expected Q4 2026) |
| NXP MCXN546 / MCXN547 | 2 × 150 MHz | yes | 1 | HLQFP100 | yes | 1 MB / 2 MB flash; N54x HLQFP100 pinout differs from N94x |
| NXP MCXN946 | 2 × 150 MHz | yes | 2 | HLQFP100 | yes | 1 MB flash |
| ST STM32H563VIT6 / VGT6 | 250 MHz | yes | 2 | LQFP100 | yes | No hardware crypto (PSA L3 lost); 2 MB / 1 MB |
| ST STM32H573VIT6 | 250 MHz | yes | 2 | LQFP100 | yes | PSA L3 |
| NXP MCXN526 / MCXN536 (MCX N52x / N53x) | 2 × 150 MHz | yes | 2 | HLQFP100 | **no** | Out until Zephyr adds them |
| NXP MCXA557 | 240 MHz | **no** | **no** | — | yes | Out (no Ethernet, no CAN-FD) |

## Sources

- NXP MCX N94x / N54x datasheet (local copy, `datasheets/mcu_security/NXP_MCXN947_datasheet.pdf`)
- NXP MCX N series highlights — https://www.nxp.com/docs/en/brochure/MCX-N-Series-Highlights.pdf
- NXP MCX N94 / N54 / N53 / N52 / N24 — https://www.nxp.com/products/MCX-N94-N54-N53-N52-N24
- NXP MCX A5 series — https://www.nxp.com/products/MCX-A5 ; fact sheet https://www.nxp.com/docs/en/fact-sheet/MCXA5FS.pdf
- CNX Software, MCX A5 announcement (2026-08-19) — https://www.cnx-software.com/2026/08/19/nxp-mcx-a5-cortex-m33-mcu-family-supports-10base-t1s-single-pair-ethernet-and-post-quantum-cryptography/
- Embedded.com, MCX A5 — https://www.embedded.com/nxp-mcx-a5-mcus-bring-10base-t1s-ethernet-to-industrial-edge-nodes/
- Microchip PIC32CK SG/GC (120 MHz) — https://www.microchip.com/en-us/products/microcontrollers-and-microprocessors/32-bit-mcus/pic32-32-bit-mcus/pic32ck-sg-gc
- NXP i.MX RT1040 — https://www.nxp.com/products/processors-and-microcontrollers/arm-microcontrollers/i-mx-rt-crossover-mcus/i-mx-rt1040-crossover-mcu-with-arm-cortex-m7-core:i.MX-RT1040
- Renesas RA8M1 / RA8E1 datasheets (local copies, `datasheets/mcu_security/`)
- Espressif ESP32-S31 datasheet, pre-release v0.5 (local copy, `datasheets/ethernet/`)
- Zephyr main branch, `soc/espressif` and `boards/*` — https://github.com/zephyrproject-rtos/zephyr
- Espressif Zephyr support status — https://developer.espressif.com/software/zephyr-support-status/
- Zephyr MCX SoC list — https://github.com/zephyrproject-rtos/zephyr/blob/main/soc/nxp/mcx/soc.yml
- NXP MCX N fact sheet — https://www.nxp.com/docs/en/fact-sheet/MCXNFS.pdf ; MCX N94 / N54 / N53 / N52 / N24 block diagram — https://www.nxp.com/assets/block-diagram/en/MCX-N94-N54-N53-N52-N24.pdf
- Arm Keil device pages: MCXN526VKL, MCXN536VAB, MCXA577VLL / VLQ / VPN — https://www.keil.arm.com/devices/
- Zephyr FRDM-MCXA577 board — https://docs.zephyrproject.org/latest/boards/nxp/frdm_mcxa577/doc/index.html
