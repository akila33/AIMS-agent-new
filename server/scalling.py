"""
Scaling and transfer
"""
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import make_column_selector,make_column_transformer
from sklearn.pipeline import make_pipeline
def function():
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
    return preprocessor