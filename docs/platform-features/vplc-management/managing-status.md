# Managing Device Status

Once you have vPLC devices running on your orchestrators, you can monitor their status, view runtime statistics, and manage their lifecycle from the Autonomy Edge platform.

## Viewing Device Status

### From the Orchestrator Page

Navigate to your orchestrator and click on the **Devices** tab to see all vPLC devices. Each device card shows:

- **Device Name**: The name you assigned when creating the device
- **Status**: Current running state (running, stopped, creating, error)
- **Network Configuration**: IP address assignment method (DHCP or Static)

![Devices list with vPLC](images/devices-list-with-vplc.png)

### From the OpenPLC Editor

When connected to a vPLC through the OpenPLC Editor, you can see detailed runtime information in the Device Orchestrators panel:

- **Connection Status**: Shows "Connected" when actively connected to the vPLC
- **PLC Status**: Current program state (EMPTY, RUNNING, STOPPED)
- **Scan Cycle Statistics**: Real-time performance metrics

![Program running](images/program-running.png)

## Understanding PLC Status

The PLC Status indicator shows the current state of the OpenPLC Runtime:

**EMPTY**: No program is loaded on the vPLC. The runtime is running but waiting for a program to be uploaded.

**RUNNING**: A program is loaded and actively executing. The scan cycle is running and processing your PLC logic.

**STOPPED**: A program is loaded but not executing. This can happen when you manually stop the program or when an error occurs.

**COMPILING**: The runtime is compiling a newly uploaded program. This state is temporary and will change to RUNNING once compilation completes.

## Scan Cycle Statistics

When a program is running, the OpenPLC Editor displays real-time scan cycle statistics:

**Scan Count**: The total number of scan cycles completed since the program started. This counter continuously increments as the PLC executes your program.

**Overruns**: The number of times the scan cycle exceeded the configured cycle time. Ideally, this should be 0. Frequent overruns indicate that your program logic is too complex for the configured cycle time, or the host machine is under heavy load.

**Scan Time (avg)**: The average time in microseconds to execute your program logic. This measures only the time spent running your PLC code, not the full cycle time.

**Cycle Time (avg)**: The average total cycle time in microseconds, including program execution and I/O processing. This should be close to your configured cycle time (default is 20ms or 20000us).

**Cycle Latency (avg)**: The average timing accuracy of the cycle. A value close to 0 indicates the cycle is running on schedule. Positive values mean cycles are starting late; negative values mean they're starting early.

## Managing vPLC Lifecycle

### Starting and Stopping Programs

You can control program execution from the OpenPLC Editor:

- **Start**: Click the Play button to start a stopped program
- **Stop**: Click the Stop button to halt a running program

When you stop a program, all outputs are set to their safe state (typically 0 or OFF) and the scan cycle stops executing.

### Uploading New Programs

To update the program running on a vPLC:

1. Make your changes in the OpenPLC Editor
2. Ensure you're connected to the target vPLC
3. Click the Download button to compile and upload

The new program will replace the existing one. The runtime automatically stops the old program, compiles the new one, and starts execution.

### Disconnecting from a vPLC

Click the **Disconnect** button in the Device Orchestrators panel to close the connection to a vPLC. This does not stop the program running on the vPLC; it only closes the editor's connection.

The vPLC continues running independently after you disconnect. You can reconnect at any time to monitor status or upload new programs.

## Monitoring Best Practices

**Regular Status Checks**: Periodically review your vPLC devices to ensure they're running as expected. Check for any devices showing error states or unexpected status changes.

**Watch for Overruns**: If you see overruns increasing, investigate the cause. Common reasons include:
- Program logic that's too complex for the cycle time
- Host machine CPU under heavy load
- Network communication delays in Modbus or other protocols

**Monitor Scan Times**: Compare your average scan time to the cycle time. If scan time approaches or exceeds cycle time, consider:
- Optimizing your program logic
- Increasing the cycle time
- Moving workloads to a more powerful host machine

**Check Connection Status**: If you can't connect to a vPLC, verify:
- The orchestrator is online and active
- The vPLC container is running
- Network connectivity between the platform and orchestrator

## Troubleshooting

**vPLC shows "stopped" unexpectedly**: Check the PLC Logs tab in the Console panel for error messages. Common causes include runtime errors in your program or resource constraints on the host machine.

**Cannot connect to vPLC**: Ensure the orchestrator is online and the vPLC container is running. Try refreshing the Device Orchestrators list.

**High overrun count**: Your program may be too complex for the configured cycle time. Try increasing the cycle time in the Resource configuration, or optimize your program logic.

**Scan time varies significantly**: This can indicate inconsistent host machine performance. Check for other processes consuming CPU resources on the orchestrator's host machine.

## Next Steps

- Learn more about [Understanding vPLC Devices](understanding-vplc)
- Create additional vPLCs by following the [Creating vPLC Devices](creating-vplc) guide
- Explore the [Orchestrator Management](../orchestrator-management/orchestrator-overview) features for monitoring your edge devices
