# Adding Orchestrators

## Quick Start: Install an Orchestrator in 5 Minutes

This guide will walk you through installing an Orchestrator. The software that connects your Linux machine to the Autonomy Edge cloud platform. No prior experience is required.

> **⚠️ Linux Required:** The Orchestrator runs ONLY on Linux. If your machine runs Windows or macOS, you cannot install the Orchestrator on it. You need a Linux machine (physical or virtual).

### What You'll Need

1. A **Linux machine**: any computer running Linux (Raspberry Pi, industrial PC, laptop, virtual machine, etc.)
2. An **internet connection** on that machine
3. An **Autonomy Edge account**: you should already be logged in to the platform in your browser

### Step-by-Step Installation

**Step 1: Open a terminal on your Linux machine**

On your Linux machine, open a terminal application. This is where you'll run the install command.

**Step 2: Run the install command**

Copy and paste this command into the terminal and press Enter:

```bash
curl https://getedge.me | bash
```

This is the **only command you need to run**. It downloads and installs the Orchestrator automatically. Wait for the installation to complete (usually 1–3 minutes).

**Step 3: Copy the Orchestrator ID**

When the installation finishes, the terminal will display a unique **Orchestrator ID**: it looks like `abc1-d2e3-f456`.

> **⚠️ IMPORTANT: The Orchestrator ID expires in 5 minutes!** You must copy it and paste it into the platform within 5 minutes, or you'll need to run the install command again.

Copy this ID immediately.

**Step 4: Link the Orchestrator in Autonomy Edge**

Go back to your web browser where Autonomy Edge is open:

1. Navigate to **Orchestrators** in the sidebar menu.
2. Click **Add Orchestrator**.
3. Enter a name for your Orchestrator (e.g., "Lab Raspberry Pi" or "Factory Floor PC").
4. Click **Next** until you reach the **Link** step.
5. Paste the Orchestrator ID you copied from the terminal.
6. Click **Create Orchestrator**.

Your Orchestrator should now appear in the list with an **Active** status. You're done!

### Common Problems

| Problem | Solution |
|---------|----------|
| Installation fails | Make sure your machine is running **Linux** (not Windows/macOS), has an **internet connection**, and you have **sudo access**. |
| Orchestrator ID expired | The ID is only valid for **5 minutes**. Run `curl https://getedge.me \| bash` again to get a new ID. |
| Orchestrator not appearing after linking | Double-check that you copied the ID correctly (no extra spaces). Verify the Linux machine still has internet access. |
| Cannot find the Orchestrators page | In the Autonomy Edge sidebar, look for **Orchestrators**. You can also click **Manage orchestrator** on the Dashboard. |

---

## Detailed Walkthrough

The sections below provide a more detailed explanation of each step in the Orchestrator setup process.

---

This guide walks you through registering a new orchestrator on Autonomy Edge. The platform uses a 3-step wizard. **Details → Install → Link**: to get your orchestrator online.

> **Important:** The only installation command is `curl https://getedge.me | bash`. If you see any other URL mentioned elsewhere, it is incorrect.

---

## Before You Begin

> **Note:** The Orchestrator runs on **Linux only**: it does not support Windows or macOS. If you don't have a Linux machine, you can use a Raspberry Pi, a virtual machine running Ubuntu, or a cloud VM.

Make sure you have:

- A **Linux machine** (physical or virtual) where you'll install the agent. Ubuntu, Debian, Fedora, RHEL/CentOS, Raspberry Pi OS, and other major distributions are supported.
- **Root or sudo access** on that machine.
- An **internet connection** on both the Linux machine and the browser where you're using Autonomy Edge.

---

## Opening the Wizard

You can start the New Orchestrator wizard in two ways:

- **From the Dashboard**: Click **Manage orchestrator** at the bottom of the Orchestrators card in the sidebar, then click **Add Orchestrator** (or the floating `+` button).
- **From the Orchestrators page**: Navigate to Orchestrators in the sidebar and click **Add Orchestrator**.

If you have no orchestrators yet, the page shows an empty state with a prominent **Add Orchestrator** button in the center.

---

## Step 1: Details

Enter basic information about your orchestrator.

- **Orchestrator name** (required): A human-friendly name to identify this machine. Choose something descriptive, like `Lab Raspberry Pi`, `Production Line 3`, or `Dev VM - Ubuntu`.
- **Description** (optional): A short note about purpose, location, or setup. Example: `Located in Building A, Room 102`.

Click **Next** to proceed.

---

## Step 2: Install

Now you'll install the orchestrator agent on your Linux machine.

The modal displays a single command:

```bash
curl https://getedge.me | bash
```

1. Click the **Copy** button to copy the command.
2. Open a terminal on your Linux machine.
3. Paste and run the command.
4. Wait for the installation to complete (usually 1–3 minutes).

When the installation finishes, you'll see output like this:

```
INSTALLATION COMPLETE
=====================================================

Orchestrator ID: abc1-d2e3-f456
Expires in: 300 seconds (at 2026-03-14T03:20:00Z)

Copy the Orchestrator ID above and paste it into the
Autonomy Edge app to link your device.
=====================================================
```

**Copy the Orchestrator ID** from the terminal. You'll need it in the next step.

> **Tip:** The install script automatically handles dependencies, setup, and secure credential generation. You don't need to configure anything manually.

Click **Next** in the modal to proceed.

---

## Step 3: Link

The final step connects the installed agent to your Autonomy Edge account.

1. Paste the **Orchestrator ID** into the **ID Orchestrator** field.
2. Click **Create Orchestrator**.
3. Wait for the success notification: **"Orchestrator created successfully!"**

The modal closes automatically. After a few seconds, your orchestrator should appear on the Orchestrators page with an **Active** status.

### ID Expiration

The Orchestrator ID is valid for **5 minutes** from the moment it's generated. If the ID expires before you complete this step:

- You'll see an error: **"Invalid or expired orchestrator ID"**.
- Re-run `curl https://getedge.me | bash` on the Linux machine to get a new ID. The script detects the existing installation and refreshes it.

> **Tip:** The ID format is `xxxx-xxxx-xxxx` (three groups of four characters separated by hyphens). Make sure you copy it exactly.

> **Note:** After linking your Orchestrator, the next step is to create a Device. Head to [Creating vPLC Devices](../vplc-management/creating-vplc) to set up your first virtual PLC.

---

## After Linking

Once your orchestrator is linked and online, you can:

- **View it in the orchestrators list**: See name, CPU usage, memory, uptime, and status at a glance.
- **Open its detail page**: Click the orchestrator to see real-time metrics and charts.
- **Add vPLC devices**: Create virtual PLCs on this orchestrator to run your programs.

### Troubleshooting

| Problem | Solution |
|---------|----------|
| Orchestrator doesn't appear online after linking | Make sure the agent is running on the Linux machine and the machine has internet access. |
| "Invalid or expired orchestrator ID" error | The ID expires after 5 minutes. Re-run the install command to get a new one. |
| Installation fails | Ensure you have root/sudo access and a working internet connection. Check that your Linux distribution is supported. |

---

## What's Next?

Learn how to monitor and manage your orchestrator:

➡️ [Orchestrator Overview and Controls](orchestrator-overview): Explore the detail page, system metrics, resource charts, devices tab, and management actions.
