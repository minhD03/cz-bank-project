import duckdb
from airflow.hooks.base import BaseHook

AWS_CONN = BaseHook.get_connection("aws")
AWS_ACCESS_KEY_ID = AWS_CONN.login
AWS_SECRET_ACCESS_KEY = AWS_CONN.password
AWS_S3_ENDPOINT = "berka-michael.s3.ap-southeast-4.amazonaws.com"
S3_BUCKET = "berka-michael"


class S3CsvFileProcessor:
    def __init__(self):
        self.conn = duckdb.connect()
        self.conn.execute(f"""
            CREATE OR REPLACE SECRET berka_michael (
                TYPE s3,
                KEY_ID '{AWS_ACCESS_KEY_ID}',
                SECRET '{AWS_SECRET_ACCESS_KEY}',
                REGION 'ap-southeast-4',
                SCOPE 's3://{S3_BUCKET}'
            );
        """)
        self.table_cleaning_rules = {
            "account": self._process_account,
            "card": self._process_card,
            "client": self._process_client,
            "disp": self._process_disp,
            "district": self._process_district,
            "loan": self._process_loan,
            "orders": self._process_orders,
            "trans": self._process_trans,
        }

    def _process_file(self, file_path):
        prefix, object_name = file_path.split("/", 1)
        table_name = object_name.split(".")[0]
        self.conn.execute(
            f"CREATE OR REPLACE TABLE {table_name} AS SELECT DISTINCT * FROM 's3://{S3_BUCKET}/{prefix}/{object_name}'"
        )
        cleaning_function = self._get_cleaning_function(table_name)
        cleaning_function()
        self._save_file(table_name)
        processed_file_path = f"processed/{table_name}.parquet"
        return processed_file_path

    def _get_cleaning_function(self, table_name):
        return self.table_cleaning_rules.get(table_name)

    def _process_account(self):
        self.conn.execute("""
            UPDATE account
                SET FREQUENCY = CASE
                    WHEN FREQUENCY = 'POPLATEK MESICNE' THEN 'MONTHLY ISSUANCE'
                    WHEN FREQUENCY = 'POPLATEK TYDNE' THEN 'WEEKLY ISSUANCE'
                    WHEN FREQUENCY = 'POPLATEK PO OBRATU' THEN 'ISSUANCE AFTER TRANSACTION'
                    ELSE FREQUENCY
                END;
        """)

    def _process_card(self):
        pass

    def _process_client(self):
        pass

    def _process_disp(self):
        self.conn.execute("""
            UPDATE disp
                SET TYPE = CASE
                    WHEN TYPE = 'DISPONENT' THEN 'USER'
                    ELSE TYPE
                END;
        """)

    def _process_district(self):
        pass

    def _process_loan(self):
        pass

    def _process_orders(self):
        self.conn.execute("""
            UPDATE orders
                SET K_SYMBOL = CASE
                    WHEN K_SYMBOL = 'POJISTNE' THEN 'INSURANCE'
                    WHEN K_SYMBOL = 'SIPO' THEN 'HOUSEHOLD'
                    WHEN K_SYMBOL = 'UVER' THEN 'LOAN'
                    ELSE K_SYMBOL
                END;
        """)

    def _process_trans(self):
        self.conn.execute("""
            UPDATE trans
                SET K_SYMBOL = CASE
                    WHEN K_SYMBOL = 'POJISTNE' THEN 'INSURANCE'
                    WHEN K_SYMBOL = 'SIPO' THEN 'HOUSEHOLD'
                    WHEN K_SYMBOL = 'UVER' THEN 'LOAN'
                    WHEN K_SYMBOL = 'SLUZBY' THEN 'STATEMENT'
                    WHEN K_SYMBOL = 'UROK' THEN 'INTEREST CREDITED'
                    WHEN K_SYMBOL = 'SANKC. UROK' THEN 'SANCTION INTEREST'
                    WHEN K_SYMBOL = 'DUCHOD' THEN 'OLD-AGE PENSION'
                    ELSE K_SYMBOL
                END;
            UPDATE trans
                SET OPERATION = CASE
                    WHEN OPERATION = 'VYBER KARTOU' THEN 'WITHDRAWAL'
                    WHEN OPERATION = 'VKLAD' THEN 'CREDIT IN CASH'
                    WHEN OPERATION = 'PREVOD Z UCTU' THEN 'COLLECTION FROM ANOTHER BANK'
                    WHEN OPERATION = 'VYBER' THEN 'WITHDRAWAL IN CASH'
                    WHEN OPERATION = 'PREVOD NA UCET' THEN 'REMITTANCE TO ANOTHER BANK'
                    ELSE OPERATION
                END;
            UPDATE trans
                SET TYPE = CASE
                    WHEN TYPE = 'PRIJEM' THEN 'CREDIT'
                    WHEN TYPE = 'VYDAJ' THEN 'DEBIT'
                    ELSE TYPE
                END;
        """)

    def _save_file(self, table_name):
        self.conn.execute(f"""
            COPY {table_name}
            TO 's3://{S3_BUCKET}/processed/{table_name}.parquet'
            (FORMAT 'parquet')
        """)
