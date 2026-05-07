# C++ Editor Features

The Autonomy Edge IDE provides a rich editing experience for C++ function blocks. When you open a C++ function block, you get syntax highlighting, intelligent code completion, signature help, and code snippets that help you write correct code faster.

## Editor Basics

The C++ code editor provides:

- **Syntax highlighting** — Keywords, types, strings, numbers, comments, and preprocessor directives are color-coded for easy reading.
- **Bracket matching** — Matching braces, parentheses, and brackets are highlighted when your cursor is next to one.
- **Auto-closing** — Opening braces, parentheses, brackets, and quotes automatically insert their closing counterpart.
- **Indentation** — The editor automatically indents code inside blocks, functions, and control structures.
- **Code folding** — Collapse and expand function bodies, conditional blocks, and other code regions.

These features work out of the box with no configuration required.

## Code Completion

The IDE includes a comprehensive completion provider that offers intelligent suggestions as you type. Press `Ctrl+Space` (or `Cmd+Space` on macOS) to manually trigger the completion menu at any time.

The completion provider draws from four sources:

### 1. Standard C/C++ Library Functions

The editor suggests functions from commonly used standard library headers:

**stdio.h** — Standard input/output:

| Function | Description |
|----------|-------------|
| `printf()` | Formatted output to stdout |
| `sprintf()` | Formatted output to a string buffer |
| `snprintf()` | Formatted output with buffer size limit |
| `sscanf()` | Formatted input from a string |

**stdlib.h** — General utilities:

| Function | Description |
|----------|-------------|
| `abs()` | Absolute value (integer) |
| `atoi()` | Convert string to integer |
| `atof()` | Convert string to float |
| `malloc()` | Allocate memory |
| `free()` | Deallocate memory |
| `rand()` | Generate pseudo-random number |
| `srand()` | Seed the random number generator |

**string.h** — String and memory operations:

| Function | Description |
|----------|-------------|
| `memcpy()` | Copy memory block |
| `memset()` | Fill memory with a value |
| `strcmp()` | Compare two strings |
| `strlen()` | Get string length |
| `strcpy()` | Copy a string |
| `strcat()` | Concatenate strings |

**math.h** — Mathematical functions:

| Function | Description |
|----------|-------------|
| `sin()`, `cos()`, `tan()` | Trigonometric functions |
| `asin()`, `acos()`, `atan()` | Inverse trigonometric functions |
| `sqrt()` | Square root |
| `pow()` | Power (base, exponent) |
| `log()`, `log10()` | Natural and base-10 logarithm |
| `fabs()` | Absolute value (floating point) |
| `floor()`, `ceil()` | Round down / round up |
| `fmod()` | Floating point modulo |

### 2. Arduino API Functions

When your project targets Arduino-compatible hardware, the completion provider also suggests Arduino API functions:

**Core Functions:**

| Function | Description |
|----------|-------------|
| `pinMode(pin, mode)` | Configure a pin as INPUT, OUTPUT, or INPUT_PULLUP |
| `digitalWrite(pin, value)` | Write HIGH or LOW to a digital pin |
| `digitalRead(pin)` | Read the state of a digital pin |
| `analogRead(pin)` | Read an analog input (0–1023) |
| `analogWrite(pin, value)` | Write a PWM value (0–255) to a pin |
| `delay(ms)` | Pause execution for milliseconds |
| `delayMicroseconds(us)` | Pause execution for microseconds |
| `millis()` | Milliseconds since program started |
| `micros()` | Microseconds since program started |

**Serial Communication:**

| Function | Description |
|----------|-------------|
| `Serial.begin(baud)` | Initialize serial at given baud rate |
| `Serial.print(data)` | Print data to serial port |
| `Serial.println(data)` | Print data followed by newline |
| `Serial.read()` | Read one byte from serial buffer |
| `Serial.available()` | Number of bytes available to read |
| `Serial.write(data)` | Write binary data to serial port |

**I2C (Wire Library):**

| Function | Description |
|----------|-------------|
| `Wire.begin()` | Initialize I2C as controller |
| `Wire.begin(address)` | Initialize I2C as peripheral |
| `Wire.requestFrom(addr, qty)` | Request bytes from a peripheral |
| `Wire.beginTransmission(addr)` | Begin transmission to peripheral |
| `Wire.write(data)` | Queue data for transmission |
| `Wire.endTransmission()` | Send queued data |
| `Wire.read()` | Read one byte from receive buffer |

