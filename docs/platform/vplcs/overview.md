# vPLC devices

A **vPLC** (virtual PLC) is a Docker container that runs the OpenPLC v4 runtime on your edge hardware. It's the thing that actually executes your project, the scan loop, the I/O, the communication protocols.

You can run multiple vPLCs on a single piece of hardware. Each one is isolated, gets its own IP address on the physical LAN (via MACVLAN), and behaves like a standalone PLC to the rest of the network.

## Why containers?

Three benefits:

1. **Density.** Modern industrial PCs and even Raspberry Pi 5s have plenty of CPU. Running one vPLC per machine wastes most of it. With vPLCs you can consolidate several PLC workloads onto one device.
2. **Isolation.** A bug or a runaway scan in one vPLC doesn't affect the others. They have separate filesystems, separate memory, separate processes.
3. **Reproducibility.** Each vPLC runs a pinned runtime image. You always know exactly which runtime version is in production.

## How a vPLC fits with the rest of the platform

- A vPLC is created **inside** an orchestrator. Without an orchestrator there's nowhere for a vPLC to run.
- A vPLC runs **one project at a time**. You deploy a project to it from the **[OpenPLC Editor](../../openplc-editor/overview)**.
- A vPLC has **runtime users**, which are separate from your platform account. When you first connect to a vPLC from the editor, you create the first runtime user. You'll use those credentials every time you connect to that vPLC afterwards.

## The vPLC lifecycle

| State | What it means |
|---|---|
| **Stopped** | The container exists but isn't running. No scan loop, no I/O. |
| **Running** | The container is running. A project may or may not be loaded; if not, the runtime is idle. |
| **Inactive** | The container is unreachable. Usually means the orchestrator itself is offline. |

Start / stop / restart actions are available from the vPLC card's **3-dot menu** in the orchestrator's Devices tab.

## What a vPLC sees on the network

Thanks to MACVLAN, each vPLC has:

- Its own MAC address (auto-generated or manually set).
- Its own IP address (DHCP-assigned or static).
- Full access to the same network the host is on.

This means your sensors, drives, HMIs, and remote I/O modules talk to the vPLC over Modbus TCP, EtherCAT, OPC-UA, or whatever protocol you choose, exactly as if they were talking to a hardware PLC.

See **[Network modes](network-modes)** for the details on DHCP vs static and how multiple NICs work.

## Plan limits

- **Community**: 2 vPLC devices total.
- Paid plans go much higher; see **[Plan limits](../../plans-and-billing/plan-limits)** for exact numbers.

When you hit the limit, attempting to create another vPLC shows the plan-limit modal:

![Plan limit reached, Device limit reached (2/2) on plan Community](images/vplc-plan-limit.png)

## Where to next

- **Create a vPLC** → **[Creating a vPLC](creating-a-vplc)**.
- **See a vPLC's details** → **[vPLC detail](vplc-detail)**.
- **DHCP vs static** → **[Network modes](network-modes)**.
- **Deploy a project to it** → **[Connecting from the editor](connecting-from-editor)** or follow the **[Quick Start](../../getting-started/quick-start)**.
