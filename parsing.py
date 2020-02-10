request = 'Continue'
while request != 'quit':

    # Get user request
    request = input().lower()

    # Break user request into individual terms
    rTerms = request.split()

    invalid = True

    if request == 'quit':
        break
        
    if rTerms[0] == 'students':
        if len(rTerms) >= 2:
            validTerms = ['grades', 'course', 'passing']
            # is the second term of the request valid?
            for term in validTerms:
                if term == rTerms[1]:
                    invalid = False
            if invalid:
                print("Missing 'grades'/'course'/'passing' after 'students' : ")

            # if valid and there's at least three terms of the request
            if not invalid:
                if len(rTerms) >= 3:
                    # 'students grades ...'
                    if rTerms[1] == 'grades':
                        print('SELECT * from StudentTable WHERE grade ==', rTerms[2])
                    # 'students course ...'
                    elif rTerms[1] == 'course':
                        print('SELECT * from StudentTable WHERE course ==', rTerms[2])
                    # 'students passing ...'
                    elif rTerms[1] == 'passing':
                        print('SELECT * from StudentTable WHERE grade > 60 AND course =', rTerms[2])
                else:
                    print("Missing grade or course number.")
        else:
            print("Request too short. Type 'help' for available options.")

    else:
        print('Invalid request.')


