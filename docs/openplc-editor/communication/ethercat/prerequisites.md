# Prerequisites

EtherCAT is a wire-level real-time protocol. Unlike Modbus or OPC-UA, it does not run over TCP/IP and cannot share a network interface with general-purpose traffic. Before you can drive a segment from Autonomy Edge, the host running the runtime needs to be set up correctly. This page lists everything you should check before scanning a bus.

## Runtime and host

| Requirement | Details |
|-------------|---------|
| Runtime | Runtime v4 |
| Operating system | Linux (any modern distribution that supports raw Ethernet sockets) |
| Architecture | x86-64 or ARM64 (most edge boxes and industrial PCs) |
| Privileges | The runtime process needs permission to send raw Ethernet frames on the EtherCAT NIC |

EtherCAT is **not available** on Runtime v3 or on Arduino targets. If you need to run EtherCAT, your project must target a Runtime v4 host.

## A dedicated network interface

EtherCAT must own its NIC. The master continuously sends and receives Ethernet frames on the chosen interface, and any other traffic on that wire (DHCP requests, ARP, monitoring agents, container bridges) will create jitter and CRC errors that the master will report as working-counter mismatches.

In practice this means:

- Use a **second NIC** on the host, separate from the one you use for SSH, for the orchestrator connection, and for the rest of your enterprise network.
- Do not assign an IP address to the EtherCAT NIC. The master uses raw Ethernet, so an IP makes no difference, but it discourages other tools from sending traffic onto that link.
- Disable any NetworkManager or netplan configuration that brings the EtherCAT interface up automatically with DHCP.

The Bus Editor lists every interface the runtime can see in its **Network Interface** dropdown, so once the NIC is plugged in and recognised by the kernel it will appear there ready to be selected.

### Recommended NIC chipsets

EtherCAT relies on a low-latency raw-socket path through the kernel. Most server and industrial-grade NICs work fine; the typical pitfalls are USB-Ethernet dongles and consumer wireless-bridging cards. Known-good chipsets:

| Chipset | Notes |
|---------|-------|
| Intel i210, i211, i225, i350 | Excellent latency, well-supported in Linux. The default choice. |
| Realtek RTL8111 / RTL8125 | Works for development and small segments. May show occasional jitter on heavy hosts. |
| Beckhoff CCAT (built into IPCs) | Native support, optimal latency. |

USB-Ethernet adapters and Wi-Fi devices are **not supported**: they cannot deliver the timing EtherCAT requires.

## Operating-system permissions

To send raw Ethernet frames, the runtime process needs the `CAP_NET_RAW` Linux capability. There are two common ways to grant this:

1. **Run the runtime as root.** Simplest, but discouraged on production hosts.
2. **Grant the capability to the runtime binary or service unit.** Preferred on production hosts.

If you installed the runtime via a systemd unit, edit the unit (or use a drop-in override) so that the service starts with the capability:

```ini
[Service]
AmbientCapabilities=CAP_NET_RAW
CapabilityBoundingSet=CAP_NET_RAW
```

Reload systemd (`systemctl daemon-reload`) and restart the runtime. If you prefer not to touch the unit, you can also set the capability on the binary directly with `setcap cap_net_raw+ep <path-to-runtime>`, but this only works when the runtime is launched as a regular executable rather than from a container.

If the capability is missing, the EtherCAT plugin reports a clear error in the runtime log when the bus tries to start, and the Bus Editor's **Bus** tab shows an `EtherCAT Discovery Service Not Available` banner once the runtime is connected. See [Troubleshooting](troubleshooting) for the matching diagnostics.

## Physical layer and topology

EtherCAT uses ordinary Ethernet cabling and connectors but with strict topology requirements.

| Item | Requirement |
|------|-------------|
| Cable | CAT5e or better, shielded recommended |
| Connector | RJ45 |
| Maximum cable length per hop | 100 m (standard Ethernet) |
| Topology | Daisy-chain (line) or ring; star is allowed only via EtherCAT junctions |
| Switches | **Not allowed in the segment.** Managed switches break the protocol. |

The master's EtherCAT NIC connects to the IN port of the first slave. The OUT port of each slave connects to the IN port of the next. The last slave's OUT port is left open, or. For redundancy. Looped back to a second NIC on the master.

> **Do not put a managed switch between the master and the slaves.** EtherCAT relies on slaves processing frames on the wire as they pass through. A switch buffers and forwards full frames, which destroys the timing the protocol depends on. If you are seeing intermittent working-counter errors, look for a switch in the segment first.

## Cycle-time floor by segment size

The master cycle time is configured in the [Advanced](bus-advanced) tab of the Bus Editor (default 1000 µs). Use this table as a starting point and tune from there:

| Slave count | Recommended cycle time floor |
|-------------|------------------------------|
| Up to 8 slaves | 250 µs |
| 8 -- 32 slaves | 500 µs |
| 32 -- 64 slaves | 1000 µs (default) |
| 64 -- 128 slaves | 2000 µs |
| Over 128 slaves | 4000 µs or more |

These are conservative defaults. Beckhoff EL terminals on a clean segment can run faster; long cable runs, slower hosts, or distributed-clock motion control may need slower cycles. If the runtime reports cycle-time overruns, increase the cycle time before changing anything else. See [Troubleshooting](troubleshooting) for how to read those warnings.

## What's next?

Once your host meets these prerequisites and the EtherCAT NIC is plugged into the first slave, continue to **[Adding an EtherCAT segment](adding-ethercat)** to create the bus entry in your project.
