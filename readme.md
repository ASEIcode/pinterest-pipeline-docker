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
| AWS S3 | MinIO (S3-compatible local object storage) | 🔜 Sprint 3 |
| AWS MWAA (Airflow) | Apache Airflow in Docker | 🔜 Sprint 5 |
| AWS API Gateway | FastAPI (Python) | 🔜 Sprint 2 |
| Databricks notebooks | Jupyter notebooks in Docker | 🔜 Sprint 6 |

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
auto-created on first message. User posting emulator to be rewritten 
using the Faker library to generate synthetic data matching the original 
schema, removing the dependency on the decommissioned AWS RDS instance.

### 🔜 Sprint 2 — FastAPI Emulator
Replace AWS API Gateway with a custom FastAPI application. Rewrite the 
emulator to send data via FastAPI endpoints to Kafka. Build a custom 
Docker image for the FastAPI app and add it to docker-compose, connected 
to the Kafka container.

### 🔜 Sprint 3 — MinIO Data Lake
Add MinIO as a containerised S3-compatible data lake. Data from Kafka 
will sink into MinIO, replicating the original S3 storage layer. Fully 
containerised and added to docker-compose.

### 🔜 Sprint 4 — Spark Processing
Containerise Apache Spark to read from MinIO and apply bronze, silver, 
and gold table transformations. Connect Spark and MinIO containers in 
docker-compose. Existing Spark transformation logic from the original 
project will be adapted with minimal changes.

### 🔜 Sprint 5 — Airflow Orchestration
Add Apache Airflow in Docker to orchestrate batch processing and trigger 
Spark jobs on schedule. Connect Airflow to the Spark container in 
docker-compose. Existing DAG logic from the original project will be 
reused.

### 🔜 Sprint 6 — Notebooks + Metadata Store
Add Jupyter notebooks in Docker for interactive data exploration and 
debugging transformations. Add Postgres and PGAdmin for metadata storage 
and querying — required by Airflow and useful for inspecting table state.

### 🔜 Sprint 7 — Data Quality
Integrate Soda.io for automated data quality checks and validation. 
Write tests against the bronze, silver, and gold tables to catch data 
drift and schema violations.

### 🔜 Sprint 8 — Cloud Deployment
Deploy the full containerised stack to AWS ECS or EKS, demonstrating 
that the local development environment translates directly to production 
cloud infrastructure.

## Status

Sprint 1 complete — Kafka running locally in Docker using KRaft.