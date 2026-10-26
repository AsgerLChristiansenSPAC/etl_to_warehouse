# Quick-fix of import issues when importing this module.
# Not ideal, but it works.
if __name__ != "__main___":
    from utils import geojson



def list_kwargs_values(**kwargs):
    """Takes key-value pairs and returns list of values, in order of keyword entry.
    Useful for turning dicts into SQL records."""
    row = [kwargs[key] for key in kwargs]
    return row


def db_row_from_feature(feature:dict, mapper:dict, data_source = "dmi"):
    """Takes a geojson feature object, and
    a mapper (dictionary of postgres table column names and 
    the associated geojson properties), and turns
    into a "row-like" dictionary, whose keys match
    the column names of the database, rather
    than the names used in the geojson object.
    This function, with an appropriate mapper dict,
    should allow the transformation of data from
    multiple sources (with different naming schemes)
    into the same database.
    """
    db_row = {}
    db_row.update({"dataSource" : data_source})
    property_mapping = {key : geojson.get_property(feature, val) for key, val in mapper.items()}
    db_row.update(property_mapping)
    return db_row

def db_row_to_pseudo_table(db_row:dict):
    """Turns a db_row into a "pseudo-table", a list of lists
    where the first list contains column names,
    and the second list contains row entries.
    This structure is used for later
    execution of SQL INSERT using 
    psycopg."""
    cols = list(db_row.keys())
    row = list_kwargs_values(**db_row)
    return [cols, row] # List of lists


def transform_feature(feature:dict, mapper:dict, data_source = "dmi", array_properties:list = None):
    """Takes a geojson dictionary and
    a mapper (dictionary of table column names and 
    the associated geojson properties), and turns
    into "pseudo dataframe" (list of lists).
    First list is column names (AKA a header),
    subsequent lists are row entries."""
    table_schema = db_row_from_feature(feature, mapper, data_source=data_source)
    pseudo_table = db_row_to_pseudo_table(table_schema)
    return pseudo_table
    

def transform_station_parameters(feature:dict):
    """Transform relevant properties
    from DMI geojson feature Station,
    for later loading.
    This function could ideally be
    more flexible (using some of the unused
    functions in the geojson module).
    The reason it isn't is that the
    parameterId property from the dmi API
    has a many-to-one relationship between
    stations and observations, but is otherwise
    identical to any other geojson property. This is
    difficult to handle dynamically."""

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

    # Construct pseudo-table:
    station_parameters = []

    station_parameters.append(cols)
    for parameter_id in parameter_ids:
        row = list_kwargs_values(dataSource = data_source,
                      stationId = station_id,
                      parameterId = parameter_id)
        station_parameters.append(row)

    return station_parameters # List of lists
 



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