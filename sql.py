import csv
import sqlite3
import re
import Parse as p
import itertools



open_db = False

def load_database():

    global cursor, connection, open_db
    if open_db == False:
# Create the database
        connection = sqlite3.connect('/Users/rexgodbout/PycharmProjects/GradeBook/gradebook.db')
        cursor = connection.cursor()
    open_db = True
    # Create the table

    cursor.execute('DROP TABLE IF EXISTS students')
    cursor.execute(
        'CREATE TABLE Students (studentId INTEGER NOT NULL, studentName TEXT NOT NULL, gradeCourse INTEGER NOT NULL, courseName TEXT NOT NULL)')
    cursor.execute('DROP TABLE IF EXISTS courses')
    cursor.execute('CREATE TABLE Courses (courseId INTEGER NOT NULL, teacherName TEXT NOT NULL, courseName TEXT NOT NULL)')
    connection.commit()

    # Load the CSV file into CSV reader
    csvfile = open('students.csv', 'r')
    creader = csv.reader(csvfile, delimiter=',', quotechar='|')

    csvfile2 = open('courses.csv', 'r')
    creader2 = csv.reader(csvfile2, delimiter=',', quotechar='|')

    for s in creader:
        cursor.execute('INSERT INTO Students VALUES (?,?,?,?)', s)

    for c in creader2:
        cursor.execute('INSERT INTO Courses VALUES (?,?,?)', c)

    # Close the csv file, commit changes, and close the connection
    csvfile.close()
    csvfile2.close()
    connection.commit()


def sql_query_execute(query):
    global cursor, open_db, connection
    if open_db == False:
        open_db = True
        connection = sqlite3.connect('/Users/rexgodbout/PycharmProjects/GradeBook/gradebook.db')
        cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    rows = cursor.fetchall()

    if len(rows) == 0:
        print("No data for query")
    print(str(rows).replace("('", "").replace("',)", "\n").replace(",", "").replace("[", "").replace("]", ""))



# help message for all user commands (*to be filled in)


# help message for all user commands (*to be filled in)
def help_msg():
   print("Try entering one of the following commands:"
          "\n~ students grades *grade value*"
          "\n~ students course *course*"
          "\n~ students passing *course*"
          "\n~ grade student *name*"
          "\n~ grade student *id number*"
          "\n~ professor course *course*"
          "\n~ professor student *student name*"
          "\n~ course student *student name*"
          "\n~ professor classes *professor name*")


# message function for short request
def short_req():
    print("Request too short. Type 'help' for available options.")


# message function for invalid name input
def valid_name():
    print('Enter a valid first and last name')


# message function for invalid course name input
def view_courses():
    courses = ['cs205', 'cs201', 'cs275', 'cs110', 'cs21', 'cs292']
    print("Here is a list of available courses:")
    print(courses)
