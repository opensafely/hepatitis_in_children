import re
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parents[1]
OUTPUT_DIR = BASE_DIR / "output"
ANALYSIS_DIR = BASE_DIR / "analysis"


def match_input_files(file: str) -> bool:
    """Checks if file name has format outputted by cohort extractor"""
    pattern = r"^input_20\d\d-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])\.csv.gz"
    return True if re.match(pattern, file) else False


def get_date_input_file(file: str) -> str:
    """Gets the date in format YYYY-MM-DD from input file name string"""
    # check format
    if not match_input_files(file):
        raise Exception("Not valid input file format")

    else:
        date = result = re.search(r"input_(.*)\.csv.gz", file)
        return date.group(1)


def match_input_files_weekly(file: str) -> bool:
    """Checks if file name has format outputted by cohort extractor"""
    pattern = r"^input_weekly_20\d\d-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])\.csv.gz"
    return True if re.match(pattern, file) else False


def get_date_input_file_weekly(file: str) -> str:
    """Gets the date in format YYYY-MM-DD from input file name string"""
    # check format
    if not match_input_files_weekly(file):
        raise Exception("Not valid input file format")

    else:
        date = result = re.search(r"input_weekly_(.*)\.csv.gz", file)
        return date.group(1)


def redact_small_numbers(
    df, n, numerator, denominator, rate_column, date_column, groupby_column
):
    """
    Takes counts df as input and suppresses low numbers.  Sequentially redacts
    low numbers from numerator and denominator until count of redcted values >=n.
    Rates corresponding to redacted values are also redacted.
    df: input df
    n: threshold for low number suppression
    numerator: numerator column to be redacted
    denominator: denominator column to be redacted
    groupby_column: column measure is grouped by, if any
    """

    def suppress_column(column):
        suppressed_column = column[column > n]
        suppressed_count = column[column <= n].sum()

        # if no values suppressed dont need to suppress anything
        if len(suppressed_column) == len(column):
            pass

        else:
            column[column <= n] = np.nan
            # if not all nan make sure enough redacted
            if column.any():
                while suppressed_count <= n:
                    suppressed_count += column.min()

                    column[column.idxmin()] = np.nan

                    # if whole column redacted stop
                    if not column.any():
                        break
        return column

    df_list = []

    dates = df[date_column].unique()

    for d in dates:
        df_subset = df.loc[df[date_column] == d, :]

        for column in [numerator, denominator]:
            df_subset.loc[:, column] = suppress_column(df_subset.loc[:, column])

        df_subset.loc[
            (df_subset[numerator].isna()) | (df_subset[denominator].isna()), rate_column
        ] = np.nan
        df_list.append(df_subset)

    redacted_df = pd.concat(df_list, axis=0)

    if groupby_column:
        for column in [numerator, denominator]:
            redacted_df.groupby(by=groupby_column)[[column]].transform(
                lambda x: suppress_column(x)
            )

    else:
        for column in [numerator, denominator]:
            redacted_df[column] = suppress_column(redacted_df[column])

    return redacted_df


def plot_measures(
    df,
    filename: str,
    title: str,
    column_to_plot: str,
    y_label: str,
    as_bar: bool = False,
    category: str = None,
):
    """Produce time series plot from measures table.  One line is plotted for each sub
    category within the category column. Saves output in 'output' dir as jpeg file.
    Args:
        df: A measure table
        title: Plot title
        column_to_plot: Column name for y-axis values
        y_label: Label to use for y-axis
        as_bar: Boolean indicating if bar chart should be plotted instead of line chart. Only valid if no categories.
        category: Name of column indicating different categories
    """
    plt.figure(figsize=(15, 8))

    df = df.sort_values(by="date")
    # mask nan values (redacted)
    mask = np.isfinite(df[column_to_plot])

    if category:
        df = df[df[category].notnull()]
        for unique_category in sorted(df[category].unique()):
            # subset on category column and sort by date
            df_subset = df[df[category] == unique_category].sort_values("date")

            plt.plot(
                df_subset["date"][mask], df_subset[column_to_plot][mask], marker="o"
            )
    else:
        if as_bar:
            df.plot.bar("date", column_to_plot, legend=False)
        else:
            plt.plot(df["date"][mask], df[column_to_plot][mask], marker="o")

    x_labels = sorted(df["date"].unique())
    plt.ylabel(y_label)
    plt.xlabel("Date")
    plt.xticks(x_labels, rotation="vertical")
    plt.title(title)
    plt.xlim(x_labels[0], x_labels[-1])
    plt.ylim(
        bottom=0,
        top=100
        if df[column_to_plot].isnull().values.all()
        else df[column_to_plot].max() * 1.05,
    )

    if category:
        plt.legend(
            sorted(df[category].unique()), bbox_to_anchor=(1.04, 1), loc="upper left"
        )

    plt.tight_layout()

    plt.savefig(f"output/{filename}.png")
    plt.clf()


def convert_binary(df, binary_column, positive, negative):
    """Converts a column with binary variable codes as 0 and 1 to understandable strings.
    Args:
        df: dataframe with binary column
        binary_column: column name of binary variable
        positive: string to encode 1 as
        negative: string to encode 0 as
    Returns:
        Input dataframe with converted binary column
    """
    replace_dict = {0: negative, 1: positive}
    df[binary_column] = df[binary_column].replace(replace_dict)
    return df


def calculate_rate(df, value_col, rate_per=1000, round_rate=False):
    """Calculates the number of events per 1,000 of the population.
    This function operates on the given measure table in-place, adding
    a `rate` column.
    Args:
        df: A measure table.
        value_col: The name of the numerator column in the measure table.
        population_col: The name of the denominator column in the measure table.
        round: Bool indicating whether to round rate to 2dp.
    """
    if round_rate:
        rate = round(df[value_col] * rate_per, 2)

    else:
        rate = df[value_col] * rate_per

    return rate


def count_unique_practices(df):
    return len(np.unique(df["practice"]))


def drop_irrelevant_practices(df):
    """Drops irrelevant practices from the given measure table.
    An irrelevant practice has zero events during the study period.
    Args:
        df: A measure table.
    Returns:
        A copy of the given measure table with irrelevant practices dropped.
        A summary of the number of practices included
    """

    is_relevant = df.groupby("practice").value.any()
    df_relevant = df[df.practice.isin(is_relevant[is_relevant == True].index)]
    practice_summary = {
        "num_practices": count_unique_practices(df),
        "num_practices_included": count_unique_practices(df_relevant),
    }
    return df_relevant, practice_summary


def round_values(x, base=5):
    if not np.isnan(x):
        rounded = int(base * round(x / base))
    else:
        rounded = np.nan
    return rounded
