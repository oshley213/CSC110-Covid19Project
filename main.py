"""Main python file for project"""
import runpy

import covid_filtering
from crime_filtering import read_crimes, crimes_by_province, filter_by_month, crimes_by_type
import math

####################################################################################################


def total_by_month(month: list[int], province: str, categories: list[str]) \
        -> list[str, int]:
    """Return the sum of 'numtoday', 'numactive' or other 'num_' categories of the
    coressponding month. (Only applicable for data type int).

    The month should be given in following format [year, month].
    Only one province name should be entered.

    >>> total_by_month([2021, 5], 'Ontario', ['numtoday', 'numactive'])
    """
    categories = ['prname', 'date'] + categories
    dataset = covid_filtering.filter_by_date(month, month)
    dataset = covid_filtering.filter_by_province([province], dataset)
    dataset = covid_filtering.dataset_by_type(dataset)
    dataset = covid_filtering.filter_columns(categories, dataset)
    sum_so_far = 0
    list_so_far = [province, month]

    for j in range(2, len(dataset[1])):
        for i in range(len(dataset)):
            sum_so_far = sum_so_far + int(dataset[i][j])
        list_so_far = list_so_far + [sum_so_far]
        sum_so_far = 0

    return list_so_far


def avg_by_month(month: list[int], province: str, category: [str]) -> int:
    """Return the average of each category's by dividing total value by number of dates in
    corresponding month.

    You can only put one category at a time

    The format for other inputs are the same with avg_by_month function.

    >>> avg_by_month([2021, 5], 'Ontario', ['numtoday'])
    2197
    """
    total_value = total_by_month(month, province, category)
    dataset = covid_filtering.filter_by_date(month, month)
    dataset = covid_filtering.filter_by_province([province], dataset)
    all_avg = round(int(total_value[2]) / len(dataset))

    return all_avg

####################################################################################################


def avg_of_province(month: list[int], province: str, category: [str]) -> int:
    """Return the average of category's value by dividing total value by number of provincial police
     incorresponding month.

    Returning dictionary should be in {'category_name': int].

    You must only put one category per time.

    >>> avg_of_province([2021, 5], 'Ontario', ['Total assaults'])
    487
    """
    dataset = read_crimes('../../Data/crimes_original_data.csv')
    dataset = crimes_by_province(dataset, [province])
    dataset = crimes_by_type(dataset, category)
    dataset = filter_by_month(dataset, month, month)
    list_so_far = []

    for i in range(len(dataset)):
        if dataset[i][3] != '':
            list_so_far = list_so_far + [int(dataset[i][3])]

    all_avg = round(sum(list_so_far) / len(list_so_far))

    return all_avg


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


####################################################################################################

def covid_data_for_r(start_month: list[int], end_month: list[int], province: str,
                     covid_category: str) -> list[int]:
    """
    This function is made to be used for calculating correlation coefficient value, r.

    >>> covid_data_for_r([2021, 3], [2021, 5], 'Ontario', 'numactive')
    [13462, 35007, 26183]
    """
    covid_so_far = []
    i = start_month[1]

    if start_month[0] == 2020 and end_month[0] == 2020:
        while i <= end_month[1]:
            covid_so_far = covid_so_far + [[[2020, i],
                                            avg_by_month([2020, i], province, [covid_category])]]
            i = i + 1
    elif start_month[0] == 2021 and end_month[0] == 2021:
        while i <= end_month[1]:
            covid_so_far = covid_so_far + [[[2021, i],
                                            avg_by_month([2021, i], province, [covid_category])]]
            i = i + 1
    elif start_month[0] == 2020 and end_month[0] == 2021:
        while i <= 12 + end_month[1]:
            if i <= 12:
                covid_so_far = covid_so_far + [[[2020, i],
                                                avg_by_month([2020, i], province, [covid_category])]]
            if i > 12:
                covid_so_far = covid_so_far + [[[2021, i - 12],
                                                avg_by_month([2021, i - 12], province,
                                                [covid_category])]]
            i = i + 1

    covid_so_far = [covid_so_far[x][1] for x in range(len(covid_so_far))]
    return covid_so_far


def crime_data_for_r(start_month: list[int], end_month: list[int], province: str,
                     crime_category: str) -> list[int]:
    """
    This function is made to be used for calculating correlation coefficient value, r.

    This function takes about 30 seconds to run. Please be patient.

    >>> crime_data_for_r([2021, 3], [2021, 5], 'Ontario', 'Total assaults')
    [450, 412, 487]
    """
    crime_so_far = []
    j = start_month[1]

    if start_month[0] == 2020 and end_month[0] == 2020:
        while j <= end_month[1]:
            crime_so_far = crime_so_far + [[[2020, j],
                                            avg_of_province([2020, j], province, [crime_category])]]
            j = j + 1
    elif start_month[0] == 2021 and end_month[0] == 2021:
        while j <= end_month[1]:
            crime_so_far = crime_so_far + [[[2021, j],
                                            avg_of_province([2021, j], province,
                                                            [crime_category])]]
            j = j + 1
    elif start_month[0] == 2020 and end_month[0] == 2021:
        while j <= 12 + end_month[1]:
            if j <= 12:
                crime_so_far = crime_so_far + [[[2020, j],
                                                avg_of_province([2020, j], province,
                                                                [crime_category])]]
            if j > 12:
                crime_so_far = crime_so_far + [[[2021, j - 12],
                                                avg_of_province([2021, j - 12], province,
                                                [crime_category])]]
            j = j + 1

    crime_so_far = [crime_so_far[x][1] for x in range(len(crime_so_far))]
    return crime_so_far


def correlation_coefficient(covid_dataset: list[int], crime_dataset: list[int]) -> float:
    """Return the value for correlation coefficient of covid-19 dataset and crime case dataset from
    the given province and given period. The covid-19 dataset and crime case dataset should be
    average by month value.

    ***
    covid_data_for_r must be used to get the covid_dataset.
    crime_data_for_r must be used to get the crime_dataset.

    Precondition:
        - len(covid_dataset) > 2
        - len(crime_dataset) > 2

    >>> covid_dataset = covid_data_for_r([2020, 4], [2021, 5], 'Ontario', 'numactive')
    >>> crime_dataset = crime_data_for_r([2020, 4], [2021, 5], 'Ontario', 'Total assaults')
    >>> correlation_coefficient(covid_dataset, crime_dataset)
    -0.382
    """
    covid_mean = sum(covid_dataset) / len(covid_dataset)
    crime_mean = sum(crime_dataset) / len(crime_dataset)

    r_value = sum([(covid_dataset[x] - covid_mean) * (crime_dataset[x] - crime_mean)
                   for x in range(len(covid_dataset))]) / \
                math.sqrt(sum([(covid_dataset[x] - covid_mean) ** 2
                               for x in range(len(covid_dataset))]) *
                          sum([(crime_dataset[x] - crime_mean) ** 2
                               for x in range(len(crime_dataset))]))

    return round(r_value, 3)


def show_linear_regression() -> None:
    """
    Open the linear regression file

    >>> show_linear_regression()
    """
    runpy.run_path('linear.py')


def open_visual(date: list[int]) -> None:
    """
    open the visualization of corresponding month

    >>> open_visual([2020, 5])
    """
    year = str(date[0] - 2000)
    month = str(date[1])
    file_name = 'visualization_' + year + '_' + month + '.py'
    runpy.run_path(file_name)
