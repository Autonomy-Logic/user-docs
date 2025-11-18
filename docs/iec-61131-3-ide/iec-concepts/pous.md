# Program Organization Units (POUs)

Program Organization Units (POUs) are the fundamental building blocks of IEC 61131-3 programs. They allow you to organize your code into modular, reusable components that can be tested independently and combined to create complex automation systems.

## What are POUs?

POUs are self-contained code modules that encapsulate specific functionality. The IEC 61131-3 standard defines three types of POUs, each serving a different purpose in your program architecture:

1. **Programs**: Top-level execution units
2. **Function Blocks**: Stateful, reusable components
3. **Functions**: Stateless, reusable calculations

Understanding when and how to use each type of POU is essential for creating well-structured, maintainable automation programs.

## The Three Types of POUs

### 1. Programs

Programs are the top-level POUs in your project. They represent the main logic that will be executed by the PLC runtime.

#### Characteristics of Programs:
- **Executed by Tasks**: Programs are assigned to tasks that control when and how often they run
- **Can Have State**: Programs can maintain internal variables that persist between execution cycles
- **Call Other POUs**: Programs can call functions and function blocks to perform specific operations
- **One or More Per Project**: A project can have multiple programs, each assigned to different tasks
- **Cannot Be Called**: Programs cannot be called by other POUs; they are only executed by tasks

#### When to Use Programs:
- As the main entry point for your application logic
- To organize different aspects of your control system (e.g., one program for motion control, another for safety logic)
- When you need a POU that will be directly executed by a task

#### Example Program Structure:
```
PROGRAM main
VAR
    counter : INT := 0;
    running : BOOL := FALSE;
END_VAR

// Main program logic
IF running THEN
    counter := counter + 1;
END_IF;
END_PROGRAM
```

### 2. Function Blocks

Function Blocks are reusable components that maintain internal state between calls. They are the workhorses of IEC 61131-3 programming, ideal for implementing control algorithms, state machines, and complex logic.

#### Characteristics of Function Blocks:
- **Maintain State**: Internal variables persist between calls
- **Multiple Instances**: You can create multiple instances of the same function block, each with its own state
- **Input and Output Parameters**: Accept inputs and produce outputs
- **Can Call Other POUs**: Function blocks can call functions and other function blocks
- **Reusable**: Once defined, can be used throughout your project

#### When to Use Function Blocks:
- For control algorithms that need to remember previous states (e.g., PID controllers, timers, counters)
- When you need multiple instances with independent states (e.g., multiple motor controllers)
- For complex logic that you want to reuse in different parts of your program
- When implementing state machines or sequential logic

#### Example Function Block:
```
FUNCTION_BLOCK MotorController
VAR_INPUT
    start : BOOL;
    stop : BOOL;
    speed_setpoint : INT;
END_VAR
VAR_OUTPUT
    motor_running : BOOL;
    current_speed : INT;
END_VAR
VAR
    state : INT := 0;  // Internal state variable
END_VAR

// Motor control logic with state
CASE state OF
    0: // Stopped
        IF start THEN
            state := 1;
            motor_running := TRUE;
        END_IF;
    1: // Running
        IF stop THEN
            state := 0;
            motor_running := FALSE;
        END_IF;
        current_speed := speed_setpoint;
END_CASE;
END_FUNCTION_BLOCK
```

#### Using Function Block Instances:
To use a function block, you must first declare an instance of it:
```
PROGRAM main
VAR
    motor1 : MotorController;  // Instance 1
    motor2 : MotorController;  // Instance 2
END_VAR

// Each instance maintains its own state
motor1(start := TRUE, stop := FALSE, speed_setpoint := 100);
motor2(start := FALSE, stop := TRUE, speed_setpoint := 50);
END_PROGRAM
```

### 3. Functions

Functions are stateless POUs that perform calculations or transformations and return a single value. They are similar to mathematical functions: given the same inputs, they always produce the same output.

#### Characteristics of Functions:
- **No Internal State**: Functions cannot have variables that persist between calls
- **Return a Single Value**: Every function has a return type (e.g., INT, REAL, BOOL)
- **Pure Computation**: Ideal for calculations, data conversions, and transformations
- **Cannot Call Function Blocks**: Functions can only call other functions
- **Efficient**: Because they have no state, functions are typically faster than function blocks

#### When to Use Functions:
- For mathematical calculations (e.g., converting units, calculating averages)
- For data type conversions (e.g., INT to REAL, REAL to STRING)
- For simple logic operations that don't need to remember previous values
- When you need a pure, predictable operation with no side effects

#### Example Function:
```
FUNCTION CelsiusToFahrenheit : REAL
VAR_INPUT
    celsius : REAL;
END_VAR

// Simple conversion calculation
CelsiusToFahrenheit := (celsius * 9.0 / 5.0) + 32.0;
END_FUNCTION
```

#### Using Functions:
Functions are called directly and return a value:
```
PROGRAM main
VAR
    temp_c : REAL := 25.0;
    temp_f : REAL;
END_VAR

// Call the function and use its return value
temp_f := CelsiusToFahrenheit(temp_c);
END_PROGRAM
```

## Comparison of POU Types

| Feature | Program | Function Block | Function |
|---------|---------|----------------|----------|
| **Maintains State** | Yes | Yes | No |
| **Return Value** | No | No (uses outputs) | Yes (single value) |
| **Can Be Instanced** | No | Yes | No |
| **Called By** | Tasks only | Programs, FBs | Programs, FBs, Functions |
| **Can Call FBs** | Yes | Yes | No |
| **Use Case** | Main logic | Stateful algorithms | Calculations |

