# Example: Exposing the Blink Project's LED Output

This walk-through configures an S7Comm server against the standard Autonomy Edge **blink** project and connects to it from a generic S7 client. By the end you will have a Siemens-style DB1 that toggles every cycle as the program runs, observable from any S7 tool.

The starting project is the default blink program: a single rung that toggles a `BOOL` output named `led` mapped to `%QX0.0`, driven by two timers. Nothing about the program logic needs to change.

## Step 1: Add an S7Comm Server

1. In the project explorer, click the **+** button.
2. Choose **Server**, then select **Siemens S7comm** as the protocol.
3. Name the server `blink-s7-server` and click **Create**.
4. The new entry appears under the **Servers** folder. Click it to open the configuration panel.

## Step 2: Configure the Server

In the **Server Configuration** accordion, set:

| Field | Value |
|-------|-------|
| Enable Server | **On** |
| Bind Address | All Interfaces (0.0.0.0) |
| Port | 102 |
| Max Clients | 32 |
| PDU Size | 480 |

That is everything you need on the network side. The defaults are correct for a standard Siemens client.

## Step 3: Define DB1

The blink project's only output is `led` at `%QX0.0`. This is bit 0 of byte 0 of the **Boolean Output** buffer, so the matching mapping type is `Boolean Output (%QX)`.

1. Expand the **Data Blocks** accordion.
2. Click **+ Add Data Block**.
3. Fill in:

| Field | Value |
|-------|-------|
| DB Number | `1` |
| Description | `Blink LED state` |
| Size (bytes) | `1` |
| Mapping Type | `Boolean Output (%QX)` |
| Start Buffer | `0` |
| Bit Addressing | **On** |

4. Click **Add Data Block**.

The accordion now shows a single row: `DB1 / Blink LED state / 1 bytes / Boolean Output (%QX)`. The header counter reads `Data Blocks (1/64)`.

The combination of `Size = 1` byte, `Start Buffer = 0`, and `Bit Addressing = on` exposes the 8 bits of `%QX0.0` through `%QX0.7` as `DB1.DBX0.0` through `DB1.DBX0.7`. Only `DB1.DBX0.0` is wired to anything in this project. That is the blink LED.

## Step 4: Save and Transfer

Save the project and transfer it to a vPLC device the same way you would any other project. The runtime starts the S7Comm listener on port 102 as soon as the program runs.

## Step 5: Connect from an S7 Client

The plugin is server-side; the rest of this section describes things you do **on the client tool**. Pick whichever tool is convenient:

- **`python-snap7`**: a Python wrapper around the Snap7 library
- **`libnodave` / NodeS7**: Node.js drivers used by many open-source SCADA stacks
- **A Siemens HMI** (WinCC, TIA Portal monitor windows)
- **Diagnostic GUIs** such as PLCSIM Advanced's connection tester

S7 clients typically ask for four things to make a connection:

| Client Field | Value | Notes |
|--------------|-------|-------|
| **IP Address** | The runtime host's IP (e.g. `192.168.1.50`) | Use the actual host IP, not `0.0.0.0` |
| **Port** | `102` | The server's bind port |
| **Rack** | `0` | Client-side conventional value for an S7-300 |
| **Slot** | `1` | Client-side conventional value for the CPU slot |

`Rack` and `Slot` are S7 connection conventions on the **client side**. They do not correspond to anything you configure in the Autonomy Edge editor. The OpenPLC runtime is not a real S7 chassis.

In informal documentation the endpoint is sometimes written as `s7://192.168.1.50:102`. The S7 protocol does not define a URI scheme, but the shorthand is convenient.

## Step 6: Read the Toggling Bit

Once connected, ask the client to read **`DB1.DBX0.0`**. With the blink program running, the value alternates between `false` and `true` roughly every 500 ms / 1500 ms (driven by the project's TON and TOF blocks).

Here is what a minimal `python-snap7` reader looks like, for reference (this is **client-side** code, not something you put in the project):

```python
import snap7

client = snap7.client.Client()
client.connect('192.168.1.50', 0, 1)        # IP, rack, slot
data = client.db_read(1, 0, 1)              # DB1, offset 0, 1 byte
bit = bool(data[0] & 0x01)                  # DBX0.0 is the LSB of byte 0
print('LED state:', bit)
client.disconnect()
```

You will see the bit flip on every read as the rung evaluates.

## Step 7: Add a Writable DB (Optional)

If you also want the client to be able to *write* values that the PLC program can react to, add a second DB pointing at a `Boolean Memory (%MX)` or `Word Memory (%MW)` area, and reference the corresponding `%MX` / `%MW` variable from your ladder. Memory mappings give you read-write semantics that don't compete with the PLC scan over the output buffer.

## What's Next?

- **[Troubleshooting](troubleshooting)**: Resolve common connection failures
- **[Data Blocks](data-blocks)**: Browse the full mapping catalog for more elaborate setups
- **[S7Comm Server Overview](README)**: Return to the protocol overview
