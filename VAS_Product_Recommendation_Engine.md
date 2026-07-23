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

# Project Folder Structure
```text
vasrecommendationsystem/
│
├── config/ **(I will add this later)**
│   └── config.py **(I will add this later)**
│
├── src/
│   ├── stage1_validation.py
│   ├── stage2_cleaning.py
│   ├── stage3_eda.py
│   ├── stage4_product_catalogue.py
│   └── stage5_customer_segmentation.py
│
├── data/
│   ├── raw/
│   ├── stage1/
│   ├── stage2/
│   ├── stage3/
│   ├── stage4/
│   └── stage5/
│
├── run_pipeline.py **(I will add this later)**
├── requirements.txt
└── VAS_Product_Recommendation_Engine.md
```

## Stage 1 — Data Investigation
Investigation column types and missing vlaues

## Stage 2 — Data Cleaning/ Feature Engineering
You can use data warehouse in proudction here. But I used csv files

## Stage 3 — Product Catalogue
Create a product master.

**Example**
```text
Product	      Category	    Vendor	    Price
Football TV	      Digital	   MTN	    5
Cartoon TV	      Digital	   MTN	    3
Gospel Music	Digital	   MTN	    2
CRBT Pop	      CRBT	        Huawei	    2
SMS Bundle	      SMS	        MTN	          1
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