import logging

import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

from env import CO2_SIGNAL_TOKEN, LIFX_API_TOKEN

app = Flask(__name__)
CORS(app)

LIFX_API = 'https://api.lifx.com/v1'
CO2_SIGNAL_API = 'https://api.co2signal.com/v1/latest'


@app.route('/<zone>', methods=['GET'])
def get_carbon_intensity_data(zone):
    carbon_intensity_data = get_country_carbon_intensity_data(zone)

    return carbon_intensity_data


def get_country_carbon_intensity_data(country_code):
    headers = {
        'auth-token': '%s' % CO2_SIGNAL_TOKEN,
    }

    response = requests.get(CO2_SIGNAL_API + f'?countryCode={country_code}', headers=headers)

    return response.json()


@app.route('/setState', methods=['PUT'])
def set_bulb_state():
    json_response = request.get_json()

    headers = {
        'Authorization': 'Bearer %s' % LIFX_API_TOKEN,
    }

    requests.put(LIFX_API + f'/lights/{json_response["selector"]}/state', data=json_response["bulb_data"],
                 headers=headers)

    return jsonify({'response': 'Light bulb state updated'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
