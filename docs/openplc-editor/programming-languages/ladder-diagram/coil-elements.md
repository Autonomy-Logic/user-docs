# Coil Elements

Coils are the output elements of a Ladder Diagram rung. They receive the power state from the rung's logic (the result of evaluating all contacts and blocks) and write a Boolean value to their assigned variable. The Autonomy Edge IDE supports six coil types, covering standard outputs, latching, and edge-triggered behavior.

## Coil Types Overview

| Type | Symbol | Behavior |
|------|--------|----------|
| Regular | `--( )--` | Writes the rung's power state to the variable |
| Negated | `--(/)--` | Writes the inverse of the rung's power state |
| Set (Latch) | `--(S)--` | Sets the variable to TRUE when energized; does not affect it otherwise |
| Reset (Unlatch) | `--(R)--` | Sets the variable to FALSE when energized; does not affect it otherwise |
| Rising Edge | `--(P)--` | Sets the variable TRUE for one scan on a rising power edge |
| Falling Edge | `--(N)--` | Sets the variable TRUE for one scan on a falling power edge |

All coils require a `BOOL` variable. Assigning a non-BOOL variable or an undefined name highlights the coil in red.

## Regular Coil

The Regular coil is the most common output type. It directly reflects the power state of the rung:

- Rung is energized (power reaches the coil) → variable is set to **TRUE**
- Rung is de-energized (power does not reach the coil) → variable is set to **FALSE**

**Key characteristic:** The variable is updated every scan cycle. It follows the rung state in real time.

**Example. Direct output:**

<ladder-diagram src="/docs/diagrams/ladder/coil-regular.json"></ladder-diagram>

`alarm_light` mirrors `sensor_active`. When the sensor is active, the light is on. When the sensor is inactive, the light is off.

**Example. AND logic with regular coil:**

<ladder-diagram src="/docs/diagrams/ladder/coil-regular-and.json"></ladder-diagram>

`motor_run` is TRUE only when both conditions are met simultaneously.

## Negated Coil

The Negated coil writes the **inverse** of the rung's power state:

- Rung is energized → variable is set to **FALSE**
- Rung is de-energized → variable is set to **TRUE**

**Use case:** Creating inverted outputs without needing a separate rung with a normally closed contact.

**Example. Inverted status:**

<ladder-diagram src="/docs/diagrams/ladder/coil-negated.json"></ladder-diagram>

`system_ok` is TRUE when `system_fault` is FALSE, and vice versa. This is equivalent to:

<ladder-diagram src="/docs/diagrams/ladder/coil-negated-alt.json"></ladder-diagram>

Both approaches produce the same result. The negated coil approach is more compact.

## Set Coil (Latch)

The Set coil is a **latching** output. When the rung is energized, it sets the variable to TRUE and **leaves it there**. When the rung is de-energized, the coil does nothing. The variable retains its current value.

- Rung energized → variable = **TRUE**
- Rung de-energized → variable **unchanged** (stays at its current value)

**Key characteristic:** Once set, the variable stays TRUE until explicitly reset by a Reset coil or by other logic.

**Use case:** Latch/unlatch pairs for motor control, alarm memory, and any situation where you need to "remember" that a condition occurred.

**Example. Latching motor start:**

<ladder-diagram src="/docs/diagrams/ladder/coil-set-motor.json"></ladder-diagram>

<ladder-diagram src="/docs/diagrams/ladder/coil-reset-motor.json"></ladder-diagram>

Pressing `start_button` latches `motor` to TRUE. It stays TRUE even after `start_button` is released. Pressing `stop_button` resets `motor` to FALSE.

## Reset Coil (Unlatch)

The Reset coil is the counterpart to the Set coil. When the rung is energized, it forces the variable to FALSE. When de-energized, it does nothing.

- Rung energized → variable = **FALSE**
- Rung de-energized → variable **unchanged**

**Use case:** Always paired with a Set coil to create a latch/unlatch circuit.

**Example. Emergency stop with latch/unlatch:**

<ladder-diagram src="/docs/diagrams/ladder/coil-reset-estop-set.json"></ladder-diagram>

<ladder-diagram src="/docs/diagrams/ladder/coil-reset-estop-r1.json"></ladder-diagram>

<ladder-diagram src="/docs/diagrams/ladder/coil-reset-estop-r2.json"></ladder-diagram>

`running` is latched TRUE when `run_command` is active and no `fault` exists. It is reset (unlatched) by either `e_stop` or `fault`.

### Set/Reset Priority

When a Set and a Reset for the same variable are both energized in the same scan, the **last one evaluated wins** (since rungs execute top to bottom). In the example above, if both `run_command` and `e_stop` are TRUE simultaneously, the Reset in Rung 2 executes after the Set in Rung 1, so `running` ends up FALSE. This is the desired "stop has priority" behavior. To get "start has priority," place the Set rung below the Reset rung.

## Rising Edge Coil

The Rising Edge coil produces a single-scan pulse when the rung transitions from de-energized to energized.

- Rung transitions from de-energized to energized → variable = **TRUE** for one scan
- All other conditions → variable = **FALSE**

**Use case:** Generating trigger pulses from sustained conditions, one-shot event signaling.

**Example. One-shot pulse from level signal:**

<ladder-diagram src="/docs/diagrams/ladder/coil-rising-edge.json"></ladder-diagram>

`notify_pulse` goes TRUE for exactly one scan when `process_complete` transitions to TRUE. Even if `process_complete` stays TRUE for many scans, `notify_pulse` is only TRUE once.

## Falling Edge Coil

The Falling Edge coil produces a single-scan pulse when the rung transitions from energized to de-energized.

- Rung transitions from energized to de-energized → variable = **TRUE** for one scan
- All other conditions → variable = **FALSE**

**Use case:** Detecting when a process ends, counting deactivation events.

**Example. Detect process end:**

<ladder-diagram src="/docs/diagrams/ladder/coil-falling-edge.json"></ladder-diagram>

`cycle_ended` pulses TRUE for one scan when `cycle_active` drops from TRUE to FALSE.

## Changing Coil Type in the IDE

To change a coil's type:

1. Double-click the coil element on the rung.
2. A dialog appears with six options: **Default**, **Negated**, **Set**, **Reset**, **Rising Edge**, **Falling Edge**.
3. Select the desired type.
4. The coil's visual symbol updates immediately.

The variable assignment is preserved when you change types.

## Multiple Coils on a Rung

A single rung can drive multiple coils:

<ladder-diagram src="/docs/diagrams/ladder/coil-multiple.json"></ladder-diagram>

Both `output_1` and `output_2` receive the same power state. However, for clarity, it's usually better to use separate rungs or have a single output per rung.

---

## What's Next?

Learn how to use function blocks within ladder rungs: [Function Blocks in LD](function-blocks-ld).
