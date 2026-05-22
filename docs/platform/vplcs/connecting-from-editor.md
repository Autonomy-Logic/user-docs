# Connecting from the editor

Once you have a project and a vPLC, you connect them through the **[OpenPLC Editor](../../openplc-editor/overview)**. The editor's left sidebar has a **Devices → Orchestrators** panel; that's the only place the cloud platform and the runtime meet.

## Steps

1. **Open the project in the editor.** From the project page click **Open in editor**. The editor loads with your project.
2. **Open the Devices panel.** In the editor's left sidebar expand **Devices**, then click **Orchestrators**. A panel slides out listing every orchestrator your account has access to.
3. **Expand the orchestrator that owns your vPLC.** Each orchestrator entry shows its connection status (Active / Inactive). Expand it to reveal its vPLCs.
4. **Select the target vPLC.** Click on the device row. It should report status **Running** (or you'll need to start it via the device's 3-dot menu from the platform).
5. **Click Connect** at the top of the panel.

## First-time runtime user

The first time anyone connects to a freshly-created vPLC, the runtime prompts for a new user account. **This account lives on the vPLC, not on the cloud** — it's how you authenticate to the runtime itself.

Pick:

- **Username** — `admin` is conventional.
- **Password** — at least 8 characters.
- **Confirm password** — matches the above.

Click **Create User**. The runtime stores the credentials and signs you in.

On subsequent connections from any browser, the runtime shows a regular sign-in dialog. Enter the runtime username and password. There's no "forgot password" flow on the runtime side; if you lose it you'll need to delete and recreate the vPLC.

> **Don't reuse your Autonomy Edge password here.** The runtime user is local to the vPLC. Pick a password manager entry just for runtime users.

## After connecting

When connected, the editor's bottom-right status bar shows:

- **Connected** — green.
- **PLC Status**: `EMPTY` (no program loaded), `STOPPED`, or `RUNNING`.

You can now use the editor's **Download** button (folder with a down arrow, top-left) to compile and upload your project. If compilation succeeds, the program is sent to the runtime and PLC Status moves to `RUNNING`. The **Scan Cycle Statistics** panel becomes useful at this point — it shows live scan counts, average scan time, and overruns.

## Reconnecting after a refresh

Browser refresh disconnects the editor from the runtime. Just click **Connect** again — the editor remembers which vPLC you were on.

## What happens if the orchestrator goes offline

If the orchestrator-agent loses its cloud connection while you're connected to a vPLC:

- The vPLC keeps running locally with whatever program is loaded.
- The editor can't issue new commands (Download, Stop, Start) until the orchestrator reconnects.
- I/O traffic to physical devices is unaffected.

When the orchestrator returns to **Active**, your editor connection resumes automatically.

## Where to next

- **Walkthrough of a full first deploy** → **[Quick Start](../../getting-started/quick-start)**.
- **Editor reference** → **[OpenPLC Editor overview](../../openplc-editor/overview)**.
- **Troubleshooting connectivity** → **[Orchestrator not connecting](../../troubleshooting/orchestrator-not-connecting)**.
