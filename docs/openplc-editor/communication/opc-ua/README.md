# OPC-UA Server

> **Coming Soon:** OPC-UA support is currently in development. The documentation below is a preview of the upcoming feature and may change before release.

OPC-UA (Open Platform Communications Unified Architecture) is a modern, platform-independent communication protocol designed for secure and reliable data exchange in industrial automation. Unlike Modbus, OPC-UA includes built-in support for encryption, authentication, role-based access control, and rich data modeling. Autonomy Edge provides a full OPC-UA server implementation that lets you expose any project variable to external clients such as SCADA systems, MES platforms, historians, and cloud gateways.

The OPC-UA server runs as a runtime plugin. It supports bidirectional synchronization between the PLC runtime and OPC-UA address space, meaning external clients can both read variable values and write to them.

## Adding an OPC-UA Server

To add an OPC-UA server to your project in the Autonomy Edge web editor:

1. In the project explorer, click the **+** button.
2. Select **Server** from the dropdown menu.
3. Choose **OPC-UA** as the protocol and enter a descriptive name.
4. Click **Create**.
5. The new server entry appears under the **Servers** folder in the project tree.
6. Click the server entry to open its configuration panel.

The configuration panel is organized into five tabs: **General**, **Security Profiles**, **Users**, **Certificates**, and **Address Space**.

## Platform Support

| Runtime | OPC-UA Server Support |
|---------|----------------------|
| Runtime v4 | Yes |
| Runtime v3 | No |
| Arduino | No |

OPC-UA is only available on Runtime v4 running on Linux-based targets. It is not supported on Runtime v3 or Arduino boards.

## General Settings

The General tab configures the server's network identity and performance parameters.

| Setting | Description | Default |
|---------|-------------|---------|
| **Enabled** | Toggle to enable or disable the OPC-UA server at runtime | Enabled |
| **Server Name** | Human-readable name that appears in OPC-UA discovery | `Autonomy Edge OPC-UA Server` |
| **Bind Address** | Network interface IP to listen on. Use `0.0.0.0` for all interfaces. | `0.0.0.0` |
| **Port** | TCP port for OPC-UA connections | `4840` |
| **Endpoint Path** | URL path appended to the server address (e.g., `/opcua`) | -- |
| **Application URI** | Unique URI identifying this server application | Auto-generated |
| **Product URI** | URI identifying the product type | Auto-generated |
| **Cycle Time (ms)** | How frequently the server synchronizes variable values with the PLC runtime | -- |

The full server endpoint URL follows this pattern:

```
opc.tcp://<bind_address>:<port><endpoint_path>
```

For example, with the default settings and endpoint path `/opcua`:

```
opc.tcp://0.0.0.0:4840/opcua
```

## Security Profiles

The Security Profiles tab lets you define which combinations of security policy and message security mode the server accepts. Each profile determines the encryption and signing algorithms used for the connection.

### Security Policies

| Policy | Description |
|--------|-------------|
| **None** | No encryption or signing. Suitable only for isolated, trusted networks. |
| **Basic256Sha256** | AES-256 encryption with SHA-256 signing. Recommended for most deployments. |
| **Aes128_Sha256_RsaOaep** | AES-128 encryption with SHA-256 signing and RSA-OAEP key exchange. |
| **Aes256_Sha256_RsaPss** | AES-256 encryption with SHA-256 signing and RSA-PSS signatures. Strongest option. |

### Message Security Modes

| Mode | Description |
|------|-------------|
| **None** | No security applied to messages. Only valid with the `None` security policy. |
| **Sign** | Messages are digitally signed to ensure integrity but not encrypted. |
| **SignAndEncrypt** | Messages are both signed and encrypted. Recommended for production. |

### Configuring a Security Profile

You can add multiple security profiles to support different client capabilities. Each profile is a combination of one security policy and one message security mode.

**Example profiles for a production deployment**:

| Profile | Policy | Mode | Use Case |
|---------|--------|------|----------|
| 1 | Basic256Sha256 | SignAndEncrypt | Primary secure connection |
| 2 | Aes256_Sha256_RsaPss | SignAndEncrypt | Highest security clients |

**Example for a development environment**:

| Profile | Policy | Mode | Use Case |
|---------|--------|------|----------|
| 1 | None | None | Quick testing without certificates |
| 2 | Basic256Sha256 | Sign | Testing with signed messages |

> **Security recommendation**: Avoid using the `None/None` profile in production environments. Always require at least message signing for any network-accessible deployment.

### Authentication Methods

Each security profile also specifies which authentication methods are accepted:

| Method | Description |
|--------|-------------|
| **Anonymous** | No credentials required. Client connects without identifying itself. |
| **Username/Password** | Client provides a username and password (verified against the Users tab). |
| **Certificate** | Client authenticates using an X.509 certificate (must be in the trusted certificates list). |

You can enable multiple authentication methods per profile.

## Users

The Users tab defines the user accounts that can authenticate with the OPC-UA server. Each user has credentials and an assigned role that controls what they can do.

### User Properties

