let g:vjs_tags_enabled = 0

fun! s:watch(cmd)
  return "rg --files | entr -r -c sh -c 'echo ".escape('"'.a:cmd.'"', '"')." && ".a:cmd."'"
endf
