# Function Blocks in Ladder Diagram

While contacts and coils handle Boolean logic, many PLC applications need timers, counters, math operations, and custom processing. Function blocks bring this capability into Ladder Diagram by providing multi-input, multi-output processing elements that sit inline on a rung.

## What a Function Block Looks Like in LD

A function block appears as a rectangular box placed on a rung between contacts and coils. It has:

- **Input pins** on the left side. Values fed into the block
- **Output pins** on the right side. Results produced by the block
- **A name label** showing the block type (e.g., `TON`, `CTU`, `ADD`)
- **Variable connections** for each pin, linking to your POU variables

The rung's power flow enters the block from the left, passes through its logic, and continues out the right side. This means you can place contacts *before* a function block to control when it runs, and use its output pins to drive coils or feed into other blocks further along the rung.

## Placing a Function Block

To add a function block to a rung:

1. Click a placeholder position on the rung (the small circular target nodes between elements).
2. The block selection dialog opens. Browse the available blocks from two sources:
   - **System library**: Standard IEC 61131-3 function blocks (timers, counters, math, comparators, edge detectors, bistable blocks, etc.)
   - **User library**: Custom function blocks you've created in your project
3. Select a block. The editor inserts it at the chosen position with input pins on the left and output pins on the right.

## Connecting Variables to Pins

Each input and output pin on a function block has a variable field you need to fill in:

1. Click the variable area next to a pin.
2. Type a variable name from the Variables Table. Autocomplete filters by compatible data type.
3. Input pins accept any variable whose type matches the pin's expected type.
4. Output pins write their results to the assigned variable each scan cycle.

Make sure you've declared all the variables you need in the Variables Table before wiring them to pins. For function block types like `TON` or `CTU`, you also need a variable declared with that function block type to hold the block's internal state.

## Execution Control with EN/ENO

Some function blocks support `EN` (Enable) and `ENO` (Enable Out) pins:

- **EN** (input): When FALSE, the block does not execute. All outputs retain their previous values.
- **ENO** (output): Mirrors EN. TRUE when the block executed successfully, FALSE when skipped.

This gives you fine-grained control over when a block runs, independent of the rung's power flow.

## User-Defined Function Blocks

Any function block POU you create in your project appears in the user library. You place and wire it on a rung exactly like a standard block. The editor reads your block's variable definitions (inputs and outputs) and creates the corresponding pins automatically.

This lets you encapsulate complex logic. PID controllers, filters, custom algorithms written in ST or any other language. And reuse it visually in your Ladder Diagrams.

## Practical Example: Motor Start with Timer

Here's a common pattern that uses a TON timer to add a startup delay to a motor:

**Variables:**

| Name | Type | Class | Description |
|------|------|-------|-------------|
| `start_cmd` | BOOL | Local | Start command from operator |
| `e_stop` | BOOL | Local | Emergency stop (NC) |
| `delay_timer` | TON | Local | Startup delay timer instance |
| `motor_run` | BOOL | Local | Motor run output |

**Rung 1. Timer logic:**

<ladder-diagram src="/docs/diagrams/ladder/fb-ton-timer.json"></ladder-diagram>

**Rung 2. Motor output:**

<ladder-diagram src="/docs/diagrams/ladder/fb-ton-output.json"></ladder-diagram>

The `start_cmd` contact and `e_stop` normally-closed contact control rung power into the TON block. When both conditions are met, the timer starts counting. After 3 seconds, `delay_timer.Q` goes TRUE and energizes `motor_run` on the second rung.

## Standard Function Block Reference

For detailed documentation on each standard function block. Including pin tables, timing behavior, and examples. See the dedicated reference pages:

- [Timer Blocks](../../standard-function-blocks/timer-blocks): TON, TOF, TP
- [Counter Blocks](../../standard-function-blocks/counter-blocks): CTU, CTD, CTUD
- [Edge Detection Blocks](../../standard-function-blocks/edge-detection-blocks): R_TRIG, F_TRIG
- [Bistable Blocks](../../standard-function-blocks/bistable-blocks): SR, RS

---

## What's Next?

Explore other programming languages: [FBD Basics](../function-block-diagram/fbd-basics) for a fully graphical block-based approach, or [ST Basics](../structured-text/st-basics) for text-based programming.
