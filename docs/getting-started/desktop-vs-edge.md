# Desktop Editor vs. Autonomy Edge

Two products, two workflows. Choose the right one for your setup.

---

## Overview

Autonomy Logic offers two ways to program PLCs: the **Autonomy Edge** cloud platform and the **Desktop Editor** (standalone OpenPLC Editor). They share the same IEC 61131-3 programming languages, but they work very differently.

This page explains what each product does, how they differ, and which one fits your workflow.

---

## Autonomy Edge (Cloud Platform)

Autonomy Edge is a browser-based platform for programming, deploying, and managing PLC programs through the cloud.

- **Program in the browser** at [edge.autonomylogic.com](https://edge.autonomylogic.com). No installation required
- **Deploy to devices** through an Orchestrator that manages the Runtime automatically
- **Requires:** an internet connection and a Linux machine to run the Orchestrator
- **Collaborative:** share projects, browse the activity feed, and use the AI assistant
- **Best for:** teams, remote device management, and cloud-first workflows

With Autonomy Edge, you never install or configure a Runtime directly. The Orchestrator handles that for you.

---

## Desktop Editor (Standalone Application)

The Desktop Editor is a traditional, locally installed application for writing PLC programs and deploying them over your local network.

- **Install on Windows, macOS, or Linux**: runs entirely on your machine
- **Connect directly** to a Runtime on the same network
- **No cloud account needed**: everything stays local
- **You install and manage** the Runtime yourself
- **Single-user**, local workflow
- **Best for:** local development, education, and offline use

Download the Desktop Editor at [autonomylogic.com](https://autonomylogic.com).

---

## Side-by-Side Comparison

| | **Autonomy Edge** | **Desktop Editor** |
|---|---|---|
| **Interface** | Web browser | Installed application |
| **Runtime management** | Automatic (via Orchestrator) | Manual (you install and configure) |
| **Deployment** | Cloud → Orchestrator → Device | Direct network connection |
| **Internet required** | Yes | No |
| **Collaboration** | Projects, sharing, activity feed, AI assistant | Single-user |
| **Account needed** | Yes | No |
| **Best for** | Teams, remote management, cloud workflows | Local development, education, offline use |

---

## Which Should I Use?

- **Want to program from the browser and manage devices remotely?** → Use **Autonomy Edge**. Sign up at [edge.autonomylogic.com](https://edge.autonomylogic.com) and follow the [Quick Start Guide](./quick-start).

- **Want a local, standalone setup without a cloud account?** → Use the **Desktop Editor**. Download it from [autonomylogic.com](https://autonomylogic.com).

- **Not sure yet?** Both products use the same IEC 61131-3 programming languages and project format. Projects created in one can generally be opened in the other, so you can try both without losing work.

---

## Common Confusion

These are real questions we see from users. If you've hit one of these, you're not alone.

### "I installed the Runtime from GitHub but can't connect to Autonomy Edge"

The standalone Runtime (OpenPLC Runtime) is designed to work with the **Desktop Editor**, not with Autonomy Edge. If you want to use Autonomy Edge, install an **Orchestrator** instead. It manages the Runtime automatically.

➡️ See [Understanding Orchestrators](../platform-features/orchestrator-management/understanding-orchestrators) to get started.

### "The Runtime web interface shows a 404 or doesn't work"

The Runtime's built-in web interface is part of the **Desktop Editor** workflow. In Autonomy Edge, you don't need it. Everything is managed through the cloud platform at [edge.autonomylogic.com](https://edge.autonomylogic.com).

If you're using Autonomy Edge, ignore the Runtime web interface entirely and manage your devices from the platform dashboard.

---

## What's Next?

- **Using Autonomy Edge?** Continue to [Account Setup](./account-setup) to create your account.
- **Using the Desktop Editor?** See the [OpenPLC Editor Overview](../openplc-editor/overview) for installation and usage guides.
