# Deploying to a vPLC

Deployment is the upload half of **Build & Upload**. Once your project compiles cleanly, the editor ships the binary to a connected vPLC over the runtime's HTTP transport. No separate deploy command.

## Prerequisites

- A project that compiles. See **[Building a project](project-compilation)**.
- An **online orchestrator** with at least one **running vPLC** on it. See **[Orchestrators](../../platform/orchestrators/overview)** in the platform docs.
- A **connected session** with that vPLC. See **[Connecting to a vPLC](../connecting-to-runtimes)**.

## The deployment flow

1. **Build options** → **Build & Upload** (or **Clean Upload** for a from-scratch build).
2. The editor runs the build pipeline. The console reports each step.
3. On a successful compile, the editor POSTs the binary to the runtime's webserver.
4. The runtime persists the new program, computes its MD5, and reports readiness.
5. The editor logs `Upload completed`.

At this point the new program is loaded but **not yet running**. To start it, click the activity-bar **Play** button. The runtime swaps to the uploaded program and reports `PLC running`.

To swap to a different program later, repeat **Build & Upload** + **Play**. The runtime hot-swaps without a restart.

## Stopping the PLC

The **Play** button is also a **Stop** button. Click it once while the PLC is running and the runtime halts the program. The vPLC stays connected; only the IEC program is stopped.

## Verifying the deployment

Three quick checks that the new program is what's actually running:

1. **MD5 verification**: open the **Debugger**. It immediately compares the local MD5 against the runtime's. A mismatch tells you something is off (older build is still running).
2. **PLC Logs**: open the console's **PLC Logs** tab. New program output starts appearing once you press Play.
3. **Live variable values**: opt some variables into the Debug column and watch them in the debugger.

## Troubleshooting

**Upload fails with a transport error.** The connection dropped between compile and upload. Verify the orchestrator is still online and reconnect.

**MD5 mismatch in the debugger.** The runtime is still running an older program. Re-run **Build & Upload** to ship the current build.

**`Play` button is grey.** You're not connected, or the upload failed. Check the console for the specific error.

**PLC starts then immediately stops.** A runtime fault. Open **PLC Logs**, the runtime usually publishes the cause (out-of-range memory access, missing library binding, etc.).

**Program runs but Modbus / OPC-UA / S7Comm clients can't connect.** The server is configured but disabled. Open the server's editor and toggle **Enabled** on, then rebuild and re-upload.

## What's next

- **[Debugger](debugger)**: live variable monitoring on the deployed program.
- **[Console & PLC Logs](../workspace-overview/console-debugging)**: reading the runtime's log stream.
- **[Building a project](project-compilation)**: the compile step before upload.
