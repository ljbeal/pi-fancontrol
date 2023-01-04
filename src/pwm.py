import RPi.GPIO as GPIO


class pwm:

    _pwmpins = {12: 'PWM0',
                18: 'PWM0',
                13: 'PWM1',
                19: 'PWM1'}

    def __init__(self,
                 pin: int = 12):

        if pin not in pwm._pwmpins:
            raise ValueError(f'pin selection ({pin}) is not a PWM pin! '
                             f'({list(pwm._pwmpins.keys())})')

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        GPIO.setwarnings(False)

        self._pwmobj = GPIO.PWM(pin, 25000)
        self._pwmobj.start(25)

    def set_duty(self, pc: int):
        pc = int(pc)

        dmin = 0
        dmax = 100

        if dmin > pc > dmax:
            raise ValueError(f'duty cycle must be between {dmin} and {dmax}')

        self._pwmobj.ChangeDutyCycle(pc)
        # print(f'set fan duty cycle to {pc}')

    def cleanup(self):
        GPIO.cleanup()
