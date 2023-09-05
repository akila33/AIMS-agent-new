import numpy as np
import pandas as pd
import scanpy as sc
import matplotlib.pyplot as plt
import seaborn as sns

def function(file_path):
    adata = sc.read(file_path)
    
    adata_cpm = adata.copy()  # apply this to a copy so we can compare methods
    adata_cpm.raw = adata_cpm  # store a copy of the raw values before normalizing
    sc.pp.normalize_per_cell(adata_cpm, counts_per_cell_after=1e6)
    sc.pp.pca(adata_cpm)
    sc.pl.pca_overview(adata_cpm, color='mouse.id',save='_result.png')
    
    adata_cpm_ex = adata.copy() # make a copy so we can compare results
    sc.pp.normalize_total(adata_cpm_ex, target_sum=1e6, exclude_highly_expressed=True) # normalize
    sc.pp.pca(adata_cpm_ex) # run pca
    sc.pl.pca_overview(adata_cpm_ex,save='_normalisation.png') # plot pca
    
    not_Rn45s = adata_cpm.var.index != 'Rn45s'
    adata_no_Rn45s = adata_cpm[:, not_Rn45s]

    sc.pp.pca(adata_no_Rn45s)
    sc.pl.pca_overview(adata_no_Rn45s, color='mouse.id', save='_gene_normalisation.png')
    
    sc.pp.log1p(adata_cpm)  # Returns or updates data, depending on copy. X = log(X + 1) 
    sc.pp.scale(adata_cpm)  # Scale data to unit variance and zero mean.
    # updates adata with a scaled adata.X, annotated with 'mean' and 'std' in adata.var.
    sc.pp.pca(adata_cpm)  
    sc.pl.pca_overview(adata_cpm, color='plate.barcode',save='_plate_barcode_overview.png')
    
    path = 'results/brain_normalized.h5ad'
    adata_cpm.write(path)
    
    return path