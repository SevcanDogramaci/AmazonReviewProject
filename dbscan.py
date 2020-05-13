from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans

import hdbscan

class DbScan:
    @staticmethod
    def performDbScan(data):
        clusters = DBSCAN(min_samples=5, eps=0.3).fit(data)
        print(len(set(clusters.labels_)) - (1 if -1 in clusters.labels_ else 0))
        return clusters.labels_
    
class HDbScan(DbScan):
    @staticmethod
    def performDbScan(data):
        from sklearn.datasets import make_blobs

        clusterer = hdbscan.RobustSingleLinkage(cut=1, k=2)
        cluster_labels = clusterer.fit_predict(data)
        hierarchy = clusterer.cluster_hierarchy_
        alt_labels = hierarchy.get_clusters(0.100, 5)
        hierarchy.plot()
        return cluster_labels