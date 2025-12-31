# -- Execution Date and Hour
RUN_DATE = "2025-12-15"
RUN_HOUR = "16"

# Source Wikimedia Pageviews URL
WIKIMEDIA_BASE_URL = "https://dumps.wikimedia.org/other/pageviews"

PAGEVIEWS_URL = (
    f"{WIKIMEDIA_BASE_URL}/2025/2025-12/"
    f"pageviews-20251215-160000.gz"
)

# Base Data Directory
BASE_DATA_DIR = "/home/kate/launchsentiment"

RAW_DIR = f"{BASE_DATA_DIR}/raw"
EXTRACTED_DIR = f"{BASE_DATA_DIR}/extracted"
TRANSFORMED_DIR = f"{BASE_DATA_DIR}/transformed"

RAW_FILENAME = "pageviews.gz"
EXTRACTED_FILENAME = "pageviews.txt"
TRANSFORMED_FILENAME = "company_pageviews.csv"

RAW_FILE_PATH = f"{RAW_DIR}/{RAW_FILENAME}"
EXTRACTED_FILE_PATH = f"{EXTRACTED_DIR}/{EXTRACTED_FILENAME}"
TRANSFORMED_FILE_PATH = f"{TRANSFORMED_DIR}/{TRANSFORMED_FILENAME}"

# Business Rules
TARGET_PROJECT = "en"

TARGET_COMPANIES = [
    "Amazon",
    "Apple_Inc.",
    "Facebook",
    "Google",
    "Microsoft",
]

# Database Configuration
DB_TABLE = "company_pageviews"

MSSQL_CONFIG = {
    "driver": "{ODBC Driver 17 for SQL Server}",
    "server": r".\SQLEXPRESS",
    "database": "LaunchSentimentDB",
    "trusted_connection": "yes"
}
