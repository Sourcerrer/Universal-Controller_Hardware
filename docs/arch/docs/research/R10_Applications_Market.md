# R10 — Applications Survey and Competitive Benchmark (Universal Controller)

Status: COMPLETE WITH GAPS. Web search budget ran out, so some benchmark items are unresearched; see section 8.
Date: 2026-11-14

Scope: applications survey (India first, then global), competitive benchmark including stackable PLC-style
families, derived baseboard IO mix / SKU bundles / protocol list, and common Indian tender requirements, for a
stackable family of individually enclosed DIN-rail modules (controller with IO + fieldbus; 4G + Ethernet + Wi-Fi
module; Wi-Fi + BLE module; LoRa module; each usable standalone).

## 1. Executive summary

1. Best-fit applications for a low-cost MCU-based modular product, in order: water/wastewater incl. JJM, energy sub-metering, DG-set and telecom-tower monitoring, solar PV/PM-KUSUM, MSME machine monitoring/OEE, and utility OEM embeds (compressors, boilers). OCEMS, cold chain and agriculture come next (section 4).
2. JJM's reference architecture matches the module family directly: a LoRa first mile (865-867 MHz) feeding a 4G gateway, MQTT/HTTPS with TLS, OTA updates, 30-day to 2-month local storage and IP67/68 housings [S20]. The national portal ingests HTTPS JSON POST [S21].
3. CPCB OCEMS requires at least 1 year of non-volatile storage, multi-server push without a plant PC, alarms on configuration changes, and remote regulator access with audit [S22].
4. Almost every application needs RS-485 Modbus, 4-20 mA AI and 24 V DI. CAN (J1939) is needed for DG sets. DLMS/IS 15959 matters for utility and DT meters, but the smart-meter DCU and RF-mesh segment is captive to meter OEMs [S24-S26].
5. Recommended baseboard: 6-8 DI (2 counters), 2-4 DO (2 relays), 4 configurable 4-20 mA/0-10 V AI, battery-voltage sense, at least 1 isolated RS-485 (2nd RS-485 + CAN on baseboard or a fieldbus card, decision open), RTC, and storage for at least 1 year (section 6.1).
6. Price floor in India: plain 4G RS-485-to-MQTT gateways list at INR 3,900-7,500 on IndiaMART; USR-M100 with IO costs INR 7,160 + GST [S10, S43]. Global brands cost INR 15-40k (Teltonika TRB145 INR 19,450 in India; InHand IG502 ~INR 25.8k; RUT956 ~INR 37k) [S33, S42, S35].
7. Stackable competitors (Arduino Opta ~INR 12-16k plus ~INR 12k per expansion, Revolution Pi, PLCnext ~INR 1 lakh, LOGO!) offer expansion modules but no enclosed cellular/LoRa radio modules that also run standalone. This is the main whitespace for the UC [S48, S7, S8, S13].
8. Ten SKU bundles are proposed, from the 4G meter gateway at INR 6-9k to the full multi-radio unit at INR 16-22k (section 6.2).
9. Tenders ask for IP65-68, at least 1 year (CPCB/CWC) or 30-60 days (JJM) of storage, solar power with surge/lightning protection, HTTP/MQTT with TLS, OTA, and a 5-year warranty with O&M [S20, S22, S45]. MTCTE applies to IoT gateways (Phase III), and TEC 33010:2025 sets the IoT Gateway generic requirements [S30, S31].
10. Key risks: the IndiaMART price floor, the cost of per-module enclosures and certification, IP67 needs for JJM, -48 V input for telecom, and the LoRa gateway-vs-point-to-point decision at a INR 1,000 card cost (section 8).

## 2. Method, conventions and exchange rate

- Exchange rate used: USD 1 = INR 93.9 (mid-market ~2026-11-08; range 93.7-94.9 in the first half of Nov 2026) [S1]. EUR/GBP/AUD conversions are NOT re-checked; where a non-USD price is given it is converted at approximate rates marked "approx" (EUR 1 ~ INR 105-110, GBP 1 ~ INR 120-125, AUD 1 ~ INR 60-62: UNVERIFIED).
- Cost convention: finished cost = BOM x 1.4 (product-owner decision).
- Prices are web-listing prices (retail/reseller, mostly excl. tax unless stated), not quotes. IndiaMART/TradeIndia prices are seller listings, GST often excluded.

## 3. Applications survey

### 3.0 Primary-source notes (working; consolidated table in 3.1)

- JJM (rural water, Jal Jeevan Mission) Technical Expert Committee report on measurement and monitoring (2021) [S20]:
  - Communication module / RTU minimum spec: battery or mains powered; cellular (GSM/GPRS, 4G/LTE, 5G, NB-IoT), LoRa or other RF, Wi-Fi/Ethernet; LoRa RTU range 400-1000 m; telemetry via MQTT / AMQP / HTTPS with TLS/DTLS/AES; 15-min transmission for mains-powered RTU, 2x/day for battery RTU; memory card storing >= 30 days; IP67/IP68 body; remote config of reporting interval + OTA firmware; certifications CE / FCC / "CISPER" (sic).
  - Gateway minimum spec: power supply or solar with battery; LoRa/Wi-Fi etc. to nodes, cellular or Wi-Fi/Ethernet to cloud; hardware AES 128/192/256; IP68 casing; 15-min (mains) / 4-hour (solar) transmission; memory card storing >= 2 months; OTA.
  - Recommended architecture: LoRa (865-867 MHz licence-free band or licensed LoRaWAN operator) first mile + 4G gateway; RTU "should ideally be 4G-based"; devices in IP65-68 rugged enclosures inside pump houses/ESRs; solar + battery where no mains; sensors: bulk flow meters, ESR level, pressure (tail end), chlorine, pump status/energy.
  - "Implementation agencies may follow global standards in case Indian standards are not defined (such as CE/FCC for IoT devices)".
- JJM national IoT portal (ejalshakti IoT Web, Operational Manual for IoT data integration, 18 Feb 2026) [S21]: vendors/agencies register sensors (flow meter, chlorine, pH, turbidity, level...) and push data by HTTPS Web API POST (JSON, API key in header) to ejalshakti.gov.in/IoT_API. So the gateway must be able to post JSON over HTTPS REST, not only MQTT.
- CPCB 1st Revised Guidelines for Continuous Emission Monitoring Systems (Aug 2018) [S22]: analyser/DAS must transmit raw and validated data to SPCB/CPCB central server; remote system access from central server for log files; simultaneous multi-server transmission "without intermediate PC or plant server"; alarm to server on configuration or calibration change; log of all operational information; non-volatile memory for >= 1 year of continuous data; plant-level data viewing/retrieval via Ethernet, Modbus and USB. Remote access to the industry data logger must be available to CPCB/SPCB at any time with auditing (CPCB presentation, [S23]). Analysers typically output 4-20 mA or Modbus to the DAS.
- Smart metering (RDSS/AMI): IS 16444 (smart meters) + IS 15959 Parts 1-3 (DLMS/COSEM data exchange; Part 3 = CT/PT-operated meters incl. DT meters). Cellular smart meters carry a plug-in NIC that is "compatible with 4G and fall back to 2G", with the meter powering the NIC; communication per IS 16444 Part 2 cl. 8.3; key management per IS 15959 Parts 2/3 [S24]. CEA AMI Interoperability Report (Jan 2025): RF, PLC and cellular are all specified for RDSS; RF-mesh needs intermediate gateways/DCUs and "most of the RF Mesh solutions are proprietary" [S25]. BIS scheme of inspection for IS 16444 requires re-test on any change of RF module model/supplier and IS 15959 protocol testing every two years [S26]. Implication: the DCU/RF-mesh gateway market is locked to meter OEMs' proprietary stacks; a general-purpose gateway fits better as a DLMS-reading sub-metering/DT-monitoring gateway (DLMS client over RS-485/optical) than as a utility DCU.
- Telecom towers: DoT's Tower Monitoring System monitors grid/DG/battery status at BTS sites, plus fuel and temperature sensing, cameras and geo-tagging [S27]. Typical RMS I/O (vendor RFQ example): AIs for 2 battery currents, load current, bus voltage, 2 battery voltages, 3 temperatures, 1 fuel level; DI for SPD status; alarms for DG on/off, mains on/off, door, fire/smoke [S28]. Site power controllers (IPMS) expose RS-232 for remote monitoring and RS-485 for inter-site polling [S29]. No published TEC/DoT RMS hardware specification was found (UNVERIFIED).

