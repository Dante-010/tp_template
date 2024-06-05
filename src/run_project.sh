#!/bin/bash

./preprocess.sh

python create_data_matrices.py
python sex_and_handedness.py

python laterality_quotient_matrices.py
./laterality_quotient_t_test.sh
python significant_voxels.py

python umap_data.py
python umap_svm.py
python independent_t_test.py

python mask.py
python lasso_boruta.py

python dsc.py

python sex_and_handedness.py

python figure2.py
python figure3.py