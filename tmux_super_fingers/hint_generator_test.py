from tmux_super_fingers.hint_generator import HintGenerator


def test_generates_hint_from_number():
    hint_generator = HintGenerator()
    assert hint_generator.next_hint("1") == "a"
    assert hint_generator.next_hint("2") == "b"
    assert hint_generator.next_hint("1") == "a"

    for i in range(27):
        hint_generator.next_hint(str(i))

    assert hint_generator.next_hint("2222") == "1b"
