# super fingers

Opens file links in vim, urls in the browser. And more.

<details>
  <summary>See it in action</summary>
    
  https://user-images.githubusercontent.com/23721/124262753-b2d3ba00-db32-11eb-83ee-77c65dd00d39.mp4
    
</details>

<img src="https://i.imgur.com/y2wd9rK.gif" />

The idea is similar to tmux [fingers](https://github.com/morantron/tmux-fingers) plugin, with few improvements:

- actually opens files in vim running elsewhere in the same tmux session
- open files at line number
- only existing files paths are highlighted

## Install

Requires python3.

Use [TPM](https://github.com/tmux-plugins/tpm):

    set -g @plugin 'artemave/tmux_super_fingers'
    
Hit <kbd>prefix</kbd> + <kbd>I</kbd> to fetch and source the plugin.
