# Runtime Debugging

Once your PLC program compiles and runs, you need tools to verify that it behaves correctly. The Autonomy Edge IDE provides a built-in debugging environment with real-time variable monitoring, a console output panel, and graphical data visualization. This guide covers how to use these tools to diagnose and fix runtime issues.

## The Debug Workflow

Debugging a PLC program is different from debugging traditional software. Because PLC programs run in continuous scan cycles, you observe behavior over time rather than stepping through lines:

1. **Deploy** — Compile and upload your program to the runtime
2. **Start** — Start the runtime to begin executing your program
3. **Monitor** — Watch variables in real-time using the IDE's debug panel
4. **Analyze** — Use the console and charts to understand timing and state transitions
5. **Modify** — Stop the runtime, edit your code, recompile, and redeploy
6. **Repeat** — Continue until the program behaves as expected

## The Console Panel

The console panel at the bottom of the IDE workspace displays real-time log messages from the runtime. It's your primary tool for understanding what the runtime is doing.

### Log Levels

| Level | Color | Meaning |
|-------|-------|---------|
| **Debug** | Gray | Detailed diagnostic information (verbose) |
| **Info** | White | Normal operational messages (startup, status changes) |
| **Warning** | Yellow | Potential problems that don't stop execution (scan overruns, timing issues) |
| **Error** | Red | Failures that affect program execution (load errors, communication failures) |

### Filtering Console Output

Use the filter controls above the console to focus on what matters:

- **Level filter** — Show only messages at a specific severity (e.g., only Warnings and Errors)
- **Search** — Filter messages by text content or timestamp
- **Timestamp format** — Choose between full date-time (`DD-MM-YY HH:MM:SS`), time only (`HH:MM:SS`), or no timestamps

> **Tip:** Start with **Warning** and **Error** filters to see problems first, then widen to **Info** and **Debug** for context.

### Exporting Logs

The console supports exporting logs in three formats for offline analysis:

| Format | Best For |
|--------|----------|
| **JSON** | Programmatic analysis, importing into other tools |
| **CSV** | Spreadsheet analysis, data processing |
| **TXT** | Human-readable plain text with formatted timestamps |

Click the export button in the console toolbar and select your preferred format.

## Variable Monitoring

The Variables Panel shows the real-time values of all variables in your running PLC program. This is the most direct way to verify your logic is working.

### Opening the Variables Panel

When a program is running, the Variables Panel displays:

- **Variable name** — As declared in the Variables Table
- **Variable type** — The IEC data type (BOOL, INT, REAL, TIME, etc.)
- **Current value** — Updated in real-time as the program runs

The panel separates regular variables from Function Block instances (TON, TOF, CTU, etc.), making it easy to inspect timer and counter states.

### What to Look For

| Symptom | What to Check | Possible Cause |
|---------|---------------|----------------|
| Output never turns ON | The controlling BOOL variable | Condition never TRUE; check input variables |
| Output stuck ON | The turn-off condition | Missing reset logic; check stop/reset inputs |
| Timer doesn't count | The timer's `IN` and `ET` values | `IN` not staying TRUE long enough |
| Counter won't reset | The reset input (`R` or `LD`) | Reset signal not reaching the counter |
| Value always zero | The variable's source | Input not mapped; variable never assigned |
| Value oscillating | The logic that writes the variable | Conflicting assignments in different code blocks |

### Monitoring Function Block Instances

Expand a Function Block instance in the Variables Panel to see its internal state:

**Timer instance (e.g., TON):**
- `IN` — Current input state
- `PT` — Preset time
- `Q` — Current output state
- `ET` — Elapsed time (watch this count up to verify timing)

**Counter instance (e.g., CTU):**
- `CU` — Count-up input
- `R` — Reset input
- `PV` — Preset value
- `Q` — Output (TRUE when `CV` >= `PV`)
- `CV` — Current count value

## Graphical Data Visualization

The debugger includes a real-time charting feature that plots variable values over time. This is great for:

- Observing analog value trends (temperature, pressure, level)
- Verifying timer timing accuracy
- Detecting oscillations or instability in control loops
- Confirming state machine transitions

### Using the Chart View

1. In the Variables Panel, toggle the **graph view** for any variable you want to chart
2. The chart appears at the top of the debug panel
3. Use the **range selector** to choose the time window:
   - **1 second** — For fast events and high-resolution timing
   - **2 seconds** — Default view for most debugging
   - **60 seconds** — For observing slow trends and long-duration timers