### 3.0b Telecom certification note
- MTCTE (TEC, Indian Telegraph (Amendment) Rules 2017): "IoT (Internet of Things) Gateway" is a Phase-III product with mandatory certification from 1 Jan 2024 per a DoT annexure (date was extended several times from Jul 2022) [S30]. TEC 33010:2025 "Standard for Generic Requirements - IoT Gateway" was notified in the Gazette on 23 Jan 2026 [S31]. Whether a product with a pre-certified cellular module still needs its own MTCTE certificate as an "IoT Gateway" must be confirmed with a CAB (UNVERIFIED; current status on the MTCTE portal not checked).

### 3.1 Application table

Legend: source tags [Sxx] where a primary/vendor source backs the row; **E** = engineering estimate from typical installations, not verified against a source in this study (treat as UNVERIFIED). Price sensitivity: H = buyer compares against INR 4-8k Indian 4G Modbus gateways [S10, S43]; M = system/tender sale where the box is a small share; L = premium, spec-driven. Count notation: DI/DO/AI.

| # | Application (India first) | Field interfaces and typical counts | Wireless / uplink | Field / cloud protocols | Power | Environment | Special compliance / tender | Volume / price sensitivity (India) |
|---|---|---|---|---|---|---|---|---|
| 1 | Energy monitoring / sub-metering (factories, commercial) | 1-2 RS-485 (8-32 meters per bus), 0-2 DI (pulse), Ethernet optional | 4G or Wi-Fi uplink; LoRa for spread meters (UC100-class nodes [S36]) | Modbus RTU/TCP; DLMS/COSEM (IS 15959) for utility-grade/DT meters [S24]; MQTT/HTTPS | 230 V AC panel or 24 V DC | Indoor panel, 0-55 C (E) | None mandatory beyond EMC/safety; DLMS key handling if reading utility meters [S24] | Very high volume, H |
| 2 | DG-set monitoring (telecom, industrial, commercial) | CAN J1939 from ECU (newer engines), RS-485 Modbus from DG controller, 2-4 DI (run, fault), 1-2 AI (fuel level 4-20 mA / resistive), battery voltage (E) | 4G (remote sites) | J1939, Modbus RTU; MQTT/HTTPS | 12/24 V DG battery (cranking dips) | Canopy, vibration, -10..60 C (E) | Telecom-tower RMS buyer specs (no public TEC hardware spec found) [S27] | High, H |
| 3 | Telecom tower RMS / energy management | ~8-10 AI (battery currents/voltages, bus V, 3 temps, fuel) + DI alarms (DG on/off, mains, door, smoke, SPD) [S28]; RS-232/485 to IPMS/SMPS [S29] | 4G, dual SIM (E) | Modbus, SNMP (E); MQTT/HTTPS | -48 V DC site bus (needs isolated -48 V input or DC-DC) (E) | Shelter/outdoor cabinet, hot | Operator RFQs; DoT TMS [S27] | Large installed base (~ lakhs of towers) but consolidated buyers (tower cos), M |
| 4 | Solar PV plant monitoring (rooftop C&I, utility, PM-KUSUM pumps) | 1-2 RS-485 (inverters, energy meter, WMS), 2-4 AI (pyranometer 4-20 mA, temps), 2-4 DI (breaker status) (E) | 4G; Ethernet in larger plants | Modbus RTU/TCP, SunSpec (E); MQTT/HTTPS to SCADA/portal | 24 V DC from aux/UPS or solar + battery | Outdoor kiosk, hot, dusty | PM-KUSUM remote monitoring architecture referenced in tender docs (not opened) | High volume, H for rooftop, M for utility |
| 5 | Water / wastewater (JJM, AMRUT, STP/ETP pumping) | Flow meters (pulse or RS-485 Modbus), level (4-20 mA), pressure (4-20 mA), chlorine/pH/turbidity (4-20 mA/Modbus), pump status/energy [S20]; typical 2-4 AI, 2-4 DI, 1-2 DO, 1 RS-485 | LoRa first-mile (865-867 MHz) + 4G gateway; Wi-Fi where BharatNet exists [S20] | Modbus; MQTT/AMQP/HTTPS with TLS; JJM portal HTTPS JSON POST [S20, S21] | Mains or solar + battery; battery RTU 2 reports/day [S20] | Pump house/ESR, IP65-68 required [S20] | JJM: IP67/68, 30-day/2-month storage, OTA, CE/FCC [S20]; CWC: 1-year storage, 5-year warranty+O&M [S45] | Very high volume (7.5 lakh villages scope [S20]), tender-driven, H |
| 6 | Smart agriculture / irrigation | Soil moisture, weather, valve DO, pump DI; mostly battery LoRa nodes (E) | LoRa nodes + 4G gateway | LoRaWAN; MQTT | Li-ion/solar for nodes | Outdoor, IP67 | None specific | Volume potential but extremely price-sensitive, H |
| 7 | Environmental: CEMS / effluent (OCEMS) data logging to CPCB/SPCB | Analyser outputs 4-20 mA or Modbus [S22]; 4-8 AI, 2-4 DI (analyser status), RS-485 (E) | 4G / Ethernet | Modbus; CPCB server push (multi-server), remote log access [S22] | 230 V AC | Analyser shelter | CPCB CEMS guidelines: >= 1-year NV memory, multi-server push, config-change alarms, regulator remote access with audit [S22, S23] | Mandatory for 17 categories of highly polluting industries (E: count not verified), M |
| 8 | Cold chain / pharma | Temperature/RH probes (RS-485 or NTC/PT100), door DI, compressor status (E) | 4G / Wi-Fi; BLE loggers | Modbus; MQTT/HTTPS | Mains + backup battery | Cold rooms, reefer trucks | 21 CFR Part 11 / GDP audit trails for pharma (E) | M |
| 9 | HVAC / BMS | BACnet MS/TP (RS-485), BACnet/IP, Modbus; DI/DO for AHU status (E) | Ethernet / Wi-Fi | BACnet, Modbus; MQTT/REST | 24 V AC/DC | Plant rooms | None specific | M; dominated by BMS OEMs |
| 10 | Machine monitoring / OEE | 4-8 DI (run, count, alarm), 1-2 AI (current CT), RS-485/Ethernet to PLCs (E) | Wi-Fi / Ethernet / 4G | Modbus TCP, OPC UA (larger), MQTT | 24 V DC panel | Factory floor | None | High volume in MSME clusters, H |
| 11 | Predictive maintenance (vibration, temperature) | Vibration sensors via RS-485/IEPE (high-rate sampling beyond MCU-class ADCs) (E) | Wi-Fi/BLE/4G | Modbus; MQTT | 24 V DC | Factory | None | Niche, L; better served by dedicated sensors |
| 12 | Street lighting (CCMS) | Contactor DO, energy meter RS-485, door/phase DI (E) | 4G / RF mesh / LoRa | Modbus, DLMS; MQTT | 230 V AC feeder pillar | Outdoor feeder pillar | EESL-style CCMS tenders (not opened, UNVERIFIED) | M |
| 13 | EV charging | OCPP is in the charger itself; gateway role limited to site energy meter/load management (E) | 4G / Ethernet | OCPP (in charger), Modbus | AC | Outdoor | BIS/CEA charger rules apply to charger, not gateway (E) | Low fit |
| 14 | City gas / oil & gas RTUs | Pressure/temperature 4-20 mA, flow computer RS-485, valve DI/DO; hazardous-area certification often needed (E) | 4G, VSAT | Modbus, DNP3/IEC 60870-5-104 (E) | Solar + battery | Hazardous zones | PNGRB/PESO approvals (UNVERIFIED) | M-L; certification barrier |
| 15 | Distribution-transformer monitoring | DT meter (DLMS, IS 15959 Part 3) over RS-485/optical, oil temp/level AI, door DI [S24] | 4G (2G fallback), RF mesh [S25] | DLMS/COSEM; HES integration | Tapped from LT side | Pole/plinth outdoor, IP65+ | RDSS/IS 16444/15959; BIS SIT re-test on RF module change [S26] | Large RDSS volume but meter-OEM-captive, M |
| 16 | Smart-metering DCU / NAN gateway | RF mesh to meters (proprietary stacks) [S25] | RF mesh + 4G | DLMS, proprietary mesh | Pole | Outdoor | IS 16444, CEA interoperability [S25, S26] | Captive to AMISP/meter OEMs; low fit |
| 17 | Fuel and tank monitoring | Level probe 4-20 mA/RS-485, 1-2 DI (lid/theft) (E) | 4G | Modbus; MQTT | 12/24 V vehicle/DG or solar | Outdoor | None specific | M |
| 18 | Compressors / boilers / utilities | Controller RS-485 Modbus, 2-4 AI (pressure, temp), DI (run/trip), energy meter (E) | 4G / Wi-Fi | Modbus; MQTT | 24 V/230 V | Plant room | IBR for boilers concerns the boiler, not the logger (E) | High volume via OEMs, H/M |
| 19 | Smart buildings (multi-utility) | Energy/water/DG meters on RS-485, BACnet, LoRa sensors (E) | Wi-Fi / Ethernet / LoRa | Modbus, BACnet, LoRaWAN; MQTT | AC | Indoor | None | M |
| 20 | Retail refrigeration | Case-controller RS-485 (Modbus), temperature probes, door DI (E) | 4G / Wi-Fi | Modbus; MQTT | AC | Indoor | Food-safety logging (E) | M, chain-store volumes |
| 21 | Railways (station/utilities, signalling-adjacent monitoring) | DI/AI for point-machine/track-circuit/power monitoring (E) | 4G | Modbus, proprietary | 24/110 V DC | Trackside, harsh EMC | RDSO approval needed (UNVERIFIED) | Low fit for v1; long approval cycle |

