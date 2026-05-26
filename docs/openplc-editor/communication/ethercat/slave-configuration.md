# Configuration

The **Configuration** tab is the third tab in the Slave Device Editor. It is the largest configuration surface for an EtherCAT slave and exposes every per-slave knob the master needs: startup verification, EtherCAT addressing, state-machine timeouts, watchdogs, and distributed clocks.

When you add a slave (either from a scan or from the repository), the editor fills the tab with sensible defaults that match the SOEM master's recommended values. You only need to come here when the defaults do not fit the device. Typically motion drives that need distributed clocks, or slaves that take unusually long to enter operational state.

The Configuration tab is organised into five labelled sections, top to bottom:

1. **Startup Checks**
2. **Addressing**
3. **Timeouts**
4. **Watchdog**
5. **Distributed Clocks (DC)**

## Startup Checks

Two checkboxes that decide what the master verifies before accepting a slave at the configured position.

| Checkbox | Default | Effect when checked |
|----------|---------|---------------------|
| **Verify Vendor ID** | On | Master refuses to bring the slave to OP if its reported vendor ID does not match the configured one. |
| **Verify Product Code** | On | Master refuses to bring the slave to OP if its reported product code does not match the configured one. |

Both default to on and you almost never want to turn them off. They are your defence against someone replacing a configured slave with a different model: instead of silently running with mismatched I/O, the master halts at startup with a clear identification error.

The two main reasons to disable a check:

- **Replacing a slave with a compatible model from the same vendor**: turn off Verify Product Code temporarily, swap the unit, then turn it back on once the configuration has been updated.
- **OEM segments where slaves carry generic vendor IDs** (rare; usually only relevant for white-label industrial products).

Do not leave verification disabled in production.

## Addressing

| Field | Default | Range | Hint |
|-------|---------|-------|------|
| **EtherCAT Address** | `0` | 0 -- 65535 | `0 = auto` |

The EtherCAT address is the 16-bit station address the slave gets after the master enumerates the segment. Leaving the value at `0` tells the master to assign one automatically based on the slave's position on the wire. Which is what you want in almost every case.

Set a non-zero address only when:

- You have a topology with multiple physical segments and need a stable station address that survives re-cabling.
- A specific application or third-party diagnostic tool expects to find a slave at a fixed address.

For a typical line-topology segment with one master, leave it at `0`.

## Timeouts

Three fields, all in milliseconds, controlling how long the master waits during the slave's startup state-machine transitions.

| Field | Default | Meaning |
|-------|---------|---------|
| **SDO (ms)** | `1000` | Maximum time the master waits for any single SDO read or write to complete. SDO traffic happens during startup parameter writes and during initial state transitions. |
| **I → P (ms)** | `3000` | Maximum time allowed for the slave to transition from **Init** to **Pre-Op**. |
| **P → S/S → O (ms)** | `10000` | Maximum time allowed for both **Pre-Op → Safe-Op** and **Safe-Op → Op** transitions. |

The defaults are generous and work for most catalog devices. When to extend them:

- **SDO**: motion drives that perform long internal calculations on parameter writes (some Beckhoff servo drives) may need 2000 -- 5000 ms.
- **I → P**: rarely needed; mostly a problem on segments with very long cable runs combined with slow slaves.
- **P → S / S → O**: large drives or cameras that load firmware blocks during this transition can need 30000 ms or more.

When to shorten them:

- For a desk-test segment of pure I/O terminals you can drop **P → S / S → O** to 2000 -- 5000 ms to fail faster on bad cabling.

## Watchdog

The watchdog section has two independent watchdogs. Each one has an enable checkbox and a time field that becomes editable only when the checkbox is on.

