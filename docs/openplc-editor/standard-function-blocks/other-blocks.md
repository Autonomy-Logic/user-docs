# Additional Function Blocks

Beyond timers, counters, bistables, and edge detectors, the IEC 61131-3 standard library includes function blocks for real-time clocking, process control, signal generation, and network communication. These blocks are available in the Autonomy Edge web IDE under **System Libraries** and address more specialized automation needs. From PID loop control to TCP socket communication.

---

## RTC: Real-Time Clock

The RTC block gives you access to the current date and time. When enabled, it outputs the current date-time value, offset by a user-supplied starting reference. This is useful for timestamping events, scheduling operations, or implementing time-of-day logic.

### Inputs

| Name | Type | Description |
|------|------|-------------|
| `IN` | `BOOL` | Enable. Starts the clock when TRUE |
| `PDT` | `DT` | Preset Date and Time. Reference starting point |

### Outputs

| Name | Type | Description |
|------|------|-------------|
| `Q` | `BOOL` | TRUE while the clock is running |
| `CDT` | `DT` | Current Date and Time |

### Behavior

- On the rising edge of `IN`, the block captures the difference between the system time and `PDT` as an offset.
- While `IN` is TRUE, `CDT` outputs the system time adjusted by this offset, and `Q` is TRUE.
- When `IN` goes FALSE, `Q` goes FALSE and `CDT` holds its last value.

### Structured Text Example

```iecst
PROGRAM TimeStamper
  VAR
    EnableClock : BOOL := TRUE;
    StartTime   : DT := DT#2025-01-01-00:00:00;
    ClockActive : BOOL;
    CurrentTime : DT;
    Clock       : RTC;
  END_VAR

  Clock(IN := EnableClock, PDT := StartTime);
  ClockActive := Clock.Q;
  CurrentTime := Clock.CDT;
END_PROGRAM
```

---

## INTEGRAL: Integration Block

The INTEGRAL block performs numerical integration of an input signal over time. It calculates the running integral of `XIN` using the trapezoidal method, accumulating the result in `XOUT`. You'll commonly use this in process control for computing flow totals from flow rate measurements, or as a building block within PID controllers.

### Inputs

| Name | Type | Description |
|------|------|-------------|
| `RUN` | `BOOL` | Enable integration when TRUE |
| `R1` | `BOOL` | Reset. Sets XOUT to X0 when TRUE |
| `XIN` | `REAL` | Input signal to integrate |
| `X0` | `REAL` | Initial value for XOUT after reset |
| `CYCLE` | `TIME` | Execution cycle time (must match task interval) |

### Outputs

| Name | Type | Description |
|------|------|-------------|
| `Q` | `BOOL` | TRUE while integration is running |
| `XOUT` | `REAL` | Integrated output value |

### Behavior

- When `R1` is TRUE, `XOUT` is set to `X0`.
- When `RUN` is TRUE and `R1` is FALSE, `XOUT` accumulates the integral of `XIN` over time.
- `CYCLE` must match the actual execution interval of the task running this program. Incorrect values produce inaccurate results.

> **Tip:** If your task runs every 100ms, set `CYCLE := T#100ms`. Getting this wrong is the most common cause of inaccurate integration results.

### Structured Text Example

```iecst
PROGRAM FlowTotalizer
  VAR
    Measuring   : BOOL := TRUE;
    ResetTotal  : BOOL;
    FlowRate    : REAL;        (* Liters per second from sensor *)
    TotalVolume : REAL;        (* Accumulated liters *)
    Integrator  : INTEGRAL;
  END_VAR

  Integrator(RUN := Measuring, R1 := ResetTotal,
             XIN := FlowRate, X0 := 0.0, CYCLE := T#100ms);
  TotalVolume := Integrator.XOUT;
END_PROGRAM
```

---

## DERIVATIVE: Differentiation Block

