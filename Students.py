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

    def grade_all_students(self, project_number, skip_graded=False):
        options = ["Open all the files", "Open the scoresheet", "Grade Previous Student", "Grade Next Student"]
        current_student_index = 0
        while current_student_index < len(self.students) - 1:
            current_student_index += 1
            # print(current_student_index)
            student = self.students[current_student_index]
            project = student.get_project(project_number)
            if skip_graded and project.is_graded:
                continue
            os.system("clear")
            student.print_project_info_and_check_score(project_number)
            option = "ooblah"
            while (option != "x"):
                option = print_menu(options, "Project Grading")
                if option == "x":
                    print("Returning to main menu.")
                    return
                elif option == "1":
                    project.open_files()
                elif option == "2":
                    project.open_scoresheet()
                    project.check_scoresheet()
                elif option == "3":
                    if current_student_index == 0:
                        print("You are on the first student!")
                elif option == "4":
                    current_student_index += 1
                    break
                else:
                    current_student_index -= 1
                    break

        input("\nFinished grading all students. Press enter to return to the main menu.")

