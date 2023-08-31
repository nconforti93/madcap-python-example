import requests
import datetime
import pytz

# Function make_api_request
# Input
#   url - the URL of the API we will connect to
#   parameters - Any parameters needed in the API call
# Output: response.json() - returns a json string containing the API response
# Purpose:
#   This function connects to an API and returns the results in JSON format
def make_api_request(url, parameters):
    response = requests.get(url, params=parameters)
    return response.json()

# Function convert_epoch_time
# Input
#   ts - timestamp to convert (in epoch format)
#   timezone - timezone of the newly converted timestamp
#   format - the format the timestamp should be returned as
# Output: timestamp matching the timezone and format specified (as string)
# Purpose:
#   This function will convert epoch times to a more human-readable time defined by the format given. The weather API
#   uses epoch time in all of its calls, so this must be converted
def convert_epoch_time(ts, timezone, format):
    utc_time = datetime.datetime.fromtimestamp(ts)
    converted_time = utc_time.astimezone(pytz.timezone(timezone))

    return converted_time.strftime(format)

# Function create_dict_with_multiple_units
# Input
#   conversion_type - either 'temperature' or 'speed'
#   value_metric - the metric that is converted
# Output: A dictionary with the a measure stored in either deg C or F or mps or m/s
# Purpose:
#   The weather API only returns things in either metric or imperial, so this function will store both values
#   This allows us to add it to the topic directly from the dictionary
def create_dict_with_multiple_units(conversion_type, value_metric):
    d = {}
    if conversion_type == 'temperature':
        d['Metric'] = str(round(value_metric)) + ' ' + u'\N{DEGREE SIGN}' + 'C'
        d['Imperial'] = str(round((value_metric * 1.8) + 32)) + ' ' + u'\N{DEGREE SIGN}' + 'F'

    if conversion_type == 'speed':
        d['Metric'] = str(round(value_metric)) + ' m/s'
        d['Imperial'] = str(round(value_metric * 2.236936)) + ' mph'

    return d

# Function get_weather_data:
# Input:
#   api_url = url to make the request to
#   api_parameters = parameters for the API call
# output:
#   weather_data: A list object with the current, hourly, and daily weather
# Purpose:
#   This function is the meat and potatoes. It will take the data from the API call and transform the values into a
#   human-readable format. Times are converted, Temps are given in either C or F, speeds in mph or m/s.
#   The weather_data list contains the following entries:
#       [0] current_weather, type dict
#       [1] hourly_forecast, type list
#       [2] daily_forecast, type list
#       [3] alerts, type string
def get_weather_data(api_url, api_parameters):
    data = make_api_request(api_url, api_parameters)

    # Initialize all required variables
    weather_data = []

    current_weather = {}
    hourly_forecast = []
    daily_forecast = []

    # Set all of the current weather attributes
    current_weather['time'] = convert_epoch_time(data['current']['dt'], data['timezone'], '%A, %B %d, %Y at %I:%M %p')
    current_weather['temp'] = create_dict_with_multiple_units('temperature', data['current']['temp'])
    current_weather['weather_conditions'] = data['current']['weather']
    current_weather['feels_like'] = create_dict_with_multiple_units('temperature', data['current']['feels_like'])
    current_weather['humidity'] = str(data['current']['humidity']) + ' %'
    current_weather['uv'] = str(data['current']['uvi'])
    current_weather['windspeed'] = create_dict_with_multiple_units('speed', data['current']['wind_speed'])

    # Add current_weather into weather_data list
    weather_data.append(current_weather)

    # Get hourly weather for the next 12 hours
    for i in range(0,12):
        hourly_weather = {}
        hourly_weather['time'] = convert_epoch_time(data['hourly'][i]['dt'], data['timezone'], '%I:%M %p')
        hourly_weather['temp'] = create_dict_with_multiple_units('temperature', data['hourly'][i]['temp'])
        hourly_weather['weather_conditions'] = data['hourly'][i]['weather']
        hourly_weather['chance_of_rain'] = str(round(data['hourly'][i]['pop'] * 100)) + '%'

        hourly_forecast.append(hourly_weather)

    # Add hourly weather to the weather_data list
    weather_data.append(hourly_forecast)

    # Get daily forecast for the next 7 days
    for x in range(0,7):
        daily_weather = {}
        daily_weather['time'] = convert_epoch_time(data['daily'][x]['dt'], data['timezone'], '%B %d')
        daily_weather['min temp'] = create_dict_with_multiple_units('temperature', data['daily'][x]['temp']['min'])
        daily_weather['max temp'] = create_dict_with_multiple_units('temperature', data['daily'][x]['temp']['max'])
        daily_weather['weather_conditions'] = data['daily'][x]['weather']
        daily_weather['chance_of_rain'] = str(round(data['daily'][x]['pop'] * 100)) + '%'

        daily_forecast.append(daily_weather)

    # Add daily forecast to the weather_data list
    weather_data.append(daily_forecast)

    # If there are any alerts, then store these as well.
    if "alerts" in data:
        weather_data.append(data['alerts'][0]['description'])
    else:
        weather_data.append("There are no alerts.")

    # Return a list of all of the weather
    return weather_data








