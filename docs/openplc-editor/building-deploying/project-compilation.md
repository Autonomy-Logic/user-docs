# Building a project

The **Build options** icon in the activity bar (the download icon, between Zoom and Play) opens a small popover with three actions:

| Action | What it does |
|---|---|
| **Build only** | Compile the project. Doesn't touch the connected vPLC. Useful for quick syntax checks without redeploying. |
| **Build & Upload** | Compile, then HTTP-upload the result to the connected vPLC. Doesn't start the PLC; you press **Play** for that. Disabled if you're not connected. |
| **Clean Upload** | Force a full rebuild (discards build cache) and then upload. Use when something seems off and you suspect the cache. Disabled if you're not connected. |

## The build pipeline

Each compilation runs the same sequence:

1. **Save** any unsaved bodies.
2. **Sync variable aliases** — for each variable bound to a producer (Modbus master point, EtherCAT channel, etc.), resolve the current address via the alias registry.
3. **STruC++ compile** — translate every POU body to C++ source. (Earlier builds called out to MatIEC's `iec2c`; the current pipeline uses STruC++ as a drop-in replacement.)
4. **Generate `defines.h`** — pin map, Modbus address map, MD5 of the program, runtime-side hooks.
5. **Compile to binary** — `arduino-cli` for Arduino-class targets (desktop only), `openplc-compiler` for runtime targets.
6. **Upload** (if you picked **Build & Upload** or **Clean Upload**) — HTTP POST to the runtime's webserver.

The console shows each step as it runs, with timestamps. A successful run ends with `Compilation completed successfully`.

## Reading errors

When the compiler returns an error, the console message is **clickable** — clicking it jumps to the offending source line in the appropriate POU body.

Typical compile errors and what they mean:

- **Syntax errors** — usually a missing semicolon in ST, or an unclosed comment.
- **Type errors** — assigning a `REAL` to a `BOOL`, calling a function block with wrong-typed inputs, etc. STruC++ reports the offending line and the expected vs. actual type.
- **Undeclared variable** — referenced but not in the POU's variable table (or globals). Add it before retrying.
- **Library not enabled** — using a block from a library that isn't enabled for this project. Open the **Library Manager** and tick it on.
- **Address collision** — two variables claim the same `Location`. Pick a non-overlapping address.

## Build without a connection

You can **Build only** any time, with or without a connected vPLC. This validates your code and produces the build artifacts; it just doesn't ship them anywhere.

`Build & Upload` and `Clean Upload` are disabled in the popover until the editor has a live connection. Click **Orchestrators**, log in to a vPLC, then come back.

## Build artifacts

The compile pipeline produces:

- `defines.h` — the generated header.
- A platform-specific binary (`.bin`, `.hex`, or similar) inside `build/`.
- A debug symbol map (`.dbg`) used by the debugger to read variables by name.
- An MD5 hash of the final binary, used by the debugger to verify the runtime is executing the same build the editor just compiled.

These live inside the project's `build/` directory and are gitignored — no need to commit them.

## What's next

- **[Deployment to a vPLC](deployment-vplc)** — the upload step in detail.
- **[Debugger](debugger)** — live variable inspection on the running PLC.
- **[Console & PLC Logs](../workspace-overview/console-debugging)** — read the build stream and the runtime's own logs.
