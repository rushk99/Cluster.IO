import sys

sys.path.append("../")

from sklearn.cluster import AgglomerativeClustering, Birch, DBSCAN, KMeans, OPTICS, SpectralClustering
from sklearn.mixture import GaussianMixture
# TODO I was looking through the clustering algorithms and saw there were a couple more that could
# TODO     be imported, check this out
from sklearn_extra.cluster import KMedoids
import numpy as np
import math
import hdbscan
import seaborn as sns
from fcmeans import FCM
from helpers import DeconHelper, StringDefinitionsHelper
from helpers.Errors import InvalidClusteringMethodError

DEFAULT_METHOD = StringDefinitionsHelper.K_MEANS_LABEL
DEFAULT_DETAILS = {"num_clusters": "3", "random_state": "0"}


def perform_clustering(data_df, clustering_details=DEFAULT_DETAILS, clustering_method=DEFAULT_METHOD,
                       additional_outlier_clusters=False,label="Hardness"):
    """

    :param data_df: The data we are clustering
    :param clustering_details: The details involving the method of clustering we are doing
    :param clustering_method: The clustering method we are using
    :param additional_outlier_clusters: Whether or not to make any outliers separate clusters, with one cluster
        on either side of the set of clusters
    :return: The clustered data based on the data_df column

    Performs clustering on the data inside the data_df based off of the clustering method and details. It calls
    the necessary clustering method helper to perform it's clustering

    """

    altered_df = data_df

    if additional_outlier_clusters:
        # If we want to make the outliers their own clusters then we first separate them from the main set

        cleaned_data = altered_df["Data"]

        # We use mean, standard deviation, and z score to determine outliers
        mean_val = np.mean(cleaned_data)
        stddev_val = np.std(cleaned_data)
        z_scores = 3

        # There are the outliers below the main data set
        outliers_below = cleaned_data[cleaned_data - mean_val < -1 * stddev_val * z_scores]
        outliers_below = pd.DataFrame(outliers_below)

        # These are the outliers above the main data set
        outliers_above = cleaned_data[cleaned_data - mean_val > stddev_val * z_scores]
        outliers_above = pd.DataFrame(outliers_above)

        # The data set which is now free of outliers
        no_outliers = cleaned_data[abs(cleaned_data - mean_val) <= stddev_val * z_scores]

        # The number of outliers above, below, and in the data set
        num_outliers_below = len(outliers_below)
        num_outliers_above = len(outliers_above)

        # Booleans which represent if there are outliers or not
        outliers_below_exist = num_outliers_below > 0
        outliers_above_exist = num_outliers_above > 0

        # We create a bew DataFrame which is used to store our remaining data values which are not outliers
        hard_df_no_outliers = pd.DataFrame()
        hard_df_no_outliers["Data"] = no_outliers

        altered_df = hard_df_no_outliers
    if clustering_method == StringDefinitionsHelper.AGGLOMERATIVE_LABEL:
        # Agglomerative Clustering
        num_clusters = int(clustering_details[StringDefinitionsHelper.NUM_CLUSTERS_LABEL])
        linkage = clustering_details[StringDefinitionsHelper.LINKAGE_LABEL]
        clustered_df = perform_agglomerative(data_df=altered_df, num_clusters=num_clusters, linkage=linkage)

    elif clustering_method == StringDefinitionsHelper.BIRCH_LABEL:
        # Birch Clustering
        num_clusters = int(clustering_details[StringDefinitionsHelper.NUM_CLUSTERS_LABEL])
        threshold=float(clustering_details["threshold"])
        branching_factor=int(clustering_details["branching_factor"])
        clustered_df = perform_birch(data_df=altered_df, num_clusters=num_clusters,threshold=threshold,branching_factor=branching_factor)

    elif clustering_method == StringDefinitionsHelper.DBSCAN_LABEL:
        # DBSCAN Clustering
        eps = float(clustering_details[StringDefinitionsHelper.EPS_LABEL])
        min_samples = int(clustering_details[StringDefinitionsHelper.MIN_SAMPLES_LABEL])
        algorithm = clustering_details[StringDefinitionsHelper.ALGORITHM_LABEL]
        clustered_df = perform_dbscan(data_df=altered_df, eps=eps, min_samples=min_samples, algorithm=algorithm)

    elif clustering_method == StringDefinitionsHelper.DECONVOLUTION_LABEL:
        
        # Deconvolution Clustering
        m_val = int(clustering_details[StringDefinitionsHelper.M_VAL_LABEL])
        max_iter = int(clustering_details[StringDefinitionsHelper.MAX_ITER_LABEL])
        limit = float(clustering_details[StringDefinitionsHelper.LIMIT_LABEL])
        
        clustered_df = perform_decon(data_df=altered_df, m_val=m_val, max_iter=max_iter, limit=limit, label=label,
                                     )

    elif clustering_method == StringDefinitionsHelper.K_MEANS_LABEL:
        # K Means Clustering
        num_clusters = int(clustering_details[StringDefinitionsHelper.NUM_CLUSTERS_LABEL])
        random_state = int(clustering_details[StringDefinitionsHelper.RANDOM_STATE_LABEL])
        clustered_df = perform_k_means(data_df=altered_df, num_clusters=num_clusters, random_state=random_state)

    elif clustering_method == StringDefinitionsHelper.K_MEDOIDS_LABEL:
        # K Medoids Clustering
        num_clusters = int(clustering_details[StringDefinitionsHelper.NUM_CLUSTERS_LABEL])
        init = clustering_details[StringDefinitionsHelper.INIT_LABEL]
        random_state = int(clustering_details[StringDefinitionsHelper.RANDOM_STATE_LABEL])
        clustered_df = perform_k_medoids(data_df=altered_df, num_clusters=num_clusters, init=init,
                                         random_state=random_state)

    elif clustering_method == StringDefinitionsHelper.OPTICS_LABEL:
        # OPTICS Clustering
        max_eps = float(clustering_details["max_eps"])
        min_samples = int(clustering_details[StringDefinitionsHelper.MIN_SAMPLES_LABEL])
        algorithm = clustering_details[StringDefinitionsHelper.ALGORITHM_LABEL]
        clustered_df = perform_optics(data_df=altered_df, max_eps=max_eps, min_samples=min_samples, algorithm=algorithm)
    
    elif clustering_method == "fuzzycmeans":
        # Fuzzy C Means Clustering
        num_clusters = int(clustering_details["num_clusters"])
        Fuzzifier = int(clustering_details["fuzzifier"])
        clustered_df = perform_fuzzycmeans(data_df=altered_df, num_clusters=num_clusters, Fuzzifier=Fuzzifier)

    elif clustering_method == "gaussianmixturemodel":
        num_clusters = int(clustering_details["num_clusters"])
        clustered_df = perform_gaussianmixturemodel(data_df=altered_df, num_clusters=num_clusters)

    elif clustering_method == StringDefinitionsHelper.SPECTRAL_LABEL:
        # Spectral Clustering
        num_clusters = int(clustering_details[StringDefinitionsHelper.NUM_CLUSTERS_LABEL])
        assign_labels = clustering_details[StringDefinitionsHelper.ASSIGN_LABELS_LABEL]
        affinity = clustering_details[StringDefinitionsHelper.AFFINITY_LABEL]
        random_state = int(clustering_details[StringDefinitionsHelper.RANDOM_STATE_LABEL])
        clustered_df = perform_spectral(data_df=altered_df, num_clusters=num_clusters, assign_labels=assign_labels,
                                        affinity=affinity, random_state=random_state)

    elif clustering_method == StringDefinitionsHelper.HDBSCAN_LABEL:
        metric = clustering_details[StringDefinitionsHelper.DISTANCE_METRIC_LABEL]
        min_cluster_size = int(clustering_details[StringDefinitionsHelper.MIN_CLUSTER_SIZE_LABEL])
        min_samples = int(clustering_details[StringDefinitionsHelper.MIN_SAMPLES_LABEL])
        clustered_df = perform_hdbscan(data_df=altered_df, metric=metric, min_cluster_size=min_cluster_size,
                                       min_samples=min_samples)
    else:
        raise InvalidClusteringMethodError(clustering_method)
        # print("You have done something bad... stop doing that!")
        # exit(-50)

    if additional_outlier_clusters:
        # If we want to make the outliers their own clusters then we need to add them back to the clustered data

        # Find unique values so we can generate new clusters after this
        unique_cluster_values = np.unique(clustered_df["Data"].values)

        # We get the index from the previous set of data with no outliers so we can recombine them
        no_outliers_index = hard_df_no_outliers.index

        # We combine the data values based on the index
        combined_clusters = pd.DataFrame(clustered_df["Data"].values, index=no_outliers_index, columns=["Data"])

        if outliers_below_exist:
            # The new outliers below the data have a value set to 1 below the min cluster value
            outliers_below["Data"] = np.full(shape=num_outliers_below, fill_value=min(unique_cluster_values) - 1)

            combined_clusters = combined_clusters.append(outliers_below)

        if outliers_above_exist:
            # The new outliers below the data have a value set to 1 above the min cluster value
            outliers_above["Data"] = np.full(shape=num_outliers_above, fill_value=max(unique_cluster_values) + 1)

            combined_clusters = combined_clusters.append(outliers_above)

        combined_clusters = combined_clusters.sort_index()

        clustered_df = combined_clusters

    # Get new DataFrame with ordered clusters
    new_df = order_clusters(data_df=data_df, clustered_data_df=clustered_df)
    return new_df


