# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 09:21:36 2018

@author: Vit Saidl
"""

import os
import pathlib
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from typing import Union, List
import pandas as pd

START_TEXT_AREA = "1.0"
END_TEXT_AREA = tk.END


def _get_separator(combo_separator_value: str) -> str:
    """Returns the separator in a form usable for other functions

    Args:
        combo_separator_value (str): Separator value from combobox

    Returns:
        str: Separator in a non-word form
    """
    if combo_separator_value == "space":
        columns_separator = r"\s+"
    elif combo_separator_value == "tab":
        columns_separator = "\t"
    else:
        columns_separator = combo_separator_value
    return columns_separator


def _get_header_location(header_location_combo: str) -> Union[int, None]:
    """Returns location of header in loaded file

    Option "Manually" is used for case of custom or corrupted header

    Args:
        header_location_combo (str): Header location from combobox

    Returns:
        int/None: Either 0 or None - params in this forms expected \
        by pandas function
    """
    header_location: Union[int, None]
    if header_location_combo in ["On first row", "Manual input"]:
        header_location = 0
    elif header_location_combo == "Doesn't exist":
        header_location = None
    return header_location


def _get_user_col_names(cust_col_names: str) -> List[str]:
    """Parse content of text area for custom column names and return the names in \
    form of list

    Args:
        cust_col_names (str): Custom columns names separated by comma

    Returns:
        list[str]: Columns names given by an user
    """
    column_names = cust_col_names.split(",")
    column_names = list(map(str.strip, column_names))
    return column_names


def _get_column_names(header_location_combo: str) -> Union[None, List[str]]:
    """Returns columns names depending on the user choices

    Args:
        header_location_combo (str): Header location from combobox

    Returns:
        None/List[str]: Either columns names are in the file/are not \
        desirable or the users input is used for them
    """
    if header_location_combo in ["On first row", "Doesn't exist"]:
        column_names = None
    elif header_location_combo == "Manual input":
        string_col_names = textfield_custom_header.get(
            START_TEXT_AREA, END_TEXT_AREA
        )
        column_names = _get_user_col_names(string_col_names)
    return column_names


def _get_file_name() -> str:
    """Shows window-like interface for chosing loaded file

    Returns:
        str: Name of loaded file (clink on cancel button leads to "")
    """
    home_dir = os.path.dirname(os.path.realpath(__file__))
    file_types = (
        ("csv files", "*.csv"),
        ("txt files", "*.txt"),
        ("all files", "*.*"),
    )
    loaded_file = filedialog.askopenfilename(
        initialdir=home_dir, title="Choose file", filetypes=file_types
    )
    return loaded_file


class ExaminedData:
    """Representing data from loaded csv-like file
    """

    def __init__(self):
        self.reset_data()

    def reset_data(self):
        """Reseting instance properties to state before loading a file
        """
        self.loaded_table = pd.DataFrame()
        self.nonevalued_columns = []
        self.evalued_columns = []
        self.report = ""

    def load_table_set_col_names(
        self,
        file_name,
        columns_names,
        header_location,
        columns_separator,
        file_encoding,
    ):
        """Loads file in pandas dataset and sets nonevalued_columns parameter \
        to datasets name

        Args:
            file_name (str): File containing data
            columns_names (None/List[str]): Column names or None (if absent or
            in file)
            header_location(None/int): Either None or 0 (header on 1st line)
            columns_separator(str): Char(s) separating individual columns
            file_encoding(str): File encoding
        """
        self.loaded_table = pd.read_csv(
            file_name,
            names=columns_names,
            header=header_location,
            sep=columns_separator,
            encoding=file_encoding,
        )
        # even in case of nonexplicit column names these have to be of str type
        self.loaded_table.columns = list(map(str, self.loaded_table.columns))
        self.nonevalued_columns = list(self.loaded_table.columns)

    def create_report(self) -> None:
        """Creates report about loaded table
        """
        self.report = (
            f"Number of table lines is equal to {len(self.loaded_table)}\n"
        )
        for column in self.loaded_table.columns:
            no_unique_values = self.loaded_table[column].nunique()
            self.report += (
                "Number of unique values of column "
                f"{column} is {no_unique_values}\n"
            )

    def col_to_eval(self, column_name: str) -> None:
        """Moves specified column from nonevalued_columns to evalued_columns

        Args:
            column_name (str): Column name
        """
        self.evalued_columns.append(column_name)
        self.nonevalued_columns.remove(column_name)

    def col_to_deval(self, column_name: str) -> None:
        """Moves specified column from evalued_columns to nonevalued_columns

        Args:
            column_name (str): Column name
        """
        self.evalued_columns.remove(column_name)
        self.nonevalued_columns.append(column_name)

    def get_result_table(
        self,
        duplicity_def: Union[bool, str],
        want_uniques: int,
        only_chosen_cols: int,
    ) -> pd.DataFrame:
        """Create result table based on loaded table and user specifications

        Args:
            duplicity_def(bool/str): Either value is "first" - first occurence
            of element isn't defined as duplicate - or value is False
            - even first from duplicate elements is defined as duplicate
            want_uniques(int): Either we want only duplicates in result
            table (0) or we want only unique values (1)
            only_chosen_cols(int): Either we want all columns in result
            table (0) or we want only specified columns (1)

        Returns:
            pandas.DataFrame: Subset of loaded table
        """
        is_duplicity_row = self.loaded_table.duplicated(
            subset=self.evalued_columns, keep=duplicity_def
        )
        if want_uniques == 1:
            wanted_rows = [not bool_flag for bool_flag in is_duplicity_row]
        else:
            wanted_rows = is_duplicity_row
        result_table = self.loaded_table[wanted_rows]
        # row number should start with index 1, no 0
        result_table.rename(index=lambda row_ind: row_ind + 1, inplace=True)
        if only_chosen_cols == 1:
            result_table = result_table[self.evalued_columns]
        return result_table


def _clean_summary_field() -> None:
    """Delete all content in the summary text area
    """
    textfield_summary.config(state=tk.NORMAL)
    textfield_summary.delete("1.0", tk.END)
    textfield_summary.config(state=tk.DISABLED)


def _fill_summary_field(text: str) -> None:
    """Insert text into the summary text area

    Args:
        text(str): Info about loaded file with respect to duplicities
    """
    textfield_summary.config(state=tk.NORMAL)
    textfield_summary.insert(tk.END, text)
    textfield_summary.config(state=tk.DISABLED)


def _repopulate_duplicity_combolistbox(file_content: ExaminedData) -> None:
    """Delete obsolete content of duplicity combo and listboxes and fill
    them with new info
    """
    combobox_add_column["values"] = file_content.nonevalued_columns
    listbox_duplicity_list.delete(0, tk.END)
    listbox_duplicity_list.insert(tk.END, *file_content.evalued_columns)
    combobox_remove_column["values"] = file_content.evalued_columns


def load_file(file_content: ExaminedData) -> None:
    """Reads from user interface, loads file and sets comboboxes

    Args:
        file_content(ExaminedData): Contains info about loaded file
    """
    loaded_file = _get_file_name()
    is_file_chosen = loaded_file != ""

    header_location_combo = combobox_header.get()
    file_encoding = combobox_encoding.get()
    columns_separator_combo = combobox_separator.get()

    if is_file_chosen:
        button_remove_column.config(state=tk.DISABLED)
        button_generate_result.config(state=tk.DISABLED)
        file_content.reset_data()
        _repopulate_duplicity_combolistbox(file_content)
        combobox_remove_column.set("")
        _clean_summary_field()

        columns_separator = _get_separator(columns_separator_combo)
        columns_names = _get_column_names(header_location_combo)
        header_location = _get_header_location(header_location_combo)
        file_content.load_table_set_col_names(
            loaded_file,
            columns_names,
            header_location,
            columns_separator,
            file_encoding,
        )
        file_content.create_report()
        _fill_summary_field(file_content.report)

        combobox_add_column["values"] = file_content.nonevalued_columns
        if len(file_content.nonevalued_columns) > 0:
            combobox_add_column.current(0)

        button_add_column.config(state=tk.NORMAL)
    else:
        messagebox.showerror("Error", "No file has been chosen")


def add_column(file_content: ExaminedData) -> None:
    """Moves column from noneval to eval + updated user interface accordingly

    Args:
        file_content(ExaminedData): Contains info about loaded file
    """
    column_name = combobox_add_column.get()
    file_content.col_to_eval(column_name)
    _repopulate_duplicity_combolistbox(file_content)

    button_remove_column.config(state=tk.NORMAL)
    button_generate_result.config(state=tk.NORMAL)
    combobox_remove_column.current(0)

    if len(file_content.nonevalued_columns) > 0:
        combobox_add_column.current(0)
    else:
        combobox_add_column.set("")
        button_add_column.config(state=tk.DISABLED)


def remove_column(file_content: ExaminedData) -> None:
    """Moves column from eval to noneval + updated user interface accordingly

    Args:
        file_content(ExaminedData): Contains info about loaded file
    """
    column_name = combobox_remove_column.get()
    file_content.col_to_deval(column_name)
    _repopulate_duplicity_combolistbox(file_content)

    button_add_column.config(state=tk.NORMAL)
    combobox_add_column.current(0)

    if len(file_content.evalued_columns) > 0:
        combobox_remove_column.current(0)
    else:
        combobox_remove_column.set("")
        button_remove_column.config(state=tk.DISABLED)
        button_generate_result.config(state=tk.DISABLED)


def generate_result_file(file_content: ExaminedData) -> None:
    """Saves table with/without duplicates into csv file

    Args:
        file_content(ExaminedData): Contains info about loaded file
    """
    duplicity_flag: Union[str, bool]
    if var_duplicity_def.get() == 1:
        duplicity_flag = "first"
    else:
        duplicity_flag = False

    result = file_content.get_result_table(
        duplicity_flag, var_want_uniques.get(), var_want_chosen_col.get()
    )
    separator_output = _get_separator(combobox_separator.get())
    if separator_output == r"\s+":
        separator_output = " "

    output_file_path = pathlib.Path("duplicity_result.csv")

    want_row_number_in_result = checkbox_index.state() == ("selected",)
    result.to_csv(
        output_file_path,
        sep=separator_output,
        encoding=combobox_encoding.get(),
        index=want_row_number_in_result,
    )
    output_file_whole_path = output_file_path.resolve()
    messagebox.showinfo(
        "Info", "File saved as \n" + str(output_file_whole_path)
    )


if __name__ == "__main__":

    file_content = ExaminedData()

    root = tk.Tk()
    root.title("Duplicity finder")
    mainframe = ttk.Frame(root, padding=(3, 3, 12, 12))
    mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)

    label_separator = ttk.Label(mainframe, text="Column separator")
    label_separator.grid(column=0, row=0, sticky=tk.W)
    separator_values = [",", ".", ";", ":", "|", "/", "\\", "space", "tab"]
    combobox_separator = ttk.Combobox(
        mainframe, values=separator_values, state="readonly"
    )
    combobox_separator.grid(column=0, row=0, sticky=tk.E)
    combobox_separator.set(separator_values[0])

    label_encoding = ttk.Label(mainframe, text="Encoding")
    label_encoding.grid(column=0, row=1, sticky=tk.W)
    encoding_values = ["utf8", "windows-1250"]
    combobox_encoding = ttk.Combobox(
        mainframe, values=encoding_values, state="readonly"
    )
    combobox_encoding.grid(column=0, row=1, sticky=tk.E)
    combobox_encoding.set(encoding_values[0])

    label_header = ttk.Label(mainframe, text="Header")
    label_header.grid(column=0, row=2, sticky=tk.W)
    header_values = ["Doesn't exist", "On first row", "Manual input"]
    combobox_header = ttk.Combobox(
        mainframe, values=header_values, state="readonly"
    )
    combobox_header.grid(column=0, row=2, sticky=tk.E)
    combobox_header.set(header_values[1])

    label_custom_header = ttk.Label(
        mainframe, text="Custom header - separate column names by comma"
    )
    label_custom_header.grid(column=0, row=3)
    # textfield width sets width of whole app window
    textfield_custom_header = tk.Text(mainframe, height=1, width=80)
    textfield_custom_header.grid(column=0, row=4)

    button_load_file = ttk.Button(
        mainframe, text="Load file", command=lambda: load_file(file_content)
    )
    button_load_file.grid(column=0, row=5)

    label_summary = ttk.Label(mainframe, text="Summary")
    label_summary.grid(column=0, row=6)
    textfield_summary = tk.Text(mainframe, height=8, width=80)
    textfield_summary.config(state=tk.DISABLED)
    textfield_summary.grid(column=0, row=7, sticky=tk.W)

    label_add_column = ttk.Label(mainframe, text="Add to list")
    label_add_column.grid(column=0, row=8, sticky=tk.W)
    combobox_add_column = ttk.Combobox(mainframe, state="readonly")
    combobox_add_column.grid(column=0, row=9, sticky=tk.W)
    button_add_column = ttk.Button(
        mainframe,
        text="Add column",
        command=lambda: add_column(file_content),
        state=tk.DISABLED,
    )
    button_add_column.grid(column=0, row=10, sticky=tk.W)

    label_duplicity_list = ttk.Label(
        mainframe, text="Columns of subtable studied because of duplicities"
    )
    label_duplicity_list.grid(column=0, row=8)
    listbox_duplicity_list = tk.Listbox(mainframe)
    listbox_duplicity_list.grid(column=0, row=9)

    label_remove_column = ttk.Label(mainframe, text="Remove from list")
    label_remove_column.grid(column=0, row=8, sticky=tk.E)
    combobox_remove_column = ttk.Combobox(mainframe, state="readonly")
    combobox_remove_column.grid(column=0, row=9, sticky=tk.E)
    button_remove_column = ttk.Button(
        mainframe,
        text="Remove column",
        command=lambda: remove_column(file_content),
        state=tk.DISABLED,
    )
    button_remove_column.grid(column=0, row=10, sticky=tk.E)

    label_duplicity_def = ttk.Label(mainframe, text="Duplicity definition")
    label_duplicity_def.grid(column=0, row=11)
    var_duplicity_def = tk.IntVar()
    var_duplicity_def.set(1)
    radiobutton_duplicity_def = ttk.Radiobutton(
        mainframe,
        text="Second and subsequent occurences of certain value",
        variable=var_duplicity_def,
        value=1,
    )
    radiobutton_duplicity_def.grid(column=0, row=12)
    radiobutton_duplicity_def = ttk.Radiobutton(
        mainframe,
        text="All occurences of certain value (first including)",
        variable=var_duplicity_def,
        value=2,
    )
    radiobutton_duplicity_def.grid(column=0, row=13)

    label_want_uniques = ttk.Label(mainframe, text="We want")
    label_want_uniques.grid(column=0, row=14)
    var_want_uniques = tk.IntVar()
    var_want_uniques.set(1)
    radiobutton_want_uniques = ttk.Radiobutton(
        mainframe, text="Unique rows", variable=var_want_uniques, value=1
    )
    radiobutton_want_uniques.grid(column=0, row=15)
    radiobutton_want_uniques = ttk.Radiobutton(
        mainframe, text="Duplicated rows", variable=var_want_uniques, value=0
    )
    radiobutton_want_uniques.grid(column=0, row=16)

    label_want_chosen_col = ttk.Label(
        mainframe, text="Table in output file consists of"
    )
    label_want_chosen_col.grid(column=0, row=17)
    var_want_chosen_col = tk.IntVar()
    var_want_chosen_col.set(1)
    radiobutton_want_chosen_col = ttk.Radiobutton(
        mainframe, text="All columns", variable=var_want_chosen_col, value=0
    )
    radiobutton_want_chosen_col.grid(column=0, row=18)
    radiobutton_want_chosen_col = ttk.Radiobutton(
        mainframe,
        text="Only columns chosen for duplicity determination",
        variable=var_want_chosen_col,
        value=1,
    )
    radiobutton_want_chosen_col.grid(column=0, row=19)

    checkbox_index = ttk.Checkbutton(
        mainframe, text="Row numbers in output file"
    )
    checkbox_index.state(["!alternate"])  # delete undefined state
    checkbox_index.state(
        ["selected"]
    )  # set selected state; impossible without prev. row
    checkbox_index.grid(column=0, row=20)

    button_generate_result = ttk.Button(
        mainframe,
        text="Generate output file",
        command=lambda: generate_result_file(file_content),
        state=tk.DISABLED,
    )
    button_generate_result.grid(column=0, row=21)

    root.mainloop()
