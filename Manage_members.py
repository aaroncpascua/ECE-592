import csv
import os
import datetime
from datetime import date
from pynput import keyboard #install
import time
import re
from tabulate import tabulate #install

# Global Variables
memberDict = {}
key = ['Mno', 'Fn', 'MI', 'Ln', 'DoB', 'Address', 'Status', 'msd', 'med', 'rdate', 'Phone', 'Email', 'Notes']
requiredKey = ['Mno', 'Fn', 'Ln', 'DoB', 'Status', 'msd', 'rdate', 'Phone']
status = ['Basic', 'Silver', 'Gold', 'Platinum', 'None']
break_program = False
regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
nameRegex = re.compile(r'([A-Z][a-z]+(?:-[A-Z][a-z]+)?)')
statusUpdated = "Manage Members"
deleteMember = False
upgradeDowngrade = False
modifyMemberBool = False

# %% Manage Members Menu
def Manage_members(): # Add status updated print
    os.system('clear')
    globals()['memberDict'] = readMemberCSV('memberdata.csv')
    
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
        addNewMember(globals()['memberDict'])
    elif userInput == 'b':
        globals()['deleteMember'] = True
        searchMembers(globals()['memberDict'])
        globals()['deleteMember'] = False
    elif userInput == 'c':
        globals()['upgradeDowngrade'] = True
        searchMembers(globals()['memberDict'])
        globals()['upgradeDowngrade'] = False
    elif userInput == 'd':
        globals()['modifyMemberBool'] = True
        searchMembers(globals()['memberDict'])
        globals()['modifyMemberBool'] = False
    elif userInput == 'e':
        importMembers(globals()['memberDict'])
    elif userInput == 'f':
        searchMembers(globals()['memberDict'])
    elif userInput == 'g':
        return
    else:
        Manage_members()
 
