# Worked example

This page walks end-to-end through configuring a small but realistic EtherCAT segment in Autonomy Edge. The hardware is a Beckhoff EK1100 coupler followed by mixed digital and analog terminals, which is the most common starting point for EtherCAT in industrial deployments. Every step uses the editor exactly as it is, no custom scripting.

## What we are building

| Position | Device | Function | I/O |
|----------|--------|----------|-----|
| 1 | Beckhoff EK1100 EtherCAT Coupler (2A E-Bus) | Bus coupler | None. Passes E-bus to terminals downstream |
| 2 | Beckhoff EL1809 16-channel digital input | 16 24V digital inputs | `%IX0.0` -- `%IX1.7` |
| 3 | Beckhoff EL2809 16-channel digital output | 16 24V digital outputs | `%QX0.0` -- `%QX1.7` |

This matches the segment used in the screenshots throughout the EtherCAT pages.

The wiring is a single CAT5e cable from the Linux host's dedicated NIC into the EK1100's IN port. The downstream terminals plug into the coupler's E-bus side. No managed switch is present.

## Step 1: Prerequisites

Before opening the editor, make sure the host meets the [Prerequisites](prerequisites):

- Runtime v4 on Linux.
- A second NIC dedicated to EtherCAT, separate from the host's management network.
- `CAP_NET_RAW` granted to the runtime (typically via the systemd unit override described in Prerequisites).
- The EtherCAT NIC connected to the EK1100's IN port. The EK1100 is powered.

Plug the cable in, confirm the EK1100 link LED is solid, and continue.

## Step 2: Add the EtherCAT bus to the project

1. Open the project in the Autonomy Edge editor.
2. Click the **+** next to the project name.
3. Select **Remote Device**.
4. Type `eth` in **Device name**.
5. Choose **EtherCAT** from the **Protocol** dropdown.
6. Click **Create**.

The bus appears under **Remote Devices** as `eth`. Click it to open the EtherCAT Bus Editor. The header reads `EtherCAT Bus: eth` with the subtitle `EtherCAT Master Configuration`. The **Bus** tab is selected by default.

## Step 3: Upload the ESI files

The Beckhoff terminals are Beckhoff Automation devices, and Beckhoff publishes one ESI XML per terminal series. For our segment we need:

- `Beckhoff EK11xx.xml` (covers the EK1100 family)
- `Beckhoff EL1xxx.xml` (covers the EL1809 along with the rest of the EL1xxx digital input series)
- `Beckhoff EL2xxx.xml` (covers the EL2809 along with the rest of the EL2xxx digital output series)

Download the three files from the Beckhoff website (search for "Beckhoff ESI files"), then:

1. Switch to the **Repository** tab in the Bus Editor.
2. Drag the three `.xml` files onto the **ESI Device Files** drop zone. The progress display shows each file as it parses.
3. When parsing finishes, the **Loaded Files** table shows the three files with a `Beckhoff Automation GmbH & Co. KG (0x2)` vendor and the device count for each.

You should see something like:

```
Loaded Files (3) - 317 device(s)

Beckhoff EK11xx.xml    Beckhoff Automation GmbH & Co. KG (0x2)    24
Beckhoff EL1xxx.xml    Beckhoff Automation GmbH & Co. KG (0x2)    155
Beckhoff EL2xxx.xml    Beckhoff Automation GmbH & Co. KG (0x2)    138
```

The device counts will vary as Beckhoff publishes new revisions; the structure is the same.

## Step 4: Set the master configuration

1. Switch to the **Advanced** tab.
2. Confirm **ENABLE BUS** is on.
3. Leave **CYCLE TIME (MICROSECONDS)** at `1000`. Three slaves on a clean segment is well within the default's headroom.
4. Leave **TASK PRIORITY** at `1` for a development host. On a PREEMPT_RT industrial PC you can raise it later.
5. Leave **WATCHDOG TIMEOUT (CYCLES)** at `3`.

These defaults are appropriate for a segment of this size. Save the project (Ctrl+S).

## Step 5: Scan and add the slaves

1. Switch back to the **Bus** tab.
2. Confirm the **Network Interface** dropdown shows the NIC connected to the EK1100. If your second NIC is `enp4s0` (typical on a desktop tower) or `eth1` (typical on a single-board computer), pick that one. Avoid `lo` and your management interface.
3. Make sure the runtime is connected. The **Scan** button activates only when both the runtime is reachable and the EtherCAT discovery service is available.
4. Click **Scan**. The button shows **Scanning…** while the master enumerates the segment. After a few seconds the **Scanned Devices** table fills in:

```
Pos  Name                                       Vendor    Product
1    EK1100 EtherCAT Coupler (2A E-Bus)         0x0002    0x044C2C52
2    EL1809 16Ch. Dig. Input 24V, 3ms           0x0002    0x07113052
3    EL2809 16Ch. Dig. Output 24V, 0.5A         0x0002    0x0AF93052
```