def perform_agglomerative(data_df, num_clusters=3, linkage="ward"):
    """

    :param data_df: The data being clustered
    :param num_clusters: The number of clusters we are clustering the data into
    :param linkage: Which linkage criterion to use. The linkage criterion determines which distance to use between sets
        of observation. The algorithm will merge the pairs of cluster that minimize this criterion.

    :return: Clustered data

    Performs agglomerative clustering

    """

    agglomerative = AgglomerativeClustering(n_clusters=num_clusters, linkage=linkage).fit(data_df)

    agglomerative_results = agglomerative.labels_
    return transform_to_df(agglomerative_results)


def perform_birch(data_df,threshold,branching_factor,num_clusters=3):
    """

    :param data_df: The data being clustered
    :param num_clusters: The number of clusters we are clustering the data into

    :return: Clustered data

    Performs birch clustering

    """

    birch = Birch(n_clusters=num_clusters, threshold=threshold,branching_factor=branching_factor).fit(data_df)
    birch_results = birch.labels_
    return transform_to_df(birch_results)


def perform_dbscan(data_df, eps=0.75, min_samples=100, algorithm="auto"):
    """

    :param data_df: The data being clustered
    :param eps: The maximum distance between two samples for one to be considered as in the neighborhood of the other.
        This is not a maximum bound on the distances of points within a cluster.
        This is the most important DBSCAN parameter to choose appropriately for your data set and distance function.

    :param min_samples: The number of samples (or total weight) in a neighborhood for a point to be considered as a
        core point. This includes the point itself.

    :param algorithm: The algorithm to be used by the NearestNeighbors module to compute pointwise distances and find
        nearest neighbors. See NearestNeighbors module documentation for details.

    :return: Clustered data

    Performs DBSCAN clustering

    """

    dbscan = DBSCAN(algorithm=algorithm, eps=eps, min_samples=min_samples).fit(data_df)
    dbscan_results = dbscan.labels_
    return transform_to_df(dbscan_results)


