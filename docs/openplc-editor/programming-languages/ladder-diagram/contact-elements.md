# Contact Elements

Contacts are the input elements of a Ladder Diagram rung. They read Boolean variables and either pass power (TRUE) or block it (FALSE) based on the variable's value and the contact type. The Autonomy Edge IDE supports four contact types, each serving a different logical purpose.

## Contact Types Overview

| Type | Symbol | Passes Power When... |
|------|--------|---------------------|
| Normally Open (NO) | `--[ ]--` | Variable is TRUE |
| Normally Closed (NC) | `--[/]--` | Variable is FALSE |
| Rising Edge (P) | `--[P]--` | Variable transitions FALSE → TRUE |
| Falling Edge (N) | `--[N]--` | Variable transitions TRUE → FALSE |

All contacts require a `BOOL` variable. If you assign a non-BOOL variable or an undefined name, the contact is highlighted in red to indicate an error.

## Normally Open Contact (NO)

The Normally Open contact is the most common contact type. It acts like a switch that is "open" (blocking current) when its variable is FALSE and "closed" (passing current) when its variable is TRUE.

**Behavior:**
- Variable = TRUE → power passes through → downstream elements are energized
- Variable = FALSE → power is blocked → downstream elements are not energized

**Use case:** Testing whether an input is active, a button is pressed, or a condition is met.

**Example — Start button controls a motor:**

<ladder-diagram src="/docs/diagrams/ladder/contact-no-start.json"></ladder-diagram>

When `start_button` is TRUE, power flows through and `motor_run` becomes TRUE.

**Electrical analogy:** A pushbutton that is normally disconnected. Pressing it closes the circuit.

## Normally Closed Contact (NC)

The Normally Closed contact is the inverse of the Normally Open contact. It passes power when its variable is FALSE and blocks power when TRUE.

**Behavior:**
- Variable = FALSE → power passes through
- Variable = TRUE → power is blocked

**Use case:** Implementing NOT logic, safety interlocks, and emergency stop conditions.

**Example — Emergency stop circuit:**

<ladder-diagram src="/docs/diagrams/ladder/contact-nc-estop.json"></ladder-diagram>

`system_enabled` is TRUE as long as `e_stop` is FALSE. When `e_stop` goes TRUE (button pressed), power is blocked and `system_enabled` goes FALSE.

**Electrical analogy:** A pushbutton that is normally connected. Pressing it opens (breaks) the circuit.

**Example — Safety interlock:**

<ladder-diagram src="/docs/diagrams/ladder/contact-nc-interlock.json"></ladder-diagram>

The motor can only start when the safety guard is closed (`guard_open` = FALSE) AND `motor_ready` is TRUE.

## Rising Edge Contact (P)

The Rising Edge contact detects the transition of a variable from FALSE to TRUE. It passes power for exactly **one scan cycle** at the moment of transition, then blocks power on subsequent scans — even if the variable remains TRUE.

**Behavior:**
- Variable transitions FALSE → TRUE → power passes for one scan
- Variable stays TRUE → power is blocked (no longer a transition)
- Variable is FALSE → power is blocked
- Variable transitions TRUE → FALSE → power is blocked (that's a falling edge)

**Use case:** Counting events, triggering one-shot actions, detecting button presses without continuous activation.

**Example — Count button presses:**

<ladder-diagram src="/docs/diagrams/ladder/contact-rising-edge.json"></ladder-diagram>

Each press of `count_button` produces a single pulse on `increment_pulse`. Holding the button does not produce repeated pulses.

> **Tip:** Rising edge detection compares the current variable value with its value from the previous scan. The runtime tracks this automatically for each rising edge contact.

## Falling Edge Contact (N)

The Falling Edge contact detects the transition of a variable from TRUE to FALSE. It passes power for exactly **one scan cycle** at the moment the variable goes from TRUE to FALSE.

**Behavior:**
- Variable transitions TRUE → FALSE → power passes for one scan
- Variable stays FALSE → power is blocked
- Variable is TRUE → power is blocked (waiting for the transition)
- Variable transitions FALSE → TRUE → power is blocked (that's a rising edge)

**Use case:** Detecting release events, triggering actions when a process ends, counting deactivation events.

**Example — Detect button release:**

<ladder-diagram src="/docs/diagrams/ladder/contact-falling-edge.json"></ladder-diagram>

`released_pulse` goes TRUE for one scan when `start_button` is released (transitions from TRUE to FALSE).

## Combining Contact Types

You can freely mix different contact types on the same rung. This allows expressive Boolean logic:

### AND with Negation

<ladder-diagram src="/docs/diagrams/ladder/contact-and-negation.json"></ladder-diagram>

`output` = `sensor_a` AND (NOT `sensor_b`).

### OR with Edge Detection

<ladder-diagram src="/docs/diagrams/ladder/contact-or-edge.json"></ladder-diagram>

`trigger` fires for one scan when either `pulse_1` or `pulse_2` has a rising edge.

### Complex Interlock

<ladder-diagram src="/docs/diagrams/ladder/contact-complex-interlock.json"></ladder-diagram>

`run` = `enable` AND (NOT `fault`) AND `ready`. This pattern is standard for motor interlocks: the system must be enabled, free of faults, and in a ready state before a run command is issued.

## Changing Contact Type in the IDE

To change a contact's type after placing it:

1. Double-click the contact element on the rung.
2. A dialog appears with four options: **Default** (NO), **Negated** (NC), **Rising Edge** (P), **Falling Edge** (N).
3. Click the desired type.
4. The contact's visual symbol updates immediately.

The variable assignment is preserved when you change the contact type.

## Variable Assignment

Each contact must be assigned a BOOL variable:

1. Click the variable name area above the contact.
2. Type the variable name. Autocomplete shows matching BOOL variables from the Variables Table.
3. Press **Enter** or click a suggestion to confirm.

If the name doesn't match a defined BOOL variable, the contact turns red. This is a visual error indicator — fix it by correcting the variable name or adding the missing variable to the Variables Table.

---

## What's Next?

Learn about the output side of the rung: [Coil Elements](coil-elements).
