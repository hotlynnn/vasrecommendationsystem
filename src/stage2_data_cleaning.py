import os
import numpy as np
import pandas as pd

INPUT_FILE = "data/stage1/stage1_customer_data.csv"

OUTPUT_FOLDER = "data/stage2"

OUTPUT_FILE = os.path.join(
    OUTPUT_FOLDER,
    "stage2_clean_customer_data.csv"
)

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

df = pd.read_csv(INPUT_FILE)

###########################################
# Numeric Missing Values
###########################################

numeric_columns = df.select_dtypes(
    include=np.number
).columns

for col in numeric_columns:

    df[col] = df[col].fillna(
        df[col].median()
    )

###########################################
# Categorical Missing Values
###########################################

categorical_columns = df.select_dtypes(
    exclude=np.number
).columns

for col in categorical_columns:

    df[col] = df[col].fillna("Unknown")

###########################################
# Standardize Text
###########################################

for col in categorical_columns:

    df[col] = (

        df[col]

        .astype(str)

        .str.strip()

        .str.upper()

    )

###########################################
# Convert Yes/No Columns
###########################################

mapping = {

    "YES":1,
    "NO":0,
    "Y":1,
    "N":0,
    "TRUE":1,
    "FALSE":0

}

for col in categorical_columns:

    unique = set(df[col].dropna().unique())

    if unique.issubset(mapping.keys()):

        df[col] = df[col].map(mapping)

###########################################
# Save
###########################################

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("Stage 2 Complete")