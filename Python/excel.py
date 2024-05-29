import pandas as pd

def copy_matching_columns(source_csv_path, target_csv_path, output_csv_path):
    """
    Copies data from matching columns in a source CSV file to a target CSV file.

    Args:
        source_csv_path (str): Path to the source CSV file.
        target_csv_path (str): Path to the target CSV file.
        output_csv_path (str): Path to the output CSV file where changes are saved.
    """

    # Load data with error handling
    try:
        source_df = pd.read_csv(source_csv_path)
        target_df = pd.read_csv(target_csv_path)
    except FileNotFoundError as e:
        print(f"Error: File not found: {e}")
        return

    # Find matching columns efficiently 
    matching_columns = list(set(source_df.columns) & set(target_df.columns))

    # Copy data and handle potential mismatches
    for col in matching_columns:
        if col in target_df.columns:  # Check if column exists for safety
            target_df[col] = source_df[col]
        else:
            print(f"Warning: Column '{col}' not found in target CSV")   

    # Save the modified target DataFrame
    try:
        target_df.to_csv(output_csv_path, index=False)
        print(f"Data copied to {output_csv_path} for matching columns: {matching_columns}")
    except PermissionError as e:
        print(f"Error: Unable to save file: {e}")


# Example usage of the function
source_csv_path = 'Complete_Intelligent_Transformed_Companies.csv'  # Replace with your source file path
target_csv_path = 'Company_Search_Results.csv'  # Replace with your target file path
output_csv_path = 'final.csv'  # Replace with desired output file path

# Uncomment the line below to execute the function with your file paths
copy_matching_columns(source_csv_path, target_csv_path, output_csv_path)
