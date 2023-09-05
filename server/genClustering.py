import numpy as np
import pandas as pd
import scanpy as sc
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
#from scanpy.tl import louvain

def function(path):
    adata = sc.read(path)
    n_c = len(adata.obs['cell_ontology_class'].unique())
    umap_coordinates = adata.obsm['X_umap'] # extract the UMAP coordinates for each cell
    kmeans = KMeans(n_clusters=n_c, random_state=0).fit(umap_coordinates) # fix the random state for reproducibility

    adata.obs['kmeans'] = kmeans.labels_ # retrieve the labels and add them as a metadata column in our AnnData object
    adata.obs['kmeans'] = adata.obs['kmeans'].astype(str)

    sc.pl.umap(adata, color='kmeans',save='_clusters.png') # plot the results, Ploting the umap with the color as the cluster label
    
    path = 'results/brain_clusters.h5ad'
    adata.write(path)
    
    return path

