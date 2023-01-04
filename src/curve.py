import bisect


def get_duty_cycle(temp):
    # specify curve points in {temp: pwm} % format
    curve_points = {30: 10,
                    70: 65,
                    80: 100}

    temps = sorted(list(curve_points.keys()))

    # create flat lines outside of boundaries
    if temp <= min(temps):
        return curve_points[min(temps)]

    elif temp >= max(temps):
        return curve_points[max(temps)]

    # create linear lines between points
    # find lower and upper points for this temp
    temp_id = bisect.bisect(temps, temp)

    lower_bound = temps[temp_id - 1]
    upper_bound = temps[temp_id]

    lower_pwm = curve_points[lower_bound]
    upper_pwm = curve_points[upper_bound]

    # need y = mx + c form
    m = (upper_pwm - lower_pwm)/(upper_bound-lower_bound)
    c = upper_pwm - upper_bound * m

    output = temp * m + c

    if output < 0:
        return 0
    if output > 100:
        return 100

    return output
