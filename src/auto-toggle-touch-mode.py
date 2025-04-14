#!/usr/bin/env python3
"""Auto Toggle Touch mode.

Automatically Toggles touch mode when a touchpad is connected or disconnected.
"""

import logging
import subprocess
from pathlib import Path

from pyudev import Device, Context, Monitor, MonitorObserver

logging.basicConfig(level=logging.INFO)

# Get the directory of the current file
current_file_directory = Path(__file__).resolve().parent

# Path to the other script in the same directory
mode_toggler_path = current_file_directory / "toggle-touch-mode.py"


# TODO(MRDGH2821): reject further calls done in quick succession. Check `logs.log` for more info.
# https://github.com/MRDGH2821/kde-auto-touch-mode/issues/1
# Duplicate calls are happening due to same device being added 3 times with different properties.
def toggle_mode(device: Device) -> None:
    """Toggle touch mode based on the device action."""
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
context = Context()
monitor = Monitor.from_netlink(context)
monitor.filter_by(subsystem="input")
observer = MonitorObserver(monitor, callback=toggle_mode)
observer.start()

# Keep the script running
try:
    while True:
        pass
except KeyboardInterrupt:
    observer.stop()
