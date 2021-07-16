import subprocess
import re
from typing import Dict, Any, List

def compact(l):
    return [e for e in l if e]

def camel_to_snake(string):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def flatten(list: List[List[Any]]) -> List[Any]:
    return sum(list, [])

def shell(command):
    return subprocess.run(
        command.split(' '),
        stdout=subprocess.PIPE,
        check=True
    ).stdout.decode('utf-8').rstrip()

def strip(text):
    return '\n'.join(
        map(lambda line: line.rstrip(), text.split('\n'))
    )
