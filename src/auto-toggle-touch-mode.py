#!/usr/bin/env python3
"""Auto Toggle Touch mode.

Automatically Toggles touch mode when a touchpad is connected or disconnected.
"""

import logging
import subprocess
import time
from pathlib import Path

from evdev import InputDevice, list_devices

logging.basicConfig(level=logging.INFO)


def is_touchpad_present() -> bool:
    """Check if a touchpad is present among input devices."""
    devices = (InputDevice(fn).name.lower() for fn in list_devices())
    return any("touchpad" in device for device in devices)


# Get the directory of the current file
current_file_directory = Path(__file__).resolve().parent

# Initial state of touchpad presence
touchpad_present = is_touchpad_present()
logging.debug(
    "Auto toggler started",
    extra={
        "cwd": current_file_directory,
        "Initial touchpad presence": touchpad_present,
    },
)

mode_toggler_path = current_file_directory / "touch-mode-toggle.py"
while True:
    current_touchpad_present = is_touchpad_present()

    if current_touchpad_present != touchpad_present:
        touchpad_present = current_touchpad_present
        if touchpad_present:
            logging.info("Touchpad detected. Deactivating touch mode...")
        else:
            logging.info("Touchpad disconnected. Activating touch mode...")
        subprocess.call([mode_toggler_path])

    # Sleep for a longer period to reduce CPU usage
    time.sleep(1)
