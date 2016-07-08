"""
creates dictionary based on csv-like text file
#
# data used for testing ('database_creator_test_fooder.txt'):
Algeria,73.131000,6406.8166213983,0.1
Angola,51.093000,5519.1831786593,2
Argentina,75.901000,15741.0457726686,0.5
Armenia,74.241000,4748.9285847709,0.1
"""
import numpy as np


profile_name = np.genfromtxt('database_AM_v2015_03.txt', usecols=(0), delimiter=',', comments="#", dtype=None)
profile_data = np.genfromtxt('database_AM_v2015_03.txt', usecols=(1,2,3,4,5,6), delimiter=',', comments="#", dtype=None)

dict_list = zip(profile_name, profile_data)
my_dict = dict(dict_list)
print(my_dict)
print(my_dict[b'HE 300 A'][0])


"""
profile_name = np.genfromtxt('database_creator_test_fooder.txt', usecols=(0), delimiter=',', comments="#", dtype=None)
profile_data = np.genfromtxt('database_creator_test_fooder.txt', usecols=(1,2,3), delimiter=',', comments="#", dtype=None)

dict_list = zip(profile_name, profile_data)
my_dict = dict(dict_list)
"""


"""
# testing and understanding:
# loadtext and genfromtxt
#
# loadtxt
print("\n\nloadtxt:")
data=np.loadtxt('database_creator_test_fooder.txt', delimiter=',',dtype=[('f0','|S15'),('f1',float),('f2',float),('f3',float)])
# nie wiem dlaczego str nie dziala jako dtype. '|S15' dziala
x, y = np.loadtxt('database_creator_test_fooder.txt', delimiter=',', usecols=(1, 2), unpack=True)
z = np.loadtxt('database_creator_test_fooder.txt', delimiter=',', usecols=(1, 2), unpack=True)
print("data: \n", data)
print("x: ", x)
print("y: ", y)
print("z: ", z)
#
# genfromtxt
print("\n\ngenfromtxt:")
col1, col2 = np.genfromtxt('database_creator_test_fooder.txt', delimiter=',', usecols=(1, 2), dtype=None, unpack=True)
columns = np.genfromtxt('database_creator_test_fooder.txt', usecols=(0,1,2,3), delimiter=',', dtype=None)
columns2 = np.genfromtxt('database_creator_test_fooder.txt', delimiter=',', dtype=None)
print("data: \n", data)
print("col1: ", col1)
print("col2: ", col2)
print("columns: ", columns)
print("columns2: ", columns2)
# /test
"""
