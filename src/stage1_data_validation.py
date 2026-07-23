import os
import pandas as pd

#############################################
# Configuration
#############################################

INPUT_FILE = "data/raw/vas_customer_features.csv"

OUTPUT_FOLDER = "data/stage1"
OUTPUT_FILE = os.path.join(
    OUTPUT_FOLDER,
    "stage1_customer_data.csv"
)

PROFILE_FILE = os.path.join(
    OUTPUT_FOLDER,
    "data_profile.csv"
)

#############################################
# Create Output Folder
#############################################

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

#############################################
# Read Data
#############################################

df = pd.read_csv(INPUT_FILE)

print(f"Rows : {len(df)}")
print(f"Columns : {len(df.columns)}")

#############################################
# Remove Duplicates
#############################################

duplicates = df.duplicated().sum()

print(f"Duplicates Found : {duplicates}")

df = df.drop_duplicates()

#############################################
# Missing Value Report
#############################################

profile = pd.DataFrame({

    "Column": df.columns,

    "DataType": df.dtypes.astype(str),

    "MissingValues": df.isnull().sum(),

    "MissingPercent":
        (df.isnull().sum()/len(df)*100).round(2)

})

profile.to_csv(PROFILE_FILE, index=False)

#############################################
# Basic Validation
#############################################

if "age" in df.columns:
    df = df[(df["age"] >= 0) & (df["age"] <= 120)]

revenue_columns = [c for c in df.columns if "rev" in c.lower()]

for col in revenue_columns:
    df.loc[df[col] < 0, col] = 0

#############################################
# Save
#############################################

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("Stage 1 Complete")