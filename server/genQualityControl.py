import numpy as np
import pandas as pd
import scanpy as sc
import matplotlib.pyplot as plt
import seaborn as sns

def function(file_path):
    adata = sc.read(file_path)
    qc = sc.pp.calculate_qc_metrics(adata, qc_vars = ['ERCC'])# this returns a tuple of (cell_qc_dataframe, gene_qc_dataframe)
                                 # ask for the percentage of reads from spike ins
                                
    cell_qc_dataframe = qc[0]
    gene_qc_dataframe = qc[1]
    
    sns.jointplot(
        data=cell_qc_dataframe,
        x="log1p_total_counts",
        y="log1p_n_genes_by_counts",
        kind="hex",
    )
    plt.savefig('figures/2.1_cell_quality_control_dataframe.png')
    
    sns.histplot(cell_qc_dataframe["pct_counts_ERCC"])
    plt.savefig('figures/2.2_cell_quality_pct_counts_ERCC.png')
    
    plt.hist(cell_qc_dataframe['total_counts'], bins=1000)
    plt.xlabel('Total counts')
    plt.ylabel('N cells')
    plt.axvline(50000, color='red')
    plt.savefig('figures/2.3_total_number_of_reads_detected_per_cell.png')
    
    plt.hist(cell_qc_dataframe['n_genes_by_counts'], bins=100)
    plt.xlabel('N genes')
    plt.ylabel('N cells')
    plt.axvline(1000, color='red')
    plt.savefig('figures/2.4_count_total_numbers_unique_genes_detected_in_each_sample.png')
    
    plt.hist(cell_qc_dataframe['pct_counts_ERCC'], bins=1000)
    plt.xlabel('Percent counts ERCC')
    plt.ylabel('N cells')
    plt.axvline(10, color='red')
    plt.savefig('figures/2.5_ratio_between_ERCC_spikein_RNAs_and_endogenous_RNAs.png')
    
    low_ERCC_mask = (cell_qc_dataframe['pct_counts_ERCC'] < 10)
    adata = adata[low_ERCC_mask]
    sc.pp.filter_cells(adata, min_genes = 750)
    plt.savefig('figures/2.6_quality_control_filtering_outcome.png')
    
    path = 'results/brain_qc.h5ad'
    
    adata.write(path)
    
    return path
