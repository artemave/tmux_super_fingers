from ..mark import Mark
from ..targets import UrlTarget
from .test_utils import create_pane


def test_finds_url():
    pane = create_pane({
        'unwrapped_text': 'Some url https://wfhftw.org yarp',
    })
    expected_marks = [
        Mark(
            start=9,
            text='https://wfhftw.org',
            target=UrlTarget(
                url='https://wfhftw.org'
            )
        )
    ]
    assert pane.marks == expected_marks
