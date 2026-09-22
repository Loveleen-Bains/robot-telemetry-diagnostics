from src.diagnostics import (
    check_battery,
    check_temperature,
    check_wheel_imbalance,
    check_wheel_stall,
)
from src.robot import Robot
from src.telemetry import TelemetryReading


robot = Robot("ROBO-001")


def test_battery_normal():
    """Normal battery voltage should return NORMAL."""

    reading = TelemetryReading(
        timestamp=None,
        left_rpm=120.0,
        right_rpm=120.0,
        battery_voltage=12.3,
        temperature=37.0,
    )

    result = check_battery(reading, robot)

    assert result.status == "NORMAL"


def test_battery_low():
    """Low battery voltage should return WARNING."""

    reading = TelemetryReading(
        timestamp=None,
        left_rpm=120.0,
        right_rpm=120.0,
        battery_voltage=10.5,
        temperature=37.0,
    )

    result = check_battery(reading, robot)

    assert result.status == "WARNING"


def test_temperature_normal():
    """Normal temperature should return NORMAL."""

    reading = TelemetryReading(
        timestamp=None,
        left_rpm=120.0,
        right_rpm=120.0,
        battery_voltage=12.3,
        temperature=40.0,
    )

    result = check_temperature(reading, robot)

    assert result.status == "NORMAL"


def test_temperature_high():
    """High temperature should return WARNING."""

    reading = TelemetryReading(
        timestamp=None,
        left_rpm=120.0,
        right_rpm=120.0,
        battery_voltage=12.3,
        temperature=55.0,
    )

    result = check_temperature(reading, robot)

    assert result.status == "WARNING"


def test_wheel_imbalance_normal():
    """Small wheel RPM difference should return NORMAL."""

    reading = TelemetryReading(
        timestamp=None,
        left_rpm=120.0,
        right_rpm=110.0,
        battery_voltage=12.3,
        temperature=37.0,
    )

    result = check_wheel_imbalance(reading, robot)

    assert result.status == "NORMAL"


def test_wheel_imbalance_warning():
    """Large wheel RPM difference should return WARNING."""

    reading = TelemetryReading(
        timestamp=None,
        left_rpm=170.0,
        right_rpm=112.0,
        battery_voltage=12.3,
        temperature=37.0,
    )

    result = check_wheel_imbalance(reading, robot)

    assert result.status == "WARNING"


def test_wheel_stall_normal():
    """Active wheels should return NORMAL."""

    reading = TelemetryReading(
        timestamp=None,
        left_rpm=120.0,
        right_rpm=120.0,
        battery_voltage=12.3,
        temperature=37.0,
    )

    result = check_wheel_stall(reading)

    assert result.status == "NORMAL"


def test_wheel_stall_critical():
    """A stopped wheel should return CRITICAL."""

    reading = TelemetryReading(
        timestamp=None,
        left_rpm=172.0,
        right_rpm=0.0,
        battery_voltage=12.3,
        temperature=37.0,
    )

    result = check_wheel_stall(reading)

    assert result.status == "CRITICAL"