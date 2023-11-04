import sys

sys.path.append("../")

from helpers import ClusteringHelper as ch, ClusteringComparisonHelper as cch, DataAnalysisHelper as dah, \
    DataCollectionHelper as dch, DirectoryManagerHelper as dmh, PreProcessingHelper as pph, \
    StringDefinitionsHelper as sdh, CHI, DBI, SilhouetteCoefficient
from server_files.store import queues
from sklearn.metrics import adjusted_rand_score
import asyncio
from queue import PriorityQueue
import numpy as np
import time
from datetime import datetime

WAIT_TIME = 0.001

COLUMN_DEFAULT = sdh.HARDNESS_LABEL


async def execute(clustering_methods_list, clustering_details_list, cluster_names_list,
                  file_name, file_format, clustered_column=COLUMN_DEFAULT, caller_id=None,
                  show_contour_clustered=True, show_contour_raw=True, show_bar=True, remove_outliers=False,
                  save_contour_clustered=False, give_cluster_report=False, print_to_console=False,
                  print_to_text_file=False, text_report_name="RunReport.txt",
                  clusters_save_dir=sdh.CLUSTER_RESULTS_DIR,
                  rand_index_save_dir=sdh.RAND_INDEX_VISUALIZATION_DIR,
                  text_files_save_dir=sdh.TEXT_FILE_DIR,
                  data_save_dir=sdh.DATA_FILES_DIR,
                  cluster_fraction_save_dir=sdh.FRACTION_HISTOGRAMS_DIR,
                  save_rand_index_visualizations=False, additional_outlier_clusters=False, show_rand_index_plots=False,
                  save_cluster_histograms=False, decon_dir=sdh.DECONVOLUTION_SAVE_DIR,
                  save_clustered_data=False):
    """

    :param clustering_methods_list: The clustering methods we are using for our clustering,
        see StringDefinitionsHelper for options
    :param clustering_details_list: The details associated with the clustering methods we are using for our
        clustering methods, see StringDefinitionsHelper.py and ClusteringHelper.py for details
    :param cluster_names_list: How to identify the clusters for print reports
    :param file_name: The name of the file we are reading in relative to the folder of the executable
    :param file_format: The format of the file we are reading in, see StringDefinitionsHelper for options
    :param clustered_column: The name of the type of column we are clustering, default value of Hardness
    :param caller_id: #TODO Eric describe this
    :param show_contour_clustered: A boolean of whether or not to show the final clustered data's contour plot
    :param show_contour_raw: A boolean of whether or not to show the raw data's contour plot
    :param show_bar: A boolean of whether or not to show the bar graph
    :param remove_outliers: A boolean of whether or not to remove outliers
    :param save_contour_clustered: A boolean of whether or not save the clustered contour plot
    :param give_cluster_report: A boolean of whether or not to print out a report of the clusters' details
    :param print_to_console: A boolean of whether or not to print out information to the console
    :param print_to_text_file: A boolean of whether or not to print out information to a text file
    :param text_report_name: The file path to save the text file to
    :param clusters_save_dir: The directory to save the clustered figures to
    :param rand_index_save_dir: The directory to save the rand index visualization figures to
    :param text_files_save_dir: The directory to save the text files to
    :param data_save_dir: The directory to save the data files to
    :param cluster_fraction_save_dir: The directory to save the histograms which highlight cluster fractions to
    :param save_rand_index_visualizations: A boolean of whether or not to save the rand index visualization
    :param additional_outlier_clusters: A boolean of whether to place any outliers into separate clusters
    :param show_rand_index_plots: A boolean of whether to show the rand index visualization plots or not
    :param save_cluster_histograms: A boolean of whether or not to save the cluster fraction histograms
    :param decon_dir: The directory to save the deconvolution plots in
    :param save_clustered_data: A boolean of whether or not to save the clustered data

    :return: Nothing at the moment

    Reads in all of the data and performs the necessary clustering. It performs the following steps: Reading in the
    data, preprocessing the data, clustering the data, an then analyzing the data. The the respective helper classes
    for more details as to how the processes work.

    """

    assert len(clustering_methods_list) == len(clustering_details_list) == len(cluster_names_list)

    # Variables we use for keeping track of time
    start_time = time.time()
    prev_time = time.time()

    # Set up the necessary directories
    save_dir_path = dmh.create_necessary_directories(cluster_results_dir=clusters_save_dir,
                                                     rand_index_visualization_dir=rand_index_save_dir,
                                                     text_file_dir=text_files_save_dir,
                                                     data_files_dir=data_save_dir,
                                                     decon_dir=decon_dir, file_name=file_name)

    text_file_path = save_dir_path + text_files_save_dir + "/" + text_report_name
    progress_text_file_path = save_dir_path + text_files_save_dir + "/" + "ProgressReport.txt"
    cluster_save_path = save_dir_path + clusters_save_dir
    cluster_histogram_path = save_dir_path + cluster_fraction_save_dir
    rand_index_vis_path = save_dir_path + rand_index_save_dir
    decon_plots_path = save_dir_path + decon_dir
    clustered_data_dir = save_dir_path + data_save_dir

    if print_to_console:
        print("\nTime to setup directories: " + str(time.time() - prev_time) + "\n")
    if print_to_text_file:
        f = open(text_file_path, "a")
        print("\nTime to setup directories: " + str(time.time() - prev_time) + "\n", file=f)
        f.close()

        progress_text_file = open(progress_text_file_path, "a")
        print("Working with file " + str(file_name), file=progress_text_file)
        print("Start time: " + str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")), file=progress_text_file)
        print("\nIn progress...", file=progress_text_file)
        progress_text_file.close()

    prev_time = time.time()

    failed_cluster_methods_list = []
    failed_cluster_details_list = []
    failed_cluster_names_list = []

    if print_to_console:
        print("Starting analysis...")
        print("\tFile format: " + str(file_format))
        print("\tFile Name: " + str(file_name))
        print("\tFile Format: " + str(file_format))
        print("\tSaving Directory: " + str(save_dir_path))
        print("\tClustering Column: " + str(clustered_column))
        print("\tShow Raw Data: " + str(show_contour_raw))
        print("\tShow Clustered Contour Plot: " + str(show_contour_clustered))
        print("\tShow Bar Graph: " + str(show_bar))
        print("\tRemove Outliers: " + str(remove_outliers))
        print("\tSave Clustered Contour Plot: " + str(save_contour_clustered))
        print("\tSave Rand Index Visualization Contour Plots: " + str(save_rand_index_visualizations))
        print("\tCluster Contour Plot Save Directory: " + str(clusters_save_dir))
        print("\tRand Index Visualization Save Directory: " + str(rand_index_save_dir))
        print("\tText File Save Directory: " + str(text_files_save_dir))
        print("\tData Files Save Directory: " + str(data_save_dir))
        print("\tCluster Fraction Histograms Save Directory: " + str(cluster_fraction_save_dir))
        print("\tGive Cluster Report: " + str(give_cluster_report))
        print("\tOutliers become additional clusters: " + str(additional_outlier_clusters))
        print("\n")
        for i in range(len(clustering_methods_list)):
            print(str(cluster_names_list[i]))
            print("Iteration: " + str(i))
            print("Clustering Method: " + str(clustering_methods_list[i]))
            print("\tClustering Details: ")
            for cluster_param in clustering_details_list[i]:
                print("\t\t" + str(cluster_param) + ": " + str(clustering_details_list[i][cluster_param]))
            print("\n")

    if print_to_text_file:
        f = open(text_file_path, "a")
        print("Starting analysis...", file=f)
        print("\tFile format: " + str(file_format), file=f)
        print("\tFile Name: " + str(file_name), file=f)
        print("\tFile Format: " + str(file_format), file=f)
        print("\tSaving Directory: " + str(save_dir_path), file=f)
        print("\tClustering Column: " + str(clustered_column), file=f)
        print("\tShow Raw Data: " + str(show_contour_raw), file=f)
        print("\tShow Clustered Contour Plot: " + str(show_contour_clustered), file=f)
        print("\tShow Bar Graph: " + str(show_bar), file=f)
        print("\tRemove Outliers: " + str(remove_outliers), file=f)
        print("\tSave Clustered Contour Plot: " + str(save_contour_clustered), file=f)
        print("\tSave Rand Index Visualization Contour Plots: " + str(save_rand_index_visualizations), file=f)
        print("\tCluster Contour Plot Save Directory: " + str(clusters_save_dir), file=f)
        print("\tRand Index Visualization Save Directory: " + str(rand_index_save_dir), file=f)
        print("\tText File Save Directory: " + str(text_files_save_dir), file=f)
        print("\tData Files Save Directory: " + str(data_save_dir), file=f)
        print("\tCluster Fraction Histograms Save Directory: " + str(cluster_fraction_save_dir), file=f)
        print("\tOutliers become additional clusters: " + str(additional_outlier_clusters), file=f)
        print("\tGive Cluster Report: " + str(give_cluster_report), file=f)
        print("\n", file=f)
        for i in range(len(clustering_methods_list)):
            print(str(cluster_names_list[i]), file=f)
            print("Iteration: " + str(i), file=f)
            print("Clustering Method: " + str(clustering_methods_list[i]), file=f)
            print("\tClustering Details: ", file=f)
            for cluster_param in clustering_details_list[i]:
                print("\t\t" + str(cluster_param) + ": " + str(clustering_details_list[i][cluster_param]), file=f)
            print("\n", file=f)
        f.close()

    if print_to_console:
        print("Time for initial report printout: " + str(time.time() - prev_time) + "\n")
    if print_to_text_file:
        f = open(text_file_path, "a")
        print("Time for initial report printout: " + str(time.time() - prev_time) + "\n", file=f)
        f.close()
    prev_time = time.time()

    # TODO Specify different parameters to be used, clustering details need dictionary
    # TODO Fix project name in auto docs and readme
    # Read in data
    for queue in queues:
        await queue.put("READING")
    await asyncio.sleep(WAIT_TIME)
    if print_to_console:
        print("Reading Data... ")
    if print_to_text_file:
        f = open(text_file_path, "a")
        print("Reading Data... ", file=f)
        f.close()
    data_df, x_df, y_df = dch.get_data(file_name, file_format, clustered_column)

    if print_to_console:
        print("\nTime for reading data: " + str(time.time() - prev_time) + "\n")
    if print_to_text_file:
        f = open(text_file_path, "a")
        print("\nTime for reading data: " + str(time.time() - prev_time) + "\n", file=f)
        f.close()
    prev_time = time.time()

    # Pre process the data
    for queue in queues:
        await queue.put("PREPROCESSING")
    await asyncio.sleep(WAIT_TIME)
    if print_to_console:
        print("PreProcessing Data... ")
    if print_to_text_file:
        f = open(text_file_path, "a")
        print("PreProcessing Data... ", file=f)
        f.close()
    data_df, x_df, y_df = pph.preprocess_data(data_df=data_df, x_df=x_df, y_df=y_df,
                                              remove_outliers=remove_outliers)

    if print_to_console:
        print("\nTime for preprocessing data: " + str(time.time() - prev_time) + "\n")
    if print_to_text_file:
        f = open(text_file_path, "a")
        print("\nTime for preprocessing data: " + str(time.time() - prev_time) + "\n", file=f)
        f.close()
    prev_time = time.time()
    cluster_time = time.time()

    # Cluster the data
    for queue in queues:
        await queue.put("CLUSTERING")
    await asyncio.sleep(WAIT_TIME)
    if print_to_console:
        print("Clustering Data... ")
    if print_to_text_file:
        f = open(text_file_path, "a")
        print("Clustering Data... ", file=f)
        f.close()
    list_of_clustered_data = []
    i = 0
    while i < len(clustering_methods_list):
        if print_to_console:
            print("Clustering Data with clustering method: " + str(cluster_names_list[i]))
        if print_to_text_file:
            f = open(text_file_path, "a")
            print("Clustering Data with clustering method: " + str(cluster_names_list[i]), file=f)
            f.close()
        if clustering_methods_list[i] == sdh.DECONVOLUTION_LABEL:
            clustering_details_list[i][sdh.DECON_CLUSTER_ITER_LABEL] = i
            clustering_details_list[i][sdh.DECON_CLUSTER_NAME_LABEL] = cluster_names_list[i]
            clustering_details_list[i][sdh.DECON_SAVE_DIR_LABEL] = decon_plots_path
        try:
            clustered_data = ch.perform_clustering(data_df=data_df,
                                                   clustering_method=clustering_methods_list[i],
                                                   clustering_details=clustering_details_list[i],
                                                   additional_outlier_clusters=additional_outlier_clusters)
            list_of_clustered_data.append(clustered_data)
            if print_to_console:
                print("Time for cluster " + str(cluster_names_list[i]) + ": " + str(time.time() - cluster_time)
                      + ". Total time so far: " + str(time.time() - start_time) + "\n")
            if print_to_text_file:
                f = open(text_file_path, "a")
                print("Time for cluster " + str(cluster_names_list[i]) + ": " + str(time.time() - cluster_time)
                      + ". Total time so far: " + str(time.time() - start_time) + "\n", file=f)
                f.close()
            cluster_time = time.time()
            i = i + 1

        except Exception:
            if print_to_console:
                print("WARNING: METHOD FAILED")
                print("Clustering method " + str(cluster_names_list[i]) + " failure time: "
                      + str(time.time() - cluster_time) + ". Total time so far: "
                      + str(time.time() - start_time) + "\n")
            if print_to_text_file:
                f = open(text_file_path, "a")
                print("WARNING: METHOD FAILED", file=f)
                print("Clustering method " + str(cluster_names_list[i]) + " failure time: "
                      + str(time.time() - cluster_time) + ". Total time so far: "
                      + str(time.time() - start_time) + "\n", file=f)
                f.close()
            cluster_time = time.time()
            failed_cluster_methods_list.append(clustering_methods_list[i])
            failed_cluster_details_list.append(clustering_details_list[i])
            failed_cluster_names_list.append(cluster_names_list[i])
            del clustering_methods_list[i]
            del clustering_details_list[i]
            del cluster_names_list[i]

    if print_to_console:
        print("Time for all clustering: " + str(time.time() - prev_time) + ". Total time so far: "
              + str(time.time() - start_time))
    if print_to_text_file:
        f = open(text_file_path, "a")
        print("Time for all clustering: " + str(time.time() - prev_time) + ". Total time so far: "
              + str(time.time() - start_time), file=f)
        f.close()
    prev_time = time.time()

    # Print out a little report which says what methods failed
    if len(failed_cluster_methods_list) > 0:
        if print_to_console:
            print("\n")
            print("The Following Clustering methods failed...")

            for i in range(len(failed_cluster_methods_list)):
                print("\n" + str(failed_cluster_names_list[i]))
                print("Iteration: " + str(i))
                print("Clustering Method: " + str(failed_cluster_methods_list[i]))
                print("\tClustering Details: ")
                for cluster_param in failed_cluster_details_list[i]:
                    print("\t\t" + str(cluster_param) + ": " + str(failed_cluster_details_list[i][cluster_param]))
                print("\n")

        if print_to_text_file:
            f = open(text_file_path, "a")
            print("\n", file=f)
            print("The Following Clustering methods failed...", file=f)

            for i in range(len(failed_cluster_methods_list)):
                print("\n" + str(failed_cluster_names_list[i]), file=f)
                print("Iteration: " + str(i), file=f)
                print("Clustering Method: " + str(failed_cluster_methods_list[i]), file=f)
                print("\tClustering Details: ", file=f)
                for cluster_param in failed_cluster_details_list[i]:
                    print("\t\t" + str(cluster_param) + ": " + str(failed_cluster_details_list[i][cluster_param]),
                          file=f)
                print("\n", file=f)
            f.close()

    prev_time = time.time()

    for queue in queues:
        await queue.put("Visualizing")
    await asyncio.sleep(WAIT_TIME)
    if print_to_console:
        print("Visualizing Data... ")
    if print_to_text_file:
        f = open(text_file_path, "a")
        print("Visualizing Data... ", file=f)
        f.close()
    for i in range(len(clustering_methods_list)):
        if print_to_console:
            print("\nVisualizing Data with clustering method: " + str(cluster_names_list[i]))
        if print_to_text_file:
            f = open(text_file_path, "a")
            print("\nVisualizing Data with clustering method: " + str(cluster_names_list[i]), file=f)
            f.close()

        dah.perform_analysis(data_df=data_df, x_df=x_df, y_df=y_df,
                             clustered_data=list_of_clustered_data[i],
                             prop=clustered_column, show_contour_clustered=show_contour_clustered,
                             show_contour_raw=show_contour_raw, show_bar=show_bar,
                             cluster_name=cluster_names_list[i], cluster_iter=i,
                             save_clustered_contour=save_contour_clustered,
                             give_cluster_report=give_cluster_report, print_to_console=print_to_console,
                             print_to_text_file=print_to_text_file, text_file_name=text_file_path,
                             clusters_save_dir=cluster_save_path, save_cluster_histograms=save_cluster_histograms,
                             cluster_histogram_dir=cluster_histogram_path, save_clustered_data=save_clustered_data,
                             clustered_data_dir=clustered_data_dir)

    if print_to_console:
        print("\nVisualization time: " + str(time.time() - prev_time) + "\n")
    if print_to_text_file:
        f = open(text_file_path, "a")
        print("\nVisualization time: " + str(time.time() - prev_time) + "\n", file=f)
        f.close()
    prev_time = time.time()

    # Setting up the priority queues to store all of the information and sort it
    rand_index_queue = PriorityQueue()
    chi_queue = PriorityQueue()
    dbi_queue = PriorityQueue()
    silhouette_queue = PriorityQueue()

    # For every cluster configuration, calculate the necessary information
    i = 0
    while i < len(clustering_methods_list):
        if len(np.unique(list_of_clustered_data[i]["Data"].values)) <= 1:
            chi_value = np.inf
            dbi_value = np.inf
            silhouette_value = np.inf
        else:
            chi_value = CHI.chi(data_df, list_of_clustered_data[i]["Data"].values)
            dbi_value = DBI.dbi(data_df, list_of_clustered_data[i]["Data"].values)
            silhouette_value = SilhouetteCoefficient.silhouetteCoefficient(data_df,
                                                                           list_of_clustered_data[i]["Data"].values)
        chi_queue.put((chi_value, cluster_names_list[i]))
        dbi_queue.put((dbi_value, cluster_names_list[i]))
        silhouette_queue.put((silhouette_value, cluster_names_list[i]))
        j = i
        # For every other clustering method pair we haven't gotten with this method, calculate the rand index
        while j < len(clustering_methods_list):
            if not i == j:
                clustered_df1 = list_of_clustered_data[i]
                clustered_df2 = list_of_clustered_data[j]
                cluster_method_one_list = clustered_df1["Data"].values
                cluster_method_two_list = clustered_df2["Data"].values
                rand_index = adjusted_rand_score(cluster_method_one_list, cluster_method_two_list)
                cluster_pair = str(cluster_names_list[i]) + " and " + str(cluster_names_list[j])
                rand_index_queue.put((rand_index, cluster_pair))

                curr_iter_save_path = rand_index_vis_path + "/RandIndexVis_" + str(i) + "_" + str(j) + "_" \
                    + str(cluster_names_list[i]) + "_" + str(cluster_names_list[j]) + ".png"
                cch.rand_index_visualization(x_df=x_df, y_df=y_df, clustered_df1=clustered_df1,
                                             clustered_df2=clustered_df2, save_plot=save_rand_index_visualizations,
                                             save_path=curr_iter_save_path, show_plot=show_rand_index_plots,
                                             cluster1_name=cluster_names_list[i], cluster2_name=cluster_names_list[j],
                                             cluster1_iter=i, cluster2_iter=j)
            j = j + 1
        i = i + 1

    # Make stacks to put everything in to reverse the order
    rand_index_stack = []
    chi_stack = []
    dbi_stack = []
    silhouette_stack = []

    if print_to_console:
        print("\nRand index, chi, dbi, silhouette computation time: " + str(time.time() - prev_time))
    if print_to_text_file:
        f = open(text_file_path, "a")
        print("\nRand index, chi, dbi, silhouette computation time: " + str(time.time() - prev_time), file=f)
        f.close()
    prev_time = time.time()

    # Put all the information in stacks
    while not rand_index_queue.empty():
        rand_index_stack.append(str(rand_index_queue.get()))

    while not chi_queue.empty():
        chi_stack.append(str(chi_queue.get()))

    while not dbi_queue.empty():
        dbi_stack.append(str(dbi_queue.get()))

    while not silhouette_queue.empty():
        silhouette_stack.append(str(silhouette_queue.get()))

    # Rand index initial print
    if print_to_text_file:
        f = open(text_file_path, "a")
        print("\n\nRand Index Values... ", file=f)
    if print_to_console:
        print("\n\nRand Index Values... ")

    # Rand index print loop
    while len(rand_index_stack) > 0:
        next_line = str(rand_index_stack.pop())
        if print_to_text_file:
            print(next_line, file=f)
        if print_to_console:
            print(next_line)

    # Chi initial print
    if print_to_text_file:
        print("\n\nCHI Values... ", file=f)
    if print_to_console:
        print("\n\nCHI Values... ")

    # Chi values print loop
    while len(chi_stack) > 0:
        next_line = str(chi_stack.pop())
        if print_to_text_file:
            print(next_line, file=f)
        if print_to_console:
            print(next_line)

    # DBI initial print
    if print_to_text_file:
        print("\n\nDBI Values... ", file=f)
    if print_to_console:
        print("\n\nDBI Values... ")

    # DBI values print loop
    while len(dbi_stack) > 0:
        next_line = str(dbi_stack.pop())
        if print_to_text_file:
            print(next_line, file=f)
        if print_to_console:
            print(next_line)

    # Silhouette initial print
    if print_to_text_file:
        print("\n\nSilhouette Values... ", file=f)
    if print_to_console:
        print("\n\nSilhouette Values... ")

    # Silhouette values print loop
    while len(silhouette_stack) > 0:
        next_line = str(silhouette_stack.pop())
        if print_to_text_file:
            print(next_line, file=f)
        if print_to_console:
            print(next_line)

    for queue in queues:
        await queue.put("COMPLETE")
        print(queue)

    if print_to_console:
        print("\nRand index, chi, dbi, silhouette print time: " + str(time.time() - prev_time))
    if print_to_text_file:
        print("\nRand index, chi, dbi, silhouette print time: " + str(time.time() - prev_time), file=f)
    prev_time = time.time()

    # Finishing print
    if print_to_text_file:
        print("\nProcess complete in " + str(time.time() - start_time) + " seconds / " + str(
            (time.time() - start_time) / 60.0) + " minutes / " + str((time.time() - start_time) / 3600.0) + " hours",
              file=f)
        f.close()
    if print_to_console:
        print("\nProcess complete in " + str(time.time() - start_time) + " seconds / " + str(
            (time.time() - start_time) / 60.0) + " minutes / " + str((time.time() - start_time) / 3600.0) + " hours")

        progress_text_file = open(progress_text_file_path, "a")
        print("\nProcess complete on " + str(file_name), file=progress_text_file)
        print("End time: " + str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")), file=progress_text_file)
        print("Total time: " + str(time.time() - start_time) + " seconds / " + str(
            (time.time() - start_time) / 60.0) + " minutes / " + str((time.time() - start_time) / 3600.0) + " hours",
              file=progress_text_file)
        progress_text_file.close()
