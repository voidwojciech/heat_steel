"""
Obliczanie temperatury elmentów stalowych zgodnie z PN EN 1993-1-2
UWAGA: emisyjność stali ustawiono jako 0.8 (wartość 0.7 jest mocno krytykowana)
       można ją zmienić przechodząc do heat.py i zmieniając
       "em_steel = 0.8" na "em_steel = 0.7"

Projekt w fazie realizacji
Można dodawać nowe profile w "database_profiles.py": składnia: 'NAZWA (np. HEB200)': [Am/V, Am/V(box)]
lub recznie wpisac wartosci w liniach AmV oraz AmVb
Nazwy profili w bazie zgodne z Arcelor Mittal
http://sections.arcelormittal.com/products-services/products-ranges.html
np. z serii IPE 180:
IPE AA 180, IPE A 180, IPE 180, IPE O 180
z serii HE 200:
HE 200 AA, HE 200 A, HE 200 B, HE 200 C, HE 200 M

DEVELOPER NOTES:
+ typy ekspozycji wbudowane w funkcję gas_temp(ekspozycja, time)
    'ISO-834'
    'LP' - do testowania krzywych wyznaczonych przez zestaw punktów. Lista a: czas (sec), Lista b: temperatura gazów (wymiary a i b musza być równe)
    'ISO-834-1800-dacay-1800' - 1800 s acc. to ISO-834, followed by 1800 s with linear decay down to 20 degC
+ sprawdzenie poprawności list a i b jest wywoływane wielokrotnie - całkowicie niepotrzebnie

"""
# Ustawiane przez użytkownika:
profile_type = 'dwuteownik'  # 'dwuteownik' lub 'rura'
profile_name = 'HE 200 B'  # wypelnic jesli dwuteownik / patrz opis wyzej
profile_name = 'HEB200-3'  # na  SARBINOWO ('HEB200-' + '4', '3' lub '1')
grubosc_scianki_rury = 6.0  # wypelnic jesli rura
czas_analizy = 900  # czas analizy w sekundach
ekspozycja = 'ISO-834'
# mozliwe ekspozycje: 'ISO-834', 'LP', 'ISO-834-1800-dacay-1800'

#####################################
# Koniec ustawień użytkownika
# Poniżej nie trzeba niczego zmieniać
#####################################
from math import log10
import numpy as np
import database_profiles as dp
import material_prop as mp
import interpolate_mine as interp
import heat


if profile_type == 'dwuteownik':
    AmV = dp.data_miner(profile_name)[3]
    AmVb = dp.data_miner(profile_name)[5]
    #
    """#    
    #       
    ### NOT ROBUST!!!!
    #
    #"""
    if profile_name == 'HEB200-1':
        k_sh = AmVb / AmV
    else:
        k_sh = 0.9 * AmVb / AmV
    """### NOT ROBUST!!!!
    #
    #
    #
    #"""
    #
    print("Selected profile: %s" % profile_name)
    print("Its Am/V ratio is: %.1f" % AmV)
    print("Its Am/V (box) ratio is: %.1f" % AmVb)
    print("Data taken from Arcelor Mittal\n")
elif profile_type == 'rura':
    AmV = 1.0 / (grubosc_scianki_rury / 1000.)
    k_sh = 1.0
    print("Selected profile: tube with diameter = %.1f" % grubosc_scianki_rury)


#(2) W przypadku przekrojów dwuteowych narażonych na oddziaływania pożaru
# nominalnego, współczynnik poprawkowy związany z efektem zacienienia może być
# wyznaczony według wzoru:

temp_steel = 20
dtime = 5

def print_output():
    print("time: %.1f sec" % time)
    print("gas temp: %.1f deg C" % temp)
    print("Element temperature: %.1f deg C" % temp_steel)
    print("\n")

def gas_temp(ekspozycja, time):
    if ekspozycja == 'ISO-834':
        temp = 20 + 345 * log10(8 * (time / 60.0) + 1)
    elif ekspozycja == 'LP':
        a = [0.0, 238.9, 316.0, 396.7, 499.4, 598.3, 697.0, 795.7, 850.9, 894.9, 946.1, 1044.8, 1099.5, 1146.8, 1194.1, 1245.1, 1333.2, 1439.7, 1494.7, 1590.4, 1697.0, 1800.1, 1892.2, 1965.7, 2090.7]
        b = [20.0, 20.0, 27.9, 53.1, 103.2, 169.2, 253.3, 348.7, 348.9, 362.6, 403.5, 505.8, 571.7, 653.4, 748.7, 814.6, 851.1, 860.4, 881.0, 863.0, 867.8, 838.6, 818.4, 811.7, 821.1]
        print(time)        
        temp = interp.void_interpolate(time, a, b)
    elif ekspozycja == 'ISO-834-1800-dacay-1800':
        decay_start = 1800
        decay_end = decay_start + 1800
        max_temp = 20 + 345 * log10(8 * (decay_start / 60.0) + 1)
        if time <= 1800:
            temp = 20 + 345 * log10(8 * (time / 60.0) + 1)
        else:
            # temp = 20  # testing
            if time < decay_end:
                procent = (time - decay_start) / (decay_end - decay_start)
                temp = max_temp - procent * (max_temp - 20)
            else:
                temp = 20
    return temp

time_list = []
steelTemp_list = []
time_steelTemp_list = []

for time in range(0, czas_analizy + 1, dtime):
    temp = gas_temp(ekspozycja, time)
    h_net = heat.HF_conv(temp, temp_steel) + heat.HF_rad(temp, temp_steel)
    dtemp = k_sh * (AmV / (mp.steel_sh(temp_steel) * 7850)) * h_net * dtime
    temp_steel += dtemp
    if time <= 300:
        print_output()
    elif time > czas_analizy * 0.9 and time > czas_analizy - 100:
        print_output()
    elif time % 60 == 0:
        print(".")
    else: pass
    time_list.append(time)
    steelTemp_list.append(temp_steel)
    time_steelTemp_list.append([time, temp_steel])


np.savetxt('LP_time_list.txt', time_list, fmt='%.1f')
np.savetxt('LP_steelTemp_list.txt', steelTemp_list, fmt='%.1f')
"""
print(time_list)
print(steelTemp_list)
print(time_steelTemp_list)
np.savetxt('LP_time_list.txt', time_list, fmt='%.1f')
np.savetxt('LP_steelTemp_list.txt', steelTemp_list, fmt='%.1f')
"""

if profile_type == 'dwuteownik':
    print("\nTemperatura przekroju %s po %.1f sekundach (%.1f minuty) wyniesie %.1f stopni Celsjusza" % (profile_name, czas_analizy, czas_analizy / 60, temp_steel))
elif profile_type == 'rura':
    print("\nTemperatura przekroju rury o grubosci %.1f mm po %.1f sekundach (%.1f minuty) wyniesie %.1f stopni Celsjusza" % (grubosc_scianki_rury, czas_analizy, czas_analizy / 60, temp_steel))
print("Prawdopodobnie wkrotce dodam wykres temperatura-czas")
print("Inne funkcje na życzenie")
