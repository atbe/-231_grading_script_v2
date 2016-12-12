#!/usr/bin/env python3.4

from pathlib import Path
import argparse
from Student import Student
from Students import Students
from Tools import print_menu
import os
import sys
import pickle
import time
import pprint
import operator

DEBUG = True

def printd(*says):
    if DEBUG:
        for saying in says:
            print(saying, " ", end="")
        print()

# Check if we are even on the CSE Server
if not Path("/user/cse231/Handin").exists() and not DEBUG:
    print("You are not on the CSE server.\nUse -p option or run this program on the CSE server.")
    sys.exit()

parser = argparse.ArgumentParser(description="Find average scores of projects in sections.")
parser.add_argument("-path", "-p", help="Path to Handin root.", default="/user/cse231/Handin/", type=str)
args = vars(parser.parse_args())

# Handin and section path objects, ye
printd("Args = ", args)
handin_path = Path(args["path"])

def save_results(results):
    """
    Saves the result dictionary into a file.
    """
    with open('results{}.pickle'.format(int(time.time())), 'wb') as outfile:
        pickle.dump(results, outfile)

def open_results(results_file_name):
    """
    Opens the result dictionary from a file.
    """
    with open(results_file_name, 'rb') as infile:
        return pickle.load(infile)

def get_averages():
    """
    Gets the dictionary section->[(project average, average)]

    TODO:
     - Handle not-submitted students and have a tally of submitted / total

    """
    section_to_projects_dict = {}
    sections = list(range(1,18))
    sections.append(730)
    for section_number in sections:
        # Create Section object
        section_path = handin_path / "Section{:03d}".format(section_number)

        # just for kicks
        for project_number in range(0, 10):
            # Create a students object and populate it with students
            students = Students()
            students.get_all_students_in_section(section_path)

            # grab the project average for this section
            section_result = []
            for student in students:
                if student.submitted_project(project_number):
                    try:
                        project_total = student.get_project(project_number).get_percent_score()
                        section_result.append(project_total)
                    except Exception as e:
                        print(e)
                        section_result.append(0)
                        continue
                else:
                    # assuming a no show is a 0
                    section_result.append(0)
            if section_number not in section_to_projects_dict:
                section_to_projects_dict[section_number] = []
            project_avg = float( sum(section_result) / len(section_result) )
            section_to_projects_dict[section_number].append((project_number, project_avg))
    # print(section_to_projects_dict)
    return section_to_projects_dict

def main():
    """
    Hackish demo.

    Easily extendable to:
        - Show project averages by request.
        - See where there is a drop in project scores.
    """

    # option = input('Would you like to store the results? (Y/n): ')
    # while option.lower().strip() not in 'y n':
        # option = input('Would you like to store the results? (Y/n): ')
    # if option == 'y':

    results = open_results('results1481517992.pickle')
    # sort

    # find the worst project for each section
    lowest_project_scores = []
    for section_number in results:
        # -1 because of project 0
        worst_project = min(results[section_number][1:], key=operator.itemgetter(1))

        # group the project as a tuple of section, project, score
        worst_project = (section_number, worst_project[0], worst_project[1])
        lowest_project_scores.append(worst_project)

    # sort based on project
    lowest_project_scores.sort(key=operator.itemgetter(1))
    for section, project, score in lowest_project_scores:
        print('Section:', section, ' Project: ', project, ' Average:'" = ", score * 100.0)

    # grab the average of all projects for each section
    section_all_projects_average_dict = {}
    for section_number in results:
        results[section_number].sort(key=operator.itemgetter(1), reverse=True)
        project_sum = sum([project_result[1] * 100 for project_result in results[section_number]])
        section_all_projects_average_dict[section_number] = project_sum / len(results[section_number])
    # pprint.pprint(results)
    # pprint.pprint(section_all_projects_average_dict)
    sorted_average_results = sorted(list(section_all_projects_average_dict.items()), key=operator.itemgetter(1), reverse=True)
    for r in sorted_average_results:
        print(r)

