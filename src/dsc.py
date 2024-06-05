import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

from scipy.spatial.distance import dice
from nilearn.image import load_img, get_data

# Dado que dice() computa el coeficiente de 'disimilaridad', tomamos el complemento.
def dice_coefficient(img1, img2):
    data1 = img1.astype(bool)
    data2 = img2.astype(bool)
    return 1 - dice(data1.ravel(), data2.ravel())

script_dir = os.path.dirname(os.path.abspath(__file__))

value_ranges = [np.arange(0, 0.61, 0.02), np.arange(0, -0.61, -0.02)]
ticks = [np.arange(0, 0.61, 0.1), np.arange(0, -0.61, -0.1)]

for i in range(2):
    lq = get_data(load_img(f'./matrix/avg_laterality_quotient_dataset{i}.nii.gz'))
    t_test = get_data(load_img(f'./matrix/significant_voxels{i}.nii.gz'))

    for case, value_range in enumerate(value_ranges):
        results = {'Threshold': [], 'T-test': []}
        for thresh in value_range:
            lq_thresh = lq >= thresh

            dsc_t_test = dice_coefficient(lq_thresh, t_test)
            print(dsc_t_test)

            results['Threshold'].append(thresh)
            results['T-test'].append(dsc_t_test)

        df = pd.DataFrame(results)
        fig, ax = plt.subplots(figsize=(10, 6))
        bar_width = 0.3

        r1 = np.arange(len(df['Threshold'].unique()))
        r2 = [x + bar_width for x in r1]

        ax.bar(r1, df['T-test'], color='b', width=bar_width, edgecolor='grey', label='T-test')

        ax.set_xlabel('LQ Threshold', fontweight='bold')
        ax.set_ylabel('Dice Similarity Coefficient', fontweight='bold')
        
        major_ticks = ticks[i]
        ax.set_xticks(r1)
        ax.set_xticklabels([f'{tick:.2f}' for tick in df['Threshold']], rotation=45, ha='right')

        ax.legend()
        case_title = 'rightward' if case == 0 else 'leftward'
        # plt.title(f'Comparison with LQ at different thresholds (Dataset {i} | {case_title})')
        plt.savefig(os.path.join(script_dir, 'plots', f'dsc_plot_dataset{i}{case}.png'))