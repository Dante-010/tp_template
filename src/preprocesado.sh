#!/bin/bash

INPUT_DATASET_URL="https://github.com/OpenNeuroDatasets/ds002785"
INPUT_DATASET2_URL="https://github.com/OpenNeuroDatasets/ds002790"
INPUT_FOLDER="input_data"
OUTPUT_FOLDER="output_data"
DATASET_NAME="brain_hemispheres_dataset"
DERIVATIVES_PATH="derivatives/vbm"

DATASET_URLS=("$INPUT_DATASET_URL" "$INPUT_DATASET2_URL")

export FSLOUTPUTTYPE=NIFTI_GZ

for i in "${!DATASET_URLS[@]}"; do
    
    datalad create ${DATASET_NAME}$i
    cd ${DATASET_NAME}$i

    datalad install -d . -s ${DATASET_URLS[i]} $INPUT_FOLDER
    datalad get $INPUT_FOLDER/$DERIVATIVES_PATH

    mkdir -p $OUTPUT_FOLDER/original
    mkdir -p $OUTPUT_FOLDER/zscore

    echo "Running python script..."

    cd ..
    python ./preprocess_brain_images.py ${DATASET_NAME}$i/$INPUT_FOLDER/$DERIVATIVES_PATH ${DATASET_NAME}$i/$OUTPUT_FOLDER
    
    mkdir -p ./matrix
    mkdir -p ./matrix/original
    mkdir -p ./matrix/zscore
    fslmerge -t ./matrix/merged_original$i.nii.gz ${DATASET_NAME}$i/output_data/original/*.nii.gz
    fslmerge -t ./matrix/merged_zscore$i.nii.gz ${DATASET_NAME}$i/output_data/zscore/*.nii.gz

    echo "Processing complete. Dataset $i is ready."
done
