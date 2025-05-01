import pandas as pd
import sqlite3
import logging
import time
from apscheduler.schedulers.background import BackgroundScheduler
from sdv.single_table import GaussianCopulaSynthesizer
from sdv.metadata import SingleTableMetadata

# Configure Logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


# SQLite Connection
def get_connection():
    return sqlite3.connect("data_source.db")


# Function to Read Data from SQLite
def read_existing_data():
    connection = get_connection()
    query = "SELECT * FROM original_data"  # Read from the original data table
    df = pd.read_sql(query, connection)
    connection.close()
    return df


# Function to Generate Synthetic Data
def generate_synthetic_data(df, num_samples=10):
    # Define metadata
    metadata = SingleTableMetadata()
    metadata.detect_from_dataframe(df)

    # Initialize and fit the synthesizer
    synthesizer = GaussianCopulaSynthesizer(metadata)
    synthesizer.fit(df)

    # Generate synthetic data
    synthetic_data = synthesizer.sample(num_rows=num_samples)
    logging.info(f"Generated {num_samples} synthetic records")
    return synthetic_data


# Function to Append Synthetic Data to Raw Data
def append_synthetic_data(synthetic_data):
    connection = get_connection()

    # Append synthetic data to the raw_data table
    synthetic_data.to_sql("raw_data", connection, if_exists="append", index=False)
    connection.commit()
    connection.close()
    logging.info(f"Appended {len(synthetic_data)} synthetic records to 'raw_data'")


# Function to Display Raw Data
def display_raw_data():
    connection = get_connection()
    query = "SELECT * FROM raw_data ORDER BY ROWID DESC LIMIT 10"  # Show the latest 10 records
    raw_data = pd.read_sql(query, connection)
    connection.close()
    if not raw_data.empty:
        logging.info("Latest records in 'raw_data':")
        print(raw_data)
    else:
        logging.info("No data found in 'raw_data'.")


# Main Function to Run the Pipeline
def main_pipeline():
    logging.info("Starting data synthesis process...")
    df = read_existing_data()
    synthetic_data = generate_synthetic_data(
        df, num_samples=10
    )  # Generate 10 synthetic records
    append_synthetic_data(synthetic_data)  # Append synthetic data to raw_data
    display_raw_data()  # Display the latest records in raw_data
    logging.info("Data synthesis process completed successfully!")


# Scheduler Setup
scheduler = BackgroundScheduler()
scheduler.add_job(main_pipeline, "interval", minutes=1)  # Runs every 1 minute
scheduler.start()

logging.info("Scheduler started. Running every 1 minute...")

# Keep the script running
try:
    while True:
        time.sleep(1)  # Sleep to avoid high CPU usage
except KeyboardInterrupt:
    logging.info("Stopping scheduler...")
    scheduler.shutdown()
    logging.info("Scheduler stopped.")