## 4. Application ranking

Scoring (1-5 each): fit to an MCU-class modular product (low data rate, Modbus/4-20 mA/DI centric), India volume, buyer access (fragmented SMEs/SIs vs captive OEMs), and tender/compliance burden (5 = light). Weighted judgement, not a market-sized model.

| Rank | Application | Fit | Volume | Access | Compliance | Notes |
|---|---|---|---|---|---|---|
| 1 | Water / wastewater incl. JJM | 5 | 5 | 4 | 3 | LoRa node + 4G gateway is exactly the JJM reference architecture [S20]; needs IP67/68 housing option and HTTPS JSON push [S21] |
| 2 | Energy monitoring / sub-metering | 5 | 5 | 5 | 5 | RS-485 Modbus + 4G/Wi-Fi; lowest-cost SKU; DLMS read as upsell |
| 3 | DG-set + telecom tower monitoring | 5 | 4 | 3 | 4 | CAN J1939 + RS-485 + DI/AI; -48 V input option needed for towers |
| 4 | Solar PV / PM-KUSUM pump monitoring | 4 | 5 | 4 | 4 | RS-485 inverters + AI for weather; solar-powered |
| 5 | Machine monitoring / OEE (MSME) | 5 | 4 | 5 | 5 | DI counters + Modbus; Wi-Fi SKU |
| 6 | Compressors / boilers / utilities (OEM embed) | 5 | 4 | 4 | 5 | OEM white-label opportunity |
| 7 | Environmental OCEMS data logger | 4 | 3 | 4 | 2 | 1-year storage + multi-server push + audit trail [S22] |
| 8 | Cold chain / retail refrigeration | 4 | 3 | 4 | 4 | BLE/LoRa sensors + 4G |
| 9 | Smart agriculture | 4 | 4 | 3 | 5 | LoRa node standalone on Li-ion; very price-sensitive |
| 10 | Street lighting, fuel/tank, smart buildings, HVAC/BMS | 3-4 | 3 | 3 | 4 | BACnet support needed for BMS |
| 11 | DT monitoring | 3 | 4 | 2 | 2 | Meter-OEM captive [S25] |
| 12 | Oil & gas RTU, railways, EV charging, smart-meter DCU, predictive maintenance | 1-3 | 2-3 | 1-2 | 1-2 | Certification barriers or wrong compute class |

## 5. Competitive benchmark

### 5.1 Findings logged so far (working notes; consolidated table follows in 5.2 when complete)

