import random
import sqlite3



class Database:
    """
    Simple helper class to interact with a SQLite database.

    Usage examples:
        users_db = Database("Users.db")
        row = users_db.execute("SELECT * FROM students WHERE Id = ?", (12345,), fetchone=True)
        users_db.execute(
            "INSERT INTO students (username, email) VALUES (?, ?)",
            ("abdulkreem", "abdulkreem@stu.kau.edu.sa"),
            commit=True,
        )
    """
    def __init__(self, db_name):
        self.db_name = db_name

    def execute(self,query: str,params: tuple = (), *,fetchone: bool = False,fetchall: bool = False,commit: bool = False,):
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()
        cur.execute(query, params)

        result = None
        if fetchone:
            result = cur.fetchone() ### to select single row
        elif fetchall:
            result = cur.fetchall() ### to select multiple rows

        if commit:
            conn.commit() ### for insert, update, delete operations

        conn.close()
        return result

# _______________________________________________________________________________________________________________
### open database connection
users_db = Database("Users.db")
courses_db = Database("courses.db")
programs_db = Database("programs.db")
# _______________________________________________________________________________________________________________

class user:
    user_count = 0  # class variable to keep track of user IDs
    def __init__(self, username, password=None, email=None, status="inactive", Id=None):
        self.username = username
        self.Id, self.email, self.password = self.generate_admin_instructor()

    def display_info(self):  # to display user information
        return f"Username: {self.username}, Email: {self.email}, Status: {self.status}, ID: {self.Id}"

    def activate(self):  # to activate user account
        if self.status == "active":
            return f"{self.username}'s account is already active."
        else:
            self.status = "active"
            return f"{self.username}'s account has been activated."

    def deactivate(self):  # to deactivate user account
        if self.status == "inactive":
            return f"{self.username}'s account is already inactive."
        else:
            self.status = "inactive"
            return f"{self.username}'s account has been deactivated."

    def is_admin(self):  # to check if user is admin
        # This will later be known by which table is the information in (student or admin)
        return True if isinstance(self, admin) else False

    def is_student(self):  # to check if user is student
        # This will later be known by which table is the information in (student or admin)
        return True if isinstance(self, student) else False

    def generate_admin_instructor(self):  # generates instructor/admin account
        existing_a_Ids = users_db.execute("SELECT Id FROM admins", fetchall=True)
        existing_i_Ids = users_db.execute("SELECT Id FROM instructors", fetchall=True)
        existing_Ids = set(existing_a_Ids + existing_i_Ids)
        Id = random.randint(1000000000,9999999999)
        while Id in existing_Ids:
            Id = random.randint(1000000000,9999999999) 
        email = f"{self.username}{Id}@kau.edu.sa"
        if password is None:
            password = self.username + str(random.randint(100000, 999999))
        else:
            password = password
        return Id, email, password
        
    

class subject:  ### Data base team said that this is currently not needed but i think its better to have it for future use
    def __init__(self, subject_name, subject_code, prerequisites=None):
        self.subject_code = subject_code
        self.subject_name = subject_name
        self.enrolled_students = []
        self.prerequisites = prerequisites if prerequisites is not None else []

    def is_full(self):  # to check if subject is full
        # in the future this can depend on subject capacity if needed
        pass

    def view_enrolled_students(self):  # to view all enrolled students
        # later this can return / print all enrolled students for this subject
        pass

    def inroll_student_in_subject(self, student_id):  # to enroll a student in the subject for data only (admin use only)
        ### just for data tracking, actual enrollment is handled in student class
        ### notce that when considering database design, function will have to update the database instead of just appending to list
        pass

    def drop_student_from_subject(self, student_id):  # to drop a student from the subject for data only (admin use only)
        pass

### notce that when considering database design, function will have to update the database instead of just removing from list
        pass


# _______________________________________________________________________________________________________________

