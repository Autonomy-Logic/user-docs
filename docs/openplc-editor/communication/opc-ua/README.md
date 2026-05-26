# OPC-UA Server

OPC-UA (Open Platform Communications Unified Architecture) is a modern, platform-independent communication protocol designed for secure and reliable data exchange in industrial automation. Unlike Modbus, OPC-UA includes built-in support for encryption, certificate-based authentication, role-based access control, and rich data modeling. Autonomy Edge provides a full OPC-UA server that lets you expose project variables to external clients such as SCADA systems, HMIs, MES platforms, historians, and cloud gateways.

The server supports bidirectional communication: external clients can both read variable values and, when their assigned role allows it, write new values back to the running PLC program.

## When to Use OPC-UA Instead of Modbus

Modbus is simple and ubiquitous, but it lacks security, structured data support, and fine-grained access control. Use OPC-UA when any of the following apply:

| Requirement | Recommended Protocol |
|-------------|---------------------|
| Encrypted, authenticated communication | OPC-UA |
| Role-based access (operators vs. engineers) | OPC-UA |
| Exposing structured data types or arrays | OPC-UA |
| Connecting to a modern enterprise system (MES, historian, cloud) | OPC-UA |
| Connecting to legacy PLCs, drives, or sensors | Modbus |
| Highest throughput on a trusted local network | Modbus |

In many deployments both protocols are used together, with Modbus on the field-device side and OPC-UA for higher-level integrations.

## Adding an OPC-UA Server to a Project

To add an OPC-UA server in the Autonomy Edge web editor:

1. In the project explorer, click the **+** button next to the project name.
2. Select **Server** from the element-type dialog.
3. Enter a **Server name** (at least 3 characters) and choose **OPC-UA** from the **Protocol** dropdown.
4. Click **Create**.
5. The new server appears under the **Servers** folder in the project tree, and its configuration tab opens automatically.

The configuration view is organized into five tabs:

- **[General Settings](general-settings)**: server identity, network binding, port, endpoint path, application URIs, cycle time, namespace.
- **[Security Profiles](security-profiles)**: accepted security policies, message security modes, and authentication methods.
- **[Users](users)**: password and certificate-based user accounts with role assignment.
- **[Certificates](certificates)**: server certificate strategy and trusted client certificates.
- **[Address Space](address-space)**: selection of PLC variables to expose and per-role access permissions.

## Default Configuration

When you create an OPC-UA server, Autonomy Edge applies the following defaults so the server is ready to configure:

| Setting | Default |
|---------|---------|
| Enable Server | Off |
| Port | `4840` |
| Cycle Time | `100` ms |
| Network Interface | `All Interfaces (0.0.0.0)` |
| Security profile | One profile named `insecure` (Policy `None`, Mode `None`, Authentication `Anonymous`) |
| Server certificate strategy | `Auto-generate Self-Signed` |
| Address space | Empty (no variables exposed) |

The default `insecure` profile is intended for first-time exploration only. Replace or supplement it with an encrypted profile and configure users before exposing the server on a shared network.

## Server Endpoint URL

Once the server is enabled and the project is deployed, OPC-UA clients connect using a URL built from the **Network Interface**, **Port**, and **Endpoint Path** settings on the General Settings tab:

```
opc.tcp://<host>:<port><endpoint_path>
```

For example, with the editor defaults and an Endpoint Path of `/openplc/opcua` on a host with IP `192.168.1.50`:

```
opc.tcp://192.168.1.50:4840/openplc/opcua
```

## Platform Support

OPC-UA is available on Runtime v4 only.

| Runtime | OPC-UA Server Support |
|---------|----------------------|
| Runtime v4 | Yes |
| Runtime v3 | No |
| Arduino | No |

Runtime v3 and Arduino targets do not include the OPC-UA plugin. If your project requires OPC-UA, deploy to a Runtime v4 vPLC.

## Sub-Pages

- **[General Settings](general-settings)**: server name, network interface, port, endpoint path, application identity, cycle time.
- **[Security Profiles](security-profiles)**: security policies, message security modes, authentication methods, recommended profiles.
- **[Users](users)**: user accounts, password rules, role assignment, certificate-bound users.
- **[Certificates](certificates)**: self-signed vs. custom server certificates, trusted client certificate management.
- **[Address Space](address-space)**: variable selection, namespace, IEC 61131-3 to OPC-UA type mapping, per-role permissions.
- **[Worked Example](example)**: end-to-end walkthrough exposing variables from the blink program with one secure profile, an operator user, and a self-signed certificate.
- **[Troubleshooting](troubleshooting)**: common errors shown in the editor or by connecting clients, and the fix for each.

## What's Next?

- **[General Settings](general-settings)**: start here once the server is created.
- **[Worked Example](example)**: follow the end-to-end walkthrough.
- **[Communication Protocols Overview](../README)**: return to the protocols overview and Modbus documentation.
