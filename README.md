# 🤖 RoboDiag — Robot Telemetry & Diagnostic CLI

A Python-based engineering tool for analyzing mobile-robot telemetry, detecting abnormal operating conditions, classifying robot health, and generating diagnostic reports.

## 📌 Project Overview

RoboDiag is a Week 1 robotics engineering project focused on building practical foundations in Python, OOP, Linux, Git/GitHub, telemetry processing, validation, diagnostics, testing, CLI tools, and report generation.

The project simulates a real robotics workflow where a robot produces telemetry data and an engineering system analyzes that data to determine whether the robot is operating normally or showing signs of a fault.

## 🎯 Why RoboDiag?

Real robots continuously generate telemetry such as wheel speeds, battery voltage, temperature, IMU measurements, motor current, and sensor readings.

RoboDiag provides a small but realistic foundation for that workflow:

```text
Robot Telemetry → Data Ingestion → Validation → Diagnostics → Health Classification → Report
```

## ✨ Key Features

- 📡 CSV-based robot telemetry ingestion
- ✅ Telemetry validation
- 🔋 Battery voltage diagnostics
- 🌡️ Temperature diagnostics
- ⚙️ Wheel RPM imbalance detection
- 🛑 Wheel stall detection
- 🧠 Persistent-warning analysis
- 🚨 Critical-condition prioritization
- 💻 Command-line interface
- 📄 Automatic diagnostic report generation
- 🧪 Automated testing with pytest
- 🐧 Linux / WSL development
- 🌿 Modular Python architecture
- 🔧 Git-based engineering workflow

## 🏗️ System Architecture

```text
                  ┌─────────────────────┐
                  │   Robot Telemetry   │
                  │       CSV Log       │
                  └──────────┬──────────┘
                             ↓
                  ┌─────────────────────┐
                  │  Telemetry Ingestion│
                  │    & Validation     │
                  └──────────┬──────────┘
                             ↓
                  ┌─────────────────────┐
                  │   Recent Readings   │
                  │     Time Window     │
                  └──────────┬──────────┘
                             ↓
                  ┌─────────────────────┐
                  │  Diagnostic Engine  │
                  ├─────────────────────┤
                  │ Battery             │
                  │ Temperature         │
                  │ Wheel Imbalance     │
                  │ Wheel Stall         │
                  └──────────┬──────────┘
                             ↓
                  ┌─────────────────────┐
                  │ Health Classification│
                  ├─────────────────────┤
                  │ HEALTHY             │
                  │ WARNING             │
                  │ CRITICAL            │
                  └──────────┬──────────┘
                             ↓
                  ┌─────────────────────┐
                  │  Diagnostic Report  │
                  └─────────────────────┘
```

## 📊 Telemetry Model

Each telemetry reading contains:

| Field | Description |
|---|---|
| `timestamp` | Time at which the reading was recorded |
| `left_rpm` | Left wheel rotational speed |
| `right_rpm` | Right wheel rotational speed |
| `battery_voltage` | Robot battery voltage |
| `temperature` | Robot temperature |

### Example

```csv
timestamp,left_rpm,right_rpm,battery_voltage,temperature
2026-09-21T10:00:00,120,120,12.60,36.0
2026-09-21T10:00:01,121,121,12.58,36.2
```

The CSV files are simulated recorded robot telemetry logs, not machine-learning datasets.

## 🔍 Diagnostic Engine

RoboDiag currently performs four diagnostic checks.

### 1. Battery Voltage:

Current project configuration:

```text
Minimum battery voltage = 11.0 V
```

If `battery_voltage < 11.0 V`, the result becomes `WARNING`.

### 2. Temperature:

Current project configuration:

```text
Maximum temperature = 50.0 °C
```

If `temperature > 50.0 °C`, the result becomes `WARNING`.

### 3. Wheel Imbalance:

```text
imbalance = |left_rpm - right_rpm|
```

