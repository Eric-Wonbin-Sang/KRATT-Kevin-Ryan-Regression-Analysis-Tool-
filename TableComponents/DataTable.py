import numpy
import statsmodels.api as sm

from TableComponents import Variable

from General import Functions


class DataTable:

    def __init__(self, data_list_list, **kwargs):

        header_depth = kwargs.get("header_depth")
        state_list = kwargs.get("state_list")
        date_indexes = kwargs.get("date_indexes")

        self.data_list_list = data_list_list
        self.state_list = state_list

        self.date_indexes = date_indexes
        self.header_depth = header_depth if header_depth is not None else self.get_header_depth()
        self.header_list_list = self.get_header_list_list()
        self.var_list_list = self.get_var_list_list()

        self.input_list_list, self.output_list = [], []
        self.get_inputs_and_output(self.state_list)

    # constructing ------------------------------
    def get_header_depth(self):

        def is_data_list(a_data_list):
            if self.date_indexes:
                a_data_list = [a_data for temp_i, a_data in enumerate(data_list) if temp_i not in self.date_indexes]
            return all(type(a_data) in [float, int] for a_data in a_data_list)

        for d_i, data_list in enumerate(self.data_list_list):
            if is_data_list(data_list):
                return d_i
        return 1

    def get_header_list_list(self):
        return Variable.list_list_to_var_list_list(self.data_list_list[:self.header_depth])

    def get_var_list_list(self):
        return Variable.list_list_to_var_list_list(self.data_list_list[self.header_depth:], self.header_list_list)
    # constructing ------------------------------

    # combining ---------------------------------
    def get_inputs_and_output(self, state_list):
        input_list_list = []
        output_list = []

        if state_list:
            for i, var_list in enumerate(Functions.flip_list_list(self.var_list_list)):
                if state_list[i] == 1:
                    input_list_list.append(var_list)
                elif state_list[i] == 2:
                    output_list = var_list

        self.input_list_list = input_list_list
        self.output_list = output_list

    def get_combo_list_list(self):
        """
        Returns a 2d list of every combination of the DataTable's input_list in DataTable.input_list_list
        with the DataTable.output_list appended to the back.
        """
        combo_list_list = []
        for b_num in Functions.get_binary_list(2 ** len(self.input_list_list), len(self.input_list_list))[1:]:
            combo_list_list.append([input_list for il_i, input_list in enumerate(self.input_list_list)
                                    if [int(letter) for letter in b_num][il_i]] + [self.output_list])
        return combo_list_list

    def get_combo_data_table_list(self):
        """
        Returns a list of DataTables that are every combination of the parent's inputs and output
        """
        return [var_list_list_to_data_table(combo_list) for combo_list in self.get_combo_list_list()]
    # combining ---------------------------------

    # statistics --------------------------------
    def get_stats_results(self):

        x = sm.add_constant(numpy.array(Variable.var_list_list_to_data_list_list(self.input_list_list)).T)
        y = Variable.var_list_to_data_list(self.output_list)

        return sm.OLS(endog=y, exog=x).fit()

    # statistics --------------------------------

    def to_str(self):
        header_list_list_to_str = Functions.data_list_list_to_str(
            Variable.var_list_list_to_str_list_list(self.header_list_list))

        data_separator = "-" * len(header_list_list_to_str.split("\n")[0])

        var_list_list_to_str = Functions.data_list_list_to_str(
            Variable.var_list_list_to_str_list_list(self.var_list_list))

        return "\n".join([header_list_list_to_str, data_separator, var_list_list_to_str])


def var_list_list_to_data_table(var_list_list):

    data_list_list = Functions.flip_list_list(var_list_list)

    header_list_list = Functions.flip_list_list([data.header_list for data in data_list_list[0]])
    header_list_list = Variable.var_list_list_to_data_list_list(header_list_list)
    data_list_list = Variable.var_list_list_to_data_list_list(data_list_list)

    source_list_list = header_list_list + data_list_list
    return DataTable(source_list_list, state_list=([1] * (len(var_list_list) - 1)) + [2])
