# Worked example: OPC-UA, read a variable from UaExpert

Expose a `REAL` variable from your PLC over OPC-UA, then browse and subscribe to it from [**UaExpert**](https://www.unified-automation.com/products/development-tools/uaexpert.html), the de-facto reference client.

**Surfaces exercised:** OPC-UA server tabs (General Settings, Security Profiles, Users, Address Space), namespace identifiers, the runtime's WebSocket bridge.

**Expected time:** about 15 minutes (mostly UaExpert install + first connection).

## What we're building

A vPLC running an OPC-UA server with one exposed variable:

- `process_temp : REAL`, updated every PLC scan with a sin wave between 20.0 and 30.0.

A UaExpert session that connects, browses the address space, and subscribes to live updates.

## Step 1: The program

Create an ST program with these variables:

| Name | Class | Type |
|---|---|---|
| `process_temp` | Local | REAL |
| `t` | Local | TIME |

```iec
(* Update process_temp with a sin wave every scan *)
t := TIME();
process_temp := 25.0 + 5.0 * SIN(REAL_TO_LREAL(TIME_TO_DINT(t)) * 0.001);
```

`SIN` is in **iec-std-functions** (enabled by default). The full chain converts the current time (TIME) to seconds (DINT) to a real, then takes its sine multiplied by 5, offset by 25 to centre the wave at 25.0.

## Step 2: Add the OPC-UA server

1. **`+`** at the top of the project tree → **server** → **OPC-UA**.
2. Name it `opcua`, click **Create**.
3. The new server appears under **Servers**. Click it.

## Step 3: General Settings

In the first tab:

- **Enable Server**: on.
- **Server Name**: `Process Demo OPC UA`.
- **Network Interface**: `0.0.0.0`.
- **Port**: `4840`.
- **Endpoint Path**: `/openplc/opcua`.
- **Cycle Time**: `100` ms (how often the server pushes updates to subscribed clients).

Leave the **Application URI** and **Product URI** at their defaults.

The endpoint URL clients will use is:

```
opc.tcp://<vPLC IP>:4840/openplc/opcua
```

For the Simulator, that's `127.0.0.1:4840`. (The Simulator's network bridge accepts incoming OPC-UA connections from your host machine on this port.)

## Step 4: Security Profiles

For a first connection, allow anonymous unencrypted access. Add a profile (or edit the default) with:

- **Security Policy**: `None`.
- **Security Mode**: `None`.
- **Auth methods**: `Anonymous`.
- **Enabled**: on.

This is fine for a local-only demo. For anything off your machine, configure a profile with `Basic256Sha256` and `SignAndEncrypt`, plus certificates (see the Certificates tab).

## Step 5: Address Space

This tab lets you pick which variables get published, with per-variable browse names and permissions.

1. The tree on the left mirrors your project (POU variables + globals).
2. Tick `process_temp`.
3. Fill in:
   - **Node ID**: `process_temp` (or accept the auto-generated one).
   - **Browse Name**: `ProcessTemp`.
   - **Display Name**: `Process Temperature`.
   - **Description**: `Demo sin wave centred at 25°C with ±5°C amplitude.`
   - **Permissions**: tick **r** (read) for the `viewer` role.

Save.

## Step 6: Run and connect

Click **Start Simulator** (or Build & Upload + Play on a vPLC). The OPC-UA server boots inside the runtime and starts listening.

Open **UaExpert** (download from Unified Automation):

1. **Server → Add → Custom Discovery**. Paste the endpoint URL: `opc.tcp://127.0.0.1:4840/openplc/opcua`.
2. Pick the endpoint that appears (it'll match the policy you configured: `None`/`None`/`Anonymous`).
3. Click **OK**, then double-click the new server entry to connect.

The session opens and UaExpert's **Address Space** pane on the left now shows the server's tree. Navigate to **Objects → Process Demo OPC UA → ProcessTemp**.

## Step 7: Subscribe

Drag **ProcessTemp** from the Address Space pane onto the **Data Access View** in the centre. A subscription starts:

- **Value** updates every 100 ms (your configured cycle time).
- It oscillates between roughly 20.0 and 30.0.

Right-click the row → **Show DataChange Trend** to plot it.

## Step 8: Writing back (optional)

If you grant write permission on the node (tick **w** in the Address Space permissions), UaExpert can also push values:

1. Right-click the variable in the Data Access View.
2. Pick **Write Value...**.
3. Set a new value and confirm.

Your ST program will overwrite the value on the next scan unless you tweak the code. To make the write stick, change the program to only update `process_temp` if a separate "remote control" flag is `FALSE`.

## Permissions cheat sheet

OPC-UA permissions on this build are **role-based**: `viewer`, `operator`, `engineer`. Each role gets per-node `r` / `w` toggles:

- `viewer` typically gets `r` only: read-only HMI / dashboard accounts.
- `operator` gets `r` plus `w` on safe-to-write nodes (setpoints, modes).
- `engineer` gets `r` plus `w` on everything, including configuration nodes.

Roles are assigned to users in the **Users** tab, see **[OPC-UA users](../communication/opc-ua/users)** for the full reference.

## Troubleshooting

**UaExpert says "endpoint not found".** The server isn't listening, or the endpoint path is wrong. Check the runtime is running (Play is green), and that the URL exactly matches the Endpoint Path field.

**Connection succeeds but the address space is empty.** No variables are ticked in the Address Space tab. Open the tab, tick `process_temp`, save, restart the PLC.

**Values update but stay constant at 25.0.** Your `SIN` argument might be in radians where the wave period is far longer than your observation window. Bump the multiplier from `0.001` to something larger to see faster oscillation.

## Where to next

- **[OPC-UA server reference](../communication/opc-ua/general-settings)**: every tab, every field.
- **[OPC-UA address space](../communication/opc-ua/address-space)**: how to expose structures and arrays, not just scalars.
- **[Security profiles](../communication/opc-ua/security-profiles)**: moving from `None`/`Anonymous` to certificate-based auth.
