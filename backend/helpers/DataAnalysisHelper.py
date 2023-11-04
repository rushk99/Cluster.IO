import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import pandas as pd
from helpers import StringDefinitionsHelper as sdh
import io
import base64

def perform_analysis(data_df, x_df, y_df, clustered_data, prop, show_contour_clustered=True, show_contour_raw=True,
                     show_bar=True, cluster_name="", cluster_iter=0, save_clustered_contour=False, save_dir="",
                     give_cluster_report=False, print_to_console=False, print_to_text_file=False, text_file_name="",
                     clusters_save_dir=sdh.CLUSTER_RESULTS_DIR, cluster_histogram_dir=sdh.FRACTION_HISTOGRAMS_DIR,
                     save_cluster_histograms=False, save_clustered_data=True, clustered_data_dir=sdh.DATA_FILES_DIR):
    """

    :param data_df: The original data we are clustering off of
    :param x_df: The x values of the dataset
    :param y_df: The y values of the dataset
    :param clustered_data: The clustered data from the original dataset
    :param prop: The property we are showing off, something like Hardness for example
    :param show_contour_clustered: A boolean of whether or not to show the contour plots
    :param show_contour_raw: A boolean of whether or not to show the contour plots
    :param show_bar: A boolean of whether or not to show the bar graphs
    :param cluster_name: The name of the cluster
    :param cluster_iter: The iteration of the cluster
    :param save_clustered_contour: A boolean of whether or not to save the clustered contour plot
    :param save_dir: The directory to save the figures to ######### Deprecated #########
    :param give_cluster_report: A boolean of whether or not to print out a report of the clusters' details
    :param print_to_console: A boolean of whether or not to print out information to the console
    :param print_to_text_file: A boolean of whether or not to print out information to a text file
    :param text_file_name: The file path to save the text file to
    :param clusters_save_dir: The directory to save the contour plots to
    :param cluster_histogram_dir: The directory to save the histograms which highlight cluster fractions to
    :param save_cluster_histograms: A boolean of whether or not to save the clustered data's histogram representation
    :param save_clustered_data: A boolean of whether or not to save the clustered data
    :param clustered_data_dir: The directory to store the clustered data inside of

    :return: Nothing at the moment

    Performs the data analysis associated with the given data and clustered results.

    """

    # TODO Check potential need to save data and transfer it over
    if show_contour_raw:
        plot_raw_data(data_df=data_df, x_df=x_df, y_df=y_df, prop=prop)

    if show_contour_clustered or save_clustered_contour:
        plot_clustered_data(x_df=x_df, y_df=y_df, clustered_data=clustered_data, prop=prop, cluster_name=cluster_name,
                            cluster_iter=cluster_iter, save_clustered_contour=save_clustered_contour, save_dir=save_dir,
                            show_contour_clustered=show_contour_clustered, clusters_save_dir=clusters_save_dir)

    if show_bar or save_cluster_histograms:
        plot_clusters_fractions(cluster_results=clustered_data, prop=prop, show_bar=show_bar,
                                save_cluster_histograms=save_cluster_histograms,
                                cluster_histogram_dir=cluster_histogram_dir, cluster_name=cluster_name,
                                cluster_iter=cluster_iter)

    if give_cluster_report:
        print_cluster_details(data_df=data_df, clustered_data_df=clustered_data, cluster_name=cluster_name,
                              print_to_console=print_to_console, print_to_text_file=print_to_text_file,
                              text_file_name=text_file_name)

    if save_clustered_data:
        save_data(data_df=data_df,x_df=x_df, y_df=y_df,clustered_data=clustered_data,prop=prop, clustered_data_dir=clustered_data_dir, cluster_name=cluster_name,
                  cluster_iteration=cluster_iter)

    # TODO I'm not entirely sure how this is sent to frontend, I imagine we need to save it, look into this

    return


