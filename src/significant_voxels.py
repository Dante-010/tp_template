import os
import numpy as np
from glob import glob
from nilearn.image import load_img, get_data, new_img_like

matrix_file_paths = ["./fsl/lq_output_dataset0_tfce_corrp_tstat1.nii.gz", "./fsl/lq_output_dataset0_tfce_corrp_tstat1.nii.gz"]
script_dir = os.path.dirname(os.path.abspath(__file__))

for idx, path in enumerate(matrix_file_paths):
    img = load_img(path)
    data = get_data(img)
    data[data < 0.95] = 0
    significant_voxels = new_img_like(img, data)
    significant_voxels.to_filename(f'./matrix/significant_voxels{idx}.nii.gz')

print("All datasets processed.")