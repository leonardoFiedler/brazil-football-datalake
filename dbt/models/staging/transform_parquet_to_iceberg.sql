{{ config(
    materialized='table',
    schema='staging'
) }}

WITH parquet_data AS (
    SELECT * FROM parquet_scan('s3a://datalake/landing/2024/sc_teams.parquet')
)

SELECT * FROM parquet_data