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