section_db=Database("courses.db") ### since section class will use database a lot i think its better to create database object here
class section(subject):
    # def __init__(self,section_name=None,section_code=None,capacity = 0,enrolled_students=None, schedule=None, instructor=None, prerequisites=None, status="closed"):
    def __init__(self,section_name,subject_name,subject_code,schedule=None,capacity=0,enrolled_students=None,instructor=None,prerequisites=None,status="closed",):
        ### this constructor version is the one we will use, we have to discuss it and compare it with main (the line above)
        super().__init__(subject_name, subject_code, prerequisites)
        self.schedule = schedule
        self.instructor = instructor
        self.capacity = capacity
        # self.enrolled_students = enrolled_students if enrolled_students is not None else [] ### I dont think we need this
        self.section_name = section_name
        self.student_in_section_db = Database("i dont what is the file name")  ### as menshed I dont know what is the file name one i know it and know the database design i will implement it to be completely functional
        row = self.student_in_section_db.execute("SELECT student_id, student_name FROM students_in_section WHERE section_code = ?", (self.section_code,), fetchall=True)
        if not row:
            self.enrolled_students = []
        else:
            # Build lists from query rows without overwriting the Database object
            self.enrolled_students = [f"{r[0]} - {r[1]}" for r in row]
            self.student_id_in_section = [r[0] for r in row]
            self.student_name_in_section = [r[1] for r in row]
        self.status = status

    def sectioon_info_student(self,section_code):  # to display section information
        self.section_code = section_code
        row= section_db.execute("SELECT cours_code, cours_name, sections, capacity, times FROM sections WHERE section_code = ?",(self.section_code,),fetchone=True)
        if row==None:
            return f"{self.section_code}, Section not found"
        self.section_code=row[0]
        self.subject_name=row[1]   
        self.section_name=row[2]
        self.capacity=row[3]
        self.schedule=row[4]
        return f"Section Code: {self.section_code}, Subject Name: {self.subject_name}, Section Name: {self.section_name}, Capacity: {self.capacity}, Schedule: {self.schedule}"
        ###we still need structors name in the database to return it here

        ### return section name, subject name, instructor, schedule (will be used by student)
       

    def open_section(self):  # to open section for enrollment
        ### status can be changed to open if capacity not zero
        pass

    def is_full(self, section_code):  # to check if section is full
        self.section_code = section_code
        row= section_db.execute("SELECT capacity FROM sections WHERE section_code = ?",(self.section_code,),fetchone=True)
        if row==None:
            return f"{self.section_code}, Section not found"
        if len(self.enrolled_students)>=row[0]: ### since there is no data base fore enrolled student i'm going to write it like this (temporary)
            return True
        else:
            return False
        ### this can compare len(enrolled_students) with capacity
        

    def view_enrolled_students(self,):  # to view all enrolled students
        print(self.enrolled_students)
        ### in the future can return/print list of all enrolled students
        pass

    def has_time_conflict(self, student_id, section_code):  # to check time conflict with student's schedule
        ### I will need to inrolle some students in some sections to be able to check time conflict fartheremore Data base has to add more sections 
        pass

    def prerequisites_met(self, completed_subjects):  # to check if student meets prerequisites
        ### must compare subject prerequisites with completed_subjects list
        pass
    def student_is_existing(self, student_id):  # to check if student is already enrolled in the section
        try:
            student_id = int(student_id)
        except: 
            return "Student ID must be an integer."
        if student_id in self.student_id_in_section:
            return True
        else:
            return False

    def all_conditions_met(self): # to check if all conditions are met for enrollment
        if self.is_full():
            return False , f"the section {self.section_name} is full"
        if not self.prerequisites_met():
            return False
        if self.has_time_conflict():
            return False
    def enroll_student_in_section(self, student_id):  # to enroll a student in the section for data only (admin use only)
         ### I will need to inrolle some students in some sections to be able to do this 
        ### just for data tracking, actual enrollment logic is handled in student class
        ### notce that when considering database design, function will have to update the database instead of just appending to list
        pass

    def drop_student_from_section(self, student_id):  # to drop a student from the section for data only (admin use only)
         ### I will need to inrolle some students in some sections to be able to do this
        ### notce that when considering database design, function will have to update the database instead of just removing from list
        pass

    def new_capacity(self, new_capacity):  # to expand the capacity of the section
        try:
            new_capacity = int(new_capacity)
        except: 
            return "Capacity must be an integer."
        if new_capacity < len(self.student_id_in_section):
            return "New capacity cannot be less than the number of enrolled students."
        self.capacity = new_capacity
        section_db.execute("UPDATE sections SET capacity = ? WHERE section_code = ?", (self.capacity, self.section_code), commit=True)
         ### it's very very very very importanat to abdate line 213 when database design is apdeted and add sereal number for each section
        return f"Section {self.section_name} capacity updated to {self.capacity}."

        ### can be used by admin to increase capacity
        

    def remaining_seats(self):  # to check remaining seats in the section
        ### should return capacity - len(enrolled_students)
        ### I will need to inrolle some students in some sections to be able to do this
        pass


# _______________________________________________________________________________________________________________

