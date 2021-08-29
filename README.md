# Tmux Super Fingers [![Tmux Super Fingers](https://github.com/artemave/tmux_super_fingers/actions/workflows/python-app.yml/badge.svg)](https://github.com/artemave/tmux_super_fingers/actions/workflows/python-app.yml)

<p align="center">
<img width="300" src="https://78.media.tumblr.com/e1712952f6eb24f418a997a8da6ae831/tumblr_ou1znif6LW1w4t58uo1_500.gif" />
</p>

A tmux "mode" that allows you to open file links in an `$EDITOR`, urls in the browser and more.


<details>
  <summary>Demo</summary>

https://user-images.githubusercontent.com/23721/127735461-e716cca9-c6e4-46b9-97d1-05bc7f84e00c.mp4

</details>

## Description

Tmux [fingers](https://github.com/morantron/tmux-fingers) plugin introduced the "fingers" mode, where particularly looking chunks of text (e.g. file paths) are highlighted and assigned a character "mark". When user hits the mark key, the highlighted text gets copied to clipboard.

Super Fingers builds upon this idea. Notably:

- it opens files in a terminal `$EDITOR`* running elsewhere within the same tmux session**
- only files paths that actually exist are highlighted
- it opens files at line number
- text that isn't a file path, but maps onto one (e.g. `UsersController#show` in rails log or `+++ b/app/models/user.rb` in a diff) is also highlighted
- different types of marks are actioned differently: text files are sent to editor, urls and image files - to OS open.***
- works across all panes in a window
- handles multiline marks (wrapping)

\* _currently this behavior only works for (n)vim - everything else is sent to OS open._</br>
\** _if no running terminal `$EDITOR` is found in the session, plugin attempts to start one in a new window._</br>
\*** _code is designed in such a way that it should be easy to add new types of marks/actions._</br>

### Secondary action

Pressing <kbd>space</kbd> toggles "secondary" mode. In this mode, mark is copied to clipboard.

## Install

Requires python3.

### Using [TPM](https://github.com/tmux-plugins/tpm):

    set -g @plugin 'artemave/tmux_super_fingers'

Hit <kbd>prefix</kbd> + <kbd>I</kbd> to fetch and source the plugin.

### Manual

Clone the repo:

    git clone https://github.com/artemave/tmux_super_fingers.git ~/.tmux/plugins/tmux_fingers_fingers

Source it in your `.tmux.conf`:

    run-shell ~/.tmux/plugins/tmux_fingers_fingers/tmux_super_fingers.tmux

Reload TMUX conf by running:

    tmux source-file ~/.tmux.conf

## Configuration

#### @super-fingers-key

Customize how to enter fingers mode. Always preceded by prefix: `prefix + @super-fingers-key`. Defaults to `f`.

```
set -g @super-fingers-key f
```

### Custom actions

Requires writing some python code.

There are different types of mark [targets](./tmux_super_fingers/targets) (e.g. text file target, url target). Each target type has a primary and a secondary action. You can supply a python file that changes default actions for target types.

For example, the following code changes primary action to open files in vscode and secondary action to send them to vim:

```python3
import os
from .targets.file_target import FileTarget
from .actions.send_to_vim_in_tmux_pane_action import SendToVimInTmuxPaneAction
from .actions.action import Action
from .targets.target_payload import EditorOpenable


class SendToVsCodeAction(Action):
    def __init__(self, target_payload: EditorOpenable):
        self.target_payload = target_payload

    def perform(self):
        path = self.target_payload.file_path

        if self.target_payload.line_number:
            path += f':{self.target_payload.line_number}'

        os.system(f'code -g {path}')


FileTarget.primary_action = SendToVsCodeAction
FileTarget.secondary_action = SendToVimInTmuxPaneAction
```

_You can also define new action types. See [existing actions](./tmux_super_fingers/actions) for details._

Now let's plug it in:

```
set -g @super-fingers-extend /path/to/the/above/code.py
```

## Development

Prerequisites: python3, pipenv, node, make

```
git clone https://github.com/artemave/tmux_super_fingers.git
cd tmux_super_fingers
pipenv install
npm install
```

Run checks and tests:

```
make
```

## TODO

- [x] generic, configurable/pluggable way to send highlited text to arbitrary action (not just `vim` and `xdg-open`)
- [ ] search marks
- [x] secondary action
- [x] configurable `@super-fingers-key`
- [x] create vim window if there are none in the session
- [x] extract untested code into tested packages
- [ ] python stack traces (line numbers)
- [x] handle image files
