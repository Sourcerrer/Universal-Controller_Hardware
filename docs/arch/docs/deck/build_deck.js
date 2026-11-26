// Universal Controller overview deck: specs, architecture, video, costing.
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");
const { applyTheme } = require("/home/anup/.claude/skills/synced/b16bfdc9-aebc-4d41-99dd-ab5ec1f7f960_d8255e3b-ad11-4e00-8780-923ac709e6bb/pptx/scripts/apply_theme.js");

// usage: node build_deck.js <out.pptx> <hardware/docs/arch> <assets dir with arch_p1.png and video_cover.png>
const OUT = process.argv[2];
const ROOT = process.argv[3];          // hardware/docs/arch
const ASSETS = process.argv[4];
// cost.json is written by docs/diagram/build_architecture.py — every price at 100 units (owner, 2026-11-19)
const cost = JSON.parse(fs.readFileSync(path.join(__dirname, "cost.json"), "utf8"));

const THEME = {
  name: "Universal Controller",
  headFontFace: "Calibri",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "1B1F24", lt1: "FFFFFF", dk2: "23303D", lt2: "F2F4F6",
    accent1: "C46A00", accent2: "1F7F8C", accent3: "2F5FB3", accent4: "2E8540",
    accent5: "6B3FB3", accent6: "5A6470", hlink: "2F5FB3", folHlink: "6B3FB3",
  },
};

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = "Universal Controller — overview";
pres.author = "Universal Controller hardware team";
const C = pres.SchemeColor;

pres.defineSlideMaster({
  title: "TITLE_ONLY",
  background: { color: "FFFFFF" },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.5, y: 0.3, w: 12.3, h: 0.65, fontSize: 30, bold: true, color: C.text2, valign: "middle", margin: 0 }, text: "" } },
  ],
  slideNumber: { x: 12.35, y: 7.08, w: 0.5, h: 0.3, fontSize: 10, color: C.accent6, align: "right" },
});

const SUB = { fontSize: 13, color: C.accent6, margin: 0, isTextBox: true };
const HDR = { bold: true, color: C.background1, fill: { color: C.text2 }, fontSize: 12, valign: "middle" };
const CELL = { fontSize: 12, color: C.text1, valign: "middle" };

function subtitle(s, t) { s.addText(t, { x: 0.5, y: 0.95, w: 12.3, h: 0.35, ...SUB }); }