users_db = Database("Users.db")  ### since student class will use database a lot i think its better to create database object here
class student(user):
    def __init__(self,Id,username=None,email=None,major=None,password=None,enrolled_subjects=None,completed_subjects=None,status="inactive",GPA=None,):
        super().__init__(username, password, email, status, Id)
        self.GPA = GPA
        self.enrolled_subjects = enrolled_subjects if enrolled_subjects is not None else [] # list of section codes the student is currently enrolled in
        self.completed_subjects = completed_subjects if completed_subjects is not None else []  # list of subject codes the student has completed
        self.current_credits = 0 ### total credits of current enrolled subjects for checking max credits allowed per semester not current total subjects
        self.email = f"{self.username}{self.Id}@kau.edu.sa" if email is None else email
        majors_row=users_db.execute("SELECT major fROM students WHERE Id = ?", (self.Id,), fetchone=True)
        if majors_row==None:
            self.major=major
        self.major=majors_row[0]
        

    # def generate_unique_id(self): # generates random id for each student
    #     while True:
    #         Id = random.randint(100000, 999999)  # Generate a random 6-digit ID
    #         if Id not in existing_ids and Id not in emails:  # Check that the ID is not in emails or existing_ids
    #             existing_ids.add(Id)  # Add the ID to the set
    #             return Id  # Return the unique ID
    # this can be used later if we want automatic ID generation

    def test(self):
        ### this function used before for quick testing
        pass

    def add_term(self):  # to add or define new term
        ### i think we will need table for term later in database
        pass

    def return_info(self):  # to return student information
        ### similar to display_info but can return in different format
        pass

    def display_info(self):  # to display student information
        ### can extend parent display_info to include GPA, major, etc.
        pass

    def enroll_subject(self, section_code):  # to enroll student in a subject section
        ### must check prerequisites, time conflict, section capacity, max credit hours etc.
        ### this function will be main function for student enrollment logic
        pass

    def drop_subject(self, section_code):  # to drop a subject section for the student
        ### must update enrolled_subjects list and database
        pass

    def view_enrolled_subjects(self):  # to view all enrolled subjects for the student
        ### this should show all current sections that student enrolled in
        pass

    def calculate_GPA(self):  # to calculate GPA based on completed subjects and their grades
        if self.Id != int(self.Id):
            return "Student ID must be an integer."
        row=users_db.execute("SELECT major fROM students WHERE Id = ?", (self.Id,), fetchone=True)
        if row==None:
            return f"{self.Id}, Student not found"
        if self.major=="Electrical communication and electronics engineering":
            ### GPA calculation logic for this major
            pass
        if self.major=="Electrical computer engineering":
            ### GPA calculation logic for this major
            pass
        if self.major=="Electrical power and machines engineering":
            pass
        if self.major=="Electrical biomedical engineering":
            pass
        ### must use completed_subjects and grades (when database design is complete)
        pass

    ### not sure if these all the methods needed for student class

    def transcript(self):  # to generate a transcript of completed subjects and grades
        ### will be used later to print full academic record
        pass


# _______________________________________________________________________________________________________________


class admin(user):
    def __init__(self, username, password=None, email=None, status="inactive", Id=None):
        super().__init__(username, password, email, status, Id)
        self.password = chr(random.randint(97,97+25)) + str(random.randint(1000000,9999999))
        

            
        


    def add_subject(self, section_code, student_id):  # to add a subject to a student
        ### later this will probably call student.enroll_subject with correct ID and section_code
        pass

    def remove_subject(self, section_code, student_id):  # to remove a subject from a student
        ### later this will probably call student.drop_subject with correct ID and section_code
        ### we might create student object from database data here
        pass

    def display_student_in_section(self, section_code):  # to display students in a section
        ### can create section object then call section.display_student_in_section
        pass

    # def view_all_students(self, section_code=None): # to view all students, optionally filtered by section
    #     ### this can be implemented later using database design
    #     pass

    def find_student(self, student_id):  # to find student by id
        ### must search in database for student_id and return student info
        pass

    def view_all_subjects(self, available_only):  # to view all available subjects
        ### if available_only True, only show open sections
        pass

    def find_sections(self, subject_code):  # to view sections for a specific subject
        ### must search in database for sections with this subject_code
        pass

    def expand_capacity(self, section_code, new_capacity):  # to expand section capacity
        ### must check some constraints then call section.new_capacity
        pass

    def reduce_capacity(self, section_code, new_capacity):  # to reduce section capacity
        ### must ensure not less than number of already enrolled students
        pass

    def avilable_subjects(self, student_id):  # to view subjects that a student can enroll in
        ### here as well i have to understand data base more to implement this function
        ### must check prerequisites, time conflicts, capacity etc.
        pass


# Example test (from original file) - commented to avoid running automatically
# st1 = student('ABDULAZIZ', 1234, 'Electrical communication and electronics engineering', Id=2490248)
# print(st1.display_info())
# s1 = student(username='tariq', password='Electrical communication and electronics',
#              email='tariq@stu.kau.edu.sa', Id='2430020')
# print(s1.display_info())

