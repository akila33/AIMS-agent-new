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
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import make_column_selector,make_column_transformer
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
#from autokeras import StructuredDataClassifier
def function(X):
    imp_median = SimpleImputer(strategy='median', add_indicator=True)
    scaler = StandardScaler()

    # set up preprocessing numeric columns
    imp_median = SimpleImputer(strategy='median', add_indicator=True)
    scaler = StandardScaler()

    # set up preprocessing categorical columns
    imp_constant = SimpleImputer(strategy='constant')
    ohe = OneHotEncoder(handle_unknown='ignore')

    # select columns by datatype
    num_cols = make_column_selector(dtype_include='number')
    cat_cols = make_column_selector(dtype_exclude='number')

    # do all preprocessing
    preprocessor = make_column_transformer(
        (make_pipeline(imp_median, scaler), num_cols),
        (make_pipeline(imp_constant, ohe), cat_cols)
    )
    
    mlmodel = LogisticRegression()
    models = dict()
    for i in range(2, len(X.columns)):
        rfe = RFE(estimator=mlmodel, n_features_to_select=i)
        pipeline = make_pipeline(preprocessor,rfe)
        #print(pipeline.named_steps['rfe'].ranking_[i],pipeline.named_steps['rfe'].support_[i])
        models[str(i)] = pipeline
    return [models]