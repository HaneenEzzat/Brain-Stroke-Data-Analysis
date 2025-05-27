import taipy.gui.builder as tgb
import plotly.graph_objects as go
import pandas as pd
import sqlite3
import numpy as np
from taipy.gui import Gui, Icon, navigate


connection = sqlite3.connect("data/enriche_data.db")
query = "SELECT * FROM clean_stroke"
df = pd.read_sql(query, connection)


categories = ["Never Smoked", "Formerly Smoked", "Smokes", "Unknown"]

fig1 = go.Figure()

for status in categories:
    subset = df[(df["smoking_status"] == status) & (df["stroke"] == "Yes")]
    count = len(subset)

    fig1.add_trace(
        go.Bar(x=[status], y=[count], name=status, text=[count], textposition="outside")
    )

fig1.update_layout(
    title="Stroke Cases by Smoking Status",
    xaxis_title="Smoking Status",
    yaxis_title="Stroke Count",
    barmode="group",
    template="plotly_white",
    height=600,
)

# -------------------figure no. 2----------------------

never_smoked_stroke_df = df[
    (df["smoking_status"] == "Never Smoked") & (df["stroke"] == "Yes")
]
hypertension_count = never_smoked_stroke_df["hypertension"].value_counts()
fig2 = go.Figure(
    data=[
        go.Bar(
            x=hypertension_count.index.astype(str),
            y=hypertension_count.values,
            text=hypertension_count.values,
            textposition="outside",
        )
    ]
)
fig2.update_layout(
    title="Hypertension Levels for Non-Smoker",
    xaxis_title="Hypertension",
    yaxis_title="Count",
    template="plotly_white",
    height=600,
)

# -------------------figure no. 3----------------------

Residence_type_count = never_smoked_stroke_df["Residence_type"].value_counts()
fig3 = go.Figure(
    data=[
        go.Bar(
            x=Residence_type_count.index,
            y=Residence_type_count.values,
            marker_color="blue",
            text=Residence_type_count.values,
            textposition="outside",
        )
    ]
)
fig3.update_layout(
    title="Residence Type Distribution ( Non_Smokers)",
    xaxis_title="Residence_type",
    yaxis_title="Count",
    template="plotly_white",
    height=600,
)

# -------------------figure no. 4----------------------

work_type_count = never_smoked_stroke_df["work_type"].value_counts()
fig4 = go.Figure(
    data=[
        go.Bar(
            x=work_type_count.index,
            y=work_type_count.values,
            text=work_type_count.values,
            textposition="outside",
        )
    ]
)
fig4.update_layout(
    title="Work Type Distribution in Non-Smokers with Stroke",
    xaxis_title="Work Type",
    yaxis_title="Count",
    template="plotly_white",
    height=600,
)

# -------------------figure no. 5----------------------

bins = np.histogram_bin_edges(never_smoked_stroke_df["bmi"], bins="auto")
counts, bin_edges = np.histogram(never_smoked_stroke_df["bmi"], bins=bins)
bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
fig5 = go.Figure(
    data=[go.Bar(x=bin_centers, y=counts, text=counts, textposition="outside")]
)
fig5.update_layout(
    title="BMI Distribution of Non-Smokers with Stroke",
    xaxis_title="BMI",
    yaxis_title="Count",
    template="plotly_white",
    height=600,
)

# -------------------figure no. 6----------------------

fig6 = go.Figure()
fig6.add_trace(go.Box(y=df[df["stroke"] == "Yes"]["avg_glucose_level"], name="Stroke"))
fig6.add_trace(
    go.Box(y=df[df["stroke"] == "No"]["avg_glucose_level"], name="No Stroke")
)
fig6.update_layout(
    title="Average Glucose Levels by Stroke Status",
    yaxis_title="Avg Glucose Level",
    template="plotly_white",
    height=600,
)

# -------------------figure no. 7----------------------

fig7 = go.Figure()
for status_2 in df["Residence_type"].unique():
    subset2 = df[(df["Residence_type"] == status_2) & (df["stroke"] == "Yes")]
    count2 = len(subset2)
    fig7.add_trace(
        go.Bar(
            x=[status_2],
            y=[count2],
            name=status_2,
            text=[count2],
            textposition="outside",
        )
    )

fig7.update_layout(
    title="Stroke Cases by Residence type",
    xaxis_title="Residence type",
    yaxis_title="Stroke Count",
    barmode="group",
    template="plotly_white",
    height=600,
)

# -------------------figure no. 8----------------------

stroke_df = df[df["stroke"] == "Yes"]
hist_values, bin_edges = pd.cut(stroke_df["age"], bins=11, retbins=True)
age_counts = hist_values.value_counts().sort_index()

fig8 = go.Figure(
    data=[
        go.Bar(
            x=[
                f"{int(bin_edges[i])}-{int(bin_edges[i + 1])}"
                for i in range(len(bin_edges) - 1)
            ][::-1],
            y=age_counts.values[::-1],
            text=age_counts.values[::-1],
            textposition="outside",
        )
    ]
)
fig8.update_layout(
    title="Age Distribution",
    xaxis_title="Age Group",
    yaxis_title="Count",
    template="plotly_white",
    height=600,
)

# -------------------figure no. 9----------------------

