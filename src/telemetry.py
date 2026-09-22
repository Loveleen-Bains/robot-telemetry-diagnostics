"""Telemetry data models and CSV loading utilities.

    structure:
        telemetry.py
        │
        ├── Read CSV
        ├── Convert rows → TelemetryReading
        ├── Validate data
        ├── Give us full telemetry log
        
        
    Functions:
        telemetry.py
        │
        ├── TelemetryReading
        │
        ├── TelemetryLog
        │   ├── load_csv()
        │   ├── latest()
        │   ├── recent()
        │   ├── all_readings()
        │   └── validate()
        │
        └── CSV/data handling"""

from dataclasses import dataclass
from datetime import datetime
import csv
from pathlib import Path


@dataclass
class TelemetryReading:
    """Represents one telemetry reading from the robot."""

    timestamp: datetime
    left_rpm: float
    right_rpm: float
    battery_voltage: float
    temperature: float

class TelemetryLog:
    """Stores and provides access to robot telemetry readings."""

    def __init__(self, readings: list[TelemetryReading]):
        self.readings = readings

    def latest(self) -> TelemetryReading:
        """Return the most recent telemetry reading."""
        return self.readings[-1]

    def recent(self, count: int = 10) -> list[TelemetryReading]:
        """Return the most recent telemetry readings."""

        if count <= 0:
            raise ValueError("Count must be greater than 0.")

        return self.readings[-count:]

    def all_readings(self) -> list[TelemetryReading]:
        """Return all telemetry readings."""
        return self.readings


    #validation method: 
    def validate(self) -> None:
        """Validate all telemetry readings."""

        if not self.readings:
            raise ValueError("Telemetry log is empty.")

        for reading in self.readings:
            if reading.left_rpm < 0:
                raise ValueError("Left RPM cannot be negative.")

            if reading.right_rpm < 0:
                raise ValueError("Right RPM cannot be negative.")

            if reading.battery_voltage <= 0:
                raise ValueError("Battery voltage must be greater than 0.")

            if reading.temperature < -50:
                raise ValueError("Temperature is below the valid range.")


    #Load CSV method:
    @classmethod
    def load_csv(cls, file_path: str | Path) -> "TelemetryLog":
        """Load telemetry readings from a CSV file."""

        readings = []

        with open(file_path, "r", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                reading = TelemetryReading(
                    timestamp=datetime.fromisoformat(row["timestamp"]),
                    left_rpm=float(row["left_rpm"]),
                    right_rpm=float(row["right_rpm"]),
                    battery_voltage=float(row["battery_voltage"]),
                    temperature=float(row["temperature"]),
                )

                readings.append(reading)

        log = cls(readings)
        log.validate()

        return log