# brazil-football-datalake

## 1. How to Run this project

0. Install Python (3.12), Docker, and Docker Compose
1. Install Airflow

```
docker build . --tag extending_airflow:latest -f airflow/Dockerfile
cd airflow
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env
docker compose up airflow-init -d
docker compose up -d
```

1. Install all softwares required

```
cd devops
docker compose up -d
```