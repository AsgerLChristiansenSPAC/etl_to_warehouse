if __name__ != "__main___":
    from utils import geojson

# Construct a row

def construct_row(**kwargs):
    """Takes key-value pairs and returns list of values, in order of keyword entry.
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


def transform_station_parameters(feature:dict):
    """Transform relevant properties
    from DMI geojson feature Station,
    for later loading."""

    # Hardcode table column names
    cols = ["dataSource",
            "stationId",
            "parameterId"]

    # Hardcode data-source
    data_source = "dmi"


    # Hardcode which properties to extract.
    station_id = geojson.get_property(
        feature, "stationId")
    
    parameter_ids = geojson.get_property(feature, "parameterId")
    
    station_parameters = []

    station_parameters.append(cols)
    for parameter_id in parameter_ids:
        row = construct_row(dataSource = data_source,
                      stationId = station_id,
                      parameterId = parameter_id)
        station_parameters.append(row)

    return station_parameters # List of lists
 


def transform_station(feature:dict):
    """Transform relevant properties
    from DMI geojson feature Station,
    for later loading."""

    # Hardcode table column names
    cols = ["dataSource",
            "stationId",
            "validTo",
            "validFrom"]

    # Hardcode data-source
    data_source = "dmi"


    # Hardcode which properties to extract.
    station_id = geojson.get_property(
        feature, "stationId")
    valid_to = geojson.get_property(feature, "validTo")
    valid_from = geojson.get_property(feature, "validFrom")

    row = construct_row(dataSource = data_source,
                      stationId = station_id,
                      validTo = valid_to,
                      validFrom = valid_from)
    return [cols, row] # List of lists
 

def transform_observation(feature:dict):

    observation = {"dataSource" : "dmi",
            "stationId" : geojson.get_property(
        feature, "stationId"),
            "parameterId" :  geojson.get_property(feature, "parameterId"),
            "calculatedAt" : geojson.get_property(feature, "calculatedAt"),
            "observationValue": geojson.get_property(feature, "value"),
            "timeResolution": geojson.get_property(feature, "timeResolution")
            
    }
    cols = list(observation.keys())

    row = construct_row(**observation)
    return [cols, row] # List of lists


if __name__ == "__main__":
    from utils import geojson
    featureStation = {
        "properties" :
        {
            "stationId" : 1,
            "validFrom" : 2,
            "validTo" : 3
        }

        
    }

    featureObs = {
        "properties" :
        {"stationId" : 1,
            "parameterId" :  2,
            "calculatedAt" : 3,
            "value" : 4,
            "observationValue":4,
            "timeResolution": 5
         }
    }

    print(transform_station(featureStation))
    print(transform_observation(featureObs))


