"""Command-line interface for RoboDiag."""

import argparse
from pathlib import Path

from src.health import analyze_recent_readings
from src.report import generate_report, save_report
from src.robot import Robot
from src.telemetry import TelemetryLog


def main() -> None:
    """Run the RoboDiag command-line application."""

    parser = argparse.ArgumentParser(
        description="Analyze mobile robot telemetry and generate a health report."
    )

    parser.add_argument(
        "telemetry_file",
        help="Path to the robot telemetry CSV file.",
    )

    args = parser.parse_args()

    robot = Robot("ROBO-001")

    log = TelemetryLog.load_csv(args.telemetry_file)

    recent_readings = log.recent(10)

    health = analyze_recent_readings(
        recent_readings,
        robot,
    )

    report = generate_report(
        robot=robot,
        telemetry_file=args.telemetry_file,
        readings_analyzed=len(recent_readings),
        health=health,
    )

    print(report)

    telemetry_path = Path(args.telemetry_file)
    report_name = f"{telemetry_path.stem}_report.txt"
    report_path = Path("reports") / report_name

    save_report(
        report,
        report_path,
    )

    print(f"Report saved to: {report_path}")


if __name__ == "__main__":
    main()