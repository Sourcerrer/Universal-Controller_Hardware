# R01 — Standards, Compliance and Certification Strategy

Status: PARTIAL — all sections written 2026-11-14, but research was cut off by tool limits (web-search budget exhausted, then fetch limit). Items marked **UNVERIFIED** are engineering knowledge of the standards not confirmed against a source fetched in this run; they must be checked against the standard text or a test-lab before being used in a test plan or DoC. Sourced items carry [n].
Scope: modular industrial IoT gateway/controller family — enclosed, DIN-rail, side-by-side stackable modules (baseboard controller with secure MCU + secure element and IO/ADC; Wi-Fi+BLE module; LoRa module; combined 4G + Ethernet + Wi-Fi module; CAN/RS-485 fieldbus either on baseboard or on a small fieldbus card). India first, EU (CE + CRA) later.

Convention: every regulatory statement carries a source number [n] from the list in section 12. Anything not confirmed against a source is marked UNVERIFIED.

## 1. Executive summary

1. Treat **every enclosed module as its own product** (own CE/RED DoC, own India approvals) and also certify defined **stack configurations** (worst case: baseboard + 4G/Eth/Wi-Fi + LoRa + Wi-Fi/BLE + fieldbus, all radios transmitting together).
2. **EU radio SKUs** fall under RED 2014/53/EU (not EMC/LVD directly); the baseboard and the fieldbus card (no radio) fall under EMC 2014/30/EU, and LVD 2014/35/EU only for the AC-mains variant. Key radio ENs as cited (list of Oct 2025 [25]): EN 300 328 V2.2.2, EN 300 220-2 V3.3.1 (V3.1.1 ceases 11 Jun 2027), EN 301 908-1 V15.2.1, EN 301 908-13 V13.3.1, EN 301 511 V12.5.1, EN 301 489-1 V2.2.3 with -3 V2.3.2, -17 V3.3.1, -19 V2.2.1, -52 V1.3.1.
3. **EMC environment = industrial** (EN IEC 61000-6-2 immunity, EN IEC 61000-6-4 / CISPR 11/32 Class A emission). Design to Class B emissions anyway if any SKU may be sold for residential/light-industrial use. Design targets: ESD ±8 kV contact / ±15 kV air, EFT ±4 kV power, surge ±2 kV on long lines (one level above the standard) — UNVERIFIED test-level values, see 3.3.
4. **Cyber (EU):** RED Delegated Reg. 2022/30 (EN 18031-1/-2) applies from 1 Aug 2025 and is **repealed from 11 Dec 2027** by Reg. 2026/339 [23]; from then the **CRA** applies in full. CRA reporting duties (24 h / 72 h / 14 d) already apply since **11 Sep 2026** to products on the EU market [14][21].
5. **CRA class:** the 4G+Ethernet+Wi-Fi module (cellular modem + router, possibly Wi-Fi AP) is very likely **Important Class I (Annex III item 12)** [15][17]; the baseboard controller is default class if marketed as a controller, Class I if marketed as a router/gateway. The 2022 "industrial IACS/IIoT" entries were removed from the final text [15][20]. Class I needs a notified body unless a cited harmonised standard is applied in full — none cited yet [5][6][18].
6. **India:** WPC licence-exempt LoRa under **G.S.R. 853(E) 2021**: 500 mW e.r.p., APC, ≤ 2.5 % duty cycle (≤ 10 % for gateways), ≤ 200 kHz, ETA required [24]. TEC MTCTE "IoT Gateway" mandatory since 1 Jan 2024 [11]. BIS CRS: Li-ion cells/packs to IS 16046-2 [9][10]; whether the gateway itself falls in a CRS category is UNVERIFIED.
7. **Pre-certified radio modules** save the RED 3.2 conducted radio test suite and most of the module-level radio work, but the host still needs: radiated spurious/EN 301 489 EMC, RF exposure, safety, co-location (multi-TX) checks, and its own DoC — UNVERIFIED in detail (ETSI EG 203 367 not fetched).
8. **Open risks:** CRA class of the stack, BIS CRS category, MTCTE scope for each standalone module, 2.4 GHz WPC limits and ETA self-declaration process, CRA standards timing, exposed stack connector ESD/touch safety, Li-ion in outdoor enclosures.

## 2. Compliance matrix

Legend: Base = baseboard controller; 4G = 4G+Eth+Wi-Fi module; WB = Wi-Fi+BLE module; LoRa = LoRa module; FB = fieldbus card (if built). M = mandatory, R = recommended. "UV" = UNVERIFIED edition/level.

| Area | Standard (edition) | Applies to | Test level / key criterion | HW design implication | Market | M/R |
|---|---|---|---|---|---|---|
| Radio 2.4 GHz | EN 300 328 V2.2.2 [25] | WB, 4G (Wi-Fi) | Spectrum access, adaptivity, spurious | Use pre-certified module, keep antenna within approved type/gain | EU | M |
| Radio SRD 863-870 | EN 300 220-2 V3.3.1 (V3.1.1 until 11 Jun 2027) [25] | LoRa | Duty cycle/power per sub-band | Duty-cycle enforcement in firmware | EU | M |
| Radio LTE | EN 301 908-1 V15.2.1, -13 V13.3.1 [25] | 4G | Conducted/radiated spurious, ACLR | Pre-certified modem; antenna gain limit | EU | M |
| Radio GSM | EN 301 511 V12.5.1 [25] | 4G (if 2G) | GSM RF | Pre-certified modem | EU | M |
| GNSS (if used) | EN 303 413 V1.2.1 [25] | 4G (if GNSS enabled) | Receiver | — | EU | M if GNSS |
| EMC radio | EN 301 489-1 V2.2.3 + -3 V2.3.2, -17 V3.3.1, -19 V2.2.1, -52 V1.3.1 [25] | all radio SKUs | Immunity/emission per port | Filtering on all ports | EU | M |
| EMC immunity | EN IEC 61000-6-2:2019 (UV) | Base, FB, all modules | Industrial levels, see 3.3 | TVS, CMCs, shielding | EU/Global | M (via EMC/RED 3.1b) |
| EMC emission | EN IEC 61000-6-4:2019 (UV) / EN 55032 Class A | all | Class A (Class B recommended) | Spread-spectrum clocks, ground planes | EU/Global | M |
| Safety | EN IEC 62368-1:2020+A11 (UV) | all (SELV); Base with AC | Reinforced insulation mains-SELV | Certified AC-DC module, creepage | EU/India | M |
| Safety alt. | EN 61010-1 / EN IEC 61010-2-201 (UV) | Base (if sold as control equipment) | — | See 3.6 | EU | Option |
| RF exposure | EN IEC 62311 / EN 50665 / EN 62479 (UV) | all radio SKUs | ≥ 20 cm separation statement | Antenna placement, user manual | EU | M |
| Cyber (RED) | EN 18031-1/-2/-3:2024 with restrictions [25][7] | radio SKUs placed 1 Aug 2025 - 10 Dec 2027 | Passwords mandatory | Unique credentials, secure update | EU | M |
| Cyber (CRA) | Reg. (EU) 2024/2847 Annex I [22]; EN 40000 (pending) | all | Annex I Part I/II | See section 9 | EU | M from 11 Dec 2027 |
| ESD (system) | IEC 61000-4-2 (UV) | all, incl. exposed bus connector | ±4 kV contact/±8 kV air minimum | TVS on every external pin | Global | M |
| ESD (factory) | IEC 61340-5-1 / ANSI/ESD S20.20 (UV) | production | ESD programme | EPA in factory | Global | R |
| Battery | Reg. (EU) 2023/1542 (UV details) | modules with Li-ion | Labelling, removability, due diligence | Replaceable cell holder | EU | M |
| Li-ion cell | IEC 62133-2 / IS 16046-2:2018 [9][10]; UN 38.3 | modules with Li-ion | Cell certification | Buy certified cells | EU/India | M |
| RoHS/REACH/WEEE | 2011/65/EU + 2015/863; REACH; WEEE (UV) | all | Substance limits | Component declarations | EU | M |
| India radio | G.S.R. 853(E) 2021 [24]; 2.4 GHz rules (UV) | LoRa; WB, 4G | 500 mW e.r.p., ≤2.5 % DC | Power/duty limits in FW | India | M (ETA) |
| India telecom | TEC MTCTE IoT Gateway (TEC 33010:2025 UV) [11][12] | stack, 4G (likely) | EMC, safety, security | Same design as CE | India | M |
| India safety | BIS CRS IS 13252-1 / IS 16046-2 [9] | adapter, cells; gateway UV | — | — | India | M (if category) |
| Environment | IEC 60068-2-x, IEC 60529 IP20/IP65 (UV) | all | See 6 | Enclosure, conformal coat | Global | R |
| IO | IEC 61131-2 (UV) | Base IO | Type 1/3 DI, analog | Input design | Global | R |
| Mechanics | EN 60715 (UV) | all | 35 mm rail | Clip design | Global | R |

