#!/usr/bin/env python3
"""Touch mode Toggle.

Toggles touch mode on KDE Plasma.
"""

import os
import subprocess
from enum import Enum, auto
from typing import TypeAlias, overload
try:
    from typing import override
except ImportError:
    from typing import TypeVar, Any
    from collections.abc import Callable
    from contextlib import suppress
    F = TypeVar("F", bound=Callable[..., Any])
    def override(method: F) -> F:
        with suppress(AttributeError, TypeError):
            method.__override__ = True
        return method

import gi
from gi.repository import Gio, GLib

gi.require_version("Gio", "2.0")

KDE_VERSION = os.environ.get("KDE_SESSION_VERSION", 6)

OBJECT_PATH = "/kwinrc"
INTERFACE_NAME = "org.kde.kconfig.notify"
SIGNAL_NAME = "ConfigChanged"

# When minimum required version of Python is 3.12 or above,
# use the `type` statement to declare type alias instead:
#
#     type TabletModeAlias = TabletMode
#
# When minimum required version of Python is 3.14 or above,
# annotation evaluation is deferred, so forward references
# should "just work", and this can be removed.
TabletModeAlias: TypeAlias = "TabletMode"

# When minimum required version of Python is 3.11 or above,
# the class should inherit from `StrEnum` instead
class TabletMode(Enum):
    AUTO = auto()
    ON = auto()
    OFF = auto()

    @staticmethod
    def _generate_next_value_(name: str, *_, **__) -> str:
        return name.lower()

    @override
    def __str__(self) -> str:
        return self.value

    @staticmethod
    @overload
    def config() -> TabletModeAlias:
        ...

    @staticmethod
    @overload
    def config(mode: TabletModeAlias) -> TabletModeAlias:
        ...

    @staticmethod
    def config(mode: TabletModeAlias | None=None) -> TabletModeAlias:
        is_reading = mode is None
        arguments = [
            "--file",
            "kwinrc",
            "--group",
            "Input",
            "--key",
            "TabletMode"
        ]
        action = "write"
        if is_reading:
            arguments.append("--default")
            action = "read"
            mode = TabletMode.AUTO

        arguments.insert(0, f"k{action}config{KDE_VERSION}")
        arguments.append(mode.value)
        run = lambda **kwargs: subprocess.run(arguments, check=True, **kwargs).stdout
        if is_reading:
            return TabletMode(run(capture_output=True, encoding="utf-8").strip())
        else:
            run()
            return mode

def toggle(from_auto_to: TabletMode=TabletMode.ON) -> TabletMode:
    new_mode = TabletMode.config({
        TabletMode.AUTO: from_auto_to,
        TabletMode.ON: TabletMode.OFF,
        TabletMode.OFF: TabletMode.ON
    }.get(TabletMode.config()))

    connection = Gio.bus_get_sync(Gio.BusType.SESSION, None)
    variant = GLib.Variant.new_tuple(GLib.Variant("a{saay}", {"Input": [b"TabletMode"]}))
    Gio.DBusConnection.emit_signal(
        connection,
        None,
        OBJECT_PATH,
        INTERFACE_NAME,
        SIGNAL_NAME,
        variant,
    )
    return new_mode

if __name__ == "__main__":
    toggle()
