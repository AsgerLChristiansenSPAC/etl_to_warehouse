# GLOBAL VARIABLES
DMI_CLIMATE_URLS = {
    "stations" : 'https://opendataapi.dmi.dk/v2/climateData/collections/station/items',
    "observations" : 'https://opendataapi.dmi.dk/v2/climateData/collections/stationValue/items'
}

DEFAULT_DATETIME = {
    "begin" : "2026-01-09T03:00:00Z",
    "end" : "2026-01-09T11:00:00Z",
    "sep" : "/",
    "format" : '%Y-%m-%dT%H:%M:%SZ'
}

DEFAULT_DATETIME.update({"datetime" : f"{DEFAULT_DATETIME["begin"]}{DEFAULT_DATETIME["sep"]}{DEFAULT_DATETIME["end"]}"})
DEFAULT_STATION = {
    "stationId" : '06070'
    #"limit" : 5
}
