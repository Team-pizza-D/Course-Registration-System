import sqlite3
import bcrypt
from classses2 import admin, student,section,subject,instructor,Database, user


# db = sqlite3.connect("Users.db")
# cr = db.cursor()
# cr.execute("DROP TABLE IF EXISTS enrollments")
# cr.execute("DROP TABLE IF EXISTS admins")
# cr.execute("CREATE TABLE IF NOT EXISTS admins (id TEXT, username TEXT, password TEXT, email TEXT, status TEXT)")
# cr.execute("CREATE TABLE IF NOT EXISTS enrollments (section TEXT, instructor TEXT, course TEXT, student_id TEXT, student_name TEXT, time TEXT, credit TEXT)")
# db.commit()
# db.close()
tariq = student( id=2430020)
# print("--------------------------------")
# print(tariq.view_available_subjects())
print(tariq.email)
print(tariq.display_info())
# print("--------------------------------")
# print(tariq.view_enrolled_subjects())
# print("--------------------------------")
# tariq.enroll_subject("AW")
# print("--------------------------------")
# print(tariq.view_available_subjects())
# print("--------------------------------")
# print(tariq.view_enrolled_subjects())
# tariq.drop_subject("AW")
# a = section("AW")
# print(a.section_info_student())
# b = (a.student_id_in_section())
# print(b)

# ahmad=student(id=2453089)
# print(ahmad.display_info())
# courses_db = Database("courses.db")
# ronaldo = student("ronaldo",database=True)
# tariq = student( id=2320003)
# tariq.enroll_subject("FA")
# cours=section("AA")
# print(cours.has_time_conflict("2430020"))
# tariq = student( id=2510005)
# print(tariq.display_info())
# tariq = student( id=2430020)
# print(tariq.view_available_subjects())
# sec=section("AW")
# print(sec.remaining_seats())
# print(sec.section_info_student())
# print(tariq.calculate_GPA())
# print(tariq.is_existing())
# print(tariq.display_info())
# print(float(70))
# print(tariq.drop_subject("AW"))
# print(tariq.correct_password("tariq899413"))
# print(tariq.view_available_subjects())
# tariq.enroll_subject("DG")
# tariq.drop_subject("AX")
# tariq.enroll_subject("AV")
# tariq.enroll_subject("AX")
# print(tariq.view_enrolled_subjects())
# tariq.enroll_subject("AW")
# tariq.enroll_subject("AV")
# tariq.enroll_subject("AX")
# print(tariq.view_enrolled_subjects())
# print(tariq.view_available_subjects())
# Ahmed = admin(id=78640)
# print(Ahmed.display_student_in_section("AW"))
# print(Ahmed.find_student(tariq))
# print(Ahmed.find_sections("EE250"))
# print(Ahmed.view_all_subjects("2430020"))
# tariq = student(id=2430020)
# print(tariq.is_existing())
# print(tariq.display_info())
# print(tariq.view_enrolled_subjects())
# print(tariq.transcript())

# print(tariq.all_conditions_met("BG"))
# print(ronaldo.display_info())
# section1= section("CU , CV")
# okay,mass= section1.prerequisites_met("2430020")
# print(okay)
# # s1= student(id="2404449",major="computer")
# # print(s1.display_info())
# print(mass)
from classses2 import admin, student, Database
from classses2 import admin, student, Database, instructor

# ahmed = student(id="12345")
# print(ahmed.display_info())
# print(ahmed.view_enrolled_subjects())

# print(("Aziz AA").strip())
# nn = admin("Lionel Messi", database=True)
# nn = instructor("Azoz Alqahtani", "EE250", "AW", database=True)
# bb = instructor("benzima", "EE331", "BB", database=True)
# print(bb.display_info())
# print(nn.display_info())
# users_db = Database("Users.db")

# row = users_db.execute("SELECT id,username,major FROM students WHERE id = ?", (2478624,), fetchone=True)
# student1 = student(row[1], id=row[0], major=row[2])

# calculated_gpa = student1.calculate_GPA()
# print(f"Calculated GPA for student ID {student1.Id}: {calculated_gpa}")

# messi = admin("messi",database=True)
# print(messi.display_info())
# ronaldo = student("ronaldo",major="computer")
# print(ronaldo.display_info())
# s1 = admin(Id=2430020)
# print(s1.calculate_GPA())
# print(s1.display_info())
# random = admin("azoz")
# random_admin2 = admin("ali")
# random_admin3 = admin("ali", Id=9911991199)
# random_admin4 = admin("ali")


# print(random.display_info())
# print(random_admin2.display_info())
# print(random_admin3.display_info())
# print(random_admin4.display_info())


# def connect_db():
#     return sqlite3.connect("students.db")

# def create_students_table():
#     db = sqlite3.connect("Users.db")
#     cr = db.cursor()
#     cr.execute("""
#     CREATE TABLE IF NOT EXISTS students (
#         username TEXT,
#         password TEXT,
#         email TEXT,
#         status TEXT,
#         Id INTEGER PRIMARY KEY,
#         GPA REAL
#     )
#     """)
#     db.commit()
#     db.close()

# def create_admin_table():
#     db = sqlite3.connect("Users.db")
#     cr = db.cursor()
#     cr.execute("""
#     CREATE TABLE IF NOT EXISTS admins (
#                username TEXT,
#                password TEXT,
#                email TEXT,
#                status TEXT
#                )
#                """)

# def insert_student(user):
#     db = connect_db()
#     cr = db.cursor()
#     cr.execute("""
#     INSERT INTO students (username, password, email, status, Id)
#     VALUES (?, ?, ?, ?, ?)
#     """, (user.username, user.password, user.email, user.status, user.Id))
#     db.commit()
#     db.close()
#     print(f"suc Added {user.username} to database.")

# def get_all_students():
#     db = connect_db()
#     cr = db.cursor()
#     cr.execute("SELECT * FROM students")
#     rows = cr.fetchall()
#     db.close()
#     return rows
# create_admin_table()
# create_students_table()
# from classes import user
# bb = "ali ahmed"
# z = bb.find(" ")
# print(z)
# new = ""
# for i in range(z):
#     new += bb[i]
# print(new)

# Create table if not already exists


# Get user input
# data = input("Enter username, password, email, status, Id, GPA separated by commas: ").split(",")
# data = [x.strip() for x in data]

# # Create User object
# username, password, email, status, Id, = data
# student = user(username, password, email, status, int(Id))

# Add student to database
# create_students_table()
# insert_student(student)

# Display all students
# print("\nAll students in database:")
# for row in get_all_students():
#     print(row)

db = sqlite3.connect("Users.db")
cr = db.cursor()
# cr.execute("DELETE FROM admins")
# computer = cr.fetchall()
# print(computer)
# cr.execute("DROP TABLE IF EXISTS instructors")
# cr.execute("CREATE TABLE IF NOT EXISTS instructors (id INTEGER,username TEXT, password TEXT, email TEXT, status TEXT, course_code TEXT, section TEXT)")
# power = cr.fetchall()
# print(power)
# cr.execute("SELECT course_code,terms FROM communication")
# communication = cr.fetchall()
# print(communication)
# cr.execute("SELECT course_code,terms FROM biomedical")
# biomedical = cr.fetchall()
# print(biomedical)



# times = [item[0].split(',')[1].strip() for item in azoz]
db.commit()
db.close()
# print(times)
# print(1 // 26)
# print(1 % 26)
# i = "2430020"
# db = sqlite3.connect("Users.db")
# cr = db.cursor()
# cr.execute(f"SELECT course FROM grades WHERE student_id = {i}")
# courses_taken = cr.fetchall()
# courses_taken = [i[0] for i in courses_taken]
# db.commit()
# db.close()
# print(courses_taken)

# db = sqlite3.connect("courses.db")
# cr = db.cursor()
# terms_taken=[]
# for i in range(len(courses_taken)):
#     cr.execute(f"SELECT terms FROM power WHERE course_code = ?", (courses_taken[i],))
#     terms_taken.append(cr.fetchall())
# b = max(terms_taken)
# b = b[0][0]
# print(b)
# cr.execute(f"SELECT capacity FROM power WHERE terms = ?", (b,))
# row = cr.fetchall()
# db.commit()
# db.close()
# print(b)
# print(row)

# tt = [1,0,50,33,44]
# for p in tt:
#     if p > 0:
#         print("class available")
#     else:
#         print("class is full")        
#
# db = sqlite3.connect("test.db")
# cr = db.cursor()
# cr.execute("CREATE TABLE IF NOT EXISTS test (id TEXT PRIMARY KEY, username TEXT, email TEXT, major TEXT, password TEXT, current_term INTEGER)") 
# db.commit()
# db.close()
# class signup(user):
#     def __init__(self, username, password, email=None, id=None):
#         super().__init__(username, password, email, id)
#         if self.id is None:
#             self.id = self.generate_unique_id()
#         if self.email is None:
#             self.email = self.generate_email()
#     def register(self):
#         self.email = self.generate_email()
#         self.hashed = bcrypt.hashpw(self.password.encode(), bcrypt.gensalt()).decode()
#         db = sqlite3.connect("test.db")
#         cr = db.cursor()
#         cr.execute(
#         "INSERT INTO test (id, username, email, password) VALUES (?, ?, ?, ?)",
#         (self.id, self.username, self.email, self.hashed))
#         db.commit()
#         db.close()  
#     def checking(self):
#         print("ID I'm searching for:", self.id)
#         checker = input("Enter your password: ")
#         new_hashed = bcrypt.hashpw(checker.encode(), bcrypt.gensalt()).decode()
#         print(checker)
#         print(new_hashed)
#         print(self.hashed)
#         if bcrypt.checkpw(checker.encode(), self.hashed.encode()):
#             print("Same")
#         else:
#             print("Not same")
# test_obj = signup(username="Abdulaziz aa", password="mypass")
# test_obj.register()
# # a = input("Enter username: ")
# # b = input("Enter password: ")
# # test_obj2 = signup(username=a, password=b)
# # test_obj2.register()
# test_obj.checking()
# m = "abc123"
# print(list(m))
# t = "A"
# print(t.isupper())

def is_special(ch): # this is for password ensuring it has a special character
    return not ch.isalnum()

def has_sequence(chars, length=3):
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


def signup(FN, LN, Npassword): # FN = first name , LN = last name
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
    s = student(id = stu_id, username=Tusername,email= f"{FN}{stu_id}@stu.kau.edu.sa", password=Npassword, major="preparatory engineering", database=True)

    db.commit()
    db.close()
        
# a = input()
# b = input()
# c = input()
# signup(a,b,c)

