# Understanding vPLC Devices

Virtual PLCs (vPLCs) are software-based programmable logic controllers that run inside Docker containers on your orchestrator's host machine. They provide the same functionality as physical PLCs but with the flexibility and scalability of containerized applications.

## What is a vPLC?

A vPLC is a containerized instance of the OpenPLC Runtime that runs on an edge device managed by an orchestrator agent. Each vPLC operates as an independent PLC, capable of running IEC 61131-3 programs written in languages like Structured Text, Ladder Diagram, Function Block Diagram, and more.

When you create a vPLC through the Autonomy Edge platform, the orchestrator agent automatically provisions a new Docker container with the OpenPLC Runtime software. This container runs independently on the host machine and can be managed remotely through the platform.

## Key Benefits

**Rapid Deployment**: Create new PLC instances in seconds without any physical hardware installation. Simply configure the network settings and your vPLC is ready to run programs.

**Scalability**: Run multiple vPLCs on a single edge device, each with its own network configuration and program. This allows you to consolidate automation workloads and reduce hardware costs.

**Remote Management**: Monitor, configure, and update your vPLCs from anywhere through the Autonomy Edge platform. Upload new programs, check status, and view runtime statistics without physical access to the device.

**Consistency**: Every vPLC runs the same OpenPLC Runtime software, ensuring consistent behavior across all your automation projects. Programs developed and tested on one vPLC will work identically on others.

**Integration with OpenPLC Editor**: The built-in OpenPLC Editor on Autonomy Edge connects directly to your vPLCs through the orchestrator agent. This seamless integration allows you to develop, compile, and deploy programs without leaving the platform.

## How vPLCs Work

When you create a vPLC, the following happens behind the scenes:

1. The Autonomy Edge platform sends a request to the orchestrator agent running on your edge device
2. The orchestrator agent creates a new Docker container with the OpenPLC Runtime image
3. The container is configured with the network settings you specified (DHCP or static IP)
4. The vPLC starts running and becomes available for program uploads

The orchestrator agent continuously monitors the vPLC container and reports its status back to the platform. You can see real-time information about each vPLC including its running state, network configuration, and resource usage.

## vPLC vs Physical PLCs

vPLCs and physical PLCs serve the same fundamental purpose: executing automation programs that control industrial processes. However, there are some important differences to consider:

**Network Configuration**: vPLCs use virtual network interfaces (vNICs) that can be configured with DHCP or static IP addresses. The orchestrator agent manages the network bridge that connects vPLCs to the physical network.

**I/O Access**: Physical PLCs have direct access to hardware I/O modules. vPLCs can access I/O through network protocols like Modbus TCP/IP, allowing them to communicate with remote I/O devices and other PLCs on the network.

**Performance**: vPLCs share the host machine's CPU and memory resources. For time-critical applications, ensure your edge device has sufficient resources to maintain consistent scan cycle times.

**Portability**: vPLC programs can be easily moved between different edge devices. Simply create a new vPLC on another orchestrator and upload the same program.

## Compatibility with OpenPLC Editor Desktop

vPLCs run the exact same OpenPLC Runtime as physical devices running OpenPLC. This means you can also connect to vPLCs using the OpenPLC Editor desktop application from any computer on the same local network.

This is particularly useful for:

- Offline operation when internet connectivity is unavailable
- Local debugging and monitoring
- Integration with existing OpenPLC workflows

The OpenPLC Editor desktop application sees no difference between a vPLC and a physical OpenPLC device, so all features work identically.

## Next Steps

Now that you understand what vPLCs are and how they work, you can:

- [Create your first vPLC](creating-vplc) on an orchestrator
- [Upload a program](creating-vplc#uploading-programs) to your vPLC using the OpenPLC Editor
- [Monitor your vPLC status](managing-status) and view runtime statistics
