import api
import flare
import api_secrets

import pandas as pd
import os
import pycountry_convert as pc

# Variables

# Number of cities we want to get the weather for (max 100 because I didn't implement offsets)
number_of_cities = str(100)

# API Url we will connect to get the largest cities
geonames_api = \
    "https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/geonames-all-cities-with-a-population-500/records"

# Parameters for the API call to get the right data
geonames_parameters = {'select': 'name, ascii_name, latitude, longitude, country_code, population, timezone, country',
                       'where': 'population > 500000',
                       'order_by': 'population desc',
                       'limit': number_of_cities}

# List of additional cities we want the weather for (note - the city name must be unique!)
special_cities = ['Nuernberg',
                  'Chicago']

# URL for the API containing the weather data
weather_api = "https://api.openweathermap.org/data/3.0/onecall"

root_dir = os.path.realpath(
    os.path.join(os.path.dirname(__file__), '..'))  # Absolute Path to the top-level folder in the repo
content_folder_dir = root_dir + '\\Content'  # Absolute path to the content folder as the base for all files
toc_dir = root_dir + '\\Project\\TOCs\\Generated_TOCs'  # Absolute path to the directory containing the generated TOCs
snippet_dir = content_folder_dir + '\\Resources\\Snippets'

# List of snippet files stored in the project
snippets = [f'{snippet_dir}\\Africa.flsnp',
            f'{snippet_dir}\\Asia.flsnp',
            f'{snippet_dir}\\Europe.flsnp',
            f'{snippet_dir}\\NorthAmerica.flsnp',
            f'{snippet_dir}\\Oceania.flsnp',
            f'{snippet_dir}\\SouthAmerica.flsnp']

# List of TOCs stored in the project
TOCs = [f'{toc_dir}\\Africa.fltoc',
        f'{toc_dir}\\Asia.fltoc',
        f'{toc_dir}\\Europe.fltoc',
        f'{toc_dir}\\NorthAmerica.fltoc',
        f'{toc_dir}\\Oceania.fltoc',
        f'{toc_dir}\\SouthAmerica.fltoc']

if __name__ == "__main__":

    print(f"Requesting data for top {number_of_cities} cities")
    # Get list of 100 most populous cities using Geonames API
    cities = pd.json_normalize(api.make_api_request(geonames_api, geonames_parameters)["results"])

    # Add special cities to list
    for city in special_cities:
        geonames_parameters['where'] = f"ascii_name='{city}'"
        cities = pd.concat([cities, pd.json_normalize(api.make_api_request(geonames_api, geonames_parameters)["results"])])


    print("Initializing TOCs and snippets")

    # Initialize TOCs (open and empty them)
    TOC_soup_objects = {}
    for TOC in TOCs:
        TOC_soup_objects[TOC] = flare.initialize_toc(TOC)

    # Initialize snippets (open and empty them)
    snippet_soup_objects = {}
    for snippet in snippets:
        snippet_soup_objects[snippet] = flare.initialize_snippet(snippet)

    # Loop through all of the cities we got earlier

    for index, row in cities.sort_values('ascii_name').iterrows():
        print(f"Getting weather data for {row['ascii_name']}")

        # Connect to weather api now
        weather_parameters = {
            'appid': api_secrets.openweather_api_key,
            'exclude': 'minutely',
            'lat': row['latitude'],
            'lon': row['longitude'],
            'units': 'metric'}

        # Get the forecast for the specific city
        forecast = api.get_weather_data(weather_api, weather_parameters)

        # Convert the country code to the name of the continent so we know which folder to put it in
        continent_code = pc.country_alpha2_to_continent_code(row['country_code'])
        continent_name = pc.convert_continent_code_to_continent_name(continent_code).replace(' ', '')

        # Check if topic exists (if not, create it), and empty the topic
        topic = flare.initialize_topic(f'{content_folder_dir}/{continent_name}/{row["ascii_name"]}.htm',
                                       row["ascii_name"])

        # Add the current weather forecast to the top
        topic = flare.update_current_weather(topic, forecast)

        # Add the hourly forecast
        topic = flare.update_hourly_forecast(topic, forecast)

        # Add the daily forecast
        topic = flare.update_daily_forecast(topic, forecast)

        # Insert the new xml into the file
        flare.insert_into_file(f'{content_folder_dir}/{continent_name}/{row["ascii_name"]}.htm', topic)

        # Add to TOC
        for TOC in TOCs:
            if continent_name in TOC:
                TOC_soup_objects[TOC] = flare.add_entry_to_toc(TOC_soup_objects[TOC], continent_name, row['ascii_name'])

        # Add entry to the appropriate overview snippet
        for snippet in snippets:
            if continent_name in snippet:
                snippet_soup_objects[snippet] = flare.add_entry_to_snippet_list(snippet_soup_objects[snippet],
                                                                                continent_name, row['ascii_name'])

    print("Saving TOCs and snippets")
    # save all TOC files
    for file, soup in TOC_soup_objects.items():
        flare.insert_into_file(file, soup)

    # Save all snippets
    for file, soup in snippet_soup_objects.items():
        flare.insert_into_file(file, soup)
