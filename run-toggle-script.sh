#!/bin/sh

script=
if basename "$0" | grep -E -q -i '(^|\-|_)auto(\-|_|$)'; then
    script="auto_"
fi

echo "src/${script}toggle_touch_mode.py"
