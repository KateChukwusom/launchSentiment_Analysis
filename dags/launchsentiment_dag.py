from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.standard.operators.python.PythonOperator import PythonOperator
import sys

# Make your pipeline importable
sys.path.append("/opt/airflow/airflow_launchsentiment")

from ingestion.downloader import download_pageviews
from ingestion.extractor import extract_companies
from ingestion.transformer import transform_pageviews
from ingestion.loader import load_to_mssql

default_args = {
    "executor": "LocalExecutor",
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="launchsentiment_pipeline",
    default_args=default_args,
    schedule_interval=None,  
    start_date=datetime(2025, 12, 31),
) as dag:

    download_data = PythonOperator(
        task_id="download_pageviews",
        python_callable=download_pageviews
    )

    extract_data = PythonOperator(
        task_id="extract_companies",
        python_callable=extract_companies
    )

    transform_data = PythonOperator(
        task_id="transform_data",
        python_callable=transform_data 
    )

    load_data = PythonOperator(
        task_id="load_to_mssql",
        python_callable=load_to_mssql
    )

    # Set explicit dependencies
    download_data >> extract_data >> transform_data >> load_data
