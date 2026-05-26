# OpenPLC Editor Docs Rewrite — Plan

> **Status:** Proposal — for user review before drafting begins.
> **Sources:** Live editor at `https://editor-staging.autonomylogic.com/`, source inventory in [EDITOR-SOURCE-INVENTORY.md](./EDITOR-SOURCE-INVENTORY.md), online vPLC `01` on orchestrator `SLM-RP4`.

## Guiding principles (carried over from the platform docs rewrite)

1. **Plain prose. No LLM tells.** Short sentences. Em-dashes replaced with periods, commas, or parentheses (the `dedash.py` sweep should run on the editor section as a finishing step).
2. **Show, don't list.** Every UI surface gets a clean screenshot (no Chrome MCP overlay), cropped tight. Long forms get one screenshot per logical section, not one mega-shot.
3. **Worked examples, not tutorials.** Each major feature lands an end-to-end worked example with a real vPLC.
4. **Block docs are concise.** Beckhoff-style — 1–2 paragraphs, an inputs/outputs table, a timing diagram or wire diagram when useful. No fluff.
5. **Reuse the FBD/LD diagram renderer.** Authoring a JSON diagram is faster than capturing screenshots and renders crisp at any zoom. Use renderer for all block reference pages.

## What's there today

`docs/openplc-editor/` — **87 .md files, 14013 lines.** Structure: Overview, Installation, Connecting to Runtimes, Workspace Overview, IEC Concepts, Programming Languages (ST/LD/FBD/IL), Custom Languages (Python/C++), Working with Variables, Custom Data Types, Standard Function Blocks, Task Configuration, Hardware Configuration, Building and Deploying, Communication Protocols (Modbus/OPC-UA/S7Comm/EtherCAT).

### What survives mostly intact

- **IEC Concepts** (`iec-concepts/`) — the standard is the standard. Light edit for tone, but the content is fine.
- **Standard Function Blocks** (`standard-function-blocks/`) — block reference pages are roughly the shape we want. **Rewrite for tone + Beckhoff-style diagrams, but the structure stays.**
- **Python / C++ block tutorials** in `custom-languages/` — accurate per source, just dedash + concision pass.
- **Existing diagram JSONs** in `autonomy-edge/apps/frontend/public/docs/diagrams/` — there are already 22 FBD and 26 LD example JSONs. **Reuse aggressively.**

### What needs a full rewrite

- **Overview** — current text is generic.
- **Workspace Overview** (`workspace-overview/`) — the activity bar, project tree, console panel are all real surfaces with real semantics. Current docs are vague.
- **Hardware Configuration** — current docs describe pin-mapping screens that don't exist in this build (pins live in VPP packages). Needs to be replaced with **Board Selection + VPP Vendor Screens**.
- **Communication Protocols** — current docs are partial. Modbus is missing the live address-mapping table behavior. OPC-UA has 5 tabs we need to walk through. S7Comm has 14 buffer mapping types. EtherCAT has 3 bus-level tabs + 4 per-slave tabs.
- **Building and Deploying** — needs to be re-grounded against `simulator`/`openplc-compiler`/STruC++ pipeline (the legacy `iec2c` references are stale).
- **Connecting to Runtimes** — current docs predate the Orchestrators screen. Now it's: click an Orchestrator → expand → click a vPLC → login.

### What's missing entirely

- **Remote Devices** (Modbus master, EtherCAT master). No current section.
- **Servers tree node** in the project explorer (Modbus / OPC-UA / S7Comm slaves) — covered in Communication, but the *project tree* placement and lifecycle needs explanation.
- **Library Manager** — `Manage libraries…` flow, project-vs-system libraries, `.stlib`/`.lib`/`.library` import.
- **AI Engineer** — consent modal, inline completions in ST/IL/Python/C++, chat panel for LD/FBD too, ACU accounting, telemetry transparency.
- **Source Control panel** — Changes/History tabs, inline diff, commit, discard/restore, branches.
- **Debugger** — live variable polling, debug compile + MD5 verification flow, time-series chart, no breakpoints.
- **Search in Project** — POU + variable tree, highlight, navigation.
- **Diagram authoring guide** — how to author FBD/LD JSON to render in docs. Schema + worked examples.

