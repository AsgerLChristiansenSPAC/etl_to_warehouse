import psycopg
import sys
def connect(host:str, dbname:str, user:str):
    """ Connect to the PostgreSQL database server.
    Requires hostname, databasename and username,
    and queries the user for password."""
    print(f"Please enter password for user {user}")
    password = input()

    logon_params = {"host" : host,
                    "dbname" : dbname,
                    "user" : user,
                    "password" : password}
    conn = None
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg.connect(**logon_params)
    except (Exception, psycopg.DatabaseError) as error:
        print(error)
        sys.exit(1)
    print("Connection successful")
    return conn


def insert_rows(conn, cols:list, rows:list, table, verbose = True):
    """Executes an INSERT INTO using a psycopg connection
    of input (list of columns, list of rows) into specified table."""

    # Comma-separated dataframe columns
    col_str = ','.join(list(cols))
    # SQL quert to execute
    unique_violations = 0
    cursor = conn.cursor()
    for row in rows:
        row_str = ','.join(["'"+str(item)+"'" for item in row])
        try:
            cursor.execute(f"""
            INSERT INTO {table} ({col_str})
            VALUES ({row_str});
            """)
        except psycopg.errors.UniqueViolation:
            unique_violations += 1
            conn.rollback()
            continue
    
    conn.commit()
    if unique_violations > 0:
        print(f"""{len(rows)} rows were tried loaded into table {table}.
        {unique_violations} duplicates detected.
        {len(rows) - unique_violations} rows succesfully inserted.""")
    else:
        if verbose:
            print(f"""{len(rows)} loaded.""")
    cursor.close()


def load(host, dbname, user, table, data:list):
    conn = connect(host, dbname, user)

    if len(data) > 0:

        cols = data[0]
        rows = data[1:]
    
        # INSERT INTO DB
        insert_rows(conn, cols = cols, rows = rows, table = table)
    
    # Close the connection
    conn.close()