def perform_decon(data_df, m_val=3, max_iter=1500, limit=10 ** -6, label="Hardness", show_plots=False,
                  save_plots=False, save_dir="", cluster_iter=0, cluster_name=""):
    """

    :param data_df: The data being clustered
    :param m_val: The number of clusters we are clustering the data into
    :param max_iter: The max number of iterations to run the deconvolution method with, should be an integer,
        1500 by default
    :param limit: The limit or degree of precision we are using, it is a value used in the decon method to check if a
        solution is valid or not
    :param label: The column we are using for analysis, can be 'Hardness' for example
    :param show_plots: A boolean of whether or not to show the plots
    :param save_plots: A boolean of whether or not to save the plots
    :param save_dir: The directory to save the plots in
    :param cluster_iter: The iteration of this cluster configuration
    :param cluster_name: The name of this cluster configuration

    :return: Clustered data

    Performs Deconvolution clustering

    """
    
    dh_res = DeconHelper.DeconHelper()
    input_data = data_df["Data"].values
    dh_res.run_process(input_data=input_data, max_iter=max_iter, limit=limit, label=label, m=m_val,
                       show_plots=show_plots, save_plots=save_plots, save_dir=save_dir,
                       cluster_iter=cluster_iter, cluster_name=cluster_name)
    

    def custom_curve_i_normpdf(x, index_val):
        """

        :param x: The value being looked at
        :param index_val: The index of the decon phase

        :return: The normpdf of the value relative to the curve at index index_val

        Function used to determine which curve a point belongs to

        """

        return math.fabs(
            DeconHelper.normpdf(x=x, mean=dh_res.minprumer[index_val], sd=dh_res.minstddev[index_val]))

    decon_results = []
    # For every data point, determine which bin it falls into
    for i in range(data_df["Data"].values.size):
        temp_decon_list = []
        for j in range(m_val):
            temp_decon_list.append(custom_curve_i_normpdf(x=data_df["Data"].values[i], index_val=j))
        decon_results.append(np.argmax(temp_decon_list))

    return transform_to_df(decon_results)