def plot_raw_data(data_df, x_df, y_df, prop):
    """

    :param data_df: The DataFrame of data we are clustering
    :param x_df: The x values of the data
    :param y_df: The y values of the data
    :param prop: The property we are actually clustering
    :return: Nothing at the moment

    Plots the raw data we read in as a contour plot
    """

    # Define variables
    x_values = np.unique(x_df["Data"].values)
    y_values = np.unique(y_df["Data"].values)
    grid_size_x = int(x_values.size)
    grid_size_y = int(y_values.size)

    # Set the number of clusters and limit it to 20
    num_clusters = len(np.unique(data_df))
    if num_clusters > 20:
        num_clusters = 20

    if "Data" in data_df.columns:
        z_values = np.rot90(data_df["Data"].values.reshape(grid_size_x, grid_size_y))

        fig, ax = plt.subplots(figsize=(6, 6))

        ax.set_aspect('equal')
        # Plots contour plot
        cf = ax.contourf(x_values, y_values, z_values, num_clusters - 1)

        cb = fig.colorbar(cf, ax=ax)
        # Labels being set
        cb.set_label("Raw " + str(prop) + " Values (GPA)")
        plt.title(str(prop) + " Raw Data VS Coordinate")
        plt.xlabel("X Values (um)")
        plt.ylabel("Y Values (um)")
        plt.savefig('../temp_image/raw_data.png')
        #plt.show()
        plt.close()
        return
    else:
        z_values1 = np.rot90(data_df["Hardness"].values.reshape(grid_size_x, grid_size_y))
        z_values2 = np.rot90(data_df["Modulus"].values.reshape(grid_size_x, grid_size_y))



        # Create a figure and axis object
        fig, ax = plt.subplots(figsize=(6, 6))

        # Set the aspect ratio of the plot
        ax.set_aspect('equal')

        # Plot the contour plot for the first value (Hardness)
        cf1 = ax.contourf(x_values, y_values, z_values1, num_clusters - 1)

        # Add a colorbar to the plot
        cb1 = fig.colorbar(cf1, ax=ax)
        cb1.set_label("Raw Hardness Values (GPA)")

        # Plot the contour plot for the second value (Modulus)
        cf2 = ax.contourf(x_values, y_values, z_values2, num_clusters - 1)

        # Add a colorbar to the plot
        cb2 = fig.colorbar(cf2, ax=ax)
        cb2.set_label("Raw Modulus Values (GPA)")

        # Set the title and axis labels for the plot
        plt.title("Hardness and Modulus Raw Data VS Coordinate")
        plt.xlabel("X Values (um)")
        plt.ylabel("Y Values (um)")

        # Save the plot to a file and display it
        plt.savefig('../temp_image/raw_data.png')
        #plt.show()
        plt.close()
        return



