# Persistent storage for retained variables

A PLC loses the contents of its memory when it powers down. Most of the time that is what you want: the program starts from a known state. Sometimes it is not. A production counter, a totaliser, an operator's chosen recipe or a machine's last mode are all values that should still be there after a power cut.

IEC 61131-3 handles this with **retained** variables, and this page covers both halves of making them work:

1. Marking a variable as retained, in the variables table.
2. Telling the device where to keep the values, on the **Persistent Storage** screen.

Both are needed. A retained variable on a device with no storage configured behaves like an ordinary one, starting at its initial value every time.

## Marking a variable as retained

Retention is set per variable, in the **Flags** column of the variables table.

![The variables editor for a program. The Flags column sits between Class and Type; the row for a DINT named parts_made has its Flags dropdown open, showing the three options: a dash, Constant, and Retain](../images/variables-flags-column.png)

| Flag | IEC declaration | Meaning |
|---|---|---|
| **—** | `VAR` | The default. The variable starts at its initial value on every start. |
| **Constant** | `VAR CONSTANT` | Fixed at build time and never written at run time. |
| **Retain** | `VAR RETAIN` | The value is preserved across a restart, if the device has somewhere to keep it. |

The dash is a real choice, not an empty placeholder: pick it to clear a flag you set earlier.

A **Constant** cannot have a `Location`. It is folded into the program when you build, so there is no storage behind it to bind an address to; setting the flag clears the `Location` cell.

Keep the retained set small. Every retained variable is written to storage on the interval you configure below, and on flash or an SD card that write budget is finite. Retain the handful of values that genuinely have to survive, not everything that might be interesting.

## The Persistent Storage screen

Once your program has retained variables, the device needs somewhere to put them. That setting lives on the device, not in the project, so it has its own screen under the **Device** branch of the project tree.

![The project tree with the Device branch expanded, showing Orchestrators and Persistent Storage beneath it](../images/tree-persistent-storage.png)

Being device-scoped matters. Two people opening the same project against two different PLCs are configuring two different things, and neither setting travels with the project. It works the same way as User Management, for the same reason.

### When the screen appears

It is in the tree when both of these hold:

- **You are connected to the device.** The screen reads its values from the runtime, so there is nothing to show until a connection exists. Open it without one and it says so.
- **The runtime is version 4.2.0 or newer.** Earlier runtimes have no built-in store to configure.

It is also removed, deliberately, on a board whose vendor package provides its own retention. See [When a board handles retention itself](#when-a-board-handles-retention-itself) below.

### Configuring it

![The Persistent Storage screen. A heading and explanatory line at the top with a refresh button at the right; a checkbox "Keep retained variables on this device" with its help text; a File location field showing an absolute path in a monospace font; a "Save every" number field reading 5 with the unit "seconds"; and Save and Cancel buttons below a divider](../images/persistent-storage-screen.png)

**Keep retained variables on this device**

Off by default, matching the runtime. Until you turn it on, retention does nothing and every retained variable starts at its initial value. Turning it on enables the two fields below.

**File location**

An absolute path on the device where the values are written. The default is shown beneath the field and is the right answer for almost everyone.

The runtime checks the path when you save, and refuses one it could not honour, telling you exactly what is wrong:

- The path must be **absolute**, so that it does not depend on which directory the runtime happened to start in.
- It must be given in **normalised form**, without `..` segments.
- It must name a **file**, not an existing directory.
- Its **parent directory must already exist**. Otherwise every save would fail on the device with nothing but a log line to show for it.

**Save every**

How often the runtime commits the retained values to storage, between **1 and 3600 seconds**, defaulting to **5**.

This number is a real trade-off, not a default to leave alone:

- **A shorter interval risks less.** The interval is the window of recent change a power cut can cost you. Save every second and you lose at most a second's worth.
- **A shorter interval works the storage harder.** On an SD card or onboard flash, that shortens its life.

Pick from how much loss the process can absorb. A parts counter that can be off by a few units after an outage is fine at 30 seconds. A totaliser feeding a billing record is not.

**Save** and **Cancel** become available once you change something. Cancel restores the values currently on the device; the refresh button at the top right re-reads them.

### Changes apply at the next PLC start

Saving writes the settings to the device immediately, and the runtime reads them when it next loads a program. **A running PLC keeps using the settings it started with.** Stop and start it, or upload again, for a change to take effect.

### Viewing versus changing

Anyone signed in to the device can open the screen and read how it is configured. **Changing the settings requires an administrator account** on that device. If yours is not, the runtime refuses the save and says so.

## What happens at run time

With storage enabled and a program holding retained variables:

- The runtime works out how many bytes the program's retained variables occupy and reports it in the device log when the program loads.
- Values are committed on your interval, written in a way that survives a power cut partway through the write. Either the previous contents or the new ones are there, never a half-written mixture.
- On the next start, the values are restored before the program's first scan.

**A change to the program's retained variables discards the stored values.** Add, remove, reorder or retype a retained variable and the saved data no longer describes the program that is loading, so it is not restored, and those variables start at their initial values once. This is the correct outcome: restoring bytes into a different set of variables would put arbitrary values into them. Expect it after any change to your retained set, and plan the first start after a deployment accordingly.

## When a board handles retention itself

Some boards keep retained values in hardware, in battery-backed RAM or FRAM, through a driver in their vendor package. That is better than a file when it is available: it is faster and it does not wear out.

When you target such a board, the editor **removes the Persistent Storage screen from the tree and switches the runtime's own file store off on the device.**

The two go together on purpose. Removing only the screen would be worse than leaving it: the built-in store would keep running alongside the hardware one, both writing on every scan, both appearing to work, and which set of values you got back after a power cut would depend on timing. Turning it off leaves exactly one thing responsible for retention.

You do not need to do anything for this. It happens when you connect, and again if you change target. Retention still works; it is the vendor's driver doing it, and there is nothing on this screen for you to set.

## If retained values are not surviving a restart

Work down this list:

1. **Is the variable's Flags cell set to Retain?** An ordinary variable is never preserved.
2. **Is the checkbox on?** Off is the default, and it is a no-op until turned on.
3. **Was the PLC restarted after you saved the settings?** They apply at the next program load, not immediately.
4. **Did the program's retained variables change?** Any change to the set discards the stored values once, as above.
5. **Check the device log after a start.** The runtime reports how many bytes it is retaining and where they are being kept, which distinguishes "storage is not configured" from "the program retains nothing".
6. **Is the path still valid?** A path whose directory was removed after you saved it fails on every write.

## Related

- **[The variables editor](../working-with-variables/variables-editor)** for the Flags column in context.
- **[Global Variable Lists](../working-with-variables/global-variable-lists)**, whose list-level qualifier is preserved but not applied. Retention has to be set on a POU or Resource variable.
- **[Deployment to a vPLC](deployment-vplc)** for connecting to a device in the first place.
