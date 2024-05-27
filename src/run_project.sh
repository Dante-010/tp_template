#!/bin/bash

preprocesado.sh
python create_data_matrices.py
python laterality_quotient_matrices.py