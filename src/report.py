"""Report generation utilities for RoboDiag."""

from pathlib import Path

from src.health import HealthStatus
from src.robot import Robot


def generate_report(
    robot: Robot,
    telemetry_file: str,
    readings_analyzed: int,
    health: HealthStatus,
) -> str:
    """Generate a formatted RoboDiag health report."""

    return (
        "================================\n"
        "        ROBODIAG REPORT\n"
        "================================\n"
        f"Robot: {robot.robot_id}\n"
        f"Log: {telemetry_file}\n"
        f"Readings analyzed: {readings_analyzed}\n"
        "\n"
        f"Overall Health: {health.status}\n"
        f"Message: {health.message}\n"
        "================================\n"
    )


def save_report(
    report: str,
    output_path: str | Path,
) -> None:
    """Save a RoboDiag report to a text file."""

    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path.write_text(
        report,
        encoding="utf-8",
    )