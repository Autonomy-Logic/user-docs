# Headless CLI, `openplc-cli`

`openplc-cli` runs the editor's operations from a terminal, with no window: create a project, build it, upload it to a device, and drive a live debug session against real hardware. It exists for the cases a GUI cannot serve, above all automated testing and build pipelines.

Every command triggers the same operation the corresponding editor control triggers. `openplc-cli compile` runs what **Build** runs; `openplc-cli debug read` reads a variable the way the Debugger reads it. It is one program with two front ends, not a second implementation that has to be kept in step, so a build that passes in the pipeline is a build that would pass in the editor.

| Editor control | Command |
|---|---|
| **Build** | `openplc-cli compile <project>` |
| **Build & Upload** | `openplc-cli upload <project>` |
| Device search, serial-port list | `openplc-cli devices` |
| **Debug** | `openplc-cli debug open …` |
| **Start** / **Stop** | `openplc-cli debug start` / `stop` |
| Variable monitoring, the force dialog | `openplc-cli debug read` / `force` |

> The CLI ships inside the **desktop** OpenPLC Editor application, which is what supplies the compiler and the device transports it drives. It runs on a machine with the desktop editor installed, including a headless CI machine, and works against the same devices as the editor.

## Installing

The openplc-cli utility is a small launcher placed on your `PATH`. The application installs it **the first time it runs**, so opening OpenPLC Editor once is usually all it takes, on Windows, Linux and macOS alike.

```sh
openplc-cli --version
```

The launcher goes into the first directory you can write to, preferring one already on your `PATH`:

| Platform | Directory |
|---|---|
| macOS, Linux | `~/.local/bin`, then `~/bin` |
| Windows | `%LOCALAPPDATA%\Programs\openplc-cli` |

Nothing is written to a privileged location and you are never asked for an administrator password. If the chosen directory is not on your `PATH`, the editor prints the one line to add. On Windows the per-user `PATH` is updated for you, so open a new terminal afterwards.

### When the editor cannot be opened

A build image that never launches the GUI has nowhere to get the launcher from, so ask the application for it directly. This is the one case where you invoke the **application binary**, not `openplc-cli`:

```sh
# Linux (AppImage)
./'OpenPLC Editor-4.2.2.AppImage' --cli install-cli

# macOS
'/Applications/OpenPLC Editor.app/Contents/MacOS/OpenPLC Editor' --cli install-cli
```

```bat
REM Windows
"%LOCALAPPDATA%\Programs\OpenPLC Editor\OpenPLC Editor.exe" --cli install-cli
```

Run the same command again if you later move the application, or just open the editor once, which notices and repairs the launcher itself.

### macOS

Install the application into `/Applications` first, then open it once.

Installing from the mounted `.dmg` does not work, and the application says so rather than installing something that breaks later: the launcher would point inside the disk image and stop working the moment it is ejected. The same applies if macOS has quarantined the application, which is what happens when you launch it straight out of `Downloads`.

### Linux

The editor ships as an AppImage, which is mounted at a new temporary path every time it starts, so the launcher points at the **`.AppImage` file itself**. Put the file where you intend to keep it before opening it the first time. If you move it later, open it again, or re-run the `--cli install-cli` form above.

```sh
chmod +x 'OpenPLC Editor-4.2.2.AppImage'
./'OpenPLC Editor-4.2.2.AppImage'          # opening it once is what installs the launcher
openplc-cli --version
```

You do **not** need `xvfb-run` or a display server for the CLI itself. An SSH session or a CI runner with no display works as it is.

Containers are the one case needing an extra switch, and only once. Container runtimes usually block the sandboxing feature the application would otherwise use, so pass `--no-sandbox` on the installing call:

```sh
./OpenPLC-Editor.AppImage --no-sandbox --cli install-cli
openplc-cli devices        # no switches needed from here on
```

The launcher records that it was installed this way and carries the switch for you afterwards. A normal desktop install does not get it, and keeps the sandbox.

### Windows

Run the installer, then launch the editor once. `openplc-cli.cmd` is placed in `%LOCALAPPDATA%\Programs\openplc-cli` and that directory is added to your user `PATH`. Open a new terminal afterwards.

> **Calling it from a `.bat` or `.cmd` script needs `call`.** The launcher is a batch file, and one batch file invoking another without `call` hands over control instead of returning, so the rest of your script never runs and you never see the exit code. This is how every `.cmd` wrapper behaves, `npm.cmd` included.
>
> ```bat
> call openplc-cli compile "C:\path\to\project"
> if errorlevel 1 exit /b %ERRORLEVEL%
> ```
>
> From PowerShell, an interactive `cmd` prompt, or any non-batch caller, the plain form is right and the exit code is set as expected.

Redirection and piping work normally (`openplc-cli devices > devices.json`), which is what matters for a test harness.

## The commands

