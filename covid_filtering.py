"""Covid-19 Cases Filtering"""

import csv
import math


def load_data(filename: str) -> list[list[str]]:
    """Return a list of lists based on the data in filename. Each list contains covid-19 data from
    different date and different province.

    The data in filename is in a csv format with 40 columns. The 40 columns correspond to pruid,
    prname, prnameFR, date, update, numconf, numprob, numdeaths, numtotal, numtested, numtests,
    numrecover, percentrecover, ratetested, ratetests, numtoday, percentoday, ratetotal, ratedeaths,
    numdeathstoday, percentdeath, numtestedtoday, numteststoday, numrecoveredtoday, percentactive,
    numactive, rateactive, numtotal_last14, ratetotal_last14, numdeaths_last14, ratedeaths_last14,
    numtotal_last7, ratetotal_last7, numdeaths_last7, ratedeaths_last7, avgtotal_last7,
    avgincidence_last7, avgdeaths_last7, avgratedeaths_last7, raterecovered, in that order.

    >>> load_data('../../Data/covid19_original_data.csv')
    """
    sublist_so_far = []
    list_so_far = []

    with open(filename) as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)  # skip the header

        for row in reader:
            assert len(row) == 40  # 'Expected every row to contain 40 elements.'
            # row is a list of strings
            sublist_so_far = sublist_so_far + \
                             [str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]),
                              str(row[5]), str(row[6]), str(row[7]), str(row[8]), str(row[9]),
                              str(row[10]), str(row[11]), str(row[12]), str(row[13]),
                              str(row[14]), str(row[15]), str(row[16]), str(row[17]),
                              str(row[18]), str(row[19]), str(row[20]), str(row[21]),
                              str(row[22]), str(row[23]), str(row[24]), str(row[25]),
                              str(row[26]), str(row[27]), str(row[28]), str(row[29]),
                              str(row[30]), str(row[31]), str(row[32]), str(row[33]),
                              str(row[34]), str(row[35]), str(row[36]), str(row[37]),
                              str(row[38]), str(row[39])]
            list_so_far = list_so_far + [sublist_so_far]
            sublist_so_far = []

    return list_so_far


def dataset_by_type(dataset: list[list[str]]) -> list[list[str, int, float]]:
    """Fill in the blank of list with 0 when the corresponding index is ''. Also, change all the
    strings in the dataset into a appropriate type.

    * Warning: This function should be runned before filter_columns(_, _) function.
    >>> dataset = filter_by_date([2020, 4], [2021, 5])
    >>> dataset_by_type(dataset)
    """
    sublist_so_far = []
    new_list_so_far = []

    for i in range(len(dataset)):
        for j in range(40):
            if dataset[i][j] == '' or dataset[i][j] == 'N/A':
                list.insert(dataset[i], j, '0')
                list.pop(dataset[i], j + 1)
        sublist_so_far = sublist_so_far + \
                         [str(dataset[i][0]), str(dataset[i][1]), str(dataset[i][2]),
                          str(dataset[i][3]), int(dataset[i][4]), int(dataset[i][5]),
                          int(dataset[i][6]), int(dataset[i][7]), int(dataset[i][8]),
                          int(dataset[i][9]), int(dataset[i][10]), int(dataset[i][11]),
                          float(dataset[i][12]), int(dataset[i][13]), int(dataset[i][14]),
                          int(dataset[i][15]), float(dataset[i][16]), float(dataset[i][17]),
                          float(dataset[i][18]), float(dataset[i][19]), float(dataset[i][20]),
                          int(dataset[i][21]), int(dataset[i][22]), int(dataset[i][23]),
                          float(dataset[i][24]), int(dataset[i][25]), float(dataset[i][26]),
                          int(dataset[i][27]), float(dataset[i][28]), int(dataset[i][29]),
                          float(dataset[i][30]), int(dataset[i][31]), float(dataset[i][32]),
                          int(dataset[i][33]), float(dataset[i][34]), int(dataset[i][35]),
                          float(dataset[i][36]), int(dataset[i][37]), float(dataset[i][38]),
                          float(dataset[i][39])]
        new_list_so_far = new_list_so_far + [sublist_so_far]
        sublist_so_far = []

    return new_list_so_far


def filter_by_date(start_date: list[int], end_date: list[int]) -> list[list[str]]:
    """Filter the covid-19 dataset by choosing starting year, month and ending year, month.
    each start_date and end_date should be in format [year, month]. The earliest possible date for
    start date 2020, 1 and latest possible date for end date is 2021, 11.

    This function is for the 'Data/covid19_original_data.csv' file.

    Preconditions:
    - start_date[0] <= end_date[0]

    >>> filter_by_date([2020, 4], [2021, 5])
    """
    dataset = load_data('../../Data/covid19_original_data.csv')
    new_list_so_far = []

    for i in range(len(dataset)):
        date_in_list = str.split(dataset[i][3], '-')
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


