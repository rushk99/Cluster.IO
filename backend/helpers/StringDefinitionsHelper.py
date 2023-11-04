AGGLOMERATIVE_LABEL = "Agglomerative"
"""
Agglomerative Label
"""

BIRCH_LABEL = "Birch"
"""
Birch Label
"""

DBSCAN_LABEL = "DBSCAN"
"""
DBSCAN Label
"""

DECONVOLUTION_LABEL = "Deconvolution"
"""
Deconvolution Label
"""

K_MEANS_LABEL = "K Means"
"""
K Means Label
"""

K_MEDOIDS_LABEL = "K Medoids"
"""
K Medoids Label
"""

K_MEANS_NAME = "KMeans"
"""
K Means Name
"""

K_MEDOIDS_NAME = "KMedoids"
"""
K Medoids Name
"""

OPTICS_LABEL = "OPTICS"
"""
OPTICS Label
"""

SPECTRAL_LABEL = "Spectral"
"""
Birch Label
"""

HDBSCAN_LABEL = "HDBSCAN"
"""
Birch Label
"""

# Shared Clustering Labels

NUM_CLUSTERS_LABEL = "num_clusters"
"""
The label to use for the number of clusters to cluster the data into. Parameters tied with this should be any
integer value above 0.
"""

NUM_CLUSTERS_LABEL_DEFAULT = 3
"""
Default value for the number of clusters.
"""


# Agglomerative Labels
# Uses NUM_CLUSTERS_LABEL

LINKAGE_LABEL = "linkage"
"""
The label for the linkage property.
"""

LINKAGE_LABEL_DEFAULT = "ward"
"""
We use ward by default.
Taken from: https://scikit-learn.org/stable/modules/generated/sklearn.cluster.AgglomerativeClustering.html
LINKAGE_LABEL
Which linkage criterion to use. The linkage criterion determines which distance to use between sets of observation. 
The algorithm will merge the pairs of cluster that minimize this criterion.

    ‘ward’ minimizes the variance of the clusters being merged.

    ‘average’ uses the average of the distances of each observation of the two sets.

    ‘complete’ or ‘maximum’ linkage uses the maximum distances between all observations of the two sets.

    ‘single’ uses the minimum of the distances between all observations of the two sets.

"""

# TODO There is another property called affinity which was overlooked, this may be another variation we can use

# Birch Labels
"""
Taken from: https://scikit-learn.org/stable/modules/generated/sklearn.cluster.Birch.html#sklearn.cluster.Birch
"""
# Uses NUM_CLUSTERS_LABEL
# No unique labels

# DBSCAN Labels
"""
Taken from: https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html#sklearn.cluster.DBSCAN
EPS_LABEL - eps float, default=0.5
The maximum distance between two samples for one to be considered as in the neighborhood of the other. 
This is not a maximum bound on the distances of points within a cluster. 
This is the most important DBSCAN parameter to choose appropriately for your data set and distance function.

MIN_SAMPLES_LABEL - min_samples int, default=5
The number of samples (or total weight) in a neighborhood for a point to be considered as a core point. 
This includes the point itself.

ALGORITHM_LABEL - algorithm{‘auto’, ‘ball_tree’, ‘kd_tree’, ‘brute’}, default=’auto’
The algorithm to be used by the NearestNeighbors module to compute pointwise distances and find nearest neighbors. 
See NearestNeighbors module documentation for details.
"""
EPS_LABEL = "eps"
EPS_LABEL_DEFAULT = 0.75
MIN_SAMPLES_LABEL = "min_samples"
MIN_SAMPLES_LABEL_DEFAULT = 100
ALGORITHM_LABEL = "algorithm"
ALGORITHM_LABEL_DEFAULT = "auto"

# Deconvolution Labels
"""
M_VAL_LABEL - The number of clusters we are using, must be above 0 and an int

MAX_ITER_LABEL - The max number of iterations to run the deconvolution method with, should be an integer, 
1500 by default

LIMIT_LABEL - The limit or degree of precision we are using, it is a value used in the decon method to check if a 
solution is valid or not

LABEL_LABEL - The column we are using for analysis, can be 'Hardness' for example
"""
# TODO
M_VAL_LABEL = "m_val"
M_VAL_LABEL_DEFAULT = 3
MAX_ITER_LABEL = "max_iter"
MAX_ITER_LABEL_DEFAULT = 1500
LIMIT_LABEL = "limit"
LIMIT_LABEL_DEFAULT = 10 ** -6
LABEL_LABEL = "label"
LABEL_LABEL_DEFAULT = "Hardness"

SHOW_DECON_PLOTS_DEFAULT = False
SHOW_DECON_PLOTS_LABEL = "show_plots"
SAVE_DECON_PLOTS_DEFAULT = False
SAVE_DECON_PLOTS_LABEL = "save_plots"
# See later for default save location
DECON_SAVE_DIR_LABEL = "save_dir"
DECON_CLUSTER_ITER_DEFAULT = 0
DECON_CLUSTER_ITER_LABEL = "cluster_iter"
DECON_CLUSTER_NAME_DEFAULT = ""
DECON_CLUSTER_NAME_LABEL = "cluster_name"
# K Means Labels
# Uses NUM_CLUSTERS_LABEL
"""
Taken from: https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html#sklearn.cluster.KMeans
RANDOM_STATE_LABEL - The random seed the environment is set to before clustering. The method uses randomness so this
allows for reproducibility
"""
RANDOM_STATE_LABEL = "random_state"
RANDOM_STATE_LABEL_DEFAULT = 0

