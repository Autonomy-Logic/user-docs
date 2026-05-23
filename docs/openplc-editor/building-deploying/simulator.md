# In-process simulator (desktop only)

The standalone OpenPLC Editor (desktop) ships with an **in-process simulator** based on the `avr8js` ATmega2560 emulator. It runs the compiled firmware inside the editor without needing an external runtime.

**The web editor does not include this simulator.** USB device access and the AVR8JS bridge are Electron-side features that don't exist in the browser.

If you need to test programs without deploying to physical hardware while using the web editor, create a **virtual vPLC** on an orchestrator instead. A vPLC is a Docker container running the same OpenPLC runtime that a physical device would run; it behaves on the network like a standalone PLC. See **[Creating a vPLC](../../platform/vplcs/creating-a-vplc)** in the platform docs.

If you want the in-editor simulator specifically, install the desktop OpenPLC Editor and use it alongside Autonomy Edge — projects are interchangeable.

## What's next

- **[Connecting to a vPLC](../connecting-to-runtimes)** — the web-editor equivalent of "run my code somewhere".
- **[Project compilation](project-compilation)** — what the build options popover does.
- **[Debugger](debugger)** — live variable monitoring on a connected vPLC.
