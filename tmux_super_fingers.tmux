#!/usr/bin/env bash

CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

DEFAULT_FINGERS_KEY="f"
FINGERS_KEY=$(tmux show-option -gqv @super-fingers-key)
FINGERS_KEY=${FINGERS_KEY:-$DEFAULT_FINGERS_KEY}
FINGERS_EXTEND=$(tmux show-option -gqv @super-fingers-extend)

tmux bind "$FINGERS_KEY" new-window -e "FINGERS_EXTEND=$FINGERS_EXTEND" -d -n super-fingers "$CURRENT_DIR/run.sh"
