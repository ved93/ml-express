import pandas_profiling


import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import warnings
from scipy import stats
from scipy.stats import norm

import os


warnings.filterwarnings("ignore")

def create_summary_report(df,name = None):
    # Data profiling/EDA
    profile = pandas_profiling.ProfileReport(
        df, title="Data Audit Report \nAuthor: {}".format(name)
    )

    if not os.path.exists('./reports/data_audit_report.html'):
        os.makedirs('reports')


    profile.to_file(output_file="./reports/data_audit_report.html")

def check_missing_data(df):
    flag=df.isna().sum().any()
    if flag==True:
        total = df.isnull().sum()
        percent = (df.isnull().sum()*100)/(df.isnull().count())
        output = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
        data_type = []
        # written by Ved
        for col in df.columns:
            dtype = str(df[col].dtype)
            data_type.append(dtype)
        output['Types'] = data_type
        return(np.transpose(output))
    else:
        return(False)


def reduce_mem_usage(df, verbose=True):
    numerics = ["int16", "int32", "int64", "float16", "float32", "float64"]
    start_mem = df.memory_usage(deep=True).sum() / 1024 ** 2
    for col in df.columns:
        col_type = df[col].dtypes
        if col_type in numerics:
            c_min = df[col].min()
            c_max = df[col].max()
            if str(col_type)[:3] == "int":
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)
            else:
                if (
                    c_min > np.finfo(np.float16).min
                    and c_max < np.finfo(np.float16).max
                ):
                    df[col] = df[col].astype(np.float16)
                elif (
                    c_min > np.finfo(np.float32).min
                    and c_max < np.finfo(np.float32).max
                ):
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)
    end_mem = df.memory_usage(deep=True).sum() / 1024 ** 2
    if verbose:
        print(
            "Mem. usage decreased to {:5.2f} Mb ({:.1f}% reduction)".format(
                end_mem, 100 * (start_mem - end_mem) / start_mem
            )
        )
    return df


def gen_eda(data_frame):

    print("##########----------##########")
    print(f"Dataset has {data_frame.shape[0]} rows and {data_frame.shape[1]} columns.")

    print("##########----------##########")
    print(
        f"There are {data_frame.isnull().any().sum()} columns in the dataset with missing values."
    )

    print("##########----------##########")
    one_value_cols = [
        col for col in data_frame.columns if data_frame[col].nunique() <= 1
    ]
    print(
        f"There are {len(one_value_cols)} columns in the dataset with one unique value."
    )

    print("##########----------##########")
    dtype_df = data_frame.dtypes.reset_index()
    dtype_df.columns = ["Count", "Column Type"]
    print(dtype_df)

    print("##########----------##########")
    df1 = dtype_df.groupby("Column Type").aggregate("count").reset_index()
    print(df1)

    print("##########----------##########")
    # Number of unique classes in each object column
    df2 = data_frame.select_dtypes("object").apply(pd.Series.nunique, axis=0)
    print(df2)


def general_stats(data_frame):
    stats = []
    for col in data_frame.columns:
        stats.append(
            (
                col,
                data_frame[col].nunique(),
                data_frame[col].isnull().sum() * 100 / data_frame.shape[0],
                data_frame[col].value_counts(normalize=True, dropna=False).values[0]
                * 100,
                data_frame[col].dtype,
            )
        )

    stats_df = pd.DataFrame(
        stats,
        columns=[
            "Feature",
            "Unique_values",
            "Percentage of missing values",
            "Percentage of values in the biggest category",
            "type",
        ],
    )
    stats_df.sort_values("Percentage of missing values", ascending=False)
    print(stats_df)


def find_correlations(data_frame, dependent):
    # Find correlations with the target and sort
    correlations = data_frame.corr()[dependent].sort_values()

    # Display correlations
    print("Most Positive Correlations:\n", correlations.tail(15))
    print("\nMost Negative Correlations:\n", correlations.head(15))


