# Understanding Orchestrators

An orchestrator connects your Linux machine to the Autonomy Edge cloud platform. This page explains what orchestrators are, why you need one, and what they can do.

---

## What Is an Orchestrator?

An orchestrator is a lightweight software agent that you install on a Linux machine. A Raspberry Pi, an industrial PC, a cloud VM, or any Linux system. Once installed and linked to your Autonomy Edge account, it acts as the bridge between the cloud platform and your local hardware.

Think of it as a "local representative" of the platform on your edge machine. It receives commands from the cloud, runs them locally, and reports back with status and metrics.

---

## Why Do You Need One?

Autonomy Edge is a cloud platform. You access the IDE, create projects, and manage devices from your browser. But PLC programs need to run close to the physical process they control: on the factory floor, in a lab, or on-site.

Orchestrators solve this by giving you the best of both worlds:

- **Cloud convenience**: Manage everything from a web browser, from anywhere.
- **Edge execution**: Programs run locally with low latency, directly on your hardware.
- **Centralized monitoring**: See CPU, memory, disk, and network across all your edge machines in one place.

Without an orchestrator, the platform has no way to deploy programs or send commands to machines in your network.

---

## What Can an Orchestrator Do?

Each orchestrator can manage multiple virtual PLC devices (vPLCs) on its host machine. Here's what it handles for you:

- **Create, start, stop, restart, and delete vPLC devices**: all from the web interface, no SSH required.
- **Report system health**: CPU usage, memory, disk, uptime, and status are sent to the cloud automatically.
- **Monitor devices**: Per-device CPU and memory usage are tracked and displayed on the platform.
- **Detect network interfaces**: The orchestrator knows which physical network interfaces are available, so you can assign them to your vPLC devices.

---

## One Orchestrator, Many Devices

A single orchestrator can run multiple vPLC devices on the same machine. Each vPLC is independent. With its own IP address, program, and configuration. You manage them all from the Autonomy Edge web interface.

When you delete an orchestrator, all of its vPLC devices are also removed.

---

## What's Next?

Ready to set one up?

➡️ [Adding Orchestrators](adding-orchestrators): Walk through the 3-step wizard to install and link an orchestrator to your account.
