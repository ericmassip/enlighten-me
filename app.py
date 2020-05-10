import logging

import schedule
import requests

from flask import Flask, request

# from business_logic.country.service import country_service
# from business_logic.food.service import food_service
# from business_logic.agegroup.service import agegroup_service
from bulb import Bulb

# app = Flask(__name__)

LIFX_API = 'https://api.lifx.com/v1'
LIFX_API_TOKEN = 'c8c752462e6e252d11004eada7007657f345f7c4353b77f6d8d2f3b2e0a5071c'

CO2_SIGNAL_API = 'https://api.co2signal.com/v1/latest'
CO2_SIGNAL_TOKEN = '833dff203793160d'


# app.register_blueprint(country_service, url_prefix='/country')
# app.register_blueprint(agegroup_service, url_prefix='/agegroup')
# app.register_blueprint(food_service, url_prefix='/food')

def job():
    print("Updating bulb status...")
    update_bulb_state_2('FR')


schedule.every(1).seconds.do(job)



# @app.route('/update', methods=['POST'])
# def update_bulb_state():
#     bulb_data = request.get_json()
#     bulb = Bulb(bulb_data)
#
#     headers = {
#         'Authorization': 'Bearer %s' % LIFX_API_TOKEN,
#     }
#
#     payload = {
#         'power': 'on',
#         'color': 'red'
#     }
#
#     requests.put(LIFX_API + f'/lights/{bulb.selector}/state', data=payload, headers=headers)


def get_country_carbon_intensity_data(country_code):
    headers = {
        'auth-token': '%s' % CO2_SIGNAL_TOKEN,
    }

    response = requests.get(CO2_SIGNAL_API + f'?countryCode={country_code}', headers=headers)

    try:
        return response.json()['data']['carbonIntensity']

    except Exception:
        logging.error(response.json())
        return 800


def get_color(carbon_intensity):
    if 0 <= carbon_intensity <= 50:
        return '#6ac174'
    elif 50 <= carbon_intensity <= 100:
        return '#72bb5d'
    elif 100 <= carbon_intensity <= 150:
        return '#a1cd56'
    elif 150 <= carbon_intensity <= 200:
        return '#d8db50'
    elif 200 <= carbon_intensity <= 250:
        return '#ebd749'
    elif 250 <= carbon_intensity <= 300:
        return '#d8b341'
    elif 300 <= carbon_intensity <= 350:
        return '#d1a53e'
    elif 350 <= carbon_intensity <= 400:
        return '#c58c3a'
    elif 400 <= carbon_intensity <= 450:
        return '#bb7935'
    elif 450 <= carbon_intensity <= 500:
        return '#b26831'
    elif 500 <= carbon_intensity <= 550:
        return '#a8572c'
    elif 550 <= carbon_intensity <= 600:
        return '#994727'
    elif 600 <= carbon_intensity <= 650:
        return '#7e371c'
    elif 650 <= carbon_intensity <= 700:
        return '#602c11'
    elif 700 <= carbon_intensity <= 750:
        return '#482307'
    elif 750 <= carbon_intensity <= 800:
        return '#391e02'


def update_bulb_state_2(country_code):
    color = get_color(get_country_carbon_intensity_data(country_code))
    # bulb_data = request.get_json()
    selector = 'all'
    bulb_data = {'power': 'on', 'color': color + ' saturation:1', 'brightness': 0.5}
    bulb = Bulb(bulb_data)

    headers = {
        'Authorization': 'Bearer %s' % LIFX_API_TOKEN,
    }

    requests.put(LIFX_API + f'/lights/{selector}/state', data=bulb_data, headers=headers)


while True:
    schedule.run_pending()


# if __name__ == '__main__':
#     update_bulb_state_2()
