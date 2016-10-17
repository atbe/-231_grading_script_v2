from Project import Project
import subprocess

class Student:
    """
    Student class used to model a student of the course.

    Attributes
    ----------
    path : Path
        Path to the students folder.
    netid : string
        Netid of the student.
    projects : map<int, Project>
        Dictionary of project_number to project objects belonging to the student.
    """

    def __init__(self, path):
        """
        Default constructor for Student object.

        Parameters
        ----------
        path : Path
            Path to the students folder.
        """
        self.path = path
        self.netid = path.name
        self.projects = self._populate_projects()

    def submitted_project(self, project_number):
        """
        Check if the student submitted the project.

        Returns
        -------
        bool
            True if the project file exists.
        """
        return (self.path / "{:02d}".format(project_number)).exists()

    def _populate_projects(self):
        """
        Used to populate the projects attribute.

        Returns
        -------
        map<int, Project>
            Map of project_number to projects.
        """
        projects = {}
        for project_path in self.path.iterdir():
            # print(project_path.name)
            if project_path.name.isdigit():
                projects[int(project_path.name)] = Project(project_path)
                # projects.append(Project(project_path))

        # print(projects)
        return projects

    def get_project(self, project_number):
        """
        Get the students project, if it was submitted.

        Parameters
        ----------
        project_number : int
            The project being grabbed.

        Returns
        -------
        Project
            The project requested.

        Raises
        ------
        IndexError
            Student did not submit the project.
        """
        if project_number not in self.projects:
            raise IndexError("{} has not submitted project {:02d}".format(self.netid, project_number))
        else:
            return self.projects[project_number]

    def run_project_py_file(self, project_number):
        """
        Runs the py files in Python3

        Parameters
        ----------
        project_number : int
            The project to run.
        """
        project_path = self.get_project(project_number)
        # print(project_path)
        print ("Running {} project {}".format(self.netid, project_number))
        for py_path in project_path.py_paths:
            # print(str(absolute_path))
            print("{} output:".format(py_path))
            subprocess.Popen(["python3", str(py_path)], stdout=subprocess.STDOUT, stderr=subprocess.STDOUT)

    def print_project_info_and_check_score(self, project_number):
        """
        Prints the project info relative to this student.

        Parameters
        ----------
        project_number : int
            The project whos stats will be outputted
        """
        print("Current Student: {}".format(self.netid))
        print("Current Project: {}".format(project_number))
        is_graded = self.projects[project_number].is_graded
        print("Is Graded: {}".format(is_graded))
        if is_graded:
            print("Current score: {}".format(self.projects[project_number].get_project_total_score()[1][0]))

    def __lt__(self, other_student):
        """
        Less than comparision for iteration based on netid.

        Returns
        -------
        bool
            True if students netid is less than the other students netid.
        """
        return self.netid < other_student.netid

    def __gt__(self, other_student):
        """
        Greater than comparision for iteration based on netid.

        Returns
        -------
        bool
            True if the netid is > other net id.
        """
        return not self < other_student

