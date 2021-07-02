# super fingers

A tmux "mode" that allows you to open file links in vim, urls in the browser.

<details>
  <summary>See it in action</summary>
    
  https://user-images.githubusercontent.com/23721/124262753-b2d3ba00-db32-11eb-83ee-77c65dd00d39.mp4
    
</details>

<img src="https://i.imgur.com/y2wd9rK.gif" />

## Description

Tmux [fingers](https://github.com/morantron/tmux-fingers) plugin introduced the "fingers" mode, where particularly looking chunks of text (e.g. file paths) get highlighted and assigned a "mark". When user hits a key corresponding to the mark, the highlighted text gets copied into clipboard.

Super fingers extends on this idea. Notably:

- it opens files in vim running elsewhere within the same tmux session*
- it opens files at line number
- only files paths that actually exist are highlighted
- text that isn't a file path, but maps onto one (e.g. `UsersController#show` in rails log or `+++ b/app/models/user.rb`) is also highlighted

* _By default, if no running (n)vim is found in the session, plugin attempts to start nvim in a new window and, failing that, attempts to start vim._

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
