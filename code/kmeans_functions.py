import os
import warnings

import numpy as np
import matplotlib.pyplot as plt

import seaborn as sns

import sklearn
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.preprocessing import minmax_scale
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA

os.environ["OMP_NUM_THREADS"] = "1"
warnings.simplefilter("ignore", UserWarning)


def create_graph(df, x_val, y_val, hue, title, x_size=10, y_size=10):
    # Plot warming_DF
    plt.figure(figsize=(x_size, y_size))
    sns.scatterplot(data=df, x=x_val, y=y_val, hue=hue).set_title(title)
    plt.show()


# Elbow method for determining number of clusters. Temp method, may be changed later
def elbow_method(data):
    wcss = []
    for i in range(1, 11):
        # k_means = KMeans(n_clusters = i, random_state = 10, n_init='auto').fit(data)
        k_means = KMeans(init="k-means++", n_clusters=i, n_init=5).fit(data)
        wcss.append(k_means.inertia_)

    # plot elbow curve
    plt.plot(np.arange(1, 11), wcss)
    plt.xlabel('Clusters')
    plt.ylabel('SSE')
    plt.show()


def silhouette_method(data):
    best_s = 0
    best_n = 0
    for n in range(2, 11):
        # k_means = KMeans(n_clusters = n, random_state = 10, n_init='auto').fit(data)
        k_means = KMeans(init="k-means++", n_clusters=n, n_init=5).fit(data)
        labels = k_means.fit_predict(data)

        # Shape data into a 2D array
        silhouette_avg = silhouette_score(data, labels)
        # print(
        #     "For n_clusters =",
        #     n,
        #     "The average silhouette_score is :",
        #     silhouette_avg,
        # )

        if silhouette_avg > best_s:
            best_s = silhouette_avg
            best_n = n
    print(
        "For n_clusters =",
        best_n,
        ", the average silhouette_score is :",
        best_s,
    )
    return best_n


# TODO: Create 3D graph
# TODO: Add code pulled from SKLEARN to showcase k-means
