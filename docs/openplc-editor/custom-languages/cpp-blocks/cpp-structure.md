# C++ Function Block Structure

This page explains how C++ function blocks bridge with the IEC runtime. Understanding the variable access mechanism, IEC type mappings, and Arduino conditional compilation will help you write more effective C++ code and debug issues when they arise.

## The Two Required Functions

Every C++ function block must define exactly two functions:

### `void setup()`

Called once on the first scan cycle. Use it for initialization:

```cpp
void setup() {
    // Initialize hardware
    // Set default output values
    // Allocate or prepare any resources
}
```

### `void loop()`

Called on every scan cycle after the first. This is your main execution logic:

```cpp
void loop() {
    // Read inputs
    // Process logic
    // Write outputs
}
```

The IDE validates that both functions are present. If either `void setup()` or `void loop()` is missing, the build will fail with a validation error. The signatures must match exactly — no parameters, no return value.

## How Variable Access Works

When you declare variables in the Variables Table and reference them by name in your C++ code, the IDE generates accessor macros behind the scenes. This lets you write clean code like `OUTPUT_VAL = INPUT_VAL * 2.0;` without managing pointers or memory directly.

For each C++ function block, the IDE generates:

1. **A pointer struct** holding references to every declared variable
2. **Accessor macros** (`#define`) that let you use variable names directly
3. **A wrapper** that handles calling `setup()` on the first scan and `loop()` on every subsequent scan

For example, if your function block is named `MyFilter` with variables `INPUT_VAL` (Input, REAL) and `OUTPUT_VAL` (Output, REAL), the generated macros work like this:

```c
#define INPUT_VAL (*(vars->INPUT_VAL))
#define OUTPUT_VAL (*(vars->OUTPUT_VAL))
```

You don't need to manage any of this yourself — just use the variable names directly in your code. When another POU instantiates your C++ function block, it works exactly like any IEC function block.

## The hasBeenInitialized Variable

Every C++ function block automatically receives a local BOOL variable called `hasBeenInitialized`. The wrapper uses this to determine whether to call `setup()` or `loop()`:

- On the **first scan**: `hasBeenInitialized` is FALSE, so `setup()` is called, then `hasBeenInitialized` is set to TRUE.
- On **every subsequent scan**: `hasBeenInitialized` is TRUE, so `loop()` is called.

You don't need to declare or manage this variable — it's injected automatically.

## IEC Type Definitions

When your C++ code accesses variables from the Variables Table, the values use IEC-standard data types that map to specific C types. Here's the complete mapping:

### Integer Types

| IEC Type | C Type | Size | Range |
|----------|--------|------|-------|
| `IEC_SINT` | `int8_t` | 8-bit | -128 to 127 |
| `IEC_INT` | `int16_t` | 16-bit | -32,768 to 32,767 |
| `IEC_DINT` | `int32_t` | 32-bit | -2,147,483,648 to 2,147,483,647 |
| `IEC_LINT` | `int64_t` | 64-bit | -9.2 × 10¹⁸ to 9.2 × 10¹⁸ |
| `IEC_USINT` | `uint8_t` | 8-bit | 0 to 255 |
| `IEC_UINT` | `uint16_t` | 16-bit | 0 to 65,535 |
| `IEC_UDINT` | `uint32_t` | 32-bit | 0 to 4,294,967,295 |
| `IEC_ULINT` | `uint64_t` | 64-bit | 0 to 1.8 × 10¹⁹ |

### Floating Point Types

| IEC Type | C Type | Size | Precision |
|----------|--------|------|-----------|
| `IEC_REAL` | `float` | 32-bit | ~7 decimal digits |
| `IEC_LREAL` | `double` | 64-bit | ~15 decimal digits |

### Boolean and Bit String Types

| IEC Type | C Type | Size | Description |
|----------|--------|------|-------------|
| `IEC_BOOL` | `uint8_t` | 8-bit | Boolean (0 = FALSE, nonzero = TRUE) |
| `IEC_BYTE` | `uint8_t` | 8-bit | 8-bit bit string |
| `IEC_WORD` | `uint16_t` | 16-bit | 16-bit bit string |
| `IEC_DWORD` | `uint32_t` | 32-bit | 32-bit bit string |
| `IEC_LWORD` | `uint64_t` | 64-bit | 64-bit bit string |

### String Type

| IEC Type | C Struct | Description |
|----------|----------|-------------|
| `IEC_STRING` | `struct { int8_t len; uint8_t body[126]; }` | Fixed-size string buffer |

