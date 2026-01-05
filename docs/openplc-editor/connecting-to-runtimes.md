# Connecting to Runtimes

OpenPLC Editor needs to connect to an OpenPLC Runtime to deploy and run your PLC programs. The connection method depends on whether you're using the desktop editor or the web editor (Autonomy Edge).

## Understanding the Connection Architecture

### Desktop Editor: Direct Connection

The desktop editor connects directly to OpenPLC Runtime instances over your local network. This provides low-latency communication and works without internet access.

```
┌─────────────────┐         LAN          ┌─────────────────┐
│  OpenPLC Editor │ ◄──────────────────► │ OpenPLC Runtime │
│    (Desktop)    │      Port 8443       │   (v3 or v4)    │
└─────────────────┘                      └─────────────────┘
```

### Web Editor: Connection via Orchestrator

The web editor (Autonomy Edge) connects to runtimes through orchestrator agents. This enables remote access to PLCs anywhere in the world through a secure, encrypted connection.

```
┌─────────────────┐       Internet       ┌─────────────────┐       LAN        ┌─────────────────┐
│  OpenPLC Editor │ ◄──────────────────► │  Orchestrator   │ ◄──────────────► │ OpenPLC Runtime │
│      (Web)      │        mTLS          │     Agent       │    Port 8443     │      (v4)       │
└─────────────────┘                      └─────────────────┘                  └─────────────────┘
```

## Desktop Editor: Connecting to Local Runtimes

### Prerequisites

Before connecting, ensure that:

1. OpenPLC Runtime is installed and running on your target device
2. The runtime is accessible on your local network
3. You know the IP address or hostname of the runtime
4. Port 8443 is not blocked by firewalls

### Adding a Runtime Connection

1. Open OpenPLC Editor
2. Navigate to the **Device** section in the project explorer
3. Click on **Configuration** to open the device settings
4. Enter the runtime connection details:
   - **Host**: The IP address or hostname of the runtime (e.g., `192.168.1.100` or `plc.local`)
   - **Port**: The runtime port (default: `8443`)
5. Click **Connect** to establish the connection

### First-Time Connection to Runtime v4

When connecting to a new OpenPLC Runtime v4 installation for the first time, you'll need to create the initial user account:

1. Connect to the runtime using the steps above
2. The editor will detect that no users exist and prompt you to create one
3. Enter a username and password for the runtime
4. Click **Create User** to complete the setup

This user account is stored on the runtime and will be required for all future connections.

### Connection Status

Once connected, the editor displays the connection status:

- **Connected**: Successfully connected to the runtime
- **Disconnected**: No active connection
- **Connecting**: Attempting to establish connection
- **Error**: Connection failed (check the console for details)

### Deploying Programs

With an active connection, you can deploy your program to the runtime:

1. Ensure your project compiles without errors
2. Click the **Compile and Download** button (down arrow icon) in the toolbar
3. The editor will compile your program and upload it to the runtime
4. Monitor the console for compilation and upload progress
5. Once uploaded, use the runtime controls to start the PLC program

## Web Editor: Connecting via Orchestrator

The web editor connects to runtimes through orchestrator agents, which are managed through the Autonomy Edge platform.

### Prerequisites

Before connecting, ensure that:

1. You have an orchestrator agent installed and linked to your Autonomy Edge account
2. A vPLC device has been created on the orchestrator
3. The vPLC is running and accessible

For information on setting up orchestrators and vPLCs, see:
- [Understanding Orchestrators](../platform-features/orchestrator-management/understanding-orchestrators.md)
- [Creating vPLC Devices](../platform-features/vplc-management/creating-vplc.md)

### Connecting to a vPLC

1. Open your project in the Autonomy Edge web editor
2. Navigate to the **Device** section in the project explorer
3. Click on **Orchestrators** to view available connections
4. Select the orchestrator and vPLC you want to connect to
5. Click **Connect** to establish the connection

### First-Time Connection to a vPLC

When connecting to a newly created vPLC for the first time:

1. The editor will detect that no users exist on the vPLC
2. You'll be prompted to create the initial user account
3. Enter a username and password
4. Click **Create User** to complete the setup

### Deploying Programs to vPLCs

1. Ensure your project compiles without errors
2. Click the **Compile and Download** button in the toolbar
3. The program will be compiled and uploaded through the orchestrator
4. Monitor the console for progress
5. Use the vPLC controls in the Device panel to start the program

## Runtime Compatibility

### Desktop Editor Compatibility

| Runtime Version | Supported | Notes |
|----------------|-----------|-------|
| Runtime v4 | Yes | Full support |
| Runtime v3 | Yes | Full support |
| Arduino/Microcontrollers | Yes | Direct USB upload |

### Web Editor Compatibility

| Runtime Version | Supported | Notes |
|----------------|-----------|-------|
| Runtime v4 | Yes | Via orchestrator only |
| Runtime v3 | No | Not supported |
| Arduino/Microcontrollers | No | Not supported |

## Connection Security

### Runtime v4 Security

OpenPLC Runtime v4 uses HTTPS with self-signed certificates for secure communication:

- All traffic is encrypted using TLS
- JWT (JSON Web Token) authentication protects API endpoints
- User credentials are stored securely on the runtime

### Orchestrator Security

Connections through orchestrator agents use mTLS (mutual TLS) encryption:

- RSA-4096 certificates for authentication
- End-to-end encryption between the web editor and runtime
- No direct internet exposure of the runtime required

## Troubleshooting

### Cannot Connect to Runtime

1. **Verify the runtime is running**: Check that the OpenPLC Runtime service is active on the target device
2. **Check network connectivity**: Ensure you can ping the runtime's IP address
3. **Verify the port**: Confirm port 8443 is open and not blocked by firewalls
4. **Check credentials**: Ensure you're using the correct username and password

### Connection Timeout

- The runtime may be overloaded or unresponsive
- Network latency may be too high
- Try restarting the runtime service

### Certificate Errors

Runtime v4 uses self-signed certificates, which may trigger browser warnings. This is expected behavior for local development. The connection is still encrypted and secure.

### Orchestrator Connection Issues

1. **Verify orchestrator status**: Check that the orchestrator is online in the Autonomy Edge dashboard
2. **Check vPLC status**: Ensure the vPLC container is running
3. **Review orchestrator logs**: Check for connection errors in the orchestrator management page

## Offline Operation

Once a program is deployed to a runtime, it continues running independently of the editor connection. This means:

- The PLC program runs even if the editor is closed
- Network disconnections don't stop the running program
- You can reconnect at any time to monitor or update the program

For more information about offline operation with orchestrators, see [Understanding Orchestrators](../platform-features/orchestrator-management/understanding-orchestrators.md#offline-operation-and-local-network-access).
