import random
import sqlite3
import os
import bcrypt

class Database: # SQLite database helper class

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
            result = cur.fetchone() # to select single row
        elif fetchall:
            result = cur.fetchall() # to select multiple rows

        if commit:
            conn.commit() # for insert, update, delete operations

        conn.close()
        return result
# _______________________________________________________________________________________________________________
# open database connection
users_db = Database("Users.db")
courses_db = Database("courses.db")
# _______________________________________________________________________________________________________________

class user: # main user class that will be inherited by student, instructor, admin
    user_count = 0  # class variable to keep track of user IDs
    def __init__(self, username=None, password=None, email=None, id=None): # user constructor
        self.id = id
        self.username = username
        self.email = email
        self.password = password



        if self.is_existing():
                row = users_db.execute("SELECT username,password, email FROM admins WHERE id = ? UNION SELECT username, password,email FROM instructors WHERE id = ? UNION SELECT username, password, email FROM students WHERE id = ?", (id, id, id), fetchone=True)
                self.username = row[0]
                self.password = row[1]
                self.email = row[2]
                self.id = id
        
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
    
    
    def is_admin(self):  # to check if user is admin
        # This will later be known by which table is the information in (student or admin)
        row = users_db.execute("SELECT id FROM admins WHERE id = ?", (self.id,), fetchone=True)
        if row:
            return True
        else:
            return False

    def return_id(self):
        return self.id

    def is_student(self):  # to check if user is student
        # This will later be known by which table is the information in (student or admin)
        row = users_db.execute("SELECT id FROM students WHERE id = ?", (self.id,), fetchone=True)
        if row:
            return True
        else:
            return False
    
    def is_instructor(self):  # to check if user is instructor
        #This will later be known by which table is the information in (student or admin)
        row = users_db.execute("SELECT id FROM instructors WHERE id = ?", (self.id,), fetchone=True)
        if row:
            return True
        else:
            return False
    
    def generate_unique_id(self):  # generates unique user ID
        existing_ids_row = users_db.execute("SELECT id FROM admins UNION SELECT id FROM instructors UNION SELECT id FROM students", fetchall=True)
        existing_ids = {row[0] for row in existing_ids_row}
        id = str(random.randint(1000000, 9999999)).strip()
        while id in existing_ids:
            id = str(random.randint(1000000, 9999999)).strip()
        return id
    
    def generate_email(self):  # generates email based on username and ID
        new_username = self.username.replace(" ", "")
        if self.is_student():
            email = f"{new_username}{self.id}@stu.kau.edu.sa"
        else:
            email = f"{new_username}{self.id}@kau.edu.sa"
        return email
    
    def generate_password(self):  # generates random password
        m = self.username.find(" ")
        first_name = ""
        for i in range(m):
            first_name += self.username[i]
        password = str(first_name) + str(random.randint(100000, 999999))
        return password
    
    def correct_password(self, password):  # to check if provided password matches user's password
        row = users_db.execute("SELECT hashed_password FROM admins WHERE id = ? UNION SELECT hashed_password FROM instructors WHERE id = ? UNION SELECT hashed_password FROM students WHERE id = ?", (self.id, self.id, self.id), fetchone=True)
        hashed_password_in_db = row[0] if row else None
        return bcrypt.checkpw(password.encode() , hashed_password_in_db.encode()) # comparing by hashed passwords (saftier)
# _______________________________________________________________________________________________________________
class subject: # subject class 

    def __init__(self, subject_name, subject_code=None,): # subject constructor
        self.subject_code = subject_code
        self.subject_name = subject_name
        prerequisites_row= courses_db.execute("SELECT prerequisites FROM Courses WHERE course_code = ?", (self.subject_name,), fetchone=True)
        if prerequisites_row==None or prerequisites_row[0]==None or prerequisites_row[0].strip()=="":
            self.prerequisites = [] # no prerequisites
        else:
            prereq_str= prerequisites_row[0]
            self.prerequisites = [prereq.strip() for prereq in prereq_str.split(",")] # list of prerequisites
        while True: # to get subject term from the correct major table
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
        

    def already_graded(self, student_id):  # to check if student has already been graded in the section
        row= users_db.execute("SELECT numeric_grade FROM grades WHERE student_id = ? AND course = ?", (student_id, self.subject_name,), fetchone=True)
        if row==None or row[0]==None or len(row[0])==0:
            return False
        else:
            return True
    
    def is_existing(self):  # to check if subject exists in database
        row= courses_db.execute("SELECT course_code FROM Courses WHERE course_code = ?",(self.subject_name,),fetchone=True)
        if row==None or len(row[0])==0:
            return False
        else:
            return True
    
    def remove_prerequisite(self, prerequisite):  # to remove a prerequisite from the subject
        if  "," in prerequisite:
            prereq_list= prerequisite.split(",")
            for preq in prereq_list:
                preq= preq.strip().upper()
                if preq=="":
                    continue
                if preq==self.subject_name:
                    return False , f"Course cannot be a prerequisite of itself."
                if not subject(preq.strip().upper()).is_existing():
                    return False , f"Prerequisite course with code {preq.strip().upper()} does not exist."
                if preq in self.prerequisites:
                    self.prerequisites.remove(preq)
                    courses_db.execute("UPDATE Courses SET prerequisites = ? WHERE course_code = ?", (", ".join(self.prerequisites), self.subject_name), commit=True)
                    return True , f"Prerequisite {preq} removed from subject {self.subject_name}."
                else:
                    return False , f"Prerequisite {preq} not found in subject {self.subject_name}.  "
        else:
            
            prerequisite= prerequisite.strip().upper()
            if prerequisite==self.subject_name:
                return False , f"Course cannot be a prerequisite of itself."
            if not subject(prerequisite).is_existing():
                return False , f"Prerequisite course with code {prerequisite} does not exist. reminder if you are trying to delete more than one prerequisite, separate them with commas"
            if prerequisite in self.prerequisites:
                self.prerequisites.remove(prerequisite)
                courses_db.execute("UPDATE Courses SET prerequisites = ? WHERE course_code = ?", (", ".join(self.prerequisites), self.subject_name), commit=True)
                return True , f"Prerequisite {prerequisite} removed from subject {self.subject_name}."
            else:
                return False , f"Prerequisite {prerequisite} not found in subject {self.subject_name}. (reminder if you are trying to delete more than one prerequisite, separate them with commas)"
        
  
        
    
    def add_prerequisite(self, prerequisite):  # to add a prerequisite to the subject
        if  "," in prerequisite:
            prereq_list= prerequisite.split(",")
            for preq in prereq_list:
                if preq=="":
                    continue
                if preq==self.subject_name:
                    return False , f"Course cannot be a prerequisite of itself."
                if not subject(preq.strip().upper()).is_existing():
                    return False , f"Prerequisite course with code {preq.strip().upper()} does not exist."
                if subject( preq.strip().upper()).subject_term > self.subject_term:
                    return False , f"Prerequisite course with code {preq.strip().upper()} is in a higher term than the subject {self.subject_name}."
                preq= preq.strip().upper()
                if preq not in self.prerequisites:
                    self.prerequisites.append(preq)
                    courses_db.execute("UPDATE Courses SET prerequisites = ? WHERE course_code = ?", (", ".join(self.prerequisites), self.subject_name), commit=True)
                return True , f"Prerequisites {', '.join(prereq_list)} added to subject {self.subject_name}."
            else:
                return False , f"Prerequisite {preq} already exists in subject {self.subject_name}."
        else:
            prerequisite= prerequisite.strip().upper()
            if prerequisite==self.subject_name:
                return False , f"Course cannot be a prerequisite of itself."
            if not subject(prerequisite).is_existing():
                return False , f"Prerequisite course with code {prerequisite} does not exist. reminder if you are trying to add more than one prerequisite, separate them with commas"
            if prerequisite not in self.prerequisites:
                self.prerequisites.append(prerequisite)
                courses_db.execute("UPDATE Courses SET prerequisites = ? WHERE course_code = ?", (", ".join(self.prerequisites), self.subject_name), commit=True)
                return True , f"Prerequisite {prerequisite} added to subject {self.subject_name}."
            else:
                return False , f"Prerequisite {prerequisite} already exists in subject {self.subject_name}."
    
    def get_all_sections(self):  # to get all sections of the subject
        row= courses_db.execute("SELECT section FROM Courses WHERE course_code = ?",(self.subject_name.strip().upper(),),fetchall=True)
        if row==None or len(row)==0:
            return []
        sections= [r[0] for r in row]
        return sections
         
