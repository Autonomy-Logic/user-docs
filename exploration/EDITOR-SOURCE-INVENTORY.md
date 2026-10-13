# OpenPLC Editor — Source Inventory

> Internal reference for the docs rewrite. Source-of-truth: `/Users/thiagoralves/Documents/Code/openplc-editor` (Electron+React, Zustand). Architecture and conventions documented in the editor's `CLAUDE.md`. The web/orchestrator side at `autonomy-edge` reuses the same store + port contracts.

## 1. Project structure

**Source:**
- Schema: `src/backend/shared/types/PLC/open-plc.ts` — Zod `PLCProjectSchema` (top-level: `{ meta, data }`).
- File layout: `src/backend/shared/project/project-files-schema.ts`.
- Parser: `src/backend/shared/utils/parse-project-files.ts`.
- Create-element UI: `src/frontend/components/_features/[workspace]/create-element/index.tsx` + `element-card/index.tsx`.
- Tree UI: `src/frontend/components/_organisms/explorer/project.tsx`.

**On-disk layout of a project folder:**
```
<project>/
├── project.json              # Top-level metadata + structured project data
├── library.json              # Only for `plc-library` projects (raw manifest bytes)
├── devices/
│   ├── configuration.json    # Board selection + per-VPP screen data
│   └── pin-mapping.json      # Array of devicePinSchema entries
├── pous/
│   ├── functions/<Name>/     # body.st, .il, .ld, .fbd, .py, .cpp
│   ├── function-blocks/<Name>/
│   └── programs/<Name>/
└── build/                    # Compiler output (gitignored)
```

**`project.json` top-level (`PLCProjectSchema`):**
```ts
{
  meta: { name: string, type: 'plc-project' | 'plc-library' },
  data: {
    dataTypes: PLCDataType[],
    pous: PLCPou[],
    configuration: {
      resource: {
        tasks: PLCTask[],
        instances: PLCInstance[],
        globalVariables: PLCVariable[]
      }
    },
    servers?: PLCServer[],
    remoteDevices?: PLCRemoteDevice[],
    libraries?: { name, version }[],
    libraryManifest?: string,
    debugVariables?: { global?: string[], pous?: Record<string, string[]> },
    deletedPous?, deletedServers?, deletedRemoteDevices?
  }
}
```

Element types creatable from the "+" popover: `function`, `function-block`, `program`, `data-type`, `server`, `remote-device`. Library projects only expose `function`, `function-block`, `data-type`. Server / remote-device only enabled for Runtime v4 / Simulator targets.

Name validation: CamelCase / PascalCase / snake_case, min 3 chars.

New Project wizard (3 steps for PLC, 2 for Library): type → name+path → main language + cyclic task interval (default `T#20ms`, language default ST).

## 2. Editors per language

### Structured Text (ST)
No hand-rolled tokenizer — colorization, hovers, completions, goto-definition come from the **STruC++ LSP worker** (semantic-tokens protocol). Monaco registers `st` with bracket/comment/indent rules only. Auto-indent on `IF/FOR/WHILE/REPEAT/CASE/FUNCTION/FUNCTION_BLOCK/PROGRAM/VAR/STRUCT/CLASS/METHOD`, dedent on `END_*`. AI inline completion rides on top via `AIPort.registerInlineCompletions`.

### Instruction List (IL)
Plain Monaco Monarch tokenizer (no LSP). Opcodes: `LD/LDN/ST/STN/S/R/AND/ANDN/&/&N/OR/ORN/XOR/XORN/NOT/ADD/SUB/MUL/DIV/MOD/GT/GE/EQ/NE/LE/LT/JMP/JMPC/JMPN/CAL/CALC/CALN/RET/RETC/RETN`. String literals invalid.

### Ladder Diagram (LD)
DnD Kit-based (not @xyflow). Toolbox: Block, Coil, Contact, Delete-selected.
- Contact variants: `default | negated | risingEdge | fallingEdge`.
- Coil variants: `default | negated | set | reset | risingEdge | fallingEdge`.
- Parallel branching supported.

