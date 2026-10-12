

MOCK_DATA =  [
    ["dataSource", "stationId", "parameterId"],
    ["dmi","06060","power"],
    ["dmi","06060","finesse"],
    ["dmi","06060","resistance"]
    ]


if __name__ == "__main__":
    data = MOCK_DATA
    table = "test"

    cols = data[0]
    rows = data[1:]
    col_str = ','.join(cols)

    for row in rows:

        row_str = ','.join(["'"+str(item)+"'" for item in row])
        print(f"""
            INSERT INTO {table} ({col_str})
            VALUES ({row_str});
            """) # Use single quotes within the query!