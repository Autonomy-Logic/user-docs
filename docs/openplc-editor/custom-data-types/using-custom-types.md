# Using Custom Data Types

Creating a data type is only the first step. The real value comes from using your custom types throughout your project — declaring variables, accessing their contents in code, passing them between POUs, and combining them into richer data models. This page shows you how to work with arrays, enumerations, and structures once they're defined.

## Declaring Variables with Custom Types

After you create a custom data type, it becomes available in the **Type** dropdown of any POU's Variables Table. Custom types appear under the **User Data Types** category in the dropdown.

To declare a variable with a custom type:

1. Open a POU (Program, Function, or Function Block) in the Editor Area.
2. In the Variables Table, click the **+** button to add a new variable.
3. Enter a name for the variable.
4. Click the **Type** cell and select your custom type from the **User Data Types** section of the dropdown.
5. Optionally set a variable class (Local, Input, Output, InOut, External, Temp).
6. Optionally set an initial value.

**Example variable declarations:**

| Name | Class | Type | Initial Value |
|------|-------|------|---------------|
| `temperatures` | Local | `SensorBank` | |
| `machineState` | Local | `MachineState` | `IDLE` |
| `motorParams` | Input | `MotorConfig` | |
| `alarmLog` | Local | `AlarmRecord` | |

## Working with Array Variables

### Accessing Elements

Use bracket notation with an index to read or write individual array elements:

```
(* Variable: temps of type SensorBank (ARRAY [0..9] OF REAL) *)

(* Write to an element *)
temps[0] := 22.5;
temps[5] := sensor_reading;

(* Read from an element *)
currentTemp := temps[3];
```

### Iterating with FOR Loops

The most common pattern for working with arrays is iterating through all elements with a FOR loop:

```
(* Sum all values in the array *)
total := 0.0;
FOR i := 0 TO 9 DO
    total := total + temps[i];
END_FOR;
average := total / 10.0;
```

```
(* Find the maximum value *)
maxTemp := temps[0];
FOR i := 1 TO 9 DO
    IF temps[i] > maxTemp THEN
        maxTemp := temps[i];
        maxIndex := i;
    END_IF;
END_FOR;
```

### Multi-Dimensional Array Access

For multi-dimensional arrays, provide one index per dimension separated by commas:

```
(* Variable: matrix of type SpeedTable (ARRAY [1..6, 0..10] OF REAL) *)

(* Read a value *)
targetSpeed := matrix[currentGear, throttlePosition];

(* Write a value *)
matrix[3, 5] := 1500.0;

(* Iterate over a 2D array *)
FOR row := 1 TO 6 DO
    FOR col := 0 TO 10 DO
        matrix[row, col] := 0.0;
    END_FOR;
END_FOR;
```

### Using an Index Variable

Often the index comes from a calculated value or an input. Always validate that the index is within bounds:

```
IF (selectedSensor >= 0) AND (selectedSensor <= 9) THEN
    displayValue := temps[selectedSensor];
ELSE
    displayValue := 0.0;
END_IF;
```

## Working with Enumeration Variables

### Assignment

Assign an enumeration value by name:

```
(* Variable: state of type MachineState *)

state := IDLE;
state := RUNNING;
```

### Comparison

Compare enumeration variables using `=` and `<>`:

```
IF state = RUNNING THEN
    motorEnable := TRUE;
END_IF;

IF state <> FAULTED THEN
    allowOperation := TRUE;
END_IF;
```

### CASE Statements

The CASE statement is the standard pattern for enumeration-based state machines. Each branch handles one (or more) enumeration values:

```
CASE state OF
    IDLE:
        motorEnable := FALSE;
        readyIndicator := TRUE;

    STARTING:
        motorEnable := TRUE;
        IF motorAtSpeed THEN
            state := RUNNING;
        END_IF;

    RUNNING:
        motorEnable := TRUE;
        readyIndicator := TRUE;
        IF stopCommand THEN
            state := STOPPING;
        ELSIF faultDetected THEN
            state := FAULTED;
        END_IF;

    STOPPING:
        motorEnable := FALSE;
        IF motorStopped THEN
            state := IDLE;
        END_IF;

    FAULTED:
        motorEnable := FALSE;
        readyIndicator := FALSE;
        alarmOutput := TRUE;
        IF resetCommand THEN
            alarmOutput := FALSE;
            state := IDLE;
        END_IF;
END_CASE;
```

### State Transitions

A common pattern is combining enumeration assignments with conditional logic for clean state transitions:

```
(* Transition from any state to FAULTED on fault *)
IF faultDetected AND (state <> FAULTED) THEN
    previousState := state;
    state := FAULTED;
END_IF;
```

## Working with Structure Variables

### Accessing Fields

Use dot notation to read and write individual fields of a structure variable:

```
(* Variable: sensor of type SensorData *)

(* Write to fields *)
sensor.Value := 23.7;
sensor.Valid := TRUE;
sensor.SensorId := 1;

(* Read from fields *)
currentReading := sensor.Value;
isValid := sensor.Valid;
```

### Using Multiple Fields Together

Structures are most powerful when you work with several fields in context:

```
(* Update a sensor reading *)
sensor.Value := analogInput;
sensor.Valid := (analogInput > 0.0) AND (analogInput < 1000.0);

(* Only process valid readings *)
IF sensor.Valid THEN
    processedValue := sensor.Value * calibrationFactor;
END_IF;
```

