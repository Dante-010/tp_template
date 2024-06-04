#!/bin/bash
mkdir -p ./fsl

export FSLOUTPUTTYPE=NIFTI_GZ

for i in {0..1} 
do
    randomise -i ./matrix/laterality_quotients_dataset${i}.nii.gz -o ./fsl/lq_output_dataset${i} -1 -T -n 1000 --debug --seed=1000
    fsl-cluster -i ./fsl/lq_output_dataset${i}_tfce_corrp_tstat1.nii.gz -t 0.95 --scalarname="1-p" > ./fsl/cluster_corrpdataset${i}.txt
done
