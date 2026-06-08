import pandas as pd

df = pd.read_csv('dataset/GroceryStoreDataset.csv')

print(df.head())

print("\nInfo Dataset")
print(df.info())

print("\nMissing Value")
print(df.isnull().sum())