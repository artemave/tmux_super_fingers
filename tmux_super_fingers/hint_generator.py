from typing import Dict


class HintGenerator:
    """Generates hints - e.g. `1a` - for a number (mark index)"""

    def __init__(self):
        self.hints: Dict[str, str] = {}

    def next_hint(self, mark_text: str) -> str:
        if mark_text not in self.hints:
            self.hints[mark_text] = self._number_to_hint(len(self.hints))

        return self.hints[mark_text]

    def _number_to_hint(self, number: int) -> str:
        prefix = int(number / 26)
        letter_number = number % 26
        letter = chr(97 + letter_number)

        if prefix > 0:
            return f'{prefix}{letter}'

        return letter
