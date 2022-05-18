pyramidInput = input("Enter string for message pyramid: ")

def pyramid(s):
    '''Takes a user input and creates a pyramid pattern of the letters
    in the string'''
    
    strList = []
    for i in range(1,len(s)+1):
        strList.append(s[:i])
    print("\n".join(strList))
    
pyramid(pyramidInput)