import etl.transform.geojson as t_geo

# Data entries in MOCK_FEATURE without entries is rendered as None in python,
# and null with dmi_prettyprint.

#dmi_prettyprint(MOCK_FEATURE)


# For a given feature (dictionary) in a list of features

# Get the following attributes:

# run extract_property on the following:


#print(stationId)
#print(parameterId)
# Then for each entry in the parameterId array

# Construct a row

def construct_row(**kwargs):
    """Takes key-value pairs and returns list, in order of keyword entry.
    Useful for turning dicts into SQL records."""
    row = [kwargs[key] for key in kwargs]
    return row


def str_to_sql(value:str): # String entries
    return "'"+str(value)+"'"

def float_to_sql(value:float):
    return str(value)

def value_to_sql(value):
    if type(value) == str:
        return str_to_sql(value)
    else:
        return float_to_sql(value)


def row_to_sql(row:list):
    """Takes list and turns into sql VALUES for INSERT INTO or similar."""
    begin = "("
    middle = ','.join([value_to_sql(item) for item in row])
    end =  ")"
    values = begin+middle+end
    return values



def cols_to_sql(cols:list):
    """Takes list of cols and turns into column string for SQL"""
    begin = "("
    middle = ','.join(cols) # All cols should be string!
    end =  ")"
    return cols_to_sql


def get_dmi_station_parameters(feature:dict):
    """Takes a station feature from dmi and turns into list of lists."""
    data_source = "dmi"
    station_id = t_geo.extract_property(feature, "stationId")
    parameter_ids = t_geo.extract_property(feature, "parameterId") # This is a list
    station_parameters = []
    cols = ["dataSource", "stationId", "parameterId"]
    station_parameters.append(cols)
    for parameter_id in parameter_ids:
        row = construct_row(dataSource = data_source,
                      stationId = station_id,
                      parameterId = parameter_id)
        station_parameters.append(row)

    return station_parameters
    





# And construct an appropriate header

# We need to improve our sql code. Run it through psycopg probably.
# DB setup can be bash, it's fine. But tables should be setup in psycopg. Shouldn't be hard.

# For now though:
