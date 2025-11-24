import sqlite3
<<<<<<< HEAD
from classses2 import admin, student,section,subject 

section1= section("CU , CV")
okay,mass= section1.prerequisites_met("2430020")
print(okay)
# s1= student(id="2404449",major="computer")
# print(s1.display_info())
print(mass)
=======
from classses2 import admin, student, Database
# users_db = Database("Users.db")

# row = users_db.execute("SELECT id,username,major FROM students WHERE id = ?", (2478624,), fetchone=True)
# student1 = student(row[1], id=row[0], major=row[2])

# calculated_gpa = student1.calculate_GPA()
# print(f"Calculated GPA for student ID {student1.Id}: {calculated_gpa}")

# messi = admin("messi",database=True)
# print(messi.display_info())
# ronaldo = student("ronaldo",major="computer")
# print(ronaldo.display_info())
s1 = admin(Id=2430020)
# print(s1.calculate_GPA())
print(s1.display_info())
>>>>>>> 03ec990e3f05d5e034968403dc798298da64f403
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

# db = sqlite3.connect("courses.db")
# cr = db.cursor()
# cr.execute("SELECT course_code,terms FROM computer")
# computer = cr.fetchall()
# print(computer)
# cr.execute("SELECT course_code,terms FROM power")
# power = cr.fetchall()
# print(power)
# cr.execute("SELECT course_code,terms FROM communication")
# communication = cr.fetchall()
# print(communication)
# cr.execute("SELECT course_code,terms FROM biomedical")
# biomedical = cr.fetchall()
# print(biomedical)



# times = [item[0].split(',')[1].strip() for item in azoz]
# db.commit()
# db.close()
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
