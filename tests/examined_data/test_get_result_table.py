from duplicity import ExaminedData
import pandas as pd
import pathlib


def test_returned_dataframe_wantuniques_dupldeffirst_wantallcolumns():
    new_dataset = ExaminedData()

    file_name = pathlib.Path("tests/files_for_testing/data_with_header.txt")
    columns = None
    header = 0
    sep = ","
    encoding = "UTF-8"
    new_dataset.load_table_set_col_names(
        file_name, columns, header, sep, encoding
    )
    new_dataset.evalued_columns = ["second"]

    duplicity_def = "first"
    want_uniques = 1
    only_chosen_cols = 0
    actual_dataframe = new_dataset.get_result_table(
        duplicity_def, want_uniques, only_chosen_cols
    )

    first_col = [10, 20]
    second_col = [50, 30]
    expected_dataframe = pd.DataFrame.from_dict(
        {"first": first_col, "second": second_col}
    )
    expected_dataframe.rename(index=lambda row_ind: row_ind + 1, inplace=True)

    dataframes_difference = pd.testing.assert_frame_equal(
        actual_dataframe, expected_dataframe
    )

    assert dataframes_difference is None


def test_returned_dataframe_wantdupl_dupldeffirst_wantallcolumns():
    new_dataset = ExaminedData()

    file_name = pathlib.Path("tests/files_for_testing/data_with_header.txt")
    columns = None
    header = 0
    sep = ","
    encoding = "UTF-8"
    new_dataset.load_table_set_col_names(
        file_name, columns, header, sep, encoding
    )
    new_dataset.evalued_columns = ["second"]

    duplicity_def = "first"
    want_uniques = 0
    only_chosen_cols = 0
    actual_dataframe = new_dataset.get_result_table(
        duplicity_def, want_uniques, only_chosen_cols
    )

    first_col = [40]
    second_col = [50]
    expected_dataframe = pd.DataFrame.from_dict(
        {"first": first_col, "second": second_col}
    )
    expected_dataframe.rename(index={0: 3}, inplace=True)

    dataframes_difference = pd.testing.assert_frame_equal(
        actual_dataframe, expected_dataframe
    )

    assert dataframes_difference is None


def test_returned_dataframe_wantdupl_dupldeffalse_wantallcolumns():
    new_dataset = ExaminedData()

    file_name = pathlib.Path("tests/files_for_testing/data_with_header.txt")
    columns = None
    header = 0
    sep = ","
    encoding = "UTF-8"
    new_dataset.load_table_set_col_names(
        file_name, columns, header, sep, encoding
    )
    new_dataset.evalued_columns = ["second"]

    duplicity_def = False
    want_uniques = 0
    only_chosen_cols = 0
    actual_dataframe = new_dataset.get_result_table(
        duplicity_def, want_uniques, only_chosen_cols
    )

    first_col = [10, 40]
    second_col = [50, 50]
    expected_dataframe = pd.DataFrame.from_dict(
        {"first": first_col, "second": second_col}
    )
    expected_dataframe.rename(index={0: 1, 1: 3}, inplace=True)

    dataframes_difference = pd.testing.assert_frame_equal(
        actual_dataframe, expected_dataframe
    )

    assert dataframes_difference is None


def test_returned_dataframe_wantdupl_dupldeffalse_wantchosencolumns():
    new_dataset = ExaminedData()

    file_name = pathlib.Path("tests/files_for_testing/data_with_header.txt")
    columns = None
    header = 0
    sep = ","
    encoding = "UTF-8"
    new_dataset.load_table_set_col_names(
        file_name, columns, header, sep, encoding
    )
    new_dataset.evalued_columns = ["second"]

    duplicity_def = False
    want_uniques = 0
    only_chosen_cols = 1
    actual_dataframe = new_dataset.get_result_table(
        duplicity_def, want_uniques, only_chosen_cols
    )

    second_col = [50, 50]
    expected_dataframe = pd.DataFrame.from_dict({"second": second_col})
    expected_dataframe.rename(index={0: 1, 1: 3}, inplace=True)
    dataframes_difference = pd.testing.assert_frame_equal(
        actual_dataframe, expected_dataframe
    )

    assert dataframes_difference is None
