# Troubleshooting

This page covers the most common S7Comm Server failure modes you will encounter in the editor or in the runtime logs, and what to do about each one.

## Server Doesn't Start

**Symptom**: The runtime is up and your program is running, but no client can connect on port 102.

Check, in order:

1. **Enable Server is on.** Open the S7Comm Server entry in the project explorer, expand **Server Configuration**, and verify the **Enable Server** toggle is on. If the helper text reads `Server is disabled`, flip it on, save, and re-transfer the project.
2. **The latest project was transferred.** Configuration changes require a project transfer to take effect. Turning the toggle on in the editor alone does not start the listener.
3. **The port is not in use.** Only one process can bind to a given TCP port on a given interface. If another runtime, another plugin, or any system service already listens on 102, the S7Comm listener fails to start. The runtime log records the bind error. Pick a different port (e.g., 1102) or stop the conflicting service.
4. **The runtime has permission to bind below 1024.** On Linux, ports 1 -- 1023 are privileged. The runtime needs `CAP_NET_BIND_SERVICE` to bind to port 102. If the log shows a permission denied error, either grant the capability or move the server to a port above 1024.

## Clients Cannot Connect (Connection Refused)

**Symptom**: The client tool reports `connection refused` or a TCP RST.

1. **Verify the listener is up.** From the client host, try `telnet <runtime-ip> 102` or `nc -zv <runtime-ip> 102`. If TCP itself fails, the listener is not running. See the section above.
2. **Check the bind address.** If you set Bind Address to `Localhost (127.0.0.1)`, only clients running on the same host as the runtime can connect. Switch to `All Interfaces (0.0.0.0)` to accept remote connections.
3. **Check the firewall.** The runtime host's firewall (or any intermediate network firewall) must allow inbound TCP 102. On a typical Linux host, run `sudo iptables -L INPUT -n | grep 102` to spot blocking rules.
4. **Confirm the client is using the right IP and port.** `0.0.0.0` is a "listen on everything" address. It is **not** the address the client should dial. The client needs the runtime host's actual LAN address.

## Clients Connect Then Disconnect Immediately

**Symptom**: The client establishes the TCP connection, then drops it within a second.

1. **PDU negotiation mismatch.** S7 clients propose a PDU size in their first request. The server agrees on the smaller of its configured PDU and the client's request. Older clients sometimes misbehave when the server's advertised PDU is much larger than they expect. If you set **PDU Size** to 960, try lowering it to 480 (the default) for older clients.
2. **Identity strings rejected.** Some strict HMI engines parse the SZL identity and refuse connections from CPUs they don't recognise. If you customised the **Module Type** field in **PLC Identity**, restore the default `CPU 315-2 PN/DP` and try again.
3. **Max Clients limit reached.** If the runtime already has the configured maximum number of S7 clients connected, the next accept is refused. Disconnect any forgotten sessions or raise **Max Clients**.

## Cannot Add a Data Block: "DB&lt;n&gt; already exists"

**Symptom**: The Add Data Block modal shows a red error such as `DB1 already exists` and refuses to save.

The DB number you entered is in use by another DB on the same server. Either:

- Pick a different number (any value 1 -- 65535 not already in the table), or
- Delete the conflicting DB from the table first if you intended to replace it, or
- Use the pencil icon on the existing row to edit it instead of creating a new one.

The same validation applies when you edit a DB and try to change its number to one that already exists. The row you are editing is the only one exempt from the duplicate check.

## Cannot Add a Data Block: Other Validation Errors

The modal blocks the save action with these inline errors:

| Error Message | Cause | Fix |
|---------------|-------|-----|
| `DB Number must be between 1 and 65535` | The DB Number field is empty, non-numeric, or out of range. | Enter an integer 1 -- 65535. |
| `Size must be between 1 and 65536 bytes` | Size is empty, non-numeric, or out of range. | Enter a byte count 1 -- 65536. |
| `Start buffer must be between 0 and 1023` | Start Buffer is empty, negative, or above 1023. | Enter an offset 0 -- 1023 within the chosen buffer. |

## Add Data Block Button Is Disabled

The **+ Add Data Block** button greys out when the project already contains the maximum of **64** Data Blocks per server. The accordion header shows `Data Blocks (64/64)` in this state. Delete an unused DB before you can add a new one.

## Reads Return Unchanging or Wrong Values

**Symptom**: The client successfully reads a DB but the value is always 0, always the same, or visibly wrong.

1. **Wrong mapping type.** Make sure the DB's mapping type matches the IEC variable's prefix. `%QX0.0` lives in **Boolean Output (%QX)**, not in **Boolean Memory (%MX)**: picking the wrong one points the DB at an unrelated buffer.
2. **Wrong Start Buffer offset.** A DB starting at offset 4 reads from the 5th byte of the chosen buffer (`%QB4` or `%QW4` depending on width). Walk the offset against your IEC addresses with care.
3. **Bit Addressing not enabled for bool DBs.** When the mapping is `bool_*` and you want individual bits at `DBX<byte>.<bit>`, turn the **Bit Addressing** toggle on. With it off, clients see packed bytes instead.
4. **The PLC program is not driving the variable.** Confirm the variable is actually written by your program. A `%QX` output that no rung touches sits at its initial value forever.

## PDU Negotiation Anomalies

**Symptom**: Bulk reads return less data than requested, or split into unexpectedly many round trips.

The PDU you set in **Server Configuration** is the *maximum*. Clients can. And routinely do. Propose smaller PDUs. The agreed-upon PDU is the smaller of the two values, and it is the upper bound on a single read or write. If a client tries to read more than the negotiated PDU allows, the client (not the server) splits the request into multiple S7 messages.

If you need larger transfers per round trip:

- Raise the server's **PDU Size** to 960.
- Configure the client to request the same maximum.
- Verify in the runtime logs (with **Log Connections** on) that the negotiated PDU is what you expect.

## Where to Look in the Logs

Enable **Log Errors** (default on) for protocol-level failures and **Log Connections** (default on) for accept/disconnect lines. For deep debugging. Wrong DB numbers, malformed offsets. Turn on **Log Data Access** temporarily; this records every read and write and is far too verbose for normal operation.

Logs are written to the runtime log stream, which surfaces in the orchestrator's runtime view and in the runtime host's system journal.

## What's Next?

- **[Server Configuration](server-configuration)**: Revisit the network settings
- **[Data Blocks](data-blocks)**: Re-check buffer mappings and offsets
- **[S7Comm Server Overview](README)**: Return to the protocol overview
