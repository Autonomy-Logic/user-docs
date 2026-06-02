# C++ Function Block Structure

This page covers the two functions every C++ block contains, the type that each variable in the Variables Table becomes in your C++ code, and how to write portable code that compiles for both Arduino and non-Arduino targets.

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

The signatures must match exactly. No parameters, no return value. If either function is missing, the build fails.

## Variables: Name in the Table = Name in the Code

Variables you declare in the Variables Table. Inputs and Outputs (the only two classes available for C++ blocks). Are plain C++ variables inside `setup()` and `loop()`, using the exact names from the table. Internal state stays in your C++ source: declare ordinary variables at file scope above `setup()`/`loop()` to persist them between scan cycles, or inside the functions for scratch values.

```cpp
// With ENABLE (BOOL Input), SPEED (INT Input), MOTOR_ON (BOOL Output) declared in the table:

void loop() {
    if (ENABLE && SPEED > 0) {
        MOTOR_ON = 1;
    } else {
        MOTOR_ON = 0;
    }
}
```

When another POU instantiates your function block, it behaves exactly like any IEC function block. The inputs and outputs you declared in the Variables Table are its interface.

## IEC ↔ C Type Mapping

The IEC type you pick in the Variables Table determines the C type your variable has in code. You'll mostly think in IEC terms, but the mapping matters when you call standard library functions or interface with hardware libraries.

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

### String Types

| IEC Type | Capacity | Element Type | Notes |
|----------|----------|--------------|-------|
| `IEC_STRING` | 254 chars | `char` (UTF-8 / ASCII) | Fixed-size string with automatic length tracking |
| `IEC_WSTRING` | 254 chars | `char16_t` (UTF-16) | Wide-character variant of `IEC_STRING` |

`IEC_STRING` and `IEC_WSTRING` variables behave like small string objects (similar in feel to `std::string`, but with a fixed capacity and no heap allocation). Length tracking and the trailing null terminator are handled for you. You read with `.length()` / `.c_str()` / `[i]` and write with `=` / `.get()` + mutate + assign-back.

> **Tip:** `IEC_BOOL` is `uint8_t`, not the C++ `bool` type. Use `0` for FALSE and `1` (or any nonzero value) for TRUE. When comparing, always compare against `0` rather than against `1`.

## Working with STRING and WSTRING

A STRING variable from the Variables Table is exposed in your C++ code as a string-like object. You don't manipulate length and bytes directly — instead the variable handles bookkeeping (length, null terminator) and gives you a small set of methods to read and mutate it. The same patterns apply to WSTRING, just with `char16_t` instead of `char` and `u""` literals instead of `""`.

### Reading

```cpp
size_t len     = MY_STRING.length();   // current length (number of chars)
const char* p  = MY_STRING.c_str();    // null-terminated C string, read-only
char c         = MY_STRING[3];         // single character, by value
```

`c_str()` is the bridge to anything that takes a C string — `printf`, `strcmp`, `Serial.print`, etc. The pointer it returns stays valid until the next time you write to the variable, so don't hold onto it across an assignment.

### Assigning a whole string

You can assign directly from a C string literal, another STRING variable, or any null-terminated `char*` buffer:

```cpp
MY_STRING = "Hello";              // from a literal
MY_STRING = OTHER_STRING;         // copy from another STRING

char buf[64];
snprintf(buf, sizeof(buf), "count=%d", count);
MY_STRING = buf;                  // from a null-terminated C buffer
```

If the source is longer than the variable's capacity (254 characters), it's truncated.

### Changing characters in the middle

The pin variable's `[]` returns a character by value — read-only. To mutate, grab the underlying buffer with `.get()`, change it, and assign back:

```cpp
strucpp::IECString<254> buf = MY_STRING.get();   // copy into a local buffer
buf[3] = 'X';                                    // mutable indexing
buf[4] = buf[4] + 1;                             // tweak in place
MY_STRING = buf;                                 // write back
```

`buf` is an independent copy — changes to it don't touch `MY_STRING` until you assign. This is also what protects you from partial writes: if your C++ code throws, returns, or aborts mid-mutation, the variable still holds its previous value.

### Concatenating

The local buffer supports `+=` for both C strings and other STRING variables, and `.append()` for a single character:

```cpp
strucpp::IECString<254> buf = MY_STRING.get();
buf += " world";                                 // append a literal
buf += OTHER_STRING.get();                       // append another STRING
buf.append('!');                                 // append one character
MY_STRING = buf;
```

Building from scratch works the same way — start with an empty buffer and append:

```cpp
strucpp::IECString<254> result;
result = "Hello, ";
result += NAME.get();
result += '!';
GREETING = result;
```

### Converting a C buffer to STRING

A plain `char` array with a null terminator can be assigned directly:

```cpp
char received[128];
size_t n = Serial.readBytesUntil('\n', received, sizeof(received) - 1);
received[n] = '\0';
MY_STRING = received;
```

If your buffer isn't null-terminated (e.g. fixed-size frame data), construct an `IECString` with an explicit length:

```cpp
char frame[16];
read_packet(frame);                              // not null-terminated
MY_STRING = strucpp::IECString<254>(frame, 16);
```

### Converting STRING to a C buffer

`c_str()` gives you a null-terminated pointer you can read directly. To copy bytes out into a buffer of your own, use the standard `strncpy` / `memcpy` pattern:

```cpp
char dest[128];
strncpy(dest, MY_STRING.c_str(), sizeof(dest) - 1);
dest[sizeof(dest) - 1] = '\0';                   // belt-and-suspenders terminator
```

### Comparing

Equality and inequality work directly against literals and other STRING variables:

```cpp
if (COMMAND == "STOP") { /* ... */ }
if (COMMAND != PREVIOUS) { /* ... */ }
```

For ordering (`<`, `<=`, `>`, `>=`), compare the underlying buffers via `.get()`:

```cpp
if (MY_STRING.get() < OTHER.get()) { /* lexicographic */ }
```

### WSTRING — same shape, wide characters

WSTRING variables behave identically but store `char16_t` (UTF-16). Use the `u""` prefix for literals and `strucpp::IECWString<254>` for the local buffer type:

```cpp
W_STRING = u"Hello";
const char16_t* p = W_STRING.c_str();
char16_t c        = W_STRING[0];

strucpp::IECWString<254> buf = W_STRING.get();
buf[0] = u'X';
buf += u" suffix";
W_STRING = buf;
```

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
- Reading inputs and writing outputs by name, just like any IEC variable
- Mixing IEC types and standard C types in the same expression

---

## What's Next?

Explore the editor features that make writing C++ code easier, including code completion, snippets, and Arduino API suggestions: [C++ Editor Features](/docs/openplc-editor/custom-languages/cpp-blocks/cpp-completion).
