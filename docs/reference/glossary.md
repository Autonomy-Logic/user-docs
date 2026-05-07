# Glossary

Key terms used throughout the Autonomy Edge platform and IEC 61131-3 PLC programming documentation.

---

## A

### Analog Input
An input signal that represents a continuous range of values (e.g., 0–10V, 4–20mA) rather than a discrete ON/OFF state. Mapped to `%IW` (input word) addresses in IEC 61131-3. Commonly used for sensors measuring temperature, pressure, level, and flow.

### Analog Output
An output signal that drives a continuous value (e.g., 0–10V, 4–20mA) to an actuator. Mapped to `%QW` (output word) addresses. Used for controlling variable-speed drives, proportional valves, and other modulating devices.

---

## B

### BOOL
The most basic IEC 61131-3 data type. Represents a single binary value: `TRUE` (1) or `FALSE` (0). Used for digital inputs, outputs, flags, and control signals.

---

## C

### Coil
In Ladder Diagram, a coil is an output element placed at the right side of a rung. When the rung logic evaluates to TRUE, the coil is energized (sets its associated BOOL variable to TRUE). Variants include normal coils, negated coils, set coils, and reset coils.

### Configuration
The top-level organizational element in IEC 61131-3. A configuration defines the runtime environment, contains one or more Resources, and specifies global variables. In Autonomy Edge, each project has one configuration.

### Contact
In Ladder Diagram, a contact is an input element placed on a rung. It reads the value of a BOOL variable. Normally-open contacts pass power when TRUE; normally-closed contacts pass power when FALSE.

### Counter
A standard function block that counts events. IEC 61131-3 defines three counters: CTU (count up), CTD (count down), and CTUD (count up/down). See [Counter Function Blocks](../openplc-editor/standard-function-blocks/counter-blocks).

---

## D

### Data Type
The classification of a variable that determines its range, precision, and allowed operations. IEC 61131-3 defines elementary types (BOOL, INT, REAL, STRING, TIME) and allows user-defined types. See [Data Types Reference](data-types).

### Digital Input
A binary input signal that is either ON or OFF. Mapped to `%IX` (input bit) addresses. Used for switches, buttons, proximity sensors, and limit switches.

### Digital Output
A binary output signal that drives a load ON or OFF. Mapped to `%QX` (output bit) addresses. Used for relays, contactors, solenoid valves, and indicator lights.

---

## E

### Edge Detection
The process of detecting a transition in a boolean signal. A rising edge (R_TRIG) detects the FALSE-to-TRUE transition. A falling edge (F_TRIG) detects the TRUE-to-FALSE transition. Edge detection is essential for triggering actions on signal changes rather than signal levels.

---

## F

### FBD (Function Block Diagram)
One of the five IEC 61131-3 programming languages. FBD uses graphical blocks connected by wires to represent logic flow. Each block performs a function and passes results to connected blocks. Well-suited for data flow and signal processing applications.

### Function (FC)
A POU that performs a computation and returns a single value. Functions are stateless — they produce the same output for the same inputs every time. Examples: `ABS()`, `SQRT()`, `MAX()`, type conversion functions.

### Function Block (FB)
A POU that encapsulates logic with internal state. Unlike Functions, Function Blocks retain their variable values between scan cycles. Each use requires a named instance. Examples: TON (timer), CTU (counter), PID controllers. Function Blocks are the primary mechanism for code reuse in IEC 61131-3.

---

## G

### Global Variable
A variable declared with `VAR_GLOBAL` scope that is accessible from multiple POUs within the same configuration. Use global variables sparingly for data that genuinely needs to be shared (e.g., system mode, emergency stop status).

### GPIO (General-Purpose Input/Output)
Physical pins on a hardware platform that can be configured as digital inputs or outputs. Platforms like Raspberry Pi provide GPIO pins that the OpenPLC Runtime can use through the HAL.

---

## H

### HAL (Hardware Abstraction Layer)
The layer in OpenPLC Runtime that maps IEC 61131-3 located variable addresses (`%I`, `%Q`) to physical hardware pins. The HAL configuration is defined in a `hals.json` file and allows the same PLC program to run on different hardware platforms.

### Heartbeat
A periodic status check sent by the orchestrator to the Autonomy Edge cloud. The heartbeat confirms the orchestrator is online and healthy, and includes basic system metrics like CPU usage, memory, and uptime.

---

## I

### I/O Image Table
An in-memory buffer that holds the current state of all inputs and outputs. At the start of each scan cycle, physical inputs are read into the input image table. At the end, the output image table is written to physical outputs. This ensures consistent I/O within a single scan.

### IEC 61131-3
The international standard for programmable logic controller (PLC) programming. It defines five programming languages (ST, LD, FBD, IL, SFC), data types, program organization units, and a common execution model. Autonomy Edge supports ST, LD, FBD, and IL.

### Instance
A named copy of a Function Block. Each instance has its own set of internal variables and maintains its own state. For example, declaring `Timer1 : TON;` creates an instance of the TON function block named `Timer1`.