- Teltonika TRB245: LTE Cat4 gateway, 3 configurable I/O (DI 0-6 V low / 8-30 V high; open-collector out 30 V/300 mA), 1 analog in 0-30 V, RS232/RS485, 1x RJ45 10/100, dual SIM, GNSS [S2]. Price: EUR 174 excl. VAT (Discomp CZ), EUR 170 incl. VAT (Buerklin DE) -> ~INR 18-19k at EUR1~107 (approx) [S3,S4]. Reseller lists differ on I/O (2 DI+1 DO vs 3 configurable): treat datasheet as authoritative.
- Teltonika TRB145 (datasheet, 2023): LTE Cat 1 (3G/2G fallback), 1x RS485, 2 configurable I/O on the power connector (DI 0-5 V low / 8-30 V high; open-collector out 30 V/300 mA), no Ethernet port in use (1 RJ45 not listed), single SIM; ARM Cortex-A7 1.2 GHz, 128 MB RAM, 512 MB flash, RutOS (OpenWrt), Modbus RTU master/TCP, MQTT, DNP3; 9-30 VDC, <5 W; aluminium, 74.5x25x64.4 mm, DIN rail; -40..75 C, IP30; CE/RED, EAC, RoHS [S32]. Price: INR 19,450 (thinkrobotics.com, India, 2026-11 listing), EUR 131.20 (arvutitark.ee), GBP 162.81 excl. VAT (controltech.uk) [S33].
- Teltonika RUT956 (datasheet v1.3, 2023): LTE Cat 4, dual SIM, GNSS, Wi-Fi 4 2.4 GHz, 4x RJ45 10/100 (1 WAN + 3 LAN), RS232 (DB9) + RS485; I/O: 1 dry DI, 1 isolated DI 0-30 V, 1 AI 0-24 V, 1 non-isolated DI, 2 open-collector DO, 1 SPST relay (40 V/4 A); MediaTek MIPS 24Kc 580 MHz, 128 MB RAM; 9-30 VDC (+passive PoE 9-50 V), <7 W; aluminium + plastic, 110x50x100 mm, DIN rail; -40..75 C, IP30 [S34]. Price: KES 51,275 excl. tax (cloudone.co, Kenya) ~ USD 397 at KES~129/USD (UNVERIFIED rate) [S35].
- Milesight UC300: 4 DI + 2 DO (relay 3 A), 1 RS232 + 1 RS485, AI variants (2x 4-20 mA, 2x 0-10 V, 2x PT100), -20..60 C, 93x70x22 mm; LoRaWAN or 4G variants [S5]. Prices: EUR 125 (EU868 LoRaWAN, Invibit/Elmark); AUD 484 +GST (4G variant, PB Tech) [S6].
- Milesight UC100 (LoRaWAN RS485-to-LoRaWAN controller): reads up to 32 Modbus RTU slaves (16 per some resellers), 1200-115200 bps, 120 ohm termination switch, 5-24 VDC or USB-C 5 V, IP30, -20..60 C [S36]. Prices: USD 52 (US reseller), AUD 69 excl. GST (AU) [S36].
- Milesight UG65 (8-ch LoRaWAN gateway, SX1302, quad-core, >2,000 nodes, IP65, 1x GbE with 802.3af/at PoE, Wi-Fi, optional 4G): EUR 388.49 (aio.lv, Latvia, listing valid to 2026-07), AUD 866.99 +GST (PB Tech), ZAR 6,800 non-LTE (ComX) [S37].
- Moxa UC-2100 (UC-2101/2111-LX): Armv7 Cortex-A8 600 MHz, 512 MB DDR3, 8 GB eMMC, Moxa Industrial Linux 1 (Debian 9, EOL 2027); 1-2x 10/100 RJ45, 1-2 serial RS-232/422/485; -10..60 C (wide-temp -T variants) [S38]. Prices: NZD 835 excl. GST (UC-2101-LX), NZD 983 (UC-2111-LX) (PB Tech NZ); PHP 26,569 excl. VAT (RS PH, UC-2101-LX) ~ INR 39-45k (approx, UNVERIFIED rates) [S38].
- Advantech WISE-4012 (Wi-Fi 2.4 GHz IO module): 4 universal inputs (16-bit) + 2 DO; Modbus/TCP, HTTP, MQTT, RESTful JSON API; 10-30 VDC. Prices: USD 164.70 MSRP (US reseller), USD 209.99 (CDW), GBP 171.13 excl. VAT (RS UK). WISE-4060: 4 DI + 4 relay, Modbus/TCP, REST, MQTT; price not found [S39].
- Advantech ECU-1051 (RTU/edge gateway): TI Cortex-A8 600 MHz, 256 MB DDR3L, 512 MB NAND; 2x 10/100 LAN, 2x RS-232/485 (isolated option); mini-PCIe for 4G (dual SIM); EdgeLink: Modbus RTU/TCP master+slave, DNP3 client/server, IEC 61850 MMS/GOOSE (paid licence). Price AUD 321 excl. GST (PB Tech AU), NZD 436 [S40].
- Siemens SIMATIC IOT2050: Basic = TI AM6528 GP, 1 GB DDR4, 1x RS-232/422/485, Ethernet, USB, 24 V nominal, 0..50 C; Advanced = AM6548 HS (secure boot), 2 GB, Arduino-shield + mPCIe expansion. Prices: Basic GBP 303 excl. VAT (RS UK), EUR 290.88 excl. VAT (RS DE); Advanced SGD 971.82 excl. GST (RS SG) [S41].
- InHand IG502 (edge gateway): 2x 10/100 Ethernet, optional 4 DI + 4 DO (isolated), 1x RS-232 + 1x RS-485 (or 2x RS-485), ARM Cortex-A8 600 MHz, 512 MB RAM, 8 GB eMMC, LTE Cat 1/Cat 4 by region, Wi-Fi/GPS options, Python apps, DeviceSupervisor with "80+ industrial protocols". Price USD 274.99 (IG502-FQ33-IO, embeddedworks.net, US) [S42].
- USR IoT USR-M100 (remote-IO edge gateway, expandable): onboard 2 AI (4-20 mA) + 2 DI + 2 relay DO, 2x RS232/RS485, 4G and Ethernet SKUs; expands over RS-485 with USR-IO modules (e.g. IO8000 8 DI, IO0080 8 relay). Prices: INR 7,160 + 18% GST (4G+ETH, robu.in), INR 5,990 (IndiaMART), EUR 114.33 excl. VAT (SOS Electronic) [S43]. This is the closest low-cost "expandable" competitor sold in India.
- Four-Faith F2x14 (cellular IP modem/RTU): 1x RS232/RS485, 5 I/O, 15 kV ESD on serial ports; no price found [S44].
- Arduino Opta datasheet [S46]: three variants Lite / RS485 / WiFi; all have 10/100 Ethernet; RS485 half-duplex on RS485 and WiFi variants; Wi-Fi b/g/n + BLE on WiFi variant only; 8 analog/digital inputs, 4 NO relays 10 A/250 VAC; STM32H747XI (M7 480 MHz + M4) MCU + ATECC608B secure element; 12-24 VDC; proprietary side expansion port for auxiliary modules; certifications cULus, ENEC, FCC, CE, CB, UKCA. Architecturally the closest analogue to the UC concept (MCU + secure element + side-click expansions), but no cellular/LoRa module.
- Arduino Portenta Machine Control (AKX00032) datasheet [S47]: STM32H747XI + NXP SE050 secure element; 24 VDC +/-20 %; 8 DI (0-24 V), 8 DO (24 V high-side), 12 programmable DIO, 3 AI (0-10 V / 4-20 mA / NTC), 4 AO, 3 temperature channels (thermocouple J/K, PT100), 2 ABZ encoders, CAN (TJA1049), RS-232/422/485 configurable, Ethernet, USB-A, Wi-Fi/BLE. Price: see the Arduino store line below [S48].
- Arduino official store prices (fetched 2026-11-14) [S48]: Opta Lite USD 128.35, Opta RS485 USD 141.10 (EUR 145.80 on EU store), Opta WiFi USD 169.15 (EUR 175.10); Portenta Machine Control USD 300.00 (EUR 201.37 on EU store).
- RAKwireless official store prices (fetched 2026-11-14) [S49]: WisGate Soho Lite RAK7266S (8-ch indoor LoRaWAN, no LTE) USD 99, with LTE USD 165; WisGate Edge Lite 2 Verizon (RAK7268CV2, LTE) USD 299; WisGate Edge Pro RAK7289V2 (outdoor 8/16-ch) USD 382 (no LTE) / 422 (LTE); WisGate Connect Industrial (Raspberry Pi CM4, LoRa/Zigbee/WisBlock expansion) from USD 301; WisBlock Starter Kit (RAK19007 base + RAK4631 nRF52840+SX1262 core) USD 24.99; RAK3172 LoRaWAN module USD 7.99; LTE add-on module for WisGate Connect (EG95) USD 69.90. WisBlock is the closest "modular" analogue at board level (base board + core + IO/sensor slots), but it is a dev/OEM platform, not an enclosed DIN-rail product.
- Arduino Opta RS485 (AFX00001): 12-24 V, relay outputs, analog/digital inputs, RS485; expansions D1608E (16 DI/AI + 8 relay) approx USD 130-137 (DigiKey/Arduino launch), A0602 EUR 120 (Kubii, pre-order) [S7]. Base unit prices: see the Arduino store line above [S48].
- Revolution Pi Connect 4: RS UK GBP 422.72 excl. VAT (32 GB/4 GB), GBP 442.44 (WiFi) [S8]. RevPi Core price not found (UNVERIFIED).
- Dragino RS485-LN (LoRaWAN RS485 node): USD 51-56 (reach.dog, DigiKey via Zenode), EUR 46.5 excl. VAT (exp-tech.de) [S9]. LG308N price not found.
- Robustel R1520 (lite LTE gateway): 1x RS232 + 1x RS485 (or 2x RS232), 5x LAN, dual SIM, GPS; EG5120 edge gateway: 2x Ethernet, 2x RS232/RS485 (software configurable), 2x DI/DO; no public prices found (distributor quote) [S11].
- Norvi (Sri Lanka) IIOT-AE02-I: 8 DI 24 V, 6x 4-20 mA AI, 2 transistor out, RS-485, WiFi/BT, ESP32; AE02-V listed USD 204.36 [S12]. Industrial Shields ESP32 PLC 14: EUR 109 (Ethernet, WiFi, RS485); ESP32 PLC 21 EUR 239; ESP32 PLC 38AR EUR 319 (10 AI, 8 relays) [S12].
- Phoenix Contact AXC F 2152 (PLCnext, Axioline F stackable): GBP 851 excl. VAT (RS UK), ~EUR 929 (Buerklin); Siemens LOGO! 230RCE EUR 250 (Mouser DE) [S13]. WAGO PFC100 price not found (UNVERIFIED).
- Indian 4G Modbus gateway listings (IndiaMART/TradeIndia, accessed 2026-11-14, price excl/incl GST unclear): Ethicstech Modbus 4G IoT gateway INR 3,900; Augmatic 4G RS485 MQTT gateway INR 4,777; Aliter RTU-to-MQTT GPRS gateway INR 7,000; GISpec 4G Modbus RTU->MQTT INR 7,500 (+18% GST on TradeIndia); Ithing Mechatronics 4G Modbus gateway INR 27,000; Pyrotron 4G RS485 gateway INR 31,000; Satlink 4G data logger IoT gateway Modbus TCP/RTU INR 46,000; Arrow Touch 4G RTU INR 1,80,000 [S10].

