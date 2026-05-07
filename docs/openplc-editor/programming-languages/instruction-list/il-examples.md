# IL Practical Examples

This section provides practical examples of Instruction List programming. Each example includes the Variables Table definition, the IL code, and an explanation of how it works. Equivalent Structured Text code is shown alongside for comparison.

## Basic AND Logic

The simplest IL pattern: combine two inputs with AND logic to drive an output.

### Variables

| Name | Type | Class |
|------|------|-------|
| `sensor_a` | BOOL | Local |
| `sensor_b` | BOOL | Local |
| `output` | BOOL | Local |

### IL Code

```
        LD      sensor_a        (* Load first input *)
        AND     sensor_b        (* AND with second input *)
        ST      output          (* Store result *)
```

### Equivalent ST

```
output := sensor_a AND sensor_b;
```

### Explanation

1. `LD sensor_a` loads the value of `sensor_a` into the accumulator.
2. `AND sensor_b` performs a logical AND between the accumulator and `sensor_b`. The result stays in the accumulator.
3. `ST output` writes the accumulator value to `output`.

## OR Logic with Negation

Combine OR and NOT to create a safety interlock.

### Variables

| Name | Type | Class |
|------|------|-------|
| `start_cmd` | BOOL | Local |
| `auto_start` | BOOL | Local |
| `fault` | BOOL | Local |
| `enable` | BOOL | Local |

### IL Code

```
        LD      start_cmd       (* Load manual start *)
        OR      auto_start      (* OR with auto start *)
        ANDN    fault           (* AND NOT fault — block if fault active *)
        ST      enable          (* Store result *)
```

### Equivalent ST

```
enable := (start_cmd OR auto_start) AND NOT fault;
```

### Explanation

1. Load `start_cmd`.
2. OR with `auto_start` — accumulator is TRUE if either is TRUE.
3. `ANDN fault` — AND with NOT `fault`. This blocks the result if `fault` is TRUE.
4. Store the final result in `enable`.

## Latch/Unlatch (Set/Reset)

Implement a latching motor control using Set and Reset instructions.

### Variables

| Name | Type | Class |
|------|------|-------|
| `start_button` | BOOL | Local |
| `stop_button` | BOOL | Local |
| `motor` | BOOL | Local |

### IL Code

```
        LD      start_button    (* Check start condition *)
        S       motor           (* Set (latch) motor if TRUE *)
        LD      stop_button     (* Check stop condition *)
        R       motor           (* Reset (unlatch) motor if TRUE *)
```

### Equivalent ST

```
IF start_button THEN
    motor := TRUE;
END_IF;
IF stop_button THEN
    motor := FALSE;
END_IF;
```

### Explanation

The `S` instruction sets `motor` to TRUE only if the accumulator is TRUE — it does nothing if the accumulator is FALSE. Similarly, `R` resets `motor` to FALSE only if the accumulator is TRUE. Since the stop logic comes after the start logic, stop has priority if both buttons are pressed simultaneously.

## Arithmetic — Temperature Scaling

Scale a raw sensor reading to engineering units.

### Variables

| Name | Type | Class |
|------|------|-------|
| `raw_value` | INT | Local |
| `scaled` | REAL | Local |
| `offset` | REAL | Local |
| `gain` | REAL | Local |
| `temp_real` | REAL | Local |

### IL Code

```
        LD      raw_value       (* Load raw integer value *)
        INT_TO_REAL             (* Convert to REAL *)
        ST      temp_real       (* Store intermediate *)
        LD      temp_real       (* Reload for calculation *)
        MUL     gain            (* Multiply by gain factor *)
        ADD     offset          (* Add offset *)
        ST      scaled          (* Store final scaled value *)
```

### Equivalent ST

```
temp_real := INT_TO_REAL(raw_value);
scaled := (temp_real * gain) + offset;
```

### Explanation

IL doesn't support nested expressions like `(raw * gain) + offset` in a single line. You must break the calculation into sequential steps: load, operate, store or chain.

## Comparison and Conditional Jump

Implement a bounded counter using comparison and conditional jumps.

### Variables

| Name | Type | Class |
|------|------|-------|
| `count_pulse` | BOOL | Local |
| `reset` | BOOL | Local |
| `counter` | INT | Local |
| `max_count` | INT | Local |
| `at_max` | BOOL | Local |

