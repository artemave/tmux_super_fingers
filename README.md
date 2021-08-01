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

Tmux [fingers](https://github.com/morantron/tmux-fingers) plugin introduced the "fingers" mode, where particularly looking chunks of text (e.g. file paths) are highlighted and assigned a "mark". When user hits the mark key, the highlighted text gets copied to clipboard.

Super Fingers builds upon this idea. Notably:

- it opens files in a terminal `$EDITOR`* running elsewhere within the same tmux session**
- only files paths that actually exist are highlighted
- it opens files at line number
- text that isn't a file path, but maps onto one (e.g. `UsersController#show` in rails log or `+++ b/app/models/user.rb` in a diff) is also highlighted
- different types of marks are actioned differently: text files are sent to editor, urls and image files - to OS open.***

\* _currently this behavior only works for (n)vim - everything else is sent to OS open._

\** _if no running terminal `$EDITOR` is found in the session, plugin attempts to start one in a new window._

\*** _code is designed in such a way that it should be easy to add new types of marks/actions._

### Secondary action

If you press <kbd>alt</kbd> when choosing a mark, highlighted text is copied into clipboard instead.

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

## TODO

- [ ] generic, configurable/pluggable way to send highlited text to arbitrary target (not just `vim` and `xdg-open`)
- [ ] search marks
- [ ] secondary action
- [x] configurable `@super-fingers-key`
- [x] create vim window if there are none in the session
- [ ] extract untested code into tested packages
- [ ] python stack traces (line numbers)
