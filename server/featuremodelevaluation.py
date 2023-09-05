import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.feature_selection import RFE, RFECV
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.pipeline import make_pipeline

# evaluate a give model using cross-validation
def function(models, X_train, y_train):
    scores=[]
    for i in models:
        cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)
        score = cross_val_score(models[i], X_train, y_train, scoring='accuracy', cv=cv, n_jobs=-1, error_score='raise')
        scores.append(score.mean())
    tmp = max(scores)
    index = scores.index(tmp)
    #print (index)
    return models[str(index)]