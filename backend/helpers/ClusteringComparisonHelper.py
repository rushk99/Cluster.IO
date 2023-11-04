import sys

sys.path.append("../")

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def rand_index_visualization(x_df, y_df, clustered_df1, clustered_df2, save_plot, save_path, show_plot=False,
                             cluster1_name="", cluster2_name="", cluster1_iter=0, cluster2_iter=0):
    """

    :param x_df: The x values of the dataset
    :param y_df: The y values of the dataset
    :param clustered_df1: The clustered data from the original dataset using the first method
    :param clustered_df2: The clustered data from the original dataset using the second method
    :param save_plot: A boolean of whether or not to save the plot
    :param save_path: The path to save the plots at
    :param show_plot: A boolean of whether or not to show the plot
    :param cluster1_name: The name of the first clustering configuration
    :param cluster2_name: The name of the second clustering configuration
    :param cluster1_iter: The iteration of the first clustering configuration
    :param cluster2_iter: The iteration of the second clustering configuration

    :return: Nothing

    Plots a visual representation of the rand index metric. It checks for all the locations where two clustering
    methods gather the same and different cluster values for individual data points, plotting the similarities and
    differences.

    """

    # Check to ensure that the same clusters are being compared
    data_values_1 = clustered_df1["Data"]
    data_values_2 = clustered_df2["Data"]

    data_values_1 = np.unique(data_values_1)
    data_values_2 = np.unique(data_values_2)

    if len(data_values_1) == len(data_values_2):
        two_clusters1 = pd.DataFrame()
        two_clusters1["Cluster1"], two_clusters1["Cluster2"] = transform_to_same_range(clustered_df1=clustered_df1,
                                                                                       clustered_df2=clustered_df2)

        two_clusters1["Data"] = np.where((two_clusters1["Cluster1"] == two_clusters1["Cluster2"]), 1, 0)

        x_values = np.unique(x_df["Data"].values)
        y_values = np.unique(y_df["Data"].values)
        grid_size_x = int(x_values.size)
        grid_size_y = int(y_values.size)
        z_values = np.rot90(two_clusters1["Data"].values.reshape(grid_size_x, grid_size_y))

        fig, ax = plt.subplots(figsize=(6, 6))

        ax.set_aspect('equal')
        # Plots contour plot
        cf = ax.contourf(x_values, y_values, z_values, cmap="winter", levels=[-0.5, 0.5, 1.5])
        # Plots color bar
        cb = fig.colorbar(cf, ax=ax)
        # Labels being set
        cb.set_label("0: Different, 1: Same")
        plt.suptitle(str(cluster1_name) + " iter " + str(cluster1_iter)
                     + " vs " + cluster2_name + " iter " + str(cluster2_iter))
        plt.title("Rand Index Visualization")
        plt.xlabel("X Values (um)")
        plt.ylabel("Y Values (um)")

        if save_plot:
            plt.savefig(save_path)

        if show_plot:
            plt.show()
        else:
            plt.close()


def transform_to_same_range(clustered_df1, clustered_df2):
    """

    :param clustered_df1: The first DataFrame of clustered data
    :param clustered_df2: The second DataFrame of clustered data

    :return: Two lists of data from the DataFrames that are corrected

    Ensures that the min and max values of the two DataFrames are the same. To get to this point, they
    are already of the same size so we can just apply a transformation which adds a constant equal to
    the difference in their min values.

    """

    min_val1 = min(clustered_df1["Data"])
    min_val2 = min(clustered_df2["Data"])
    clustered_df1_copy = clustered_df1.copy()
    if min_val1 != min_val2:
        clustered_df1_copy["Data"] = clustered_df1_copy["Data"] + min_val2 - min_val1
    return clustered_df1_copy["Data"].values, clustered_df2["Data"].values