The DERIVATIVE block computes the rate of change of an input signal over time. It approximates the mathematical derivative of `XIN`, outputting the result in `XOUT`. Use it to detect rapid changes in process variables or as a component within PID controllers.

The block uses multiple previous samples internally to produce a smoothed derivative, reducing the impact of noise in the input signal.

### Inputs

| Name | Type | Description |
|------|------|-------------|
| `RUN` | `BOOL` | Enable differentiation when TRUE |
| `XIN` | `REAL` | Input signal to differentiate |
| `CYCLE` | `TIME` | Execution cycle time (must match task interval) |

### Outputs

| Name | Type | Description |
|------|------|-------------|
| `XOUT` | `REAL` | Differentiated output (rate of change) |

### Structured Text Example

```iecst
PROGRAM RateOfChange
  VAR
    Monitoring     : BOOL := TRUE;
    Temperature    : REAL;     (* Current temperature reading *)
    TempChangeRate : REAL;     (* Degrees per second *)
    Differentiator : DERIVATIVE;
  END_VAR

  Differentiator(RUN := Monitoring, XIN := Temperature, CYCLE := T#100ms);
  TempChangeRate := Differentiator.XOUT;
END_PROGRAM
```

---

## PID: PID Controller

The PID block implements a Proportional-Integral-Derivative controller. The most widely used feedback control algorithm in industrial automation. It continuously calculates an error value (the difference between a desired setpoint and a measured process variable) and applies a correction based on proportional, integral, and derivative terms.

### Inputs

| Name | Type | Description |
|------|------|-------------|
| `AUTO` | `BOOL` | Automatic mode. TRUE enables PID control |
| `PV` | `REAL` | Process Variable. Measured value from the process |
| `SP` | `REAL` | Setpoint. Desired target value |
| `X0` | `REAL` | Manual output value (used when AUTO is FALSE) |
| `KP` | `REAL` | Proportional gain |
| `TR` | `REAL` | Integral time (reset time) in seconds |
| `TD` | `REAL` | Derivative time in seconds |
| `CYCLE` | `TIME` | Execution cycle time (must match task interval) |

### Outputs

| Name | Type | Description |
|------|------|-------------|
| `XOUT` | `REAL` | Controller output |

### Behavior

- When `AUTO` is TRUE, the block computes: `XOUT = KP * (ERROR + ITERM + DTERM)`
  - **Proportional**: Responds to the current error magnitude.
  - **Integral**: Accumulated error over time, eliminating steady-state offset. Controlled by `TR`.
  - **Derivative**: Rate of change of the error, providing anticipatory control. Controlled by `TD`.
- When `AUTO` is FALSE, `XOUT` is set directly to `X0` (manual mode). The integral term is held to prevent windup.

### Tuning Parameters

| Parameter | Effect of Increasing | Typical Starting Value |
|-----------|---------------------|----------------------|
| `KP` | Stronger response to error, but may cause oscillation | 1.0 – 10.0 |
| `TR` | Slower integral action (larger TR = less aggressive I-term) | 1.0 – 100.0 seconds |
| `TD` | Stronger damping of rapid changes | 0.0 – 10.0 seconds |

A common starting approach:
1. Set `TD` to 0 and `TR` to a very large value (effectively disabling the I and D terms).
2. Increase `KP` until the system responds reasonably without excessive oscillation.
3. Decrease `TR` gradually to eliminate steady-state error.
4. Increase `TD` if you need to reduce overshoot and dampen oscillations.

### Structured Text Example

```iecst
PROGRAM TemperatureControl
  VAR
    AutoMode      : BOOL := TRUE;
    CurrentTemp   : REAL;      (* Temperature sensor reading *)
    TargetTemp    : REAL := 75.0; (* Desired temperature *)
    ManualOutput  : REAL := 0.0;
    HeaterPower   : REAL;      (* 0-100% output to heater *)
    TempPID       : PID;
  END_VAR

  TempPID(AUTO := AutoMode, PV := CurrentTemp, SP := TargetTemp,
          X0 := ManualOutput, KP := 2.0, TR := 10.0, TD := 1.0,
          CYCLE := T#100ms);
  HeaterPower := TempPID.XOUT;
END_PROGRAM
```

