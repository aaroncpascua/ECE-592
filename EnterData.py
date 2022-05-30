from Homework2 import *

def EnterData():
    """
    Takes in user input for their name, height in lbs and weight in feet.
    Data is stored in your current directory called dataRecords.csv"""
    
    #Variables
    userName = input("Enter your name: ")
    userWeight = input("Enter your weight in pounds (lbs): ")
    userHeight = input("Enter your height in feet (ft): ")
    
    #Check to see if input is numerical
    if '.' in userWeight: 
        try:
            float(userWeight)
        except ValueError:
            return -1
    if '.' in userHeight:
        try:
            float(userHeight)
        except ValueError:
            return -1
    if float(userWeight) == 0 or float(userHeight) == 0:
        print ("Invalid weight or height\npoo")
        EnterData()
    if float(userWeight) < 0 or float(userHeight) < 0:
        print ("Invalid weight or height\n")
        EnterData()
    else:
        dict = {
            "Name": str,
            "Weight": float,
            "Height": float
            }
        dict["Name"] = userName
        dict["Weight"] = userWeight
        dict["Height"] = userHeight

    dataRecorder('dataRecords.csv', dict)