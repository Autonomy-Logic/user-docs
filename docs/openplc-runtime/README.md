# OpenPLC Runtime

OpenPLC Runtime is a headless industrial Programmable Logic Controller (PLC) runtime that transforms standard computing hardware into a powerful automation controller. It executes IEC 61131-3 programs created in OpenPLC Editor, supporting all standard PLC programming languages as well as Python, C, and C++.

## Overview

OpenPLC Runtime v4 is a complete rewrite of the runtime, built from the ground up for modern industrial automation needs. It provides:

- **Modern Architecture**: Redesigned for reliability, security, and extensibility
- **Real-time Execution**: SCHED_FIFO priority scheduling for deterministic scan cycles
- **Plugin System**: Extensible architecture supporting Python and C/C++ plugins
- **Secure Communication**: HTTPS with JWT authentication for all API endpoints
- **WebSocket Debug**: Real-time variable inspection and forcing capabilities

## In This Section

- **[Overview](overview.md)**: Architecture and key features of Runtime v4
- **[Installation](installation.md)**: How to install the runtime on Linux
- **[Program Upload](program-upload.md)**: Uploading programs via the REST API
- **[First User Setup](first-user-setup.md)**: Creating the initial user account
- **[Located Variables and Addressing](located-variables-and-addressing.md)**: IEC 61131-3 address format
- **[Hardware](hardware/)**: Pin mapping and hardware configuration
- **[v3 Legacy](v3-legacy/)**: Information for users migrating from Runtime v3

## Runtime Versions

### Runtime v4 (Current)

The current version of OpenPLC Runtime, featuring:

- REST API for all operations (no web UI)
- JWT-based authentication
- Plugin system for protocols and hardware I/O
- HTTPS-only communication (port 8443)
- ZIP-based program upload

### Runtime v3 (Legacy)

The previous version of OpenPLC Runtime, which includes:

- Web-based configuration interface
- Built-in protocol support (Modbus, DNP3, EtherNet/IP)
- HTTP communication
- Database-driven configuration

> **Note**: Runtime v3 is being deprecated. New installations should use Runtime v4.

## Supported Platforms

OpenPLC Runtime v4 runs on:

- **Linux**: Native installation on most distributions
- **Docker**: Containerized deployment on any Docker-capable system
- **Raspberry Pi**: ARM-based single-board computers
- **Industrial Edge Devices**: Linux-based industrial PCs and PLCs

## Getting Started

1. [Install the runtime](installation.md) on your target hardware
2. [Create the first user](first-user-setup.md) account
3. Connect from OpenPLC Editor to upload and run programs
4. Configure [communication protocols](../openplc-editor/communication/) as needed
