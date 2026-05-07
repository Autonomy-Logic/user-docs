# Common Compilation Errors

When you compile a PLC program in Autonomy Edge, the IDE translates your IEC 61131-3 code (Structured Text, Ladder Diagram, Function Block Diagram) into an executable that the runtime loads. Errors can happen during translation or when the runtime tries to load the result. This guide covers the most common compilation errors and how to fix them.

## Structured Text Errors

### Syntax Errors

**Missing Semicolons**

Every ST statement must end with a semicolon. Missing one produces an error pointing to the line *after* the missing semicolon.

**Symptom:**
```
Error on line N (the line after the missing semicolon)
```

**Cause:** Forgot the semicolon on the previous line.

**Fix:** Add the semicolon:
```iecst
(* Before — missing semicolon *)
counter := counter + 1
IF counter > 10 THEN    (* error reported here *)

(* After — fixed *)
counter := counter + 1;
IF counter > 10 THEN
```

---

**Unmatched Control Structures**

Every `IF` needs an `END_IF`, every `FOR` needs an `END_FOR`, every `CASE` needs an `END_CASE`.

**Symptom:** Unexpected end-of-file or "expected END_IF" error.

**Cause:** A control structure wasn't properly closed.

**Fix:** Close all control structures:

| Structure | Closing Keyword |
|-----------|----------------|
| `IF ... THEN` | `END_IF;` |
| `FOR ... DO` | `END_FOR;` |
| `WHILE ... DO` | `END_WHILE;` |
| `REPEAT` | `END_REPEAT;` |
| `CASE ... OF` | `END_CASE;` |

---

**Invalid Assignment Operator**

ST uses `:=` for assignment, not `=`. Using `=` performs a comparison instead, leading to unexpected errors.

**Symptom:** Logic doesn't work as expected, or you get a type error.

**Cause:** Used `=` instead of `:=`.

**Fix:**
```iecst
(* Wrong: = is comparison, not assignment *)
counter = counter + 1;

(* Correct: := is assignment *)
counter := counter + 1;
```

### Type Errors

**Type Mismatch in Assignment**

**Symptom:**
```
Error: cannot assign REAL to INT
```

**Cause:** Assigning a value of one type to a variable of a different, incompatible type.

**Fix:** Use explicit type conversion:
```iecst
(* Error *)
myInt : INT;
myInt := 3.14;

(* Fix *)
myInt := REAL_TO_INT(3.14);
```

**Common type conversion functions:**

| From | To | Function |
|------|----|----------|
| `REAL` | `INT` | `REAL_TO_INT()` |
| `INT` | `REAL` | `INT_TO_REAL()` |
| `BOOL` | `INT` | `BOOL_TO_INT()` |
| `INT` | `BOOL` | `INT_TO_BOOL()` |
| `DINT` | `INT` | `DINT_TO_INT()` |
| `INT` | `STRING` | `INT_TO_STRING()` |
| `TIME` | `DINT` | `TIME_TO_DINT()` |

---

**Incompatible Operands**

**Symptom:** Type error on an expression involving different types.

**Cause:** Using operators with incompatible types.

**Fix:** Make sure operands share compatible types, or convert them explicitly:
```iecst
(* Error: cannot compare STRING with INT *)
IF myString > 5 THEN ...

(* Error: cannot add BOOL and INT *)
result := myBool + myInt;
```

### Undefined Variable Errors

**Variable Not Declared**

**Symptom:**
```
Error: Undefined variable 'temp_value'
```

