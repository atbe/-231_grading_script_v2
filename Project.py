import os.path

class Project:

    def __init__(self, path):
        self.path = path
        self.number = int(path.name)
        self.py_paths = self.get_py_paths()

    def get_py_paths(self):
        py_paths = []
        for path in self.path.iterdir():
            if ".py" in path.name:
                # print(path.name)
                py_paths.append(path)

        return py_paths
