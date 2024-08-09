from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'airflow'
}

dag = DAG(
    'dbt_trino_to_postgres',
    default_args=default_args,
    description='Transform data from Trino (Iceberg) to Postgres using DBT'
)

# Task para transformar dados na camada de staging usando Trino
dbt_run_all = BashOperator(
    task_id='dbt_run_all',
    bash_command='cd /opt/airflow/dbt/brazil_football && dbt run',
    dag=dag,
)

dbt_run_all