def filter_by_province(provinces: list[str], dataset: list[list[str]]) -> list[list[str]]:
    """Filter the covid-19 cases by selecting numbers of province that we want to focus on instead
    of using all the province from the original dataset.

    Provinces should be one of British Colombia, Alberta, Saskatchewan, Manitoba, Ontario, Quebec,
    Newfoundland and Labrador, New Brunswick, Nova Scotia, Prince Edward Island, Yukon,
    Northwest Territories, Nunavut, Repatriated travellers, Canada.

    This function must be used before filter_columns.

    >>> provinces = ['British Columbia', 'Alberta', 'Ontario', 'Quebec']
    >>> dataset = filter_by_date([2020, 7], [2020, 9])
    >>> filter_by_province(provinces, dataset)
    """
    sublist_so_far = []
    list_so_far = []

    for k in range(len(dataset)):
        for i in range(len(provinces)):
            if dataset[k][1] == provinces[i]:
                sublist_so_far = sublist_so_far + dataset[k]
                list_so_far = list_so_far + [sublist_so_far]
                sublist_so_far = []
            else:
                list_so_far = list_so_far

    return list_so_far


def filter_columns(categories: list[str], dataset: list[list[str, int, float]]) -> list[list[str, int, float]]:
    """Return the new dataset where it removes unnecessary columns from the original dataset.
    The new list includes the data for pruid, prname, date, numconf, numprob, numdeaths, numtotal,
    numtested, numtests, numrecover, numtoday, numdeathstoday, numtestedtoday, numteststoday,
    numrecoveredtoday, numactive, in that order.
    This function is designed for the file 'Data/covid19_original_data.csv'
    This function should be runned at the end of all the filtering process.

    >>> categories = ['prname', 'date', 'numconf', 'numprob', 'numdeaths', 'numtotal', \
    'numtested', 'numtests', 'numrecover', 'numtoday', 'numdeathstoday', 'numtestedtoday', \
    'numteststoday', 'numrecoveredtoday', 'numactive']
    >>> dataset = filter_by_date([2020, 4], [2021, 5])
    >>> filter_columns(categories, dataset)
    """
    all_categories = ['pruid', 'prname', 'prnameFR', 'date', 'update', 'numconf', 'numprob',
                      'numdeaths', 'numtotal', 'numtested', 'numtests', 'numrecover',
                      'percentrecover', 'ratetested', 'ratetests', 'numtoday', 'percentoday',
                      'ratetotal', 'ratedeaths', 'numdeathstoday', 'percentdeath', 'numtestedtoday',
                      'numteststoday', 'numrecoveredtoday', 'percentactive',
                      'numactive', 'rateactive', 'numtotal_last14', 'ratetotal_last14',
                      'numdeaths_last14', 'ratedeaths_last14', 'numtotal_last7', 'ratetotal_last7',
                      'numdeaths_last7', 'ratedeaths_last7', 'avgtotal_last7', 'avgincidence_last7',
                      'avgdeaths_last7', 'avgratedeaths_last7', 'raterecovered']
    sublist_so_far = []
    list_so_far = []

    for k in range(len(dataset)):
        for i in range(len(categories)):
            if categories[i] in all_categories:
                index = list.index(all_categories, categories[i])
                sublist_so_far = sublist_so_far + [dataset[k][index]]
        list_so_far = list_so_far + [sublist_so_far]
        sublist_so_far = []

    return list_so_far


def total_by_month(month: list[int], province: str, categories: list[str]) \
        -> list[str, int]:
    """Return the sum of 'numtoday', 'numactive' or other 'num_' categories of the
    coressponding month. (Only applicable for data type int).

    The month should be given in following format [year, month].
    Only one province name should be entered.

    >>> total_by_month([2021, 5], 'Ontario', ['numtoday', 'numactive'])
    """
    categories = ['prname', 'date'] + categories
    dataset = filter_by_date(month, month)
    dataset = filter_by_province([province], dataset)
    dataset = dataset_by_type(dataset)
    dataset = filter_columns(categories, dataset)
    sum_so_far = 0
    list_so_far = [province, month]

    for j in range(2, len(dataset[1])):
        for i in range(len(dataset)):
            sum_so_far = sum_so_far + int(dataset[i][j])
        list_so_far = list_so_far + [sum_so_far]
        sum_so_far = 0

    return list_so_far
