import math

def calBMI():
    """
    Take the user input for weight in lbs, Height in feet
    Print weight in Kgs, print height in meters
    Calculate Body mass Index = Weight(Kg) / (height (m))^2
    Print BMI  (5 pts)
    Output should look like  (5 pts)
    Weight = ____ lbs =  ____ Kg, 
    Height = ____ feet = ____ m, 
    BMI = ____"""
    pass

def getUserInput():
    #Variables
    userWeight = input("Enter your weight in pounds (lbs): ")
    userHeight = input("Enter your height in feet (ft): ")
    calcBMI(userWeight, userHeight)

def calcBMI(userWeight, userHeight):
    #Check to see if input is numerical
    if not str(userWeight).isnumeric() or not str(userHeight).isnumeric():
        print("Invalid entry")
        return -1
    if int(userWeight) == 0 or int(userHeight) == 0:
        print ("Invalid weight or height")
        getUserInput()
    else:
        #Convert user inputs to floats
        weightFloat = float(userWeight)
        heightFloat = float(userHeight)
        
        #Imperial to metric conversions
        lbs2kg = weightFloat * 0.453592
        ft2m = heightFloat * 0.3048
        
        #Calculate BMI
        BMI = lbs2kg / (math.pow(ft2m,2))
        
        #Print weight, height, and BMI
        print('Weight = {0} lbs = {1} Kg,'.format(format(weightFloat,".3f"), format(lbs2kg,".3f")))
        print('Height = {0} feet = {1} m,'.format(format(heightFloat,".3f"), format(ft2m,".3f"))) 
        print('BMI = {0}'.format(format(BMI,".3f")))
        
getUserInput()