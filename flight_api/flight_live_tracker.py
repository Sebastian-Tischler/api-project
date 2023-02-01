from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re

# Functions
# Validation of the flight number. Detects only if the format is correct!
def validate_Flight_number(string):
    pattern = re.compile("^[a-zA-Z0-9]{2}[0-9]{1,5}$")
    return bool(pattern.match(string))

# this function extracts the information from the html
def extract_flight_data(html):
    soup = BeautifulSoup(html, 'html.parser')#
    
    # Departure day
    departure_day = soup.select_one(".flightPageSummaryDepartureDay")
    if departure_day:
        departure_day = departure_day.text
    else:
        departure_day = None

    # Departure time
    departure_time = soup.select_one(".flightPageSummaryDeparture em")
    if departure_time:
        departure_time = departure_time.text
    else:
        departure_time = None

    # Departure status
    departure_status = soup.select_one(".flightPageDepartureDelayStatus")
    if departure_status:
        departure_status = departure_status.text
    else:
        departure_status = None

    # Arrival day
    arrival_day = soup.select_one(".flightPageSummaryArrivalDay")
    if arrival_day:
        arrival_day = arrival_day.text
    else:
        arrival_day = None

    # Arrival time
    arrival_time = soup.select_one(".flightPageSummaryArrival em")
    if arrival_time:
        arrival_time = arrival_time.text
    else:
        arrival_time = None

    #  Arrival status
    arrival_status = soup.select_one(".flightPageArrivalDelayStatus")
    if arrival_status:
        arrival_status = arrival_status.text
    else:
        arrival_status = None

    # Travel time
    travel_time = soup.select_one(".flightPageProgressTotal")
    if travel_time:
        travel_time = travel_time.text
    else:
        travel_time = None

    # Departure airport code
    start_airport_code = soup.select_one(".flightPageSummaryOrigin .flightPageSummaryAirportCode")
    if start_airport_code:
        start_airport_code = start_airport_code.text
    else:
        start_airport_code = None

    # Departure airport city
    start_airport_city = soup.select_one(".flightPageSummaryOrigin .flightPageSummaryCity")
    if start_airport_city:
        start_airport_city = start_airport_city.text
    else:
        start_airport_city = None

    # Destination airport code
    end_airport_code = soup.select_one(".flightPageSummaryDestination .flightPageSummaryAirportCode")
    if end_airport_code:
        end_airport_code = end_airport_code.text
    else:
        end_airport_code = None

    # Destination airport city
    end_airport_city = soup.select_one(".flightPageSummaryDestination .flightPageSummaryCity span")
    if end_airport_city:
        end_airport_city = end_airport_city.text
    else:
        end_airport_city = None

    return {
        'start_airport': (start_airport_code, start_airport_city),
        'end_airport': (end_airport_code, end_airport_city),
        'departure_day': departure_day,
        'departure_time': departure_time,
        'departure_status': departure_status,
        'arrival_day': arrival_day,
        'arrival_time': arrival_time,
        'arrival_status': arrival_status,
        'travel_time': travel_time
    }

# this function cleans the result dict
def clean_flight_data(flight_data):
    cleaned_data = {}
    for key, value in flight_data.items():
        try:
            if isinstance(value, tuple):
                cleaned_data[key] = (value[0].replace('\n', '').replace('\t', ''), value[1].replace('\n', '').replace('\t', ''))
            else:
                cleaned_data[key] = value.replace('\n', '').replace('\t', '').replace('\xa0', ' ')
        except:
            pass
    return cleaned_data

# define path
path = "C:\Program Files (x86)\chromedriver.exe"


app = Flask(__name__)

@app.route("/flightnumber", methods=["GET"])


def flightnumber():
    # get url
    url = request.args.get("url")


    if validate_Flight_number(url) == False:
        return 'no valid flightnumber'

    # create a new browser instance
    driver = webdriver.Chrome(path)


    # load website
    driver.get("https://de.flightaware.com/account/locale_switch.rvt?csrf_token=357218367&locale=en_US")

    # load input field
    input_field = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div/div[2]/div[1]/div[2]/div[1]/div/form/div[1]/ul/li/input")

    # insert flightnumber
    input_field.send_keys(url)
    input_field.send_keys(Keys.RETURN)

    # Agree cookie window
    try:
        button = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/button[2]")
        button.click()
    except:
        pass
    
    try:
        # Live Tracking
        live = driver.find_element(By.XPATH, '//*[@id="flightPageTourStep1"]')

        # save html content from live tracking
        html_content = live.get_attribute("outerHTML")
    except:
        return 'no results'

    # quit and close driver
    driver.quit()
    
    # extract information from html
    live_tracking = extract_flight_data(html_content)
    
    # cleane result dict
    result = clean_flight_data(live_tracking)
    
    # return result dict as json 
    return jsonify(result)

    

if __name__ == "__main__":
    app.run(debug=True)


# 'http://localhost:5000/flightnumber?url=your_flightnumber'
