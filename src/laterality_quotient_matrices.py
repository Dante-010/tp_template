import numpy as np

matrix_file_paths = ["matrix/dataset0.npy", "matrix/dataset1.npy"]

def compute_laterality_quotient(left_vector, right_vector):
    # Subtract the left hemisphere from the right hemisphere
    difference = right_vector - left_vector
    
    # Compute the total sum of their values
    total_sum = np.sum(left_vector) + np.sum(right_vector)
    
    # Compute the laterality quotient
    laterality_quotient = difference / total_sum
    
    return laterality_quotient

for idx, path in enumerate(matrix_file_paths):
    matrix = np.load(path)
    
    # Initialize a list to store laterality quotient matrices
    laterality_quotients = []

    # Iterate over pairs of rows (representing both hemispheres)
    for i in range(0, matrix.shape[0], 2):
        # Get the left and right hemisphere vectors
        left_vector = matrix[i]
        right_vector = matrix[i + 1]
        
        # Compute laterality quotient for each pair of vectors
        laterality_quotient = compute_laterality_quotient(left_vector, right_vector)
        
        # Append the laterality quotient to the list
        laterality_quotients.append(laterality_quotient)

    # Concatenate all laterality quotient matrices along the first axis
    final_laterality_quotient_matrix = np.vstack(laterality_quotients)

    # Save the final laterality quotient matrix
    np.save(f"matrix/final_laterality_quotient_matrix{idx}.npy", final_laterality_quotient_matrix)

    print("Final laterality quotient matrix saved successfully.")