## 3. EU / CE

### 3.1 Applicable legislation
- **RED 2014/53/EU** (OJ L 153, 22.5.2014 [23]) for every radio SKU (WB, LoRa, 4G) and for any stack containing one: Art. 3.1(a) safety (LVD objectives, no lower voltage limit), 3.1(b) EMC, 3.2 spectrum use, 3.3(d)(e)(f) cybersecurity via Delegated Reg. (EU) 2022/30 (OJ L 7, 12.1.2022) applicable from 1 Aug 2025 [23]; EN 18031-1/-2/-3:2024 cited by Implementing Decision (EU) 2025/138 with restrictions — e.g. no presumption under 3.3(d) if, under clauses 6.2.5.1/6.2.5.2, "the user is allowed not to set and use any password" [25]. 2022/30 is repealed from 11 Dec 2027 [23].
- **EMC 2014/30/EU** for non-radio products (baseboard alone, fieldbus card); **LVD 2014/35/EU** for non-radio products with 50–1000 V AC (baseboard AC variant). The 12–24 V DC-only non-radio products are outside LVD (below 75 V DC) — threshold UNVERIFIED in this run but stated in LVD Art. 1.
- **RoHS 2011/65/EU** + Delegated Directive (EU) 2015/863 (10 substances), **REACH** (SVHC Art. 33 information), **WEEE 2012/19/EU** (registration per country, bin label) — UNVERIFIED (not fetched).
- **Battery Regulation (EU) 2023/1542**: applies to batteries incorporated in products. Expected relevant points (UNVERIFIED, EUR-Lex not reachable): portable batteries in appliances must be removable and replaceable by the end-user from 18 Feb 2027 (Art. 11), with exceptions for devices that need continuity of power/safety reasons; CE/labelling and separate-collection symbol; QR code from 2027. Implication: design the Li-ion cell as user-replaceable (holder or plug-in pack) to avoid relying on an exception.
- **GPSR (EU) 2023/988**: applies to consumer products only; a B2B industrial controller is generally outside, but outdoor nodes sold to consumers would be in — UNVERIFIED.
- **CRA (EU) 2024/2847**: see section 4.

### 3.2 Harmonised standards and current editions
Radio and EMC-for-radio editions below are from the Commission's RED summary list (generated 13.10.2025; amendments up to 4 Sep 2026 exist, latest by Implementing Decision (EU) 2026/2003 — check for newer versions) [25][26]:

| Standard | Edition cited | Cited (OJ) | Note |
|---|---|---|---|
| EN 300 328 | V2.2.2 | 6.2.2020, 2020/167 | 2.4 GHz wideband |
| EN 300 220-2 | V3.3.1 | 11.12.2025, 2025/2499 | V3.1.1 presumption ends 11.06.2027 |
| EN 301 908-1 | V15.2.1 | 4.10.2023, 2023/2392 | IMT common |
| EN 301 908-13 | V13.3.1 | 15.05.2025, 2025/893 | E-UTRA UE |
| EN 301 511 | V12.5.1 | 9.2.2018 | GSM |
| EN 303 413 | V1.2.1 | 29.3.2022 | GNSS receivers |
| EN 301 489-1 | V2.2.3 (11-2019) | referenced by the -x parts | EMC common |
| EN 301 489-3 | V2.3.2 | 15.05.2025 | SRD (LoRa) |
| EN 301 489-17 | V3.3.1 | 15.05.2025 | Wi-Fi/BLE |
| EN 301 489-19 | V2.2.1 | 15.05.2025 | GNSS receive-only |
| EN 301 489-52 | V1.3.1 | 15.05.2025 | Cellular UE |
| EN 18031-1/-2/-3 | 2024 | 30.01.2025, 2025/138 | with restrictions |
| EN 55035 | 2017 | cited under RED | multimedia immunity |

Not confirmed this run (UNVERIFIED): EN IEC 61000-6-2:2019, EN IEC 61000-6-4:2019 (+A1:2021?), EN 55032:2015+A11:2020/A1:2020, EN IEC 61326-1:2021, EN IEC 62368-1:2020+A11:2020, EN 61010-1:2010+A1:2019, EN IEC 61010-2-201:2018, EN IEC 62311:2020, EN 50665:2017, EN 62479:2010. An In Compliance article (Jul 2026) notes the EMC-Directive list (Implementing Decision (EU) 2019/1326) has not been amended for new content since 9 Jun 2022 and no IEC-based harmonised standard has been newly cited since the start of 2025 [27] — so older cited editions remain the presumption basis.

