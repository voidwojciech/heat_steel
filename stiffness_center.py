import math
from scipy.interpolate import interp1d
"""



2016/04/22: THIS CODE IS NO LONGER SUPPERTED
see stifness_center_func



"""

d = 168.3
r = d / 2
t = 6
E = 210 * 10 ** 3
A = math.pi / 1 * ((r ** 2 ) - ((r - t) ** 2))
I = math.pi / 4 * ((r ** 4 ) - ((r - t) ** 4))
rad_gyr = math.sqrt(I / A)

r_outside = d / 2
r_inside = d / 2 - t
r_inner = d / 2 - t / 2
division = 36
A_i = A / division

temperatures = [20,100,200,300,400,500,600,700,800,900,1000,1100,1200]
kEs = [1.0,1.0,0.9,0.8,0.7,0.6,0.31,0.13,0.09,0.0675,0.0450,0.0225,0.001]
kEs_interp = interp1d(temperatures, kEs)
#
interp_range = [-r_inner, r_inner]
interp_data = [500, 700]
temp_interp = interp1d(interp_range, interp_data)

I_sum = 0
EI_sum = 0
EI_matrix = []
for angle in range(0, 360, int(360/division)):
    angle_rad = angle / 360 * (2 * math.pi)
    y = r_inner * math.sin(angle_rad)
    I_i = A_i * y ** 2
    t_i = float(temp_interp(y))
    E_i = E * kEs_interp(t_i)
    EI_i = I_i * E_i
    #
    I_sum = I_sum + I_i
    EI_sum = EI_sum + EI_i
    print("%.1f, %.4f, %.2f, %.1f, %.1f" % (angle, angle_rad, y, I_i, t_i))
    EI_matrix.append([y, I_i, EI_i, t_i])

print("check (I_sum / I): %.4f" % (I / I_sum))
print("check (EI_sum / EI): %.4f" % (EI_sum / (E*I)))
print("\n\n")

def EI_ratio_func(EI_matrix):
    EI_corr_high_sum = 0
    EI_corr_low_sum = 0
    for item in EI_matrix:
        y = item[0]
        if y > 0:
            EI_corr_high_sum += item[2]
        elif y < 0:
            EI_corr_low_sum += item[2]
    EI_ratio = EI_corr_high_sum / EI_corr_low_sum
    return EI_ratio


def update_y(EI_matrix, y_shift):
    for item in EI_matrix:
        item[0] -= y_shift
        item[1] = A_i * item[0] ** 2
        E_i = E * kEs_interp(item[3])
        item[2] = E_i * item[1]
    return EI_matrix


EI_ratio = EI_ratio_func(EI_matrix)
print("EI_ratio:", EI_ratio)

y_shift = -0.1  # mm
y_shift_sum = 0
n = 0
while abs(EI_ratio) < 0.999:
    update_y(EI_matrix, y_shift)
    #print(EI_matrix[1])
    EI_ratio = EI_ratio_func(EI_matrix)
    print("y_shift_sum = %.1f mm, EI_ratio: %.4f" % (y_shift_sum, EI_ratio))
    y_shift_sum += y_shift
print("\ny_shift = %.1f mm, EI_ratio: %.4f" % (y_shift_sum-y_shift, EI_ratio))



















