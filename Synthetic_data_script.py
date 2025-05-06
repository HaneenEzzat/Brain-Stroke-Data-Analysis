# %%
# Importing libraries and dependencies
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sqlite3
import os
from sdv.single_table import GaussianCopulaSynthesizer
from sdv.metadata import SingleTableMetadata

# %%
# Load csv dataset into SQLite3
df = pd.read_csv("healthcare-dataset-stroke-data.csv")

# %%
# Changing the id column name to mrn(medical record number)


# %%
# Testing the id column has been changed to mrn
df.columns

# %%
connection = sqlite3.connect("data_source.db")
df.to_sql("original_data", connection, if_exists="replace")

# %%
print(df.columns)  # Check if 'mrn' is in the column list

# %%
# Show a sample of the dataset after loading in SQLite
query = "SELECT * FROM original_data"
data_sql = pd.read_sql(query, connection)
print(data_sql)

# %%
# Show the number of records and columns of the dataset before synthesizing
data_sql.shape

# %% [markdown]
# **Data Synthesizing**
# 

# %%
# Detect metadata from the original dataset
metadata = SingleTableMetadata()
metadata.detect_from_dataframe(data_sql)

# Initialize the SDV synthesizer
synthesizer = GaussianCopulaSynthesizer(metadata)

# Fit the synthesizer to the original data
synthesizer.fit(data_sql)

# %%
# Generate synthetic data (same number of rows as original data)
synthetic_data = synthesizer.sample(num_rows=2*len(data_sql))

print("\nSynthetic Data:")
print(synthetic_data.head())

# %%
# Concatenate original and synthetic data
original_synthetic_data = pd.concat([data_sql, synthetic_data], ignore_index=True)

print("\n Original and Synthetic data together:")
print(original_synthetic_data.shape)

# %%
# Save combined data to a new table
original_synthetic_data.to_sql("raw_data", connection, if_exists="replace", index=False)

# Close connection
connection.close()

print("Combined data saved to SQLite database successfully.")