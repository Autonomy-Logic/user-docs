# Running with the Simulator

The editor ships with a built-in **OpenPLC Simulator** that runs entirely in the browser. It's an `avr8js` ATmega2560 emulator (pure JavaScript), so there's no hardware to plug in and no server-side runtime to talk to. Compile your project, hit Play, and the program is running in a sandbox under your editor tab.

This is the fastest path from "I have an idea" to "let me try it" — ideal for learning, prototyping, and quick smoke tests before deploying to a real vPLC.

![The Device Orchestrators screen with OpenPLC Simulator selected by default at the top, and the user's two registered orchestrators (SLM-RP4 with 1 device and Toradex Ivy with 2 devices) listed below](../images/orchestrators-screen.png)

## Selecting the Simulator

The Simulator is the default target. Until you connect to an orchestrator-managed vPLC, anything you build runs on the Simulator.

If you're already connected to a vPLC and want to switch back:

1. In the project tree, expand **Device** and click **Orchestrators**.
2. The Orchestrators screen opens. **OpenPLC Simulator** sits at the top with a **Selected** badge.
3. Click on it. (If you were connected to a real vPLC, the editor disconnects from that vPLC and re-targets the Simulator.)

You don't need to log in to the Simulator. There's no separate user account.

## Running a program

With the Simulator selected:

1. Click the activity-bar **Build options** icon → **Build & Upload**. The Simulator counts as "connected" for the purposes of the upload step.
2. Watch the console — compilation steps log there.
3. Click **Play** in the activity bar. The Simulator boots, loads the firmware, and starts the program.
4. (Optional) Click the **Debugger** icon to watch live variable values on the chart.

The whole loop typically takes 10–30 seconds for a small project, most of which is the STruC++ compile.

## What the Simulator can and can't do

**What it can do:**

- Execute any IEC body the compiler accepts: ST, LD, FBD, IL, Python function blocks, C++ function blocks.
- Run timers, counters, edge-triggers — anything that operates on the simulated AVR's clock.
- Speak Modbus TCP server, OPC-UA server, S7Comm server — these are all part of the runtime image baked into the Simulator firmware.
- Connect outwards as a Modbus master to remote slaves running in the same browser session, or reachable from your local network (the runtime opens real sockets via the browser's network stack).
- Drive the debugger, the same as a real runtime would.

**What it can't do:**

- Touch any physical I/O. There's no hardware behind `%IX`, `%QX`, etc. — they exist in the emulator's memory image. Modbus / OPC-UA / S7Comm can read and write them, but no physical sensor or relay reacts.
- Persist anything across page reloads. The Simulator's state lives in the editor tab. Reload the page and the program is freshly cold-booted on the next Play.

If you need physical I/O — or a long-running PLC that survives page reloads — deploy to a vPLC instead. See **[Connecting to a vPLC](../connecting-to-runtimes)**.

## Behind the scenes

When you press Play with the Simulator selected, the editor:

1. Compiles your project through the **STruC++** pipeline (same compile path as for a real runtime).
2. Targets the `arduino:avr:mega` platform (Arduino Mega 2560 — what `avr8js` emulates).
3. Loads the resulting `.hex` into the in-browser `avr8js` core.
4. Starts the core's clock and hooks up the runtime's I/O bridges so server traffic, debugger queries, and Python/C++ block invocations all work as they would on real hardware.

Stopping the PLC (the same activity-bar Play button when running) halts the emulator's clock. Compile + upload again to swap in a new program — same flow as a real runtime.

## Limitations to keep in mind

- **Memory.** The emulated Mega has 256 KB flash and ~8 KB RAM. Very large projects can outgrow this. Real runtime targets (v4) have far more headroom; if you hit a memory error on the Simulator, try the program on a vPLC.
- **Performance.** Emulation overhead means the Simulator runs slower than the real chip. For timing-sensitive tests (sub-millisecond cycles), prefer a vPLC.
- **No retentive memory.** Page reload wipes everything. Test retentive logic on a real runtime where retain memory survives restarts.

## What's next

- **[Connecting to a vPLC](../connecting-to-runtimes)** — when you're ready to run on a real (or orchestrator-managed virtual) device.
- **[Project compilation](project-compilation)** — what the build options popover does in detail.
- **[Debugger](debugger)** — watch live variable values whether you're on the Simulator or a vPLC.