**Cause:** The variable name isn't in the Variables Table. Common reasons:
- Typo in the variable name
- Variable declared in a different POU (local variables aren't visible outside their POU)
- Variable deleted from the Variables Table but still referenced in code

**Fix:** Add the variable to the Variables Table or correct the spelling.

---

**Function Block Not Instantiated**

**Symptom:** Error when calling a Function Block type name directly.

**Cause:** Calling the type instead of an instance.

**Fix:** Declare an instance in the Variables Table, then call the instance:
```iecst
(* Error: TON is a type, not an instance *)
TON(IN := start, PT := T#5s);

(* Fix: declare myTimer : TON in Variables Table, then: *)
myTimer(IN := start, PT := T#5s);
```

### Function Block Call Errors

**Wrong Parameter Names**

**Symptom:** Error about unknown input or output name.

**Cause:** Using incorrect parameter names for a Function Block.

**Fix:** Use the correct names:
```iecst
(* Error: TON has no input named 'Enable' *)
myTimer(Enable := TRUE, Duration := T#5s);

(* Correct *)
myTimer(IN := TRUE, PT := T#5s);
```

---

**Accessing Non-existent Outputs**

**Symptom:**
```
Error: TON has no output named 'Done'
```

**Cause:** Referencing an output name that doesn't exist on the block.

**Fix:** Use the correct output name:
```iecst
(* Error *)
result := myTimer.Done;

(* Correct *)
result := myTimer.Q;
```

**Standard Function Block quick reference:**

| Block | Inputs | Outputs |
|-------|--------|---------|
| `TON` | `IN` (BOOL), `PT` (TIME) | `Q` (BOOL), `ET` (TIME) |
| `TOF` | `IN` (BOOL), `PT` (TIME) | `Q` (BOOL), `ET` (TIME) |
| `TP` | `IN` (BOOL), `PT` (TIME) | `Q` (BOOL), `ET` (TIME) |
| `CTU` | `CU` (BOOL), `R` (BOOL), `PV` (INT) | `Q` (BOOL), `CV` (INT) |
| `CTD` | `CD` (BOOL), `LD` (BOOL), `PV` (INT) | `Q` (BOOL), `CV` (INT) |
| `SR` | `S1` (BOOL), `R` (BOOL) | `Q1` (BOOL) |
| `RS` | `S` (BOOL), `R1` (BOOL) | `Q1` (BOOL) |

## Ladder Diagram Errors

### Invalid Rung Structure

**Symptom:** Compilation error related to rung connectivity.

**Cause:**
- **Open rung** — A rung must connect the left power rail to the right through at least one element
- **Floating element** — Every element must be connected to both rails through a continuous path
- **Multiple coils on the same variable** — Assigning the same output in multiple rungs can cause unpredictable behavior

**Fix:** Ensure every rung forms a complete path from left rail to right rail.

### Contact/Coil Type Mismatch

**Symptom:** Type error on a contact or coil element.

**Cause:** Contacts and coils must reference BOOL variables. Using an INT or REAL variable produces a type error.

**Fix:** Make sure all contacts and coils reference variables declared as `BOOL` in the Variables Table.

## Function Block Diagram Errors

### Unconnected Pins

**Symptom:** Compilation error about unconnected inputs.

**Cause:** A required input pin on an FBD block isn't connected.

**Fix:** Connect all required inputs, or remove unused blocks from the diagram.

### Wire Type Mismatches

**Symptom:**
```
Error: Cannot connect REAL output to BOOL input
```

**Cause:** Connecting an output of one type to an input of a different type.

**Fix:** Insert an appropriate conversion block between mismatched types, or make sure connected pins share compatible types.

## Build Errors

### Not a Valid PLC Program

**Symptom:**
```
[ERROR] Not a valid PLC Program file.
```

**Cause:** The uploaded file isn't a valid program file, or it's corrupted.

**Fix:** Use the normal compile-and-download workflow in the IDE. Don't manually modify exported files.

### Build Failed

**Symptom:**
```
[ERROR] Compilation failed (exit=1)
[WARNING] PLC program has not been updated because the build failed
```

**Cause:** There are semantic errors in your PLC code that weren't caught earlier in translation.

**Fix:** Review the full compilation output in the console for specific error messages. The first error is usually the root cause — later errors are often cascading failures.

## Troubleshooting Workflow

When you hit a compilation error, follow this process:

1. **Read the error message carefully** — The first error is usually the root cause; subsequent errors often cascade from it
2. **Check the line number** — The IDE highlights the approximate location
3. **Verify variable declarations** — Open the Variables Table and confirm all referenced variables exist with correct types
4. **Check control structure pairing** — Every opening keyword needs its closing counterpart
5. **Look for typos** — Misspelled variable names and keywords are the most common cause
6. **Simplify and test** — Comment out suspect code and recompile to isolate the problem
7. **Check the console** — The full compilation output often has more detail than the inline error display

> **Tip:** When you get multiple errors, always fix the first one and recompile. Many "errors" are just cascading symptoms of a single root cause.

## What's Next?

- [Runtime Debugging](runtime-debugging) — Debug your running program with the IDE's monitoring tools
- [Network Issues](network-issues) — Troubleshoot connectivity problems
- [ST Language Basics](../../openplc-editor/programming-languages/structured-text/st-basics) — Review ST syntax rules
