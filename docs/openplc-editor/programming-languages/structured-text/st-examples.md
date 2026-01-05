# ST Programming Examples

This section provides practical examples of common Structured Text programming patterns. These examples demonstrate how to apply ST language features to solve real-world control problems.

## Temperature Control System

This example demonstrates a complete temperature control program that uses conditional logic, timers, and alarm handling. The program controls heating and cooling based on temperature readings with a safety delay before activating the heater.

### Variables Definition

First, define the variables in the Variables Table:

| Name | Class | Type | Description |
|------|-------|------|-------------|
| `sensor_temp` | Local | REAL | Current temperature reading from sensor |
| `setpoint` | Local | REAL | Desired target temperature |
| `enable` | Local | BOOL | Enable/disable the control system |
| `heater_on` | Local | BOOL | Heater control output |
| `cooler_on` | Local | BOOL | Cooler control output |
| `alarm` | Local | BOOL | Out-of-range alarm flag |
| `temp_error` | Local | REAL | Temperature error (setpoint - actual) |
| `timer` | Local | TON | Timer for heater activation delay |

### Complete Code

```
IF enable THEN
    temp_error := setpoint - sensor_temp;

    (* Start heater only after 5s of continuous heat demand *)
    timer(IN := (temp_error > 2.0), PT := T#5s);

    IF timer.Q THEN
        heater_on := TRUE;
        cooler_on := FALSE;
    ELSIF temp_error < -2.0 THEN
        heater_on := FALSE;
        cooler_on := TRUE;
    ELSE
        heater_on := FALSE;
        cooler_on := FALSE;
    END_IF;

    (* Out-of-range alarm *)
    IF (sensor_temp > 50.0) OR (sensor_temp < 0.0) THEN
        alarm := TRUE;
    ELSE
        alarm := FALSE;
    END_IF;
ELSE
    heater_on := FALSE;
    cooler_on := FALSE;
    alarm := FALSE;
    counter := 0;
    timer(IN := FALSE, PT := T#5s);
END_IF;
```

![Temperature Control Program](images/st-syntax-highlighting.png)
*Complete temperature control program showing syntax highlighting and structure*

### Code Explanation

**Enable Logic**: The outer IF statement checks if the system is enabled. When disabled, all outputs are turned off and the timer is reset.

**Temperature Error Calculation**: The difference between setpoint and actual temperature is calculated to determine heating or cooling needs.

**Timer-Based Heater Control**: The timer prevents rapid cycling by requiring 5 seconds of continuous heat demand before activating the heater. The expression `(temp_error > 2.0)` is passed directly to the timer's IN parameter.

**Conditional Output Control**: 
- If `timer.Q` is TRUE (timer elapsed), activate heater
- If temperature error is less than -2.0 (too hot), activate cooler
- Otherwise, turn off both heater and cooler

**Safety Alarm**: An independent check monitors if the temperature is outside the safe range (0°C to 50°C) and sets an alarm flag.

### Key Patterns Demonstrated

1. **Nested IF statements** for complex decision logic
2. **Function block calls** with named parameters
3. **Accessing function block outputs** using dot notation (`timer.Q`)
4. **Expressions as parameters** passing `(temp_error > 2.0)` directly to timer
5. **Multi-line comments** using `(* ... *)` for documentation
6. **Boolean logic** with OR operator for alarm conditions
7. **Arithmetic operations** for error calculation

## State Machine Pattern

State machines are common in industrial control for managing sequential operations. This example shows a simple motor control state machine.

### Variables

```
VAR
    state : INT := 0;              // Current state (0=Stopped, 1=Starting, 2=Running, 3=Stopping)
    start_button : BOOL;           // Start command
    stop_button : BOOL;            // Stop command
    motor_ready : BOOL;            // Motor ready feedback
    motor_running : BOOL;          // Motor running feedback
    motor_command : BOOL;          // Motor start command output
    start_timer : TON;             // Startup delay timer
    stop_timer : TON;              // Shutdown delay timer
END_VAR
```

### Code

