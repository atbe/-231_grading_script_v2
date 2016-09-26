from Student import Student

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
