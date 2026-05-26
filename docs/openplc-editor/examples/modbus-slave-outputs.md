# Worked example: Modbus slave, expose digital outputs

Set up your vPLC as a Modbus TCP slave, drive `%QX0.0` from a small ST program, and read it back from an external Modbus client. This is the lightest-weight way to integrate a vPLC with SCADA, an HMI, or any monitoring system that speaks Modbus.

**Surfaces exercised:** Modbus TCP server configuration, the buffer mapping accordion, the address mapping rule, the Servers branch in the project tree, deploying to either the Simulator or a vPLC.

**Expected time:** about 10 minutes.

## What we're building

A vPLC that:

1. Toggles a `BOOL` output every two seconds.
2. Exposes that output as **Modbus coil 0**.
3. Lets an external Modbus client (or `mbpoll`) read or write that coil.

## Step 1: The program

Create a new ST program. Add two variables:

| Name | Class | Type | Location |
|---|---|---|---|
| `pulse` | Local | BOOL | (empty) |
| `out_bit` | Local | BOOL | `%QX0.0` |

The `Location` on `out_bit` is the IEC address, `%QX0.0` is "output byte 0, bit 0". The Modbus server will expose this address as Modbus coil 0.

Add a TON timer to drive the pulse:

```iec
VAR
    timer : TON;
END_VAR

(* main body *)
timer(IN := NOT timer.Q, PT := T#2s);
IF timer.Q THEN
    out_bit := NOT out_bit;
END_IF;
```

The TON's `Q` goes high two seconds after `IN` becomes true. We feed `NOT timer.Q` into `IN`, so as soon as `Q` fires, `IN` drops, the timer resets, and the cycle restarts. Net effect: `Q` pulses true for one PLC cycle every two seconds. Each pulse flips `out_bit`.

## Step 2: Add the Modbus server

1. In the project tree, click **`+`** at the top.
2. Pick **server** in the popover, then **Modbus / TCP**.
3. Name it `modbus` and click **Create**.
4. The new server appears under **Servers**. Click it to open the configuration editor.

## Step 3: Configure the server

In the **Server Configuration** section at the top:

- **Enabled**: on.
- **Network Interface**: `0.0.0.0`.
- **Port**: `502`.

In the **Buffer Mapping** accordion, expand **Coils**:

- `%QX` count: `8` (so coils 0–7 cover `%QX0.0`–`%QX0.7`).
- `%MX` count: `0` (we don't need memory bits exposed for this demo).

The other segments (Holding Registers, Discrete Inputs, Input Registers) can stay at their defaults. They just won't be used.

Open the **Address Mapping Reference** accordion to confirm: it should show `Modbus coil 0 ⇔ %QX0.0` for the first row.

## Step 4: Build and run

If you're running on the **Simulator**:

1. Click **Start Simulator**. Watch the console for `Simulator started`.
2. The Modbus server binds to `127.0.0.1:502` inside the browser's network bridge.

If you're running on a **vPLC** (orchestrator-managed):

1. Open the Orchestrators screen, expand your orchestrator, pick a vPLC, click **Connect**, log in.
2. Click **Build options** → **Build & Upload**.
3. Click **Play** to start the program.
4. The Modbus server is now reachable at the vPLC's IP on port `502`.

## Step 5: Read coil 0 from a Modbus client

Install [`mbpoll`](https://github.com/epsilonrt/mbpoll) (`brew install mbpoll` on macOS, `apt install mbpoll` on Debian/Ubuntu) and run:

```bash
# Replace 127.0.0.1 with the vPLC's IP if you're not on the Simulator
mbpoll -t 0 -r 0 -c 1 127.0.0.1
```

`-t 0` selects coil function codes (FC 1 read, FC 5 write). `-r 0` is the coil reference (0-based). `-c 1` asks for one coil. You should see:

```
-- Polling slave... Ctrl-C to stop)
[0]: 0
[0]: 1
[0]: 0
[0]: 1
...
```

The value flips every two seconds, matching `out_bit`.

## Step 6: Write coil 0 from outside

You can also push values **into** `%QX0.0` over Modbus:

```bash
mbpoll -t 0 -r 0 -1 127.0.0.1 1
```

`-1` means "single write, then exit". This sends FC 5 (Write Single Coil) with value `1` to address 0. Watch the Debugger in the editor: `out_bit` flips to `TRUE` for the next two seconds, then the ST program flips it back.

This is the heart of integration: the external client and the PLC share the same address, and either can change it. Whoever wrote last wins.

## Address mapping recap

Within the Coils block:

| Modbus coil | IEC address |
|---|---|
| 0 | `%QX0.0` |
| 1 | `%QX0.1` |
| 2 | `%QX0.2` |
| ... | ... |
| 7 | `%QX0.7` |
| 8 | `%QX1.0` |

The bit numbering follows the IEC byte/bit convention. See **[Modbus addressing](../communication/modbus/addressing)** for the full mapping rule.

## Troubleshooting

**`Connection refused` from mbpoll.** The runtime isn't listening on port 502. On macOS / Linux, ports below 1024 sometimes need elevated privileges. Change the server's port to `1502`, restart the PLC, and add `-p 1502` to the mbpoll command.

**Reads always return 0.** Confirm the variable's `Location` is `%QX0.0` (not `%MX0.0`, not just `Local` with no Location). The Modbus server only exposes addresses you've put in the buffer mapping.

**Writes return success but the PLC doesn't reflect them.** Your ST program is overwriting them. In this example, the toggle every 2 s wins, external writes only persist until the next pulse fires.

## Where to next

- **[Modbus server](../communication/modbus/server)**: full reference for every server field.
- **[Modbus addressing](../communication/modbus/addressing)**: the canonical mapping rule with worked examples for all four block types.
- **[OPC-UA: read a variable from UaExpert](opcua-read)**: same idea, different protocol.
