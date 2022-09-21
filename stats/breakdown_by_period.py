"""
This module allows you to split data into periods when there is a periodic phenomenon.
"""


from pkgutil import extend_path


def get_positions_of_the_period_changes(data: list) -> list:
    """
    return a list with the positions where there is a change of period
    param data : is the list of data to analyse
    """
    list_of_position = []
    list_of_the_evolution_of_the_slope = __get_the_list_of_the_evolution_of_the_slope(
        data)

    for i in range(len(list_of_the_evolution_of_the_slope)):
        if i != 0:
            if list_of_the_evolution_of_the_slope[i] == "-" and list_of_the_evolution_of_the_slope[i-1] == "+":
                list_of_position.append(i+1)

    return list_of_position


def __get_the_list_of_the_evolution_of_the_slope(data: list):
    list_to_return = []

    for i in range(len(data)):
        if i == 0:
            list_to_return.append("")
        else:
            try:
                list_to_return.append(
                    "+" if float(data[i].replace(",", ".")) - float(data[i-1].replace(",", ".")) >= 0 else "-")
            except ValueError as E:
                print(E)

    return list_to_return
