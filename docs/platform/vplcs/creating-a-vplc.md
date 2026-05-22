# Creating a vPLC

vPLCs are created inside an orchestrator. The flow is:

1. Open the orchestrator that should host the new vPLC.
2. Click **+ New Device**.
3. Walk through the Add Device wizard.

## Step 1. Open the orchestrator

From the **[Orchestrators list](../orchestrators/orchestrators-list)**, click the orchestrator card. You land on **[Orchestrator detail](../orchestrator-detail)** with the **Devices** tab active.

The Devices tab shows your existing vPLCs as cards, plus a dashed **+ New Device** tile at the end of the grid. Click that tile.

If you've already used your plan's device limit, you'll see the plan-limit modal instead:

![Device limit reached (2/2) on plan Community](images/vplc-plan-limit.png)

Delete one of the existing devices, or upgrade your plan via **[Pricing](../../plans-and-billing/pricing)**.

## Step 2. Name the device

The Add Device wizard opens with the first step:

- **Device name** *(required)*: e.g. *vPLC 02*, *MachineA-Main*, *Demo vPLC*. Must be unique within this orchestrator.

Click **Next**.

## Step 3. Choose a runtime version

- **Runtime version** *(required)*: the OpenPLC v4 runtime image that this vPLC will run. Pick the **latest** unless you have a specific reason to pin an older version. Pinning is useful when reproducing an exact production environment.

Each version corresponds to a specific build of the runtime container (`ghcr.io/autonomy-logic/openplc-runtime:<version>`). The agent pulls and caches images on first use.

Click **Next**.

## Step 4. Configure network interfaces

The wizard requires **at least one virtual NIC**. A NIC is what gives the vPLC its presence on your physical LAN.

For each NIC you configure:

| Field | What it does |
|---|---|
| **Name** | Logical name for the NIC inside the runtime. `veth0` is the default. |
| **Physical port** | Which host network interface to attach to. Pick from the list of interfaces the orchestrator has reported (e.g. `eth0`, `enp3s0`, `wlan0`). |
| **Network mode** | **DHCP** (default, auto-assigned from your router) or **Static**. |
| **IP address / subnet mask / gateway / DNS** | Required for Static. Empty for DHCP. |
| **MAC mode** | **Auto** (Docker generates one) or **Manual** (you type one in). |
| **MAC address** | Required if MAC mode is Manual. Useful when your DHCP server or asset tracker expects a fixed MAC. |

The default of "one DHCP NIC on the host's primary physical port with auto MAC" is what most users want for a quick test. Click **+ Add NIC** to add more if you need the vPLC to live on multiple networks (e.g. a control LAN plus a management LAN).

See **[Network modes](network-modes)** for more on the DHCP vs Static decision and the MACVLAN model.

## Step 5, (Optional) Serial ports

If the runtime needs access to host serial devices (USB-to-RS485 adapters, on-board UARTs, etc.), expand the **Serial ports** section and:

- Click **Detect serial devices** to scan the host.
- Tick the boxes for the devices to expose into the vPLC container.
- Pick a container path for each, e.g. `/dev/ttyUSB0`.

Serial ports passed through this way are visible to the OpenPLC runtime for Modbus RTU, custom protocols, etc.

## Step 6. Create

Click **Create** at the bottom of the wizard.

The platform sends the creation command to the agent, which:

1. Pulls the runtime image (if not cached).
2. Creates the container with the MACVLAN configuration.
3. Starts the container.

You should see the new device card appear in the Devices tab within a few seconds, with status **Running** once the runtime is alive.

## After creation

A freshly-created vPLC has no project loaded, the runtime status will be **EMPTY** when you connect from the editor. The next step is to **[connect to it from the editor](connecting-from-editor)** and deploy a project.

If the vPLC stays in **Stopped** or **Inactive** state, see **[vPLC stuck in Stopped](../../troubleshooting/vplc-stuck-stopped)**.

## Where to next

- **Connect a project to this vPLC** → **[Connecting from the editor](connecting-from-editor)**.
- **Inspect this vPLC's details** → **[vPLC detail](vplc-detail)**.
- **Understand DHCP vs static** → **[Network modes](network-modes)**.
