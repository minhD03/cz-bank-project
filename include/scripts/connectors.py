import boto3
from airflow.hooks.base import BaseHook
from sqlalchemy import create_engine


def _create_mysql_engine(db_config):
    """Create a SQLAlchemy engine for MySQL."""
    connection_string = (
        f"mysql+pymysql://{db_config['user']}:{db_config['password']}@"
        f"{db_config['host']}:{db_config['port']}/{db_config['database']}"
    )
    return create_engine(connection_string, echo=False)


def _get_s3_client():
    AWS_CONN = BaseHook.get_connection("aws")
    AWS_ACCESS_KEY_ID = AWS_CONN.login
    AWS_SECRET_ACCESS_KEY = AWS_CONN.password
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name="ap-southeast-4",
    )
    return s3_client
