"""Diagnostic checks for robot telemetry.
    
    
    diagnostics.py
    │
    ├── check_battery()
    ├── check_temperature()
    ├── check_wheel_imbalance()
    └── check_wheel_stall()
    └── run_diagnostics() 
    
    """

from dataclasses import dataclass

from src.robot import Robot
from src.telemetry import TelemetryReading


@dataclass
class DiagnosticResult:
    """Represents the result of a single diagnostic check."""

    name: str
    status: str
    message: str


def check_battery(
    reading: TelemetryReading,
    robot: Robot,
) -> DiagnosticResult:
        """Check the robot's current battery voltage."""

        if reading.battery_voltage < robot.min_battery_voltage:
            return DiagnosticResult(
                name="Battery Voltage",
                status="WARNING",
                message=(
                    f"Battery voltage is low: "
                    f"{reading.battery_voltage:.2f} V"
                ),
            )

        return DiagnosticResult(
            name="Battery Voltage",
            status="NORMAL",
            message=(
                f"Battery voltage is normal: "
                f"{reading.battery_voltage:.2f} V"
            ),
        )

def check_temperature(
    reading: TelemetryReading,
    robot: Robot,
) -> DiagnosticResult:
    """Check the robot's current temperature."""

    if reading.temperature > robot.max_temperature:
        return DiagnosticResult(
            name="Temperature",
            status="WARNING",
            message=(
                f"Temperature is high: "
                f"{reading.temperature:.1f} °C"
            ),
        )

    return DiagnosticResult(
        name="Temperature",
        status="NORMAL",
        message=(
            f"Temperature is normal: "
            f"{reading.temperature:.1f} °C"
        ),
    )

def check_wheel_imbalance(
    reading: TelemetryReading,
    robot: Robot,
) -> DiagnosticResult:
    """Check the difference between left and right wheel RPM."""

    imbalance = abs(reading.left_rpm - reading.right_rpm)

    if imbalance > robot.max_wheel_imbalance:
        return DiagnosticResult(
            name="Wheel Imbalance",
            status="WARNING",
            message=(
                f"Wheel RPM imbalance detected: "
                f"{imbalance:.1f} RPM"
            ),
        )

    return DiagnosticResult(
        name="Wheel Imbalance",
        status="NORMAL",
        message=(
            f"Wheel RPM difference is normal: "
            f"{imbalance:.1f} RPM"
        ),
    )


def check_wheel_stall(
    reading: TelemetryReading,
) -> DiagnosticResult:
    """Check whether either robot wheel has stalled."""

    if reading.left_rpm == 0 or reading.right_rpm == 0:
        return DiagnosticResult(
            name="Wheel Stall",
            status="CRITICAL",
            message=(
                f"Wheel stall detected: "
                f"left={reading.left_rpm:.1f}, "
                f"right={reading.right_rpm:.1f}"
            ),
        )

    return DiagnosticResult(
        name="Wheel Stall",
        status="NORMAL",
        message=(
            f"Wheel RPM is active: "
            f"left={reading.left_rpm:.1f}, "
            f"right={reading.right_rpm:.1f}"
        ),
    )

def run_diagnostics(
    reading: TelemetryReading,
    robot: Robot,
) -> list[DiagnosticResult]:
    """Run all diagnostic checks for one telemetry reading."""

    return [
        check_battery(reading, robot),
        check_temperature(reading, robot),
        check_wheel_imbalance(reading, robot),
        check_wheel_stall(reading),
    ]