**Which safety standard:** EN IEC 62368-1 (ICT/AV equipment, hazard-based) fits a gateway with communication function and is what TEC/BIS (IS 13252/IS/IEC 62368-1) and most test labs expect for IoT gateways; EN 61010-1 (+ -2-201 for control equipment such as PLCs) fits a controller whose main function is industrial measurement/control. Recommendation (judgement): use **EN IEC 62368-1** for all communication modules and the baseboard (it aligns EU and India), and check -2-201 clauses only if the baseboard is marketed as a PLC. UNVERIFIED as to standard text.

### 3.3 EMC test levels per port (industrial environment)
Values below are the commonly applied EN IEC 61000-6-2 (industrial immunity) levels — **UNVERIFIED in this run** (standard is paywalled; no lab summary fetched). Confirm against the purchased standard. Performance criteria: A = normal operation within spec; B = temporary degradation, self-recovering; C = temporary loss needing reset/operator.

| Phenomenon | Enclosure | AC mains port | DC power port | Signal/IO, Ethernet, RS-485/CAN | Crit. | Design target |
|---|---|---|---|---|---|---|
| ESD IEC 61000-4-2 | ±4 kV contact / ±8 kV air | — | — | — | B | ±8 kV contact / ±15 kV air |
| Radiated RF 61000-4-3 | 10 V/m 80 MHz–1 GHz; 3 V/m 1.4–2 GHz; 1 V/m 2–2.7 GHz (6-2:2019 extends to 6 GHz) | — | — | — | A | 20 V/m |
| EFT/burst 61000-4-4 | — | ±2 kV | ±2 kV | ±1 kV (lines > 3 m) | B | ±4 kV power, ±2 kV signal |
| Surge 61000-4-5 | — | ±2 kV CM / ±1 kV DM | ±0.5 kV CM/DM | ±1 kV CM (lines > 30 m) | B | ±2 kV CM on DC & long lines |
| Conducted RF 61000-4-6 | — | 10 V | 10 V | 10 V (lines > 3 m) | A | 20 V |
| Power-freq. magnetic 61000-4-8 | 30 A/m | — | — | — | A | 100 A/m |
| Dips/interrupts 61000-4-11 | — | 0 % 1 cycle (B), 40 % 10 cycles (C), 70 % 25 cycles (C), 0 % 250 cycles (C) | 61000-4-29 not mandatory in 6-2 | — | B/C | ride-through ≥ 20 ms with Li-ion backup |

Emissions: EN IEC 61000-6-4 references CISPR 11/EN 55011 Group 1 **Class A** or EN 55032 Class A (radiated 30 MHz–6 GHz, conducted AC port, plus DC power port per 6-4:2019) — UNVERIFIED. Class A requires a warning in the manual and is not appropriate for residential use. Recommendation: target **Class B** with 6 dB margin at pre-scan so any module can also be sold under 61000-6-3/EN 55032 Class B. Radio SKUs additionally follow EN 301 489-1 port tables (similar levels; surge applies to DC ports only when cables > 30 m or connected to outdoor lines) — UNVERIFIED. EN IEC 61326-1 (industrial EMC for measurement/control) is an alternative product standard for the baseboard IO; IEC 61131-2 sets PLC-specific immunity (e.g. higher EFT on IO) — UNVERIFIED.

### 3.4 ESD
- System level: IEC 61000-4-2 ±4 kV contact / ±8 kV air (industrial) is the compliance minimum; design to ±8 kV contact / ±15 kV air (level 4) on every user-accessible point, including the exposed side stack connector of a standalone module — UNVERIFIED levels.
- Component level: ICs typically rated HBM ±2 kV (JS-001) and CDM ±500 V (JS-002); these protect only in handling, not in the field — UNVERIFIED.
- Manufacturing: run an ESD control programme to IEC 61340-5-1 (2024 ed. UNVERIFIED) or ANSI/ESD S20.20-2021: EPA, grounded wrist straps/mats, ionisers, packaging to IEC 61340-5-3, training, compliance verification.
- Exposed plug-in/stack connector: (1) TVS array (low capacitance for high-speed pairs) at the connector on every pin, return to chassis/ground via short path; (2) recessed connector or sliding/hinged cover/blanking cap on the outermost module; (3) ground/shield pins make first-break-last (longer pins) — Hirose/Würth connectors with such options to be confirmed; (4) series resistors on low-speed signals; (5) the bus must be SELV/ES1 only — never route mains or > 60 V DC on it; (6) define a "connector covered" test configuration but also test direct contact discharge to the uncovered pins (labs typically apply to accessible conductive parts).

### 3.5 Pre-certified radio modules — what is inherited, what is not
(UNVERIFIED in detail — ETSI EG 203 367 and REDCA TGNs were not fetched in this run; content below is standard industry practice.)
- Inherited: the module maker's RED 3.2 conducted radio test reports (EN 300 328 / 300 220 / 301 908 / 301 511) and module EU-type examination/DoC, **provided** the host uses the module within its stated conditions: same antenna type and max gain (or lower), same RF trace/matching per the integration manual, no firmware changes affecting RF parameters, power supply within spec.
- Still required on the host: (a) a full host DoC under RED (the host maker is the manufacturer); (b) EN 301 489-1 + relevant -x parts on the host; (c) radiated spurious emissions with the module in the host (EN 300 328 / 301 908 radiated parts), typically a reduced "spot check"; (d) RF exposure assessment (EN 62311 / EN 50665 / EN 62479) for the final antenna arrangement, including simultaneous transmission; (e) safety (EN IEC 62368-1); (f) **co-location**: 4G + Wi-Fi in the same enclosure, and LoRa/Wi-Fi/BLE modules side-by-side in the stack — intermodulation/spurious with all transmitters active, receiver blocking; (g) EN 18031 / CRA for the host.
- Modular family: test each standalone module as a product; then test the worst-case stack (all radios, max cable lengths, AC variant) and declare stack configurations in the DoC; document why intermediate configurations are covered.
- FCC/ISED equivalent: modular approval (FCC Part 15.212, KDB 996369; ISED RSS-Gen) lets the host reuse the module grant if antenna/integration conditions are met; host still needs Part 15B unintentional-radiator verification and co-location (KDB 447498 for RF exposure) — UNVERIFIED.

