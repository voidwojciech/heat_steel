# -*- coding: utf-8 -*-
"""
"""
import numpy as np
import math
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import mod_reduction_factors as mrf
from material_prop import steel_elongation
from stiffness_center_func import stiffness_center_f


fy = 235
E = 210 * 10 ** 3
L = 3000
l_cr = L * 1
load = 100
scaled_chart = 'n'  # 'y' or 'n' --- vertical axis scaled from 0 to 1
max_N_b_fi_t_Rd = 1  # for non-scaled chart

# rura okragla:
d = 168.3
r = d / 2
t = 6
A = math.pi / 1 * ((r ** 2 ) - ((r - t) ** 2))
I = math.pi / 4 * ((r ** 4 ) - ((r - t) ** 4))
rad_gyr = math.sqrt(I / A)
"""
# rura kwadratowa:
A = 1070
rad_gyr = 22.3
"""
##############################################################################
##############################################################################
##############################################################################
#
if mrf.CS_class(d, t, fy) == 4:
    raise Exception("Class 4 cross-section, critical temperature is 350 degC")

kys_interp = interp1d(mrf.temperatures, mrf.kys)
kps_interp = interp1d(mrf.temperatures, mrf.kps)
kEs_interp = interp1d(mrf.temperatures, mrf.kEs)

temp = 20
res_output = []
N_b_fi_t_Rd = 10 ** 12


def reduction_factors(temp):
    ky_theta = kys_interp(temp)
    kE_theta = kEs_interp(temp)
    return ky_theta, kE_theta


alpha = 0.65 * math.sqrt(235 / fy)
lambda_1 = math.pi * math.sqrt(E / fy)
nd_slend = l_cr / rad_gyr * 1 / lambda_1
def chi_fi_func(temp):
    ky_theta, kE_theta = reduction_factors(temp)
    nd_slend_theta = nd_slend * math.sqrt(ky_theta / kE_theta)
    # print(temp, ky_theta)
    phi_theta = 0.5 * (1 + alpha * nd_slend_theta + nd_slend_theta ** 2)
    chi_fi = 1 / (phi_theta + math.sqrt(phi_theta ** 2 - nd_slend_theta ** 2))
    return ky_theta, kE_theta, nd_slend_theta, phi_theta, chi_fi

chi_fis = []
nd_slend_thetas = []
phi_thetas = []
#for temp in range(20, 20+1, 1):
while N_b_fi_t_Rd > load:
    temp_step = 1
    ky_theta, kE_theta, nd_slend_theta, phi_theta, chi_fi = chi_fi_func(temp)
    #
    nd_slend_thetas.append(nd_slend_theta)
    phi_thetas.append(phi_theta)
    chi_fis.append(chi_fi)
    N_pl_Rd_basic = A * fy / 1000
    N_fi_theta_Rd_tension = A * fy * ky_theta / 1000
    N_b_fi_t_Rd = A * fy * ky_theta * chi_fi / 1000
    if temp == 20 or temp % 100 == 0:
        print("temp = %i, N_b_fi_t_Rd = %i" % (temp, N_b_fi_t_Rd))
    res_output.append([temp, N_b_fi_t_Rd])
    if temp == 100 and scaled_chart == 'y':
        # store maxiumum LBC for scaled chart
        max_N_b_fi_t_Rd = N_b_fi_t_Rd
    temp = temp + temp_step

print("\nUltimate Temperature: ", (temp - temp_step))
# full data is stored in res_output
print("N_pl_Rd_basic = %i" % N_pl_Rd_basic)
print("N_fi_theta_Rd_tension = %i" % N_fi_theta_Rd_tension)
print("N_b_fi_t_Rd = %.1f\n" % N_b_fi_t_Rd)

# CHART
res_output_np = np.array(res_output)
x = res_output_np[:,0]
y = res_output_np[:,1] / max_N_b_fi_t_Rd
plt.plot(x, y, color='green', linestyle='dashed')


