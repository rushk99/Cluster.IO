import numpy as np
from helpers import StringDefinitionsHelper


data = {
    "clusteringMethods": [
        {
            "name": StringDefinitionsHelper.K_MEANS_NAME,
            "label": StringDefinitionsHelper.K_MEANS_LABEL,
            "options": [
                {
                    "name": StringDefinitionsHelper.NUM_CLUSTERS_LABEL,
                    "description": "The number of clusters to form as well as the number of centroids to generate.",
                    "type": "INT",
                    "default": 3,
                    "required": True
                },
                {
                    "name": StringDefinitionsHelper.RANDOM_STATE_LABEL,
                    "description": "Determines random number generation for centroid initialization. Use an int to make the randomness deterministic.",
                    "type": "INT",
                    "default": 0,
                    "required": True
                }
            ]
        },
        {
            "name": StringDefinitionsHelper.BIRCH_LABEL,
            "label": StringDefinitionsHelper.BIRCH_LABEL,
            "options": [
                {
                    "name": StringDefinitionsHelper.NUM_CLUSTERS_LABEL,
                    "description": "Number of clusters after the final clustering step, which treats the subclusters from the leaves as new samples.",
                    "type": "INT",
                    "default": 3,
                    "required": True
                },
                {
                    "name": "threshold",
                    "description": "The radius of the subcluster obtained by merging a new sample and the closest subcluster should be lesser than the threshold. Otherwise a new subcluster is started. Setting this value to be very low promotes splitting and vice-versa.",
                    "type": "FLOAT",
                    "default": 0.5,
                    "required": True
                },
                {
                    "name": "branching_factor",
                    "description": "Maximum number of CF subclusters in each node. If a new samples enters such that the number of subclusters exceed the branching_factor then that node is split into two nodes with the subclusters redistributed in each. The parent subcluster of that node is removed and two new subclusters are added as parents of the 2 split nodes.",
                    "type": "INT",
                    "default": 50,
                    "required": True
                }
            ]
        },
        {
            "name": StringDefinitionsHelper.AGGLOMERATIVE_LABEL,
            "label": StringDefinitionsHelper.AGGLOMERATIVE_LABEL,
            "options": [
                {
                    "name": StringDefinitionsHelper.NUM_CLUSTERS_LABEL,
                    "description": "The number of clusters to find.",
                    "type": "INT",
                    "default": 3,
                    "required": True
                },
                {
                    "name": StringDefinitionsHelper.LINKAGE_LABEL,
                    "description": "Which linkage criterion to use. The linkage criterion determines which distance to use between sets of observation. The algorithm will merge the pairs of cluster that minimize this criterion. ‘ward’ minimizes the variance of the clusters being merged. ‘average’ uses the average of the distances of each observation of the two sets. ‘complete’ or ‘maximum’ linkage uses the maximum distances between all observations of the two sets. ‘single’ uses the minimum of the distances between all observations of the two sets.",
                    "type": "STRING",
                    "default": "ward",
                    "required": True
                }
            ]
        },
        {
            "name": StringDefinitionsHelper.DBSCAN_LABEL,
            "label": StringDefinitionsHelper.DBSCAN_LABEL,
            "options": [
                {
                    "name": StringDefinitionsHelper.EPS_LABEL,
                    "description": "The maximum distance between two samples for one to be considered as in the neighborhood of the other. This is not a maximum bound on the distances of points within a cluster. This is the most important DBSCAN parameter to choose appropriately for your data set and distance function",
                    "type": "FLOAT",
                    "default": 0.75,
                    "required": True
                },
                {
                    "name": StringDefinitionsHelper.MIN_SAMPLES_LABEL,
                    "description": "The number of samples (or total weight) in a neighborhood for a point to be considered as a core point. This includes the point itself.",
                    "type": "INT",
                    "default": 5,
                    "required": True
                },
                {
                    "name": StringDefinitionsHelper.ALGORITHM_LABEL,
                    "description": "The algorithm to be used by the NearestNeighbors module to compute pointwise distances and find nearest neighbors. It can either be ‘auto’, ‘ball_tree’, ‘kd_tree’ or ‘brute’",
                    "type": "STRING",
                    "default": "auto",
                    "required": True
                }
            ]
        },
        {
            "name": StringDefinitionsHelper.DECONVOLUTION_LABEL,
            "label": StringDefinitionsHelper.DECONVOLUTION_LABEL,
            "options": [
                {
                    "name": StringDefinitionsHelper.M_VAL_LABEL,
                    "description": "The number of clusters we are using, must be above 0 and an int",
                    "type": "INT",
                    "default": 3,
                    "required": True
                },
                {
                    "name": StringDefinitionsHelper.MAX_ITER_LABEL,
                    "description": "The max number of iterations to run the deconvolution method with, should be an integer.",
                    "type": "INT",
                    "default": 1500,
                    "required": True
                },
                {
                    "name": StringDefinitionsHelper.LIMIT_LABEL,
                    "description": "The limit or degree of precision we are using, it is a value used in the decon method to check if a solution is valid or not.",
                    "type": "FLOAT",
                    "default": 10 ** -6,
                    "required": True
                }
            ]
        },
        {
            "name": StringDefinitionsHelper.K_MEDOIDS_NAME,
            "label": StringDefinitionsHelper.K_MEDOIDS_LABEL,
            "options": [
                {
                    "name": StringDefinitionsHelper.NUM_CLUSTERS_LABEL,
                    "description": "The number of clusters to form as well as the number of medoids to generate.",
                    "type": "INT",
                    "default": 3,
                    "required": True
                },
                {
                    "name": StringDefinitionsHelper.INIT_LABEL,
                    "description": "Specify medoid initialization method. ‘random’ selects n_clusters elements from the dataset. ‘heuristic’ picks the n_clusters points with the smallest sum distance to every other point. ‘k-medoids++’ follows an approach based on k-means++_, and in general, gives initial medoids which are more separated than those generated by the other methods. ‘build’ is a greedy initialization of the medoids used in the original PAM algorithm. Often ‘build’ is more efficient but slower than other initializations on big datasets and it is also very non-robust, if there are outliers in the dataset, use another initialization.",
                    "type": "STRING",
                    "default": 'random',
                "required": True
                },
                {
                    "name": StringDefinitionsHelper.RANDOM_STATE_LABEL,
                    "description": "Specify random state for the random number generator. Used to initialise medoids when init=’random’.",
                    "type": "INT",
                    "default": 0,
                "required": True
                }
            ]
        },
        {
            "name": "Fuzzycmeans",
            "label": "Fuzzycmeans",
            "options": [
                {
                    "name": "num_clusters",
                    "description": "The number of clusters to form.",
                    "type": "INT",
                    "default": 3,
                    "required": True
                },
                {
                    "name": "fuzzifier",
                    "description": "Describes how fuzzy you want the clusters to be.",
                    "type": "INT",
                    "default": 2,
                "required": True
                }
            ]
        },
        {
            "name": "GaussianMixtureModel",
            "label": "GaussianMixtureModel",
            "options": [
                {
                    "name": "num_clusters",
                    "description": "The number of clusters to form.",
                    "type": "INT",
                    "default": 3,
                    "required": True
                }
            ]
        },
        {
            "name": StringDefinitionsHelper.OPTICS_LABEL,
            "label": StringDefinitionsHelper.OPTICS_LABEL,
            "options": [
                {
                    "name": "max_eps",
                    "description": "The maximum distance between two samples for one to be considered as in the neighborhood of the other.",
                    "type": "FLOAT",
                    "default": "infinity (very large number)",
                    "required": True
                },
                {
                    "name": StringDefinitionsHelper.MIN_SAMPLES_LABEL,
                    "description": "The number of samples in a neighborhood for a point to be considered as a core point. Also, up and down steep regions can’t have more than min_samples consecutive non-steep points. Expressed as an absolute number or a fraction of the number of samples (rounded to be at least 2).",
                    "type": "INT",
                    "default": 100,
                    "required": True
                },
                {
                    "name": StringDefinitionsHelper.ALGORITHM_LABEL,
                    "description": "Algorithm used to compute the nearest neighbors: ‘ball_tree’ will use BallTree. ‘kd_tree’ will use KDTree. ‘brute’ will use a brute-force search. ‘auto’ (default) will attempt to decide the most appropriate algorithm based on the values passed to fit method.",
                    "type": "STRING",
                    "default": "auto",
                    "required": True
                }
            ]
        },
        {
            "name": StringDefinitionsHelper.SPECTRAL_LABEL,
            "label": StringDefinitionsHelper.SPECTRAL_LABEL,
            "options": [
                {
                    "name": StringDefinitionsHelper.NUM_CLUSTERS_LABEL,
                    "description": "The dimension of the projection subspace.",
                    "type": "INT",
                    "default": 3,
                    "required": True
                },
                {
                    "name": StringDefinitionsHelper.ASSIGN_LABELS_LABEL,
                    "description": "The strategy for assigning labels in the embedding space. There are two ways to assign labels after the Laplacian embedding. k-means is a popular choice, but it can be sensitive to initialization. Discretization is another approach which is less sensitive to random initialization. The cluster_qr method directly extract clusters from eigenvectors in spectral clustering. In contrast to k-means and discretization, cluster_qr has no tuning parameters and runs no iterations, yet may outperform k-means and discretization in terms of both quality and speed.",
                    "type": "STRING",
                    "default": "discretize",
                    "required": True
                },
                {
                    "name": StringDefinitionsHelper.AFFINITY_LABEL,
                    "description": "‘nearest_neighbors’: construct the affinity matrix by computing a graph of nearest neighbors. ‘rbf’: construct the affinity matrix using a radial basis function (RBF) kernel. ‘precomputed’: interpret X as a precomputed affinity matrix, where larger values indicate greater similarity between instances. ‘precomputed_nearest_neighbors’: interpret X as a sparse graph of precomputed distances, and construct a binary affinity matrix from the n_neighbors nearest neighbors of each instance.",
                    "type": "STRING",
                    "default": "rbf",
                    "required": True
                },
                {
                    "name": StringDefinitionsHelper.RANDOM_STATE_LABEL,
                    "description": "A pseudo random number generator used for initialization.",
                    "type": "INT",
                    "default": 0,
                    "required": True
                }
            ]
        }
    ]
}
