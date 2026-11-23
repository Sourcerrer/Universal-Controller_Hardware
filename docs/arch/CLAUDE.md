# Universal Controller (UC) — hardware architecture

Working rules for Claude in `hardware/docs/arch/`. The owner is a hardware product lead who thinks in INR and lean, single-chip, cost-targeted designs.

## What the product is

A modular industrial IoT gateway in the style of a stackable PLC: individually enclosed modules click together side by side on one identical **4-pin** bus connector (BUS_V, GND, RS485_A, RS485_B; SYS-11, MECH-3; the 40-pin connector was dropped on 2026-11-16), with publish–subscribe messaging over the RS-485 pair (SYS-12). Every module is also a standalone product (remote node) with its own 5–32 V DC / USB-C PD input; one battery board backs up a whole gateway.

There are exactly **four modules**:

| Module | Role |
|---|---|
| Fieldbus controller (formerly baseboard / IO controller; optional) | Coordinator: IO image, keys (PSA L3), routing, updates. Standalone: RS-485 / CAN-FD controller and logger |
| 4G modem card (4G + Ethernet + Wi-Fi) | Cloud uplink |
| Wi-Fi + BLE | Low-cost uplink and local BLE access |
| LoRa | Gateway side and remote node (same hardware) |

Every module also carries one **power module** (PWR-10): a standalone plug-in PCB, priced as its own item. One 12 V 18 W adapter per gateway or standalone module, also priced separately. Options only: Fieldbus controller without Ethernet, PIC32CK fallback MCU, 4G modem card without Ethernet, Tier 0 4G, GNSS, battery board (PWR-2, one per gateway).

## Source of truth

- **`docs/01_Requirements_PRD.md` is the single requirements document.** Every new or changed requirement goes there with an ID (and Src O = owner / P = proposed). Never create a separate requirements file. Check its section 6 (open decisions) before assuming anything is settled.
- The PRD overrides this file and any memory if they disagree. When the owner changes a rule, update the PRD first, then the generators, then the deliverables.

## Order of work

PRD → specifications (`docs/02_Specifications.md`, not written yet) → architecture diagram → schematics, BOM, PCB, Gerbers in KiCad (KiCad MCP tools, driven by the same diagram). Don't skip ahead on your own, but follow the owner when they ask out of order.

## Folder layout

The root of `hardware/docs/arch/` holds **finished deliverables only**:

