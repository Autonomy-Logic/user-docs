# HMI Settings

**HMI Settings** holds the options that apply to the whole HMI of a project. It appears in the **HMI** branch of the project tree as soon as the project has a screen.

![HMI Settings with the General card (Start screen Overview, Frame period 100 ms, Default theme Autonomy, Font Compact, HMI address https://127.0.0.1:8443/hmi/), the Local panel card, the Screens by role grid with Overview ticked for Admin, Engineer, Operator and Viewer, and the Project themes card](images/hmi-settings-roles.png)

---

## General

| Setting | What it does |
|---|---|
| **Start screen** | The screen a display opens on after signing in, or a panel after it starts. |
| **Frame period (ms)** | How often screens update, in milliseconds. 100 (ten times a second) suits most screens. A shorter period makes animations smoother and costs more of the device's time. |
| **Default theme** | The theme of every screen that does not pick its own. |
| **Font** | **Compact** or **Full**. Compact covers English and Western European text and keeps a panel's firmware small. Full covers every character the font has. |
| **HMI address** | Where browsers open the HMI on OpenPLC Runtime v4: `https://<device IP>:8443/hmi/`. It shows the device's address once one is set in the device configuration. |

---

## Screens by role

The grid decides which accounts can open each screen. A row is a screen, a column is a role:

- **Admin** always has every screen. Its column cannot be unticked.
- **Engineer** gets every new screen.
- **Operator** and **Viewer** get only the screens you tick for them.

A new screen is visible to Admin and Engineer only. Tick it for Operator or Viewer when it is ready for them.

The device enforces the grid. An account that may not open a screen cannot reach it, even by navigating from another screen, and does not receive its values. When a role may open none of the screens, the display says so after signing in.

What each role may do outside the HMI (upload programs, debug, manage accounts) is described in [User management](../building-deploying/user-management).

> **Tip:** Give operators and viewers their own screens. A viewer typically gets overview and trend screens; an operator also gets the screens with controls.

---

## Themes

A theme is a set of colors: background, surfaces, text, borders, accent, and the success, warning and danger colors. Widgets that use theme colors follow the theme of their screen.

The editor comes with **Autonomy** (the default), **Light**, **Dark**, **Classic** and **Ocean**.

To make your own, type a name under **Project themes** and click **Add theme**. Pick the theme it starts from, then change the colors you want: the preview beside the colors shows a sample screen in the theme as you edit. A project can have up to 16 themes in total.

Pick a theme for one screen with the theme picker above its canvas, or for all screens with **Default theme**.

> **Tip:** A project theme is a quick way to rebrand an HMI for a customer: change the accent and surface colors once, and every screen follows.

---

## Local panel

This card applies to boards with their own display, such as the ESP32 CYD. On other targets it says *The selected board has no local panel.*

| Setting | What it does |
|---|---|
| **Require a PIN** | The panel shows a PIN entry before the screens. |
| **PIN** | 4 to 8 digits. |
| **Lock again** | **After idle minutes** (set the **Idle minutes** without a touch) or **Only at startup**. |
| **Touch calibration** | For panels whose touch needs calibrating: **Once** (until a calibration is stored), **After every program upload** or **On every boot**. |

A screen can also lock the panel with the **Lock the panel** action, and open the calibration with **Calibrate touch**.

> **Warning:** The panel PIN keeps casual users away from the screens. It is not a safety function and not strong protection: anyone with physical access to the panel can reach the device. Protect the panel physically, and keep safety functions in the PLC program and the machine's safety circuits.
