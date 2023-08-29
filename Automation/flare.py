import os
from bs4 import BeautifulSoup, NavigableString


# Function insert_into_file
# Input
#   file_name - the absolute path of a file to be written
#   text - the contents of the file
# Output: None - the file is overwritten
# Purpose:
#   This function overwrites the content of file_name with the string in text
def insert_into_file(file_name, text):
    with open(file_name, "w", encoding="utf-8") as file:
        # The new line characters are replaced because Python and Flare use different characters. Not switching it causes
        # Extra line breaks all over the place
        file.write(str(text).replace('\r\n', '\n'))

# Function check_if_file_exists
# Input - file_name - absolute path of a file
# Output - boolean if the file exists or not
# Purpose:
#   Checks if the given file exists or not and returns a boolean for it
def check_if_file_exists (file_name):

    if os.path.isfile(file_name):
        return True
    else:
        return False

# Function create_file
# Input
#   path_to_file - absolute path of a file to be created
#   Title - The title of the file (h1)
#   Description - text which is stored in the description metadata
# Purpose
#   This function will create the given file and then insert the string in file_start_text into that file using
#   the insert_into_file function

def create_file(path_to_file, type_of_file, title):
    # Creates the file
    f = open(path_to_file, "x")

    # Define what starting text the file needs (defining the structure)

    if type_of_file == 'topic':
        file_start_text = f"""<?xml version="1.0" encoding="utf-8"?>
            <html xmlns:MadCap="http://www.madcapsoftware.com/Schemas/MadCap.xsd">
                <head><title>Weather in [%=Heading.Level1%]</title>
                    <meta name="description" content="This page shows the weather in [%=Heading.Level1%]" />
                </head>
                <body>
                    <h1>{title}</h1>
                    <h2>Current Weather</h2>
                    <div id="current">
                        <p>Please note the following alert:</p>
                    </div>
                    <h2>Today's forecast</h2>
                    <div id="forecast_hourly">
                    </div>
                    <h2>7 Day Forecast</h2>
                    <div id="forecast_daily">
                    </div>
                </body>
            </html>"""
    elif type_of_file == 'toc':
        file_start_text = f"""<?xml version="1.0" encoding="utf-8"?>
        <CatapultToc Version="1">
        </CatapultToc>
        """

    # Insert this text into the newly-created file
    insert_into_file(path_to_file,file_start_text)

def number_is_even(num):
    if num % 2 == 0:
        return True
    else:
        return False

# Function add_entry_to_toc
# Input
    # toc_soup_object - soup object which has the content of the TOC file
    # topic_name - the name of the topic to be inserted (also serves as the title)
# Output - toc_soup_object - returns the same soup object but overwritten with the new entry
# Purpose
#   Adds a new entry into the toc soup object. When this soup object is eventually written to the file, it will contain
#   the new entry added here. It is expected that the TOC file is only a list of files, no folders or anything.

def add_entry_to_toc(toc_soup_object, folder_name, topic_name):

    # Finds the object corresponding to 'CatapultToc' which is the top-level object in the TOC
    for entry in toc_soup_object.findAll('CatapultToc'):

        # Define properties for the new object, like title and the link to the file
        toc_props = {}
        toc_props['Title'] = f'{topic_name}'
        toc_props['Link'] = f'/Content/{folder_name}/{topic_name}.htm'
        #toc_props['Class'] = 'hidden'

        # Create new TocEntry tag with the above properties
        new_toc_entry = toc_soup_object.new_tag('TocEntry', **toc_props)

        # Add the new tag at the end of the 'CatapultToc' tag
        entry.append(new_toc_entry)
    return toc_soup_object

def create_table(*args):

    # Set any table attributes, if any are needed. For this script, none are needed
    table_attributes = {}
    table_attributes['style'] = "mc-table-style: url('../Resources/TableStyles/Alternate-Row-Color.css');"
    table_attributes['class'] = 'TableStyle-Alternate-Row-Color'
    table_attributes['cellspacing'] = '21'

    # Create table soup object to hold the table tag
    table_object = BeautifulSoup('')

    # Create new table tag and insert it into soup object
    new_tab = table_object.new_tag('table', **table_attributes)
    table_object.insert(0, new_tab)

    # Insert columns into the table by iterating through the list of arguments
    for k in args:
        col_attrs = {}
        col_attrs['class'] = 'TableStyle-Alternate-Row-Color-Column-Column1'

        # Create new column tag
        new_col = table_object.new_tag('col', **col_attrs)
        # Insert column into soup object
        table_object.find('table').append(new_col)

    # Create and insert empty thead and tbody tag
    thead = table_object.new_tag('thead')
    table_object.find('table').append(thead)
    tbody = table_object.new_tag('tbody')
    table_object.find('table').append(tbody)

    tr_attrs = {'class': 'TableStyle-Alternate-Row-Color-Head-Header1'}
    # Create new header row and insert it into thead div
    header_row = table_object.new_tag('tr')
    table_object.find('thead').append(header_row)

    # Iterate through arguments and insert the text into the only tr row in the header
    for k in args:
        th_attrs = {'class': 'TableStyle-Alternate-Row-Color-HeadE-Column1-Header1'}
        th = table_object.new_tag('th')
        th.insert(0, k)
        table_object.find('tr').append(th)

    return new_tab

