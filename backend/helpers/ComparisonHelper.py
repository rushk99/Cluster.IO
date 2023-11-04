from helpers import CHI,DBI,SilhouetteCoefficient

def compare_cluster(datapoints,labels,metric):
    if metric=="calinski_harabasz_score":
        return CHI.chi(datapoints,labels)
    if metric=="davies_bouldin_score":
        return DBI.dbi(datapoints,labels)
    if metric=="silhouette_score":
        return SilhouetteCoefficient.silhouetteCoefficient(datapoints,labels)