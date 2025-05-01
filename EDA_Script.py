# %% [markdown]
# **Import the required Python libraries**
# %%
import numpy as np
import pandas as pd
import sqlite3
import plotly.graph_objs as go
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from tabulate import tabulate

# %% [markdown]
# **Import the dataset**
# %%
connection = sqlite3.connect("data_source.db")
query = "SELECT * FROM raw_data"
df = pd.read_sql(query, connection)

# %% [markdown]
# # Overview of the dataset
# %%
print(df.shape)
print(df.columns)

df.head()
df.tail()

df.info()

# %% [markdown]
# Check BMI distribution to determine how to handle missing values
# %%
hist = go.Figure(go.Histogram(x=df["bmi"]))
hist.show()

# Fill missing values with median
df["bmi"].fillna(df["bmi"].median(), inplace=True)

# Recheck missing values
df.info()

# %% [markdown]
# Tabulate the data
# %%
table = tabulate(df, headers="keys", tablefmt="pretty", showindex=False)
print(table)

# %%
print(df.describe())

# %%
df["age_category"] = np.where(df["age"] < 16, "Pediatric", "Adult")
print(df.info())

# %%
conditions = [
    df["avg_glucose_level"] < 100,
    (df["avg_glucose_level"] >= 100) & (df["avg_glucose_level"] < 126),
    df["avg_glucose_level"] >= 126,
]
categories = ["Normal", "Prediabetic", "Diabetic"]
df["glucose_category"] = np.select(conditions, categories)

print(df.info())

# %% [markdown]
# Check for anomalies in the dataset
# %%
assert pd.notnull(df).all().all()

# %% [markdown]
# # Univariate analysis
print(df["stroke"].describe())
print("Skewness:", df["stroke"].skew())

# %%
counts = df["stroke"].value_counts()
fig_distribution = go.Figure(
    data=go.Bar(x=counts.index, y=counts.values, marker_color=["pink", "blue"])
)
fig_distribution.update_layout(
    title="Distribution of Stroke Variable",
    xaxis_title="Stroke (0 = No, 1 = Yes)",
    yaxis_title="Count",
    template="plotly_dark",
)
fig_distribution.show()

# %% [markdown]
# # Multivariate analysis
# %%
df["ever_married"].value_counts()

# %%
scaler = StandardScaler()
numeric_features = ["age", "hypertension", "heart_disease", "avg_glucose_level", "bmi"]
categorical_features = ["smoking_status", "Residence_type", "ever_married", "work_type"]

encoder = OneHotEncoder(handle_unknown="ignore", drop="first")
preprocessor = ColumnTransformer(
    [("num", scaler, numeric_features), ("cat", encoder, categorical_features)]
)

scaled_data = preprocessor.fit_transform(df)

# %%
pca = PCA(n_components=2)
pca_result = pca.fit_transform(scaled_data)

pca_figure = go.Figure()
pca_figure.add_trace(
    go.Scatter(
        x=pca_result[:, 0],
        y=pca_result[:, 1],
        mode="markers",
        marker=dict(color=df["stroke"], showscale=True, size=10),
        text=df.index,
    )
)
pca_figure.update_layout(
    title="PCA of Stroke Data", xaxis_title="pca1", yaxis_title="pca2"
)
pca_figure.show()

# %% [markdown]
# Save transformed data to a new SQLite database
# %%
new_connection = sqlite3.connect("enriched_data.db")
df.to_sql("clean_stroke", new_connection, if_exists="replace")
# finish eda