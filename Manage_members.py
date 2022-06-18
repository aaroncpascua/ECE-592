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
status = ['Basic', 'Silver', 'Gold', 'Platinum', 'None']
break_program = False
regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
statusUpdated = "Manage Members"
deleteMember = False
upgradeDowngrade = False

# %% Manage Members Menu
def Manage_members(): # Add status updated print
    os.system('clear')
    globals()['memberDict'] = readMemberCSV()
    
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
        return
    elif userInput == 'e':
        return
    elif userInput == 'f':
        searchMembers(globals()['memberDict'])
    elif userInput == 'g':
        return
    elif userInput == 'h':
        return
    else:
        Manage_members()
 
# %% Add New Member function
def addNewMember(tempDict):
    os.system('clear')
    addNewMemberStr = "Adding new member:\n"
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
        if any(chr.isdigit() for chr in inputFirstName):
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
        if any(chr.isdigit() for chr in inputLastName):
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
def removeMember(tempDict, optionSelected, tableStr):  
    membershipNumList = []
    for memNum in tempDict['Mno']:
        membershipNumList.append(memNum)
        
    actualDictionary = globals()['memberDict']
    loopBool = False
    showWarning = False
    while not loopBool:
        os.system('clear')
        print(optionSelected)
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
    
# %% Upgrade/Downgrade Memberships
def upgradeDowngradeFunc(tempDict, optionSelected, tableStr):    
    membershipNumList = []
    for memNum in tempDict['Mno']:
        membershipNumList.append(memNum)
        
    actualDictionary = globals()['memberDict']
    loopBool = False
    showWarning = False
    while not loopBool:
        os.system('clear')
        print(optionSelected)
        print(tableStr + "\n")
        if showWarning:
            print("Invalid Input\n")
        deleteMember = input("Choose Mno to upgrade or downgrade: ")
        if deleteMember in tempDict['Mno']:
            loopBool1 = False
            showWarning = False
            while not loopBool1:
                os.system('clear')
                print(optionSelected)
                print(tableStr + "\n")
                if showWarning:
                    print("Invalid Input\n")
                upgradeChoice = input("Enter new Status ['Basic', 'Silver', 'Gold', 'Platinum']: ")
                if upgradeChoice in globals()['status'].pop(4):
                    for i in range(len(actualDictionary['Mno'])):
                        if deleteMember in actualDictionary['Mno'][i]:
                            todayPlusOneYear = datetime.date.today() + datetime.timedelta(days=365)
                            todayPlusOneYearStr = todayPlusOneYear.strftime('%B %d %Y')
                            actualDictionary['med'][i] = ''
                            actualDictionary['rdate'][i] = todayPlusOneYearStr
                            actualDictionary['Status'][i] = upgradeChoice
                            firstName = actualDictionary['Fn'][i]
                            lastName = actualDictionary['Ln'][i]
                            writeCSV(actualDictionary)
                            loopBool = True
                else:
                    showWarning = True
                    continue
        else:
            showWarning = True
            continue
    
        return firstName, lastName, upgradeChoice

