#!/usr/bin/env python3.4
from pathlib import Path
import argparse
from Section import Section
from Student import Student
from Students import Students
from Tools import print_menu

DEBUG = True

def printd(*says):
    if DEBUG:
        for saying in says:
            print(saying, " ", end="")
        print()

parser = argparse.ArgumentParser(description="Help with lab 0 grading. poc.")
parser.add_argument("section", help="Section to grade.", type=int)
parser.add_argument("project", help="Project to grade.", type=int)
parser.add_argument("-path", "-p", help="Path to Handin root.", default="/user/cse231/Handin/", type=str)
args = vars(parser.parse_args())

if args["section"] is not None:
    section_number = args["section"]
if args["project"] is not None:
    project_number = args["project"]
else:
    project_number = None

# Handin and section path objects, ye
printd("Args = ", args)
handin_path = Path(args["path"])

# Create Section object
section_path = handin_path / "Section{:03d}".format(section_number)

# Create a students object and populate it with students
students = Students()
students.get_all_students_in_section(section_path)

grading_options = ["Grade all students in your Section", "Grade ungraded projects", "Grade one student"]
option = "bangbang"
while option != "x":
    option = print_menu(grading_options, "231 Grading Script")
    if option == "1":
        students.grade_all_students(project_number)
    elif option == "2":
        students.grade_all_students(project_number, skip_graded=True)
    elif option == "3":
        # TODO: Implement single grading
        0
print("c ya later")
