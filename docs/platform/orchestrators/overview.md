# Orchestrators

An **orchestrator** is the cloud-side representation of a small piece of software (the *orchestrator agent*) that you run on your edge hardware. The agent's job is to manage **vPLC containers** on that hardware. The cloud talks to the agent over a secure connection, and the agent does the real work of starting, stopping, and monitoring vPLCs locally.

You need at least one orchestrator before you can deploy a project. The agent runs on Linux only, typically a PLC, PAC, industrial PC, dedicated server, or a Raspberry Pi.

## Why an agent on the edge?

Three reasons:

1. **Real-time runtime.** PLCs need to execute their scan loop with predictable timing. Running the runtime container directly on the edge device (rather than in the cloud) keeps latency to the I/O hardware low.
2. **Network resilience.** Once the project is deployed, the vPLC keeps running even if the agent's connection to the cloud is interrupted. The cloud connection is only needed for management, not for control.
3. **Native networking.** The agent sets up MACVLAN networking, which makes each vPLC container appear on your physical LAN with its own IP address, the same way a standalone PLC would. Sensors, drives, and HMIs see vPLCs as just another device on the wire.

## What you get when you "create" an orchestrator

Creating an orchestrator in the web app:

1. Reserves a unique orchestrator entity in the cloud with the name and ID you give it.
2. Generates an installation command.
3. Waits for the agent to call home from your edge device and complete the pairing.

After pairing, the orchestrator's status moves from **Inactive** to **Active** (or **Connected**) and you can start adding vPLC devices to it.

## What the agent itself does

Once paired and running, the agent:

- Maintains a persistent mutual-TLS (mTLS) WebSocket to the cloud.
- Sends periodic heartbeats with CPU, memory, disk, and uptime metrics: the values you see on the orchestrator card.
- Pulls and runs OpenPLC v4 runtime container images on demand.
- Configures MACVLAN networking for each vPLC according to its NIC settings.
- Reacts to host network changes (LAN reconnect, IP changes) and reconfigures containers as needed.
- Reports vPLC status (running, stopped, restarted) back to the cloud.

If you want to dig deeper, the agent's own documentation lives in its [GitHub repository](https://github.com/Autonomy-Logic/orchestrator-agent). Users don't normally need to read it, installation is one command and management is done from the web app.

## Where to next

- **Install the agent on a device** → **[Installing the agent](installing-the-agent)**.
- **See your orchestrators in the web app** → **[Orchestrators list](orchestrators-list)**.
- **Inspect a single orchestrator** → **[Orchestrator detail](orchestrator-detail)**.
- **Rename, delete, or replace an orchestrator** → **[Managing orchestrators](managing-orchestrators)**.
- **Add a vPLC to an orchestrator** → **[Creating a vPLC](../vplcs/creating-a-vplc)**.
