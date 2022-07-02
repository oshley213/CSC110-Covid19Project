"""crime filtering"""
import csv


def read_crimes(filename: str) -> list[list[str]]:
    """
    >>> read_crimes('../../Data/crimes_original_data.csv')
    """
    list_so_far = []

    with open(filename, encoding='UTF8') as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)

        for row in reader:
            sublist_so_far = []
            sublist_so_far = sublist_so_far + [str(row[0]), str(row[1]), str(row[3]), str(row[11])]
            list_so_far = list_so_far + [sublist_so_far]

    return list_so_far


def crimes_by_province(dataset: list[list[str]], province: list[str]) -> list[list[str]]:
    """
    The name for provincial police should be one of

    >>> dataset = read_crimes('../../Data/crimes_original_data.csv')
    >>> crimes_by_province(dataset, ['Quebec', 'Ontario'])
    """

    list_so_far = []
    for each in dataset:
        sublist_so_far = []
        for other in province:
            if other in each[1]:
                sublist_so_far = sublist_so_far + each
                list_so_far = list_so_far + [sublist_so_far]
            else:
                list_so_far = list_so_far

    return list_so_far


def crimes_by_type(dataset: list[list[str]], types: list[str]) -> list[list[str]]:
    """
    * Caution: This function should be used before filter_by_month.
    >>> dataset = read_crimes('../../Data/crimes_original_data.csv')
    >>> crimes_by_type(dataset, ['Total assaults'])
    """

    list_so_far = []
    for each in dataset:
        sublist_so_far = []
        for other in types:
            if other in each[2]:
                sublist_so_far = sublist_so_far + each
                list_so_far = list_so_far + [sublist_so_far]
            else:
                list_so_far = list_so_far

    return list_so_far


def filter_by_month(dataset: list[list[str]], start_date: list[int], end_date: list[int]) -> list[list[str]]:
    """
    This function is for the 'Data/covid19_original_data.csv' file.
    * Caution: This function should be used after all the filtering.

    Preconditions:
    - start_date[0] <= end_date[0]

    >>> dataset = read_crimes('../../Data/crimes_original_data.csv')
    >>> filter_by_month(dataset, [2020, 4], [2021, 5])
    """
    new_list_so_far = []

    for i in range(len(dataset)):
        date_in_list = str.split(dataset[i][0], '-')
        date_in_list = [int(x) for x in date_in_list]
        if date_in_list[0] == start_date[0] == end_date[0]:
            if start_date[1] <= date_in_list[1] <= end_date[1]:
                new_list_so_far = new_list_so_far + [dataset[i]]
        elif date_in_list[0] == start_date[0] and date_in_list[0] != end_date[0]:
            if start_date[1] <= date_in_list[1]:
                new_list_so_far = new_list_so_far + [dataset[i]]
        elif date_in_list[0] != start_date[0] and date_in_list[0] == end_date[0]:
            if date_in_list[1] <= end_date[1]:
                new_list_so_far = new_list_so_far + [dataset[i]]

    return new_list_so_far


def sum_all_crimes(month: list[int], province: str) -> int:
    """
    ...
    >>> sum_all_crimes([2020, 5], 'Ontario')
    """
    dataset = read_crimes('../../Data/crimes_original_data.csv')
    dataset = crimes_by_province(dataset, [province])
    dataset = filter_by_month(dataset, month, month)
    sum_so_far = 0

    for i in range(len(dataset)):
        if dataset[i][3] != '':
            sum_so_far = sum_so_far + int(dataset[i][3])

    return sum_so_far


