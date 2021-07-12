#!/usr/bin/env bash

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
tmux bind f new-window -n super-fingers "$CURRENT_DIR/run.py"
