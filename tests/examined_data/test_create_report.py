from duplicity import ExaminedData
import pathlib


def test_expected_report_is_created():
    new_dataset = ExaminedData()

    file_name = pathlib.Path("tests/files_for_testing/data_with_header.txt")
    columns = None
    header = 0
    sep = ","
    encoding = "UTF-8"
    new_dataset.load_table_set_col_names(
        file_name, columns, header, sep, encoding
    )
    new_dataset.create_report()

    lines = []
    lines.append("Number of table lines is equal to 3")
    lines.append("Number of unique values of column first is 3")
    lines.append("Number of unique values of column second is 2\n")
    expected_report = "\n".join(lines)

    actual_report = new_dataset.report
    assert expected_report == actual_report
