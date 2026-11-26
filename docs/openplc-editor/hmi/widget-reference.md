# Widget reference

Everything a widget block can use: what it inherits, what it can override, the drawing and input functions, and the attributes that shape how the designer presents it. For a walkthrough, start with [Creating widgets](creating-widgets).

Positions and lengths are in **logical units** (lu). On a display at normal density, one lu is one pixel: an 800 by 480 panel is 800 by 480 lu. Angles are whole degrees, clockwise from 3 o'clock.

---

## What every widget has

Every widget block extends `HmiElement`, directly or through another widget, and inherits these.

### Inputs (properties)

| Input | Meaning |
|---|---|
| `Parent` | The container the element sits in. |
| `AutoSize`, `Span` | Sizing in a stack. See [Screen layout that fits any display](layout). |
| `PrefWidth`, `PrefHeight` | Fixed size when AutoSize is off. 0 means the natural size. |
| `MinWidth`, `MaxWidth`, `MinHeight`, `MaxHeight` | Limits to the size. 0 means no limit. |
| `Floating` | Left out of the layout. The screen's code places it. |
| `X`, `Y` | Position inside a diagram. |
| `Visible` | Hidden elements are not drawn and take no room. |
| `Enabled` | Controls ignore touch while it is FALSE. |

### The box (read only)

| Value | Meaning |
|---|---|
| `Left`, `Top`, `Width`, `Height` | The box the container gave the element this frame. |

### Helpers

| Helper | Returns |
|---|---|
| `Right()`, `Bottom()` | The right and bottom edges of the box. |
| `CenterX()`, `CenterY()` | The center of the box. |
| `Sc(V)` | A length `V`, designed at natural size, scaled to the size the widget has. Positive lengths stay at least 1. |
| `FitSize(Text, Size, Font, Avail)` | The largest text size up to `Size` at which `Text` fits in `Avail` lu. |
| `PointerOver()` | TRUE while the pointer is over the box (with a minimum touch area for small controls). |
| `MeasureWidth()`, `MeasureHeight()` | The size the element asks for: its preferred or natural size, within its limits. |

---

## What a widget can override

All of these are `METHOD PROTECTED OVERRIDE`.

| Method | Override it to |
|---|---|
| `NaturalWidth`, `NaturalHeight` | Say how big the widget would like to be. The base returns 0 (no wish). |
| `Draw` | Draw the widget. Return TRUE. |
| `TakesInput` | Return TRUE for a control, so it takes part in touch handling. |
| `Input` | Read the pointer and update the widget's state. Runs every frame, top-most widget first. Return TRUE when the widget took the press. |
| `ScaleWidth`, `ScaleHeight` | Choose the size `Sc()` scales against. By default the natural size. Override when the natural size follows a changing value (such as a text), so the scale stays steady. |
| `Prepare` | Compute geometry that depends on other elements before anything is drawn. |

---

## Drawing

