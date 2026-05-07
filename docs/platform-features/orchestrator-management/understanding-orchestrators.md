# Understanding Orchestrators

## New to Autonomy Edge? Start Here

If this is your first time using Autonomy Edge, here's the big picture:

**Autonomy Edge** is a cloud platform you access from your web browser. It lets you manage programmable logic controllers (PLCs). The small computers that control industrial machines, sensors, and automation systems.

But there's a challenge: the cloud platform runs on the internet, while your physical devices (PLCs, sensors, machines) are on a local network in your factory, lab, or office. Something needs to connect the two.

**That something is the Orchestrator.**

### What Is an Orchestrator in Plain Language?

The Orchestrator is a small piece of software that you install on a **Linux machine**: any computer running Linux. This could be a Raspberry Pi, an industrial PC, a laptop, or a virtual machine. It doesn't matter, as long as it runs Linux.

Once installed, the Orchestrator acts as a **bridge** between:

- **The Autonomy Edge cloud platform** (where you manage everything from your browser)
- **Your physical devices** (PLCs, boards, and sensors connected to that Linux machine)

You control everything from the web. The Orchestrator handles the rest locally.

> **In short:** You install the Orchestrator on a Linux machine. It connects that machine to the cloud. Then you manage your devices from the Autonomy Edge web interface. No need to SSH into the machine or edit config files.

---

## Prerequisites

Before setting up an Orchestrator, make sure you have:

> **⚠️ Linux Required:** The Orchestrator runs ONLY on Linux. It does not work on Windows or macOS. If you don't have a Linux machine, you'll need to set one up first (a Raspberry Pi, a virtual machine, or any computer running a Linux distribution).

- A **Linux machine** (Ubuntu, Debian, Fedora, Raspberry Pi OS, or other major distributions)
- An **internet connection** on that Linux machine
- An **Autonomy Edge account** (sign up at the Autonomy Edge website if you don't have one)

---

## How It All Fits Together

Here's the flow from start to finish:

1. **You sign up** for Autonomy Edge and log in from your browser.
2. **You install the Orchestrator** on your Linux machine with a single terminal command.
3. **You link the Orchestrator** to your account by pasting an ID into the platform.
4. **You create Devices** (virtual PLCs) on that Orchestrator. Entirely from the web interface.
5. **You deploy programs** to those Devices and monitor everything from the cloud.

The Orchestrator handles all the communication between the cloud and your local machine. You never need to manually configure networking, install runtimes, or manage files on the Linux machine.

---

## Detailed Technical Overview

The following sections go deeper into how Orchestrators work and what they can do.

---

An orchestrator connects your Linux machine to the Autonomy Edge cloud platform. This page explains what orchestrators are, why you need one, and what they can do.

---

## How Autonomy Edge Works

Autonomy Edge is a cloud platform. You do everything from your browser. Here's the complete flow from zero to a running PLC program:

1. **Write code in the browser**: Use the cloud IDE to create your PLC program (Structured Text, Ladder Diagram, or any supported language).
2. **Install an Orchestrator on a Linux machine**: This is your bridge between the cloud platform and the physical world. One command installs it: `curl https://getedge.me | bash`
3. **Create a Device through the web interface**: The Orchestrator sets up the virtual PLC automatically on your Linux machine. No manual configuration needed.
4. **Deploy with one click**: Send your program from the browser straight to the Device. It starts running immediately.

That's it. The Orchestrator handles everything behind the scenes. Installing the Runtime, managing Devices, and keeping the cloud in sync.

> **Important:** The Orchestrator requires a **Linux machine** (Raspberry Pi, Ubuntu, Debian, Fedora, etc.). It does not run on Windows or macOS.

---

## What Is an Orchestrator?

Think of the Orchestrator as an extension of Autonomy Edge installed on your machine. It's how the cloud platform reaches your local hardware.

An orchestrator is a lightweight software agent that you install on a Linux machine. A Raspberry Pi, an industrial PC, a cloud VM, or any Linux system. Once installed and linked to your Autonomy Edge account, it acts as the bridge between the cloud platform and your local hardware.

It receives commands from the cloud, runs them locally, and reports back with status and metrics.

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

## Common Questions

**Do I need to install or configure the Runtime?**
No. The Orchestrator manages the Runtime automatically. You never need to install, update, or configure it yourself.

**Can I install the Orchestrator on Windows or Mac?**
No. The Orchestrator requires Linux. If you don't have a Linux machine, you can use a Raspberry Pi, a virtual machine running Ubuntu, or a cloud VM.

**What's the difference between Autonomy Edge and the Desktop Editor?**
They are two separate products. **Autonomy Edge** is the cloud platform. You program in the browser and deploy to devices through an Orchestrator. The **Desktop Editor** is a standalone local application with its own built-in Runtime. They do not share projects or devices.

---

## What's Next?

Ready to set one up?

➡️ [Adding Orchestrators](adding-orchestrators): Walk through the 3-step wizard to install and link an orchestrator to your account.