> **Tip:** `IEC_BOOL` is `uint8_t`, not the C++ `bool` type. Use `0` for FALSE and `1` (or any nonzero value) for TRUE. When comparing, always compare against `0` rather than against `1`.

## String Handling

The `IEC_STRING` type is a fixed-size struct, not a null-terminated C string. To work with it in C++:

```cpp
void loop() {
    // Reading a string variable (declared as STRING in the Variables Table)
    int length = MY_STRING.len;
    // Access individual characters: MY_STRING.body[0] through MY_STRING.body[length - 1]

    // Writing to a string variable
    const char *msg = "HELLO";
    MY_STRING.len = 5;
    for (int i = 0; i < 5; i++) {
        MY_STRING.body[i] = msg[i];
    }
}
```

The maximum string length is 126 bytes (the size of the `body` array). Always set the `len` field to reflect the actual content length.

## Arduino Conditional Compilation

When your target hardware is an Arduino-compatible board, the build adds the `ARDUINO` macro so you can use the Arduino API:

```cpp
#ifdef ARDUINO
#include <Arduino.h>
#endif
```

When the `ARDUINO` macro is defined (i.e., the build targets Arduino hardware), you get access to the full Arduino API:

- **Core functions**: `pinMode()`, `digitalWrite()`, `digitalRead()`, `analogWrite()`, `analogRead()`, `delay()`, `millis()`, `micros()`
- **Serial communication**: `Serial.begin()`, `Serial.print()`, `Serial.read()`, `Serial.available()`
- **I2C (Wire)**: `Wire.begin()`, `Wire.requestFrom()`, `Wire.read()`, `Wire.write()`
- **SPI**: `SPI.begin()`, `SPI.transfer()`, `SPI.beginTransaction()`
- **EEPROM**: `EEPROM.read()`, `EEPROM.write()`, `EEPROM.update()`

When targeting non-Arduino platforms (Linux, Raspberry Pi, etc.), the `ARDUINO` macro is not defined and Arduino-specific code is excluded.

> **Tip:** Use `#ifdef ARDUINO` guards to write portable code that works on both Arduino and Linux targets:

```cpp
void setup() {
    #ifdef ARDUINO
    pinMode(13, OUTPUT);
    Serial.begin(9600);
    #endif
    OUTPUT_READY = 1;
}

void loop() {
    #ifdef ARDUINO
    digitalWrite(13, ENABLE ? HIGH : LOW);
    #endif
    STATUS = ENABLE;
}
```

## Complete Example with Variables

Here's a full example: a C++ function block that implements a debounced digital input reader.

**Variables Table:**

| Name | Class | Type | Description |
|------|-------|------|-------------|
| RAW_INPUT | Input | BOOL | Raw digital input signal |
| DEBOUNCE_MS | Input | INT | Debounce time in milliseconds |
| STABLE_OUTPUT | Output | BOOL | Debounced output signal |
| IS_CHANGING | Output | BOOL | TRUE while input is bouncing |

**C++ Code:**

```cpp
#include <stdlib.h>

unsigned long lastChangeTime = 0;
int lastState = 0;
int stableState = 0;

unsigned long getTimeMs() {
    #ifdef ARDUINO
    return millis();
    #else
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (unsigned long)(ts.tv_sec * 1000 + ts.tv_nsec / 1000000);
    #endif
}

void setup() {
    lastChangeTime = getTimeMs();
    lastState = 0;
    stableState = 0;
    STABLE_OUTPUT = 0;
    IS_CHANGING = 0;
}

void loop() {
    unsigned long now = getTimeMs();
    int currentInput = RAW_INPUT ? 1 : 0;

    if (currentInput != lastState) {
        lastChangeTime = now;
        lastState = currentInput;
        IS_CHANGING = 1;
    }

    if ((now - lastChangeTime) >= (unsigned long)DEBOUNCE_MS) {
        if (currentInput != stableState) {
            stableState = currentInput;
            STABLE_OUTPUT = stableState;
        }
        IS_CHANGING = 0;
    }
}
```

This example demonstrates several important patterns:

- Using `#ifdef ARDUINO` for cross-platform timing
- Persistent state in global variables across scan cycles
- Reading IEC inputs and writing IEC outputs through the generated macros
- Casting between IEC types and standard C types

---

## What's Next?

Explore the editor features that make writing C++ code easier, including code completion, snippets, and Arduino API suggestions: [C++ Editor Features](cpp-completion).
