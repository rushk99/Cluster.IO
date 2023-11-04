from sklearn.metrics import calinski_harabasz_score


def chi(data_df, cluster_labels):
    """
    :param data_df: the data used to create the cluster
    :param cluster_labels: predicted labels for each sample

    :return: The DBI of the cluster

    Computes the Calinski-Harabasz Index (CHI) of a given cluster

    """
    chi_val = calinski_harabasz_score(data_df, cluster_labels)
    return chi_val


def getBest(data_df, clusters):
    """
    :param data_df: The data frame with the data from which the clusters where created
    :param clusters: A list of clusters using the same dataset

    :return: The index in the list of the best cluster based on its CHI and its value

    Takes a list of clusters and returns th best one based on their CHI

    """
    max_idx = 0
    max_score = 0
    for idx, cluster in enumerate(clusters):
        score = chi(data_df, cluster)
        print(score)
        if score > max_score:
            max_score = score
            max_idx = idx
    return max_idx, max_score
