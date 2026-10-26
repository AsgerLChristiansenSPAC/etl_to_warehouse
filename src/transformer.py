if __name__ != "__main___":
    from utils import geojson

def kwargs_to_values_list(**kwargs):
    """Takes key-value pairs and returns list of values, in order of keyword entry.
    Useful for turning dicts into SQL records."""
    row = [kwargs[key] for key in kwargs]
    return row


def feature_to_table_schema(feature:dict, mapper:dict, data_source = "dmi"):
    """Takes a geojson dictionary and
    a mapper (dictionary of table column names and 
    the associated geojson properties), and turns
    into "pseudo table" schema"""

    table_schema = {}
    table_schema.update({"dataSource" : data_source})
    property_mapping = {key : geojson.get_property(feature, val) for key, val in mapper.items()}
    table_schema.update(property_mapping)
    return table_schema

def schema_to_pseudo_table(table_schema:dict):
    cols = list(table_schema.keys())
    row = kwargs_to_values_list(**table_schema)
    return [cols, row] # List of lists

def transform_feature(feature:dict, mapper:dict, data_source = "dmi"):
    """Takes a geojson dictionary and
    a mapper (dictionary of table column names and 
    the associated geojson properties), and turns
    into "pseudo dataframe" (list of lists).
    First list is column names (AKA a header),
    subsequent lists are row entries."""
    table_schema = feature_to_table_schema(feature, mapper, data_source=data_source)
    pseudo_table = schema_to_pseudo_table(table_schema)
    return pseudo_table
    

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
        row = kwargs_to_values_list(dataSource = data_source,
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

    row = kwargs_to_values_list(dataSource = data_source,
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

    row = kwargs_to_values_list(**observation)
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

#    print(transform_station(featureStation))
#    print(transform_observation(featureObs))

    from configs.etl_config import TABLE_MAPPERS


    print(transform_feature(featureObs, TABLE_MAPPERS["observations"]))
    print(transform_feature(featureStation, TABLE_MAPPERS["stations"]))