### Function Block Diagram (FBD)
Built on `@xyflow/react`. Node types: `block`, `input-variable`, `output-variable`, `inout-variable`, `connector`, `continuation`, `comment`. Toolbox: Block, Input Variable, Output Variable, Connector, Continuation, Comment.
Block sizing: width 216, connector Y 48 with 48px pitch. Variables 128×32. Optional EN/ENO (`executionControl: true`).

### Sequential Function Chart (SFC)
**Stub** — body returns `<div>heres the sfceditor</div>`. The picker disables SFC. **Not functional in this build.**

### Python function blocks
Available only for `function-block` POUs. Gated by `pythonFunctionBlocks` capability. Available on Simulator + Runtime v3 + Runtime v4. **Blocked on Arduino.** Variables marshalled via `struct.pack`/`unpack` generated from the FB interface.

### C/C++ function blocks
Available only for `function-block` POUs. Variables exposed as `strucpp::IEC_INT*` pointers; strings via `strucpp::IECString<254>`. Inline Arduino API completions when `arduinoApiCompletions` is set (Simulator only by default).

## 3. Variables editor

Table mode (default) ⇄ Code mode toggle. Code mode shows raw `VAR ... END_VAR` blocks; save re-parses to table.

`PLCVariable`:
```ts
{ id?, name, class?, type: PLCVariableType, location, alias?, initialValue?, documentation, debug? }
```
`PLCVariableType.definition` is one of `'base-type' | 'user-data-type' | 'array' | 'derived'`.

**Classes:**
- Python/C++ POUs: only `input`, `output`.
- ST/IL/LD/FBD POUs: `input`, `output`, `inOut`, `external`, `local`, `temp`.
- Globals (Resource editor): always `global`.

Filter chip above the table: `All | Local | Input | Output | InOut | External | Temp`.

Columns for non-program POUs: `# | Name | Class | Type | Initial Value | Documentation | Debug`. Programs add `Location` between Type and Initial Value.

**Location format:** IEC strings like `%IX0.0`, `%QW3`, `%MD5`, `%MX0.7`.

**Alias:** persistent name bound to a producer-managed address (pin mapping / VPP slot / EtherCAT channel / remote IO point). When the producer moves the address, `location` is rewritten from the alias registry on `syncVariableAliases()`. Orphan alias gets an amber warning glyph. Registry in `src/backend/shared/utils/iec-address/`.

**Rename impact:** `RenameImpactModal` runs `findAllReferencesToVariable` across all bodies before committing.

## 4. Custom data types

`PLCDataType` derivations: `array | enumerated | structure`. Defaults:
- Array → `baseType = BOOL`, empty dimensions.
- Enumerated → empty values.
- Structure → empty variable array.

Custom types appear in the Variables editor type-picker alongside base types.

## 5. Hardware configuration / boards

Built-in targets (3 only):

| Name | Compiler | Capabilities |
|---|---|---|
| **OpenPLC Simulator** | `simulator` (in-process AVR8JS) | full feature set; debug via `modbus-serial` |
| **OpenPLC Runtime v3** | `openplc-compiler` | minimal: python FBs only; debug via `modbus-tcp` |
| **OpenPLC Runtime v4** | `openplc-compiler` | full set; debug via `websocket`; `hasRuntimeStats: true` |

Pin mapping disabled for all three in `hals.json` — pins live in **VPP packages** (vendor screens). Board dropdown includes `__install_additional_boards__` synthetic entry → package manager.

## 6. Communication / Servers

### Modbus TCP slave
- **Server Configuration:** Enable, Interface (`0.0.0.0` / `127.0.0.1`), Port (default 502).
- **Buffer Mapping** (Accordion):
  - Holding Registers (FC 3/6/16): `%QW`, `%MW`, `%MD` (2 regs each), `%ML` (4 regs each). Max 1024.
  - Coils (FC 1/5/15): `%QX`, `%MX`. Max 8192 bits.
  - Discrete Inputs (FC 2): `%IX`. Max 8192.
  - Input Registers (FC 4): `%IW`. Max 1024.
- **Address Mapping Reference** (collapsible live table).

