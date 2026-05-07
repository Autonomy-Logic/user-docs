# FBD Practical Examples

This section provides practical examples of Function Block Diagram programming patterns. These examples show how to combine standard and custom blocks to solve real-world control problems using the data-flow approach.

## Temperature Alarm System

This example uses comparison blocks and Boolean logic to generate alarms from a temperature sensor.

### Variables

| Name | Type | Class | Description |
|------|------|-------|-------------|
| `sensor_temp` | REAL | Local | Current temperature reading |
| `high_limit` | REAL | Local | High temperature threshold (e.g., 80.0) |
| `low_limit` | REAL | Local | Low temperature threshold (e.g., 5.0) |
| `high_alarm` | BOOL | Local | High temperature alarm |
| `low_alarm` | BOOL | Local | Low temperature alarm |
| `any_alarm` | BOOL | Local | Combined alarm output |

### FBD Structure

```
[sensor_temp] → [GT] → [high_alarm]
[high_limit]  →  ↑

[sensor_temp] → [LT] → [low_alarm]
[low_limit]   →  ↑

[high_alarm] → [OR] → [any_alarm]
[low_alarm]  →  ↑
```

### How It Works

1. The **GT** (Greater Than) block compares `sensor_temp` against `high_limit`. If the temperature exceeds the limit, `high_alarm` goes TRUE.
2. The **LT** (Less Than) block compares `sensor_temp` against `low_limit`. If the temperature drops below the limit, `low_alarm` goes TRUE.
3. The **OR** block combines both alarms. If either alarm is active, `any_alarm` is TRUE.

This pattern scales easily — add more comparison blocks for additional thresholds (warning levels, critical levels) and chain them with OR/AND blocks.

## Analog Signal Scaling

Industrial sensors often output raw values (e.g., 0–4095 from a 12-bit ADC) that need to be scaled to engineering units.

### Variables

| Name | Type | Class | Description |
|------|------|-------|-------------|
| `raw_input` | INT | Local | Raw ADC reading (0–4095) |
| `raw_real` | REAL | Local | Raw value converted to REAL |
| `scaled_value` | REAL | Local | Scaled output in engineering units |
| `raw_min` | REAL | Local | Minimum raw value (0.0) |
| `raw_max` | REAL | Local | Maximum raw value (4095.0) |
| `eng_min` | REAL | Local | Minimum engineering value (0.0) |
| `eng_max` | REAL | Local | Maximum engineering value (100.0) |
| `span_raw` | REAL | Local | Raw range |
| `span_eng` | REAL | Local | Engineering range |
| `normalized` | REAL | Local | Normalized 0.0–1.0 value |

### FBD Structure

The scaling formula is: `scaled = eng_min + ((raw - raw_min) / (raw_max - raw_min)) * (eng_max - eng_min)`

```
Step 1: Convert raw INT to REAL
[raw_input] → [INT_TO_REAL] → [raw_real]

Step 2: Calculate (raw - raw_min)
[raw_real] → [SUB] → [offset]
[raw_min]  →  ↑

Step 3: Calculate (raw_max - raw_min)
[raw_max] → [SUB] → [span_raw]
[raw_min] →  ↑

Step 4: Normalize to 0.0–1.0
[offset]   → [DIV] → [normalized]
[span_raw] →  ↑

Step 5: Calculate (eng_max - eng_min)
[eng_max] → [SUB] → [span_eng]
[eng_min] →  ↑

Step 6: Scale to engineering range
[normalized] → [MUL] → [scaled_offset]
[span_eng]   →  ↑

Step 7: Add engineering minimum
[scaled_offset] → [ADD] → [scaled_value]
[eng_min]       →  ↑
```

### How It Works

This example demonstrates FBD's strength: a multi-step mathematical calculation expressed as a clear left-to-right data flow. Each block performs one arithmetic operation, and the chain transforms a raw integer into a scaled real-number value.

## Timer-Based Pump Control

This example uses TON timers to implement a pump that must run for a minimum duration once started, with a cooldown period before it can restart.

### Variables