- `UC_Architecture.pdf`, `UC_Specsheet.pdf`, `UC_Overview.pptx` (the owner's single deck), `images/UC_3D_*.png` (the client video `UC_Architecture_Video.mp4` lives in `../specs/`)
- No SVGs, scripts or tool folders in the root (owner objected).

Everything else lives in `docs/`:

| Path | Contents |
|---|---|
| `docs/01_Requirements_PRD.md` | Requirements, cost targets, vendor and RTOS rules |
| `docs/research/Rnn_*.md` | Trade studies (R01–R22 so far); continue the numbering |
| `docs/datasheets/<category>/` | **All** datasheets, by category (cellular, connectors, ethernet, industrial, io_frontend, linux_soc, lora, mcu_security, power, standards, wifi_ble) |
| `docs/bom/` | BOM CSVs |
| `docs/diagram/` | `build_architecture.py` → per-page SVGs; `print_architecture.html` combines them into the PDF |
| `docs/specsheet/UC_Specsheet.html` | Source of `UC_Specsheet.pdf` |
| `docs/deck/` | `build_deck.js` + `cost.json` → `UC_Overview.pptx` |
| `docs/video/` | `build_video.py` (MP4) and `render_3d.py` (3D PNGs) |

## Rebuilding deliverables

- **Diagram:** `python3 docs/diagram/build_architecture.py docs/diagram` writes the page SVGs; then print `docs/diagram/print_architecture.html` to PDF with headless Chrome (`google-chrome --headless --print-to-pdf=../../UC_Architecture.pdf ...`, A3 landscape, no margins). Bump the `REV` string when content changes. Pages: 1 physical front view of the device · 2 IO sharing · 3 bus and power · 4 prices on one page (build-up per module, power module and adapter; options; all 15 combinations, each row showing its modules by name plus its power modules, a break-up bar, and every step to the price before and after profit; the owner approved this layout on 2026-11-19) · 5 BOM basis line items, the Fieldbus cost-down log and notes · 6 software and security · 7 Tier-2 router. When pages are added or renumbered, update `print_architecture.html` and delete the stale SVGs.
- **Specsheet:** print `docs/specsheet/UC_Specsheet.html` to PDF the same way.
- **Deck:** `build_architecture.py` also writes `docs/deck/cost.json` (100-unit prices), so rebuild the diagram first. Then, in a scratch dir:
  1. `npm install pptxgenjs@3.12.0`
  2. Render `arch_p1.png` from the page-1 SVG with headless Chrome (`--force-device-scale-factor=2 --window-size=1588,1123`).
  3. Copy a `video_cover.png` (for example `images/UC_3D_Stack.png`).
  4. Run `NODE_PATH=<scratch>/node_modules node docs/deck/build_deck.js <out.pptx> <hardware/docs/arch> <scratch>`.
- **Video / 3D:** `python3 docs/video/build_video.py <ffmpeg> <out.mp4>` and `python3 docs/video/render_3d.py images/`. No system ffmpeg or 3D software is installed: get ffmpeg from the `imageio-ffmpeg` pip package in a scratch venv. Renders are pure PIL.
- Keep scratch venvs, node_modules and temp files out of the project.

## Part selection rules (owner)

1. **Reliability and safety come first, ahead of cost.** If a cost target can't be met without weakening them, the target gives way and the gap is reported to the owner.
2. **Silicon:** ST, NXP, Nordic. ESP32-C6 is tolerated for Wi-Fi + BLE. Fieldbus controller: a 100-pin MCU with **Ethernet as standard**. Speed ≥ 144 MHz (owner, 2026-11-22); MCU chip below INR 500 at 100 units (owner, 2026-11-22). The MCU sits on a removable control card (BASE-11): STM32H573VIT6 main, NXP MCXN947 proposed as the second card (PRD D-38); the version without Ethernet was dropped on 2026-11-19. Ruled out: Microchip PIC32CK (120 MHz, no upstream Zephyr drivers) and Raspberry Pi RP2350 (no Ethernet MAC, no CAN).
3. **Ethernet only through a MAC inside the host chip**, never an SPI Ethernet controller.
4. **Mornsun parts are banned.**
5. Pre-certified radio modules; latest-generation parts with ≥ 5 years longevity; easy to buy in India; second source where possible.
6. Firmware: **upstream Zephyr support is a must** for every MCU we program — the chip and the peripherals we use (owner, 2026-11-22; PRD FW-1). Parts without it are out (PIC32CK, PIC32MZ-W1).
7. Easy to manufacture at Indian contract manufacturers: standard PCB tech, avoid fine-pitch BGA.

## Never add parts silently

When a rule or priority forces extra chips or cost, **stop and state the consequence first**: extra parts, INR delta, alternatives. Prefer the single-chip, lowest-part-count answer. Never add a second processor to a module without raising it explicitly. (Past mistakes: adding an STM32H573 next to the ESP32-C6 on the 4G module to satisfy the MAC rule; a premium-everywhere baseboard at INR 4,645 against a ≤ INR 2,000 limit.)

## Cost rules

- **All prices at 100 units only, in every document and in messages to the owner.** Never show or mention prices at any other quantity (owner, 2026-11-18 and again 2026-11-19: "forget prices at 1k"). The BOM line items in `build_architecture.py` are stored at 100 units (research price × 1.3 until 100-unit quotes exist). Distributor quotes cited as sources keep their own quantity.
- **Relays and fuses: no online prices** (owner, 2026-11-22) — they are priced only from the owner's local quotes. All other parts may use online distributor prices at 100 units.
- **Finished cost = BOM × 1.5** (50 % for manufacturing, packing, logistics). Price build-up: BOM → ×1.5 → + NRE ÷ volume → + firmware royalty → price. Exact figures in PRD §4.16.
- Targets: 4G modem card ≤ INR 1,000 finished cost; Wi-Fi + BLE ≤ INR 600 finished cost; LoRa **selling price INR 1,600** (price after profit, without power module and adapter; 2026-11-19); Fieldbus controller BOM ≤ INR 2,000 (hard limit).
- Always show the **price before profit** (cost + royalty) and the **price after profit** (ex-works). Price the power module (one per module) and the adapter (one per stack) as separate items, never folded into module prices (owner, 2026-11-19).
- Check every estimate against its target **before** presenting it. Offer design-to-cost options, not a premium build. Mark unverified prices as ESTIMATE / UNVERIFIED.

## Owner-facing material (diagram, deck, costing)

- Show **only the four modules** plus a short options/accessories section. No "LEAN", chip-down or alternative-variant rows; they read as extra products. Put cost-down ideas in the PRD open decisions or ask.
- Use current names: **Fieldbus controller** (not baseboard / IO controller), **4G modem card**.
- Never label rows or options with opaque codes (C1, C2 …). Name every module and combination and show it visually; give it a dedicated page rather than squeezing it in (owner, 2026-11-19: called the coded table "laziness").
- Keep it simple; the owner reacts badly to clutter.

## Certification

Phase 1: India-only launch (TEC MTCTE, WPC, BIS). Phase 2: global (CE, CRA, others) only after Phase 1 succeeds. Design in now anything that would need a hardware change later.

## Research

- When a request splits into several independent research topics, run **parallel agents on Opus** (not Fable: it burned the whole usage window; not Sonnet: the owner overrode it). Small single-topic tasks: do them directly.
- Each agent writes its report to `docs/research/Rnn_<Topic>.md`, saving findings every few sources, and must not read whole PDFs into context. Datasheets go to `docs/datasheets/<category>/`.
- The main session reviews and consolidates findings into the PRD.
- On relaunch, tell agents to continue from the partial report on disk. If agents stop on a usage limit, resume them with SendMessage after the reset instead of starting new ones.

## Working with the owner

- The owner sends many short, terse follow-up messages mid-task (often with typos). Collect them all, fold them into the PRD, and state how each ambiguous one was interpreted (PRD §5).
- Write dates as absolute dates (YYYY-MM-DD) when recording decisions.
- Ask when a decision is genuinely the owner's (cost vs. reliability trade-offs, new modules, architecture changes); otherwise pick the sensible default and say so.
