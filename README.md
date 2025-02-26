# E-commerce A/B Test Analysis: Optimizing Average Order Value

## Overview

This project analyzes the impact of a promotional campaign on Average Order Value (AOV) using A/B testing. It includes SQL scripts for generating data, and Python scripts for analysis.

## Project Structure

*   `ab_test_analysis.ipynb`: Jupyter Notebook with the analysis (interactive).
*   `sql/`: SQL scripts for data generation and querying.
*   `data/`: CSV files containing the A/B test data:
    *   `variant_a_order_values.csv`: Data for the control group.
    *   `variant_b_order_values.csv`: Data for the treatment group.
*   `scripts/`: Python scripts for data testing and A/B testing analysis.

## Prerequisites

*   Python 3 with the `pandas`, `scipy`, and `statsmodels` libraries. Install them using `pip install pandas scipy statsmodels`.

## Getting Started

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/pragadishprem/ecommerce-ab-test-analysis.git
    cd ecommerce-ab-test-analysis
    ```

2.  **Analyze the Data:**

    *   Run the Python A/B testing analysis script:

        ```bash
        cd scripts/
        python ab_test_analyzer.py ../data/variant_a_order_values.csv ../data/variant_b_order_values.csv
        ```

        This will print the A/B testing results to the console.

    *   (Optional) Explore the data interactively using the Jupyter Notebook:

        ```bash
        jupyter notebook ab_test_analysis.ipynb
        ```

        This will open the notebook in your web browser. Follow the instructions in the notebook to perform the analysis.

**Data Dictionary:**

*   `user_id`: Unique identifier for each customer.
*   `order_id`: Unique identifier for each order.
*   `order_date`: Date of the order.
*   `group`: 'A' (Control) or 'B' (Treatment/Campaign).
*   `order_value`: Total value of the order.
