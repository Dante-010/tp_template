import os
import sys
import numpy as np
import nibabel as nib
from glob import glob

script_dir = os.path.dirname(os.path.abspath(__file__))

def z_score_standardize(data):
    mean = np.mean(data)
    std = np.std(data)
    standardized_data = (data - mean) / std
    return standardized_data

def save_matrix_as_img(matrix, affine, img_name, nii_file, original=False):
    img = nib.Nifti1Image(matrix, affine)
    dest = 'original' if original else 'zscore'
    output_path = os.path.join(output_folder, dest, f'{os.path.basename(os.path.dirname(nii_file))}_{img_name}.nii.gz')
    nib.save(img, output_path)

def process_brain_images(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    nii_files = sorted(glob(os.path.join(input_folder, 'sub*/*.nii.gz')))

    # Obtenemos informacion de la primer imagen
    img = nib.load(nii_files[0])
    # Utilizamos float32 debido a que input_data viene en ese formato
    data = img.get_fdata(dtype=np.float32)
    affine = img.affine
    x, y, z = data.shape
    affine[:3, 3] = affine[:3, 3] - np.array([x // 2, 0, 0])

    for nii_file in nii_files:
        img = nib.load(nii_file)
        data = img.get_fdata(dtype=np.float32)
        # Como ya sabemos que el cerebro esta centrado y ambos hemisferios son "simetricos"
        # consideramos la mitad del eje x para dividir. NO incluimos el midpoint.
        midpoint = x // 2

        left_hemisphere = data[:midpoint, :, :]
        right_hemisphere = data[midpoint + 1:, :, :]
        
        left_hemisphere_flipped = np.flip(left_hemisphere, axis=0)

        save_matrix_as_img(left_hemisphere_flipped, affine, 'left_flipped_original', nii_file, original=True)
        save_matrix_as_img(right_hemisphere, affine, 'right_original', nii_file, original=True)

        left_hemisphere_flipped = z_score_standardize(left_hemisphere_flipped)
        right_hemisphere = z_score_standardize(right_hemisphere)

        save_matrix_as_img(left_hemisphere_flipped, affine, 'left_flipped_z', nii_file)
        save_matrix_as_img(right_hemisphere, affine, 'right_z', nii_file)

        print(f'Processed {nii_file}: left_flipped and right hemispheres saved.')

if __name__ == "__main__":
    input_folder = sys.argv[1]
    output_folder = sys.argv[2]
    process_brain_images(input_folder, output_folder)