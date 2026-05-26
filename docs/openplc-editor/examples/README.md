# Worked examples

End-to-end recipes that exercise the editor against a running PLC. Each one starts from a blank project and ends with the program executing on the **Simulator** (in-browser) or a real **vPLC** (orchestrator-managed).

- **[Blink](blink)**: the simplest possible LD program. A `BOOL` that toggles once a second. Demonstrates: LD bodies, timers, the Simulator.
- **[Motor start / stop with seal-in](start-stop-seal-in)**: the classic latching circuit. Demonstrates: parallel branches in LD, normally-closed contacts, the live-execution colouring.
- **[Modbus slave: expose digital outputs](modbus-slave-outputs)**: set up a Modbus TCP server on the vPLC and toggle `%QX0.0` from an external client. Demonstrates: Modbus server configuration, address mapping, the runtime's network bridge.
- **[OPC-UA: read a variable from UaExpert](opcua-read)**: expose a `REAL` to an OPC-UA address space and browse it from an external client. Demonstrates: OPC-UA tabs (general settings, address space, security profiles).
- **[Python function block: data transform](python-function-block)**: write a Python FB that scales an integer to a real, call it from an ST program. Demonstrates: Python authoring, the variables marshalling boundary, calling Python from IEC code.

Each example notes which surfaces it touches and links to the relevant reference pages.