Each row should be free of the `No XML` badge. If a row has it, the matching ESI is missing or its revision does not match. Re-check Step 3 and look at the slave's **Device Info** for the revision the wire is reporting.

5. Tick the checkbox at the top of the table to select all three rows.
6. Click **Add Selected (3)**.

The three slaves move into the **Configured Devices** panel on the right. The project tree updates: under **Remote Devices > eth** you now see three child nodes:

- `EK1100 EtherCAT Coupler (2A E-Bus)`
- `EL1809 16Ch. Dig. Input 24V, 3ms`
- `EL2809 16Ch. Dig. Output 24V, 0.5A`

## Step 6: Inspect the channel mappings

1. Click the `EL1809` child node. The Slave Device Editor opens with the **Channel Mappings** tab selected.
2. The toolbar shows `All (16)`, `Inputs (16)`, `Outputs (0)`.
3. The table is pre-populated with 16 rows of `Input`, `BOOL`, with addresses `%IX0.0` through `%IX1.7`.
4. The **Alias** column is empty. Optionally fill in human-readable names: `pump_running`, `tank_level_high`, `e_stop_status`, and so on.

5. Click the `EL2809` child node. Same layout, but every row is `Output`, `BOOL`, with addresses `%QX0.0` through `%QX1.7`. The **Inputs (0) / Outputs (16)** filters confirm there are no inputs.

6. Click `EK1100`. **Channel Mappings** shows `No channels available for this device.`. Couplers do not contribute process data, only mechanical and bus continuity. This is expected.

## Step 7: Tune the per-slave configuration if needed

For this segment, the default per-slave configuration is correct. Spot-check one slave to be sure:

1. Click `EL1809`, then the **Configuration** tab.
2. Confirm **Verify Vendor ID** and **Verify Product Code** are both ticked (defaults).
3. **Addressing > EtherCAT Address** = `0` (auto, default).
4. **Timeouts**: SDO 1000, I → P 3000, P → S/S → O 10000. Defaults.
5. **Watchdog**: SM Watchdog on at 100 ms; PDI Watchdog off at 100 ms. Defaults.
6. **Distributed Clocks (DC)**: Enable DC off. Defaults. Digital terminals do not need DC.

No edits required. Repeat for `EL2809` if you want to be thorough; results are the same.

## Step 8: Use the addresses in your program

With the segment configured, you can wire the I/O into Ladder, ST, or FBD code in the project. A trivial pump-control rung in Ladder:

```
+----( IX0.0 )-----( IX0.1 )---+----( QX0.0 )---+
|    pump_running   tank_low   |    pump_relay  |
+------------------------------+----------------+
```

In Structured Text:

```pascal
PROGRAM main
VAR
    pump_running AT %IX0.0 : BOOL;
    tank_low     AT %IX0.1 : BOOL;
    pump_relay   AT %QX0.0 : BOOL;
END_VAR

pump_relay := pump_running AND NOT tank_low;
END_PROGRAM
```

The `%IX0.0`, `%IX0.1`, `%QX0.0` references resolve directly to the EL1809 input bits and the EL2809 output bit you mapped earlier. There is no separate "EtherCAT bind" step.

## Step 9: Run

1. Save the project (Ctrl+S).
2. Compile and transfer the program to the runtime as you would for any project.
3. The runtime starts the EtherCAT bus on first program execution.
4. Watch the [Diagnostics](diagnostics) panel. Within a couple of seconds the master state should transition `IDLE → SCANNING → CONFIGURING → OPERATIONAL`. The per-slave table should show all three slaves at `OP` with `Errors = 0`.

5. Toggle a 24V signal on one of the EL1809 inputs. The pump_relay output on the EL2809 should respond per your logic.

## Adding more terminals later

The same flow extends naturally:

- For an additional terminal in the EL3xxx (analog input) family, download `Beckhoff EL3xxx.xml` to the repository and re-scan. The new slave appears at the next position with `Input` channels of `INT` or `UINT` type mapped to consecutive `%IW` addresses.
- For an EL4xxx analog output, repeat with `Beckhoff EL4xxx.xml`. Channels are mapped to `%QW`.
- For mixed analog/digital terminals, the editor's IEC-type table in [Channel Mappings](slave-channel-mappings) shows the exact mapping.

The master cycle time (1000 µs default) handles up to a few dozen of these comfortably. Past that, follow the cycle-time floor table in [Prerequisites](prerequisites) to size the cycle for the segment.

## What's next?

- **[Troubleshooting](troubleshooting)** if any slave fails to reach OP
- **[Diagnostics](diagnostics)** for what to monitor while the bus is running
- **[Communication Protocols Overview](../README)** to compare EtherCAT with the other supported protocols
