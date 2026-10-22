from src.configs import postgres_config
import sql_utils as sql
import psycopg
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

host_name = postgres_config.host_name
new_database_name = postgres_config.new_database_name
superuser_name = postgres_config.superuser_name
superuser_password = postgres_config.superuser_password


# to run from terminal:
# uvicorn {filename}:{app_name} --reload

app = FastAPI()


def db_connect(host:str = host_name, dbname:str = new_database_name, user:str = superuser_name, password = superuser_password):
    if password == None:
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
        raise HTTPException(status_code=500, detail="Database connection error")
    print("Connection successful")
    return conn

class Station(BaseModel):
    dataSource: str
    stationId: str
    validFrom: str
    validTo: str | None = None



def read_data(table_name, model, **params):
    params = sql.evaluate_query_params(**params)
    conn = db_connect()
    cursor = conn.cursor()
    cols = list(model.__pydantic_fields__.keys())
    sql_code = sql.write_SELECT(cols,
                            table_name = table_name, **params)
    try:
        cursor.execute(sql_code)
        stations = cursor.fetchall()
        station_kwargs = [{cols[i] : item for i, item in enumerate(row)}
              for row in stations]
        station_list = [model(**row_kwargs) for row_kwargs in station_kwargs]
        cursor.close()
        conn.close()
        return station_list
    except psycopg.Error as e:
        print(f"Error reading {table_name}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to read {table_name}")


@app.get("/stations", response_model=list[Station])
def read_stations(stationId:str|None = None):
    station_list = read_data(table_name="stations", model = Station, stationId = stationId)
    return station_list



class StationParameter(BaseModel):
    dataSource: str
    stationId: str
    parameterId: str


@app.get("/stationParameters", response_model=list[StationParameter])
def read_station_parameters():
    station_list = read_data(table_name="stationParameters", model = StationParameter)
    return station_list


class Observation(BaseModel):
    dataSource: str
    stationId: str
    parameterId: str
    calculatedAt: str
    observationValue: float
    timeResolution: str

@app.get("/observations", response_model=list[Observation])
def read_observations(stationId:str|None = None, parameterId:str|None = None):
    station_list = read_data(table_name="observations",
                             model = Observation,
                             stationId = stationId,
                             parameterId = parameterId)
    return station_list
