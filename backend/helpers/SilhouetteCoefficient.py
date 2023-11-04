from sklearn.metrics import silhouette_score


def silhouetteCoefficient(data_df, cluster_labels):
    """
    :param data_df: The data used to create the cluster
    :param cluster_labels: predicted labels for each sample

    :return: The silhouette coefficient

    Computes the silhouette coefficient of a given cluster and the data on which that cluster was computed

    """
    silhouette_avg = silhouette_score(data_df, cluster_labels)
    return silhouette_avg


def getBest(data_df, clusters):
    """
    :param data_df: The data frame with the data from which the clusters where created
    :param clusters: A list of clusters using the same dataset

    :return: The index in the list of the best cluster based on its silhouette coefficient and its value

    Takes a list of clusters and returns th best one based on their silhouette coefficient

    """
    max_idx = 0
    max_value = 0
    for idx, cluster in enumerate(clusters):
        coefficient = silhouetteCoefficient(data_df, cluster)
        if coefficient > max_value:
            max_value = coefficient
            max_idx = idx
    return max_idx, max_value
