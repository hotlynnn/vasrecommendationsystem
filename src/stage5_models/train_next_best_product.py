import os
import joblib
import pandas as pd

from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score

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

print(f"Dataset Shape : {df.shape}")

#############################################
# REMOVE LEAKAGE
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

y = df["label_product_name"]

#############################################
# IDENTIFY CATEGORICAL COLUMNS
#############################################

categorical_features = X.select_dtypes(

    include=["object"]

).columns.tolist()

cat_feature_indices = [

    X.columns.get_loc(col)

    for col in categorical_features

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

    loss_function="MultiClass",

    eval_metric="Accuracy",

    verbose=100,

    random_seed=42

)

#############################################
# TRAIN
#############################################

model.fit(

    X_train,

    y_train,

    cat_features=cat_feature_indices,

    eval_set=(X_test, y_test),

    use_best_model=True

)

#############################################
# EVALUATE
#############################################

predictions = model.predict(X_test)

accuracy = accuracy_score(

    y_test,

    predictions

)

print()

print("Accuracy")

print(accuracy)

print()

print(classification_report(

    y_test,

    predictions

))

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

        "feature_importance.csv"

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

        "next_best_product.pkl"

    )

)

#############################################
# PREDICT EVERY CUSTOMER
#############################################

probabilities = model.predict_proba(X)

classes = model.classes_

prob_df = pd.DataFrame(

    probabilities,

    columns=classes

)

recommendations = pd.DataFrame()

recommendations["msisdn"] = df["msisdn"]

#############################################
# TOP 3 PRODUCTS
#############################################

recommendations["Recommendation1"] = prob_df.idxmax(axis=1)

recommendations["Score1"] = prob_df.max(axis=1)

prob2 = prob_df.copy()

for i, p in enumerate(recommendations["Recommendation1"]):

    prob2.loc[i, p] = -1

recommendations["Recommendation2"] = prob2.idxmax(axis=1)

recommendations["Score2"] = prob2.max(axis=1)

prob3 = prob2.copy()

for i, p in enumerate(recommendations["Recommendation2"]):

    prob3.loc[i, p] = -1

recommendations["Recommendation3"] = prob3.idxmax(axis=1)

recommendations["Score3"] = prob3.max(axis=1)

#############################################
# SAVE
#############################################

recommendations.to_csv(

    os.path.join(

        OUTPUT_FOLDER,

        "next_best_product_predictions.csv"

    ),

    index=False

)

print()

print("Training Complete")