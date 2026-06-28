# CZ Bank Financial Project
# 1) Overview: 
This project utilizes Airflow to trigger DAGs and collect data from [CTU Relational](https://relational.fel.cvut.cz/dataset/Financial), saves raw and processed data into AWS S3 instance as Data Lake. Then, the datasets are formatted before saving it into Snowflake as Datawarehouse.
![alt text](https://github.com/minhD03/cz-bank-project/blob/f49a560568ebd10d6cff02e370b9c3fdb178eda4/images/Diagram1.png)
# 2) Datasets:
Below is the data schema. For further information, visit [This website](https://web.archive.org/web/20180506061559/http://lisp.vse.cz/pkdd99/Challenge/chall.htm)


![alt text](https://github.com/minhD03/cz-bank-project/blob/f49a560568ebd10d6cff02e370b9c3fdb178eda4/images/dataset.svg)

# 3) Core functions:
These are the steps inside the process:
![alt text](https://github.com/minhD03/cz-bank-project/blob/f49a560568ebd10d6cff02e370b9c3fdb178eda4/images/Diagram2.png)

- Get the table list from dataset source.
- Ingest the tables into AWS server.
- Process files by converting data into correct format (For example: Translating language into English).
- Create the tables inside Snowflake.
- Copy processed dataset into those created tables in Snowflake.
- Rename the District columns.

# 4) Installation steps:
- Initiate the container:

```bash
docker compose up -d --build
```

- Login to your local Airflow at (Username and password are "airflow"):
http://localhost:8080/

- Inside your AWS account
  + Create your S3 Bucket in your AWS, remember the Access ID and Secret Key.
  + Create a new IAM user with "AmazonS3FullAccess"
  + Create a new Role with "AmazonS3FullAccess" also change the trust relationship to recoginze the Snowflake in "Load to Datawarehouse" step:
    ```
      "Principal":
                "AWS": "Your arn code in snowflake. See details below for the code."
    ```

- Create your Snowflake account, then create new database and schema (optional).
- Inside Snowflake, run this command to create integrated Storage to Disable MFA (for 24 hours, set any number you want) and Interact with AWS:
  ```
  ALTER USER <username> SET MINS_TO_BYPASS_MFA = 1440;

  Create Storage integration
  CREATE STORAGE INTEGRATION s3_berka
      TYPE = EXTERNAL_STAGE
      STORAGE_PROVIDER = S3
      ENABLED = TRUE
      STORAGE_AWS_ROLE_ARN = "your ARN code from AWS Role"
      STORAGE_ALLOWED_LOCATIONS = ('s3://<your s3 bucket name>/');
  
  DESC INTEGRATION s3_berka;
  
  SHOW STORAGE INTEGRATIONS;
  ```

  Inside here, there is an ARN code to paste back into the "Principal" Section above.

- Inside Airflow, go to **Admin => Connection => Add a new record** and add these 2 connections:
    + Your AWS Access ID and Secret Key (aws).
    + Your snowflake account (snowflake) with schema, username, password, account (after successfully logged in the website will become "app.snowflake.com/a/b/", replace a/b/ into a-b), database, role (mostly ACCOUNTADMIN if your account is newly created), datawarehouse (mostly COMPUTE_WH).

- Configure the bucket name, database and schema name inside constant.py, all .sql files.
- Trigger the DAG and the dataset is ready inside snowflake.
- Use Power BI and log in to your Snowflake account to obtain the data for visualization.
