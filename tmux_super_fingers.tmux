#!/usr/bin/env bash

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

DEFAULT_FINGERS_KEY="f"
FINGERS_KEY=$(tmux show-option -gqv @super-fingers-key)
FINGERS_KEY=${FINGERS_KEY:-$DEFAULT_FINGERS_KEY}

EXTEND=$(tmux show-option -gqv @super-fingers-extend)

# The plugin relies on $EDITOR being set. However,
# sometimes (and don't know under what circumstances) tmux does not inherit environment
tmux set-environment -g EDITOR $EDITOR
tmux bind $FINGERS_KEY new-window -n super-fingers "$CURRENT_DIR/run.py $EXTEND"
