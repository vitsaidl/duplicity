from duplicity import _get_column_names


def test_header_first_row():
    actual_result = _get_column_names("On first row")
    assert actual_result is None


def test_header_doesnt_exist():
    actual_result = _get_column_names("Doesn't exist")
    assert actual_result is None