| Name | Type | Class | Description |
|------|------|-------|-------------|
| `start_cmd` | BOOL | Local | Operator start command |
| `stop_cmd` | BOOL | Local | Operator stop command |
| `pump_running` | BOOL | Local | Current pump state |
| `min_run_ok` | BOOL | Local | Minimum run time has elapsed |
| `cooldown_ok` | BOOL | Local | Cooldown period has elapsed |
| `can_start` | BOOL | Local | Starting is permitted |
| `can_stop` | BOOL | Local | Stopping is permitted |
| `run_timer` | TON | Local | Minimum run timer |
| `cooldown_timer` | TON | Local | Cooldown timer |

### FBD Structure

```
Minimum run timer:
[pump_running] → [TON: run_timer, PT=T#30s] → [min_run_ok]

Cooldown timer:
[NOT pump_running] → [TON: cooldown_timer, PT=T#60s] → [cooldown_ok]

Start permission:
[start_cmd]   → [AND] → [can_start]
[cooldown_ok] →  ↑
[NOT pump_running] → ↑

Stop permission:
[stop_cmd]    → [AND] → [can_stop]
[min_run_ok]  →  ↑

Pump state (SR bistable):
[can_start] → [SR] → [pump_running]
[can_stop]  →  ↑
```

### How It Works

1. The **run timer** counts while the pump is running. After 30 seconds, `min_run_ok` allows stopping.
2. The **cooldown timer** counts while the pump is stopped. After 60 seconds, `cooldown_ok` allows restarting.
3. The **start AND** block ensures starting only when commanded, cooldown has elapsed, and pump is not already running.
4. The **stop AND** block ensures stopping only when commanded and minimum run time has elapsed.
5. The **SR** bistable holds the pump state between scan cycles.

## Counter with Reset and Display

Count items passing a sensor and reset when a batch is complete.

### Variables

| Name | Type | Class | Description |
|------|------|-------|-------------|
| `item_sensor` | BOOL | Local | Item detected (pulsed) |
| `batch_reset` | BOOL | Local | Reset counter for new batch |
| `batch_size` | INT | Local | Target batch count (e.g., 100) |
| `item_count` | INT | Local | Current count |
| `batch_complete` | BOOL | Local | Batch target reached |

### FBD Structure

```
[item_sensor] → [CTU: counter, PV=batch_size, RESET=batch_reset] → Q: [batch_complete]
                                                                    → CV: [item_count]
```

### How It Works

The **CTU** (Counter Up) block increments on each rising edge of `item_sensor`. When `item_count` reaches `batch_size`, `batch_complete` goes TRUE. The `batch_reset` input clears the counter for a new batch.

## Selector and Multiplexer

Choose between automatic and manual control modes.

### Variables

| Name | Type | Class | Description |
|------|------|-------|-------------|
| `auto_mode` | BOOL | Local | Automatic mode selector |
| `auto_speed` | REAL | Local | Speed from automatic controller |
| `manual_speed` | REAL | Local | Speed from operator |
| `output_speed` | REAL | Local | Actual speed command sent to drive |

### FBD Structure

```
[auto_mode]    → [SEL] → [output_speed]
[manual_speed] →  ↑  (IN0 — selected when G=FALSE)
[auto_speed]   →  ↑  (IN1 — selected when G=TRUE)
```

### How It Works

The **SEL** (Selector) block chooses between two inputs based on a Boolean selector:
- When `auto_mode` is FALSE → `output_speed` = `manual_speed`
- When `auto_mode` is TRUE → `output_speed` = `auto_speed`

This is the FBD equivalent of an IF/ELSE statement in ST:

```
IF auto_mode THEN
    output_speed := auto_speed;
ELSE
    output_speed := manual_speed;
END_IF;
```

## Best Practices for FBD

1. **Flow left to right** — Keep data flow consistent. Inputs on the left, outputs on the right.
2. **Name all variables** — Give every input and output variable a meaningful name in the Variables Table.
3. **Break complex logic into stages** — Use intermediate variables to split long processing chains into understandable steps.
4. **Use comments** — Add comment nodes to explain non-obvious logic.
5. **Group related blocks** — Position blocks that work together close to each other on the canvas.
6. **Keep it flat** — If your FBD diagram gets too complex, consider refactoring parts into a custom function block.

---

## What's Next?

Explore other programming languages: [Instruction List Basics](../instruction-list/il-basics) for a low-level text-based approach, or return to [Ladder Diagram](../ladder-diagram/ld-basics) for relay-style logic.
