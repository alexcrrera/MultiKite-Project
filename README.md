# MultiKite Project

Ground station setup guide: how to upload the firmware to an Arduino Mega and connect it to Serial Studio for live telemetry and control.

---

## Table of Contents

1. [Hardware Required](#1-hardware-required)
2. [Wiring](#2-wiring)
3. [Install Arduino IDE](#3-install-arduino-ide)
4. [Install Required Libraries](#4-install-required-libraries)
5. [Upload the Sketch](#5-upload-the-sketch)
6. [Install Serial Studio](#6-install-serial-studio)
7. [Configure and Connect Serial Studio](#7-configure-and-connect-serial-studio)
8. [Verify the Connection](#8-verify-the-connection)
9. [Command Reference](#9-command-reference)

---

## 1. Hardware Required

| Item | Notes |
|------|-------|
| Arduino Mega 2560 | Any genuine or compatible board |
| Hobbywing ESC | Pulse range 850–1940 µs; other ESCs may need `b_systemParameters.ino` adjusted |
| Base tilt servo | Continuous rotation or position servo (see wiring note) |
| Reel servo | Continuous rotation servo |
| USB Type-B cable | USB-A to USB-B, used for programming and serial communication |
| External 5 V BEC or power supply | For servo power — do **not** power servos from the Arduino 5 V pin |

---

## 2. Wiring

The three actuators connect to PWM-capable pins on the Mega. All signal wires share a common ground with the Arduino.

```
                  Arduino Mega 2560
                 ┌─────────────────────┐
  Base Tilt ◄── │ Pin  9  (PWM / OC2B)│
  ESC       ◄── │ Pin 10  (PWM / OC2A)│
  Reel      ◄── │ Pin 11  (PWM / OC1A)│
                │                     │
  GND rail  ◄── │ GND                 │
  PC        ◄── │ USB (programming    │
                │      + telemetry)   │
                └─────────────────────┘
```

**Servo power**: connect signal and ground from the Arduino; power the servo rail from an external BEC. Never run servo power through the Arduino's 5 V regulator — stall current can exceed its rating and damage the board.

**Changing pin assignments**: edit `BASE_PIN`, `ESC_PIN`, and `REEL_PIN` in `b_systemParameters.ino`. Verify the replacement pins support hardware PWM on the Mega — not all digital pins do.

---

## 3. Install Arduino IDE

### Windows

1. Download Arduino IDE 2.x from [arduino.cc/en/software](https://www.arduino.cc/en/software).
2. Run the `.exe` installer and accept the defaults (includes USB drivers for the Mega).
3. Launch Arduino IDE.

### macOS

1. Download the `.dmg` from [arduino.cc/en/software](https://www.arduino.cc/en/software).
2. Open the disk image and drag **Arduino IDE** into **Applications**.
3. On first launch, macOS may prompt to install additional components — allow it.

### Linux (Ubuntu / Debian)

```bash
# Option A – AppImage (recommended, always up to date)
chmod +x arduino-ide_*.AppImage
./arduino-ide_*.AppImage

# Option B – apt (may install an older version)
sudo apt update && sudo apt install arduino
```

---

## 4. Install Required Libraries

The sketch depends on three libraries. Install them via **Tools → Manage Libraries…** in Arduino IDE.

| Library | Search term in Library Manager | Purpose |
|---------|-------------------------------|---------|
| **TextParser** | `TextParser` (by Alex Taujenis) | Parses comma-separated incoming commands |
| **elapsedMillis** | `elapsedMillis` | Non-blocking millisecond/microsecond timers |
| **Servo** | Built-in — no install needed | PWM output to ESC and servos |

> **TextParser note**: if the Library Manager search returns no results, install manually:
> 1. Download from [arduinotextparser.readthedocs.io](https://arduinotextparser.readthedocs.io/en/latest/).
> 2. In Arduino IDE: **Sketch → Include Library → Add .ZIP Library…** and select the downloaded file.

---

## 5. Upload the Sketch

### 5.1 Select board and port

1. Connect the Arduino Mega to the computer via USB.
2. In Arduino IDE: **Tools → Board → Arduino AVR Boards → Arduino Mega or Mega 2560**.
3. **Tools → Processor → ATmega2560**.
4. **Tools → Port** — select the port that appeared when you plugged in the Mega:
   - **Windows**: `COMx` (e.g., `COM3`). If unsure: Device Manager → Ports (COM & LPT).
   - **macOS**: `/dev/cu.usbmodem` followed by a number.
   - **Linux**: `/dev/ttyACM0` or `/dev/ttyUSB0`. Run `ls /dev/tty*` before and after plugging in to find the new entry.

### 5.2 Open the sketch

**File → Open** → navigate to `src/mainCodeKite/mainCodeKite.ino`.

Arduino IDE loads all `.ino` files in the folder as tabs automatically. You should see tabs for `a_userParameters`, `b_systemParameters`, `c_parametersCheck`, `e_setupConfiguration`, `g_auxComputing`, `h_motorsUtilities`, `i_telemetryUtilities`, and `z_mainBody`.

### 5.3 Compile and upload

1. Click **Upload** (the right-arrow button) or press **Ctrl+U** (Cmd+U on macOS).
2. The IDE compiles then uploads. Watch the output panel at the bottom.
3. A successful upload ends with: `avrdude done. Thank you.`
4. Open **Tools → Serial Monitor**, set baud rate to **57600**. The board should print `STARTUP COMPLETE` within a second of resetting.

> **Compilation errors**: if the compiler rejects a value in `a_userParameters.ino`, the `static_assert` checks in `c_parametersCheck.ino` will display a descriptive error message. Fix the parameter and re-upload.

---

## 6. Install Serial Studio

Serial Studio is the ground station GUI used to display telemetry and send commands.
Download the latest release from: [github.com/Serial-Studio/Serial-Studio/releases](https://github.com/Serial-Studio/Serial-Studio/releases)

### Windows

1. Download the `.exe` installer.
2. Run it; default install location is fine.
3. Launch **Serial Studio** from the Start Menu.

### macOS

1. Download the `.dmg`.
2. Open it and drag **Serial Studio** to **Applications**.
3. First launch: right-click the app → **Open** to bypass Gatekeeper, then click **Open** in the dialog.

### Linux

1. Download the `.AppImage`.
2. Make it executable and run:
   ```bash
   chmod +x SerialStudio-*.AppImage
   ./SerialStudio-*.AppImage
   ```
3. If FUSE is missing: `sudo apt install libfuse2` then retry.

---

## 7. Configure and Connect Serial Studio

### 7.1 Load the project file

1. Launch Serial Studio.
2. **File → Open Project** (or drag-and-drop) → select:
   ```
   base.json
   ```
   This loads the dashboard layout and all pre-configured action buttons.

### 7.2 Set connection parameters

In the left-side connection panel, configure:

| Parameter | Value | Reason |
|-----------|-------|--------|
| Port | Same port as in Arduino IDE | Whichever COM/tty the Mega is on |
| Baud Rate | **57600** | Must match `TELEM_BAUDRATE` in `a_userParameters.ino` |
| Data bits | 8 | Arduino default |
| Parity | None | Arduino default |
| Stop bits | 1 | Arduino default |
| Flow control | None | |

### 7.3 Connect

Click **Connect**. Serial Studio begins parsing frames and populates the dashboard.

The dashboard contains two panels:

| Panel | Contents |
|-------|----------|
| **STATUS** | Position (PX/PY/PZ), orientation (Yaw/Pitch/Roll), error message, acknowledgement message |
| **MOTOR STATUS** | Motor thrust bar, arm/disarm status, mode, brake status |

> Most STATUS fields (position, orientation) are currently commented out in the firmware and will show `--.-` until sensors are wired and those code sections are enabled.

---

## 8. Verify the Connection

After clicking Connect you should see:

- **ACK Message** field: `STARTUP COMPLETE` (sent once at boot), then `NO ERRORS` cycling at 10 Hz.
- **MOTOR STATUS**: `DISARMED`.
- **MOTOR THRUST**: `0` (bar at zero).

If all fields show `--.-`:
1. Confirm baud rate is `57600` on both the Arduino and Serial Studio.
2. Confirm the correct port is selected (not a Bluetooth COM port or another device).
3. Re-open the project JSON file in Serial Studio — the frame parser may need to reload.
4. Try pressing the Mega's reset button; it re-sends `STARTUP COMPLETE`.

---

## 9. Command Reference

These are the action buttons pre-configured in the Serial Studio project file. Buttons send commands over the same serial port used for telemetry.

| Button label | Command sent | Effect on firmware |
|---|---|---|
| ARM MOTOR | `MARM` | Sets `motor_armed = true` |
| DISARM MOTOR | `DSRM` | Sets `motor_armed = false` |
| KILL MOTOR (WARNING) | `MOFF` | Sets `motor_on = false`, output goes to zero immediately |
| Motor Test | `MTEST` | Toggles test mode — motor must be armed first |
| INC THRUST | `IMTR,5` | Adds 5 % to `motor_test_percentage` (clamped to `MOTOR_MAX_PERCENTAGE`) |
| DCR THRUST | `IMTR,-5` | Subtracts 5 % (clamped to `MOTOR_MIN_PERCENTAGE`) |
| TILT BASE+ | `SBASE,1` | Starts one tilt-up burst (`BASE_TILT_BURST_TIME_MILLIS` ms) |
| TILT BASE- | `SBASE,-1` | Starts one tilt-down burst |

**Motor test procedure** (minimum safe sequence):

```
1. ARM MOTOR        → status changes to ARMED
2. Motor Test       → test mode starts, thrust at MOTOR_MIN_PERCENTAGE (8 %)
3. INC THRUST       → increases by 5 % per press
4. Motor Test       → toggles test mode off, motor stops
5. DISARM MOTOR     → returns to safe DISARMED state
```

> For a detailed explanation of the firmware internals, parameter tuning, and how to extend the code, see [docs/CODE_INTERNALS.md](docs/CODE_INTERNALS.md).
