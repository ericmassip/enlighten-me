import datetime as dt
import json
import logging
import sys

import requests
import schedule

from bulbs.lifx_bulb import LIFXBulb
from bulbs.yeelight_bulb import YeelightBulb
from env import CO2_SIGNAL_TOKEN, YEELIGHT_BULB_IP, BULB_API_TOKEN

CO2_SIGNAL_API = 'https://api.co2signal.com/v1/latest'

with open("color_gradient.json") as json_file:
    color_gradient = json.load(json_file)


def update_bulb_job():
    zone = sys.argv[1]
    co2_response = get_country_carbon_intensity_data(zone)

    if 'error' in co2_response:
        logging.error(co2_response['error'])

    elif 'data' not in co2_response and 'message' in co2_response:
        logging.error(co2_response['message'])

    elif 'carbonIntensity' not in co2_response['data']:
        logging.error('Carbon intensity not found in response. Zone lost connection?')

    else:
        carbon_intensity = co2_response['data']['carbonIntensity']
        fossil_fuel_percentage = co2_response['data']['fossilFuelPercentage']
        carbon_color = get_carbon_intensity_color(carbon_intensity)

        update_bulb(carbon_color)

        print(f'Datetime = {dt.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")} | Zone = {zone} | '
              f'Carbon Intensity = {round(carbon_intensity, 2)} gCO2eq/kWh | Fossil Fuel Percentage = {round(fossil_fuel_percentage, 2)} %')


def get_country_carbon_intensity_data(country_code):
    headers = {
        'auth-token': '%s' % CO2_SIGNAL_TOKEN,
    }

    response = requests.get(CO2_SIGNAL_API + f'?countryCode={country_code}', headers=headers)

    return response.json()


def get_carbon_intensity_color(carbon_intensity):
    truncated_carbon_intensity = base_round(carbon_intensity)

    if truncated_carbon_intensity > 600:
        return color_gradient['600']

    else:
        return color_gradient[str(truncated_carbon_intensity)]


def base_round(x, base=20):
    return base * round(x / base)


def update_bulb(carbon_color):
    """
    Replace this bulb type with your own!
    """
    # Comment these lines if you do not want to use a LIFX Bulb
    LIFXBulb(url='https://api.lifx.com/v1',
             headers={'Authorization': 'Bearer %s' % BULB_API_TOKEN},
             color=carbon_color).update_bulb_state()

    # Comment these lines if you do not want to use a Xiaomi Yeelight Bulb
    YeelightBulb(url=YEELIGHT_BULB_IP,
                 color=carbon_color).update_bulb_state()


update_bulb_job()
schedule.every(1).minutes.do(update_bulb_job)

while True:
    schedule.run_pending()
