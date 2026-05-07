# Adding Orchestrators

This guide walks you through registering a new orchestrator on Autonomy Edge. The platform uses a 3-step wizard. **Details → Install → Link**: to get your orchestrator online.

---

## Before You Begin

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
