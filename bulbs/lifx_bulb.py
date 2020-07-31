import requests

from bulbs.bulb import Bulb


class LIFXBulb(Bulb):

    def __init__(self, url, color, headers, selector='all'):
        super().__init__(url, color, headers)
        self.selector = selector

    def update_bulb_state(self):
        requests.put(url=self.url + f'/lights/{self.selector}/state',
                     data=self._get_bulb_data(),
                     headers=self.headers)

    def _get_bulb_data(self):
        return {'power': 'on',
                'color': self.color + ' saturation:1',
                'brightness': 0.5}