# %% Add New Member function
def addNewMember(tempDict):
    os.system('clear')
    addNewMemberStr = "Adding new member\n"
    print(addNewMemberStr)
    
    #Enter first name
    inputFirstNameBool = False
    warningBool = False    
    while not inputFirstNameBool:
        os.system('clear')
        print(addNewMemberStr)
        if warningBool:
            print('Warning: Invalid Input\n')
        print('Required:\nFirst name format can only contain letters and special characters\n')
        inputFirstName = input("Enter first name: ")
        if not re.fullmatch(nameRegex, inputFirstName):
            inputFirstNameBool = False
            warningBool = True
        else:
            inputFirstNameBool = True
            addNewMemberStr += "First name: " + inputFirstName + "\n"
    
    #Enter middle initial
    inputMidInitialBool = False
    warningBool = False
    while not inputMidInitialBool:      
        try:
            os.system('clear')
            print(addNewMemberStr)
            if warningBool:
                print('Warning: Invalid Input\n')
            print("Optional:\nMiddle initial format can only contain a letter\n")
            inputMidInitial = input("Enter middle initial name: ").upper()
            if inputMidInitial.isspace() or inputMidInitial == '':
                inputMidInitialBool = True
                inputMidInitial = ''
                addNewMemberStr += "Middle Initial: " + inputMidInitial + "\n"
            if len(inputMidInitial) > 1 or not inputMidInitial.isalnum() or any(chr.isdigit() for chr in inputMidInitial):
                warningBool = True
                continue
            else:
                inputMidInitialBool = True
                addNewMemberStr += "Middle Initial: " + inputMidInitial + "\n"
        except ValueError:
            warningBool = True
            continue
    
    #Enter last name
    inputLastNameBool = False
    warningBool = False
    while not inputLastNameBool:
        os.system('clear') 
        print(addNewMemberStr)
        if warningBool:
            print('Warning: Invalid Input\n')
        print('Required:\nLast name format can only contain letters and special characters\n')
        inputLastName = input("Enter last name: ")
        if not re.fullmatch(nameRegex, inputLastName):
            warningBool = True
            continue
        else:
            inputLastNameBool = True
            addNewMemberStr += "Last name: " + inputLastName + "\n"
    
    #Enter date of birth
    inputDoBBool = False
    warningBool = False
    while not inputDoBBool:
        os.system('clear')
        print(addNewMemberStr)
        if warningBool:
            print('Warning: Invalid Input\n')
        print("Required:\nDate of Birth must be in the format like June 15 1996")
        print("You must be at least 18 years old.\n")
        inputDateOfBirth = input("Enter Date of Birth: ").capitalize()
        try:
            checkAge = age(datetime.datetime.strptime(inputDateOfBirth, '%B %d %Y'))
            if checkAge < 18:
                globals()['statusUpdated'] = "You must be at least 18 years old"
                Manage_members()
            else:
                datetime.datetime.strptime(inputDateOfBirth, '%B %d %Y')
                inputDoBBool = True
                addNewMemberStr += "Date of Birth: " + inputDateOfBirth + "\n"
        except ValueError:
            warningBool = True
            continue
        
    if findDuplicate(tempDict, inputFirstName, inputLastName, inputDateOfBirth):
        globals()['statusUpdated'] = "Membership exists for " + inputFirstName + " " + inputLastName
        Manage_members()
        
    #Enter address
    os.system('clear')
    print(addNewMemberStr)
    print("Optional:\nThis can literally be anything\n")
    inputAddress = input("Enter address: ")
    addNewMemberStr += "Address: " + inputAddress + "\n"
    
    #Enter status
    inputStatusBool = False
    warningBool = False
    while not inputStatusBool:
        os.system('clear')
        print(addNewMemberStr)
        if warningBool:
            print('Warning: Invalid Input\n')
        print("Required:\nEnter Basic, Silver, Gold, or Platinum\n")
        inputStatus = input("Enter member status: ").capitalize()
        if not inputStatus in status:
            warningBool = True
            continue
        else:
            inputStatusBool = True
            addNewMemberStr += "Status: " + inputStatus + "\n"
            
    #Enter Member Start Date
    inputMemStartDateBool = False
    warningBool = False
    while not inputMemStartDateBool:
        os.system('clear')
        print(addNewMemberStr)
        if warningBool:
            print('Warning: Invalid Input\n')
        print("Required:\nMembership start date must be in the format like June 15 1996.") 
        print("If blank, membership start date will be today's date.")
        print("Date must be a valid date after December 31 1980.\n")
        inputMemStartDate = input("Enter membership start date: ").capitalize()
        try:
            originDate = datetime.date(1981,1,1)
            inputDateObject = datetime.datetime.strptime(inputMemStartDate, '%B %d %Y').date()
            timeBetween = (inputDateObject - originDate).days
            if timeBetween < 0:
                warningBool = True
                continue
            if inputMemStartDate.isspace() or inputMemStartDate == '':
                inputMemStartDateBool = True
                inputMemStartDate = datetime.date.today().strftime('%B %d %Y')
                addNewMemberStr += "Membership Start Date: " + inputMemStartDate + "\n"
            else:
                datetime.datetime.strptime(inputMemStartDate, '%B %d %Y')
                inputMemStartDateBool = True
                addNewMemberStr += "Membership Start Date: " + inputMemStartDate + "\n"
        except ValueError:
            warningBool = True
            continue
        
    #Enter Member Renewal Date
    inputMemRenewDateBool = False
    warningBool = True
    while not inputMemRenewDateBool:
        os.system('clear')
        print(addNewMemberStr)
        if warningBool:
            print('Warning: Invalid Input\n')
        print("Required:\nMembership renewal date must be in the format like June 15 1996.")
        print("If blank, membership start date will be 1 year from membership start date")
        print("Membership renewal date cannot be more than 5 years of today's date\n")
        inputMemRenewDate = input("Enter membership renewal date: ").capitalize()
        try:
            if inputMemRenewDate != '':
                compareRenewDate = datetime.datetime.strptime(inputMemRenewDate, '%B %d %Y').date()
                fiveYearsFuture = datetime.date.today() + datetime.timedelta(days=1826)
                if compareRenewDate > fiveYearsFuture:
                    warningBool = True
                    continue
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
            warningBool = True
            continue
    
    #Enter Phone number
    inputPhoneNumBool = False
    warningBool = False
    while not inputPhoneNumBool:
        os.system('clear')
        print(addNewMemberStr)
        if warningBool:
            print('Warning: Invalid Input\n')
        print("Required:\nEnter 10 digit phone number. Phone number cannot start with 0\n")
        inputPhoneNum = input("Enter phone number (Example: 3367401337): ")
        if not inputPhoneNum.isnumeric() or len(inputPhoneNum) != 10 or inputPhoneNum[0] == '0':
            warningBool = True
            continue
        else:
            inputPhoneNumBool = True
            addNewMemberStr += "Phone Number: " + inputPhoneNum + "\n"
            
    #Enter email
    inputEmailBool = False
    warningBool = False
    while not inputEmailBool:
        os.system('clear')
        print(addNewMemberStr)
        if warningBool:
            print('Warning: Invalid Input\n')
        print("Optional:\nFormat: (username)@(domainname).(top-leveldomain)\n")
        inputEmail = input("Enter email: ")
        if inputEmail == '':
            inputEmailBool = True
            addNewMemberStr += "Email: " + inputEmail + "\n"
        if not re.fullmatch(regex, inputEmail):
            warningBool = True
            continue
        else:
            inputEmailBool = True
            addNewMemberStr += "Email: " + inputEmail + "\n"
    
    #Enter Notes
    os.system('clear')
    print(addNewMemberStr)
    print("Optional:\nThis can literally be anything\n")
    inputNotes = input("Any notes you want to add to your membership?: ")
    addNewMemberStr += "Notes: " + inputNotes + "\n"
    
    largestNumSortList = tempDict['Mno']
    largestNumSortList.sort()
    memNumStr = str(int(largestNumSortList[-1]) + 1)
    
    os.system('clear')
    print(addNewMemberStr)
    print("Adding new member...")
    globals()['statusUpdated'] = "New member added: " + inputFirstName + " " + inputLastName
    
    tempDict['Mno'].append(memNumStr)
    tempDict['Fn'].append(inputFirstName)
    tempDict['MI'].append(inputMidInitial)
    tempDict['Ln'].append(inputLastName)
    tempDict['DoB'].append(inputDateOfBirth)
    tempDict['Address'].append(inputAddress)
    tempDict['Status'].append(inputStatus)
    tempDict['msd'].append(inputMemStartDate)
    tempDict['med'].append('')
    tempDict['rdate'].append(inputMemRenewDate)
    tempDict['Phone'].append(inputPhoneNum)
    tempDict['Email'].append(inputEmail)
    tempDict['Notes'].append(inputNotes)
    
    writeCSV(tempDict)
    
    Manage_members()

