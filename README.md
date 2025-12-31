## LaunchSentiment Analysis ETL Pipeline
LaunchSentiment is a data pipeline project designed to analyze Wikipedia pageview data to generate sentiment indicators for selected companies (Amazon, Apple, Facebook, Google, Microsoft).

 This project demonstrates data engineering best practices including modularity, separation of concerns, idempotency, logging, error handling, and orchestration using Apache Airflow with Docker.

## Project Overview:
The main goal of LaunchSentiment is to ingest, process, and store hourly Wikipedia pageview data and produce actionable insights for sentiment analysis. It:

- Downloads hourly Wikipedia pageviews .gz files

- Extracts only relevant company data

- Transforms and load into a database (MSSQL) and 

- Performs simple analysis on pageviews

The pipeline’s orchestration is handled by Apache Airflow, where each ETL stage is executed as a PythonOperator task. Task dependencies are explicitly defined: the download must complete before extraction, extraction before transformation, and transformation before loading. Airflow is configured with the LocalExecutor, providing a reliable single-node execution environment while still supporting retries, logging, and observability. The pipeline is fully automated and reproducible.

## Project Structure
```
airflow/                        # Airflow project root
├── dags/                        # Airflow DAGs
│   └── launchsentiment_dag.py   # DAG to run LaunchSentiment pipeline
├── logs/                        
├── plugins/                     
├── docker-compose.yaml           
├── airflow-launchsentiment/      #  ETL pipeline project        
│   ├── Ingestion/                # Modular ETL stages
│   │   ├── downloader.py         # Download pageviews
│   │   ├── extractor.py          # Extract target company data
│   │   ├── transformer.py        # Transform to final format
│   │   └── loader.py             # Load into MSSQL
│   ├── config/                   # Config files
│   │   └── settings.py           # Paths, URLs, database config, target companies
│   └── utils/                    # filesystem operations
│       └── filesystem.py
├── .env                          # Airflow UID for non-root container
└── README.md                     # Project documentation
```
## Pipeline Design Principles
- Modularity
Each stage is isolated: downloader, extractor, transformer, loader.

-- Makes the code easier to maintain and test.
Rationale: Modularity ensures each stage is independent, testable, and maintainable.  

- Separation of Concerns

Each module has a single responsibility:

-- Downloader → download raw .gz files

-- Extractor → parse and filter relevant data

-- Transformer → clean and format for database

-- Loader → write to MSSQL

Rationale: Clear separation of concerns allows easy updates or replacements for any ETL stage and clear separation allows re-processing of specific stages without repeating the whole pipeline.


- Idempotency
Downloader checks if the file already exists to prevent re-downloading.

Rationale: Prevents duplicate entries during retries or re-runs.

- Single Source of Truth
All configurable parameters (date, hour, directories, URLs) are stored in settings.py.

Rationale: Single source of truth ensures consistencyand changes in one place propagate throughout the pipeline.

- Best Practices
-- Logging: using Python’s logging module

-- Error handling: exceptions are caught and logged

-- Memory efficiency: large .gz files downloaded in chunks

Rationale: Ensures observability and robustness, and it facilitates troubleshooting

## Best Practices Implemented
Separation of concerns: Each stage is independent.

Idempotency: Skip duplicate downloads, extracts, or inserts.

Error handling & logging: Each module logs progress and failures.

Airflow orchestration: PythonOperator for clear task orchestration.

LocalExecutor: Simple, reliable execution.

Modular configuration: All paths, URLs, and database settings in settings.py.