## POU Variables

Each POU can declare variables in different categories:

### Variable Classes in POUs:

1. **VAR_INPUT**: Input parameters passed to the POU
2. **VAR_OUTPUT**: Output values returned by the POU
3. **VAR_IN_OUT**: Parameters that are both input and output (passed by reference)
4. **VAR**: Local variables (internal to the POU)
5. **VAR_TEMP**: Temporary variables (not persistent, cleared after each execution)

### Example with All Variable Types:
```
FUNCTION_BLOCK DataProcessor
VAR_INPUT
    raw_value : INT;        // Input parameter
    enable : BOOL;
END_VAR
VAR_OUTPUT
    processed_value : INT;  // Output parameter
    valid : BOOL;
END_VAR
VAR_IN_OUT
    buffer : ARRAY[0..9] OF INT;  // In-out parameter
END_VAR
VAR
    sum : INT := 0;         // Local variable (persistent)
    count : INT := 0;
END_VAR
VAR_TEMP
    temp : INT;             // Temporary variable (not persistent)
END_VAR

// Processing logic here
END_FUNCTION_BLOCK
```

## Creating POUs in the IDE

### Step-by-Step: Creating a New POU

1. **Open the Project Explorer**: Ensure the Explorer panel is visible
2. **Click the + Button**: At the top of the Project Explorer
3. **Select POU Type**: Choose Program, Function Block, or Function
4. **Choose Language**: Select from ST, LD, IL, FBD, or SFC
5. **Enter Name**: Provide a descriptive name following naming conventions
6. **Configure**: The new POU will open in the editor with a template

### Naming Conventions:

Follow these best practices for naming POUs:
- **Use PascalCase**: `MotorController`, `CalculateAverage`, `MainProgram`
- **Be Descriptive**: Names should clearly indicate the POU's purpose
- **Avoid Abbreviations**: Use `TemperatureController` instead of `TempCtrl`
- **Use Prefixes** (optional): `FB_MotorControl`, `FC_ConvertUnits`, `PRG_Main`

## Best Practices for Using POUs

### 1. Single Responsibility Principle
Each POU should have one clear purpose. Don't create a single large POU that does everything.

**Good Example:**
- `MotorController` - Controls a single motor
- `ConveyorSystem` - Coordinates multiple motors
- `SafetyMonitor` - Monitors safety conditions

**Bad Example:**
- `MainControl` - Does everything (motor control, safety, communication, etc.)

### 2. Appropriate POU Selection
Choose the right type of POU for each task:
- Use **Functions** for pure calculations
- Use **Function Blocks** for stateful logic
- Use **Programs** as top-level coordinators

### 3. Modular Design
Break complex logic into smaller, reusable POUs:
```
PROGRAM main
VAR
    conveyor1 : ConveyorController;
    conveyor2 : ConveyorController;
    safety : SafetyMonitor;
END_VAR

// Coordinate multiple function blocks
safety();
IF safety.system_safe THEN
    conveyor1(enable := TRUE);
    conveyor2(enable := TRUE);
END_IF;
END_PROGRAM
```

### 4. Documentation
Always document your POUs:
- Add a description in the Documentation field
- Comment complex logic within the code
- Explain input and output parameters
- Document any assumptions or limitations

### 5. Testing
Test POUs independently before integrating them:
- Create test programs for individual function blocks
- Verify functions with known inputs and outputs
- Test edge cases and error conditions

## Advanced POU Concepts

### Inheritance (Future Feature)
Some IEC 61131-3 implementations support function block inheritance, allowing you to create specialized versions of existing function blocks. This feature may be added in future versions of the IDE.

### Methods (Future Feature)
Advanced implementations allow function blocks to have methods (functions that operate on the function block's data). This feature may be added in future versions.

### Properties (Future Feature)
Properties provide controlled access to function block internal variables. This feature may be added in future versions.

## Common POU Patterns

### Pattern 1: State Machine Function Block
```
FUNCTION_BLOCK StateMachine
VAR_INPUT
    trigger : BOOL;
    reset : BOOL;
END_VAR
VAR_OUTPUT
    state : INT;
END_VAR
VAR
    internal_state : INT := 0;
END_VAR

IF reset THEN
    internal_state := 0;
ELSIF trigger THEN
    internal_state := internal_state + 1;
END_IF;
state := internal_state;
END_FUNCTION_BLOCK
```

### Pattern 2: Utility Functions Library
Create a collection of related functions:
- `MathUtils`: `Clamp()`, `Scale()`, `Average()`
- `StringUtils`: `Concat()`, `ToUpper()`, `Trim()`
- `TimeUtils`: `SecondsToDuration()`, `FormatTime()`

### Pattern 3: Coordinator Program
Use programs to coordinate multiple function blocks:
```
PROGRAM ProductionLine
VAR
    station1 : WorkStation;
    station2 : WorkStation;
    conveyor : ConveyorController;
END_VAR

// Coordinate the production line
station1(enable := TRUE);
IF station1.complete THEN
    conveyor(move := TRUE);
    IF conveyor.position_reached THEN
        station2(enable := TRUE);
    END_IF;
END_IF;
END_PROGRAM
```

## Next Steps

Now that you understand Program Organization Units, you can learn about Variables and Data Types to understand how to declare and use data in your POUs, and then explore Tasks and Instances to learn how programs are executed by the PLC runtime.
