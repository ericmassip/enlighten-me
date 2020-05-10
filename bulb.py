class Bulb:

    def __init__(self, bulb_data):
        self.power = bulb_data.get('power', '')
        self.color = bulb_data.get('color', '')
        self.brightness = bulb_data.get('brightness', '')
        self.duration = bulb_data.get('duration', '')
        self.infrared = bulb_data.get('infrared', '')
        self.fast = bulb_data.get('fast', False)

    def get_payload(self):
        return self.__dict__
