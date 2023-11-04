import numpy as np
from sklearn.metrics import davies_bouldin_score


def dbi(data_df, cluster_labels):
    """
    :param data_df: the data used to create the cluster
    :param cluster_labels: predicted labels for each sample

    :return: The DBI of the cluster

    Computes the Davie Bouldin Index (DBI) of a given cluster

    """
    dbi_val = davies_bouldin_score(data_df, cluster_labels)
    return dbi_val


def getBest(data_df, clusters):
    """
    :param data_df: The data frame with the data from which the clusters where created
    :param clusters: A list of clusters using the same dataset

    :return: The index in the list of the best cluster based on its DBI and its value

    Takes a list of clusters and returns th best one based on their DBI

    """
    min_idx = 0
    min_score = np.inf
    for idx, cluster in enumerate(clusters):
        score = dbi(data_df, cluster)
        if score < min_score:
            min_score = score
            min_idx = idx
    return min_idx, min_score
