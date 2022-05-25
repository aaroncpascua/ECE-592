from Homework2 import *

def getUserInput():
    """Takes in user input for their name, height in lbs and weight in feet"""
    
    #Variables
    userName = input("Enter your name: ")
    userWeight = input("Enter your weight in pounds (lbs): ")
    userHeight = input("Enter your height in feet (ft): ")
    
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
        print ("Invalid weight or height")
        getUserInput()
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