# _______________________________________________________________________________________________________________
class section(subject): # section class composed of subject class

    def __init__(self,section_name,subject_name=None,subject_code=None,schedule=None,capacity=0,instructor=None,): # section constructor

        super().__init__(subject_name, subject_code)
        self.schedule = schedule
        self.instructor = instructor
        self.capacity = capacity
        self.section_name = section_name
        self.student_in_section_db = Database("Users.db")  
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
            self.subject=subject_name
        else: 
            self.subject= find_subject_list[0].strip()
        

    def section_info_student(self):  # to display section information
        row= courses_db.execute("SELECT course_code, course_name, section, capacity, time, instructor FROM Courses WHERE section = ?",(self.section_name,),fetchone=True) ### database design must be abdated to include instructor name and creat a table name sections
        if row==None:
            return f"{self.section_name}, Section not found"
        self.subject_code=row[0]
        self.subject_name=row[1]   
        self.section_name=row[2]
        self.capacity=row[3]
        self.schedule=row[4]
        self.instructor=row[5]
        self.remaining_seats= self.remaining_seats()
        
        return f" Subject Name: {self.subject_name}, Section Name: {self.section_name}, subject_code: {self.subject_code} max Capacity: {self.capacity}, Schedule: {self.schedule}, Instructor: {self.instructor},seats remaining: {self.remaining_seats}"

       
    def section_is_existing(self):  # to check if section exists
        row= courses_db.execute("SELECT section FROM Courses WHERE section = ?",(self.section_name,),fetchone=True)
        if row==None or len(row[0])==0:
            return False
        else:
            return True

    def is_full(self):  # to check if section is full
        row= courses_db.execute("SELECT capacity FROM Courses WHERE section = ?",(self.section_name,),fetchone=True)
        if row==None:
            return True
        if len(self.enrolled_students)>=int(row[0]): 
            return True
        else:
            return False
        

    def view_enrolled_students(self):  # to view all enrolled students
        print(self.enrolled_students)
        pass

    def has_time_conflict(self, student_id,lab_time=False):  # to check time conflict with student's schedule
        if lab_time:
            coulmn_name="lab_time"
        else:
            coulmn_name="time"
        section_time_list=[]
        time_row=courses_db.execute(f"SELECT {coulmn_name} FROM Courses WHERE section = ?", (self.section_name,), fetchone=True)
        time= time_row[0]
        times= time.split(",")
        day= times[1].strip()
        class_time= times[0].strip()
        class_time= class_time.split("-")
        start_time=class_time[0].strip().split(":")
        end_time=class_time[1].strip().split(":")
        start_time_hour=int(start_time[0])
        end_time_hour=int(end_time[0])
        start_time_minute=int(start_time[1])
        end_time_minute=int(end_time[1])
        if start_time_hour>end_time_hour:
            end_time_hour+=12
        if start_time_hour == end_time_hour:
            end_time_hour+= (end_time_minute- start_time_minute)/100
        if start_time_hour  < end_time_hour:
            diff= end_time_hour - start_time_hour
            if diff==1:
                if start_time_minute < end_time_minute:
                    end_time_hour =start_time_hour +0.60+((end_time_minute-start_time_minute)/100)
                else:
                    end_time_hour =start_time_hour +0.60-((start_time_minute-end_time_minute)/100)    
            if diff==2:
                if start_time_minute < end_time_minute:
                    end_time_hour =start_time_hour +1.60+((end_time_minute-start_time_minute)/100)
                else:
                    end_time_hour =start_time_hour +1.60-((start_time_minute-end_time_minute)/100)
            if diff==3:
                if start_time_minute < end_time_minute:
                    end_time_hour =start_time_hour +2.60+((end_time_minute-start_time_minute)/100)
                else:
                    end_time_hour =start_time_hour +2.60-((start_time_minute-end_time_minute)/100)  
        start_time_hour*=100
        end_time_hour*=100
        start_time_hour=int(start_time_hour)
        end_time_hour=int(end_time_hour)
               

        for i in range(start_time_hour, end_time_hour ,5): # using 1 as a stip would be more accurate but would create a very long list, based on data base design used 5 should be enough
            time_loop= (i+5)/100
            section_time_list.append(time_loop)    


        schedule_row= users_db.execute("SELECT time FROM enrollments WHERE student_id = ?", (student_id,), fetchall=True) 
        if schedule_row is None or len(schedule_row)==0: 
            return False , f"No time conflict with student's schedule."
        for t in schedule_row:
            student_time= t[0]
            student_times= student_time.split(",")
            student_day= student_times[1].strip()
            student_class_time= student_times[0].strip()
            student_class_time= student_class_time.split("-")
            student_start_time=student_class_time[0].strip().split(":")
            student_end_time=student_class_time[1].strip().split(":")
            student_start_time_hour=int(student_start_time[0])
            student_end_time_hour=int(student_end_time[0])
            student_start_time_minute=int(student_start_time[1])
            student_end_time_minute=int(student_end_time[1])
            if student_start_time_hour>student_end_time_hour:
                student_end_time_hour+=12
            if student_start_time_hour == student_end_time_hour:
                student_end_time_hour+= (student_end_time_minute- student_start_time_minute)/100
            if student_start_time_hour  < student_end_time_hour:
                diff= student_end_time_hour - student_start_time_hour
                if diff==1:
                    if student_start_time_minute < student_end_time_minute:
                        student_end_time_hour =student_start_time_hour +0.60+((student_end_time_minute-student_start_time_minute)/100)
                    else:
                        student_end_time_hour =student_start_time_hour +0.60-((student_start_time_minute-student_end_time_minute)/100)    
                if diff==2:
                    if student_start_time_minute < student_end_time_minute:
                        student_end_time_hour =student_start_time_hour +1.60+((student_end_time_minute-student_start_time_minute)/100)
                    else:
                        student_end_time_hour =student_start_time_hour +1.60-((student_start_time_minute-student_end_time_minute)/100)
                if diff==3:
                    if student_start_time_minute < student_end_time_minute:
                        student_end_time_hour =student_start_time_hour +2.60+((student_end_time_minute-student_start_time_minute)/100)
                    else:
                        student_end_time_hour =student_start_time_hour +2.60-((student_start_time_minute-student_end_time_minute)/100)  
            student_start_time_hour*=100
            student_end_time_hour*=100
            student_start_time_hour=int(student_start_time_hour)
            student_end_time_hour=int(student_end_time_hour)
            for i in range(student_start_time_hour, student_end_time_hour ,5): # using 1 as a stip would be more accurate but would create a very long list, based on data base design used 5 should be enough
                student_time_loop= (i+5)/100
                if day==student_day:
                    if student_time_loop in section_time_list:
                        return True ,f"Time conflict with student's schedule on {t}"
        return False , f"No time conflict with student's schedule."
    

    def prerequisites_met(self, student_id,):  # to check if student meets prerequisites
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

        the_subject= subject(section_subject_code.strip())
        if the_subject.subject_term > student_term:
            return False , f"{section_subject_code} is not in the plan fore the term number {student_term}." 
        

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
        student_completed_subjects_upper= [subj.upper() for subj in student_completed_subjects]            

                   

        if prerequisites==None:
            return False , f"Section {self.section_name} not in study plan of {The_id.major}" 
        elif str(prerequisites).strip()=="":
            return True , "No prerequisites for this section."
        for prereq in prerequisites:
            preq= prereq.strip()
            preq=preq.upper()
            grade= students_taken_subject_with_grades.get(preq)
            if grade== None:
                return False , f"Prerequisite {preq} not completed."
            if  grade == "F":
                return False , f"Prerequisite {preq} not passed."
        for prereq in prerequisites:
            prereq= prereq.strip()
            prereq=prereq.upper()
            if prereq not in student_completed_subjects_upper:
                return False , f"Prerequisite {prereq} not completed."
            
      
        return True , "All prerequisites met."    

    def student_is_existing(self, student_id):  # to check if student is already enrolled in the section
        if str(student_id) in self.student_id_in_section:
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
        
    def already_taken_subject(self, student_id):  # to check if student has already completed the subject
        stu=student(id=student_id)
        return stu.already_taken_subject(self.subject)
    
    def enroll_lab(self, student_id):  # to enroll student in lab section if applicable
        okay , message= self.has_time_conflict(student_id, lab_time=True)
        if okay:
            return False ,f"conflict in lab time : " + message
        lab_section_row=courses_db.execute("SELECT instructor, course_code, lab_time FROM Courses WHERE section = ?", (self.section_name,), fetchone=True) 
        instructor= lab_section_row[0]
        course_code= lab_section_row[1]
        lab_time= lab_section_row[2]
        student_name_row=users_db.execute("SELECT username FROM students WHERE id = ?", (student_id,), fetchone=True)
        student_name= student_name_row[0]
        self.student_in_section_db.execute("INSERT INTO enrollments (student_id, student_name, section,instructor,course,time,credit) VALUES ( ?, ?, ?,?,?,?,?)", (student_id, student_name, self.section_name, instructor,course_code,lab_time,0), commit=True)
        return True , f"Student with ID {student_id} successfully enrolled in lab for section {self.section_name}."

    
    def has_a_lab(self,student_id):  # to check if section has a lab component, if so enroll student in lab using enroll_lab function
        row= courses_db.execute("SELECT lab_time FROM Courses WHERE section = ?",(self.section_name,),fetchone=True)
        if row==None or row[0]==None:
            return False , f"Section {self.section_name} has no lab component."
        else:
            okay , message= self.enroll_lab(student_id)
            if not okay:
                return False , message
            else:
                return True , message
       

           

    def all_conditions_met(self,student_id): # to check if all conditions are met for enrollment

        if not self.student_is_real(student_id):
            return False , f"student with ID {student_id} does not exist"
        if self.student_is_existing(student_id):
            return False , f"student with ID {student_id} is already enrolled in section {self.section_name}"
        if not self.section_is_existing():
            return False , f"section {self.section_name} does not exist"
        if self.already_taken_subject(student_id):
            return False , f"student with ID {student_id} has already completed subject {self.subject}"
        okay,message= self.one_section_for_subject(student_id)
        if  okay:
            return False , message
        if self.is_full():
            return False , f"the section {self.section_name} is full"
        okay , message =  self.prerequisites_met(student_id) # this function must return tuple (bool,str)
        if not okay:
            return False , message
        okay , message= self.has_time_conflict(student_id) # this function must return tuple (bool,str)
        if  okay:
            return False, message
        return True , f"All conditions met for enrollment."
    
    def enroll_student_in_section(self, student_id):  # to enroll a student in the section for data only (admin use only)
        stu=student(student_id)
        if not stu.is_existing():
            return False , f"student with ID {student_id} does not exist"
        okay , message = self.all_conditions_met(student_id)
        if not okay:
            return False , message
        okay , message= self.has_a_lab(student_id)
        if not okay and not (message.find("has no lab component") != -1):
            return False , message
    

        row=courses_db.execute("SELECT instructor, course_code, time, credit FROM Courses WHERE section = ?", (self.section_name,), fetchone=True)
        self.instructor=row[0]
        course_code=row[1]
        time=row[2]
        self.credit=row[3]
        student_name_row=users_db.execute("SELECT username FROM students WHERE id = ?", (student_id,), fetchone=True)
        student_name= student_name_row[0]

        self.student_in_section_db.execute("INSERT INTO enrollments (student_id, student_name, section,instructor,course,time,credit) VALUES (?, ?, ?, ?,?,?,?)", (student_id, student_name, self.section_name, self.instructor,course_code,time,self.credit), commit=True)
        self.enrolled_students.append(f"{student_id} - {student_name}")
        self.student_id_in_section.append(student_id)
        self.student_name_in_section.append(student_name)
        users_db.execute("INSERT INTO grades (student_id, course) VALUES (?, ?)", (student_id, self.subject), commit=True)

        return True , f"Student with ID {student_id} successfully enrolled in section {self.section_name}."

        

        



    def drop_student_from_section(self, student_id):  # to drop a student from the section for data only (admin use only)
        if not self.student_is_real(student_id):
            return False , f"student with ID {student_id} does not exist"
        if not self.student_is_existing(student_id):
            return False , f"student with ID {student_id} is not enrolled in section {self.section_name}"
        if not self.section_is_existing():
            return False , f"section {self.section_name} does not exist"
        if self.already_taken_subject(student_id):
            return False , f"student with ID {student_id} has already completed subject {self.subject}"
        if self.already_graded(student_id):
            return False , f"student with ID {student_id} has already been graded in subject {self.subject}"
        users_db.execute("DELETE FROM enrollments WHERE student_id = ? AND section = ?", (student_id, self.section_name,), commit=True)
        users_db.execute("DELETE FROM grades WHERE student_id = ? AND course = ?", (student_id, self.subject,), commit=True)
        index = self.student_id_in_section.index(str(student_id))
        self.enrolled_students.pop(index)
        self.student_id_in_section.pop(index)
        return True , f"Student with ID {student_id} successfully dropped from section {self.section_name}."


    def new_capacity(self, new_capacity):  # to expand the capacity of the section
        try:
            new_capacity = int(new_capacity)
        except: 
            return f"Capacity must be an integer."
        if new_capacity < len(self.student_id_in_section):
            return f"New capacity cannot be less than the number of enrolled students."
        self.capacity = new_capacity
        courses_db.execute("UPDATE Courses SET capacity = ? WHERE section = ?", (self.capacity, self.section_name), commit=True)
        return f"Section {self.section_name} capacity updated to {self.capacity}."

        

    def remaining_seats(self):  # to check remaining seats in the section
        if not self.section_is_existing():
            return f"section {self.section_name} does not exist"
        row= courses_db.execute("SELECT capacity FROM Courses WHERE section = ?",(self.section_name,),fetchone=True)
        capacity=row[0]
        remaining= int(capacity) - len(self.student_id_in_section)
        return remaining
