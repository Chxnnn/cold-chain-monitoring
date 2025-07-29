# utils/snowflake_conn.py

import os
from dotenv import load_dotenv
import snowflake.connector
import pandas as pd

load_dotenv()

def fetch_data():
    conn = snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA")
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM cold_chain_data;")
    df = cur.fetch_pandas_all()
    cur.close()
    conn.close()
    return df
