# LD Language Basics

Ladder Diagram (LD) is a graphical programming language defined in the IEC 61131-3 standard. It represents logic using a visual metaphor borrowed from electrical relay circuits: power flows from left to right across "rungs" of a virtual ladder, passing through contacts (conditions) and energizing coils (outputs). LD is the most widely used PLC language in manufacturing and discrete control.

## Why Ladder Diagram?

LD was designed to look like the relay logic diagrams that electricians and controls engineers have used for decades. If you have an electrical background, you can often "read" an LD program by tracing current flow, just like you would trace a wiring diagram.

Key strengths of LD:

- **Visual and intuitive**: Logic is immediately visible in the diagram structure.
- **Great for Boolean logic**: AND, OR, NOT, latching, and edge detection are trivially expressed.
- **Self-documenting**: The graphical layout reveals the logical relationships between inputs and outputs.
- **Familiar**: The most commonly understood PLC language worldwide.

LD is ideal for discrete control: conveyors, motor start/stop, interlocking, safety logic, and simple sequencing. For complex math, string processing, or data manipulation, consider [Structured Text](../structured-text/st-basics) instead.

## Core Concepts

### Power Rails

Every rung starts at the **left power rail** and ends at the **right power rail**. These represent the power supply in the relay circuit metaphor:

- **Left Power Rail**: Represents the "live" side. Power originates here.
- **Right Power Rail**: Represents the "neutral" side. Power terminates here.

In the IDE, power rails appear as vertical bars at the left and right edges of each rung.

### Rungs

A **rung** is a horizontal circuit connecting the left rail to the right rail. Each rung typically evaluates one logical condition and drives one or more outputs.

A simple rung might look like this:

<ladder-diagram src="/docs/diagrams/ladder/basic-contact-coil.json"></ladder-diagram>

This reads: "If `start_btn` is TRUE, then `motor_on` is TRUE."

The IDE displays rungs vertically stacked within the LD editor, each numbered for reference. You can add new rungs, reorder them by dragging, and delete them.

### Contacts

**Contacts** sit on the left side of a rung and represent input conditions. They test Boolean variable values. A contact either passes power (the condition is met) or blocks it (the condition is not met).

| Contact Type | Symbol | Behavior |
|-------------|--------|----------|
| Normally Open (NO) | `--[ ]--` | Passes power when the variable is TRUE |
| Normally Closed (NC) | `--[/]--` | Passes power when the variable is FALSE |
| Rising Edge (P) | `--[P]--` | Passes power for one scan when the variable transitions FALSE → TRUE |
| Falling Edge (N) | `--[N]--` | Passes power for one scan when the variable transitions TRUE → FALSE |

For detailed coverage of each contact type, see [Contact Elements](contact-elements).

### Coils

**Coils** sit on the right side of a rung and represent outputs. They store the result of the rung's logic evaluation into a Boolean variable.

| Coil Type | Symbol | Behavior |
|-----------|--------|----------|
| Regular | `--( )--` | Sets the variable to the current power state of the rung |
| Negated | `--(/)--` | Sets the variable to the inverse of the rung's power state |
| Set (Latch) | `--(S)--` | Sets the variable to TRUE when energized; never resets it |
| Reset (Unlatch) | `--(R)--` | Sets the variable to FALSE when energized; never sets it |
| Rising Edge | `--(P)--` | Sets the variable TRUE for one scan on a rising edge |
| Falling Edge | `--(N)--` | Sets the variable TRUE for one scan on a falling edge |

For detailed coverage of each coil type, see [Coil Elements](coil-elements).

### Function Blocks

LD isn't limited to contacts and coils. You can place **function blocks** (timers, counters, math operations, custom blocks) inline on a rung. Function blocks receive inputs from the left and produce outputs to the right, integrating seamlessly with the contact/coil flow.

For details, see [Function Blocks in LD](function-blocks-ld).

## Logic Patterns

### AND Logic (Series Contacts)

Place contacts in series (one after another on the same rung) to create AND logic. Power flows through only if **all** contacts pass:

<ladder-diagram src="/docs/diagrams/ladder/and-logic.json"></ladder-diagram>

`alarm` is TRUE only when **both** `sensor_A` AND `sensor_B` are TRUE.

### OR Logic (Parallel Contacts)

Use parallel branches to create OR logic. Power flows if **any** branch passes:

<ladder-diagram src="/docs/diagrams/ladder/or-logic.json"></ladder-diagram>

`light` is TRUE when `button_1` OR `button_2` (or both) is TRUE.

In the IDE, you create parallel branches by adding a contact to a parallel path, visually stacking the two branches vertically.

### NOT Logic (Negated Contact)

Use a Normally Closed (NC) contact to invert a condition:

<ladder-diagram src="/docs/diagrams/ladder/not-logic.json"></ladder-diagram>

`system_ok` is TRUE when `error` is FALSE.

### Latch / Unlatch (Set / Reset)

A common pattern uses two rungs to create a latching output:

<ladder-diagram src="/docs/diagrams/ladder/latch-set.json"></ladder-diagram>

<ladder-diagram src="/docs/diagrams/ladder/latch-reset.json"></ladder-diagram>

- Pressing `start_btn` latches `motor_on` to TRUE.
- Pressing `stop_btn` resets `motor_on` to FALSE.
- `motor_on` retains its state between scan cycles.

### Self-Holding Circuit (Seal-In)

An alternative to Set/Reset coils that keeps an output energized after a momentary input:

<ladder-diagram src="/docs/diagrams/ladder/seal-in.json"></ladder-diagram>

When `start_btn` is pressed, `motor_on` goes TRUE. The parallel `motor_on` contact "seals in" the circuit. Power continues to flow through `motor_on` even after `start_btn` is released. Pressing `stop_btn` (normally closed) breaks the circuit.

## Execution Order

LD programs execute top to bottom, rung by rung. Within each rung, evaluation proceeds left to right:

1. The runtime evaluates Rung 1 (all contacts and blocks from left to right), then writes the coil outputs.
2. It moves to Rung 2 and repeats the process.
3. This continues through all rungs in the program.
4. After the last rung, the cycle is complete and the runtime waits for the next task trigger.

> **Tip:** If Rung 5 reads a variable that Rung 3 writes, the value used by Rung 5 is the one written by Rung 3 in the **current** scan, not the previous one. Keep this in mind when designing logic with dependencies between rungs.

## Variables in Ladder Diagram

All contacts and coils must be bound to Boolean variables (`BOOL` type). You define these in the Variables Table above the graphical editor:

- **Contacts** read from Boolean variables (input conditions).
- **Coils** write to Boolean variables (output results).
- **Function blocks** can use any data type for their parameters.

If a contact or coil references a variable that doesn't exist in the Variables Table, or references a non-BOOL variable, the IDE highlights it in red as an error.

### Variable Naming

When you place a contact or coil, you assign it a variable by typing the name directly above the element. The IDE provides autocomplete. As you type, matching variable names from the table appear in a dropdown.

## Comparison with Other Languages

| Feature | Ladder Diagram | Structured Text |
|---------|---------------|----------------|
| Visual representation | Yes (graphical) | No (textual) |
| Best for | Boolean logic, discrete control | Math, algorithms, data processing |
| Learning curve | Low for electricians | Low for programmers |
| Complex math | Requires function blocks | Native support |
| Readability at scale | Degrades with complexity | Scales well |

> **Tip:** Most real projects use LD for the main control logic and ST for calculations and complex algorithms, calling ST functions from within LD rungs via function blocks.

---

## What's Next?

Learn how to use the LD visual editor in the IDE: [LD Editor](ld-editor).
