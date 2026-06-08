from mlxtend.frequent_patterns import (
    apriori,
    association_rules
)



# GENERATE ASSOCIATION RULES

def generate_rules(
    basket,
    min_support,
    min_confidence,
    min_lift
):

    # Frequent Itemsets
    frequent_itemsets = apriori(
        basket,
        min_support=min_support,
        use_colnames=True
    )

    # Jika itemset kosong
    if frequent_itemsets.empty:

        return frequent_itemsets, None

    # Association Rules
    rules = association_rules(
        frequent_itemsets,
        metric='confidence',
        min_threshold=min_confidence
    )

    # Jika rules kosong
    if rules.empty:

        return frequent_itemsets, None

    # Filter lift
    rules = rules[
        rules['lift'] >= min_lift
    ]

    # Jika setelah filter kosong
    if rules.empty:

        return frequent_itemsets, None

    # Sorting
    rules = rules.sort_values(
        by='confidence',
        ascending=False
    )

    return frequent_itemsets, rules