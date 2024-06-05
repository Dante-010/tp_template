import os
import numpy as np
import pandas as pd

from julearn import run_cross_validation

matrix_file_paths = ["matrix/umap_embeddings_dataset0.npy", "matrix/umap_embeddings_dataset1.npy"]
script_dir = os.path.dirname(os.path.abspath(__file__))

def train_svm(matrix, idx, output_path=None):
    df = pd.DataFrame(matrix, columns=['dimension1', 'dimension2'])
    df['hemisphere'] = ['left' if i % 2 == 0 else 'right' for i in range(len(df))]

    X = ['dimension1', 'dimension2']
    y = 'hemisphere'

    scores = run_cross_validation(
        X=X,
        y=y,
        data=df,
        model='svm',
        problem_type='classification',
        pos_labels='left'
    )

    print(scores['test_score'])
    avg = np.mean(scores['test_score'])
    print(avg)

    out = f'./matrix/umap_test_scores{idx}.txt' if output_path is None else output_path

    with open(out, '+w') as fd:
        fd.write(str(scores['test_score']))
        fd.write('\n')
        fd.write(str(avg))

if __name__ == "__main__":
    for idx, path in enumerate(matrix_file_paths):
        matrix = np.load(path)
        train_svm(matrix, idx)

    print("All datasets processed.")