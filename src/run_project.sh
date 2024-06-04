#!/bin/bash

./preprocesado.sh
python create_data_matrices.py
python laterality_quotient_matrices.py
./laterality_quotient_t_test.sh
python umap_data.py
python umap_svm.py
python lasso_boruta.py
python dsc.py
python sex_and_handedness.py