### OPC-UA server
Five tabs:
1. **General Settings:** Server Name, Interface, Port (4840), Endpoint Path (`/openplc/opcua`), Application URI, Product URI, Cycle Time (10..10000 ms), Namespace URI.
2. **Security Profiles:** `securityPolicy: 'None'|'Basic128Rsa15'|'Basic256'|'Basic256Sha256'`, `securityMode: 'None'|'Sign'|'SignAndEncrypt'`, `authMethods: ('Anonymous'|'Username'|'Certificate')[]`.
3. **Users:** `password` (`username`+`passwordHash`) or `certificate`. Role: `viewer | operator | engineer`.
4. **Certificates:** Server cert strategy (`auto_self_signed` / `custom`); trusted client certs.
5. **Address Space:** variable tree with per-variable `OpcUaNodeConfig { nodeId, browseName, displayName, description, permissions[role][r/w/rw], nodeType: 'variable'|'structure'|'array', ...}`.

### S7Comm server
1. **Server Configuration:** Enable, Bind Address, Port (102), Max Clients (1..1024), PDU Size (240..960).
2. **Data Blocks (max 64):** `{ dbNumber (1..65535), description, sizeBytes (1..65536), mapping: { type, startBuffer, bitAddressing } }`. 14 buffer types: `bool_input %IX`, `bool_output %QX`, `bool_memory %MX`, `byte_input %IB`, `byte_output %QB`, `int_input %IW`, `int_output %QW`, `int_memory %MW`, `dint_input %ID`, `dint_output %QD`, `dint_memory %MD`, `lint_input %IL`, `lint_output %QL`, `lint_memory %ML`.
3. **PLC Identity:** Name, Module Type (default `CPU 315-2 PN/DP`), Serial, Copyright, Module Name.
4. **Logging:** Connections / Data Access / Errors toggles.

## 7. Remote devices

Protocols: `Modbus`, `EtherNet/IP` (disabled), `EtherCAT`, `PROFINET` (disabled). Gated to Runtime v4 / Simulator.

### Modbus remote (master)
Tabbed table of **I/O Groups** (`ModbusIOGroup`):
- Function Code: FC 1/2/3/4/5/6/15/16.
- Cycle time (ms), Offset, Length, Error handling (`keep-last-value` | `set-to-zero`).
- I/O Points: `{ name, type, iecLocation, alias? }`.

Transport: TCP/IP (host+port 502) or RTU/Serial (port from `runtime.getSerialPorts`, baud 9600..115200, N/E/O parity, 1/2 stop bits, 7/8 data bits). Slave ID: TCP 0..255; RTU 1..247.

## 8. EtherCAT

Bus master editor with three tabs:
1. **Scan Bus:** interface from `runtime.getNetworkInterfaces`, Scan via `runtime.scanEthercatDevices` (5000ms default). Matches against local ESI repository.
2. **Repository:** Manage ESI XML (import/delete/list). Backed by `useEsi()` port.
3. **Advanced:** `networkInterface`, `cycleTimeUs` (default 1000), `watchdogTimeoutCycles` (default 3), optional `taskPriority`.

Per-slave editor: identity, startup checks, Channel Mappings (`%IX/%QX` etc.), SDO parameters, Advanced (timeouts, watchdog, distributed clocks), Diagnostics.

## 9. Tasks & Instances

Rolled into the **Resources** screen: `GlobalVariablesEditor` + `TaskEditor` + `InstancesEditor`.

`PLCTask`: `{ name, triggering: 'Cyclic'|'Interrupt', interval: 'T#20ms', priority }`.
`PLCInstance`: `{ name, task, program }`.

## 10. Library manager

Two tabs:
- **System Libraries:** pool of `InstalledLibrary[]`. Add (`.stlib`, `.lib`, `.library`) / Remove. Bundled libs always-on. CoDeSys `.lib`/`.library` runs the STruC++ codesys importer.
- **Project Libraries:** subset enabled per project.

`SystemLibraryPou`: `{ name, type: 'function'|'function-block', language: 'il'|'st'|'ld'|'sfc'|'fbd'|'cpp', variables, body, documentation, extensible?, category? }`. `extensible: true` blocks render a `+` handle in graphical editors.

Library projects build to `.stlib` archives via `compiler.compileLibrary`.

## 11. Standard function block catalog