**SPI Library:**

| Function | Description |
|----------|-------------|
| `SPI.begin()` | Initialize SPI bus |
| `SPI.transfer(data)` | Send and receive one byte |
| `SPI.beginTransaction(settings)` | Begin SPI transaction with settings |
| `SPI.endTransaction()` | End SPI transaction |

**EEPROM Library:**

| Function | Description |
|----------|-------------|
| `EEPROM.read(address)` | Read one byte from EEPROM |
| `EEPROM.write(address, value)` | Write one byte to EEPROM |
| `EEPROM.update(address, value)` | Write only if value has changed |

### 3. Code Snippets

The editor provides code snippets for common C++ patterns. Type a snippet prefix and select it from the completion menu to insert a template with tab stops.

| Prefix | Expands To |
|--------|------------|
| `if` | `if` statement with braces |
| `ifelse` | `if/else` statement with braces |
| `for` | `for` loop with counter |
| `while` | `while` loop |
| `dowhile` | `do/while` loop |
| `switch` | `switch/case` statement |
| `struct` | Struct definition |
| `function` | Function definition with return type |

For example, typing `for` and selecting the snippet produces:

```cpp
for (int i = 0; i < count; i++) {
    // body
}
```

The cursor is positioned at the first tab stop (`i`), and you can press Tab to jump to the next editable position.

### 4. Local Variable Parsing

The completion provider analyzes your code in real time and extracts locally declared variables. Variables you define in your C++ code (not just those in the Variables Table) appear in the completion suggestions.

The parser recognizes common declaration patterns including:

- Simple declarations: `int x = 0;`
- Pointer declarations: `float *ptr;`
- Array declarations: `int buffer[100];`
- Const declarations: `const int MAX_SIZE = 50;`

## Signature Help

When you type an opening parenthesis `(` after a known function name, the editor displays a **signature help** popup showing the function's parameters, their types, and a brief description. As you type each argument and add commas, the popup highlights the current parameter.

For example, typing `pinMode(` displays:

```
pinMode(pin: uint8_t, mode: uint8_t)
  pin  - The pin number to configure
  mode - INPUT, OUTPUT, or INPUT_PULLUP
```

Signature help is available for standard C/C++ library functions and Arduino API functions.

## Tips for Effective C++ Editing

### Use Tab Completion

Instead of typing full function names, type the first few characters and press `Tab` or `Enter` to accept the highlighted completion. This reduces typos and speeds up coding.

### Leverage the Variables Table

Variables declared in the Variables Table are always available in your code by name. If a variable name doesn't autocomplete, check that it's properly defined in the Variables Table.

### Watch for Type Mismatches

The IEC types map to specific C types (see [C++ Function Block Structure](/docs/openplc-editor/custom-languages/cpp-blocks/cpp-structure) for the full table). Common pitfalls:

- `IEC_BOOL` is `uint8_t`, not C++ `bool`. Use `0` and `1`, not `false` and `true`.
- `IEC_INT` is `int16_t` (16-bit), not `int` (typically 32-bit). Arithmetic overflow can occur at 32,767.
- `IEC_REAL` is `float` (32-bit), not `double`. Use `f` suffix for float literals (e.g., `3.14f`) to avoid implicit conversion warnings.

### Keep Code Organized

Even though all your C++ code goes into a single `loop()` function, you can define helper functions and call them from `loop()`:

```cpp
float clamp(float value, float minVal, float maxVal) {
    if (value < minVal) return minVal;
    if (value > maxVal) return maxVal;
    return value;
}

void setup() {
    OUTPUT = 0.0;
}

void loop() {
    OUTPUT = clamp(INPUT * GAIN, 0.0f, 100.0f);
}
```

Helper functions, global variables, struct definitions, and `#define` constants can all be placed above `setup()` and `loop()`.

### Use Preprocessor Guards for Arduino Code

If your function block might run on both Arduino and non-Arduino targets, wrap Arduino-specific code in `#ifdef ARDUINO` guards:

```cpp
void setup() {
    #ifdef ARDUINO
    Serial.begin(9600);
    pinMode(LED_PIN, OUTPUT);
    #endif
}
```

This prevents build errors when targeting Linux or other non-Arduino platforms.

---

## What's Next?

Learn how to declare and manage variables for all POU types, including the variable classes, data types, and editor features: [Local Variables](/docs/openplc-editor/working-with-variables/local-variables).
