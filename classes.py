

import random
import sqlite3


classes_db = sqlite3.connect('courses.db')
cr = classes_db.cursor()
cr.execute('SELECT prerequisites,course_code FROM biomedical WHERE course_code = "Basic Electrical Circuits" ')
a = cr.fetchall()
print(a)
class user:
    user_count = 0  # class variable to keep track of user IDs
    def __init__(self, username, password,  email=None, status="inactive", Id=None ):
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
        return True if isinstance(self, admin) else False ### This will be known by which table is the information in (student or admin)
    
    def is_student(self): # to check if user is student
        return True if isinstance(self, student) else False ### This will be known by which table is the information in (student or admin)

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
    def inroll_student_in_subject(self, student_id): # to enroll a student in the subject for data only ( admin use only)
        self.enrolled_students.append(student_id) ### just for data tracking, actual enrollment is handled in student class
        ### notce that when considering database design, functions like inroll_student_in_section and drop_student_from_section will have to update the database instead of just removing from list


    def drop_student_from_subject(self, student_id): # to drop a student from the subject for data only ( admin use only)
        if student_id in self.enrolled_students:
            self.enrolled_students.remove(student_id) ### i didnt put error handling here becuase it will be handled in student class or section class
        ### notce that when considering database design, functions like inroll_student_in_section and drop_student_from_section will have to update the database instead of just removing from list

#___________________________________________________________________________________________________________________________

class section(subject):
    # def __init__(self,section_name=None,section_code=None, subject_name=None, subject_code=None, capacity = None, schedule=None,enrolled_students=None, instructor=None, prerequisites=None, status="closed"):
    def __init__(self,section_name, subject_name, subject_code, capacity = None, schedule=None,enrolled_students=None, instructor=None, prerequisites=None, status="closed"): ### idont know what is the difference u made here so i will keep it and we have to discuss it and compare it with main ( the line above )
        super().__init__(subject_name, subject_code,prerequisites)
        self.schedule = schedule
        self.instructor = instructor
        self.capacity = capacity
        self.enrolled_students = enrolled_students if enrolled_students is not None else []
        self.section_name = section_name
        self.student_in_section = [] # list of student IDs enrolled in this section

    def display_student_in_section(self): # to display students in the section
        return f"Enrolled Students in Section {self.section_name}: {self.enrolled_students}"    
    def sectioon_info_student(self): # to display section information
        return f"Section Name: {self.section_name} Subject Name: {self.subject_name}, Subject Code: {self.subject_code}, Instructor: {self.instructor}, Schedule: {self.schedule}"    

    def open_section(self): # to open section for enrollment
            if self.status == "open": ### From database guy : work at this by capacity ! Also, This should be at admin class .
                return f"Section {self.section_name} is already open for enrollment."
            else:
                self.status = "open"
                return f"Section {self.section_name} is now open for enrollment."
            
    def is_full(self): # to check if section is full
            return True if len(self.enrolled_students) >= self.capacity else False ### this function is alredy in subject class ?
    
    def view_enrolled_students(self): # to view all enrolled students in the section
            return self.enrolled_students
    
    def has_time_conflict(self, other_sections): # to check for time conflicts with other sections
            pass
    
    def prerequisites_met(self, completed_subjects): # to check if prerequisites are met
            for prereq in self.prerequisites:
                if prereq not in completed_subjects:
                    return False
            return True
    def enroll_student_in_section(self, student_id): # to enroll a student in the section for data only ( admin use only)
        self.student_in_section.append(student_id) ### just for data tracking, actual enrollment is handled in student class
        self.enroll_student_in_subject(student_id)

    def drop_student_from_section(self, student_id): # to drop a student from the section for data only ( admin use only)    
        if student_id in self.student_in_section:
            self.student_in_section.remove(student_id) ### i didnt put error handling here becuase it will be handled in student class or subject class
            self.drop_student_from_subject(student_id)
            ### notce that when considering database design, functions like inroll_student_in_section and drop_student_from_section will have to update the database instead of just removing from list
    def new_capacity(self, new_capacity): # to expand the capacity of the section
            self.capacity = new_capacity
    def remaining_seats(self): # to check remaining seats in the section
            return self.capacity - len(self.enrolled_students)
           
