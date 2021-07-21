# Tmux Super Fingers [![Tmux Super Fingers](https://github.com/artemave/tmux_super_fingers/actions/workflows/python-app.yml/badge.svg)](https://github.com/artemave/tmux_super_fingers/actions/workflows/python-app.yml)


<img width="300" src="https://78.media.tumblr.com/e1712952f6eb24f418a997a8da6ae831/tumblr_ou1znif6LW1w4t58uo1_500.gif" />

A tmux "mode" that allows you to open file links in vim, urls in the browser.


<details>
  <summary>Demo</summary>
    
  https://user-images.githubusercontent.com/23721/124262753-b2d3ba00-db32-11eb-83ee-77c65dd00d39.mp4
    
</details>

## Description

Tmux [fingers](https://github.com/morantron/tmux-fingers) plugin introduced the "fingers" mode, where particularly looking chunks of text (e.g. file paths) are highlighted and assigned a "mark". When user hits a key corresponding to the mark, the highlighted text gets copied to clipboard.

Super fingers extends on this idea. Notably:

- it opens files in vim running elsewhere within the same tmux session*
- it opens files at line number
- only files paths that actually exist are highlighted
- text that isn't a file path, but maps onto one (e.g. `UsersController#show` in rails log or `+++ b/app/models/user.rb` in a diff) is also highlighted

\* _if no running (n)vim is found in the session, plugin attempts to start nvim in a new window and, failing that, attempts to start vim._

### Secondary action

If you press <kbd>alt</kbd> when choosing a mark, highlighted text is copied into clipboard instead.

## Install

Requires python3.

Use [TPM](https://github.com/tmux-plugins/tpm):

    set -g @plugin 'artemave/tmux_super_fingers'
    
Hit <kbd>prefix</kbd> + <kbd>I</kbd> to fetch and source the plugin.

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
- [ ] create vim window if there are none in the session
- [ ] extract untested code into tested packages
