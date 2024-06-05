import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Define the indices and file paths
indices = range(2)
file_paths = {
    (0, 0): '../img/avg_lq_render{idx}.png',
    (1, 0): '../img/avg_lq_render{idx}_alt.png',
    (0, 1): '../img/significant_voxels{idx}.png',
    (1, 1): '../img/significant_voxels_alt{idx}.png',
    (0, 2): './plots/dsc_plot_dataset{idx}0.png',
    (1, 2): './plots/dsc_plot_dataset{idx}1.png'
}

# Column titles
column_titles = ['Laterality Quotient', 'T-test (TFCE)', 'Comparison with LQ at different thresholds']

for idx in indices:
    fig, axs = plt.subplots(2, 3, figsize=(20, 10))  # Make the figure wider
    fig.suptitle(f'Dataset {idx + 1}', fontsize=16)
    
    # Add column titles
    for col, title in enumerate(column_titles):
        axs[0, col].set_title(title, fontsize=14)
    
    for position, path_template in file_paths.items():
        row, col = position
        image_path = path_template.format(idx=idx)
        try:
            img = mpimg.imread(image_path)
            if col == 2:  # Make the third column images bigger
                axs[row, col].imshow(img)
                axs[row, col].axis('off')
                axs[row, col].set_xticks([])
                axs[row, col].set_yticks([])
            else:
                axs[row, col].imshow(img)
                axs[row, col].axis('off')
        except FileNotFoundError:
            print(f"File {image_path} not found.")
            axs[row, col].text(0.5, 0.5, 'Image not found', ha='center', va='center', fontsize=12)
            axs[row, col].axis('off')

    plt.tight_layout(rect=[0, 0, 1, 0.96])  # Adjust layout to make room for the main title
    plt.savefig(f'./plots/figure2_{idx}.png')
