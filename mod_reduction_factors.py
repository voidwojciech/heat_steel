import math


# interpolation data for EC3 constructional steel
temperatures = [20,100,200,300,400,500,600,700,800,900,1000,1100,1200]
kys = [1.0,1.0,1.0,1.0,1.0,0.78,0.47,0.23,0.11,0.06,0.04,0.02,0.001]
kps = [1.0,1.0,0.807,0.613,0.420,0.360,0.180,0.075,0.050,0.0375,0.0250,0.0125,0.001]
kEs = [1.0,1.0,0.9,0.8,0.7,0.6,0.31,0.13,0.09,0.0675,0.0450,0.0225,0.001]


def CS_class(d, t, fy):
    # tylko dla rur okraglych
    eps_cs_class = math.sqrt(235 / fy) * 0.85  #  * 0.85 fo fire (4.2, EN312)
    if d / t <= 50 * eps_cs_class ** 2:
        cs_class = 1
    elif d / t <= 70 * eps_cs_class ** 2:
        cs_class = 2
    elif d / t <= 90 * eps_cs_class ** 2:
        cs_class = 3
    else:
        cs_class = 4
    print ("d/t is %.1f, CS is %i" % ((d/t), cs_class))
    print ("for d/t > %.1f, CS is 3" % (70 * eps_cs_class ** 2))
    print ("for d/t > %.1f, CS is 4" % (90 * eps_cs_class ** 2))
    return cs_class