### IL Code

```
        LD      reset           (* Check for reset *)
        JMPC    do_reset        (* Jump to reset if TRUE *)

        LD      count_pulse     (* Check for count pulse *)
        NOT                     (* Negate: TRUE if no pulse *)
        JMPC    done            (* Skip if no pulse *)

        LD      counter         (* Load current count *)
        GE      max_count       (* Compare: counter >= max_count? *)
        JMPC    done            (* Skip increment if at max *)

        LD      counter         (* Load current count *)
        ADD     1               (* Increment *)
        ST      counter         (* Store back *)
        JMP     check_max       (* Jump to max check *)

do_reset:
        LD      0               (* Load zero *)
        ST      counter         (* Reset counter *)

check_max:
        LD      counter         (* Load count *)
        GE      max_count       (* Check if at max *)
        ST      at_max          (* Store comparison result *)
        JMP     end_prog

done:
        LD      counter         (* Load count *)
        GE      max_count       (* Check if at max *)
        ST      at_max          (* Update at_max flag *)

end_prog:
```

### Equivalent ST

```
IF reset THEN
    counter := 0;
ELSIF count_pulse AND (counter < max_count) THEN
    counter := counter + 1;
END_IF;
at_max := counter >= max_count;
```

### Explanation

This example shows why IL is verbose compared to ST. The same logic that takes 4 lines in ST requires labels, jumps, and repeated loads in IL. The JMP/JMPC instructions serve as IL's version of IF/ELSE logic. Note that `JMPN` (jump if FALSE) is not supported — use `NOT` followed by `JMPC` instead.

## Parenthesized Expressions

Use parentheses to implement complex Boolean logic without intermediate variables.

### Variables

| Name | Type | Class |
|------|------|-------|
| `a` | BOOL | Local |
| `b` | BOOL | Local |
| `c` | BOOL | Local |
| `d` | BOOL | Local |
| `result` | BOOL | Local |

### IL Code

```
        LD      a
        AND(    b               (* Begin parenthesized expression *)
        OR      c               (* b OR c *)
        )                       (* Close parenthesis: a AND (b OR c) *)
        OR      d               (* OR d *)
        ST      result          (* result = (a AND (b OR c)) OR d *)
```

### Equivalent ST

```
result := (a AND (b OR c)) OR d;
```

### Explanation

Without parentheses, `LD a / AND b / OR c / OR d` would evaluate as `((a AND b) OR c) OR d`. Parentheses change the evaluation order so that `b OR c` is computed first, then ANDed with `a`.

## Function Block Call

Call a TON timer function block.

### Variables

| Name | Type | Class |
|------|------|-------|
| `enable` | BOOL | Local |
| `timer_out` | BOOL | Local |
| `my_timer` | TON | Local |

### IL Code

```
        LD      enable          (* Load enable signal *)
        ST      my_timer.IN     (* Set timer input *)
        LD      T#5s            (* Load preset time *)
        ST      my_timer.PT     (* Set timer preset *)
        CAL     my_timer        (* Call the timer *)
        LD      my_timer.Q      (* Load timer output *)
        ST      timer_out       (* Store to output variable *)
```

### Equivalent ST

```
my_timer(IN := enable, PT := T#5s);
timer_out := my_timer.Q;
```

### Explanation

In IL, calling a function block requires:
1. Setting each input parameter individually using LD/ST.
2. Calling the block with `CAL`.
3. Reading outputs with LD.

This is considerably more verbose than ST's single-line call syntax — another reason ST is preferred for modern projects.

## When to Use IL

IL makes sense in a few specific situations:

- **Legacy migration** — Converting old PLC programs from manufacturers that used IL-like instruction sets.
- **Tiny programs** — Very short, simple Boolean logic where the overhead of understanding IL is minimal.
- **Learning** — Understanding IL helps you grasp the fundamentals of how PLC logic is evaluated at the lowest level.

For everything else, use [Structured Text](../structured-text/st-basics) — it provides the same capabilities with dramatically better readability.

---

## What's Next?

Explore other programming languages: [Structured Text](../structured-text/st-basics) | [Ladder Diagram](../ladder-diagram/ld-basics) | [Function Block Diagram](../function-block-diagram/fbd-basics).
