# Network and Connectivity Issues

Autonomy Edge relies on network connectivity between several components: the web IDE, the cloud backend, orchestrators on your edge hardware, and your PLC devices. When connections fail, you may see devices going offline, programs failing to deploy, or communication protocols (Modbus, OPC-UA) not working. This guide helps you quickly find and fix the most common network problems.

## IDE and Cloud Connectivity

### Can't Access the IDE

**Symptom:** The Autonomy Edge web IDE at edge.autonomylogic.com doesn't load or is very slow.

**Cause:** Internet connectivity issue, DNS problem, or browser cache.

**Fix:**
1. Check your internet connection
2. Try accessing `https://edge.autonomylogic.com` in an incognito/private window
3. Clear your browser cache and try again
4. If the issue persists, check [Autonomy Edge status](https://edge.autonomylogic.com) for any service announcements

---

### API Requests Failing

**Symptom:** API calls to the Autonomy Edge platform return errors or time out.

**Cause:** Authentication expired, network issue, or rate limiting.

**Fix:**
1. **Check your token**: If you get `401 Unauthorized`, your access token has expired. Refresh it using the `/auth/refresh` endpoint
2. **Check rate limits**: If you get `429 Too Many Requests`, wait and retry
3. **Check connectivity**: Verify you can reach `https://edge.autonomylogic.com` from your machine

## Orchestrator Connection Issues

### Orchestrator Shows "Offline"

**Symptom:** The orchestrator appears offline in the dashboard, even though the edge hardware is powered on.

**Cause:** The orchestrator service isn't running, or the edge device can't reach the cloud.

**Fix:**
1. **Verify the orchestrator is running** on your edge device. Check the service status
2. **Check internet connectivity** from the edge device:
   ```bash
   ping edge.autonomylogic.com
   ```
3. **Check DNS resolution:**
   ```bash
   nslookup edge.autonomylogic.com
   ```
4. **Check firewall rules**: Outbound HTTPS (port 443) must be open
5. **Restart the orchestrator** if the above checks pass

---

### Orchestrator Connects Then Disconnects

**Symptom:** The orchestrator briefly shows as online then goes offline again repeatedly.

**Cause:** Authentication issue or network instability causing connection drops.

**Fix:**
1. Check that the orchestrator credentials are valid
2. Check for network instability (high latency, packet loss)
3. The orchestrator automatically reconnects with backoff. If reconnection attempts continue, the issue is likely authentication rather than network

## Device Issues

### Device Won't Start

**Symptom:** Clicking "Start" on a device in the dashboard fails or the device remains stopped.

**Cause:** The orchestrator is offline, or the edge device lacks resources.

**Fix:**
1. **Check the orchestrator is online**: The start command goes through the orchestrator
2. **Check available resources** on the edge device. Verify disk space and memory aren't exhausted:
   ```bash
   df -h
   free -h
   ```
3. **Check the console** in the dashboard for error messages

---

### Device Stuck in "Creating"

**Symptom:** A new device stays in "Creating" status and never becomes ready.

**Cause:** The runtime is being downloaded (slow network), or there's a resource conflict.

**Fix:**
1. **Wait**: On slow connections, initial setup can take several minutes
2. **Check the orchestrator status** in the dashboard for error details
3. If it's stuck for more than 10 minutes, try deleting the device and creating a new one

## Modbus Communication Issues

### Modbus Client Not Connecting

**Symptom:** Your PLC program uses Modbus TCP to communicate with remote I/O modules, but the connection fails or values aren't updating.

**Cause:** Network path blocked, wrong IP/port, or incorrect Modbus configuration.

**Fix:**

1. **Verify network path** from the edge device to the Modbus device:
   ```bash
   ping <modbus-device-ip>
   ```
2. **Verify the Modbus port is open:**
   ```bash
   nc -zv <modbus-device-ip> 502
   ```
   Standard Modbus TCP uses port 502. Some devices use alternative ports.
3. **Check your Modbus configuration** in the project:
   - Is the IP address correct?
   - Is the correct Modbus unit ID (slave ID) configured?
   - Do the register addresses match the device's documentation?
   - Are the function codes correct for the register type?

**Common Modbus function code mapping:**

| Register Type | Read Function | Write Function | IEC Address |
|---------------|---------------|----------------|-------------|
| Coils (discrete outputs) | FC01 | FC05/FC15 | `%QX` |
| Discrete Inputs | FC02 |. (read-only) | `%IX` |
| Holding Registers | FC03 | FC06/FC16 | `%QW` / `%MW` |
| Input Registers | FC04 |. (read-only) | `%IW` |

---

### Modbus Values Incorrect or Stale

**Symptom:** Modbus communication is active but values don't match what you expect.

**Cause:** Byte order mismatch, register offset, or data type mapping issue.

**Fix:**
- **Byte order**: Some devices use big-endian, others little-endian. Swapped bytes produce garbled values for 16-bit and 32-bit registers
- **Register offset**: Some devices use 0-based addressing, others 1-based. A register documented as "40001" might be address 0 or 1 depending on the convention
- **Data type**: A 32-bit float spans two consecutive Modbus registers. Make sure your mapping accounts for this
- **Poll rate**: If the Modbus poll interval is slower than your scan cycle, values may appear stale

---

### Modbus Server Not Responding to External Clients

**Symptom:** Your device is acting as a Modbus server and external systems can't connect to it.

**Cause:** The Modbus server plugin isn't enabled, wrong port, or network routing issue.

**Fix:**
1. Verify the Modbus server plugin is enabled in the runtime configuration
2. Check the listening port. Default is 502, but it may be configured differently
3. Make sure the external client can reach the device's IP address and port

## OPC-UA Communication Issues

### OPC-UA Connection Failed

**Symptom:** The OPC-UA plugin can't connect to the OPC-UA server.

**Cause:** Wrong endpoint, security mismatch, or firewall blocking the port.

**Fix:**
- **Endpoint URL**: Verify the OPC-UA server endpoint (e.g., `opc.tcp://192.168.1.100:4840`)
- **Security policy**: Make sure the security settings match the server's requirements
- **Certificates**: OPC-UA may require certificate exchange between client and server
- **Firewall**: OPC-UA typically uses port 4840 but can be configured differently

## General Network Diagnostics

### Quick Checks

When something network-related isn't working, start with these:

| Check | Command |
|-------|---------|
| Internet connectivity | `ping 8.8.8.8` |
| DNS resolution | `nslookup edge.autonomylogic.com` |
| Target reachability | `ping <target-ip>` |
| Port open | `nc -zv <ip> <port>` |
| System resources | `free -h && df -h` |

### Firewall Considerations

Make sure these ports are open on your edge hardware:

| Port | Protocol | Direction | Purpose |
|------|----------|-----------|---------|
| 443 | HTTPS | Outbound | Cloud platform access |
| 502 | Modbus TCP | Both | Modbus communication |
| 4840 | OPC-UA | Both | OPC-UA communication |
| 102 | S7Comm | Both | S7 communication |

> **Tip:** If devices are referenced by hostname instead of IP and connections fail, try using IP addresses directly. This eliminates DNS as a potential issue.

## What's Next?

- [Compilation Errors](compilation-errors): Fix code issues before deployment
- [Runtime Debugging](runtime-debugging): Debug your running program
- [Edge Functions](../integration-apis/edge-functions): Understand the Autonomy Edge REST API
