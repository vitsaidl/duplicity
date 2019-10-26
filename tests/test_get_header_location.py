from duplicity import _get_header_location


def test_header_on_the_first_row():
    header_location = "On first row"
    expected_result = 0
    actual_result = _get_header_location(header_location)
    assert expected_result == actual_result


def test_header_manual_input():
    header_location = "Manual input"
    expected_result = 0
    actual_result = _get_header_location(header_location)
    assert expected_result == actual_result


def test_header_doesnt_exist():
    header_location = "Doesn't exist"
    expected_result = None
    actual_result = _get_header_location(header_location)
    assert expected_result == actual_result
