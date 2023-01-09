import bisect
import logging
import os

try:
    import RPi.GPIO as GPIO
except ImportError:
    GPIO = None


class CaseFan:

    _pwmpins = {12: 'PWM0',
                18: 'PWM0',
                13: 'PWM1',
                19: 'PWM1'}

    def __init__(self,
                 pin: int,
                 name: str = None,
                 curve: dict = None):

        self._logger = logging.getLogger(f"fan-{pin}")
        self._logger.setLevel(logging.DEBUG)

        try:
            logfile = os.path.join(os.environ["HOME"], 'fancontrol', 'fans.log')
        except KeyError:
            logfile = os.path.join(os.getcwd(), 'fans.log')

        handler = logging.FileHandler(logfile)
        self._logger.addHandler(handler)

        if curve is None:
            curve = {0: 100,
                     100: 100}

        self._name = name
        self._curve = curve

        if pin not in CaseFan._pwmpins:
            self._logger.error(f'non PWM pin selected: {pin}')
            raise ValueError(f'pin selection ({pin}) is not a PWM pin! '
                             f'({list(CaseFan._pwmpins.keys())})')

        if GPIO:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(pin, GPIO.OUT)
            GPIO.setwarnings(False)

        self._pwmobj = GPIO.PWM(pin, 25000)
        self._pwmobj.start(25)

        self._logger.info(f'set up a fan on pin {pin}')

    @property
    def curve(self):
        return self._curve

    def update(self, temperature):

        curve_points = self.curve

        temps = sorted(list(curve_points.keys()))

        # create flat lines outside of boundaries
        if temperature <= min(temps):
            return curve_points[min(temps)]

        elif temperature >= max(temps):
            return curve_points[max(temps)]

        # create linear lines between points
        # find lower and upper points for this temp
        temp_id = bisect.bisect(temps, temperature)

        lower_bound = temps[temp_id - 1]
        upper_bound = temps[temp_id]

        lower_pwm = curve_points[lower_bound]
        upper_pwm = curve_points[upper_bound]

        # need y = mx + c form
        m = (upper_pwm - lower_pwm)/(upper_bound-lower_bound)
        c = upper_pwm - upper_bound * m

        return temperature * m + c

    def set_duty(self, pc: int):
        pc = int(pc)

        dmin = 0
        dmax = 100

        if dmin > pc > dmax:
            raise ValueError(f'duty cycle must be between {dmin} and {dmax}')

        self._pwmobj.ChangeDutyCycle(pc)
        # print(f'set fan duty cycle to {pc}')

    @staticmethod
    def cleanup():
        if GPIO is not None:
            GPIO.cleanup()
