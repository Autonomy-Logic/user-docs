# vPLC detail

The vPLC detail page is the read-only "I want to see what this device looks like right now" view. URL: `edge.autonomylogic.com/{slug}/devices/{deviceId}?orchestratorId={orchId}`.

![vPLC detail page for a Stopped device](images/vplc-detail.png)

## Header

- **Cube icon** and **vPLC name** at the top left.
- **Status badge** (Running / Stopped / Inactive).
- **Subtitle** with the NIC mode (DHCP / Static) and the container engine version (`Container <version>` or `Container unknown` if the agent hasn't reported it yet).

The breadcrumb at the very top — **Orchestrators → {orchestrator name} → {vplc name}** — lets you jump back one step at a time.

## Stats grid

A row of read-only metrics:

| Field | Description |
|---|---|
| **UPTIME** | How long the container has been running since its last start. |
| **RESTARTS** | How many times the container has restarted. Helpful for spotting crash loops. |
| **INTERNAL IP** | The IP the vPLC actually got on the LAN (DHCP-assigned address, or the static one if you set one). |
| **NETWORK MODE** | `DHCP` or `Static`. |
| **GATEWAY** | The gateway the vPLC is using. |
| **DNS** | DNS server. |
| **SUBNET MASK** | Subnet mask. |
| **CREATED** | The date this vPLC was created. |

Fields show `N/A` when the device hasn't reported back yet (e.g. status is Stopped or Inactive).

## Network Interfaces section

Below the stats, a panel labelled **Network Interfaces** lists every virtual NIC attached to this vPLC, with its name, physical port, network mode, IP, and MAC.

For a freshly-created or Stopped vPLC the list reads **No network interfaces found**.

When populated, each row shows the NIC's status (up/down) and its current address(es) — useful for verifying the runtime can actually reach the rest of the network.

## Where to find the actions

The detail page itself doesn't have action buttons. Lifecycle actions live in the **3-dot menu** on the device card in the orchestrator's Devices tab:

- **Start** — start a Stopped container.
- **Stop** — gracefully stop a Running container.
- **Restart** — stop + start in one click.
- **Edit** — open the Add Device wizard pre-populated with this device's settings (renames, NIC changes).
- **Delete** — permanently remove this vPLC from the orchestrator.

Stopping a vPLC does not delete it. Its config and any project deployed to it are preserved, ready to resume.

## Logs and runtime details

The detail page shows network and lifecycle information. For runtime logs (scan cycles, PLC errors, communication trace) you need to connect to the vPLC from the **[OpenPLC Editor](../../openplc-editor/overview)** — those logs live on the runtime itself, not in the platform's metric stream.

## When things look wrong

- **Status is Inactive but the orchestrator is Active** — check **[vPLC stuck in Stopped](../../troubleshooting/vplc-stuck-stopped)**.
- **Status is Running but Network Interfaces says "No network interfaces found"** — the runtime hasn't pushed an update yet. Refresh after 10 seconds. If still empty, restart the vPLC from the 3-dot menu.

## Where to next

- **Deploy a project to this vPLC** → **[Connecting from the editor](connecting-from-editor)**.
- **Change network settings** → 3-dot menu → **Edit**. See **[Network modes](network-modes)** for what the fields mean.
- **Inspect the parent orchestrator's metrics** → **[Orchestrator detail](../orchestrators/orchestrator-detail)**.
