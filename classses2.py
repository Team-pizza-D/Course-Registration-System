import random
import sqlite3
import os



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
# _______________________________________________________________________________________________________________

class user:
    user_count = 0  # class variable to keep track of user IDs
    def __init__(self, username=None, password=None, email=None, id=None):
        self.id = id
        self.username = username
        self.email = email
        self.password = password

         ### if id is provided check if user exists in database and load data
         ### else generate new user with provided or generated data

        if self.is_existing():
            # try:
                row = users_db.execute("SELECT username,password, email FROM admins WHERE id = ? UNION SELECT username, password,email FROM instructors WHERE id = ? UNION SELECT username, password, email FROM students WHERE id = ?", (id, id, id), fetchone=True)
                self.username = row[0]
                self.password = row[1]
                self.email = row[2]
                self.id = id
            # except sqlite3.Error as e:
            #     print(f"Database error: {e}")
        
        else:
            if username is None:
                self.username = "user"
            else:
                self.username = username

            if id is None:
                self.id = self.generate_unique_id()
            else:
                self.id = id
            if email is None:
                self.email = self.generate_email()
            else:
                self.email = email
            if password is None:
                self.password = self.generate_password()
            else:
                self.password = password
        

        
    def is_existing(self):  # to check if user exists in database
        row = users_db.execute("SELECT id FROM admins WHERE id = ? UNION SELECT id FROM instructors WHERE id = ? UNION SELECT id FROM students WHERE id = ?", (self.id, self.id, self.id), fetchone=True)
        return True if row else False
    
    def display_info(self):  # to display user information
        return f"Username: {self.username}, Email: {self.email}, ID: {self.id}"
    def is_admin(self):  # to check if user is admin
        # This will later be known by which table is the information in (student or admin)
        return True if isinstance(self, admin) else False

    def is_student(self):  # to check if user is student
        # This will later be known by which table is the information in (student or admin)
        return True if isinstance(self, student) else False
    
    def is_instructor(self):  # to check if user is instructor
        #This will later be known by which table is the information in (student or admin)
        return True if isinstance(self, instructor) else False
    
    def generate_unique_id(self):  # generates unique user ID
        existing_ids_row = users_db.execute("SELECT id FROM admins UNION SELECT id FROM instructors UNION SELECT id FROM students", fetchall=True)
        existing_ids = {row[0] for row in existing_ids_row}
        id = random.randint(1000000000, 9999999999)
        while id in existing_ids:
            id = random.randint(1000000000, 9999999999)
        return id
    
    def generate_email(self):  # generates email based on username and ID
        if self.is_student():
            email = f"{self.username}{self.id}@stu.kau.edu.sa"
        else:
            email = f"{self.username}{self.id}@kau.edu.sa"
        return email
    
    def generate_password(self):  # generates random password
        m = self.username.find(" ")
        first_name = ""
        for i in range(m):
            first_name += self.username[i]
        password = str(first_name) + str(random.randint(100000, 999999))
        return password
    
        
    

class subject:  ### Data base team said that this is currently not needed but i think its better to have it for future use
    def __init__(self, subject_name, subject_code=None, prerequisites=None):
        self.subject_code = subject_code
        self.subject_name = subject_name
        self.enrolled_students = []
        self.prerequisites = prerequisites if prerequisites is not None else []
        while True:
            subject_term= courses_db.execute("SELECT terms FROM computer WHERE course_code = ?", (self.subject_name,), fetchone=True)
            if subject_term == None:
                subject_term= courses_db.execute("SELECT terms FROM communication WHERE course_code = ?", (self.subject_name,), fetchone=True)
                if subject_term == None:
                    subject_term= courses_db.execute("SELECT terms FROM power WHERE course_code = ?", (self.subject_name,), fetchone=True)
                    if subject_term == None:
                        subject_term= courses_db.execute("SELECT terms FROM biomedical WHERE course_code = ?", (self.subject_name,), fetchone=True)
                        if subject_term == None:
                            self.subject_term= subject_term
                            break
                        else:
                            self.subject_term= subject_term[0]
                            break
                else:
                    self.subject_term= subject_term[0]
                    break


            else: 
                self.subject_term= subject_term[0]
                break
        


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

