USE DATABASE "berka-michael";

USE SCHEMA RAW;

CREATE OR REPLACE TABLE DISTRICT (
    district_id INT PRIMARY KEY,
    A2 VARCHAR(100),
    A3 VARCHAR(100),
    A4 INT,
    A5 INT,
    A6 INT,
    A7 INT,
    A8 INT,
    A9 INT,
    A10 FLOAT,
    A11 INT,
    A12 FLOAT,
    A13 FLOAT,
    A14 INT,
    A15 INT,
    A16 INT
);

CREATE OR REPLACE TABLE ACCOUNT (
    account_id INT PRIMARY KEY,
    district_id INT,
    frequency VARCHAR(100),
    date DATE,
    FOREIGN KEY (district_id) REFERENCES DISTRICT(district_id)
);

CREATE OR REPLACE TABLE DISP (
    disp_id INT PRIMARY KEY,
    client_id INT,
    account_id INT,
    type VARCHAR(100)
);

CREATE OR REPLACE TABLE CARD (
    card_id INT PRIMARY KEY,
    disp_id INT,
    type VARCHAR(100),
    issued DATE,
    FOREIGN KEY (disp_id) REFERENCES DISP(disp_id)
);

CREATE OR REPLACE TABLE CLIENT (
    client_id INT PRIMARY KEY,
    gender VARCHAR(100),
    birth_date DATE,
    district_id INT,
    FOREIGN KEY (district_id) REFERENCES DISTRICT(district_id)
);

CREATE OR REPLACE TABLE LOAN (
    loan_id INT PRIMARY KEY,
    account_id INT,
    date DATE,
    amount FLOAT,
    duration INT,
    payments FLOAT,
    status VARCHAR(100),
    FOREIGN KEY (account_id) REFERENCES ACCOUNT(account_id)
);

CREATE OR REPLACE TABLE ORDERS (
    order_id INT PRIMARY KEY,
    account_id INT,
    bank_to VARCHAR(100),
    account_to INT,
    amount FLOAT,
    k_symbol VARCHAR(100),
    FOREIGN KEY (account_id) REFERENCES ACCOUNT(account_id)
);

CREATE OR REPLACE TABLE TRANS (
    trans_id INT PRIMARY KEY,
    account_id INT,
    date DATE,
    type VARCHAR(100),
    operation VARCHAR(100),
    amount INT,
    balance INT,
    k_symbol VARCHAR(100),
    bank VARCHAR(100),
    account INT
)

