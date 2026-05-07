# PLC Identity

When an S7 client connects, one of the first things it usually does is query the controller's **SZL** (System Status List) to find out what kind of CPU it is talking to. The SZL response carries identification strings. The device name, the module type, a serial number, a copyright line, and a module name. HMIs and engineering tools display these values, and some of them filter their feature set based on the module type (for example, only enabling certain function block calls when they detect an S7-1500).

The **PLC Identity** accordion lets you customise those strings for the OpenPLC runtime so that S7 clients see whatever model and identifier you want.

The accordion's helper text reads:

> Configure the PLC identity returned in S7 SZL queries. These values help HMIs identify the PLC.

## Field Walk-through

| Field | Type | Default | Max Length | Description |
|-------|------|---------|------------|-------------|
| **PLC Name** | Text | `OpenPLC Runtime` | 64 | The friendly device name returned to clients. |
| **Module Type** | Text | `CPU 315-2 PN/DP` | 64 | The CPU model string. Defaults to a Siemens S7-300 model so that HMIs filtering by module type accept the connection. |
| **Serial Number** | Text | `S C-OPENPLC01` | 64 | The serial number string. The space and `C-` prefix follow the Siemens factory format. |
| **Copyright** | Text | `OpenPLC Project` | 64 | The copyright field. Some clients display this in an "About" dialog. |
| **Module Name** | Text | `OpenPLC` | 64 | The short module name. |

All fields apply on **blur**: values are saved as soon as the field loses focus.

## Why the Defaults Look Like a Real S7-300

The factory defaults are deliberately chosen to match a Siemens **CPU 315-2 PN/DP** (an S7-300 with built-in Profinet). This is the most permissive identity we can present:

- HMI engines that filter by CPU family ("S7-300", "S7-1200", "S7-1500", …) recognise it as a 300-series controller.
- Older engineering tools that only know S7-300/400 still connect.
- Newer tools that handle S7-1200/1500 still connect because S7-300 compatibility is a baseline expectation.

If you are integrating with a tool that explicitly rejects unknown CPU types, leave these defaults alone. Your HMI will believe it is talking to an S7-300 with a serial number of `S C-OPENPLC01`.

## When to Customise

Most users never change these values. You should consider customising the identity when:

- **You operate a fleet of OpenPLC runtimes.** Setting a unique `Serial Number` per device makes them easy to distinguish in HMI device lists and asset registers.
- **Your monitoring system displays the `PLC Name` field on dashboards.** Use a meaningful site/equipment name (`Pump Station 4 PLC`) instead of the default.
- **You want to replicate the identity of a specific Siemens controller** that a third-party tool already trusts. Match the `Module Type` and `Module Name` to the original device's strings.

## Character Limit

Each field is capped at **64 characters**. The input prevents you from typing more. The editor will silently stop accepting characters once the limit is reached. Keep strings short; some legacy clients truncate display fields at 16 or 24 characters.

## What's Next?

- **[Logging](logging)**: Decide what to record about client interactions
- **[Troubleshooting](troubleshooting)**: Resolve identity-related connection issues
- **[S7Comm Server Overview](README)**: Return to the protocol overview
