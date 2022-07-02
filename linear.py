"""linear regression models between covid cases and crime reports"""

import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.formula.api import ols
from covid_filtering import total_by_month
from crime_filtering import crimes_by_type, read_crimes, filter_by_month

# In the linear regression model, we want to see the relationship between the number of covid cases
# and the number of crime rates per crime type and see if we can predict the
# crime number with the number of covid cases.

# The below list contains the list of months from March, 2020 to May 2021.


def all_dates_list() -> list[list[int]]:
    """
    >>> all_dates_list()
    [[2020, 3], [2020, 4], [2020, 5], [2020, 6], [2020, 7], [2020, 8], [2020, 9], [2020, 10],
    [2020, 11], [2020, 12], [2021, 1], [2021, 2], [2021, 3], [2021, 4], [2021, 5], [2021, 6],
    [2021, 7], [2021, 8]]
    """
    list_2020 = [[2020, x] for x in range(3, 13)]
    list_2021 = [[2021, x] for x in range(1, 9)]
    return list_2020 + list_2021


def new_covid_data(date: list[list[int]]) -> pd.DataFrame:
    """
    This function returns a new data frame consisting of the number of total covid cases, active cases,
    and non-active cases per month in Canada.

    >>> date = all_dates_list()
    >>> new_covid_data(date)
    """
    lst = []
    for each in date:
        lst = lst + [total_by_month(each, 'Canada', ['numtotal', 'numtoday', 'numactive'])]
    return pd.DataFrame(lst)


def new_crime_data(crimetype: str) -> pd.DataFrame:
    """
    This function returns a new data frame that includes the total number of crime reports of a
    particular crime between 2020.4 and 2021.5.

    >>> new_crime_data('Total assault')
    """
    dataset = read_crimes('../../Data/crimes_original_data.csv')
    crimes_so_far = crimes_by_type(dataset, [crimetype])
    date = all_dates_list()

    lst_so_far = []
    count = 0

    for each in date:
        result = filter_by_month(crimes_so_far, each, each)
        for i in range(len(result)):
            if result[i][3] != '':
                count = count + int(result[i][3])
        lst_so_far = lst_so_far + [count]
        count = 0

    return pd.DataFrame(lst_so_far)


def new_df(dataframe1: pd.DataFrame, dataframe2: pd.DataFrame) -> pd.DataFrame:
    """
    This function creates a final dataframe by merging the two given dataframes.

    >>> date = all_dates_list()
    >>> new_1 = new_covid_data(date)
    >>> new_2 = new_crime_data('Total assault')
    >>> new_df(new_1, new_2)
    """
    dataframe1.rename(columns={0: 'Country'}, inplace=True)
    dataframe1.rename(columns={1: 'Date'}, inplace=True)
    dataframe1.rename(columns={2: 'Total num'}, inplace=True)
    dataframe1.rename(columns={3: 'Active'}, inplace=True)
    dataframe1.rename(columns={4: 'Non-Active'}, inplace=True)

    final = pd.merge(dataframe1, dataframe2, how='outer', left_index=True, right_index=True)
    final.rename(columns={0: 'Crime'}, inplace=True)
    return final


def linear_regression(x: pd.Series, y: pd.Series) -> list[float, str]:
    """
    This function calculates linear regression model in y = ax + b form.
    It takes a series of monthly covid cases and monthly crime reports of a particular type of crime as inputs.
    and returns an intercept, linear coefficient, and fitted regression line.

    >>> date = all_dates_list()
    >>> new_1 = new_covid_data(date)
    >>> new_2 = new_crime_data('Total assault')
    >>> final = new_df(new_1, new_2)
    >>> x = final['Active']
    >>> y = final['Crime']
    >>> linear_regression(x, y)
    """
    n = len(x)
    x_mean = x.mean()
    y_mean = y.mean()

    b1_num = ((x - x_mean) * (y - y_mean)).sum()
    b1_den = ((x - x_mean) ** 2).sum()
    b1 = b1_num / b1_den

    b0 = y_mean - (b1 * x_mean)

    reg_line = 'y = {} + {}β'.format(b0, round(b1, 3))

    return [b0, b1, reg_line]


def show(final_data: pd.DataFrame) -> None:
    """
    This function aims to check whether the changes in the number of Covid cases are not associated
    with changes in the number of crime reports with p-value and confirm the regression coefficient
    obtained from the previous function.

    >>> date = all_dates_list()
    >>> new_1 = new_covid_data(date)
    >>> new_2 = new_crime_data('Total assault')
    >>> final = new_df(new_1, new_2)
    >>> show(final)
    """

    fit = ols('Crime ~ Active', data=final_data).fit()
    print(fit.summary())


def display_graph(x: pd.Series, y: pd.Series, b_0: float, b_1: float) -> None:
    """
    This function displays a scatter plot of the corresponding linear graph.

    """

    plt.figure(figsize=(12, 5))
    plt.scatter(x, y, s=300, linewidths=1, color="m", marker="o")

    y_pred = b_0 + b_1 * x

    plt.plot(x, y_pred, color="g")

    # Labeling x and y axis.
    plt.title('Association between the Number of Crime Reports and Covid Cases')
    plt.xlabel('Monthly Covid Cases')
    plt.ylabel('Monthly Crime Reports')

    # function to display the plot
    plt.show()


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['matplotlib.pyplot',
                          'numpy'],
        'allowed-io': [],
        'max-line-length': 150,
        'disable': ['R1705', 'C0200']
    })
