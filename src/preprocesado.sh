#!/bin/bash

INPUT_DATASET_URL="https://github.com/OpenNeuroDatasets/ds002785"
INPUT_DATASET2_URL="https://github.com/OpenNeuroDatasets/ds002790"
INPUT_FOLDER="input_data"
OUTPUT_FOLDER="output_data"
DATASET_NAME="brain_hemispheres_dataset"
DERIVATIVES_PATH="derivatives/vbm"

DATASET_URLS=("$INPUT_DATASET_URL" "$INPUT_DATASET2_URL")

for i in "${!DATASET_URLS[@]}"; do
    
    datalad create ${DATASET_NAME}$i
    cd ${DATASET_NAME}$i

    datalad install -d . -s ${DATASET_URLS[i]} $INPUT_FOLDER
    datalad get $INPUT_FOLDER/$DERIVATIVES_PATH

    mkdir -p $OUTPUT_FOLDER

    echo "Running python script..."
    python ../preprocess_brain_images.py $INPUT_FOLDER/$DERIVATIVES_PATH $OUTPUT_FOLDER

    datalad save -m "Processed brain images: split hemispheres and flipped left hemisphere" $OUTPUT_FOLDER

    echo "Processing complete. Dataset $i is ready."
    
    cd ..
done