def perform_k_means(data_df, num_clusters=3, random_state=0):
    """

    :param data_df: The data being clustered
    :param num_clusters: The number of clusters we are clustering the data into
    :param random_state: The random seed the environment is set to before clustering. The method uses randomness so
        this allows for reproducibility

    :return: Clustered data

    Performs K Means clustering

    """

    k_means = KMeans(n_clusters=num_clusters, random_state=random_state).fit(data_df)
    
    k_means_results = k_means.predict(data_df)

    return transform_to_df(k_means_results)


def perform_k_medoids(data_df, num_clusters=3, init="random", random_state=0):
    """

    :param data_df: The data being clustered
    :param num_clusters: The number of clusters we are clustering the data into
    :param init: Specify medoid initialization method. ‘random’ selects n_clusters elements from the dataset.
        ‘heuristic’ picks the n_clusters points with the smallest sum distance to every other point. ‘k-medoids++’
        follows an approach based on k-means++_, and in general, gives initial medoids which are more separated than
        those generated by the other methods. ‘build’ is a greedy initialization of the medoids used in the original PAM
        algorithm. Often ‘build’ is more efficient but slower than other initializations on big datasets and it is
        also very non-robust, if there are outliers in the dataset, use another initialization.

    :param random_state: The random seed the environment is set to before clustering. The method uses randomness so
        this allows for reproducibility

    :return: Clustered data

    Performs K Medoids clustering

    """

    k_medoids = KMedoids(n_clusters=num_clusters, init=init, random_state=random_state).fit(data_df)

    k_medoids_results = k_medoids.labels_
    return transform_to_df(k_medoids_results)


def perform_optics(data_df, max_eps=0.09, min_samples=100, algorithm="auto"):
    """

    :param data_df: The data being clustered
    :param eps: The maximum distance between two samples for one to be considered as in the neighborhood of the other.
        By default it assumes the same value as max_eps. Used only when cluster_method='dbscan'.
    :param min_samples: The number of samples in a neighborhood for a point to be considered as a core point.
        Also, up and down steep regions can’t have more than min_samples consecutive non-steep points.
        Expressed as an absolute number or a fraction of the number of samples (rounded to be at least 2).
    :param algorithm: Algorithm used to compute the nearest neighbors

    :return: Clustered data

    Performs OPTICS clustering

    """

    optics = OPTICS(algorithm=algorithm, max_eps=max_eps, min_samples=min_samples).fit(data_df)
    optics_results = optics.labels_
    return transform_to_df(optics_results)

def perform_fuzzycmeans(data_df, num_clusters=3, Fuzzifier=2):
    """

    :param data_df: The data being clustered
    :param eps: The maximum distance between two samples for one to be considered as in the neighborhood of the other.
        By default it assumes the same value as max_eps. Used only when cluster_method='dbscan'.
    :param min_samples: The number of samples in a neighborhood for a point to be considered as a core point.
        Also, up and down steep regions can’t have more than min_samples consecutive non-steep points.
        Expressed as an absolute number or a fraction of the number of samples (rounded to be at least 2).
    :param algorithm: Algorithm used to compute the nearest neighbors

    :return: Clustered data

    Performs OPTICS clustering

    """
    
    fcm = FCM(n_clusters=num_clusters, Fuzzifier=Fuzzifier).fit(data_df)
    fcm_results = fcm.predict(data_df)
    return transform_to_df(fcm_results)

