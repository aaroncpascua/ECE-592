import names
import random
import datetime
import dateutil
import csv

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
        first_name, last_name, birthDay = genRandPerson()

        #Generate random Membership Status from status[]
        memStatus = random.choice(status)
        
        #Generate random Membership Start Date and Renewal Date starting from Dec 1 1980
        #If member status is None, Renewal Date is blank
        if (memStatus != 'None'):
            memStartDate, memRenewalDate = genRandDate(1980,12,1,True)
        else:
            memStartDate, memRenewalDate = genRandDate(1980,12,1,True)
            memRenewalDate = ''
        
        #Generate random 10 digit phone number
        phoneStr = str(random.randint(1000000000,9999999999))
        
        #Add values to dictionary
        memberDict['Mno'].append(memNumStr)
        memberDict['Fn'].append(first_name)
        memberDict['MI'].append('')
        memberDict['Ln'].append(last_name)
        memberDict['DoB'].append(birthDay)
        memberDict['Address'].append('')
        memberDict['Status'].append(memStatus)
        memberDict['msd'].append(memStartDate)
        memberDict['med'].append('')
        memberDict['rdate'].append(memRenewalDate)
        memberDict['Phone'].append(phoneStr)
        memberDict['Email'].append('')
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
def genRandDate(year, month, day, needRenewal):
    '''
    Generate a random date starting from a given year, month, and day
    if false, return dayStr
    if true, return dayStr and renewalDate
    '''
    
    startDate = datetime.date(year,month,day)
    endDateY = int(datetime.date.today().strftime("%Y"))
    endDateM = int(datetime.date.today().strftime("%m"))
    endDateD = int(datetime.date.today().strftime("%d"))
    endDate = datetime.date(endDateY, endDateM, endDateD)
    timeBetween = endDate - startDate
    daysBetween = timeBetween.days
    getDay = startDate + datetime.timedelta(days=random.randrange(daysBetween))
    getRenewal = getDay + dateutil.relativedelta.relativedelta(years=5)
    dayStr = getDay.strftime("%B %d %Y")
    renewalStr = getRenewal.strftime("%B %d %Y")
    
    if not needRenewal:
        return dayStr
    else:
        return dayStr, renewalStr
    
# %% Generate a random person
def genRandPerson():
    '''Generates a random first name, last name, and birthday'''
    
    #Generate random first and last names
    fname = names.get_first_name()
    lname = names.get_last_name()
    
    #Generate random birthdays
    birthDay = genRandDate(1904,2,11,False)
    
    #Check for duplicate member of the same first name, last name, and birthday
    #If there is a duplicate, genRandPerson()
    if (findDuplicate(memberDict['Fn'], fname) and findDuplicate(memberDict['Ln'], lname) and findDuplicate(memberDict['DoB'], birthDay)):
        fname, lname, birthDay = genRandPerson()
    
    return fname, lname, birthDay

# %% Find duplicate in memberDict[key] list
def findDuplicate(valueList, value):
    '''Loop through memberDict[key] for any duplicates'''
    
    if (valueList.count(value) > 1): return True
    else: return False

# %% Test Function
gen_member_data()