### 5.2 Consolidated benchmark table

INR at USD 1 = 93.9 [S1]; EUR at ~107, GBP ~123, AUD ~61 (approx, UNVERIFIED). Listing prices, excl. tax unless stated. "Mod" = stackable or expandable architecture.

| Product | Class | IO (DI/DO/AI) | Field interfaces | Radios | CPU / OS | Power | Mount / IP | Certs | Price (source) | ~INR | Mod |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Teltonika TRB145 | Cat-1 RS-485 gateway | 2 configurable DI/DO | 1 RS-485 | LTE Cat 1 (3G/2G) | Cortex-A7, RutOS | 9-30 V | DIN, IP30, -40..75 C | CE/RED, EAC | INR 19,450 (IN retail) [S33] | 19,450 | No |
| Teltonika TRB245 | Cat-4 gateway | 3 cfg I/O + 1 AI | RS-232, RS-485, 1 Eth | LTE Cat 4, dual SIM, GNSS | RutOS | 9-30 V | DIN | CE | EUR 174 [S3] | ~18,600 | No |
| Teltonika RUT956 | Cat-4 router | 3 DI, 3 DO (1 relay), 1 AI | RS-232, RS-485, 4 Eth | LTE Cat 4 dual SIM, Wi-Fi 4, GNSS | MIPS 580 MHz, RutOS | 9-30 V | DIN, IP30 | CE | KES 51,275 [S35] | ~37,000 (UNVERIFIED rate) | No |
| Robustel R1520 / EG5120 | LTE router / edge gateway | EG5120: 2 DI/DO | R1520: RS-232+RS-485, 5 LAN; EG5120: 2 Eth, 2 serial | LTE dual SIM | Linux | - | DIN | - | not public [S11] | - | No |
| Milesight UC300 | IO controller | 4 DI, 2 relay, 2x4-20 mA / 0-10 V / PT100 | RS-232, RS-485 | LoRaWAN or 4G | MCU | - | -20..60 C | - | EUR 125 (LoRaWAN) [S6] | ~13,400 | No |
| Milesight UC100 | RS-485-to-LoRaWAN node | - | RS-485 (32 slaves) | LoRaWAN | MCU | 5-24 V | IP30 | - | USD 52 [S36] | ~4,900 | No |
| Milesight UG65 | LoRaWAN gateway | - | 1 GbE PoE | 8-ch LoRa, Wi-Fi, opt 4G | quad-core Linux | PoE / DC | IP65 | - | EUR 388 [S37] | ~41,500 | No |
| Moxa UC-2101-LX | Arm computer | - | 1 Eth, 1 serial | none | Cortex-A8, Debian 9 (EOL 2027) | - | DIN | - | PHP 26,569 [S38] | ~42,000 (approx) | No |
| Advantech WISE-4012 | Wi-Fi IO module | 4 UI, 2 DO | - | Wi-Fi 2.4 GHz | MCU | 10-30 V | - | - | USD 164.70 [S39] | ~15,500 | No |
| Advantech ECU-1051 | RTU gateway | - | 2 Eth, 2 RS-232/485 | 4G via mPCIe | Cortex-A8 Linux | - | DIN | - | AUD 321 [S40] | ~19,600 | No |
| Siemens IOT2050 Basic | Edge gateway | - | 1 serial, 2 Eth | none | AM6528, Linux | 24 V | DIN, 0..50 C | - | EUR 290.88 [S41] | ~31,100 | Arduino shield / mPCIe (Adv.) |
| InHand IG502 | Edge gateway | 4 DI, 4 DO (opt) | 2 Eth, RS-232+RS-485 | LTE Cat 1/4, opt Wi-Fi | Cortex-A8, Python | - | DIN | - | USD 274.99 [S42] | ~25,800 | No |
| USR-M100 | Remote-IO gateway | 2 DI, 2 relay, 2 AI (4-20 mA) | 2 RS-232/485, Eth | 4G (SKU) | - | - | DIN | - | INR 7,160 + GST [S43] | 7,160 | Yes (IO over RS-485) |
| Four-Faith F2x14 | Cellular RTU modem | 5 I/O | 1 RS-232/485 | cellular | - | - | - | - | n/a [S44] | - | No |
| Arduino Opta (Lite/RS485/WiFi) | Micro PLC | 8 AI/DI, 4 relays 10 A | Eth; RS-485 (RS485/WiFi) | Wi-Fi+BLE (WiFi) | STM32H747 + ATECC608B | 12-24 V | DIN | cULus, CE, FCC, ENEC, UKCA | USD 128 / 141 / 169 [S48] | 12,000-15,900 | Yes (side expansions, ~USD 130 each [S7]) |
| Arduino Portenta Machine Control | Machine controller | 8 DI, 8 DO, 12 DIO, 3 AI, 4 AO, 3 temp, 2 enc | CAN, RS-232/422/485, Eth | Wi-Fi/BLE | STM32H747 + SE050 | 24 V | DIN | - | USD 300 [S48] | ~28,200 | No |
| Revolution Pi Connect 4 | RPi CM4 PLC | via expansion | Eth, serial | opt Wi-Fi | CM4 Linux | 24 V | DIN | - | GBP 422.72 [S8] | ~52,000 | Yes (PiBridge side modules) |
| Dragino RS485-LN | RS-485 LoRaWAN node | - | RS-485 | LoRaWAN | MCU | - | - | - | USD 51-56 [S9] | 4,800-5,300 | No |
| RAKwireless WisGate Soho Lite / Edge Pro / WisBlock | LoRaWAN gateways / modular OEM | - | Eth | LoRa 8/16-ch, opt LTE | Linux / nRF52840 | - | indoor / outdoor | - | USD 99 / 165 (LTE) / 422; WisBlock kit USD 24.99 [S49] | 9,300 / 15,500 / 39,600; 2,350 | WisBlock yes (board level) |
| Norvi IIOT-AE02 | ESP32 DIN controller | 8 DI, 6x 4-20 mA, 2 DO | RS-485 | Wi-Fi/BT | ESP32 | 24 V | DIN | - | USD 204.36 [S12] | ~19,200 | No |
| Industrial Shields ESP32 PLC 14 / 38AR | ESP32 PLCs | up to 10 AI, 8 relays | Eth, RS-485 | Wi-Fi | ESP32 | 24 V | DIN | - | EUR 109 / 319 [S12] | ~11,700 / ~34,100 | Family sizes |
| Phoenix Contact AXC F 2152 | PLCnext + Axioline F | via Axioline modules | Eth | none | Linux PLCnext | 24 V | DIN | - | GBP 851 [S13] | ~105,000 | Yes (stacked bus) |
| Siemens LOGO! 230RCE | Logic module | 8 DI, 4 relay | Eth | none | - | 230 V | DIN | - | EUR 250 [S13] | ~26,800 | Yes (expansion modules) |
| WAGO PFC100 / CC100, Siemens ET 200SP | Stackable PLC/IO | modular | Eth fieldbus | - | - | 24 V | DIN | - | not found (UNVERIFIED) | - | Yes |
| Indian 4G Modbus gateways (Ethicstech, Augmatic, Aliter, GISpec, Ithing, Pyrotron, Satlink, Arrow Touch) | RS-485-to-MQTT 4G gateways / RTUs | mostly 0-few IO | RS-485 | 4G/GPRS | - | - | - | - | INR 3,900 / 4,777 / 7,000 / 7,500 / 27,000 / 31,000 / 46,000 / 1,80,000 [S10] | as listed | No |

