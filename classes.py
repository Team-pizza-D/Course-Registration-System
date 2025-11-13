class user:
    def __init__(self, username, password,  email, status="inactive", Id=None ):
        self.username = username
        self.password = password
        self.Id = Id
        self.email = email
        self.status = status

    def display_info(self):
        return f"Username: {self.username}, Email: {self.email}, Status: {self.status}, ID: {self.Id}"
    
    def activate(self):
        self.status = "active"

    def deactivate(self):
        self.status = "inactive"

    def is_admin(self):
        return True if isinstance(self, admin) else False
    
    def is_student(self):
        return True if isinstance(self, student) else False

class subject:
    def __init__(self, subject_name, subject_code,prerequisites=None):
        self.subject_code = subject_code
        self.subject_name = subject_name
        self.enrolled_students = []
        self.prerequisites = prerequisites if prerequisites is not None else []

    def is_full(self):
        return len(self.enrolled_students) >= self.capacity
    
    def view_enrolled_students(self):
        pass

class section(subject):
    def __init__(self, subject_name, subject_code, capacity = None, schedule=None, instructor=None, prerequisites=None):
        super().__init__(subject_name, subject_code, capacity, prerequisites)
        self.schedule = schedule
        self.instructor = instructor
    pass

class admin(user):
    def __init__(self, username, password, email, status="inactive", Id=None):
        super().__init__(username, password, email, status, Id)
        super().__init__(subject_code=None, subject_name=None, capacity=None)
    def add_subject(self, subject_code):
        pass
    
    def remove_subject(self, subject_code, student_id):
        pass
    
    def view_all_students(self):
        pass
    
    def find_student(self, student_id):
        pass
    
    def view_all_subjects(self):
        pass
    
    def find_subject(self, subject_code):
        pass
    
    def expand_capacity(self, subject_code, new_capacity):
        pass 

class student(user):
    def __init__(self, username, password, email,taken_subjects = None, status="inactive", Id=None, GPA=None):
        super().__init__(username, password, email, status, Id)
        self.GPA = GPA
        self.enrolled_subjects = taken_subjects if taken_subjects is not None else []
        

    def enroll_subject(self,section_code): 
    
        ### after making sure subject can be taken (not full, not already taken,prerequisites met,time conflict etc.)

        self.enrolled_subjects.append(section_code)
        return f"Enrolled in subject {section_code} successfully."

    def drop_subject(self, subject_code):
        pass
    
    def view_enrolled_subjects(self):
        pass
    
    def calculate_GPA(self):
        pass   
    
