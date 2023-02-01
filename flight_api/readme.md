# Flight Status Scraper
This project is a web scraper that scrapes flight status data from a website using Selenium and BeautifulSoup. It has a RESTful API built with Flask that allows users to search for flight status by flight number. The scraped data includes departure and arrival times, travel time, departure and arrival statuses, and start and end airports with codes and cities.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites
- [Python 3](https://docs.python.org/3/)
- [Flask](https://flask.palletsprojects.com/en/2.2.x/)
- [Selenium](https://selenium-python.readthedocs.io/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Regular expression (re)](https://docs.python.org/3/library/re.html)
- [Chrome webdriver](https://chromedriver.chromium.org/documentation)

### Installing
You can install the required libraries by running the following command in your terminal:

- pip install Flask 
- pip install selenium 
- pip install beautifulsoup4
- pip install re

You can download the Chrome webdriver from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads).

### Running the API
To run the API, open your browser and access the following URL:
'http://localhost:5000/flightnumber?url=your_flightnumber'

Replace your_flightnumber with the flight number you wish to retrieve information for. The API will then retrieve information about the flight and display it on the browser.

### RESTful API
The RESTful API has one endpoint, /flight/<flight_number>, where flight_number is the flight number to search for.

#### Request
The endpoint accepts a GET request.

#### Response
The response is a JSON object containing the scraped flight data, or an error message if the flight number is not valid or the flight data could not be found.

## Used functions
### Validation of Flight Number
The function validate_Flight_number validates the format of the flight number entered by the user. It checks if the flight number has a pattern of two letters followed by one to five numbers, using a regular expression pattern.

### Extracting Flight Data
The function extract_flight_data takes an HTML page as input and uses BeautifulSoup to parse the page and extract relevant information, such as departure and arrival times, travel time, departure and arrival statuses, and start and end airports with codes and cities.

### Cleaning Flight Data
The function clean_flight_data takes the extracted flight data and removes unwanted characters, such as newlines and tabs, to ensure that the data is clean and easy to use.

### Limitations
This program is limited by the website it scrapes, as the website's structure and content may change over time. If the website's structure changes, the program may need to be updated to continue scraping the correct data. Additionally, the program is limited to searching for flight status by flight number, and may not work for all airlines or flight numbers.
