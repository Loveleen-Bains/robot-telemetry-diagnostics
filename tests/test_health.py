from pathlib import Path

from src.diagnostics import DiagnosticResult, run_diagnostics
from src.health import (
    analyze_recent_readings,
    classify_health,
    classify_persistent_health,
    evaluate_reading_health,
)
from src.robot import Robot
from src.telemetry import TelemetryLog


DATA_DIR = Path("data")

robot = Robot("ROBO-001")


def test_classify_health_healthy():
    """All normal diagnostics should produce HEALTHY."""

    diagnostics = [
        DiagnosticResult("Battery", "NORMAL", "Battery is normal."),
        DiagnosticResult("Temperature", "NORMAL", "Temperature is normal."),
    ]

    result = classify_health(diagnostics)

    assert result.status == "HEALTHY"


def test_classify_health_warning():
    """A warning diagnostic should produce WARNING."""

    diagnostics = [
        DiagnosticResult("Battery", "WARNING", "Battery is low."),
        DiagnosticResult("Temperature", "NORMAL", "Temperature is normal."),
    ]

    result = classify_health(diagnostics)

    assert result.status == "WARNING"


def test_classify_health_critical():
    """A critical diagnostic should produce CRITICAL."""

    diagnostics = [
        DiagnosticResult("Battery", "WARNING", "Battery is low."),
        DiagnosticResult("Wheel Stall", "CRITICAL", "Wheel stalled."),
    ]

    result = classify_health(diagnostics)

    assert result.status == "CRITICAL"


def test_persistent_warning_at_threshold():
    """Seven warnings should trigger persistent WARNING."""

    diagnostics = [
        DiagnosticResult("Test", "WARNING", "Warning.")
        for _ in range(7)
    ]

    result = classify_persistent_health(
        diagnostics,
        warning_threshold=7,
    )

    assert result.status == "WARNING"


def test_persistent_warning_below_threshold():
    """Six warnings should not trigger persistent WARNING."""

    diagnostics = [
        DiagnosticResult("Test", "WARNING", "Warning.")
        for _ in range(6)
    ]

    diagnostics.extend(
        [
            DiagnosticResult("Test", "NORMAL", "Normal.")
            for _ in range(4)
        ]
    )

    result = classify_persistent_health(
        diagnostics,
        warning_threshold=7,
    )

    assert result.status == "HEALTHY"


def test_persistent_critical_overrides_warning():
    """A critical condition should override warnings."""

    diagnostics = [
        DiagnosticResult("Test", "WARNING", "Warning.")
        for _ in range(9)
    ]

    diagnostics.append(
        DiagnosticResult(
            "Wheel Stall",
            "CRITICAL",
            "Wheel stalled.",
        )
    )

    result = classify_persistent_health(
        diagnostics,
        warning_threshold=7,
    )

    assert result.status == "CRITICAL"


def test_evaluate_reading_health():
    """Per-reading health should prioritize CRITICAL over WARNING."""

    diagnostics = [
        DiagnosticResult("Battery", "WARNING", "Battery is low."),
        DiagnosticResult("Temperature", "NORMAL", "Temperature is normal."),
        DiagnosticResult("Wheel Stall", "CRITICAL", "Wheel stalled."),
    ]

    result = evaluate_reading_health(diagnostics)

    assert result == "CRITICAL"


def test_normal_log_is_healthy():
    """Normal telemetry should produce HEALTHY."""

    log = TelemetryLog.load_csv(
        DATA_DIR / "normal_run.csv"
    )

    result = analyze_recent_readings(
        log.recent(10),
        robot,
    )

    assert result.status == "HEALTHY"


def test_warning_log_is_warning():
    """Persistent warning telemetry should produce WARNING."""

    log = TelemetryLog.load_csv(
        DATA_DIR / "warning_run.csv"
    )

    result = analyze_recent_readings(
        log.recent(10),
        robot,
    )

    assert result.status == "WARNING"


def test_critical_log_is_critical():
    """Critical telemetry should produce CRITICAL."""

    log = TelemetryLog.load_csv(
        DATA_DIR / "critical_run.csv"
    )

    result = analyze_recent_readings(
        log.recent(10),
        robot,
    )

    assert result.status == "CRITICAL"
    