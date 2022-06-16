import csv

memberDict = {}

def Manage_members():
    memberDict = readMemberCSV()
    print('Menu:')
    print('a. Add a new member')
    print('b. Remove member')
    print('c. Upgrade/Downgarde membership')
    print('d. Modify member data')
    print('e. Import members (csv or txt)')
    print('f. Search a member')
    print('g. Bulk operation')
    print('h. Help')
    userInput = input('Please choose an option: ')
    
    if userInput == 'a':
        addNewMember(memberDict)
    elif userInput == 'b':
        return
    elif userInput == 'c':
        return
    elif userInput == 'd':
        return
    elif userInput == 'e':
        return
    elif userInput == 'f':
        return
    elif userInput == 'g':
        return
    elif userInput == 'h':
        return
    else:
        print("\n\n\n\n\n" + userInput + " is an invalid input")
        Manage_members()
     
# %% Add New Member functions
def addNewMember(tempDict):
    print("\n\n\n\n\nAdding new member:")
    inputFirstName = input("Enter first name: ")
    inputLastName = input("Enter last name: ")
    inputDateOfBirth = input("Enter Date of Birth (Example: June 15 1996): ")
    inputAddress = input("Enter address: ")
    inputStatus = input("What member status do you want? (Basic, Silver, Gold, Platinum)")

def readMemberCSV():
    tempDict = {}
    with open('memberdata.csv', mode='r') as inFile:
        keyReader = csv.reader(inFile)
        key = []
        key = next(keyReader)
        for i in range(0, len(key)):
            tempDict[key[i]] = []
        inFile.close()
        
    with open('memberdata.csv', mode='r') as inFile:    
        recordReader = csv.DictReader(inFile)
        for record in recordReader:
            for k in tempDict:
                tempDict[k].append(record[k])
    
    return tempDict

#Manage_members()
readMemberCSV()