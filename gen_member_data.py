import names #isntall
import random
import datetime
import dateutil #install
import csv
import string
import random_address #install

#Global Variables
key = ['Mno', 'Fn', 'MI', 'Ln', 'DoB', 'Address', 'Status', 'msd', 'med', 'rdate', 'Phone', 'Email', 'Notes']
status = ['Basic', 'Silver', 'Gold', 'Platinum', 'None']
memberDict = {}

# %% Generate Member Data
def gen_member_data(fname:str = 'memberdata.csv', no:int = 1000):
    """
    Inputs are -no <number of members> and -fname <filename>
    -no is number of random members to be generated in -fname
    If no arguments are given, generate 1000 members and save in a new file "memberdata.csv"
    """
    
    if not isinstance(fname, str) or not ('.csv') in fname or not isinstance(no, int):
        print('Invalid Input')
        return
    
    # Create keys in memberDict using key[]
    for i in range(0, len(key)):
        memberDict[key[i]] = []

    # Generate random values for each of the required attributes, remaining returns blank
    counter = 0
    while counter < no:
        #Generate random Membership Numbers
        memNumStr = str(random.randint(100000,999999))

        #Generate a random person's first name, last name, and birthday
        first_name, last_name, birthDay = genRandPerson(memberDict)
        
        #Generate a random capital letter for middle initial
        middleInitial = random.choice(string.ascii_letters).upper()
        
        #Generate Random Addresses
        try:
            addressDict = random_address.real_random_address()
            addressStr = addressDict['address1'] + ', ' + addressDict['city'] + ', ' + addressDict['state'] + ' ' + addressDict['postalCode']
        except KeyError:
            addressStr = addressDict['address1'] + ', Greensboro, ' + addressDict['state'] + ' ' + addressDict['postalCode']

        #Generate random Membership Status from status[]
        memStatus = random.choice(status)
        
        #Generate random Membership Start Date and Renewal Date starting from Dec 1 1980
        #If member status is None, Renewal Date is blank
        if (memStatus != 'None'):
            memStartDate, memRenewalDate = genRandDate(1981,1,1,True)
            memEndDate = ''
        else:
            memStartDate, memEndDate = genRandDate(1981,1,1,False)
            memRenewalDate = ''
        
        #Generate random 10 digit phone number
        phoneStr = str(random.randint(1000000000,9999999999))
        
        #Generate email in the NCSU email format for funsies
        usedEmailCounter = 0
        reducedLastName = ""
        reducedLastNameCounter = 0
        while reducedLastNameCounter < 6:
            if len(last_name) < 6:
                reducedLastName = last_name
                break
            else:
                reducedLastName += last_name[reducedLastNameCounter]
                reducedLastNameCounter += 1
        emailStr = generateNCSUEmail(memberDict, first_name, middleInitial, reducedLastName, usedEmailCounter)
        
        #Add values to dictionary
        memberDict['Mno'].append(memNumStr)
        memberDict['Fn'].append(first_name)
        memberDict['MI'].append(middleInitial)
        memberDict['Ln'].append(last_name)
        memberDict['DoB'].append(birthDay)
        memberDict['Address'].append(addressStr)
        memberDict['Status'].append(memStatus)
        memberDict['msd'].append(memStartDate)
        memberDict['med'].append(memEndDate)
        memberDict['rdate'].append(memRenewalDate)
        memberDict['Phone'].append(phoneStr)
        memberDict['Email'].append(emailStr)
        memberDict['Notes'].append('')
        
        counter += 1
        
    #Create CSV and add create header with key[]
    file = open(fname, 'w', newline='')
    writer = csv.writer(file, delimiter=',', quotechar='"')
    writer.writerow(key)
    
    writerCounter = 0
    while writerCounter < no:
        writeThis = []
        for k in memberDict:
            writeThis.append(memberDict[k][writerCounter])
        writer.writerow(writeThis)
        
        writerCounter += 1
    file.close()

# %% Generate a random date
def genRandDate(year, month, day, currentMember):
    '''
    Generate a random date starting from a given year, month, and day
    if false, return dayStr
    if true, return dayStr and renewalDate
    '''
    
    originDate = datetime.date(year,month,day)
    todayDateY = int(datetime.date.today().strftime("%Y"))
    todayDateM = int(datetime.date.today().strftime("%m"))
    todayDateD = int(datetime.date.today().strftime("%d"))
    todayDate = datetime.date(todayDateY, todayDateM, todayDateD)
    timeBetween1 = todayDate - originDate
    daysBetween1 = timeBetween1.days
    startDate = originDate + datetime.timedelta(days=random.randrange(daysBetween1))
    startStr = startDate.strftime("%B %d %Y")
    getRenewal = startDate + dateutil.relativedelta.relativedelta(years=5)
    renewalStr = getRenewal.strftime("%B %d %Y")
    timeBetween2 = todayDate - startDate
    daysBetween2 = timeBetween2.days
    endDate = startDate + datetime.timedelta(days=random.randrange(daysBetween2))
    endStr = endDate.strftime("%B %d %Y")
    
    if not currentMember:
        return startStr, endStr
    else:
        return startStr, renewalStr
    
# %% Generate a random person
def genRandPerson(tempDict):
    '''Generates a random first name, last name, and birthday'''
    
    #Generate random first and last names
    fname = names.get_first_name()
    lname = names.get_last_name()
    
    #Generate random birthdays
    birthDay, throwAwayValue = genRandDate(1904,2,11,False)
    
    #Check for duplicate member of the same first name, last name, and birthday
    #If there is a duplicate, genRandPerson()
    if (findDuplicate(tempDict, fname, lname, birthDay)):
        fname, lname, birthDay = genRandPerson(tempDict)
    
    return fname, lname, birthDay

# %% Find duplicate in memberDict[key] list
def findDuplicate(tempDict, firstName, lastName, DoB):
    '''
    Loop through memberDict[key] for any duplicates. 
    Return true for a duplicate
    Return false for original
    '''
    
    duplicateCheck = 0
    
    if (tempDict['Fn'].count(firstName) > 1): duplicateCheck += 1
    if (tempDict['Ln'].count(lastName) > 1): duplicateCheck += 1
    if (tempDict['DoB'].count(DoB) > 1): duplicateCheck += 1
    
    if duplicateCheck == 3: return True
    else: return False
    
# %% Generate email based on the NCSU email format
def generateNCSUEmail(tempDict, firstName, middleInitial, lastName, usedEmailCounter):
    '''
    Take the first letter of first name, middle initial, and last name
    up to 6 characters and create an @ncsu.edu email
    '''
    if usedEmailCounter == 0:
        emailStr = firstName[0].lower() + middleInitial.lower() + lastName.lower() + '@ncsu.edu'
        if tempDict['Email'].count(emailStr) > 1:
            usedEmailCounter += 1
            generateNCSUEmail(firstName, middleInitial, lastName, usedEmailCounter)
        else:
            return emailStr
    else:
        emailStr = firstName[0].lower() + middleInitial.lower() + lastName.lower() + '{}@ncsu.edu'.format(usedEmailCounter)
        if findDuplicate(memberDict['Email'], emailStr):
            usedEmailCounter += 1
            generateNCSUEmail(firstName, middleInitial, lastName, usedEmailCounter)
        else:
            return emailStr