#___________________________________________________________________________________________________________________________

existing_ids = set()

class student(user):
    def __init__(self, username, password, email=None,enrolled_subjects = None,completed_subjects = None, status="inactive", Id=None, GPA=None, cummulative_GPA=None):
        super().__init__(username, password, email, status, Id)
        self.GPA = GPA
        self.cummulative_GPA = cummulative_GPA
        self.enrolled_subjects = enrolled_subjects if enrolled_subjects is not None else [] # list of section codes the student is currently enrolled in
        self.completed_subjects = completed_subjects if completed_subjects is not None else [] # list of section codes the student has completed
        self.current_credits = 0  ### total credits of currently enrolled subjects, i believe this is needed for checking max credits allowed per semester not current total subjects
        self.Id = self.generate_unique_id()
        self.email = f"{self.username}@stu.kau.edu.sa"
    
    def generate_unique_id(self): # generates random id for each student
        while True:
            Id = random.randint(100000, 999999)  # Generate a random 6-digit ID
            cursor.execute("SELECT 1 FROM students WHERE Id = ?", (Id,))
            if cursor.fetchone() is None:
                return Id
            
    def enroll_subject(self, section_code): # to enroll in a subject (student initiated)
    
        availabilty = True  ### Check availability of the subject first


    def enroll_subject(self,section_code): 
        for sec in self.enrolled_subjects: # to check if already enrolled
            if sec.subject_code == section_code.subject_code:
                availabilty = False
                print(f"Already enrolled in subject {section_code}.")
        
        for sec in self.completed_subjects: # to check if already completed
            if sec.subject_code == section_code.subject_code:
                availabilty = False
                print(f"Subject {section_code} has already been completed.")

        
        if self.current_credits + section_code.credits > 21:  ### assuming max 21 credits allowed per semester
            availabilty = False
            print("Cannot exceed maximum credit limit of 21.")
        
        if section_code.is_full():  ### assuming this function checks if the section is full
            availabilty = False
            print(f"Subject {section_code} is full.")
        
        if section_code.has_time_conflict(self.enrolled_subjects): ### assuming this function checks for time conflicts with currently enrolled subjects
            availabilty = False
            print(f"Subject {section_code} has a time conflict with your current schedule.")
        
        if not section_code.prerequisites_met(self.completed_subjects): ### assuming this function checks if prerequisites are met
            availabilty = False
            print(f"Prerequisites for subject {section_code} are not met.")

        if section_code.status != "open":
            availabilty = False
            print(f"Subject {section_code} is not open for enrollment.")
        
        if section_code not in section_db: ### assuming section_db is a database or list of all sections
            availabilty = False
            print(f"Subject {section_code} does not exist.")
        
        if availabilty:
            self.enrolled_subjects.append(section_code)  ### append wont be used if we are using a database, instead we will have to update the database
            self.current_credits += section_code.credits 
            self.inroll_student_in_section(self.Id) ### enroll student in section for data tracking , ### same here, we will have to update the database instead of appending
            return f"Enrolled in subject {section_code} successfully.\n Here is all the information about the section you just enrolled in:\n {section_code.sectioon_info_student()}"
        

        
        

        ### after making sure subject can be taken (not full, not already taken,prerequisites met,time conflict etc.)
        ### this is the second use of this function after admin.avilable_subjects
        ### always put in mind error handling and edge cases (e.g., what if section_code does not exist?)

      

    def drop_subject(self, subject_code): # to drop a subject (student initiated)

        availabilty = True  ### Check if the subject is enrolled first

        if subject_code not in self.enrolled_subjects:
            availabilty = False
            return f"Not enrolled in subject {subject_code}."  
        
        if availabilty:
            self.enrolled_subjects.remove(subject_code) ### again, this is for list, for database we will have to update the database
        subject_code.enrolled_students.remove(self.Id) ### same here, update database instead of removing
        self.drop_student_from_section(self.Id) ### same here, update database instead of removing

        return f"Dropped subject {subject_code} successfully."
        ### make sure student is enrolled in the subject before dropping
        ### not sure if we should put in mind a certain deadline for dropping subjects
        pass
    
    def view_enrolled_subjects(self):# to view all enrolled subjects (student initiated)
        
        if self.enrolled_subjects == None or len(self.enrolled_subjects) == 0:
            return "No subjects enrolled."
        else:
            return self.enrolled_subjects ### again, this is for list, for database we will have to fetch from database (return all inmformantion about enrolled subjects)
        ### i think this function should return schedule, instructor, section name
        ### notce that section name is different from subject code, for example, subject code is 233746 but section name can be SA, SB etc. so far this is a data base design issue


        pass
    
    def calculate_GPA(self): # to calculate GPA based on completed subjects and their grades
        pass  
    ### not sure if these all the mwthods needed for student class

    def transcript(self): # to generate a transcript of completed subjects and grades
        pass
    