class section(subject):
    # def __init__(self,section_name=None,section_code=None,capacity = 0,enrolled_students=None, schedule=None, instructor=None, prerequisites=None, status="closed"):
    def __init__(self,section_name,subject_name=None,subject_code=None,schedule=None,capacity=0,instructor=None,prerequisites=None):
        ### this constructor version is the one we will use, we have to discuss it and compare it with main (the line above)
        super().__init__(subject_name, subject_code, prerequisites)
        self.schedule = schedule
        self.instructor = instructor
        self.capacity = capacity
        # self.enrolled_students = enrolled_students if enrolled_students is not None else [] ### I dont think we need this
        self.section_name = section_name
        self.student_in_section_db = Database("Users.db")  ### as menshed I dont know what is the file name one i know it and know the database design i will implement it to be completely functional
        row = self.student_in_section_db.execute("SELECT student_id, student_name FROM enrollments WHERE section = ?", (self.section_name,), fetchall=True)
        if not row:
            self.enrolled_students = []
            self.student_id_in_section = []
            self.student_name_in_section = []
        else:
            # Build lists from query rows without overwriting the Database object
            self.enrolled_students = [f"{r[0]} - {r[1]}" for r in row]
            self.student_id_in_section = [r[0] for r in row]
            self.student_name_in_section = [r[1] for r in row]
        find_subject_list=courses_db.execute("SELECT course_code FROM courses WHERE section= ?",(self.section_name,),fetchone=True)
        if find_subject_list==None:
            return None
        find_subject= find_subject_list[0].strip()
        
        self.subject_= subject(find_subject)
        self.section_term= self.subject_.subject_term
        self.subject=self.subject_.subject_name

    def sectioon_info_student(self):  # to display section information
        row= courses_db.execute("SELECT course_code, course_name, sections, capacity, times FROM sections WHERE sections = ?",(self.section_name,),fetchone=True) ### database design must be abdated to include instructor name and creat a table name sections
        if row==None:
            return f"{self.section_name}, Section not found"
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
    def section_is_existing(self):  # to check if section exists
        row= courses_db.execute("SELECT section FROM Courses WHERE section = ?",(self.section_name,),fetchone=True)
        if row==None:
            return False
        else:
            return True

    def is_full(self):  # to check if section is full
        ### allways use the function section_is_existing before using this function to avoid errors
        row= courses_db.execute("SELECT capacity FROM Courses WHERE section = ?",(self.section_name,),fetchone=True)
        if row==None:
            return True
        if len(self.enrolled_students)>=int(row[0]): ### since there is no data base fore enrolled student i'm going to write it like this (temporary)
            return True
        else:
            return False
        ### this can compare len(enrolled_students) with capacity
        

    def view_enrolled_students(self):  # to view all enrolled students
        print(self.enrolled_students)
        ### in the future can return/print list of all enrolled students
        pass

    def has_time_conflict(self, student_id):  # to check time conflict with student's schedule
        self.section_time=courses_db.execute("SELECT time FROM Courses WHERE section = ?",(self.section_name,),fetchone=True)
        self.section_time=self.section_time[0].strip()
        student_schedule_rows= self.student_in_section_db.execute("SELECT section FROM enrollments WHERE student_id = ?", (student_id,), fetchall=True)
        student_schedules = []
        for row in student_schedule_rows:
            sec_time = courses_db.execute("SELECT time FROM Courses WHERE section = ?", (row[0],), fetchone=True)
            if sec_time:
                student_schedules.append(sec_time[0].strip())
        for sched in student_schedules:
            if sched == self.section_time:
                return True
        return False
        ### I will need to inrolle some students in some sections to be able to check time conflict fartheremore Data base has to add more sections 
        

    def prerequisites_met(self, student_id,):  # to check if student meets prerequisites
        
        try:
            student_id = int(student_id)
        except: 
            return False , "Student ID must be an integer."
        The_id= student(id=student_id)
        row1=users_db.execute("SELECT course , letter_grade FROM grades WHERE student_id = ?", (The_id.id,), fetchall=True)
        students_taken_subject_with_grades={}
        for cours,letter_grade in row1:
            students_taken_subject_with_grades[cours]=letter_grade
        student_completed_subjects=list(students_taken_subject_with_grades.keys()) 
        
        

        row=users_db.execute("SELECT major , term FROM students WHERE id = ?", (The_id.id,), fetchone=True)
        student_term=row[1]

        if row[0]==None:
            return  False , f"{The_id.Id}, Student not found"
        
        section_subject_row=courses_db.execute("SELECT course_code FROM Courses WHERE section = ?", (self.section_name,), fetchone=True)
        if section_subject_row==None:
            return False , f"Section {self.section_name} not found"
        section_subject_code= section_subject_row[0].strip()
        

        if The_id.major.strip()=="Electrical communication and electronics engineering":
            subject_db=courses_db.execute("SELECT prerequisites FROM communication WHERE course_code = ?", (section_subject_code,), fetchone=True)
            if subject_db==None:
                prerequisites=None
            else:
                prereq_str=subject_db[0]
                if prereq_str is None or prereq_str.strip()=="":
                    return True , f"The subject has no prerequisites."
                else:
                    prerequisites=prereq_str.split(",")
            

            
        
        if The_id.major.strip()=="Electrical computer engineering":
            subject_db=courses_db.execute("SELECT prerequisites FROM computer WHERE course_code = ?", (section_subject_code,), fetchone=True)
            if subject_db==None:
                prerequisites=None
            else:
                prereq_str=subject_db[0]
                if prereq_str is None or prereq_str.strip()=="":
                    return True , f"The subject has no prerequisites."
                else:
                    prerequisites=prereq_str.split(",")


        if The_id.major.strip()=="Electrical power and machines engineering":
            subject_db=courses_db.execute("SELECT prerequisites FROM power WHERE course_code = ?", (section_subject_code,), fetchone=True)
            if subject_db==None:
                prerequisites=None
            else:
                prereq_str=subject_db[0]
                if prereq_str is None or prereq_str.strip()=="":
                    return True , f"The subject has no prerequisites."
                else:
                    prerequisites=prereq_str.split(",")


        if The_id.major.strip()=="Electrical biomedical engineering":
            subject_db=courses_db.execute("SELECT prerequisites FROM biomedical WHERE course_code = ?", (section_subject_code,), fetchone=True)
            if subject_db==None:
                prerequisites=None
            else:
                prereq_str=subject_db[0]
                if prereq_str is None or prereq_str.strip()=="":
                    return True , f"The subject has no prerequisites."
                else:
                    prerequisites=prereq_str.split(",")

        if prerequisites==None:
            return False , f"Section {self.section_name} not in study plan of {The_id.major}" 
        elif str(prerequisites).strip()=="":
            return True , "No prerequisites for this section."
        for prereq in prerequisites:
            preq= prereq.strip()
            grade= students_taken_subject_with_grades.get(preq)
            if grade== None:
                return False , f"Prerequisite {preq} not completed."
            if  grade == "F":
                return False , f"Prerequisite {preq} not passed."
        for prereq in prerequisites:
            prereq= prereq.strip()
            if prereq not in student_completed_subjects:
                return False , f"Prerequisite {prereq} not completed."
            
        the_subject= subject(section_subject_code.strip())
        if the_subject.subject_term > student_term:
            return False , f"{section_subject_code} is not in the plane fore the term number {student_term}."
        return True , "All prerequisites met."    

    def student_is_existing(self, student_id):  # to check if student is already enrolled in the section
        if student_id in self.student_id_in_section:
            return True
        else:
            return False
    def student_is_real(self, student_id):  # to check if student exists in the database
        row= users_db.execute("SELECT id FROM students WHERE id = ?", (student_id,), fetchone=True)
        if row==None:
            return False
        else:
            return True

    def one_section_for_subject(self, student_id):  # to ensure student is enrolled in only one section per subject
        row= users_db.execute("SELECT section FROM enrollments WHERE student_id = ?", (student_id,), fetchall=True)
        student_sections = [r[0] for r in row]
        for sec in student_sections:
            course_row=courses_db.execute("SELECT course_code FROM Courses WHERE section = ?", (sec,), fetchone=True)
            if course_row==None:
                continue
            course_code= course_row[0]
            if course_code.strip() == self.subject.strip():
                return True , f"Student with ID {student_id} is already enrolled in section {sec} for subject {self.subject}."
        return False , f""
        ### I will need to inrolle some students in some sections to be able to do this 
        pass    

    def all_conditions_met(self,student_id): # to check if all conditions are met for enrollment

        if not self.student_is_real(student_id):
            return False , f"student with ID {student_id} does not exist"
        if self.student_is_existing(student_id):
            return False , f"student with ID {student_id} is already enrolled in section {self.section_name}"
        if not self.section_is_existing():
            return False , f"section {self.section_name} does not exist"
        okay,message= self.one_section_for_subject(student_id)
        if  okay:
            return False , message
        if self.is_full():
            return False , f"the section {self.section_name} is full"
        okay , message =  self.prerequisites_met(student_id) ### this function must return tuple (bool,str)
        if not okay:
            return False , message
        # if self.has_time_conflict(student_id):
        #     return False, f"Time conflict with student's schedule."
        return True , f"All conditions met for enrollment."
    
    def enroll_student_in_section(self, student_id):  # to enroll a student in the section for data only (admin use only)
        okay , message = self.all_conditions_met(student_id)
        if not okay:
            return False , message
        row=courses_db.execute("SELECT instructor, course_code FROM Courses WHERE section = ?", (self.section_name,), fetchone=True)
        self.instructor=row[0]
        course_code=row[1]
        student_name_row=users_db.execute("SELECT username FROM students WHERE id = ?", (student_id,), fetchone=True)
        student_name= student_name_row[0]

        self.student_in_section_db.execute("INSERT INTO enrollments (student_id, student_name, section,instructor,course) VALUES (?, ?, ?, ?,?)", (student_id, student_name, self.section_name, self.instructor,course_code), commit=True)
        self.enrolled_students.append(f"{student_id} - {student_name}")
        self.student_id_in_section.append(student_id)
        self.student_name_in_section.append(student_name)
        users_db.execute("INSERT INTO grades (student_id, course) VALUES (?, ?)", (student_id, self.subject), commit=True)
         ### it's very very very very importanat to abdate line 213 when database design is apdeted and add sereal number for each section

        return True , f"Student with ID {student_id} successfully enrolled in section {self.section_name}."

        

        
            
           
         ### I will need to inrolle some students in some sections to be able to do this 
        ### just for data tracking, actual enrollment logic is handled in student class
        ### notce that when considering database design, function will have to update the database instead of just appending to list


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
        courses_db.execute("UPDATE sections SET capacity = ? WHERE sections = ?", (self.capacity, self.section_name), commit=True)
        return f"Section {self.section_name} capacity updated to {self.capacity}."

        ### can be used by admin to increase capacity
        

    def remaining_seats(self):  # to check remaining seats in the section
        ### should return capacity - len(enrolled_students)
        ### I will need to inrolle some students in some sections to be able to do this
        pass


