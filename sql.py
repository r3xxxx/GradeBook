import csv
import sqlite3
import re
import itertools


# Create the database
connection = sqlite3.connect('/Users/rexgodbout/PycharmProjects/GradeBook/gradebook.db')
cursor = connection.cursor()

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







def load_database():


# Create the database
    connection = sqlite3.connect('/Users/rexgodbout/PycharmProjects/GradeBook/gradebook.db')
    cursor = connection.cursor()

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
    connection.close()

def sql_query_execute(query):
    cursor.execute(query)
    rows = cursor.fetchall()

    if len(rows) == 0:
        print("No data for query")
    print(str(rows).replace("('", "").replace("',)", "\n").replace(",", "").replace("[", "").replace("]", ""))



# help message for all user commands (*to be filled in)
def help_msg():
    print('Valid courses: CS201, CS205, CS201, CS275, CS110, CS21, & CS292')


# message function for short request
def short_req():
    print("Request too short. Type 'help' for available options.")


# message function for invalid name input
def valid_name():
    print('Enter a valid first and last name')


# message function for invalid course name input
def view_courses():
    print("Type 'help' to view available courses")


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
        load_database()
        print("load successsful")
    courses = ['cs205', 'cs201', 'cs275', 'cs110', 'cs21', 'cs292']

    # --- queries for obtaining all students with a specific grade, taking a specified course, or is passing a course --
    # example query structure below:
    '''
    >STUDENTS GRADES *GRADE VALUE*
    SELECT grades FROM Students WHERE grade >= 'INPUT'
    >STUDENTS COURSE *COURSE*
    >STUDENTS PASSING *COURSE*
    '''
    if rTerms[0] == 'students':
        if len(rTerms) >= 2:
            # next valid terms
            validTerms = ['grades', 'course', 'passing']
            # is the second term of the request valid?
            for term in validTerms:
                if term == rTerms[1]:
                    invalid = False
            if invalid:
                print("Missing 'grades'/'course'/'passing' after 'students'")

            # if valid and there's at least three terms of the request
            if not invalid:
                if len(rTerms) >= 3:
                    # 'students grades ...'
                    if rTerms[1] == 'grades':
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
                    elif rTerms[1] == 'course':
                        if rTerms[2] in courses:  # check if course is valid
                            query_param = "SELECT studentName from Students WHERE courseName ='" + str(rTerms[2] + "'")
                            sql_query_execute(query_param)
                        else:
                            view_courses()
                    # returns students passing a particular course
                    elif rTerms[1] == 'passing':
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
    elif rTerms[0] == 'grade':
        if len(rTerms) >= 2:
            if rTerms[1] == 'student':
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
                    print('Missing student ID or name')  # prompt user to enter name or ID
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
    elif rTerms[0] == 'professor':
        if len(rTerms) >= 2:
            if rTerms[1] == 'course':  # obtain professors who teach a particular course
                if len(rTerms) == 3:
                    if rTerms[2] in courses:  # is the course name the user entered valid?

                        query_param = "SELECT teacherName from Courses WHERE courseName= '" + str(rTerms[2] + "'")
                        sql_query_execute(query_param)
                    else:
                        view_courses()
                else:
                    print('Missing course number')  # if only two valid terms in request
            elif rTerms[1] == 'student':
                try:
                    name = rTerms[2] + ' ' + rTerms[3]
                    cursor.execute("SELECT courseName from Students WHERE studentName = '" + str(name + "'"))
                    courseName = cursor.fetchall()
                    courseFinal = list(itertools.chain(*courseName))

                    print(courseFinal[0])
                    query_param = "SELECT teacherName from Courses WHERE courseName= '" + str(courseFinal[0]) + "'"
                    sql_query_execute(query_param)

                except IndexError:
                    valid_name()
            else:
                print("Did you mean 'course'/'student' after 'professor'?")  # if second term is not 'course' or
                # 'student'
        else:
            short_req()  # user request too short

        # query the course name the student is enrolled in
        # example query structure below:
        '''
        >COURSE STUDENT *NAME*
        '''

    elif rTerms[0] == 'course':
        if len(rTerms) >= 2:
            if rTerms[1] == 'student':
                try:  # see if valid name can be extracted from user input
                    name = rTerms[2] + ' ' + rTerms[3]

                    query_param = "SELECT courseName from Students WHERE studentName = '" + str(name + "'")
                    sql_query_execute(query_param)
                except IndexError:
                    valid_name()  # prompt user to enter valid name if request is too short
            else:
                print("Did you mean to type 'student' after 'course'?")  # if second request term is invalid

        else:
            short_req()  # issue message if request is too short
    else:
        print("Invalid request. Type 'help' for available options.")


connection.commit()
connection.close()