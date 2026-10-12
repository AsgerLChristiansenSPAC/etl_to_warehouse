import psycopg
import sys
def connect(params_dic):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg.connect(**params_dic)
    except (Exception, psycopg.DatabaseError) as error:
        print(error)
        sys.exit(1)
    print("Connection successful")
    return conn


def insert_rows(conn, cols, rows, table):

    # Create a list of tupples from the dataframe values
    # Comma-separated dataframe columns
    col_str = ','.join(list(cols))
    # SQL quert to execute
    cursor = conn.cursor()
    for row in rows:
        row_str = ','.join(["'"+str(item)+"'" for item in row])
        cursor.execute(f"""
        INSERT INTO {table} ({col_str})
        VALUES ({row_str});
        """)
    conn.commit()
   # except (Exception, psycopg2.DatabaseError) as error:
    #    print("Error: %s" % error)
    #    conn.rollback()
    #    cursor.close()
    #    return 1
    #print("execute_values() done")
    cursor.close()


