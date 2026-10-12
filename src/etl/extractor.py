import etl.extract.dmi_api as dmi_api
import etl.extract.geojson as e_geojson

# Defining extract_dmi() as dmi-specific version of geo.get_query()

extract_dmi_collection = dmi_api.dmi_query(e_geojson.get_query)

# Make the function able to loop through pages.
extract_dmi_pages = dmi_api.loop_through_pages(extract_dmi_collection)
