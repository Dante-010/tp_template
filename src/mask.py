import numpy as np
import pandas as pd
import os
import nibabel as nib

from nilearn.image import load_img, get_data, index_img

merged_paths = ["matrix/merged_original0.nii.gz", "matrix/merged_original1.nii.gz"]
avg_paths = ["matrix/avg_laterality_quotient_dataset0.nii.gz", "matrix/avg_laterality_quotient_dataset1.nii.gz"]

def create_nonzero_voxel_mask(input_image_path, output_mask_path):
    img = nib.load(input_image_path)
    data = img.get_fdata()

    mask_data = np.where(data != 0, 1, 0)
    mask_img = nib.Nifti1Image(mask_data, img.affine, img.header)
    
    nib.save(mask_img, output_mask_path)
    print(f"Mask saved to {output_mask_path}")

for idx, path in enumerate(merged_paths):
    matrix = load_img(path)
    non_zero_indices = set()

    for i in range(0, matrix.shape[3]):
        nifti_array = get_data(index_img(matrix, i))
        flattened_array = nifti_array.ravel()
        non_zero_indices.update(np.nonzero(flattened_array)[0])

    non_zero_indices = sorted(list(non_zero_indices))
    np.save(f'./matrix/non_zero_indices{idx}.npy', non_zero_indices)

    print(f'Mask {i} saved')
    print(non_zero_indices)

for idx, path in enumerate(merged_paths):
    create_nonzero_voxel_mask(path, f'./matrix/avg_lq_mask{idx}.nii.gz')

    print(f'Avg LQ mask {idx} saved')