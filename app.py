import streamlit as st
import pandas as pd

from src.preprocessing import (
    create_basket_matrix
)

from src.apriori_model import (
    generate_rules
)

from src.visualisasi import (
    create_top_product_chart,
    create_low_product_chart
)

from src.helper import (
    format_frozenset,
    get_top_products,
    get_low_products
)

from src.insight_generator import (
    generate_insight
)



# PAGE CONFIG


st.set_page_config(
    page_title="Sistem Bundling Produk",
    layout="wide"
)



# HEADER


st.title(
    "Sistem Rekomendasi Bundling Produk"
)

st.markdown("""
Sistem ini membantu pemilik toko
mengetahui
produk paling laris, produk kurang laris, rekomendasi bundling produk.

Analisis dilakukan otomatis
berdasarkan data transaksi pelanggan.
""")



# SIDEBAR


st.sidebar.header(
    "Pengaturan Analisis"
)

min_support = st.sidebar.slider(
    "Minimum Pola Produk",
    0.01,
    1.0,
    0.01,
    0.01
)

min_confidence = st.sidebar.slider(
    "Minimum Tingkat Kecocokan",
    0.01,
    1.0,
    0.2,
    0.01
)

min_lift = st.sidebar.slider(
    "Minimum Hubungan Produk",
    1.0,
    10.0,
    1.0,
    0.1
)



# TEMPLATE DOWNLOAD


st.sidebar.subheader(
    "Download Template"
)

template_df = pd.DataFrame({
    'TransactionID': [1, 2],
    'Items': [
        'KOPI,GULA',
        'MIE INSTAN,TELUR'
    ]
})

template_csv = template_df.to_csv(
    index=False
)

st.sidebar.download_button(
    label="Download Template CSV",
    data=template_csv,
    file_name='template_dataset.csv',
    mime='text/csv'
)



# PERIODE


periode = st.text_input(
    "Periode Analisis",
    placeholder="Contoh: Juni 2026"
)



# FILE UPLOAD


uploaded_file = st.file_uploader(
    "Upload Dataset Penjualan",
    type=['csv']
)



# MAIN SYSTEM


if uploaded_file:


    # LOAD DATASET


    df = pd.read_csv(uploaded_file)


    # VALIDASI


    required_columns = [
        'TransactionID',
        'Items'
    ]

    if not all(
        col in df.columns
        for col in required_columns
    ):

        st.error("""
        Format dataset tidak sesuai.

        Gunakan format:
        - TransactionID
        - Items
        """)

        st.stop()


    # METRICS


    total_transactions = (
        df['TransactionID']
        .nunique()
    )

    total_products = len(
        set(
            ','.join(df['Items'])
            .split(',')
        )
    )

    top_product = (
        get_top_products(df, 1)[0]
    )

    low_product = (
        get_low_products(df, 1)[0]
    )

    st.subheader(
        "Ringkasan Penjualan"
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Transaksi",
        total_transactions
    )

    col2.metric(
        "Total Produk",
        total_products
    )

    col3.metric(
        "Produk Terlaris",
        top_product[0]
    )

    col4.metric(
        "Produk Kurang Laris",
        low_product[0]
    )


    # VISUALISASI


    st.subheader(
        "Analisis Produk"
    )

    tab1, tab2 = st.tabs([
        "Produk Terlaris",
        "Produk Kurang Laris"
    ])

    with tab1:

        fig1 = create_top_product_chart(df)

        st.pyplot(fig1)

    with tab2:

        fig2 = create_low_product_chart(df)

        st.pyplot(fig2)


    # PREPROCESSING


    basket = create_basket_matrix(df)


    # APRIORI


    frequent_itemsets, rules = (
        generate_rules(
            basket,
            min_support,
            min_confidence,
            min_lift
        )
    )


    # REKOMENDASI BUNDLING


    st.subheader(
        "Rekomendasi Bundling Produk"
    )

    if rules is not None:

        product_input = st.text_input(
            "Masukkan Nama Produk"
        )

        if product_input:

            product_input = (
                product_input.upper()
            )

            rekomendasi = rules[
                rules['antecedents']
                .apply(
                    lambda x:
                    product_input in list(x)
                )
            ]

            rekomendasi = (
                rekomendasi
                .sort_values(
                    by='confidence',
                    ascending=False
                )
            )

            if not rekomendasi.empty:

                for index, row in rekomendasi.iterrows():

                    antecedent = format_frozenset(
                        row['antecedents']
                    )

                    consequent = format_frozenset(
                        row['consequents']
                    )

                    confidence_percent = round(
                        row['confidence'] * 100,
                        1
                    )

                    st.markdown("---")

                    col1, col2 = st.columns([2, 1])

                    with col1:

                        st.subheader(
                            f"{antecedent} + {consequent}"
                        )

                        insight = generate_insight(
                            antecedent,
                            consequent,
                            row['confidence']
                        )

                        st.write(insight)

                    with col2:

                        st.metric(
                            "Tingkat Kecocokan",
                            f"{confidence_percent}%"
                        )

                        st.progress(
                            int(confidence_percent)
                        )

            else:

                st.warning("""
                Tidak ditemukan
                rekomendasi bundling.
                """)

    else:

        st.warning("""
        Tidak ditemukan pola
        pembelian yang cukup kuat.
        """)


    # DOWNLOAD


    if rules is not None:

        st.subheader(
            "Download Hasil Analisis"
        )

        download_rules = rules[
            [
                'antecedents',
                'consequents',
                'confidence'
            ]
        ].copy()

        download_rules['antecedents'] = (
            download_rules['antecedents']
            .apply(format_frozenset)
        )

        download_rules['consequents'] = (
            download_rules['consequents']
            .apply(format_frozenset)
        )

        download_rules['Persentase Kecocokan'] = (
            download_rules['confidence']
            * 100
        ).round(1)

        download_rules = download_rules[
            [
                'antecedents',
                'consequents',
                'Persentase Kecocokan'
            ]
        ]

        csv = download_rules.to_csv(
            index=False
        )

        st.download_button(
            label="Download Hasil Bundling",
            data=csv,
            file_name='hasil_bundling.csv',
            mime='text/csv'
        )

else:

    st.info("""
    Upload dataset penjualan
    untuk memulai analisis.
    """)