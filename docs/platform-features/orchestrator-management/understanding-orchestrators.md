# Understanding Orchestrators

An orchestrator is a software agent that runs on a Linux machine and serves as the bridge between the Autonomy Edge cloud platform and your local industrial automation devices. It enables you to remotely manage, monitor, and deploy PLC programs to virtual PLC devices (vPLCs) from anywhere in the world through the Autonomy Edge platform.

## What Does an Orchestrator Do?

The orchestrator performs several critical functions in your automation infrastructure:

**Remote Device Management**: The orchestrator creates and manages virtual PLC containers (vPLCs) on your local machine. These vPLCs run the OpenPLC runtime and can execute your PLC programs just like physical industrial controllers.

**Secure Cloud Communication**: The orchestrator maintains a persistent, encrypted connection to the Autonomy Edge cloud using mutual TLS (mTLS) authentication. This ensures that only authorized devices can connect to your account and that all communication is protected from eavesdropping or tampering.

**System Monitoring**: The orchestrator continuously reports system health metrics including CPU usage, memory consumption, disk space, and uptime. These metrics are displayed in real-time on the Autonomy Edge platform, allowing you to monitor your edge devices from anywhere.

**Network Integration**: Virtual PLC devices created by the orchestrator can be configured to appear as physical devices on your local network using MACVLAN networking. This allows them to communicate directly with other industrial equipment using standard protocols like Modbus TCP.

**Dynamic Network Adaptation**: If your host machine moves between different networks (for example, a portable industrial system), the orchestrator automatically detects the network change and reconfigures the vPLC containers to maintain connectivity.

## Architecture Overview

The orchestrator system consists of two Docker containers that work together:

**Orchestrator Agent**: This is the main control daemon that handles communication with the Autonomy Edge cloud, manages vPLC containers, and coordinates all orchestration activities.

**Network Monitor**: A companion container that monitors the host's physical network interfaces and manages DHCP clients for vPLC containers. It enables the dynamic network adaptation feature that keeps your vPLCs connected even when network conditions change.

Both containers run with automatic restart policies, ensuring your automation infrastructure remains operational even after system reboots or unexpected failures.

## When to Use an Orchestrator

You should deploy an orchestrator when you want to:

- Remotely manage PLC programs on edge devices without physical access
- Deploy and update automation logic across multiple sites from a central location
- Monitor the health and status of your industrial computing infrastructure
- Create virtual PLC devices that can communicate with physical industrial equipment
- Maintain secure, authenticated connections between your edge devices and the cloud

## System Requirements

Before installing an orchestrator, ensure your target machine meets the following requirements:

**Operating System**: Linux is required. The installer supports major distributions including Ubuntu, Debian, Red Hat Enterprise Linux (RHEL), CentOS, and Fedora.

**Privileges**: Root or sudo access is required for installation. The installer needs elevated privileges to install Docker (if not already present), create system directories, and configure the orchestrator containers.

**Docker**: Docker must be installed and running. If Docker is not present, the installer will attempt to install it automatically using your system's package manager.

**Network Access**: The machine must have internet access during installation to download container images and communicate with the Autonomy Edge provisioning service. After installation, ongoing internet access is required to maintain the connection with the cloud platform.

**Hardware**: The orchestrator itself has minimal resource requirements. However, you should ensure adequate resources for the vPLC containers you plan to run. Each vPLC requires approximately 256 MB of RAM and minimal CPU resources during normal operation.

The installer automatically checks for and installs these dependencies if they are missing: curl, jq, openssl, and docker.

## Security Model

The orchestrator uses a robust security model based on mutual TLS (mTLS) authentication:

**Certificate-Based Identity**: Each orchestrator is assigned a unique identifier during installation. This identifier is embedded in an RSA-4096 certificate that the orchestrator uses to authenticate with the cloud.

**Mutual Authentication**: Both the orchestrator and the cloud server verify each other's identity before establishing a connection. This prevents unauthorized devices from connecting to your account and protects against man-in-the-middle attacks.

**Encrypted Communication**: All data transmitted between the orchestrator and the cloud is encrypted using TLS 1.2 or higher.

**Secure Credential Storage**: The orchestrator's private key is stored with restricted file permissions (600) in a protected directory, ensuring only the orchestrator process can access it.

For more information about adding orchestrators to your account, see [Adding Orchestrators](adding-orchestrators).
