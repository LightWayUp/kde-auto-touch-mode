#!/usr/bin/env bash

# Touch mode Toggle for KDE Plasma

# Get KDE session version
KDE_VERSION=${KDE_SESSION_VERSION:-6}

# Read current mode
current_mode=$(kreadconfig${KDE_VERSION} --file kwinrc --group Input --key TabletMode --default auto)

# Toggle mode
if [ "$current_mode" == "on" ]; then
	kwriteconfig${KDE_VERSION} --file kwinrc --group Input --key TabletMode off
else
	kwriteconfig${KDE_VERSION} --file kwinrc --group Input --key TabletMode on
fi

# Emit signal

dbus-send --session --dest=org.kde.kconfig --print-reply --type=signal /kwinrc org.kde.kconfig.notify.ConfigChanged dict:string:string:Input,array:string:TabletMode