plt.plot(x+30, y, color='red', linestyle='dashed')
wyniki_100 = np.array([[768, 50],
                       [670, 100],
                       [577, 200],
                       [612, 220],
                       [598, 240],
                       [589, 260],
                       [658, 280],
                       [596, 300]])
x100 = wyniki_100[:,0]
x100a = []
for item in x100:
    chi_fi_diff = chi_fi_func(item)[4]
    x100a.append(chi_fi_diff)

"""
v_chi_fi_func = np.vectorize(chi_fi_func)
x100_chi = v_chi_fi_func"""


plt.plot((0, 600), (600 / max_N_b_fi_t_Rd, 600 / max_N_b_fi_t_Rd), 'k-')
plt.show()



##############################################################################
# 2016/04/22
# ponizej czesc do obliczen compression + bending:
##############################################################################
if mrf.CS_class(d, t, fy) >= 3:
    raise Exception("Class 3 or 4 cross-section. W_el is not implemented") 

print("\n\nMembers with Class 1, 2, subject to combined"
      "bending and axial compression:\n")
scheme = 'pinned_pinned'  # 'pinned_pinned' or cantilever'
t_mean = 650
delta_t = 300
# load = load * 1000
def max_displacement(L, d, t_mean, delta_t, scheme):
    if scheme =='pinned_pinned':
        denominator = 8
    elif scheme =='cantilever':
        denominator = 2
    th_elong_cold = steel_elongation(t_mean - delta_t / 2)
    th_elong_hot = steel_elongation(t_mean + delta_t / 2)
    max_displ = (th_elong_hot - th_elong_cold) * L ** 2 / (d * denominator)
    return max_displ


lista = np.array([[2400, 100, 50], [2400, 100, 75], [2400, 100, 100],
                  [2400, 100, 125], [2400, 100, 150], [2400, 100, 175],
                  [2400, 100, 200], [2400, 100, 225], [2400, 100, 250],
                  [2400, 100, 275],
                  [2700, 100, 50], [2700, 100, 75], [2700, 100, 100],
                  [2700, 100, 125], [2700, 100, 150], [2700, 100, 175],
                  [2700, 100, 200], [2700, 100, 225], [2700, 100, 250],
                  [2700, 100, 275],
                  [3000, 100, 50], [3000, 100, 75], [3000, 100, 100],
                  [3000, 100, 125], [3000, 100, 150], [3000, 100, 175],
                  [3000, 100, 200], [3000, 100, 225], [3000, 100, 250],
                  [3000, 100, 275],
                  [3300, 100, 50], [3300, 100, 75], [3300, 100, 100],
                  [3300, 100, 125], [3300, 100, 150], [3300, 100, 175],
                  [3300, 100, 200], [3300, 100, 225], [3300, 100, 250],
                  [3300, 100, 275],
                  [3600, 100, 50], [3600, 100, 75], [3600, 100, 100],
                  [3600, 100, 125], [3600, 100, 150], [3600, 100, 175],
                  [3600, 100, 200], [3600, 100, 225], [3600, 100, 250],
                  [3600, 100, 275],
                  [3900, 100, 50], [3900, 100, 75], [3900, 100, 100],
                  [3900, 100, 125], [3900, 100, 150], [3900, 100, 175],
                  [3900, 100, 200], [3900, 100, 225], [3900, 100, 250],
                  [3900, 100, 275],
                  [4200, 100, 50], [4200, 100, 75], [4200, 100, 100],
                  [4200, 100, 125], [4200, 100, 150], [4200, 100, 175],
                  [4200, 100, 200], [4200, 100, 225], [4200, 100, 250],
                  [4200, 100, 275],
                  [6000, 100, 50], [6000, 100, 75], [6000, 100, 100],
                  [6000, 100, 125], [6000, 100, 150], [6000, 100, 175],
                  [6000, 100, 200], [6000, 100, 225], [6000, 100, 250],
                  [6000, 100, 275]
                  ])