request = 'Continue'
while request != 'quit':

    # Get user request
    request = input().lower()

    # Break user request into individual terms
    rTerms = request.split()

    invalid = True

    if request == 'quit':
        break

    # valid courses in database
    if request == 'load':
        loaded = True
        load_database()
        print("load successsful")
    courses = ['cs205', 'cs201', 'cs275', 'cs110', 'cs21', 'cs292','cs124','cs120','cs167','cs222','cs225','cs224','cs166','cs121','cs64','cs254','cs202','cs142','cs148','cs006','cs008']

    # --- queries for obtaining all students with a specific grade, taking a specified course, or is passing a course --
    # example query structure below:
    '''
    >STUDENTS GRADES *GRADE VALUE*
    SELECT grades FROM Students WHERE grade >= 'INPUT'
    >STUDENTS COURSE *COURSE*
    >STUDENTS PASSING *COURSE*
    '''
    if rTerms[0] == 'students' or p.errorParsing(rTerms[0],'students','default',2,1):
        if len(rTerms) >= 2:


                if len(rTerms) >= 3:
                    # 'students grades ...'
                    if rTerms[0]+rTerms[1] == 'studentsgrades' or p.errorParsing(request,"students grades",rTerms[2],2,0):
                        try:
                            num = int(rTerms[2])
                            if 0 <= num <= 100:

                                query_param = "SELECT studentName from Students WHERE gradeCourse = " + str(num)
                                sql_query_execute(query_param)

                            else:
                                print('Grade must be between 0 and 100')
                        except ValueError:
                            print('Grade must be an integer value')
                    # obtain all students taking a particular course
                    elif rTerms[0]+rTerms[1] == 'studentscourse' or p.errorParsing(request,"students course",rTerms[2],3,0):
                        if rTerms[2] in courses:  # check if course is valid
                            query_param = "SELECT studentName from Students WHERE courseName ='" + str(rTerms[2] + "'")
                            sql_query_execute(query_param)
                        else:
                            view_courses()
                    # returns students passing a particular course
                    elif rTerms[0]+rTerms[1] == 'studentspassing' or p.errorParsing(request,"students passing",rTerms[2],3,0):
                        if rTerms[2] in courses:
                            query_param = "SELECT studentName from Students WHERE gradeCourse >= 30 AND courseName ='" + str(rTerms[2] + "'")
                            sql_query_execute(query_param)
                        else:
                            view_courses()
                else:
                    print("Missing grade or course number.")  # if only two valid terms in user request
        else:
            short_req()

        # ------------- requesting individual grades by name or student ID -----------------
        # example query structure below:
        '''
        >GRADE STUDENT *NAME*
        >GRADE STUDENT *ID NUMBER*
        '''
    elif rTerms[0] == 'grade' or p.errorParsing(rTerms[0], "grade", "default", 1, 1):
        if len(rTerms) >= 2:
            if rTerms[0]+rTerms[1] == 'gradestudent' or p.errorParsing(request,"grade student",rTerms[2],2,0):
                if len(rTerms) >= 3:
                    try:  # try to convert input to integer for student ID
                        studentID = int(rTerms[2])
                        query_param = "SELECT gradeCourse from Students WHERE studentID= " + str(studentID)
                        sql_query_execute(query_param)
                    except ValueError:  # ValueError, so input must be string (for name)
                        try:
                            studentName = rTerms[2] + ' ' + rTerms[3]
                            query_param = "SELECT gradeCourse from Students WHERE studentName= '" + str(studentName + "'")
                            sql_query_execute(query_param)
                        except IndexError:
                            valid_name()

            else:
                print("Missing 'student' after 'grade'")  # prompt if user has invalid second term
        else:
            short_req()

    # help command
    elif rTerms[0] == 'help':
        help_msg()

        # ------ queries for professor names by entering either course name or student name ------
        # example query structure below:
        '''
        > PROFESSOR COURSE *COURSE*
        > PROFESSOR STUDENT *NAME*
        '''
    elif rTerms[0] == 'professor' or p.errorParsing(rTerms[0], "professor", "default", 2, 1):
        if len(rTerms) >= 2:
            if rTerms[0]+rTerms[1] == 'professorcourse' or p.errorParsing(request,"professor course",rTerms[2],1,0):   # obtain professors who teach a particular course
                if len(rTerms) == 3:
                    if rTerms[2] in courses:  # is the course name the user entered valid?

                        query_param = "SELECT teacherName from Courses WHERE courseName= '" + str(rTerms[2] + "'")
                        sql_query_execute(query_param)
                    else:
                        view_courses()
                else:
                    print('Missing course number')  # if only two valid terms in request
            elif rTerms[1] == 'classes':  # get all courses taught by desired professor
                if len(rTerms) == 3:
                    print('Enter a valid first and last name for a professor')
                else:
                    try:
                        name = rTerms[2] + ' ' + rTerms[3]
                        query_param = "SELECT courseName from Courses WHERE teacherName= '" + str(name + "'")
                        sql_query_execute(query_param)

                    except IndexError:
                        print('Missing first or last name of professor')

            elif rTerms[0]+rTerms[1] == 'professorstudent' or p.errorParsing(request,"professor student",rTerms[2],1,0):
                try:
                    name = rTerms[2] + ' ' + rTerms[3]

                    if open_db == False:
                        open_db = True
                        connection = sqlite3.connect('/Users/rexgodbout/PycharmProjects/GradeBook/gradebook.db')
                        cursor = connection.cursor()
                    cursor.execute("SELECT courseName from Students WHERE studentName = '" + str(name + "'"))
                    courseName = cursor.fetchall()
                    connection.commit()
                    courseFinal = list(itertools.chain(*courseName))

                    #print(courseFinal[0])
                    query_param = "SELECT teacherName from Courses WHERE courseName= '" + str(courseFinal[0]) + "'"
                    sql_query_execute(query_param)

                except IndexError:
                    valid_name()

        else:
            short_req()  # user request too short

        # query the course name the student is enrolled in
        # example query structure below:
        '''
        >COURSE STUDENT *NAME*
        '''


    elif rTerms[0] == 'course' or p.errorParsing(rTerms[0], "course", "default", 2, 1):
        if len(rTerms) >= 2:
            if rTerms[0]+rTerms[1] == 'coursestudent' or p.errorParsing(request,"course student",rTerms[2],2,0):
                try:  # see if valid name can be extracted from user input
                    name = rTerms[2] + ' ' + rTerms[3]

                    query_param = "SELECT courseName from Students WHERE studentName = '" + str(name + "'")
                    sql_query_execute(query_param)
                except IndexError:
                    valid_name()  # prompt user to enter valid name if request is too short


        else:
            short_req()  # issue message if request is too short
    else:
        print("Type 'help' to view more available options for more options.")


connection.commit()
connection.close()