### Passing Structures to Function Blocks

Structure variables can be passed as inputs or outputs to function blocks. Define the function block's parameter with the structure type:

```
(* Function block TemperatureMonitor has input: config : MotorConfig *)

tempMonitor(config := myMotorConfig);
```

For InOut parameters (passed by reference), the function block can modify the structure's fields directly:

```
(* Function block with InOut: data : SensorData *)

sensorProcessor(data := mySensor);
(* After the call, mySensor.Valid may have been updated by the FB *)
```

## Nesting Custom Types

One of the most powerful features of IEC 61131-3 data types is **composability** — you can use custom types as building blocks for other custom types.

### Structures Containing Enumerations

Define a structure with an enumeration field for self-describing data:

```
(* Assuming AlarmLevel enumeration: NONE, INFO, WARNING, CRITICAL *)
(* Structure AlarmRecord with field Level of type AlarmLevel *)

alarm.Level := WARNING;
alarm.Active := TRUE;
alarm.Message := 'Pressure high';

IF alarm.Level = CRITICAL THEN
    emergencyStop := TRUE;
END_IF;
```

### Structures Containing Arrays

A structure can include array fields for grouped collections:

```
(* Structure ChannelData with field Readings of type ARRAY [0..9] OF REAL *)

channel.ChannelId := 3;
channel.Readings[0] := 22.5;
channel.Readings[1] := 23.1;

(* Compute average from the array inside the structure *)
sum := 0.0;
FOR i := 0 TO 9 DO
    sum := sum + channel.Readings[i];
END_FOR;
channel.Average := sum / 10.0;
```

### Arrays of Structures

Declare an array type whose base type is a structure for a table of structured records:

```
(* Array type SensorArray: ARRAY [0..19] OF SensorData *)
(* Variable: sensors of type SensorArray *)

(* Access the Value field of sensor at index 5 *)
reading := sensors[5].Value;

(* Update all sensors in a loop *)
FOR i := 0 TO 19 DO
    sensors[i].Value := rawInputs[i];
    sensors[i].Valid := (rawInputs[i] > minThreshold);
END_FOR;

(* Find the first faulted sensor *)
FOR i := 0 TO 19 DO
    IF NOT sensors[i].Valid THEN
        firstFaultIndex := i;
        EXIT;
    END_IF;
END_FOR;
```

### Structures Containing Structures

Nested structures model hierarchical data:

```
(* Structure DriveUnit containing a MotorConfig field *)

drive.Config.Speed := 1500.0;
drive.Config.Enabled := TRUE;
drive.Status.Running := TRUE;
drive.Status.Current := 8.5;
```

## Custom Types as Function and Function Block Parameters

Custom types work seamlessly as POU parameters — instead of passing five separate values, you pass one structure:

```
(* As Input — caller passes value to the FB *)
processSensor(data := mySensorReading);

(* As Output — FB produces a value the caller reads *)
readSensor();
currentValue := readSensor.result.Value;

(* As InOut — FB modifies the caller's variable in place *)
updateConfig(config := myMotorParams);
```

## Using Custom Types in Graphical Languages

In **Ladder Diagram**, custom type variables work with function block instances on rungs. Individual structure fields can serve as contacts or coils using dot notation (e.g., `sensor.Valid` as a contact, `motor.Enabled` as a coil). Array elements use bracket notation (e.g., `outputs[3]`).

In **Function Block Diagram**, custom type variables connect to function block input/output pins by name. The same dot and bracket notation applies — wire `sensor.Value` to a comparison block input, or connect a math block output to `results[i]`.

## Practical Example: Complete Sensor Monitoring System

This example ties together all three custom type derivations in a realistic scenario.

**Type definitions:**

```
(* Enumeration *)
TYPE SensorStatus : (OK, WARN, FAULT) := OK; END_TYPE

(* Structure *)
TYPE SensorReading :
  STRUCT
    Value     : REAL := 0.0;
    Status    : SensorStatus := OK;
    HighLimit : REAL := 100.0;
    LowLimit  : REAL := 0.0;
  END_STRUCT
END_TYPE

(* Array *)
TYPE SensorArray : ARRAY [0..7] OF SensorReading; END_TYPE
```

**Program using these types:**

```
(* Variables table:
   sensors    : SensorArray   (Local)
   faultCount : INT           (Local)
   warnCount  : INT           (Local)
   allOk      : BOOL          (Output)
*)

faultCount := 0;
warnCount := 0;

FOR i := 0 TO 7 DO
    (* Check against limits *)
    IF (sensors[i].Value > sensors[i].HighLimit) OR
       (sensors[i].Value < sensors[i].LowLimit) THEN
        sensors[i].Status := FAULT;
        faultCount := faultCount + 1;
    ELSIF (sensors[i].Value > sensors[i].HighLimit * 0.9) OR
          (sensors[i].Value < sensors[i].LowLimit * 1.1) THEN
        sensors[i].Status := WARN;
        warnCount := warnCount + 1;
    ELSE
        sensors[i].Status := OK;
    END_IF;
END_FOR;

allOk := (faultCount = 0) AND (warnCount = 0);
```

This program monitors 8 sensors, each with its own configurable limits and status, using just three custom types and a handful of variables.

---

## What's Next?

Learn about the standard function blocks available for timing and counting with [Timer Function Blocks](../standard-function-blocks/timer-blocks).
