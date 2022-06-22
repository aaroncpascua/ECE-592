import csv
import os
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from pynput import keyboard #install
import time
import re
from tabulate import tabulate #install
import argparse
import pandas as pd
import textwrap
import matplotlib.pyplot as plt
import numpy as np

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
        bulkMemberOperation(globals()['memberDict'])
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
            if ".txt" in importPath:
                txtToCSV = pd.read_csv(importPath)
                FileName = importPath.split('.')
                importPath = FileName[0] + ".csv"
                txtToCSV.to_csv(importPath, index=None)
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
            print("There are " + str(len(reduceList)) + " members with invalid attribute values. These members are not added.")
            if warningBool:
                print("Invalid Input\n")
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
        
# %% Bulk member operation
def bulkMemberOperation(wholeDict):
    bulkStr = 'Bulk Operations\n'
    bulkMenu = "a. Push the renewal date (in integer months)\n" + "b. Change membership status\n" + "c. Remove members\n"
    criteriaMenu = "Options: \n"
    criteriaMenu += "Age <min age*> <max age> e.g. Age 25 40 or Age 65\n" 
    criteriaMenu += "Member <min period in years*> <max period in years> e.g. Member 1 10 or Member 10\n"
    criteriaMenu += "Status <membership status*> e.g. Basic or Basic Gold\n"
    criteriaMenu += "You can merge the criteria separted by comma e.g. Age 65, Status Basic Gold\n\n"
    criteriaMenu += "Note: * means it is a required input\n"
    
    loopBool = False
    warningBool = False
    while not loopBool:
        os.system('clear')
        print(bulkStr)
        print(bulkMenu)
        if warningBool:
            print("Invalid Input\n")
        menuChoice = input("Enter bulk operation option (a-c): ").lower()
            
        if menuChoice == 'a':
            choiceBool = False
            warningChoiceBool = False
            while not choiceBool:
                os.system('clear')
                print(bulkStr)
                print("Push the Renewal Date\n")
                if warningChoiceBool:
                    print('Invalid Input\n')
                choiceValue = input("Enter the renewal date in integer months: ")
                if choiceValue.isdigit():
                    bulkDict, bulkList = getBulkMembers(bulkStr, criteriaMenu, wholeDict, menuChoice, True, '')
                    for j in range(len(bulkDict['Mno'])):
                        for i in range(len(globals()['memberDict']['rdate'])):
                            if bulkDict['rdate'][j] == globals()['memberDict']['rdate'][i] and bulkDict['rdate'][j] != '':
                                renewalDate = datetime.datetime.strptime(globals()['memberDict']['rdate'][i], '%B %d %Y')
                                newRenewalDate = renewalDate + relativedelta(months=int(choiceValue))
                                newRenewalDateStr = newRenewalDate.strftime('%B %d %Y')
                                globals()['memberDict']['rdate'][i] = newRenewalDateStr
                                break
                    choiceBool = True
                else:
                    warningChoiceBool = True
            writeCSV(globals()['memberDict'])
            globals()['statusUpdated'] = "Renewal Date pushed " + choiceValue + " month(s) for " + str(len(bulkDict['Mno'])) + " members"
            Manage_members()
                    
        if menuChoice == 'b':
            choiceBool = False
            warningChoiceBool = False
            statusRegex = re.compile(r'[a-zA-z]+')
            while not choiceBool:
                os.system('clear')
                print(bulkStr)
                print("Change Membership Status\n")
                if warningChoiceBool:
                    print('Invalid Input\n')
                print("Status options: Basic, Silver, Gold, Platinum\n")
                choiceValue = input("Enter the new membership status: ").capitalize()
                if not re.fullmatch(statusRegex, choiceValue):
                    warningChoiceBool = True
                    continue
                if choiceValue not in globals()['status'][:-1]:
                    warningChoiceBool = True
                    continue
                else:
                    bulkDict, bulkList = getBulkMembers(bulkStr, criteriaMenu, wholeDict, menuChoice, True, '')
                    for j in range(len(bulkDict['Mno'])):
                        for i in range(len(globals()['memberDict']['Status'])):
                            if bulkDict['Status'][j] == globals()['memberDict']['Status'][i]:
                                globals()['memberDict']['Status'][i] = choiceValue
                                break
                    choiceBool = True
            writeCSV(globals()['memberDict'])
            globals()['statusUpdated'] = "Membership status changed to " + choiceValue + " for " + str(len(bulkDict['Mno'])) + " members"
            Manage_members()
                        
        if menuChoice == 'c':
            choiceBool = False
            warningChoiceBool = False
            statusRegex = re.compile(r'[a-zA-z]+')
            while not choiceBool:
                os.system('clear')
                print(bulkStr)
                print("Remove members\n")
                bulkDict, bulkList = getBulkMembers(bulkStr, criteriaMenu, wholeDict, menuChoice, True, '')
                for j in range(len(bulkDict['Mno'])):
                    for i in range(len(globals()['memberDict']['Mno'])):
                        if bulkDict['Mno'][j] == globals()['memberDict']['Mno'][i]:
                            globals()['memberDict']['med'][i] = date.today().strftime('%B %d %Y')
                            globals()['memberDict']['rdate'][i] = ''
                            break
                choiceBool = True
            writeCSV(globals()['memberDict'])
            globals()['statusUpdated'] = str(len(bulkDict['Mno'])) + " members removed"
            Manage_members()
        
        else:
            warningBool = True
        
