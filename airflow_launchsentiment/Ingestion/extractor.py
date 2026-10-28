import gzip
import csv
import logging
import os
from config.settings import RAW_FILE_PATH, EXTRACTED_DIR, EXTRACTED_FILE_PATH, TARGET_COMPANIES

from utils.file_system import ensure_dir, file_exists


# Configure logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# Extractor function

def extract_companies():
    """
    Extract target companies from the Wikimedia pageviews .gz file.
    Keeps only English Wikipedia ('en') pages and target companies.
    Saves results to an intermediate file.
    """
    try:
        # Ensure extracted directory exists
        ensure_dir(EXTRACTED_DIR)
        logging.info(f"Ensured extracted directory exists: {EXTRACTED_DIR}")
        
        # Check if raw file exists
        if not file_exists(RAW_FILE_PATH):
            raise FileNotFoundError(f"Raw file not found at {RAW_FILE_PATH}")
        
        # Skip extraction if output file already exists (idempotency)
        if file_exists(EXTRACTED_FILE_PATH):
            logging.info(f"Extracted file already exists at {EXTRACTED_FILE_PATH}. Skipping extraction.")
            return
        
        logging.info(f"Starting extraction from {RAW_FILE_PATH} ...")
        
        # Read .gz file and filter lines
        with gzip.open(RAW_FILE_PATH, "rt", encoding="utf-8") as f, \
             open(EXTRACTED_FILE_PATH, "w", newline="", encoding="utf-8") as out_f:

            writer = csv.writer(out_f)
            for line in f:
                parts = line.strip().split()
                if len(parts) < 4:
                    continue  # skip malformed lines
                project, page_name, views, _ = parts
                if project == "en" and page_name in TARGET_COMPANIES:
                    writer.writerow([page_name, views])

        logging.info(f"Extraction completed successfully. Output saved to {EXTRACTED_FILE_PATH}")

    except Exception as e:
        logging.error(f"Extraction failed: {e}")
        raise
