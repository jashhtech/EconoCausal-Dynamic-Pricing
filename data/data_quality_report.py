import pandas as pd

# Load cleaned dataset
df = pd.read_csv("retail_data.csv")

# Basic quality checks
quality_report = {
    "Rows": len(df),
    "Columns": len(df.columns),
    "Missing values": df.isnull().sum().sum(),
    "Duplicate rows": df.duplicated().sum()
}

# Display quality report
print("DATA QUALITY REPORT")
print("-------------------")

for key, value in quality_report.items():
    print(f"{key}: {value}")

# Save report
pd.DataFrame(
    quality_report.items(),
    columns=["Check", "Result"]
).to_csv("data_quality_report.csv", index=False)

print("Data quality report saved as data_quality_report.csv")