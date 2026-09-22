from pathlib import Path

import pytest

from src.telemetry import TelemetryLog


DATA_DIR = Path("data")


def test_load_csv():
    """Telemetry CSV should load successfully."""

    log = TelemetryLog.load_csv(
        DATA_DIR / "normal_run.csv"
    )

    assert len(log.all_readings()) == 30


def test_latest_reading():
    """Latest should return the final telemetry reading."""

    log = TelemetryLog.load_csv(
        DATA_DIR / "normal_run.csv"
    )

    latest = log.latest()

    assert latest.left_rpm == 121.0
    assert latest.right_rpm == 121.0
    assert latest.battery_voltage == 12.31
    assert latest.temperature == 37.5


def test_recent_readings():
    """Recent should return the requested number of readings."""

    log = TelemetryLog.load_csv(
        DATA_DIR / "normal_run.csv"
    )

    recent = log.recent(10)

    assert len(recent) == 10


def test_recent_invalid_count():
    """Recent should reject non-positive counts."""

    log = TelemetryLog.load_csv(
        DATA_DIR / "normal_run.csv"
    )

    with pytest.raises(ValueError):
        log.recent(0)