Colors are `UDINT`: use the `COLOR` constants (see [Screen code](screen-code#colors)) and `HMI_Alpha(Color, OpacityPct)`.

| Function | Draws |
|---|---|
| `HMI_FillRect(X, Y, W, H, Radius, Color)` | A filled rectangle with rounded corners (Radius 0 for square). |
| `HMI_StrokeRect(X, Y, W, H, Radius, Width, Color)` | A rectangle outline, drawn inside the rectangle. |
| `HMI_Line(X1, Y1, X2, Y2, Width, Color)` | A line. |
| `HMI_FillCircle(Cx, Cy, R, Color)` | A filled circle. |
| `HMI_StrokeCircle(Cx, Cy, R, Width, Color)` | A circle outline, centered on the radius. |
| `HMI_FillEllipse(Cx, Cy, Rx, Ry, Color)` | A filled ellipse. |
| `HMI_StrokeEllipse(Cx, Cy, Rx, Ry, Width, Color)` | An ellipse outline. |
| `HMI_Arc(Cx, Cy, R, Width, A0, A1, Color)` | An arc from angle A0 to A1, centered on the radius. |
| `HMI_PolyBegin(Color)`, `HMI_PolyPoint(X, Y)`, `HMI_PolyFill()` | A filled polygon: begin, add points, fill. |
| `HMI_PolyStroke(Width, Closed)` | Strokes the polygon's points instead of filling them. |
| `HMI_Text(X, Y, Text, Size, Font, Align, Color)` | One line of text, aligned on X. |
| `HMI_TextBox(X, Y, W, H, Text, Size, Font, HAlign, VAlign, Color)` | Text aligned in a box. |
| `HMI_Clip(X, Y, W, H)`, `HMI_Unclip()` | Limits drawing to a rectangle, and ends the limit. |

Fonts are `HMI_FONT#Regular` and `HMI_FONT#Bold`. Alignments are `HMI_ALIGN#Left`, `#Center` and `#Right`, and vertically `HMI_VALIGN#Top`, `#Middle` and `#Bottom`.

> **Warning:** Take every position and length from `Left`, `Top`, `Width` and `Height`, with `Sc()` for fixed lengths. A drawing call with a fixed number as a position or length fails the build, and the preview warns when a widget draws outside its box.

---

## Text and numbers

| Function | Returns |
|---|---|
| `HMI_TextWidth(Text, Size, Font)` | The width of a text, in lu. |
| `HMI_FormatReal(Value, Decimals)` | A REAL as text, with that many decimals. |
| `HMI_FormatInt(Value)` | A DINT as text. |
| `HMI_FormatValue(Value, Decimals, Unit)` | A REAL as text followed by its unit. |
| `HMI_ParseReal(Text, Fallback)` | A REAL read from a text, or Fallback when the text is not a number. |
| `HMI_Truncate(Text, MaxLength)` | A text cut to at most MaxLength characters. |
| `HMI_ListCount(List)`, `HMI_ListItem(List, I)` | The number of items, and item I (from 0), of a list separated by `;`. |
| `HMI_Sin(Deg, Amp)`, `HMI_Cos(Deg, Amp)` | `Amp * sin(Deg)` and `Amp * cos(Deg)`, rounded, for drawing round shapes. |
| `HMI_TimeMs()` | A clock in milliseconds, for animations. Compare two readings to measure time. |

---

## Touch

| Function | Returns |
|---|---|
| `HMI_PtrX()`, `HMI_PtrY()` | The pointer position. |
| `HMI_PtrDown()` | TRUE while the pointer is pressed. |
| `HMI_PtrPressed()` | TRUE in the frame the pointer went down, if nothing on top took the press. |
| `HMI_PtrReleased()` | TRUE in the frame the pointer was released. |
| `HMI_PtrConsume()` | Takes this frame's press, so widgets underneath ignore it. |
| `HMI_Hit(X, Y, W, H)` | TRUE when the pointer is inside the rectangle. |

The usual pattern, in `Input`: on `HMI_PtrPressed()` with `PointerOver()`, start the press and call `HMI_PtrConsume()`. While the press lasts, follow the pointer. When `HMI_PtrDown()` turns FALSE, finish. See the example in [Creating widgets](creating-widgets#making-a-widget-interactive).

---

## Outputs and the designer

The designer reads a widget's inputs and outputs to decide how to present it:

| The widget has | The designer |
|---|---|
| A main input (`hmi_main`) | Binds a dropped variable to it. The widget shows the variable. |
| A main input plus outputs **Changed** and **NewValue** | Treats it as a control: a bound variable is also written with NewValue whenever Changed is TRUE. |
| A main BOOL output plus **Changed** | Treats it as a button: a dropped BOOL is written while it is pressed. |
| Other BOOL outputs | Lists them as events on the **Actions** tab, like **Clicked**. |

Make **Changed** and event outputs TRUE for one frame only, so each operator action is handled once.

---

## Attributes

Attributes go before a declaration, like `{attribute 'hmi_main'}`.

### On an input or output

| Attribute | Effect |
|---|---|
| `{attribute 'hmi_main'}` | The main value: what a dropped variable binds to. One per widget. |
| `{attribute 'hmi_color'}` | A color picker on the properties card. |
| `{attribute 'hmi_group' := 'data'}` | The properties card tab: `data`, `display` (shown as Style) or `layout`. |
| `{attribute 'hmi_enabled_by' := 'Name'}` | Greyed out on the card while the BOOL input `Name` is FALSE. |
| `{attribute 'hmi_element_ref'}` | A STRING input that names another element, picked from a list. |
| `{attribute 'hmi_preview' := '1'}` | On the main input: the value the preview and the palette thumbnail show. |
| `{attribute 'hmi_series' := 'value'}` | Marks one value of a multi-series widget (also `'color'` and `'count'`). |
| `{attribute 'hmi_range' := 'MinValue..MaxValue'}` | On **NewValue**: the values it can take. Numbers or input names. The device refuses writes outside it. |
| `{attribute 'hmi_max_length' := 'MaxLength'}` | On a STRING **NewValue**: its longest length, as a number or an input name. |

### On the widget block

| Attribute | Effect |
|---|---|
| `{attribute 'hmi_palette' := 'Group'}` | The palette group the widget appears in. A library's widgets need it to appear in the palette. Widget blocks of the project appear under **Project widgets**. |
| `{attribute 'hmi_default' := 'AutoSize := TRUE'}` | Start values for inherited inputs, which a derived block cannot declare again. |

---

## Popups

A widget can open a popup that draws above everything else, like the numeric entry's keypad. Call `SetPopup(TRUE)` to open it and `SetPopup(FALSE)` to close it, check it with `PopupOpen()`, and override `DrawPopup` and `PopupInput` to draw it and handle its touches. A popup closes by itself when its widget is hidden or disabled.
