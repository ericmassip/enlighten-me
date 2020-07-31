import yeelight

from bulbs.bulb import Bulb


class YeelightBulb(Bulb):

    def __init__(self, url, color, headers=None):
        super().__init__(url, color, headers)
        self.yeelight_bulb = yeelight.Bulb(self.url)

    def update_bulb_state(self):
        self.yeelight_bulb.set_brightness(60)
        self.yeelight_bulb.set_rgb(*self._hex_to_rgb(self.color))

    def _get_bulb_data(self):
        pass

    @staticmethod
    def _hex_to_rgb(color):
        return [int(color.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4)]
