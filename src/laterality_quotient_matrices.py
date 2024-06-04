import os
import numpy as np
from glob import glob
from nilearn.image import load_img, get_data, index_img, new_img_like

matrix_file_paths = ["matrix/merged_original0.nii.gz", "matrix/merged_original1.nii.gz"]
script_dir = os.path.dirname(os.path.abspath(__file__))

def compute_laterality_quotient(left_hemisphere, right_hemisphere):
    diff = right_hemisphere - left_hemisphere
    total = right_hemisphere + left_hemisphere
    laterality_quotient = np.where(total != 0, diff / total, 0)
    return laterality_quotient

for idx, path in enumerate(matrix_file_paths):
    matrix = load_img(path)
    laterality_quotient_images = []

    for i in range(0, matrix.shape[3], 2):
        print(f'{path} | subj {(i+2)//2}')

        left_hemisphere = get_data(index_img(matrix, i))
        right_hemisphere = get_data(index_img(matrix, i + 1))

        laterality_quotient = compute_laterality_quotient(left_hemisphere, right_hemisphere)
        laterality_quotient_images.append(laterality_quotient)

    # Combinamos las imagenes 3D en una imagen 4D
    laterality_quotient_4d = np.stack(laterality_quotient_images, axis=-1)
    output_path = os.path.join(script_dir, 'matrix', f'laterality_quotients_dataset{idx}.nii.gz')
    laterality_quotient_img = new_img_like(matrix, laterality_quotient_4d, copy_header=False)
    laterality_quotient_img.to_filename(output_path)
    print(f"4D laterality quotient image for dataset {idx} saved successfully.")

    # Miramos el primer archivo para determinar el formato de los datos originales
    input_folder = os.path.join(script_dir, f'brain_hemispheres_dataset{idx}/output_data/original/')
    nii_files = sorted(glob(os.path.join(input_folder, 'sub-0001*.nii.gz')))    
    first_img_path = nii_files[0]
    img = load_img(first_img_path)

    # Imagen LQ promedio
    avg_laterality_quotient = np.mean(laterality_quotient_4d, axis=-1)
    avg_output_path = os.path.join(script_dir, 'matrix', f'avg_laterality_quotient_dataset{idx}.nii.gz')
    avg_laterality_quotient_img = new_img_like(img, avg_laterality_quotient, copy_header=False)
    avg_laterality_quotient_img.to_filename(avg_output_path)
    print(f"Average laterality quotient image for dataset {idx} saved successfully.")

print("All datasets processed.")
