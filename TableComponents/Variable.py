from General import Functions


class Variable:

    def __init__(self, data, header_list=None):

        self.data = data
        self.header_list = header_list

    def to_str(self):
        if self.header_list is None:
            return "VH: {}".format(self.data)
        else:
            return "VD: {}".format(self.data)


def list_list_to_var_list_list(data_list_list, header_list_list=None):
    if header_list_list is None:
        return [[Variable(data) if data is not None else data
                 for data in data_list] for data_list in data_list_list]
    else:
        flipped_header_list_list = Functions.flip_list_list(header_list_list)
        return [[Variable(data, header_list=flipped_header_list_list[d_i])
                 if data is not None else data for d_i, data in enumerate(data_list)]
                for data_list in data_list_list]


def var_list_to_str_list(var_list):
    return [var.to_str() if var is not None else var for var in var_list]


def var_list_list_to_str_list_list(var_list_list):
    return [var_list_to_str_list(var_list) for var_list in var_list_list]


def var_list_to_data_list(var_list):
    return [var.data if var is not None else None for var in var_list]


def var_list_list_to_data_list_list(var_list_list):
    return [var_list_to_data_list(var_list) for var_list in var_list_list]
