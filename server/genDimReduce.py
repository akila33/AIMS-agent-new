from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
import numpy as np
import pandas as pd
import scanpy as sc
import matplotlib.pyplot as plt
import seaborn as sns

def function(path):
    adata = sc.read(path)
    
    sc.tl.tsne(adata, perplexity=30, learning_rate=1000, random_state=0)  # add X_tsne in obsm
    sc.pl.tsne(adata, color='cell_ontology_class',save='_cell_ontology_class.png')  # Plots using X_tsne which is tSNE coordinates of data.
    
    sc.pp.neighbors(adata) # UMAP is based on the neighbor graph; we'll compute this first
    # |_ Compute a neighborhood graph of observations
    # Depending on copy, updates or returns adata with the following: connectivities and distances.
    sc.tl.umap(adata, min_dist=0.5, spread=1.0, random_state=1, n_components=2)  # # add X_umap in obsm
    sc.pl.umap(adata, color='cell_ontology_class', save='_cell_ontology_class.png' )
    
    path = 'results/brain_embeddings.h5ad'
    adata.write(path)
    
    return path
    