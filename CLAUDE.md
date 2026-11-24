# Universal Controller — hardware repo (umbrella)

This repo is the umbrella for all hardware of the Universal Controller family. It holds the system documents and pins one design repo per module as a git submodule (owner, 2026-11-24).

## Repo map

| Path | Repo | Contents |
|---|---|---|
| `docs/arch/` | this repo | PRD, specifications, research, architecture PDF, deck, specsheet, datasheets — working rules in `docs/arch/CLAUDE.md` |
| `modules/fieldbus-controller/` | `UC-HW-Fieldbus-Controller` | Base card + raised plug-in MCU cards (STM32C5A3VGT6 standard, STM32H573VIT6 option) |
| `modules/4g-modem-card/` | `UC-HW-4G-Modem-Card` | Quectel EC200U-CN card (LTE Cat 1 + GPS) |
| `modules/gps-card/` | `UC-HW-GPS-Card` | GPS-only card (D-40) |
| `modules/wifi-ble/` | `UC-HW-WiFi-BLE` | ESP32-C6 module |
| `modules/lora/` | `UC-HW-LoRa` | STM32WLE5 module |
| `modules/battery-board/` | `UC-HW-Battery-Board` | Optional battery + charger board with its own 18650 holder |
| `lib/` inside every module repo | `UC-HW-Lib` | Shared KiCad library, circuit blocks, templates, housing models, tools |

Firmware lives in separate repos (`UniCon`). Hardware links to it by board revision and by the minimum firmware version in each hardware release note.

## Where things go

- **Requirements:** only in `docs/arch/docs/01_Requirements_PRD.md`.
- **Specs every module must follow:** `docs/arch/docs/02_Specifications.md`. That covers the stack bus, the 4G UART link, the battery-board socket, the power stage and the enclosure family.
- **Everything about one module:** that module's repo. That covers its design spec, schematics, PCBs, BOM, mechanical CAD and production guidelines.
- **Parts, footprints, circuit blocks or housing models used by more than one module:** `UC-HW-Lib`.
- **Part selection, cost and owner-facing rules:** `docs/arch/CLAUDE.md`. Read it before choosing parts or quoting prices.

## Git

- **Cloning:** use `git clone --recurse-submodules <url>`. After a pull, run `git submodule update --init --recursive`.
- **Submodule URLs are relative** (`../UC-HW-<name>.git`), so they follow whatever URL this repo was cloned with.
- **Commit inside the module repo,** on its own branch. Move this repo's pointer to a module only for a system release, meaning a set of module revisions known to work together.
- **The library is pinned in each module repo.** Moving a module's `lib/` pointer is a deliberate step.
- **Fab outputs are not committed.** Generate them with the jobset and zip them into the GitHub release.
- **Board revisions:** the letter goes in the title block and on the silkscreen, with a tag `<board>-rev-<letter>` per fab release.
- **This repo's own commits are made by the owner.** Their messages are version-style (`V0.0.x-dirtyN`), so leave changes here staged rather than committing them, unless asked.

## Tools

- **KiCad 10** runs as an AppImage, with `kicad-cli` on PATH. Use the KiCad MCP tools for schematic and layout work.
- **Mechanical CAD** is build123d (Python), in each module's `mech/`. Keep the venv outside the repos.
