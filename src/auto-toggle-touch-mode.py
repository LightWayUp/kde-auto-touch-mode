#!/usr/bin/env python3
"""Auto Toggle Touch mode.

Automatically Toggles touch mode when a touchpad is connected or disconnected.
"""

import logging
import subprocess
from pathlib import Path

import pyudev
import pyudev.device

logging.basicConfig(level=logging.INFO)

# Get the directory of the current file
current_file_directory = Path(__file__).resolve().parent

# Path to the other script in the same directory
mode_toggler_path = current_file_directory / "touch-mode-toggle.py"


def toggle_mode(device: pyudev.device._device.Device) -> None:
    """Handle udev events for input devices."""
    if device.properties.get("ID_INPUT_TOUCHPAD") != "1":
        return

    if device.properties.get("ACTION") == "add":
        logging.info("Touchpad detected. Deactivating touch mode...")
    else:
        logging.info("Touchpad disconnected. Activating touch mode...")
    subprocess.call([mode_toggler_path])


logging.debug(
    "Auto toggler started",
    extra={
        "cwd": current_file_directory,
    },
)

# Set up udev monitor
context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by(subsystem="input")
observer = pyudev.MonitorObserver(monitor, callback=toggle_mode)
observer.start()

# Keep the script running
try:
    while True:
        pass
except KeyboardInterrupt:
    observer.stop()
