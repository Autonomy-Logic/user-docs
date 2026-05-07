# Managing Device Status

Once your vPLC devices are running, you can monitor their health, control their lifecycle, and perform management actions from the platform. This page covers device statuses, available operations, and troubleshooting tips.

---

## Viewing Devices

### The Devices Table

From the orchestrator detail page, the **Devices** tab shows a table of all vPLC devices. Each row displays:

| Column | Description |
|--------|-------------|
| **Device Name** | The name you assigned. Sortable. |
| **Project** | The project deployed to this device, or `N/A`. Sortable. |
| **Status** | Color-coded label showing the device's current status. |
| **Uptime** | How long the device has been running (e.g., `24h 30m`). |
| **CPU Usage** | Current CPU utilization of the device. |
| **Memory Usage** | Current memory consumption of the device. |
| **Created At** | When the device was created. Sortable. |
| **Actions** | Three-dot menu (⋮) for management actions. |

You can **sort** by clicking column headers and **search** by name using the search bar above the table.

Click any device row to open its [device detail page](device-detail).

---

## Understanding Device Status

### Platform Status

The platform-level status appears as a color-coded label in the Devices table and on the device detail page:

| Status | Color | Meaning |
|--------|-------|---------|
| **Active** | Green | The device is responsive and working normally. |
| **Not Found** | Red | The device could not be reached. It may have been removed, or the orchestrator is offline. |
| **Unknown** | Gray | Status could not be determined. Typically when the orchestrator hasn't responded yet. |

### Device State

On the [device detail page](device-detail), the **Status** card shows the device's operational state:

- **running**: The device is up and actively executing.
- **exited**: The device has stopped (either intentionally or due to an error).
- **created**: The device exists but hasn't started yet.

### Running Flag

The **Running** indicator shows `Yes` or `No` and reflects whether the device's main process is actively executing. A device can have a "running" state while the OpenPLC Runtime inside it may be in different program states (empty, running a program, or idle).

---

## Device Lifecycle Operations

Control your vPLC devices through the **Actions** dropdown menu (⋮) on each device row.

### Restart

Restarts the vPLC device. The device is stopped and then started again.

**When to use:**

- The device is unresponsive or behaving unexpectedly.
- You've made configuration changes that require a fresh start.
- The runtime is in an error state.

**What happens:**

1. A confirmation modal appears: *"Are you sure you want to restart \<device name\>?"*
2. After confirmation, the device stops and starts again.
3. The uptime counter resets and the restart count increments by one.
4. Any loaded PLC program remains loaded. The runtime re-initializes it on startup.

The device may be briefly unreachable during the restart. Status updates automatically once it's back.

### Rename

Changes the device's display name.

1. A modal opens with the current name pre-filled.
2. Enter the new name (1–100 characters) and click **Save changes**.
3. The name updates immediately. This doesn't affect any running programs.

### Delete

Permanently removes the vPLC device from both the host machine and the platform.

1. A confirmation modal appears: *"Are you sure you want to delete \<device name\>? This action cannot be undone."*
2. After confirmation, the device is stopped, removed from the host, and deleted from the platform.
3. The device disappears from the Devices table.

> **Warning:** This action is irreversible. Any program loaded on the device is lost. Download your program from the IDE before deleting if you need to keep it.

---

## Start and Stop

In addition to the table actions, vPLC devices support **start** and **stop** commands:

- **Start**: Resumes a stopped device.
- **Stop**: Stops a running device. The device is preserved and can be started again later.

When you send a start or stop command, the platform communicates with the orchestrator, which carries out the operation and reports the new status.

---

## Monitoring Device Health

### Key Indicators to Watch

- **Uptime**: A healthy device shows steadily increasing uptime. If it keeps resetting to `0h 0m`, the device may be crashing and restarting repeatedly.
- **Restart Count**: A non-zero count isn't necessarily a problem (you may have restarted manually), but a rapidly increasing count indicates instability.
- **Status**: Should be `running` for normal operation. If you see `exited`, check if it was intentional.
- **Running Flag**: Should be `Yes` during normal operation.
- **Serial Port Status**: If your vPLC uses serial passthrough, check that ports show `Connected`. A `Disconnected` status means the physical device has been unplugged. An `Error` status requires investigation.

### Troubleshooting Common Issues

| Problem | What to Check |
|---------|---------------|
| Device shows "Not Found" | Check the orchestrator's status on the Orchestrators page. The orchestrator may be offline. |
| Device status is "exited" | Try restarting the device. Check if the host machine has sufficient resources (memory, disk space). |
| High restart count with low uptime | The device is likely crashing repeatedly. This can happen if the runtime version is incompatible with the host, a resource limit is hit, or there's a network config conflict. |
| Can't connect from the IDE | Verify the device status is **Active** and running. Check that the orchestrator is online. If using static IP, verify the IP on the [device detail page](device-detail). |

---

## Quick Reference: Device Actions

| Action | Where | Description |
|--------|-------|-------------|
| **Add Device** | Devices tab / empty state | Create a new vPLC on this orchestrator |
| **Restart** | Three-dot menu (⋮) | Stop and restart the device |
| **Rename** | Three-dot menu (⋮) | Change the device's display name |
| **Delete** | Three-dot menu (⋮) | Permanently remove the device |
| **Start** | Platform controls | Start a stopped device |
| **Stop** | Platform controls | Stop a running device |
| **View Details** | Click device row | Navigate to the device detail page |

---

## What's Next?

Now that your infrastructure is set up, start writing PLC programs:

➡️ [IDE Workspace Layout](../../openplc-editor/workspace-overview/workspace-layout): Learn the browser-based editor and start coding.
