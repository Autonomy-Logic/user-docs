# Orchestrator Overview and Controls

Once your orchestrator is linked and online, you can monitor its health, view resource charts, manage its vPLC devices, and perform control actions. This page covers the orchestrator detail page and the orchestrators list.

---

## Navigating to the Detail Page

From the **Orchestrators** page, click any orchestrator to open its detail page. A breadcrumb at the top (`Orchestrators > <name>`) lets you navigate back.

The detail page has two tabs:

- **Overview** — System information and resource usage charts.
- **Devices** — All vPLC devices on this orchestrator.

---

## The Overview Tab

The Overview tab shows a snapshot of your orchestrator's current state and resource usage.

### Status and System Info

A card at the top displays the orchestrator's name, status, and key system details:

- **Status** — Color-coded label:
  - **Active** (green) — Connected and healthy.
  - **Not Found** (red) — Cannot be reached (agent may not be running or has lost connectivity).
  - **Unknown** (gray) — Status could not be determined.
- **Network** — IP addresses of the host's physical network interfaces, shown as `interface_name (ip_address)`.
- **Memory** — Total RAM on the host (GB).
- **OS** — Host operating system (e.g., `Ubuntu 24.04 LTS`).
- **CPU** — Number of logical CPUs available.
- **Disk** — Total disk space (GB).
- **Description** — The description you provided when creating the orchestrator, or `-` if none.

### Resource Usage Charts

Below the system info card, two interactive line charts show resource consumption over time:

- **CPU Usage Chart** — CPU utilization as a percentage (0–100%) over time.
- **Memory Usage Chart** — Memory usage in megabytes (MB) over time.

Each chart has a dropdown to select the time window:

| Period | Description |
|--------|-------------|
| **1h** | Last 1 hour (default) |
| **6h** | Last 6 hours |
| **12h** | Last 12 hours |
| **24h** | Last 24 hours |

The two charts work independently — you can view CPU over 24 hours while viewing memory for the last hour.

---

## The Devices Tab

The Devices tab shows a table of all vPLC devices on this orchestrator.

### Device Table

| Column | Description |
|--------|-------------|
| **Device Name** | The name you gave the device. |
| **Project** | The project deployed to this device, or `N/A` if none. |
| **Status** | Current status (e.g., `running`, `stopped`, `error`), color-coded. |
| **Uptime** | How long the device has been running (e.g., `24h 30m`). |
| **CPU Usage** | Current CPU utilization of the device. |
| **Memory Usage** | Current memory consumption of the device. |
| **Created At** | When the device was created. |
| **Actions** | A dropdown menu with device actions. |

You can **sort** by Device Name, Project, and Created At by clicking the column headers. A **search bar** above the table filters devices by name in real time.

### Device Actions

Each device row has a three-dot menu (⋮) with:

- **Restart** — Restarts the device. A confirmation modal appears first.
- **Rename** — Opens a modal to change the device's name.
- **Delete** — Permanently removes the device. A confirmation modal warns this can't be undone.

### Adding a Device

Click the **Add Device** button to create a new vPLC on this orchestrator. See [Creating a vPLC Device](../vplc-management/creating-vplc) for the full walkthrough.

Click any device row to open its [detail page](../vplc-management/device-detail).

---

## Orchestrator Management

From the orchestrators list page, each row has a three-dot menu (⋮) with management actions.

### Rename

Opens a modal to change the orchestrator's display name (up to 100 characters).

### Delete

Opens a confirmation modal. What happens depends on whether the orchestrator is online:

**If online:** The platform sends a cleanup command to the agent, which removes all devices and then removes itself from the host. The orchestrator and all its devices are removed from the platform.

**If offline:** The platform can't communicate with the agent. You'll be offered a **Force Delete** option that removes the orchestrator and its devices from the platform database only.

> **Tip:** If you force-delete an offline orchestrator, the software may still be running on the host machine. You can clean it up manually by running the install script again or contacting your system administrator.

---

## Filtering the Orchestrators List

The orchestrators list includes a **Status** filter button:

| Filter | Shows |
|--------|-------|
| **Active** | Only online, connected orchestrators |
| **Inactive** | Only offline or disconnected orchestrators |
| **Error** | Only orchestrators in an error state |

Click a status to apply the filter. Click the same status again to clear it and show all orchestrators.

---

## Quick Reference: Available Actions

| Action | Where | Description |
|--------|-------|-------------|
| **Add Orchestrator** | Orchestrators list page | Opens the 3-step setup wizard |
| **Search** | Orchestrators list page | Filter by orchestrator name |
| **Filter by Status** | Orchestrators list page | Show only a specific status |
| **Rename** | Three-dot menu on row | Change the display name |
| **Delete** | Three-dot menu on row | Delete the orchestrator |
| **Add Device** | Devices tab on detail page | Create a new vPLC device |
| **Restart Device** | Three-dot menu on device row | Restart a specific vPLC |
| **Rename Device** | Three-dot menu on device row | Change a device's name |
| **Delete Device** | Three-dot menu on device row | Permanently remove a vPLC |

---

## What's Next?

Learn about the devices your orchestrators run:

➡️ [Understanding vPLC Devices](../vplc-management/understanding-vplc) — What virtual PLCs are, what they can do, and when to use them.