Current project configuration:

```text
Maximum wheel imbalance = 20 RPM
```

If the difference exceeds the threshold, the result becomes `WARNING`.

### 4. Wheel Stall:

If either wheel reaches zero RPM:

```text
left_rpm == 0 OR right_rpm == 0
```

the diagnostic result becomes `CRITICAL`.

The thresholds above are project configuration choices, not universal robotics safety standards.

## 🧠 Health Classification

RoboDiag uses three overall health states:

```text
HEALTHY
WARNING
CRITICAL
```

A critical condition overrides warning conditions.

For recent telemetry, RoboDiag also checks for persistent warnings. The current project rule is:

```text
7 or more warning readings
out of the recent analysis window
→ WARNING
```

This is a project-specific persistence rule designed to demonstrate temporal reasoning.

## ⏱️ Temporal Reasoning

| Perspective | Question |
|---|---|
| Latest reading | What is happening now? |
| Recent window | Is the problem persistent? |
| Full log | What is the overall trend? |
| Rate/trend | Is the condition worsening? |
| Event detection | Did something dangerous happen? |
| Validation | Is the data itself suspicious? |

This provides a foundation for future robotics systems involving sensor monitoring, fault detection, predictive maintenance, autonomous navigation, and robot health monitoring.

## 🧪 Sample Telemetry Scenarios

```text
data/
├── normal_run.csv
├── warning_run.csv
└── critical_run.csv
```

### Normal Run

Stable wheel speeds, normal temperature, gradual battery decline, and no persistent warnings.

**Expected health:**

`HEALTHY`

### Warning Run

Persistent wheel-speed imbalance and increasing temperature.

**Expected health:**

`WARNING`

### Critical Run

Wheel stall, very low battery voltage, and high temperature.

**Expected health:**

`CRITICAL`

## 📁 Project Structure

```text
robot-telemetry-diagnostics/
│
├── data/
│   ├── normal_run.csv
│   ├── warning_run.csv
│   └── critical_run.csv
│
├── reports/
│   ├── normal_run_report.txt
│   ├── warning_run_report.txt
│   └── critical_run_report.txt
│
├── src/
│   ├── __init__.py
│   ├── robot.py
│   ├── telemetry.py
│   ├── diagnostics.py
│   ├── health.py
│   ├── report.py
│   └── main.py
│
├── tests/
│   ├── test_telemetry.py
│   ├── test_diagnostics.py
│   ├── test_health.py
│   ├── test_main.py
│   └── test_report.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

## 🧩 Module Responsibilities

| Module | Responsibility |
|---|---|
| `robot.py` | Robot identity and diagnostic configuration |
| `telemetry.py` | Data models, CSV loading, access, validation |
| `diagnostics.py` | Battery, temperature, wheel imbalance, and stall checks |
| `health.py` | Health classification and persistence analysis |
| `report.py` | Report generation and saving |
| `main.py` | Command-line interface and pipeline integration |

## 🧪 Automated Testing

Current test suite:

```text
27 tests
27 passed
```

| Test Module | Tests |
|---|---:|
| `test_telemetry.py` | 4 |
| `test_diagnostics.py` | 8 |
| `test_health.py` | 10 |
| `test_main.py` | 3 |
| `test_report.py` | 2 |
| **Total** | **27** |

The tests cover CSV loading, telemetry validation, diagnostics, health classification, critical-condition priority, persistent warnings, real sample scenarios, CLI integration, report generation, and report saving.

## ▶️ Installation

```bash
git clone https://github.com/Loveleen-Bains/robot-telemetry-diagnostics.git
cd robot-telemetry-diagnostics
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 🚀 Running RoboDiag

```bash
python -m src.main data/normal_run.csv
python -m src.main data/warning_run.csv
python -m src.main data/critical_run.csv
```

The program prints the result and automatically saves a report inside `reports/`.

### Example:

```text
================================
        ROBODIAG REPORT
================================
Robot: ROBO-001
Log: data/normal_run.csv
Readings analyzed: 10

Overall Health: HEALTHY
Message: No persistent warning detected: 0/10 readings were warnings.
================================
```

## 📄 Diagnostic Reports

The repository includes three curated sample reports:

```text
reports/
├── normal_run_report.txt
├── warning_run_report.txt
└── critical_run_report.txt
```

Generated report files are generally ignored by Git, while these three sample reports are explicitly kept under version control as project examples.

## 🧪 Running Tests

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest -v
```

Or:

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest -q
```

Expected result:

```text
27 passed
```

The `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` workaround prevents unrelated ROS 2 Pytest plugins in the development environment from interfering with this project's test suite.

## 🔐 Telemetry Validation

RoboDiag validates incoming telemetry before analysis.

Examples of invalid data include:

- Negative wheel RPM
- Non-positive battery voltage
- Temperature below the accepted validation range
- Empty telemetry logs

The goal is to prevent obviously invalid data from silently entering the diagnostic pipeline.

## ⚙️ Configuration

Current robot configuration:

```python
Robot(
    robot_id="ROBO-001",
    min_battery_voltage=11.0,
    max_temperature=50.0,
    max_wheel_imbalance=20.0
)
```

These values are configurable and could later be moved into YAML, JSON, ROS 2 parameters, or environment variables.

## 🧠 Engineering Decisions

### CSV as an external data source

The telemetry CSV acts as a stand-in for a real robot data stream. Later this can be replaced by live ROS 2 topics and sensor data.

### Dataclasses for structured data

Dataclasses are used for:

```text
Robot
TelemetryReading
DiagnosticResult
HealthStatus
```

### Separate modules

Responsibilities are separated into modules to make the system easier to test, debug, extend, reuse, and integrate.

### Critical conditions override warnings

A critical condition represents a more serious state than a warning, so it takes priority.

### Recent-window analysis

The system examines recent telemetry rather than only the latest reading, introducing temporal reasoning.

## 🚧 Current Limitations

RoboDiag is intentionally a small Week 1 project.

It currently does not include:

- Live robot hardware
- ROS 2
- Gazebo
- RViz
- Real sensors
- Real motor controllers
- Computer vision
- Machine learning
- Database storage
- Network telemetry
- Predictive-maintenance models

These are intentionally left for later stages of the robotics roadmap.

## 🔮 Future Development

Possible extensions include:

- ROS 2 telemetry topics
- ROS 2 nodes and parameters
- Real robot sensor data
- Live telemetry dashboards
- Real-time alerts
- Historical analysis
- Trend and rate-of-change detection
- More fault types
- Sensor consistency checks
- Statistical anomaly detection
- Predictive maintenance
- Machine-learning-based fault classification
- Matplotlib telemetry visualization

## 🤖 Project Context

RoboDiag is Project 1 — Week 1 of a larger robotics learning roadmap.

The long-term project direction is:

**Mobile Robot With Vision Tracking**

The roadmap progresses through:

```text
Programming
     ↓
Robotics Fundamentals
     ↓
ROS 2
     ↓
Sensors
     ↓
Computer Vision
     ↓
Localization
     ↓
Mapping
     ↓
Navigation
     ↓
Target Tracking
     ↓
Full Robot Integration
```

RoboDiag establishes the first engineering layer before moving into robotics middleware, simulation, perception, and autonomous navigation.

## 📌 Project Status

```text
Project:         RoboDiag
Phase:           Week 1
Status:          Completed
Language:        Python
Platform:        Linux / Ubuntu WSL
Testing:         27/27 passing
Version Control: Git + GitHub
```

## 👩‍💻 Author

**Loveleen Bains**

BTech Computer Science & Engineering — AI & ML

Robotics-focused engineering journey.

## 📄 License

This project is currently intended as an educational and portfolio project.
