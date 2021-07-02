# super fingers

<img src="https://i.imgur.com/y2wd9rK.gif" />

Open files/urls without having to manually copy paths/urls.

The idea is similar to tmux [fingers](https://github.com/morantron/tmux-fingers) plugin, with few improvements:

- actually opens files in vim running elsewhere in the same tmux session
- only existing files paths are highlighted

## Install

Requires python3.

Use [TPM](https://github.com/tmux-plugins/tpm):

    set -g @plugin 'artemave/tmux_super_fingers'
    
Hit <kbd>prefix</kbd> + <kbd>I</kbd> to fetch and source the plugin.
