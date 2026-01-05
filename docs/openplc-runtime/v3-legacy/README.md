# Runtime v3 Legacy

This section provides information for users migrating from OpenPLC Runtime v3 to v4, and documents v3-specific features for reference.

> **Note**: OpenPLC Runtime v3 is being deprecated. New installations should use Runtime v4.

## Overview

OpenPLC Runtime v3 was the previous generation of the runtime, featuring a web-based configuration interface and built-in protocol support. While v3 is still functional, v4 offers improved architecture, security, and extensibility.

## Key Differences from v4

| Feature | Runtime v3 | Runtime v4 |
|---------|-----------|-----------|
| Configuration | Web UI | REST API / Editor |
| Authentication | Basic HTTP | JWT tokens |
| Protocols | Built-in | Plugin-based |
| Port | 8080 (HTTP) | 8443 (HTTPS) |
| Database | SQLite | JSON files |

## v3-Only Features

Some features in v3 are not directly available in v4:

### Built-in Protocols

v3 included built-in support for:

- DNP3 (Distributed Network Protocol)
- EtherNet/IP
- S7 Protocol

These protocols are not yet available as v4 plugins.

### Web Interface

v3 provided a web-based interface for:

- Uploading programs
- Configuring hardware
- Setting up slave devices
- Monitoring runtime status

In v4, these functions are performed through OpenPLC Editor or the REST API.

## Migration Guide

### Preparing for Migration

1. Document your current v3 configuration
2. Export your PLC programs
3. Note all protocol and hardware settings
4. Plan for any v3-only features you rely on

### Installing v4

1. Install Runtime v4 on your target system
2. Create the first user account
3. Connect from OpenPLC Editor

### Migrating Programs

PLC programs created for v3 are compatible with v4:

1. Open your project in OpenPLC Editor
2. Connect to the v4 runtime
3. Upload the program

### Migrating Protocol Configuration

Protocol configuration has changed:

- **Modbus**: Configure in OpenPLC Editor, uploaded as JSON
- **DNP3/EtherNet/IP**: Not yet available in v4

### Migrating Hardware Configuration

Hardware configuration is now done in the editor:

1. Open Hardware Configuration in your project
2. Add and configure pins as needed
3. Upload with your program

## Keeping v3

If you need v3-specific features, you can continue using v3:

- v3 remains available at [github.com/thiagoralves/OpenPLC_v3](https://github.com/thiagoralves/OpenPLC_v3)
- OpenPLC Editor desktop supports both v3 and v4 runtimes
- Consider running v3 for legacy systems while using v4 for new projects

## Getting Help

If you encounter issues migrating from v3 to v4:

- Check the [OpenPLC Forum](https://openplc.discussion.community/)
- Review the v4 documentation
- Report issues on GitHub