---

## RAMP: Ramp Generator

The RAMP block generates a linearly increasing or decreasing output that transitions from one value to another over a specified time. Use it for soft-start of motors, gradual setpoint changes, or any application where abrupt value changes are undesirable.

### Inputs

| Name | Type | Description |
|------|------|-------------|
| `RUN` | `BOOL` | Enable the ramp when TRUE |
| `X0` | `REAL` | Starting value |
| `X1` | `REAL` | Target value |
| `TR` | `TIME` | Ramp duration (time to go from X0 to X1) |
| `CYCLE` | `TIME` | Execution cycle time (must match task interval) |

### Outputs

| Name | Type | Description |
|------|------|-------------|
| `BUSY` | `BOOL` | TRUE while the ramp is in progress |
| `XOUT` | `REAL` | Current ramp output value |

### Behavior

- When `RUN` goes TRUE, `XOUT` begins at `X0` and linearly moves toward `X1` over the duration `TR`.
- While ramping, `BUSY` is TRUE.
- When `XOUT` reaches `X1`, `BUSY` goes FALSE and `XOUT` holds at `X1`.
- If `RUN` goes FALSE during the ramp, `XOUT` holds at its current value.

### Structured Text Example

```iecst
PROGRAM SoftStart
  VAR
    StartMotor   : BOOL;
    Ramping      : BOOL;
    MotorSpeed   : REAL;       (* 0-100% speed command *)
    SpeedRamp    : RAMP;
  END_VAR

  SpeedRamp(RUN := StartMotor, X0 := 0.0, X1 := 100.0,
            TR := T#10s, CYCLE := T#100ms);
  Ramping    := SpeedRamp.BUSY;
  MotorSpeed := SpeedRamp.XOUT;
END_PROGRAM
```

The motor speed gradually increases from 0% to 100% over 10 seconds, avoiding the mechanical stress and current spikes of an instant start.

---

## HYSTERESIS: Hysteresis Boolean Output

The HYSTERESIS block produces a boolean output based on the difference between two real-valued inputs, with a deadband defined by `EPS`. This prevents rapid on/off switching (chattering) when a measured value hovers near a threshold.

### Inputs

| Name | Type | Description |
|------|------|-------------|
| `XIN1` | `REAL` | First input value (e.g., measured value) |
| `XIN2` | `REAL` | Second input value (e.g., threshold) |
| `EPS` | `REAL` | Hysteresis band (epsilon) |

### Outputs

| Name | Type | Description |
|------|------|-------------|
| `Q` | `BOOL` | Hysteresis output |

### Behavior

- `Q` switches to TRUE when `XIN1` falls below `(XIN2 - EPS)`.
- `Q` switches to FALSE when `XIN1` rises above `(XIN2 + EPS)`.
- When `XIN1` is between `(XIN2 - EPS)` and `(XIN2 + EPS)`, `Q` retains its previous value.

This creates a deadband of `2 * EPS` centered around `XIN2`, preventing the output from toggling when the input fluctuates near the threshold.

### Structured Text Example

```iecst
PROGRAM ThermostatControl
  VAR
    RoomTemp    : REAL;        (* Current temperature *)
    SetPoint    : REAL := 22.0; (* Desired temperature *)
    HeaterOn    : BOOL;        (* Output to heater relay *)
    TempHyst    : HYSTERESIS;
  END_VAR

  TempHyst(XIN1 := RoomTemp, XIN2 := SetPoint, EPS := 1.0);
  HeaterOn := TempHyst.Q;
END_PROGRAM
```

