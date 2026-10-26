def value_to_sql(value):
    """Adds single quotations around str-type 
    values, necessary for insertion in SQL."""
    if type(value) == str:
        return "'"+str(value)+"'"
    else:
        return value

def row_to_sql(row:list):
    """Takes list and turns into sql VALUES for INSERT INTO or similar."""
    begin = "("
    middle = ','.join([value_to_sql(item) for item in row])
    end =  ")"
    values = begin+middle+end
    return values


def cols_to_sql(cols:list):
    """Takes list of cols and turns into column string for SQL"""
    return ','.join(cols)


def write_sql_VALUES(rows):
    values_str = 'VALUES '
    first_row = True
    for row in rows:
        if not first_row:
            values_str = values_str + ","
        row_string = row_to_sql(row)
        values_str = values_str + row_string
        if first_row:
            first_row = False
    return values_str



def write_INSERT_INTO(cols, rows, table_name:str):
    col_str = cols_to_sql(cols)
    values_str = write_sql_VALUES(rows)
    insert_into_str =f"""INSERT INTO {table_name} {col_str}
    {values_str}"""

    return insert_into_str + ";"


def write_WHERE(operator = "=", **params):
    param_str = ''
    first_param = True
    for key, val in params.items():
        val = value_to_sql(val)
        if not first_param:
            param_str = param_str + ","
        else:
            first_param = False
        param_str = param_str + f"{key} {operator} {val}"
    return f"WHERE {param_str}"

def write_SELECT(cols:list, table_name, **params):
    col_str = cols_to_sql(cols)
    sql = f"SELECT {col_str} FROM {table_name}"
    if params:
        param_str = write_WHERE(**params)
        sql = sql + ' ' + param_str
    return sql + ";"

def evaluate_query_params(**params):
    """Removes query parameters of type None,
    allowing **params to be passed more smoothly
    to lower level functions."""
    none_keys = []
    for key, val in params.items():
        if val == None:
            none_keys.append(key)
    for key in none_keys:
        params.pop(key)
    return params


if __name__ == "__main__":
    rows = [
        (1,"a",3),
        (2,"b",4),
        (3,"c",5)
    ]
    cols = ["one", "two", "three"]
    table_name = "a_table"
    print(write_INSERT_INTO(cols, rows, table_name))
    params = {"one" : 2, "two" : "None", "three" : None}
    params = evaluate_query_params(**params)
    print(write_SELECT(cols, table_name, **params))