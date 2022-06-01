import datetime
import string
import random
import os.path
import csv
import itertools

def gen_code_file(secretword:str, freq:int, maxlength:int):
    """Take user inputted secret word, frequency the secret word is shown,
    and how long the file length. The secret word will be randomly placed
    within the file given the frequency. Each line contains 250 characters"""
    
    if not type(secretword) is str or not type(freq) is int or not type(maxlength) is int:
        print("Improper input")
        return -1
    
    #Generate file path
    dateStr = datetime.date.today().strftime("%m%d%y")
    timeStr = datetime.datetime.now().time().strftime("%H%M")
    filePath = 'random_letters_new_{0}_{1}.txt'.format(dateStr, timeStr)
    
    #Open file and write maxlength of random ascii letters
    with open(filePath, 'w') as file:
        i = 1
        while i < maxlength + 1:
            randLet = random.choice(string.ascii_letters)
            if i%250 == 0 and i != 0:
                file.write(randLet)
                file.write("\n")
            else:
                file.write(randLet)
            i += 1
    file.close()
    
    #Generate random number within maxlength and length of secretword
    #Store file string and secret word into list
    #Replace characters starting from randNum
    #Write back to file
    listUsedNum = []
    randNum = random.randint(0, maxlength - len(secretword) - 10)
    secretDateStr = datetime.date.today().strftime("%m-%d-%Y")
    secretList1 = list(secretword + "{0}".format(secretDateStr))
    secretList2 = list(secretword)
    j = 0
    i = 0
    while i < freq:
        file = open(filePath, 'r')
        fileStr = file.read()
        tempStrList = list(fileStr)


        #First occurence will have secretword + date
        #else, print secretword
        if i == 0:
            while j < len(secretList1):
                tempStrList[randNum + j] = secretList1[j] 
                listUsedNum.append(randNum + j)
                j += 1
        else:
            while j < len(secretList2):
                tempStrList[randNum + j] = secretList2[j]
                listUsedNum.append(randNum + j)
                j += 1
               
        #Account for space in front of secret word
        j = 0
        while j < len(secretList1):
                if (randNum + j - len(secretList1) - 1) >= -1:
                    listUsedNum.append(randNum + j - len(secretList1))
                j += 1
                
        j = 0
        #Make sure secretword doesn't overlap each other
        randNum = random.choice([k for k in range(0, maxlength - len(secretword) - 10) if k not in listUsedNum])
        fileStr = "".join(tempStrList)
        file.close()
        
        file = open(filePath, 'w')
        file.write(fileStr)
        file.close()
        i += 1
        
    findWord(filePath, secretword)
        
def findWord(filename:str, word:str):
    """Opens a text file and finds the first index of a given word. Store every
    the index of every instance of the word in a list and returns that list.
    Checks if the file exists or not. Returns -1 if file doesn't exist"""
    
    #Check if variables are non strings
    if not type(filename) is str or not type(word) is str:
        print("Filename or word is a non-string")
        return -1
    
    if os.path.isfile(filename):
        file = open(filename, 'r')
        fileStrList = list(file.read())
        
        i = 0
        indexList = []
        wordList = []
        counter = 0
        for x in word:
            wordList[counter] = wordList.append(None)
            counter += 1
        while i < len(fileStrList):
            j = 0
            while j < len(wordList) - 1:
                wordList[j] = wordList[j + 1]
                j += 1
            wordList[len(word) - 1] = fileStrList[i]
            compStr = ''.join(map(str,wordList))
            if compStr == word:
                indexList.append(i - (len(word)-2))
            i += 1
        print(indexList)
    else:
        print("File doesn't exist >:(")
        return -1
    
def dataSorter(filename:str):
    """Reads a 2 x n csv file with categories and values then organizes the
    data by category. Saves to a file called sorteddata.csv in your current
    directory."""
    
    dict = {}
    
    #Check if input is a string
    if not type(filename) is str:
        print("Input is non string")
        return -1
    
    #Check to see if file exists
    if not os.path.isfile(filename):
        print("File doesn't exist >:(")
        return -1
    else:
        #Open csv, create keys, and append to keys
        with open(filename, 'r') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',')
            next(csvreader)
            headers = []
            
            #Populate Dictionary of lists
            for row in csvreader:
                category = row[0]
                value = row[1]
                if not category in dict:
                    dict.update({category: []})
                    if not value in dict[category]:                        
                        if value.isnumeric():
                            dict[category].append(value)
                        else:
                            dict[category].append(value)
                    headers.append(category)
                else:
                    if not value in dict[category]:
                        if value.isnumeric():
                            dict[category].append(value)
                        else:
                            dict[category].append(value)
              
            #Store dictionary data into a horizontal table then transpose
            horizontalTable = []
            dataList = []
            for header in sorted(headers):
                if dict[header][0].isnumeric():
                    counter = 0
                    for dictString in dict[header]:
                        dict[header][counter] = int(dictString)
                        counter += 1
                    dataList = sorted(dict[header])
                    dataList.insert(0, header)
                    horizontalTable.append(dataList)
                elif isFloat(dict[header][0]):
                    counter = 0
                    for dictString in dict[header]:
                        dict[header][counter] = int(dictString)
                        counter += 1
                    dataList = sorted(dict[header])
                    dataList.insert(0, header)
                    horizontalTable.append(dataList)
                else:
                    dataList = sorted(dict[header])
                    dataList.insert(0, header)
                    horizontalTable.append(dataList)           
            verticalTable = list(map(list, itertools.zip_longest(*horizontalTable, fillvalue=None)))
            
        #Create csv file and write keys as headers and their respective values
        with open('sorteddata.csv', 'w', newline='') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"')
            writer.writerows(verticalTable)
            file.close()
        
def dataRecorder(filename:str, record:dict):
    if not os.path.isfile(filename):
        file = open(filename, 'w', newline='')
        writer = csv.writer(file, delimiter=',', quotechar='"')
        
        headers = ['Name', 'Weight (lbs)', 'Height (ft)']
        writer.writerow(headers)
    else:
        file = open(filename, 'a', newline='')
        writer = csv.writer(file, delimiter=',', quotechar='"')
          
    writeThis = []
    for key in record:
        writeThis.append(record[key])
    writer.writerow(writeThis)
    file.close
    
def isFloat(num):
    """Check if string is a float"""
    try:
        float(num)
        return True
    except ValueError:
        return False
    
dataSorter("E:/Documents/College/NCSU/ECE492/Homework2_Text_Files/answer.csv")