**Sources:**
- IEC standard FBs: `resources/bin/<platform>/<arch>/xml2st/_internal/plcopen/Standard_Function_Blocks.xml`.
- IEC standard functions (POU type `function`): `iec_std.csv`.
- Additional libs: `Additional_Function_Blocks.xml`, `Communication_Blocks.xml`, `MQTT.xml`, `Arduino_Function_Blocks.xml`, `CAN_Function_Blocks.xml`, `SM_Cards.xml`, `P1AM.xml`, `Jaguar.xml`, `SL-RP4.xml`.

### Standard Function Blocks

| Block | Category | Inputs | Outputs | Notes |
|---|---|---|---|---|
| `SR` | Bistable | `S1, R: BOOL` | `Q1: BOOL` | Set-dominant latch |
| `RS` | Bistable | `S, R1: BOOL` | `Q1: BOOL` | Reset-dominant latch |
| `SEMA` | Bistable | `CLAIM, RELEASE: BOOL` | `BUSY: BOOL` | Semaphore |
| `R_TRIG` | Edge | `CLK: BOOL` | `Q: BOOL` | Rising-edge pulse |
| `F_TRIG` | Edge | `CLK: BOOL` | `Q: BOOL` | Falling-edge pulse |
| `CTU` / `_DINT` / `_UDINT` / `_LINT` / `_ULINT` | Counter | `CU, R: BOOL, PV` | `Q: BOOL, CV` | Up counter (5 type variants) |
| `CTD` / `_DINT` / `_UDINT` / `_LINT` / `_ULINT` | Counter | `CD, LD: BOOL, PV` | `Q: BOOL, CV` | Down counter (5 type variants) |
| `CTUD` / `_DINT` / `_UDINT` / `_LINT` / `_ULINT` | Counter | `CU, CD, R, LD: BOOL, PV` | `QU, QD: BOOL, CV` | Up-down (5 variants) |
| `TP` | Timer | `IN: BOOL, PT: TIME` | `Q: BOOL, ET: TIME` | Pulse timer |
| `TON` | Timer | `IN: BOOL, PT: TIME` | `Q: BOOL, ET: TIME` | On-delay |
| `TOF` | Timer | `IN: BOOL, PT: TIME` | `Q: BOOL, ET: TIME` | Off-delay |

### Additional Function Blocks
`RTC`, `INTEGRAL`, `DERIVATIVE`, `PID`, `RAMP`, `HYSTERESIS`.

### Communication Blocks
`TCP_CONNECT`, `TCP_CLOSE`, `TCP_SEND`, `TCP_RECEIVE`.

### MQTT
`MQTT_CONNECT`, `MQTT_CONNECT_AUTH`, `MQTT_DISCONNECT`, `MQTT_SEND`, `MQTT_RECEIVE`, `MQTT_SUBSCRIBE`, `MQTT_UNSUBSCRIBE`.

### Arduino
`ARDUINOCAN_CONF`, `ARDUINOCAN_READ`, `ARDUINOCAN_WRITE`, `ARDUINOCAN_WRITE_WORD`, `CLOUD_BEGIN`, `CLOUD_ADD_BOOL`, `CLOUD_ADD_DINT`, `CLOUD_ADD_REAL`, `DS18B20`, `DS18B20_2_OUT`, `DS18B20_3_OUT`, `DS18B20_4_OUT`, `DS18B20_5_OUT`, `PWM_CONTROLLER`.

### CAN
`STM32CAN_CONF`, `STM32CAN_READ`, `STM32CAN_WRITE`.

### SM Cards (Sequent Microsystems HATs)
`SM_8RELAY`, `SM_16RELAY`, `SM_8DIN`, `SM_16DIN`, `SM_4REL4IN`, `SM_8MOSFET`, `SM_RTD`, `SM_BAS`, `SM_HOME`, `SM_INDUSTRIAL`.

### P1AM (Productivity1000)
`P1AM_INIT`, `P1_04AD`, `P1_08N`, `P1_08T`, `P1_16N`, `P1_16TR`, `P1_16CDR`.

### Other small libs
- Jaguar: `ADC_CONFIG`.
- SL-RP4: `ROTARY_SWITCH`.

