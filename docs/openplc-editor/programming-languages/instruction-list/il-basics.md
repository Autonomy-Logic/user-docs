# IL Language Basics

Instruction List (IL) is a low-level text-based programming language defined in the IEC 61131-3 standard. It works like assembly language for PLCs — each line contains a single instruction that operates on an **accumulator** register. IL is the most compact IEC language but also the least readable, making it best suited for simple programs or legacy migration.

> **Note:** IL was deprecated in the IEC 61131-3 third edition (2013) in favor of Structured Text. The Autonomy Edge IDE supports IL for backward compatibility, but for new projects, Structured Text is recommended.

## How IL Works

IL uses an **accumulator-based** execution model. There's a single implicit register (the "current result" or accumulator) that every instruction operates on:

1. You **load** a value into the accumulator.
2. You perform **operations** (AND, OR, ADD, etc.) between the accumulator and an operand.
3. You **store** the accumulator value into an output variable.

Every IL program follows this load → operate → store pattern, repeated for each piece of logic.

## Instruction Format

Each IL instruction occupies one line:

```
[label:]  operator  [operand]  [comment]
```

- **Label** (optional) — A name followed by a colon. Used as a jump target.
- **Operator** — The instruction mnemonic (e.g., `LD`, `AND`, `ST`).
- **Operand** (optional) — The variable or literal the instruction operates on.
- **Comment** (optional) — Text inside `(* ... *)`.

Examples:

```
        LD      sensor_a        (* Load sensor_a into accumulator *)
        AND     sensor_b        (* AND with sensor_b *)
        ST      output          (* Store result to output *)
```

## Core Instructions

### Load and Store

| Instruction | Description | Example |
|-------------|-------------|---------|
| `LD` | Load operand into accumulator | `LD sensor_a` |
| `LDN` | Load negated operand into accumulator | `LDN error_flag` |
| `ST` | Store accumulator to operand | `ST output` |
| `STN` | Store negated accumulator to operand | `STN alarm_clear` |
| `S` | Set operand to TRUE (latch) | `S motor_run` |
| `R` | Reset operand to FALSE (unlatch) | `R motor_run` |

`LD` always starts a new logic evaluation. `ST` writes the result without modifying the accumulator, so you can chain multiple stores.

### Boolean Logic

| Instruction | Description | Example |
|-------------|-------------|---------|
| `AND` | Logical AND with operand | `AND ready_signal` |
| `ANDN` | Logical AND NOT with operand | `ANDN fault_signal` |
| `OR` | Logical OR with operand | `OR alternate_input` |
| `ORN` | Logical OR NOT with operand | `ORN inhibit` |
| `XOR` | Logical exclusive OR | `XOR toggle_input` |
| `XORN` | Logical exclusive OR NOT | `XORN parity_bit` |
| `NOT` | Negate the accumulator (no operand) | `NOT` |

The `N` suffix on AND, OR, and XOR means "negate the operand before the operation" — equivalent to operating with NOT(operand).

### Arithmetic

| Instruction | Description | Example |
|-------------|-------------|---------|
| `ADD` | Add operand to accumulator | `ADD offset_value` |
| `SUB` | Subtract operand from accumulator | `SUB correction` |
| `MUL` | Multiply accumulator by operand | `MUL gain` |
| `DIV` | Divide accumulator by operand | `DIV scale_factor` |
| `MOD` | Modulo (remainder) | `MOD wrap_limit` |

### Comparison

| Instruction | Description | Result |
|-------------|-------------|--------|
| `GT` | Greater than | Accumulator = TRUE if previous > operand |
| `GE` | Greater than or equal | Accumulator = TRUE if previous ≥ operand |
| `EQ` | Equal | Accumulator = TRUE if previous = operand |
| `NE` | Not equal | Accumulator = TRUE if previous ≠ operand |
| `LE` | Less than or equal | Accumulator = TRUE if previous ≤ operand |
| `LT` | Less than | Accumulator = TRUE if previous < operand |

### Jump and Call

| Instruction | Description | Example |
|-------------|-------------|---------|
| `JMP` | Unconditional jump to label | `JMP loop_start` |
| `JMPC` | Jump if accumulator is TRUE | `JMPC error_handler` |
| `CAL` | Call function block | `CAL timer_instance` |
| `CALC` | Call if accumulator is TRUE | `CALC my_block` |
| `RET` | Return from POU | `RET` |
| `RETC` | Return if accumulator is TRUE | `RETC` |

> **Tip:** To jump when the accumulator is FALSE, use `NOT` followed by `JMPC`. The `JMPN`, `CALN`, and `RETN` instructions from the IEC standard are not supported.

## Program Structure

A complete IL program follows this pattern:

```
(* Load first input *)
        LD      input_1
(* Combine with second input *)
        AND     input_2
(* Store the result *)
        ST      output_1
```

There are no explicit variable declarations in the IL code body — all variables are defined in the Variables Table above the editor.

## Labels and Jumps

Labels mark locations in the code that can be targeted by JMP instructions:

```
start:  LD      counter
        ADD     1
        ST      counter
        LD      counter
        LT      100
        JMPC    start           (* Jump back to 'start' if counter < 100 *)
        LD      TRUE
        ST      done
```

This creates a loop that increments `counter` until it reaches 100.

> **Tip:** Loops in IL using JMP/JMPC can cause the scan to overrun if the loop doesn't terminate quickly. For long-running loops, use a state machine pattern across multiple scan cycles instead.

## Parenthesized Expressions

IL supports parentheses to change evaluation order, similar to nested expressions in algebra:

```
        LD      a
        AND(    b
        OR      c
        )
        ST      result
```

This evaluates as: `result := a AND (b OR c)`.

Without parentheses, IL evaluates strictly left to right, so `LD a / AND b / OR c` would compute as `(a AND b) OR c`.

For more complex expressions with multiple levels of nesting, use an intermediate variable instead of deeply nested parentheses:

```
        LD      z
        OR      w
        AND     y
        ST      temp
        LD      x
        OR      temp
        ST      output
```

This evaluates as: `output := x OR (y AND (z OR w))`. Breaking complex expressions into steps with intermediate variables is more readable and avoids compiler limitations with deeply nested parentheses.

## The IL Editor

The Autonomy Edge IDE provides a code editor for IL with:

- **Syntax highlighting** — Keywords (`LD`, `AND`, `OR`, `ST`, etc.) are highlighted in a distinct color. Labels, operands, and comments each have their own color.
- **Label recognition** — Labels (text followed by `:`) are highlighted differently for easy identification.
- **Block comments** — The editor supports `(* ... *)` comment blocks.
- **Case insensitivity** — IL keywords can be uppercase or lowercase; the editor recognizes both.

Unlike ST, the IL editor does not currently provide IntelliSense autocomplete for variable names. You'll need to reference the Variables Table manually when writing IL code.

## IL vs. Other Languages

| Aspect | Instruction List | Structured Text |
|--------|-----------------|----------------|
| Abstraction level | Low (assembly-like) | High (Pascal-like) |
| Readability | Poor for complex logic | Good |
| Code density | Very compact | Moderate |
| Learning curve | Steep | Moderate |
| Modern recommendation | Deprecated (use ST) | Preferred |

---

## What's Next?

See practical IL examples: [IL Examples](il-examples).
