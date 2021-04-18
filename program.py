import glob
import os
import os.path
from os import path
import requests
import json
import csv
import sys
import argparse
from collections import defaultdict

if 'API_KEY' in os.environ:
    # Gets authorization key from OS.ENVIORMENT. This has to be set in the command prompt. 
    header = {'Authorization': 'Bearer ' + os.environ['API_KEY']}


    # Get grades function, with course ID as a parameter. 
    def getGrades(courseID):
        # GET METHOD to retreive JSON data of course enrollment. 
        response = requests.get("https://sjsu.instructure.com/api/v1/courses/" + courseID+ "/enrollments", headers = header)
        json_data = json.loads(response.text)
    
        # Loop the data to find user that are students and output their COURSE ID, GRADE, STUDNET ID, NAME, AND GRADE. 
        try:
            with open ('student_grades.csv', 'w', newline='') as f:
                fieldnames = ['course_id', 'date','student_id', 'name','final_grade' ]
                write_stuff = csv.DictWriter(f, fieldnames=fieldnames)
                write_stuff.writeheader()
                for grade in json_data:
                    if grade['role'] == "StudentEnrollment":
                        write_stuff.writerow({'course_id': grade['course_id'], 'date': grade['created_at'], 'student_id': grade['user']['sis_user_id'], 'name': grade['user']['name'], 'final_grade': grade['grades']['final_score']}) 
                print("A .csv file called student_grades.csv was generated to display a list of student's grades.")
        except:
            print(json_data)



    def enrollStudents(courseID, csv_file):
        
        if str(path.exists("student_information.csv")) == "True":

            columns = defaultdict(list) # each value in each column is appended to a list
            with open(csv_file,'r') as csv_file:
                reader = csv.DictReader(csv_file) # read rows into a dictionary format
                for row in reader: # read a row as {column1: value1, column2: value2,...}
                    for (k,v) in row.items(): # go over each column name and value 
                        columns[k].append(v) # append the value into the appropriate list

                student_id_number = columns['sis_user_id']

                count = 0
                enrolled_count = 0 
                for stuff in student_id_number:
                    body = {
                    "enrollment[user_id]" : "sis_user_id:" + str(stuff),
                    "enrollment[type]":"StudentEnrollment",
                    "enrollment[enrollment_state]": "active",
                    "enrollment[notify]" : True
                    }

                    enroll_students = requests.post('https://sjsu.instructure.com/api/v1/courses/' + courseID+ '/enrollments', headers = header, data=body)    

                    json_data = json.loads(enroll_students.text)

                    for x in json_data:
                        if x == "errors":
                            count += 1

                    enrolled_count = count - enrolled_count

                response = requests.get("https://sjsu.instructure.com/api/v1/courses/" + courseID+ "/enrollments", headers = header)

                response_data = json.loads(response.text)

                response_id = []
                for x in response_data:
                    response_id.append(x['user']['sis_user_id'])
                
                set1 = set(student_id_number)
                set2 = set(response_id)

                unmatched = set1 - set2
                unmatched_list = list(unmatched)
                matched = set1.intersection(set2)


                print("Students who were enrolled: ")
                print(matched)
                print(str(enrolled_count) + " were enrolled.")
                print("-----------------------------------------------------------")
                print("Students who were not enrolled: ")
                print(unmatched)
                print(str(len(unmatched_list)) + " failed to enroll.")
                print('-----------------------------------------------------------')
                print('A .csv file called student_not_enrolled.csv was generated to display sis_user_id who failed to enroll.')

            
            # Create .csv file with list of students that failed to enroll.    
            with open ('student_not_enrolled.csv', 'w', newline='') as f:
                fieldnames = ['sis_user_id']
                write_stuff = csv.DictWriter(f, fieldnames=fieldnames)
                write_stuff.writeheader()
                for y in unmatched_list:
                    write_stuff.writerow({'sis_user_id': y})
            
        else:
            print("The name of the .csv file is incorrect. Please enter the correct file: student_information.csv")


    def main():
        # Reads the text that is typed in the command-line prompt 
        try:
            parser = argparse.ArgumentParser()
            parser.add_argument("-r", "--courseID", help="ENTER COURSE-ID(7-digits) e.g. -r 1234567 (Course ID for getGrades)", dest="courseID", type=str, required=False)
            parser.add_argument("-d", "--courseID2", help="ENTER COURSE-ID(7-digits) e.g. -d 1234567 (Course ID for enrollStudents)", type=str, required=False)
            parser.add_argument("-f", "--csv_file", help="ENTER CSV_FILE. Name of file must be student_information.csv.", dest="csvfile", type=str, required=False)

            args = parser.parse_args()

            if args.courseID:
                getGrades(args.courseID)
            elif args.courseID2 and args.csvfile:
                enrollStudents(args.courseID2, args.csvfile)
        except:
            print('---------------------------------')
            print('INSTRUCTIONS: ')
            print('---------------------------------')
            print('Getting student grades: \n' +
            'ENTER: -r course_id_number (e.g. -r 1234567) \n' +
            '--------------------------------- \n' +
            'Enrolling students from csv_file: \n' +
            'ENTER: -d course_id_number -f csv_file (e.g. -d 1234567 -f student_information.csv) \n' +
            'csv_file MUST be named: student_information.csv')

            print('---------------------------------')
            sys.exit(0)


    if __name__ == "__main__":
        main()
else:
    print("Please set the environmental variable. e.g. API_KEY=authorization_key")





    

    
        