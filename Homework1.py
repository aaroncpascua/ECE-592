import math

def pyramid(s):
    """Takes a user input and creates a pyramid pattern of the letters
    in the string."""
    
    strList = []
    for i in range(1,len(s)+1):
        strList.append(s[:i])
    print("\n".join(strList))
    
def findSquares(s = 0.0, e = 0.0):
    """Find and print a list of numbers which are exact squares of an 
    integer between two user inputted integer values."""
    
    #Find the lowest number of the two integers
    if s < e:
        lowNum = int(s)
        highNum = int(e)
    elif s == 0:
        lowNum = 0
        highNum = int(e)
    elif e == 0:
        lowNum = 0
        highNum = int(s)
    else:
        lowNum = int(e)
        highNum = int(s)
    
    #Loop through the numbers, find perfect squares, and store into list
    perfRoots = []
    for x in range(lowNum, highNum + 1):
        root = math.sqrt(x)
        if int(root + 0.5) ** 2 == x:
            #print(x)
            perfRoots.append(x)
    return perfRoots
    
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

def calLetterGrade(points:float, gradescale = [98, 94, 91, 88, 85, 82, 79, 76, 73, 70, 67, 64]):
    """Calculates letter grade based on the points and the grade scale."""
    
    gradeDict = {
                0: 'A+',
                1: 'A',
                2: 'A-',
                3: 'B+',
                4: 'B',
                5: 'B-',
                6: 'C+',
                7: 'C',
                8: 'C-',
                9: 'D+',
                10: 'D',
                11: 'D-',
                12: 'F'
                }
    
    #Check for invalid points input
    if not str(int(points)).isnumeric():
        print("Points is not numeric")
        return -1
    
    #Check for duplicates
    for x in gradescale:
        if gradescale.count(x) > 1:
            print("Duplicate in grade scale")
            return -1
    
    #Check for invalid list input, else print letter grade
    counter = 0
    for x in gradescale:
        if not str(x).isnumeric():
            print("List member is not numeric")
            return -1
        elif len(gradescale) > 12:
            print("grade scale is larger than 12")
            return -1
        else:
            if points >= x:
                if len(gradescale) < 12:
                    if counter < len(gradescale):
                        return gradeDict[counter]
                    else:
                        return 'F'
                else:
                    return gradeDict[counter]
                counter += 1
            else:
                if counter == len(gradescale) - 1:
                    return 'F'
                else:
                    counter += 1