# Function insert_row_into_table
# Input
    # table - soup object containing the table you are inserting
    # even - a boolean for if the row is even or odd. Some tables have different, alternating styles for rows. In our case, it doesn't matter
    # args - data to be inserted into the table
# Output - Table - overwritten soup object containing a table with the newly added row
# Purpose
#   Adds a row into the given table and returns the soup object with that new row
def insert_row_into_table(table, even, *args):
    soup_object = BeautifulSoup('', 'xml')

    if even:
        tr_attrs = {'class': 'TableStyle-Standard-Body-Body2'}
        td_attrs = {'class': 'TableStyle-Standard-BodyB-Column1-Body2'}
    else:
        tr_attrs = {'class': 'TableStyle-Standard-Body-Body1'}
        td_attrs = {'class': 'TableStyle-Standard-BodyB-Column1-Body1'}

    # Create new 'tr' tag to be inserted into the table
    tr = soup_object.new_tag('tr')

    # Loop through the argumemts (columns) to get the data to insert
    for arg in args:
        # create new 'td' tag
        td = soup_object.new_tag('td')
        #print(arg)

        # Add the text from the argument to the 'td' tag
        td.append(arg)
        # Append the td tag to the table row
        tr.append(td)
    # After all columns are inserted, add the 'tr' to the tbody tag
    table.find('tbody').append(tr)

    # return the table with the new row
    return table

def create_code_snippet(code_example, language):
    # Set up dict to hold the properties
    code_snippet_body_attrs = {}

    code_snippet_body_attrs['MadCap:useLineNumbers'] = "False"
    code_snippet_body_attrs['MadCap:lineNumberStart'] = "1"
    code_snippet_body_attrs['MadCap:continue'] = "False"
    code_snippet_body_attrs['xml:space'] = "preserve"
    if language != '':
        code_snippet_body_attrs['style'] = f'mc-code-lang: {language}'

    # Create soup object
    snippet_object = BeautifulSoup('', 'xml')
    # Create MadCap code snippet tag
    code_snippet = snippet_object.new_tag('MadCap:codeSnippet')
    code_snippet.append(snippet_object.new_tag('MadCap:codeSnippetCopyButton'))
    code_snippet_body = snippet_object.new_tag('MadCap:codeSnippetBody', **code_snippet_body_attrs)
    # Insert the text into the tag
    code_snippet_body.insert(0, NavigableString(code_example))
    code_snippet.append(code_snippet_body)

    # Return code snippet with text in it
    return code_snippet

def cross_reference(url, text):
    soup_object = BeautifulSoup('', "xml")
    props = {'href': url}
    xref = soup_object.new_tag('MadCap:xref', **props)
    xref.string = text
    return xref

# Function create_anchor_tag
# input
#   url - the url that is linked
#   the text for the a tag
# output - a_tag - a soup object containing anchor tag
# Purpose
#   This script creates an anchor tag with the given url and text and returns the new tag
def create_anchor_tag(url, text):
    soup_object = BeautifulSoup('', "xml")
    # Set the href property
    a_tag_props = {}
    a_tag_props['href'] = f'{url}'

    # Create new tag with the properties
    a_tag = soup_object.new_tag('a', **a_tag_props)
    # Set the text within the <a>...</a> tag
    a_tag.string = text

    return a_tag

def create_p_tag(text):
    soup_object = BeautifulSoup('', "xml")
    p_tag = soup_object.new_tag('p')
    #p_tag['id'] =
    p_tag.string = text

    return p_tag

def create_conditional_text(conditions, text):
    soup_object = BeautifulSoup('', "xml")
    tag = soup_object.new_tag('MadCap:conditionalText')
    tag['MadCap:conditions'] = conditions
    tag.string = text

    return tag


def initialize_toc(file_name):
    if not check_if_file_exists(file_name):
        create_file(file_name, 'toc', '')

    with open(file_name, encoding="utf-8-sig") as toc:
        toc_soup = BeautifulSoup(toc, "xml")

    toc_soup.find('CatapultToc').clear()

    insert_into_file(file_name, toc_soup)

    return toc_soup

def make_readable_text(text):
    if text == 'temp':
        return 'Temperature'
    elif text == 'weather_conditions':
        return 'Weather Conditions'
    elif text == 'feels_like':
        return 'Feels like'
    elif text == 'humidity':
        return 'Humidity (%)'
    elif text == 'uv':
        return 'UV Index'
    elif text == 'windspeed':
        return 'Wind speed'
    else:
        exit('Text not expected')