def plot_clustered_data(x_df, y_df, clustered_data, prop, cluster_name, cluster_iter, save_clustered_contour, save_dir,
                        show_contour_clustered=False, clusters_save_dir=sdh.CLUSTER_RESULTS_DIR):
    """

    :param x_df: The x values of the data
    :param y_df: The y values of the data
    :param clustered_data: The clustered result of the data
    :param prop: The property we are clustering on
    :param cluster_name: The name of the cluster
    :param cluster_iter: The iteration of the cluster
    :param save_clustered_contour: A boolean of whether or not to save the clustered contour plot
    :param save_dir: The directory to save the figures to ####### DEPRECATED ######
    :param show_contour_clustered: Whether or not to show the contour plot
    :param clusters_save_dir: The directory to save the contour plots to
    :return: Nothing at the moment

    """
    
    num_clusters = len(np.unique(clustered_data))
    if num_clusters > 20:
        num_clusters = 20
    x_values = np.unique(x_df["Data"].values)
    y_values = np.unique(y_df["Data"].values)
    grid_size_x = int(x_values.size)
    grid_size_y = int(y_values.size)
    z_values = np.rot90(clustered_data["Data"].values.reshape(grid_size_x, grid_size_y))

    fig, ax = plt.subplots(figsize=(6, 6))

    ax.set_aspect('equal')
    # Plots contour plot
    cf = ax.contourf(x_values, y_values, z_values, num_clusters - 1)
    # TODO I would like to figure out how to make the contour plot's color bar only have integers next to it
    # TODO An alternative to the thing above is to remove the numbers entirely, decimals make it confusing in my opinion
    # Plots color bar
    cb = fig.colorbar(cf, ax=ax)
    # Labels being set
    cb.set_label("Phase")
    plt.title(str(prop) + " Clustered VS X, Y" )
    plt.xlabel("X Values (um)")
    plt.ylabel("Y Values (um)")

    if save_clustered_contour:
        plt.savefig(clusters_save_dir + "/clustered_data_" + str(cluster_iter) + "_" + str(cluster_name))

    # Whether or not to show the contour plot
    if show_contour_clustered:
        plt.savefig('../temp_image/clustered_data.png')
        #plt.show()
        plt.close()
    else:
        # Necessary or EVERYTHING goes to one plot... this produces very bad things
        plt.close()

    return


def plot_clusters_fractions(cluster_results, prop, show_bar=False, save_cluster_histograms=False,
                            cluster_histogram_dir="", cluster_name="", cluster_iter=0):
    """

    :param cluster_results: The results of a clustering algorithm, storing the clustered data inside of a
        DataFrame
    :param prop: The property we are clustering
    :param show_bar: A boolean of whether to show the bar graph or not
    :param save_cluster_histograms: A boolean of whether to save the bar graph or not
    :param cluster_histogram_dir: A directory to save the file to if we are saving it
    :param cluster_name: The name of the clustering configuration we are using
    :param cluster_iter: The iteration of the clustering configuration we are using

    :return: Nothing

    Plots the fraction of data inside of each cluster in the cluster_results DataFrame

    """

    res_list = cluster_results["Data"].tolist()
    cluster_fractions = []
    cluster_num = []
    unique_cluster_values = np.unique(cluster_results)
    for i in unique_cluster_values:
        fraction = float(res_list.count(i)) / float(len(res_list))
        cluster_fractions.append(fraction)
        cluster_num.append(i + 1)
    plt.bar(cluster_num, height=cluster_fractions, width=0.4)

    # TODO I would like to revisit how we are making this bar graph, I don't like the width being a set amount
    # TODO I would also like to see if it is possible to make the bar graph only use integer values for it's x values

    plt.title("Distribution of " + str(prop) + " Data After Clustering into " + str(len(cluster_num)) + " Clusters")
    plt.xlabel("Cluster (" + str(len(cluster_num)) + " Clusters)")
    plt.ylabel("Percentage of Data Contained Within Cluster")

    if save_cluster_histograms:
        plt.savefig(cluster_histogram_dir + "/clustered_data_" + str(cluster_iter) + "_" + str(cluster_name))
        # print(
        #     "----------------------------------------------------------------------------------------------------------------------------------------------------------")

    if show_bar:
        plt.savefig('../temp_image/clusters_fractions.png')
        #plt.show()
        plt.close()
    else:
        plt.close()


