from duplicity import ExaminedData


def test_column_moves_from_eval_to_deval():
    new_dataset = ExaminedData()
    new_dataset.evalued_columns = ["old_eval", "moving"]
    new_dataset.nonevalued_columns = ["old_deval"]
    new_dataset.col_to_deval("moving")
    assert new_dataset.evalued_columns == ["old_eval"]
    assert new_dataset.nonevalued_columns == ["old_deval", "moving"]