---

## L

### LD (Ladder Diagram)
One of the five IEC 61131-3 programming languages. LD resembles electrical relay logic diagrams with power rails, contacts (inputs), and coils (outputs). It is the most widely used PLC language, particularly for discrete control applications.

### Located Variable
A variable that is bound to a specific physical or logical address in the I/O image table. The address format is `%<type><size><byte>.<bit>`, for example: `%IX0.0` (digital input, byte 0, bit 0), `%QW2` (analog output, word 2).

---

## M

### Modbus
An industrial communication protocol widely used for connecting PLCs to sensors, actuators, and other devices. Modbus TCP operates over Ethernet. The OpenPLC Runtime supports both Modbus client (master) and Modbus server (slave) modes.

---

## O

### OPC-UA
An industrial communication standard (Open Platform Communications Unified Architecture) for secure, reliable data exchange. The OpenPLC Runtime supports OPC-UA through a plugin for connecting to OPC-UA servers.

### Orchestrator
A software agent that runs on your edge hardware (e.g., Raspberry Pi, industrial gateway) and manages vPLCs. The orchestrator connects securely to the Autonomy Edge cloud, receives commands, deploys programs, and reports status. Install with `curl https://getedge.me | bash`.

---

## P

### PLC (Programmable Logic Controller)
A ruggedized computer designed for industrial control applications. PLCs execute cyclic scan programs that read inputs, process logic, and write outputs in a deterministic loop. Autonomy Edge virtualizes PLCs as vPLCs running on edge hardware.

### Plugin
An extension module for the OpenPLC Runtime that provides additional functionality. Plugins can be written in Python (for protocols, APIs, custom logic) or C/C++ (for high-performance, real-time I/O). Built-in plugins include Modbus, OPC-UA, and S7Comm drivers.

### POU (Program Organization Unit)
The building block of IEC 61131-3 programs. There are three types: Programs (top-level executable units assigned to tasks), Function Blocks (reusable stateful components), and Functions (stateless computations). See [POUs](../openplc-editor/iec-concepts/pous).

### Program
A POU type that serves as the top-level executable unit. Programs are assigned to tasks for execution. They can instantiate Function Blocks and call Functions. Each task executes one or more Programs at its configured interval.

---

## R

### Resource
An IEC 61131-3 organizational element within a Configuration. A Resource represents a processing unit (CPU) and contains task definitions and program instances. In Autonomy Edge, each configuration typically has one Resource.

### Rung
A single row in a Ladder Diagram, connecting the left power rail to the right power rail through contacts and coils. Each rung represents one logical statement.

### Runtime
The OpenPLC Runtime software that executes compiled PLC programs. The runtime manages the scan cycle, I/O image tables, plugin loading, and communication protocols. In Autonomy Edge, the runtime powers each vPLC.

---

## S

### S7Comm
A Siemens proprietary communication protocol used by S7 series PLCs. The OpenPLC Runtime supports S7Comm through a native plugin, enabling communication with Siemens equipment.

### Scan Cycle
The fundamental execution loop of a PLC program: read inputs → execute logic → write outputs. One complete pass through this loop is one scan cycle. The time to complete one cycle is the scan time. The configured interval between cycles is the scan period (task period).

### ST (Structured Text)
One of the five IEC 61131-3 programming languages. ST is a high-level text-based language with Pascal-like syntax. It supports variables, expressions, control flow (IF, CASE, FOR, WHILE), and function calls. See [ST Language Basics](../openplc-editor/programming-languages/structured-text/st-basics).

---

## T

### Task
An execution unit in IEC 61131-3 that defines when and how often Programs run. Tasks have a type (cyclic or event-driven) and a period (e.g., 50 ms). Programs are assigned to tasks, and the runtime executes each task's programs at the configured interval.

### Timer
A standard function block that introduces time-based behavior. IEC 61131-3 defines three timers: TON (on-delay), TOF (off-delay), and TP (pulse). See [Timer Function Blocks](../openplc-editor/standard-function-blocks/timer-blocks).

---

## V

### Variable
A named storage location for data in a PLC program. Variables have a name, a data type, and a class (Local, Input, Output, InOut, External, Global, Temp). They are declared in the Variables Table of each POU.

### vPLC (Virtual PLC)
A software-based PLC running the OpenPLC Runtime on edge hardware, managed by an orchestrator. Instead of dedicated PLC hardware, vPLCs run as isolated processes on Linux devices. They execute standard IEC 61131-3 programs and connect to physical I/O through Modbus, OPC-UA, or GPIO passthrough.

---

## W

### Watchdog
A safety mechanism in the OpenPLC Runtime that monitors whether the PLC program is completing scan cycles. If the program becomes unresponsive (e.g., stuck in an infinite loop), the watchdog triggers an error state and logs a warning.

## What's Next?

- [Data Types Reference](data-types) — Complete IEC 61131-3 data type details
- [IEC 61131-3 Keywords](iec-keywords) — Reserved keywords reference
- [FAQ](faq) — Common questions about Autonomy Edge
