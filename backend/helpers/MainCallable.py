import sys

sys.path.append("../")

from helpers import ClusteringHelper, DataAnalysisHelper, DataCollectionHelper, PreProcessingHelper, \
    StringDefinitionsHelper
from server_files.store import queues
import asyncio

WAIT_TIME = 0.001

COLUMN_DEFAULT = StringDefinitionsHelper.HARDNESS_LABEL


async def execute(clustering_method, clustering_details, file_name, file_format,
                  clustered_column=COLUMN_DEFAULT, caller_id=None,
                  show_contour_clustered=True, show_contour_raw=True, show_bar=True, remove_outliers=False):
    """

    :param clustering_method: The clustering method we are using, see StringDefinitionsHelper for options
    :param clustering_details: The details associated with the clustering method we are using, see
        StringDefinitionsHelper
    :param file_name: The name of the file we are reading in relative to the folder of the executable
    :param file_format: The format of the file we are reading in, see StringDefinitionsHelper for options
    :param clustered_column: The name of the type of column we are clustering, default value of Hardness
    :param caller_id: # TODO Eric describe this
    :param show_contour_clustered: A boolean of whether or not to show the final clustered data's contour plot
    :param show_contour_raw: A boolean of whether or not to show the raw data's contour plot
    :param show_bar: A boolean of whether or not to show the bar graph
    :param remove_outliers: A boolean of whether or not to remove outliers
    :return: Nothing at the moment

    Reads in all of the data and performs the necessary clustering. It performs the following steps: Reading in the
    data, preprocessing the data, clustering the data, an then analyzing the data. The the respective helper classes
    for more details as to how the processes work.

    """

    # Print Out Report
    print("\n")
    print("Clustering Method: " + str(clustering_method))
    print("\tClustering Details: ")
    for cluster_param in clustering_details:
        print("\t\t" + str(cluster_param) + ": " + str(clustering_details[cluster_param]))
    print("\tFile Name: " + str(file_name))
    print("\tFile Format: " + str(file_format))
    print("\tClustering Column: " + str(clustered_column))
    print("\tShow Raw Data: " + str(show_contour_raw))
    print("\tShow Clustered Contour Plot: " + str(show_contour_clustered))
    print("\tShow Bar Graph: " + str(show_bar))
    print("\tRemove Outliers: " + str(remove_outliers))
    print("\n")

    # TODO Specify different parameters to be used, clustering details need dictionary
    # TODO Fix project name in auto docs and readme
    # Read in data
    for queue in queues:
        await queue.put("READING")
    await asyncio.sleep(WAIT_TIME)
    print("Reading Data...")
    data_df, x_df, y_df = DataCollectionHelper.get_data(file_name, file_format, clustered_column)
    print("Done Reading Data")
    # Pre process the data
    for queue in queues:
        await queue.put("PREPROCESSING")
    await asyncio.sleep(WAIT_TIME)
    print("PreProcessing Data... ")
    data_df, x_df, y_df = PreProcessingHelper.preprocess_data(data_df=data_df, x_df=x_df, y_df=y_df,remove_outliers=remove_outliers)
    print("Done PreProcessing Data")
    # Cluster the data
    for queue in queues:
        await queue.put("CLUSTERING")
    await asyncio.sleep(WAIT_TIME)
    print("Clustering Data... ")
    clustered_data = ClusteringHelper.perform_clustering(data_df=data_df,
                                                         clustering_method=clustering_method,
                                                         clustering_details=clustering_details,
                                                         label=clustered_column)
    print("Done Clustering Data")
    # Provide Analysis
    for queue in queues:
        await queue.put("ANALYZING")
    await asyncio.sleep(WAIT_TIME)
    print("Analyzing Data... ")
    DataAnalysisHelper.perform_analysis(data_df=data_df, x_df=x_df, y_df=y_df, clustered_data=clustered_data,
                                        prop=clustered_column, show_contour_clustered=show_contour_clustered,
                                        show_contour_raw=show_contour_raw, show_bar=show_bar)
    print("Done Analyzing Data")
    for queue in queues:
        await queue.put("COMPLETE")
        print(queue)
    print("Process complete")
    return
