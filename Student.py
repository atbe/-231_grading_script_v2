import os
from Project import Project
from subprocess import call

# for testing purposes only.
EDITOR="gedit"

class Student:

    def __init__(self, path):
        self.path = path
        self.netid = path.name
        # Project paths is a list of Path objects to all projects
        self.project_paths = self._populate_projects()
        # Projects is a dictionary mapping {Project Number -> Project Path}
        self.projects = self._populate_projects()

    def submitted_project(self, project_number):
        return (self.path / "{:02d}".format(project_number)).exists()

    def _populate_projects(self):
        projects = {}
        for project_path in self.path.iterdir():
            # print(project_path.name)
            if project_path.name.isdigit():
                projects[int(project_path.name)] = Project(project_path)
                # projects.append(Project(project_path))

        # print(projects)
        return projects

    def get_project(self, project_number):
        if project_number not in [proj.number for proj in self.project_paths]:
            raise IndexError("{} has not submitted project {:02d}".format(self.netid, project_number))
        else:
            return self.project_paths[project_number]

    def run_project_py_file(self, project_number):
        project_path = self.get_project(project_number)
        # print(project_path)
        print ("Running {} project {}".format(self.netid, project_number))
        for py_path in project_path.py_paths:
            absolute_path = py_path.resolve()
            # print(str(absolute_path))
            print("{} output:".format(absolute_path))
            call(["python3", str(absolute_path)])

    def open_files(self, project_number):
        # TODO: Implement checking for when project does not exist
        project = self.projects[project_number]
        files_to_open = " ".join([path.name for path in project.all_file_paths])

        print("Current Student: {}\nCurrent Project: {}\nIs Graded: {}".format(self.netid, project.number, project.is_graded))
        input("Press enter to open the files in {}.".format(EDITOR))
        for path in project.all_file_paths:
            # print("Project graded = ", project.is_graded)
            print("Opening: ", str(path))
            os.system("{} {} &".format(EDITOR, str(path)))
        # input("Press enter to continue")

    def __lt__(self, other_student):
        return self.netid < other_student.netid

    def __gt__(self, other_student):
        return not self < other_student

