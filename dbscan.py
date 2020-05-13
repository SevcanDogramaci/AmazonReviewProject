from sklearn.cluster import DBSCAN
import hdbscan

class DbScan:
    @staticmethod
    def performDbScan(data, min_samples_val, eps_val):
        clusters = DBSCAN(min_samples=min_samples_val, eps=eps_val).fit(data)
        labels = clusters.labels_
        n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
        n_noise_ = list(labels).count(-1)
        print('Estimated number of clusters: %d' % n_clusters_)
        print('Estimated number of noise points: %d' % n_noise_)
        return clusters
    
    
class HDbScan(DbScan):
    @staticmethod
    def performDbScan(data):
        from sklearn.datasets import make_blobs

        data, _ = make_blobs(1000)

        clusterer = hdbscan.RobustSingleLinkage(cut=0.125, k=7)
        cluster_labels = clusterer.fit_predict(data)
        hierarchy = clusterer.cluster_hierarchy_
        alt_labels = hierarchy.get_clusters(0.100, 5)
        hierarchy.plot()
        return cluster_labels