import csv
import sqlite3

# Create the database
connection = sqlite3.connect('/Users/rexgodbout/PycharmProjects/GradeBook/gradebook.db')
cursor = connection.cursor()

# Create the table
cursor.execute('DROP TABLE IF EXISTS students')
cursor.execute('CREATE TABLE Students (studentId INTEGER NOT NULL, gradeCourse INTEGER NOT NULL, courseName TEXT NOT NULL, className TEXT NOT NULL)')
cursor.execute('DROP TABLE IF EXISTS courses')
cursor.execute('CREATE TABLE Courses (courseId INTEGER NOT NULL, teacherName TEXT NOT NULL, courseName TEXT NOT NULL)')
connection.commit()

# Load the CSV file into CSV reader
csvfile = open('Students.csv', 'r')
creader = csv.reader(csvfile, delimiter=',', quotechar='|')

csvfile2 = open('courses.csv', 'r')
creader2 = csv.reader(csvfile2, delimiter=',', quotechar='|')

for s in creader:
    cursor.execute('INSERT INTO  students VALUES (?,?,?,?)', s)


for c in creader2:
    cursor.execute('INSERT INTO  courses VALUES (?,?,?)', c)

# Close the csv file, commit changes, and close the connection
csvfile.close()
csvfile2.close()
connection.commit()
connection.close()
