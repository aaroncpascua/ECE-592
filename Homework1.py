import math

def pyramid(s):
    """Takes a user input and creates a pyramid pattern of the letters
    in the string"""
    
    strList = []
    for i in range(1,len(s)+1):
        strList.append(s[:i])
    print("\n".join(strList))
    
def findSquares(s = 0, e = 0):
    """Find and print a list of numbers which are exact squares of an 
    integer between two user inputted integer values"""
    
    #Find the lowest number of the two integers
    if s < e:
        lowNum = s
        highNum = e
    elif s == 0:
        lowNum = 0
        highNum = e
    elif e == 0:
        lowNum = 0
        highNum = s
    else:
        lowNum = e
        highNum = s
    
    #Loop through the numbers, find perfect squares, and store into list
    perfRoots = []
    for x in range(lowNum, highNum):
        root = math.sqrt(x)
        if int(root + 0.5) ** 2 == x:
            #print(x)
            perfRoots.append(x)
    print(perfRoots)
    
def calSalary(h:float, r = 20):
    """Calculate salary given number of hours and hourly rate. Calculates
    overtime rate if hours are greater than 40."""
    
    if h < 0:
        print("Not valid hours")
        return -1
    elif h > 40:
        rate = r + (r * 0.2)
        hours = (h - 40)
        salary = (40 * r) + (hours * rate)
    else:
        salary = h * r
    return salary