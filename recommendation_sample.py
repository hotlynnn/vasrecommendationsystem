from src.stage6_business_rules.business_rules import BusinessRules

rules = BusinessRules()

recommendations = [

    "Video_Premium",

    "Movie_HD",

    "Sports_HD",

    "Movie_Basic",

    "Games_Plus"

]

subscribed_products = [

    "Movie_HD"

]

result = rules.apply(

    recommendations=recommendations,

    subscribed_products=subscribed_products,

    digital_propensity=0.91,

    churn_probability=0.18,

    traditional_probability=0.82,

    handset_type="Smartphone"

)

print(result)