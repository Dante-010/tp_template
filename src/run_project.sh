#!/bin/bash

./preprocesado.sh
python create_data_matrices.py
python laterality_quotient_matrices.py
./laterality_quotient_t_test.sh