from abc import ABC, abstractmethod


class Bulb(ABC):

    def __init__(self, url, color, headers):
        self.url = url
        self.color = color
        self.headers = headers

    @abstractmethod
    def update_bulb_state(self):
        pass

    @abstractmethod
    def _get_bulb_data(self):
        pass
