#!/usr/bin/env python3

from evdev import InputDevice, list_devices
import subprocess
import time

print("Auto-toggle touch mode script started.")


def is_touchpad_present():
    """Check if a touchpad is present among input devices."""
    devices = (InputDevice(fn).name.lower() for fn in list_devices())
    # print(devices)
    return len(tuple(filter((lambda x: "touchpad" in x), devices))) > 0


# Initial state of touchpad presence
touchpad_present = is_touchpad_present()
print(touchpad_present)

while True:
    current_touchpad_present = is_touchpad_present()
    # print("Present?", current_touchpad_present)

    if current_touchpad_present != touchpad_present:
        touchpad_present = current_touchpad_present
        if touchpad_present:
            print("Touchpad detected. Deactivating touch mode...")
        else:
            print("Touchpad disconnected. Activating touch mode...")
        subprocess.call(["./touch-mode-toggle.py"])

    # Sleep for a longer period to reduce CPU usage
    time.sleep(1)
