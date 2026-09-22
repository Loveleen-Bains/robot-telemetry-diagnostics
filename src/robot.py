"""Robot configuration and identity.

    Robot
    │
    ├── Configuration
    │      ├── battery limit
    │      ├── temperature limit
    │      └── wheel imbalance limit
"""



from dataclasses import dataclass


@dataclass
class Robot:
    """Represents a robot and its diagnostic configuration."""

    robot_id: str
    min_battery_voltage: float = 11.0
    max_temperature: float = 50.0
    max_wheel_imbalance: float = 20.0