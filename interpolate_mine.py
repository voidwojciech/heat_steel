"""
Interpolacja liniowa na podstawie krzywej wyrazonej przez zestaw punktow
#
dwie listy o rownych wymiarach
lista a: czas (s) oraz lista b: odpowiadajaca temperatura (degC)
#
jesli interpolate ma byc zawsze wywolywane z zewnatrz, to ordertest musi byc przeniesiony na zewnatrz (teraz jest w pierwszych liniach void_interpolate)
"""

def void_interpolate(point, a, b):
    if ordertest(a):
        raise Exception("ordertest not passed")
    else:
        print('ordertest: PASSED, "a" is in ascending order')

    n = 0
    for item in a[0:-1]:  # [0:-1], otherwise point = a[-1] will cause problem
        if item <= point:
            lower_bound = item
            try:
                upper_bound = a[n+1]
            except:
                raise Exception("UNABLE TO INTERPOLATE - point outside the scope of defined data")
            n += 1
        elif item > point:
            break
        else:
            break
    print('point is %.1f' % point)
    print('lower_bound = %.1f' % lower_bound)
    print('upper_bound = %.1f' % upper_bound)
    print(n)
    difference = point - lower_bound
    print("difference = %.1f" % difference)
    procent = difference / (upper_bound - lower_bound)
    print("procent = %.1f" % procent)
    lower_bound_value = b[n-1]
    upper_bound_value = b[n]
    print('lower_bound_value = %.1f' % lower_bound_value)
    print('upper_bound_value = %.1f' % upper_bound_value)
    point_value = lower_bound_value + procent * (upper_bound_value - lower_bound_value)
    print('point_value = %.1f' % point_value)
    return point_value


def ordertest(A):
    for i in range(len(A) - 1):
        if A[i] < A[i+1]:
            pass
        else:
            print("values in 'a' list are not in ascending order. Cannot interpolate")
            print("list a: check position %i with value %.1f" % (i, A[i]))
            return True


def ordertest(A, b):
    for i in range(len(A) - 1):
        if A[i] < A[i+1]:
            pass
        else:
            print("values in 'a' list are not in ascending order. Cannot interpolate")
            print("list a: check position %i with value %.1f" % (i, A[i]))
            return True
    # length test:
    if len(a) == len(b):
        print("lengthtest: PASSED, both lists have equal length")
    else:
        raise Exception("lengthtest not passed")

# TESTING:
# simplest test:
#a = [0, 10, 20, 30, 40]
#b = [0, 100, 400, 300, 400]
#point = 11
# trial:
#a = [0.0, 238.9, 316.0, 396.7, 499.4, 598.3, 697.0, 795.7, 850.9, 894.9, 946.1, 1044.8, 1099.5, 1146.8, 1194.1, 1245.1, 1333.2, 1439.7, 1494.7, 1590.4, 1697.0, 1800.1, 1892.2, 1965.7, 2090.7]
#b = [20.0, 20.0, 27.9, 53.1, 103.2, 169.2, 253.3, 348.7, 348.9, 362.6, 403.5, 505.8, 571.7, 653.4, 748.7, 814.6, 851.1, 860.4, 881.0, 863.0, 867.8, 838.6, 818.4, 811.7, 821.1]
#point = 11

#print(void_interpolate(point, a, b))

