from app.deck_generator.cleanup import (
    cleanup,
    replace_with_bold,
    replace_with_italic,
    strip_spaces,
)  # Assuming these are in a module


def test_strip_spaces():
    assert strip_spaces("   hello world   ") == "hello world"
    assert strip_spaces("no leading or trailing") == "no leading or trailing"
    assert (
        strip_spaces("   multiple    spaces   inside  ")
        == "multiple    spaces   inside"
    )


def test_replace_with_italic():
    assert (
        replace_with_italic("This is _italic_ text.") == "This is <i>italic</i> text."
    )
    assert replace_with_italic("This is *italic* too.") == "This is <i>italic</i> too."
    assert replace_with_italic("No italics here.") == "No italics here."
    assert replace_with_italic("_multiple_ *italic*") == "<i>multiple</i> <i>italic</i>"


def test_replace_with_bold():
    assert replace_with_bold("This is __bold__ text.") == "This is <b>bold</b> text."
    assert replace_with_bold("This is **bold** too.") == "This is <b>bold</b> too."
    assert replace_with_bold("No bold here.") == "No bold here."
    assert replace_with_bold("__multiple__ **bold**") == "<b>multiple</b> <b>bold</b>"


def test_cleanup_pipeline():
    input_text = "   This is _italic_ and __bold__ text.  "
    expected_output = "This is <i>italic</i> and <b>bold</b> text."
    assert cleanup(input_text) == expected_output

    input_text = "__bold__ and *italic* in the same sentence."
    expected_output = "<b>bold</b> and <i>italic</i> in the same sentence."
    assert cleanup(input_text) == expected_output

    input_text = "   No formatting here.   "
    expected_output = "No formatting here."
    assert cleanup(input_text) == expected_output

    input_text = "Some _italics_, some **bold**."
    expected_output = "Some <i>italics</i>, some <b>bold</b>."
    assert cleanup(input_text) == expected_output
