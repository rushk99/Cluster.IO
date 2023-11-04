import sys

sys.path.append("../")

from helpers import RemoveOutliers


def preprocess_data(data_df, x_df, y_df, remove_nulls=True, remove_outliers=False, outlier_method="Z-Score"):
    """

    :param data_df: The DataFrame which contains the raw data
    :param x_df: The DataFrame which contains the x values
    :param y_df: The DataFrame which contains the y values
    :param remove_nulls: A boolean of whether or not to remove nulls
    :param remove_outliers: A boolean of whether or not to remove outliers
    :param outlier_method: The method by which we are going to try to remove outliers

    :return: The preprocessed data DataFrame, the x values as a DataFrame, and the y values as a DataFrame

    Preprocess the data and return the results

    """
    print("Removing Outliers")
    if remove_nulls:
        data_df = RemoveOutliers.correct_nulls(data_df, x_df=x_df, y_df=y_df)
    if remove_outliers:
        data_df = RemoveOutliers.remove_data_from_outliers(data_df=data_df, x_df=x_df, y_df=y_df, method=outlier_method)
    print("Done Removing Outliers")
    return data_df, x_df, y_df
