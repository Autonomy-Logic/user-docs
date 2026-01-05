# Understanding Orchestrators

The orchestrator agent is one of the central pieces of the Autonomy Edge platform. It is the essential component that enables you to run PLC programs on physical hardware. Without an orchestrator agent installed on your edge device, the Autonomy Edge platform cannot connect to or control local PLC runtimes. The orchestrator serves as the secure bridge between the cloud-based Autonomy Edge application and your industrial automation equipment, making remote deployment and management of PLC programs possible from anywhere in the world.

## Why the Orchestrator is Essential

The Autonomy Edge platform is designed as a cloud-first solution where you create and edit PLC programs through a web browser. However, to actually execute these programs on real hardware and interact with physical I/O, you need a way to bridge the gap between the cloud and your local industrial network. This is exactly what the orchestrator agent provides.

When you deploy a PLC program from Autonomy Edge, the request flows from the cloud platform through the orchestrator agent to the OpenPLC runtime running on your edge device. The orchestrator handles all the complexity of secure communication, container management, and network configuration, allowing you to focus on your automation logic rather than infrastructure concerns.

## What Does an Orchestrator Do?

The orchestrator performs several critical functions in your automation infrastructure:

**Remote Device Management**: The orchestrator creates and manages virtual PLC containers (vPLCs) on your local machine. These vPLCs run the OpenPLC runtime and can execute your PLC programs just like physical industrial controllers.

**Secure Cloud Communication**: The orchestrator maintains a persistent, encrypted connection to the Autonomy Edge cloud using mutual TLS (mTLS) authentication. This ensures that only authorized devices can connect to your account and that all communication is protected from eavesdropping or tampering.

**System Monitoring**: The orchestrator continuously reports system health metrics including CPU usage, memory consumption, disk space, and uptime. These metrics are displayed in real-time on the Autonomy Edge platform, allowing you to monitor your edge devices from anywhere.

**Network Integration**: Virtual PLC devices created by the orchestrator can be configured to appear as physical devices on your local network using MACVLAN networking. This allows them to communicate directly with other industrial equipment using standard protocols like Modbus TCP.

**Dynamic Network Adaptation**: If your host machine moves between different networks (for example, a portable industrial system), the orchestrator automatically detects the network change and reconfigures the vPLC containers to maintain connectivity.

## Offline Operation and Local Network Access

An important characteristic of the orchestrator architecture is that internet connectivity is only required for remote monitoring and management. Once a vPLC instance is running your PLC program, all control logic executes locally on the edge device. If you lose internet connectivity, your PLC programs do not stop. The automation continues running normally, controlling your physical I/O and communicating with other devices on the local network.

What you lose without internet connectivity is the ability to use the Autonomy Edge cloud platform to monitor your vPLC instances, upload different programs, create new vPLCs, or view system metrics. However, all of these operations remain possible from the local network even without internet access.

Each vPLC instance runs exactly the same OpenPLC runtime as any physical PLC device running OpenPLC Runtime. This means you can use the OpenPLC Editor desktop software from any computer connected to the same local network to connect directly to your vPLC instances. From the perspective of OpenPLC Editor, there is no difference between a vPLC device created and managed by the Autonomy Edge orchestrator agent and a real physical OpenPLC Runtime running on dedicated PLC hardware.

This design provides operational resilience for industrial applications where continuous operation is critical. Your automation logic keeps running regardless of internet availability, and you always have local network access as a fallback for monitoring and programming.

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

## Compatible Industrial Devices

The orchestrator agent was designed to be widely compatible with any Linux device that provides shell access and can run Docker containers. This makes it suitable for deployment on a broad range of industrial hardware, from dedicated edge controllers to industrial PCs.

**Linux-Based PLCs and Edge Controllers**: Many modern industrial controllers run Linux and provide terminal access, making them excellent candidates for running the orchestrator agent. Examples include the Siemens IOT2050 industrial edge device, Opto 22 groov EPIC and groov RIO controllers, WAGO PFC200 series controllers, Phoenix Contact PLCnext controllers, Revolution Pi (Kunbus) industrial Raspberry Pi modules, and Hilscher netPI edge gateways.

**Industrial PCs and Edge Gateways**: Ruggedized industrial computers running Linux distributions are ideal hosts for the orchestrator. Popular options include Advantech UNO and ARK series industrial PCs, OnLogic industrial computers, Kontron embedded PCs, Moxa industrial computers and gateways, and Axiomtek and AAEON industrial box PCs.

**General-Purpose Linux Systems**: For development, testing, or less demanding applications, the orchestrator can run on any standard Linux system including server hardware, desktop computers, or single-board computers like Raspberry Pi (for evaluation purposes).

The key requirements for any device are: a supported Linux distribution (Ubuntu, Debian, RHEL, CentOS, or Fedora), the ability to run Docker containers, shell access with root or sudo privileges, and network connectivity to the internet. Before deploying to a specific industrial device, verify that your device's firmware allows Docker installation and that you have the necessary access permissions.

## Security Model

The orchestrator uses a robust security model based on mutual TLS (mTLS) authentication:

**Certificate-Based Identity**: Each orchestrator is assigned a unique identifier during installation. This identifier is embedded in an RSA-4096 certificate that the orchestrator uses to authenticate with the cloud.

**Mutual Authentication**: Both the orchestrator and the cloud server verify each other's identity before establishing a connection. This prevents unauthorized devices from connecting to your account and protects against man-in-the-middle attacks.

**Encrypted Communication**: All data transmitted between the orchestrator and the cloud is encrypted using TLS 1.2 or higher.

**Secure Credential Storage**: The orchestrator's private key is stored with restricted file permissions (600) in a protected directory, ensuring only the orchestrator process can access it.

For more information about adding orchestrators to your account, see [Adding Orchestrators](adding-orchestrators).
