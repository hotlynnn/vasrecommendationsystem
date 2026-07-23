## Overall Architecture
```text
Customer Data
      │
      ▼
Feature Engineering
      │
      ▼
Customer Segmentation
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

vasrecommendationsystem/
│
├── data/
│   ├── raw/
│   │     vas_customer_features.csv
│   │
│   ├── stage1/
│   │     stage1_customer_data.csv
│   │
│   ├── stage2/
│   │     stage2_clean_customer_data.csv
│   │
│   ├── stage3/
│   │     product_catalogue.csv
│   │
│   ├── stage4/
│   │     customer_segments.csv
│   │
│   └── outputs/
│
├── notebooks/
├── models/
└── src/

## Stage 1 — Data Collection

## Stage 2 — Data cleaning 
You can use data warehouse in proudction here. But I used csv files

## Stage 3 — Product Catalogue
Create a product master.

**Example**

#### Product	          Category	    Vendor	    Price
Football TV	      Digital	    MTN	        5
Cartoon TV	      Digital	    MTN	        3
Gospel Music	  Digital	    MTN	        2
CRBT Pop	      CRBT	        Huawei	    2
SMS Bundle	      SMS	        MTN	        1

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