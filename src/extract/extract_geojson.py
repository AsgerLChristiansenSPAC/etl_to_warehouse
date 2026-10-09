import requests
# Modified from: https://www.geeksforgeeks.org/python/how-to-make-api-calls-using-python/



def get_query(query):
    try:
        # Make a GET request to the API endpoint using requests.get()
        response = requests.get(query)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Call .json() method of requests.Response object, which creates dictionary from json string.
            stations = response.json() 
            return stations # Dictionary
        else:
            print('Error:', response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        # Handle any network-related errors or exceptions
        print('Error:', e)
        return None

def extract_features(feature_colletion:dict):
    try:
        features = feature_colletion["features"] # List of dicts.
        return features
    except KeyError as e:
        print(e)
        print("No features found, maybe not feature-collection")
        return None



def extract_property(feature:dict, property:str):
    return feature["properties"][property]

