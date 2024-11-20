import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas.api.types import is_numeric_dtype, is_categorical_dtype
import re

def sanitize_filename(filename):
    """
    Sanitize a string to be used as a valid filename.
    Replace invalid characters with underscores.
    """
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def analyze_data(data, output_file="analysis_report.html", dist_cols=None):
    """
    Function to analyze the dataset and create an HTML report with necessary steps.
    """
    # 1. Columns with missing values
    missing_columns = data.columns[data.isnull().any()].tolist()
    print(f"Columns with missing values: {missing_columns}")

    # 2. Categorize columns based on data type
    numeric_cols = [col for col in data.columns if is_numeric_dtype(data[col])]
    categorical_cols = [col for col in data.columns if is_categorical_dtype(data[col]) or data[col].dtype == 'object']
    print(f"Numeric columns: {numeric_cols}")
    print(f"Categorical columns: {categorical_cols}")

    # 3. Remove duplicate columns
    duplicate_columns = data.columns[data.T.duplicated()].tolist()
    print(f"Duplicate columns: {duplicate_columns}")
    data_cleaned = data.loc[:, ~data.columns.duplicated()]

    # 4. Remove constant columns
    constant_cols = [col for col in data_cleaned.columns if data_cleaned[col].nunique() == 1]
    print(f"Constant columns: {constant_cols}")
    data_cleaned = data_cleaned.drop(columns=constant_cols)

    # 5. Boxplots for numeric columns
    print("\nCreating boxplots for numeric columns...")
    boxplot_paths = []
    for col in numeric_cols:
        if col not in constant_cols:
            plt.figure(figsize=(6, 4))
            sns.boxplot(data=data_cleaned, x=col)
            plt.title(f"Boxplot for {col}")
            plot_path = sanitize_filename(f"{col}_boxplot.png")  # Sanitize filename
            plt.savefig(plot_path)
            boxplot_paths.append(plot_path)
            plt.close()

    # 6. Distribution charts for selected columns
    if dist_cols is None:
        dist_cols = data.columns[:6]  # Default to the first 6 columns
    print(f"\nCreating distribution plots for columns: {dist_cols}")
    distplot_paths = []
    for col in dist_cols:
        plt.figure(figsize=(6, 4))
        if is_numeric_dtype(data[col]):
            sns.histplot(data[col].dropna(), kde=True, bins=20, color="blue")
        elif is_categorical_dtype(data[col]) or data[col].dtype == 'object':
            sns.countplot(y=data[col], order=data[col].value_counts().index, palette="Set2")
        plt.title(f"Distribution of {col}")
        plot_path = sanitize_filename(f"{col}_distribution.png")  # Sanitize filename
        plt.savefig(plot_path)
        distplot_paths.append(plot_path)
        plt.close()

    # 7. Generate HTML report
    print("\nGenerating HTML report...")
    html_report = f"""
    <html>
    <head><title>Data Analysis Report</title></head>
    <body>
    <h1>Data Analysis Report</h1>
    <h2>1. Columns with Missing Values</h2>
    <ul>{"".join([f"<li>{col}</li>" for col in missing_columns])}</ul>
    <h2>2. Numeric Columns</h2>
    <ul>{"".join([f"<li>{col}</li>" for col in numeric_cols])}</ul>
    <h2>3. Categorical Columns</h2>
    <ul>{"".join([f"<li>{col}</li>" for col in categorical_cols])}</ul>
    <h2>4. Duplicate Columns</h2>
    <p>{duplicate_columns}</p>
    <h2>5. Constant Columns</h2>
    <p>{constant_cols}</p>
    <h2>6. Boxplots</h2>
    {"".join([f'<img src="{path}" width="400">' for path in boxplot_paths])}
    <h2>7. Distributions</h2>
    {"".join([f'<img src="{path}" width="400">' for path in distplot_paths])}
    </body>
    </html>
    """

    with open(output_file, "w") as f:
        f.write(html_report)
    print(f"\nHTML report saved as {output_file}")

# Example Usage
if __name__ == "__main__":
    df = pd.read_csv('python.csv')  # Replace with your dataset
    analyze_data(df, output_file="analysis_report.html", dist_cols=df.columns[:6])