## Proposed new structure

Top-level outline (each leaf = one .md file). **bold** = brand new; *italic* = full rewrite; plain = light edit / dedash only.

### 1. Getting Started
- Overview *
- **Editor vs. Platform** (where the editor sits in the larger system)
- *Connecting to a vPLC* (replaces Installation + Connecting to Runtimes; new flow via Orchestrators)

### 2. Workspace
- *Workspace layout* (title bar, activity bar, project tree, central editor area, console)
- *Activity bar reference* (icons in order, what each one does, conditional toolbox)
- *Project tree* (Functions / Function Blocks / Programs / Data Types / Resource / Device / Servers; tree-header `+` popover)
- *Console & PLC Logs* (filters, sources, runtime-log subscription)
- **Search in Project** (POU + variable index; navigation from results)
- **Source Control** (Changes, History, Branches, diff view, commit workflow)
- **AI Engineer** (consent, inline completion, chat panel, ACU accounting)

### 3. Programming Languages (IEC 61131-3)
The existing nested layout works.
- IEC concepts (POUs, variables/data types, tasks/instances) — lightly edited.
- Structured Text — keep, *light rewrite of editor features section*.
- Ladder Diagram — keep contact/coil/FB pages, **add LD authoring walkthrough with the worked example**.
- Function Block Diagram — *rewrite basics with FBD diagram renderer examples*.
- Instruction List — keep.
- *Note: SFC is offered in the picker but disabled — call this out.*

### 4. Custom Programming Languages
- Python function blocks — keep with light edits.
- C++ function blocks — keep with light edits.

