import numpy as np
import pandas as pd
import scanpy as sc
import matplotlib.pyplot as plt
import seaborn as sns

def function(two_csvfiles):
    files = two_csvfiles.split(',')
    # This might take a minute.
    count_dataframe = pd.read_csv(files[0],index_col=0)  # use the first column to label the rows (the 'index')
    metadata_dataframe = pd.read_csv(files[1], index_col=0)
    #print('csv files loaded')
    adata = sc.AnnData(X = count_dataframe, obs = metadata_dataframe)
    #print('AnnData shape: ',adata.shape)
    is_spike_in = {}
    number_of_spike_ins = 0

    for gene_name in adata.var_names:
        if 'ERCC' in gene_name:
            is_spike_in[gene_name] = True # record that we found a spike-in
            number_of_spike_ins += 1 # bump the counter
        else:
            is_spike_in[gene_name] = False # record that this was not a spike-in
        
    adata.var['ERCC'] = pd.Series(is_spike_in) # because the index of adata.var and the keys of is_spike_in match, anndata will take care of matching them up
    #print('found this many spike ins: ', number_of_spike_ins)
    rpath = 'results/brain_raw.h5ad' 
    adata.write(rpath)
    return rpath