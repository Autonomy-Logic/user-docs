# Widget library

The **HMI Standard Widgets** library comes with the editor and is always available. Its widgets are listed in the palette by group, with a live thumbnail of each. This page shows each one and what it is for.

Every widget takes its colors from the screen's theme, so it looks the same in the editor, in a browser and on a panel. The pictures use the default theme and sample values.

Every widget has a **main** value: the one a variable is wired to when you drop the variable on the widget. It is listed below for each widget.

---

## Containers

| Widget | Use it for |
|---|---|
| **Vertical stack** | Placing widgets side by side. |
| **Horizontal stack** | Placing widgets top to bottom. |
| **Diagram** | Process graphics: symbols at positions on a grid, connected by pipes, scaled as a whole. |

Stacks have no look of their own: they arrange what they hold. See [Screen layout that fits any display](layout).

A diagram with two vessels, a pump and a valve, connected by pipes with flow shown:

![A diagram with tank T-1 at 70.0, pump P-1, valve V-1 and tank T-2 at 30.0, connected by blue pipes with moving flow marks](images/widgets/diagram.png)

---

## Shapes

Plain shapes for frames, backgrounds, separators and simple graphics. Their colors can follow a variable through screen code.

| Widget | Looks like |
|---|---|
| **Rect** | ![A white rectangle with rounded corners and a thin outline](images/widgets/rect.png) |
| **Ellipse** | ![A white circle with a thin outline](images/widgets/ellipse.png) |
| **Polygon** | ![A white triangle with a thin outline](images/widgets/polygon.png) |
| **Line** | ![A straight horizontal line](images/widgets/line.png) |

---

## Display

| Widget | Shows | Main value | Looks like |
|---|---|---|---|
| **Label** | A text. | Text | ![The Label widget: a short text](images/widgets/label.png) |
| **Value** | A number with caption, unit and decimals. | Value | ![The Value widget: a framed number with its caption](images/widgets/value.png) |
| **Readout** | A framed number with a unit, the small readouts of process diagrams. | Value | ![The Readout widget: a small framed number](images/widgets/readout.png) |
| **Lamp** | An on or off state, optionally blinking. | Value (BOOL) | ![The Lamp widget: a green light with its caption](images/widgets/lamp.png) |
| **Multi lamp** | One of several states, each with its own color and text. | Value | ![The Multi lamp widget: a green light with the caption Status and the state Running](images/widgets/multi-lamp.png) |
| **LED** | A small on or off indicator. | Value (BOOL) | ![The LED widget: a small green dot with its caption](images/widgets/led.png) |
| **Gauge** | A value on a round dial, with optional zones. | Value | ![The Gauge widget: a round dial with its value in the centre](images/widgets/gauge.png) |
| **Tank** | A fill level. | Value | ![The Tank widget: a tall container filled in blue to its level](images/widgets/tank.png) |
| **Vessel** | A vessel symbol with its fill level. | Value | ![The Vessel widget: a steel tank on legs with a sight glass showing the level](images/widgets/vessel.png) |
| **Thermometer** | A temperature on a thermometer scale. | Value | ![The Thermometer widget: a vertical thermometer with a scale](images/widgets/thermometer.png) |
| **Bar graph** | One or more values as bars. | Value | ![The Bar graph widget: a Level bar filled to 60.0 over a 0 to 100 scale](images/widgets/bar-graph.png) |
| **Progress** | Progress of a task, as a bar. | Value | ![The Progress widget: a partly filled horizontal bar](images/widgets/progress.png) |
| **Seven segment** | A number in seven segment digits. | Value | ![The Seven segment widget: a number in seven segment digits](images/widgets/seven-segment.png) |
| **Trend** | Up to 8 values over time, as pens on a chart. | Value | ![The Trend widget: two pens, level and flow, drawn over time with the latest value at the top right](images/widgets/trend.png) |
| **Date and time** | The date and time of a DT value. | Value (DT) | ![The Date and time widget: 14:35:20 over Thu 26 Nov 2026](images/widgets/date-time.png) |
| **Clock** | The time of a DT value on an analog clock face, with a second hand. | Value (DT) | ![The Clock widget: an analog clock at 14:35:20](images/widgets/clock.png) |

---

## Controls

Controls show a variable and write it when the operator uses them.

| Widget | The operator | Main value | Looks like |
|---|---|---|---|
| **Button** | Presses it. The variable is set while it is held. | Pressed | ![The Button widget](images/widgets/button.png) |
| **Toggle button** | Turns something on and off with one button. | Value (BOOL) | ![The Toggle button widget, switched on and showing ON](images/widgets/toggle-button.png) |
| **Lamp button** | Presses a round button that also lights up to show a state. | Value | ![The Lamp button widget: a round START push button](images/widgets/lamp-button.png) |
| **Switch** | Flips an on and off switch. | Value (BOOL) | ![The Switch widget, switched on](images/widgets/switch.png) |
| **Check box** | Ticks a box. | Value (BOOL) | ![The Check box widget, ticked](images/widgets/check-box.png) |
| **Slider** | Drags to a value between a minimum and a maximum. | Value | ![The Slider widget: a track with a handle](images/widgets/slider.png) |
| **Knob** | Turns a knob to a value. | Value | ![The Knob widget: a round knob at 60 % with an arc showing the value](images/widgets/knob.png) |
| **Stepper** | Steps a value up and down. | Value | ![The Stepper widget: minus and plus buttons around a value](images/widgets/stepper.png) |
| **Numeric entry** | Types a number on an on-screen keypad, within its limits. | Value | ![The Numeric entry widget: a framed number with its caption](images/widgets/numeric-input.png) |
| **Text entry** | Types a text on an on-screen keyboard. | Value (STRING) | ![The Text entry widget: a framed text field with its caption](images/widgets/text-input.png) |
| **Selector** | Turns a rotary selector to one of two or three positions. | Value | ![The Selector widget: a rotary switch between HAND, OFF and AUTO, set to OFF](images/widgets/selector.png) |
| **Option buttons** | Picks one of several options. | Value | ![The Option buttons widget: Manual, Auto and Off, with Auto selected](images/widgets/option-buttons.png) |
| **Drop-down** | Picks one item from a list. | Value | ![The Drop-down widget, closed, showing the selected item](images/widgets/drop-down.png) |
| **Dialog** | Confirms an action in a pop-up before it happens. |  | ![The Dialog widget open over a dimmed screen: a warning icon, the title Stop the pump?, a message, and Cancel and Stop buttons](images/widgets/dialog.png) |

