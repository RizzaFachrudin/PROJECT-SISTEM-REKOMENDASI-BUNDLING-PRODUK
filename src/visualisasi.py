import matplotlib.pyplot as plt

from src.helper import (
    count_products
)



# TOP PRODUCT CHART


def create_top_product_chart(df):

    counter = count_products(df)

    sorted_items = sorted(
        counter.items(),
        key=lambda x: x[1],
        reverse=True
    )

    top_products = sorted_items[:10]

    produk = [x[0] for x in top_products]

    jumlah = [x[1] for x in top_products]

    fig, ax = plt.subplots(
        figsize=(10, 5)
    )

    ax.bar(produk, jumlah)

    ax.set_title(
        'Produk Terlaris'
    )

    ax.set_xlabel('Produk')

    ax.set_ylabel('Jumlah Pembelian')

    plt.xticks(rotation=45)

    return fig



# LOW PRODUCT CHART


def create_low_product_chart(df):

    counter = count_products(df)

    sorted_items = sorted(
        counter.items(),
        key=lambda x: x[1]
    )

    low_products = sorted_items[:10]

    produk = [x[0] for x in low_products]

    jumlah = [x[1] for x in low_products]

    fig, ax = plt.subplots(
        figsize=(10, 5)
    )

    ax.bar(produk, jumlah)

    ax.set_title(
        'Produk Kurang Laris'
    )

    ax.set_xlabel('Produk')

    ax.set_ylabel('Jumlah Pembelian')

    plt.xticks(rotation=45)

    return fig