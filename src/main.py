import logging
import os.path
from logging.handlers import RotatingFileHandler

from pwm import pwm
from monitor import monitor
import time
import datetime


def get_duty_cycle(temp):

    if temp > 65:
        return 100

    return int(temp)


def update(pwm, monitor):
    cpu_t = monitor.cpu_temp
    drive_t = monitor.drive_temps

    t = max([cpu_t] + drive_t)
    fan_pc = get_duty_cycle(t)

    logtime = datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S')

    logstr = f'[{logtime}] cpu temp is {cpu_t}°c, ' \
             f'drive temps are {drive_t}°c. ' \
             f'setting duty cycle to {fan_pc}'

    logger = logging.getLogger("temps")
    logger.info(logstr)
    print(logstr)

    pwm.set_duty(fan_pc)


if __name__ == '__main__':
    fanpwm = pwm()
    temps = monitor()

    logger = logging.getLogger("temps")
    logger.setLevel(logging.DEBUG)

    handler = RotatingFileHandler('/home/pi/fancontrol/temps.log',
                                  maxBytes=102400,
                                  backupCount=2)
    logger.addHandler(handler)

    try:
        while True:
            update(fanpwm, temps)

            time.sleep(10)

    except KeyboardInterrupt:
        fanpwm.cleanup()
        print('\ninterrupt caught, exiting')

    except:
        fanpwm.cleanup()
        raise
