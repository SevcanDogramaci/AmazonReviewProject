import matplotlib.pyplot as plt
import numpy as np
import random


class Plotter:

    def __init__(self):
            super().__init__()
            self.labels_color_map = { 0: '#F00000',
                                    1: '#00F000',
                                    2: '#0000F0',
                                    3: '#f08c14',
                                    4: '#f014f0',
                                    5: '#f0dc28',
                                    6: '#a028dc',
                                    7: '#00b4f0',
                                    8: '#007814',
                                    9: '#a05000'}

    def plot_k_distance(self, data, k=2):
        from sklearn.neighbors import NearestNeighbors
        title = 'K-distance'
        x_label = 'distance no'
        y_label = 'distance'
        
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
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)

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
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.hlines(distances[i], plt.xlim()[0], plt.xlim()[1], linestyles='dashed')
        plt.tight_layout()
        plt.savefig('k_distance.jpg')
        plt.show()
   
        
        return round(distances[i], 2)

    def __get_color(self, index):
        if not (index in self.labels_color_map):
            #def r(): return random.randint(0, 255)
            def r(): return random.randrange(0,255,20)
            color = ('#%02X%02X%02X' % (r(), r(), r()))
            if color in self.labels_color_map.values():
                return self.__get_color(index)
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
        x_ax_label = "PCA component 1"
        y_ax_label = "PCA component 2"

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
            
        colors = ListedColormap(self.labels_color_map.values())
        
        import matplotlib.patches as mpatches
        patches = []
        c = [value for value in labels if value != -1]
        for i in range(len(classes)):
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
        plt.xlabel(x_ax_label)
        plt.ylabel(y_ax_label)

        plt.savefig(title.replace(" ", "").replace(":", "_")+'.jpg', bbox_inches='tight')
        plt.show()