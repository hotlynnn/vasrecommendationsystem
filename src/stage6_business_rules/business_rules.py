import pandas as pd


class BusinessRules:

    def __init__(self):

        # Configurable thresholds
        self.digital_propensity_threshold = 0.70
        self.churn_threshold = 0.70

        # Maximum recommendations
        self.max_recommendations = 3


    ############################################################
    # Rule 1
    # Remove products customer already owns
    ############################################################

    def remove_existing_products(
        self,
        recommendations,
        subscribed_products
    ):

        return [
            product
            for product in recommendations
            if product not in subscribed_products
        ]


    ############################################################
    # Rule 2
    # Digital Propensity
    ############################################################

    def apply_propensity_rule(
        self,
        recommendations,
        digital_propensity
    ):

        if digital_propensity < self.digital_propensity_threshold:

            return []

        return recommendations


    ############################################################
    # Rule 3
    # Churn Rule
    ############################################################

    def apply_churn_rule(

        self,

        recommendations,

        churn_probability

    ):

        if churn_probability >= self.churn_threshold:

            return []

        return recommendations


    ############################################################
    # Rule 4
    # Device Compatibility
    ############################################################

    def apply_device_rule(

        self,

        recommendations,

        handset_type

    ):

        filtered = []

        for product in recommendations:

            if "Video" in product:

                if handset_type == "Feature Phone":

                    continue

            filtered.append(product)

        return filtered


    ############################################################
    # Rule 5
    # Traditional Upgrade
    ############################################################

    def apply_upgrade_rule(

        self,

        recommendations,

        traditional_probability

    ):

        if traditional_probability > 0.80:

            recommendations.insert(

                0,

                "Premium Digital Bundle"

            )

        return recommendations


    ############################################################
    # Rule 6
    # Remove Duplicate Categories
    ############################################################

    def diversity_rule(

        self,

        recommendations

    ):

        categories = set()

        final = []

        for product in recommendations:

            category = product.split("_")[0]

            if category in categories:

                continue

            final.append(product)

            categories.add(category)

        return final


    ############################################################
    # Rule 7
    # Keep Top N
    ############################################################

    def top_three(

        self,

        recommendations

    ):

        return recommendations[:self.max_recommendations]


    ############################################################
    # Main Pipeline
    ############################################################

    def apply(

        self,

        recommendations,

        subscribed_products,

        digital_propensity,

        churn_probability,

        traditional_probability,

        handset_type

    ):

        recommendations = self.remove_existing_products(

            recommendations,

            subscribed_products

        )

        recommendations = self.apply_propensity_rule(

            recommendations,

            digital_propensity

        )

        recommendations = self.apply_churn_rule(

            recommendations,

            churn_probability

        )

        recommendations = self.apply_device_rule(

            recommendations,

            handset_type

        )

        recommendations = self.apply_upgrade_rule(

            recommendations,

            traditional_probability

        )

        recommendations = self.diversity_rule(

            recommendations

        )

        recommendations = self.top_three(

            recommendations

        )

        return recommendations