#!/usr/bin/env bash

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

DEFAULT_FINGERS_KEY="f"
FINGERS_KEY=$(tmux show-option -gqv @super-fingers-key)
FINGERS_KEY=${FINGERS_KEY:-$DEFAULT_FINGERS_KEY}

tmux bind $FINGERS_KEY new-window -n super-fingers "$CURRENT_DIR/run.py"