# %% Remove member
def removeMember(tempDict, tableStr):  
    membershipNumList = []
    for memNum in tempDict['Mno']:
        membershipNumList.append(memNum)
        
    actualDictionary = globals()['memberDict']
    loopBool = False
    showWarning = False
    while not loopBool:
        os.system('clear')
        print("Removing member\n")
        print(tableStr + "\n")
        if showWarning:
            print("Invalid Input\n")
        deleteMember = input("Choose Mno to remove: ")
        if deleteMember in tempDict['Mno']:
            for i in range(len(actualDictionary['Mno'])):
                if deleteMember in actualDictionary['Mno'][i]:
                    todayDate = datetime.date.today()
                    actualDictionary['med'][i] = todayDate.strftime('%B %d %Y')
                    actualDictionary['rdate'][i] = ''
                    actualDictionary['Status'][i] = 'None'
                    firstName = actualDictionary['Fn'][i]
                    lastName = actualDictionary['Ln'][i]
                    writeCSV(actualDictionary)
                    loopBool = True
        else:
            showWarning = True
            continue
    
        return firstName, lastName        
    
# %% Upgrade/Downgrade Membership
def upgradeDowngradeFunc(tempDict, tableStr):    
    membershipNumList = []
    for memNum in tempDict['Mno']:
        membershipNumList.append(memNum)
        
    actualDictionary = globals()['memberDict']
    loopBool = False
    showWarning = False
    while not loopBool:
        os.system('clear')
        print("Upgrading or Downgrading member\n")
        print(tableStr + "\n")
        if showWarning:
            print("Invalid Input\n")
        deleteMember = input("Choose Mno to upgrade or downgrade: ")
        if deleteMember in tempDict['Mno']:
            loopBool1 = False
            showWarning = False
            while not loopBool1:
                os.system('clear')
                print("Upgrading or Downgrading member\n")
                print(tableStr + "\n")
                if showWarning:
                    print("Invalid Input\n")
                upgradeChoice = input("Enter new Status ['Basic', 'Silver', 'Gold', 'Platinum']: ")
                if upgradeChoice in globals()['status'][:4]:
                    for i in range(len(actualDictionary['Mno'])):
                        if deleteMember in actualDictionary['Mno'][i]:
                            todayPlusOneYear = datetime.date.today() + datetime.timedelta(days=365)
                            todayPlusOneYearStr = todayPlusOneYear.strftime('%B %d %Y')
                            actualDictionary['med'][i] = ''
                            actualDictionary['rdate'][i] = todayPlusOneYearStr
                            actualDictionary['Status'][i] = upgradeChoice
                            writeCSV(actualDictionary)
                            firstName = actualDictionary['Fn'][i]
                            lastName = actualDictionary['Ln'][i]
                            loopBool = True
                            loopBool1 = True
                else:
                    showWarning = True
                    continue
        else:
            showWarning = True
            continue
    
        return firstName, lastName, upgradeChoice

# %% Modify Member
def modifyMember(tempDict, tableStr):
    membershipNumList = []
    for memNum in tempDict['Mno']:
        membershipNumList.append(memNum)
        
    actualDictionary = globals()['memberDict']
    loopBool = False
    showWarning = False
    while not loopBool:
        os.system('clear')
        print("Modifying member\n")
        print(tableStr + "\n")
        if showWarning:
            print("Invalid Input\n")
        memberToModify = input("Choose Mno to modify: ")
        if memberToModify in tempDict['Mno']:
            loopBool1 = False
            showWarning = False
            while not loopBool1:
                os.system('clear')
                print("Modifying member\n")
                print(tableStr + "\n")
                if showWarning:
                    print("Invalid Input\n")
                attributeToModify = input("Enter Attribute to modify: ")
                for j in range(len(globals()['key'])):
                    if attributeToModify == globals()['key'][j]:
                        modifiedValue = modifyMemberValue(globals()['key'][j])                            
                        for i in range(len(actualDictionary[attributeToModify])):
                            if memberToModify in actualDictionary['Mno'][i]:
                                actualDictionary[attributeToModify][i] = modifiedValue
                                writeCSV(actualDictionary)
                                firstName = actualDictionary['Fn'][i]
                                lastName = actualDictionary['Ln'][i]
                                loopBool = True
                                loopBool1 = True
                else:
                    showWarning = True
                    continue
        else:
            showWarning = True
            continue
    
        return firstName, lastName, attributeToModify, modifiedValue

