import matplotlib.pyplot as plt
import numpy as np


def plot_k_distance(data):
    from sklearn.neighbors import NearestNeighbors
    import seaborn as sns

    sns.set()
    neigh = NearestNeighbors(n_neighbors=2)
    nbrs = neigh.fit(data)
    distances, indices = nbrs.kneighbors(data)
    distances = np.sort(distances, axis=0)
    distances = distances[:, 1]
    plt.plot(distances)


def plot_cluster(cluster, sample_matrix):
    from sklearn.preprocessing import StandardScaler

    sample_matrix = StandardScaler().fit_transform(sample_matrix)
    core_samples_mask = np.zeros_like(cluster.labels_, dtype=bool)
    core_samples_mask[cluster.core_sample_indices_] = True
    labels = cluster.labels_

    # Black removed and is used for noise instead.
    unique_labels = set(labels)
    colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = 'k'

        class_member_mask = (labels == k)  # generator comprehension
        # X is your data matrix
        X = np.array(sample_matrix)

        xy = X[class_member_mask & core_samples_mask]

        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
                 markeredgecolor='k', markersize=14)

        xy = X[class_member_mask & ~core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
                 markeredgecolor='k', markersize=6)

    plt.show()
    # plt.savefig('cluster.png')
