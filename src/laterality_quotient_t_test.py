import subprocess
import os

def run_randomise(data_matrix_file, design_file, output_prefix, num_permutations=5000, cluster_threshold=2.3, p_threshold=0.05):
    # Convert numpy matrix to NIfTI format
    convert_command = f"fslmaths {data_matrix_file} {data_matrix_file.replace('.npy', '.nii.gz')}"
    subprocess.run(convert_command, shell=True)
    
    # Create design file if not present
    if not os.path.exists(design_file):
        with open(design_file, 'w') as f:
            f.write("1\n")
    
    # Run randomise command
    # randomise_command = f"randomise -i {data_matrix_file.replace('.npy', '.nii.gz')} -o ./matrix/{output_prefix} -d {design_file} -1 -T -n {num_permutations} -x -C {cluster_threshold} --cluster --cluster-localthresh --cluster-connectivity --atlasquery -x -1 {p_threshold}"
    subprocess.run(randomise_command, shell=True)

    print("Randomise completed successfully.")

# Example usage
data_matrix_file = "data_matrix.npy"
design_file = "design.txt"
output_prefix = "output"
num_permutations = 5000
cluster_threshold = 2.3
p_threshold = 0.05

run_randomise(data_matrix_file, design_file, output_prefix, num_permutations, cluster_threshold, p_threshold)
