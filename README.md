#  Brain Stroke Data Analysis

##  Project Summary
This project analyzes stroke risks using health and demographic data from the [Stroke Prediction Dataset](https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset). It applies:
- An automated ETL pipeline
- Exploratory data analysis (EDA) techniques to visualize risk factors and identify key patterns through an interactive Taipy dashboard.
- Techniques to visualize risk factors and identify key patterns through an interactive **Taipy dashboard**.
🔗 Live Dashboard: [View Dashboard](https://brain-stroke-data-analysis.onrender.com/general)
---

## Core Idea
The goal is to build a data-driven, interactive dashboard that helps in understanding the impact of features like age, BMI and glucose level on stroke probability.

---

##  Key Features
-  **ETL Workflow**: Automated steps for loading, cleaning, encoding, and storing the data
-  **EDA & Outlier Detection**: Visual analysis of distributions and anomalies
-  **Taipy Dashboard**: Interactive interface for exploring stroke risk insights
-  **SQLite Integration**: Transformed data stored in a database file for simplicity (OLAP)

---

## 📦 Tech Stack
- Programming Language:`Python`
-  Storage: `SQLite`,
-  Scheduling: `APScheduler`
-  Data Synthization: `SDV`,  `Sklearn`
-  EDA: `Pandas`, `Seaborn`, `Matplotlib`
-  Dashboard: `Plotly`,`Taipy`
-  Testing and Formatting: `Pytest`, `Ruff`
-  CI/CD: `Github Actions`
-  Deployment: `Render`

---

## 🛠️ How to Run
```bash
git clone https://github.com/HaneenEzzat/Brain-Stroke-Data-Analysis.git
cd Brain-Stroke-Data-Analysis
python app.py
