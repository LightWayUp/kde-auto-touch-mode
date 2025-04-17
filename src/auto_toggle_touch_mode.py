#!/usr/bin/env python3
"""Auto Toggle Touch mode.

Automatically Toggles touch mode when a touchpad is connected or disconnected.
"""

import toggle_touch_mode

import logging
from pathlib import Path

from pyudev import Device, Context, Monitor

logging.basicConfig(level=logging.INFO)

# Get the directory of the current file
current_file_directory = Path(__file__).resolve().parent

# TODO(MRDGH2821): reject further calls done in quick succession. Check `logs.log` for more info.
# https://github.com/MRDGH2821/kde-auto-touch-mode/issues/1
# Duplicate calls are happening due to same device being added 3 times with different properties.
def toggle_mode(device: Device) -> None:
    """Toggle touch mode based on the device action."""
    if device.properties.get("ID_INPUT_TOUCHPAD") != "1":
        return

    if device.action == "add":
        logging.info("Touchpad detected. Deactivating touch mode...")
    else:
        logging.info("Touchpad disconnected. Activating touch mode...")
    toggle_touch_mode.toggle()


logging.debug(
    "Auto toggler started",
    extra={
        "cwd": current_file_directory,
    },
)

# Set up udev monitor
context = Context()
monitor = Monitor.from_netlink(context)
monitor.filter_by("input")
try:
    for device in iter(monitor.poll, None):
        toggle_mode(device)
except KeyboardInterrupt:
    pass
