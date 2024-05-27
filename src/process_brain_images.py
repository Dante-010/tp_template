import os
import sys
import numpy as np
import nibabel as nib
from glob import glob

def z_score_standardize(data):
    mean = np.mean(data)
    std = np.std(data)
    standardized_data = (data - mean) / std
    return standardized_data

def process_brain_images(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Get list of .nii.gz files in the input folder
    nii_files = glob(os.path.join(input_folder, 'sub*/*.nii.gz'))

    for nii_file in nii_files:
        img = nib.load(nii_file)
        data = img.get_fdata()
        affine = img.affine

        # data = z_score_standardize(data)

        x, y, z = data.shape

        # Como ya sabemos que el cerebro esta centrado y ambos hemisferios son "simetricos"
        # consideramos la mitad del eje x para dividir. En nuestro caso, x = 91, por lo tanto,
        # incluimos el 'midpoint' en ambos hemisferios
        midpoint = x // 2

        left_hemisphere = data[:midpoint + 1, :, :]
        right_hemisphere = data[midpoint:, :, :]

        left_hemisphere_flipped = np.flip(left_hemisphere, axis=0)

        # Save the left hemisphere flipped
        left_img = nib.Nifti1Image(left_hemisphere_flipped, affine)
        left_output_path = os.path.join(output_folder, f'{os.path.basename(os.path.dirname(nii_file))}_left_flipped.nii.gz')
        nib.save(left_img, left_output_path)

        # Save the right hemisphere
        right_img = nib.Nifti1Image(right_hemisphere, affine)
        right_output_path = os.path.join(output_folder, f'{os.path.basename(os.path.dirname(nii_file))}_right.nii.gz')
        nib.save(right_img, right_output_path)

        print(f'Processed {nii_file}: left_flipped and right hemispheres saved.')

if __name__ == "__main__":
    input_folder = sys.argv[1]
    output_folder = sys.argv[2]
    process_brain_images(input_folder, output_folder)
