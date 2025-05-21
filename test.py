import pytest
import pandas as pd
import sqlite3
import numpy as np
from chart_test import (
    chart1,
    chart2,
    chart3,
    chart4,
    chart5,
    chart6,
    chart7,
    chart8,
    chart9,
    chart10,
    chart11,
    chart12,
    chart13,
    chart14,
)


@pytest.fixture
def load_data():
    connection = sqlite3.connect("Data/enriche_data.db")
    query = "SELECT * FROM clean_stroke"
    df = pd.read_sql(query, connection)
    return df


def test_chart1(load_data):
    df = load_data
    fig1 = chart1(df)

    for trace in fig1.data:
        print(f"Trace: {trace.name}, Y-value: {trace.y[0]}")

    expected_total = df[df["stroke"] == "Yes"]["smoking_status"].notna().sum()

    total_y = sum(trace.y[0] for trace in fig1.data)

    assert total_y == expected_total, (
        f"Test Failed: Expected {expected_total}, but got {total_y}"
    )


def test_chart2(load_data):
    df = load_data
    fig2 = chart2(df)

    # Filter to Never Smoked stroke cases
    never_smoked_stroke_df = df[
        (df["smoking_status"] == "Never Smoked") & (df["stroke"] == "Yes")
    ]

    # Expected total stroke cases in this group
    expected_total = never_smoked_stroke_df.shape[0]

    # Print actual hypertension value counts (for verification)
    hypertension_count = never_smoked_stroke_df["hypertension"].value_counts()
    print(f"Expected total (stroke cases): {expected_total}")
    print(f"Hypertension count from data: {hypertension_count}")

    # Sum of all bar heights (Y-values from the trace)
    total_y = sum(fig2.data[0].y)  # Instead of trace.y[0], take all y-values

    print(f"Total Y (hypertension counts): {total_y}")

    assert total_y == expected_total, (
        f"Test Failed: Expected {expected_total}, but got {total_y}"
    )


def test_chart3(load_data):
    df = load_data
    fig3 = chart3(df)

    # Filter for Never Smoked stroke cases
    never_smoked_stroke_df = df[
        (df["smoking_status"] == "Never Smoked") & (df["stroke"] == "Yes")
    ]

    # Calculate expected total
    expected_total = never_smoked_stroke_df.shape[0]

    # Print residence type counts from the raw data for debug
    residence_count = never_smoked_stroke_df["Residence_type"].value_counts()
    print(f"Expected total (stroke cases): {expected_total}")
    print(f"Residence type count from data:\n{residence_count}")

    # Sum all Y-values from the chart
    total_y = sum(fig3.data[0].y)

    print(f"Total Y (residence type counts): {total_y}")

    # Assertion to check if the chart values match actual data
    assert total_y == expected_total, (
        f"Test Failed: Expected {expected_total}, but got {total_y}"
    )


def test_chart4(load_data):
    df = load_data
    fig4 = chart4(df)

    never_smoked_stroke_df = df[
        (df["smoking_status"] == "Never Smoked") & (df["stroke"] == "Yes")
    ]
    expected_total = never_smoked_stroke_df.shape[0]

    work_type_count = never_smoked_stroke_df["work_type"].value_counts()
    print(f"Expected total (stroke cases): {expected_total}")
    print(f"Work type counts from data:\n{work_type_count}")

    total_y = sum(fig4.data[0].y)
    print(f"Total Y (work type counts): {total_y}")

    assert total_y == expected_total, (
        f"Test Failed: Expected {expected_total}, but got {total_y}"
    )


def test_chart5(load_data):
    df = load_data
    fig5 = chart5(df)

    never_smoked_stroke_df = df[
        (df["smoking_status"] == "Never Smoked") & (df["stroke"] == "Yes")
    ]
    expected_total = never_smoked_stroke_df["bmi"].notna().sum()

    total_y = sum(fig5.data[0].y)
    print(f"Expected total (non-null BMI stroke cases): {expected_total}")
    print(f"Total Y (BMI bin counts): {total_y}")

    assert total_y == expected_total, (
        f"Test Failed: Expected {expected_total}, but got {total_y}"
    )


def test_chart6(load_data):
    df = load_data
    fig6 = chart6(df)

    stroke_count = df[df["stroke"] == "Yes"]["avg_glucose_level"].notna().sum()
    no_stroke_count = df[df["stroke"] == "No"]["avg_glucose_level"].notna().sum()

    trace_stroke = fig6.data[0]
    trace_no_stroke = fig6.data[1]

    print(
        f"Stroke count (non-null glucose): {stroke_count}, Boxpoints: {len(trace_stroke.y)}"
    )
    print(
        f"No stroke count (non-null glucose): {no_stroke_count}, Boxpoints: {len(trace_no_stroke.y)}"
    )

    assert len(trace_stroke.y) == stroke_count, (
        f"Expected {stroke_count} stroke glucose values, got {len(trace_stroke.y)}"
    )
    assert len(trace_no_stroke.y) == no_stroke_count, (
        f"Expected {no_stroke_count} non-stroke glucose values, got {len(trace_no_stroke.y)}"
    )


