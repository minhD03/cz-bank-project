# CZ Bank Financial Project
# 1) Overview: 
This project utilizes Airflow to trigger DAGs and collect data from [CTU Relational](https://relational.fel.cvut.cz/dataset/Financial), saves raw and processed data into AWS S3 instance. Then, the datasets are formatted before saving it into Snowflake as Datawarehouse.