def get_value_from_metric(metric):
    soup_object = BeautifulSoup('', "xml")
    if isinstance(metric, dict):
        span = soup_object.new_tag('span')

        for k,v in metric.items():
            span.append(create_conditional_text(f"Units.{k}", v))
        return span
    elif isinstance(metric, list):
        return metric[0]['description']
    else:
        return metric

def initialize_topic(file_name, title):
    if not check_if_file_exists(file_name):
        create_file(file_name, 'topic', title)



    with open(file_name, encoding="utf-8-sig") as topic:
        topic_soup = BeautifulSoup(topic, "xml")

    # Clear content from the head tag in the topic
    header = topic_soup.find('head')
    header.clear()

    # re-add necessary details in the topic, such as topic, stylesheet, and description
    header.append(topic_soup.new_tag('title'))
    header.find('title').string = f"Weather in [%=Heading.Level1%]"
    header.append(topic_soup.new_tag('link', {'href': 'Resources/TableStyles/Alternate-Row-Color.css',
                                              'rel': 'stylesheet',
                                              'MadCap:stylesheetType': 'table'}))
    header.append(topic_soup.new_tag('meta', attrs={'name': 'description',
                                                    'content': f"This page shows the weather in [%=Heading.Level1%]"}))

    # Clear out the details_table
    current_weather = topic_soup.find('div', id='current')
    current_weather.clear()

    hourly_forecast = topic_soup.find('div', id='forecast_hourly')
    hourly_forecast.clear()

    daily_forecast = topic_soup.find('div', id='forecast_daily')
    daily_forecast.clear()

    return topic_soup

def initialize_snippet(file_name):
    with open(file_name, encoding="utf-8-sig") as snippet:
        snippet_soup = BeautifulSoup(snippet, "xml")

    body = snippet_soup.find('body')
    body.clear()

    list = snippet_soup.new_tag('ul')
    body.append(list)

    return snippet_soup

def update_current_weather(soup_object, weather_data):

    current_weather = soup_object.find('div', id='current')

    # Add time information
    p_tag_1 = soup_object.new_tag('p')
    p_tag_1.string = f"As of {weather_data[0]['time']} local time, the current weather is:"
    current_weather.append(p_tag_1)

    # Add temp and pictures
    p_tag_2 = soup_object.new_tag('p')
    p_tag_2['class'] = 'weather'

    # Add temperature with conditional text
    for unit,temp in weather_data[0]['temp'].items():
        p_tag_2.append(create_conditional_text(f"Units.{unit}", temp))

    # Add weather icon
    img_tag = soup_object.new_tag('img')
    img_tag['src'] = f"../Resources/Images/weather_icons/{weather_data[0]['weather_conditions'][0]['icon']}.png"
    img_tag['class'] = "icon_big"
    p_tag_2.append(img_tag)

    current_weather.append(p_tag_2)

    # Add table with weather data
    table = create_table('Metric', 'Value')
    counter = 1
    for metric, value in weather_data[0].items():
        if metric != 'time':
            table = insert_row_into_table(table, number_is_even(counter), make_readable_text(metric), get_value_from_metric(value))
            counter += 1

    current_weather.append(table)

    # add code alert
    p_tag_3 = soup_object.new_tag('p')
    p_tag_3.string = "Please note the following alert:"
    current_weather.append(p_tag_3)

    # Add code snippet
    current_weather.append(create_code_snippet(weather_data[3],''))

    return soup_object

def update_hourly_forecast(soup_object, weather_data):

    hourly_forecast = soup_object.find('div', id='forecast_hourly')

    table = create_table('Time', 'Weather', 'Temperature', 'Chance of Rain')
    counter = 1
    for time in weather_data[1]:
        table = insert_row_into_table(table, number_is_even(counter), time['time'], get_value_from_metric(time['weather_conditions']), get_value_from_metric(time['temp']), time['chance_of_rain'])
        counter += 1

    hourly_forecast.append(table)

    return soup_object


def update_daily_forecast(soup_object, weather_data):
    daily_forecast = soup_object.find('div', id='forecast_daily')

    table = create_table('Time', 'Weather', 'Min Temp', 'Max Temp', 'Chance of Rain')
    counter = 1
    for time in weather_data[2]:
        table = insert_row_into_table(table, number_is_even(counter), time['time'],
                                      get_value_from_metric(time['weather_conditions']),
                                      get_value_from_metric(time['min temp']), get_value_from_metric(time['max temp']), time['chance_of_rain'])
        counter += 1

    daily_forecast.append(table)

    return soup_object

def add_entry_to_snippet_list(soup_object, folder, topic_name):
    list = soup_object.find('ul')

    list_item = soup_object.new_tag('li')

    p_tag = soup_object.new_tag('p')
    p_tag.append(cross_reference(f'../../{folder}/{topic_name}.htm', topic_name))

    list_item.append(p_tag)

    list.append(list_item)

    return soup_object






