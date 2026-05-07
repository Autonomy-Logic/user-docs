# Troubleshooting

This page is a checklist of common failures grouped by where you see them: in the **Bus Editor**, in the **Slave Device Editor**, in the **Repository**, and at runtime once the bus is started. Each entry describes the symptom in the editor's own words and gives a concrete fix.

## In the Bus Editor

### "EtherCAT Discovery Service Not Available" yellow banner

**Symptom.** The **Bus** tab shows a yellow banner with this text along with a more detailed message from the runtime. The **Scan** button is disabled.

**Most likely cause.** The runtime cannot send raw Ethernet frames because the Linux `CAP_NET_RAW` capability is missing on the process.

**Fix.** Add the capability to the systemd unit running the runtime:

```ini
[Service]
AmbientCapabilities=CAP_NET_RAW
CapabilityBoundingSet=CAP_NET_RAW
```

Run `systemctl daemon-reload` followed by a restart of the runtime service. The banner clears and the **Scan** button becomes active. See [Prerequisites](prerequisites) for the full setup.

### Scan button stays disabled

**Symptom.** No banner, but **Scan** is greyed out.

**Possible causes, in priority order.**

1. **The runtime is not connected.** Confirm the runtime indicator in the editor toolbar shows "connected". If it does not, fix the connection first.
2. **No network interface is selected.** Pick one from the **Network Interface** dropdown.
3. **The discovery service is not yet ready.** The editor checks the service status when the runtime first connects. If the runtime just came online, give it a second or two.

### "No devices found" after a successful scan

**Symptom.** The **Scan** completes (`Completed in <N>ms`) but the Scanned Devices table reads `No devices found. Click "Scan" to discover EtherCAT devices on the network.`

**Possible causes.**

| Cause | Check |
|-------|-------|
| Wrong NIC selected | Pick the NIC that is actually wired to the first slave. The dropdown also accepts a typed value if the runtime has not refreshed. |
| Cable not seated in the slave's IN port | EtherCAT is directional. Plugging into the OUT port instead of IN gives no response. |
| Slave not powered | Couplers like the EK1100 need a 24V supply on top of the EtherCAT cable. |
| EtherCAT NIC has no link | Check the link LED on both ends. If it is off, the cable, the slave, or the NIC has a hardware fault. |

### Selected device shows "No XML" badge

**Symptom.** A row in the Scanned Devices table has a small `No XML` badge next to the name. If you tick it and click **Add Selected**, the **Missing ESI XML for some devices** modal appears.

**Cause.** The runtime found the slave on the wire but no ESI XML in your repository describes that vendor / product / revision combination.

**Fix.**

1. Note the **Vendor** and **Product** values in the modal (or in the table itself).
2. Download the ESI XML for the device from the manufacturer's website.
3. Open the **Repository** tab and import the XML.
4. Re-run the scan and add the device again.

If the repository already contains an ESI for the same vendor and product code, the issue is likely a revision gap. The slave on the wire reports a revision newer or older than any covered ESI. Download the latest version from the vendor.

## In the Repository

### "<N> file(s) failed to parse" red banner

**Symptom.** After uploading one or more files, a collapsible red banner reads `<N> file(s) failed to parse`. Click it to see one row per failed file.

**Common reasons and fixes.**

| Error message contains | Likely cause | Fix |
|------------------------|--------------|-----|
| "File too large" | The file is larger than 100 MB. | Check that you uploaded the ESI itself, not a vendor zip with extras. |
| "No XML files found" | None of the files you dropped end in `.xml`. | The drop zone only accepts `.xml`. Extract the ESI from any vendor archive first. |
| Schema or parsing errors | The XML is malformed or non-ETG.2000. | Re-download the file from the vendor. Some vendors publish ESI variants for specific tools that do not parse cleanly. |
| Generic parse failure | The file is not actually an ESI. | Confirm you have the right file. Some vendors ship firmware in `.xml` form alongside the ESI. |

The other files you dropped at the same time still load. The banner is per-file, not per-batch.

### "No ESI files loaded. Upload files above to populate the repository."

This is the empty-state message in the Repository table when nothing has been uploaded. Drag your `.xml` files onto the zone above to populate it.

### Can't remove an ESI file

**Symptom.** Clicking **Remove** on a row in the Loaded Files table reports an error and the row stays.

**Cause.** A configured slave in some open project still references this ESI. The editor refuses the removal so that you do not orphan a slave.

**Fix.** Either remove the configured slave first (from the Bus tab in that project) or simply leave the ESI in the repository. The storage cost is trivial.

