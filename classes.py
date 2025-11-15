class user:
    def __init__(self, username, password,  email, status="inactive", Id=None ):
        self.username = username
        self.password = password
        self.Id = Id
        self.email = email
        self.status = status

    def display_info(self): # to display user information
        return f"Username: {self.username}, Email: {self.email}, Status: {self.status}, ID: {self.Id}"
    def activate(self): # to activate user account
        if self.status == "active":
            return f"{self.username}'s account is already active."
        else:
            self.status = "active"
            return f"{self.username}'s account has been activated."

    def deactivate(self): # to deactivate user account
        if self.status == "inactive":
            return f"{self.username}'s account is already inactive."
        else:
            self.status = "inactive"
            return f"{self.username}'s account has been deactivated."

    def is_admin(self): # to check if user is admin
        return True if isinstance(self, admin) else False
    
    def is_student(self): # to check if user is student
        return True if isinstance(self, student) else False

class subject: ### Data base team said that this is currently not needed but i think its better to have it for future use
    def __init__(self, subject_name, subject_code,prerequisites=None):
        self.subject_code = subject_code
        self.subject_name = subject_name
        self.enrolled_students = []
        self.prerequisites = prerequisites if prerequisites is not None else []

    def is_full(self): # to check if subject is full
        return len(self.enrolled_students) >= self.capacity
    
    def view_enrolled_students(self): # to view all enrolled students
        pass

class section(subject):
    def __init__(self,section_name,section_code, subject_name, subject_code, capacity = None, schedule=None,enrolled_students=None, instructor=None, prerequisites=None):
        super().__init__(subject_name, subject_code, capacity, prerequisites)
        self.schedule = schedule
        self.instructor = instructor
        self.capacity = capacity
        self.enrolled_students = enrolled_students if enrolled_students is not None else []
        self.section_name = section_name
        self.section_code = section_code

    def is_full(self): # to check if section is full
            return True if len(self.enrolled_students) >= self.capacity else False
    
    def view_enrolled_students(self): # to view all enrolled students in the section
            return self.enrolled_students
    
    def has_time_conflict(self, other_sections): # to check for time conflicts with other sections
            pass
    

class admin(user):
    def __init__(self, username, password, email, status="inactive", Id=None):
        super().__init__(username, password, email, status, Id)
    def add_subject(self, section_code, student_id): # to add a subject to a student
        pass
    
    def remove_subject(self, section_code, student_id): # to remove a subject from a student
        pass
    
    def view_all_students(self, section_code=None): # to view all students, optionally filtered by section 
        pass
    
    def find_student(self, student_id): # to find student's information by ID
        pass
    
    def view_all_subjects(self, available_only=False): # to view all subjects, optionally filtering only available ones
        pass
    def find_sections(self, subject_code,): # to find subject's information by code
        ### return subject details each with section info (schedule, instructor, capacity, enrolled students etc.)
        ### not sure if including enrolled students is a good idea
        pass
    def expand_capacity(self, section_code, new_capacity): # to expand the capacity of a section
        pass 
    def reduce_capacity(self, section_code, new_capacity): # to reduce the capacity of a subject
        pass
    def avilable_subjects(self, student_id): # to view subjects that a student can enroll in
        ### must check prerequisites, time conflicts, capacity etc.

        pass 
    

class student(user):
    def __init__(self, username, password, email,enrolled_subjects = None,completed_subjects = None, status="inactive", Id=None, GPA=None):
        super().__init__(username, password, email, status, Id)
        self.GPA = GPA
        self.enrolled_subjects = enrolled_subjects if enrolled_subjects is not None else [] # list of section codes the student is currently enrolled in
        self.completed_subjects = completed_subjects if completed_subjects is not None else [] # list of section codes the student has completed
    def enroll_subject(self,section_code): 

        if section_code in self.enrolled_subjects:
            return f"Already enrolled in subject {section_code}."
        
        if section_code in self.completed_subjects:
            return f"Subject {section_code} has already been completed."
        
        if len(self.enrolled_subjects) >= 5:  ### assuming max 5 subjects can be taken
            return "Cannot enroll in more than 5 subjects."
        
        if section_code.is_full():  ### assuming this function checks if the section is full
            return f"Subject {section_code} is full."
        
        if section_code.has_time_conflict(self.enrolled_subjects): ### assuming this function checks for time conflicts with currently enrolled subjects
            return f"Subject {section_code} has a time conflict with your current schedule."
        
        if not section_code.prerequisites_met(self.completed_subjects): ### assuming this function checks if prerequisites are met
            return f"Prerequisites for subject {section_code} are not met."
        

        ### after making sure subject can be taken (not full, not already taken,prerequisites met,time conflict etc.)
        ### this is the second use of this function after admin.avilable_subjects
        ### always put in mind error handling and edge cases (e.g., what if section_code does not exist?)

        self.enrolled_subjects.append(section_code) ### this line and the next line will only work if the previous checks are done (return true)
        return f"Enrolled in subject {section_code} successfully."

    def drop_subject(self, subject_code): # to drop a subject (student initiated)
        ### make sure student is enrolled in the subject before dropping
        ### not sure if we should put in mind a certain deadline for dropping subjects
        pass
    
    def view_enrolled_subjects(self):# to view all enrolled subjects (student initiated)
        ### i think this function should return schedule, instructor, section name
        ### notce that section name is different from subject code, for example, subject code is 233746 but section name can be SA, SB etc. so far this is a data base design issue


        pass
    
    def calculate_GPA(self): # to calculate GPA based on completed subjects and their grades

        pass   
    