Observations:
- Indian-market price floor for a plain "RS-485 to MQTT over 4G" box is INR 3,900-7,500 (IndiaMART) [S10]; USR-M100 with IO at INR 7,160 + GST [S43]. Global brand gateways sit at INR 15-40k [S33, S3, S42].
- Stackable/expandable products with an MCU + secure element and side-click expansions exist only at Western-PLC prices (Opta ~INR 12-16k base + ~INR 12k per expansion [S48, S7]); no competitor found offers individually enclosed cellular / Wi-Fi / LoRa radio modules that click onto an IO controller AND also run standalone.
- LoRa nodes cost INR ~4,800-5,300 (UC100, RS485-LN) [S36, S9]; LoRaWAN gateways start at USD 99 indoor / ~USD 400 outdoor [S49].

## 6. Derived recommendations

### 6.1 Baseboard (controller) IO mix
Derived from rows 1-5 and 7 of 3.1, from the telecom RMS IO list [S28], from the JJM sensor set [S20] and from competitor IO counts (UC300, Opta, USR-M100, Norvi):
- 6-8 DI, 24 V-tolerant, 2 of them high-speed pulse/counter inputs (flow meters, energy pulses, OEE counts); dry-contact capable.
- 2-4 DO: 2 relays (pump/DG start, alarms) + 2 open-drain/high-side 24 V.
- 4 AI, configurable 4-20 mA / 0-10 V (level, pressure, fuel, pyranometer, analysers), >= 16-bit effective for CEMS-grade use; optional 2 RTD (PT100/PT1000) via configurable inputs.
- Supply/battery voltage monitoring channel (DG battery, solar battery; CWC tender asks for battery-voltage monitoring [S45]).
- Fieldbus: 1x isolated RS-485 minimum (2x preferred: one for meters, one for slave/inverter or Modbus slave to SCADA); 1x CAN/CAN-FD for J1939 DG ECUs. Decide whether these live on the baseboard (lowest cost for the energy/DG SKUs) or on a no-Ethernet fieldbus card (cleaner for IO-less standalone use) - see 8.
- Local storage: microSD or >= 16 MB SPI flash sized for >= 1 year of 1-min data on ~32 tags (CPCB [S22], CWC [S45]); JJM minimum 30 days / 2 months [S20].
- RTC with backup cell, NTP sync (CWC asks < 1 s/week drift [S45]).
- Power: 12-24 V DC nominal (9-36 V range), reverse-polarity and surge protection; optional AC-mains PSU; optional -48 V DC entry for telecom (accessory, not baseboard).

### 6.2 Top SKU bundles (stackable modules; target India street price, excl. GST)
Card finished-cost targets from the product owner: Wi-Fi+BLE <= INR 600; LoRa <= INR 1,000; 4G+Eth+Wi-Fi <= INR 1,000. Baseboard cost is not given in the brief; street prices below are positioned against the competitor prices in 5.2 (a judgement, not cost-derived).

| # | SKU | Modules | Main applications | Target price band (INR) | Competitor anchor |
|---|---|---|---|---|---|
| 1 | UC-4G Meter Gateway | Controller (RS-485, DI) + 4G/Eth/Wi-Fi | Sub-metering, solar rooftop, compressors | 6,000-9,000 | IndiaMART 4G Modbus gateways INR 3.9-7.5k [S10]; USR-M100 INR 7.2k [S43] |
| 2 | UC-4G RTU (IO) | Controller full IO + 4G/Eth/Wi-Fi | Water pumping/JJM, DG, OCEMS, fuel | 9,000-14,000 | UC300-4G, IG502 (INR 25k), TRB245 (INR 18.6k) |
| 3 | UC-Wi-Fi Edge | Controller + Wi-Fi/BLE | OEE in MSMEs, buildings, cold rooms with Wi-Fi | 5,000-8,000 | Opta WiFi INR 15.9k [S48]; WISE-4012 INR 15.5k [S39] |
| 4 | UC-LoRa Node (standalone LoRa module + Li-ion or 12-24 V) | LoRa module alone, with its own RS-485/sensor input (TBD - module has no IO per decision 1) | JJM tail-end, agriculture, remote meters | 2,500-4,000 | UC100 ~INR 4.9k, RS485-LN ~INR 5k [S36, S9] |
| 5 | UC-LoRa Gateway (lite) | Controller + LoRa + 4G/Eth/Wi-Fi | Village water clusters, campuses, farms | 12,000-18,000 | RAK Soho Lite LTE INR 15.5k; UG65 INR 41.5k [S49, S37] |
| 6 | UC-DG / Tower Monitor | Controller (CAN + RS-485 + full IO) + 4G | DG sets, telecom towers | 10,000-15,000 | Indian tower RMS boxes (no price found) |
| 7 | UC-OCEMS Logger | SKU 2 + Eth + 1-year storage + CPCB push firmware | CEMS/effluent | 18,000-30,000 (software value) | Satlink 4G data logger INR 46k [S10] |
| 8 | UC-Remote IO / Modbus slave | Controller only (RS-485 Modbus slave) | IO expansion for SCADA/PLC | 3,000-5,000 | USR-IO, Advantech ADAM-class |
| 9 | UC-BLE Sensor Hub | Controller + Wi-Fi/BLE (BLE scanning of temp/RH tags) | Cold chain, retail refrigeration | 6,000-9,000 | - |
| 10 | UC-Full (all radios) | Controller + 4G/Eth/Wi-Fi + LoRa + Wi-Fi/BLE | Smart buildings, multi-utility | 16,000-22,000 | RUT956 INR ~37k, IG502 |

### 6.3 Must-have protocols
- Field (v1): Modbus RTU master + slave, Modbus TCP client + server; CAN J1939 read (DG); DLMS/COSEM client per IS 15959 over RS-485 (upsell, needed for utility/DT meters) [S24]; pulse/counter; LoRaWAN Class A (node) and a LoRa gateway/concentrator path (or point-to-point LoRa to the baseboard, decision open).
- Field (v2): BACnet MS/TP + BACnet/IP (BMS), SunSpec model mapping over Modbus, IEC 60870-5-104 / DNP3 for utilities (Advantech ECU-1051 offers DNP3 [S40]).
- Cloud: MQTT 3.1.1/5 over TLS 1.2+; HTTPS REST JSON POST (mandatory for JJM portal [S21]; CWC asks HTTP POST/FTP/SMS [S45]); multi-server simultaneous push (CPCB [S22]); SMS alerts; NTP; OTA firmware with signed images (JJM asks OTA [S20]); remote configuration of reporting interval [S20].

### 6.4 Differentiators for a modular "universal" product
1. Pay-per-radio: a 4G-only meter gateway at IndiaMART prices, growing into LoRa gateway or full RTU by clicking on modules; no competitor surveyed offers enclosed radio modules that also run standalone (5.2).
2. Same LoRa module serves as a standalone field node and as the gateway's radio - one design, two revenue lines, matching the JJM LoRa+4G architecture [S20].
3. MCU + secure element root of trust (like Opta's ATECC608B / PMC's SE050 [S46, S47]) at Indian price points; supports CRA/EN 18031 later.
4. Tender-ready firmware packs: JJM portal push, CPCB multi-server push with audit log, CWC-style 1-year storage - few low-cost Indian boxes document these.
5. Baseboard can power-cycle a hung module (watchdog) - matters for unattended JJM/tower sites with 95 % data-availability clauses [S45].

## 7. Indian tender requirements (consolidated)

