import re

#check for matches with any existing command
#the value for this function can be taken out while parsing
def errorParsing(userInput, command, value, error, type):
    userInput=userInput[0:len(command)]
    if userInput[0]==command[0]: # to not get GRADE STUDENT AND STUDENTS GRADE confused
        setCommand="["+command+"]"
        #print(setCommand)#to make sure that the findall searches for chars and not the keyword
        matches = re.findall(setCommand, userInput)
        #print(matches)
        if len(matches) > (len(command)-error):
            if type==0:
                correctCommand = "Did you mean "+command +" "+ value + " ?(y/n): "
                check=input(correctCommand)
                if check=='y':
                    return True
                else:
                    return False
            return True
    return False