# K Medoids Labels
"""
Taken from: https://scikit-learn-extra.readthedocs.io/en/latest/generated/sklearn_extra.cluster.KMedoids.html
INIT_LABEL - init{‘random’, ‘heuristic’, ‘k-medoids++’, ‘build’}, optional, default: ‘build’
Specify medoid initialization method. ‘random’ selects n_clusters elements from the dataset. ‘heuristic’ 
picks the n_clusters points with the smallest sum distance to every other point. ‘k-medoids++’ follows an 
approach based on k-means++_, and in general, gives initial medoids which are more separated than those 
generated by the other methods. ‘build’ is a greedy initialization of the medoids used in the original PAM 
algorithm. Often ‘build’ is more efficient but slower than other initializations on big datasets and it is 
also very non-robust, if there are outliers in the dataset, use another initialization.
"""
# Uses NUM_CLUSTERS_LABEL
INIT_LABEL = "init"
INIT_LABEL_DEFAULT = "random"
# Uses RANDOM_STATE_LABEL

# OPTICS Labels (Same as DBSCAN)
"""
Taken from: https://scikit-learn.org/stable/modules/generated/sklearn.cluster.OPTICS.html#sklearn.cluster.OPTICS
Note: Use these descriptions as they are different than DBSCAN
EPS_LABEL - eps float, default=None
The maximum distance between two samples for one to be considered as in the neighborhood of the other. 
By default it assumes the same value as max_eps. Used only when cluster_method='dbscan'.

MIN_SAMPLES_LABEL - min_samples int > 1 or float between 0 and 1, default=5
The number of samples in a neighborhood for a point to be considered as a core point. 
Also, up and down steep regions can’t have more than min_samples consecutive non-steep points. 
Expressed as an absolute number or a fraction of the number of samples (rounded to be at least 2).

ALGORITHM_LABEL - algorithm{‘auto’, ‘ball_tree’, ‘kd_tree’, ‘brute’}, default=’auto’
Algorithm used to compute the nearest neighbors:

‘ball_tree’ will use BallTree

‘kd_tree’ will use KDTree

‘brute’ will use a brute-force search.

‘auto’ will attempt to decide the most appropriate algorithm based on the values passed to fit method. (default)

Note: fitting on sparse input will override the setting of this parameter, using brute force.
"""
# Uses EPS_LABEL
# Uses MIN_SAMPLES_LABEL
# Uses ALGORITHM_LABEL

# Spectral Labels
"""
Taken from: https://scikit-learn.org/stable/modules/generated/sklearn.cluster.SpectralClustering.html
ASSIGN_LABELS_LABEL - assign_labels{‘kmeans’, ‘discretize’}, default=’kmeans’
The strategy to use to assign labels in the embedding space. There are two ways to assign labels after the laplacian 
embedding. k-means can be applied and is a popular choice. But it can also be sensitive to initialization. 
Discretization is another approach which is less sensitive to random initialization.

AFFINITY_LABEL - affinity str or callable, default=’rbf’
How to construct the affinity matrix.
‘nearest_neighbors’ : construct the affinity matrix by computing a graph of nearest neighbors.

‘rbf’ : construct the affinity matrix using a radial basis function (RBF) kernel.

‘precomputed’ : interpret X as a precomputed affinity matrix.

‘precomputed_nearest_neighbors’ : interpret X as a sparse graph of precomputed nearest neighbors, and 
constructs the affinity matrix by selecting the n_neighbors nearest neighbors.

one of the kernels supported by pairwise_kernels.

Only kernels that produce similarity scores (non-negative values that increase with similarity) should be used. 
This property is not checked by the clustering algorithm.

"""
# Uses NUM_CLUSTERS_LABEL
ASSIGN_LABELS_LABEL = "assign_labels"
ASSIGN_LABELS_LABEL_DEFAULT = "discretize"
AFFINITY_LABEL = "affinity"
AFFINITY_LABEL_DEFAULT = "rbf"
# Uses RANDOM_STATE_LABEL

# HDBSCAN Labels

"""

"""
DISTANCE_METRIC_LABEL = "distance_metric"
MIN_CLUSTER_SIZE_LABEL = "min_cluster_size"


# Possible Columns to Cluster:
# Used for Data Analysis Plots and Data Reading
HARDNESS_LABEL = "Hardness"
MODULUS_LABEL = "Modulus"

# File reading properties:
FILE_FORMAT_ONE = "format_1"
FILE_FORMAT_TWO = "format_2"


# Directory Defaults
CLUSTER_RESULTS_DIR = "/ClusterPlots"
RAND_INDEX_VISUALIZATION_DIR = "/RandIndexVisualization"
TEXT_FILE_DIR = "/TextFiles"
DATA_FILES_DIR = "../temp_clustered_data"
FRACTION_HISTOGRAMS_DIR = "/ClusterInfoHistograms"
DECONVOLUTION_SAVE_DIR = "/DeconvolutionPlots"