# _______________________________________________________________________________________________________________

class student(user):
    def __init__(self,id=None,username = None,email=None,major=None,password=None,enrolled_subjects=None,completed_subjects=None,GPA=None,database=False):
        super().__init__(username, password, email, id)
        self.enrolled_subjects = enrolled_subjects if enrolled_subjects is not None else [] # list of section codes the student is currently enrolled in
        self.completed_subjects = completed_subjects if completed_subjects is not None else []  # list of subject codes the student has completed
        self.current_credits = 0 ### total credits of current enrolled subjects for checking max credits allowed per semester not current total subjects
        # self.email = f"{self.username}{self.Id}@kau.edu.sa" if email is None else email
        # majors_row=users_db.execute("SELECT major fROM students WHERE id = ?", (self.id,), fetchone=True)
        # if majors_row==None:
        #     self.major=major
        # self.major=majors_row[0]
        self.major = major
        if GPA is None:
            self.GPA = self.calculate_GPA()
        self.database = database
        ### set database to true if you want to insert this student into database upon creation
        ### eg. student = student("azad", database=True)
        if self.database:
            try:
                users_db.execute(
                    "INSERT INTO students (username, password, email, Id,major) VALUES (?, ?, ?, ?, ?)",
                    (self.username, self.password, self.email, self.id,self.major),
                    commit=True,
                    )
            except sqlite3.IntegrityError:
                print(f"Student with ID {self.id} already exists in the database.")
        # else:
        #     row=users_db.execute(
        #         "SELECT username, password, email, Id, major FROM students WHERE Id = ?", (self.id,), fetchone=True
        #     )
        #     self.username = row[0]
        #     self.password = row[1]
        #     self.email = row[2]
        #     self.major = row[4]
            pass ### I will do this later to select student data from database if database is false         
    def return_id(self):
        return self.id
    
    def display_info(self):  # to display student information
        return super().display_info() + f", Major: {self.major}, GPA: {self.GPA} "

    def enroll_subject(self, section_code):  # to enroll student in a subject section
        sec=section(section_name=section_code)
        okay,massege =sec.enroll_student_in_section(self.id)
        return print(okay, massege)

    def drop_subject(self, section_code):  # to drop a subject section for the student
        sect=section(section_name=section_code)
        okay,massege =sect.drop_student_from_section(self.id)
        return okay, massege

    def view_enrolled_subjects(self):  # to view all enrolled subjects for the student
        row = users_db.execute("SELECT section FROM enrollments WHERE student_id = ?", (self.id,), fetchall=True)
        print(row)
        if row is None or len(row) == 0:
            return f"{self.id}, No enrolled subjects found"
        enrolled_sections = [r[0] for r in row]
        return enrolled_sections

        ### this should show all current sections that student enrolled in
        pass


    def calculate_GPA(self):  # to calculate GPA based on completed subjects and their grades
        

        #map letter grades to grade points
        grade_map = {
            'A+':5.0, 'A': 4.75, 'B+': 4.5, 'B': 4.0, 'C+': 3.5,
            'C': 3.0, 'D+': 2.5, 'D': 2.0, 'F': 1.0
        }
        
        Major_table_map = {
                           'Electrical communication and electronics engineering': "Communication",
                            'Electrical computer engineering' : "Computer",
                            'Electrical biomedical engineering' : "Biomedical",
                            'Electrical power and machines engineering' : "Power"
        }
            
        #find the students major to determine used table
        major_row = users_db.execute("SELECT major FROM students WHERE id = ?", (self.id,), fetchone=True)
        
        if major_row is None:
            return f"Student with ID {self.id} not found."
        major = major_row[0]
        subjects_table = Major_table_map.get(major)
        if subjects_table is None:
            return f"Major '{major}' not recognized."
        
        #correct table found, now fetch completed subjects and grades

        conn = sqlite3.connect("Users.db")
        cur = conn.cursor()
        courses_db_path = os.path.join(os.getcwd(), 'courses.db')
        cur.execute(f"ATTACH DATABASE '{courses_db_path}' AS courses_db")

        query = f"""
                       SELECT g.course , g.Letter_grade , s.credit
                       FROM grades AS g
                       JOIN courses_db."{subjects_table}" AS s ON g.course = s.course_code
                       WHERE g.student_id = ?
                       """
        cur.execute(query, (self.id,))
        rows = cur.fetchall()

        if not rows:
            conn.close()
            return f"No completed subjects found for student ID {self.id}."
        total_credits = 0
        total_points = 0
        for course, letter_grade, credit in rows:
            grade_point = grade_map.get(letter_grade, 0)
            total_credits += credit
            total_points += grade_point * credit
            
        if total_credits == 0:
            conn.close()
            return "No credits found for GPA calculation."
        
        gpa = total_points / total_credits
        conn.close()
        
        return round(gpa, 2)

    ### not sure if these all the methods needed for student class

    def transcript(self):  # to generate a transcript of completed subjects and grades
        row = users_db.execute("SELECT course, Letter_grade FROM grades WHERE student_id = ?", (self.id,), fetchall=True)
        if row==None or len(row)==0:
            return f"{self.id}, No completed subjects found"
        transcript = {r[0]: r[1] for r in row}
        return transcript
        ### will be used later to print full academic record
        pass
        