### 5. Variables and Data Types
- *Variables editor* (table vs code mode, classes, location, alias, debug)
- *Global variables* (Resource scope)
- *Custom data types* (array, enumerated, structure) — keep current pages, light edit.
- **Aliases and producer-managed addresses** (new: explain why `alias` exists alongside `location`, when the registry updates a variable's address, the orphan-alias warning)

### 6. Standard Block Library
The new editor ships **exactly four** bundled libraries (as `.stlib` archives via the STruC++ runtime). The legacy `iec2c` XML catalog (Arduino, CAN, SM_Cards, P1AM, Jaguar, SL-RP4, MQTT, Communication_Blocks) is **deprecated and not user-facing** — do not document those.

- **Library Manager** (system vs project libraries, importing `.stlib`/`.lib`/`.library`)
- *iec-std-functions* (the 89-function CSV catalog)
  - Type conversion
  - Numerical / arithmetic
  - Time arithmetic
  - Bit-shift & bitwise
  - Selection (SEL, MAX, MIN, LIMIT, MUX)
  - Comparison
  - Character string
- *iec-standard-fb* (Beckhoff-style 1–2 paragraph pages, FBD-rendered diagrams)
  - Bistable: SR, RS, SEMA
  - Edge detection: R_TRIG, F_TRIG
  - Counters: CTU, CTD, CTUD (+ their type-suffixed variants in a compact table)
  - Timers: TP, TON, TOF
- *additional-function-blocks* (RTC, INTEGRAL, DERIVATIVE, PID, RAMP, HYSTERESIS)
- **oscat-basic** — short overview page, link out to upstream OSCAT documentation. No per-block reference here.

### 7. Tasks and Instances
- *Task editor* — Cyclic vs Interrupt, interval, priority.
- *Instance editor* — bind program → task.
- Keep existing structure, dedash + accuracy pass.

### 8. Hardware (Board) Configuration
**Web editor ships with the board baked in by the vPLC runtime image. The board selector, VPP vendor screens, and additional-boards installer are desktop-only and not documented here.** This section is replaced by a short note pointing users to the vPLC creation flow in the platform docs, where the runtime image (and therefore the board capabilities) is chosen.

### 9. Communication
- **Address mapping fundamentals** (cross-protocol primer: `%IX`, `%QX`, `%MW`, byte.bit notation, why `%QX0.0 → coil 0` but `%QX1.0 → coil 8`)
- *Modbus*
  - Modbus server (slave) — buffer mapping accordion, address mapping reference table
  - Modbus remote device (master) — I/O groups, function codes, TCP vs RTU transport
  - **Modbus addressing reference** (canonical formula + worked examples)
- *OPC-UA* — 5 tab walkthrough
- *S7Comm* — server configuration, data blocks, identity, logging
- *EtherCAT* — bus master tabs, slave tabs, ESI repository, scan flow
- Optional: EtherNet/IP and PROFINET — **call out as visible but disabled**

### 10. Building, Running, Debugging
- *Build options* (build-only, build-upload, clean-upload)
- *Deployment to a vPLC* (runtime targets connected via Orchestrators)
- **Debugger** (debug compile, MD5 verification, polling, time-series chart, opting variables in)

**Note: the in-process AVR8JS simulator is desktop-only — not documented here.**

### 11. Diagram Renderer (for docs authors)
- **FBD/LD JSON authoring guide** — schemas, handle conventions, layout tips
- **MDX usage** (`<FBDDiagramViewer src="..." />` / `<LadderDiagramViewer src="..." />`)
- **Example gallery** — point to existing JSONs in `apps/frontend/public/docs/diagrams/`

### 12. Worked Examples
End-to-end recipes connecting all of the above. Each example: project setup → variables → body → compile → deploy to vPLC `01` → observe in debugger.

- **Blink** (LD; the EDF Demo project — TON→TOF self-feeding)
- **Start/stop with seal-in** (LD; classic motor starter; reuses `seal-in.json`)
- **Modbus slave: expose digital outputs** (configure Modbus server, write to `%QX0.0`, observe `coil 0` from a Modbus client)
- **OPC-UA: read variable from a UA client** (configure server, set permissions, browse with UaExpert)
- **Python function block** (replaces PID example — author a small Python FB doing a data transform, expose to ST, run on the simulator/vPLC)

## Screenshot inventory (priorities — capture all clean, no Chrome MCP overlays)

| # | Surface | Crop hint |
|---|---|---|
| 1 | Editor first-open with the EDF Demo project (blink LD) | Full window |
| 2 | Activity bar with hover tooltips | Vertical strip |
| 3 | File / Edit / Display / Help / Recent menus (one shot each, open) | Menu pop |
| 4 | Project tree with `+` popover open | Left panel |
| 5 | New POU modal (function/function-block/program; show language picker — call out disabled SFC) | Modal |
| 6 | Variables editor — table mode | Table only |
| 7 | Variables editor — code mode (`VAR ... END_VAR`) | Editor area |
| 8 | Variables editor — class filter dropdown open | Dropdown + table |
| 9 | LD editor — full rung with TON/TOF | Rung only |
| 10 | LD contact-variant picker | Modal |
| 11 | LD coil-variant picker | Modal |
| 12 | LD block selector | Modal |
| 13 | FBD editor — small worked diagram | Editor area |
| 14 | ST editor — STruC++ LSP active (semantic colors, hover tooltip) | Code area |
| 15 | IL editor — minimal example | Code area |
| 16 | Data Type editor — Array, Enumerated, Structure (one each) | Per editor |
| 17 | Resource editor (Globals + Tasks + Instances) | Full area |
| 18 | ~~Board selector dropdown~~ | **Desktop-only — skipped** |
| 19 | Library Manager — System Libraries tab | Modal |
| 20 | Library Manager — Project Libraries tab | Modal |
| 21 | Modbus server editor — Server Configuration section | Form |
| 22 | Modbus server — Buffer Mapping accordion expanded | Accordion |
| 23 | Modbus server — Address Mapping Reference live table | Table |
| 24 | Modbus remote device — I/O Groups | Tabbed table |
| 25 | Modbus remote — TCP transport config | Form |
| 26 | Modbus remote — RTU transport config | Form |
| 27 | OPC-UA server — General Settings | Tab |
| 28 | OPC-UA server — Security Profiles | Tab |
| 29 | OPC-UA server — Users | Tab |
| 30 | OPC-UA server — Certificates | Tab |
| 31 | OPC-UA server — Address Space tree | Tab |
| 32 | S7Comm server — Server Configuration | Accordion |
| 33 | S7Comm — Data Blocks | Table + modal |
| 34 | S7Comm — PLC Identity | Form |
| 35 | EtherCAT — Scan Bus | Tab |
| 36 | EtherCAT — Repository | Tab |
| 37 | EtherCAT — Advanced | Tab |
| 38 | EtherCAT — per-slave Devices tab | Tab |
| 39 | EtherCAT — per-slave Channel Mappings | Tab |
| 40 | EtherCAT — per-slave SDO Parameters | Tab |
| 41 | Source Control — Changes (with one staged + one unstaged) | Panel |
| 42 | Source Control — Diff view | Editor diff |
| 43 | Source Control — History | Panel |
| 44 | Branch switcher popover | Popover |
| 45 | Debugger — chart with two variables | Panel |
| 46 | Build options popover | Popover |
| 47 | AI consent modal | Modal |
| 48 | AI Chat panel | Right rail |
| 49 | AI inline completion in ST | Code with ghost text |
| 50 | Orchestrators screen — SLM-RP4 expanded showing vPLC 01 | Editor area |
| 51 | Runtime login modal | Modal |
| 52 | Search in Project — populated results tree | Panel |
| 53 | Console — filters dropdown open | Filters |
| 54 | PLC Logs panel — runtime stream | Panel |

## Diagram reuse strategy

`apps/frontend/public/docs/diagrams/` already has:
- **22 FBD JSONs.** `sfb-*.json` (ten standard function blocks) — already shaped for the block reference pages. `fbd-basics-*` and `fbd-examples-*` — for the FBD basics + worked-example sections.
- **26 LD JSONs.** Covers `basic-contact-coil`, `coil-*` (six coil variants), `contact-*` (six contact variants), `latch-set`/`latch-reset`, `seal-in`, `and/or/not-logic`, `fb-ton-*`. Aligns with the LD section.

**Action:** Audit each existing JSON for correctness against the schema, then reuse in MDX. **Author new diagrams only where coverage is thin** (e.g., parallel branching, advanced FBD execution control with EN/ENO).

## Tone-and-finish sweep

After the structural rewrite:
1. Run `dedash.py` across `docs/openplc-editor/` (same script used for the platform docs).
2. Hunt for "comprehensive", "robust", "powerful", "leverage", "utilize", "in order to" — typical LLM filler. Replace or delete.
3. Hard cap on adjective stacking. Avoid "this powerful and intuitive feature lets you…" patterns.

## Ordering of work

1. **Capture screenshots** (work down the inventory above) — explorer build dependent on a real session in the editor, so collect them before drafting.
2. **Rewrite the structural pages** (Overview, Workspace, Communication, Building/Deploying, Debugger) — the ones with the highest accuracy debt.
3. **Tone-pass the block reference + IEC concept pages** that are already structurally OK.
4. **Author new pages** (Library Manager, Search, AI Engineer, Source Control, Remote Devices, Diagram authoring).
5. **Build the worked examples** against vPLC `01`.
6. **Final pass:** `dedash.py`, link-check, image-size check, navigation update in `_config.json`.
7. **Commit, push, merge to development, bump `autonomy-edge/apps/frontend/docs-version.json`.**

## Decisions captured (user, 2026-05-23)

1. **OSCAT Basic** — overview page only, link out to upstream OSCAT docs. No per-block reference.
2. **Platform-specific libraries** — **do not document.** Those libs are no longer surfaced in the new editor; the legacy XMLs are deprecated artifacts.
3. **Worked examples** — keep four of five; **replace PID temperature loop with a Python function block example** (data-transform FB, run on the connected vPLC).
4. **Editor source branch** — local checkout must be on `v4.2.0-rc1` to match the deployed editor. Confirmed.
5. **Desktop-only surfaces excluded.** The editor codebase is shared between desktop (Electron) and web (embedded in autonomy-edge), but several screens render only on desktop. **These are out of scope for these docs:** Board selector / target selection, VPP vendor screens, `Install additional boards…` flow, in-process AVR8JS simulator, Arduino USB upload, local-disk path fields. We only document what a web-editor user can actually reach.
