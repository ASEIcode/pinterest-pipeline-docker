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