## In the Slave Device Editor

### "Device not found" message

**Symptom.** Opening a slave child node shows `The EtherCAT device could not be found. It may have been removed from the bus configuration.`

**Cause.** The slave was removed from the bus while a tab for it was still open.

**Fix.** Close the stale tab. Re-add the slave from the [Bus tab](bus-scan) if you removed it by mistake.

### "Device Info > ESI File: Not found"

**Symptom.** The **Device Info** tab shows `ESI File: Not found`.

**Cause.** The ESI XML this slave was matched against has been removed from the repository, but the slave configuration is still in the project.

**Fix.** Re-import the same ESI to the [Repository](bus-repository). The slave will pick it up the next time the project is opened.

### "No CoE Object Dictionary available for this device" on Startup Parameters

**Symptom.** The Startup Parameters tab shows this empty-state message.

**Cause.** The matched ESI does not include a CoE dictionary for this slave. For most plain digital terminals (e.g. EL1809, EL2809) this is normal. They have nothing configurable via SDO.

**Action.** None needed unless you have a specific reason to expect SDO writes. If you do, check that you imported the ESI with the most recent revision; some older revisions ship without the dictionary.

### Startup Parameters value reverts on type-out

**Symptom.** You type a value in the **Value** column, tab out, and the cell snaps to a different value.

**Cause.** The value was outside the data type's range and the editor clamped it. For example, `300` typed into a `UINT8` cell becomes `255`.

**Fix.** Check the **Type** column for the data type and the bit length. The editor will not let you write a value the slave will refuse.

## At runtime

### Master stuck in PRE-OP

**Cause and fix.** Almost always an ESI revision mismatch between the configured and the physical slave. Open the affected slave's [Device Info](slave-info) tab and compare the **Revision** field with what the manufacturer publishes for the unit on the wire. Download a fresh ESI and re-add the slave.

### Master stuck in SAFE-OP, not transitioning to OP

**Cause and fix.** A startup SDO write failed. Look at the runtime log for an entry containing `SDO error` followed by an index/sub-index pair. Match it to your [Startup Parameters](slave-startup-params) and either correct the value or, if the SDO is not yours to configure, remove that row from the table.

If the failing SDO is one the editor created automatically (for example via **Auto-configure from ESI defaults**), the device's ESI may declare a default the slave does not actually accept. Vendor errata. Replace the value manually.

### Working counter (WKC) mismatches

**Symptom.** The diagnostics panel shows a green `OPERATIONAL` master state but the runtime log fills with WKC mismatch warnings, or the master state oscillates between `OPERATIONAL` and `RECOVERING`.

**Possible causes, in priority order.**

| Cause | How to verify |
|-------|---------------|
| Managed switch in the segment | Trace the cable between the master and the first slave. Switches are not allowed; replace with a direct cable or an EtherCAT junction. |
| Cable longer than 100 m | Measure or check the install drawing. Above 100 m, packet integrity collapses. |
| Failing slave generating CRC errors on its ports | Inspect the slave's CoE error counters via the runtime log. |
| Heavy unrelated CPU load on the host | Check the host's CPU and IRQ utilisation. Raise **Task Priority** in the [Advanced tab](bus-advanced) on a real-time kernel. |
| Cycle time too aggressive | If overruns are reported in the runtime log, increase the cycle time in the [Advanced tab](bus-advanced). |

### A slave is missing from the per-slave table

**Symptom.** The Diagnostics master state is `OPERATIONAL` with `slave_count` lower than the number of configured slaves.

**Cause.** The cable upstream of the missing slave is broken or unplugged. EtherCAT enumerates from the master outward; the first missing slave is the one immediately downstream of the break.

**Fix.** Inspect the cable between the last slave that did appear and the first missing one. Replace the cable or re-seat both connectors.

### "Cycle-time overrun" warnings in the runtime log

**Cause.** The host could not finish a process-data cycle within the configured cycle time. The bus continues to run but with degraded determinism.

**Fix.**

1. Increase **Cycle Time (microseconds)** in the [Advanced tab](bus-advanced). Use the table in [Prerequisites](prerequisites) for guidance.
2. If the host is loaded with other workloads, move them off or onto a dedicated CPU core.
3. On a real-time kernel, raise **Task Priority** to give the EtherCAT cyclic task more headroom against other real-time tasks.

## What's next?

- **[Diagnostics](diagnostics)** for the runtime status panel reference
- **[Configuration](slave-configuration)** for slave-level timeouts and watchdog tuning
- **[Communication Protocols Overview](../README)** to compare EtherCAT with the other supported protocols