def missing_values_table(df):
    # Total missing values
    mis_val = df.isnull().sum()

    # Percentage of missing values
    mis_val_percent = 100 * df.isnull().sum() / len(df)

    # Make a table with the results
    mis_val_table = pd.concat([mis_val, mis_val_percent], axis=1)

    # Rename the columns
    mis_val_table_ren_columns = mis_val_table.rename(
        columns={0: "Missing Values", 1: "% of Total Values"}
    )

    # Sort the table by percentage of missing descending
    mis_val_table_ren_columns = (
        mis_val_table_ren_columns[mis_val_table_ren_columns.iloc[:, 1] != 0]
        .sort_values("% of Total Values", ascending=False)
        .round(1)
    )

    # Print some summary information
    print(
        "Your selected dataframe has " + str(df.shape[1]) + " columns.\n"
        "There are "
        + str(mis_val_table_ren_columns.shape[0])
        + " columns that have missing values."
    )

    # Return the dataframe with missing information
    return mis_val_table_ren_columns


def print_quantiles(data_frame, column):
    data_frame[column] = data_frame[column].astype(float)
    print(f"{column} Quantiles:")
    print(
        data_frame[column].quantile(
            [0.0, 0.01, 0.025, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.975, 0.99, 1.0]
        )
    )


def time_series_plot(df):
    """Given dataframe, generate times series plot of numeric data by daily, monthly and yearly frequency"""
    print(
        "\nTo check time  series of numeric data  by daily, monthly and yearly frequency"
    )
    if len(df.select_dtypes(include="datetime64").columns) > 0:
        for col in df.select_dtypes(include="datetime64").columns:
            for p in ["D", "M", "Y"]:
                if p == "D":
                    print("Plotting daily data")
                elif p == "M":
                    print("Plotting monthly data")
                else:
                    print("Plotting yearly data")
                for col_num in df.select_dtypes(include=np.number).columns:
                    __ = df.copy()
                    __ = __.set_index(col)
                    __T = __.resample(p).sum()
                    ax = __T[[col_num]].plot()
                    ax.set_ylim(bottom=0)
                    ax.get_yaxis().set_major_formatter(
                        matplotlib.ticker.FuncFormatter(
                            lambda x, p: format(int(x), ",")
                        )
                    )
                    plt.show()


def numeric_eda(df, hue=None):
    """Given dataframe, generate EDA of numeric data"""
    print("\nTo check: \nDistribution of numeric data")
    pd.display(df.describe().T)
    columns = df.select_dtypes(include=np.number).columns
    figure = plt.figure(figsize=(20, 10))
    figure.add_subplot(1, len(columns), 1)
    for index, col in enumerate(columns):
        if index > 0:
            figure.add_subplot(1, len(columns), index + 1)
        sns.boxplot(y=col, data=df, boxprops={"facecolor": "None"})
    figure.tight_layout()
    plt.show()

    if len(df.select_dtypes(include="category").columns) > 0:
        for col_num in df.select_dtypes(include=np.number).columns:
            for col in df.select_dtypes(include="category").columns:
                fig = sns.catplot(
                    x=col, y=col_num, kind="violin", data=df, height=5, aspect=2
                )
                fig.set_xticklabels(rotation=90)
                plt.show()

    # Plot the pairwise joint distributions
    print("\nTo check pairwise joint distribution of numeric data")
    if hue == None:
        sns.pairplot(df.select_dtypes(include=np.number))
    else:
        sns.pairplot(df.select_dtypes(include=np.number).join(df[[hue]]), hue=hue)
    plt.show()


def top5(df):
    """Given dataframe, generate top 5 unique values for non-numeric data"""
    columns = df.select_dtypes(include=["object", "category"]).columns
    for col in columns:
        print("Top 5 unique values of " + col)
        print(
            df[col]
            .value_counts()
            .reset_index()
            .rename(columns={"index": col, col: "Count"})[
                : min(5, len(df[col].value_counts()))
            ]
        )
        print(" ")


def categorical_eda(df, hue=None):
    """Given dataframe, generate EDA of categorical data"""
    print("\nTo check: \nUnique count of non-numeric data\n")
    print(df.select_dtypes(include=["object", "category"]).nunique())
    top5(df)
    # Plot count distribution of categorical data
    for col in df.select_dtypes(include="category").columns:
        fig = sns.catplot(x=col, kind="count", data=df, hue=hue)
        fig.set_xticklabels(rotation=90)
        plt.show()


if __name__ == "__main__":
    df = pd.read_csv("../input/train_house_price.csv")
    # gen_eda(df)
    # general_stats(df)
    # find_correlations(df, 'SalePrice')
    missing_values_table(df)