# %% Modify member value
def modifyMemberValue(inputVal):
    newVal =''
    modifyStr = 'Modifying Attribute: ' + inputVal + "\n"
    
    if inputVal == 'Fn':
        #Enter first name
        inputFirstNameBool = False
        warningBool = False    
        while not inputFirstNameBool:
            os.system('clear')
            print(modifyStr)
            if warningBool:
                print('Warning: Invalid Input\n')
            print('First name format can only contain letters and special characters\n')
            newVal = input("Enter first name: ")
            if any(chr.isdigit() for chr in newVal):
                inputFirstNameBool = False
                warningBool = True
            else:
                inputFirstNameBool = True
    
    #Enter middle initial
    if inputVal == 'MI':
        inputMidInitialBool = False
        warningBool = False
        while not inputMidInitialBool:      
            try:
                os.system('clear')
                print(modifyStr)
                if warningBool:
                    print('Warning: Invalid Input\n')
                print("Middle initial format can only contain a letter\n")
                newVal = input("Enter middle initial name: ").upper()
                if newVal.isspace() or newVal == '':
                    inputMidInitialBool = True
                    newVal = ''
                if len(newVal) > 1 or not newVal.isalnum() or any(chr.isdigit() for chr in newVal):
                    warningBool = True
                    continue
                else:
                    inputMidInitialBool = True
            except ValueError:
                warningBool = True
                continue
    
    #Enter last name
    if inputVal == 'Ln':
        inputLastNameBool = False
        warningBool = False
        while not inputLastNameBool:
            os.system('clear') 
            print(modifyStr)
            if warningBool:
                print('Warning: Invalid Input\n')
            print('Last name format can only contain letters and special characters\n')
            newVal = input("Enter last name: ")
            if any(chr.isdigit() for chr in newVal):
                warningBool = True
                continue
            else:
                inputLastNameBool = True
    
    #Enter date of birth
    if inputVal == 'DoB':
        inputDoBBool = False
        warningBool = False
        while not inputDoBBool:
            os.system('clear')
            print(modifyStr)
            if warningBool:
                print('Warning: Invalid Input\n')
            print("Date of Birth must be in the format like June 15 1996")
            print("You must be at least 18 years old.\n")
            newVal = input("Enter Date of Birth: ").capitalize()
            try:
                checkAge = age(datetime.datetime.strptime(newVal, '%B %d %Y'))
                if checkAge < 18:
                    globals()['statusUpdated'] = "You must be at least 18 years old"
                    Manage_members()
                else:
                    datetime.datetime.strptime(newVal, '%B %d %Y')
                    inputDoBBool = True
            except ValueError:
                warningBool = True
        
    #Enter address
    if inputVal == 'Address':
        os.system('clear')
        print(modifyStr)
        print("This can literally be anything\n")
        newVal = input("Enter address: ")
        
        #Enter status
        inputStatusBool = False
        warningBool = False
        while not inputStatusBool:
            os.system('clear')
            print(modifyStr)
            if warningBool:
                print('Warning: Invalid Input\n')
            print("Enter Basic, Silver, Gold, or Platinum\n")
            newVal = input("Enter member status: ").capitalize()
            if not newVal in status:
                warningBool = True
                continue
            else:
                inputStatusBool = True
        
    #Enter Member Renewal Date
    if inputVal == 'rdate':
        inputMemRenewDateBool = False
        warningBool = True
        while not inputMemRenewDateBool:
            os.system('clear')
            print(modifyStr)
            if warningBool:
                print('Warning: Invalid Input\n')
            print("Membership renewal date must be in the format like June 15 1996.")
            print("If blank, membership start date will be 1 year from membership start date")
            print("Membership renewal date cannot be more than 5 years of today's date\n")
            newVal = input("Enter membership renewal date: ").capitalize()
            try:
                if newVal != '':
                    compareRenewDate = datetime.datetime.strptime(newVal, '%B %d %Y').date()
                    fiveYearsFuture = datetime.date.today() + datetime.timedelta(days=1826)
                    if compareRenewDate > fiveYearsFuture:
                        warningBool = True
                        continue
                if newVal.isspace() or newVal == '':
                    inputMemRenewDateBool = True
                    inputMemRenewDate0 = datetime.date.today() + datetime.timedelta(days=365)
                    inputMemRenewDate = inputMemRenewDate0.strftime('%B %d %Y')
                else:
                    datetime.datetime.strptime(inputMemRenewDate, '%B %d %Y')
                    inputMemRenewDateBool = True
            except ValueError:
                warningBool = True
                continue
    
    #Enter Phone number
    if inputVal == 'Phone':
        inputPhoneNumBool = False
        warningBool = False
        while not inputPhoneNumBool:
            os.system('clear')
            print(modifyStr)
            if warningBool:
                print('Warning: Invalid Input\n')
            print("Enter 10 digit phone number. Phone number cannot start with 0\n")
            newVal = input("Enter phone number (Example: 3367401337): ")
            if not newVal.isnumeric() or len(newVal) != 10 or newVal[0] == '0':
                warningBool = True
                continue
            else:
                inputPhoneNumBool = True
            
    #Enter email
    if inputVal == 'Email':
        inputEmailBool = False
        warningBool = False
        while not inputEmailBool:
            os.system('clear')
            print(modifyStr)
            if warningBool:
                print('Warning: Invalid Input\n')
            print("Format: (username)@(domainname).(top-leveldomain)\n")
            newVal = input("Enter email: ")
            if newVal == '':
                inputEmailBool = True
            if not re.fullmatch(regex, newVal):
                warningBool = True
                continue
            else:
                inputEmailBool = True
    
    #Enter Notes
    if inputVal == 'Notes':
        os.system('clear')
        print(modifyStr)
        print("This can literally be anything\n")
        newVal = input("Any notes you want to add to your membership?: ")
    
    return newVal

