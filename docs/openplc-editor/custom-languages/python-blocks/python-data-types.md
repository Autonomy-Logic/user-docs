# Python Data Types: Structures, Enumerations and Arrays

A Python function block is not limited to single numbers and strings. Any structure, enumeration or array you declare in the Variables Table crosses into your script as an ordinary Python object — a class instance, an `IntEnum` member, or a list. You never unpack bytes yourself.

This page shows what each IEC type looks like on the Python side, and how to read and write it.

## The One Rule That Explains Everything

> **Tip:** Every variable in the Variables Table becomes a plain Python global with the **same name and the same spelling** you typed. Structure members keep their declared spelling too.

If the Variables Table says `motor : Motor` and `Motor` has a member `speed`, then in Python you write `motor.speed` — lowercase, exactly as declared. This matters because C++ blocks are different: there, the compiler uppercases everything, so the same member is `motor.SPEED`. Two languages, two spellings, one Variables Table.

## Base Types

| IEC Type | Python Type |
|---|---|
| `BOOL` | `bool` |
| `SINT`, `INT`, `DINT`, `LINT` | `int` |
| `USINT`, `UINT`, `UDINT`, `ULINT` | `int` |
| `BYTE`, `WORD`, `DWORD`, `LWORD` | `int` |
| `REAL`, `LREAL` | `float` |
| `STRING` | `str` |
| `WSTRING` | `str` |
| `TIME`, `DATE`, `TOD`, `DT` | `int` (see [Temporal types](#temporal-types)) |

## Structures

A structure declared in the Data Types editor becomes a Python **class** with one attribute per member.

Given a structure `Motor`:

| Member | Type |
|---|---|
| `speed` | `INT` |
| `label` | `STRING` |
| `trims` | `ARRAY [0..2] OF INT` |

and a Variables Table entry `mot : Motor` (Input), the class is generated for you and `mot` is already an instance when `block_loop()` runs:

```python
def block_loop():
    global out_speed, out_label

    out_speed = mot.speed          # 12
    out_label = mot.label          # 'mot-lbl'
    first_trim = mot.trims[1]      # nested array member
```

### Writing a structure output

Construct the class by name and assign it. The class is defined above your code, so you can use it freely:

```python
def block_loop():
    global result                  # result : Motor (Output)

    result = Motor()
    result.speed = 55
    result.label = 'py-written'
    result.trims = [1, 2, 3]
```

> **Warning:** `Motor()` starts with its attributes unset. Assign every member you care about. A member you never assign keeps whatever the output held before.

You can also modify an input structure and assign it onward — the input is a normal Python object, and changing it does not affect the PLC-side input:

```python
def block_loop():
    global result
    mot.speed = mot.speed + 1      # local change only
    result = mot                   # ...but this reaches the PLC
```

## Enumerations

An enumeration becomes a Python [`IntEnum`](https://docs.python.org/3/library/enum.html#enum.IntEnum) with the member names you declared.

Given `Mode : (STOPPED, RUNNING, MANUAL)` and `mode : Mode` (Input):

```python
def block_loop():
    global label, number, running

    label   = mode.name            # 'RUNNING'
    number  = int(mode)            # 1
    running = (mode == Mode.RUNNING)

    if mode is Mode.MANUAL:
        pass
```

Because it is an `IntEnum`, a member compares equal to its integer value, so `mode == 1` also works. Prefer the named form — it survives someone reordering the enumeration.

### Writing an enumeration output

Assign a member of the generated class:

```python
def block_loop():
    global state                   # state : Mode (Output)
    state = Mode.MANUAL
```

Assigning a bare integer works too, but nothing checks it is in range, so a typo becomes a silently invalid enumeration value on the PLC side. Use the named member.

## Arrays

An array becomes a Python **list**.

```python
# names : ARRAY [0..1] OF STRING (Input)
def block_loop():
    global joined
    joined = names[0] + '/' + names[1]
    count  = len(names)            # 2
```

### IEC indices are preserved — mind the lower bound

This is the one place where Python's view differs from what you might expect.

> **Warning:** The list is indexed by the **IEC index**, not from zero. An `ARRAY [1..2] OF INT` becomes a list of length **3**, where index `0` is `None` and the real elements are at `1` and `2`.

```python
# grid : ARRAY [1..2, 0..2] OF INT (Input)
def block_loop():
    global first
    first = grid[1][0]             # the IEC element grid[1,0]
    # grid[0]   is None — there is no IEC element 0
    # len(grid) is 3, not 2
```

So `for row in grid:` will hand you `None` first. Iterate over the declared range instead:

```python
total = 0
for i in range(1, 3):              # IEC bounds 1..2
    for j in range(0, 3):          # IEC bounds 0..2
        total += grid[i][j]
```

An array declared `[0..n]` has no hole, so it iterates naturally. Declaring your arrays from `0` is the simplest way to avoid the whole question.

### Multi-dimensional arrays

Rank 2 and rank 3 arrive as nested lists, indexed one bracket per dimension:

```python
# grid : ARRAY [1..2, 0..2] OF INT
value = grid[2][1]                 # IEC grid[2,1]
```

Rank 4 and beyond cannot cross into a Python block; the build refuses them with a message naming the variable.

### Arrays of structures

A list of class instances, exactly as you would expect:

```python
# bank : ARRAY [0..1] OF Motor (Input)
def block_loop():
    global total
    total = bank[0].speed + bank[1].speed
    name  = bank[1].label
```

### Arrays of enumerations

A list of `IntEnum` members:

```python
# modes : ARRAY [0..1] OF Mode (Input)
if modes[1] is Mode.MANUAL:
    pass
```

### Writing an array output

Assign a whole list, or write elements in place:

```python
def block_loop():
    global names_out, grid_out, bank_out

    names_out = ['first', 'second']            # whole list

    grid_out = [None, [10, 11, 12], [20, 21, 22]]   # note the None at index 0
                                                    # for a [1..2] lower bound

    m = Motor()
    m.speed = 88
    m.label = 'bank-py'
    m.trims = [0, 0, 7]
    bank_out = [m, m]
```

> **Warning:** Keep the declared length. The PLC-side array is fixed size, so only the declared elements are copied back — a longer list is truncated and a shorter one leaves the remaining elements at their previous values. `append()` and `pop()` on an output list do not grow or shrink the PLC array.

## Strings

`STRING` and `WSTRING` are ordinary Python `str`. Nothing special is required:

```python
def block_loop():
    global message
    message = 'temp=' + str(reading)
```

> **Warning:** Strings crossing the boundary are capped at **126 characters**. A longer value is truncated at the boundary, not rejected — check `len()` yourself if the full value matters.

## Temporal Types

`TIME`, `DATE`, `TOD` and `DT` arrive as integers, and the unit depends on the type:

| IEC Type | Python value |
|---|---|
| `TIME` | nanoseconds |
| `TOD` (`TIME_OF_DAY`) | nanoseconds since midnight |
| `DT` (`DATE_AND_TIME`) | nanoseconds since the epoch |
| `DATE` | **days** since the epoch |

`DATE` being days rather than nanoseconds is the one that catches people:

```python
import datetime

def block_loop():
    global day_name
    day_name = (datetime.date(1970, 1, 1) + datetime.timedelta(days=start_date)).isoformat()
```

## Function Block Instances

A function block instance declared on a Python POU is called for you, once per PLC scan, by the generated wrapper. From Python you read and write its pins by name.

> **Warning:** Declare the instance under **`VAR`** (Local), not Input. Only a Local or In/Out instance can be *driven* from Python. Declared as an Input, all four pins still arrive — you can read `Q` and `ET` — but your writes to `IN` and `PT` never reach the PLC, so the timer sits at zero and nothing tells you why.

```python
# ton0 : TON (Local)
def block_loop():
    global elapsed, done
    ton0.IN = True
    ton0.PT = 5_000_000_000        # TIME is nanoseconds — 5 s
    elapsed = ton0.ET              # counts up: 3s100ms, 4s400ms, ...
    done    = ton0.Q               # True once ET reaches PT
```

Only the pins that make sense in each direction are exchanged: `IN` and `PT` travel out to the PLC, `Q` and `ET` come back. You do not have to think about which — write the ones the block takes, read the ones it produces.

> **Tip:** Pin names on a function block instance are **uppercase**, because that is how the standard library declares them (`IN`, `PT`, `Q`, `ET`). Structure members you declared yourself keep your spelling. When unsure, use the code completion — see [Python Language Server](/docs/openplc-editor/custom-languages/python-blocks/python-language-server).

Because the instance is evaluated on the PLC scan and your block runs on its own ~100 ms loop, **outputs lag by one exchange**: `ton0.Q` inside `block_loop()` is the value from the previous cycle. That is correct for timers and counters, which are driven by the scan rather than by your loop.

Gate an instance with `EN` and read `ENO` back:

```python
ton0.EN = enable_flag              # False: not evaluated this scan
was_run = ton0.ENO
```

## What Cannot Cross

The build refuses these with a message naming the variable, rather than producing a block that misreads memory:

| Declaration | Why |
|---|---|
| Rank 4 or higher array | The compiler declares array containers up to rank 3 |
| A named `ARRAY` type (an alias declared in Data Types) | Not supported yet — declare the array inline on the variable instead |
| A structure that nests too deeply, or refers to itself | The layout cannot be enumerated |
| `VAR_TEMP` | Has no meaning in a process that outlives the scan — use `VAR` |

## Complete Example

A block that takes a bank of motors, finds the fastest, and reports it as a structure and an enumeration:

```python
import os
import time
import struct
from multiprocessing import shared_memory


def block_init():
    pass


def block_loop():
    global fastest, state, fastest_index

    best = 0
    for i in range(len(bank)):
        if bank[i].speed > bank[best].speed:
            best = i

    fastest_index = best

    fastest = Motor()
    fastest.speed = bank[best].speed
    fastest.label = bank[best].label
    fastest.trims = list(bank[best].trims)

    if bank[best].speed == 0:
        state = Mode.STOPPED
    elif manual_request:
        state = Mode.MANUAL
    else:
        state = Mode.RUNNING
```

Variables Table for the example:

| Name | Class | Type |
|---|---|---|
| `bank` | Input | `ARRAY [0..3] OF Motor` |
| `manual_request` | Input | `BOOL` |
| `fastest` | Output | `Motor` |
| `state` | Output | `Mode` |
| `fastest_index` | Output | `INT` |

Note `list(bank[best].trims)` rather than `bank[best].trims` — assigning the list directly would make the output share the input's list object. It still works, but copying keeps the two independent if you later modify one.

## What's Next?

- [Python Block Structure](/docs/openplc-editor/custom-languages/python-blocks/python-structure) — the two functions and how variables reach your script
- [Python Variable Restrictions](/docs/openplc-editor/custom-languages/python-blocks/python-restrictions) — the execution model and its limits
- [C++ Data Types](/docs/openplc-editor/custom-languages/cpp-blocks/cpp-data-types) — the same types, on the C++ side
