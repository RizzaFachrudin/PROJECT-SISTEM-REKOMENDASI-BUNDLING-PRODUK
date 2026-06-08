from collections import Counter



# FORMAT FROZENSET


def format_frozenset(value):

    return ', '.join(list(value))



# CONVERT TRANSACTIONS


def convert_transactions(df):

    transactions = []

    for item in df['Items']:

        transaksi = [
            x.strip().upper()
            for x in item.split(',')
        ]

        transactions.append(transaksi)

    return transactions



# COUNT PRODUCTS


def count_products(df):

    all_items = []

    for item in df['Items']:

        products = item.split(',')

        for p in products:

            all_items.append(
                p.strip().upper()
            )

    return Counter(all_items)



# TOP PRODUCTS


def get_top_products(df, n=5):

    counter = count_products(df)

    return counter.most_common(n)



# LOW PRODUCTS


def get_low_products(df, n=5):

    counter = count_products(df)

    sorted_products = sorted(
        counter.items(),
        key=lambda x: x[1]
    )

    return sorted_products[:n]