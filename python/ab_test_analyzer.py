import pandas as pd
from scipy import stats
import os

def analyze_ab_test_from_separate_csvs(csv_url_a, csv_url_b):
    """
    Performs A/B testing analysis on order values from two separate CSV files,
    handling different file paths and column name variations.

    Args:
        csv_url_a (str): URL to the CSV file containing order values for Variant A.
        csv_url_b (str): URL to the CSV file containing order values for Variant B.
    """

    try:
        # 1. Load the CSV files into Pandas DataFrames
        df_a = pd.read_csv(csv_url_a)
        df_b = pd.read_csv(csv_url_b)

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
        print(f"Error: Could not find a valid order value column in {csv_url_a}. Checked for order_value, order_value_a, value, and OrderTotal")
        return

    if not order_value_col_b:
        print(f"Error: Could not find a valid order value column in {csv_url_b}. Checked for order_value, order_value_b, value, and OrderTotal")
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
            print(f"Variant B (the promotional campaign) had a significantly higher AOV (AOV_A = {aov_a:.2f}, AOV_B = {aov_b:.2f}, p-value = {p_value:.3f})."
                  f" We reject the null hypothesis. This suggests that the promotional campaign had a positive impact on AOV.")
        else:
            print(f"Variant A had a significantly higher AOV (unexpected)(AOV_A = {aov_a:.2f}, AOV_B = {aov_b:.2f}, p-value = {p_value:.3f})."
                  f"We reject the null hypothesis. Further investigation needed")
    else:
        print(f"\nThe difference in AOV is not statistically significant (p-value = {p_value:.3f})."
              f" We fail to reject the null hypothesis. We cannot conclude that the promotional campaign had a significant impact on AOV.")
        if aov_b > aov_a:
            print("Variant B (the promotional campaign) had a higher AOV although not statistically significant, so there is some evidence of improvement.")
        else:
            print("Variant A performed higher than Variant B (unexpected)")

if __name__ == "__main__":
    # Replace with the Raw URLs from your GitHub repository:
    csv_url_a = "https://raw.githubusercontent.com/pragadishprem/ecommerce-ab-test-analysis/main/data/variant_a_order_values.csv"
    csv_url_b = "https://raw.githubusercontent.com/pragadishprem/ecommerce-ab-test-analysis/main/data/variant_b_order_values.csv"

    analyze_ab_test_from_separate_csvs(csv_url_a, csv_url_b)
