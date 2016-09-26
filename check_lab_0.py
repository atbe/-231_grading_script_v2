#!/usr/bin/env python3.4
from pathlib import Path
import argparse
from Student import Student
from Students import Students

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
    section = args["section"]
if args["project"] is not None:
    project = args["project"]
# Handin and section path objects, ye
printd("Args = ", args)
handin_path = Path(args["path"])
section_path = handin_path / "Section{:03d}".format(section)

# Create a students object and populate it with students
students = Students()
students.get_all_students_in_section(section_path)

def prompt_continue():
    cont = "oobla"
    while ((cont != "n") and (cont != "y")):
        cont = input("Would you like to continue? (Y,n): ").lower()
    return cont

# Check on project 0 completion
for student in students:
    try:
        student.run_project_py_file(0)
        cont = prompt_continue()
        if cont == 'n': break
    except IndexError as e:
        print(e, "moving on to next student.")
        continue
