# Pinterest Data Pipeline — Docker Rebuild

## Why this exists

The original Pinterest pipeline (pinterest-data-pipeline684) was built 
using managed AWS services — MSK (Kafka), MWAA (Airflow), Kinesis, 
S3, API Gateway, and Databricks. When the course environment was 
decommissioned, access to those resources was lost.

Rather than treating this as a dead end, I used it as an opportunity 
to rebuild the same architecture using containerised, open source, 
low-cost alternatives — demonstrating that the same engineering 
principles apply regardless of whether you're using managed cloud 
services or self-hosted infrastructure.

The containerised stack can also be deployed to AWS ECS or EKS with 
minimal changes, demonstrating that local development and cloud 
deployment use the same underlying infrastructure.

## What's been replaced

| Original (AWS managed) | Rebuild (containerised) | Status |
|------------------------|------------------------|--------|
| AWS MSK (Kafka) | Apache Kafka in Docker (KRaft) | ✅ Complete |
| AWS Kinesis | Apache Kafka (handles streaming too) | ✅ Complete |
| AWS API Gateway | FastAPI (Python) | ✅ Complete |
| AWS S3 | MinIO (S3-compatible local object storage) | 🔜 Sprint 3 |
| Databricks (Spark) | Apache Spark in Docker | 🔜 Sprint 4 |
| Databricks (transforms) | dbt Core + DuckDB | 🔜 Sprint 5 |
| AWS MWAA (Airflow) | Apache Airflow in Docker | 🔜 Sprint 6 |
| Databricks notebooks | Jupyter notebooks in Docker | 🔜 Sprint 7 |

## Running Kafka locally

```bash
cd docker
docker compose up
```

Requires Docker Desktop installed. Kafka will be available at 
localhost:9092. Topics are created automatically on first message.

## Sprint Plan

### ✅ Sprint 1 — Kafka (Complete)
Apache Kafka running locally in Docker using KRaft (no Zookeeper 
dependency). Three topics (pinterest.pin, pinterest.geo, pinterest.user) 
auto-created on first message. User posting emulator rewritten using 
the Faker library to generate synthetic data matching the original 
schema, removing the dependency on the decommissioned AWS RDS instance.

### ✅ Sprint 2 — FastAPI + Emulator (Complete)
AWS API Gateway replaced with a custom FastAPI application. Three POST 
endpoints built with Pydantic models for schema validation, tested via 
Swagger UI. Emulator updated to POST to FastAPI endpoints rather than 
producing directly to Kafka.

### 🔜 Sprint 3 — MinIO Data Lake
Add MinIO as a containerised S3-compatible data lake. Kafka Connect 
will sink data from Kafka topics into MinIO, replicating the original 
S3 storage layer. Fully containerised and added to docker-compose.

### 🔜 Sprint 4 — Spark Processing
Containerise Apache Spark to read from MinIO and apply bronze, silver, 
and gold table transformations. Connect Spark and MinIO containers in 
docker-compose. Existing Spark transformation logic from the original 
project will be adapted with minimal changes. Spark output written as 
Parquet files back to MinIO.

### 🔜 Sprint 5 — dbt Core + DuckDB (Transformation Layer)
Add DuckDB as a lightweight, containerised analytical warehouse. dbt 
Core will sit on top of DuckDB to apply SQL-based transformations and 
build a structured data model from the Spark-processed Parquet output. 
This replaces the Databricks notebook transformation layer with a 
portable, open-source equivalent — demonstrating platform-agnostic 
transformation design using industry-standard tooling.

### 🔜 Sprint 6 — Airflow Orchestration
Add Apache Airflow in Docker to orchestrate batch processing and trigger 
Spark jobs and dbt runs on schedule. Connect Airflow to the Spark and 
dbt containers in docker-compose. Existing DAG logic from the original 
project will be extended to cover the full batch pipeline.

### 🔜 Sprint 7 — Notebooks + Metadata Store
Add Jupyter notebooks in Docker for interactive data exploration and 
debugging transformations. Add Postgres and PGAdmin for metadata storage 
and querying — required by Airflow and useful for inspecting table state.

### 🔜 Sprint 8 — Data Quality
Integrate Soda.io for automated data quality checks and validation. 
Write tests against the bronze, silver, and gold tables to catch data 
drift and schema violations.

### 🔜 Sprint 9 — Cloud Deployment
Deploy the full containerised stack to AWS ECS or EKS, demonstrating 
that the local development environment translates directly to production 
cloud infrastructure.

## Status

Sprints 1 and 2 complete — Kafka running locally in Docker using KRaft, 
FastAPI endpoints live with Pydantic validation, tested via Swagger UI.
Sprint 3 next: Kafka producer logic wired into FastAPI endpoints, MinIO 
data lake added to docker-compose.
