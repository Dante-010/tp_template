import numpy as np
import pandas as pd
import os

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RepeatedKFold

from julearn import run_cross_validation
from julearn.utils import configure_logging
from julearn.config import set_config

from boruta import BorutaPy

matrix_file_paths = ["matrix/zscore/dataset0.npy", "matrix/zscore/dataset1.npy"]
script_dir = os.path.dirname(os.path.abspath(__file__))
configure_logging('INFO')
set_config('disable_x_check', True)

for idx, path in enumerate(matrix_file_paths):
    matrix = np.load(path) # Matriz NxV
    y = ['left' if i % 2 == 0 else 'right' for i in range(matrix.shape[0])]
    
    cols = [str(i) for i in range(matrix.shape[1])]

    # LASSO
    print(matrix.shape)
    df = pd.DataFrame(matrix, columns=cols)
    df['hemisphere'] = y

    # Utilizar LogisticRegression con penalty 'l1' es equivalente a utilizar LASSO,
    # para el caso de clasificacion en vez de regresion.
    log_reg = LogisticRegression(
        random_state=1000,
        penalty='l1',
        solver='liblinear',
    )

    scores = run_cross_validation(
        X=cols,
        y='hemisphere',
        data=df,
        problem_type='classification',
        model=log_reg,
        cv=RepeatedKFold(n_repeats=1, n_splits=3, random_state=1000),
    )

    print(scores['test_score'])

    with open(f'./matrix/lasso_test_scores{idx}.txt', '+w') as fd:
        fd.write(str(scores['test_score'])) 

    # Boruta
    X = matrix
    rf = RandomForestClassifier(random_state=1000)
    feat_selector = BorutaPy(rf, n_estimators='auto', verbose=2, random_state=1000)
    feat_selector.fit(X, y)
    
    print(feat_selector.ranking_[:100])
    print(feat_selector.support_[:100])

    X_filtered = feat_selector.transform(X)
    print(X_filtered)

    with open(f'./matrix/boruta_features{idx}.txt', '+w') as fd:
        fd.write(str(feat_selector.ranking_[:100])) 

print("All datasets processed.")