| Requirement | Typical value seen | Source |
|---|---|---|
| Enclosure / IP | IP65 (CWC data logger), IP67/68 (JJM RTU), IP68 (JJM gateway) | [S45], [S20] |
| Operating temperature | -5..+60 C (CWC GSM modem); competitors spec -40..75 C | [S45], [S32] |
| Local storage | >= 1 year (CPCB, CWC); >= 30 days (JJM RTU); >= 2 months (JJM gateway) | [S22], [S45], [S20] |
| Reporting interval | 15 min mains; 2/day battery RTU; 4 h solar gateway (JJM) | [S20] |
| Cloud protocols | MQTT/AMQP/HTTPS with TLS (JJM); HTTP POST/FTP/SMS (CWC); multi-server push (CPCB) | [S20], [S45], [S22] |
| Security | TLS/DTLS/AES, hardware AES-128/192/256 (JJM gateway); user levels and passwords (CWC); config-change alarms, audit trail (CPCB) | [S20], [S45], [S22] |
| Remote management | OTA firmware, remote config of interval (JJM); remote log access by regulator (CPCB) | [S20], [S22] |
| Certifications | CE/FCC accepted where no Indian standard (JJM); MTCTE for IoT gateways (Phase III, 1 Jan 2024); TEC 33010:2025 IoT Gateway GR | [S20], [S30], [S31] |
| Power | Solar + battery with monsoon autonomy, battery voltage monitoring, surge/lightning protection on all sensor interfaces | [S45], [S20] |
| Warranty / O&M | 5-year comprehensive warranty + O&M, SIM/data cost on bidder (CWC) | [S45] |
| Bidder experience | Prior GSM/GPRS telemetry stations required (CWC) | [S45] |
| Dual SIM | Common in competitor products (TRB245, RUT956) [S2, S34]; no tender clause found requiring it | UNVERIFIED as tender clause |
| BIS | BIS CRS (IS 13252-1) registration for IT equipment and IS 16444/15959 for meters; applicability of CRS to an IoT gateway not verified | [S26]; CRS UNVERIFIED |
| Make in India | Public Procurement (Make in India) Order 2017 local-content classes (Class-I / Class-II suppliers) appear in central tenders; exact thresholds not re-verified in this study | UNVERIFIED |

## 8. Gaps, risks and open decisions

Risks
1. Price floor: Indian 4G Modbus gateways list at INR 3,900-7,500 [S10]. The 4G+Eth+Wi-Fi card alone is targeted at INR 1,000 finished cost; baseboard + enclosures + certification must keep SKU 1 under ~INR 9k street to compete.
2. Per-module enclosures and a pass-through 40-pin bus add mechanical cost and ESD/EMC exposure at every joint; each standalone module also needs its own power entry and certification.
3. Certification load multiplies with modules: MTCTE (IoT gateway, Phase III) [S30], TEC 33010:2025 [S31], CE/RED per radio, BIS. Using pre-certified radio modules lowers but does not remove this (UNVERIFIED with a CAB).
4. Smart-metering/DT segments are locked to meter OEMs' proprietary RF mesh and BIS re-test rules [S25, S26] - do not plan v1 volume there.
5. JJM-type tenders want IP67/68, which DIN-rail modules don't meet on their own. An IP67 field enclosure kit is needed [S20].
6. Telecom towers need a -48 V DC input and operator-specific RMS integration; no public TEC RMS specification was found.
7. Revenue in tender markets often comes through system integrators with 5-year O&M obligations [S45]. Hardware-only margin is thin.

Open decisions
- Is the RS-485 + CAN fieldbus on the baseboard MCU or on a separate low-cost fieldbus card? The baseboard option is cheapest for SKUs 1, 2 and 6. The card option keeps the baseboard minimal for SKU 3 and the Wi-Fi-only SKUs. Recommendation: put 1 RS-485 on the baseboard (nearly every application needs it) and offer the 2nd RS-485 + CAN on the card. This needs to be confirmed against the BOM.
- LoRa topology: should the LoRa module be a LoRaWAN gateway (8-channel SX1302-class, costly) or a single-channel/point-to-point LoRa link to own nodes? A INR 1,000 finished-cost target suggests the latter. Interoperability with third-party LoRaWAN sensors would then be lost.
- Standalone LoRa node IO: decision 1 puts all IO on the baseboard, but a standalone LoRa node used as a field node (UC100/RS485-LN class) needs at least RS-485 or sensor inputs. Choose between allowing minimal IO on the LoRa module and requiring a baseboard at every node.
- Is a -48 V and AC-mains power-entry accessory in scope?
- Does the product target IP67 field-box kits for JJM?

Gaps in this study (not completed or verified)
- Web search budget ran out mid-study. The following were NOT researched: WAGO, Siemens ET 200SP and Phoenix Axioline module-level prices; Robustel EG5100 and Four-Faith prices; Moxa ioLogik; Advantech ADAM-6700; Dragino LG308N; RevPi Core; named Indian PLC/RTU makers (none of them benchmarked beyond the IndiaMART listings); Indian tower-RMS product prices.
- Not verified: PM-KUSUM, EESL CCMS and RDSO specifications; Make-in-India thresholds; whether BIS CRS applies; warranty norms beyond the CWC tender; India volume figures (number of towers, OCEMS installations).
- Application interface counts marked E in 3.1 are engineering estimates.
- EUR/GBP/AUD/KES/PHP exchange rates were not checked. Only USD/INR (93.9) is sourced [S1].

## Appendix A. Tender source notes (detail behind the table in section 7)
- CWC / National Hydrology Project tender NHP/2021-RDC-1/02/VRS (2 Jun 2021, automated flow measurement at river sites, Ministry of Jal Shakti) [S45]: data logger with 2 AI, non-volatile flash for one year of data expandable to 16 GB via USB/SD; per-sensor recording interval; log and transmit simultaneously; display + keypad; solar-powered with battery voltage monitoring, "fully operational during monsoon"; lithium RTC backup (2-year storage); user levels/passwords; RTC drift < 1 s/week with NTP sync (IST); IP65 (NEMA 4) enclosure; GSM/GPRS modem -5..+60 C, transmission by HTTP POST, FTP and SMS, interrogation or event-triggered, >= 95 % data reception availability; antenna 900/1800 MHz "4G and better"; surge suppression on all sensor interfaces + lightning rod + separate earthing; 5-year comprehensive warranty + O&M, with telemetry SIM/communication cost borne by the bidder; bidder experience with GSM/GPRS telemetry stations required.
- JJM reference specs (see 3.0) [S20]: IP67/IP68 RTU, IP68 gateway, 30-day (RTU) / 2-month (gateway) local storage on memory card, 15-min reporting, MQTT/AMQP/HTTPS + TLS, OTA, CE/FCC accepted where no Indian standard exists; national portal ingests HTTPS JSON POST [S21].
- CPCB OCEMS [S22]: >= 1 year non-volatile storage, multi-server push without plant PC, remote access/audit for regulators, config/calibration-change alarms, Ethernet/Modbus/USB local retrieval.
- MTCTE: IoT gateways in Phase III (mandatory from 1 Jan 2024 per DoT annexure); TEC 33010:2025 IoT Gateway GR notified 23 Jan 2026 [S30, S31].

## 9. Sources

