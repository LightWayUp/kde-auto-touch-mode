#!/usr/bin/env python3
"""Auto Toggle Touch mode.

Automatically Toggles touch mode when a touchpad is connected or disconnected.
"""

import logging
import subprocess
import time
from pathlib import Path

from evdev import InputDevice, list_devices

path = Path()
logging.basicConfig(level=logging.INFO)


def is_touchpad_present() -> None:
    """Check if a touchpad is present among input devices."""
    devices = (InputDevice(fn).name.lower() for fn in list_devices())
    return len(tuple(filter((lambda x: "touchpad" in x), devices))) > 0


# Get the directory of the current file
current_file_directory = path.join(path.parent, path.resolve(__file__))

# Initial state of touchpad presence
touchpad_present = is_touchpad_present()
logging.debug(touchpad_present)

mode_toggler_path = Path(current_file_directory).joinpath("touch-mode-toggle.py")
while True:
    current_touchpad_present = is_touchpad_present()

    if current_touchpad_present != touchpad_present:
        touchpad_present = current_touchpad_present
        if touchpad_present:
            logging.info("Touchpad detected. Deactivating touch mode...")
        else:
            logging.info("Touchpad disconnected. Activating touch mode...")
        subprocess.call([f"{mode_toggler_path}"])

    # Sleep for a longer period to reduce CPU usage
    time.sleep(1)
