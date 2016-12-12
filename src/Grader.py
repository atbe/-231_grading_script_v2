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
import traceback

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
    file_name = 'results{}.pickle'.format(int(time.time()))
    with open(file_name, 'wb') as outfile:
        pickle.dump(results, outfile)
        print('Results saved to', file_name)

def open_results(results_file_name):
    """
    Opens the result dictionary from a file.
    """
    with open(results_file_name, 'rb') as infile:
        return pickle.load(infile)

def collect_averages(project_numbers, section_numbers):
    """
    Gets the dictionary section->[(project average, average)]

    TODO:
     - Handle not-submitted students and have a tally of submitted / total

    """
    section_to_projects_dict = {}
    for section_number in section_numbers:
        # Create Section object
        section_path = handin_path / "Section{:03d}".format(section_number)

        # Create a students object and populate it with students
        students = Students()
        students.get_all_students_in_section(section_path)

        # just for kicks
        for project_number in project_numbers:
            # grab the project average for this section
            section_result = []
            for student in students:
                if student.submitted_project(project_number):
                    try:
                        project_total = student.get_project(project_number).get_percent_score()
                        section_result.append(project_total)
                    except IndexError as e:
                        print(e)
                        continue
                    except Exception as e:
                        print('Some exception was encountered.\nStudent: ', student.netid, ' Section:', section_number,
                                'Project: ', project_number, '\nError:', e)
                        print(traceback.format_exc())
                        input('Press enter to continue')
                        continue
                else:
                    # assuming a no show is a 0
                    section_result.append(None)

            # filter out only the students who did submit a project
            project_scores_submitted = [score for score in section_result if score is not None]
            count_no_submission = len([score for score in section_result if score is None])
            project_avg = float( sum(project_scores_submitted) / len(project_scores_submitted) )

            # insert the project result into the dict
            if section_number not in section_to_projects_dict:
                section_to_projects_dict[section_number] = []
            section_to_projects_dict[section_number].append((project_number, project_avg))

            # output the results for students who did not submit
            if count_no_submission:
                print('Section:', section_number, 'Project:', project_number, 'Did not submit:', count_no_submission)
    # print(section_to_projects_dict)
    return section_to_projects_dict

def get_input_range_list(ending_range):
    """
    Helper function translates 1-17 to list of 1 through 17.

    ending_range : int
        - What the highest digit is exclusive.
    """
    single_section = False
    while True:
        section_numbers_input = input('What range would you like the averages of? (Example: 1-17, or 7): ')
        section_numbers_split = section_numbers_input.split('-')
        try:
            section_numbers_split = [int(item.strip()) for item in section_numbers_split]

        except ValueError:
            print('Please enter valid section numbers.')
            continue

        # check if only one digit was entered
        if len(section_numbers_split) == 1:
            if section_numbers_split[0] > 0 and section_numbers_split[0] < ending_range:
                single_section = True
                break
            else:
                print('Sections requested is out of range. Please try again. (single)')
                continue
        # validate the section range
        else:
            if section_numbers_split[0] > 0 and section_numbers_split[1] < ending_range:
                break
            else:
                print('Sections requested is out of range. Please try again. (multi)')
                continue
    if single_section:
        section_numbers = section_numbers_split
    else:
        section_numbers = list(range(section_numbers_split[0], section_numbers_split[1] + 1))

    return section_numbers

def collect_averages_menu():
    """
    Menu to load up the averages then get to the options.
    """
    os.system("clear")
    averages = {  }

    # prompt for seciton numbers
    print('First you will be prompted for the section ranges')
    section_numbers = get_input_range_list(18) # only have sections 1-17
    option_online_section = 'haaa'
    while option_online_section not in 'y n':
        option_online_section = input('Would you like to include section 730? (Y/n): ').lower().strip()
    if option_online_section == 'y':
        section_numbers.append(730)
    print('Requested sections:', section_numbers)

    # prompt for project numbers
    print('\nNow you will be prompted for the project ranges.')
    project_numbers = get_input_range_list(12)
    print('Requested projects:', project_numbers)


    averages = collect_averages(project_numbers, section_numbers)
    print('Averages collected. Saving now.')
    save_results(averages)
    return averages

def process_averages_menu(results):
    pprint.pprint(results)
    '''
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
    '''


def average_collector_menu():
    """
    This is the menu for averages tool. You can either collect
    averages for the current time or load up averages from a pickle
    file and run analysis.
    """
    os.system("clear")
    grading_options = ['Collect Averages', 'Load Averages']
    option = "bangbang"
    averages = {  }
    while option != "x":
        option = print_menu(grading_options, "231 Grading Script")
        if option == "1":
            averages = collect_averages_menu()
            process_averages_menu(averages)
        elif option == "2":
            file_name= input('What is the name of the pickle file?: ')
            try:
                averages = open_results(file_name)
                process_averages_menu(averages)
                break
            except FileNotFoundError:
                print('Could not find', file_name, 'Please try again.')
                continue
    print("c ya later")


def main():
    """
    Hackish demo.

    Easily extendable to:
        - Show project averages by request.
        - See where there is a drop in project scores.
    """


    os.system("clear")
    grading_options = ["Grade all students in your Section", "Grade ungraded projects", "Grade one student", "Average Calculator"]
    option = "bangbang"
    while option != "x":
        option = print_menu(grading_options, "231 Grading Script")
        if option == "1":
            students.grade_all_students(project_number)
        elif option == "2":
            students.grade_all_students(project_number, skip_graded=True)
        elif option == "3":
            netid = input("What is the netid?: ")
            try:
                students.grade_one_student(netid, project_number)
            except IndexError as e:
                print(str(e))
        elif option == "4":
                average_collector_menu()
    print("c ya later")

    # option = input('Would you like to store the results? (Y/n): ')
    # while option.lower().strip() not in 'y n':
        # option = input('Would you like to store the results? (Y/n): ')
    # if option == 'y':

