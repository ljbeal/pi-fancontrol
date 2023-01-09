import logging
import os

import yaml
from logging.handlers import RotatingFileHandler

from casefan import CaseFan


class MainBoard:
    """
    Class to represent the thermal state of the Pi
    """

    def __init__(self, config: str = '/home/pi/fancontrol/config.yaml'):

        self._logger = logging.getLogger("temps")
        self._logger.setLevel(logging.DEBUG)

        handler = RotatingFileHandler(f'/home/pi/fancontrol/temps.log',
                                      maxBytes=102400,
                                      backupCount=2)
        self._logger.addHandler(handler)

        self._fans = []
        self.create_fans(config)

    @staticmethod
    def read_cpu_temp() -> float:
        """
        Obtain CPU temperature in Celsius as a float value by reading the temp
        file
        """

        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as o:
            temp = float(o.read().strip())/1000

        return temp

    def create_fans(self, config_file):
        """
        Creates fan objects from a yaml format config file

        Files should be in the following format:

        fan_name:
            pin: (int) pwm pin that the fan is attached to
            curve: (dict) fan curve in temp: percent format
                10: 20
                50: 50
                80: 100
        """
        with open(config_file, 'r') as o:
            data = yaml.safe_load(o)

        for name, data in data.items():

            if 'pin' not in data:
                raise ValueError(f'"pin" attribute not found in fan {name}')

            if 'curve' not in data:
                raise ValueError(f'"curve" attribute not found in fan {name}')

            self.add_fan(data['pin'], name, data['curve'])

    def add_fan(self, pin, name, curve):
        self._fans.append(CaseFan(pin, name, curve))

    @property
    def fans(self):
        return self._fans

    def update(self):
        t = self.read_cpu_temp()  # read the temp once per loop
        for fan in self.fans:
            newpc = fan.update(t)
            self._logger.info(f'for temperature {t}, set fan to {newpc}%')

    def cleanup(self):
        for fan in self.fans:
            fan.cleanup()


if __name__ == '__main__':
    piboard = MainBoard()

    print(f'cpu temp reported as {piboard.read_cpu_temp}°c')
