import pandas as pd

# Load cleaned dataset
df = pd.read_csv("retail_data.csv")

# Create data dictionary
data_dictionary = pd.DataFrame({
    "column_name": df.columns,
    "data_type": df.dtypes.astype(str),
    "description": [
        "Unique customer identifier",
        "Customer birth year",
        "Customer education level",
        "Customer marital status",
        "Customer yearly income",
        "Number of children in household",
        "Number of teenagers in household",
        "Date when customer became a customer",
        "Number of days since last purchase",
        "Amount spent on wine products",
        "Amount spent on fruit products",
        "Amount spent on meat products",
        "Amount spent on fish products",
        "Amount spent on sweet products",
        "Amount spent on gold products",
        "Number of purchases made with deals",
        "Number of purchases made through the web",
        "Number of purchases made through the catalog",
        "Number of purchases made in stores",
        "Number of web visits per month",
        "Accepted campaign 3",
        "Accepted campaign 4",
        "Accepted campaign 5",
        "Accepted campaign 1",
        "Accepted campaign 2",
        "Customer complaint indicator",
        "Campaign contact cost value",
        "Campaign revenue value",
        "Response to the latest campaign",
        "Customer age",
        "Total amount spent across products",
        "Total number of purchases across channels",
        "Indicator for purchases made with deals",
        "Indicator for previous campaign exposure",
        "Campaign response outcome"   
    ]
})

# Save data dictionary
data_dictionary.to_csv("data_dictionary.csv", index=False)

print("Data dictionary created successfully.")
print("Columns documented:", len(data_dictionary))

