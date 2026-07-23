import os
import pandas as pd

INPUT_FILE = "data/stage2/stage2_clean_customer_data.csv"

OUTPUT_FOLDER = "data/stage4"

OUTPUT_FILE = os.path.join(
    OUTPUT_FOLDER,
    "customer_segments.csv"
)

os.makedirs(
    OUTPUT_FOLDER,
    exist_ok=True
)

df = pd.read_csv(INPUT_FILE)

###########################################
# Thresholds
###########################################

digital_threshold = df["digital_rev"].median()

high_value = df["total_spend"].quantile(.80)

###########################################
# Segment Logic
###########################################

def segment(customer):

    if customer["digital_consistent_user"] == 1 and customer["digital_rev"] >= digital_threshold:

        return "Heavy Digital"

    elif customer["ever_used_digital"] == 1:

        return "Light Digital"

    elif customer["ever_used_trad"] == 1 and customer["ever_used_digital"] == 0:

        return "Traditional Only"

    elif customer["crbt_consistent_user"] == 1:

        return "CRBT Loyal"

    elif customer["label_any_vas"] == 0:

        return "New To VAS"

    elif customer["total_spend"] >= high_value:

        return "High Value"

    elif customer["is_price_sensitive"] == 1:

        return "Price Sensitive"

    elif customer["days_since_last_vas_txn"] > 90:

        return "Dormant"

    else:

        return "General"

###########################################
# Create Segment
###########################################

df["CustomerSegment"] = df.apply(
    segment,
    axis=1
)

###########################################
# Save Segment Table
###########################################

segments = df[

    [

        "msisdn",

        "CustomerSegment",

        "digital_rev",

        "trad_rev",

        "crbt_rev",

        "total_spend"

    ]

]

segments.to_csv(
    OUTPUT_FILE,
    index=False
)

###########################################
# Save Customer Master
###########################################

customer_master = os.path.join(
    OUTPUT_FOLDER,
    "customer_master.csv"
)

df.to_csv(
    customer_master,
    index=False
)

print("Stage 4 Complete")