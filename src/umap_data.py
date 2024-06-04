import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import umap

# Para poder asegurarnos que siempre obtenemos los mismos datos, seteamos una seed.
reducer = umap.UMAP(random_state=1000)
matrix_file_paths = ["matrix/zscore/dataset0.npy", "matrix/zscore/dataset1.npy"]
script_dir = os.path.dirname(os.path.abspath(__file__))

if not(os.path.exists('./plots')):
    os.makedir('./plots')

for idx, path in enumerate(matrix_file_paths):
    matrix = np.load(path)    
    embedding = reducer.fit_transform(matrix)    
    np.save(os.path.join(script_dir, 'matrix', f'umap_embeddings_dataset{idx}.npy'), embedding)
    print(f"UMAP embeddings for dataset {idx + 1} saved successfully.")

    # Labels para los hemisferios
    labels = np.array(['left' if i % 2 == 0 else 'right' for i in range(embedding.shape[0])])

    plt.figure(figsize=(14, 7))
    
    # KDE plot
    plt.subplot(1, 2, 1)
    sns.kdeplot(x=embedding[:, 0], y=embedding[:, 1], hue=labels, thresh=.3)
    plt.title(f'KDEPlot {idx + 1}')
    plt.xlabel('dimension1')
    plt.ylabel('dimension2')
    plt.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)

    # Scatterplot
    plt.subplot(1, 2, 2)
    sns.scatterplot(x=embedding[:, 0], y=embedding[:, 1], hue=labels)
    plt.title(f'Scatterplot {idx + 1}')
    plt.xlabel('dimension1')
    plt.ylabel('dimension2')
    plt.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
    
    plt.tight_layout()
    plt.savefig(os.path.join(script_dir, 'plots', f'umap_plots_dataset{idx}.png'))

print("All datasets processed.")