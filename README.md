# Banking Transaction Reconciliation

An end-to-end Data Engineering portfolio project.

## Project Overview

Build a banking transaction reconciliation pipeline
using Python, SQL, PostgreSQL, PySpark, Delta Lake,
Databricks, Apache Airflow and Azure.

## Objectives

- Ingest synthetic financial transactions
- Validate and transform transaction data
- Identify matched and unmatched transactions
- Detect duplicate and invalid records
- Generate reconciliation reports
- Automate the pipeline

## Project Status

-Stage 1 - Project Setup and Git  
Establish project folders, VS Code, Python environment and local Git repository.

-Stage 2 - synthetic transaction data generation  
Generate bank CSV and payment JSON datasets with deliberate exceptions.

-Stage 3 - Python ingestion, validation & quarantine  
Implement reusable ingestion, schema checks, duplicate detection, quarantine and logging.

-Stage 4 - PostgreSQL & data modelling  
Design transactions, ingestion batches and quarantine tables; apply keys and constraints
