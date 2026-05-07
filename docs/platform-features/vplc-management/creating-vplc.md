# Creating a vPLC Device

This guide walks you through creating a new vPLC device on an orchestrator. By the end, you'll have a running virtual PLC ready to receive programs from the IDE.

---

## Before You Begin

You need:

- An orchestrator linked to your Autonomy Edge account and showing **Active** status. See [Adding Orchestrators](../orchestrator-management/adding-orchestrators) if you haven't set one up yet.

---

## Opening the New Device Modal

There are two ways to start:

- **From the orchestrator's Devices tab** — Navigate to **Orchestrators**, click your orchestrator, switch to the **Devices** tab, and click **Add Device**. If this is your first device, you'll see a prominent **Add Device** button in the center.
- **From the orchestrators list** — Expand an orchestrator row to see its devices, then click **Add Device**.

Both paths open the same **Add New Device** modal.

---

## Basic Settings

### Device Name

Enter a descriptive name for your vPLC — for example, `Palletizer Machine`, `Lab Controller 1`, or `Demo vPLC`. The name must be unique within the orchestrator.

### Runtime Version

Select which version of the OpenPLC Runtime to run. The dropdown lists all available versions (v4.0.6 and later).

- The **latest stable release** is pre-selected by default.
- Pre-release versions are marked with a **(Pre-release)** label.
- The most recent stable version shows a **- Latest** suffix.

> **Tip:** If you're unsure, keep the default. You can always create a new device with a different version later.

---

## Network Configuration

Every vPLC needs at least one virtual network interface (vNIC) to communicate on the network. The **Network** tab lets you configure one or more vNICs.

### Default Setup

When the modal opens, a default vNIC named `veth0` is already created and linked to the first physical interface detected on the host. For most setups, you only need to decide between DHCP and static IP.

### Adding and Removing NICs

- Click **Add** to create additional vNICs (useful if your vPLC needs to be on multiple network segments).
- Click the **trash icon** on a NIC to remove it. You must always have at least one.
- Click a NIC in the list to select it and configure its settings.

### NIC Settings

#### Virtual Interface Name

The name of the virtual interface (e.g., `veth0`, `veth1`). You can rename it to something meaningful.

#### Link to Physical Port

Select which physical network interface on the host this vNIC should use. The dropdown lists all physical interfaces detected on the host (e.g., `eth0`, `enp3s0`, `wlan0`) along with their current IP addresses.

Each physical port can only be used by one vNIC per device.

#### IP Address — DHCP or Static

Choose how the vNIC gets its IP address:

**DHCP (Automatic)** — Your network's DHCP server assigns an IP address automatically. This is the simplest option and works for most setups. No additional configuration needed.

**Static IP** — You manually specify the network settings. Four additional fields appear:

- **IP Address** — The fixed IP for this vNIC (e.g., `192.168.1.100`). Required.
- **Subnet Mask** — The network subnet mask (e.g., `255.255.255.0`). Required.
- **Gateway** — The default gateway for outbound traffic (e.g., `192.168.1.1`). Optional but recommended.
- **DNS Server** — The DNS server address (e.g., `8.8.8.8`). Optional.

> **Tip:** Use **DHCP** if you're getting started or prototyping. Use **Static IP** when your vPLC needs a fixed address — for example, when other devices on the network need to connect to it at a known IP.

All IP fields are validated in real time — invalid formats are flagged immediately.

#### MAC Address — Auto or Manual

**Automatic** (default) — A random MAC address is generated. Works for most cases.

**Manual** — You specify a MAC address in `XX:XX:XX:XX:XX:XX` format. Use this when your network requires specific MACs (e.g., for MAC-based firewall rules, DHCP reservations, or license-locked devices).

---

## Serial Port Configuration (Optional)

The **Serial Ports** tab lets you pass through USB-to-serial adapters and other serial devices from the host machine into the vPLC. Skip this tab if your vPLC only uses network communication.

### Available Devices

The left panel shows three groups:

- **Configured** — Serial devices already added to this vPLC.
- **Available Devices** — Serial devices detected on the host that are not in use. Click a device or its **+** button to add it.
- **In Use by Other Devices** — Serial devices assigned to other vPLCs on this orchestrator. These are grayed out (a serial device can only be assigned to one vPLC at a time).

Click the **refresh** button (↻) to re-scan the host for newly connected devices.

### Serial Port Settings

When you select a configured serial port:

- **Port Name** — A friendly name (e.g., `serial0`, `rs485-sensor`). You can change this.
- **Device ID** — The unique identifier of the physical serial device. Read-only. Used for automatic reconnection if the device is unplugged and reconnected.
- **Device Path** — The path your PLC program will use to access the serial port (e.g., `/dev/ttyUSB0`). You can customize it.

---

## Creating the Device

Once you've configured the name, runtime version, network, and (optionally) serial ports, click **Create**.

The modal shows a loading spinner with "Creating device... Please wait a moment." This typically takes a few seconds as the platform provisions your vPLC on the orchestrator's machine.

When complete, the modal shows a green checkmark and **"Device created successfully!"** Your new device appears in the orchestrator's Devices tab.

If creation fails (e.g., the orchestrator is offline), an error message is shown and the device record is automatically cleaned up.

---

## After Creation

Your vPLC is now running and ready to use. From here you can:

- **View device details** — Click the device row to open the [device detail page](device-detail) with full information, network interfaces, and serial port status.
- **Upload a program** — Open a project in the IDE, connect to the vPLC through the Device Orchestrators panel, and upload your PLC program.
- **Manage the device** — Use the three-dot menu (⋮) to restart, rename, or delete the device.

---

## What's Next?

Explore the device detail page to see your vPLC's full configuration and real-time status:

➡️ [Device Detail Page](device-detail) — Overview tab, network interfaces, serial port status, and all the information available for each device.
