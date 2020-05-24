from abc import ABC, abstractmethod


class Bulb(ABC):

    def __init__(self, url, headers, color):
        self.url = url
        self.headers = headers
        self.color = color

    @abstractmethod
    def update_bulb_state(self):
        pass

    @abstractmethod
    def _get_bulb_data(self):
        pass
