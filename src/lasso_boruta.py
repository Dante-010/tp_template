import numpy as np
import pandas as pd
import os

# import nibabel as nib

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RepeatedKFold
from sklearn.metrics import accuracy_score

from julearn import run_cross_validation
from julearn.utils import configure_logging
from julearn.config import set_config 

# from boruta import BorutaPy

matrix_file_paths = ["matrix/zscore/dataset0.npy", "matrix/zscore/dataset1.npy"]
configure_logging("INFO")
set_config('disable_x_check', True)
set_config('disable_xtypes_check', True)

def train_lasso(matrix, idx, output_path=None):
    mask = np.load(f'./matrix/non_zero_indices{idx}.npy')    
    print(matrix.shape)

    # Consideramos solo los pixeles de la mascara para que el calculo sea viable 
    # con los recursos computacionales que tenemos
    matrix = matrix[:,mask]
    print(matrix.shape)

    cols = [str(i) for i in range(matrix.shape[1])]
    df = pd.DataFrame(matrix, columns=cols)
    df['hemisphere'] = ['left' if i % 2 == 0 else 'right' for i in range(matrix.shape[0])]
    
    # Utilizar el modelo LogisticRegression con penatly 'l1' es equivalente a utilizar LASSO.
    log_reg = LogisticRegression(
        random_state=1000,
        penalty='l1',
        solver='liblinear',
        verbose=1
    )

    scores = run_cross_validation(
        X=cols,
        y='hemisphere',
        data=df,
        model=log_reg,
        problem_type='classification',
        cv=RepeatedKFold(n_repeats=1, n_splits=3, random_state=1000),
        pos_labels='left'
    )

    print(scores['test_score'])
    avg = np.mean(scores['test_score'])
    print(avg)


    out = f'./matrix/lasso_test_scores{idx}.txt' if output_path is None else output_path

    with open(out, '+w') as fd:
        fd.write(str(scores['test_score']))
        fd.write('\n')
        fd.write(str(avg))

    # Boruta Feature Selection
    # rf = RandomForestClassifier(n_jobs=-1, class_weight='balanced', max_depth=5, random_state=1000)
    # feat_selector = BorutaPy(rf, n_estimators='auto', verbose=2, random_state=1000)
    # feat_selector.fit(X, y)

    # chosen_voxels = np.zeros(X.shape[1], dtype=int)
    # chosen_voxels[feat_selector.support_] = 1
    
    # print(chosen_voxels)

    # boruta_img = chosen_voxels.reshape((45, 109, 91))

    # nii_img = nib.Nifti1Image(boruta_img, np.eye(4))
    # nib.save(nii_img, f'./matrix/boruta_voxels{idx}.nii.gz')

if __name__ == "__main__":
    for idx, path in enumerate(matrix_file_paths):
        matrix = np.load(path)
        train_lasso(matrix, idx)

    print("All datasets processed.")