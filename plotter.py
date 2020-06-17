import matplotlib.pyplot as plt
import numpy as np
import random


class Plotter:

    def __init__(self):
        super().__init__()
        self.labels_color_map = {}

    def plot_k_distance(self, data, k=2):
        from sklearn.neighbors import NearestNeighbors
        
        print("k : %d" % k)

        # calculate the distance from each point to its closest neighbour
        neigh = NearestNeighbors(n_neighbors=k)  # number of neighbor
        nbrs = neigh.fit(data)

        # distances = the distance to the closest n_neighbors points
        # indices = the index for each of those points
        distances, indices = nbrs.kneighbors(data)

        # sort and plot distances
        distances = np.sort(distances, axis=0)
        distances = distances[:, 1]
        plt.subplot(1, 2, 1)
        plt.plot(distances)

        # eliminate distances with 0 value not to stick
        distances = [distance for distance in distances if distance > 0.0]
        
        y = distances
        x = range(1, len(y)+1)
        
        from kneed import KneeLocator
        kn = KneeLocator(x, y, curve='concave', direction='increasing')
        
        max_indices_y = []
        for max_index in kn.maxima_indices:
            max_indices_y.append(distances[max_index])
            
        second_derivative = np.diff(max_indices_y, n=2)
        
        # find maxima index with the highest second derivative
        i = np.argmax(second_derivative)
        print("Second derivative :")
        print(i)
        print(distances[i]) # y value of index
        
        # plotting
        plt.subplot(1, 2, 2)
        plt.plot(x, y)
        plt.hlines(distances[i], plt.xlim()[0], plt.xlim()[1], linestyles='dashed')
        plt.tight_layout()
        plt.show()
        
        return round(distances[i], 2)

    def __get_color(self, index):
        if not (index in self.labels_color_map):
            def r(): return random.randint(0, 255)
            self.labels_color_map[index] = ('#%02X%02X%02X' % (r(), r(), r()))
        return self.labels_color_map[index]

    # plots clusters obtained from dbscan, black points for noise, other colors for clusters
    def plot_cluster(self, cluster, sample_matrix, title):
        from sklearn.decomposition import PCA
        from sklearn.manifold import TSNE
        from sklearn.preprocessing import StandardScaler
        from matplotlib.colors import ListedColormap

        pca_num_components = 2
        labels = cluster.labels_
        X = sample_matrix.values
        reduced_data = PCA(n_components=pca_num_components).fit_transform(X)

        _, ax = plt.subplots()
        x_ax = []
        y_ax = []

        classes = list(set(labels))
        
        if(-1 in classes):
            classes.remove(-1)
        
        for index, _ in enumerate(reduced_data):
            
            pca_comp_1, pca_comp_2 = reduced_data[index]
            if labels[index] == -1:
                ax.scatter(pca_comp_1, pca_comp_2, c='#000000', label=f"Cluster {labels[index]}", zorder=0)
                continue
            color = self.__get_color(labels[index])

            x_ax.append(pca_comp_1)
            y_ax.append(pca_comp_2)
            
            """else:
                ax.scatter(pca_comp_1, pca_comp_2, c=color, label=f"Cluster {labels[index]}", zorder=10)
            """
        colors = ListedColormap(self.labels_color_map.values())
        
        import matplotlib.patches as mpatches
        patches = []
        c = [value for value in labels if value != -1]
        for i in range(len(self.labels_color_map.values())):
            patches.append(mpatches.Patch(color=list(self.labels_color_map.values())[i], label=classes[i]))


        scatter = plt.scatter(x_ax, y_ax,c=c, cmap=colors)
        ax.grid(False)
        
        y_len = 0.0
        if(len(classes) > 12):
             y_len = 1.15 + len(classes) / 12 * 0.04
        else:
             y_len = 1.15
             
        plt.legend(bbox_to_anchor=(0., y_len, 1., .102), ncol=12, loc='center', 
                   handles=patches, labels=classes, title="Clusters")
        plt.title(title)
        plt.show()

        
        
"""        
# plots clusters obtained from dbscan, black points for noise, other colors for clusters
def plot_cluster(cluster, sample_matrix):
    from sklearn.preprocessing import StandardScaler

    # standardize matrix by removing the mean and scaling to unit variance
    #sample_matrix = StandardScaler().fit_transform(sample_matrix)
    
    # get matrix shape 
    core_samples_mask = np.zeros_like(cluster.labels_, dtype=bool)
    
    # mark core points of clusters
    core_samples_mask[cluster.core_sample_indices_] = True
    labels = cluster.labels_

    # number of clusters in labels, ignoring noise if present. 
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0) 
    
    # Black removed and is used for noise instead
    unique_labels = set(labels)

    # assign colors to each unique label
    colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
    
    for k, col in zip(unique_labels, colors):

        # make noises black color
        if k == -1:
            col = 'k'

        # make elements of cluster True
        class_member_mask = (labels == k)  # generator comprehension
        
        # X is your data matrix
        X = np.array(sample_matrix)

        # core points in this cluster
        xy = X[class_member_mask & core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
                 markeredgecolor='k', markersize=14)

        # non-core points in this cluster
        #xy = X[class_member_mask & ~core_samples_mask]
        #plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
         #        markeredgecolor='k', markersize=6)

    plt.title('number of clusters: %d' %n_clusters_) 
    plt.show()
    """