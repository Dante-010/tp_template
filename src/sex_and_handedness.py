import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import umap

from nilearn.image import load_img, get_data, index_img, new_img_like

from julearn import run_cross_validation
from julearn.utils import configure_logging
from julearn.config import set_config 

from umap_svm import train_svm
from lasso_boruta import train_lasso

configure_logging("INFO")
set_config('disable_x_check', True)
set_config('disable_xtypes_check', True)

data_dirs = ["brain_hemispheres_dataset0", "brain_hemispheres_dataset1"]
matrix_file_paths = ["matrix/zscore/dataset0.npy", "matrix/zscore/dataset1.npy"]
script_dir = os.path.dirname(os.path.abspath(__file__))
reducer = umap.UMAP(random_state=1000)
msg_list = []

def process_subjects_by_attribute(df, attribute, i):
    unique_values = df[attribute].unique()
    for value in unique_values:
        if value in [np.nan, 'ambidextrous']:
            continue

        attribute_df = df[df[attribute] == value]
        participant_ids = attribute_df['participant_id'].tolist()

        matrix_path = matrix_file_paths[i]
        matrix = np.load(matrix_path)
        
        filter_indices = np.array([pid in participant_ids for pid in df['participant_id'] for _ in range(2)])
        filtered_matrix = matrix[filter_indices]

        category_msg = f'Dataset {i}: {value} {len(filtered_matrix)}'
        print(category_msg)
        msg_list.append(category_msg)

        print("Fitting UMAP")
        embedding = reducer.fit_transform(filtered_matrix)
        plot_embedding(embedding, attribute_df, f'{attribute} | {value}', i)

        print("Training SVM")
        train_svm(embedding, i, output_path=f'./matrix/umap_test_scores{i}_{attribute}_{value}.txt')
        print("Training Lasso")
        train_lasso(filtered_matrix, i, output_path=f'./matrix/lasso_test_scores{i}_{attribute}_{value}.txt')

def plot_embedding(embedding, df, attribute, idx):
    labels = np.array(['left' if i % 2 == 0 else 'right' for i in range(embedding.shape[0])])

    plt.figure(figsize=(7, 7))

    sns.scatterplot(x=embedding[:, 0], y=embedding[:, 1], hue=labels, alpha=0.5, legend=False)
    plt.title(f'Scatterplot and KDEPlot Overlay Dataset {idx + 1} ({attribute})')
    plt.xlabel('dimension1')
    plt.ylabel('dimension2')
    plt.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)

    sns.kdeplot(x=embedding[:, 0], y=embedding[:, 1], hue=labels, thresh=.3, alpha=0.5, legend=False)

    plt.tight_layout()
    plt.savefig(os.path.join(script_dir, 'plots', f'umap_plots_dataset{idx}_{attribute}.png'))
    plt.close()

# ---- Main logic ----
for i, data_dir in enumerate(data_dirs):
    tsv_path = os.path.join(data_dir, "input_data", "participants.tsv")
    df = pd.read_csv(tsv_path, sep='\t')
    df = df[['participant_id', 'sex', 'handedness']]

    # df['sex'] = df['sex'].map({'M': 0, 'F': 1})
    # df['handedness'] = df['handedness'].map({'right': 0, 'left': 1})

    process_subjects_by_attribute(df, 'sex', i)
    process_subjects_by_attribute(df, 'handedness', i)


print(msg_list)
with open(f'./matrix/sex_and_handedness_info{i}', 'w') as fd:
    fd.write(str(msg_list))

print("All datasets processed.")