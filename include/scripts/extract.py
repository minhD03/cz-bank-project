from io import BytesIO

import polars as pl

from include.constants import S3_BUCKET
from include.scripts.connectors import _create_mysql_engine, _get_s3_client


def _get_table_list(db_config):
    engine = _create_mysql_engine(db_config)
    with engine.connect() as conn:
        result = conn.execute("SHOW TABLES;")
        tables = [row[0] for row in result.fetchall()]
    return tables


def _ingest_table_to_s3(table_name, db_config):
    engine = _create_mysql_engine(db_config)
    query = f"SELECT * FROM `{table_name}`"
    df = pl.read_database(query, engine)
    s3 = _get_s3_client()
    if table_name == "order":
        table_name = "orders"
    buffer = BytesIO()
    df.write_csv(buffer)
    buffer.seek(0)
    file_path = f"raw/{table_name}.csv"
    try:
        s3.delete_object(Bucket=S3_BUCKET, Key=file_path)
    except Exception as e:
        print(f"Error deleting existing file: {e}")
    s3.upload_fileobj(buffer, S3_BUCKET, file_path)
    print(f"Uploaded {table_name} to S3 bucket {S3_BUCKET} as {file_path}")
    return file_path
