import numpy as np
import matplotlib.pyplot as plt

"""
The purpose of this class is to provide helper methods that involve making plots that are involved in the process
of plotting contour plots for hardness or modulus values. This involving directly plotting the contour plots or
plotting bar graphs involving other data.
"""


def plot_base_data(x_df, y_df, data_df, prop):
    """

    :param x_df: A DataFrame containing the x values used by the contour plot
    :param y_df: A DataFrame containing the y values used by the contour plot
    :param data_df: A DataFrame containing the data values used by the contour plot
    :param prop: The label of the property we will be making this plot for

    :return: Nothing

    Plots the contour plot in the format of it being the original data gathered from an excel file.

    """
    # Setting up variables to use for contour plot
    x_values = np.unique(x_df["Data"].values)
    y_values = np.unique(y_df["Data"].values)
    grid_size_x = int(x_values.size)
    grid_size_y = int(x_values.size)
    z_values = np.rot90(data_df["Data"].values.reshape(grid_size_x, grid_size_y))

    fig, ax = plt.subplots(figsize=(6, 6))

    ax.set_aspect('equal')
    # Plots contour plot
    cf = ax.contourf(x_values, y_values, z_values)
    # Plots color bar
    cb = fig.colorbar(cf, ax=ax)
    # Labels being set
    cb.set_label("Raw " + str(prop) + " Values (GPA)")
    plt.title(str(prop) + " Raw Data VS Coordinate")
    plt.xlabel("X Values (um)")
    plt.ylabel("Y Values (um)")

    plt.show()

    return


def plot_final_decon_data(x_df, y_df, decon_results_df, prop, curr_m):
    """

    :param x_df: A DataFrame containing the x values used by the contour plot
    :param y_df: A DataFrame containing the y values used by the contour plot
    :param decon_results_df: The results of the decon algorithm
    :param prop: The label of the property we will be making this plot for
    :param curr_m: The current number of phases in the decon method

    :return: Nothing

    Plots the contour plot based on the results of the deconvolution algorithm

    """

    x_values = np.unique(x_df["Data"].values)
    y_values = np.unique(y_df["Data"].values)
    grid_size = int(x_values.size)
    # Uses decon results instead of hardness values
    z_values = np.rot90(decon_results_df["Data"].values.reshape(grid_size, grid_size))

    fig, ax = plt.subplots(figsize=(6, 6))

    ax.set_aspect('equal')
    # Creates the contour plot with curr_m - 1 different categories
    cf = ax.contourf(x_values, y_values, z_values, curr_m - 1)
    cb = fig.colorbar(cf, ax=ax)
    cb.set_label("Deconvolution Phase")
    plt.title("Deconvolution Phase For " + prop + " Vs Coordinate")
    plt.xlabel("X Values (um)")
    plt.ylabel("Y Values (um)")

    plt.show()

    return


def plot_f(dh, prop, method="in each K Means Cluster"):
    """

    :param dh: The deconvolution helper used for analysis
    :param prop: The property that we will use as a label
    :param method: What method is being used

    :return: Nothing

    Plots the fractions of data points that land in each decon phase

    """

    # Bar plot for the fraction of items in each cluster
    plt.bar(dh.minprumer, height=dh.minf, width=0.4)
    plt.title("Fractions of Data " + method)
    plt.xlabel("K Means Cluster Means Value (" + str(prop) + " in GPA)")
    plt.ylabel("Fraction")
    plt.show()

    return


def plot_final_k_means_data(x_df, y_df, k_means_results_df, prop, num_clusters):
    """

    :param x_df: A DataFrame containing the x values used by the contour plot
    :param y_df: A DataFrame containing the y values used by the contour plot
    :param k_means_results_df: A DataFrame containing hte results of the K-Means Clustering algorithm
    :param prop: The label of the property we will be making this plot for
    :param num_clusters: The number of clusters in the K-Means Clustering algorithm

    :return: Nothing

    Plots a contour plot of the results of the K-Means Clustering algorithm

    """

    # Creating variables to use for the contour plot
    x_values = np.unique(x_df["Data"].values)
    y_values = np.unique(y_df["Data"].values)
    grid_size = int(x_values.size)
    z_values = np.rot90(k_means_results_df["Data"].values.reshape(grid_size, grid_size))

    fig, ax = plt.subplots(figsize=(6, 6))

    ax.set_aspect('equal')
    # Contour plot with num_clusters number of colors
    cf = ax.contourf(x_values, y_values, z_values, num_clusters - 1)
    # Color bar
    cb = fig.colorbar(cf, ax=ax)
    # Plot labels
    cb.set_label("Cluster (Integer)")
    plt.title("K Means Cluster for " + str(prop) + " VS Coordinate")
    plt.xlabel("X Values (um)")
    plt.ylabel("Y Values (um)")

    plt.show()

    return


def plot_k_means_frac(cluster_means_arr, cluster_fractions, prop):
    """

    :param cluster_means_arr: The means of the clusters
    :param cluster_fractions: The fraction of data in each cluster
    :param prop: The label to use in the plot's labels

    :return: Nothing

    Plots the fraction of data that lands in each cluster as a bar graph

    """

    # Bar plot for the fraction of items in each cluster
    plt.bar(cluster_means_arr, height=cluster_fractions, width=0.4)
    plt.title("Fractions of Data in each K Means Cluster")
    plt.xlabel("K Means Cluster Means Value (" + str(prop) + " in GPA)")
    plt.ylabel("Fraction")
    plt.show()

    return
