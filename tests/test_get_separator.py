from duplicity import _get_separator


def test_normal_char_returned_without_change():
    separator = "|"
    expected_result = separator
    actual_result = _get_separator(separator)
    assert expected_result == actual_result


def test_space_returned_in_nontext_form():
    separator = "space"
    expected_result = r"\s+"
    actual_result = _get_separator(separator)
    assert expected_result == actual_result


def test_tab_returned_in_nontext_form():
    separator = "tab"
    expected_result = "\t"
    actual_result = _get_separator(separator)
    assert expected_result == actual_result
