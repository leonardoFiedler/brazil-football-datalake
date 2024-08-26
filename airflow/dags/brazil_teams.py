from __future__ import annotations

import sys
import duckdb

sys.path.insert(0, '/opt/airflow/src')

import logging

from airflow.decorators import dag, task, task_group

from ingestion.teams.sc_teams import process_sc_teams

log = logging.getLogger(__name__)

PATH_TO_PYTHON_BINARY = sys.executable


@dag(
    schedule=None,
    catchup=False
)
def brazil_teams():
    
    @task_group
    def process_state_teams_tg():
        
        @task
        def process_sc_teams_task():
            process_sc_teams()
            return "SC Teams done"
        
        @task
        def create_duck_db_table_task():
            with duckdb.connect("/opt/airflow/src/main.db") as conn:
                conn.execute("""
                            INSTALL httpfs;
                            LOAD httpfs;
                            SET s3_region='us-east-1';
                            SET s3_url_style='path';
                            SET s3_endpoint='minio:9000';
                            SET s3_access_key_id='minio' ;
                            SET s3_secret_access_key='minio123';
                            SET s3_use_ssl='false';
                            """)
                
                conn.sql(f"""
                    DROP TABLE IF EXISTS teams;
                    CREATE TABLE teams AS
                    SELECT * FROM read_parquet('s3://datalake/landing/teams/year=2024/*.parquet', filename = true);
                """)
        
        process_sc_teams_task() >> create_duck_db_table_task()

    process_state_teams_tg()

brazil_teams()