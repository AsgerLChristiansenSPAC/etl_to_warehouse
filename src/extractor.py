import utils.dmi_api as dmi_api
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
# Defining extract_dmi() as dmi-specific version of geo.get_query()

extract_dmi_collection = dmi_api.dmi_query(get_query)

# Make the function able to loop through pages.
extract_dmi_pages = dmi_api.loop_through_pages(extract_dmi_collection)
