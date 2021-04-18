# Getting student's grade and enrolling students Program
## Installation:
Drag and store all necessary files into __one single folder.__\
__Necessary Files:__
- The python Program
- The .csv file with list of students. __(Must be named student_information.csv)__

Use the package manager to install the nescessary packages and libaries for usage.

```bash
pip install glob
pip install request
pip install json
pip install csv
pip instal sys
pip install arsparse
pip install collections
```
## Usage
__Setting everything up__
1. Open up command-prompt
2. Set enviormental variable in command-prompt __SET API_KEY=AUTHORIZATION KEY__ (No space after equal)
3. Set the path to the folder where everything is stored. __cd FILEPATH__

__Help Menu__
- After finishing the initial set-up type __python program_name -h__ to open a help menu that displays __additional instructions__ and a __list of arguments__ that are used.


__Getting a list of student's grade__
1. Input in the command-line __python program_name -r course_id_number__ to generate a .csv called __student_grades.csv__ that will include everybody's name and final_grade.

__Enrolling students from your csv_file__
1. __REMEMBER__ to change your __csv_file__ name to __student_information.csv__ or the program will __FAIL TO RUN__
2. Input in the command-line __python program_name -d course_id_number -f csv_file__ to enroll students into the course.
3. A __.csv file__ called __student_not_enrolled.csv__ will be generated listing the __student ids that failed to enroll.__
