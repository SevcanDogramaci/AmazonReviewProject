from sklearn.cluster import DBSCAN
import hdbscan


class DbScan:
    def perform_db_scan(self, data, min_samples_val, eps_val):
        from sklearn import metrics
        clusters = DBSCAN(min_samples=min_samples_val,
                          eps=eps_val, n_jobs=-1).fit(data)
        labels = clusters.labels_
        n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
        n_noise_ = list(labels).count(-1)
        print("Eps: %0.2f  Min_samples: %d" % (eps_val, min_samples_val))
        print('Estimated number of clusters: %d' % n_clusters_)
        print('Estimated number of noise points: %d' % n_noise_)
        print("Silhouette Coefficient: %0.3f" %
              metrics.silhouette_score(data, labels))
        return clusters

    def perform_hdb_scan(self, data):
        from sklearn.datasets import make_blobs

        data, _ = make_blobs(1000)

        clusterer = hdbscan.RobustSingleLinkage(cut=0.125, k=7)
        cluster_labels = clusterer.fit_predict(data)
        hierarchy = clusterer.cluster_hierarchy_
        alt_labels = hierarchy.get_clusters(0.100, 5)
        hierarchy.plot()
        return cluster_labels