```
CASE state OF
    0:  (* Stopped State *)
        motor_command := FALSE;
        IF start_button AND motor_ready THEN
            state := 1;  // Transition to Starting
        END_IF;
    
    1:  (* Starting State *)
        motor_command := TRUE;
        start_timer(IN := TRUE, PT := T#2s);
        
        IF start_timer.Q THEN
            IF motor_running THEN
                state := 2;  // Transition to Running
                start_timer(IN := FALSE, PT := T#2s);  // Reset timer
            END_IF;
        END_IF;
        
        IF stop_button THEN
            state := 3;  // Emergency stop
            start_timer(IN := FALSE, PT := T#2s);
        END_IF;
    
    2:  (* Running State *)
        motor_command := TRUE;
        IF stop_button OR NOT motor_running THEN
            state := 3;  // Transition to Stopping
        END_IF;
    
    3:  (* Stopping State *)
        motor_command := FALSE;
        stop_timer(IN := TRUE, PT := T#1s);
        
        IF stop_timer.Q THEN
            state := 0;  // Transition to Stopped
            stop_timer(IN := FALSE, PT := T#1s);  // Reset timer
        END_IF;
        
ELSE
    (* Error state - reset to stopped *)
    state := 0;
    motor_command := FALSE;
END_CASE;
```

### Pattern Explanation

This state machine uses a CASE statement to organize different operational states. Each state:
- Performs specific actions (setting outputs)
- Checks conditions for state transitions
- Uses timers for delays between states
- Handles error conditions

The ELSE clause catches any invalid state values and resets to a safe state.

## Array Processing

This example shows how to work with arrays for data processing.

### Variables

```
VAR
    sensor_readings : ARRAY[0..9] OF REAL;    // 10 sensor values
    average : REAL;                            // Calculated average
    max_value : REAL;                          // Maximum value found
    min_value : REAL;                          // Minimum value found
    sum : REAL;                                // Sum for average calculation
    i : INT;                                   // Loop counter
END_VAR
```

### Code

```
(* Initialize min/max with first value *)
max_value := sensor_readings[0];
min_value := sensor_readings[0];
sum := 0.0;

(* Process all array elements *)
FOR i := 0 TO 9 DO
    (* Update sum for average *)
    sum := sum + sensor_readings[i];
    
    (* Track maximum value *)
    IF sensor_readings[i] > max_value THEN
        max_value := sensor_readings[i];
    END_IF;
    
    (* Track minimum value *)
    IF sensor_readings[i] < min_value THEN
        min_value := sensor_readings[i];
    END_IF;
END_FOR;

(* Calculate average *)
average := sum / 10.0;
```

### Pattern Explanation

This example demonstrates:
- **Array indexing** with `sensor_readings[i]`
- **FOR loop** for iterating through array elements
- **Accumulator pattern** for calculating sum
- **Min/max tracking** by comparing each element
- **Floating-point division** for average calculation

## Counter with Rollover

This example shows how to implement a bounded counter that rolls over at a maximum value.

### Variables

```
VAR
    counter : INT := 0;
    increment : BOOL;              // Pulse to increment
    reset : BOOL;                  // Reset to zero
    max_count : INT := 999;        // Maximum value before rollover
    last_increment : BOOL := FALSE; // Edge detection
END_VAR
```

### Code

```
(* Reset has priority *)
IF reset THEN
    counter := 0;
ELSIF increment AND NOT last_increment THEN
    (* Rising edge detection - increment only once per pulse *)
    IF counter >= max_count THEN
        counter := 0;  // Rollover
    ELSE
        counter := counter + 1;
    END_IF;
END_IF;

(* Store current state for next cycle edge detection *)
last_increment := increment;
```

### Pattern Explanation

This example shows:
- **Edge detection** to trigger on rising edge only
- **Priority logic** with reset taking precedence
- **Rollover behavior** using IF/ELSE
- **State preservation** for edge detection between cycles

## Timer Patterns

### Pulse Generator

Generate a periodic pulse with configurable on/off times.

