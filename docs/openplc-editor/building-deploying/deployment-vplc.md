# Deploying to Devices

This page covers how to deploy your compiled PLC program to a device, verify it's running, and troubleshoot common deployment issues.

## How Deployment Works

When you click **Compile** while connected to a device, the IDE automatically:

1. Compiles your project (validates code, checks for errors).
2. Packages the compiled program.
3. Uploads it to the connected device.
4. Monitors the device until it confirms the program is ready.

You don't need a separate "deploy" step. Compilation and deployment happen together when a device is connected.

> **Tip:** If you compile without a connected device, the IDE still validates your code. It just skips the upload. You can connect and recompile later when you're ready to deploy.

## Prerequisites

Before deploying, make sure you have:

- A project that compiles successfully. See [Project Compilation](project-compilation).
- An online orchestrator with at least one active device. See [Understanding Orchestrators](../../platform/orchestrators/overview).
- An active connection to the target device. See [Connecting to Runtimes](../connecting-to-runtimes).

## Selecting a Device

1. In the **Project Explorer** on the left, expand the **Device** folder.
2. Click **Orchestrators** inside the Device folder to open the Orchestrators page.
3. You'll see the **OpenPLC Simulator** at the top (selected by default) and your registered Orchestrators listed below.
4. Click on an Orchestrator to expand it and see its Devices.
5. Click on a Device to select it. Only active (online) devices can be selected.
6. Click **Connect**.

### First-Time Connection (Creating Credentials)

The first time you connect to a Device that has no users configured, the IDE opens a **Create User** dialog. Enter a username and password. These are the **runtime credentials** for this specific Device, separate from your Autonomy Edge account login.

> **Important:** Remember these credentials. You'll need them every time you reconnect to this Device.

### Reconnecting (Login)

If the Device already has credentials configured, the IDE opens a **Login** dialog instead. Enter the username and password you created during the first connection.

### Switching Devices

If you're already connected to a Device and click on a different one, the IDE shows a confirmation dialog asking if you want to switch. Confirming disconnects from the current Device and starts the connection flow with the new one.

> **Tip:** Click the **Refresh** button (↻) to reload the Orchestrator and Device list if you don't see a recently added device.

## Deploying Your Program

Once you're connected to a Device (the Orchestrators page shows your connection status):

1. Click the **Compile** button in the Activity Bar (left side of the screen).
2. Watch the Console Panel at the bottom. It shows progress for each compilation step.
3. Wait for `Compilation completed successfully`.

The IDE compiles your project, packages it, and uploads it to the Device through the Orchestrator. All in one step. Your program is now on the Device and ready to run.

## Starting and Stopping the PLC

### Starting

1. After a successful deployment, click the **Start/Stop PLC** button in the Activity Bar (the play icon).
2. The device begins executing your program according to the configured task schedule.
3. The button icon changes to a stop icon while the program is running.

### Stopping

1. Click the **Start/Stop PLC** button again (now showing the stop icon).
2. The device halts program execution.

Stopping doesn't delete the program. You can start it again without recompiling.

### PLC States

Your program can be in one of these states:

- **Empty**: No program has been uploaded yet.
- **Stopped**: A program is loaded but not executing.
- **Running**: The program is actively executing.
- **Error**: The device encountered an error during execution. Check the PLC Logs tab for details.

## Checking After Deployment

### Verify in the Console

A successful deployment ends with:

```
[INFO]  Compilation completed successfully (exit code: 0).
```

If you see `[ERROR]` messages instead, check the [Troubleshooting](#troubleshooting) section below.

### Monitor with PLC Logs

Once the program is running, switch to the **PLC Logs** tab in the Console Panel. This shows live output from the running PLC program. Separate from the compilation logs in the Console tab.

### Check Execution Statistics

When connected to a running PLC, the Orchestrators panel displays real-time stats:

- **Scan Count**: Total scan cycles executed since start.
- **Overruns**: Times a scan cycle exceeded the configured cycle time.
- **Scan Time** (avg/min/max): Duration of the PLC logic execution per cycle.
- **Cycle Time** (avg/min/max): Total cycle duration including I/O processing.

## Redeploying

To deploy an updated version of your program:

1. Make your code changes in the IDE.
2. Click **Compile** again.
3. The new program replaces the previous one on the device.
4. If the PLC was running, it's stopped automatically before the update.
5. Click **Start PLC** to run the updated program.

You don't need to disconnect and reconnect between deployments.

## Disconnecting

To disconnect from a device, click the **Logout** button in the Orchestrators panel.

**Important:** Disconnecting does not stop the PLC program. The device operates independently. Once a program is started, it keeps running even if you close your browser. To stop it, click the Stop button before disconnecting, or reconnect later.

## Troubleshooting

### Can't see any orchestrators

- Verify your orchestrator is registered and online. Check the platform dashboard.
- Click Refresh in the Orchestrators panel.

### Device shows as stopped or offline

- The device may not be running. Go to the platform dashboard and start it.
- Wait 30–60 seconds after starting. The device needs time to initialize.

### Login fails

- Use your **runtime credentials** (created during first connection), not your Autonomy Edge platform login.
- If you've forgotten the runtime credentials, you may need to recreate the device from the platform dashboard.

### Compilation succeeds but upload fails

- Check that the device is still connected (Orchestrators panel).
- The orchestrator may have gone offline during compilation. Refresh and reconnect.
- Check the Console for specific error messages.

### PLC doesn't start after deployment

- Check the Console for error messages during the final compilation step.
- Check the PLC Logs tab for runtime errors.
- Make sure the device connection is still active.

### Timeout during deployment

- The IDE waits up to 5 minutes for the device to finish processing. If it times out, the device may be under heavy load.
- Verify the device is still running in the platform dashboard.
- Reconnect and try again.

---

## What's Next?

- [Project Compilation](project-compilation): Learn how to read and fix compilation errors.
- [XML Export](xml-export): Export your project for backup or sharing.
- [Connecting to Runtimes](../connecting-to-runtimes): Full reference for the connection flow and authentication.
- [Console & Debugging](../workspace-overview/console-debugging): Learn how to read and filter build logs effectively.
