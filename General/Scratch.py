from General import Constants, Functions

from TableComponents import DataTable


# def main():
print("asdsad")
data_list_list = Functions.excel_file_to_data_list_list(Constants.test_file)
print("asdsad")

data_table = DataTable.DataTable(data_list_list)
print("asdsad")

print(data_table.to_str())

data_table.get_inputs_and_output([0, 1, 1, 1, 2])

print(data_table.to_str())

print("")

combo_data_table_list = data_table.get_combo_data_table_list()
for data_table in combo_data_table_list:

    print(data_table.to_str(), "\n\n")

    result_summary = data_table.get_stats_results().summary()
    print(result_summary)

    print("\n\n")
    print("\n\n")
    print("\n\n")


# main()
