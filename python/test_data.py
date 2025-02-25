import pandas as pd
import numpy as np
import os

def test_data(csv_file, required_columns=None):
    """Tests the data in the provided CSV file.

    Args:
        csv_file (str): Path to the CSV file.
        required_columns (list, optional): A list of column names to check for.
            If None, defaults to ['user_id', 'order_id', 'order_date', 'group', 'order_value'].

    Returns:
        bool: True if all tests pass, False otherwise.
    """

    try:
        df = pd.read_csv(csv_file)
        print(f"Successfully read CSV file: {csv_file}") # Check if CSV is read
        print(f"Columns in CSV: {df.columns.tolist()}")  # Display column names
    except FileNotFoundError:
        print(f"Error: File not found: {csv_file}")
        return False
    except pd.errors.EmptyDataError:
        print(f"Error: CSV file is empty: {csv_file}")
        return False
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return False

    # --- Define Default Required Columns if Not Provided ---
    if required_columns is None:
        required_columns = ['user_id', 'order_id', 'order_date', 'group', 'order_value']

    # --- Basic Data Checks ---
    print("Performing Basic Data Checks...")

    # 1. Check for required columns:
    if not all(col in df.columns for col in required_columns):
        missing_cols = [col for col in required_columns if col not in df.columns]
        print(f"Error: Missing required columns: {missing_cols}")
        return False
    print("Required columns present.")

    # 2. Check data types:
    if 'order_value' in df.columns:  # Only check if the column exists
        try:
            df['order_value'] = pd.to_numeric(df['order_value'])  # Ensure it's numeric
            print("'order_value' column is numeric.")
        except ValueError:
            print("Error: 'order_value' column is not numeric.")
            return False
    else:
        print("Warning: 'order_value' column not found, skipping numeric check.")  # Inform user

    # 3. Check 'group' values:
    if 'group' in df.columns:
        valid_groups = ['A', 'B']
        if not df['group'].isin(valid_groups).all():
            invalid_groups = df[~df['group'].isin(valid_groups)]['group'].unique()
            print(f"Error: Invalid 'group' values: {invalid_groups}")
            return False
        print("'group' column has valid values (A or B).")
    else:
         print("Warning: 'group' column not found, skipping group check.")

    # 4. Check for missing values (NaN):
    if df.isnull().values.any():
        print("Warning: Missing values (NaN) found in the data.")
        # Optionally, you can decide to fill them or drop them for testing:
        df.fillna(0, inplace=True)  # Example: Fill with 0
        print("Missing values filled with 0.")

    # --- A/B Group Specific Checks ---
    print("\nPerforming A/B Group Specific Checks...")

    # Conditionally check for 'group' column before proceeding
    if 'group' in df.columns:
        group_a = df[df['group'] == 'A']
        group_b = df[df['group'] == 'B']

        # 5. Check if both groups have data
        if len(group_a) == 0:
            print("Error: Group A has no data.")
            return False
        if len(group_b) == 0:
            print("Error: Group B has no data.")
            return False
        print("Both groups have data.")

        # 6. Basic AOV calculations (Only if 'order_value' exists)
        if 'order_value' in df.columns:
            aov_a = group_a['order_value'].mean()
            aov_b = group_b['order_value'].mean()
            print(f"Group A AOV: {aov_a:.2f}")
            print(f"Group B AOV: {aov_b:.2f}")

            # 7. Check if aov_b > aov_a (if you expect an increase)
            if aov_b < aov_a:
                print(f"Warning: Group B AOV is less than Group A AOV. Expected B > A given promotion.  Consider if data generation went as intended.")
        else:
            print("Skipping AOV calculations as 'order_value' column is missing.")

    else:
        print("Skipping A/B group-specific checks due to missing 'group' column.")

    # --- More checks can be added here depending on the specifics ---

    print("\nAll data tests passed!")
    return True

# --- Main Execution ---
if __name__ == "__main__":
    # Replace with the path to the relevant CSV file you want to test
    csv_file = r"C:\Users\praga\OneDrive\Documents\Projects\ecommerce-ab-test-analysis\data\variant_a_order_values.csv"  # Or variant_b_order_values.csv

    # Specify custom required columns (optional)
    # If you don't specify, it will use the default list
    # required_columns = ['user_id', 'order_id', 'order_date', 'variant', 'revenue']  # Example

    if not os.path.exists(csv_file):
        print(f"Error: File not found: {csv_file}")
    else:
        # Calling the function WITHOUT specifying required_columns will use defaults.
        if test_data(csv_file):
            print(f"Data in '{csv_file}' is valid.")
        else:
            print(f"Data in '{csv_file}' contains errors.")
