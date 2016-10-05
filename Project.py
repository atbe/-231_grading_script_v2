import re

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
        self.scoresheet_path = self.get_scoresheet()

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

    def get_scoresheet(self):
        score_file_paths = list(self.project_path.glob("./*.score"))
        if len(score_file_paths) < 1 or len(score_file_paths) > 1:
            # print("ERROR: Student does not have a score file.")
            # TODO: Handle missing score file
            # raise Exception
            return
        score_file_path = score_file_paths[0]

        return score_file_path

    def get_project_total_score(self):
        with open(str(self.scoresheet_path), "r") as file_object_read:
            lines = file_object_read.read()
            pattern_list = (re.findall(r'_+\d+_+', lines))
            # print (pattern_list)
            points_list = list()
            for elements in pattern_list:
                points = elements.split('_')
                # print (points)
                point_position = int(len(points) / 2)
                points_list.append(int(points[point_position]))
            # print (points_list)
            # Subtract the current project score from the total incase this is a regrading
            total = sum(points_list) - points_list[0]
            # print (total)
        return total, points_list

    def write_project_score(self, total, points_list):
        with open(str(self.scoresheet_path), 'r+') as file_object_write:
            lines = file_object_write.readlines()
            for i, line in enumerate(lines):
                if '__' in line and 'Score:' in line:
                    # print(line)
                    line = line.replace("__{:02d}__".format(points_list[0]), "__{}__".format(total))
                    # print(line)
                    lines[i] = line
            file_object_write.seek(0)
            file_object_write.writelines(lines)
        # print("TOTAL = ", total)

    def check_scoresheet(self):
        score_total, points_list = self.get_project_total_score()
        # print("Calculated score: {:02d}".format(score_total))
        self.write_project_score(score_total, points_list)
        return score_total
