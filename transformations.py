# %%
import pandas as pd
import sqlite3
import plotly.graph_objects as go
import matplotlib.pyplot as plt

# %%
connection = sqlite3.connect("data_source.db")
df = pd.read_sql("SELECT * FROM raw_data", connection)

# %%
print(df.shape)

# %%
print(df.isnull().sum())

# %%
print(df.dtypes)

# %%
df.info()

# %%
df.columns

# %%
print(df.describe())

# %%
df.rename(columns={"id": "mrn"}, inplace=True)

# %%
# Plot the distribution
plt.figure(figsize=(10, 6))
plt.hist(df["bmi"], bins=30, edgecolor="black", alpha=0.7)
plt.title("BMI Distribution")
plt.xlabel("BMI")
plt.ylabel("Count")
plt.grid(True)
plt.tight_layout()
plt.show()

# %%
df["bmi"].fillna(df["bmi"].median(), inplace=True)

# %%
df.info()

# %%
df["age_category"] = df["age"].apply(lambda x: "Pediatric" if x < 16 else "Adult")

# %%
df.columns


# %%
def categorize_glucose(glucose):
    if glucose < 140:
        return "Normal"
    elif 140 <= glucose < 200:
        return "Prediabetic"
    else:
        return "Diabetic"


df["avg_glucose_category"] = df["avg_glucose_level"].apply(categorize_glucose)

# %%
df.columns

# %%
df["hypertension"] = df["hypertension"].map({0: "No", 1: "Yes"})

# %%
df["heart_disease"] = df["heart_disease"].map({0: "No", 1: "Yes"})

# %%
df["stroke"] = df["stroke"].map({0: "No", 1: "Yes"})

# %%
df["work_type"] = df["work_type"].map(
    {
        "Private": "Private",
        "Self-employed": "Self-Employed",
        "Govt_job": "Government-Job",
        "children": "Childern",
    }
)

# %%
df["smoking_status"] = df["smoking_status"].map(
    {
        "formerly smoked": "Formerly Smoked",
        "never smoked": "Never Smoked",
        "smokes": "Smokes",
        "Unknown": "Unknown",
    }
)

# %% [markdown]
# **Univariant Analysis for Categorical Columns**
#

# %%
categorical_cols = [
    "gender",
    "hypertension",
    "heart_disease",
    "ever_married",
    "work_type",
    "Residence_type",
    "smoking_status",
    "stroke",
]

for col in categorical_cols:
    counts = df[col].value_counts()
    fig = go.Figure(data=[go.Bar(x=counts.index, y=counts.values)])
    fig.update_layout(
        title=f"Distribution of {col}", xaxis_title=col, yaxis_title="Count"
    )
    fig.show()

# %% [markdown]
# **Univariant Analysis for Numircal Columns**
#

# %%
numerical_cols = ["age", "avg_glucose_level", "bmi"]

for col in numerical_cols:
    fig = go.Figure(data=[go.Histogram(x=df[col], nbinsx=50)])
    fig.update_layout(
        title=f"Distribution of {col}", xaxis_title=col, yaxis_title="Count"
    )
    fig.show()

# %% [markdown]
# **Bivariate Analysis**
#

# %%
bivariate = [
    "gender",
    "hypertension",
    "heart_disease",
    "smoking_status",
    "avg_glucose_category",
]

for col in bivariate:
    stroke_yes = df[df["stroke"] == "Yes"][col].value_counts()
    stroke_no = df[df["stroke"] == "No"][col].value_counts()

    fig = go.Figure()
    fig.add_trace(go.Bar(name="Stroke: Yes", x=stroke_yes.index, y=stroke_yes.values))
    fig.add_trace(go.Bar(name="Stroke: No", x=stroke_no.index, y=stroke_no.values))

    fig.update_layout(
        barmode="group", title=f"{col} vs Stroke", xaxis_title=col, yaxis_title="Count"
    )
    fig.show()

# %%
conn = sqlite3.connect("enriche_data.db")
df.to_sql("clean_stroke", conn, if_exists="replace", index=False)

# %%
connection = sqlite3.connect("enriche_data.db")
query = "SELECT * FROM clean_stroke"
df2 = pd.read_sql(query, connection)
