# Transform functions specific to DMI's climate API.
import datetime

def datetime_dmi(date_time):
    format = '%Y-%m-%dT%H:%M:%SZ'
    datetime_str = datetime.datetime.strptime(date_time, format)

    return datetime_str


## If useful to specify parameters as dict, use these functions:

def index_parameter_keys(parameters:dict):
    keys = list(parameters.keys())
    key_indeces = list(range(0,len(keys)))
    indexed_keys = [(keys[idx], idx) for idx in key_indeces]
    return indexed_keys

def chain_parameter(query_tail:str, key:str, value:str, first = False):
    key_val = key + '=' + value
    if first:
        query_tail = query_tail + key_val
    else:
        query_tail = query_tail + '&' + key_val
    return query_tail
    

def chain_parameters(parameters:dict):
    indexed_keys = index_parameter_keys(parameters)
    query_tail = '?'
    for key, idx in indexed_keys:
        value = str(parameters[key])
        if idx == 0: # If first entry, no ampersand
            query_tail = chain_parameter(query_tail, key, value, first = True)
        else: # If not first entry
            query_tail = chain_parameter(query_tail, key, value)
    return query_tail


def compose_query(url, parameters:dict = {}):
    if len(parameters)>0:
        query_tail = chain_parameters(parameters)
        query = url + query_tail
    else:
        query = url
    return query
        



