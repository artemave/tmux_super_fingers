#!/usr/bin/env bash

CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

rm -f /tmp/tmux_super_fingers_error.txt

export FINGERS_TARGET_WINDOW=$(tmux display-message -p '#{window_id}')

"$CURRENT_DIR/run.py" 2>/tmp/tmux_super_fingers_error.txt
if [ $? -ne 0 ]; then
  cat /tmp/tmux_super_fingers_error.txt | less
fi
