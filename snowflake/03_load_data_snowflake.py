import pandas as pd
import snowflake.connector
import os
from dotenv import load_dotenv

load_dotenv()
df = pd.read_csv("data/cold_chain_data.csv")

conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA")
)
cur = conn.cursor()
for _, row in df.iterrows():
    cur.execute("""
        INSERT INTO cold_chain_data (timestamp, container_id, temperature, location)
        VALUES (%s, %s, %s, %s)
    """, (row['timestamp'], row['container_id'], row['temperature'], row['location']))
cur.close()
conn.close()
print("Data loaded into Snowflake.")