### 3.6 Safety — AC mains, Li-ion
(UNVERIFIED — values from IEC 62368-1 knowledge; confirm against the standard.)
- Use a **certified, encapsulated AC-DC module** (IEC/EN 62368-1, reinforced insulation, OVC II, 4 kVac / 3 kVac primary-secondary hipot class) so the baseboard only has to manage the mains input wiring.
- 230 VAC (≤ 300 V rms), OVC II, PD2, material group IIIb: reinforced clearance ≈ 3.0 mm (up to 2000 m), reinforced creepage ≈ 5.0 mm on PCB; basic ≈ 1.5 mm clearance / 2.5 mm creepage. Use ≥ 6.4 mm creepage/slots as margin for outdoor PD3 conditions.
- Fuse in line (time-lag, before the module, rated per module datasheet, breaking capacity ≥ 1500 A for 230 V), MOV/varistor L-N (and L/N-PE with GDT if PE present) ahead of module; surge test ±2 kV CM/±1 kV DM.
- PE: if Class I, PE terminal with ≥ same cross-section and marking; DIN-rail Class II construction is simpler — no PE needed if reinforced insulation throughout.
- Markings: rated voltage/frequency/current, symbol for Class II, fuse rating, manufacturer, model, CE.
- Stack bus and all external IOs must be ES1 (SELV, ≤ 60 V DC) — 24 V IO qualifies.
- Li-ion: IEC 62368-1 Annex M (batteries and charging): charging within the cell maker's voltage/current/temperature window under single-fault conditions, protection IC + secondary protection, no charging below 0 °C; cells certified to IEC 62133-2 (India: IS 16046-2 [9][10]); transport per UN 38.3 test summary (UN 38.3 test summary required by shippers). Outdoor enclosures can exceed 60 °C — charging cutoff by NTC is mandatory.

## 4. EU Cyber Resilience Act

Note on sources: EUR-Lex blocked automated download/fetch from this environment (returns the OJ landing page). Article/Annex wording below was read from springlex.eu, which reproduces the OJ text (OJ L 2024/2847, 20.11.2024) article by article [14]-[19]; it should be spot-checked against EUR-Lex [2] by a human before being relied on in a DoC.

### 4.1 Scope and dates
- Scope: products with digital elements (hardware or software with a data connection to a device or network) placed on the EU market [2]. Every UC module and the baseboard are in scope (all have data connections).
- Art. 71: entry into force on the 20th day after OJ publication (OJ 20 Nov 2024 -> 10 Dec 2024); Chapter IV (notified bodies, Arts 35-51) applies from **11 Jun 2026**; Art. 14 reporting obligations from **11 Sep 2026**; everything else (essential requirements, CE marking, conformity assessment) from **11 Dec 2027** [14]. Art. 14 applies also to products already on the market [1].

### 4.2 Classification (Annex III / IV, as read 2026-11-14)
- Annex III Class I (19 entries) includes: (1) identity management/access-control hardware, (5) VPN products, (6) network management systems, (8) boot managers, (10) **physical and virtual network interfaces**, (11) operating systems, (12) **routers, modems intended for the connection to the internet, and switches**, (13) microprocessors and (14) **microcontrollers with security-related functionalities**, (15) ASIC/FPGA with security functions [15].
- Annex III Class II (4 entries): hypervisors/container runtimes; firewalls/IDS/IPS; tamper-resistant microprocessors; tamper-resistant microcontrollers [15]. The 2022 Commission proposal had Class I entries for "Industrial Automation & Control Systems (IACS) ... such as PLC" and "Industrial Internet of Things", and Class II entries for "routers, modems ... and switches, intended for industrial use", IACS/IIoT "intended for the use by essential entities" and PLC microprocessors [20]. **None of these industrial entries are in the final Regulation** [15] — a PLC/industrial IoT controller is no longer important merely because it is industrial.
- Annex IV critical: hardware devices with security boxes; smart-meter gateways (Directive 2019/944) and devices for advanced security purposes incl. secure cryptoprocessing; **smartcards or similar devices, including secure elements** [16].
- Implementing Regulation (EU) 2025/2392 (OJ 1 Dec 2025, in force 21 Dec 2025) gives technical descriptions [3][17]: routers = products that "establish and control the flow of data between different networks" (network layer); internet modems explicitly include "cellular modems"; physical network interfaces include Wi-Fi, Ethernet, USB, Bluetooth, Zigbee, **Fieldbus** interface cards/controllers/adapters; microcontrollers with security-related functionalities = MCUs whose security functions (encryption, authentication, secure key storage, RNG, TEE) protect "other products, networks or services beyond the microcontroller itself"; tamper-resistant MCU (Class II) = additionally tamper evidence/resistance/response with AVA_VAN level 2 or 3 [17]. Classification follows the product's **core functionality**; the important/critical procedures apply only "if that product as a whole is an important or critical product"; integrating such a component (e.g. a secure element or security MCU) does not by itself make the host product important, but the manufacturer must still evaluate the security of the whole product including that component [17] (verified in the OJ PDF, recital text). Also verified in [17]: routers "include but are not limited to wired and wireless routers ... routers with or without modems"; switches include "bridges such as wireless access points" — so if the 4G module's Wi-Fi acts as an access point/hotspot it is caught by entry 12 a second way.

**Assessment for this product family (analysis, not legal advice):**

| Product as placed on market | Likely CRA class | Reasoning | Conformity route |
|---|---|---|---|
| Combined 4G + Ethernet + Wi-Fi module, sold standalone (or the stack when it routes LAN/fieldbus traffic to the internet via LTE) | **Important Class I, entry 12 (router / internet modem)** — high probability | Its core function is connecting a local network/device to the internet over a cellular modem and forwarding traffic between networks; 2025/2392 lists "cellular modems" explicitly [17] | Module A only if a harmonised standard (or cert scheme) is applied in full; otherwise Module B+C or H with a notified body [18] |
| Baseboard controller (secure MCU + SE, IO/ADC, routes data between modules) | Default class is arguable if it is marketed as a controller/data-logger; **Class I entry 12 (router)** risk if marketed as a "gateway" that routes between networks | Core function is IO control + data aggregation. The MCU and SE inside are components; their class applies to the chip vendor, not to the host [3] | Module A (default) — or as above if Class I |
| Wi-Fi + BLE module / LoRa module / fieldbus card, sold standalone as an add-on to the stack | **Possible Class I entry 10 (physical network interface)** — if sold as a network interface card for the controller; default if sold as a self-contained sensor/remote node | 2025/2392 names Wi-Fi, Bluetooth, Fieldbus interface cards and adapters [17] | As Class I |
| Full stack sold as one product | Highest class among its core functions -> likely Class I | Core functionality test [3] | As Class I |

Practical consequence: plan for **Class I** for the 4G module and the stack. Until the CRA harmonised standards are cited in the OJ, Module A is not available for Class I, so budget a notified-body Module B+C (EU-type examination) for these SKUs, or time the EU launch after citation of EN 40000-series/vertical standards (see 4.3).

### 4.2a Conformity-assessment routes (Art. 32) [18]
- Default products: Module A (internal control), or B+C, or H, or an EU cybersecurity certification scheme.
- Class I: Module A only if harmonised standards / common specifications / EU certification scheme (>= "substantial") are applied in full; otherwise B+C or H.
- Class II: B+C, H, or certification scheme ("substantial"+); always third party.
- Critical (Annex IV): European cybersecurity certification scheme per Art. 8(1); if not mandated, Class II routes.
- "CRA certified" is therefore not normally a certificate: for default and (standards-based) Class I products the manufacturer performs the assessment, draws up the technical documentation (Annex VII) and EU DoC, and affixes CE. A notified-body certificate (EU-type examination certificate) exists only for B+C/H routes.

