let g:vigun_test_keywords = ['def test_[a-zA-Z_]\+']
let g:vjs_tags_enabled = 0

fun! s:watch(cmd)
  return "rg --files | entr -r -c sh -c 'echo ".escape('"'.a:cmd.'"', '"')." && ".a:cmd."'"
endf

let g:vigun_mappings = [
      \ {
      \   'pattern': 'test/.*_test.py$',
      \   'all': 'pytest -s #{file}',
      \   'watch-all': s:watch('pytest -s #{file}'),
      \ }
      \]
