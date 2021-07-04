#!/usr/bin/env bash

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
tmux bind f new-window -n super-fingers "python3 $CURRENT_DIR/__init__.py"