### 4.2b Manufacturer obligations (selected)
- Annex I Part I (product properties) [22]: (1) appropriate cybersecurity based on risk assessment; (2)(a) no known exploitable vulnerabilities at release; (b) secure-by-default configuration with reset to original state; (c) vulnerabilities fixable by security updates, automatic updates on by default with opt-out; (d) protection from unauthorised access (authentication, identity/access management), report possible unauthorised access; (e) confidentiality of stored/transmitted data (state-of-the-art encryption); (f) integrity of data, commands, programs and configuration, report corruption; (g) data minimisation; (h) availability of essential functions incl. DoS resilience; (i) do not degrade other devices/networks; (j) limit attack surface incl. external interfaces; (k) exploitation-mitigation mechanisms; (l) record/monitor relevant internal activity (security logging) with user opt-out; (m) secure permanent deletion of all data and settings.
- Annex I Part II (vulnerability handling) [22]: (1) identify components and draw up "a software bill of materials in a commonly used and machine-readable format covering at the very least the top-level dependencies"; (2) remediate without delay, security updates separate from feature updates where feasible; (3) regular security testing; (4) publicly disclose fixed vulnerabilities; (5) coordinated vulnerability disclosure policy; (6) contact address for reports; (7) secure update distribution; (8) free, timely security updates with advisories. The SBOM need not be published but goes into the technical documentation.
- Support period: at least **5 years** unless expected use time is shorter (Art. 13(8)); each security update must remain available for at least **10 years** after issue (Art. 13(9)); technical documentation and DoC retained **10 years** or the support period if longer (Art. 13(13)) [19]. For industrial equipment with 10-15 year lifetimes, the expected-use-time rule pushes the support period well beyond 5 years.
- Due diligence on third-party components including open source (Art. 13(5)) [19].
- Reporting (Art. 14, from 11 Sep 2026) via the ENISA single reporting platform to the coordinating CSIRT and ENISA: actively exploited vulnerability — early warning **24 h**, notification **72 h**, final report **14 days** after a fix is available; severe incident — **24 h / 72 h / 1 month**; inform users [21].
### 4.3 Harmonised standards status
- Standardisation request M/606; draft amendment (Jul 2026) would move drafting deadlines to 31 Oct 2026 (horizontal A/B) and 31 Dec 2026 (vertical C) - still draft. EN 40000-1-1 (vocabulary) / EN 40000-1-2 (principles for cyber resilience, risk management) reportedly passed CEN-CENELEC formal vote with ratification scheduled for 2 Nov 2026 — ratification and any OJ citation **UNVERIFIED as of 2026-11-14**; prEN 40000-1-3 (vulnerability handling) in preparation; prEN 50770 series for OT/industrial products, with a part for routers/switches (secondary source). No CRA harmonised standard is known to be cited in the OJ yet [5][6]. Consequence: for Class I products Module A is not available until a standard is cited and applied in full (Art. 32(2)) [18].
- Useful interim references (not presumption of conformity under CRA): IEC 62443-4-1 (secure development lifecycle) and IEC 62443-4-2 (component security requirements, SL 1-4) for industrial components; ETSI EN 303 645 (consumer IoT baseline); EN 18031-1 (RED internet-connected radio). Edition years: IEC 62443-4-1:2018, IEC 62443-4-2:2019, ETSI EN 303 645 V3.1.3 (2024-09) — editions UNVERIFIED in this run (not fetched).

### 4.4 RED delegated act / EN 18031 and the hand-over to CRA
- Delegated Regulation (EU) 2022/30 (OJ L 7, 12.1.2022) activates RED Art. 3.3(d) network protection, (e) personal data/privacy, (f) fraud for internet-connected radio equipment; requirements apply from **1 Aug 2025** [23].
- EN 18031-1/-2/-3:2024 cited in OJ with restrictions via Implementing Decision (EU) 2025/138 (30 Jan 2025); restrictions concern default passwords (6.2.5.1/6.2.5.2 of -1), parental control in -2, fraud in -3 — where a restriction bites (e.g. a product allowing users to keep no password), no presumption of conformity and a notified body is needed [7][8].
- **Delegated Regulation (EU) 2026/339** of 16 Feb 2026 (OJ L 29.4.2026) repeals 2022/30 **with effect from 11 Dec 2027**, the date the CRA applies in full, to avoid double regulation; radio equipment placed on the market between 1 Aug 2025 and 10 Dec 2027 remains subject to RED 3.3(d)(e)(f) surveillance [23]. The Commission plans to withdraw the EN 18031 references under RED after the repeal [23].
- Practical consequence for UC: any radio SKU (Wi-Fi/BLE, LoRa, 4G) placed on the EU market **before 11 Dec 2027** needs EN 18031-1 (and -2 if it processes personal data, -3 only if it handles monetary value) under RED; from 11 Dec 2027 it needs CRA instead. Since the EU launch is "later", target an EU launch on or after 11 Dec 2027 and design once to CRA Annex I — EN 18031-1 work is largely reusable as CRA evidence (but is not a CRA presumption).

## 5. India

### 5.1 BIS Compulsory Registration Scheme (CRS)
- IS 13252 (Part 1):2010 (= IEC 60950-1) is the CRS safety standard for IT equipment; BIS lab scope listings show it [9]. Transition of CRS to IS/IEC 62368-1 — UNVERIFIED in this run (could not fetch a BIS/MeitY order). Which CRS product categories capture an *industrial* IoT gateway/controller is **UNVERIFIED**: CRS lists named product categories (e.g. adaptors/power supplies for IT equipment, "wireless keyboards", "smart watches", etc.); a DIN-rail industrial controller may not fall into any listed category. The external/internal **power adapter** category (power adaptors for IT equipment) is the one most likely to apply if the product ships with a separate adapter. Action: obtain a written BIS/MeitY category opinion before launch.
- Li-ion: IS 16046 (Part 2):2018 (= IEC 62133-2:2017) is the CRS standard for sealed secondary lithium cells/batteries; registration is per cell/battery model by the cell/pack manufacturer [9][10]. Buy only cells/packs that already hold a BIS CRS registration (R-number) for IS 16046-2.
- Government procurement: BIS registration is legally mandatory only for products in notified CRS categories (sale/import), but government/utility tenders commonly ask for BIS, TEC MTCTE and PPP-MII documents — tender-specific (UNVERIFIED as a general rule).
- Cost/timeline: CRS testing at a BIS-recognised lab plus registration typically weeks to a few months; fees not verified this run (UNVERIFIED).

