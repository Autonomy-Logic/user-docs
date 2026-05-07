# Device Detail Page

When you click a device row in the orchestrator's Devices tab, you open the device detail page. This page gives you a complete view of your vPLC's current state, network configuration, and serial port status.

---

## Page Layout

A **breadcrumb** at the top shows your navigation path:

**Orchestrators** → **Orchestrator** → **Device Name** (with a status badge)

Click "Orchestrators" to go back to the list, or "Orchestrator" to return to the parent orchestrator's detail page.

The device name appears alongside a color-coded **status label**:

- **Active** (green) — The device is online and healthy.
- **Not Found** (red) — The device could not be reached (the orchestrator is likely offline).
- **Unknown** (gray) — Status could not be determined.

---

## Overview Tab

The Overview tab is the default view, divided into three sections: status cards, device information, and network/serial port details.

### Status Cards

Four cards at the top provide an at-a-glance summary:

| Card | What It Shows |
|------|---------------|
| **Status** | The device's current state (e.g., `running`, `exited`, `created`). |
| **Running** | Whether the device is actively executing — **Yes** or **No**. |
| **Restart Count** | How many times the device has been restarted since creation. A high count may indicate instability. |
| **Uptime** | How long the device has been running since its last start (e.g., `24h 30m`). Shows `N/A` if not running. |

These values are fetched live from the orchestrator every time you open the page.

### Device Information

Below the status cards, a **Device Information** card shows a two-column grid of details:

| Field | Description |
|-------|-------------|
| **Device Name** | The name you assigned. |
| **Network Mode** | How the first vNIC gets its IP — `dhcp` or `static`. |
| **Status** | Same as the status badge in the breadcrumb. |
| **Gateway** | The gateway configured on the first vNIC, or `N/A`. |
| **Running** | `Yes` or `No`. |
| **DNS** | The DNS server configured on the first vNIC, or `N/A`. |
| **Subnet Mask** | The subnet mask on the first vNIC, or `N/A`. |
| **Restart Count** | Same as the status card. |
| **Uptime** | Same as the status card. |
| **Created At** | The date the device was created. |

> **Tip:** The fields in Device Information show the **configured** values from when you created the device. The Network Interfaces section below shows **live** values reported at runtime — useful for confirming DHCP-assigned addresses.

### Network Interfaces

The **Network Interfaces** card shows the live network configuration for each interface on the device:

| Field | Description |
|-------|-------------|
| **Network** | The network name. |
| **IP Address** | The currently assigned IP address. For DHCP, this is what your DHCP server assigned. For static, this is the address you configured. |
| **MAC Address** | The MAC address of the virtual interface. |
| **Gateway** | The gateway address for this network. |

This section is useful for verifying that:

- DHCP assigned the expected IP address.
- Static IP configuration was applied correctly.
- The MAC address matches your network's expectations (e.g., for DHCP reservations).

If the orchestrator can't reach the device, you'll see "No network interfaces found."

### Serial Ports

The **Serial Ports** card only appears if you configured serial port passthrough. For each serial port:

| Field | Description |
|-------|-------------|
| **Port Name** | The friendly name you assigned (e.g., `serial0`). |
| **Status** | Connection state: **Connected** (green), **Disconnected** (gray), **Error** (red), or **Unknown** (gray). |
| **Device Path** | The path inside the vPLC (e.g., `/dev/ttyUSB0`) — this is what your PLC program references. |
| **Host Path** | The current path on the host machine. Shows `N/A` if the device is disconnected. |
| **Device ID** | The unique identifier of the physical serial device, used for automatic reconnection. |

> **Tip:** Check serial port status before running a PLC program that uses serial communication. A "Disconnected" status means the physical device has been unplugged or isn't detected.

---

## Network Configuration Tab

The **Network Configuration** tab is currently reserved for a future release. When enabled, it will let you edit your vPLC's network settings directly from this page without recreating the device.

---

## What's Next?

Learn how to manage your device's lifecycle:

➡️ [Managing Device Status](managing-status) — Status indicators, start/stop/restart operations, and troubleshooting tips.
