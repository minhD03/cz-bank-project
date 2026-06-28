{% set s3_bucket = 's3://berka-michael/' %}
{% set processed_file_path = params["processed_file_path"] %}
{% set table_name = processed_file_path.split('/')[-1].split('.')[0] %}
{% set full_s3_path = s3_bucket ~ processed_file_path %}

USE WAREHOUSE COMPUTE_WH;

COPY INTO "berka-michael".RAW.{{ table_name }}
FROM {{ full_s3_path }}
FILE_FORMAT = (TYPE = 'PARQUET')
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
STORAGE_INTEGRATION = s3_berka;