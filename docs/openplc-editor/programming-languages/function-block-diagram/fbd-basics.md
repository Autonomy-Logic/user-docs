# FBD Language Basics

Function Block Diagram (FBD) is a graphical programming language defined in the IEC 61131-3 standard. Unlike Ladder Diagram's relay-circuit metaphor, FBD uses a data-flow model: signals flow from left to right through interconnected blocks, with each block performing an operation on its inputs and producing outputs. FBD is the natural choice when your program's logic is best expressed as a flow of data transformations.

## Why Function Block Diagram?

FBD excels in scenarios where you think about your program as a signal processing chain:

- **Control loops**: PID controllers, filters, and regulators where sensor data flows through processing stages to produce actuator commands.
- **Math-heavy logic**: Calculations involving multiple operations chained together.
- **Signal routing**: Selecting, multiplexing, and conditioning analog values.
- **Complex Boolean logic**: When AND/OR/NOT relationships have many inputs and nested structure.

FBD is visual like LD but operates on any data type, not just Boolean. It's the preferred language for continuous process control (temperature, pressure, flow) where analog values dominate.

## Core Concepts

### Blocks

A **block** is the fundamental element in FBD. Each block represents a function or function block:

- **Input pins** on the left side receive values.
- **Output pins** on the right side produce results.
- **The block name** (displayed inside) identifies the operation (e.g., `ADD`, `TON`, `GT`, `MUX`).

Blocks come from two sources:
- **System library**: Standard IEC functions and function blocks (arithmetic, comparison, timers, counters, bistable, edge detectors, etc.)
- **User library**: Custom function blocks and functions you've defined in your project

### Connections

Connections are lines (wires) drawn from an output pin of one block to an input pin of another. They carry data. A Boolean, integer, real number, time value, or any IEC data type.

Connections always flow **left to right**. You can't create feedback loops directly within a single FBD diagram. Use variables to carry values between scan cycles for feedback.

### Variables

Variables in FBD appear as named nodes connected to block pins:

- **Input variables** connect to the left side of blocks, providing values.
- **Output variables** connect to the right side of blocks, storing results.

All variables must be defined in the Variables Table before use. The IDE provides autocomplete when assigning variables to pins.

### Connectors and Continuations

For complex diagrams that would need very long connection lines, FBD supports **connectors** and **continuations**:

- A **connector** marks the end of a signal at one point in the diagram.
- A **continuation** picks up the same signal at a different location.

These act as named "jumper wires" that keep the diagram clean.

### Comments

You can add comment nodes to the FBD diagram to annotate and explain your logic. Comments are purely visual and don't affect execution.

## How FBD Executes

The runtime evaluates an FBD diagram by determining the data dependencies between blocks:

1. Blocks with no input dependencies (connected only to input variables) are evaluated first.
2. Blocks that depend on the outputs of already-evaluated blocks are evaluated next.
3. This continues until all blocks have been evaluated.
4. Output variables are written with the final computed values.

Within a single scan cycle, the entire FBD diagram is evaluated once. The order is determined by data flow. A block can't execute until all its inputs are available.

## FBD vs. Ladder Diagram

| Aspect | Function Block Diagram | Ladder Diagram |
|--------|----------------------|----------------|
| Metaphor | Data flow / signal processing | Electrical relay circuits |
| Data types | Any (BOOL, INT, REAL, TIME, etc.) | Primarily BOOL |
| Best for | Analog processing, control loops, math | Discrete logic, interlocking, Boolean |
| Structure | Free-form blocks and wires | Horizontal rungs with rails |
| Visual style | Block-and-wire diagram | Relay ladder diagram |

## The FBD Editor in Autonomy Edge

The Autonomy Edge IDE provides a visual editor for FBD. Key features:

- **Single canvas**: Unlike LD's multiple rungs, FBD uses a single continuous canvas containing all elements.
- **Block placement**: Drag blocks from the system and user libraries onto the canvas.
- **Variable nodes**: Input and output variables appear as separate nodes connected to block pins.
- **Autocomplete**: When assigning variables to pins, the editor provides autocomplete from the Variables Table, filtered by compatible data type.
- **Drag and drop**: Drag function blocks from the Library panel directly onto the FBD canvas.
- **Connection drawing**: Click on an output handle and drag to an input handle to create a wire.

### Placing Blocks

1. Drag a block from the Library panel onto the FBD canvas, or click a placeholder node.
2. The block appears with its input and output pins.
3. Assign variables to each pin using the autocomplete fields.
4. Draw connections from output pins to input pins of other blocks.

### Connecting Blocks

To connect two blocks:

1. Hover over an output pin. The handle becomes visible.
2. Click and drag from the output handle.
3. Release on an input handle of the target block.
4. A connection line appears between the two pins.

The editor validates data type compatibility. Connecting incompatible types (e.g., a BOOL output to an INT input) shows a visual error.

## Common FBD Patterns

### Arithmetic Chain

Chain ADD and MUL blocks to compute a weighted sum:

<fbd-diagram src="/docs/diagrams/fbd/fbd-basics-arithmetic-chain.json"></fbd-diagram>

The ADD block sums `sensor1` and `sensor2`, then the MUL block multiplies the result by `gain`.

### Comparison with Action

Use a GT (greater than) block to drive a Boolean output:

<fbd-diagram src="/docs/diagrams/fbd/fbd-basics-gt-comparison.json"></fbd-diagram>

If `temperature > threshold`, `alarm` becomes TRUE.

### Timer with Enable

Place a TON block with an enable condition:

<fbd-diagram src="/docs/diagrams/fbd/fbd-basics-ton-timer.json"></fbd-diagram>

The timer starts when `enable_signal` is TRUE and fires `delayed_output` after 5 seconds.

### Selector Logic

Use a SEL (selector) block to choose between two values based on a condition:

<fbd-diagram src="/docs/diagrams/fbd/fbd-basics-sel-selector.json"></fbd-diagram>

When `manual_mode` is TRUE, `output_speed` gets `manual_speed`. When FALSE, it gets `auto_speed`.

---

## What's Next?

See practical examples of FBD programming: [FBD Examples](fbd-examples).
