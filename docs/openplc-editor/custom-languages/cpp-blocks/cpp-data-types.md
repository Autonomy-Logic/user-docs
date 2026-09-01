# C++ Data Types: Structures, Enumerations and Arrays

A C++ function block reaches its variables directly — nothing is copied or serialised. A structure in the Variables Table is a real C++ `struct` in your code, an array is a real container, an enumeration is a real `enum class`. This page shows the spelling for each.

For `STRING` and `WSTRING`, see [Working with STRING and WSTRING](/docs/openplc-editor/custom-languages/cpp-blocks/cpp-structure#working-with-string-and-wstring) on the structure page.

## The One Rule That Explains Everything

> **Warning:** The IEC compiler **uppercases every identifier**. A structure member declared `speed` is `SPEED` in your C++ code. An enumeration value declared `Running` is `RUNNING`.

The variable's own name is the exception: the block's pins are bound under the exact spelling from the Variables Table, so `motor` stays `motor` while its member becomes `motor.SPEED`.

This is the opposite of a Python block, where members keep their declared spelling. If you are porting logic between the two, expect to change the case of every member access.

## Structures

Given a structure `Motor` with members `speed : INT`, `label : STRING` and `trims : ARRAY [0..2] OF INT`, and a Variables Table entry `mot : Motor`:

```cpp
void loop()
{
    int16_t s = mot.SPEED;             // member: UPPERCASE
    out_label = mot.LABEL;             // a STRING member behaves like a STRING pin
    int16_t t = mot.TRIMS[1];          // nested array member
}
```

Writing a structure output is the same, member by member:

```cpp
void loop()
{
    result.SPEED    = 111;
    result.LABEL    = "written";
    result.TRIMS[2] = 77;
}
```

The type name itself is available if you need to declare your own local of that type, or write a helper:

```cpp
static void copy_motor(MOTOR &dst, const MOTOR &src)
{
    dst.SPEED = src.SPEED;
    dst.LABEL = src.LABEL;
    for (int k = 0; k <= 2; k++) {
        dst.TRIMS[k] = src.TRIMS[k];
    }
}

void loop()
{
    copy_motor(result, mot);
}
```

> **Tip:** The struct type is spelled in uppercase too — `MOTOR`, not `Motor`.

## Enumerations

An enumeration becomes a C++ `enum class` whose values are uppercase.

Given `Mode : (STOPPED, RUNNING, MANUAL)` and `mode : Mode`:

```cpp
void loop()
{
    // A scalar enumeration pin converts implicitly to the raw enum
    MODE current = mode;

    if (current == MODE::RUNNING) {
        // ...
    }

    // For the numeric value, cast the raw enum
    out_number = static_cast<int32_t>(current);
}
```

Writing one:

```cpp
void loop()
{
    state = MODE::MANUAL;              // state : Mode (Output)
}
```

> **Warning:** `mode.get()` does **not** give you the raw enum — it returns an internal wrapper, and casting that to `int` fails to compile with *invalid cast from type `IEC_ENUM_Value<MODE>`*. Assign to a `MODE` variable first, as above, and cast that.

## Arrays

How you index an array depends on its rank, because the compiler uses a different container for each.

### One dimension — square brackets

A 1-D array pin arrives as a pointer to its first element, with the IEC lower bound already folded in. Index it with the IEC index directly:

```cpp
// names : ARRAY [0..1] OF STRING
// bank  : ARRAY [0..1] OF Motor
// trims : ARRAY [1..3] OF INT
void loop()
{
    out_first = names[0];
    out_label = bank[1].LABEL;         // array of structures
    int16_t t = trims[1];              // declared [1..3] — index 1 is the first element
}
```

Because the lower bound is folded in, you always use the index you declared. A `[1..3]` array is read at `1`, `2`, `3` — never at `0`.

> **Warning:** There is no bounds check and no length. `names[7]` on a two-element array compiles and reads whatever follows it in memory. Loop over the bounds you declared.

### Two and three dimensions — parentheses

Rank 2 and rank 3 arrays are container objects, and their element accessor is `operator()`, not `[]`:

```cpp
// grid : ARRAY [1..2, 0..2] OF INT
void loop()
{
    int16_t sum = 0;
    for (int i = 1; i <= 2; i++) {
        for (int j = 0; j <= 2; j++) {
            sum = sum + grid(i, j);    // parentheses, one call, both indices
        }
    }
    total = sum;
}
```

Writing is the same shape:

```cpp
grid_out(2, 1) = 42;
```

> **Warning:** `grid[i][j]` does not compile for a multi-dimensional array. Use `grid(i, j)`.

### Arrays of enumerations

An element of an enumeration array is already the raw `enum class` — no conversion needed:

```cpp
// modes : ARRAY [0..1] OF Mode
if (modes[1] == MODE::MANUAL) {
    // ...
}
out_number = static_cast<int32_t>(modes[1]);

modes_out[0] = MODE::MANUAL;           // writing
```

This differs from a *scalar* enumeration pin, which needs the assignment-to-`MODE` step shown above. The array element skips it.

### Arrays of strings

Each element behaves like a STRING pin:

```cpp
// names : ARRAY [0..1] OF STRING
out_len   = (int32_t)names[0].length();
names_out[0] = "first";
names_out[1] = other_string;
```

## Quick Reference

| Declaration | Read | Write |
|---|---|---|
| `mot : Motor` | `mot.SPEED` | `mot.SPEED = 1;` |
| `mot : Motor` (string member) | `mot.LABEL` | `mot.LABEL = "x";` |
| `mode : Mode` | `MODE m = mode;` | `mode = MODE::RUNNING;` |
| `a : ARRAY [0..3] OF INT` | `a[2]` | `a[2] = 5;` |
| `a : ARRAY [1..3] OF INT` | `a[1]` (first element) | `a[1] = 5;` |
| `g : ARRAY [1..2, 0..2] OF INT` | `g(i, j)` | `g(i, j) = 5;` |
| `b : ARRAY [0..1] OF Motor` | `b[1].LABEL` | `b[1].SPEED = 9;` |
| `m : ARRAY [0..1] OF Mode` | `m[1]` (raw enum) | `m[1] = MODE::MANUAL;` |
| `n : ARRAY [0..1] OF STRING` | `n[0].length()` | `n[0] = "x";` |

## Temporal Types

`TIME`, `TOD` and `DT` are 64-bit **nanosecond** counts; `DATE` is a count of **days**:

```cpp
// pulse : TIME, today : DATE
int64_t ns   = pulse;
int64_t days = today;

if (pulse > 5000000000LL) {            // longer than 5 seconds
    // ...
}
```

## Function Block Instances

An instance is a real object: set its input pins, **call it**, then read its outputs — and its pins are uppercase like every other member. The call is what makes it advance, and forgetting it is silent.

See [Function Block Instances](/docs/openplc-editor/custom-languages/cpp-blocks/cpp-structure#function-block-instances) on the structure page for the full treatment, including how this differs from a Python block.

## A Note on `IEC_BOOL`

`BOOL` is `uint8_t`, not the C++ `bool`. Assign `0` or `1`, and compare against `0` rather than against `1`:

```cpp
flag = 1;
if (other_flag != 0) {
    // ...
}
```

## Complete Example

A block that scans a bank of motors, reports the fastest as a structure, and classifies the result as an enumeration:

```cpp
static void copy_motor(MOTOR &dst, const MOTOR &src)
{
    dst.SPEED = src.SPEED;
    dst.LABEL = src.LABEL;
    for (int k = 0; k <= 2; k++) {
        dst.TRIMS[k] = src.TRIMS[k];
    }
}

void setup()
{
}

void loop()
{
    int best = 0;
    for (int i = 0; i <= 3; i++) {
        if (bank[i].SPEED > bank[best].SPEED) {
            best = i;
        }
    }

    fastest_index = (int16_t)best;
    copy_motor(fastest, bank[best]);

    if (bank[best].SPEED == 0) {
        state = MODE::STOPPED;
    } else if (manual_request != 0) {
        state = MODE::MANUAL;
    } else {
        state = MODE::RUNNING;
    }
}
```

Variables Table for the example:

| Name | Class | Type |
|---|---|---|
| `bank` | Input | `ARRAY [0..3] OF Motor` |
| `manual_request` | Input | `BOOL` |
| `fastest` | Output | `Motor` |
| `state` | Output | `Mode` |
| `fastest_index` | Output | `INT` |

## What's Next?

- [C++ Block Structure](/docs/openplc-editor/custom-languages/cpp-blocks/cpp-structure) — the two functions, the type mapping, and STRING handling
- [C++ Code Completion](/docs/openplc-editor/custom-languages/cpp-blocks/cpp-completion) — member completion in the editor
- [Python Data Types](/docs/openplc-editor/custom-languages/python-blocks/python-data-types) — the same types, on the Python side
