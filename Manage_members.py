import csv
import os
import datetime
from pynput import keyboard #install
import time
import re
import random
from gen_member_data import findDuplicate

memberDict = {}
status = ['Basic', 'Silver', 'Gold', 'Platinum', 'None']
break_program = False
regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
statusUpdated = ""

def Manage_members(): # Add status updated print
    os.system('clear')
    memberDict = readMemberCSV()
    
    print(statusUpdated + "\n")
    
    print('Menu:')
    print('a. Add a new member')
    print('b. Remove member')
    print('c. Upgrade/Downgarde membership')
    print('d. Modify member data')
    print('e. Import members (csv or txt)')
    print('f. Search a member')
    print('g. Bulk operation')
    print('h. Help')
    userInput = input('Please choose an option (a-h): ').lower()
    
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
        Manage_members()
 
# %% Add New Member functions
def addNewMember(tempDict):
    os.system('clear')
    addNewMemberStr = "Adding new member:\n"
    print(addNewMemberStr)
    
    #Enter first name
    inputFirstNameBool = False    
    while not inputFirstNameBool:
        os.system('clear')
        print(addNewMemberStr)
        print('Required: First name format can only contain letters and special characters\n')
        inputFirstName = input("Enter first name: ")
        if any(chr.isdigit() for chr in inputFirstName):
            inputFirstNameBool = False
        else:
            inputFirstNameBool = True
            addNewMemberStr += "First name: " + inputFirstName + "\n"
    
    #Enter middle initial
    inputMidInitialBool = False
    while not inputMidInitialBool:      
        try:
            os.system('clear')
            print(addNewMemberStr)
            print("Optional: Middle initial format can only contain a letter\n")
            inputMidInitial = input("Enter middle initial name: ").upper()
            if inputMidInitial.isspace() or inputMidInitial == '':
                inputMidInitialBool = True
                inputMidInitial = ''
                addNewMemberStr += "Middle Initial: " + inputMidInitial + "\n"
            if len(inputMidInitial) > 1 or not inputMidInitial.isalnum() or any(chr.isdigit() for chr in inputMidInitial):
                continue
            else:
                inputMidInitialBool = True
                addNewMemberStr += "Middle Initial: " + inputMidInitial + "\n"
        except ValueError:
            continue
    
    #Enter last name
    inputLastNameBool = False
    while not inputLastNameBool:
        os.system('clear') 
        print(addNewMemberStr)
        print('Required: Last name format can only contain letters and special characters\n')
        inputLastName = input("Enter last name: ")
        if any(chr.isdigit() for chr in inputLastName):
            continue
        else:
            inputLastNameBool = True
            addNewMemberStr += "Last name: " + inputLastName + "\n"
    
    #Enter date of birth
    inputDoBBool = False
    while not inputDoBBool:
        os.system('clear')
        print(addNewMemberStr)
        print("Required: Date of Birth must be in the format like June 15 1996\n")
        inputDateOfBirth = input("Enter Date of Birth: ")
        try:
            datetime.datetime.strptime(inputDateOfBirth, '%B %d %Y')
            inputDoBBool = True
            addNewMemberStr += "Date of Birth: " + inputDateOfBirth + "\n"
        except ValueError:
            continue
        
    if (findDuplicate(memberDict['Fn'], inputFirstName) and findDuplicate(memberDict['Ln'], inputLastName) and findDuplicate(memberDict['DoB'], inputDateOfBirth)):
        statusUpdated = "Membership exists for " + inputFirstName + " " + inputLastName
        return
        
    #Enter address
    os.system('clear')
    print(addNewMemberStr)
    print("Optional: This can literally be anything\n")
    inputAddress = input("Enter address: ")
    addNewMemberStr += "Address: " + inputAddress + "\n"
    
    #Enter status
    os.system('clear')
    print(addNewMemberStr)
    inputStatusBool = False
    while not inputStatusBool:
        os.system('clear')
        print(addNewMemberStr)
        print("Required: Enter Basic, Silver, Gold, or Platinum\n")
        inputStatus = input("Enter member status: ")
        if not inputStatus in status:
            continue
        else:
            inputStatusBool = True
            addNewMemberStr += "Status: " + inputStatus + "\n"
            
    #Enter Member Start Date ---- Need to make sure user is at least 18
    os.system('clear')
    inputMemStartDateBool = False
    while not inputMemStartDateBool:
        print(addNewMemberStr)
        print("Required: Membership start date must be in the format like June 15 1996.") 
        print("If blank, membership start date will be today's date.")
        print("Date must be a valid date after December 31 1980.")
        print("You must be at least 18 years old.\n")
        inputMemStartDate = input("Enter membership start date (Example: June 15 1996): ")
        try:
            if inputMemStartDate.isspace() or inputMemStartDate == '':
                inputMemStartDateBool = True
                inputMemStartDate = datetime.date.today().strftime('%B %d %Y')
                addNewMemberStr += "Membership Start Date: " + inputMemStartDate + "\n"
            else:
                datetime.datetime.strptime(inputMemStartDate, '%B %d %Y')
                inputMemStartDateBool = True
                addNewMemberStr += "Membership Start Date: " + inputMemStartDate + "\n"
        except ValueError:
            continue
        
    #Enter Member Renewal Date
    os.system('clear')
    print(addNewMemberStr)
    inputMemRenewDateBool = False
    while not inputMemRenewDateBool:
        os.system('clear')
        print(addNewMemberStr)
        print("Required: Membership renewal date must be in the format like June 15 1996.")
        print("If blank, membership start date will be 1 year from membership start date\n")
        inputMemRenewDate = input("Enter membership renewal date: ")
        try:
            if inputMemRenewDate.isspace() or inputMemRenewDate == '':
                inputMemRenewDateBool = True
                inputMemRenewDate0 = datetime.date.today() + datetime.timedelta(days=365)
                inputMemRenewDate = inputMemRenewDate0.strftime('%B %d %Y')
                addNewMemberStr += "Membership Renewal Date: " + inputMemRenewDate + "\n"
            else:
                datetime.datetime.strptime(inputMemRenewDate, '%B %d %Y')
                inputMemRenewDateBool = True
                addNewMemberStr += "Membership Renewal Date: " + inputMemRenewDate + "\n"
        except ValueError:
            continue
    
    #Enter Phone number
    inputPhoneNumBool = False
    while not inputPhoneNumBool:
        os.system('clear')
        print(addNewMemberStr)
        print("Required: Enter 10 digit phone number. Phone number cannot start with 0\n")
        inputPhoneNum = input("Enter phone number (Example: 3367401337): ")
        if not inputPhoneNum.isnumeric() or len(inputPhoneNum) != 10:
            continue
        else:
            inputPhoneNumBool = True
            addNewMemberStr += "Phone Number: " + inputPhoneNum + "\n"
            
    #Enter email
    inputEmailBool = False
    os.system('clear')
    print(addNewMemberStr)
    print("Email format must be in the format: (username)@(domainname).(top-leveldomain)")
    while not inputEmailBool:
        inputEmail = input("Enter email: ")
        if not re.fullmatch(regex, inputEmail):
            continue
        else:
            inputEmailBool = True
            addNewMemberStr += "Email: " + inputEmail + "\n"
    
    #Enter Notes
    os.system('clear')
    print(addNewMemberStr)
    print("Optional: This can literally be anything\n")
    inputNotes = input("Any notes you want to add to your membership?: ")
    addNewMemberStr += "Notes: " + inputNotes + "\n"
    
    memNumStr = str(random.randint(100000,999999))
    
    os.system('clear')
    print(addNewMemberStr)
    print("Adding new member...")
    statusUpdated = "New member added"
    
    memberDict['Mno'].append(memNumStr)
    memberDict['Fn'].append(inputFirstName)
    memberDict['MI'].append(inputMidInitial)
    memberDict['Ln'].append(inputLastName)
    memberDict['DoB'].append(inputDateOfBirth)
    memberDict['Address'].append(inputAddress)
    memberDict['Status'].append(inputStatus)
    memberDict['msd'].append(inputMemStartDate)
    memberDict['med'].append('')
    memberDict['rdate'].append(inputMemRenewDate)
    memberDict['Phone'].append(inputPhoneNum)
    memberDict['Email'].append(inputEmail)
    memberDict['Notes'].append(inputNotes)

# %% Read and return CSV file with member data
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

def on_press(key):
    global break_program
    if key == keyboard.Key.esc:
        print ('\nProgram exited')
        os.system('clear')
        os._exit(0)
        break_program = True
        return False

with keyboard.Listener(on_press=on_press) as listener:
    while break_program == False:
        Manage_members()
        time.sleep(1)
    listener.join()