# %% Import members from csv or txt
def importMembers(tempDict):
    importStr = "Importing new members or modifying existing members\n"
    
    importBool = False
    warningBool = False
    while not importBool:
        os.system('clear')
        print(importStr)
        print("Example input: E:\\Documents\\College\\NCSU\\ECE492\\importmembers.csv\n")
        if warningBool:
            print("File does not exist\n")
        importPath = input("Enter file path to import: ")
        if os.path.exists(importPath):
            importBool = True
        else:
            warningBool = True
            
    importDict = {}
    importDict = readMemberCSV(importPath)
    
    memberExistList = []
    memberExistIndeces = []
    
    #Create dictionary
    memberExistDict = {}
    for i in range(0, len(globals()['key'])):
        memberExistDict[globals()['key'][i]] = []
        
    #Find members from csv who are duplicates
    searchKeys = []
    searchVals = []
    searchType = []
    for i in range(len(importDict['Mno'])):
        firstNameExist = False
        lastNameExist = False
        dobExist = False 
        if importDict['Fn'][i] in globals()['memberDict']['Fn']:
            firstNameExist = True
        if importDict['Ln'][i] in globals()['memberDict']['Ln']:
            lastNameExist = True
        if importDict['DoB'][i] in globals()['memberDict']['DoB']:
            dobExist = True
        if firstNameExist and lastNameExist and dobExist:
            memberExistIndeces.append(i)
            searchKeySub = []
            searchKeySub.append('Fn')
            searchKeySub.append('Ln')
            searchKeySub.append('DoB')
            searchKeys.append(searchKeySub)
            searchValSub = []
            searchValSub.append(importDict['Fn'][i])
            searchValSub.append(importDict['Ln'][i])
            searchValSub.append(importDict['DoB'][i])
            searchVals.append(searchValSub)
            searchType.append('other')
            continue
        if importDict['Mno'][i] in tempDict['Mno'][i]:
            if importDict['Mno'][i] == '':
                continue
            memberExistIndeces.append(i)
            searchKeySub = []
            searchKeySub.append('Mno')
            searchKeys.append(searchKeySub)
            searchValSub = []
            searchValSub.append(importDict['Mno'][i])
            searchVals.append(searchValSub)
            searchType.append('Mno')
            continue
            
    #Create list with duplicate members
    for i in memberExistIndeces:
        memberInfo = []
        for k in importDict:
            memberInfo.append(importDict[k][i])
        memberExistList.append(memberInfo)
    tabulatedResults = tabulate(memberExistList, headers=globals()['key'])
    
    #Create dictionary with duplicate members
    for i in range(len(memberExistList)):
        member = memberExistList[i]
        j = 0
        for key in memberExistDict:
            memberExistDict[key].append(member[j])
            j += 1
    try:   
        if memberExistList:
            loopBool = False
            warningBool = False
            while not loopBool:
                os.system('clear')
                print(importStr)
                print(tabulatedResults + "\n")
                if warningBool:
                    print("Invalid Input\n")
                addMemberChoice = input('The list above are existing members. Do you want to overwrite their data? (Y/N): ').upper()
                if addMemberChoice == 'Y':
                    for i in range(len(memberExistIndeces)):
                        resultList, resultDict, resultIndex = searchDictionary(globals()['memberDict'], searchKeys[i], searchVals[i])
                        ri = resultIndex[0]
                        mi = memberExistIndeces[i]
                        for k in globals()['memberDict']:
                            if searchType[i] == 'Mno':
                                tempDict[k][ri] = importDict[k][mi]
                            if searchType[i] == 'other':
                                tempDict[k][ri] = importDict[k][mi]
                    
                    #remove member from members from dictionary
                    removedIndex = 0
                    for i in range(len(memberExistIndeces)):
                        mi = memberExistIndeces[i] - removedIndex
                        j = 0
                        for k in globals()['memberDict']:
                            if importDict[k][mi] == memberExistList[i][j]:
                                importDict[k].pop(mi)
                            j += 1
                        removedIndex += 1
                    writeCSV(tempDict)
                    globals()['statusUpdated'] = "Overwrote member data"
                    loopBool = True
                if addMemberChoice == 'N':
                    loopBool = True
                    globals()['statusUpdated'] = "No members added from " + importPath
                else:
                    warningBool = True
    except IndexError as error:
        globals()['statusUpdated'] = "Issue modifying members: " + str(error)
        Manage_members()
    
    #Create list to reduce for invalid attributes and blank required attributes
    reduceList = []
    reduceListIndeces = []
    wrongAttributeTotal = 0
    isRequiredEmptyList = []
    
    #Create dictionary
    reducedDict = {}
    for i in range(0, len(globals()['key'])):
        reducedDict[globals()['key'][i]] = []
        
    #Check if a required value is blank, store index into reduceListIndeces[]
    for i in range(len(importDict['Mno'])):
        for key in importDict:
            if key in globals()['requiredKey']:
                if importDict[key][i] == '':
                    print(importDict[key][i])
                    isRequiredEmptyList.append(i)
                    break
      
    #Loop through each attribute of each member and see if there are attributes with invalid values
    for i in range(len(importDict['Mno'])):                
        for key in importDict:
            wrongAttributeBool = False
            
            #Enter Mno
            if key == 'Mno':
                if importDict[key][i] == '':
                    continue
                inputMno = importDict[key][i]
                if not inputMno.isnumeric() or len(inputMno) != 6 or inputMno[0] == '0':
                    wrongAttributeTotal += 1
                    wrongAttributeBool = True
                    break
            
            #Enter first name
            elif key == 'Fn':
                if importDict[key][i] == '':
                    continue
                inputFirstName = importDict[key][i]
                if not re.fullmatch(nameRegex, inputFirstName):
                    wrongAttributeTotal += 1
                    wrongAttributeBool = True
                    break
            
            #Enter middle initial    
            elif key == "MI":
                if importDict[key][i] == '':
                    continue
                try:
                    inputMidInitial = importDict[key][i]
                    if len(inputMidInitial) > 1 or not inputMidInitial.isalnum() or any(chr.isdigit() for chr in inputMidInitial):
                        wrongAttributeTotal += 1
                        wrongAttributeBool = True
                        break
                except ValueError:
                    wrongAttributeTotal += 1
                    wrongAttributeBool = True
                    break
            
            #Enter last name
            elif key == 'Ln':
                if importDict[key][i] == '':
                    continue
                inputLastName = importDict[key][i]
                if not re.fullmatch(nameRegex, inputLastName):
                    wrongAttributeTotal += 1
                    wrongAttributeBool = True
                    break
            
            #Enter date of birth
            elif key == 'DoB':
                if importDict[key][i] == '':
                    continue
                try:
                    inputDateOfBirth = importDict[key][i].capitalize()
                    checkAge = age(datetime.datetime.strptime(inputDateOfBirth, '%B %d %Y'))
                    if checkAge < 18:
                        wrongAttributeTotal += 1
                        wrongAttributeBool = True
                        break
                except ValueError:
                    wrongAttributeTotal += 1
                    wrongAttributeBool = True
                    break
                
            #if findDuplicate(tempDict, inputFirstName, inputLastName, inputDateOfBirth):
            #    Manage_members()
            
            #Enter status
            elif key == 'Status':
                if importDict[key][i] == '':
                    continue
                inputStatus = importDict[key][i].capitalize()
                if not inputStatus in status:
                    wrongAttributeTotal += 1
                    wrongAttributeBool = True
                    break
                    
            #Enter Member Start Date
            elif key == 'msd':
                if importDict[key][i] == '':
                    continue
                try:
                    inputMemStartDate = importDict[key][i].capitalize()
                    originDate = datetime.date(1981,1,1)
                    inputDateObject = datetime.datetime.strptime(inputMemStartDate, '%B %d %Y').date()
                    timeBetween = (inputDateObject - originDate).days
                    if timeBetween < 0:
                        wrongAttributeTotal += 1
                        wrongAttributeBool = True
                        break
                except ValueError:
                    wrongAttributeTotal += 1
                    wrongAttributeBool = True
                    break
                
            #Enter Member Start Date
            elif key == 'med':
                if importDict[key][i] == '':
                    continue
                try:
                    inputDateOfBirth = importDict[key][i].capitalize()
                    datetime.datetime.strptime(inputDateOfBirth, '%B %d %Y')
                except ValueError:
                    wrongAttributeTotal += 1
                    wrongAttributeBool = True
                    break
                
            #Enter Member Renewal Date
            elif key == 'rdate':
                if importDict[key][i] == '':
                    continue
                try:
                    inputMemRenewDate = importDict[key][i].capitalize()
                    compareRenewDate = datetime.datetime.strptime(inputMemRenewDate, '%B %d %Y').date()
                    fiveYearsFuture = datetime.date.today() + datetime.timedelta(days=1826)
                    if compareRenewDate > fiveYearsFuture:
                        wrongAttributeTotal += 1
                        wrongAttributeBool = True
                        break
                    if inputMemRenewDate != '' and importDict['Status'][i] == 'None':
                        wrongAttributeTotal += 1
                        wrongAttributeBool = True
                        break
                except ValueError:
                    wrongAttributeTotal += 1
                    wrongAttributeBool = True
                    break
            
            #Enter Phone number
            elif key == 'Phone':
                if importDict[key][i] == '':
                    continue
                inputPhoneNum = importDict[key][i]
                if not inputPhoneNum.isnumeric() or len(inputPhoneNum) != 10 or inputPhoneNum[0] == '0':
                    wrongAttributeTotal += 1
                    wrongAttributeBool = True
                    break
                    
            #Enter email
            elif key == 'Email':
                if importDict[key][i] == '':
                    continue
                inputEmail = importDict[key][i]
                if not re.fullmatch(regex, inputEmail):
                    wrongAttributeTotal += 1
                    wrongAttributeBool = True
                    break
        if not wrongAttributeBool and i in isRequiredEmptyList:
            reduceListIndeces.append(i)    
      
    #Store members with empty required values and proper attributes into reduceList[]
    for i in reduceListIndeces:
        memberInfo = []
        for k in importDict:
            memberInfo.append(importDict[k][i])
        reduceList.append(memberInfo)
    tabulatedResults = tabulate(reduceList, headers=globals()['key'])
    
    #Create dictionary to store members with empty required values
    for i in range(len(reduceList)):
        member = reduceList[i]
        j = 0
        for key in reducedDict:
            reducedDict[key].append(member[j])
            j += 1
            
    #Check if there are any missing members, if there are, prompt user if they want to add anyway
    if reduceList:
        loopBool = False
        warningBool = False
        while not loopBool:
            os.system('clear')
            print(importStr)
            print(tabulatedResults + "\n")
            print("There are " + str(wrongAttributeTotal) + " members with invalid attribute values. These members are not added.")
            if warningBool:
                print("Invalid Input")
            addMemberChoice = input('The list above have missing required attributes. Do you want to add anyway? (Y/N): ').upper()
            if addMemberChoice == 'Y':
                for i in range(len(reduceList)):
                    for key in reducedDict:
                        globals()['memberDict'][key].append(reducedDict[key][i])
                writeCSV(globals()['memberDict'])
                globals()['statusUpdated'] = "Added " + str(len(reduceList)) + " members from " + importPath
                loopBool = True
            if addMemberChoice == 'N':
                loopBool = True
                globals()['statusUpdated'] = "No members added from " + importPath
            else:
                warningBool = True
        Manage_members()
    else:
        for i in range(len(importDict['Mno'])):
            for key in importDict:
                globals()['memberDict'][key].append(importDict[key][i])
                writeCSV(globals()['memberDict'])
        Manage_members()
        
