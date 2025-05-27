from os import path
from typing import Optional
from ..mark import Mark
from ..targets.file_target import FileTarget, ContentType
from ..cli_adapter import RealCliAdapter


class FilePathFinderBase():
    def _match_to_mark(
        self,
        path_prefix: str,
        start: int,
        text: str,
        file_path: str,
        line_number: Optional[str]
    ) -> Optional[Mark]:
        if file_path in ('.', '..', './', '../', '/'):
            return None

        file_path = path.abspath(
            path.join(path_prefix, path.expanduser(file_path))
        )

        if path.isfile(file_path) or path.isdir(file_path):
            cli_adapter = RealCliAdapter()
            content_type = {
                'text': ContentType.TEXT,
            }.get(cli_adapter.get_file_type(file_path)) or ContentType.DATA
            mark_target = FileTarget(file_path, content_type)
            if line_number:
                mark_target.line_number = int(line_number)

            return Mark(
                start=start,
                text=text,
                target=mark_target
            )

        return None
