import pandas as pd
import plotly.graph_objects as go
import numpy as np


def chart1(df):
    categories = ["Never Smoked", "Formerly Smoked", "Smokes", "Unknown"]
    fig1 = go.Figure()

    for status in categories:
        subset = df[(df["smoking_status"] == status) & (df["stroke"] == "Yes")]
        count = len(subset)

        fig1.add_trace(
            go.Bar(
                x=[status], y=[count], name=status, text=[count], textposition="outside"
            )
        )

    fig1.update_layout(
        title="Stroke Cases by Smoking Status",
        xaxis_title="Smoking Status",
        yaxis_title="Stroke Count",
        barmode="group",
        template="plotly_white",
        height=600,
    )
    return fig1


def chart2(df):
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
    return fig2


def chart3(df):
    never_smoked_stroke_df = df[
        (df["smoking_status"] == "Never Smoked") & (df["stroke"] == "Yes")
    ]
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
    return fig3


def chart4(df):
    never_smoked_stroke_df = df[
        (df["smoking_status"] == "Never Smoked") & (df["stroke"] == "Yes")
    ]
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
    return fig4


def chart5(df):
    never_smoked_stroke_df = df[
        (df["smoking_status"] == "Never Smoked") & (df["stroke"] == "Yes")
    ]
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
    return fig5


def chart6(df):
    fig6 = go.Figure()
    fig6.add_trace(
        go.Box(y=df[df["stroke"] == "Yes"]["avg_glucose_level"], name="Stroke")
    )
    fig6.add_trace(
        go.Box(y=df[df["stroke"] == "No"]["avg_glucose_level"], name="No Stroke")
    )
    fig6.update_layout(
        title="Average Glucose Levels by Stroke Status",
        yaxis_title="Avg Glucose Level",
        template="plotly_white",
        height=600,
    )
    return fig6


def chart7(df):
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
    return fig7


def chart8(df):
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
    return fig8


def chart9(df):
    fig9 = go.Figure()
    for status3 in df["age_category"].unique():
        subset3 = df[(df["age_category"] == status3) & (df["stroke"] == "Yes")]
        count3 = len(subset3)
        fig9.add_trace(
            go.Bar(
                x=[status3],
                y=[count3],
                name=status3,
                text=[count3],
                textposition="outside",
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
    return fig9


def chart10(df):
    stroke_df = df[df["stroke"] == "Yes"]
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
    return fig10


def chart11(df):
    stroke_df = df[df["stroke"] == "Yes"]
    categories_glucose = ["Normal", "Prediabetic", "Diabetic"]
    glucose_count = stroke_df["avg_glucose_category"].value_counts()
    counts = [glucose_count.get(cat, 0) for cat in categories_glucose]
    fig11 = go.Figure(
        data=[
            go.Bar(x=categories_glucose, y=counts, text=counts, textposition="outside")
        ]
    )
    fig11.update_layout(
        title="Glucose Category",
        xaxis_title="Glucose Category",
        yaxis_title="Count",
        template="plotly_white",
        height=600,
    )
    return fig11


def chart12(df):
    stroke_df = df[df["stroke"] == "Yes"]
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
    return fig12


def chart13(df):
    stroke_df = df[df["stroke"] == "Yes"]
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
    return fig13


def chart14(df):
    stroke_df = df[df["stroke"] == "Yes"]
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
    return fig14