# %% Search Members
def searchMembers(tempDict):
    searchOptions = "Searching for members\n"
    
    loopDone = False
    showWarning = False
    tabulatedResults = ""
    while not loopDone:
        strippedKey = []
        strippedKeyValue = []
        os.system('clear')
        print(searchOptions)
        if (showWarning):
            print("Warning: Invalid Input\n")
        print("Key Options: Mno, Fn, MI, Ln, DoB, Address, Status, msd, med, rdate, Phone, Email, Notes\n")
        print("Example input: [key]:[value], [key]:[value], ...\n")
        try:
            inputSearchOptions = input("Pick a search option: ")
            split = inputSearchOptions.split(',')
            for i in range(len(split)):
                split[i] = split[i].strip()
            for i in range(len(split)):
                split[i] = split[i].split(':')
            for i in range(len(split)):
                strippedKey.append(split[i][0])
                strippedKeyValue.append(split[i][1])
            resultList, tempDict, dumbyValue = searchDictionary(tempDict, strippedKey, strippedKeyValue)
        except (KeyError,IndexError):
            showWarning = True
            continue
        
        if len(resultList) > 10:
            printCheckBool = False
            showWarning1 = False
            while not printCheckBool:
                os.system('clear')
                print(searchOptions)
                if showWarning1:
                    print("Warning: Invalid Input\n")
                printCheck = input("More than 10 members are matching the critera, print? (Y/N): ").upper()
                if printCheck == 'Y':
                    tabulatedResults = tabulate(resultList, headers=globals()['key'])
                    if globals()['deleteMember']:
                        firstName, lastName = removeMember(tempDict, tabulatedResults)
                        globals()['statusUpdated'] = "Deleted member " + firstName + " " + lastName
                        Manage_members()
                    if globals()['upgradeDowngrade']:
                        firstName, lastName, statusChange = upgradeDowngradeFunc(tempDict, tabulatedResults)
                        globals()['statusUpdated'] = firstName + " " + lastName + " Status changed to " + statusChange
                        Manage_members()
                    if globals()['modifyMemberBool']:
                        firstName, lastName, keyChange, valueChange = modifyMember(tempDict, tabulatedResults)
                        globals()['statusUpdated'] = firstName + " " + lastName +  " " + keyChange + "changed to " + valueChange
                        Manage_members()
                    else:
                        globals()['statusUpdated'] = "Search Results:\n" + tabulatedResults + "\n"
                        Manage_members()
                if printCheck == 'N':
                    searchMembers(globals()['memberDict'])
                else:
                    showWarning1 = True
                    continue
        else:
            tabulatedResults = tabulate(resultList, headers=globals()['key'])
            if globals()['deleteMember']:
                removeMember(tempDict, tabulatedResults)
                globals()['statusUpdated'] = "Deleted member" + firstName + " " + lastName
                Manage_members()
            if globals()['upgradeDowngrade']:
                firstName, lastName, statusChange = upgradeDowngradeFunc(tempDict, tabulatedResults)
                globals()['statusUpdated'] = "Deleted member " + firstName + " " + lastName + " Status changed to " + statusChange
                Manage_members()
            if globals()['modifyMemberBool']:
                firstName, lastName, keyChange, valueChange = modifyMember(tempDict, tabulatedResults)
                globals()['statusUpdated'] = firstName + " " + lastName +  " " + keyChange + "changed to " + valueChange
                Manage_members()
            else:
                globals()['statusUpdated'] = "Search Results:\n" + tabulatedResults + "\n"
                Manage_members()
        