# %% Search Members
def searchMembers(tempDict):
    searchOptions = "Search options:\n"
    
    Mno, Fn, MI, Ln, DoB, Address, Status, msd, med, rdate, Phone, Email, Notes = "", "", "", "", "", "", "", "", "", "", "", "", ""
    
    MnoStr = "Mno: "
    FnStr = "Fn: "
    MIStr = "MI: "
    LnStr = "Ln: "
    DoBStr = "DoB: "
    AddressStr = "Address: "
    StatusStr = "Status: "
    msdStr = "msd: "
    medStr = "med: "
    rdateStr = "rdate: "
    PhoneStr = "Phone: "
    EmailStr = "Email: "
    NotesStr = "Notes: "
    
    searchOptions += MnoStr + Mno + "\n"
    searchOptions += FnStr + Fn + "\n"  
    searchOptions += MIStr + MI + "\n" 
    searchOptions += LnStr + Ln + "\n"
    searchOptions += DoBStr + DoB + "\n"
    searchOptions += AddressStr + Address + "\n"
    searchOptions += StatusStr + Status + "\n" 
    searchOptions += msdStr + msd + "\n"
    searchOptions += medStr + med + "\n"
    searchOptions += rdateStr + rdate + "\n"
    searchOptions += PhoneStr + Phone + "\n"
    searchOptions += EmailStr + Email + "\n"
    searchOptions += NotesStr + Notes + "\n"
    
    loopDone = False
    showWarning = False
    showResults = False
    tabulatedResults = ""
    while not loopDone:
        os.system('clear')
        print(searchOptions)
        if showResults:
            print(tabulatedResults + "\n")
        if (showWarning):
            print("Warning: Invalid Input\n")
        inputKey = input("Pick a search option: ")
        if inputKey == 'Mno':
            Mno = input("Mno = ")
            showWarning = False
            resultList, tempDict = searchDictionary(tempDict, inputKey, Mno)
        elif inputKey == 'Fn':
            Fn = input("Fn = ")
            showWarning = False
            resultList, tempDict = searchDictionary(tempDict, inputKey, Fn)
        elif inputKey == 'MI':
            MI = input("MI = ")
            showWarning = False
            resultList, tempDict = searchDictionary(tempDict, inputKey, MI)
        elif inputKey == 'Ln':
            Ln = input("Ln = ")
            showWarning = False
            resultList, tempDict = searchDictionary(tempDict, inputKey, Ln)
        elif inputKey == 'DoB':
            DoB = input("DoB = ")
            showWarning = False
            resultList, tempDict = searchDictionary(tempDict, inputKey, DoB)
        elif inputKey == 'Address':
            Address = input("Address = ")
            showWarning = False
            resultList, tempDict = searchDictionary(tempDict, inputKey, Address)
        elif inputKey == 'Status':
            Status = input("Status = ")
            showWarning = False
            resultList, tempDict = searchDictionary(tempDict, inputKey, Status)
        elif inputKey == 'msd':
            msd = input("msd = ")
            showWarning = False
            resultList, tempDict = searchDictionary(tempDict, inputKey, msd)
        elif inputKey == 'med':
            med = input("med = ")
            showWarning = False
            resultList, tempDict = searchDictionary(tempDict, inputKey, med)
        elif inputKey == 'rdate':
            rdate = input("rdate = ")
            showWarning = False
            resultList, tempDict = searchDictionary(tempDict, inputKey, rdate)
        elif inputKey == 'Phone':
            Phone = input("Phone = ")
            showWarning = False
            resultList, tempDict = searchDictionary(tempDict, inputKey, Phone)
        elif inputKey == 'Email':
            Email = input("Email = ")
            showWarning = False
            resultList, tempDict = searchDictionary(tempDict, inputKey, Email)
        elif inputKey == 'Notes':
            Notes = input("Notes = ")
            showWarning = False
            resultList, tempDict = searchDictionary(tempDict, inputKey, Notes)
        else:
            showWarning = True
            continue
        
        searchOptions = ''
        searchOptions += MnoStr + Mno + "\n"
        searchOptions += FnStr + Fn + "\n"  
        searchOptions += MIStr + MI + "\n" 
        searchOptions += LnStr + Ln + "\n"
        searchOptions += DoBStr + DoB + "\n"
        searchOptions += AddressStr + Address + "\n"
        searchOptions += StatusStr + Status + "\n" 
        searchOptions += msdStr + msd + "\n"
        searchOptions += medStr + med + "\n"
        searchOptions += rdateStr + rdate + "\n"
        searchOptions += PhoneStr + Phone + "\n"
        searchOptions += EmailStr + Email + "\n"
        searchOptions += NotesStr + Notes + "\n"
        
        if len(resultList) > 10:
            printCheckBool = False
            showWarning1 = False
            while not printCheckBool:
                if showWarning1:
                    print("Warning: Invalid Input\n")
                printCheck = input("More than 10 members are matching the critera, print? (Y/N): ").upper()
                if printCheck == 'Y':
                    tabulatedResults = tabulate(resultList, headers=globals()['key'])
                    if globals()['deleteMember']:
                        firstName, lastName = removeMember(tempDict, searchOptions, tabulatedResults)
                        globals()['statusUpdated'] = "Deleted member " + firstName + " " + lastName
                        Manage_members()
                    if globals()['upgradeDowngrade']:
                        firstName, lastName, statusChange = upgradeDowngradeFunc(tempDict, searchOptions, tabulatedResults)
                        globals()['statusUpdated'] = "Deleted member " + firstName + " " + lastName + " Status changed to " + statusChange
                        Manage_members()
                    else:
                        showResults = True
                        printCheckBool = True
                        showWarning = False
                if printCheck == 'N':
                    searchMembers(globals()['memberDict'])
                else:
                    showWarning = True
                    continue
        else:
            tabulatedResults = tabulate(resultList, headers=globals()['key'])
            if globals()['deleteMember']:
                removeMember(tempDict, searchOptions, tabulatedResults)
                globals()['statusUpdated'] = "Deleted member" + firstName + " " + lastName
                Manage_members()
            if globals()['upgradeDowngrade']:
                firstName, lastName, statusChange = upgradeDowngradeFunc(tempDict, searchOptions, tabulatedResults)
                globals()['statusUpdated'] = "Deleted member " + firstName + " " + lastName + " Status changed to " + statusChange
                Manage_members()
            else:
                showResults = True
        
# %% Read CSV and return dictionary with member data
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

# %% search through dictionary and return list of lists with member data
def searchDictionary(dictionary, key, searchVal):
    indeces = []
    searchResults = []
    searchDict = {}
    for i in range(len(dictionary[key])):
        if searchVal in dictionary[key][i]:
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

    return searchResults, searchDict

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