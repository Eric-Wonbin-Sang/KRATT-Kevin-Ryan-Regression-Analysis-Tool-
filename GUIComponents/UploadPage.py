from PyQt5.QtWidgets import *

from TableComponents import DataTable, Variable

import PyCute
import Functions
import Constants


class UploadPage(QWidget):

    def __init__(self, parent_widget):

        super().__init__()

        self.parent_widget = parent_widget

        self.button_dict = {
            "Submit": PyCute.Button(default_text='Submit', connect_func=self.setup_data_table_layout),
            "Delete": PyCute.Button(default_text='Delete', connect_func=self.delete_button_func),
            "Reload": PyCute.Button(default_text='Reload', connect_func=self.reload_button_func),
            "Commit": PyCute.Button(default_text='Commit', connect_func=self.commit_button_func)
        }

        self.text_box_dict = {
            "filename": PyCute.TextBox(text=Constants.test_file)
        }

        self.excel_scrape_layout = self.excel_scrape_layout()
        self.data_table_layout = QGridLayout()

        self.data_table, self.layout_dict = None, None

        self.layout = PyCute.add_to_layout(QVBoxLayout(), self.excel_scrape_layout, self.data_table_layout)
        self.setLayout(self.layout)

    def excel_scrape_layout(self):
        return PyCute.add_to_layout(QGridLayout(),
                                    (PyCute.Label(default_text="File path", align_right=True), 0, 0),
                                    (self.text_box_dict["filename"], 0, 1, 1, 3),
                                    (self.button_dict["Submit"], 1, 3),
                                    (self.button_dict["Delete"], 2, 3))

    def set_data_table(self, **kwargs):
        self.data_table = DataTable.DataTable(
            Functions.excel_file_to_data_list_list(self.text_box_dict["filename"].text()), **kwargs)

    def add_to_grid_layout(self):
        PyCute.remove_from_layout(self.data_table_layout)
        for i, key in enumerate(self.layout_dict):
            PyCute.add_to_layout(self.data_table_layout,
                                 (PyCute.Label(default_text=key, align_right=True), i, 0),
                                 (self.layout_dict[key], i, 1, 1, 3))
        PyCute.add_to_layout(self.data_table_layout,
                             (self.button_dict["Reload"], len(self.layout_dict) + 1, 3),
                             (self.button_dict["Commit"], len(self.layout_dict) + 2, 3))

    def delete_button_func(self):
        PyCute.remove_from_layout(self.data_table_layout)
        self.data_table, self.layout_dict = None, None

    def reload_button_func(self):
        state_dict = {"Ignore": 0, "Input": 1, "Output": 2}
        header_depth, state_list = 0, []
        for key in self.layout_dict:
            if type(self.layout_dict[key]) == PyCute.TextBox:
                header_depth = int(self.layout_dict[key].text())
            elif type(self.layout_dict[key]) == PyCute.DropDown:
                state_list.append(state_dict[self.layout_dict[key].currentText()])
        self.setup_data_table_layout(header_depth=header_depth, state_list=state_list)

    def set_layout_dict(self):
        layout_dict = {"Header Depth": PyCute.TextBox(text=self.data_table.header_depth)}
        header_list_list = Functions.flip_list_list(
            Variable.var_list_list_to_data_list_list(self.data_table.header_list_list))
        for i, header_list in enumerate(header_list_list):
            layout_dict[str(header_list)] = \
                PyCute.DropDown(option_list=["Input", "Output", "Omit"],
                                default_option=None if i != len(header_list_list) - 1 else "Output")
        self.layout_dict = layout_dict

    def setup_data_table_layout(self, **kwargs):
        self.set_data_table(**kwargs)
        self.set_layout_dict()
        self.add_to_grid_layout()

    def commit_button_func(self):
        self.parent_widget.stats_page.data_table = self.data_table
        self.parent_widget.switch_page()
        self.parent_widget.stats_page.build_gui()
