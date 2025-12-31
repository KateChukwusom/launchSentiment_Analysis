import logging
import csv
from logging import config
import pyodbc
from config.settings import TRANSFORMED_FILE_PATH, MSSQL_CONFIG
from utils.file_system import file_exists


# Configure logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def load_to_mssql():
    """
    Load transformed CSV into MSSQL table.
    Best practices included:
    - Logging
    - Error handling
    - Idempotency (skips if table already has data for this date/hour)
    """
    try:
        # Check if transformed file exists
        if not file_exists(TRANSFORMED_FILE_PATH):
            raise FileNotFoundError(f"Transformed file not found at {TRANSFORMED_FILE_PATH}")

        logging.info(f"Connecting to MSSQL database: {MSSQL_CONFIG['database']}")

        # Connect to MSSQL
        conn_str = (
            f"DRIVER={MSSQL_CONFIG['driver']};"
            f"SERVER={MSSQL_CONFIG['server']};"
            f"DATABASE={MSSQL_CONFIG['database']};"
            f"Trusted_Connection=yes;"
        )
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Check if data already exists for this date/hour (idempotency)
        date, hour = None, None
        with open(TRANSFORMED_FILE_PATH, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            first_row = next(reader, None)
            if first_row:
                date = first_row['date']
                hour = first_row['hour']

        cursor.execute(
            "SELECT COUNT(*) FROM pageviews WHERE date=? AND hour=?",
            date, hour
        )
        existing_count = cursor.fetchone()[0]
        if existing_count > 0:
            logging.info(f"Data for date {date} and hour {hour} already exists. Skipping load.")
            return

        # Load data into table
        logging.info(f"Loading data into MSSQL table...")
        with open(TRANSFORMED_FILE_PATH, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                cursor.execute(
                    """
                    INSERT INTO pageviews (company, views, date, hour)
                    VALUES (?, ?, ?, ?)
                    """,
                    row['company'], int(row['views']), row['date'], row['hour']
                )
        conn.commit()
        logging.info(f"Data loaded successfully into MSSQL table.")

    except Exception as e:
        logging.error(f"Loader failed: {e}")
        raise

    finally:
        try:
            cursor.close()
            conn.close()
            logging.info("Database connection closed.")
        except:
            pass



