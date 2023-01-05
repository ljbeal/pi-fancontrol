from casefan import CaseFan

if __name__ == '__main__':
    fanpwm = CaseFan(18)

    default = 50

    try:
        while True:
            duty = input(f'input duty cycle (0-100) [{default}]: ')

            if duty is None or duty == '':
                duty = default

            fanpwm.set_duty(duty)

    except KeyboardInterrupt:
        fanpwm.cleanup()
        print('\ninterrupt caught, exiting')

    except:
        fanpwm.cleanup()
        raise
