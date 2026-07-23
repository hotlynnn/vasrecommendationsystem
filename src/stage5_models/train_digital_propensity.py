import os
import joblib
import pandas as pd

from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
    roc_auc_score
)

#############################################
# CONFIGURATION
#############################################

INPUT_FILE = "data/stage4/customer_master.csv"

MODEL_FOLDER = "models"
OUTPUT_FOLDER = "model_outputs"

os.makedirs(MODEL_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

#############################################
# LOAD DATA
#############################################

df = pd.read_csv(INPUT_FILE)

print(f"Dataset Shape: {df.shape}")

#############################################
# REMOVE TARGET LEAKAGE
#############################################

remove_columns = [

    "msisdn",

    "label_product_name",

    "label_digital",

    "label_traditional",

    "label_crbt",

    "label_sms_bundle",

    "label_any_vas"

]

X = df.drop(columns=remove_columns)
y = df["label_digital"]

#############################################
# IDENTIFY CATEGORICAL FEATURES
#############################################

categorical_columns = X.select_dtypes(include=["object"]).columns.tolist()

cat_features = [
    X.columns.get_loc(col)
    for col in categorical_columns
]

#############################################
# TRAIN TEST SPLIT
#############################################

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.20,

    random_state=42,

    stratify=y

)

#############################################
# BUILD MODEL
#############################################

model = CatBoostClassifier(

    iterations=500,

    learning_rate=0.05,

    depth=8,

    loss_function="Logloss",

    eval_metric="AUC",

    random_seed=42,

    verbose=100

)

#############################################
# TRAIN MODEL
#############################################

model.fit(

    X_train,
    y_train,

    cat_features=cat_features,

    eval_set=(X_test, y_test),

    use_best_model=True

)

#############################################
# EVALUATE
#############################################

predictions = model.predict(X_test)

probabilities = model.predict_proba(X_test)[:,1]

print()

print("Accuracy")

print(accuracy_score(

    y_test,

    predictions

))

print()

print("ROC AUC")

print(

    roc_auc_score(

        y_test,

        probabilities

    )

)

print()

print(

    classification_report(

        y_test,

        predictions

    )

)

print()

print(

    confusion_matrix(

        y_test,

        predictions

    )

)

#############################################
# FEATURE IMPORTANCE
#############################################

importance = pd.DataFrame({

    "Feature": X.columns,

    "Importance":

        model.get_feature_importance()

})

importance = importance.sort_values(

    "Importance",

    ascending=False

)

importance.to_csv(

    os.path.join(

        OUTPUT_FOLDER,

        "digital_feature_importance.csv"

    ),

    index=False

)

#############################################
# SAVE MODEL
#############################################

joblib.dump(

    model,

    os.path.join(

        MODEL_FOLDER,

        "digital_propensity.pkl"

    )

)

#############################################
# SCORE ALL CUSTOMERS
#############################################

all_probabilities = model.predict_proba(X)[:,1]

results = pd.DataFrame({

    "msisdn": df["msisdn"],

    "DigitalPropensity":

        all_probabilities

})

#############################################
# ASSIGN PROPENSITY BAND
#############################################

def propensity_band(score):

    if score >= 0.90:
        return "Very High"

    elif score >= 0.70:
        return "High"

    elif score >= 0.50:
        return "Medium"

    elif score >= 0.30:
        return "Low"

    return "Very Low"

results["PropensityBand"] = results["DigitalPropensity"].apply(
    propensity_band
)

#############################################
# IDENTIFY CAMPAIGN ELIGIBILITY
#############################################

results["EligibleForDigitalCampaign"] = (

    results["DigitalPropensity"] >= 0.70

)

#############################################
# SAVE RESULTS
#############################################

results.to_csv(

    os.path.join(

        OUTPUT_FOLDER,

        "digital_propensity_predictions.csv"

    ),

    index=False

)

print()

print("Model Saved Successfully")

print("Predictions Saved Successfully")