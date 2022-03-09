#!/usr/bin/env bash

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Show error if present before exiting. This will keep tmux window open so that user can see the error.
# Copied from https://stackoverflow.com/a/19590753/51209
exec 3>&1
stderr=$("$CURRENT_DIR/run.py" "$@" 2>&1 1>&3)
if [ $? -ne 0 ]; then
  echo $stderr | less
fi