# %% Read CSV and return dictionary with member data
def readMemberCSV(filePath):
    tempDict = {}
    with open(filePath, mode='r') as inFile:
        keyReader = csv.reader(inFile)
        key = []
        key = next(keyReader)
        for i in range(0, len(key)):
            tempDict[key[i]] = []
        inFile.close()
        
    with open(filePath, mode='r') as inFile:    
        recordReader = csv.DictReader(inFile)
        for record in recordReader:
            for k in tempDict:
                tempDict[k].append(record[k])
    
    return tempDict

# %% Get dictionary and write over previous CSV file
def writeCSV(tempDict):
    file = open('memberdata.csv', 'w', newline='')
    writer = csv.writer(file, delimiter=',', quotechar='"')
    writer.writerow(key)
    
    writerCounter = 0
    while writerCounter < len(tempDict['Mno']):
        writeThis = []
        for k in memberDict:
            writeThis.append(memberDict[k][writerCounter])
        writer.writerow(writeThis)
        
        writerCounter += 1
    file.close()

# %% Find duplicate in memberDict[key] list
def findDuplicate(tempDict, firstName, lastName, DoB):
    '''
    Loop through memberDict[key] for any duplicates. 
    Return true for a duplicate
    Return false for original
    '''
    
    firstNameDup = False
    lastNameDup = False
    DoBDup = False
    
    if (tempDict['Fn'].count(firstName) >= 1): firstNameDup = True
    if (tempDict['Ln'].count(lastName) >= 1): lastNameDup = True
    if (tempDict['DoB'].count(DoB) >= 1): DoBDup = True
    print(tempDict['DoB'].count(DoB))
    
    if firstNameDup and lastNameDup and DoBDup: return True
    else: return False

