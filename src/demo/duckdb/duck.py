import duckdb

# Conexão com DuckDB
con = duckdb.connect("/tmp/dbt.db")

# Instalar a extensão S3 e habilitar
con.execute("INSTALL httpfs;")
con.execute("LOAD httpfs;")

# Defina as credenciais e o endpoint do S3 (MinIO)
con.execute("SET s3_region='us-east-1';")
con.execute("SET s3_url_style='path';")
con.execute("SET s3_endpoint='localhost:9000';")
con.execute("SET s3_access_key_id='minio';")
con.execute("SET s3_secret_access_key='minio123';")
con.execute("SET s3_use_ssl = false;")

# Leia o arquivo Parquet e crie a tabela Iceberg
# con.execute("""
# CREATE TABLE iceberg_staging AS
# SELECT *
# FROM read_parquet('s3://datalake/landing/2024/sc_teams.parquet')
# """)

con.execute("""
describe table 's3://datalake/landing/2024/sc_teams.parquet';
""")