// ---------------------------------------------------------------- 1 specs
pres.addSection({ title: "Overview" });
{
  const s = pres.addSlide({ masterName: "TITLE_ONLY", sectionTitle: "Overview" });
  s.addText("Specifications", { placeholder: "title" });
  subtitle(s, "Modular DIN-rail IoT gateway: modules click together side by side, and each also works on its own as a remote node");
  const fam = [
    ["Fieldbus controller", "90 mm", "Base card + raised plug-in MCU card (STM32C5A3 standard, STM32H573 option; newer MCUs by a new card) · two models: with Ethernet — 4 AI, 6 DI · without Ethernet — 6 AI, 10 DI, 2 extra outputs · both: 6 SPDT relays 10 A (front-replaceable fuses) + 4 high-side 24 V · isolated RS-485 + CAN-FD · data log · motor-control card as an option"],
    ["4G modem card", "45 mm", "Quectel EC200U-CN: LTE Cat 1, GSM fallback, built-in GPS · low cost"],
    ["Wi-Fi + BLE", "45 mm", "ESP32-C6: Wi-Fi 6, BLE 5, 802.15.4 · isolated RS-485 + CAN 2.0 · 6 DI, 4 DO, 4 AI, 2 SPDT relays 10 A"],
    ["LoRa", "45 mm", "STM32WLE5, 865–867 MHz private network, long range · remote IO node: RS-485 · 6 DI, 4 AI, 4 DO"],
    ["Battery + charger board", "option, per module", "TI BQ25601 charger with backup, its own 18650 holder (cell ≈ 3000 mAh), I²C status"],
  ];
  const rows = [[{ text: "Module", options: HDR }, { text: "Width", options: HDR }, { text: "What it does", options: HDR }]];
  fam.forEach((r, i) => {
    const fill = { color: i % 2 ? "FFFFFF" : "F2F4F6" };
    rows.push([{ text: r[0], options: { ...CELL, bold: true, fill } }, { text: r[1], options: { ...CELL, fill } }, { text: r[2], options: { ...CELL, fill } }]);
  });
  s.addTable(rows, { x: 0.5, y: 1.5, w: 7.6, colW: [1.75, 1.15, 4.7], rowH: 0.62, border: { type: "solid", pt: 0.5, color: "C9D0D8" }, margin: 0.06, objectName: "family table" });

  const key = [
    ["Power", "5–32 V DC or USB-C 5 V on every module; one 12 V 18 W adapter per gateway or standalone module; relay contacts may switch mains, behind 5 kV isolation"],
    ["Stack bus", "One 4-pin connector: power + RS-485 (≈ 2 Mbit/s); publish–subscribe between modules; any order, up to 5"],
    ["Security", "Hardware root of trust, secure boot, signed + encrypted updates, no open services"],
    ["Software", "Zephyr RTOS · Modbus RTU / TCP, J1939, MQTT over TLS, signed OTA"],
    ["Certification", "Phase 1 India: TEC MTCTE, WPC, BIS · Phase 2: CE, CRA"],
    ["Mounting", "35 mm DIN rail, each module in its own enclosure"],
  ];
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 8.45, y: 1.5, w: 4.4, h: 5.4, fill: { color: C.background2 }, line: { color: "C9D0D8", width: 0.75 }, rectRadius: 0.08, objectName: "key specs card" });
  const runs = [];
  key.forEach((k, i) => {
    runs.push({ text: k[0], options: { bold: true, color: C.accent1, fontSize: 13, breakLine: true } });
    runs.push({ text: k[1], options: { color: C.text1, fontSize: 12, breakLine: i < key.length - 1, paraSpaceAfter: 7 } });
  });
  s.addText(runs, { x: 8.65, y: 1.62, w: 4.0, h: 5.2, valign: "top", margin: 0, isTextBox: true, objectName: "key specs" });
  s.addText("Preliminary · parts and figures from the PRD Draft 0.6 and research reports R01–R25 · prices at 100 units", { x: 0.5, y: 7.08, w: 9, h: 0.3, fontSize: 10, color: C.accent6, margin: 0, isTextBox: true });
}

// ---------------------------------------------------------------- 2 architecture
{
  const s = pres.addSlide({ masterName: "TITLE_ONLY", sectionTitle: "Overview" });
  s.addText("Hardware architecture", { placeholder: "title" });
  subtitle(s, "Front view of a full stack on a DIN rail, covers removed (page 1 of UC_Architecture.pdf)");
  const ih = 5.75, iw = ih * 3176 / 2246;
  s.addImage({ path: path.join(ASSETS, "arch_p1.png"), x: 0.5, y: 1.4, w: iw, h: ih, altText: "Architecture diagram: Fieldbus controller, 4G modem, Wi-Fi + BLE and LoRa modules on a DIN rail with the gateway adapter", objectName: "architecture diagram" });
  const pts = [
    ["Power stage on every module", "Buck regulator + protection on each module PCB (terminal ∥ USB-C 5 V ∥ bus) + optional plug-in battery + charger board"],
    ["Battery per module, optional", "Plug-in charger board with its own 18650 holder; it backs up its module and can feed the stack over the bus"],
    ["Every module stands alone", "In a stack the coordinator is elected: Fieldbus controller, else Wi-Fi + BLE, else LoRa"],
    ["Full drawing set", "UC_Architecture.pdf: IO sharing, bus pinout and power, pricing, software, Tier-2 router"],
  ];
  const x = 0.5 + iw + 0.35, w = 12.83 - x;
  const runs = [];
  pts.forEach((p, i) => {
    runs.push({ text: p[0], options: { bold: true, color: C.accent1, fontSize: 14, breakLine: true } });
    runs.push({ text: p[1], options: { color: C.text1, fontSize: 12, breakLine: i < pts.length - 1, paraSpaceAfter: 12 } });
  });
  s.addText(runs, { x, y: 1.45, w, h: 5.6, valign: "top", margin: 0, isTextBox: true, objectName: "key points" });
}

