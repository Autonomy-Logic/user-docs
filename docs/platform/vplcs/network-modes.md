# Network modes

Every vPLC has at least one virtual NIC. Two things about that NIC determine how the vPLC participates in your network: the **network mode** (DHCP or Static) and the **MAC mode** (auto or manual).

## MACVLAN, in one paragraph

Behind the scenes, every NIC you configure uses Docker's **MACVLAN** driver. MACVLAN gives the vPLC container its own MAC and IP address on the physical network, *not* an internal Docker bridge IP that gets NAT'd. From the perspective of every other device on your LAN, a vPLC is just another piece of hardware with its own MAC. Switches, routers, DHCP servers, and Modbus slaves all treat it the same as they would a standalone PLC.

This is the difference that matters: regular `docker run` containers hide behind their host. vPLCs do not.

## DHCP mode

In DHCP mode the vPLC gets its IP address from your network's DHCP server (usually the router).

**Pros**

- Zero configuration. You don't need to coordinate IPs.
- Easy to spin up disposable test vPLCs.

**Cons**

- The IP can change at any time. A device that expects to find the vPLC at `192.168.1.50` may suddenly find nothing there if the lease renews to a different address.
- Hard to script firewalls and ACLs that depend on a fixed IP.

**When to use**: development, demos, anything where the vPLC is a *client* of other devices (it polls them, not vice versa).

## Static mode

In Static mode you provide the IP, subnet mask, gateway, and DNS. The vPLC uses exactly those.

**Required fields**

| Field | Notes |
|---|---|
| **IP address** | The static IP. Must be in the subnet of the physical port the NIC is attached to, and must not collide with other devices. Reserve the IP on your DHCP server to be safe. |
| **Subnet mask** | Usually `255.255.255.0` (`/24`). |
| **Gateway** | Your network's default gateway. |
| **DNS** | A DNS server reachable from the LAN. `8.8.8.8` works if you don't have a local one. |

**Pros**

- Predictable IP for firewall rules, OPC-UA endpoint URLs, Modbus master configurations.
- Required for production deployments where remote I/O modules and HMIs are statically configured against a specific PLC address.

**Cons**

- One more thing to keep in sync. If you change the LAN subnet, you'll need to update every static vPLC.

**When to use**: production, anything that other devices need to reach by IP.

## MAC mode: Auto vs Manual

The MAC address is independent of the IP. By default, MACVLAN auto-generates one for each NIC. You can override this and supply a specific MAC.

**When to use Manual MAC**

- Your DHCP server reserves leases by MAC. Pinning the MAC means the DHCP server always hands out the same IP. (This is a common pattern for "static IP via DHCP reservation" without using true static.)
- Your asset tracking system or network monitoring tool keys off MAC.
- You're replacing a piece of hardware and want the vPLC to inherit its MAC so the rest of the network doesn't need reconfiguring.

**Format**: standard `aa:bb:cc:dd:ee:ff` notation. The first byte should be locally administered (`x2`, `x6`, `xa`, or `xe`) to avoid collisions with hardware vendors' MAC ranges.

## Multiple NICs

You can attach more than one NIC to a single vPLC. The wizard has a **+ Add NIC** action that lets you add as many as the host has interfaces for.

Common reasons:

- **Control LAN + management LAN.** One NIC on the field network for talking to sensors/drives, another on the office network for cloud and HMI access.
- **Redundant interfaces.** Two NICs on the same network with different IPs for failover.
- **Cross-subnet routing.** The vPLC bridges Modbus on one VLAN to OPC-UA on another.

Each NIC is configured independently: its own physical port, its own network mode, its own MAC mode.

## Dynamic network adaptation

The agent watches the host's network configuration. If the host moves to a new network (different subnet, different DHCP lease), the agent re-runs MACVLAN setup for each vPLC automatically. DHCP NICs get new IPs and Static NICs keep their addresses. You don't need to bounce containers manually.

For deeper details on the network monitor sidecar, see the orchestrator agent's own repo. For end users, "it just works when the network changes" is the take-away.

## Changing network mode on an existing vPLC

The 3-dot menu on a vPLC card has **Edit**, which reopens the Add Device wizard pre-populated with the current settings. Change the network mode, IP, or MAC and click **Save**. The agent reconfigures the container in place. Brief downtime (a few seconds) is expected while the container restarts with new networking.

## Troubleshooting

- **vPLC starts but Internal IP shows `N/A`**: DHCP server not reachable from the chosen physical port, or no DHCP server on that subnet.
- **Static IP collisions**: two devices answering for the same IP cause connectivity to flap. Use `ping -c 3 <ip>` from another host while the vPLC is **Stopped** to verify the IP is free.
- **MAC duplicates**: if you set a manual MAC that collides with another device, the switch will get confused. Stick to locally administered MAC prefixes.

## Where to next

- **Create a vPLC with a specific network config** → **[Creating a vPLC](creating-a-vplc)**.
- **Verify the assigned IP and gateway** → **[vPLC detail](vplc-detail)**.
- **Talk to the vPLC over Modbus, OPC-UA, etc.** → **[OpenPLC Editor: Communication](../../openplc-editor/connecting-to-runtimes)**.
