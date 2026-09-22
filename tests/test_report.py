from pathlib import Path

from src.health import HealthStatus
from src.report import generate_report, save_report
from src.robot import Robot


def test_generate_report():
    """Report should contain the expected health information."""

    robot = Robot("ROBO-001")

    health = HealthStatus(
        status="HEALTHY",
        message="All diagnostics are normal.",
    )

    report = generate_report(
        robot=robot,
        telemetry_file="data/normal_run.csv",
        readings_analyzed=10,
        health=health,
    )

    assert "ROBODIAG REPORT" in report
    assert "Robot: ROBO-001" in report
    assert "Log: data/normal_run.csv" in report
    assert "Readings analyzed: 10" in report
    assert "Overall Health: HEALTHY" in report
    assert "All diagnostics are normal." in report


def test_save_report(tmp_path: Path):
    """Report should be saved to a text file."""

    report = "Test RoboDiag Report"

    output_path = tmp_path / "test_report.txt"

    save_report(
        report,
        output_path,
    )

    assert output_path.exists()
    assert output_path.read_text(encoding="utf-8") == report

    