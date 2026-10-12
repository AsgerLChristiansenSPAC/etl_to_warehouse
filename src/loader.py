import psycopg
import sys
import pandas as pd
from load.load import connect, insert_rows

# Here you want to change your database, username & password according to your own values
param_dic = {
    "host"      : "localhost",
    "dbname"  : "test",
    "user"      : "developer",
    "password"  : "specialisterne"
}

table_name = "observations"
import load.mock_data as m

#data = m.MOCK_DATA

#cols = list(data.keys())
#data = [data[col] for col in cols]


data = m.MOCK_DATA

cols = data[0]
rows = data[1:]



conn = connect(param_dic)
    # Run the execute_many strategy
insert_rows(conn, cols = cols, rows = rows, table = "stationParameters")
    # Close the connection
conn.close()

# Adapted from: https://naysan.ca/2020/05/16/pandas-to-postgresql-using-psycopg2-bulk-insert-using-execute_values/
# Somewhat old - uses psycopg2 rather than psycopg.

