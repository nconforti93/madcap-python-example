import requests
import datetime
import pytz


def make_api_request(url, parameters):
    response = requests.get(url, params=parameters)
    return response.json()

def convert_epoch_time(ts, timezone, format):
    utc_time = datetime.datetime.fromtimestamp(ts)
    converted_time = utc_time.astimezone(pytz.timezone(timezone))

    return converted_time.strftime(format)

def create_dict_with_multiple_units(conversion_type, value_metric):
    d = {}
    if conversion_type == 'temperature':
        d['Metric'] = str(round(value_metric)) + ' ' + u'\N{DEGREE SIGN}' + 'C'
        d['Imperial'] = str(round((value_metric * 1.8) + 32)) + ' ' + u'\N{DEGREE SIGN}' + 'F'

    if conversion_type == 'speed':
        d['Metric'] = str(round(value_metric)) + ' m/s'
        d['Imperial'] = str(round(value_metric * 2.236936)) + ' mph'

    return d


def get_weather_data(api_url, api_parameters):
    data = make_api_request(api_url, api_parameters)

    weather_data = []

    current_weather = {}
    hourly_forecast = []
    daily_forecast = []

    current_weather['time'] = convert_epoch_time(data['current']['dt'], data['timezone'], '%A, %B %d, %Y at %I:%M %p')
    current_weather['temp'] = create_dict_with_multiple_units('temperature', data['current']['temp'])
    current_weather['weather_conditions'] = data['current']['weather']
    current_weather['feels_like'] = create_dict_with_multiple_units('temperature', data['current']['feels_like'])
    current_weather['humidity'] = str(data['current']['humidity']) + ' %'
    current_weather['uv'] = str(data['current']['uvi'])
    current_weather['windspeed'] = create_dict_with_multiple_units('speed', data['current']['wind_speed'])

    weather_data.append(current_weather)

    for i in range(0,12):
        hourly_weather = {}
        hourly_weather['time'] = convert_epoch_time(data['hourly'][i]['dt'], data['timezone'], '%I:%M %p')
        hourly_weather['temp'] = create_dict_with_multiple_units('temperature', data['hourly'][i]['temp'])
        hourly_weather['weather_conditions'] = data['hourly'][i]['weather']
        hourly_weather['chance_of_rain'] = str(round(data['hourly'][i]['pop'] * 100)) + '%'

        hourly_forecast.append(hourly_weather)

    weather_data.append(hourly_forecast)

    for x in range(0,7):
        daily_weather = {}
        daily_weather['time'] = convert_epoch_time(data['daily'][x]['dt'], data['timezone'], '%B %d')
        daily_weather['min temp'] = create_dict_with_multiple_units('temperature', data['daily'][x]['temp']['min'])
        daily_weather['max temp'] = create_dict_with_multiple_units('temperature', data['daily'][x]['temp']['max'])
        daily_weather['weather_conditions'] = data['daily'][x]['weather']
        daily_weather['chance_of_rain'] = str(round(data['daily'][x]['pop'] * 100)) + '%'

        daily_forecast.append(daily_weather)

    weather_data.append(daily_forecast)

    if "alerts" in data:
        weather_data.append(data['alerts'][0]['description'])
    else:
        weather_data.append("There are no alerts.")

    return weather_data








