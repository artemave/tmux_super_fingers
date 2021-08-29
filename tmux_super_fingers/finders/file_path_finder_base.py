from os import path
from typing import Optional
from ..mark import Mark
from ..targets.file_target import FileTarget, ContentType
from ..tmux_adapter import RealTmuxAdapter


class FilePathFinderBase():
    def _match_to_mark(
        self,
        path_prefix: str,
        start: int,
        text: str,
        file_path: str,
        line_number: Optional[str]
    ) -> Optional[Mark]:
        file_path = path.abspath(
            path.join(path_prefix, path.expanduser(file_path))
        )

        if path.isfile(file_path):
            tmux_adapter = RealTmuxAdapter()
            content_type = {
                'text': ContentType.TEXT,
                'application': ContentType.EXECUTABLE
            }.get(tmux_adapter.get_file_type(file_path)) or ContentType.DATA
            mark_target = FileTarget(file_path, content_type)
            if line_number:
                mark_target.line_number = int(line_number)

            return Mark(
                start=start,
                text=text,
                target=mark_target
            )

        return None
