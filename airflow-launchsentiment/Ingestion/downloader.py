import logging
import requests
import os
import time
from config.settings import RAW_DIR, RAW_FILE_PATH, PAGEVIEWS_URL
from utils.file_system import ensure_dir, file_exists

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

MAX_RETRIES = 3
CHUNK_SIZE = 1024 * 1024  # 1MB

def download_pageviews():
    """
    Download Wikimedia pageviews file with retry and size verification.
    """
    ensure_dir(RAW_DIR)

    if file_exists(RAW_FILE_PATH):
        logging.info(f"Raw file already exists: {RAW_FILE_PATH}. Skipping download.")
        return

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logging.info(f"Attempt {attempt}: Downloading from {PAGEVIEWS_URL}")

            response = requests.get(PAGEVIEWS_URL, stream=True, timeout=60)
            response.raise_for_status()

            expected_size = int(response.headers.get("Content-Length", 0))
            downloaded_size = 0

            with open(RAW_FILE_PATH, "wb") as f:
                for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)

            if expected_size and downloaded_size != expected_size:
                raise ValueError(
                    f"Incomplete download: expected {expected_size} bytes, got {downloaded_size}"
                )

            logging.info(
                f"Download completed successfully ({downloaded_size / (1024*1024):.2f} MB)"
            )
            return

        except Exception as e:
            logging.error(f"Download attempt {attempt} failed: {e}")
            if attempt < MAX_RETRIES:
                logging.info("Retrying download...")
                time.sleep(5)
            else:
                logging.error("All download attempts failed.")
                raise

