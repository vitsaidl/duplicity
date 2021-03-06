from duplicity import ExaminedData
import pandas as pd


def test_reset_fills_parameters_with_nothing():
    new_dataset = ExaminedData()
    assert new_dataset.report == ""
    assert new_dataset.evalued_columns == []
    assert new_dataset.nonevalued_columns == []
    dataframes_difference = pd.testing.assert_frame_equal(
        new_dataset.loaded_table, pd.DataFrame()
    )
    assert dataframes_difference is None