def print_cluster_details(data_df, clustered_data_df, cluster_name, print_to_console=False, print_to_text_file=False,
                          text_file_name=""):
    """

    :param data_df: A DataFrame representation of all of the raw data we are reading
    :param clustered_data_df: A DataFrame representation of all of the clustered data we are reading
    :param cluster_name: The name of the clustering configuration we are running
    :param print_to_console: A boolean of whether or not to print out information to the console
    :param print_to_text_file: A boolean of whether or not to print out information to a text file
    :param text_file_name: The file path to save the text file to

    :return: Nothing

    Print the mean, fractions, and standard deviations of each cluster
    Mean - Mean value of all elements in a cluster
    Standard Deviation - Standard deviation of all elements in a cluster
    Fraction - The fraction of the whole data set which is in this cluster

    """

    # Combine the data for filtering
    all_data_values = pd.DataFrame()
    all_data_values["Data"] = data_df["Data"].values
    all_data_values["Cluster"] = clustered_data_df["Data"].values

    # Find the unique clusters that exist and the size of the data
    unique_values = np.unique(all_data_values["Cluster"].values)
    num_clusters = len(unique_values)
    data_size = len(all_data_values["Data"].values)

    if print_to_console or print_to_console:
        if print_to_console:
            print("\nCluster Details for " + str(cluster_name) + ": ")
        if print_to_text_file:
            f = open(text_file_name, "a")
            print("\nCluster Details for " + str(cluster_name) + ": ", file=f)

        # For every cluster, return the details
        for i in range(num_clusters):
            cluster = unique_values[i]
            data_set = all_data_values[all_data_values["Cluster"] == cluster]
            cluster_data = data_set["Data"].values
            cluster_mean = np.mean(cluster_data)
            cluster_stddev = np.std(cluster_data)
            cluster_fraction = len(cluster_data) / data_size
            cluster_min = min(cluster_data)
            cluster_max = max(cluster_data)
            # If we are printing it to the text file then print to the text file
            if print_to_text_file:
                print("\tCluster " + str(cluster) + " Details: ", file=f)
                print("\t\tCluster Mean: " + str(cluster_mean), file=f)
                print("\t\tCluster Standard Deviation: " + str(cluster_stddev), file=f)
                print("\t\tCluster Fraction: " + str(cluster_fraction), file=f)
                print("\t\tCluster Min: " + str(cluster_min), file=f)
                print("\t\tCluster Max: " + str(cluster_max), file=f)
            # If we are printing it to the console then print it to the console
            if print_to_console:
                print("\tCluster " + str(cluster) + " Details: ")
                print("\t\tCluster Mean: " + str(cluster_mean))
                print("\t\tCluster Standard Deviation: " + str(cluster_stddev))
                print("\t\tCluster Fraction: " + str(cluster_fraction))
                print("\t\tCluster Min: " + str(cluster_min))
                print("\t\tCluster Max: " + str(cluster_max))
        if print_to_text_file:
            f.close()


def save_data(data_df,x_df, y_df,clustered_data, clustered_data_dir,prop, cluster_name="", cluster_iteration=0):
    """

    :param clustered_data: The clustered data DataFrame we are saving
    :param clustered_data_dir: The directory we are saving the clustered data to
    :param cluster_name: The name of the clustering configuration we are running
    :param cluster_iteration: The iteration of the current clustering configuration
    :return: Nothing

    A helper method that is used for saving the data to a certain directory in a .xlsx file

    """

    #file_path = clustered_data_dir + "/ClusteredData_" + cluster_name + "_" + str(cluster_iteration) + ".xlsx"
    file_path = clustered_data_dir + "/ClusteredData" +".xlsx"
    x_df=x_df.round(2)
    y_df=y_df.round(2)
    data_df=data_df.round(2)
    if "Data" in data_df.columns:
        df_concat = pd.concat([x_df['Data'], y_df['Data'],data_df['Data'], clustered_data['Data']], axis=1)
        df_concat.columns = ['x', 'y',"label", 'cluster']
        df_concat = df_concat.drop(df_concat.index[-2:], axis=0)
        df_concat.to_excel(file_path, float_format="%.2f")
    else:
        df_concat = pd.concat([x_df['Data'], y_df['Data'], data_df[['Hardness', 'Modulus']].astype(str).agg(','.join, axis=1), clustered_data['Data']], axis=1)
        df_concat.columns = ['x', 'y', 'label', 'cluster']
        df_concat = df_concat.iloc[:-2] # remove last two rows
        df_concat.to_excel(file_path, float_format="%.2f")
        

