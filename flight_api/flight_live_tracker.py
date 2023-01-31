from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re

# Funktionen
# Validierung der Flugnummer. Erkennt nur ob das Format richtig ist!
def validate_Flight_number(string):
    pattern = re.compile("^[a-zA-Z0-9]{2}[0-9]{1,5}$")
    return bool(pattern.match(string))

def extract_flight_data(html):
    soup = BeautifulSoup(html, 'html.parser')#
    
    # Abflugtag
    departure_day = soup.select_one(".flightPageSummaryDepartureDay")
    if departure_day:
        departure_day = departure_day.text
    else:
        departure_day = None

    # Abfluguhrzeit
    departure_time = soup.select_one(".flightPageSummaryDeparture em")
    if departure_time:
        departure_time = departure_time.text
    else:
        departure_time = None

    # Abflugstatus
    departure_status = soup.select_one(".flightPageDepartureDelayStatus")
    if departure_status:
        departure_status = departure_status.text
    else:
        departure_status = None

    # Ankufttag
    arrival_day = soup.select_one(".flightPageSummaryArrivalDay")
    if arrival_day:
        arrival_day = arrival_day.text
    else:
        arrival_day = None

    # Ankuftuhrzeit
    arrival_time = soup.select_one(".flightPageSummaryArrival em")
    if arrival_time:
        arrival_time = arrival_time.text
    else:
        arrival_time = None

    #  Ankuftstatus
    arrival_status = soup.select_one(".flightPageArrivalDelayStatus")
    if arrival_status:
        arrival_status = arrival_status.text
    else:
        arrival_status = None

    # Reisezeit
    travel_time = soup.select_one(".flightPageProgressTotal")
    if travel_time:
        travel_time = travel_time.text
    else:
        travel_time = None

    # Startflughfaen code
    start_airport_code = soup.select_one(".flightPageSummaryOrigin .flightPageSummaryAirportCode")
    if start_airport_code:
        start_airport_code = start_airport_code.text
    else:
        start_airport_code = None

    # Startflughafen Stadt
    start_airport_city = soup.select_one(".flightPageSummaryOrigin .flightPageSummaryCity")
    if start_airport_city:
        start_airport_city = start_airport_city.text
    else:
        start_airport_city = None

    # Zielflughafen code
    end_airport_code = soup.select_one(".flightPageSummaryDestination .flightPageSummaryAirportCode")
    if end_airport_code:
        end_airport_code = end_airport_code.text
    else:
        end_airport_code = None

    # Zielflughafen Stadt
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

def enter_text_and_press_enter(driver, element, text):
    element.send_keys(text)
    element.send_keys(Keys.RETURN)

# define path
path = "C:\Program Files (x86)\chromedriver.exe"


app = Flask(__name__)

@app.route("/flugnummer", methods=["GET"])

# get url
def flugnummer():
    url = request.args.get("url")


    if validate_Flight_number(url) == False:
        return 'keine gültige Flugnummer'

    # create a new browser instance
    driver = webdriver.Chrome(path)


    # load website
    driver.get("https://de.flightaware.com/account/locale_switch.rvt?csrf_token=357218367&locale=en_US")

    # Finden alle Eingabefelder auf der Seite
    input_field = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div/div[2]/div[1]/div[2]/div[1]/div/form/div[1]/ul/li/input")

    # Flugnummer eingeben
    input_field.send_keys(url)
    input_field.send_keys(Keys.RETURN)

    # Cookie Fenster zustimmen
    try:
        button = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/button[2]")
        button.click()
    except:
        pass
    
    try:
        # Live Tracking
        live = driver.find_element(By.XPATH, '//*[@id="flightPageTourStep1"]')

        # html content von live-tracking speichern
        html_content = live.get_attribute("outerHTML")
    except:
        return 'no results'


    driver.quit()

    live_tracking = extract_flight_data(html_content)

    result = clean_flight_data(live_tracking)

    return jsonify(result)

    

if __name__ == "__main__":
    app.run(debug=True)


# 'http://localhost:5000/flugnummer?url=your_flugnummer'