def test_chart7(load_data):
    df = load_data
    fig7 = chart7(df)

    expected_counts = df[df["stroke"] == "Yes"]["Residence_type"].value_counts()
    chart_counts = {trace.name: trace.y[0] for trace in fig7.data}

    print(f"Expected stroke counts by residence type:\n{expected_counts}")
    print(f"Chart counts:\n{chart_counts}")

    for residence_type, expected_count in expected_counts.items():
        actual_count = chart_counts.get(residence_type, 0)
        assert actual_count == expected_count, (
            f"{residence_type} - Expected {expected_count}, but got {actual_count}"
        )


def test_chart8(load_data):
    df = load_data
    fig8 = chart8(df)

    stroke_df = df[df["stroke"] == "Yes"]
    hist_values, bin_edges = pd.cut(stroke_df["age"], bins=11, retbins=True)
    expected_counts = (
        hist_values.value_counts().sort_index().values[::-1]
    )  # Reversed for chart match

    chart_y_values = fig8.data[0].y

    print(f"Expected histogram bin counts: {list(expected_counts)}")
    print(f"Chart Y-values: {list(chart_y_values)}")

    assert list(chart_y_values) == list(expected_counts), (
        "Mismatch between expected age distribution and chart values"
    )


def test_chart9(load_data):
    df = load_data
    fig9 = chart9(df)

    expected_counts = df[df["stroke"] == "Yes"]["age_category"].value_counts()
    chart_counts = {trace.name: trace.y[0] for trace in fig9.data}

    print(f"Expected stroke counts by age category:\n{expected_counts}")
    print(f"Chart bar counts:\n{chart_counts}")

    for age_cat, expected_count in expected_counts.items():
        actual_count = chart_counts.get(age_cat, 0)
        assert actual_count == expected_count, (
            f"{age_cat} - Expected {expected_count}, got {actual_count}"
        )


def test_chart10(load_data):
    df = load_data
    fig10 = chart10(df)

    stroke_df = df[df["stroke"] == "Yes"]
    expected_counts = stroke_df["work_type"].value_counts()
    chart_counts = {
        trace.x[i]: trace.y[i] for trace in fig10.data for i in range(len(trace.x))
    }

    print("Expected work_type counts (stroke cases):", dict(expected_counts))
    print("Chart work_type bar counts:", chart_counts)

    for work_type, expected_count in expected_counts.items():
        actual_count = chart_counts.get(work_type, 0)
        assert actual_count == expected_count, (
            f"Work Type '{work_type}' - Expected {expected_count}, got {actual_count}"
        )


def test_chart11(load_data):
    df = load_data
    fig11 = chart11(df)

    stroke_df = df[df["stroke"] == "Yes"]
    glucose_count = stroke_df["avg_glucose_category"].value_counts()
    expected_counts = [
        glucose_count.get(cat, 0) for cat in ["Normal", "Prediabetic", "Diabetic"]
    ]
    chart_y = fig11.data[0].y

    print("Expected glucose category counts:", expected_counts)
    print("Chart glucose bar values:", list(chart_y))

    assert list(chart_y) == expected_counts, (
        "Mismatch in glucose category values in chart"
    )


def test_chart12(load_data):
    df = load_data
    fig12 = chart12(df)

    stroke_df = df[df["stroke"] == "Yes"]
    bins = np.histogram_bin_edges(stroke_df["bmi"], bins="auto")
    expected_counts, _ = np.histogram(stroke_df["bmi"], bins=bins)

    chart_counts = fig12.data[0].y

    print("Expected BMI histogram counts:", list(expected_counts))
    print("Chart BMI bar counts:", list(chart_counts))

    # Check that each bar height matches the histogram count
    assert list(chart_counts) == list(expected_counts), (
        "Mismatch in BMI histogram counts between data and chart."
    )


def test_chart13(load_data):
    df = load_data
    fig13 = chart13(df)

    stroke_df = df[df["stroke"] == "Yes"]
    expected_gender_counts = stroke_df["gender"].value_counts()

    chart_labels = fig13.data[0].labels
    chart_values = fig13.data[0].values

    print("Expected gender counts (stroke):", dict(expected_gender_counts))
    print("Chart labels and values:", list(chart_labels), list(chart_values))

    for label, value in zip(chart_labels, chart_values):
        expected_value = expected_gender_counts.get(label, 0)
        assert value == expected_value, (
            f"Gender '{label}' - Expected {expected_value}, got {value}"
        )


def test_chart14(load_data):
    df = load_data
    fig14 = chart14(df)

    stroke_df = df[df["stroke"] == "Yes"]
    expected_counts = stroke_df["hypertension"].value_counts()
    chart_counts = {
        trace.x[i]: trace.y[i] for trace in fig14.data for i in range(len(trace.x))
    }

    print("Expected hypertension counts (stroke):", dict(expected_counts))
    print("Chart hypertension bar counts:", chart_counts)

    for hypertension_status, expected_count in expected_counts.items():
        actual_count = chart_counts.get(hypertension_status, 0)
        assert actual_count == expected_count, (
            f"Hypertension '{hypertension_status}' - Expected {expected_count}, got {actual_count}"
        )
