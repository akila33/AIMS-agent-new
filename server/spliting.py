import numpy as np
from sklearn.model_selection import train_test_split
import pandas as pd
def function(dataset):
    X = dataset.drop(dataset.columns[-1], axis=1)
    y = dataset[dataset.columns[-1]].astype(int)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
    
    return [X_train, X_test, y_train, y_test]