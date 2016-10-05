#!/usr/bin/env python3.4
from pathlib import Path
import argparse
from Section import Section
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
    section_number = args["section"]
if args["project"] is not None:
    project_number = args["project"]
# Handin and section path objects, ye
printd("Args = ", args)
handin_path = Path(args["path"])

# Create Section object
section_path = handin_path / "Section{:03d}".format(section_number)
section = Section(section_path, section_number)

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
        # student.run_project_py_file(project_number)
        student.open_files(project_number)

        cont = prompt_continue()
        if cont == 'n': break
    except IndexError as e:
        print(e, "moving on to next student.")
        continue

def printMenu(options,menuName):
    print("\nChoose from the options below: [{}]\n".format(menuName))
    counter = 1
    for option in options:
        line = "    {}.....{}".format(counter,option)
        print(line)
        counter += 1
    print("\n    X.....Quit {}".format(menuName))
    options = [option.lower().strip() for option in options]
    choice_nums = [str(num) for num in range(1, len(options) + 1)]
    choice_nums.append("x")
    choice = input("\nWhat is your selection?: ").lower()
    while (choice not in choice_nums):
        print("Not a valid option. Please try again.")
        choice = input("\nWhat is your selection?: ").lower()
    return choice


grading_options = ["Grade all students in your Section", "Grade ungraded projects", "Grade one student"]
option = printMenu(grading_options, "231 Grading Script Main Menu")
if option == "x":
    print("c ya later")
elif option == "1":
    print("Grading all students in section {}".format(section))
