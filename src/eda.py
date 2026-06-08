import pandas as pd

df=pd.read_csv('dataset/GroceryStoreDataSet.csv')

print("jumlah transaksi: ", df['TransactionID'].nunique())
print("jumlah produk: ", df['ProductID'].nunique())

print("\nProduk terlaris:")
print(df['Product'].value_counts().head(10))