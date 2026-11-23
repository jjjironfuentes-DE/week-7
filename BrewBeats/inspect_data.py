
import pandas as pd

# Load the datasets
coffee = pd.read_csv("data/raw/coffee_sales.csv")
spotify = pd.read_csv("data/raw/Spotify_data.csv")


# Function to inspect each dataset
def inspect_dataset(df, name):

    print("\n" + "=" * 50)
    print(f"DATASET: {name}")
    print("=" * 50)

    print("\n1. Number of rows and columns:")
    print(df.shape)

    print("\n2. Column names:")
    print(df.columns.tolist())

    print("\n3. Data types:")
    print(df.dtypes)

    print("\n4. Missing values:")
    print(df.isnull().sum())

    print("\n5. First five rows:")
    print(df.head())


# Inspect both datasets
inspect_dataset(coffee, "COFFEE SALES")
inspect_dataset(spotify, "SPOTIFY")


# Investigate missing card values
print("\nCOFFEE SALES - CARD INVESTIGATION")

print("\nTransactions by payment type:")
print(coffee["cash_type"].value_counts(dropna=False))

print("\nMissing card values by payment type:")
print(
    coffee.groupby("cash_type")["card"]
    .apply(lambda x: x.isnull().sum())
)
