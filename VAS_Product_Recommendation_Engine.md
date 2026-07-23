## Overall Architecture
```text
Stage 1 - Customer Data - Investigation
      │
      ▼
Stage 2 - Data Cleaning/ Feature Engineering
      │
      ▼
Stage 3 - Product Catalogue
      │
      ▼
Stage 4 - Customer Segmentation
      │
      ▼
Recommendation Models
      │
      ├── Existing Digital Users
      │       │
      │       └── Recommend next Digital Product
      │
      ├── Existing Traditional Users
      │       │
      │       └── Recommend Digital Upgrade
      │
      ├── No VAS Users
      │       │
      │       └── Recommend First Product
      │
      ▼
Business Rules Layer
      │
      ▼
Top 3 Products
      │
      ▼
Campaign System
      │
      ▼
SMS / USSD / App / WhatsApp Push
```

## Stage 1 — Data Investigation
Investigation column types and missing vlaues

## Stage 2 — Data Cleaning/ Feature Engineering
You can use data warehouse in proudction here. But I used csv files

## Stage 3 — Product Catalogue
Create a product master.

**Example**
```text
Product	      Category	      Vendor	    Price
Football TV	      Digital	     MTN	       5
Cartoon TV	      Digital	     MTN	       3
Gospel Music	Digital	         MTN	       2
CRBT Pop	      CRBT	         Huawei	       2
SMS Bundle	      SMS	         MTN	       1
```
This becomes your recommendation target.

## Stage 4 — Customer Segmentation
First split customers.

**Example**

- Segment A

Heavy Digital Users

- Segment B

Light Digital Users

- Segment C

- Traditional Only

- Segment D

No VAS

- Segment E

Dormant

**Each segment will use a different recommendation strategy.**

## Stage 5 — Models
- Next Best Product model

**Objective: Which Digital product should this customer subscribe to?**

The model you have in the project is very basic and you need to improve it. It uses a CatBoost multiclass which predicts the specific VAS product (label_product_name) a customer is most likely to subscribe to next. It gives the score for the next 3 top products.

- Digital Propensity model

**Objective: How likely is this customer to subscribe to any Digital VAS product??**

It uses a CatBoost binary model and estimates the likelihood of a customer adopting any Digital VAS. Only customers with a high propensity (e.g., >0.70) proceed to the Next Best Product recommendation. 
```text
If Digital Propensity < 0.30 → Don't recommend Digital VAS; recommend Traditional VAS instead.
If Digital Propensity is 0.30–0.70 → Recommend one low-cost Digital product.
If Digital Propensity > 0.70 → Run Model 1 and recommend the Top 3 Digital products.
```

- Traditional Upgrade model

**Objective: Among customers who currently use Traditional VAS but have never used Digital VAS, predict who is most likely to upgrade to Digital VAS.?**

It uses a CatBoost binary model and estimates the likelihood of a customer upgrading to a Digital VAS. Only customers with a high probability (e.g., >0.70) are considered for this campaign. 

# Project Folder Structure
```text
vasrecommendationsystem/
│
├── config/ (Add this later)
│   └── config.py (Add this later)
│
├── src/
│   ├── stage1_validation.py
│   ├── stage2_cleaning.py
│   ├── stage3_product_catalogue.py
│   ├── stage4_customer_segmentation.py
│   └── stage5_models/
│       ├── train_next_best_product.py
│       ├── train_digital_propensity.py
│       ├── train_traditional_upgrade.py
│
├── data/
│   ├── raw/  (Contains the outputs from Stage 1 to 4)
│   ├── stage1/
│   ├── stage2/
│   ├── stage3/
│   ├── stage4/
│ 
├── models/   (Contains the models you need to improve)
│ 
├── model_outputs/   (Contains the predictions of the model)
│
├── run_pipeline.py (Add this later)
├── requirements.txt
├── VAS_Product_Recommendation_Engine.md
└── VAS_Product_Recommendation_Engine_Design_Updated.docx
```