```
openplc-cli create <name> --path <dir> [--type plc-project|plc-library]
                          [--language st|il|ld|sfc|fbd] [--time <interval>] [--force]
openplc-cli install-cli                   (re-place the launcher; see Installing)
openplc-cli devices [--timeout <ms>]
openplc-cli compile <project> [--target <board>] [--port <serial>] [--clean]
openplc-cli upload  <project> (--host <address> | --port <serial>)
                              [--target <board>] [--clean] [-y|--yes]
openplc-cli debug   open|list|status|list-vars|read|write|force|unforce
                    |start|stop|watch|poll|unwatch|close|repl|exec
```

### `devices`

Everything reachable: OpenPLC runtimes found on the network, and the serial ports on this machine. The same two searches the editor's device picker and port dropdown run.

```sh
openplc-cli devices
openplc-cli devices --timeout 5000
```

### `create`

A new project or library on disk, matching what the New Project wizard produces.

```sh
openplc-cli create demo --path ./workspace --language st
openplc-cli create utils --path ./workspace --type plc-library
```

`--force` overwrites an existing destination.

### `compile`

Builds the project and writes its artifacts to the project's build directory. Nothing is sent anywhere.

```sh
openplc-cli compile ./my-project --target "OpenPLC Runtime v4"
```

`--clean` discards the build directory first, which is what you want in a pipeline: a stale directory from an earlier run can otherwise make an incomplete build look complete.

### `upload`

Builds, then sends the result to a device. Give it either a network address or a serial port:

```sh
openplc-cli upload ./my-project --host 192.168.2.4 --credentials "$PLC_USER:$PLC_PASS"
openplc-cli upload ./my-project --port /dev/ttyACM0
```

Targets that compile on the device itself refuse to build while the PLC is **RUNNING**, exactly as the editor warns: building on a running device can stall the build or make the program miss its scan deadlines. `--yes` (or `-y`) approves stopping it first, the way `apt install -y` does. Nothing stops a running PLC without being asked.

## Output, and how to read it

The CLI decides its format by where output is going. Human-readable text at a terminal; JSON when it is piped or redirected. `--json` and `--no-json` override the choice.

In JSON mode:

- **stdout carries exactly one JSON document**, the result. Nothing else. Parsing it needs no filtering.
- Progress, warnings and diagnostics go to **stderr**.
- No colour, spinners or progress bars.
- Values carry their type, so `0` is unambiguously `BOOL FALSE` or `INT 0`. 64-bit integers arrive as decimal strings, which a JSON number cannot hold exactly.
- Errors are objects with a stable `code`. The wording beside it may change between versions; the code will not.

```sh
BUILD=$(openplc-cli compile ./my-project --target "OpenPLC Runtime v4") || exit $?
echo "$BUILD" | jq -r '.buildDirectory'
```

### Exit codes

Gate your pipeline on these rather than on log text.

| Code | Meaning |
|---|---|
| `0` | Success |
| `2` | Usage: unknown command, missing or malformed argument |
| `3` | Not found: project, file or session |
| `4` | Compile failed |
| `5` | Connection: could not reach the target, or lost it |
| `6` | Authentication: credentials refused |
| `7` | Target error: the device reported a failure |
| `8` | Timeout |
| `70` | Internal error |

## Credentials

A device reached through its runtime API needs them. A board flashed over USB does not.

```sh
--credentials user:pass          # or --user and --password
OPENPLC_CREDENTIALS=user:pass    # or OPENPLC_USER and OPENPLC_PASSWORD
```

**Prefer the environment variables in CI.** A command-line flag lands in shell history and in job logs.

`--create-user` grants permission to create the **first** user on a fresh runtime, using the credentials you already passed. It applies to `upload` and `debug open`, and does nothing on a runtime that already has users.

## Debug sessions

A debug session is long-lived, while a test step is a single short-lived process. So the CLI splits the two: `debug open` starts a session in the background and prints a **session id**, and every other debug command is a quick call that attaches to it. No reconnect, no re-verification and no re-upload per command.

```sh
openplc-cli debug open ./my-project --target "OpenPLC Runtime v4" \
  --host 192.168.2.4 --credentials "$PLC_USER:$PLC_PASS"      # prints a session id

openplc-cli debug list                          # every live session
openplc-cli debug status
openplc-cli debug list-vars --filter main
openplc-cli debug read main:counter
openplc-cli debug write main:setpoint --value 250
openplc-cli debug force main:enable TRUE
openplc-cli debug start
openplc-cli debug stop
openplc-cli debug close --all
```

With one session open, `--session` is optional. With more than one, it is required.

### Watching for changes between commands

`watch` **records into a buffer inside the session** rather than streaming to your terminal. `poll` drains what has been recorded.

```sh
openplc-cli debug watch main:counter --interval 100
# ... your test does something ...
openplc-cli debug poll
```

This is the point of the session model: a transition that happens between two of your own commands is still there when you poll for it. A streaming design would lose it, because your process was not running at the time.