# %% Get list of Mnos that match all bulk member criteria
def getBulkMembers(bulkStr, criteriaMenu, wholeDict, menuChoice, needInput, criteriaChoice):
    criteriaListOptions = ['Age', 'Member', 'Status']
    MnoList = []
    finalMno = []
    
    if menuChoice == 'a':
        menu = "Push Renewal Date"
    if menuChoice == 'b':
        menu = "Change Membership Status"
    if menuChoice == 'c':
        menu = "Remove members"
    
    criteriaLoop = False
    criteriaWarning = False
    while not criteriaLoop:
        criteriaList = []
        criteriaUsed = 0
        os.system('clear')
        print(bulkStr)
        print(criteriaMenu)
        if criteriaWarning:
            print("Invalid input\n")
        criteriaWarning = False
        if needInput:
            criteriaChoice = input("Enter " + menu + " criteria: ")
        print("Processing...")
        splitComma = criteriaChoice.split(',')
        for i in range(len(splitComma)): 
            criteriaList.append(splitComma[i].strip().capitalize().split(' '))
        #Check if input is valid
        for criteria in criteriaList:
            if criteria[0] not in criteriaListOptions:
                criteriaWarning = True
                        
        #Continue if a valid inputs are given
        if not criteriaWarning:
            for criteria in criteriaList:
                if criteria[0] == "Age":
                    criteriaUsed += 1
                    if len(criteria[1:]) > 2:
                        criteriaWarning = True
                        continue
                    else:
                        noSecondVal = False
                        try:
                            minAge = int(criteria[1])
                            try:
                                maxAge = int(criteria[2])
                            except IndexError:
                                noSecondVal = True
                        except ValueError:
                            criteriaWarning = True
                            continue
                        for i in range(len(wholeDict['DoB'])):
                            memberAge = age(datetime.datetime.strptime(wholeDict['DoB'][i], '%B %d %Y'))
                            if noSecondVal:
                                if memberAge >= minAge:
                                    MnoList.append(wholeDict['Mno'][i])
                            else:
                                if memberAge >= minAge and memberAge <= maxAge:
                                    MnoList.append(wholeDict['Mno'][i])
            
                elif criteria[0] == "Status":
                    criteriaUsed += 1
                    for c in criteria[1:]:
                        capitalizedCriteria = c.capitalize()
                        if criteria[1:].count(capitalizedCriteria) > 1:
                            criteriaWarning = True
                            continue
                        if capitalizedCriteria not in globals()['status']:
                            criteriaWarning = True
                            continue
                        else:
                            for i in range(len(wholeDict['Status'])):
                                if capitalizedCriteria == wholeDict['Status'][i]:
                                    MnoList.append(wholeDict['Mno'][i])
                
                elif criteria[0] == "Member":
                    criteriaUsed += 1
                    if len(criteria[1:]) > 2:
                        criteriaWarning = True
                        continue
                    else:
                        noSecondVal = False
                        try:
                            minMembershipAge = int(criteria[1])
                            try:
                                maxMembershipAge = int(criteria[2])
                            except IndexError:
                                noSecondVal = True
                        except ValueError:
                            criteriaWarning = True
                            continue
                        for i in range(len(wholeDict['Mno'])):
                            memberbershipAge = age(datetime.datetime.strptime(wholeDict['msd'][i], '%B %d %Y'))
                            if noSecondVal:
                                if memberbershipAge >= minMembershipAge and wholeDict['Status'][i] in globals()['status'][:-1]:
                                    MnoList.append(wholeDict['Mno'][i])
                            else:
                                if memberAge >= minMembershipAge and memberAge <= maxMembershipAge and wholeDict['Status'][i] in globals()['status'][:-1]:
                                    MnoList.append(wholeDict['Mno'][i])
                                    
            criteriaLoop = True

    for mno in wholeDict['Mno']:
        if MnoList.count(mno) == criteriaUsed:
            finalMno.append(mno)
    
    #Create list of membership data from bulk operation search
    wholeMemberList = []
    tempDict = wholeDict
    for i in range(len(finalMno)):
        for j in range(len(tempDict['Mno'])):
            member = []
            appendMember = False
            if finalMno[i] == tempDict['Mno'][j]:
                for key in tempDict:
                    appendMember = True
                    member.append(tempDict[key][j])
                if appendMember:
                    wholeMemberList.append(member)
                break
        
    #Create dictionary from wholeMemberList
    wholeListDict = {}
    for i in range(0, len(globals()['key'])):
        wholeListDict[globals()['key'][i]] = []
        
    for i in range(len(wholeMemberList)):
        member = wholeMemberList[i]
        k = 0
        for key in wholeListDict:
            wholeListDict[key].append(member[k])
            k += 1
            
    return wholeListDict, wholeMemberList
        
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
            if searchVals[j].capitalize() in dictionary[keys[j]][i]:                
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

