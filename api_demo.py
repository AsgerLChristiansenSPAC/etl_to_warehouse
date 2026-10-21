from src.configs import postgres_config


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
        #sys.exit(1)
    print("Connection successful")
    return conn





class Station(BaseModel):
    dataSource: str
    stationId: str
    validFrom: str
    validTo: str | None = None

@app.get("/stations/", response_model=list[Station])
def read_stations():
    
    conn = db_connect()
    cursor = conn.cursor()
    try:
        cursor.execute("""SELECT dataSource,
                    stationId,
                    validFrom,
                    validTo
                    FROM stations""")
        stations = cursor.fetchall()
        # Convert the results to a list of Item objects
        station_list = [Station(dataSource=row[0], stationId=row[1], validFrom=row[2],
                                validTo=row[3]) for row in stations]
        cursor.close()
        conn.close()
        return station_list
    except psycopg.Error as e:
        print(f"Error reading stations: {e}")
        raise HTTPException(status_code=500, detail="Failed to read stations")


@app.get("/stations/{station_id}", response_model=Station)
def read_station(station_id):
    conn = db_connect()
    cursor = conn.cursor()
    try:
        cursor.execute("""SELECT dataSource,
                    stationId,
                    validFrom,
                    validTo
                    FROM stations
                    WHERE stationId = %s""", (station_id,))
        item = cursor.fetchall()
        if item:
            item_obj = Station(dataSource=item[0], stationId=item[1], 
                               validFrom=item[2],
                                validTo=item[3])
            cursor.close()
            conn.close()
            return item_obj
        else:
            raise HTTPException(status_code=404, detail="Station not found")
    except psycopg.Error as e:
        print(f"Error reading station: {e}")
        raise HTTPException(status_code=500, detail="Failed to read station")


class StationParameter(BaseModel):
    dataSource: str
    stationId: str
    parameterId: str

@app.get("/stationParameters/", response_model=list[StationParameter])
def read_all_station_parameters():
    
    conn = db_connect()
    cursor = conn.cursor()
    try:
        cursor.execute("""SELECT dataSource,
                    stationId,
                    parameterId
                    FROM stationParameters""")
        stationParameters = cursor.fetchall()
        stationParameter_list = [StationParameter(dataSource=row[0], stationId=row[1], parameterId=row[2]
                                                  ) for row in stationParameters]
        cursor.close()
        conn.close()
        return stationParameter_list
    except psycopg.Error as e:
        print(f"Error reading stationParameters: {e}")
        raise HTTPException(status_code=500, detail="Failed to read stationParameters")



@app.get("/stationParameters/{station_id}", response_model=list[StationParameter])
def read_station_parameters(station_id):
    
    conn = db_connect()
    cursor = conn.cursor()
    try:
        cursor.execute("""SELECT dataSource,
                    stationId,
                    parameterId
                    FROM stationParameters
                    WHERE  stationId = %s""", (station_id,))
        stationParameters = cursor.fetchall()
        # Convert the results to a list of Item objects
        stationParameter_list = [StationParameter(dataSource=row[0], stationId=row[1], parameterId=row[2]
                                                  ) for row in stationParameters]
        cursor.close()
        conn.close()
        return stationParameter_list
    except psycopg.Error as e:
        print(f"Error reading stationParameters: {e}")
        raise HTTPException(status_code=500, detail="Failed to read stationParameters")




class Observation(BaseModel):
    dataSource: str
    stationId: str
    parameterId: str
    calculatedAt: str
    observationValue: float
    timeResolution: str

@app.get("/observations/", response_model=list[Observation])
def read_observations():

    conn = db_connect()
    cursor = conn.cursor()
    try:
        cursor.execute("""SELECT dataSource,
                            stationId,
                            parameterId,
                            calculatedAt,
                            observationValue,
                            timeResolution
                            FROM observations""")
        observations = cursor.fetchall()
        # Convert the results to a list of Item objects
        observation_list = [Observation(dataSource=row[0], stationId=row[1], parameterId=row[2],
                                        calculatedAt=row[3],
                                        observationValue=row[4],
                                        timeResolution=row[5]) for row in observations]
        cursor.close()
        conn.close()
        return observation_list
    except psycopg.Error as e:
        print(f"Error reading observations: {e}")
        raise HTTPException(status_code=500, detail="Failed to read observations")

