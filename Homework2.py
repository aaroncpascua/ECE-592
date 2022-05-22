import datetime
import string
import random

def gen_code_file(secretword:str, freq:int, maxlength:int):
    """Take user inputted secret word, frequency the secret word is shown,
    and how long the file length. The secret word will be randomly placed
    within the file given the frequency. Each line contains 250 characters"""
    
    #Generate file path
    dateStr = datetime.date.today().strftime("%m%d%y")
    timeStr = datetime.datetime.now().time().strftime("%H%M")
    filePath = 'E:/Documents/College/NCSU/ECE492/Homework2_Text_Files/random_letters_{0}_{1}.txt'.format(dateStr, timeStr)
    
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
    j = 0
    i = 0
    while i < freq:
        file = open(filePath, 'r')
        fileStr = file.read()
        tempStrList = list(fileStr)
        secretDateStr = datetime.date.today().strftime("%m-%d-%y")
        secretList1 = list(secretword + "{0}".format(secretDateStr))
        secretList2 = list(secretword)

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
                
        j = 0
        randNum = random.choice([k for k in range(0, maxlength - len(secretword) - 10) if k not in listUsedNum])
        fileStr = "".join(tempStrList)
        file.close()
        
        file = open(filePath, 'w')
        file.write(fileStr)
        file.close()
        i += 1