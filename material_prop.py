"""
Temperature-dependent material properties of steel acc. to Eurocode 1993-1-2
"""


def steel_elongation(temp):
    # EN 1993-1-2: 3.4.1.1
    if temp < 20:
        raise Exception('Temperature should be higher than 20 centigrades')
    elif temp < 750:
        elong = 1.2 * 10 ** (-5) * temp + 0.4 * 10 ** (-8) * temp ** 2 - \
                2.416 * 10 ** (-4)
    elif temp <= 860:
        elong = 1.1 * 10 ** (-2)
    elif temp <= 1200:
        elong = 2 * 10 ** (-5) * temp - 6.2 * 10 ** (-3)
    else:
        raise Exception('Temperature should be lower than 1200 centigrades')
    return elong


def steel_sh(temp):
    # EN 1993-1-2: 3.4.1.2
    if temp < 20:
        raise Exception('Temperature should be higher than 20 centigrades')
    elif temp < 600:
        sh = 425 + 7.73 * 0.1 * temp - 1.69 * 10 ** (-3) * temp ** 2 + \
             2.22 * 10 ** (-6) * temp ** 3
    elif temp < 735:
        sh = 666 + 13002 / (738 - temp)
    elif temp < 900:
        sh = 545 + 17820 / (temp - 731)
    elif temp <= 1200:
        sh = 650 
    else:
        raise Exception('Temperature should be lower than 1200 centigrades')
    return sh


def steel_conductivity(temp):
    # EN 1993-1-2: 3.4.1.2
    if temp < 20:
        raise Exception('Temperature should be higher than 20 centigrades')
    elif temp < 800:
        conductivity = 54 - 3.33 * 10 ** (-2) * temp
    elif temp <= 1200:
        conductivity = 27.3 
    else:
        raise Exception('Temperature should be lower than 1200 centigrades')
    return conductivity


