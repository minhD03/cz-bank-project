import os
from datetime import datetime, timedelta

from airflow.decorators import dag, task
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

from include.constants import DB_CONFIG
from include.scripts.extract import _get_table_list, _ingest_table_to_s3
from include.scripts.process import S3CsvFileProcessor


@dag(
    schedule_interval=None,
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["berka"],
    template_searchpath=os.path.join(os.path.dirname(__file__), "../include/sql"),
)
def berka_pipeline():
    @task
    def get_table_list():
        tables = _get_table_list(DB_CONFIG)
        return tables

    @task
    def ingest_table(table_name):
        file_path = _ingest_table_to_s3(table_name, DB_CONFIG)
        return file_path

    table_list = get_table_list()

    @task
    def process_file(file_path):
        processor = S3CsvFileProcessor()
        processed_file_path = processor._process_file(file_path)
        return processed_file_path

    create_tables = SQLExecuteQueryOperator(
        task_id="create_tables",
        sql="create_tables.sql",
        conn_id="snowflake",
    )

    ingested_file_list = ingest_table.expand(table_name=table_list)
    processed_file_list = process_file.expand(file_path=ingested_file_list)

    load_to_dw = SQLExecuteQueryOperator.partial(
        task_id="load_to_dw",
        sql="load_to_dw.sql",
        conn_id="snowflake",
    ).expand(params=processed_file_list.map(lambda path: {"processed_file_path": path}))

    rename_columns = SQLExecuteQueryOperator(
        task_id="rename_columns",
        sql="rename_columns.sql",
        conn_id="snowflake",
    )

    processed_file_list >> create_tables >> load_to_dw >> rename_columns


berka_pipeline()
