from pathlib import Path
import subprocess
import sys


DATA_DIR = Path("data")


def run_robodiag(telemetry_file):
    """Run RoboDiag through its command-line interface."""

    return subprocess.run(
        [
            sys.executable,
            "-m",
            "src.main",
            str(telemetry_file),
        ],
        capture_output=True,
        text=True,
        check=True,
    )


def test_main_normal_run():
    """CLI should report HEALTHY for normal telemetry."""

    result = run_robodiag(
        DATA_DIR / "normal_run.csv"
    )

    assert "Overall Health: HEALTHY" in result.stdout
    assert "Readings analyzed: 10" in result.stdout


def test_main_warning_run():
    """CLI should report WARNING for warning telemetry."""

    result = run_robodiag(
        DATA_DIR / "warning_run.csv"
    )

    assert "Overall Health: WARNING" in result.stdout
    assert "10/10 readings were warnings" in result.stdout


def test_main_critical_run():
    """CLI should report CRITICAL for critical telemetry."""

    result = run_robodiag(
        DATA_DIR / "critical_run.csv"
    )

    assert "Overall Health: CRITICAL" in result.stdout
    assert "10/10 readings contained a critical condition" in result.stdout