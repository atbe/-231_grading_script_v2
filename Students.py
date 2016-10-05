import os
from Student import Student
from Tools import print_menu

class Students:

    def __init__(self):
        self.students = []


    def add_student(self, student):
        self.students.append(student)

    def get_all_students_in_section(self, section_path):
        for student_path in section_path.iterdir():
            if student_path.is_dir():
                # print(student_path.name)
                self.students.append(Student(student_path))
        self.students.sort()

    def __iter__(self):
        for student in self.students:
            yield student

    def __getitem__(self, key):
        if key > len(self.students) - 1:
            raise IndexError("Index out of range")
        else:
            return self.students[key]

    def grade_all_students(self, project_number):
        options = ["Open the files", "Move on to next student"]
        for student in self.students:
            os.system("clear")
            student.print_project_info(project_number)
            option = "ooblah"
            # TODO: Add Pranshu score sheet checker and write .graded file if not already written
            while (option != "x"):
                option = print_menu(options, "Project Grading")
                if option == "x":
                    print("Returning to main menu.")
                    return
                elif option == "1":
                    student.open_files(project_number)
                elif option == "2":
                    break
        input("Finished grading all students. Press enter to return to the main menu")

    def grade_ungraded_students(self, project_number):
        options = ["Open the files", "Move on to next student"]
        for student in self.students:
            if student.get_project(project_number).is_graded:
                continue
            os.system("clear")
            student.print_project_info(project_number)
            option = "ooblah"
            while (option != "x"):
                option = print_menu(options, "Project Grading")
                if option == "x":
                    print("Returning to main menu.")
                elif option == "1":
                    student.open_files(project_number)
                elif option == "2":
                    break
        input("Finished grading all students. Press enter to return to the main menu")