- S1 https://currencybeacon.com/rates/USD/INR ; https://hdfcsky.com/news/rupee-rises-24-paise-to-93-74-against-us-dollar-in-early-trade (accessed 2026-11-14)
- S2 https://www.gowifi.co.nz/specs/TRB245_datasheet-v1.3.pdf
- S3 https://discomp.cz/teltonika-trb245-industrial-lte-cat-4-gateway_d96319.html
- S4 https://www.buerklin.com/en/p/teltonika-networks-uab/device-servers-and-gateways/trb245/81P9451
- S5 https://www.gowifi.co.nz/specs/uc300-datasheet-en.pdf
- S6 https://invibitshop.com/products/milesight-uc300-lorawan-iot-controller-industrial-automation-eu868 ; https://www.pbtech.com/product/CCTMLS1171/Milesight-UC300-L05AU-UC300-4G-IoT-Controller-with
- S7 https://www.digikey.com/en/product-highlight/a/arduino/opta-expansions ; https://www.hackster.io/news/arduino-unveils-opta-digital-analog-expansion-modules-for-bigger-plc-projects-d44d7588431d ; https://kubii.com/en/development-kit/4642-2347-arduino-pro-opta-ext-a0602-7630049204119.html
- S8 https://uk.rs-online.com/web/p/industrial-computers/2713627
- S9 https://reach.dog/shop/robotshop-usa/products/dragino-rs485-ln-rs485-to-lorawan-converter-915-mhz ; https://exp-tech.de/en/products/dragino-rs485-ln-rs485-to-lorawan-converter
- S11 https://www.robustel.com/en/?p=3882 ; https://eshop.sectron.eu/UserFiles/Image/Robustel_R1520_datasheet.pdf
- S12 https://shop.norvi.lk/products/norvi-iiot-ae02-i ; https://www.industrialshields.com/llm-product-taxonomy ; https://www.industrialshields.com/shop/product/9609
- S13 https://uk.rs-online.com/web/p/plcs-programmable-logic-controllers/1771391 ; https://www.buerklin.com/en/p/phoenix-contact/plc-controls-logic-modules/2404267/64P8342 ; https://www.mouser.fi/c/industrial-automation/controllers/programmable-logic-controllers-plcs/?pg=6&q=CA
- S20 https://jaljeevanmission.gov.in/sites/default/files/guideline/technical-expert-committee-report-on-measuring-and-monitoring.pdf (Annexure 9(b) reference hardware specs, p.57)
- S21 https://ejalshakti.gov.in/IoT_Web/UploadFile/Operational%20Manual%20IoT%20data%20integration_18Feb2026.pdf
- S22 https://tnpcb.gov.in/PDF/Waste_Mngt/Biomedical/Guidlines/GuidelinesOCEMS.pdf (CPCB, 1st Revised Guidelines for CEMS, Aug 2018, section 2 analyser/DAS requirements)
- S23 https://erc.mp.gov.in/Documents/Workshop04072017/6July_3.pdf (CPCB presentation; quoted via search snippet, not opened)
- S24 https://www.tpcentralodisha.com/Editor_UploadedDocuments/Content/Three_phase_LTCT_SMART_Meters.pdf ; https://apcpdcl.in/news/Technical%20Specifications%20of%20%20CT%20operated%20Smart%20Meters.pdf (via search snippets)
- S25 https://cea.nic.in/wp-content/uploads/dp_t/2025/01/AMI_Interoperability_Report__Final-3.pdf
- S26 https://services.bis.gov.in/tmp/SIT_IS_16444_31052019.pdf
- S27 https://deveservices.dot.gov.in/node/73
- S28 https://dpstele.com/blog/how-choose-rms-telecom-site.php ; https://sysargus.com/en/gb/?p=226
- S29 https://www.vertiv.com/en-asia/products-catalog/critical-power/dc-power-systems/integrated-power-management-systems/
- S30 https://www.stagingeservices.dot.gov.in/sites/default/files/2024-11/downloadDocument_20240701164932.pdf ; https://www.certification-india.com/en/extension-of-mandatory-certification-date-for-32-products-ers-covered-under-phase-lll-iv-of-mtcte
- S31 https://alephindia.in/tec-notification-new-standard-for-iot-gateways.php
- S32 https://download.axilogi.com/Teltonika/Datasheet/TRB145.pdf
- S33 https://thinkrobotics.com/ar/products/trb145 ; https://arvutitark.ee/en/network-devices/routers/lte-gateway-no-wifi-4g-sim-r485-port-micro-usb-teltonik-1041856 ; https://controltech.uk.com/products/trb145 (prices via search snippets, 2026-11-14)
- S34 https://www.gowifi.co.nz/specs/rut956-datasheet-v13.pdf
- S35 https://www.cloudone.co/shop/rut956-teltonika-rut956-industrial-cellular-router-11959
- S36 https://www.milesight.com/iot/product/iot-controller/uc100 ; https://store.mcci.com/products/milesight-modbus-to-lorawan-iot-controller-uc100 ; https://powertec.com.au/milesight-uc100-iot-controller
- S37 https://aio.lv/en/product--milesight-ug65-868m-uki--12001461 ; https://www.pbtech.com/product/CCTMLS1192/Milesight-UG65-915M-EA-Ursalink-UG65-Indoor-AS923 ; https://www.comx-computers.co.za/MLS-GTWY-UG65-Milesight-UG65-LoRaWAN-Gateway-Non-Buy-p-284848.php
- S38 https://www.elvac.eu/ipc/download/moxa/datasheet/uc-2100-series-datasheet-v3.0_2024.pdf ; https://www.pbtech.com/product/IPCMXAUC2100001/MOXA-UC-2101-LX-Arm-based-computer-Mini-RISC-based ; https://ph.rs-online.com/web/p/industrial-computers/2553502
- S39 https://www.mouser.com/datasheet/2/638/WISE_4012_DS_070621_20210706101557-2492391.pdf ; https://www.mouser.com/datasheet/2/638/WISE_4060_DS_070621_20210706101757-2492297.pdf ; https://www.cdw.com/product/advantech-wlan-iot-wireless-i-o-module-wise-4012-expansion-module/8385283 ; https://uk.rs-online.com/web/p/plc-accessories/0657048
- S40 https://docs.rs-online.com/90f4/A700000014350289.pdf ; https://www.pbtech.com/product/IPCAVH220399/Advantech-ECU-1051TL-R10AAE-A8-600MHz2xLAN2xCOMDua
- S41 https://uk.rs-online.com/web/p/iot-gateways/2017731 ; https://de.rs-online.com/web/p/iot-gateways/2017731 ; https://sg.rs-online.com/web/p/iot-gateways/2017732
- S42 https://www.inhand.com/products/edge-gateways/ig502 ; https://embeddedworks.net/product/wwan1848
- S43 https://www.microthings.id/product/remote-io-edge-gateway-usr-m100/ ; https://st.robu.in/product/usr-m100-iot-remote-io-gateway-module-2do-2di-2ai-expandable-io ; https://m.indiamart.com/proddetail/serial-modbus-to-4g-ethernet-gateway-with-expandable-io-usr-m100-2854258680730.html ; https://www.soselectronic.com/en-it/products/usr-iot/usr-m100-eau-397756
- S44 https://pdf.directindustry.com/pdf/xiamen-four-faith-communication-technology-co-ltd/f2x14-low-power-consumption-m2m-cellular-ip-modem/114843-896177.html
- S45 https://cwc.gov.in/sites/default/files/bidding.pdf (CWC NHP tender, IFB NHP/2021-RDC-1/02/VRS, technical specification of data logger and GSM/GPRS modem, pp.86-89)
- S46 https://docs.arduino.cc/resources/datasheets/AFX00001-AFX00002-AFX00003-datasheet.pdf
- S47 https://docs.arduino.cc/resources/datasheets/AKX00032-datasheet.pdf
- S48 https://store-usa.arduino.cc/products/opta-rs485 ; https://store-usa.arduino.cc/products/opta-wifi ; https://store-usa.arduino.cc/products/opta-lite ; https://store-usa.arduino.cc/products/portenta-machine-control ; https://store.arduino.cc/products/opta-rs485 ; https://store.arduino.cc/products/portenta-machine-control
- S49 https://store.rakwireless.com/products/wisgate-soho-lite-lorawan-gateway-rak7266 ; https://store.rakwireless.com/products/wisgate-edge-lite-2-verizon-gateway-rak7268cv2v ; https://store.rakwireless.com/products/rak7289-8-16-channel-outdoor-lorawan-gateway ; https://store.rakwireless.com/products/wisgate-connect-industrial-iot-gateway-lora-zigbee ; https://store.rakwireless.com/products/wisblock-starter-kit ; https://store.rakwireless.com/products/rak3172-f-fuota-lorawan-module
- S10 https://m.indiamart.com/proddetail/4g-iot-gateway-modbus-rtu-rs485-tomqtt-2856511936130.html ; https://m.indiamart.com/proddetail/iot-4g-gateway-w-rs485-modbus-w-mqtt-2854408897433.html ; https://m.indiamart.com/proddetail/rtu-to-mqtt-gprs-gateway-26763405791.html ; https://m.indiamart.com/proddetail/rtu-with-modbus-protocol-21565323730.html ; https://www.aajjo.com/product/4g-modbus-iot-gateway-in-ahmedabad-ithing-mechatronics-llp ; https://www.tradeindia.com/products/rs485-4g-lte-mqtt-modbus-iot-gateway-9510323.html
