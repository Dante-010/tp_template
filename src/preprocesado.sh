#!/bin/bash

INPUT_DATASET_URL="https://github.com/OpenNeuroDatasets/ds002785"
INPUT_FOLDER="input_data"
OUTPUT_FOLDER="output_data"
DATASET_NAME="brain_hemispheres_dataset"
DERIVATIVES_PATH="derivatives/vbm"

datalad create $DATASET_NAME
cd $DATASET_NAME

datalad install -d . -s $INPUT_DATASET_URL $INPUT_FOLDER
datalad get $INPUT_FOLDER/$DERIVATIVES_PATH

mkdir -p $OUTPUT_FOLDER

echo "Running python script..."
python ../process_brain_images.py $INPUT_FOLDER/$DERIVATIVES_PATH $OUTPUT_FOLDER

datalad save -m "Processed brain images: split hemispheres and flipped left hemisphere" $OUTPUT_FOLDER
echo "Processing complete. Dataset is ready."