fig9 = go.Figure()
for status3 in df["age_category"].unique():
    subset3 = df[(df["age_category"] == status3) & (df["stroke"] == "Yes")]
    count3 = len(subset3)
    fig9.add_trace(
        go.Bar(
            x=[status3], y=[count3], name=status3, text=[count3], textposition="outside"
        )
    )
fig9.update_layout(
    title="Age Category",
    xaxis_title="Age Category",
    yaxis_title="Stroke Count",
    barmode="group",
    template="plotly_white",
    height=600,
)

# -------------------figure no. 10----------------------

work_type_count = stroke_df["work_type"].value_counts()
fig10 = go.Figure(
    data=[
        go.Bar(
            x=work_type_count.index,
            y=work_type_count.values,
            text=work_type_count.values,
            textposition="outside",
        )
    ]
)
fig10.update_layout(
    title="Work Type",
    xaxis_title="Work Type",
    yaxis_title="Count",
    template="plotly_white",
    height=600,
)

# -------------------figure no. 11----------------------

categories_glucose = ["Normal", "Prediabetic", "Diabetic"]

glucose_count = stroke_df["avg_glucose_category"].value_counts()

counts = [glucose_count.get(cat, 0) for cat in categories_glucose]

fig11 = go.Figure(
    data=[go.Bar(x=categories_glucose, y=counts, text=counts, textposition="outside")]
)

fig11.update_layout(
    title="Glucose Category",
    xaxis_title="Glucose Category",
    yaxis_title="Count",
    template="plotly_white",
    height=600,
)

# -------------------figure no. 12----------------------

bins = np.histogram_bin_edges(stroke_df["bmi"], bins="auto")
counts, bin_edges = np.histogram(stroke_df["bmi"], bins=bins)
bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
fig12 = go.Figure(
    data=[go.Bar(x=bin_centers, y=counts, text=counts, textposition="outside")]
)
fig12.update_layout(
    xaxis=dict(
        tickmode="array",
        tickvals=[round(center, 1) for center in bin_centers],
        tickangle=45,
        tickfont=dict(size=12),
    ),
    title="BMI of Patients",
    xaxis_title="BMI",
    yaxis_title="Count",
    template="plotly_white",
    height=600,
)

# -------------------figure no. 13----------------------

gender_count = stroke_df["gender"].value_counts()
fig13 = go.Figure(
    data=[
        go.Pie(
            labels=gender_count.index,
            values=gender_count.values,
            textinfo="percent+label",
        )
    ]
)
fig13.update_layout(title="Gender ", template="plotly_white", height=600)

# -------------------figure no. 14----------------------

hypertension_stroke_count = stroke_df["hypertension"].value_counts()
fig14 = go.Figure(
    data=[
        go.Bar(
            x=hypertension_stroke_count.index,
            y=hypertension_stroke_count.values,
            text=hypertension_stroke_count.values,
            textposition="outside",
        )
    ]
)
fig14.update_layout(title="Hypertension", template="plotly_white", height=600)


def menu_option_selected(state, action, info):
    page = info["args"][0]
    navigate(state, to=page)


# Root Page (Navigation Menu)
with tgb.Page() as root_page:
    tgb.menu(
        label="Menu",
        lov=[
            (
                "general",
                Icon("images/icons8-brain-stroke-50.png", "General Stroke Data"),
            ),
            (
                "non_smoker",
                Icon("images/icons8-no-smoking-48.png", "Non-Smoker Stroke Patients"),
            ),
        ],
        on_action=menu_option_selected,
    )


# Page 1: General Stroke Data
with tgb.Page() as general_stroke_page:
    tgb.text("# General Stroke Data", mode="md")

    tgb.html("br")  # Adds spacing
    # Row 1
    with tgb.layout(columns="1 1"):
        tgb.chart(figure="{fig1}")
        tgb.chart(figure="{fig6}")
    tgb.html("br")

    # Row 2
    with tgb.layout(columns="1 1"):
        tgb.chart(figure="{fig7}")
        tgb.chart(figure="{fig8}")

    tgb.html("br")

    # Row 3
    with tgb.layout(columns="1 1"):
        tgb.chart(figure="{fig9}")
        tgb.chart(figure="{fig10}")

    tgb.html("br")

    # Row 4
    with tgb.layout(columns="1 1"):
        tgb.chart(figure="{fig11}")
        tgb.chart(figure="{fig12}")

    tgb.html("br")

    # Row 5
    with tgb.layout(columns="1 1"):
        tgb.chart(figure="{fig13}")
        tgb.chart(figure="{fig14}")

    tgb.html("br")


with tgb.Page() as non_smoker_stroke_page:
    tgb.text("# Non-Smoker Stroke Patients", mode="md")
    tgb.html("br")
    # Row 1
    with tgb.layout(columns="1 1"):
        tgb.chart(figure="{fig2}")
        tgb.chart(figure="{fig3}")
    tgb.html("br")
    # Row 2
    with tgb.layout(columns="1 1"):
        tgb.chart(figure="{fig4}")
        tgb.chart(figure="{fig5}")
    tgb.html("br")

pages = {
    "/": root_page,
    "general": general_stroke_page,
    "non_smoker": non_smoker_stroke_page,
}

# Run GUI
if __name__ == "__main__":
    Gui(pages=pages).run(
        title="Stroke Analysis Dashboard",
        dark_mode=False,
        debug=True,
        use_reloader=True,
        host="0.0.0.0",
        port="10000",
    )