### 5.2 TEC MTCTE
- DoT MTCTE annexure lists "IoT Gateway" in Phase-3 with mandatory certification from 1 Jan 2024 [11]. TEC 33010:2025 "Generic Requirements – IoT Gateway" reportedly gazetted 23 Jan 2026; TEC 33011:2026 test guide reportedly gazetted 6 Aug 2026 (consultancy sources, UNVERIFIED against the Gazette) [12][13]. MTCTE procedure v3.0 (TEC 93009:2024) [11].
- MTCTE essential requirements typically cover EMC, safety, technical/interface (incl. radio for the radio parts) and security (ITSAR-based) parameters, tested at TEC-designated CABs (Indian labs) — the exact test list for the IoT Gateway ER (TEC 33010:2025) was **not fetched** (UNVERIFIED). Cellular equipment (LTE UE/"Smart" devices with cellular) and Wi-Fi CPE have their own MTCTE ERs; whether a module-level MTCTE certificate (of the pre-certified LTE module) can be leveraged by the host is **UNVERIFIED** — in practice MTCTE certificates are issued per product/model by the OEM, and module test reports may be accepted by the CAB to reduce testing (verify with a CAB).
- Modular family: because each module is sold standalone, expect each SKU that falls in an MTCTE category (the 4G+Ethernet+Wi-Fi module as an "IoT gateway"/router-type product; the stack as "IoT gateway") to need its own MTCTE certificate; MTCTE allows "series"/family declarations in some ERs (UNVERIFIED for IoT Gateway).

### 5.3 WPC — radio licence exemption and Equipment Type Approval (ETA)
- **LoRa 865–867 MHz:** The governing rules are now the "Use of Low Power Equipment in the Frequency Band 865-868 MHz for Short Range Devices (Exemption from Licence) Rules, 2021", **G.S.R. 853(E), 10 Dec 2021**, which superseded the 2005 RFID rules (the older 1 W / 4 W ERP / 200 kHz RFID limits often quoted on blogs relate to the superseded 2005 rules) [24]. Limits (licence-exempt, non-interference/non-protection basis):

| Table | Use | Max power | Channel access / duty cycle | Bandwidth | EN ref |
|---|---|---|---|---|---|
| I | Non-specific SRD (telemetry, telecommand, alarms, data) | 25 mW e.r.p. | Duty cycle 1 % (or FHSS) | ≤ 50 kHz for FHSS with ≥ 58 hop channels | EN 300 220 |
| II | Tracking, tracing and **data acquisition** (meter reading, sensors/actuators, **wireless industrial applications**) | **500 mW e.r.p.** | **Adaptive power control required**; duty cycle **≤ 10 % for network access points, ≤ 2.5 % otherwise** | **≤ 200 kHz** | EN 300 220 |
| III | Wideband data | 25 mW e.r.p. | ≤ 10 % APs / ≤ 2.8 % otherwise | > 600 kHz – ≤ 1 MHz | EN 304 220 |
| IV | RFID | 2 W e.r.p. (4 channels only) | 4 s max continuous TX, 100 ms gap | ≤ 200 kHz | EN 302 208 |

  Source: Gazette text [24]. A LoRa node (125 kHz) fits Table II: 500 mW e.r.p. (≈ +27 dBm e.r.p.), APC, ≤ 2.5 % duty cycle (≤ 10 % if the device is a gateway/network access point). Rule 5: equipment **shall be type approved** (ETA) and comply with the respective EN for spectrum use; safety per ITU/ETSI/ANSI/BIS/ICNIRP [24]. Any amendment after Dec 2021 — UNVERIFIED (searching was cut off).
- **2.4 GHz Wi-Fi/BLE:** licence-exempt under the 2.4 GHz low-power rules (G.S.R. 45(E) of 28 Jan 2005, as amended) — commonly cited limits 1 W max transmitter output, 4 W e.i.r.p., spread-spectrum/OFDM. **UNVERIFIED in this run** (could not reach the DoT/C-DOT gazette host; web-search budget exhausted). ETA is required for equipment in delicensed bands; DoT moved ETA for delicensed-band equipment to a **self-declaration on the Saral Sanchar portal** with test reports from accredited labs (UNVERIFIED — date and notification not retrieved).
- **Cellular (4G/2G):** not licence-exempt band equipment; WPC ETA for licensed-band user terminals is not required in the same way, but MTCTE applies (UNVERIFIED).
- **Import licence:** historically WPC import licences for radio modules were replaced by ETA; whether an import licence/ETA is needed for modules imported for incorporation — UNVERIFIED.

### 5.4 Security mandates (India) — status
- NCCS ITSARs (Indian Telecom Security Assurance Requirements) are applied under MTCTE for security testing; an ITSAR for IoT devices/gateways exists per secondary reports — **UNVERIFIED** (not fetched).
- TEC "Code of Practice for Securing Consumer IoT" (TEC 31318:2021) — voluntary guidance, aligned with ETSI EN 303 645 (UNVERIFIED this run).
- CEA (Cyber Security in Power Sector) Guidelines 2021 and CEA regulations require utilities to source from "trusted sources" and test imported equipment — relevant if selling to power utilities (UNVERIFIED this run).
- CERT-In Directions of 28 Apr 2022: 6-hour incident reporting by service providers/body corporates; mainly an operator obligation (UNVERIFIED this run).
- Public Procurement (Preference to Make in India) Order 2017 (revised) — Class-I local supplier ≥ 50 % local content, Class-II ≥ 20 %; DoT/MeitY notify product-specific thresholds for telecom/electronics (UNVERIFIED this run).

### 4.5 CRA — status of what the manufacturer must do (summary)
"CRA certified" is usually not a certificate. For each SKU: risk assessment → apply Annex I → technical documentation (Annex VII, incl. SBOM, risk assessment, support period) → conformity assessment (Module A, or notified body for Class I without full harmonised standard) → EU DoC + CE marking → vulnerability handling and Art. 14 reporting for the whole support period [18][19][21][22].

## 6. Environmental / reliability standards
(UNVERIFIED — not fetched this run; typical specifications for DIN-rail industrial controllers.)

| Standard | Test | Typical spec |
|---|---|---|
| IEC 60068-2-1 | Cold | −25 °C (−40 °C outdoor), 16 h, operating |
| IEC 60068-2-2 | Dry heat | +70 °C operating, +85 °C storage |
| IEC 60068-2-14 | Change of temperature | −25/+70 °C, 5 cycles |
| IEC 60068-2-30 / -78 | Damp heat cyclic / steady | 55 °C 95 % RH, 6 cycles / 40 °C 93 % 4 days |
| IEC 60068-2-6 | Vibration sine | 5–150 Hz, 1 g (2 g for DIN-rail panel) |
| IEC 60068-2-27 | Shock | 15 g, 11 ms |
| IEC 60529 | IP rating | IP20 in panel; IP65/66 for outdoor node enclosure |
| UL 94 | Flammability | V-0 enclosure and connector plastics (62368-1 fire enclosure needs V-1 or better depending on PS class) |
| IEC 61131-2 | IO | 24 V DI Type 1 (ON 15–30 V, ≥ 2 mA) / Type 3 (ON 11–30 V, 2–15 mA); analog 0–10 V and 4–20 mA, ±0.5–1 % accuracy class; reverse-polarity and over-range tolerance |
| EN 60715 | DIN rail | TH35-7.5 / -15 |

