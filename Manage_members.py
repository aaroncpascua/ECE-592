from gen_member_data import *

def Manage_members():
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
        addNewMember()
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
def addNewMember():
    firstName = inputFirstName()
    middleInitial = inputMiddleIniital()
    lastName = inputLastName()
    dateOfBirth = inputBirthday()
    address = inputAddress()
    status = inputStatus()
    

Manage_members()