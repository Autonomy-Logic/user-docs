# Logging

The **Logging** accordion exposes three independent toggles that control which categories of S7Comm events the runtime records. Logs flow into the runtime's standard log stream. The same stream that surfaces in the orchestrator's runtime view alongside Modbus and OPC-UA logs.

## Field Walk-through

| Toggle | Default | Helper Text | Description |
|--------|---------|-------------|-------------|
| **Log Connections** | On | `Log client connect/disconnect` | Records every TCP accept and disconnect, with the remote IP and port. Lightweight; safe to leave on in production. |
| **Log Data Access** | Off | `Log read/write operations (verbose)` | Records every read/write request a client issues, including the DB number and offset. Verbose; intended for debugging only. |
| **Log Errors** | On | `Log errors and warnings` | Records protocol-level errors: malformed requests, timeouts, PDU mismatches, refused writes. Always leave this on. |

All toggles apply immediately. Changes are saved as soon as you flip the switch.

## Recommendations

- **Production deployments**: keep the defaults (Connections on, Data Access off, Errors on). This gives you a useful audit trail of who connected and when, plus any protocol failures, without flooding the log with per-request entries.
- **Commissioning a new client**: turn **Log Data Access** on temporarily. The verbose log will show every DB and offset the client is touching, which is the fastest way to confirm that your buffer mappings line up with what the client expects. Turn it off again once you are satisfied. Even a moderately busy HMI generates hundreds of log lines per second when this is enabled.
- **Silent installation**: turn off **Log Connections** if you find the connect/disconnect noise distracting in environments where the same SCADA is connected continuously. Leave **Log Errors** on regardless.

## Where the Logs Appear

S7Comm log entries are written to the runtime's log stream. You can read this stream wherever you normally read runtime logs. Typically in the orchestrator's runtime view on the platform, or in the host's system journal if you run the runtime as a system service.

Each line is tagged with a category and the server's name (the one you entered when you created the project entry), making it straightforward to filter by server when you have multiple S7Comm servers in the same project or multiple plugins on the same runtime.

## What's Next?

- **[Example](example)**: See logging in action with a worked configuration
- **[Troubleshooting](troubleshooting)**: Use logs to diagnose connection problems
- **[S7Comm Server Overview](README)**: Return to the protocol overview
