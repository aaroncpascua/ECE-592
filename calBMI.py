#Take the user input for weight in lbs, Height in feet
#Print weight in Kgs, print height in meters
#Calculate Body mass Index = Weight(Kg) / (height (m))^2
#Print BMI  (5 pts)
#Output should look like  (5 pts)
#Weight = ____ lbs =  ____ Kg, 
#Height = ____ feet = ____ m, 
#BMI = ____

import math

#Variables
userWeight = float(input("Enter your weight in pounds (lbs): "))
userHeight = float(input("Enter your height in feet (ft): "))

#Imperial to metric conversions
lbs2kg = userWeight * 0.453592
ft2m = userHeight * 0.3048

#Calculate BMI
BMI = lbs2kg / (math.pow(ft2m,2))

#Print weight, height, and BMI
print('Weight = {0} lbs = {1} Kg,'.format(userWeight, lbs2kg))
print('Height = {0} feet = {1} m,'.format(userHeight, ft2m)) 
print('BMI = {0}'.format(BMI))