"""Command-line interface for RoboDiag."""

import argparse

from src.health import analyze_recent_readings
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

    print("================================")
    print("        ROBODIAG REPORT")
    print("================================")
    print(f"Robot: {robot.robot_id}")
    print(f"Log: {args.telemetry_file}")
    print(f"Readings analyzed: {len(recent_readings)}")
    print()
    print(f"Overall Health: {health.status}")
    print(f"Message: {health.message}")
    print("================================")


if __name__ == "__main__":
    main()
    