// ---------------------------------------------------------------- 3 video
{
  const s = pres.addSlide({ masterName: "TITLE_ONLY", sectionTitle: "Overview" });
  s.addText("Assembly and PCB layout", { placeholder: "title" });
  subtitle(s, "45-second concept animation: modules with covers removed, inserting and removing modules, field nodes · not to scale");
  const w = 9.6, h = w * 9 / 16;
  s.addMedia({ type: "video", path: path.join(ROOT, "..", "specs", "UC_Architecture_Video.mp4"), cover: "data:image/png;base64," + fs.readFileSync(path.join(ASSETS, "video_cover.png")).toString("base64"),
               x: (13.333 - w) / 2, y: 1.45, w, h, objectName: "concept video" });
}

// ---------------------------------------------------------------- 4 costing (100 units only)
{
  const s = pres.addSlide({ masterName: "TITLE_ONLY", sectionTitle: "Overview" });
  s.addText("Costing at 100 units", { placeholder: "title" });
  subtitle(s, "INR per unit at 100 units · price before profit = BOM + 50 % manufacturing, packing, logistics + firmware royalty · price after profit = that + 30 %");
  const f = n => (n < 0 ? "−" + Math.abs(n).toLocaleString("en-IN") : n.toLocaleString("en-IN"));
  const H = (t, a) => ({ text: t, options: { ...HDR, fontSize: 10.5, align: a || "right" } });
  const rows = [[H("Item", "left"), H("Fits", "left"), H("BOM"), H("Before profit"), H("After profit")]];
  const sec = t => rows.push([{ text: t, options: { bold: true, fontSize: 10.5, color: C.text2, fill: { color: "E1E7EE" }, colspan: 5 } }]);
  const line = (name, fits, nums, i, bold) => {
    const fill = { color: i % 2 ? "FFFFFF" : "F6F8FA" };
    const c = (t, a, b) => ({ text: t, options: { fontSize: 10.5, color: C.text1, fill, align: a, bold: !!b, valign: "middle" } });
    rows.push([c(name, "left", bold), c(fits, "left"), c(f(nums[0]), "right"), c(f(nums[1]), "right"), c(f(nums[2]), "right", true)]);
  };
  sec("Modules (with their power stage), battery board and adapter");
  cost.items.forEach((r, i) => line(r[0], "", r.slice(1), i, true));
  sec("Options — add to the module they fit");
  cost.options.forEach((r, i) => line(r[0], r[1], r.slice(2), i, false));
  sec("Typical systems — add one adapter per stack; battery boards optional");
  cost.systems.forEach((r, i) => line(r[0], "", r.slice(1), i, true));
  s.addTable(rows, { x: 0.5, y: 1.4, w: 12.33, colW: [5.0, 2.33, 1.6, 1.7, 1.7], rowH: 0.2, border: { type: "solid", pt: 0.5, color: "C9D0D8" }, margin: [0.01, 0.05, 0.01, 0.05], objectName: "costing table" });
  s.addText([
    { text: "ESTIMATES, no supplier quotes yet. ", options: { bold: true } },
    { text: "BOMs at 100 units from research R02–R22. Royalty: INR 2,000 per device for the first 20 devices of every module, then INR 750 Fieldbus controller (+ INR 500 hardware royalty), 750 4G modem card, 200 Wi-Fi + BLE, 200 LoRa; none on the DC-DC board, battery board, adapter or options. All 15 combinations: UC_Architecture.pdf page 4." },
  ], { x: 0.5, y: 6.75, w: 11.6, h: 0.35, fontSize: 10, color: C.accent6, margin: 0, valign: "top", isTextBox: true, objectName: "costing notes" });
}

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("wrote", OUT);
})();
