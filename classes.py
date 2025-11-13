# class subjects:
#     def __init__(self, name, code,MaxCapacity,credits):
#         self.name = name
#         self.code = code
#         self.MaxCapacity = MaxCapacity
#         self.credits = credits

#     def display_info(self):
#         return f"Subject Name: {self.name}, Subject Code: {self.code}, Max Capacity: {self.MaxCapacity}, Credits: {self.credits}"
    
    

# class students:
#     def __init__(self, name, student_id,)

class user:
    def __init__(self, username, password,  email, status="inactive", Id=None ):
        self.username = username
        self.password = password
        self.Id = Id
        self.email = email
        self.status = status

    def display_info(self):
        return f"Username: {self.username}, Email: {self.email}, Status: {self.status}, ID: {self.Id} "
    def activate(self):
        self.status = "active"
    def deactivate(self):
        self.status = "inactive"
    def is_admin(self):
        return True if isinstance(self, admin) else False
    def is_student(self):
        return True if isinstance(self, student) else False


class admin(user):
    def __init__(self, username, password, email, status="active", Id=None):
        super().__init__(username, password, email, status, Id)
    def add_subject(self, subject_code, student_id):
        pass
    def remove_subject(self, subject_code, student_id):
        pass
    def view_all_students(self):
        pass
    def find_student(self, student_id):
        pass
    def view_all_subjects(self):
        pass
    def find_subject(self, subject_code):# to find a subject by its code
        pass
    def expand_capacity(self, subject_code, new_capacity):# to expand the capacity of a subject
        pass 
    def reduce_capacity(self, subject_code, new_capacity): # to reduce the capacity of a subject
        pass
    def avilable_subjects(self, student_id): # to view subjects that a student can enroll in
        pass 
    

class student(user):
    def __init__(self, username, password, email, status="inactive", Id=None):
        super().__init__(username, password, email, status, Id)
        self.enrolled_subjects = []

    def enroll_subject(self, subject_code):
        pass
    def drop_subject(self, subject_code):
        pass
    def view_enrolled_subjects(self):
        pass
