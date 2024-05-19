# overmind

# Drone Hive - Overmind

The Overmind component is a crucial part of the Drone Hive control system. It serves as the central intelligence that coordinates and manages the entire drone fleet.

## Features

- **Fleet Management**: The Overmind allows you to easily manage and monitor a large fleet of drones. It provides functionalities for adding new drones, removing drones, and tracking their status.

- **Mission Planning**: With the Overmind, you can plan and schedule missions for individual drones or groups of drones. It provides an intuitive interface to define waypoints, set flight paths, and specify mission objectives.

- **Real-time Monitoring**: The Overmind continuously collects telemetry data from each drone in the fleet, providing real-time updates on their location, altitude, battery status, and more. This allows you to have a comprehensive view of the entire drone operation.

- **Fault Detection and Recovery**: In case of any issues or anomalies, the Overmind is equipped with advanced algorithms to detect faults and trigger appropriate recovery actions. It can automatically reroute drones, initiate emergency landings, or notify operators about critical situations.

## Getting Started

To get started with the Drone Hive Overmind, follow these steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/KlubSympatykowLotnictwaIKolei/overmind
    ```

2. Install the required dependencies:

    ```bash
    poetry install
    ```
4. Start the Overmind:

    ```bash
    poetry run python3 main.py
    ```

    This will launch the Overmind and make it ready to manage your drone fleet.
