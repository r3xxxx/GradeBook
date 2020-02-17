import re

#error handling for parsing and checking user input

#user input
userInput=input("Type in a command: ")


#check for matches with any existing command
#the value for this function can be taken out while parsing
def errorParsing(userInput, command, value):
    userInput=userInput[0:len(command)]
    if userInput[0]==command[0]: # to not get GRADE STUDENT AND STUDENTS GRADE confused
        setCommand="["+command+"]"
        print(setCommand)#to make sure that the findall searches for chars and not the keyword
        matches = re.findall(setCommand, userInput)
        print(matches)
        if len(matches) > len(command)/4:
            correctCommand = "Did you mean "+command +" "+ value + " ?(y/n): "
            check=input(correctCommand)
            if check=='y':
                return True
    return False

errorParsing(userInput, "STUDENTS GRADE", "RAHAVEE")