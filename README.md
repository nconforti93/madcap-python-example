# Welcome
Welcome to my GitHub repository. I hope you enjoyed my presentation at MadWorld 2023 on automation. 

# What is it
The repository contains the folder and Flare projects that we went through together looking at weather data. In the Content folder, you will already see 100 topics created automatically by the script for your reference. The Automation folder contains the Python scripts needed to run the automation. 

Finally, I zipped an empty project with no generated topics in there. You can import this Zipped Flare project and start from scratch if you like.

# How to use it
If you aren't familiar with GitHub, click the green **<> Code** button at the top and you can download it as a zip. For those familiar with GitHub, clone the repository locally.

# Prerequisites
* Install [Python 3](https://www.python.org/downloads/) and install the required packages defined in **Automation/requirements.txt**. You can directly do this with the following command:

```
pip install -r /path/to/requirements.txt
```

* In order to actually use the weather api, you need to create an account on [OpenWeatherMap](openweathermap.org/api) and subscribe to the One Call API 3.0. The first 1000 calls per day are free, however you will need to enter your credit card. Once you subscribe, click on your username in the top-right corner and go to ["My API Keys"](https://home.openweathermap.org/api_keys). Copy the string listed there and save it to a file called "api_secrets.py" in the **Automation** folder. The file should look like
```
openweather_api_key = 'my_key_here'
```
To avoid my API key being used (and potentially being charged for it), this file is not synced to GitHub! 

# Help
If you need any help, feel free to reach out to me on GitHub (issues) or via email (found at the bottom of the presentation!)
