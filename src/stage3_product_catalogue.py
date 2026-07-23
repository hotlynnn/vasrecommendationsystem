import os
import pandas as pd

INPUT_FILE = "data/stage2/stage2_clean_customer_data.csv"

OUTPUT_FOLDER = "data/stage3"

OUTPUT_FILE = os.path.join(
    OUTPUT_FOLDER,
    "product_catalogue.csv"
)

os.makedirs(
    OUTPUT_FOLDER,
    exist_ok=True
)

df = pd.read_csv(INPUT_FILE)

#########################################
# Product Statistics
#########################################

catalogue = (

    df.groupby("label_product_name")

    .agg(

        Customers=("msisdn","count"),

        AvgRevenue=("total_vas_rev","mean"),

        DigitalUsers=("label_digital","sum"),

        TraditionalUsers=("label_traditional","sum"),

        CRBTUsers=("label_crbt","sum"),

        SMSUsers=("label_sms_bundle","sum")

    )

    .reset_index()

)

#########################################
# Product Category
#########################################

def category(row):

    if row["DigitalUsers"] > 0:
        return "DIGITAL"

    if row["TraditionalUsers"] > 0:
        return "TRADITIONAL"

    if row["CRBTUsers"] > 0:
        return "CRBT"

    if row["SMSUsers"] > 0:
        return "SMS"

    return "UNKNOWN"

catalogue["Category"] = catalogue.apply(
    category,
    axis=1
)

catalogue.to_csv(
    OUTPUT_FILE,
    index=False
)

print("Stage 3 Complete")