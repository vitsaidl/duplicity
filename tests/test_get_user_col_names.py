from duplicity import _get_user_col_names


def test_one_column_in_string():
    col_names = "first"
    expected_result = ["first"]
    actual_result = _get_user_col_names(col_names)
    assert expected_result == actual_result


def test_one_column_with_space_in_string():
    col_names = "  first column  "
    expected_result = ["first column"]
    actual_result = _get_user_col_names(col_names)
    assert expected_result == actual_result


def test_more_columns_with_space_in_string():
    col_names = "  first column, second column, third column  "
    expected_result = ["first column", "second column", "third column"]
    actual_result = _get_user_col_names(col_names)
    assert expected_result == actual_result
