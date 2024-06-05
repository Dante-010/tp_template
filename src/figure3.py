import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd

# Define the indices and file paths
indices = range(2)
file_paths = {
    (0, 0): './plots/umap_plots_dataset{idx}_sex | M.png',
    (1, 0): './plots/umap_plots_dataset{idx}_sex | F.png',
    (0, 1): './plots/umap_plots_dataset{idx}_handedness | right.png',
    (1, 1): './plots/umap_plots_dataset{idx}_handedness | left.png'
}

# Titles for the columns
column_titles = ['females vs males', 'right handed vs non-right handed']

# Paths to accuracy data files
accuracy_files = {
    './matrix/umap_test_scores{idx}_sex_F.txt': 'Female Accuracy',
    './matrix/umap_test_scores{idx}_sex_M.txt': 'Male Accuracy',
    './matrix/umap_test_scores{idx}_handedness_right.txt': 'Right Handed Accuracy',
    './matrix/umap_test_scores{idx}_handedness_left.txt': 'Left Handed Accuracy'
}

# Iterate over indices and create plots
for idx in indices:
    fig, axs = plt.subplots(2, 2, figsize=(10, 10))
    fig.suptitle(f'Dataset {idx + 1}', fontsize=16)

    for col in range(2):
        axs[0, col].set_title(column_titles[col])

    accuracy_file_paths = [k.format(idx=idx) for k in accuracy_files.keys()]
    count = 0

    for position, path_template in file_paths.items():
        row, col = position
        image_path = path_template.format(idx=idx)
    
        img = mpimg.imread(image_path)
        axs[row, col].imshow(img)
        axs[row, col].axis('off')

        accuracy_file_path = accuracy_file_paths[count]
        count += 1
        
        with open(accuracy_file_path, 'r') as file:
            lines = file.readlines()
            avg_accuracy = float(lines[-1].split()[-1])

            print(avg_accuracy)
        
        axs[row, col].text(0.05, 0.05, f'Avg. accuracy: {avg_accuracy:.2f}', 
            transform=axs[row, col].transAxes, fontsize=14, ha='left', va='bottom')

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(f'./plots/figure3_{idx}.png')