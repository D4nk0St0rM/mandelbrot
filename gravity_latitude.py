from math import *

latitude = float(input("What is the latitude in degrees?"))
latitude = latitude * pi / 180	# latitude in radians
acc = 9.78 * (1 + (0.0053*(sin(latitude))**2))
print "Acc. due to gravity:", acc, "metres/(sec squared)"

mylist = []
totmass = 0	
while True:
    answer = raw_input("Mass of item in kg?")
    if answer == "stop":
        break
    else:
        mylist.append(float(answer))
        mass = float(answer)
        totmass = totmass + mass
print "The items in your basket are: ", mylist
print "Total mass:", totmass, "kilograms", answer 
weight = totmass * acc
print "Total weight:", weight, "newtons"
