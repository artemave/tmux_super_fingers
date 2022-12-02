import datetime

from . import utils


def test_strip_removes_leading_whitespaces_from_each_line():
    text = ' stuff\nmore stuff \nbananas\nballs'
    assert utils.strip(text) == ' stuff\nmore stuff\nbananas\nballs'


def test_shell_runs_shell_process():
    assert utils.shell('date +%Y') == str(datetime.datetime.today().year)
