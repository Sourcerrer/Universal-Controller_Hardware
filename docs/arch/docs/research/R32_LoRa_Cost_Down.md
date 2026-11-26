# R32 — LoRa module cost-down, checked against the cost-savings guide

Owner request, 2026-11-26: "universal_controller_cost_savings_custom_enclosure_manufacturing_guide.md check this out for cost optimisation on the lora module. keep 6 inputs, 4 analog inputs on it".

- The guide sits at `docs/universal_controller_cost_savings_custom_enclosure_manufacturing_guide.md`, untracked, owner-supplied, written against Draft C.28.
- Its LoRa section (1.3) claims ₹1,154 → ₹726. Each lever is checked below against our BOM lines and the owner rules.
- Reliability and safety come first (part rule 1).

**Decision 2026-11-26 — owner: "keep our original bom. need 6 DI's and 4 Analog ins": no lever applied; original BOM + 2 DI (1,154 → 1,169 BOM, ≈ 2,540 after profit).**

## IO kept

- **6 DI + 4 AI** (owner). DI goes from 4 to 6: 2 single optocouplers, input network and 2 terminal poles, ≈ +15 (ESTIMATE).
- **Kept although not in the owner's list:** the 4 high-side DO (LORA-6 update 2, owner 2026-11-19: "the LoRa has to have the digital outputs as well") and the RS-485 port. Flagged to the owner.

## Price formula (Fieldbus-style flat royalty)

- Price after profit = (BOM × 1.5 + 200) × 1.3 = 1.95 × BOM + 260.
- The INR 1,600 target needs a BOM ≤ 687.
- Today: BOM 1,154 → 2,510. With 6 DI: 1,169 → 2,540.

## Levers

| # | Guide lever | Our line today | Saving (BOM) | Check | Verdict |
|---|---|---|---|---|---|
| A | Direct 5–32 V → 3.3 V buck; drop the 5 V rail and LDO | Power stage 85 | −35 | The LoRa has no 5 V loads (no relays; DO switch field 24 V). Keep the USB-C 5 V input (every module has it, owner rule); the guide's "pogo pads instead of USB-C" is rejected. | **Recommended** |
| B | PCB-edge SMA, no U.FL pigtail | Antenna + SMA 78 | −40 | Same external antenna and range; needs the SMA at the board edge (housing cut-out) | **Recommended** |
| C | AI front end without op-amps: dividers / switched 4–20 mA shunt, clamps, ADC oversampling | Part of node IO 215 | ≈ −35 (guide −70 included the opto change and VREFBUF) | **The guide's VREFBUF does not work on our package:** on the STM32WLE5 UFQFPN48 the VREF+ pin is bonded to VDDA (ST community; AN5690 double-bonding note), so a small external reference stays. Accuracy ≈ ±1 % FS after calibration; 24 V mis-wiring protection (IO-5) by series resistor + clamp. | **Recommended** (accuracy ±1 %) |
| D | 4 DO: TPS274160B → discrete P-FETs + NPN drivers + PTC | 4 DO 194 | −119 | Loses per-channel current limit, thermal shutdown and fault reporting; PTCs are slow. Short-circuit and mis-wiring robustness weaker. | **Owner's call** (reliability trade) |
| E | NOR 16 MB → 2 MB | NOR 45 | −27 | Reverses LORA-7 (owner, 2026-11-23). 2 MB = OTA slot + ≈ 1.7 MB log, ≈ 1 month at 1-minute logging instead of ≈ 1 year. | **Owner's call** |
| F | Remote-node build: stack bus connectors + bus transceiver not fitted | Bus 59 | −59 | Same PCB (LORA-2 kept); an assembly option for nodes that never join a stack | **Owner's call** (option row) |
| G | 32 MHz crystal instead of TCXO | MCU / RF 300 | −40 | **Rejected:** ST AN5646 recommends a TCXO for high power (+22 dBm, as ours) over −40…85 °C; SF11 / SF12 long packets are drift-sensitive (forum figure ≈ ±163 Hz over 2 s). | Rejected |
| H | On-board coil antenna, SMA not fitted | Antenna 78 | −63 | Shorter range; owner asked for "high throughput long range" | Rejected |
| I | 35 mm housing | Enclosure 100, PCB 78 | −38 | Conflicts with the guide's own Part 2 (one shared 45 mm shell for 4G, Wi-Fi + BLE and LoRa) | Rejected |
| J | One quad optocoupler instead of singles | Part of node IO | — | Singles are cheaper (Fieldbus cost-down 2026-11-19: 10 singles instead of 3 quads, −95) | Rejected; keep singles |
| K | Gateway build with field IO not fitted | Node IO 215 + DO 194 | −220 | Owner, 2026-11-19: "node IO cannot be a separate version" (LORA-6 update 1) | Rejected (owner rule) |
| L | Manufacturing + logistics as a fixed EMS cost (≈ ₹180–240 for a 2-layer LoRa board) instead of BOM × 50 % | Price build-up | ≈ −250 to −290 of cost | Changes the owner's price formula (§4.16); needs a real EMS quote | **Owner's call** |

