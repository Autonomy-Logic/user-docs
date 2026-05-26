# Diagnostics

When the runtime is connected and the EtherCAT plugin is active, a **runtime status panel** reports the live state of the master and every slave on the segment. The panel is **read-only**: it does not configure anything. Treat it as the place you go to confirm that the bus is healthy, not to change what it does.

This page describes what each indicator means and what to do when one of them goes red.

> **This page describes what you will see at runtime.** All other pages in this section describe the editor in design mode. You only see the diagnostics view once a Runtime v4 host is connected to the project, the PLC program with the EtherCAT configuration is loaded, and the runtime has started cycling the bus.

## Master state

The header of the diagnostics panel shows the master's plugin state with a coloured dot, the state name in matching colour, and a one-line summary in parentheses (e.g. `OPERATIONAL (3 slaves, WKC=12)`). The state indicates what the master is doing right now:

| State | Dot colour | What it means |
|-------|-----------|----------------|
| `IDLE` | Grey | The plugin is loaded but the bus has not been started yet. Normal during the first second after the runtime boots. |
| `SCANNING` | Blue | The master is sweeping the segment to identify slaves. Normal during startup. |
| `CONFIGURING` | Blue | The master is writing startup parameters (SDOs) and bringing slaves through Init → Pre-Op → Safe-Op. Normal during startup; lasts longer if the segment is large or has motion drives. |
| `TRANSITIONING` | Blue | A slave is moving between EtherCAT states. Brief; if it persists for more than a few seconds, look at the per-slave table for the culprit. |
| `OPERATIONAL` | Green | The bus is running. Process data is being exchanged on every cycle. This is the steady-state value you want to see. |
| `RECOVERING` | Yellow | At least one slave dropped out and the master is trying to bring it back. Investigate cabling and power. |
| `ERROR` | Red | The bus is in a fault state. Read the per-slave table and the runtime log for details. |
| `STOPPED` | Grey | The bus has been stopped (typically because the PLC program was halted). Restart the program to resume. |

A **Refresh** button on the right of the header re-polls the runtime immediately. The panel polls automatically every two seconds; manual refresh is useful only when you want to see the effect of a change you just made.

The summary in parentheses always shows:

| Field | Meaning |
|-------|---------|
| Slave count | Number of slaves the master detected on the segment. Should match the number of configured slaves in your project. A lower number means at least one slave failed to come up. |
| `WKC=<N>` | The **expected working counter** for one process-data cycle. The working counter is incremented by every slave that successfully reads or writes its slice of the frame; the master compares the actual count to this expected value to confirm every slave participated. |

## Per-slave table

Below the header, a table lists every slave the master discovered with one row per slave. The columns are:

| Column | Meaning |
|--------|---------|
| **Pos** | Position on the daisy-chain (1, 2, 3, …). Matches the **Pos** column in the Bus Editor's Configured Devices panel. |
| **Name** | Slave name as taken from the matched ESI XML at startup. |
| **State** | The slave's current EtherCAT state machine value: `INIT`, `PRE-OP`, `SAFE-OP`, or `OP`. Coloured green when `OP` and healthy, red when `has_error` is set, yellow otherwise. |
| **AL Status** | The AL (Application Layer) status code reported by the slave when it is **not** in OP. `-` when the slave is OP. A non-zero hex code points to a precise error type in the slave's documentation (e.g. `0x001A` = invalid mailbox configuration). |
| **Errors** | Cumulative error count since the bus started. `0` is healthy; non-zero values are highlighted in red. |

A row whose slave has `has_error = true` is highlighted with a pale red background so you can spot it in a long list.

## State machine and what to do when stuck

EtherCAT slaves go through four states on the way to running:

```
Init → Pre-Op → Safe-Op → Op
```

If a slave never reaches Op, the state column tells you which transition is failing.

| Stuck at | Likely cause | Action |
|----------|--------------|--------|
| `INIT` | Cable break upstream of this slave; the master cannot reach it. | Check the wire and connectors between this slave and the previous one. The first slave that fails to reach `INIT` is usually the one immediately downstream of the broken link. |
| `PRE-OP` | ESI revision mismatch between configured and physical slave. | Check **Device Info** for this slave; download a newer ESI from the vendor and re-add the slave. |
| `SAFE-OP` | A startup SDO write failed. | Check the runtime log for an SDO error code. Adjust the value in [Startup Parameters](slave-startup-params) and restart the bus. |
| Toggling | Wiring or power issue causing the slave to drop in and out. | Check 24V supply on the slave, verify the cable's CAT5e/6 rating, and look for a managed switch in the segment (which is not allowed). |

## WKC mismatches

If the **State** column reads `OP` for every slave but the master state is `RECOVERING` or `ERROR`, the most likely cause is a **working counter mismatch**: the actual WKC seen on the wire does not match the expected WKC. This typically means the segment is unstable. Packets are getting corrupted or dropped between slaves.

Common causes:

- A **managed switch** between the master and the slaves. Switches break the protocol; remove them and use a direct cable or an EtherCAT junction.
- A cable run **longer than 100 m**.
- An unshielded cable in an electrically noisy environment.
- A failing slave whose port is producing CRC errors (some slaves expose CRC counters in CoE).

## Reading the runtime log

The diagnostics panel covers the high-level state of the bus. For granular detail (which exact SDO failed, which AL status code was returned, what the master's recovery loop is doing), open the runtime log. Each EtherCAT plugin event is tagged with the master name and includes the slave position and CoE indices when relevant. Use the runtime log alongside the diagnostics panel for any non-trivial troubleshooting.

## What's next?

- **[Troubleshooting](troubleshooting)** for a checklist of UI- and runtime-visible failures with their fixes
- **[Configuration](slave-configuration)** to extend timeouts when a transition consistently fails
- **[Startup Parameters](slave-startup-params)** to fix bad SDO writes that prevent SAFE-OP
