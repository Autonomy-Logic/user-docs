# General Settings

The **General Settings** tab is where you configure the server's network identity, performance, and identification URIs. It is the first tab shown after you create an OPC-UA server entry, and it is divided into four labelled sections: **Server Configuration**, **Application Identity**, **Timing Configuration**, and **Namespace Configuration**.

![OPC-UA Server General Settings tab showing all four sections: Server Configuration (Enable, Name, Network Interface, Port 4840, Endpoint Path /openplc/opcua), Application Identity (Application URI urn:openplc:opcua:server, Product URI urn:openplc:runtime), Timing Configuration (Cycle Time 100 ms), Namespace Configuration (Namespace URI urn:openplc:opcua:namespace)](images/opcua-general-settings.png)

All fields commit on blur. Type a value and click outside the field (or press Tab) to save it.

## Server Configuration

This section controls whether the server runs and where it listens.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| **Enable Server** | Toggle | Off | Switches the OPC-UA plugin on or off at runtime. The helper text reads `Server is disabled` when off and `Server will start when PLC runs` when on. Leave off until the rest of the configuration is complete. |
| **Server Name** | Text | `OpenPLC OPC UA Server` (placeholder) | Human-readable name advertised to clients during discovery. Pick something operators will recognise (for example, `Plant Floor PLC`). |
| **Network Interface** | Dropdown | `All Interfaces (0.0.0.0)` | Selects the IP address the server binds to. Choose **Localhost (127.0.0.1)** to restrict access to the host running the runtime, or **All Interfaces (0.0.0.0)** to accept connections on every network the device is connected to. |
| **Port** | Number | `4840` | TCP port for incoming OPC-UA connections. Range: `1`–`65535`. The OPC-UA standard reserves `4840`. The label includes the inline hint `Default: 4840`. |
| **Endpoint Path** | Text | `/openplc/opcua` (placeholder) | Path appended to the endpoint URL. Some clients require an explicit path; an empty value is also accepted. |

The full endpoint URL clients use to connect is:

```
opc.tcp://<host>:<port><endpoint_path>
```

For example, with the placeholder endpoint path on a device reachable at `192.168.1.50`:

```
opc.tcp://192.168.1.50:4840/openplc/opcua
```

## Application Identity

These two URIs identify the server to clients. The defaults are placeholders the editor inserts when you create the server. You can keep them as-is for development, or replace them with values that match your organisation's URN scheme.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| **Application URI** | Text | `urn:openplc:opcua:server` (placeholder) | Globally unique URI for this server instance. If you use custom certificates, the certificate's Subject Alternative Name must match this value. |
| **Product URI** | Text | `urn:openplc:runtime` (placeholder) | URI identifying the product family. Usually shared across all OPC-UA servers in the same fleet. |

The on-screen helper text reads: *"Configure the OPC-UA application identity URIs. These are used by clients to identify the server."*

## Timing Configuration

This section sets how often the OPC-UA server refreshes the values it publishes from the running PLC program.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| **Cycle Time (ms)** | Number | `100` | Update frequency in milliseconds. Range: `10`–`10000`. The inline hint reads `Update frequency for OPC-UA variables (10-10000ms)`. |

Lower values give clients fresher data at the cost of more CPU on the runtime. The default of 100 ms is a balanced starting point. If your client only needs slow trending (one update per second), increase the cycle time to reduce load.

## Namespace Configuration

The OPC-UA address space is partitioned into namespaces. All variables you expose live inside the namespace identified by the URI shown here.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| **Namespace URI** | Text (read-only on this tab) | `urn:openplc:opcua:namespace` | URI for the namespace that holds your exposed variables. The same field is editable on the [Address Space](address-space) tab. |

The on-screen helper text reads: *"The namespace URI for OpenPLC variables in the OPC-UA address space."*

## What's Next?

- **[Security Profiles](security-profiles)**: set the encryption and authentication options clients are allowed to use.
- **[Users](users)**: add user accounts that can authenticate against the server.
- **[Address Space](address-space)**: choose which PLC variables to expose.