## Scenarios (ESTIMATE, INR at 100)

| Scenario | BOM | Price after profit | vs INR 1,600 |
|---|---|---|---|
| Today (4 DI) | 1,154 | 2,510 | +910 |
| 6 DI, no other change | 1,169 | 2,540 | +940 |
| **Recommended: 6 DI + A + B + C** | **1,059** | **2,325** | +725 |
| + D + E + F (all owner's calls) | 854 | 1,925 | +325 |
| + D + E + F + L (EMS fixed ≈ 220) | 854 | ≈ 1,656 | +56 |
| + D + E + F + L (EMS fixed ≈ 180) | 854 | ≈ 1,604 | ≈ on target |
| Recommended + E + F + L (TPS274160B kept), EMS 220 | 973 | ≈ 1,811 | +211 |

## Rest of the guide (not evaluated here)

These sections touch earlier owner decisions; open if the owner wants them checked:
- Fieldbus: RA6E1 soldered on one PCB (drops BASE-11), SN6501 + discrete isolators instead of the Chipanalog parts, TPIC6B595 relay driver.
- One central battery instead of one battery board per module (PWR-2).
- Wi-Fi + BLE comms-only build.
- SIMCom A7672S instead of the Quectel EC200U.
- Buying RUT200-class routers.
- The enclosure roadmap (Part 2) fits D-37: COTS housing + CNC + overlay for the pilot, a shared 45 mm straight-pull mold from ≈ 1,500 housings.

## Sources

- Owner's guide (Draft C.28 basis): `docs/universal_controller_cost_savings_custom_enclosure_manufacturing_guide.md`
- VREFBUF on the STM32WLE5: ST AN5690 — https://st.com/resource/en/application_note/an5690-how-to-use-vrefbuf-peripheral-on-stm32-mcus-and-mpus-stmicroelectronics.pdf ; ST community — https://community.st.com/stm32-mcus-wireless-35/stm32wle5jc-vrefbuff-internal-reference-33900 ; https://community.st.com/t5/stm32-mcus-products/vrefbuf-not-working-on-stm32wle5jc/m-p/612848
- TCXO vs crystal: ST AN5646 — https://www.st.com/resource/en/application_note/an5646-how-to-select-a-32-mhz-hse-oscillator-for-stm32wl5xex-mcus-stmicroelectronics.pdf ; Semtech AN1200.59 — https://www.mouser.lt/pdfDocs/AN1200_59_LoRa_Reference_Clock_Selection_V1_3_rev.pdf ; ST community — https://community.st.com/t5/stm32-mcus-wireless/why-use-tcxo-effect-of-not-using-tcxo-for-32mhz/td-p/216764