# %% Make some graphs based on a mode
def graphMembers(mode):
    tempDict = readMemberCSV('memberdata.csv')
    if mode.capitalize() == 'Status':
        basicList, basicDict, dumbyValue = searchDictionary(tempDict, ['Status'], ['Basic'])
        silverList, silverDict, dumbyValue = searchDictionary(tempDict, ['Status'], ['Silver'])
        goldList, goldDict, dumbyValue = searchDictionary(tempDict, ['Status'], ['Gold'])
        platinumList, platinumDict, dumbyValue = searchDictionary(tempDict, ['Status'], ['Platinum'])
        noneList, noneDict, dumbyValue = searchDictionary(tempDict, ['Status'], ['None'])
        
        numBasic = len(basicList)
        numSilver = len(silverList)
        numGold = len(goldList)
        numPlatinum = len(platinumList)
        numNone = len(noneList)
        
        xLabels = ['Basic', 'Silver', 'Gold', 'Platinum', 'None']
        yValues = [numBasic, numSilver, numGold, numPlatinum, numNone]
        plt.bar(xLabels, yValues, color='maroon',width=0.4)
        plt.title('Number of Members vs Status')
        plt.xlabel('Status')
        plt.ylabel('Number of members')
        plt.show()
    
    if mode.capitalize() == 'Age':
        ageDict1825, ageList1825 = getBulkMembers('', '', tempDict, '', False, "Age 18 25, Status Basic Silver Gold Platinum")
        ageDict2535, ageList2535 = getBulkMembers('', '', tempDict, '', False, "Age 25 35, Status Basic Silver Gold Platinum")
        ageDict3550, ageList3550 = getBulkMembers('', '', tempDict, '', False, "Age 35 50, Status Basic Silver Gold Platinum")
        ageDict5065, ageList5065 = getBulkMembers('', '', tempDict, '', False, "Age 50 65, Status Basic Silver Gold Platinum")
        ageDict65Up, ageList65Up = getBulkMembers('', '', tempDict, '', False, "Age 65, Status Basic Silver Gold Platinum")
        
        list1825 = len(ageList1825)
        list2535 = len(ageList2535)
        list3550 = len(ageList3550)
        list5065 = len(ageList5065)
        list65Up = len(ageList65Up)
        
        xLabels = ['18-25', '25-35', '35-50', '50-65', '>65']
        yValues = [list1825, list2535, list3550, list5065, list65Up]
        plt.bar(xLabels, yValues, color='maroon',width=0.4)
        plt.title('Age Distribution of Active Members')
        plt.xlabel('Age Range')
        plt.ylabel('Number of members')
        plt.show()
    
    if mode.capitalize() == 'Year':
        xLabels = []
        year = 1981
        for i in range(39):
            xLabels.append(str(year))
            year += 1

        yValuesNew = []
        yValuesOld = []
        for j in range(2):
            year = 1981
            for i in range(39):
                counter = 0
                if j == 0:
                    for k in range(len(tempDict['msd'])):
                        splitDate = tempDict['msd'][k].split(' ')
                        if splitDate[2] == str(year) and tempDict['med'][k] == '':
                            counter += 1
                    yValuesNew.append(counter)
                if j == 1:
                    for fullDate in tempDict['med']:
                        splitDate = fullDate.split(' ')
                        try:
                            if splitDate[2] == str(year):
                                counter += 1
                        except IndexError:
                            pass
                    yValuesOld.append(counter)
                year += 1
        
        xAxis = np.arange(len(xLabels))
        
        plt.bar(xAxis-0.2, yValuesNew, width=0.4, color='green', label='New Members Added')
        plt.bar(xAxis+0.2, yValuesOld, width=0.4, color='maroon', label='Members Left')
        plt.xticks(xAxis, xLabels)
        plt.title('New Members Added/Members Left vs Year')
        plt.xlabel('Year')
        plt.ylabel('Number of members')
        plt.legend()
        plt.show()
    
    else:
        globals()['statusUpdated'] = "Cannot generate plot. " + mode.capitalize() + " does not exist"
        
    globals()['statusUpdated'] = "Generated " + mode.capitalize() + " plot"
    Manage_members()
        
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
    parser=argparse.ArgumentParser(
        description="This application manages members from a local file named 'memberdata.csv'.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''\
            Graph Information:
                Status:This will plot a bar graph of number of members vs membership status 
                Age:This will plot bar graph of number of active members in following age category, 18-25, 25-35, 35-50, 50-65, >65 + 
                Year:Bar graph of number of new members added and number of members left vs year {1981 to 2019}",action="store_true'''))
    parser.add_argument("-graph", "--graph", action='store', type=str, help="Graph member data using one of the following modes: Status, Age, Year")
    args = parser.parse_args()
    try:
        graphMembers(args.graph)
    except AttributeError:
        with keyboard.Listener(on_press=on_press) as listener:
            while break_program == False:
                Manage_members()
                time.sleep(1)
            listener.join()
    
           
if __name__ == "__main__":
    main()