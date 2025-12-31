from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import sys

# Make your pipeline importable
sys.path.append("/opt/airflow/airflow-launchsentiment")

from Ingestion.downloader import download_pageviews
from Ingestion.extractor import extract_companies
from Ingestion.transformer import transform_pageviews
from Ingestion.loader import load_to_mssql

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="launchsentiment_pipeline",
    default_args=default_args,
    schedule_interval=None,  
    start_date=datetime(2025, 12, 31),
) as dag:

    download_task = PythonOperator(
        task_id="download_pageviews",
        python_callable=download_pageviews
    )

    extract_task = PythonOperator(
        task_id="extract_companies",
        python_callable=extract_companies
    )

    transform_task = PythonOperator(
        task_id="transform_data",
        python_callable=transform_data 
    )

    load_task = PythonOperator(
        task_id="load_to_mssql",
        python_callable=load_to_mssql
    )

    # Set explicit dependencies
    download_task >> extract_task >> transform_task >> load_task
