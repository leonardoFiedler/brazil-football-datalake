from __future__ import annotations

import sys
sys.path.insert(0, '/opt/airflow/src')

import logging

from airflow.decorators import dag, task

from ingestion.teams.sc_teams import process

log = logging.getLogger(__name__)

PATH_TO_PYTHON_BINARY = sys.executable


@dag(
    schedule=None,
    catchup=False,
    tags=["example"],
)
def example_python_decorator():
    # [START howto_operator_python]
    @task(task_id="print_the_context")
    def print_context(ds=None, **kwargs):
        print("Start execution")
        process()
        return "Whatever you return gets printed in the logs"

    run_this = print_context()

    run_this

example_python_decorator()