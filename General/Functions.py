import openpyxl

from General import Constants


def excel_file_to_data_list_list(filename):
    wb = openpyxl.load_workbook(filename=filename)
    sheet = wb.active
    return clean_list_list([[cell.value for cell in row] for row in sheet.rows])


def flip_list_list(data_list_list):
    return list([list(x) for x in zip(*data_list_list)])


def is_none_list(data_list):
    return all(data is None for data in data_list)


def remove_trailing_none_lists(data_list_list):
    return [data_list for data_list in data_list_list if not is_none_list(data_list)]


def clean_list_list(data_list_list):
    ret_list_list = remove_trailing_none_lists(data_list_list)
    ret_list_list = remove_trailing_none_lists(flip_list_list(ret_list_list))
    return flip_list_list(ret_list_list)


def data_to_str(data, **kwargs):
    length = kwargs.get("length", Constants.def_length)
    print_none = kwargs.get("print_none", Constants.def_print_none)

    ret_str = str(data) if print_none and data is None or data is not None else " " * length
    if length:
        ret_str = ret_str[:length] + " " * (length - len(ret_str))
    return ret_str


def data_list_to_str(data_list, **kwargs):

    def get_spacer(a_spacer):
        if type(a_spacer) == int:
            return " " * a_spacer
        else:
            return str(a_spacer)

    spacer = get_spacer(kwargs.get("spacer") if kwargs.get("spacer") else Constants.def_spacer)

    return spacer.join([data_to_str(data, **kwargs) for data in data_list])


def data_list_list_to_str(data_list_list, **kwargs):
    return "\n".join(data_list_to_str(data_list, **kwargs) for data_list in data_list_list)


def get_binary_list(count, places):
    """
    count: 0 to count
    places: amount of leading zeros
    """
    return [format(i, "0" + str(places) + "b") for i in range(count)]