| Watchdog | Default enabled? | Default time | Meaning |
|----------|------------------|--------------|---------|
| **SM Watchdog** | On | `100` ms | Sync Manager watchdog. The slave declares the bus dead and goes safe if it does not receive a process-data update for this long. Keeps outputs from latching when the master crashes. |
| **PDI Watchdog** | Off | `100` ms | Process Data Interface watchdog. The slave declares the local controller dead if its on-board logic stops responding within this time. Useful only for slaves with internal logic; leave off for plain I/O terminals. |

For ordinary digital and analog I/O terminals, leave both at their defaults: SM on at 100 ms, PDI off. Tighten the SM watchdog (50 ms or 25 ms) on safety-relevant outputs where you want the field side to react quickly when the master goes silent. Loosen it (250 -- 500 ms) on slow segments where a single missed cycle can be a normal occurrence.

The PDI watchdog is only meaningful on slaves with their own microcontroller and a vendor recommendation to enable it; turning it on for a dumb terminal is harmless but accomplishes nothing.

## Distributed Clocks (DC)

The DC section synchronises the slave's local clock with the EtherCAT reference clock so that all slaves trigger their internal events at exactly the same moment. This is essential for **synchronised motion** (multiple drives moving in coordination), some **fast analog acquisition**, and any application that cares about sub-microsecond cross-slave timing.

| Field | Default | Meaning |
|-------|---------|---------|
| **Enable DC** | Off | Master turn for DC on this slave. Other DC fields stay disabled until this is on. |
| **Sync Unit Cycle (us)** | `0` | Cycle time of the slave's sync unit, in microseconds. `0` means inherit the master's cycle time, which is what most motion drives want. |

When **Enable DC** is on, two further sub-sections become editable:

### SYNC0

| Field | Default | Meaning |
|-------|---------|---------|
| **SYNC0** checkbox | Off | Enable the SYNC0 interrupt on this slave. |
| **Cycle (us)** | `0` | Cycle of the SYNC0 signal, in microseconds. `0` means use the master's cycle. |
| **Shift (us)** | `0` | Phase shift of SYNC0 relative to the master cycle, in microseconds. Used to stagger events across slaves. |

### SYNC1

| Field | Default | Meaning |
|-------|---------|---------|
| **SYNC1** checkbox | Off | Enable the SYNC1 interrupt on this slave. SYNC1 is offset from SYNC0 and used for two-phase events (e.g. "sample then publish"). |
| **Cycle (us)** | `0` | Cycle of the SYNC1 signal. |
| **Shift (us)** | `0` | Phase shift of SYNC1 relative to SYNC0. |

### When to enable DC

DC is **off by default** because most I/O terminals do not need it and turning it on adds latency overhead to every cycle. Enable it when:

- The vendor's manual for the slave explicitly says the application "requires distributed clocks". Typical for servo drives in CSP/CSV/CST modes, EtherCAT cameras, and high-speed analog acquisition.
- You need precise time-stamps across multiple slaves: a captured input on slave A and an output transition on slave B happen on the same wall-clock instant only if both are running on DC.
- You see motion control jitter that disappears when you enable DC on a test rig. Confirmation that the application is timing-sensitive.

For ordinary digital and analog I/O terminals (Beckhoff EL1xxx, EL2xxx, EL3xxx, EL4xxx, EL5xxx series for slow acquisition), leave DC off.

### The trade-off

DC tightens jitter and aligns events but consumes a small slice of the cycle-time budget on every cycle. On a 100 µs cycle this cost is noticeable; on a 1000 µs cycle it is negligible. If you experience cycle-time overruns after enabling DC across a large segment, raise the master cycle time first.

## Saving changes

Like the master configuration, slave changes take effect the next time the runtime starts the bus. The workspace is marked unsaved as soon as you edit any field; save the project (Ctrl+S) to persist the values.

## What's next?

- **[Startup Parameters](slave-startup-params)** if your slave needs SDO writes before going operational
- **[Channel Mappings](slave-channel-mappings)** to wire the slave's I/O to IEC variables
- **[Troubleshooting](troubleshooting)** if a slave is stuck in Pre-Op or Safe-Op and you need to know which timeout to extend