#___________________________________________________________________________________________________________________________

class admin(user):
    def __init__(self, username, password, email, status="inactive", Id=None):
        super().__init__(username, password, email, status, Id)
    def add_subject(self, section_code, student_id): # to add a subject to a student
        student_id.enroll_subject(section_code)
    
    def remove_subject(self, section_code, student_id): # to remove a subject from a student
        self.The_student= student(student_id=student_id)
        self.The_student.drop_subject(section_code)  ### we made an object of student class to access drop_subject method


    def display_student_in_section(self, section_code): # to display students in a section
        self.sectionCode= section(section_code=section_code) 
        return self.sectionCode.display_student_in_section()
    
    # def view_all_students(self, section_code=None): # to view all students, optionally filtered by section 
    #     if section_code != None:
    #         return section_code.display_student_in_section() ### return list of student IDs enrolled in the section
    #     pass
    ### idont think we need view_all_students function, admin can just use display_student_in_section function 
    def find_student(self, student_id): # to find student's information by ID
        self.The_student= student(student_id=student_id)
        return self.The_student.display_info()
        pass
    
    def view_all_subjects(self, available_only): # to view all subjects, optionally filtering only available ones
        ### I have to understand data base more to implement this function
        pass

    def find_sections(self, subject_code,): # to find subject's information by code
        ### here as well i have to understand data base more to implement this function, i reallt need to understand the relationships between subjects and sections and how to access them
       
        ### return subject details each with section info (schedule, instructor, capacity, enrolled students etc.)
        ### not sure if including enrolled students is a good idea, so far i think its better to exclude it 
        pass

    def expand_capacity(self, section_code, new_capacity): # to expand the capacity of a section
        self.sectionCode= section(section_code=section_code)
        if self.sectionCode.is_full():
            self.sectionCode.new_capacity(new_capacity)
        else:
            return f"Section {section_code} is not full. Cannot expand capacity. \n the remaning seats are {self.sectionCode.remaining_seats()}"

        pass 
    def reduce_capacity(self, section_code, new_capacity): # to reduce the capacity of a subject
        self.sectionCode= section(section_code=section_code)
        if new_capacity=< len(self.sectionCode.enrolled_students):
            return f"Cannot reduce capacity to {new_capacity}. Currently enrolled students: {len(self.sectionCode.enrolled_students)}" 
        else:
            self.sectionCode.new_capacity(new_capacity)
        pass
    def avilable_subjects(self, student_id): # to view subjects that a student can enroll in
        ### here as well i have to understand data base more to implement this function
        ### must check prerequisites, time conflicts, capacity etc.

        pass 