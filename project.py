import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas.api.types import is_numeric_dtype, is_categorical_dtype

def analyze_data(data, output_file="output_report.html"):
    """
    Function to analyze the dataset and create an HTML report with necessary steps.
    """
   
    missing_columns = data.columns[data.isnull().any()].tolist()
    print(f"Columns with missing values: {missing_columns}")

    
    numeric_cols = [col for col in data.columns if is_numeric_dtype(data[col])]
    categorical_cols = [col for col in data.columns if is_categorical_dtype(data[col]) or data[col].dtype == 'object']
    print(f"Numeric columns: {numeric_cols}")
    print(f"Categorical columns: {categorical_cols}")

    
    print("\nChecking for duplicate columns...")
    duplicates = data.T.duplicated()
    duplicate_columns = data.columns[duplicates]
    print(f"Duplicate columns: {duplicate_columns.tolist()}")
    data_cleaned = data.loc[:, ~data.columns.duplicated()]
    print(f"Removed duplicate columns. Columns before: {data.shape[1]}, Columns after: {data_cleaned.shape[1]}")

    
    print("\nChecking for constant columns...")
    constant_cols = [col for col in data.columns if data[col].nunique() == 1]
    print(f"Constant columns: {constant_cols}")
    data_cleaned = data_cleaned.drop(columns=constant_cols)
    print(f"Removed constant columns. Columns before: {data.shape[1]}, Columns after: {data_cleaned.shape[1]}")

    
    print("\nCreating boxplots for numeric columns...")
    for col in numeric_cols:
        if col not in constant_cols:
            plt.figure(figsize=(6, 4))
            sns.boxplot(data=data_cleaned, x=col)
            plt.title(f"Boxplot for {col}")
            plt.savefig(f"{col}_boxplot.png")
            plt.close()

    
    selected_cols = data.columns[:6] 
    print(f"\nCreating distribution plots for columns: {selected_cols}")
    for col in selected_cols:
        plt.figure(figsize=(6, 4))
        sns.histplot(data[col].dropna(), kde=True, bins=20)
        plt.title(f"Distribution of {col}")
        plt.savefig(f"{col}_distribution.png")
        plt.close()
    
    
    columns_for_distribution = data.columns[:6]  
    for col in columns_for_distribution:
        plt.figure(figsize=(10, 6))
        if is_numeric_dtype(data[col]):
            sns.histplot(data[col], kde=True, bins=20, color="blue")
        elif is_categorical_dtype(data[col]) or data[col].dtype == 'object':
            sns.countplot(y=data[col], order=data[col].value_counts().index, palette="Set2")
        plt.title(f"Distribution of {col}")
        plt.savefig(f"distribution_{col}.png")  
        plt.show()

   

    print("\nGenerating HTML report...")
    html_report = f"""
    <html>
    <head><title>Data Analysis Report</title></head>
    <body>
    <h1>Data Analysis Report</h1>
    <h2>Missing Columns</h2>
    <p>{missing_columns}</p>
    <h2>Numeric Columns</h2>
    <p>{numeric_cols}</p>
    <h2>Categorical Columns</h2>
    <p>{categorical_cols}</p>
    <h2>Duplicate Columns</h2>
    <p>{duplicate_columns.tolist()}</p>
    <h2>Constant Columns</h2>
    <p>{constant_cols}</p>
    <h2>Boxplots</h2>
    {"".join([f'<img src="{col}_boxplot.png" width="400">' for col in numeric_cols if col not in constant_cols])}
    <h2>Distributions</h2>
    {"".join([f'<img src="{col}_distribution.png" width="400">' for col in selected_cols])}
    </body>
    </html>
    """

    with open(output_file, "w") as f:
        f.write(html_report)
    print(f"\nHTML report saved as {output_file}")

# Example Usage:
if __name__ == "__main__":
    data = pd.read_csv('python.csv') 
    analyze_data(data, output_file="analysis_report.html")
