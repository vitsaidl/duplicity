from duplicity import ExaminedData
import pandas as pd
import pathlib


def test_file_loaded_in_expected_way():
    new_dataset = ExaminedData()

    file_name = pathlib.Path("tests/files_for_testing/data_with_header.txt")
    columns = None
    header = 0
    sep = ","
    encoding = "UTF-8"
    new_dataset.load_table_set_col_names(
        file_name, columns, header, sep, encoding
    )

    first_col = [10, 20, 40]
    second_col = [50, 30, 50]
    expected_dataset = pd.DataFrame.from_dict(
        {"first": first_col, "second": second_col}
    )
    dataframes_difference = pd.testing.assert_frame_equal(
        new_dataset.loaded_table, expected_dataset
    )
    assert dataframes_difference is None


def test_noneval_columns_correct_for_file_with_header():
    new_dataset = ExaminedData()

    file_name = pathlib.Path("tests/files_for_testing/data_with_header.txt")
    columns = None
    header = 0
    sep = ","
    encoding = "UTF-8"
    new_dataset.load_table_set_col_names(
        file_name, columns, header, sep, encoding
    )

    expected_columns = ["first", "second"]
    actual_columns = new_dataset.nonevalued_columns
    assert isinstance(actual_columns[0], str)
    assert expected_columns == actual_columns


def test_noneval_columns_correct_for_file_no_header():
    new_dataset = ExaminedData()

    file_name = pathlib.Path("tests/files_for_testing/data_without_header.txt")
    columns = None
    header = None
    sep = ","
    encoding = "UTF-8"
    new_dataset.load_table_set_col_names(
        file_name, columns, header, sep, encoding
    )

    expected_columns = ["0", "1"]
    actual_columns = new_dataset.nonevalued_columns
    assert isinstance(actual_columns[0], str)
    assert expected_columns == actual_columns