# krotsza wersja do testow
"""
lista = np.array([[2400, 100, 50], [2400, 100, 75], [2400, 100, 100],
                  [2400, 100, 125], [2400, 100, 150], [2400, 100, 175],
                  [2400, 100, 200], [2400, 100, 225], [2400, 100, 250],
                  [2400, 100, 275]
                  ])
# najkrotsza wersja do testow
lista = np.array([[2400, 100, 50], [2400, 100, 75]])
"""
##############################################################################
results_matrix = []
zz = 1
for item in lista:
    print("item %i/%i" % (zz, len(lista)))
    L = item[0]
    delta_t = item[1]
    load = item[2]
    t_mean = 170
    temp_step = 1
    cond_1 = 0
    snap = 0
    no_snap = 0
    while cond_1 <= 1:
        max_displ = max_displacement(L, d, t_mean, delta_t, scheme)
        #print("L = %.1f, d = %.1f, t_mean = %.1f, delta_t =  %.1f, scheme: %s"
        #      % (L, d, t_mean, delta_t, scheme))
        #print("max_displ = %.1f mm" % max_displ)
        
        BETA_M = 1.3
        ky_theta, kE_theta, nd_slend_theta, phi_theta, chi_fi = chi_fi_func(t_mean)
        ni_LT = 0.15 * nd_slend_theta * BETA_M - 0.15
        ni_z = (1.2 * 0 - 3) * nd_slend_theta + 0.71 * 0 - 0.29
        ni_y = (2 * BETA_M - 5) * nd_slend_theta + 0.44 * BETA_M + 0.29
        # print(ni_LT, ni_z, ni_y)
        if ni_LT > 0.9 or ni_z > 0.8 or ni_y > 0.8:
            raise Exception("ni_LT, ni_z, ni_y are higher than reccomended")
        
        
        chi_LT_fi = 1  # NO LTB!!
        chi_y_fi = chi_fi
        chi_z_fi = chi_fi
        chi_min_fi = min(chi_y_fi, chi_z_fi)
        M_y = load * 1000 * max_displ
        M_z = 0
        k_LT = 1
        k_y_bc = 1 - (ni_y * load * 1000) / (chi_y_fi * A * ky_theta * fy)
        k_z_bc = 1 - (ni_z * load * 1000) / (chi_z_fi * A * ky_theta * fy)
        #print("k_y_bc: %.3f" % k_y_bc)
        #print("k_z_bc: %.3f" % k_z_bc)
        
        # Plastic section modulus: Wpl
        # only for c-s 1 and 2 !!!
        W_pl_1 = (math.pi * r ** 2 / 2) * ( 4 * r / (3 * math.pi))
        W_pl_2 = (math.pi * (r-t) ** 2 / 2) * ( 4 * (r-t) / (3 * math.pi))
        W_pl = (W_pl_1 - W_pl_2) * 2
        
        cond_1 = load * 1000 / (chi_min_fi * A * ky_theta * fy) + \
                 k_y_bc * M_y / (W_pl * ky_theta * fy) + \
                 k_z_bc * M_z / (W_pl * ky_theta * fy)
        #cond_2 = load * 1000 / (chi_z_fi * A * ky_theta * fy) + \
        #         k_LT * M_y / (chi_LT_fi * W_pl * ky_theta * fy) + \
        #         k_z_bc * M_z / (W_pl * ky_theta * fy)
        #print("Condition 1: %.3f" % cond_1)
        #######################################################################
        # 2016/04/22
        # stiffness center:
        #######################################################################
        t_cold = t_mean - delta_t / 2
        t_hot = t_mean + delta_t / 2
        EI_shift = stiffness_center_f(d, r, t, E, t_mean, t_cold, t_hot)
        
        if max_displ < abs(EI_shift):
            snap += 1
        else:
            no_snap +=1
        #######################################################################        
        # /stiffness center:
        #######################################################################
        t_mean = t_mean + temp_step
    zz += 1
    results_matrix.append([L, delta_t, load, t_mean, cond_1, snap, no_snap])

print(results_matrix)
print(len(results_matrix))
#### ggg variable