### IEC standard functions (`iec_std.csv`, 89 functions)
- Type conversion: `*_TO_**`, `TRUNC`, `BCD_TO_**`, `*_TO_BCD`, `DATE_AND_TIME_TO_TIME_OF_DAY`, `DATE_AND_TIME_TO_DATE`.
- Numerical: `ABS`, `SQRT`, `LN`, `LOG`, `EXP`, `SIN`, `COS`, `TAN`, `ASIN`, `ACOS`, `ATAN`.
- Arithmetic: `ADD` (ext.), `MUL` (ext.), `SUB`, `DIV`, `MOD`, `EXPT`, `MOVE`.
- Time arithmetic: `ADD_TIME`, `ADD_TOD_TIME`, `ADD_DT_TIME`, `MULTIME`, `SUB_TIME`, `SUB_DATE_DATE`, `SUB_TOD_TIME`, `SUB_TOD_TOD`, `SUB_DT_TIME`, `SUB_DT_DT`, `DIVTIME`.
- Bit-shift: `SHL`, `SHR`, `ROR`, `ROL`.
- Bitwise: `AND`, `OR`, `XOR` (all ext.), `NOT`.
- Selection: `SEL`, `MAX` (ext.), `MIN` (ext.), `LIMIT`, `MUX` (ext.).
- Comparison: `GT`, `GE`, `EQ`, `LT`, `LE` (all ext.), `NE`.
- Character string: `LEN`, `LEFT`, `RIGHT`, `MID`, `CONCAT` (ext.), `CONCAT_DATE_TOD`, `INSERT`, `DELETE`, `REPLACE`, `FIND`.

`extensible: yes` functions accept additional pins past the declared minimum — `+` handle in graphical editors.

## 12. Address mapping (PLC → wire-protocol)

**Live code:** `editor/server/modbus-server/address-mapping-reference.tsx` — computes a full table at render from current buffer mapping.

**Mapping rule:** within each Modbus block, IEC segments are laid out **sequentially** in declared order, starting at Modbus address 0 of that block. Sizes counted in addressable units (bits for coils/discrete, 16-bit registers for holding/input).

- **Holding Registers (FC 3/6/16):** `%QW[0..N-1]` → modbus[0..qwCount-1], then `%MW`, then `%MD` (2 regs/value), then `%ML` (4 regs/value).
- **Coils (FC 1/5/15):** `%QX` first, then `%MX`. **Bit addresses formatted as `[byte].[bit]`** — `bitIndex 0 → %QX0.0`, `bitIndex 7 → %QX0.7`, `bitIndex 8 → %QX1.0`. So `%QX0.0 → coil 0, %QX0.7 → coil 7, %QX1.0 → coil 8`.
- **Discrete Inputs (FC 2):** `%IX0.0` → discrete input 0, same byte-bit rule.
- **Input Registers (FC 4):** `%IW[0..N-1]` (no overlay).

Sizes user-configurable: `qwCount`, `mwCount`, `mdCount`, `mlCount`, `qxBits`, `mxBits`, `ixBits`, `iwCount`. Max per segment: 1024 registers / 8192 bits. Defaults in `src/frontend/utils/modbus/generate-modbus-slave-config.ts`.

`%IB`/`%QB` (byte) and `%ID`/`%QD`/`%IL`/`%QL` (double/long input/output) only surface in S7Comm `BUFFER_TYPE_OPTIONS` — Modbus doesn't index them separately.

## 13. Build & compile

Pipeline (PLC project):
```
PLCProjectData
  → projectActions.syncVariableAliases()
  → strucpp.compile (ST→C++)                  // replaces legacy MatIEC iec2c
  → generate defines.h (pin map, modbus map, MD5)
  → arduino-cli OR openplc-compiler
  → for runtime targets: HTTP upload to webserver
  → for Arduino targets: USB upload via arduino-cli
  → for Simulator: load .hex into in-process AVR8JS
```

Build Options popover: `build-only`, `build-upload`, `clean-upload`. Library projects: `build-only`, `clean-upload` (emits `.stlib` archive).

Vendor screen editor renders board-package-specific screens declared in `boardInfo.vpp.screens[screenName]`.

## 14. Simulator

`OpenPLC Simulator` board → compiler `simulator`, platform `arduino:avr:mega`. Runs **in-process** via `avr8js` ATmega2560 emulator. Build flow loads `.hex` into emulator; emits `onStopped` events. Debugging via transport `modbus-serial`. 70 digital pins, 16 analog. Activity-bar Play starts/stops (auto-builds first).

