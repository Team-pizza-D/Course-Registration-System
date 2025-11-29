import sqlite3
from classses2 import admin, student,section,subject,instructor,Database


# tariq = student( id=2430020)
# print("--------------------------------")
# print(tariq.view_available_subjects())
# print("--------------------------------")
# print(tariq.view_enrolled_subjects())
# print("--------------------------------")
# tariq.enroll_subject("AW")
# print("--------------------------------")
# print(tariq.view_available_subjects())
# print("--------------------------------")
# print(tariq.view_enrolled_subjects())
# tariq.drop_subject("AW")


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
tariq = student( id=2430020)
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