## 7. Certification strategy for the modular family
1. **Freeze design for compliance from day one** (section 8), pre-scan each module at an EMC lab after first spin (₹ cost UNVERIFIED; typically 1–2 days of chamber time).
2. **India first:** (a) WPC ETA for LoRa (G.S.R. 853(E) limits [24]) and Wi-Fi/BLE SKUs (self-declaration route UNVERIFIED); (b) TEC MTCTE for the 4G module and the stack as "IoT Gateway" [11][12] — engage a TEC-designated CAB early to confirm which SKUs need certificates and whether module reports are accepted; (c) BIS CRS — buy registered cells (IS 16046-2) and adapters; get a BIS category opinion for the gateway itself; (d) PPP-MII local-content declaration for tenders.
3. **Test once, report twice:** run EMC to EN IEC 61000-6-2/-6-4 + EN 301 489, and safety to IEC 62368-1 at an ISO 17025 lab accepted by both TEC CABs and an EU notified body/test lab, using the same samples.
4. **EU (launch ≥ 11 Dec 2027 recommended):** RED DoC per radio SKU, EMC(+LVD) DoC for non-radio SKUs; CRA: Module A for default-class SKUs, notified body (Module B+C) for Class I SKUs (4G module, router-like stack) unless EN 40000/vertical standards are cited by then. If any radio SKU ships to the EU before 11 Dec 2027, add EN 18031-1 (and -2) assessment [23][25].
5. **Inherited from pre-certified modules:** conducted radio reports, module RF exposure basis, sometimes module MTCTE/WPC paperwork (UNVERIFIED for India). **Tested on product:** EMC, radiated spurious spot checks, co-location, RF exposure of final arrangement, safety, cyber.
6. **Cost/lead time:** not verified this run (UNVERIFIED). Rough planning numbers only: EMC+safety per enclosure family 6–10 weeks; MTCTE 2–4 months after test reports; notified-body CRA type examination unknown (market not yet established).

## 8. Design-rules checklist (EMC, ESD, safety) — from day one
(Engineering practice; UNVERIFIED as to any specific standard clause.)
1. 4-layer minimum PCB; continuous ground plane; no splits under high-speed traffic; stitching vias at board edges.
2. Define a chassis/"clean" ground at the I/O edge; every external connector (power, IO, RS-485/CAN, Ethernet, antenna, stack bus) enters at one edge with its protection within 10 mm.
3. DC input: reverse-polarity protection, TVS (SMBJ/SMCJ class sized for ±0.5–2 kV surge via 42 Ω), common-mode choke + bulk/ceramic filter, fuse/PTC; 12–24 V nominal tolerant to 9–36 V and 60 V transients.
4. RS-485/CAN: transceivers with ±15 kV+ ESD and ±60 V bus-fault rating, TVS + optional GDT for > 30 m/outdoor lines, galvanic isolation (recommended, ≥ 1 kV), split termination.
5. Ethernet: magnetics with Bob Smith termination to chassis via 1–2 kV cap, low-capacitance TVS on PHY side; 1.5 kV isolation.
6. 24 V DI and analog inputs: series R + TVS + RC filter; 4–20 mA sense resistor protected against 24 V short; optional isolation per channel group.
7. Clocks: spread-spectrum where possible; series damping resistors; keep crystals away from edges; shield cans over radios/DC-DC.
8. DC-DC converters: tight hot loops, input pi-filter, layout per vendor reference; choose switching frequencies away from LoRa/cellular IFs.
9. Stack connector: ESD array on every pin, ground pins first-mate, cover/cap for exposed ends, SELV only, current limit/eFuse on bus power per module, hot-plug inrush limit.
10. Antennas: use only the antenna types/gains in the module's certification; keep ≥ 20 cm separation statement; separate 4G and Wi-Fi antennas for isolation (> 15–20 dB).
11. Safety: mains section on baseboard isolated by slot/creepage ≥ 6.4 mm, fuse + MOV ahead of certified AC-DC module, V-0 materials, Class II construction.
12. Li-ion: protection IC + secondary protection, NTC charge window 0–45 °C, charger IC with timer; cells IEC 62133-2/IS 16046-2; user-replaceable cell.
13. Provide test points/headers for EMC pre-scans; plan for ferrite and filter population options on first spin.

## 9. CRA hardware-implications checklist
Mapped to CRA Annex I Part I points [22] (hardware choices are recommendations):
- [ ] **Root of trust & secure boot** — immutable boot ROM/bootloader verifying signed firmware on the baseboard MCU and on every module MCU (2(f) integrity, 2(k)).
- [ ] **Unique device identity** — per-device key/certificate provisioned in the secure element at production; no shared default passwords (2(d); EN 18031 restriction on password-less use [25]).
- [ ] **Secure key storage** — secure element on baseboard (keys never leave); modules authenticate to baseboard over the stack bus (2(d),(e)).
- [ ] **Debug-port protection** — JTAG/SWD locked/disabled in production (readout protection level set; authenticated debug if needed) (2(j)).
- [ ] **Secure update with anti-rollback** — signed, versioned images; monotonic counter in SE/OTP; A/B or fallback image; update path for every module MCU and the cellular modem firmware (2(c), Part II 7).
- [ ] **Secure defaults & factory reset** — interfaces off unless configured, reset-to-default button/function (2(b), 2(m)).
- [ ] **Encrypted comms** — TLS/DTLS to cloud; LoRaWAN keys in SE; encrypt bus traffic carrying credentials (2(e)).
- [ ] **Tamper detection** — enclosure-open switch/light sensor input to MCU, optional key zeroisation (supports 2(f)/(l); not mandatory).
- [ ] **Security logging** — tamper, failed auth, update events, stored in non-volatile memory with timestamps (2(l)).
- [ ] **Availability/DoS** — watchdog, baseboard able to power-cycle hung modules, rate limiting (2(h)).
- [ ] **Attack-surface minimisation** — no unused services/ports, physical interfaces (USB/UART) disabled or authenticated (2(j)).
- [ ] **Data deletion** — secure erase of keys/config (2(m)).
- [ ] **SBOM and component tracking** — including modem firmware, Wi-Fi/LoRa stacks, RTOS/Linux (Part II 1) [22].
- [ ] **Support period** — size flash for ≥ 5 years (realistically 10+ years) of updates; contract chip/modem vendors for security patches over that period [19].
- [ ] Note: integrating a secure element (Annex IV "secure elements") or security MCU does not make the product critical/important; the SE vendor carries that [17].

