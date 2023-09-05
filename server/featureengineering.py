import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.feature_selection import RFE, RFECV
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import TimeSeriesSplit, cross_validate
from sklearn import metrics
from sklearn.metrics import balanced_accuracy_score, make_scorer
from sklearn.datasets import make_classification
from sklearn.tree import DecisionTreeClassifier
#from autokeras import StructuredDataClassifier
def function(X,y,mlmodel,preprocessor):
    models = dict()
    for i in range(2, len(X.columns)):
        rfe = RFE(estimator=mlmodel, n_features_to_select=i)
        pipeline = make_pipeline(preprocessor,rfe)
        #print(pipeline.named_steps['rfe'].ranking_[i],pipeline.named_steps['rfe'].support_[i])
        models[str(i)] = pipeline
    return models