# _______________________________________________________________________________________________________________
class student(user): # student class inherits of user class
    def __init__(self,id=None,username = None,email=None,major=None,password=None,enrolled_subjects=None,completed_subjects=None,GPA=None,database=False): # student constructor
        super().__init__(username, password, email, id)
        self.current_credits = 0 # total credits of current enrolled subjects for checking max credits allowed per semester not current total subjects
        self.enrolled_subjects = enrolled_subjects if enrolled_subjects is not None else [] # list of section codes the student is currently enrolled in
        self.completed_subjects = completed_subjects if completed_subjects is not None else []  # list of subject codes the student has completed
        majors_row=users_db.execute("SELECT major fROM students WHERE id = ?", (self.id,), fetchone=True)
        if  self.is_student():
            self.major=majors_row[0]
        
        if GPA is None:
            self.GPA = self.calculate_GPA()

        self.database = database # flag to indicate if student data should be inserted into database (True) or loaded from database (False)
        
        if self.database: # insert student into database
            self.major=major
            hash_pass = bcrypt.hashpw(self.password.encode(), bcrypt.gensalt()).decode()
            try:
                users_db.execute(
                    "INSERT INTO students (username, password, email, id, major, term, hashed_password) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (self.username, self.password, self.email, self.id, self.major, 1, hash_pass),
                    commit=True,
                    )
            except sqlite3.IntegrityError:
                print(f"Student with ID {self.id} already exists in the database.")
        else: # load student data from database
             try:
                majors_row=users_db.execute("SELECT major fROM students WHERE id = ?", (self.id,), fetchone=True)
                self.major=majors_row[0].strip()
                enrolled_subjects_row= users_db.execute("SELECT course FROM enrollments WHERE student_id = ?", (self.id,), fetchall=True)
                self.enrolled_subjects= [r[0].strip() for r in enrolled_subjects_row]
             except:
                 f"Student with ID {self.id} does not exist"
       
    def return_id(self):
        return self.id
    
    def change_password(self, old_password, new_password):  # to change student's password
        if not self.correct_password(old_password):
            return False , "Old password is incorrect."
        the_hashed = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
        users_db.execute("UPDATE students SET password = ?, hashed_password = ? WHERE id = ?", (new_password, the_hashed, self.id), commit=True)
        self.password = new_password
        return True , "Password changed successfully."
    

    
    def already_taken_subject(self, subject_code):  # to check if student has already completed the subject

        row= users_db.execute("SELECT course, numeric_grade FROM grades WHERE student_id = ?", (self.id,), fetchall=True)
        course_with_grades= {}
        for cours, numeric_grade in row:
            if numeric_grade==None:
                continue
            course_with_grades[cours]= numeric_grade
            
        completed_courses_list = list(course_with_grades.keys())
        completed_courses= [course.strip().upper() for course in completed_courses_list]
        subject_code= subject_code.strip().upper()
    
        if subject_code in completed_courses:
            return True
        else:
            return False
    
    def determine_major(self):  # to determine student's major from database
        row= users_db.execute("SELECT major FROM students WHERE id = ?", (self.id,), fetchone=True)
        if row==None:
            return f"{self.id}, Student not found"
        self.major=row[0]
        return self.major
 
    def enroll_subject(self, section_code):  # to enroll student in a subject section
        sec=section(section_name=section_code)
        okay,message =sec.enroll_student_in_section(self.id) # enroll student in section class method
        return okay, message

    def drop_subject(self, section_code):  # to drop a subject section for the student
        sect=section(section_name=section_code)
        okay,message =sect.drop_student_from_section(self.id) # drop student from section class method
        return okay, message

    def view_enrolled_subjects(self):  # to view all enrolled subjects for the student
        row = users_db.execute("SELECT section FROM enrollments WHERE student_id = ?", (self.id,), fetchall=True) # get sections the student is enrolled in
        if row is None or len(row) == 0:
            return f"{self.id}, No enrolled subjects found"
        enrolled_sections = [r[0] for r in row]
        row = courses_db.execute("SELECT course_code,course_name,time,credit,section,instructor FROM Courses WHERE section IN ({seq})".format(seq=','.join(['?']*len(enrolled_sections))), tuple(enrolled_sections), fetchall=True) # get details for those sections
        if row is None or len(row) == 0:
            return f"{self.id}, No enrolled subjects found"
        all_enrolled = {}
        for r in row:
            course_code = r[0]
            course_name = r[1]
            time = r[2]
            credit = r[3]
            section = r[4]
            instructor = r[5]
            all_enrolled[section] = (course_code, course_name, time, section, credit, instructor) # organize by section
        return all_enrolled
    
    def view_available_subjects(self):  # to view all available subjects for enrollment
        if self.is_student():
            row = users_db.execute("SELECT term,major FROM students WHERE id = ?", (self.id,), fetchone=True) # get student's term and major
            student_term = row[0]
            student_major = row[1]
            # map majors to their respective subject tables
            major_table_map = {
                'Electrical communication and electronics engineering': "communication",
                'Electrical computer engineering': "computer",
                'Electrical power and machines engineering': "power",
                'Electrical biomedical engineering': "biomedical"
            }
            major = major_table_map.get(student_major)
            if major is None:
                return f"Major '{student_major}' not recognized."
            
            row = courses_db.execute(f"SELECT course_code FROM {major} WHERE terms = ?", (student_term,), fetchall=True) # get subjects for the student's term
            if row is None or len(row) == 0:
                return f"Term {student_term}, No subjects found for major {student_major}"
            subjects = [r[0] for r in row]
            row = courses_db.execute("SELECT section FROM Courses WHERE course_code IN ({seq})".format(seq=','.join(['?']*len(subjects))), tuple(subjects), fetchall=True) # get sections for those subjects
            available_sections = [r[0] for r in row] 
            enrolled_row = users_db.execute("SELECT section FROM enrollments WHERE student_id = ?", (self.id,), fetchall=True) # get sections the student is already enrolled in
            enrolled_sections = [r[0] for r in enrolled_row]
            completed_row = users_db.execute("SELECT course FROM grades WHERE student_id = ?", (self.id,), fetchall=True) # get subjects the student has already completed
            completed_courses = [r[0].strip().upper() for r in completed_row] 
            available_sections = [sec for sec in available_sections if sec not in enrolled_sections and sec not in completed_courses] # filter out enrolled and completed sections
            
            all_available = {}
            for section in available_sections:
                course_row = courses_db.execute("SELECT course_code, instructor ,section,time,credit FROM Courses WHERE section = ?", (section,), fetchone=True)
                if course_row:
                    course_code = course_row[0]
                    instructor = course_row[1]
                    section = course_row[2]
                    time = course_row[3]
                    credit = course_row[4]
                    all_available[section] = (section,course_code, instructor, time, credit)
            #organize by course code
            sorted_available = dict(sorted(all_available.items(), key=lambda item: item[1][1]))
            return sorted_available

    def calculate_GPA(self):  # to calculate GPA based on completed subjects and their grades
        

        #map letter grades to grade points
        grade_map = {
            'A+':5.0, 'A': 4.75, 'B+': 4.5, 'B': 4.0, 'C+': 3.5,
            'C': 3.0, 'D+': 2.5, 'D': 2.0, 'F': 1.0
        }
        #map majors to their respective subject tables
        Major_table_map = {
                           'Electrical communication and electronics engineering': "Communication",
                            'Electrical computer engineering' : "Computer",
                            'Electrical biomedical engineering' : "Biomedical",
                            'Electrical power and machines engineering' : "Power"
        }
            
        #find the students major to determine used table
        major = self.determine_major()
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
                       """ # completed subjects with grades and credits
        cur.execute(query, (self.id,))
        rows = cur.fetchall()

        if not rows: # no completed subjects found
            conn.close()
            gpa = 0.0
            return gpa
        total_credits = 0
        total_points = 0
        for course, letter_grade, credit in rows: # calculate total points and credits
            if letter_grade not in grade_map :
                continue  # skip invalid grades
            grade_point = grade_map.get(letter_grade, 0)
            total_credits += credit
            total_points += grade_point * credit
            
        if total_credits == 0:
            conn.close()
            return "No credits found for GPA calculation."
        
        gpa = total_points / total_credits # calculate GPA
        conn.close()
        
        return round(gpa, 2)


    def transcript(self):  # to generate a transcript of completed subjects and grades
        row = users_db.execute("SELECT course, Letter_grade FROM grades WHERE student_id = ?", (self.id,), fetchall=True)
        completed = {r[0]: r[1] for r in row} # completed courses with grades
        row = users_db.execute("SELECT term, major FROM students WHERE id = ?", (self.id,), fetchone=True)
        student_term = row[0] 
        student_major = row[1]
        major_table_map = {
            'Electrical communication and electronics engineering': "communication",
            'Electrical computer engineering': "computer",
            'Electrical power and machines engineering': "power",
            'Electrical biomedical engineering': "biomedical"
        } # map major to corresponding table name

        major = major_table_map.get(student_major)
        if major is None: # major table not found
            return f"Major '{student_major}' not recognized."
        row = courses_db.execute(f"SELECT course_code,terms FROM {major}" , fetchall=True)
        subject_terms = {r[0]: r[1] for r in row} # all subjects with their terms
        # print(subject_terms)
        full_record = {}
        for course_code, term in subject_terms.items(): # build full record with term and grade
            grade = completed.get(course_code)
            if grade:
                grade = grade
            else:
                grade = "--" # not completed
            full_record[course_code] = (term, grade)
        return full_record # return full transcript record
# _______________________________________________________________________________________________________________
class instructor(user):
    def __init__(self, id=None , username=None, subject=None, sections=None, password=None, email=None,  database=False):
        super().__init__(username, password, email, id) # i will change this place
        self.subject = subject  # subject assigned to the instructor
        self.sections = sections if sections is not None else []  
        self.database = database

        if self.database:

            users_db.execute(
                "INSERT INTO instructors (username, password, email, id) VALUES (?, ?, ?, ?)",
                (self.username, self.password, self.email,self.id),
                commit=True,
            )   
    def show_students(self,section_code):  # to show all students in a section
        self.section= section(section_name=section_code)
        self.section.view_enrolled_students()

    def is_existing(self):
        row= users_db.execute("SELECT id FROM instructors WHERE id = ?", (self.id,), fetchone=True)  
        if row==None:
            return False
        else:
            return True
    def my_name(self):
        return self.username
# _______________________________________________________________________________________________________________
class admin(user): # admin class inherits from user class
    def __init__(self,id=None,username=None ,password=None, email=None, database=False): # admin constructor
       
        self.database= database
        # set database to true if you want to insert this admin into database upon creation
        # eg. admin = admin("azad", database=True)

        if self.database == True: # insert new admin into database
            super().__init__(username, password, email, id)
            
            users_db.execute(
                "INSERT INTO admins (username, password, email, id) VALUES (?, ?, ?, ?)",
                (self.username, self.password, self.email,self.id),
                commit=True,
            )
        else: # load admin data from database
            info_row= users_db.execute("SELECT username, password, email, id FROM admins WHERE id = ?", (id,), fetchone=True)
            if info_row is None:
                raise ValueError(f"Admin with ID {id} does not exist in the database.")
            self.username= info_row[0]
            self.password= info_row[1]
            self.email= info_row[2]
            self.id= info_row[3]
        

            
    def add_subject(self, section_code, student_id):  # to add a subject to a student
        stu=student(id=str(student_id).strip())
        if not stu.is_student() or not stu.is_existing():
            return f"Student with ID {student_id} does not exist."
        sect=section(section_name=section_code)
        okay,massege = sect.enroll_student_in_section(student_id)
        return okay, massege

    def remove_subject(self, section_code, student_id):  # to remove a subject from a student
        sect=section(section_name=section_code)
        okay,massege =sect.drop_student_from_section(student_id)
        return okay, massege



    def display_student_in_section(self, section_code):  # to display students in a section
        row = users_db.execute("SELECT student_id FROM enrollments WHERE section = ?", (section_code,), fetchall=True)
        if row is None:
            return f"Section {section_code}, No enrolled students found"
        enrolled_students_id = [r[0] for r in row]
        row = users_db.execute("SELECT * FROM students WHERE id IN ({seq})".format(seq=','.join(['?']*len(enrolled_students_id))), tuple(enrolled_students_id), fetchall=True)
        enrolled_students_info = {r[0]: r[1:] for r in row}
        return enrolled_students_info


        

    def view_all_subjects(self, id):  # to view all available subjects
        if student(id).is_student():
            row = users_db.execute("SELECT term,major FROM students WHERE id = ?", (id,), fetchone=True)
            student_term = row[0]
            student_major = row[1]
            major_table_map = {
                'Electrical communication and electronics engineering': "communication",
                'Electrical computer engineering': "computer",
                'Electrical power and machines engineering': "power",
                'Electrical biomedical engineering': "biomedical"
            }
            major = major_table_map.get(student_major)
            if major is None:
                return f"Major '{student_major}' not recognized."
            
            row = courses_db.execute(f"SELECT course_code FROM {major} WHERE terms = ?", (student_term,), fetchall=True)
            if row is None or len(row) == 0:
                return f"Term {student_term}, No subjects found for major {student_major}"
            subjects = [r[0] for r in row]
            row = courses_db.execute("SELECT section FROM Courses WHERE course_code IN ({seq})".format(seq=','.join(['?']*len(subjects))), tuple(subjects), fetchall=True)
            available_sections = [r[0] for r in row]
            enrolled_row = users_db.execute("SELECT section FROM enrollments WHERE student_id = ?", (id,), fetchall=True)
            enrolled_sections = [r[0] for r in enrolled_row]
            available_sections = [sec for sec in available_sections if sec not in enrolled_sections]
            all_available = {}
            for section in available_sections:
                course_row = courses_db.execute("SELECT course_code FROM Courses WHERE section = ?", (section,), fetchone=True)
                if course_row:
                    course_code = course_row[0]
                    all_available[section] = course_code
        else:
            all_available= f"Student with ID {id} does not exist."            

            return all_available


    def find_sections(self, course_code):  # to view sections for a specific subject
        row  = courses_db.execute("SELECT section FROM Courses WHERE course_code = ?", (course_code,), fetchall=True)
        if row is None or len(row) == 0:
            return f"Subject {course_code}, No sections found"
        sections = [r[0] for r in row]
        return sections

    def expand_capacity(self, section_code, new_capacity):  # to expand section capacity
        section_code=section_code.strip().upper()
        sec=section(section_name=section_code)
        massege= sec.new_capacity(new_capacity)
        return massege
    
    def add_grade(self, student_id, course_code, grade,):  # to add grade for a student in a section
        course_code=course_code.strip().upper()
        sub=subject(course_code)
        stu=student(id=student_id)
        if not stu.is_student():
            return f"Student with ID {student_id} does not exist."
        if not sub.is_existing():
            return f"Subject with code {course_code} does not exist."
        if not stu.already_taken_subject(course_code) and course_code not in stu.enrolled_subjects:
            return f"Student with ID {student_id} has not completed subject {course_code}."

        try :
            grade = float(grade)
        except:
            return "Grade must be a number."
        if grade < 0.0 or grade > 100.0:
            return "Grade must be between 0 and 100."
        if  grade >= 95.0:
            letter_grade = "A+"
        elif grade >= 90.0:
            letter_grade = "A"
        elif grade >= 85.0:
            letter_grade = "B+"
        elif grade >= 80.0:
            letter_grade = "B"
        elif grade >= 75.0:
            letter_grade = "C+"
        elif grade >= 70.0:
            letter_grade = "C"
        elif grade >= 65.0:
            letter_grade = "D+"
        elif grade >= 60.0:
            letter_grade = "D"
        else:
            letter_grade = "F"
        users_db.execute("UPDATE grades SET numeric_grade = ?, letter_grade = ? WHERE student_id = ? AND course = ?", (grade, letter_grade, student_id, course_code), commit=True)
        users_db.execute("DELETE FROM enrollments WHERE student_id = ? AND course = ?", (student_id, course_code), commit=True)
        return f"Grade {grade} ({letter_grade}) added for student ID {student_id} in course {course_code}."
    
    def add_student(self,first_name,last_name,major): # to add a new student to the database
        IDT1 = users_db.execute("SELECT id FROM students WHERE term = ?", (1,), fetchall=True)
        IDT2 = users_db.execute("SELECT id FROM students WHERE term = ?", (2,), fetchall=True)
        IDY1 = IDT1 + IDT2
        IDY10 = [x[0] for x in IDY1]
        max_id = max(IDY10)
        new_id = int(max_id) + 1
        full_name= first_name.strip().title() + " " + last_name.strip().title()
        st=student(username=full_name,major=major,database=True,id=new_id)
        return True , f"Student {full_name} added with ID {st.id} and password {st.password}."   
    
    def delete_student(self, student_id): # to delete a student from the database
        if not student(student_id).is_student():
            return False , f"Student with ID {student_id} does not exist."
        users_db.execute("DELETE FROM students WHERE id = ?", (student_id,), commit=True)
        users_db.execute("DELETE FROM enrollments WHERE student_id = ?", (student_id,), commit=True)
        users_db.execute("DELETE FROM grades WHERE student_id = ?", (student_id,), commit=True)
        return True , f"Student with ID {student_id} deleted from the database."
    
    def display_courses_by_plan_level(self,plan,Level): #display courses by plan and level
        row=courses_db.execute("SELECT course_code,course_name,credit,terms,prerequisites FROM {plan} WHERE terms = ?".format(plan=plan),(Level,),fetchall=True)
        if row is None or len(row)==0:
            return f"No courses found for term {Level} in plan {plan}."
        courses_info= {}
        for r in row:
            course_code=r[0]
            course_name=r[1]
            credit=r[2]
            term=r[3]
            prerequisites=r[4]
            courses_info[course_code]=(course_name,credit,term,prerequisites)
        return courses_info
    
    
    def rewrite_add_course(self,course_code=None,course_name=None,credit=None,sections=None,term=None,prerequisites=None): #to change added course details
        if course_code is None or course_name is None or credit is None or sections is None or term is None or prerequisites is None:
            return False , "All fields are required."
        course_code=course_code.strip().upper()
        sub=subject(course_code)
        if sub.is_existing():
            return False , f"Course with code {course_code} already exists."
        if not credit.isdigit():
            return False , "Credit must be a positive integer."
        elif int(credit)<=0:
            return False , "Credit must be a positive integer."
        if not term.isdigit():
            return False , "Term must be a positive integer."
        elif not 10>=int(term)>=1:
            return False , "Term must be between 1 and 10."
        sec=sections.strip().upper()
        if section(sec).section_is_existing():
            return False , f"Section {sec} already exists."
        if "," in prerequisites:
            prereq_list=[prereq.strip().upper() for prereq in prerequisites.split(",")]
        else:
            prereq_list= [prerequisites.strip().upper()]
        for prereq in prereq_list:
            if prereq=="":
                continue
            if prereq==course_code:
                return False , f"Course cannot be a prerequisite of itself."
            pre_sub=subject(prereq)
            if not pre_sub.is_existing():
                return False , f"Prerequisite course with code {prereq} does not exist."
            if pre_sub.subject_term > int(term):
                return False , f"Prerequisite course with code {prereq} is offered in a higher term than the new course."
        courses_db.execute("INSERT INTO Courses (course_code, course_name, credit, section, instructor, capacity, time,term,prerequisites) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (course_code, course_name, int(credit), sec, "TBA", 30, "To be scheduled", int(term),prerequisites), commit=True)
        return True , f"Course {course_code} - {course_name} added successfully with section {sec}, you will have to update the instructor and capacity from section management."
    
    def rewrite_update_course(self,course_code=None,course_name=None,credit=None,sections=None,term=None,prerequisites=None): #to update course details
        if course_code is None:
            return False , "Course code is required to update a course."
        course_code=course_code.strip().upper()
        sub=subject(course_code)
        if not sub.is_existing():
            return False , f"Course with code {course_code} does not exist."
        if credit is not None:
            if not credit.isdigit():
                return False , "Credit must be a positive integer."
            elif int(credit)<=0:
                return False , "Credit must be a positive integer."
        
            
        if sections is not None:
            if "," in sections:
                sec=[section.strip().upper() for section in sections.split(",")]
                if len(sec)>2 or len(sec)<2:
                    return False , "please use , to separate new section and old section only using , EX: AA,AW. (notce that old section first)"
                old_sec=sec[0]
                new_sec=sec[1]
                
                if section(old_sec).subject == None:
                    return False , f"Section {old_sec} does not exist."
                else:
                
                    if subject(course_code).subject_name != section(old_sec).subject:
                        return False , f"Section {old_sec} is not associated with course {course_code}."
                    if old_sec==new_sec:
                        return False , "Old section and new section cannot be the same."
                

                if not section(old_sec).section_is_existing():
                    return False , f"Section {old_sec} does not exist."
                if section(new_sec).section_is_existing():
                    return False , f"Section {new_sec} already exists."
            else:
                return False , "please use , to separate new section and old section only using , EX: AA,AW. (notce that old section first)"

            
        if term is not None:
            if not term.isdigit():
                return False , "Term must be a positive integer."
            elif not 10>=int(term)>=1:
                return False , "Term must be between 1 and 10."
            
        if prerequisites is not None:
            if "," in prerequisites:
                prereq_list=[prereq.strip().upper() for prereq in prerequisites.split(",")]
            else:
                prereq_list= [prerequisites.strip().upper()]
            for prereq in prereq_list:
                if prereq=="":
                    continue
                if prereq==course_code:
                    return False , f"Course cannot be a prerequisite of itself."
                pre_sub=subject(prereq)
                if not pre_sub.is_existing():
                    return False , f"Prerequisite course with code {prereq} does not exist."
            courses_db.execute("UPDATE Courses SET prerequisites = ? WHERE course_code = ?", (prerequisites, course_code), commit=True)
        if sections is not None:courses_db.execute("UPDATE Courses SET section = ? WHERE section = ? AND course_code = ?", (new_sec, old_sec, course_code), commit=True)
            
        if course_name is not None:courses_db.execute("UPDATE Courses SET course_name = ? WHERE course_code = ?", (course_name, course_code), commit=True)
        
        if credit is not None:courses_db.execute("UPDATE Courses SET credit = ? WHERE course_code = ?", (int(credit), course_code), commit=True)

        if term is not None:courses_db.execute("UPDATE Courses SET term = ? WHERE course_code = ?", (int(term), course_code), commit=True)

        return True , f"Course with code {course_code} updated successfully." 
    
    def rewrite_add_section(self,course_code=None,section_name=None,instructor_id=None,capacity=None,start_time=None,end_time=None,day=None):
        if course_code is None or section_name is None or instructor_id is None or capacity is None:
            return False , "Course code, section name, instructor ID, and capacity are required."
        course_code=course_code.strip().upper()
        sub=subject(course_code)
        if not sub.is_existing():
            return False , f"Course with code {course_code} does not exist."
        sec=section_name.strip().upper()
        if section(sec).section_is_existing():
            return False , f"Section {sec} already exists."
        if not instructor(instructor_id).is_existing():
            return False , f"Instructor with ID {instructor_id} does not exist."
        if not capacity.isdigit():
            return False , "Capacity must be a positive integer."
        elif int(capacity)<=0:
            return False , "Capacity must be a positive integer."
        if day == "Sunday":
            day_code = "S"
        elif day == "Monday":
            day_code = "M"
        elif day == "Tuesday":
            day_code = "T"
        elif day == "Wednesday":
            day_code = "W"
        elif day == "Thursday":
            day_code = "U"
        start_time_list = start_time.split(":")
        end_time_list = end_time.split(":")
        start_hour = int(start_time_list[0])
        end_hour = int(end_time_list[0])
        if start_time == end_time:
            return False , "Start time and end time cannot be the same."
        elif start_hour > end_hour:
            return False , "The lecture time conflict with non-academic commitments."
        elif start_hour - end_hour > 3:
            return False , "Lecture duration cannot exceed 3 hours."
        time = f"{day_code} {start_time}-{end_time}"
        credit_prerequisite_row= courses_db.execute("SELECT credit, prerequisites FROM Courses WHERE course_code = ?", (course_code,), fetchone=True)
        credit= credit_prerequisite_row[0]
        if credit_prerequisite_row[1]==None or credit_prerequisite_row[1]=="":
            prerequisites=""
        else:
            prerequisites= credit_prerequisite_row[1]
        courses_db.execute("INSERT INTO Courses (course_code, course_name, credit, section, instructor, capacity, time,prerequisites) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?)", (course_code, sub.subject_name, credit, sec, instructor_id, int(capacity), time, prerequisites), commit=True)
        return True , f"Section {sec} for course {course_code} added successfully."
    
    def rewrite_update_section(self,course_code=None,section_name=None,instructor_id=None,capacity=None,start_time=None,end_time=None,day=None):
        if course_code is None or section_name is None:
            return False , "Course code and section name are required to update a section."
        course_code=course_code.strip().upper()
        sub=subject(course_code)
        if not sub.is_existing():
            return False , f"Course with code {course_code} does not exist."
        
        sec=section_name.strip().upper()
        if sub.subject_name != section(sec).subject:
            
            return False , f"Section {sec} does not belong to course {course_code}."
        if not section(sec).section_is_existing():
            return False , f"Section {sec} does not exist."
        if instructor_id is not None:
            if not instructor(instructor_id).is_existing():
                return False , f"Instructor with ID {instructor_id} does not exist."

        if capacity is None and start_time is None and end_time is None is None and instructor_id is None:
            return False , "At least one field (instructor ID, capacity, or time) must be provided to update."    
            
        if capacity is not None:
            if not capacity.isdigit():
                return False , "Capacity must be a positive integer."
            elif int(capacity)<=0:
                return False , "Capacity must be a positive integer."
            
        if start_time is not None and end_time is not None and day is not None:
            if day == "Sunday":
                day_code = "S"
            elif day == "Monday":
                day_code = "M"
            elif day == "Tuesday":
                day_code = "T"
            elif day == "Wednesday":
                day_code = "W"
            elif day == "Thursday":
                day_code = "U"
            start_time_list = start_time.split(":")
            end_time_list = end_time.split(":")
            start_hour = int(start_time_list[0])
            end_hour = int(end_time_list[0])
            start_minute = int(start_time_list[1])
            end_minute = int(end_time_list[1])
            diff_time= (end_hour + end_minute/60) - (start_hour + start_minute/60)
            if start_time == end_time:
                return False , "Start time and end time cannot be the same."
            elif diff_time < 50/60:
                return False , "Lecture duration cannot be less than 50 minutes."
            elif start_hour > end_hour:
                return False , "The lecture time conflict with non-academic commitments."
            elif start_hour - end_hour > 3:
                return False , "Lecture duration cannot exceed 3 hours."
            time = f"{day_code} {start_time}-{end_time}"
            courses_db.execute("UPDATE Courses SET time = ? WHERE course_code = ? AND section = ?", (time, course_code, sec), commit=True)
        if instructor_id is not None:
            instructor_name= instructor(instructor_id).my_name()
            courses_db.execute("UPDATE Courses SET instructor = ? WHERE course_code = ? AND section = ?", (instructor_name, course_code, sec), commit=True)
        if capacity is not None:
            courses_db.execute("UPDATE Courses SET capacity = ? WHERE course_code = ? AND section = ?", (int(capacity), course_code, sec), commit=True)

        return True , f"Section {sec} for course {course_code} updated successfully."
   
        
        
    def courses_not_in_the_plan(self,plan_major):  # to display all subjects not in the plan_major 
        if plan_major == "Electrical communication and electronics engineering":
            row = courses_db.execute("SELECT course_code FROM communication", fetchall=True)
        elif plan_major == "Electrical computer engineering":
            row = courses_db.execute("SELECT course_code FROM computer", fetchall=True)
        elif plan_major == "Electrical power and machines engineering":
            row = courses_db.execute("SELECT course_code FROM power", fetchall=True)
        elif plan_major == "Electrical biomedical engineering":
            row = courses_db.execute("SELECT course_code FROM biomedical", fetchall=True)

        subjects_in_major = [r[0].strip().upper() for r in row]

        all_courses_row = courses_db.execute("SELECT course_code FROM Courses", fetchall=True)
        all_courses = [r[0].strip().upper() for r in all_courses_row]

        not_in_plan = []
        for course in all_courses:
            if course not in subjects_in_major:
                not_in_plan.append(course)

        # now we found (course_code) for each course in not_in_plan
        courses_info = {}

        for course_code in not_in_plan:
            row = courses_db.execute(
                "SELECT course_name, credit, term, prerequisites FROM Courses WHERE course_code = ?",
                (course_code,),
                fetchone=True)

            course_name = row[0]
            credit      = row[1]
            terms       = row[2]     
            if row[3] is None:
                prerequisites = ""
            else:
                prerequisites = row[3]

            if terms is None or terms == "":
                term_row = courses_db.execute("""
                    SELECT COALESCE(comm.terms, comp.terms, pow.terms, bio.terms)
                    FROM Courses AS c
                    LEFT JOIN communication AS comm ON comm.course_code = c.course_code
                    LEFT JOIN computer      AS comp ON comp.course_code = c.course_code
                    LEFT JOIN power         AS pow  ON pow.course_code  = c.course_code
                    LEFT JOIN biomedical    AS bio  ON bio.course_code  = c.course_code
                    WHERE c.course_code = ?
                """, (course_code,), fetchone=True)

                if term_row and term_row[0] is not None:
                    terms = term_row[0]
                else:
                    terms = ""
                   

            courses_info[course_code] = {
                "course_name": course_name,
                "credit": credit,
                "terms": terms,         
                "prerequisites": prerequisites
            }

        return courses_info

    def add_course_to_plan(self, course_code, plan_major):
        course_code = course_code.strip().upper()

        major_tables = {
            "Electrical communication and electronics engineering": "communication",
            "Electrical computer engineering": "computer",
            "Electrical power and machines engineering": "power",
            "Electrical biomedical engineering": "biomedical"
        }

        table_name = major_tables.get(plan_major)
        if table_name is None:
            return False, f"Unknown major: {plan_major}"

        already = courses_db.execute(
            f"SELECT 1 FROM {table_name} WHERE course_code = ?",
            (course_code,),
            fetchone=True
        )
        if already:
            return False, f"Course with code {course_code} is already in {plan_major} plan."

        row = courses_db.execute(
            "SELECT course_name, credit, term, prerequisites "
            "FROM Courses WHERE course_code = ?",
            (course_code,),
            fetchone=True
        )
        if not row:
            return False, "Course not found in Courses table."

        course_name = row[0] or ""
        credit = row[1]
        terms = row[2]
        prerequisites = row[3] if row[3] else ""

        if terms is None or terms == "":
            term_row = courses_db.execute("""
                SELECT COALESCE(comm.terms, comp.terms, pow.terms, bio.terms)
                FROM Courses c
                LEFT JOIN communication AS comm ON comm.course_code = c.course_code
                LEFT JOIN computer      AS comp ON comp.course_code = c.course_code
                LEFT JOIN power         AS pow  ON pow.course_code  = c.course_code
                LEFT JOIN biomedical    AS bio  ON bio.course_code  = c.course_code
                WHERE c.course_code = ?
            """, (course_code,), fetchone=True)

            if term_row and term_row[0] is not None:
                terms = term_row[0]
            else:
                terms = ""

        try:
            courses_db.execute(
                f"INSERT INTO {table_name} "
                f"(course_code, terms, prerequisites, credit, course_name) "
                f"VALUES (?, ?, ?, ?, ?)",
                (course_code, terms, prerequisites, credit, course_name),
                commit=True
            )
        except Exception as e:
            return False, f"Database error while adding course: {e}"

        return True, f"Course with code {course_code} added to {plan_major} plan successfully."


    def delete_course_from_plan(self,course_code,plan_major  ):
        course_code=course_code.strip().upper()
        row= courses_db.execute("SELECT section FROM Courses WHERE course_code = ?",(course_code.strip().upper(),),fetchall=True)
        if row==None or len(row)==0:
            return []
        sec= [r[0] for r in row]
         
        
        for section_name in sec:
            sect=section(section_name=section_name)
            if len(sect.student_id_in_section)>0:
                return False , f"Cannot delete course with code {course_code} from {plan_major} plan because students are enrolled in its sections."
       
        if plan_major=="Electrical communication and electronics engineering":
            courses_db.execute("DELETE FROM communication WHERE course_code = ?", (course_code,), commit=True)
        if plan_major=="Electrical computer engineering":
            courses_db.execute("DELETE FROM computer WHERE course_code = ?", (course_code,), commit=True)
        if plan_major=="Electrical power and machines engineering":
            courses_db.execute("DELETE FROM power WHERE course_code = ?", (course_code,), commit=True)
        if plan_major=="Electrical biomedical engineering":
            courses_db.execute("DELETE FROM biomedical WHERE course_code = ?", (course_code,), commit=True)
        return True , f"Course with code {course_code} deleted from {plan_major} plan successfully."
    
    def add_prerequisite_to_course(self,course_code,prerequisite):
        sub=subject(course_code)
        okay,massege= sub.add_prerequisite(prerequisite)
        return okay, massege
    
    def remove_prerequisite_from_course(self,course_code,prerequisite):
        sub=subject(course_code)
        okay,massege= sub.remove_prerequisite(prerequisite)
        return okay, massege
    
    def display_subjects_by_major_plan(self, major):  # to display subjects by major plan
        if major=="Electrical communication and electronics engineering":
            row= courses_db.execute("SELECT course_code, course_name, terms,credit,prerequisites FROM communication ORDER BY terms",fetchall=True)
        elif major=="Electrical computer engineering":
            row= courses_db.execute("SELECT course_code, course_name, terms,credit,prerequisites FROM computer ORDER BY terms",fetchall=True)
        elif major=="Electrical power and machines engineering":
            row= courses_db.execute("SELECT course_code, course_name, terms,credit,prerequisites FROM power ORDER BY terms",fetchall=True)
        elif major=="Electrical biomedical engineering":
            row= courses_db.execute("SELECT course_code, course_name, terms,credit,prerequisites FROM biomedical ORDER BY terms",fetchall=True)
        else:
            return f"Major {major} not found."
        subjects_info={}
        for course_code, course_name, terms, credit, prerequisites in row:
            subjects_info[course_code]={
                "course_name": course_name,
                "terms": terms,
                "credit": credit,
                "prerequisites": prerequisites
            }
        return subjects_info
    
    
    def remove_section(self,section_name):
        sect=section(section_name=section_name.strip().upper())
        if not sect.section_is_existing():
            return False , f"Section {section_name} does not exist."
        if len(sect.student_id_in_section)>0:
            return False , f"Cannot delete section {section_name} because students are enrolled in it."
        courses_db.execute("DELETE FROM Courses WHERE section = ?", (section_name,), commit=True)
        return True , f"Section {section_name} deleted successfully."
    

    
    def get_table_data_optimized(self, plan, term):
        if plan == "Electrical communication and electronics engineering":
            plan="communication"
        elif plan == "Electrical computer engineering":
            plan="computer"
        elif plan == "Electrical power and machines engineering":
            plan="power"
        elif plan == "Electrical biomedical engineering":
            plan="biomedical"
        # now we bring (section, capacity, instructor, credit, time) from Courses table for each course_code
        row= courses_db.execute("SELECT course_code, section, capacity, instructor, credit, time FROM Courses WHERE course_code IN (SELECT course_code FROM {plan} WHERE terms = ?)".format(plan=plan), (term,), fetchall=True)

        return row   
        
#________________________________________________________________________________________________________________

#password strength checker methods
def is_special(ch): # this is for password ensuring it has a special character
    return not ch.isalnum()

def has_sequence(chars, length=3): # this is for password ensuring it does not have 3 consecutive numbers
    digits = [int(c) for c in chars if c.isdigit()]
    if len(digits) < length:
        return False

    streak = 1
    for i in range(1, len(digits)):
        if digits[i] == digits[i - 1] + 1:
            streak += 1
            if streak >= length:
                return True
        else:
            streak = 1
    return False

def enforce_strong_password(new_password): # this method is checking the new password is strong enough (for new students)
    new_password_splited = list(new_password)
    cond1 = any(is_special(ch) for ch in new_password_splited) # First condition to have at least one character

    cond2 = len(new_password_splited) >= 8 # Second condition to have at least 8 letters

    cond3 = not has_sequence(new_password_splited) # Third condition to not have 3 numbers in a row
    
    cond4 = any(ch.isupper() for ch in new_password_splited) # Forth condition to have at least one capital letter

    return cond1 and cond2 and cond3 and cond4
#________________________________________________________________________________________________________________


# signup method
def signup(FN, LN, Npassword, M): # FN = first name , LN = last name
    db = sqlite3.connect("Users.db")
    cr = db.cursor()
    cr.execute("SELECT id FROM students WHERE term = ?", (1,))
    FYID1 = cr.fetchall()

    cr.execute("SELECT id FROM students WHERE term = ?", (2,))
    FYID2 = cr.fetchall()

    All_ids_FY2 = [x[0] for x in FYID2]
    All_ids_FY1 = [x[0] for x in FYID1]
    All_ids_FY = All_ids_FY1 + All_ids_FY2
    highest_id = (max(All_ids_FY))
    stu_id = int(highest_id) + 1

    
    Tusername = FN.strip() + " " + LN.strip()
    s = student(id = stu_id, username=Tusername, major=M, email= f"{FN}{stu_id}@stu.kau.edu.sa", password=Npassword, database=True)

    db.commit()
    db.close()

    return s

#________________________________________________________________________________________________________________

def update_password(student_id, new_password):

    db = sqlite3.connect("Users.db")
    cr = db.cursor()
    the_hashed = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
    s = user(id=student_id)
    if s.is_admin():
        cr.execute("UPDATE admins SET password = ?, hashed_password = ? WHERE id = ?", (new_password, the_hashed, student_id))
    elif s.is_student():
        cr.execute("UPDATE students SET password = ?, hashed_password = ? WHERE id = ?", (new_password, the_hashed, student_id))
    db.commit()
    db.close()

    return


