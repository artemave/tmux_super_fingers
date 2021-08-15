import re
import subprocess
from typing import Any, List, Iterable, Union


# Sadly, type system specify that return type is List of non None's:
#   https://github.com/python/mypy/issues/8881
def compact(things: Union[Iterable[Any], List[Any]]) -> List[Any]:
    return [e for e in things if e is not None]


def camel_to_snake(string: str) -> str:
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def flatten(list: List[List[Any]]) -> List[Any]:
    l: List[Any] = []
    return sum(list, l)


def shell(command: str) -> str:
    return subprocess.run(
        re.split(' +', command),
        stdout=subprocess.PIPE,
        check=True
    ).stdout.decode('utf-8').rstrip()


def strip(text: str) -> str:
    return '\n'.join(
        map(lambda line: line.rstrip(), text.split('\n'))
    )
