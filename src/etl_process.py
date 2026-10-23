import psycopg
import sys

from configs import etl_config
from configs import postgres_config
import extractor as extractor
import loader as loader
import transformer as transformer
from api_utils import geojson

# Defining extractor functions:

# Datetime format is:


# Takes datetime and stationId.

# Makes query.

# If more than one stationId returned, take most recent. Not great, but MVP.


def transform_and_load(feature, table):
    if table == "observations":
        transform_func = transformer.get_dmi_station_parameters
    elif table == "stationParameters":
        transform_func = None
    elif table == "stations":
        transform_func = None
    data = transform_func(feature)
    return data


def etl_stations(host, dbname, user, url, **kwargs):
    """Maps station data to tables Stations and StationParameters."""

    # EXTRACT:
    featureCollection =extractor.extract_dmi_collection(url = url,  **kwargs) # datetime and stationId go here.
    
    features = geojson.get_features(featureCollection)

    # How to deal with duplicate stations?
    # Easy. Within the station table, we have both stations and validfrom/to. Observations still map
    # to a single station.

    for feature in features: # For each station feature:
        stationParams = transformer.transform_station_parameters(feature)
        loader.load(host, dbname, user, table = "stationParameters", data = stationParams)
        station = transformer.transform_station(feature)
        loader.load(host, dbname, user, table = "stations", data = station)

        # get_dmi_station function here.


def prompt_inputs(datetime = None, station_id = None):
    if station_id == None:
        print("""No stationId specified. Please input stationId.
            See DMI's climate data API for details:
            https://www.dmi.dk/friedata/dokumentation/apis/climate-data-api-1
            To use default stationId, enter "d".
            """)
        station_input = input()
        if station_input == "d":
            stationId = etl_config.DEFAULT_STATION["stationId"]
        else: stationId = station_input
    if datetime == None:
        print(f"""No datetime specified. Please input datetime.
                Datetime format is {etl_config.DEFAULT_DATETIME["format"]}.
                Use '{etl_config.DEFAULT_DATETIME["sep"]}' between datetimes
                to specify start and endpoint.
                To use default datetime, enter "d".
                Default datetime: {etl_config.DEFAULT_DATETIME["datetime"]}""")
        datetime_input = input()
        if datetime_input == "d":
            datetime = etl_config.DEFAULT_DATETIME["datetime"]
        else:
            datetime = datetime_input
    return (datetime, stationId)

def etl_observations(host, dbname, user, url, **kwargs):
    """Maps station data to table Observations."""

    # EXTRACT:
    featureCollection =extractor.extract_dmi_collection(url = url,  **kwargs) # datetime and stationId go here.
    
    features = geojson.get_features(featureCollection)

    # How to deal with duplicate stations?
    # Easy. Within the station table, we have both stations and validfrom/to. Observations still map
    # to a single station.
    observations = []
    cols = None
    for feature in features: # For each station feature:
        observation = transformer.transform_observation(feature)
        if cols == None:
            cols = observation[0]
            observations.append(cols)
        observations.append(observation[1])
    loader.load(host, dbname, user, table = "observations", data = observations)

    
def etl(host = postgres_config.host_name,
                     dbname = postgres_config.new_database_name,
                     user = postgres_config.role_name,
                     url_stations = etl_config.DMI_CLIMATE_URLS["stations"],
                     url_observations = etl_config.DMI_CLIMATE_URLS["observations"],
                     stationId = None, datetime = None):
    
    datetime, stationId = prompt_inputs(datetime, stationId)

    etl_stations(host, dbname, user, url = url_stations, stationId = stationId, datetime = datetime)
    etl_observations(host, dbname, user, url = url_observations, stationId = stationId, datetime = datetime)




if __name__ == "__main__":
    TEST_INFO = {
    "host"      : postgres_config.host_name,
    "dbname"  : postgres_config.new_database_name,
    "user"      : postgres_config.role_name,
    "url" : etl_config.DMI_CLIMATE_URLS["stations"],
    "table" : "stationParameters",
    "datetime" : etl_config.DEFAULT_DATETIME["datetime"],
    "limit" : 5
    }
#    etl(**TEST_INFO, stationId = '06070')
    TEST_INFO = {
    "host"      : postgres_config.host_name,
    "dbname"  : postgres_config.new_database_name,
    "user"      : postgres_config.role_name,
    "url" : etl_config.DMI_CLIMATE_URLS["stations"],
    "datetime" : etl_config.DEFAULT_DATETIME["datetime"],
    "stationId" : '06070',
    "limit" : 5
    }
    #etl_stations(**TEST_INFO)
    TEST_INFO = {
    "host"      : postgres_config.host_name,
    "dbname"  : postgres_config.new_database_name,
    "user"      : postgres_config.role_name,
    "url" : etl_config.DMI_CLIMATE_URLS["observations"],
    "datetime" : etl_config.DEFAULT_DATETIME["datetime"],
    "stationId" : '06070',
    "limit" : 5
    }
    etl()

