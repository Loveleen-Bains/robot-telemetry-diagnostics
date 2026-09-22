"""Robot health classification.

This module provides functions to classify the overall health of the robot based on diagnostic results.


health.py
│
├── HealthStatus
│
├── classify_health()
│     └── basic current diagnostic classification
│
└── classify_persistent_health()
      ├── critical priority
      ├── warning persistence
      └── healthy fallback

"""

from dataclasses import dataclass

from src.diagnostics import DiagnosticResult, run_diagnostics
from src.robot import Robot
from src.telemetry import TelemetryReading


@dataclass
class HealthStatus:
    """Represents the overall health of the robot."""

    status: str
    message: str


def classify_health(
    diagnostics: list[DiagnosticResult],
) -> HealthStatus:
    """Classify overall robot health from diagnostic results."""

    critical_count = sum(
        result.status == "CRITICAL"
        for result in diagnostics
    )

    warning_count = sum(
        result.status == "WARNING"
        for result in diagnostics
    )

    if critical_count > 0:
        return HealthStatus(
            status="CRITICAL",
            message=f"{critical_count} critical diagnostic(s) detected.",
        )

    if warning_count > 0:
        return HealthStatus(
            status="WARNING",
            message=f"{warning_count} warning diagnostic(s) detected.",
        )

    return HealthStatus(
        status="HEALTHY",
        message="All diagnostics are normal.",
    )

def classify_persistent_health(
    diagnostics: list[DiagnosticResult],
    warning_threshold: int = 7,
) -> HealthStatus:
    """Classify health based on persistent diagnostic results."""

    critical_count = sum(
        result.status == "CRITICAL"
        for result in diagnostics
    )

    warning_count = sum(
        result.status == "WARNING"
        for result in diagnostics
    )

    if critical_count > 0:
        return HealthStatus(
            status="CRITICAL",
            message=f"{critical_count} critical diagnostic(s) detected.",
        )

    if warning_count >= warning_threshold:
        return HealthStatus(
            status="WARNING",
            message=(
                f"Persistent warning detected: "
                f"{warning_count}/{len(diagnostics)} readings were warnings."
            ),
        )

    return HealthStatus(
        status="HEALTHY",
        message=(
            f"No persistent warning detected: "
            f"{warning_count}/{len(diagnostics)} readings were warnings."
        ),
    )



def evaluate_reading_health(
    diagnostics: list[DiagnosticResult],
) -> str:
    """Determine the overall status for one telemetry reading."""

    if any(result.status == "CRITICAL" for result in diagnostics):
        return "CRITICAL"

    if any(result.status == "WARNING" for result in diagnostics):
        return "WARNING"

    return "HEALTHY"


def analyze_recent_readings(
    readings: list[TelemetryReading],
    robot: Robot,
) -> HealthStatus:
    """Analyze recent telemetry readings for persistent problems."""

    reading_statuses = []

    for reading in readings:
        diagnostics = run_diagnostics(reading, robot)
        status = evaluate_reading_health(diagnostics)
        reading_statuses.append(status)

    critical_count = reading_statuses.count("CRITICAL")
    warning_count = reading_statuses.count("WARNING")

    if critical_count > 0:
        return HealthStatus(
            status="CRITICAL",
            message=(
                f"{critical_count}/{len(readings)} readings "
                f"contained a critical condition."
            ),
        )

    if warning_count >= 7:
        return HealthStatus(
            status="WARNING",
            message=(
                f"Persistent warning detected: "
                f"{warning_count}/{len(readings)} readings were warnings."
            ),
        )

    return HealthStatus(
        status="HEALTHY",
        message=(
            f"No persistent warning detected: "
            f"{warning_count}/{len(readings)} readings were warnings."
        ),
    )