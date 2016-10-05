

class Project:
    """
    Used to model Project objects.
    """

    def __init__(self, path):
        self.project_path = path
        self.number = int(path.name)
        # List of Path objects to all the py files in project folder
        self.py_paths = self.get_py_paths()
        # List of Path objects to all the files in the project folder
        self.all_file_paths = self.get_all_file_paths()
        self.is_graded = self.check_graded()

    def get_py_paths(self):
        """
        Populates py_paths with paths to all py files.
        """
        py_paths = []
        for path in self.project_path.iterdir():
            if ".py" in path.name:
                # print(path.name)
                py_paths.append(path)

        return py_paths

    def get_all_file_paths(self):
        """
        Populates all_file_paths member with paths to all the files.
        """
        files = []
        for path in self.project_path.iterdir():
            if path.is_file() and path.name != ".graded":
                # print("Adding {} to project files.".format(path.name))
                files.append(path)
        return files

    def check_graded(self):
        """
        Checks if a project is graded.
        """
        return (self.project_path / ".graded").exists()