# _______________________________________________________________________________________________________________
class instructor(user):
    def __init__(self, username, subject, sections ,password=None, email=None, id=None, database=False):
        super().__init__(username, password, email, id)
        self.subject = subject  # subject assigned to the instructor
        self.sections = sections if sections is not None else []  ### will be abdated later when database design is complete to take sections from database directly
        self.database = database

        if self.database:

            users_db.execute(
                "INSERT INTO instructors (username, password, email, id) VALUES (?, ?, ?, ?)",
                (self.username, self.password, self.email,self.id),
                commit=True,
            )
    def display_info(self):
        return super().display_info() + f", Subject: {self.subject}"     
    def __add_grade(self, student_id, section_code, grade):  # to add grade for a student in a section
        pass
    def show_students(self,section_code):  # to show all students in a section
        self.section= section(section_name=section_code)
        self.section.view_enrolled_students()

# _______________________________________________________________________________________________________________

class admin(user):
    def __init__(self, username=None, password=None, email=None, id=None, database=False):
        super().__init__(username, password, email, id)
        # self.password = chr(random.randint(97,97+25)) + str(random.randint(1000000,9999999))
        self.database= database
        ### set database to true if you want to insert this admin into database upon creation
        ### eg. admin = admin("azad", database=True)

        if self.database == True:
            
            users_db.execute(
                "INSERT INTO admins (username, password, email, id) VALUES (?, ?, ?, ?)",
                (self.username, self.password, self.email,self.id),
                commit=True,
            )
        

            
        


    def add_subject(self, section_code, student_id):  # to add a subject to a student
        ### later this will probably call student.enroll_subject with correct ID and section_code
        sect=section(section_name=section_code)
        okay,massege = sect.enroll_student_in_section(student_id)
        return okay, massege

    def remove_subject(self, section_code, student_id):  # to remove a subject from a student
        sect=section(section_name=section_code)
        okay,massege =sect.drop_student_from_section(student_id)
        return okay, massege

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
        sec=section(section_name=section_code)
        massege= sec.new_capacity(new_capacity)
        return massege
    def add_grade(self, student_id, course_code, grade):  # to add grade for a student in a section

        # instr= instructor(username="temp", subject="temp", sections="temp")
        # instr.__add_grade(student_id, section_code, grade)
        ### must create instructor object to call its __add_grade method
        pass



# Example test (from original file) - commented to avoid running automatically
# st1 = student('ABDULAZIZ', 1234, 'Electrical communication and electronics engineering', Id=2490248)
# print(st1.display_info())
# s1 = student(username='tariq', password='Electrical communication and electronics',
#              email='tariq@stu.kau.edu.sa', Id='2430020')
# print(s1.display_info())
# instructor1 = instructor(username='dr.ahmed', password='instructorpass',email="ahmad@gmail.com",subject="computer science",Id=3001)
# print(instructor1.display_info())
# instructor1.show_students("CS101")
# b=section("4f")
# print(b.sectioon_info_student())