## 10. Open risks and decisions
1. **CRA class of the 4G module and of the stack** (likely Class I → notified body until standards cited). Decide marketing description ("controller" vs "gateway/router") with this in mind; get a notified-body or legal opinion.
2. **CRA harmonised standards timing** — EN 40000-1-x ratification/OJ citation UNVERIFIED; prEN 50770 industrial vertical not yet available.
3. **India BIS CRS category** for an industrial gateway — UNVERIFIED; written confirmation needed.
4. **MTCTE scope per standalone module** and acceptance of module-level reports — UNVERIFIED; TEC 33010:2025 not read.
5. **WPC 2.4 GHz limits and ETA self-declaration process** — UNVERIFIED (search budget exhausted).
6. **LoRa duty cycle**: India 2.5 % (node) per G.S.R. 853(E) [24] constrains uplink rate; gateway function allows 10 %. Confirm no post-2021 amendment.
7. **Exposed stack connector**: ESD robustness and cover design — needs early ESD test on prototype enclosure.
8. **Li-ion outdoors**: temperature range vs charging window; Battery Regulation removability (UNVERIFIED dates).
9. **Fieldbus on baseboard vs separate card**: on baseboard → covered by baseboard EMC/CRA; separate card → another product to certify (EMC DoC, possibly CRA Class I "network interface"/Fieldbus per 2025/2392 [17]).
10. **Class A vs B emissions** — Class B design is advisable for module reuse.
11. All UNVERIFIED test levels in 3.3/3.6/6 must be confirmed from purchased standards before test plans are written.

## 11. Downloaded reference documents
See docs/datasheets/standards/INDEX.md (4 PDFs: 2025/2392, 2026/339, RED summary list, G.S.R. 853(E)). EUR-Lex texts (CRA, 2022/30, Battery Regulation) could not be downloaded — EUR-Lex returned an HTML page to automated requests.

## 12. Sources
[1] https://natlawreview.com/article/cyber-resilience-act-11-september-2026-key-starting-point-reporting-obligations
[2] https://eur-lex.europa.eu/eli/reg/2024/2847/oj
[3] https://www.hsfkramer.com/notes/cybersecurity/2026-posts/cyber-resilience-act-commission-clarifies-important-and-critical-product-categories
[4] https://www.springlex.eu/en/packages/cra/tdpc-regulation/article-2/
[5] https://www.cyberresilienceact.eu/news/cra-standardisation-deadlines-pushed-back-two-months.html
[6] https://www.ibf-solutions.com/en/news-and-knowledge/technical-papers-and-news-on-ce-marking/current-status-of-standardisation-for-the-cyber-resilience-act
[7] https://www.sgs.com/en/news/2025/02/safeguards-02625-eu-harmonizes-en-18031-standards
[8] https://digital.gob.es/content/dam/portal-mtdfp/avance-digital/telecomunicacion-e-infraestructuras-digitales/areas_interes/equipos-telecomunicacion/documents/Guia-aplicacion-EN-18031.pdf
[9] https://lims.bis.gov.in/home_lab_scope/927
[10] https://www.compliancecalendar.in/learn/bis-registration-for-lithium-batteries
[11] https://www.eservices.dot.gov.in/mandatory-testing-certification-telecommunication-equipment-mtcte
[12] https://alephindia.in/tec-notification-new-standard-for-iot-gateways.php
[13] https://www.corpseed.com/law-update/dot-new-tec-standards-iot-gateway-fwa-cpe-underground-telecom-cables-2026
[14] https://www.springlex.eu/en/packages/cra/cra-regulation/article-71/
[15] https://www.springlex.eu/en/packages/cra/cra-regulation/annex-3/
[16] https://www.springlex.eu/en/packages/cra/cra-regulation/annex-4/
[17] Commission Implementing Regulation (EU) 2025/2392 of 28 Nov 2025, OJ L 1.12.2025 — OJ PDF copy https://www.ibf-solutions.com/fileadmin/dateidownloads/commission-implementing-regulation-2025-2392.pdf (saved locally); annex also at https://www.springlex.eu/en/packages/cra/tdpc-regulation/annex-1/ ; official ELI https://eur-lex.europa.eu/eli/reg_impl/2025/2392/oj/eng
[18] https://www.springlex.eu/en/packages/cra/cra-regulation/article-32/
[19] https://www.springlex.eu/en/packages/cra/cra-regulation/article-13/
[20] https://www.european-cyber-resilience-act.com/Cyber_Resilience_Act_Annex_3.html (2022 proposal text, for comparison only)
[21] https://www.springlex.eu/en/packages/cra/cra-regulation/article-14/
[22] https://www.springlex.eu/en/packages/cra/cra-regulation/annex-1/
[23] Commission Delegated Regulation (EU) 2026/339 of 16 Feb 2026, OJ L 29.4.2026, ELI http://data.europa.eu/eli/reg_del/2026/339/oj — OJ PDF copy https://www.ibf-solutions.com/fileadmin/dateidownloads/2026-339-en.pdf (saved locally); Council transmission https://data.consilium.europa.eu/doc/document/ST-6429-2026-INIT/en/pdf
[24] Gazette of India Extraordinary, Part II Sec. 3(i), G.S.R. 853(E), 10 Dec 2021, "Use of Low Power Equipment in the Frequency Band 865-868 MHz for Short Range Devices (Exemption from Licence) Rules, 2021" — https://www.thc.nic.in/Central%20Governmental%20Rules/use%20of%20low%20power%20Equipment%20in%20the%20frequency%20band%20865%20to%20868%20MHz%20for%20Short%20Range%20Devices%20Exemption%20from%20Licence%20Rules,2021.pdf (saved locally); DoT copy https://dotws.cdot.in/sites/default/files/The%20use%20of%20low%20power%20equipment%20in%20the%20frequency%20band%20865-867%20MHz%20for%20short%20range%20devices%20%28Exemption%20from%20License%29%20Rules%2C%202021.pdf (host timed out)
[25] European Commission, RED harmonised standards summary list (generated 13.10.2025) — https://single-market-economy.ec.europa.eu/document/download/b07ec281-8869-434d-ba85-49ae0e206d0f_en?filename=SummaryListForLegislation_generated%2013.10.2025.pdf (saved locally)
[26] European Commission, Harmonised standards — Radio equipment page (latest amendment 4 Sep 2026, Implementing Decision (EU) 2026/2003) — https://single-market-economy.ec.europa.eu/single-market/european-standards/harmonised-standards/radio-equipment_en
[27] In Compliance Magazine, July 2026, "EU harmonized EN EMC standards" — https://digital.incompliancemag.com/issue/july-2026/eu-harmonized-en-emc-standards/