`--since <sequence>` on `poll` returns only samples after a sequence number you already have.

### Sessions close themselves after 30 minutes idle

The one behaviour a long-running harness has to plan for, because closing a session **releases the variables it forced**. On live hardware, mid-test, if the run has been quiet long enough.

| | |
|---|---|
| Default | 30 minutes with no command |
| `--idle-timeout <ms>` on `debug open` | A different budget |
| `--idle-timeout 0` | Never close on idle |

"Idle" means no command reached the session. Two things deliberately do not count as activity: `watch` sampling in the background, and `debug list`, so that polling a list of sessions cannot keep them alive indefinitely.

### Forcing, and why close releases

`close` releases the variables the session forced, unless you pass `--keep-forces`.

This is deliberate. A force lives in the runtime, and the runtime cannot tell that a debugger has gone away: it clears forces only when the program is unloaded or stopped. A session that simply exited would leave outputs pinned on a live PLC.

`debug status` reports what the session has forced, which is what `close` will release. A stop issued from somewhere else, the runtime's own interface or a mode switch, clears forces without the session knowing, so that list can be out of date.

### Scripting a sequence

`debug exec` reads one command per line, from a file or from standard input:

```sh
openplc-cli debug exec ./test-sequence.txt
```

```
start
force main:enable TRUE
read main:counter
unforce main:enable
stop
```

By default it stops at the first failure; `--keep-going` runs the rest.

`debug repl` is the same thing with a prompt, for a person at a terminal. Use `exec` in scripts: the REPL refuses piped input rather than silently dropping commands.

### Flags by command

| Flag | Command | Meaning |
|---|---|---|
| `--session <id>` | any `debug` subcommand | Which session, when several are open |
| `--idle-timeout <ms>` | `debug open` | Idle budget; `0` disables it |
| `--force-new` | `debug open` | Start a session even if one is already open for this project and target |
| `--upload-if-needed` | `debug open` | Upload first if the device's program does not match |
| `--var <name>` | `read`, `write`, `force`, `unforce` | The variable, when you would rather not pass it positionally |
| `--value <literal>` | `write`, `force` | The value: `16#FF`, `TRUE`, `T#5s`, all as the editor accepts them |
| `--filter <substring>` | `list-vars` | Only variables whose path contains it |
| `--interval <ms>` | `watch` | Sampling cadence, minimum 20 ms |
| `--since <seq>` | `poll` | Only samples after this sequence number |
| `--keep-forces` | `close` | Leave forced variables pinned |
| `--all` | `close` | Every session, not just one |
| `--keep-going` | `exec` | Run the remaining lines after one fails |
| `--force` | `create` | Overwrite an existing destination |
| `--clean` | `compile`, `upload` | Discard the build directory first |
| `-y`, `--yes` | `upload` | Approve stopping a RUNNING PLC before building on it |
| `--create-user` | `upload`, `debug open` | Permission to create the first user on a fresh runtime |
| `--user-data <dir>` | any | Use a different editor state directory (see below) |

## In a build pipeline

A step looks like any other:

```sh
openplc-cli compile ./my-project --target "OpenPLC Runtime v4"   # 0, or 4 on a compile error
openplc-cli upload  ./my-project --host "$PLC_HOST" --yes
```

Because stdout carries one JSON document and progress goes to stderr, a step that both reports and gates looks like this:

```sh
set -e
BUILD=$(openplc-cli compile ./my-project --target "OpenPLC Runtime v4")
echo "artifacts: $(echo "$BUILD" | jq -r '.buildDirectory')"

openplc-cli upload ./my-project --host "$PLC_HOST" --yes
```

The exit code is the thing to branch on. A compile error gives `4`, an unreachable device `5`, refused credentials `6`:

```sh
if ! openplc-cli compile ./my-project --target "OpenPLC Runtime v4" > build.json; then
  case $? in
    4) echo "compile failed";       exit 1 ;;
    5) echo "could not reach PLC";  exit 1 ;;
    *) echo "unexpected failure";   exit 1 ;;
  esac
fi
```

On Linux, you need Electron's shared libraries, which a slim base image will not have:

```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
      libgtk-3-0 libnss3 libasound2 libgbm1 libxss1 libxtst6 \
      libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 \
      libxcomposite1 libxdamage1 libxfixes3 libxrandr2 \
      libpango-1.0-0 libcairo2 libatspi2.0-0 \
 && rm -rf /var/lib/apt/lists/*
```

Then, once per image:

```sh
./OpenPLC-Editor.AppImage --no-sandbox --cli install-cli
```

### A clean machine needs no warm-up

The CLI creates the editor's own settings and state directory itself the first time it runs, so a fresh container needs no preparatory step.

**Board packages are the exception.** A target provided by an installed `.vpp` package is only available if that package is present in the state directory the CLI is using. Point `--user-data <dir>` at a directory you prepared with the packages your project needs.