# %% Returns the age given a a date
def age(birthdate):
    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age

# %% Find the renewal date 5 years ahead
def greaterThan5Years(renewDate):
    today = date.today()
    age = today.year - renewDate.year - ((today.month, today.day) < (renewDate.month, renewDate.day))
    return age

# %% Search through dictionary and return list of lists with member data
def searchDictionary(dictionary, keys, searchVals):
    indeces = []
    searchResults = []
    wholeDictionaryList = []
    searchDict = {}
    
    for key in keys:
        dumbyValue = dictionary[key]
    
    for i in range(len(dictionary['Mno'])):
        member = []
        k = 0
        for key in dictionary:
            member.append(dictionary[key][i])
            k += 1
        wholeDictionaryList.append(member)
    
    for i in range(len(wholeDictionaryList)):
        allValsMatch = []
        for j in range(len(searchVals)):
            if searchVals[j] in dictionary[keys[j]][i]:                
                allValsMatch.append('True')
        if allValsMatch.count('True') == len(searchVals):
            indeces.append(i)
    for j in indeces:
        memberInfo = []
        for k in dictionary:
            memberInfo.append(dictionary[k][j])
        searchResults.append(memberInfo)
     
    for i in range(0, len(globals()['key'])):
        searchDict[globals()['key'][i]] = []
        
    for i in range(len(searchResults)):
        member = searchResults[i]
        k = 0
        for key in searchDict:
            searchDict[key].append(member[k])
            k += 1

    return searchResults, searchDict, indeces

# %% Listen for escape key press
def on_press(key):
    global break_program
    global startProgram
    if key == keyboard.Key.esc:
        os.system('clear')
        print ('Program exited')
        os._exit(0)
        break_program = False
        return False

# %% Main function definition
def main():
    with keyboard.Listener(on_press=on_press) as listener:
        while break_program == False:
            Manage_members()
            time.sleep(1)
        listener.join()
        
if __name__ == "__main__":
    main()