> **Tip:** Limits on a numeric entry or a slider are enforced on the device too: a value outside them is refused even if someone tries to send it another way.

---

## Process

Process symbols for P&ID style screens, usually placed in a **Diagram**. Symbols show a running or open state (and, where it applies, a fault) from their main value, with optional animation.

| Widget | Looks like |
|---|---|
| **Pump** | ![The Pump symbol](images/widgets/pump.png) |
| **Fan** | ![The Fan symbol](images/widgets/fan.png) |
| **Motor** | ![The Motor symbol](images/widgets/motor.png) |
| **Agitator** | ![The Agitator symbol](images/widgets/agitator.png) |
| **Conveyor** | ![The Conveyor symbol](images/widgets/conveyor.png) |
| **Valve** | ![The Valve symbol](images/widgets/valve.png) |
| **Control valve** | ![The Control valve symbol](images/widgets/control-valve.png) |
| **Check valve** | ![The Check valve symbol](images/widgets/check-valve.png) |
| **Three-way valve** | ![The Three-way valve symbol](images/widgets/three-way-valve.png) |
| **Heat exchanger** | ![The Heat exchanger symbol](images/widgets/heat-exchanger.png) |
| **Silo** | ![The Silo symbol](images/widgets/silo.png) |
| **Instrument** | ![The Instrument symbol](images/widgets/instrument.png) |

A **Pipe** connects two symbols' ports and can show flow, as in the diagram under [Containers](#containers). The **Instrument** shows an ISA style tag bubble with its measured value under it.

---

## Alarms and data

These widgets show tables kept by the PLC program rather than a single value. Instead of dropping a variable, you name the PLC variable in the widget's **Source**.

| Widget | Shows | Source | Looks like |
|---|---|---|---|
| **Alarm banner** | The newest alarm, with an acknowledge button. | An alarm summary. | ![The Alarm banner widget: the newest alarm, Tank level low, with its time and severity, a +2 more count and an ACK button](images/widgets/alarm-banner.png) |
| **Alarm list** | All active and unacknowledged alarms, each with its own acknowledge button. | An alarm table. | ![The Alarm list widget: three alarms with time, severity, message, state and an Ack button each, an Ack all button and an All alarms filter](images/widgets/alarm-list.png) |
| **Event log** | A log of alarms, acknowledgements and events. | An event log. | ![The Event log widget: a timeline of alarms raised and cleared, newest first](images/widgets/event-log.png) |
| **XY plot** | Points or a curve from two arrays. | Two arrays of REAL. | ![The XY plot widget: a curve drawn from two arrays, with scales on both axes](images/widgets/xy-plot.png) |
| **Data table** | Up to 8 tags, each with a description, a live value, a unit and a status color. | None: its values take variables like other widgets. | ![The Data table widget: four tags with descriptions, live values, units and a status dot, the last one red](images/widgets/data-table.png) |

The alarm table, summary and event log are kept by functions of the **HMI Alarms** library, which is also installed with the editor. Call them every scan in your program:

```st
PROGRAM Main
  VAR
    OverTemp, LowLevel : BOOL;
    Alarms : ARRAY[1..20] OF HMI_ALARM_ROW;
    AlarmSummary : HMI_ALARM_SUMMARY;
    Events : ARRAY[1..100] OF HMI_EVENT_ROW;
  END_VAR
  HMI_ALARM(In := OverTemp, Id := 1, Severity := 3, Message := 'Motor over temperature', Table := Alarms);
  HMI_ALARM(In := LowLevel, Id := 2, Severity := 2, Message := 'Tank level low', Table := Alarms);
  HMI_ALARMS(Summary := AlarmSummary, Table := Alarms);
  HMI_ALARM_LOGGER(Table := Alarms, Events := Events);
END_PROGRAM
```

- **HMI_ALARM** raises an alarm while **In** is TRUE. Severity is 1 (low), 2 (medium) or 3 (high).
- **HMI_ALARMS** applies the acknowledgements operators make on the screens and fills the summary.
- **HMI_ALARM_LOGGER** records raised, acknowledged and cleared alarms in the event log.
- **HMI_LOG_EVENT** adds your own entries to the event log, such as operator actions.

Then set the widgets' **Source** to the variables, for example `instance0.Main.Alarms` for an alarm list and `instance0.Main.AlarmSummary` for an alarm banner.

Size the arrays for your machine: the library sets no limit.

> **Note:** The alarm list and the event log need a target that supports them, such as OpenPLC Runtime v4. On a target without that support they are left out of the palette.

---

## More widgets

Any library you install can add widgets, and you can write your own. A library's widgets appear in the palette under their own groups. To write your own, see [Creating widgets](creating-widgets).