The heater turns on when the temperature drops below 21.0 (setpoint minus epsilon) and turns off when it rises above 23.0 (setpoint plus epsilon). This 2-degree deadband prevents the heater from rapidly cycling on and off.

---

## Communication Blocks

The System Libraries include TCP communication function blocks for network-based data exchange. These blocks let your PLC program open TCP connections, send and receive data, and close connections. They're useful for communicating with external systems, databases, or custom protocols.

### TCP_CONNECT

Establishes a TCP connection to a remote server.

**Inputs:**

| Name | Type | Description |
|------|------|-------------|
| `CONNECT` | `BOOL` | Initiates connection on rising edge |
| `IP_ADDRESS` | `STRING` | Remote server IP address |
| `PORT` | `INT` | Remote server port number |

**Outputs:**

| Name | Type | Description |
|------|------|-------------|
| `SOCKET_ID` | `INT` | Socket identifier for subsequent operations |

### TCP_SEND

Sends a string message over an established TCP connection.

**Inputs:**

| Name | Type | Description |
|------|------|-------------|
| `SEND` | `BOOL` | Triggers send on rising edge |
| `SOCKET_ID` | `INT` | Socket identifier from TCP_CONNECT |
| `MSG` | `STRING` | Message to send |

**Outputs:**

| Name | Type | Description |
|------|------|-------------|
| `BYTES_SENT` | `INT` | Number of bytes successfully sent |

### TCP_RECEIVE

Receives data from an established TCP connection.

**Inputs:**

| Name | Type | Description |
|------|------|-------------|
| `RECEIVE` | `BOOL` | Triggers receive on rising edge |
| `SOCKET_ID` | `INT` | Socket identifier from TCP_CONNECT |

**Outputs:**

| Name | Type | Description |
|------|------|-------------|
| `BYTES_RECEIVED` | `INT` | Number of bytes received |
| `MSG` | `STRING` | Received message data |

### TCP_CLOSE

Closes an established TCP connection.

**Inputs:**

| Name | Type | Description |
|------|------|-------------|
| `CLOSE` | `BOOL` | Triggers close on rising edge |
| `SOCKET_ID` | `INT` | Socket identifier from TCP_CONNECT |

**Outputs:**

| Name | Type | Description |
|------|------|-------------|
| `SUCCESS` | `INT` | Result code (0 = success) |

### TCP Communication Example

```iecst
PROGRAM DataReporter
  VAR
    DoConnect    : BOOL;
    DoSend       : BOOL;
    DoClose      : BOOL;
    SocketID     : INT;
    BytesSent    : INT;
    CloseResult  : INT;
    Connector    : TCP_CONNECT;
    Sender       : TCP_SEND;
    Closer       : TCP_CLOSE;
  END_VAR

  (* Step 1: Connect to the data server *)
  Connector(CONNECT := DoConnect,
            IP_ADDRESS := '192.168.1.100', PORT := 5000);
  SocketID := Connector.SOCKET_ID;

  (* Step 2: Send a status message *)
  Sender(SEND := DoSend, SOCKET_ID := SocketID,
         MSG := 'TEMP=75.2;PRESSURE=101.3');
  BytesSent := Sender.BYTES_SENT;

  (* Step 3: Close when done *)
  Closer(CLOSE := DoClose, SOCKET_ID := SocketID);
  CloseResult := Closer.SUCCESS;
END_PROGRAM
```

> **Tip:** In practice, you'd sequence these operations using state logic or timers to ensure each step completes before the next begins.

---

## What's Next?

With a solid understanding of the standard function block library, you can explore more advanced topics:

- [Task Configuration](../task-configuration/understanding-tasks): Configure how and when your programs execute on the runtime
- [Programming Languages](../programming-languages/structured-text/st-basics): Detailed guides for Structured Text, Ladder Diagram, FBD, and more
- [Communication Protocols](../communication/README): Set up Modbus and other industrial protocols for device-to-device communication