## 15. Debugger

Protocol: custom Modbus PDU (FC 0x41–0x45) for variable read/write. Transports: `modbus-tcp` (v3), `websocket` (v4), `modbus-serial` (Sim).

Flow: save → debug-compile (with symbols + `.dbg` + MD5) → connect → `readProgramMd5`+`verifyMd5` → prompt to upload on mismatch → start polling via `useDebugPolling`.

UI: per-variable Debug checkbox in the Variables table. Debugger panel renders a time-series line chart of selected variables with pause/play, range selector (default 10s, 10-min buffer). **No breakpoints** — live variable inspection only.

## 16. Console / PLC logs

**Console:** build/compile/runtime messages. Filters: level (`info/warning/error`) + free-text search. `consoleActions.addLog({ id, level, message, tstamp? })` called from compiler, runtime, debugger, simulator, EtherCAT, package manager. Clicking a compile error log navigates to source via `useNavigateToCompileError`.

**PLC Logs panel:** separate panel for **runtime logs from a connected Runtime v4 target** (`hasRuntimeStats`).

## 17. Source control

Activity bar GitBranch icon. Two views:
- **Changes:** modified files; per-row Discard / Restore (modal-confirmed). Inline diff via Monaco DiffEditor. Stage + Commit message box.
- **History:** commit log with details panel.

Branches: status-bar entry with current branch + pending badge → switcher popover with create / delete. Dirty-workspace switch warning. Pull/push exist on the port but only surface via commit-details actions.

## 18. AI Engineer panel

Capabilities:
- `streamCompletion` — inline code completion (Monaco inline suggestion provider). Languages: `st | il | python | cpp`.
- `streamChat` — chat. Adds `ld | fbd`.
- `fetchEntitlements` / `fetchUsage` — plan + ACU accounting.
- Models: `'haiku' | 'sonnet'`.

Telemetry: `completion_requested|shown|accepted|dismissed|error|timeout`, `chat_message`, `chat_rating`, `conversation_*`, `acu_exhausted`, `upgrade_cta_clicked`.

Flow: click AI button → consent modal (first time) → opens chat panel right-rail. Inline completion provider registered when `hasAIAssistant` + AI enabled + user consented.

## 19. Search in project

Text search across POU names, variable names, comments, body contents. Results render in a tree grouped by POU and variable kind. Highlights matched substrings via `extractSearchQuery`.

## 20. Connecting to a vPLC / Orchestrators

Editor `Device Orchestrators` screen lists registered orchestrators (each expandable to its runtimes/devices). Click device → WebRTC handshake or HTTP connection.

1. Login modal: username + password → `jwtToken` stored.
2. If runtime has no users, create-user modal: username + password (`runtime.createUser`).
3. Board target auto-switches Simulator → runtime board.

Activity bar Play/Stop: shows "Connect to runtime first" if disconnected; `runtime.startPlc` / `runtime.stopPlc` otherwise. PLC status from `runtime.getStatus` (`STOPPED`/`RUNNING`).

## 21. Title bar / activity bar

Title bar: project name, save indicator, board selector quick access.

Workspace Activity Bar (top to bottom):
1. **Explorer** (Files icon).
2. **Source Control** (GitBranch icon, pending-changes badge).
3. (Divider)
4. **Default actions:** Search, Toolbox toggle (zoom), Build Options popover, Play/Stop, Debugger, AI Chat.
5. (Divider) **Context-dependent toolbox** (only when graphical editor active):
   - FBD: Block, Input/Output Variable, Connector, Continuation, Comment.
   - LD: Block, Coil, Contact, Delete-selected.
6. Bottom: **Exit** (close project, prompt to save if dirty).

## 22. Diagrams from JSON (docs viewers)

**Source:**
- FBD: `apps/frontend/src/components/docs/diagrams/FBDDiagramViewer.tsx`.
- LD: `apps/frontend/src/components/docs/diagrams/LadderDiagramViewer.tsx`.
- Samples: `apps/frontend/public/docs/diagrams/{fbd,ladder}/*.json`.

Both fetch JSON from `/docs/...` (block external URLs, `..` traversal, non-absolute paths). MDX usage: `<FBDDiagramViewer src="..." />` / `<LadderDiagramViewer src="..." />`.

