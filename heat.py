"""
http://fire-research.group.shef.ac.uk/steelinfire/discussion.html
Brian Kirby
So that you know the emissivity for steel in EC1 was a fix. I argued
relentlessly at the time it should be 0.8 based on a whole load of data,
but was overruled. Ulf Wickstrom and I continue to argue on this.
"""


def HF_conv(temp_g, temp_m):
    alpha_c = 25
    h_net_c = alpha_c * (temp_g - temp_m)
    #print("h_net_c:", h_net_c)
    return h_net_c


def HF_rad(temp_r, temp_m):
    conf_factor = 1.0
    em_steel = 0.8
    em_fire = 1.0
    stefan = 5.67 * 10 ** (-8)
    pierdy = conf_factor * em_steel * em_fire * stefan
    #print("HF_rad: temp_r = %.f, temp_m = %.f" % (temp_r, temp_m))
    h_net_r = pierdy * ((temp_r + 273) ** 4 - (temp_m + 273) ** 4)
    #print("h_net_r:", h_net_r)
    return h_net_r

