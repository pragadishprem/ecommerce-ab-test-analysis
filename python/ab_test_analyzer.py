import pandas as pd
from scipy import stats
import os

def analyze_ab_test_from_separate_csvs(csv_file_a, csv_file_b):
    """
    Performs A/B testing analysis on order values from two separate CSV files,
    handling different file paths and column name variations.

    Args:
        csv_file_a (str): Path to the CSV file containing order values for Variant A.
        csv_file_b (str): Path to the CSV file containing order values for Variant B.
    """

    try:
        # 1. Load the CSV files into Pandas DataFrames
        df_a = pd.read_csv(csv_file_a)
        df_b = pd.read_csv(csv_file_b)

    except FileNotFoundError as e:
        print(f"Error: One or more CSV files not found: {e}")
        return
    except pd.errors.EmptyDataError as e:
        print(f"Error: One or more CSV files are empty: {e}")
        return
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    # 2. Determine order value column name.  If it doesn't exist in df, function exits
    order_value_col_a = None
    for col in ['order_value', 'order_value_a', 'value', 'OrderTotal']:
        if col in df_a.columns:
            order_value_col_a = col
            break

    order_value_col_b = None
    for col in ['order_value', 'order_value_b', 'value', 'OrderTotal']:
        if col in df_b.columns:
            order_value_col_b = col
            break

    if not order_value_col_a:
        print(f"Error: Could not find a valid order value column in {csv_file_a}. Checked for order_value, order_value_a, value, and OrderTotal")
        return

    if not order_value_col_b:
        print(f"Error: Could not find a valid order value column in {csv_file_b}. Checked for order_value, order_value_b, value, and OrderTotal")
        return

    # 3. Extract Order Values from Each DataFrame using auto-detected column names
    group_a = df_a[order_value_col_a]
    group_b = df_b[order_value_col_b]

    # 4. Perform the Independent Samples T-Test (Welch's T-test)
    #  - Equal variance is NOT assumed, so we use Welch's t-test.
    #  - alternative='two-sided' specifies a two-tailed test.
    t_statistic, p_value = stats.ttest_ind(group_a, group_b, equal_var=False, alternative='two-sided')

    # 5. Calculate the Average Order Value (AOV) for each Variant
    aov_a = group_a.mean()
    aov_b = group_b.mean()

    # 6. Print the Results
    print("Variant A AOV:", aov_a)
    print("Variant B AOV:", aov_b)
    print("T-Statistic:", t_statistic)
    print("P-Value:", p_value)

    # 7. Interpret the Results
    alpha = 0.05  # Significance level (common choice)

    if p_value <= alpha:
        print("\nThe difference in AOV is statistically significant.")
        if aov_b > aov_a:
            print("Variant B (the promotional campaign) had a significantly higher AOV.")
        else:
            print("Variant A had a significantly higher AOV (unexpected).")
    else:
        print("\nThe difference in AOV is not statistically significant.")
        print("We cannot conclude that the promotional campaign had a significant impact on AOV.")

if __name__ == "__main__":
    # Example Usage (Replace with your actual file paths)

    # Use raw strings to handle backslashes correctly on Windows
    csv_file_a = r"C:\Users\praga\OneDrive\Documents\Projects\ecommerce-ab-test-analysis\data\variant_a_order_values.csv"
    csv_file_b = r"C:\Users\praga\OneDrive\Documents\Projects\ecommerce-ab-test-analysis\data\variant_b_order_values.csv"

    # Check if the files exist
    if not os.path.exists(csv_file_a):
        print(f"Error: File not found: {csv_file_a}")
    elif not os.path.exists(csv_file_b):
        print(f"Error: File not found: {csv_file_b}")
    else:
        analyze_ab_test_from_separate_csvs(csv_file_a, csv_file_b)
