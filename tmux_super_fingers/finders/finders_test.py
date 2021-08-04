from ..mark import Mark
from ..targets import UrlTarget
from ..test_utils import create_pane


def test_skips_duplicate_marks():
    pane = create_pane({
        'unwrapped_text': 'Some url https://wfhftw.org yarp hm https://wfhftw.org yarp',
    })
    expected_marks = [
        Mark(
            start=36,
            text='https://wfhftw.org',
            target=UrlTarget(
                url='https://wfhftw.org'
            )
        )
    ]
    assert pane.marks == expected_marks
