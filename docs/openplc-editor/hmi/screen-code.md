# Screen code

Every screen is a Structured Text function block, and the designer is a visual way of writing it. Open the **Code** view of a screen to see it. You can edit either view: a change in one appears in the other.

You can build complete HMIs without writing code. This page is for when you want to compute something on the screen, react to a press, or move between screens.

---

## What a screen looks like

This is the Overview screen from [Designing screens](designing-screens), as the designer wrote it:

```st
FUNCTION_BLOCK Overview EXTENDS HmiScreen
  VAR
    Body : HmiHorizontalStack := (AutoSize := TRUE, Span := 100, Gap := 12, Padding := 16);
    Title : HmiLabel := (Parent := 'Body', Text := 'Tank station', Size := 24, Font := HMI_FONT#Bold, AutoSize := TRUE, Span := 10);
    Process : HmiVerticalStack := (Parent := 'Body', AutoSize := TRUE, Span := 65, Gap := 12);
    Level : HmiTank := (Parent := 'Process', Caption := 'Level', Unit := 'm', MaxValue := 10.0, AutoSize := TRUE, Span := 35);
    Pressure : HmiGauge := (Parent := 'Process', Caption := 'Pressure', Unit := 'bar', MaxValue := 10.0, AutoSize := TRUE, Span := 40);
    Pump : HmiLamp := (Parent := 'Process', Caption := 'Pump running', AutoSize := TRUE, Span := 25);
    Commands : HmiVerticalStack := (Parent := 'Body', AutoSize := TRUE, Span := 25, Gap := 12);
    Start : HmiButton := (Parent := 'Commands', Text := 'Start', AutoSize := TRUE, Span := 25);
    Stop : HmiButton := (Parent := 'Commands', Text := 'Stop', AccentColor := COLOR.Danger, AutoSize := TRUE, Span := 25);
    Setpoint : HmiNumericInput := (Parent := 'Commands', Caption := 'Setpoint', Unit := 'm', MinValue := 0.0, MaxValue := 10.0, AutoSize := TRUE, Span := 50);
  END_VAR
  Level.Value := instance0.Main.Level;
  Pressure.Value := instance0.Main.Pressure;
  Pump.Value := instance0.Main.PumpRunning;
  Setpoint.Value := instance0.Main.Setpoint;
  IF Start.Changed THEN
    instance0.Main.StartPump := Start.Pressed;
  END_IF;
  IF Stop.Changed THEN
    instance0.Main.StopPump := Stop.Pressed;
  END_IF;
END_FUNCTION_BLOCK
```

Three parts:

- **The declarations** are the screen's elements. Each one is a widget with its properties in the initializer. **Parent** names the container it sits in.
- **The body** runs every frame, about ten times a second by default (see the **Frame period** in [HMI Settings](hmi-settings)).
- **The assignments** in the body connect widgets to the PLC program.

---

## Reading PLC variables

Assign a variable to a widget's value in the body:

```st
Level.Value := instance0.Main.Level;
```

Program variables are named through their instance, as in the **Variables** tab: `instance0.Main.Level` is the `Level` variable of the `Main` program running as `instance0`. Global variables are named directly, like `MaxLevel`.

Any expression works, so a screen can show a computed value:

```st
LevelPercent.Value := instance0.Main.Level / 10.0 * 100.0;
```

On OpenPLC Runtime v4, the device sends each display only the variables of the screen it shows.

---

## Writing PLC variables

A control assigned to a variable, like the `Setpoint` numeric entry above, also writes the variable back when the operator changes it. You do not write that part yourself.

Buttons write on press and release. This is what the designer writes when you drop a BOOL on a button:

```st
IF Start.Changed THEN
  instance0.Main.StartPump := Start.Pressed;
END_IF;
```

Each widget reports what the operator did through its outputs, such as **Clicked**, **Pressed**, **Changed** and **NewValue**. A **Changed** or **Clicked** output is TRUE for one frame only, so code inside the IF runs once per press.

> **Warning:** Screen code runs on the operator's display, not in the PLC. Put interlocks and safety conditions in the PLC program, never only in a screen. The device does enforce the limits you set on controls (like a numeric entry's MinValue and MaxValue) and which roles may open the screen.

---

## Navigating between screens

Each screen of the project has a name in `HMI_SCREEN`. Show a screen with `HMI_Show`:

```st
IF ToTrends.Clicked THEN
  HMI_Show(HMI_SCREEN#Trends);
END_IF;
```

| Function | What it does |
|---|---|
| `HMI_Show(HMI_SCREEN#Name)` | Shows that screen from the next frame. Ignored when the operator's role may not open it. |
| `HMI_Back()` | Returns to the previous screen. |
| `HMI_CurrentScreen()` | The screen being shown, to compare with `HMI_SCREEN#Name`. |
| `HMI_SignOut()` | Signs the operator out. The display returns to the sign-in page. |
| `HMI_Lock()` | On a local panel with a PIN, locks the panel until the PIN is entered again. |
| `HMI_Calibrate()` | On a local panel with touch calibration, opens the calibration screen. |

The **Actions** tab of a widget's properties writes these for you: **Show a screen**, **Go back**, **Sign out**, **Lock the panel**, **Calibrate touch**, **Set a variable**, **Toggle a variable** or your own **ST code**.

> **Tip:** A screen only shows what someone may see. Pair a navigation button with the role grid in [HMI Settings](hmi-settings) so operators are never sent to a screen they cannot open.

---

## Changing properties at run time

Any property can be assigned in the body, not only the main value. For example, a lamp that turns red on a fault and a button that is only enabled when the pump is stopped:

```st
Pump.OnColor := SEL(instance0.Main.PumpFault, COLOR.Success, COLOR.Danger);
Start.Enabled := NOT instance0.Main.PumpRunning;
Alarm.Visible := instance0.Main.AlarmActive;
```

Every element has **Visible** and **Enabled**. A hidden element takes no room in its stack.

---

## Colors

Colors come from the `COLOR` constants:

- **Theme colors** follow the screen's theme: `Background`, `Surface`, `Text`, `TextMuted`, `Border`, `Fill`, `Accent`, `OnAccent`, `Success`, `Warning`, `Danger`, `Bar` and `OnBar`.
- **Fixed colors** are the same in every theme: `Red`, `Green`, `Blue`, `Yellow`, `Orange`, `Gray`, `White`, `Black` and `Transparent`.

`HMI_Alpha(COLOR.Accent, 50)` gives a color at 50% opacity.

Prefer theme colors. A screen that uses them changes its whole look when you switch themes, and stays readable in a dark theme.

---

## Themes per screen

A screen uses the project's default theme unless you pick another one with the theme picker above the canvas. The choice is written as an attribute on the screen:

```st
{attribute 'hmi_theme' := 'Dark'}
FUNCTION_BLOCK Overview EXTENDS HmiScreen
```

Themes are listed and created in [HMI Settings](hmi-settings).
