# Worked example: Motor start / stop with seal-in

The classic latching circuit you learn in week one of any PLC course. Pressing **Start** turns the motor on. Pressing **Stop** turns it off. The motor stays on between presses because it seals itself in through one of its own contacts.

**Surfaces exercised:** Ladder Diagram editor, variables table, parallel branches in LD, normally-closed contacts, the Simulator + debugger.

**Expected time:** about 5 minutes.

## The circuit

<LadderDiagramViewer src="/docs/diagrams/ladder/seal-in.json" />

Reading the rung left to right:

- A **parallel** pair of contacts: `start_btn` and `motor_on`. Either can pass current.
- A **normally-closed** contact for `stop_btn`. Closed by default; opens (blocks) when `stop_btn` is `TRUE`.
- The `motor_on` coil.

When `start_btn` is pressed, the top branch of the parallel passes current through the closed `stop_btn` contact to the coil. The coil sets `motor_on = TRUE`. From the next cycle onwards, the **bottom branch** (the `motor_on` contact) is also passing, so even when `start_btn` returns to `FALSE`, current still flows through `motor_on`'s own contact, keeping the coil energised. That's the **seal-in**.

Pressing `stop_btn` opens the normally-closed contact, breaking the path to the coil. `motor_on` goes `FALSE`, the seal-in contact opens, and the motor stays off until the next `start_btn` press.

## Step 1: Declare the variables

In a new LD program, add three variables:

| Name | Class | Type | Notes |
|---|---|---|---|
| `start_btn` | Local | BOOL | Tick Debug |
| `stop_btn` | Local | BOOL | Tick Debug |
| `motor_on` | Local | BOOL | Tick Debug |

All three are local for this demo. In a real installation, `start_btn` and `stop_btn` would be `Input` class with `Location` mapped to physical discrete inputs (`%IX0.0`, `%IX0.1`); `motor_on` would be `Output` mapped to `%QX0.0`. See **[Variables editor](../working-with-variables/variables-editor)**.

## Step 2: Draw the rung

You need a parallel branch in the middle of a regular series. The LD toolbox handles this through the **branch** action on a selected element:

1. Drag a **Contact** into the empty rung. Name it `start_btn`, variant `default`.
2. Right-click on the `start_btn` contact and pick **Add parallel branch**. A second lane appears below.
3. In the new lane, drop another contact: `motor_on`, variant `default`.
4. Click after the parallel block to position the cursor on the main wire.
5. Drag a **Contact** in: `stop_btn`, variant `negated` (the normally-closed style with a slash).
6. Drag a **Coil** at the end of the rung: `motor_on`, variant `default`.

Save.

## Step 3: Run on the Simulator

Click **Start Simulator**. After the compile, the rung shows live colouring, initially everything is grey because all three variables are `FALSE` and the normally-closed `stop_btn` is the only thing passing current.

## Step 4: Toggle the buttons

The Simulator has no physical buttons, so you toggle the variables manually from the debugger.

1. Open the Debugger panel at the bottom (it auto-opens when the Simulator starts).
2. The variables list shows `start_btn`, `stop_btn`, `motor_on`. Right-click `start_btn` and pick **Force value** → `TRUE`. The rung lights up, power flows through the top branch, through the `stop_btn` NC contact, into the coil. `motor_on` flips to `TRUE`.
3. Right-click `start_btn` again and force it back to `FALSE`. Notice the **bottom branch** is now green (the seal-in is holding the coil energised through `motor_on`'s own contact). `motor_on` stays `TRUE`.
4. Force `stop_btn` to `TRUE`. The NC contact opens, the rung goes grey, `motor_on` flips to `FALSE`.
5. Force `stop_btn` back to `FALSE`. Nothing happens, the motor stays off until you press start again.

## What you've shown

- The seal-in pattern is two contacts in parallel, both reading inputs that can break the latch.
- Forcing values in the debugger is how you simulate physical inputs when there are none.
- The live colouring reveals exactly which branch is carrying current at any moment, which is the easiest way to convince yourself a circuit is doing what you intended.

## Where to next

- Wire it to real hardware: change `start_btn` / `stop_btn` to `Input` class with `%IX` addresses, `motor_on` to `Output` with `%QX0.0`, deploy to a vPLC, and connect the pins.
- Expose `motor_on` over Modbus so an HMI can see it. See **[Modbus slave: expose digital outputs](modbus-slave-outputs)**.
- Try a reset-priority variant: if both buttons are held, which wins? Move `stop_btn` to before the parallel branch.
