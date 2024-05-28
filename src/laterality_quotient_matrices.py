import os
import numpy as np
import nibabel as nib
from glob import glob

matrix_file_paths = ["matrix/zscore/dataset0.npy", "matrix/zscore/dataset1.npy"]

def compute_laterality_quotient(left_vector, right_vector):
    diff = right_vector - left_vector
    total = right_vector + left_vector
    # laterality_quotient = diff / total
    laterality_quotient = np.where(total != 0, diff / total, np.nan)

    return laterality_quotient

script_dir = os.path.dirname(os.path.abspath(__file__))

for idx, path in enumerate(matrix_file_paths):
    input_folder = os.path.join(script_dir, f'brain_hemispheres_dataset{idx}/output_data/original/')
    nii_files = sorted(glob(os.path.join(input_folder, 'sub-0001*.nii.gz')))
    
    if not nii_files:
        print(f"No NIfTI files found in {input_folder}. Skipping dataset {idx}.")
        continue
    
    # Miramos el primer archivo para determinar el formato de los datos originales
    first_img_path = nii_files[0]
    img = nib.load(first_img_path)
    data = img.get_fdata(dtype=np.float32)
    affine = img.affine
    x, y, z = data.shape

    matrix = np.load(path)
    laterality_quotient_images = []

    # for i in range(0, matrix.shape[0], 2):
    for i in range(0, 10, 2):    
        print(f'{path} | subj {i//2}')

        left_vector = matrix[i]
        right_vector = matrix[i + 1]

        laterality_quotient = compute_laterality_quotient(left_vector, right_vector)
        laterality_quotient_images.append(laterality_quotient.reshape((x, y, z)))

    # Unimos todas las matrices 3D y guardamos una nueva imagen Nifti 4D
    laterality_quotient_4d = np.stack(laterality_quotient_images, axis=-1)
    output_path = os.path.join(script_dir, 'matrix', f'laterality_quotients_dataset{idx}.nii.gz')

    print(affine)
    new_affine = np.eye(4)
    new_affine[:3, :3] = affine[:3, :3]
    new_affine[:3, 3] = affine[:3, 3]
    print(new_affine)
    nib.save(nib.Nifti1Image(laterality_quotient_4d, new_affine), output_path)

    print(f"4D laterality quotient image for dataset {idx} saved successfully.")

print("All datasets processed.")
