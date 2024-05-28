import os
import numpy as np
import pandas as pd
from nilearn.image import load_img
from glob import glob

script_dir = os.path.dirname(os.path.abspath(__file__))

def process_images(input_folder):
    # Ordenamos los archivos para tener los hemisferios de cada sujeto
    # de forma consecutiva.
    nii_files = sorted(glob(os.path.join(input_folder, '*.nii*')))
    
    vectors = []

    for i, nii_file in enumerate(nii_files):
        print(nii_file)

        img = load_img(nii_file)
        
        # Obtenemos los datos como una matriz 3D
        data = img.get_fdata(dtype=np.float32)

        # Pasamos la matriz a 1D
        vector = data.ravel()    

        vectors.append(vector)
    
    # Convertimos en matriz 2D (NxV)
    matrix = np.vstack(vectors)

    print(matrix.shape)

    return matrix

input_folders = ["brain_hemispheres_dataset0/output_data", "brain_hemispheres_dataset1/output_data"]

if not(os.path.exists('./matrix')):
    os.mkdir('./matrix')
    os.mkdir('./matrix/original')
    os.mkdir('./matrix/zscore')

for i, input_folder in enumerate(input_folders):
    print(f"Processing data from: {input_folder}")

    for folder in ['original', 'zscore']:
        matrix = process_images(os.path.join(input_folder, folder))

        # Guardamos la matriz como archivo para poder reutilizarla sin tener que hacer todo de vuelta.
        output_file = os.path.join(script_dir, 'matrix', folder, f'dataset{i}')
        np.save(output_file, matrix)
        
        print(f"Data matrix saved to: {output_file}")