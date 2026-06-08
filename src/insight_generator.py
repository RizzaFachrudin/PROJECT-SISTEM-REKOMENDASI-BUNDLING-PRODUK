# GENERATE BUSINESS INSIGHT

def generate_insight(
    antecedent,
    consequent,
    confidence
):

    confidence_percent = round(
        confidence * 100,
        1
    )

    insight = f"""
    Pelanggan yang membeli
    {antecedent}
    cenderung membeli
    {consequent}
    dengan tingkat kecocokan
    sebesar {confidence_percent}%.
    """

    return insight