```
VAR
    output : BOOL := FALSE;
    on_timer : TON;
    off_timer : TON;
    on_time : TIME := T#500ms;
    off_time : TIME := T#500ms;
END_VAR

(* Pulse generator logic *)
IF output THEN
    (* Output is ON - wait for on_time to expire *)
    on_timer(IN := TRUE, PT := on_time);
    off_timer(IN := FALSE, PT := off_time);
    
    IF on_timer.Q THEN
        output := FALSE;
        on_timer(IN := FALSE, PT := on_time);
    END_IF;
ELSE
    (* Output is OFF - wait for off_time to expire *)
    off_timer(IN := TRUE, PT := off_time);
    on_timer(IN := FALSE, PT := on_time);
    
    IF off_timer.Q THEN
        output := TRUE;
        off_timer(IN := FALSE, PT := off_time);
    END_IF;
END_IF;
```

### Delayed Start/Stop

Implement delays for both starting and stopping an output.

```
VAR
    command : BOOL;                // Input command
    output : BOOL := FALSE;        // Delayed output
    start_timer : TON;
    stop_timer : TON;
    start_delay : TIME := T#3s;
    stop_delay : TIME := T#1s;
END_VAR

IF command THEN
    (* Command is ON - start delay *)
    start_timer(IN := TRUE, PT := start_delay);
    stop_timer(IN := FALSE, PT := stop_delay);
    
    IF start_timer.Q THEN
        output := TRUE;
    END_IF;
ELSE
    (* Command is OFF - stop delay *)
    stop_timer(IN := TRUE, PT := stop_delay);
    start_timer(IN := FALSE, PT := start_delay);
    
    IF stop_timer.Q THEN
        output := FALSE;
    END_IF;
END_IF;
```

## String Operations

Working with text strings for messages and data formatting.

### Variables

```
VAR
    status_code : INT;
    status_message : STRING;
    alarm_active : BOOL;
    temperature : REAL := 25.5;
END_VAR
```

### Code

```
(* Generate status message based on code *)
CASE status_code OF
    0:
        status_message := 'System OK';
    1:
        status_message := 'Warning: High Temperature';
    2:
        status_message := 'Error: Sensor Fault';
    3:
        status_message := 'Emergency Stop Active';
ELSE
    status_message := 'Unknown Status';
END_CASE;

(* Append alarm indicator if needed *)
IF alarm_active THEN
    status_message := CONCAT(status_message, ' [ALARM]');
END_IF;
```

## Best Practices Summary

Based on these examples, follow these best practices:

### Code Organization
1. **Group related logic**: Keep related operations together
2. **Use comments**: Document the purpose of code sections
3. **Consistent naming**: Use descriptive, consistent variable names
4. **One responsibility**: Each code block should have a clear purpose

### Control Flow
1. **Prefer CASE over nested IFs**: For multiple discrete values
2. **Use ELSIF**: Instead of nested IF statements when possible
3. **Handle all cases**: Include ELSE clauses for unexpected conditions
4. **Exit early**: Use RETURN or EXIT to avoid deep nesting

### Timers and Counters
1. **Reset timers**: Always reset timers when not in use
2. **Check outputs**: Use `.Q` to check timer completion
3. **Edge detection**: Implement edge detection for pulse inputs
4. **Bounded counters**: Prevent overflow with MOD or explicit checks

### Data Processing
1. **Initialize before loops**: Set initial values before FOR loops
2. **Bounds checking**: Verify array indices are valid
3. **Floating-point care**: Be aware of precision limitations
4. **Avoid division by zero**: Check denominators before division

### Safety and Reliability
1. **Fail-safe defaults**: Initialize outputs to safe states
2. **Timeout handling**: Use timers to detect stuck conditions
3. **Range checking**: Validate sensor inputs are reasonable
4. **Error states**: Always handle error conditions explicitly

## Next Steps

- [ST Language Basics](st-basics) - Review fundamental ST syntax and operators
- [ST Editor Features](st-editor) - Learn about the IDE's code editing capabilities
- [Standard Function Blocks Library](../../standard-function-blocks/overview) - Explore available function blocks
