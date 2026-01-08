import logging
import csv
from config.settings import EXTRACTED_FILE_PATH, TRANSFORMED_DIR, TRANSFORMED_FILE_PATH, RUN_DATE, RUN_HOUR
from utils.file_system import ensure_dir, file_exists

# -------------------------------
# Configure logging
# -------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def transform_data():
    """
    Transform extracted CSV into structured CSV for database:
    - Convert views to integer
    - Add date and hour
    - Save transformed CSV with header
    """
    try:
        # Ensure transformed directory exists
        ensure_dir(TRANSFORMED_DIR)
        logging.info(f"Ensured transformed directory exists: {TRANSFORMED_DIR}")

        # Check if extracted file exists
        if not file_exists(EXTRACTED_FILE_PATH):
            raise FileNotFoundError(f"Extracted file not found at {EXTRACTED_FILE_PATH}")

        # Skip if transformed file already exists (idempotency)
        if file_exists(TRANSFORMED_FILE_PATH):
            logging.info(f"Transformed file already exists at {TRANSFORMED_FILE_PATH}. Skipping transformation.")
            return

        logging.info(f"Starting transformation from {EXTRACTED_FILE_PATH} ...")

        # Read extracted CSV and transform
        transformed_rows = []
        with open(EXTRACTED_FILE_PATH, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) != 2:
                    continue  # skip malformed rows
                page_name, views = row
                try:
                    views_int = int(views)
                except ValueError:
                    views_int = 0  # handle invalid numbers
                transformed_rows.append([page_name, views_int, RUN_DATE, RUN_HOUR])

        # Write transformed CSV with header
        with open(TRANSFORMED_FILE_PATH, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["company", "views", "date", "hour"])  # header
            writer.writerows(transformed_rows)

        logging.info(f"Transformation completed successfully. {len(transformed_rows)} rows written to {TRANSFORMED_FILE_PATH}")

    except Exception as e:
        logging.error(f"Transformation failed: {e}")
        raise


