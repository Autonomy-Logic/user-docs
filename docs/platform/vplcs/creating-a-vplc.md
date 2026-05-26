# Creating a vPLC

vPLCs are created inside an orchestrator. The flow is:

1. Open the orchestrator that should host the new vPLC.
2. Click **+ New Device**.
3. Walk through the three-step Add Device wizard.

## Step 1, Open the wizard

From the **[Orchestrators list](../orchestrators/orchestrators-list)**, click the orchestrator card. You land on **[Orchestrator detail](../orchestrators/orchestrator-detail)** with the **Devices** tab active.

The Devices tab shows your existing vPLCs as cards, plus a dashed **+ New Device** tile at the end of the grid. Click that tile.

If you've already used your plan's device limit, you'll see the plan-limit modal instead:

![Device limit reached (2/2) on plan Community](images/vplc-plan-limit.png)

Delete one of the existing devices, or upgrade your plan via **[Pricing](../../plans-and-billing/pricing)**.

## Step 2, Details

The wizard opens on a dedicated page (`/{slug}/devices/create?orchestratorId={oid}`). A 3-step indicator at the top shows the flow: **1. Details**, **2. Network**, **3. Serial Ports**.

![New Device wizard, Details step: Device Name and Runtime Version](images/new-device-step1.png)

| Field | Required | Notes |
|---|---|---|
| **Device Name** | Yes | A label for this vPLC. Must be unique within the orchestrator. Examples: *Palletizer Machine*, *Conveyor Controller*, *vPLC 02*. |
| **Runtime Version** | Yes | The OpenPLC v4 runtime image that this vPLC will run. Pick the version marked **Latest** unless you have a specific reason to pin an older version. |

The runtime dropdown lists every available version, with the latest stable one labeled and pre-releases flagged as such:

![Runtime version dropdown showing v4.0.9 (Latest) and pre-release builds](images/new-device-runtime-dropdown.png)

Each version corresponds to a specific build of the runtime container (`ghcr.io/autonomy-logic/openplc-runtime:<version>`). The agent pulls and caches images on first use.

Click **Next**.

## Step 3, Network

The wizard requires **at least one virtual NIC**. A NIC is what gives the vPLC its presence on your physical LAN.

![Network step: a single default NIC (veth0) already configured](images/new-device-step2-network.png)

A default NIC named `veth0` is added for you, configured for DHCP on the host's first interface with an auto-generated MAC. Click the NIC row to expand and edit it, click **+ Add Virtual NIC** to add more, or click the trash icon to remove one.

When you expand a NIC, you can configure:

| Field | What it does |
|---|---|
| **Name** | Logical name for the NIC inside the runtime. `veth0` is the default. |
| **Physical port** | Which host network interface to attach to (e.g. `eth0`, `enp3s0`, `wlan0`). |
| **Network mode** | **DHCP** (default, auto-assigned from your router) or **Static**. |
| **IP address / subnet mask / gateway / DNS** | Required for Static, empty for DHCP. |
| **MAC mode** | **Auto** (Docker generates one) or **Manual** (you type one in). |
| **MAC address** | Required if MAC mode is Manual. Useful when your DHCP server or asset tracker expects a fixed MAC. |

See **[Network modes](network-modes)** for the deeper picture on DHCP vs Static, multiple NICs, and the MACVLAN model.

Click **Next**.

## Step 4, Serial Ports (optional)

![Serial Ports step: detect button and "No serial devices detected" empty state](images/new-device-step3-serial.png)

If the runtime needs access to host serial devices (USB-to-RS485 adapters, on-board UARTs, etc.), the platform lets you pass them through to the vPLC container.

- **Refresh** in the top-right re-scans the host for available serial devices.
- Each detected device shows its host path (e.g. `/dev/ttyUSB0`) and a checkbox to expose it.

On staging (or any host without serial hardware), this step shows: *No serial devices detected on the host machine.* That's fine, leave it empty and continue.

Click **Create Device** at the bottom right.

## What happens on Create

The platform sends the creation command to the agent, which:

1. Pulls the runtime image (if not cached).
2. Creates the container with the MACVLAN configuration.
3. Starts the container.

You should see the new device card appear in the Devices tab within a few seconds, with status **Running** once the runtime is alive.

## After creation

A freshly-created vPLC has no project loaded. The runtime status will be **EMPTY** when you connect from the editor. The next step is to **[connect to it from the editor](connecting-from-editor)** and deploy a project.

If the vPLC stays in **Stopped** or **Inactive** state, see **[vPLC stuck in Stopped](../../troubleshooting/vplc-stuck-stopped)**.

## Where to next

- **Connect a project to this vPLC** → **[Connecting from the editor](connecting-from-editor)**.
- **Inspect this vPLC's details** → **[vPLC detail](vplc-detail)**.
- **Understand DHCP vs static** → **[Network modes](network-modes)**.
