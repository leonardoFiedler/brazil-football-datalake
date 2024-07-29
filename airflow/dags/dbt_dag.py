from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'owner': 'airflow'
}

dag = DAG(
    'dbt_trino_to_postgres',
    default_args=default_args,
    description='Transform data from Trino (Iceberg) to Postgres using DBT'
)

# Task para transformar dados na camada de staging usando Trino
dbt_run_staging = BashOperator(
    task_id='dbt_run_staging',
    bash_command='cd /opt/airflow/dbt && dbt run --models staging.transform_parquet_to_iceberg',
    dag=dag,
)

dbt_run_staging
