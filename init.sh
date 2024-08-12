#!/usr/bin/env bash

cd /project/brazil_football/ && dbt compile

rm -f /airflow/airflow-webserver.pid

sleep 10
airflow db migrate
sleep 10
airflow scheduler & airflow webserver