| Property | Description |
|----------|-------------|
| **Username** | Login name for the user account |
| **Password** | Password for the account. Stored using bcrypt hashing — never in plaintext. |
| **Authentication Type** | `Username/Password` or `Certificate` |
| **Role** | The access role assigned to this user |

### Roles

Autonomy Edge defines three built-in roles with increasing levels of access:

| Role | Description | Typical Use |
|------|-------------|-------------|
| **Viewer** | Read-only access to variables configured with viewer permissions | Dashboards, reporting systems, historians |
| **Operator** | Read/write access to variables configured with operator permissions | HMI panels, operator workstations |
| **Engineer** | Full read/write access to all exposed variables | Engineering workstations, commissioning tools |

Role permissions are enforced per-variable in the Address Space configuration (see below).

### Certificate-Based Users

For certificate-based authentication, instead of a username and password, you associate a user with a specific X.509 client certificate. The certificate must also be added to the trusted certificates list in the Certificates tab.

## Certificates

The Certificates tab manages the X.509 certificates used for server identity and client authentication.

### Server Certificate

The OPC-UA server requires its own certificate for secure communications. You have two options:

| Option | Description |
|--------|-------------|
| **Auto-generated self-signed** | The server automatically generates a self-signed certificate on first startup. Suitable for development and internal deployments. |
| **Custom certificate** | Upload your own certificate and private key, signed by a trusted Certificate Authority (CA). Recommended for production. |

For auto-generated certificates, the server creates an RSA key pair and self-signed X.509 certificate using the Server Name and Application URI from the General tab.

### Trusted Client Certificates

When using certificate-based authentication, you must add each client's certificate to the trusted list. Only clients presenting a trusted certificate will be allowed to connect (when the certificate authentication method is enabled in the security profile).

To add a trusted client certificate:

1. Obtain the client's X.509 certificate file (`.der` or `.pem` format).
2. In the Certificates tab, add it to the trusted certificates list.
3. Associate the certificate with a user account in the Users tab.

### Certificate Validation

The server validates client certificates against its trusted list. Certificates that are expired, revoked, or not in the trusted list are rejected. Self-signed client certificates are accepted only if they are explicitly added to the trusted list.

## Address Space

The Address Space tab is where you select which project variables to expose through OPC-UA and configure their node IDs, data types, and per-role access permissions. This is the most important tab for defining what data external clients can see and interact with.

### Selecting Variables

The Address Space configuration shows all variables defined in your project. You can select which variables to expose by adding them to the OPC-UA address space. Supported variable types include:

- Simple variables (BOOL, INT, DINT, REAL, LREAL, etc.)
- Structured variables (user-defined data types)
- Arrays

### Node Configuration

For each exposed variable, you configure:

| Property | Description |
|----------|-------------|
| **Node ID** | Unique identifier for this variable in the OPC-UA address space. Can be numeric or string-based. |
| **Browse Name** | Human-readable name displayed when clients browse the server's address space. |
| **Description** | Optional text description of the variable's purpose. |

### Variable Type Mapping

Autonomy Edge automatically maps IEC 61131-3 data types to OPC-UA data types:

| IEC 61131-3 Type | OPC-UA Type | Size |
|-------------------|-------------|------|
| `BOOL` | Boolean | 1 bit |
| `SINT` | SByte | 8 bits |
| `USINT` | Byte | 8 bits |
| `INT` | Int16 | 16 bits |
| `UINT` | UInt16 | 16 bits |
| `DINT` | Int32 | 32 bits |
| `UDINT` | UInt32 | 32 bits |
| `LINT` | Int64 | 64 bits |
| `ULINT` | UInt64 | 64 bits |
| `REAL` | Float | 32 bits |
| `LREAL` | Double | 64 bits |
| `TIME` | Int64 | 64 bits (duration in ms) |
| `STRING` | String | Variable |

Structured data types and arrays are also supported. Structures are exposed as OPC-UA complex types, and arrays are exposed as OPC-UA array nodes.

### Per-Role Access Permissions (RBAC)

For each exposed variable, you define what each role can do:

| Permission | Symbol | Description |
|------------|--------|-------------|
| **Read** | `r` | Role can read the variable's current value |
| **Write** | `w` | Role can write a new value to the variable |
| **Read/Write** | `rw` | Role can both read and write the variable |
| **No Access** | `--` | Role cannot see or interact with this variable |

**Example access control matrix**:

| Variable | Viewer | Operator | Engineer |
|----------|--------|----------|----------|
| `MotorSpeed` | r | rw | rw |
| `MotorEnable` | r | rw | rw |
| `AlarmHistory` | r | r | rw |
| `SystemConfig` | -- | -- | rw |
| `SensorTemp` | r | r | r |

In this example:
- **Viewers** can monitor motor speed, motor status, alarms, and temperature but cannot change anything.
- **Operators** can read and write motor control variables and read alarms and temperatures.
- **Engineers** have full access to all variables, including system configuration that is hidden from other roles.

## Bidirectional Synchronization

The OPC-UA server maintains bidirectional synchronization between the PLC runtime and the OPC-UA address space:

- **Runtime to OPC-UA (Publish)**: The server reads variable values from the PLC runtime at the configured cycle time and updates the corresponding OPC-UA nodes. This ensures external clients always see current values.

- **OPC-UA to Runtime (Write)**: When an external client writes a value to an OPC-UA node (and the user has write permission), the server propagates the new value back to the PLC runtime. The PLC program sees the updated value on its next scan cycle.

The synchronization module handles the data flow in both directions, applying type conversions and access control checks.

## Configuration Export

When you transfer a project to the runtime, the OPC-UA server configuration is exported as `opcua.json` inside the program package. This file contains:

- General server settings (name, port, endpoint)
- Security profile definitions
- User accounts (with bcrypt-hashed passwords)
- Certificate references
- Address space node definitions with permissions

The file is generated automatically by the editor. You do not need to edit it manually.

## Example: Complete OPC-UA Server Setup

Here is a walkthrough of a typical OPC-UA server configuration for a production environment.

### Step 1: General Settings

```
Server Name:    Plant_Floor_PLC
Bind Address:   0.0.0.0
Port:           4840
Endpoint Path:  /opcua
Cycle Time:     100 ms
```

### Step 2: Security Profile

```
Policy:          Basic256Sha256
Mode:            SignAndEncrypt
Authentication:  Username/Password, Certificate
```

### Step 3: Users

| Username | Role | Auth Type |
|----------|------|-----------|
| `scada_reader` | Viewer | Username/Password |
| `operator_hmi` | Operator | Username/Password |
| `eng_workstation` | Engineer | Certificate |

### Step 4: Certificates

- Server certificate: Auto-generated self-signed (or upload a CA-signed certificate for production).
- Trusted client certs: Add the certificate for `eng_workstation`.

### Step 5: Address Space

| Variable | Node ID | Viewer | Operator | Engineer |
|----------|---------|--------|----------|----------|
| `MotorSpeed` | `ns=2;s=MotorSpeed` | r | rw | rw |
| `MotorEnable` | `ns=2;s=MotorEnable` | r | rw | rw |
| `TankLevel` | `ns=2;s=TankLevel` | r | r | rw |
| `PID_Kp` | `ns=2;s=PID_Kp` | -- | -- | rw |

With this configuration:
- The SCADA system (`scada_reader`) connects with username/password authentication over an encrypted channel and can read motor speed, motor enable status, and tank level.
- The HMI panel (`operator_hmi`) can read and control the motor but cannot modify PID tuning parameters.
- The engineering workstation (`eng_workstation`) authenticates via certificate and has full access to all variables, including PID parameters.

## Comparison with Modbus

| Feature | Modbus TCP | OPC-UA |
|---------|-----------|--------|
| Encryption | No | Yes (AES-128/256) |
| Authentication | No | Yes (username/password, certificate) |
| Access Control | No | Yes (role-based, per-variable) |
| Data Types | Bits and 16-bit registers | Full IEC type mapping |
| Variable Selection | Fixed buffer ranges | Any project variable |
| Structured Data | No | Yes |
| Discovery | No | Yes (server browsing) |
| Memory Addresses (`%M`) | v3 only | Yes (all variables) |

If your application requires security, rich data modeling, or access to variables beyond the Modbus buffer limits, OPC-UA is the recommended protocol.

## Troubleshooting

### Clients Cannot Discover or Connect

1. Verify the OPC-UA server is enabled in the General tab.
2. Confirm the runtime is running and the PLC program is loaded.
3. Check that port 4840 (or your custom port) is not blocked by a firewall.
4. Verify the client is using the correct endpoint URL: `opc.tcp://<host>:<port><path>`.
5. If using a security policy other than `None`, ensure the client has the server's certificate in its trust store.

### Authentication Failures

1. Verify the username and password are correct (passwords are case-sensitive).
2. For certificate authentication, ensure the client's certificate is in the server's trusted list.
3. Confirm the security profile allows the authentication method the client is using.
4. Check that the user account exists in the Users tab and has the correct authentication type.

### Permission Denied on Read or Write

1. Check the user's role assignment in the Users tab.
2. Verify the variable's per-role permissions in the Address Space tab.
3. Ensure the variable is actually added to the OPC-UA address space (not all project variables are exposed by default).

### Stale or Unchanging Values

1. Check the cycle time setting in the General tab. A very long cycle time means values update infrequently.
2. Confirm the PLC program is running and actively updating the variables.
3. Verify the synchronization module is active by checking runtime logs.

### Certificate Errors

1. If using auto-generated certificates, the client may reject the self-signed certificate. Add the server's certificate to the client's trusted list, or switch to a CA-signed certificate.
2. Check certificate expiration dates. Expired certificates are rejected by both server and client.
3. Ensure the Application URI in the certificate matches the server's configured Application URI.

## What's Next?

- **[Communication Protocols Overview](../README)** — Return to the protocols overview for Modbus and other options
- **[Modbus Server Configuration](../modbus/server)** — Simpler alternative for basic data exchange without security requirements
- **[Modbus Addressing](../modbus/addressing)** — Understand IEC-to-Modbus address mapping if using both protocols