def perform_gaussianmixturemodel(data_df, num_clusters=3):
    """

    :param data_df: The data being clustered
    :param eps: The maximum distance between two samples for one to be considered as in the neighborhood of the other.
        By default it assumes the same value as max_eps. Used only when cluster_method='dbscan'.
    :param min_samples: The number of samples in a neighborhood for a point to be considered as a core point.
        Also, up and down steep regions can’t have more than min_samples consecutive non-steep points.
        Expressed as an absolute number or a fraction of the number of samples (rounded to be at least 2).
    :param algorithm: Algorithm used to compute the nearest neighbors

    :return: Clustered data

    Performs OPTICS clustering

    """
    gmm= GaussianMixture(n_components= num_clusters).fit(data_df)
    gmm_results = gmm.predict(data_df)
    return transform_to_df(gmm_results)


def perform_spectral(data_df, num_clusters=3, assign_labels="discretize", affinity="rbf", random_state=0):
    """

    :param data_df: The data being clustered
    :param num_clusters: The number of clusters we are clustering the data into
    :param assign_labels: The strategy to use to assign labels in the embedding space. There are two ways to assign
        labels after the laplacian embedding. k-means can be applied and is a popular choice. But it can also be
        sensitive to initialization. Discretization is another approach which is less sensitive to random
        initialization.
    :param affinity: How to construct the affinity matrix.
    :param random_state: The random seed the environment is set to before clustering. The method uses randomness so
        this allows for reproducibility

    :return: Clustered data

    Performs Spectral clustering

    """

    spectral = SpectralClustering(n_clusters=num_clusters, assign_labels=assign_labels, random_state=random_state,
                                  affinity=affinity).fit(data_df)

    spectral_results = spectral.labels_
    return transform_to_df(spectral_results)


def perform_hdbscan(data_df, metric="euclidean", min_cluster_size=10, min_samples=200):
    """

    :param min_samples:
    :param min_cluster_size:
    :param metric:
    :param data_df: The data being clustered

    :return: Clustered data

    Performs HDBSCAN clustering

    """

    hdbscan_clusters = hdbscan.HDBSCAN(metric=metric, min_cluster_size=min_cluster_size, min_samples=min_samples,
                                       p=0.05).fit(data_df)
    hdbscan_results = hdbscan_clusters.labels_
    #hdbscan_clusters.condensed_tree_.plot(select_clusters=True,selection_palette=sns.color_palette('deep', 8))
    return transform_to_df(hdbscan_results)
    # return None


def transform_to_df(data_list):
    """

    :param data_list: A list representation of the data

    :return: A DataFrame made up of the list taken into the method

    Transforms the list into a DataFrame with the appropriate column name

    """

    data_df = pd.DataFrame(data_list)
    data_df.columns = ["Data"]

    return data_df


import pandas as pd
import numpy as np


def order_clusters(data_df, clustered_data_df):
    """

    :param data_df: A DataFrame representation of all of the raw data we are reading
    :param clustered_data_df: A DataFrame representation of all of the clustered data we are reading

    :return: A new DataFrame which stores the new clustered values along with the original data

    Orders the clusters so they correlate with their original hardness values

    """

    # Transform the data into a single DataFrame
    if "Data" in data_df.columns :
        original_data_values = pd.DataFrame({"Data": data_df["Data"].values, "Cluster": clustered_data_df["Data"].values})
    else:
        original_data_values =  pd.DataFrame({"Hardness": data_df["Hardness"].values,"Modulus": data_df["Modulus"].values, "Cluster": clustered_data_df["Data"].values})
    # Find the unique values to find the number of clusters we are altering
    unique_values = np.unique(original_data_values["Cluster"].values)
    num_clusters = len(unique_values) - int(-1 in unique_values)

    # Sort the data representations based on the raw data values
    if "Data" in data_df.columns :
        cluster_representations = original_data_values.groupby("Cluster")["Data"].min().reset_index().sort_values("Data")
    else :
        cluster_representations = original_data_values.groupby("Cluster")[["Hardness", "Modulus"]].min().reset_index().sort_values(["Hardness", "Modulus"])
    # Map the old cluster values to the new cluster values
    transformation_dictionary = {cluster_value: i for i, cluster_value in enumerate(cluster_representations["Cluster"])}

    # Apply the mapping function to create a new DataFrame with updated cluster values
    df_new = pd.DataFrame({"Data": original_data_values["Cluster"].map(transformation_dictionary)})

    return df_new
