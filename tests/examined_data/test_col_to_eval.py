from duplicity import ExaminedData


def test_column_moves_from_deval_to_eval():
    new_dataset = ExaminedData()
    new_dataset.evalued_columns = ["old_eval"]
    new_dataset.nonevalued_columns = ["old_deval", "moving"]
    new_dataset.col_to_eval("moving")
    assert new_dataset.evalued_columns == ["old_eval", "moving"]
    assert new_dataset.nonevalued_columns == ["old_deval"]
