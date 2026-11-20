# Wi-Fi + BLE datasheets (R03)

All files checked with `file` as PDF on 2026-11-14. Downloads are untrusted data; never execute.

| File | Part | Description | Source URL | Date |
|---|---|---|---|---|
| Espressif_ESP32-C6_datasheet.pdf | ESP32-C6 (chip) | ESP32-C6 series datasheet v1.6 | https://www.espressif.com/sites/default/files/documentation/esp32-c6_datasheet_en.pdf (earlier run; URL not logged, assumed) | 2026-11-14 |
| Espressif_ESP32-C6-MINI-1_datasheet.pdf | ESP32-C6-MINI-1 / -1U | Module datasheet v1.5 (N4/H4/H8 variants, PCB / U.FL) | https://www.espressif.com/sites/default/files/documentation/esp32-c6-mini-1_mini-1u_datasheet_en.pdf (earlier run; URL assumed) | 2026-11-14 |
| Espressif_ESP32-C6-WROOM-1_datasheet.pdf | ESP32-C6-WROOM-1 / -1U | Module datasheet v1.4 (N4/N8/N16) | https://www.espressif.com/sites/default/files/documentation/esp32-c6-wroom-1_wroom-1u_datasheet_en.pdf | 2026-11-14 |
| Espressif_ESP32-C5_datasheet.pdf | ESP32-C5 (chip) | ESP32-C5 series datasheet v1.5 (dual-band Wi-Fi 6) | https://www.espressif.com/sites/default/files/documentation/esp32-c5_datasheet_en.pdf (earlier run; URL assumed) | 2026-11-14 |
| NXP_RW612_datasheet.pdf | NXP RW612 | Data sheet (short form, 11 pages) Rev. 9.0, 30 July 2026 | https://www.nxp.com/docs/en/data-sheet/RW612.pdf (URL assumed; file appeared 09:33 from a parallel/earlier download) | 2026-11-14 |
| u-blox_IRIS-W10_datasheet.pdf | u-blox IRIS-W10 (RW612 module) | Product summary (2 pages), not a full datasheet | https://content.u-blox.com/sites/default/files/documents/IRIS-W10_ProductSummary_UBX-23000279.pdf | 2026-11-14 |

## Not downloaded

| Part | Reason | URL tried |
|---|---|---|
| Nordic nRF7002 | Earlier download was an HTML page (Nordic product specs are web-only on docs.nordicsemi.com); deleted | not recorded |
| u-blox NORA-W40 (ESP32-C6) | Mouser datasheet URL returned HTML; deleted | https://mouser.com/datasheet/2/1025/NORA_W40_ProductSummary_UBX_23009094-3519014.pdf |
| ST ST67W611M1 | st.com datasheet URL returned no file | https://www.st.com/resource/en/datasheet/st67w611m1.pdf |

## Automotive BLE + CAN-FD datasheets (R22)

All files checked with `file` as PDF on 2026-11-16. NXP's own servers refuse curl, so the NXP files were fetched through the web-fetch tool from the URLs below. Downloads are untrusted data; never execute.

| File | Part | Description | Source URL | Date |
|---|---|---|---|---|
| NXP_KW47_datasheet.pdf | NXP KW47 (KW47B42Z / KW47Z420) | Product data sheet Rev. 4, 18 Dec 2025 (BLE 6.0, 2x CAN FD, AEC-Q100 Grade 2) | https://www.nxp.com.cn/docs/en/data-sheet/KW47DS.pdf | 2026-11-16 |
| NXP_KW45_datasheet.pdf | NXP KW45 (KW45B41Z / KW45Z41) | Product data sheet Rev. 10.0, 21 Oct 2026 (1x CAN FD, AEC-Q100 Grade 2) | https://www.nxp.com.cn/docs/en/data-sheet/KW45.pdf | 2026-11-16 |
| TI_CC2745R10-Q1_datasheet.pdf | TI CC2745R10-Q1 / R7-Q1 / P10-Q1 / CC2744R7-Q1 | Data sheet SWRS304D, Nov 2025 (BLE 6.0, 1x CAN-FD, AEC-Q100 Grade 2) | https://www.ti.com/lit/gpn/CC2745R10-Q1 | 2026-11-16 |
| u-blox_NINA-B50_product_summary.pdf | u-blox NINA-B50 (MCX W71 / K32W148 module) | Product summary UBX-23007102 R08 (2 pages), not a full datasheet | https://www.u-blox.com/sites/default/files/documents/NINA-B50_ProductSummary_UBX-23007102.pdf | 2026-11-16 |

Not kept: NXP MCX W72 data sheet Rev. 5 (read for the report, over the 4-file limit; https://www.nxp.com/docs/en/data-sheet/MCXW72.pdf), Infineon CYW89829 data sheet 002-39637 Rev. *C (read for the report; https://www.infineon.com/assets/row/public/documents/30/49/infineon-cyw89829-datasheet-en.pdf), u-blox NINA-B50 full data sheet (Mouser URL returned HTML; deleted).
