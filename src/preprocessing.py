import pandas as pd

from mlxtend.preprocessing import (
    TransactionEncoder
)

from src.helper import (
    convert_transactions
)



# CREATE BASKET MATRIX


def create_basket_matrix(df):

    transactions = convert_transactions(df)

    te = TransactionEncoder()

    te_array = (
        te.fit(transactions)
        .transform(transactions)
    )

    basket = pd.DataFrame(
        te_array,
        columns=te.columns_
    )

    return basket