### LD diagram schema

```jsonc
{
  "comment": "string",     // optional
  "rungNumber": 1,         // optional
  "elements": [ /* DiagramElement[] */ ]
}
```

`DiagramElement` variants:

```ts
// Contact
{ "type": "contact",
  "variant": "default" | "negated" | "risingEdge" | "fallingEdge",
  "variable": "name_string" }

// Coil
{ "type": "coil",
  "variant": "default" | "negated" | "set" | "reset" | "risingEdge" | "fallingEdge",
  "variable": "name_string" }

// Generic block
{ "type": "block",
  "name": "TON",
  "inputs": ["IN", "PT"],
  "outputs": ["Q", "ET"] }

// Parallel branching
{ "type": "parallel",
  "branches": [ [ /* DiagramElement[] */ ], [ /* DiagramElement[] */ ] ] }
```

Auto-layouts horizontally in `CANONICAL_WIDTH = 1000` viewBox. Variable labels above contacts/coils; edge contacts/coils show `P`/`N`; negated shows slash; set/reset shows `S`/`R`.

### FBD diagram schema

```jsonc
{
  "comment": "string",         // optional
  "diagramNumber": 1,          // optional
  "nodes": [ /* FBDNode[] */ ],
  "edges": [ /* FBDEdge[] */ ]
}
```

`FBDNode` discriminated union (each has `id, type, position: {x,y}, data`):

```ts
// Block
{ "id": "ton", "type": "block", "position": { "x": 280, "y": 50 },
  "data": {
    "name": "TON",
    "blockType": "function" | "function-block",
    "executionControl": false,         // optional. true => prepend EN/ENO
    "instanceName": "run_timer",       // optional tiny label above block
    "inputs":  [ { "name": "IN", "type": "BOOL" }, { "name": "PT", "type": "TIME" } ],
    "outputs": [ { "name": "Q",  "type": "BOOL" }, { "name": "ET", "type": "TIME" } ]
  } }

// Variables
{ "id": "in_var", "type": "input-variable" | "output-variable" | "inout-variable",
  "position": { "x": 50, "y": 60 },
  "data": { "name": "sensor1", "unresolved": false /* optional, amber warning */ } }

// Connector / continuation
{ "id": "c1", "type": "connector" | "continuation",
  "position": { "x": 200, "y": 100 },
  "data": { "label": "X1", "error": false /* optional */ } }

// Comment box
{ "id": "note", "type": "comment",
  "position": { "x": 0, "y": 0 },
  "data": { "content": "Multi-line\nnote text", "width": 200, "height": 80 } }
```

`FBDEdge`:
```ts
{ "id": "e1",
  "source": "<srcId>", "sourceHandle": "OUT",
  "target": "<dstId>", "targetHandle": "IN1" }
```

**Handle conventions:**
- Block: literal pin names from `data.inputs[].name` / `data.outputs[].name`. `executionControl: true` adds implicit `EN`/`ENO` first.
- `input-variable`: one output handle named `output`.
- `output-variable`: one input handle named `input`.
- `inout-variable`: input `input` left, output `output`/`output-variable` right.
- `connector` / `continuation`: single handle each, name ignored.

**Layout:** absolute pixels, viewer auto-fits via `computeViewBox`. Block 216 wide, 48px row pitch. Variables 128×32. To wire a block to a variable, align variable Y (`y+16`) with block pin Y (`y+48+48*index`).

## Cross-cutting

- **Atomic Design:** `_atoms`, `_molecules`, `_organisms`, `_features`, `_templates`. Editor screens are usually `_features/[workspace]/editor/<name>/index.tsx` inside a `_templates/[editors]/<...>-editor-template.tsx`.
- **Zustand store, 19 slices.** User-visible: `project`, `device`, `editor`, `tabs`, `workspace`, `ladder`, `fbd`, `console`, `library`, `version-control`, `ai`.
- **Capabilities** are board-scoped (`hals.json`) AND platform-scoped (`useCapabilities()`). A feature in code may be invisible if either gate is off.
- **Project capability matrix** (`projectCapabilities()` in `middleware/shared/ports/types.ts`) is the single source of truth for what shows in PLC vs library projects.
