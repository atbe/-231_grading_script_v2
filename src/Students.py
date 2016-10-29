import os
from Student import Student
from Tools import print_menu

class Students:
    """
    Models a collection of Student objects.

    Attributes
    ----------
    students : list<Student>
        List of all the student objects in this collection.
    """

    def __init__(self):
        """
        Default construcor, takes no arguments.
        """
        self.students = []


    def add_student(self, student):
        """
        Add student to the students collection.

        Parameters
        ----------
        student : Student
            The student to be added to the collection.
        """
        self.students.append(student)

    def get_all_students_in_section(self, section_path):
        """
        Populates the students list with Student objects found in a sections path.

        Parameters
        ----------
        section_path : Path
            Path to the section to be graded.
        """
        for student_path in section_path.iterdir():
            if student_path.is_dir():
                # print(student_path.name)
                self.students.append(Student(student_path))
        self.students.sort()

    def __iter__(self):
        """
        Support iterating over the students list.
        """
        for student in self.students:
            yield student

    def __getitem__(self, key):
        """
        Support indexing []

        Raises
        ------
        IndexError
            Students request was out of range.
        """
        if key > len(self.students) - 1:
            raise IndexError("Index out of range")
        else:
            return self.students[key]

    def grade_one_student(self, netid, project_number):
        """
        Used to grade a single student.

        Parameters
        ----------
        netid : string
            The students netid.
        project_number : int
            The project to be graded.

        Raises
        ------
        IndexError
            Student is not found or project is not found.
        """
        options = ["Open all the files", "Open the scoresheet"]
        student_possible_matches = [student for student in self.students if student.netid == netid]
        if len(student_possible_matches) != 1:
            raise IndexError("Student not found!")
        student = student_possible_matches[0]
        try:
            project = student.get_project(project_number)
        except IndexError as e:
            raise e
        option="submarine"
        while(option != "x"):
            os.system("clear")
            student.print_project_info_and_check_score(project_number)
            option = print_menu(options, "Project Grading")
            if option == "x":
                print("Returning to main menu.")
                return
            elif option == "1":
                project.open_files()
                input("\nPress enter when you have finished grading.\n")
                project.check_scoresheet()
                project.mark_as_graded()
            elif option == "2":
                project.open_scoresheet()
                input("\nPress enter when you have finished grading.\n")
                project.check_scoresheet()


    def grade_all_students(self, project_number, skip_graded=False):
        """
        Grades all students.
        Supports skipping of students who are already graded.

        Parameters
        ----------
        project_number : int
            Project to be graded.
        skip_graded : bool = False
            If True, students with a .graded file in their directory will be skipped.
        """
        options = ["Open all the files", "Open the scoresheet", "Grade Previous Student", "Grade Next Student"]
        current_student_index = 0
        while current_student_index < len(self.students):
            # print(current_student_index)
            student = self.students[current_student_index]
            try:
                project = student.get_project(project_number)
            except IndexError as e:
                print(e)
                input("Press enter to continue.")
                current_student_index += -1 if option == "3" else 1
                continue
            if skip_graded and project.is_graded:
                current_student_index += 1
                continue
            option = "ooblah"
            while (option != "x"):
                os.system("clear")
                student.print_project_info_and_check_score(project_number)
                option = print_menu(options, "Project Grading")
                if option == "x":
                    print("Returning to main menu.")
                    return
                elif option == "1":
                    project.open_files()
                    input("\nPress enter when you have finished grading.\n")
                    project.check_scoresheet()
                    project.mark_as_graded()
                elif option == "2":
                    project.open_scoresheet()
                    input("\nPress enter when you have finished grading.\n")
                    project.check_scoresheet()
                elif option == "3":
                    if current_student_index == 0:
                        print("You are on the first student!")
                    else:
                        current_student_index -= 1
                        break
                elif option == "4":
                    current_student_index += 1
                    break

        input("\nFinished grading all students. Press enter to return to the main menu.")

