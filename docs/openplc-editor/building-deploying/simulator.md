# Running Programs with the Simulator

The OpenPLC Simulator lets you run and test your PLC programs directly in the browser. No hardware, no Orchestrator, and no Device required. It's the fastest way to get started and is ideal for learning, prototyping, and testing logic before deploying to real hardware.

## What Is the Simulator?

The Simulator is built into the IDE and selected by default when you create a new project. You don't need to configure anything. Just click **Start** and your program runs immediately in the browser. You can watch variables change in real time, force values, and debug your logic. All without leaving your desk or setting up any infrastructure.

> **Note:** The Simulator emulates a microcontroller (ATmega2560-compatible). This means most PLC logic. Timers, counters, Structured Text, Ladder Diagram, Function Block Diagram. Runs just like on real hardware. However, physical I/O (reading sensors, writing to outputs) has no effect since there's no hardware connected.

## Getting Started

The Simulator is already selected by default when you create a new project. You don't need to configure or enable anything. Just click **Start Simulator** and your program runs.

### Checking If the Simulator Is Selected

If you want to verify that the Simulator is the active target:

1. In the **Project Explorer** on the left, expand the **Device** folder.
2. Click on **Orchestrators** inside the Device folder.
3. The **Orchestrators** page shows available targets. At the top, you'll see **OpenPLC Simulator** with the label "Built-in simulator. No hardware required". When it's the active target, it shows a **Selected** badge.

Below the Simulator option, the page also lists your registered Orchestrators and their Devices. If you connect to a Device, the target switches to that Device automatically. When you disconnect, it switches back to the Simulator.

> **Tip:** In most cases you'll never need to visit this page. The Simulator is selected by default, and the IDE manages the switching automatically.

## Running Your Program

With a new project, the Simulator is ready to go. Just:

1. Click the **Start Simulator** button in the Activity Bar (the play icon on the left side of the screen).
2. Watch the Console Panel at the bottom. It shows build progress in real time.
3. Wait for the message: `Simulator is running. Connecting debugger...`
4. The Debugger panel opens automatically, showing your program's variables with live values.

> **Note:** When the Simulator is selected, the **Compile** button is disabled. The **Start Simulator** button handles both compilation and execution in one click.

## What Happens When You Click Start

The IDE runs the following steps automatically:

1. **Compiles your code**: Converts your project (Ladder, ST, FBD, etc.) into machine code.
2. **Builds the firmware**: Generates a firmware file targeting the emulated microcontroller.
3. **Starts the Simulator**: Loads and runs the firmware in the browser background.
4. **Connects the Debugger**: Opens a Modbus debug connection to the running simulation so you can monitor and interact with variables.

The entire process typically takes 10–30 seconds depending on project complexity.

## Monitoring Variables

Once the Simulator is running, the **Debugger** panel shows all your program variables with their current values, updating in real time as the simulation runs. You can:

- **Watch values**: See inputs, outputs, and internal variables tick through their values as your logic executes.
- **Force a value**: Right-click a variable to force it to a specific value, simulating an input signal without hardware.
- **Release a forced value**: Right-click again and release to let the program control the variable.

## Stopping the Simulator

Click the **Stop Simulator** button (the same button, now showing a stop icon) to halt the simulation. Your code and project are preserved. You can make changes and click **Start Simulator** again to restart.

## When to Use the Simulator vs. a Real Device

| Situation | Recommended |
|-----------|-------------|
| Learning PLC programming for the first time | Simulator |
| Prototyping new logic quickly | Simulator |
| Testing without access to a Linux machine | Simulator |
| Validating logic with real sensor/actuator I/O | Real Device (vPLC) |
| Running 24/7 in production | Real Device (vPLC) |
| Testing communication protocols (Modbus, OPC-UA) | Real Device (vPLC) |

## Common Questions

**Do I need an Orchestrator or Device to use the Simulator?**
No. The Simulator runs entirely in your browser. You don't need to install anything, set up an Orchestrator, or create a Device.

**Can I use the Simulator without an account?**
You need an Autonomy Edge account to access the IDE. Once you're logged in, the Simulator is available to everyone. No additional setup required.

**My Simulator isn't starting. What do I check?**
- Go to **Device > Orchestrators** in the Project Explorer and confirm that "OpenPLC Simulator" shows the **Selected** badge. If a physical Device is connected, it takes priority. Disconnect from it first.
- Check the Console Panel for error messages. A red `[ERROR]` line will explain what went wrong.
- If the Console shows "Arduino compilation failed", there may be a syntax error in your code. Fix the error and try again.

**Can I deploy the same program to a real device later?**
Yes. Once you've tested your logic in the Simulator, go to **Device > Orchestrators**, connect to a real Device, and click **Compile** to deploy. The IDE switches the target automatically when you connect.

---

## What's Next?

- [Deployment to vPLC Devices](deployment-vplc): Deploy your program to a real virtual PLC via an Orchestrator.
- [Project Compilation](project-compilation): Learn what happens during compilation and how to fix errors.
- [Debugger](../workspace-overview/debugger): Deep dive into monitoring and forcing variables at runtime.
