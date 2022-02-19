#program to calculate kinetic engery of an object for mass provided by the end user for variable speeds
#-------------------------------------------------- 
#| 1 - Set mass initial value to 0 [initialisation] [not needed as 1 only input]
#| 2 - use raw_input to take user input as variable
#| 3 - use this and calculate against each speed
#| 4 - output
#| 5 - set velocity square values to use in calculation E_k = 1/2 x m x v^2
#| Notes: Set check for zero
#---------------------------------------------------

v1 = 1.0
v2 = 4.0
v3 = 9.0
v4 = 16.0
mass = float(raw_input("Please enter the mass in kg of the object: "))
while (mass == 0):
  mass = float(raw_input("Please enter the mass in kg of the object (greater than 0): "))
else:
    Ek1 = (0.5 * mass * v1)
    Ek2 = (0.5 * mass * v2)
    Ek3 = (0.5 * mass * v3)
    Ek4 = (0.5 * mass * v4)
    print "The object of mass " ,mass,"kg, has Kinetitc Energy at the following speeds: "
    print "1.0 m s^-1 =", Ek1,"kg m^2 s^-2"
    print "2.0 m s^-1 =", Ek2,"kg m^2 s^-2"
    print "3.0 m s^-1 =", Ek3,"kg m^2 s^-2"
    print "4.0 m s^-1 =", Ek4,"kg m^2 s^-2"
    print "Kg m^2 s^-2 is also the SI unit Joule or 'J'"

    
    
    
      
      
      