4. Use the **Play/Pause** button to freeze the chart for analysis

### Reading the Charts

The chart shows:
- **X-axis** — Time (with tick counter showing scan cycles)
- **Y-axis** — Variable value
- **Multiple traces** — Each monitored variable gets its own colored line

**Tips for chart debugging:**
- BOOL values show as 0/1 step functions — look for clean edges
- REAL values should show smooth curves for analog processes — jagged lines indicate noise or scan overruns
- TIME values count up linearly when a timer is active — steps or jumps indicate timing issues

## Common Runtime Issues

### Program Not Starting

**Symptom:** You upload and start the runtime, but the program doesn't appear to execute.

**Cause:** Load error, missing task configuration, or initialization issue.

**Fix:**
1. Check the console for errors during program load
2. Verify the runtime is in RUNNING state, not ERROR
3. Make sure at least one task is configured with a Program assigned
4. Check if the program requires specific initial conditions to enter the main logic

---

### Variables Not Updating

**Symptom:** Variables in the monitoring panel show constant values even though the program should be changing them.

**Cause:** Runtime stopped, IDE disconnected, or logic path issue.

**Fix:**
1. Confirm the runtime is running (not stopped or in error)
2. Check that the IDE is connected to the runtime
3. If the task period is very long (e.g., 5000 ms), updates will appear slow — this is normal
4. Trace the logic to confirm the code that writes the variable is actually being reached

---

### Scan Overruns

**Symptom:** Console shows repeated warnings about scan overruns, and timing behavior is inconsistent.

**Cause:** The program takes longer to execute than the task period allows.

**Fix:**
1. Check if the task period is realistic for the amount of logic
2. Look for FOR loops iterating over large arrays
3. Check for heavy math operations running every scan
4. Make sure you haven't assigned too many POUs to a single fast task

See [Performance Optimization](../best-practices/performance-optimization) for detailed optimization techniques.

---

### Unexpected Output Behavior

**Symptom:** Outputs turn on/off at unexpected times or in the wrong sequence.

**Cause:** Multiple assignments, timing issue, or incorrect conditions.

**Fix:**
1. **Identify the output variable** — Which output is misbehaving?
2. **Find all assignments** — Search your code for every place that variable is written
3. **Monitor the conditions** — Watch the input variables that control the output
4. **Check for multiple writers** — If the same variable is written in multiple places, the last write wins
5. **Check timing** — Use the chart view to correlate output changes with input events

---

### Watchdog Timeout

**Symptom:**
```
[ERROR] Watchdog: No heartbeat! PLC unresponsive.
```

**Cause:** The PLC program is stuck and not completing scan cycles. This triggers the runtime's watchdog safety mechanism. Common causes:
- Infinite loop (WHILE loop with a condition that never becomes FALSE)
- Extremely long FOR loop that exceeds the watchdog timeout

**Fix:** Review all loops for guaranteed termination. WHILE loops must always have a reachable exit condition. FOR loops should have bounded iteration counts.

## Debug Best Practices

### Start Simple

When debugging complex logic, start with the simplest test case:

1. **Test inputs one at a time** — Activate a single input and verify the expected output
2. **Test state transitions individually** — Step through your state machine manually
3. **Add temporary monitoring variables** — Create local variables that capture intermediate values for observation

### Use Systematic Elimination

When you can't find the bug by inspection:

1. **Comment out half the logic** — Does the problem go away?
2. **If yes**, the bug is in the commented-out half — restore and subdivide
3. **If no**, the bug is in the remaining half — comment out half of that
4. **Repeat** until you've isolated the exact block causing the issue

### Monitor at Boundaries

Focus your monitoring on the boundaries between blocks:

- **Inputs to a Function Block** — Are they what you expect?
- **Outputs from a Function Block** — Do they match the expected behavior?
- **Global variables** — Are they being set by the right POU at the right time?

### Document What You Find

When you fix a bug, add a comment explaining what went wrong and why the fix works. This saves time when similar issues come up in future projects.

## What's Next?

- [Compilation Errors](compilation-errors) — Fix errors before your program reaches the runtime
- [Network Issues](network-issues) — Troubleshoot connectivity between the IDE and runtime
- [Performance Optimization](../best-practices/performance-optimization) — Ensure your program runs within scan time limits
