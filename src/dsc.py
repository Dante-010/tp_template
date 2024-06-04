import numpy as np
import pandas as pd
import os

from scipy.spatial.distance import dice
from nilearn.image import load_img, get_data, index_img, new_img_like


for i in range(1):
    lq = load_img(f'./matrix/avg_laterality_quotient_dataset{i}.nii.gz')
    t_test = load_img(f'./fsl/lq_output_dataset{i}_tfce_corrp_tstat1.nii.gz')
    boruta = load_img(f'./matrix/boruta_voxels{i}.nii.gz')

    for thresh in range(0, 0.6, 0.2):



script_dir = os.path.dirname(os.path.abspath(__file__))



print("All datasets processed.")